public class DMAController : IDoubleWordPeripheral, IKnownSize, IIRQSender, IDMAEngine
{
    public DMAController(Machine machine) : base(machine)
    {
        IRQ = new GPIO();
        channels = new DMAChannel[NumberOfChannels];
        for(var i = 0; i < NumberOfChannels; i++)
        {
            channels[i] = new DMAChannel(i, this);
        }
        
        registers = new DoubleWordRegistersCollection(this);
        DefineRegisters();
        Reset();
    }
    
    public override void Reset()
    {
        registers.Reset();
        foreach(var channel in channels)
        {
            channel.Reset();
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
    
    public void RequestTransfer(int channel, DMARequest request)
    {
        if(channel < 0 || channel >= NumberOfChannels)
        {
            this.Log(LogLevel.Warning, "Invalid DMA channel: {0}", channel);
            return;
        }
        
        channels[channel].StartTransfer(request);
    }
    
    public GPIO IRQ { get; private set; }
    public long Size => 0x1000;
    
    private void DefineRegisters()
    {
        // Global control register
        Registers.Control.Define(this)
            .WithFlag(0, name: "ENABLE",
                writeCallback: (_, val) => dmaEnabled = val)
            .WithReservedBits(1, 31);
            
        // Channel registers
        for(var i = 0; i < NumberOfChannels; i++)
        {
            var channelOffset = 0x100 + (i * 0x20);
            var channel = channels[i];
            
            // Source address
            ((Registers)(channelOffset + 0x00)).Define(this)
                .WithValueField(0, 31, name: $"CH{i}_SRC",
                    writeCallback: (_, val) => channel.SourceAddress = val);
                    
            // Destination address
            ((Registers)(channelOffset + 0x04)).Define(this)
                .WithValueField(0, 31, name: $"CH{i}_DST",
                    writeCallback: (_, val) => channel.DestinationAddress = val);
                    
            // Transfer count
            ((Registers)(channelOffset + 0x08)).Define(this)
                .WithValueField(0, 31, name: $"CH{i}_COUNT",
                    writeCallback: (_, val) => channel.TransferCount = val);
                    
            // Channel control
            ((Registers)(channelOffset + 0x0C)).Define(this)
                .WithFlag(0, name: $"CH{i}_ENABLE",
                    writeCallback: (_, val) => channel.Enabled = val)
                .WithFlag(1, name: $"CH{i}_INT_ENABLE",
                    writeCallback: (_, val) => channel.InterruptEnabled = val)
                .WithFlag(2, FieldMode.WriteOneToClear, name: $"CH{i}_INT_FLAG",
                    writeCallback: (_, val) =>
                    {
                        if(val) channel.ClearInterrupt();
                        UpdateInterrupts();
                    })
                .WithReservedBits(3, 29);
        }
    }
    
    private void UpdateInterrupts()
    {
        var anyInterrupt = channels.Any(ch => ch.InterruptPending);
        IRQ.Set(anyInterrupt);
    }
    
    private bool dmaEnabled;
    private readonly DMAChannel[] channels;
    private readonly DoubleWordRegistersCollection registers;
    
    private const int NumberOfChannels = 8;
    
    private enum Registers
    {
        Control = 0x00,
        Status = 0x04,
        // Channel registers start at 0x100
    }
    
    private class DMAChannel
    {
        public DMAChannel(int index, DMAController parent)
        {
            this.index = index;
            this.parent = parent;
        }
        
        public void Reset()
        {
            SourceAddress = 0;
            DestinationAddress = 0;
            TransferCount = 0;
            Enabled = false;
            InterruptEnabled = false;
            InterruptPending = false;
        }
        
        public void StartTransfer(DMARequest request)
        {
            if(!Enabled || TransferCount == 0)
            {
                return;
            }
            
            // Perform transfer
            parent.machine.SystemBus.CopyMemory(
                SourceAddress,
                DestinationAddress,
                TransferCount);
                
            // Update status
            if(InterruptEnabled)
            {
                InterruptPending = true;
                parent.UpdateInterrupts();
            }
        }
        
        public void ClearInterrupt()
        {
            InterruptPending = false;
        }
        
        public uint SourceAddress { get; set; }
        public uint DestinationAddress { get; set; }
        public uint TransferCount { get; set; }
        public bool Enabled { get; set; }
        public bool InterruptEnabled { get; set; }
        public bool InterruptPending { get; set; }
        
        private readonly int index;
        private readonly DMAController parent;
    }
}