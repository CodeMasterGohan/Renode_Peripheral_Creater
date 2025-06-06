"""
Renode Templates Module

This module provides comprehensive templates for generating Renode peripherals,
including base classes, register implementations, common patterns, and
peripheral-specific templates following Renode's coding conventions.
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import textwrap


class RegisterAccess(Enum):
    """Register access types"""
    READ_WRITE = "ReadWrite"
    READ_ONLY = "ReadOnly"
    WRITE_ONLY = "WriteOnly"
    WRITE_ONE_TO_CLEAR = "WriteOneToClear"


class PeripheralSize(Enum):
    """Peripheral register size types"""
    DOUBLE_WORD = "IDoubleWordPeripheral"  # 32-bit
    WORD = "IWordPeripheral"  # 16-bit
    BYTE = "IBytePeripheral"  # 8-bit


@dataclass
class RegisterField:
    """Represents a bit field within a register"""
    name: str
    start_bit: int
    end_bit: int
    description: str
    access: RegisterAccess = RegisterAccess.READ_WRITE


@dataclass
class RegisterDefinition:
    """Represents a register definition"""
    name: str
    offset: int
    description: str
    access: RegisterAccess = RegisterAccess.READ_WRITE
    reset_value: int = 0
    fields: List[RegisterField] = None
    has_side_effects: bool = False


class RenodeTemplates:
    """
    Main class providing Renode peripheral templates and code generation helpers.
    
    This class contains templates for:
    - Base peripheral implementations
    - Register patterns
    - Common Renode patterns
    - Peripheral-specific templates
    - Code generation utilities
    """
    
    def __init__(self):
        self.indent = "    "  # 4 spaces for C# indentation
        
    # ==================== Using Statements ====================
    
    def generate_using_statements(self, peripheral_type: str = "generic") -> str:
        """
        Generate common using statements for Renode peripherals.
        
        Args:
            peripheral_type: Type of peripheral (generic, gpio, timer, uart, etc.)
            
        Returns:
            String containing using statements
        """
        base_usings = [
            "using System;",
            "using System.Collections.Generic;",
            "using System.Linq;",
            "using Antmicro.Renode.Core;",
            "using Antmicro.Renode.Core.Structure.Registers;",
            "using Antmicro.Renode.Logging;",
            "using Antmicro.Renode.Peripherals.Bus;",
            "using Antmicro.Renode.Utilities;"
        ]
        
        peripheral_specific = {
            "gpio": ["using Antmicro.Renode.Peripherals.GPIOPort;"],
            "timer": ["using Antmicro.Renode.Peripherals.Timers;",
                     "using Antmicro.Renode.Time;"],
            "uart": ["using Antmicro.Renode.Peripherals.UART;"],
            "dma": ["using Antmicro.Renode.Peripherals.DMA;"],
            "spi": ["using Antmicro.Renode.Peripherals.SPI;"],
            "i2c": ["using Antmicro.Renode.Peripherals.I2C;"],
            "interrupt": ["using Antmicro.Renode.Peripherals.IRQControllers;"]
        }
        
        all_usings = base_usings + peripheral_specific.get(peripheral_type, [])
        return "\n".join(all_usings)
    
    # ==================== Base Peripheral Templates ====================
    
    def generate_base_peripheral(self, 
                               class_name: str,
                               namespace: str,
                               size: PeripheralSize = PeripheralSize.DOUBLE_WORD,
                               has_interrupts: bool = True,
                               has_dma: bool = False) -> str:
        """
        Generate a base peripheral class template.
        
        Args:
            class_name: Name of the peripheral class
            namespace: Namespace for the peripheral
            size: Register size (DOUBLE_WORD, WORD, or BYTE)
            has_interrupts: Whether peripheral has interrupt support
            has_dma: Whether peripheral has DMA support
            
        Returns:
            Complete peripheral class template
        """
        interfaces = [size.value, "IKnownSize"]
        if has_interrupts:
            interfaces.append("IIRQSender")
        if has_dma:
            interfaces.append("IDMAPeripheral")
            
        template = f"""namespace {namespace}
{{
    public class {class_name} : {", ".join(interfaces)}
    {{
        public {class_name}(Machine machine) : base(machine)
        {{
            IRQ = new GPIO();
            registers = new {"DoubleWord" if size == PeripheralSize.DOUBLE_WORD else "Word" if size == PeripheralSize.WORD else "Byte"}RegistersCollection(this);
            DefineRegisters();
            Reset();
        }}
        
        public override void Reset()
        {{
            registers.Reset();
            // Add custom reset logic here
        }}
        
        public {"uint" if size == PeripheralSize.DOUBLE_WORD else "ushort" if size == PeripheralSize.WORD else "byte"} ReadDoubleWord(long offset)
        {{
            return registers.Read(offset);
        }}
        
        public void WriteDoubleWord(long offset, {"uint" if size == PeripheralSize.DOUBLE_WORD else "ushort" if size == PeripheralSize.WORD else "byte"} value)
        {{
            registers.Write(offset, value);
        }}
        
        public long Size => 0x1000; // Adjust based on peripheral
        
        public GPIO IRQ {{ get; private set; }}
        
        private void DefineRegisters()
        {{
            // Register definitions go here
        }}
        
        private {"DoubleWord" if size == PeripheralSize.DOUBLE_WORD else "Word" if size == PeripheralSize.WORD else "Byte"}RegistersCollection registers;
        
        private enum Registers
        {{
            // Register offsets
        }}
    }}
}}"""
        return template
    
    # ==================== Register Implementation Patterns ====================
    
    def generate_register_definition(self, 
                                   register: RegisterDefinition,
                                   register_size: str = "DoubleWord") -> str:
        """
        Generate a register definition with fields and callbacks.
        
        Args:
            register: RegisterDefinition object
            register_size: Size of register (DoubleWord, Word, or Byte)
            
        Returns:
            Register definition code
        """
        code = f"Registers.{register.name}.Define(this, {register.reset_value:#x})\n"
        
        if register.fields:
            for field in register.fields:
                bits = f"{field.start_bit}" if field.start_bit == field.end_bit else f"{field.start_bit}, {field.end_bit}"
                
                if field.access == RegisterAccess.READ_WRITE:
                    code += f"    .WithValueField({bits}, name: \"{field.name}\")\n"
                elif field.access == RegisterAccess.READ_ONLY:
                    code += f"    .WithValueField({bits}, FieldMode.Read, name: \"{field.name}\")\n"
                elif field.access == RegisterAccess.WRITE_ONLY:
                    code += f"    .WithValueField({bits}, FieldMode.Write, name: \"{field.name}\")\n"
                elif field.access == RegisterAccess.WRITE_ONE_TO_CLEAR:
                    code += f"    .WithValueField({bits}, FieldMode.WriteOneToClear, name: \"{field.name}\")\n"
        
        if register.has_side_effects:
            code += f"    .WithWriteCallback((_, __) => Update{register.name}())\n"
            
        code = code.rstrip('\n') + ";"
        return code
    
    def generate_register_with_callback(self, 
                                      name: str,
                                      offset: int,
                                      read_callback: str = None,
                                      write_callback: str = None) -> str:
        """
        Generate a register with read/write callbacks.
        
        Args:
            name: Register name
            offset: Register offset
            read_callback: Name of read callback method
            write_callback: Name of write callback method
            
        Returns:
            Register definition with callbacks
        """
        code = f"Registers.{name}.Define(this)\n"
        
        if read_callback:
            code += f"    .WithReadCallback((_, __) => {read_callback}())\n"
        if write_callback:
            code += f"    .WithWriteCallback((_, val) => {write_callback}(val))\n"
            
        return code.rstrip('\n') + ";"
    
    def generate_register_array(self, 
                              base_name: str,
                              count: int,
                              base_offset: int,
                              stride: int = 4) -> str:
        """
        Generate an array of registers.
        
        Args:
            base_name: Base name for registers
            count: Number of registers
            base_offset: Starting offset
            stride: Offset between registers
            
        Returns:
            Register array definition code
        """
        code = f"// {base_name} register array\n"
        for i in range(count):
            offset = base_offset + (i * stride)
            code += f"{base_name}{i} = {offset:#x},\n"
        return code.rstrip(',\n')
    
    # ==================== Common Renode Patterns ====================
    
    def generate_interrupt_handling(self, irq_name: str = "IRQ") -> str:
        """
        Generate interrupt handling pattern.
        
        Args:
            irq_name: Name of the IRQ GPIO
            
        Returns:
            Interrupt handling code
        """
        return f"""private void UpdateInterrupts()
{{
    var shouldTrigger = CheckInterruptConditions();
    {irq_name}.Set(shouldTrigger);
}}

private bool CheckInterruptConditions()
{{
    // Check interrupt enable and status flags
    return interruptEnabled && interruptPending;
}}"""
    
    def generate_dma_request_pattern(self) -> str:
        """Generate DMA request handling pattern."""
        return """public int RequestDMATransfer(int channel, TransferType type, byte[] data, int count)
{
    if(!dmaEnabled || channel >= MaxDMAChannels)
    {
        return -1;
    }
    
    // Perform DMA transfer
    var transferred = PerformDMATransfer(channel, type, data, count);
    
    // Update status and trigger interrupt if needed
    UpdateDMAStatus(channel, transferred);
    
    return transferred;
}

private int PerformDMATransfer(int channel, TransferType type, byte[] data, int count)
{
    // Implement actual DMA transfer logic
    return count;
}"""
    
    def generate_timer_pattern(self) -> str:
        """Generate timer implementation pattern."""
        return """private void InitializeTimer()
{
    timer = new LimitTimer(machine.ClockSource, frequency, this, "MainTimer", 
        limit: timerPeriod,
        direction: Direction.Ascending,
        enabled: false,
        autoUpdate: true);
    
    timer.LimitReached += () =>
    {
        if(timerInterruptEnabled)
        {
            timerInterruptPending = true;
            UpdateInterrupts();
        }
        
        if(!timerOneShot)
        {
            timer.Reset();
        }
    };
}

private void UpdateTimerConfiguration()
{
    timer.Enabled = timerEnabled;
    timer.Limit = timerPeriod;
    timer.Frequency = GetTimerFrequency();
}"""
    
    def generate_fifo_implementation(self, data_type: str = "byte") -> str:
        """
        Generate FIFO buffer implementation.
        
        Args:
            data_type: Type of data stored in FIFO
            
        Returns:
            FIFO implementation code
        """
        return f"""private class Fifo<T>
{{
    public Fifo(int capacity)
    {{
        this.capacity = capacity;
        this.buffer = new Queue<T>();
    }}
    
    public bool TryEnqueue(T item)
    {{
        if(buffer.Count >= capacity)
        {{
            return false;
        }}
        
        buffer.Enqueue(item);
        return true;
    }}
    
    public bool TryDequeue(out T item)
    {{
        if(buffer.Count == 0)
        {{
            item = default(T);
            return false;
        }}
        
        item = buffer.Dequeue();
        return true;
    }}
    
    public void Clear()
    {{
        buffer.Clear();
    }}
    
    public int Count => buffer.Count;
    public bool IsFull => buffer.Count >= capacity;
    public bool IsEmpty => buffer.Count == 0;
    
    private readonly Queue<T> buffer;
    private readonly int capacity;
}}"""
    
    # ==================== Code Generation Helpers ====================
    
    def generate_property(self, 
                         name: str,
                         type: str,
                         access: str = "private",
                         has_setter: bool = True) -> str:
        """
        Generate a C# property with backing field.
        
        Args:
            name: Property name
            type: Property type
            access: Access modifier
            has_setter: Whether to include setter
            
        Returns:
            Property definition
        """
        field_name = name[0].lower() + name[1:]
        setter = " set;" if has_setter else ""
        
        return f"""{access} {type} {name} {{ get;{setter} }}"""
    
    def generate_logging_statements(self) -> str:
        """Generate common logging statement patterns."""
        return """// Logging examples
this.Log(LogLevel.Debug, "Debug message: {0}", value);
this.Log(LogLevel.Info, "Peripheral initialized");
this.Log(LogLevel.Warning, "Invalid configuration: {0}", config);
this.Log(LogLevel.Error, "Operation failed: {0}", error);
this.Log(LogLevel.Noisy, "Register {0} = 0x{1:X}", offset, value);"""
    
    def generate_exception_patterns(self) -> str:
        """Generate exception handling patterns."""
        return """// Exception patterns
if(offset >= Size)
{
    throw new ArgumentOutOfRangeException(nameof(offset), 
        $"Offset 0x{offset:X} is outside peripheral bounds");
}

if(value > MaxValue)
{
    this.Log(LogLevel.Warning, "Value {0} exceeds maximum, clamping to {1}", 
        value, MaxValue);
    value = MaxValue;
}

try
{
    // Risky operation
}
catch(Exception e)
{
    this.Log(LogLevel.Error, "Operation failed: {0}", e.Message);
    throw new RecoverableException("Peripheral operation failed", e);
}"""
    
    # ==================== Peripheral-Specific Templates ====================
    
    def generate_gpio_controller(self, 
                               class_name: str = "GPIOController",
                               num_pins: int = 32) -> str:
        """
        Generate GPIO controller template with pin management.
        
        Args:
            class_name: Name of the GPIO controller class
            num_pins: Number of GPIO pins
            
        Returns:
            Complete GPIO controller implementation
        """
        return f"""public class {class_name} : IDoubleWordPeripheral, IKnownSize, INumberedGPIOOutput
{{
    public {class_name}(Machine machine) : base(machine)
    {{
        pins = new GPIO[NumberOfPins];
        for(var i = 0; i < NumberOfPins; i++)
        {{
            pins[i] = new GPIO();
        }}
        
        registers = new DoubleWordRegistersCollection(this);
        DefineRegisters();
        Reset();
    }}
    
    public override void Reset()
    {{
        registers.Reset();
        pinDirection = 0;
        pinData = 0;
        UpdatePins();
    }}
    
    public uint ReadDoubleWord(long offset)
    {{
        return registers.Read(offset);
    }}
    
    public void WriteDoubleWord(long offset, uint value)
    {{
        registers.Write(offset, value);
    }}
    
    public IReadOnlyDictionary<int, IGPIO> Connections
    {{
        get
        {{
            var result = new Dictionary<int, IGPIO>();
            for(var i = 0; i < NumberOfPins; i++)
            {{
                result[i] = pins[i];
            }}
            return result;
        }}
    }}
    
    public long Size => 0x100;
    
    private void DefineRegisters()
    {{
        Registers.Data.Define(this)
            .WithValueField(0, 31, name: "DATA",
                valueProviderCallback: _ => pinData,
                writeCallback: (_, val) => 
                {{
                    pinData = (uint)val;
                    UpdatePins();
                }});
                
        Registers.Direction.Define(this)
            .WithValueField(0, 31, name: "DIR",
                valueProviderCallback: _ => pinDirection,
                writeCallback: (_, val) => 
                {{
                    pinDirection = (uint)val;
                    UpdatePins();
                }});
    }}
    
    private void UpdatePins()
    {{
        for(var i = 0; i < NumberOfPins; i++)
        {{
            if((pinDirection & (1u << i)) != 0) // Output
            {{
                pins[i].Set((pinData & (1u << i)) != 0);
            }}
        }}
    }}
    
    private uint pinDirection;
    private uint pinData;
    private readonly GPIO[] pins;
    private readonly DoubleWordRegistersCollection registers;
    
    private const int NumberOfPins = {num_pins};
    
    private enum Registers
    {{
        Data = 0x00,
        Direction = 0x04,
        // Add more registers as needed
    }}
}}"""
    
    def generate_timer_peripheral(self, 
                                class_name: str = "TimerPeripheral") -> str:
        """
        Generate timer peripheral with prescaler and interrupts.
        
        Args:
            class_name: Name of the timer class
            
        Returns:
            Complete timer peripheral implementation
        """
        return f"""public class {class_name} : IDoubleWordPeripheral, IKnownSize, IIRQSender
{{
    public {class_name}(Machine machine, long frequency = 1000000) : base(machine)
    {{
        IRQ = new GPIO();
        this.frequency = frequency;
        
        timer = new LimitTimer(machine.ClockSource, frequency, this, "Timer",
            limit: uint.MaxValue,
            direction: Direction.Ascending,
            enabled: false,
            autoUpdate: true);
            
        timer.LimitReached += OnTimerLimitReached;
        
        registers = new DoubleWordRegistersCollection(this);
        DefineRegisters();
        Reset();
    }}
    
    public override void Reset()
    {{
        registers.Reset();
        timer.Reset();
        prescaler = 1;
        UpdateTimerFrequency();
    }}
    
    public uint ReadDoubleWord(long offset)
    {{
        return registers.Read(offset);
    }}
    
    public void WriteDoubleWord(long offset, uint value)
    {{
        registers.Write(offset, value);
    }}
    
    public GPIO IRQ {{ get; private set; }}
    public long Size => 0x100;
    
    private void DefineRegisters()
    {{
        Registers.Control.Define(this)
            .WithFlag(0, name: "ENABLE",
                writeCallback: (_, val) => timer.Enabled = val)
            .WithFlag(1, name: "INTERRUPT_ENABLE",
                writeCallback: (_, val) => interruptEnabled = val)
            .WithFlag(2, name: "ONE_SHOT",
                writeCallback: (_, val) => oneShot = val)
            .WithReservedBits(3, 29);
            
        Registers.Value.Define(this)
            .WithValueField(0, 31, name: "CURRENT",
                valueProviderCallback: _ => (uint)timer.Value,
                writeCallback: (_, val) => timer.Value = val);
                
        Registers.Reload.Define(this)
            .WithValueField(0, 31, name: "RELOAD",
                writeCallback: (_, val) => timer.Limit = val);
                
        Registers.Prescaler.Define(this)
            .WithValueField(0, 15, name: "PRESCALER",
                writeCallback: (_, val) => 
                {{
                    prescaler = (uint)val + 1;
                    UpdateTimerFrequency();
                }})
            .WithReservedBits(16, 16);
            
        Registers.Status.Define(this)
            .WithFlag(0, FieldMode.WriteOneToClear, name: "INTERRUPT_FLAG",
                writeCallback: (_, val) => 
                {{
                    if(val) 
                    {{
                        interruptPending = false;
                        UpdateInterrupt();
                    }}
                }})
            .WithReservedBits(1, 31);
    }}
    
    private void OnTimerLimitReached()
    {{
        if(oneShot)
        {{
            timer.Enabled = false;
        }}
        
        interruptPending = true;
        UpdateInterrupt();
    }}
    
    private void UpdateInterrupt()
    {{
        IRQ.Set(interruptEnabled && interruptPending);
    }}
    
    private void UpdateTimerFrequency()
    {{
        timer.Frequency = frequency / prescaler;
    }}
    
    private bool interruptEnabled;
    private bool interruptPending;
    private bool oneShot;
    private uint prescaler;
    private readonly long frequency;
    private readonly LimitTimer timer;
    private readonly DoubleWordRegistersCollection registers;
    
    private enum Registers
    {{
        Control = 0x00,
        Value = 0x04,
        Reload = 0x08,
        Prescaler = 0x0C,
        Status = 0x10
    }}
}}"""
    
    def generate_uart_controller(self, 
                               class_name: str = "UARTController") -> str:
        """
        Generate UART controller with FIFO and flow control.
        
        Args:
            class_name: Name of the UART controller class
            
        Returns:
            Complete UART controller implementation
        """
        return f"""public class {class_name} : IDoubleWordPeripheral, IKnownSize, IUART, IIRQSender
{{
    public {class_name}(Machine machine) : base(machine)
    {{
        IRQ = new GPIO();
        txFifo = new Queue<byte>(FifoSize);
        rxFifo = new Queue<byte>(FifoSize);
        
        registers = new DoubleWordRegistersCollection(this);
        DefineRegisters();
        Reset();
    }}
    
    public override void Reset()
    {{
        registers.Reset();
        txFifo.Clear();
        rxFifo.Clear();
        UpdateInterrupts();
    }}
    
    public void WriteChar(byte value)
    {{
        if(rxFifo.Count < FifoSize)
        {{
            rxFifo.Enqueue(value);
            UpdateInterrupts();
        }}
    }}
    
    public uint ReadDoubleWord(long offset)
    {{
        return registers.Read(offset);
    }}
    
    public void WriteDoubleWord(long offset, uint value)
    {{
        registers.Write(offset, value);
    }}
    
    public event Action<byte> CharReceived;
    
    public GPIO IRQ {{ get; private set; }}
    public long Size => 0x100;
    public uint BaudRate {{ get; set; }} = 115200;
    public Bits StopBits {{ get; set; }} = Bits.One;
    public Parity ParityBit {{ get; set; }} = Parity.None;
    
    private void DefineRegisters()
    {{
        Registers.Data.Define(this)
            .WithValueField(0, 7, name: "DATA",
                valueProviderCallback: _ => 
                {{
                    if(rxFifo.Count > 0)
                    {{
                        var data = rxFifo.Dequeue();
                        UpdateInterrupts();
                        return data;
                    }}
                    return 0;
                }},
                writeCallback: (_, val) => 
                {{
                    if(txFifo.Count < FifoSize)
                    {{
                        txFifo.Enqueue((byte)val);
                        CharReceived?.Invoke((byte)val);
                        UpdateInterrupts();
                    }}
                }})
            .WithReservedBits(8, 24);
            
        Registers.Status.Define(this)
            .WithFlag(0, FieldMode.Read, name: "TX_EMPTY",
                valueProviderCallback: _ => txFifo.Count == 0)
            .WithFlag(1, FieldMode.Read, name: "TX_FULL",
                valueProviderCallback: _ => txFifo.Count >= FifoSize)
            .WithFlag(2, FieldMode.Read, name: "RX_EMPTY",
                valueProviderCallback: _ => rxFifo.Count == 0)
            .WithFlag(3, FieldMode.Read, name: "RX_FULL",
                valueProviderCallback: _ => rxFifo.Count >= FifoSize)
            .WithReservedBits(4, 28);
            
        Registers.Control.Define(this)
            .WithFlag(0, name: "TX_ENABLE",
                writeCallback: (_, val) => txEnabled = val)
            .WithFlag(1, name: "RX_ENABLE",
                writeCallback: (_, val) => rxEnabled = val)
            .WithFlag(2, name: "TX_INT_ENABLE",
                writeCallback: (_, val) => 
                {{
                    txInterruptEnabled = val;
                    UpdateInterrupts();
                }})
            .WithFlag(3, name: "RX_INT_ENABLE",
                writeCallback: (_, val) => 
                {{
                    rxInterruptEnabled = val;
                    UpdateInterrupts();
                }})
            .WithReservedBits(4, 28);
    }}
    
    private void UpdateInterrupts()
    {{
        var txInt = txInterruptEnabled && txFifo.Count < FifoSize / 2;
        var rxInt = rxInterruptEnabled && rxFifo.Count > 0;
        IRQ.Set(txInt || rxInt);
    }}
    
    private bool txEnabled;
    private bool rxEnabled;
    private bool txInterruptEnabled;
    private bool rxInterruptEnabled;
    private readonly Queue<byte> txFifo;
    private readonly Queue<byte> rxFifo;
    private readonly DoubleWordRegistersCollection registers;
    
    private const int FifoSize = 16;
    
    private enum Registers
    {{
        Data = 0x00,
        Status = 0x04,
        Control = 0x08,
        BaudRate = 0x0C
    }}
}}"""
    
    def generate_dma_controller(self, 
                              class_name: str = "DMAController",
                              num_channels: int = 8) -> str:
        """
        Generate DMA controller with channel management.
        
        Args:
            class_name: Name of the DMA controller class
            num_channels: Number of DMA channels
            
        Returns:
            Complete DMA controller implementation
        """
        return f"""public class {class_name} : IDoubleWordPeripheral, IKnownSize, IIRQSender, IDMAEngine
{{
    public {class_name}(Machine machine) : base(machine)
    {{
        IRQ = new GPIO();
        channels = new DMAChannel[NumberOfChannels];
        for(var i = 0; i < NumberOfChannels; i++)
        {{
            channels[i] = new DMAChannel(i, this);
        }}
        
        registers = new DoubleWordRegistersCollection(this);
        DefineRegisters();
        Reset();
    }}
    
    public override void Reset()
    {{
        registers.Reset();
        foreach(var channel in channels)
        {{
            channel.Reset();
        }}
        UpdateInterrupts();
    }}
    
    public uint ReadDoubleWord(long offset)
    {{
        return registers.Read(offset);
    }}
    
    public void WriteDoubleWord(long offset, uint value)
    {{
        registers.Write(offset, value);
    }}
    
    public void RequestTransfer(int channel, DMARequest request)
    {{
        if(channel < 0 || channel >= NumberOfChannels)
        {{
            this.Log(LogLevel.Warning, "Invalid DMA channel: {{0}}", channel);
            return;
        }}
        
        channels[channel].StartTransfer(request);
    }}
    
    public GPIO IRQ {{ get; private set; }}
    public long Size => 0x1000;
    
    private void DefineRegisters()
    {{
        // Global control register
        Registers.Control.Define(this)
            .WithFlag(0, name: "ENABLE",
                writeCallback: (_, val) => dmaEnabled = val)
            .WithReservedBits(1, 31);
            
        // Channel registers
        for(var i = 0; i < NumberOfChannels; i++)
        {{
            var channelOffset = 0x100 + (i * 0x20);
            var channel = channels[i];
            
            // Source address
            ((Registers)(channelOffset + 0x00)).Define(this)
                .WithValueField(0, 31, name: $"CH{{i}}_SRC",
                    writeCallback: (_, val) => channel.SourceAddress = val);
                    
            // Destination address
            ((Registers)(channelOffset + 0x04)).Define(this)
                .WithValueField(0, 31, name: $"CH{{i}}_DST",
                    writeCallback: (_, val) => channel.DestinationAddress = val);
                    
            // Transfer count
            ((Registers)(channelOffset + 0x08)).Define(this)
                .WithValueField(0, 31, name: $"CH{{i}}_COUNT",
                    writeCallback: (_, val) => channel.TransferCount = val);
                    
            // Channel control
            ((Registers)(channelOffset + 0x0C)).Define(this)
                .WithFlag(0, name: $"CH{{i}}_ENABLE",
                    writeCallback: (_, val) => channel.Enabled = val)
                .WithFlag(1, name: $"CH{{i}}_INT_ENABLE",
                    writeCallback: (_, val) => channel.InterruptEnabled = val)
                .WithFlag(2, FieldMode.WriteOneToClear, name: $"CH{{i}}_INT_FLAG",
                    writeCallback: (_, val) =>
                    {{
                        if(val) channel.ClearInterrupt();
                        UpdateInterrupts();
                    }})
                .WithReservedBits(3, 29);
        }}
    }}
    
    private void UpdateInterrupts()
    {{
        var anyInterrupt = channels.Any(ch => ch.InterruptPending);
        IRQ.Set(anyInterrupt);
    }}
    
    private bool dmaEnabled;
    private readonly DMAChannel[] channels;
    private readonly DoubleWordRegistersCollection registers;
    
    private const int NumberOfChannels = {num_channels};
    
    private enum Registers
    {{
        Control = 0x00,
        Status = 0x04,
        // Channel registers start at 0x100
    }}
    
    private class DMAChannel
    {{
        public DMAChannel(int index, {class_name} parent)
        {{
            this.index = index;
            this.parent = parent;
        }}
        
        public void Reset()
        {{
            SourceAddress = 0;
            DestinationAddress = 0;
            TransferCount = 0;
            Enabled = false;
            InterruptEnabled = false;
            InterruptPending = false;
        }}
        
        public void StartTransfer(DMARequest request)
        {{
            if(!Enabled || TransferCount == 0)
            {{
                return;
            }}
            
            // Perform transfer
            parent.machine.SystemBus.CopyMemory(
                SourceAddress,
                DestinationAddress,
                TransferCount);
                
            // Update status
            if(InterruptEnabled)
            {{
                InterruptPending = true;
                parent.UpdateInterrupts();
            }}
        }}
        
        public void ClearInterrupt()
        {{
            InterruptPending = false;
        }}
        
        public uint SourceAddress {{ get; set; }}
        public uint DestinationAddress {{ get; set; }}
        public uint TransferCount {{ get; set; }}
        public bool Enabled {{ get; set; }}
        public bool InterruptEnabled {{ get; set; }}
        public bool InterruptPending {{ get; set; }}
        
        private readonly int index;
        private readonly {class_name} parent;
    }}
}}"""
    
    def generate_interrupt_controller(self,
                                    class_name: str = "InterruptController",
                                    num_sources: int = 32) -> str:
        """
        Generate interrupt controller with priority handling.
        
        Args:
            class_name: Name of the interrupt controller class
            num_sources: Number of interrupt sources
            
        Returns:
            Complete interrupt controller implementation
        """
        return f"""public class {class_name} : IDoubleWordPeripheral, IKnownSize, IIRQController
{{
    public {class_name}(Machine machine) : base(machine)
    {{
        IRQ = new GPIO();
        sources = new InterruptSource[NumberOfSources];
        for(var i = 0; i < NumberOfSources; i++)
        {{
            sources[i] = new InterruptSource(i);
        }}
        
        registers = new DoubleWordRegistersCollection(this);
        DefineRegisters();
        Reset();
    }}
    
    public override void Reset()
    {{
        registers.Reset();
        foreach(var source in sources)
        {{
            source.Reset();
        }}
        UpdateInterrupts();
    }}
    
    public uint ReadDoubleWord(long offset)
    {{
        return registers.Read(offset);
    }}
    
    public void WriteDoubleWord(long offset, uint value)
    {{
        registers.Write(offset, value);
    }}
    
    public void OnGPIO(int number, bool value)
    {{
        if(number < 0 || number >= NumberOfSources)
        {{
            this.Log(LogLevel.Warning, "Invalid interrupt source: {{0}}", number);
            return;
        }}
        
        sources[number].Pending = value;
        UpdateInterrupts();
    }}
    
    public GPIO IRQ {{ get; private set; }}
    public long Size => 0x1000;
    
    private void DefineRegisters()
    {{
        // Interrupt enable register
        Registers.Enable.Define(this)
            .WithValueField(0, 31, name: "ENABLE",
                writeCallback: (_, val) =>
                {{
                    for(var i = 0; i < Math.Min(32, NumberOfSources); i++)
                    {{
                        sources[i].Enabled = ((val >> i) & 1) != 0;
                    }}
                    UpdateInterrupts();
                }});
                
        // Interrupt pending register
        Registers.Pending.Define(this)
            .WithValueField(0, 31, FieldMode.Read, name: "PENDING",
                valueProviderCallback: _ =>
                {{
                    uint pending = 0;
                    for(var i = 0; i < Math.Min(32, NumberOfSources); i++)
                    {{
                        if(sources[i].Pending)
                        {{
                            pending |= (1u << i);
                        }}
                    }}
                    return pending;
                }});
                
        // Priority registers
        for(var i = 0; i < NumberOfSources; i++)
        {{
            var source = sources[i];
            ((Registers)(0x100 + i * 4)).Define(this)
                .WithValueField(0, 7, name: $"PRIORITY_{{i}}",
                    writeCallback: (_, val) => source.Priority = (byte)val)
                .WithReservedBits(8, 24);
        }}
    }}
    
    private void UpdateInterrupts()
    {{
        var activeInterrupt = sources
            .Where(s => s.Enabled && s.Pending)
            .OrderByDescending(s => s.Priority)
            .FirstOrDefault();
            
        IRQ.Set(activeInterrupt != null);
    }}
    
    private readonly InterruptSource[] sources;
    private readonly DoubleWordRegistersCollection registers;
    
    private const int NumberOfSources = {num_sources};
    
    private enum Registers
    {{
        Enable = 0x00,
        Pending = 0x04,
        // Priority registers start at 0x100
    }}
    
    private class InterruptSource
    {{
        public InterruptSource(int index)
        {{
            this.index = index;
        }}
        
        public void Reset()
        {{
            Enabled = false;
            Pending = false;
            Priority = 0;
        }}
        
        public bool Enabled {{ get; set; }}
        public bool Pending {{ get; set; }}
        public byte Priority {{ get; set; }}
        
        private readonly int index;
    }}
}}"""
    
    def generate_spi_controller(self,
                              class_name: str = "SPIController") -> str:
        """
        Generate SPI controller template.
        
        Args:
            class_name: Name of the SPI controller class
            
        Returns:
            Complete SPI controller implementation
        """
        return f"""public class {class_name} : IDoubleWordPeripheral, IKnownSize, ISPIPeripheral
{{
    public {class_name}(Machine machine) : base(machine)
    {{
        txFifo = new Queue<byte>(FifoSize);
        rxFifo = new Queue<byte>(FifoSize);
        
        registers = new DoubleWordRegistersCollection(this);
        DefineRegisters();
        Reset();
    }}
    
    public override void Reset()
    {{
        registers.Reset();
        txFifo.Clear();
        rxFifo.Clear();
        currentTransfer = null;
    }}
    
    public byte Transmit(byte data)
    {{
        if(!enabled)
        {{
            return 0xFF;
        }}
        
        // In loopback mode, return transmitted data
        if(loopbackMode)
        {{
            return data;
        }}
        
        // Otherwise, return data from RX FIFO or 0xFF
        if(rxFifo.Count > 0)
        {{
            return rxFifo.Dequeue();
        }}
        
        return 0xFF;
    }}
    
    public void FinishTransmission()
    {{
        currentTransfer = null;
    }}
    
    public uint ReadDoubleWord(long offset)
    {{
        return registers.Read(offset);
    }}
    
    public void WriteDoubleWord(long offset, uint value)
    {{
        registers.Write(offset, value);
    }}
    
    public long Size => 0x100;
    
    private void DefineRegisters()
    {{
        Registers.Control.Define(this)
            .WithFlag(0, name: "ENABLE",
                writeCallback: (_, val) => enabled = val)
            .WithFlag(1, name: "LOOPBACK",
                writeCallback: (_, val) => loopbackMode = val)
            .WithValueField(2, 3, name: "MODE",
                writeCallback: (_, val) => spiMode = (uint)val)
            .WithFlag(4, name: "MSB_FIRST",
                writeCallback: (_, val) => msbFirst = val)
            .WithValueField(8, 15, name: "CLOCK_DIV",
                writeCallback: (_, val) => clockDivider = (uint)val)
            .WithReservedBits(16, 16);
            
        Registers.Data.Define(this)
            .WithValueField(0, 7, name: "DATA",
                valueProviderCallback: _ =>
                {{
                    if(rxFifo.Count > 0)
                    {{
                        return rxFifo.Dequeue();
                    }}
                    return 0;
                }},
                writeCallback: (_, val) =>
                {{
                    if(enabled && txFifo.Count < FifoSize)
                    {{
                        txFifo.Enqueue((byte)val);
                        ProcessTransfer();
                    }}
                }})
            .WithReservedBits(8, 24);
            
        Registers.Status.Define(this)
            .WithFlag(0, FieldMode.Read, name: "TX_EMPTY",
                valueProviderCallback: _ => txFifo.Count == 0)
            .WithFlag(1, FieldMode.Read, name: "TX_FULL",
                valueProviderCallback: _ => txFifo.Count >= FifoSize)
            .WithFlag(2, FieldMode.Read, name: "RX_EMPTY",
                valueProviderCallback: _ => rxFifo.Count == 0)
            .WithFlag(3, FieldMode.Read, name: "RX_FULL",
                valueProviderCallback: _ => rxFifo.Count >= FifoSize)
            .WithFlag(4, FieldMode.Read, name: "BUSY",
                valueProviderCallback: _ => currentTransfer != null)
            .WithReservedBits(5, 27);
    }}
    
    private void ProcessTransfer()
    {{
        while(txFifo.Count > 0 && rxFifo.Count < FifoSize)
        {{
            var txData = txFifo.Dequeue();
            var rxData = Transmit(txData);
            rxFifo.Enqueue(rxData);
        }}
    }}
    
    private bool enabled;
    private bool loopbackMode;
    private bool msbFirst;
    private uint spiMode;
    private uint clockDivider;
    private object currentTransfer;
    private readonly Queue<byte> txFifo;
    private readonly Queue<byte> rxFifo;
    private readonly DoubleWordRegistersCollection registers;
    
    private const int FifoSize = 16;
    
    private enum Registers
    {{
        Control = 0x00,
        Data = 0x04,
        Status = 0x08
    }}
}}"""
    
    def generate_i2c_controller(self,
                              class_name: str = "I2CController") -> str:
        """
        Generate I2C controller template.
        
        Args:
            class_name: Name of the I2C controller class
            
        Returns:
            Complete I2C controller implementation
        """
        return f"""public class {class_name} : IDoubleWordPeripheral, IKnownSize, II2CPeripheral
{{
    public {class_name}(Machine machine) : base(machine)
    {{
        txFifo = new Queue<byte>(FifoSize);
        rxFifo = new Queue<byte>(FifoSize);
        
        registers = new DoubleWordRegistersCollection(this);
        DefineRegisters();
        Reset();
    }}
    
    public override void Reset()
    {{
        registers.Reset();
        txFifo.Clear();
        rxFifo.Clear();
        currentAddress = 0;
        state = I2CState.Idle;
    }}
    
    public byte Read(int offset = 0)
    {{
        if(rxFifo.Count > 0)
        {{
            return rxFifo.Dequeue();
        }}
        return 0xFF;
    }}
    
    public void Write(int offset, byte value)
    {{
        if(txFifo.Count < FifoSize)
        {{
            txFifo.Enqueue(value);
        }}
    }}
    
    public uint ReadDoubleWord(long offset)
    {{
        return registers.Read(offset);
    }}
    
    public void WriteDoubleWord(long offset, uint value)
    {{
        registers.Write(offset, value);
    }}
    
    public long Size => 0x100;
    
    private void DefineRegisters()
    {{
        Registers.Control.Define(this)
            .WithFlag(0, name: "ENABLE",
                writeCallback: (_, val) => enabled = val)
            .WithFlag(1, name: "MASTER_MODE",
                writeCallback: (_, val) => masterMode = val)
            .WithFlag(2, name: "START",
                writeCallback: (_, val) =>
                {{
                    if(val) SendStart();
                }})
            .WithFlag(3, name: "STOP",
                writeCallback: (_, val) =>
                {{
                    if(val) SendStop();
                }})
            .WithFlag(4, name: "ACK",
                writeCallback: (_, val) => ackEnabled = val)
            .WithValueField(8, 14, name: "SLAVE_ADDR",
                writeCallback: (_, val) => slaveAddress = (byte)val)
            .WithReservedBits(15, 17);
            
        Registers.Data.Define(this)
            .WithValueField(0, 7, name: "DATA",
                valueProviderCallback: _ => Read(),
                writeCallback: (_, val) => Write(0, (byte)val))
            .WithReservedBits(8, 24);
            
        Registers.Status.Define(this)
            .WithFlag(0, FieldMode.Read, name: "BUSY",
                valueProviderCallback: _ => state != I2CState.Idle)
            .WithFlag(1, FieldMode.Read, name: "TX_EMPTY",
                valueProviderCallback: _ => txFifo.Count == 0)
            .WithFlag(2, FieldMode.Read, name: "RX_FULL",
                valueProviderCallback: _ => rxFifo.Count >= FifoSize)
            .WithFlag(3, FieldMode.Read, name: "ACK_RECEIVED",
                valueProviderCallback: _ => lastAckReceived)
            .WithReservedBits(4, 28);
            
        Registers.ClockControl.Define(this)
            .WithValueField(0, 15, name: "CLOCK_DIV",
                writeCallback: (_, val) => clockDivider = (uint)val)
            .WithReservedBits(16, 16);
    }}
    
    private void SendStart()
    {{
        if(enabled && masterMode)
        {{
            state = I2CState.Start;
            this.Log(LogLevel.Debug, "I2C START condition");
        }}
    }}
    
    private void SendStop()
    {{
        if(enabled && masterMode)
        {{
            state = I2CState.Idle;
            this.Log(LogLevel.Debug, "I2C STOP condition");
        }}
    }}
    
    private bool enabled;
    private bool masterMode;
    private bool ackEnabled;
    private bool lastAckReceived;
    private byte slaveAddress;
    private byte currentAddress;
    private uint clockDivider;
    private I2CState state;
    private readonly Queue<byte> txFifo;
    private readonly Queue<byte> rxFifo;
    private readonly DoubleWordRegistersCollection registers;
    
    private const int FifoSize = 16;
    
    private enum Registers
    {{
        Control = 0x00,
        Data = 0x04,
        Status = 0x08,
        ClockControl = 0x0C
    }}
    
    private enum I2CState
    {{
        Idle,
        Start,
        Address,
        Data,
        Stop
    }}
}}"""
    
    # ==================== Helper Methods ====================
    
    def generate_method_signature(self,
                                name: str,
                                return_type: str,
                                parameters: List[Tuple[str, str]],
                                access: str = "private") -> str:
        """
        Generate a method signature.
        
        Args:
            name: Method name
            return_type: Return type
            parameters: List of (type, name) tuples
            access: Access modifier
            
        Returns:
            Method signature
        """
        param_str = ", ".join([f"{ptype} {pname}" for ptype, pname in parameters])
        return f"{access} {return_type} {name}({param_str})"
    
    def generate_constructor_pattern(self,
                                   class_name: str,
                                   base_params: List[str] = None) -> str:
        """
        Generate constructor pattern with Machine context.
        
        Args:
            class_name: Name of the class
            base_params: Additional base constructor parameters
            
        Returns:
            Constructor pattern
        """
        base_params_str = ", ".join(base_params) if base_params else ""
        if base_params_str:
            base_params_str = ", " + base_params_str
            
        return f"""public {class_name}(Machine machine{base_params_str}) : base(machine)
{{
    // Initialize components
    InitializeRegisters();
    Reset();
}}"""
    
    def generate_reset_pattern(self) -> str:
        """Generate standard reset implementation pattern."""
        return """public override void Reset()
{
    // Reset registers
    registers?.Reset();
    
    // Reset internal state
    ResetInternalState();
    
    // Reset hardware components
    ResetHardware();
    
    // Update outputs
    UpdateOutputs();
}

private void ResetInternalState()
{
    // Reset flags, counters, etc.
}

private void ResetHardware()
{
    // Reset timers, FIFOs, etc.
}

private void UpdateOutputs()
{
    // Update GPIO outputs, interrupts, etc.
}"""
    
    def generate_documentation_template(self,
                                      peripheral_type: str,
                                      description: str) -> str:
        """
        Generate XML documentation template.
        
        Args:
            peripheral_type: Type of peripheral
            description: Description of the peripheral
            
        Returns:
            Documentation template
        """
        return f"""/// <summary>
/// {description}
/// </summary>
/// <remarks>
/// This is a Renode implementation of a {peripheral_type} peripheral.
/// Key features:
/// - Register-based configuration
/// - Interrupt support
/// - DMA capability (if applicable)
///
/// Usage example:
/// <code>
/// machine.SystemBus.Register(peripheral, new BusRangeRegistration(0x40000000, 0x1000));
/// </code>
/// </remarks>"""


# Example usage and testing
if __name__ == "__main__":
    templates = RenodeTemplates()
    
    # Example: Generate a simple GPIO controller
    print("=== GPIO Controller Example ===")
    print(templates.generate_using_statements("gpio"))
    print("\n")
    print(templates.generate_gpio_controller("CustomGPIO", 16))
    
    # Example: Generate register definitions
    print("\n\n=== Register Definition Example ===")
    reg = RegisterDefinition(
        name="Control",
        offset=0x00,
        description="Control register",
        fields=[
            RegisterField("ENABLE", 0, 0, "Enable peripheral"),
            RegisterField("INT_EN", 1, 1, "Enable interrupts"),
            RegisterField("MODE", 2, 3, "Operating mode", RegisterAccess.READ_WRITE)
        ]
    )
    print(templates.generate_register_definition(reg))