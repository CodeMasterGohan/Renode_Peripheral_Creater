# Renode Peripheral Development Patterns

This document describes common patterns and best practices for developing peripherals in Renode.

## Table of Contents

1. [Basic Peripheral Structure](#basic-peripheral-structure)
2. [Register Implementation Patterns](#register-implementation-patterns)
3. [Interrupt Handling](#interrupt-handling)
4. [State Management](#state-management)
5. [External Interfaces](#external-interfaces)
6. [Timing and Clocks](#timing-and-clocks)
7. [Memory and DMA](#memory-and-dma)
8. [Testing Patterns](#testing-patterns)
9. [Common Pitfalls](#common-pitfalls)

## Basic Peripheral Structure

### Inheritance Hierarchy

```csharp
// For simple peripherals with 32-bit registers
public class MyPeripheral : BasicDoubleWordPeripheral, IKnownSize
{
    public MyPeripheral(IMachine machine) : base(machine)
    {
        // Constructor
    }
}

// For UART peripherals
public class MyUART : UARTBase, IDoubleWordPeripheral
{
    // Implementation
}

// For SPI peripherals
public class MySPI : NullRegistrationPointPeripheralContainer<ISPIPeripheral>
{
    // Implementation
}
```

### Essential Interfaces

- `IDoubleWordPeripheral` - 32-bit register access
- `IWordPeripheral` - 16-bit register access
- `IBytePeripheral` - 8-bit register access
- `IKnownSize` - Defines peripheral memory size
- `IGPIOReceiver` - Receives GPIO signals
- `INumberedGPIOOutput` - Provides numbered GPIO outputs

## Register Implementation Patterns

### Basic Register Definition

```csharp
private void DefineRegisters()
{
    Registers.Control.Define(this)
        .WithFlag(0, name: "EN",
            valueProviderCallback: _ => isEnabled,
            writeCallback: (_, value) =>
            {
                isEnabled = value;
                UpdateState();
            })
        .WithValueField(8, 8, name: "PRESCALER",
            valueProviderCallback: _ => prescaler,
            writeCallback: (_, value) => prescaler = (uint)value)
        .WithReservedBits(16, 16);
}
```

### Read-Only Registers

```csharp
Registers.Status.Define(this)
    .WithFlag(0, FieldMode.Read, name: "BUSY",
        valueProviderCallback: _ => isBusy)
    .WithFlag(1, FieldMode.Read, name: "ERROR",
        valueProviderCallback: _ => hasError);
```

### Write-1-to-Clear Pattern

```csharp
Registers.InterruptStatus.Define(this)
    .WithFlag(0, name: "INT_FLAG",
        valueProviderCallback: _ => interruptPending,
        writeCallback: (_, value) =>
        {
            if(value) // Write 1 to clear
            {
                interruptPending = false;
                UpdateInterrupts();
            }
        });
```

### Register with Side Effects

```csharp
Registers.Command.Define(this)
    .WithValueField(0, 8, FieldMode.Write, name: "CMD",
        writeCallback: (_, value) => ExecuteCommand((byte)value))
    .WithWriteCallback((_, __) =>
    {
        // Additional actions after any write
        this.Log(LogLevel.Debug, "Command register written");
    });
```

### Banked Registers

```csharp
private uint ReadRegister(long offset)
{
    var bank = (currentBank * BankSize);
    var actualOffset = bank + (offset & BankMask);
    return registers[actualOffset];
}
```

## Interrupt Handling

### Single Interrupt

```csharp
public GPIO IRQ { get; private set; }

private void UpdateInterrupts()
{
    var shouldTrigger = interruptEnable && interruptStatus;
    IRQ.Set(shouldTrigger);
}
```

### Multiple Interrupts

```csharp
public ReadOnlyDictionary<int, IGPIO> Connections { get; private set; }

private void InitializeInterrupts()
{
    var irqs = new Dictionary<int, IGPIO>();
    for(int i = 0; i < NumberOfInterrupts; i++)
    {
        irqs[i] = new GPIO();
    }
    Connections = new ReadOnlyDictionary<int, IGPIO>(irqs);
}
```

### Interrupt Priority

```csharp
private uint GetHighestPriorityInterrupt()
{
    for(int i = 0; i < interrupts.Length; i++)
    {
        if(interrupts[i].IsPending && interrupts[i].IsEnabled)
        {
            return (uint)i;
        }
    }
    return NoInterruptPending;
}
```

## State Management

### State Machine Pattern

```csharp
private enum State
{
    Idle,
    Active,
    Error
}

private void TransitionTo(State newState)
{
    if(!IsValidTransition(currentState, newState))
    {
        this.Log(LogLevel.Warning, "Invalid state transition from {0} to {1}",
            currentState, newState);
        return;
    }

    this.Log(LogLevel.Debug, "State transition: {0} -> {1}", currentState, newState);
    currentState = newState;
    OnStateChanged();
}
```

### Persistent State

```csharp
public override void Reset()
{
    base.Reset();

    // Reset only non-persistent state
    currentValue = 0;

    // Preserve configuration
    // config remains unchanged
}
```

## External Interfaces

### GPIO Connections

```csharp
public void OnGPIO(int number, bool value)
{
    if(number >= NumberOfPins)
    {
        this.Log(LogLevel.Warning, "GPIO {0} out of range", number);
        return;
    }

    pinStates[number] = value;
    HandlePinChange(number, value);
}
```

### Clock Input

```csharp
public long ClockFrequency
{
    get => clockFrequency;
    set
    {
        clockFrequency = value;
        UpdateTimings();
    }
}
```

### DMA Interface

```csharp
public byte[] ReadDMA(uint address, int count)
{
    var data = new byte[count];
    for(int i = 0; i < count; i++)
    {
        data[i] = ReadByte(address + i);
    }
    return data;
}
```

## Timing and Clocks

### Using LimitTimer

```csharp
private void InitializeTimer()
{
    timer = new LimitTimer(machine.ClockSource, frequency, this, "timer",
        limit: periodValue,
        direction: Direction.Ascending,
        enabled: false,
        eventEnabled: true);

    timer.LimitReached += OnTimerEvent;
}
```

### Precise Timing

```csharp
private void ScheduleEvent(ulong cycles)
{
    machine.ClockSource.ExecuteInNearestSyncedState(_ =>
    {
        ProcessScheduledEvent();
    }, cycles);
}
```

### Time Synchronization

```csharp
private ulong GetCurrentTime()
{
    return machine.ClockSource.CurrentValue;
}

private void WaitCycles(ulong cycles)
{
    var targetTime = GetCurrentTime() + cycles;
    machine.ClockSource.Advance(targetTime);
}
```

## Memory and DMA

### Memory-Mapped Buffers

```csharp
private readonly byte[] buffer = new byte[BufferSize];

public byte ReadByte(long offset)
{
    if(offset < BufferOffset || offset >= BufferOffset + BufferSize)
    {
        return (byte)RegistersCollection.Read(offset);
    }

    return buffer[offset - BufferOffset];
}
```

### DMA Transfer

```csharp
private void PerformDMATransfer()
{
    var data = machine.SystemBus.ReadBytes(sourceAddress, transferCount);
    machine.SystemBus.WriteBytes(data, destinationAddress);

    OnTransferComplete();
}
```

## Testing Patterns

### Unit Test Structure

```csharp
[Test]
public void ShouldTriggerInterruptOnOverflow()
{
    var peripheral = new MyTimer(machine, 1000000); // 1MHz

    // Setup
    peripheral.WriteDoubleWord((long)Registers.Control, 0x01); // Enable
    peripheral.WriteDoubleWord((long)Registers.Period, 1000);

    // Act
    machine.ClockSource.Advance(TimeInterval.FromMicroseconds(1001));

    // Assert
    Assert.IsTrue(peripheral.IRQ.IsSet);
}
```

### Testing GPIO

```csharp
[Test]
public void ShouldDetectInputChange()
{
    var gpio = new MyGPIO(machine);
    var inputPin = 5;

    // Configure as input
    gpio.WriteDoubleWord((long)Registers.Direction, 0x00);

    // Simulate external signal
    gpio.OnGPIO(inputPin, true);

    // Read data register
    var data = gpio.ReadDoubleWord((long)Registers.Data);
    Assert.AreEqual(1u << inputPin, data);
}
```

## Common Pitfalls

### 1. Forgetting Thread Safety

```csharp
// Bad
private void UpdateFifo(byte data)
{
    fifo.Enqueue(data);
}

// Good
private void UpdateFifo(byte data)
{
    lock(fifoLock)
    {
        fifo.Enqueue(data);
    }
}
```

### 2. Incorrect Register Size Handling

```csharp
// Handle different access sizes
public uint ReadDoubleWord(long offset)
{
    return registers[offset / 4];
}

public ushort ReadWord(long offset)
{
    var doubleWord = ReadDoubleWord(offset & ~3);
    return (ushort)(doubleWord >> ((offset & 2) * 8));
}
```

### 3. Missing Reset Implementation

```csharp
public override void Reset()
{
    base.Reset(); // Don't forget this!

    // Reset peripheral-specific state
    fifo.Clear();
    currentState = State.Idle;
    interruptStatus = 0;
}
```

### 4. Improper Logging

```csharp
// Too verbose for normal operation
this.Log(LogLevel.Info, "Register read at 0x{0:X}", offset);

// Better
this.Log(LogLevel.Noisy, "Register read at 0x{0:X}", offset);
```

### 5. Not Handling Edge Cases

```csharp
private void SetDivisor(uint value)
{
    if(value == 0)
    {
        this.Log(LogLevel.Warning, "Invalid divisor value: 0");
        return;
    }

    divisor = value;
    UpdateFrequency();
}
```

## Best Practices

1. **Use Appropriate Base Classes**: Choose the right base class for your peripheral type
2. **Implement IKnownSize**: Always specify the peripheral's memory size
3. **Log Appropriately**: Use correct log levels (Noisy for frequent events, Debug for state changes, Warning for errors)
4. **Handle Reset Properly**: Ensure all state is properly reset
5. **Document Register Behavior**: Use XML comments for complex register behavior
6. **Test Edge Cases**: Include tests for boundary conditions and error cases
7. **Use Renode's Infrastructure**: Leverage existing classes like LimitTimer, CircularBuffer, etc.
8. **Thread Safety**: Use locks when accessing shared state
9. **Validate Input**: Check register values and external inputs for validity
10. **Performance Considerations**: Avoid expensive operations in frequently called methods

## Advanced Patterns

### Custom Register Collections

```csharp
private class CustomRegisterCollection : DoubleWordRegisterCollection
{
    public CustomRegisterCollection(IPeripheral parent) : base(parent)
    {
        DefineRegisters();
    }

    public override uint ReadDoubleWord(long offset)
    {
        // Custom read logic
        return base.ReadDoubleWord(offset);
    }
}
```

### Peripheral Containers

```csharp
public class MultiChannelPeripheral : SimpleContainer<IPeripheral>
{
    public MultiChannelPeripheral(IMachine machine, int channels) : base(machine)
    {
        for(int i = 0; i < channels; i++)
        {
            RegisterPeripheral(new Channel(machine, i), new NullRegistrationPoint());
        }
    }
}
```

### Event-Driven Architecture

```csharp
public event Action<uint> DataReceived;

private void OnDataReady(uint data)
{
    DataReceived?.Invoke(data);
}
```

This documentation provides a foundation for understanding Renode peripheral development patterns. Always refer to existing Renode peripherals and official documentation for the most up-to-date practices.
