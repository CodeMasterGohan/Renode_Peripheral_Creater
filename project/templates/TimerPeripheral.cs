public class TimerPeripheral : IDoubleWordPeripheral, IKnownSize, IIRQSender
{
    public TimerPeripheral(Machine machine, long frequency = 1000000) : base(machine)
    {
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
    }
    
    public override void Reset()
    {
        registers.Reset();
        timer.Reset();
        prescaler = 1;
        UpdateTimerFrequency();
    }
    
    public uint ReadDoubleWord(long offset)
    {
        return registers.Read(offset);
    }
    
    public void WriteDoubleWord(long offset, uint value)
    {
        registers.Write(offset, value);
    }
    
    public GPIO IRQ { get; private set; }
    public long Size => 0x100;
    
    private void DefineRegisters()
    {
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
                {
                    prescaler = (uint)val + 1;
                    UpdateTimerFrequency();
                })
            .WithReservedBits(16, 16);
            
        Registers.Status.Define(this)
            .WithFlag(0, FieldMode.WriteOneToClear, name: "INTERRUPT_FLAG",
                writeCallback: (_, val) => 
                {
                    if(val) 
                    {
                        interruptPending = false;
                        UpdateInterrupt();
                    }
                })
            .WithReservedBits(1, 31);
    }
    
    private void OnTimerLimitReached()
    {
        if(oneShot)
        {
            timer.Enabled = false;
        }
        
        interruptPending = true;
        UpdateInterrupt();
    }
    
    private void UpdateInterrupt()
    {
        IRQ.Set(interruptEnabled && interruptPending);
    }
    
    private void UpdateTimerFrequency()
    {
        timer.Frequency = frequency / prescaler;
    }
    
    private bool interruptEnabled;
    private bool interruptPending;
    private bool oneShot;
    private uint prescaler;
    private readonly long frequency;
    private readonly LimitTimer timer;
    private readonly DoubleWordRegistersCollection registers;
    
    private enum Registers
    {
        Control = 0x00,
        Value = 0x04,
        Reload = 0x08,
        Prescaler = 0x0C,
        Status = 0x10
    }
}