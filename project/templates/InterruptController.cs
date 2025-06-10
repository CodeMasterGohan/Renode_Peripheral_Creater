public class InterruptController : IDoubleWordPeripheral, IKnownSize, IIRQController
{
    public InterruptController(Machine machine) : base(machine)
    {
        IRQ = new GPIO();
        sources = new InterruptSource[NumberOfSources];
        for(var i = 0; i < NumberOfSources; i++)
        {
            sources[i] = new InterruptSource(i);
        }
        
        registers = new DoubleWordRegistersCollection(this);
        DefineRegisters();
        Reset();
    }
    
    public override void Reset()
    {
        registers.Reset();
        foreach(var source in sources)
        {
            source.Reset();
        }
        UpdateInterrupts();
    }
    
    public uint ReadDoubleWord(long offset)
    {
        return registers.Read(offset);
    }
    
    public void WriteDoubleWord(long offset, uint value)
    {
        registers.Write(offset, value);
    }
    
    public void OnGPIO(int number, bool value)
    {
        if(number < 0 || number >= NumberOfSources)
        {
            this.Log(LogLevel.Warning, "Invalid interrupt source: {0}", number);
            return;
        }
        
        sources[number].Pending = value;
        UpdateInterrupts();
    }
    
    public GPIO IRQ { get; private set; }
    public long Size => 0x1000;
    
    private void DefineRegisters()
    {
        // Interrupt enable register
        Registers.Enable.Define(this)
            .WithValueField(0, 31, name: "ENABLE",
                writeCallback: (_, val) =>
                {
                    for(var i = 0; i < Math.Min(32, NumberOfSources); i++)
                    {
                        sources[i].Enabled = ((val >> i) & 1) != 0;
                    }
                    UpdateInterrupts();
                });
                
        // Interrupt pending register
        Registers.Pending.Define(this)
            .WithValueField(0, 31, FieldMode.Read, name: "PENDING",
                valueProviderCallback: _ =>
                {
                    uint pending = 0;
                    for(var i = 0; i < Math.Min(32, NumberOfSources); i++)
                    {
                        if(sources[i].Pending)
                        {
                            pending |= (1u << i);
                        }
                    }
                    return pending;
                });
                
        // Priority registers
        for(var i = 0; i < NumberOfSources; i++)
        {
            var source = sources[i];
            ((Registers)(0x100 + i * 4)).Define(this)
                .WithValueField(0, 7, name: $"PRIORITY_{i}",
                    writeCallback: (_, val) => source.Priority = (byte)val)
                .WithReservedBits(8, 24);
        }
    }
    
    private void UpdateInterrupts()
    {
        var activeInterrupt = sources
            .Where(s => s.Enabled && s.Pending)
            .OrderByDescending(s => s.Priority)
            .FirstOrDefault();
            
        IRQ.Set(activeInterrupt != null);
    }
    
    private readonly InterruptSource[] sources;
    private readonly DoubleWordRegistersCollection registers;
    
    private const int NumberOfSources = 32;
    
    private enum Registers
    {
        Enable = 0x00,
        Pending = 0x04,
        // Priority registers start at 0x100
    }
    
    private class InterruptSource
    {
        public InterruptSource(int index)
        {
            this.index = index;
        }
        
        public void Reset()
        {
            Enabled = false;
            Pending = false;
            Priority = 0;
        }
        
        public bool Enabled { get; set; }
        public bool Pending { get; set; }
        public byte Priority { get; set; }
        
        private readonly int index;
    }
}