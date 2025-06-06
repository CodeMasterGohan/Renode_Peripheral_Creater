//
// Copyright (c) 2010-2024 Antmicro
//
// This file is licensed under the MIT License.
// Full license text is available in 'licenses/MIT.txt'.
//

using System;
using System.Collections.Generic;
using Antmicro.Renode.Core;
using Antmicro.Renode.Core.Structure.Registers;
using Antmicro.Renode.Logging;
using Antmicro.Renode.Peripherals.Bus;
using Antmicro.Renode.Utilities;

namespace Antmicro.Renode.Peripherals.GPIOPort
{
    public class ExampleGPIO : BasicDoubleWordPeripheral, INumberedGPIOOutput
    {
        public ExampleGPIO(IMachine machine) : base(machine)
        {
            // Initialize GPIO connections
            Connections = new Dictionary<int, IGPIO>();
            for(var i = 0; i < NumberOfPins; i++)
            {
                Connections[i] = new GPIO();
            }
            
            // Initialize internal state
            pinDirections = new bool[NumberOfPins];
            pinValues = new bool[NumberOfPins];
            interruptEnable = new bool[NumberOfPins];
            interruptStatus = new bool[NumberOfPins];
            
            // Define registers
            DefineRegisters();
            
            // Create IRQ
            IRQ = new GPIO();
            
            Reset();
        }

        public override void Reset()
        {
            base.Reset();
            
            // Reset all pins to input mode with low value
            for(var i = 0; i < NumberOfPins; i++)
            {
                pinDirections[i] = false; // Input
                pinValues[i] = false;      // Low
                interruptEnable[i] = false;
                interruptStatus[i] = false;
                
                // Update external connections
                Connections[i].Set(false);
            }
            
            UpdateInterrupts();
        }

        public IReadOnlyDictionary<int, IGPIO> Connections { get; }
        
        public GPIO IRQ { get; }

        private void DefineRegisters()
        {
            Registers.Data.Define(this)
                .WithValueField(0, 32, name: "DATA",
                    valueProviderCallback: _ => GetDataRegisterValue(),
                    writeCallback: (_, value) => SetDataRegisterValue(value))
                .WithWriteCallback((_, __) => UpdateInterrupts());

            Registers.Direction.Define(this)
                .WithValueField(0, 32, name: "DIR",
                    valueProviderCallback: _ => GetDirectionRegisterValue(),
                    writeCallback: (_, value) => SetDirectionRegisterValue(value));

            Registers.InterruptEnable.Define(this)
                .WithValueField(0, 32, name: "IE",
                    valueProviderCallback: _ => GetInterruptEnableValue(),
                    writeCallback: (_, value) => SetInterruptEnableValue(value))
                .WithWriteCallback((_, __) => UpdateInterrupts());

            Registers.InterruptStatus.Define(this)
                .WithValueField(0, 32, name: "IS",
                    valueProviderCallback: _ => GetInterruptStatusValue(),
                    writeCallback: (_, value) => ClearInterruptStatus(value))
                .WithWriteCallback((_, __) => UpdateInterrupts());

            Registers.InterruptType.Define(this)
                .WithValueField(0, 32, name: "IT",
                    valueProviderCallback: _ => (uint)interruptType,
                    writeCallback: (_, value) => interruptType = value);

            Registers.InterruptPolarity.Define(this)
                .WithValueField(0, 32, name: "IP",
                    valueProviderCallback: _ => (uint)interruptPolarity,
                    writeCallback: (_, value) => interruptPolarity = value);

            Registers.InterruptEdge.Define(this)
                .WithValueField(0, 32, name: "EDGE",
                    valueProviderCallback: _ => (uint)interruptEdge,
                    writeCallback: (_, value) => interruptEdge = value);
        }

        private uint GetDataRegisterValue()
        {
            uint value = 0;
            for(var i = 0; i < NumberOfPins; i++)
            {
                if(pinDirections[i]) // Output
                {
                    if(pinValues[i])
                    {
                        value |= (1u << i);
                    }
                }
                else // Input
                {
                    if(Connections[i].IsSet)
                    {
                        value |= (1u << i);
                    }
                }
            }
            return value;
        }

        private void SetDataRegisterValue(uint value)
        {
            for(var i = 0; i < NumberOfPins; i++)
            {
                if(pinDirections[i]) // Only affect output pins
                {
                    var newValue = (value & (1u << i)) != 0;
                    if(pinValues[i] != newValue)
                    {
                        pinValues[i] = newValue;
                        Connections[i].Set(newValue);
                        this.Log(LogLevel.Noisy, "Pin {0} set to {1}", i, newValue);
                    }
                }
            }
        }

        private uint GetDirectionRegisterValue()
        {
            uint value = 0;
            for(var i = 0; i < NumberOfPins; i++)
            {
                if(pinDirections[i])
                {
                    value |= (1u << i);
                }
            }
            return value;
        }

        private void SetDirectionRegisterValue(uint value)
        {
            for(var i = 0; i < NumberOfPins; i++)
            {
                var newDirection = (value & (1u << i)) != 0;
                if(pinDirections[i] != newDirection)
                {
                    pinDirections[i] = newDirection;
                    this.Log(LogLevel.Noisy, "Pin {0} direction set to {1}", i, 
                        newDirection ? "output" : "input");
                    
                    // If changing to output, drive the pin with current value
                    if(newDirection)
                    {
                        Connections[i].Set(pinValues[i]);
                    }
                }
            }
        }

        private uint GetInterruptEnableValue()
        {
            uint value = 0;
            for(var i = 0; i < NumberOfPins; i++)
            {
                if(interruptEnable[i])
                {
                    value |= (1u << i);
                }
            }
            return value;
        }

        private void SetInterruptEnableValue(uint value)
        {
            for(var i = 0; i < NumberOfPins; i++)
            {
                interruptEnable[i] = (value & (1u << i)) != 0;
            }
        }

        private uint GetInterruptStatusValue()
        {
            uint value = 0;
            for(var i = 0; i < NumberOfPins; i++)
            {
                if(interruptStatus[i])
                {
                    value |= (1u << i);
                }
            }
            return value;
        }

        private void ClearInterruptStatus(uint value)
        {
            // Write-1-to-clear
            for(var i = 0; i < NumberOfPins; i++)
            {
                if((value & (1u << i)) != 0)
                {
                    interruptStatus[i] = false;
                }
            }
        }

        private void UpdateInterrupts()
        {
            var shouldTrigger = false;
            for(var i = 0; i < NumberOfPins; i++)
            {
                if(interruptEnable[i] && interruptStatus[i])
                {
                    shouldTrigger = true;
                    break;
                }
            }
            
            IRQ.Set(shouldTrigger);
        }

        public void OnGPIO(int number, bool value)
        {
            if(number >= NumberOfPins)
            {
                this.Log(LogLevel.Warning, "GPIO {0} is out of range", number);
                return;
            }

            if(pinDirections[number]) // Output pin, ignore external changes
            {
                return;
            }

            var previousValue = Connections[number].IsSet;
            
            // Check if we should generate an interrupt
            if(interruptEnable[number] && ShouldTriggerInterrupt(number, previousValue, value))
            {
                interruptStatus[number] = true;
                this.Log(LogLevel.Noisy, "Interrupt triggered on pin {0}", number);
                UpdateInterrupts();
            }
        }

        private bool ShouldTriggerInterrupt(int pin, bool oldValue, bool newValue)
        {
            if(oldValue == newValue)
            {
                return false;
            }

            var isEdge = (interruptType & (1u << pin)) != 0;
            var polarity = (interruptPolarity & (1u << pin)) != 0;
            var edgeType = (interruptEdge & (1u << pin)) != 0;

            if(isEdge)
            {
                // Edge triggered
                if(edgeType) // Both edges
                {
                    return true;
                }
                else if(polarity) // Falling edge
                {
                    return oldValue && !newValue;
                }
                else // Rising edge
                {
                    return !oldValue && newValue;
                }
            }
            else
            {
                // Level triggered
                return newValue == polarity;
            }
        }

        private enum Registers : long
        {
            Data = 0x00,
            Direction = 0x04,
            InterruptEnable = 0x08,
            InterruptStatus = 0x0C,
            InterruptType = 0x10,      // 0: level, 1: edge
            InterruptPolarity = 0x14,   // 0: low/rising, 1: high/falling
            InterruptEdge = 0x18,       // 0: single edge, 1: both edges
        }

        private readonly bool[] pinDirections;
        private readonly bool[] pinValues;
        private readonly bool[] interruptEnable;
        private readonly bool[] interruptStatus;
        private uint interruptType;
        private uint interruptPolarity;
        private uint interruptEdge;

        private const int NumberOfPins = 32;
    }
}