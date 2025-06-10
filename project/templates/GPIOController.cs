public class GPIOController : IDoubleWordPeripheral, IKnownSize, INumberedGPIOOutput
{
    public GPIOController(Machine machine) : base(machine)
    {
        pins = new GPIO[NumberOfPins];
        for(var i = 0; i < NumberOfPins; i++)
        {
            pins[i] = new GPIO();
        }
        
        registers = new DoubleWordRegistersCollection(this);
        DefineRegisters();
        Reset();
    }
    
    public override void Reset()
    {
        registers.Reset();
        pinDirection = 0;
        pinData = 0;
        UpdatePins();
    }
    
    public uint ReadDoubleWord(long offset)
    {
        return registers.Read(offset);
    }
    
    public void WriteDoubleWord(long offset, uint value)
    {
        registers.Write(offset, value);
    }
    
    public IReadOnlyDictionary<int, IGPIO> Connections
    {
        get
        {
            var result = new Dictionary<int, IGPIO>();
            for(var i = 0; i < NumberOfPins; i++)
            {
                result[i] = pins[i];
            }
            return result;
        }
    }
    
    public long Size => 0x100;
    
    private void DefineRegisters()
    {
        Registers.Data.Define(this)
            .WithValueField(0, 31, name: "DATA",
                valueProviderCallback: _ => pinData,
                writeCallback: (_, val) => 
                {
                    pinData = (uint)val;
                    UpdatePins();
                });
                
        Registers.Direction.Define(this)
            .WithValueField(0, 31, name: "DIR",
                valueProviderCallback: _ => pinDirection,
                writeCallback: (_, val) => 
                {
                    pinDirection = (uint)val;
                    UpdatePins();
                });
    }
    
    private void UpdatePins()
    {
        for(var i = 0; i < NumberOfPins; i++)
        {
            if((pinDirection & (1u << i)) != 0) // Output
            {
                pins[i].Set((pinData & (1u << i)) != 0);
            }
        }
    }
    
    private uint pinDirection;
    private uint pinData;
    private readonly GPIO[] pins;
    private readonly DoubleWordRegistersCollection registers;
    
    private const int NumberOfPins = 32;
    
    private enum Registers
    {
        Data = 0x00,
        Direction = 0x04,
        // Add more registers as needed
    }
}