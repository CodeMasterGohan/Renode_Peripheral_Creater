public class UARTController : IDoubleWordPeripheral, IKnownSize, IUART, IIRQSender
{
    public UARTController(Machine machine) : base(machine)
    {
        IRQ = new GPIO();
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
        UpdateInterrupts();
    }
    
    public void WriteChar(byte value)
    {
        if(rxFifo.Count < FifoSize)
        {
            rxFifo.Enqueue(value);
            UpdateInterrupts();
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
    
    public event Action<byte> CharReceived;
    
    public GPIO IRQ { get; private set; }
    public long Size => 0x100;
    public uint BaudRate { get; set; } = 115200;
    public Bits StopBits { get; set; } = Bits.One;
    public Parity ParityBit { get; set; } = Parity.None;
    
    private void DefineRegisters()
    {
        Registers.Data.Define(this)
            .WithValueField(0, 7, name: "DATA",
                valueProviderCallback: _ => 
                {
                    if(rxFifo.Count > 0)
                    {
                        var data = rxFifo.Dequeue();
                        UpdateInterrupts();
                        return data;
                    }
                    return 0;
                },
                writeCallback: (_, val) => 
                {
                    if(txFifo.Count < FifoSize)
                    {
                        txFifo.Enqueue((byte)val);
                        CharReceived?.Invoke((byte)val);
                        UpdateInterrupts();
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
            .WithReservedBits(4, 28);
            
        Registers.Control.Define(this)
            .WithFlag(0, name: "TX_ENABLE",
                writeCallback: (_, val) => txEnabled = val)
            .WithFlag(1, name: "RX_ENABLE",
                writeCallback: (_, val) => rxEnabled = val)
            .WithFlag(2, name: "TX_INT_ENABLE",
                writeCallback: (_, val) => 
                {
                    txInterruptEnabled = val;
                    UpdateInterrupts();
                })
            .WithFlag(3, name: "RX_INT_ENABLE",
                writeCallback: (_, val) => 
                {
                    rxInterruptEnabled = val;
                    UpdateInterrupts();
                })
            .WithReservedBits(4, 28);
    }
    
    private void UpdateInterrupts()
    {
        var txInt = txInterruptEnabled && txFifo.Count < FifoSize / 2;
        var rxInt = rxInterruptEnabled && rxFifo.Count > 0;
        IRQ.Set(txInt || rxInt);
    }
    
    private bool txEnabled;
    private bool rxEnabled;
    private bool txInterruptEnabled;
    private bool rxInterruptEnabled;
    private readonly Queue<byte> txFifo;
    private readonly Queue<byte> rxFifo;
    private readonly DoubleWordRegistersCollection registers;
    
    private const int FifoSize = 16;
    
    private enum Registers
    {
        Data = 0x00,
        Status = 0x04,
        Control = 0x08,
        BaudRate = 0x0C
    }
}