public class SPIController : IDoubleWordPeripheral, IKnownSize, ISPIPeripheral
{
    public SPIController(Machine machine) : base(machine)
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
        currentTransfer = null;
    }
    
    public byte Transmit(byte data)
    {
        if(!enabled)
        {
            return 0xFF;
        }
        
        // In loopback mode, return transmitted data
        if(loopbackMode)
        {
            return data;
        }
        
        // Otherwise, return data from RX FIFO or 0xFF
        if(rxFifo.Count > 0)
        {
            return rxFifo.Dequeue();
        }
        
        return 0xFF;
    }
    
    public void FinishTransmission()
    {
        currentTransfer = null;
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
                {
                    if(rxFifo.Count > 0)
                    {
                        return rxFifo.Dequeue();
                    }
                    return 0;
                },
                writeCallback: (_, val) =>
                {
                    if(enabled && txFifo.Count < FifoSize)
                    {
                        txFifo.Enqueue((byte)val);
                        ProcessTransfer();
                    }
                })
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
    }
    
    private void ProcessTransfer()
    {
        while(txFifo.Count > 0 && rxFifo.Count < FifoSize)
        {
            var txData = txFifo.Dequeue();
            var rxData = Transmit(txData);
            rxFifo.Enqueue(rxData);
        }
    }
    
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
    {
        Control = 0x00,
        Data = 0x04,
        Status = 0x08
    }
}