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
using Antmicro.Renode.Peripherals.UART;
using Antmicro.Renode.Utilities.Collections;

namespace Antmicro.Renode.Peripherals.UART
{
    public class ExampleUART : UARTBase, IDoubleWordPeripheral, IKnownSize
    {
        public ExampleUART(IMachine machine) : base(machine)
        {
            IRQ = new GPIO();
            
            // Initialize FIFOs
            txFifo = new CircularBuffer<byte>(FifoSize);
            rxFifo = new CircularBuffer<byte>(FifoSize);
            
            DefineRegisters();
            Reset();
        }

        public override void Reset()
        {
            base.Reset();
            
            // Clear FIFOs
            txFifo.Clear();
            rxFifo.Clear();
            
            // Reset configuration
            baudRateDivisor = DefaultBaudRateDivisor;
            dataBits = 8;
            stopBits = StopBits.One;
            parityType = Parity.None;
            fifoEnabled = false;
            rxFifoTriggerLevel = 1;
            txFifoTriggerLevel = 1;
            
            // Reset interrupts
            rxInterruptEnable = false;
            txInterruptEnable = false;
            rxTimeoutInterruptEnable = false;
            modemStatusInterruptEnable = false;
            
            // Reset status
            overrunError = false;
            parityError = false;
            framingError = false;
            breakDetected = false;
            
            UpdateInterrupts();
        }

        public uint ReadDoubleWord(long offset)
        {
            return RegistersCollection.Read(offset);
        }

        public void WriteDoubleWord(long offset, uint value)
        {
            RegistersCollection.Write(offset, value);
        }

        public GPIO IRQ { get; }
        
        public long Size => 0x100;

        // UARTBase implementation
        protected override void CharWritten()
        {
            // This is called by UARTBase when a character is to be transmitted
            // In our case, we've already handled it in the data register write
        }

        protected override void QueueEmptied()
        {
            // Called when the transmit queue is empty
            UpdateInterrupts();
        }

        public override void WriteChar(byte value)
        {
            // Called when receiving a character from external source
            lock(rxFifo)
            {
                if(rxFifo.Count >= FifoSize)
                {
                    overrunError = true;
                    this.Log(LogLevel.Warning, "RX FIFO overrun");
                }
                else
                {
                    rxFifo.Enqueue(value);
                    this.Log(LogLevel.Noisy, "Received character: 0x{0:X2} '{1}'", 
                        value, (char)value);
                }
            }
            
            UpdateInterrupts();
        }

        private void DefineRegisters()
        {
            Registers.Data.Define(this)
                .WithValueField(0, 8, name: "DATA",
                    valueProviderCallback: _ => ReadDataRegister(),
                    writeCallback: (_, value) => WriteDataRegister((byte)value))
                .WithReservedBits(8, 24);

            Registers.Status.Define(this)
                .WithFlag(0, FieldMode.Read, name: "DR",
                    valueProviderCallback: _ => rxFifo.Count > 0)
                .WithFlag(1, FieldMode.Read, name: "OE",
                    valueProviderCallback: _ => overrunError)
                .WithFlag(2, FieldMode.Read, name: "PE", 
                    valueProviderCallback: _ => parityError)
                .WithFlag(3, FieldMode.Read, name: "FE",
                    valueProviderCallback: _ => framingError)
                .WithFlag(4, FieldMode.Read, name: "BI",
                    valueProviderCallback: _ => breakDetected)
                .WithFlag(5, FieldMode.Read, name: "THRE",
                    valueProviderCallback: _ => txFifo.Count < FifoSize)
                .WithFlag(6, FieldMode.Read, name: "TEMT",
                    valueProviderCallback: _ => txFifo.Count == 0)
                .WithFlag(7, FieldMode.Read, name: "RX_FIFO_ERR",
                    valueProviderCallback: _ => overrunError || parityError || framingError)
                .WithReservedBits(8, 24);

            Registers.Control.Define(this)
                .WithValueField(0, 2, name: "WLS",
                    valueProviderCallback: _ => (uint)(dataBits - 5),
                    writeCallback: (_, value) => dataBits = (int)value + 5)
                .WithFlag(2, name: "STB",
                    valueProviderCallback: _ => stopBits == StopBits.Two,
                    writeCallback: (_, value) => stopBits = value ? StopBits.Two : StopBits.One)
                .WithFlag(3, name: "PEN",
                    valueProviderCallback: _ => parityType != Parity.None,
                    writeCallback: (_, value) => 
                    {
                        if(!value) parityType = Parity.None;
                    })
                .WithFlag(4, name: "EPS",
                    valueProviderCallback: _ => parityType == Parity.Even,
                    writeCallback: (_, value) => 
                    {
                        if(parityType != Parity.None)
                            parityType = value ? Parity.Even : Parity.Odd;
                    })
                .WithFlag(6, name: "BRK",
                    writeCallback: (_, value) => 
                    {
                        if(value)
                        {
                            this.Log(LogLevel.Debug, "Break condition set");
                        }
                    })
                .WithReservedBits(7, 25);

            Registers.InterruptEnable.Define(this)
                .WithFlag(0, name: "RDAIE",
                    valueProviderCallback: _ => rxInterruptEnable,
                    writeCallback: (_, value) => 
                    {
                        rxInterruptEnable = value;
                        UpdateInterrupts();
                    })
                .WithFlag(1, name: "THREIE",
                    valueProviderCallback: _ => txInterruptEnable,
                    writeCallback: (_, value) => 
                    {
                        txInterruptEnable = value;
                        UpdateInterrupts();
                    })
                .WithFlag(2, name: "RLSIE",
                    valueProviderCallback: _ => rxLineStatusInterruptEnable,
                    writeCallback: (_, value) => 
                    {
                        rxLineStatusInterruptEnable = value;
                        UpdateInterrupts();
                    })
                .WithFlag(3, name: "MSIE",
                    valueProviderCallback: _ => modemStatusInterruptEnable,
                    writeCallback: (_, value) => 
                    {
                        modemStatusInterruptEnable = value;
                        UpdateInterrupts();
                    })
                .WithReservedBits(4, 28);

            Registers.InterruptIdentification.Define(this)
                .WithFlag(0, FieldMode.Read, name: "IP",
                    valueProviderCallback: _ => !IsInterruptPending())
                .WithValueField(1, 3, FieldMode.Read, name: "IID",
                    valueProviderCallback: _ => GetInterruptIdentification())
                .WithReservedBits(4, 2)
                .WithValueField(6, 2, FieldMode.Read, name: "FIFO_EN",
                    valueProviderCallback: _ => fifoEnabled ? 3u : 0u)
                .WithReservedBits(8, 24);

            Registers.FifoControl.Define(this)
                .WithFlag(0, FieldMode.Write, name: "FIFO_EN",
                    writeCallback: (_, value) => 
                    {
                        fifoEnabled = value;
                        if(!value)
                        {
                            txFifo.Clear();
                            rxFifo.Clear();
                        }
                    })
                .WithFlag(1, FieldMode.Write, name: "RX_FIFO_RST",
                    writeCallback: (_, value) => 
                    {
                        if(value) rxFifo.Clear();
                    })
                .WithFlag(2, FieldMode.Write, name: "TX_FIFO_RST",
                    writeCallback: (_, value) => 
                    {
                        if(value) txFifo.Clear();
                    })
                .WithValueField(6, 2, name: "RX_TRIGGER",
                    writeCallback: (_, value) => 
                    {
                        rxFifoTriggerLevel = GetTriggerLevel(value);
                    })
                .WithReservedBits(8, 24);

            Registers.BaudRateDivisorLow.Define(this)
                .WithValueField(0, 8, name: "DLL",
                    valueProviderCallback: _ => (uint)(baudRateDivisor & 0xFF),
                    writeCallback: (_, value) => 
                    {
                        baudRateDivisor = (baudRateDivisor & 0xFF00) | value;
                        UpdateBaudRate();
                    })
                .WithReservedBits(8, 24);

            Registers.BaudRateDivisorHigh.Define(this)
                .WithValueField(0, 8, name: "DLH",
                    valueProviderCallback: _ => (uint)((baudRateDivisor >> 8) & 0xFF),
                    writeCallback: (_, value) => 
                    {
                        baudRateDivisor = (baudRateDivisor & 0x00FF) | (value << 8);
                        UpdateBaudRate();
                    })
                .WithReservedBits(8, 24);
        }

        private byte ReadDataRegister()
        {
            lock(rxFifo)
            {
                if(rxFifo.Count > 0)
                {
                    var data = rxFifo.Dequeue();
                    
                    // Clear errors on read
                    overrunError = false;
                    parityError = false;
                    framingError = false;
                    
                    UpdateInterrupts();
                    return data;
                }
            }
            
            this.Log(LogLevel.Warning, "Reading from empty RX FIFO");
            return 0;
        }

        private void WriteDataRegister(byte value)
        {
            lock(txFifo)
            {
                if(txFifo.Count < FifoSize)
                {
                    txFifo.Enqueue(value);
                    
                    // Transmit immediately in simulation
                    TransmitData();
                }
                else
                {
                    this.Log(LogLevel.Warning, "TX FIFO full, dropping character");
                }
            }
            
            UpdateInterrupts();
        }

        private void TransmitData()
        {
            lock(txFifo)
            {
                while(txFifo.Count > 0)
                {
                    var data = txFifo.Dequeue();
                    TransmitCharacter(data);
                    
                    this.Log(LogLevel.Noisy, "Transmitted character: 0x{0:X2} '{1}'", 
                        data, (char)data);
                }
            }
        }

        private void UpdateBaudRate()
        {
            if(baudRateDivisor == 0)
            {
                this.Log(LogLevel.Warning, "Invalid baud rate divisor: 0");
                return;
            }
            
            var baudRate = UartClockFrequency / (16 * baudRateDivisor);
            this.Log(LogLevel.Info, "Baud rate set to {0} (divisor: {1})", 
                baudRate, baudRateDivisor);
        }

        private int GetTriggerLevel(uint value)
        {
            switch(value)
            {
                case 0: return 1;
                case 1: return 4;
                case 2: return 8;
                case 3: return 14;
                default: return 1;
            }
        }

        private bool IsInterruptPending()
        {
            return (rxInterruptEnable && rxFifo.Count >= rxFifoTriggerLevel) ||
                   (txInterruptEnable && txFifo.Count <= txFifoTriggerLevel) ||
                   (rxLineStatusInterruptEnable && (overrunError || parityError || framingError)) ||
                   (modemStatusInterruptEnable && false); // Modem status not implemented
        }

        private uint GetInterruptIdentification()
        {
            // Priority order: RX Line Status, RX Data, TX Empty, Modem Status
            if(rxLineStatusInterruptEnable && (overrunError || parityError || framingError))
            {
                return 0x6; // Receiver line status
            }
            else if(rxInterruptEnable && rxFifo.Count >= rxFifoTriggerLevel)
            {
                return 0x4; // Received data available
            }
            else if(rxTimeoutInterruptEnable && rxFifo.Count > 0)
            {
                return 0xC; // Character timeout
            }
            else if(txInterruptEnable && txFifo.Count <= txFifoTriggerLevel)
            {
                return 0x2; // Transmitter holding register empty
            }
            else if(modemStatusInterruptEnable)
            {
                return 0x0; // Modem status
            }
            
            return 0x1; // No interrupt pending
        }

        private void UpdateInterrupts()
        {
            var interrupt = IsInterruptPending();
            
            if(interrupt != IRQ.IsSet)
            {
                this.Log(LogLevel.Noisy, "IRQ {0}", interrupt ? "set" : "cleared");
                IRQ.Set(interrupt);
            }
        }

        private enum Registers : long
        {
            Data = 0x00,                    // RBR/THR
            InterruptEnable = 0x04,         // IER
            InterruptIdentification = 0x08, // IIR
            FifoControl = 0x08,            // FCR (write only, same as IIR)
            Control = 0x0C,                // LCR
            ModemControl = 0x10,           // MCR
            Status = 0x14,                 // LSR
            ModemStatus = 0x18,            // MSR
            Scratch = 0x1C,                // SCR
            BaudRateDivisorLow = 0x00,     // DLL (when DLAB=1)
            BaudRateDivisorHigh = 0x04,    // DLH (when DLAB=1)
        }

        private readonly CircularBuffer<byte> txFifo;
        private readonly CircularBuffer<byte> rxFifo;
        
        // Configuration
        private uint baudRateDivisor;
        private int dataBits;
        private StopBits stopBits;
        private Parity parityType;
        private bool fifoEnabled;
        private int rxFifoTriggerLevel;
        private int txFifoTriggerLevel;
        
        // Interrupt enables
        private bool rxInterruptEnable;
        private bool txInterruptEnable;
        private bool rxLineStatusInterruptEnable;
        private bool rxTimeoutInterruptEnable;
        private bool modemStatusInterruptEnable;
        
        // Status flags
        private bool overrunError;
        private bool parityError;
        private bool framingError;
        private bool breakDetected;
        
        private const int FifoSize = 16;
        private const uint DefaultBaudRateDivisor = 1; // For 115200 baud with 1.8432 MHz clock
        private const uint UartClockFrequency = 1843200; // 1.8432 MHz
    }
}