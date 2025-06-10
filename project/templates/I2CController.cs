public class I2CController : IDoubleWordPeripheral, IKnownSize, II2CPeripheral
{
    public I2CController(Machine machine) : base(machine)
    {
        txFifo = new Queue<byte>(FifoSize);
        rxFifo = new Queue<byte>(FifoSize);
        
        registers = new DoubleWordRegistersCollection(this);
        DefineRegisters();
        Reset();
    }
    
    public override void Reset()
    {
        registers.Reset();
        txFifo.Clear();
        rxFifo.Clear();
        currentAddress = 0;
        state = I2CState.Idle;
    }
    
    public byte Read(int offset = 0)
    {
        if(rxFifo.Count > 0)
        {
            return rxFifo.Dequeue();
        }
        return 0xFF;
    }
    
    public void Write(int offset, byte value)
    {
        if(txFifo.Count < FifoSize)
        {
            txFifo.Enqueue(value);
        }
    }
    
    public uint ReadDoubleWord(long offset)
    {
        return registers.Read(offset);
    }
    
    public void WriteDoubleWord(long offset, uint value)
    {
        registers.Write(offset, value);
    }
    
    public long Size => 0x100;
    
    private void DefineRegisters()
    {
        Registers.Control.Define(this)
            .WithFlag(0, name: "ENABLE",
                writeCallback: (_, val) => enabled = val)
            .WithFlag(1, name: "MASTER_MODE",
                writeCallback: (_, val) => masterMode = val)
            .WithFlag(2, name: "START",
                writeCallback: (_, val) =>
                {
                    if(val) SendStart();
                })
            .WithFlag(3, name: "STOP",
                writeCallback: (_, val) =>
                {
                    if(val) SendStop();
                })
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
    }
    
    private void SendStart()
    {
        if(enabled && masterMode)
        {
            state = I2CState.Start;
            this.Log(LogLevel.Debug, "I2C START condition");
        }
    }
    
    private void SendStop()
    {
        if(enabled && masterMode)
        {
            state = I2CState.Idle;
            this.Log(LogLevel.Debug, "I2C STOP condition");
        }
    }
    
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
    {
        Control = 0x00,
        Data = 0x04,
        Status = 0x08,
        ClockControl = 0x0C
    }
    
    private enum I2CState
    {
        Idle,
        Start,
        Address,
        Data,
        Stop
    }
}