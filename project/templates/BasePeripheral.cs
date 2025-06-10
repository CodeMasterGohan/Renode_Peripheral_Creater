namespace YourNamespace
{
    public class BasePeripheral : IDoubleWordPeripheral, IKnownSize, IIRQSender
    {
        public BasePeripheral(Machine machine) : base(machine)
        {
            IRQ = new GPIO();
            registers = new DoubleWordRegistersCollection(this);
            DefineRegisters();
            Reset();
        }
        
        public override void Reset()
        {
            registers.Reset();
            // Add custom reset logic here
        }
        
        public uint ReadDoubleWord(long offset)
        {
            return registers.Read(offset);
        }
        
        public void WriteDoubleWord(long offset, uint value)
        {
            registers.Write(offset, value);
        }
        
        public long Size => 0x1000; // Adjust based on peripheral
        
        public GPIO IRQ { get; private set; }
        
        private void DefineRegisters()
        {
            // Register definitions go here
        }
        
        private DoubleWordRegistersCollection registers;
        
        private enum Registers
        {
            // Register offsets
        }
    }
}