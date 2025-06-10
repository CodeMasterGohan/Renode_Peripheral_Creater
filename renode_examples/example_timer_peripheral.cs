//
// Copyright (c) 2010-2024 Antmicro
//
// This file is licensed under the MIT License.
// Full license text is available in 'licenses/MIT.txt'.
//

using System;
using Antmicro.Renode.Core;
using Antmicro.Renode.Core.Structure.Registers;
using Antmicro.Renode.Logging;
using Antmicro.Renode.Peripherals.Bus;
using Antmicro.Renode.Peripherals.Timers;
using Antmicro.Renode.Time;
using Antmicro.Renode.Utilities;

namespace Antmicro.Renode.Peripherals.Timers
{
    public class ExampleTimer : BasicDoubleWordPeripheral, IKnownSize
    {
        public ExampleTimer(IMachine machine, long frequency) : base(machine)
        {
            IRQ = new GPIO();
            
            // Create the internal timer
            internalTimer = new LimitTimer(machine.ClockSource, frequency, this, "timer",
                limit: DefaultTimerLimit,
                direction: Direction.Ascending,
                enabled: false,
                eventEnabled: true);
            
            internalTimer.LimitReached += OnLimitReached;
            
            // Initialize compare channels
            compareValues = new uint[NumberOfChannels];
            compareInterruptEnable = new bool[NumberOfChannels];
            compareInterruptStatus = new bool[NumberOfChannels];
            CompareIRQs = new GPIO[NumberOfChannels];
            for(var i = 0; i < NumberOfChannels; i++)
            {
                CompareIRQs[i] = new GPIO();
            }
            
            DefineRegisters();
            Reset();
        }

        public override void Reset()
        {
            base.Reset();
            
            internalTimer.Reset();
            prescaler = 1;
            
            for(var i = 0; i < NumberOfChannels; i++)
            {
                compareValues[i] = 0;
                compareInterruptEnable[i] = false;
                compareInterruptStatus[i] = false;
                CompareIRQs[i].Set(false);
            }
            
            overflowInterruptEnable = false;
            overflowInterruptStatus = false;
            
            UpdateInterrupts();
        }

        public GPIO IRQ { get; }
        public GPIO[] CompareIRQs { get; }
        
        public long Size => 0x100;

        private void DefineRegisters()
        {
            Registers.Control.Define(this)
                .WithFlag(0, name: "EN",
                    valueProviderCallback: _ => internalTimer.Enabled,
                    writeCallback: (_, value) => 
                    {
                        if(value && !internalTimer.Enabled)
                        {
                            this.Log(LogLevel.Debug, "Timer enabled");
                        }
                        else if(!value && internalTimer.Enabled)
                        {
                            this.Log(LogLevel.Debug, "Timer disabled");
                        }
                        internalTimer.Enabled = value;
                    })
                .WithFlag(1, name: "MODE",
                    valueProviderCallback: _ => timerMode == TimerMode.Periodic,
                    writeCallback: (_, value) => 
                    {
                        timerMode = value ? TimerMode.Periodic : TimerMode.OneShot;
                        internalTimer.Mode = value ? WorkMode.Periodic : WorkMode.OneShot;
                    })
                .WithFlag(2, name: "INT_EN",
                    valueProviderCallback: _ => overflowInterruptEnable,
                    writeCallback: (_, value) => 
                    {
                        overflowInterruptEnable = value;
                        UpdateInterrupts();
                    })
                .WithValueField(8, 8, name: "PRESCALER",
                    valueProviderCallback: _ => (uint)(prescaler - 1),
                    writeCallback: (_, value) => 
                    {
                        prescaler = (int)value + 1;
                        UpdateTimerFrequency();
                    })
                .WithReservedBits(16, 16);

            Registers.Counter.Define(this)
                .WithValueField(0, 32, FieldMode.Read, name: "COUNT",
                    valueProviderCallback: _ => (uint)internalTimer.Value);

            Registers.Period.Define(this)
                .WithValueField(0, 32, name: "PERIOD",
                    valueProviderCallback: _ => (uint)internalTimer.Limit,
                    writeCallback: (_, value) => 
                    {
                        internalTimer.Limit = value;
                        this.Log(LogLevel.Debug, "Period set to 0x{0:X}", value);
                    });

            Registers.Status.Define(this)
                .WithFlag(0, name: "OVF",
                    valueProviderCallback: _ => overflowInterruptStatus,
                    writeCallback: (_, value) => 
                    {
                        if(value) // Write-1-to-clear
                        {
                            overflowInterruptStatus = false;
                            UpdateInterrupts();
                        }
                    })
                .WithReservedBits(1, 31);

            // Define compare registers for each channel
            for(var channel = 0; channel < NumberOfChannels; channel++)
            {
                var ch = channel; // Capture for closure
                
                DefineRegister((long)(Registers.Compare0 + ch * 4))
                    .WithValueField(0, 32, name: $"COMPARE{ch}",
                        valueProviderCallback: _ => compareValues[ch],
                        writeCallback: (_, value) => 
                        {
                            compareValues[ch] = (uint)value;
                            CheckCompareMatch(ch);
                        });
                
                DefineRegister((long)(Registers.CompareControl0 + ch * 4))
                    .WithFlag(0, name: $"CMP{ch}_EN",
                        valueProviderCallback: _ => compareInterruptEnable[ch],
                        writeCallback: (_, value) => 
                        {
                            compareInterruptEnable[ch] = value;
                            UpdateInterrupts();
                        })
                    .WithFlag(1, name: $"CMP{ch}_STATUS",
                        valueProviderCallback: _ => compareInterruptStatus[ch],
                        writeCallback: (_, value) => 
                        {
                            if(value) // Write-1-to-clear
                            {
                                compareInterruptStatus[ch] = false;
                                UpdateInterrupts();
                            }
                        })
                    .WithReservedBits(2, 30);
            }

            // PWM registers
            Registers.PWMControl.Define(this)
                .WithFlag(0, name: "PWM_EN",
                    valueProviderCallback: _ => pwmEnabled,
                    writeCallback: (_, value) => pwmEnabled = value)
                .WithValueField(8, 2, name: "PWM_MODE",
                    valueProviderCallback: _ => (uint)pwmMode,
                    writeCallback: (_, value) => pwmMode = (PWMMode)value)
                .WithReservedBits(10, 22);
        }

        private void OnLimitReached()
        {
            this.Log(LogLevel.Noisy, "Timer limit reached");
            
            if(overflowInterruptEnable)
            {
                overflowInterruptStatus = true;
                UpdateInterrupts();
            }
            
            // Check all compare values when timer overflows
            for(var i = 0; i < NumberOfChannels; i++)
            {
                CheckCompareMatch(i);
            }
        }

        private void CheckCompareMatch(int channel)
        {
            if(!internalTimer.Enabled)
            {
                return;
            }
            
            var currentValue = (uint)internalTimer.Value;
            var compareValue = compareValues[channel];
            
            // Simple comparison - in real implementation might need edge detection
            if(currentValue == compareValue)
            {
                this.Log(LogLevel.Noisy, "Compare match on channel {0}", channel);
                
                if(compareInterruptEnable[channel])
                {
                    compareInterruptStatus[channel] = true;
                    UpdateInterrupts();
                }
                
                // Handle PWM if enabled
                if(pwmEnabled && channel < 2) // Assuming first 2 channels support PWM
                {
                    HandlePWMCompareMatch(channel);
                }
            }
        }

        private void HandlePWMCompareMatch(int channel)
        {
            // Simplified PWM handling
            switch(pwmMode)
            {
                case PWMMode.EdgeAligned:
                    // Toggle output on compare match
                    // In real implementation, would drive GPIO pins
                    this.Log(LogLevel.Noisy, "PWM output toggle on channel {0}", channel);
                    break;
                    
                case PWMMode.CenterAligned:
                    // More complex PWM generation
                    break;
            }
        }

        private void UpdateTimerFrequency()
        {
            var baseFrequency = internalTimer.Frequency;
            var effectiveFrequency = baseFrequency / prescaler;
            
            // In a real implementation, we'd update the timer's frequency
            this.Log(LogLevel.Debug, "Timer frequency updated: base={0}Hz, prescaler={1}, effective={2}Hz",
                baseFrequency, prescaler, effectiveFrequency);
        }

        private void UpdateInterrupts()
        {
            // Main overflow interrupt
            var mainInterrupt = overflowInterruptEnable && overflowInterruptStatus;
            
            // Check compare interrupts
            for(var i = 0; i < NumberOfChannels; i++)
            {
                var compareInterrupt = compareInterruptEnable[i] && compareInterruptStatus[i];
                CompareIRQs[i].Set(compareInterrupt);
                mainInterrupt |= compareInterrupt;
            }
            
            IRQ.Set(mainInterrupt);
        }

        private enum Registers : long
        {
            Control = 0x00,
            Counter = 0x04,
            Period = 0x08,
            Status = 0x0C,
            
            Compare0 = 0x10,
            Compare1 = 0x14,
            Compare2 = 0x18,
            Compare3 = 0x1C,
            
            CompareControl0 = 0x20,
            CompareControl1 = 0x24,
            CompareControl2 = 0x28,
            CompareControl3 = 0x2C,
            
            PWMControl = 0x30,
        }

        private enum TimerMode
        {
            OneShot,
            Periodic
        }

        private enum PWMMode
        {
            Disabled = 0,
            EdgeAligned = 1,
            CenterAligned = 2,
        }

        private readonly LimitTimer internalTimer;
        private readonly uint[] compareValues;
        private readonly bool[] compareInterruptEnable;
        private readonly bool[] compareInterruptStatus;
        
        private TimerMode timerMode;
        private int prescaler;
        private bool overflowInterruptEnable;
        private bool overflowInterruptStatus;
        private bool pwmEnabled;
        private PWMMode pwmMode;
        
        private const int NumberOfChannels = 4;
        private const uint DefaultTimerLimit = 0xFFFFFFFF;
    }
}