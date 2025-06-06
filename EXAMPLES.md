# Examples and Tutorials

This guide provides step-by-step tutorials and examples for using the Renode Peripheral Model Generator.

## Table of Contents

- [Tutorial: Generating a GPIO Peripheral](#tutorial-generating-a-gpio-peripheral)
- [Example Queries](#example-queries)
- [Integration Examples](#integration-examples)
- [Advanced Usage Scenarios](#advanced-usage-scenarios)
- [Tips and Best Practices](#tips-and-best-practices)

## Tutorial: Generating a GPIO Peripheral

This tutorial walks through generating a complete GPIO peripheral model from scratch.

### Step 1: Prepare Your Environment

```bash
# Ensure Milvus is running
docker ps | grep milvus

# Test connections
cd project
python main.py test-connection
```

Expected output:

```
Testing Milvus connection...
✓ Milvus connected
  Collection: peripheral_documentation
  Documents: 1523

Testing LLM connection...
✓ LLM connected
  Model: gpt-4
```

### Step 2: Generate the GPIO Peripheral

Run the generation command:

```bash
python main.py generate "Create a GPIO peripheral with 32 pins, interrupt support, and configurable pull-up/pull-down resistors"
```

### Step 3: Monitor Generation Progress

The generator will show progress through each stage:

```
Query: Create a GPIO peripheral with 32 pins, interrupt support...
Output: output/generation_20240106_143022

[====================================] Retrieving relevant documentation...
[====================================] Generating peripheral model...
  ✓ Context gathering
  ✓ TODO generation
  ✓ Interface definition
  ✓ Implementation
  ✓ Test generation
  ✓ Final assembly
```

### Step 4: Review Generated Files

Check the output directory:

```bash
ls -la output/generation_20240106_143022/
```

Files generated:

- `GPIOController.cs` - Main implementation
- `validation_report.json` - Validation results
- `README.md` - Documentation
- `integration_instructions.md` - Integration guide
- `GPIOController_package.zip` - Complete package

### Step 5: Examine the Generated Code

```csharp
// GPIOController.cs
using System;
using System.Collections.Generic;
using Antmicro.Renode.Core;
using Antmicro.Renode.Core.Structure.Registers;
using Antmicro.Renode.Peripherals.Bus;
using Antmicro.Renode.Logging;

namespace Antmicro.Renode.Peripherals.GPIO
{
    public class GPIOController : BasicDoubleWordPeripheral, IGPIOReceiver
    {
        public GPIOController(Machine machine) : base(machine)
        {
            DefineRegisters();
            InitializePins();
        }

        // ... implementation details ...
    }
}
```

### Step 6: Validate the Model

```bash
python main.py validate output/generation_20240106_143022/GPIOController.cs
```

Expected output:

```
Validation Status: ✓ VALID
Overall Score: 92.5/100

Check               Status  Score  Details
naming_conventions  ✓       100    All naming conventions followed
renode_patterns     ✓       95     Follows Renode design patterns
error_handling      ✓       90     Proper error handling implemented
documentation       ✓       85     Well documented code
```

### Step 7: Integrate into Renode

1. Copy the generated file to your Renode peripherals directory:

   ```bash
   cp output/generation_*/GPIOController.cs /path/to/renode/peripherals/GPIO/
   ```

2. Add to your platform file (`.repl`):

   ```
   gpio: GPIOController @ sysbus 0x40020000
       -> gic@[16-47]  // Connect 32 interrupt lines
   ```

3. Test in Renode:

   ```python
   # In Renode monitor
   mach create
   machine LoadPlatformDescription @your_platform.repl

   # Test GPIO operations
   sysbus.gpio WriteDoubleWord 0x0 0xFFFFFFFF  # Set all pins high
   sysbus.gpio ReadDoubleWord 0x8              # Read input register
   ```

## Example Queries

### Basic Peripheral Queries

1. **Simple UART**

   ```bash
   python main.py generate "Create a basic UART peripheral with 8-bit data, configurable baud rate"
   ```

2. **Timer with PWM**

   ```bash
   python main.py generate "Generate a 32-bit timer peripheral with PWM output capability and prescaler"
   ```

3. **SPI Controller**
   ```bash
   python main.py generate "Create an SPI master controller with DMA support and 4 chip selects"
   ```

### Documentation-Based Queries

1. **From Specific Chapter**

   ```bash
   python main.py generate "Create a peripheral model based on Chapter 19 eQADC from MPC5554 reference manual"
   ```

2. **With Register Details**

   ```bash
   python main.py generate "Generate an I2C controller with registers at 0x00 (Control), 0x04 (Status), 0x08 (Data), supporting 100kHz and 400kHz modes"
   ```

3. **Complex Peripheral**
   ```bash
   python main.py generate "Create an Ethernet MAC controller based on MPC5554 FEC chapter with MII interface and buffer descriptors"
   ```

### Interactive Mode Examples

```bash
# Start interactive generation
python main.py generate --interactive

# You'll be prompted at each step:
Query: Create a CAN controller with message filtering
Proceed with generation? [y/n]: y

Step 1: Context Gathering
Retrieved 15 relevant documents. Continue? [y/n]: y

Step 2: TODO Generation
Generated 12 implementation tasks. Review? [y/n]: y
...
```

## Integration Examples

### Example 1: Adding to an Existing Platform

```python
# platform.repl
cpu: CPU.CortexM4 @ sysbus
    cpuType: "cortex-m4"
    nvic: nvic

nvic: NVIC @ sysbus 0xE000E000
    -> cpu@0

// Add generated peripheral
gpio: GPIOController @ sysbus 0x40020000
    numberOfPins: 32
    -> nvic@[16-47]

// Configure initial state
gpio:
    PullUpEnabled: 0xFFFF0000    // Upper 16 pins have pull-up
    InterruptEnabled: 0x0000000F  // First 4 pins generate interrupts
```

### Example 2: Connecting Peripherals

```python
# Connect UART to GPIO for testing
uart: UARTController @ sysbus 0x40011000
    -> nvic@35

gpio: GPIOController @ sysbus 0x40020000
    16 -> uart@0  // GPIO pin 16 connected to UART RX

// In monitor:
sysbus.gpio TogglePin 16  // Simulate input to UART
```

### Example 3: Custom Configuration

```python
# Create custom peripheral with specific features
timer: TimerController @ sysbus 0x40000000
    frequency: 1000000  // 1MHz
    numberOfChannels: 4
    -> nvic@[25-28]

// Configure channels
timer:
    Channel0Mode: "PWM"
    Channel1Mode: "InputCapture"
    Channel2Mode: "OutputCompare"
    Channel3Mode: "PWM"
```

## Advanced Usage Scenarios

### Scenario 1: Batch Generation

Generate multiple peripherals from a specification file:

```bash
# peripherals.txt
Create a UART controller with DMA support
Create a 16-channel ADC with 12-bit resolution
Create an I2C slave peripheral with address filtering

# Run batch generation
while read query; do
    python main.py generate "$query" --output batch_output/
done < peripherals.txt
```

### Scenario 2: Custom Templates

Use custom templates for specific peripheral types:

```bash
# Export existing templates
python main.py export-templates --output my_templates/

# Modify templates
vim my_templates/gpio_template.cs

# Use custom template directory
export CUSTOM_TEMPLATE_DIR=my_templates/
python main.py generate "Create GPIO based on custom template"
```

### Scenario 3: Validation and Fixing

Validate and automatically fix existing peripherals:

```bash
# Validate all peripherals in a directory
for file in peripherals/*.cs; do
    echo "Validating $file..."
    python main.py validate "$file" --fix
done

# Generate validation report
python main.py validate peripherals/ --report validation_summary.html
```

### Scenario 4: Documentation Extraction

Extract and index custom documentation:

```python
# index_docs.py
from milvus_rag_handler import MilvusRAGHandler

handler = MilvusRAGHandler()

# Index custom documentation
handler.index_documents([
    {
        'content': open('custom_peripheral_spec.txt').read(),
        'source': 'custom_spec',
        'metadata': {'type': 'specification', 'version': '1.0'}
    }
])

# Now generate based on indexed docs
```

## Tips and Best Practices

### 1. Query Formulation

**Good Queries:**

- ✅ "Create a UART peripheral with 16-byte FIFO, 9-bit mode support, and hardware flow control"
- ✅ "Generate a timer based on STM32F4 TIM1 with 4 capture/compare channels"
- ✅ "Build an ADC controller with 8 channels, 12-bit resolution, and DMA support"

**Poor Queries:**

- ❌ "Make a UART" (too vague)
- ❌ "Create the best peripheral ever" (not specific)
- ❌ "Generate something like Arduino" (unclear requirements)

### 2. Performance Optimization

```yaml
# config.yaml optimizations for faster generation
pipeline:
  parallel:
    enabled: true
    max_workers: 4

cache:
  response_cache:
    enabled: true
    max_size: 5000

models:
  temperature_defaults:
    code_generation: 0.1 # Lower temperature for consistent code
```

### 3. Debugging Generation Issues

```bash
# Enable debug mode
export DEBUG_MODE=true
export SAVE_INTERMEDIATES=true

# Run with verbose logging
python main.py generate "your query" --verbose

# Check intermediate files
ls -la debug/intermediates/
```

### 4. Model Selection Strategy

```yaml
# Optimize model selection for your use case
models:
  preferences:
    # For embedded peripherals
    analysis: "gpt-4"              # Best understanding
    code_generation: "claude-3-opus" # Best code quality

    # For simple peripherals
    analysis: "gpt-3.5-turbo"      # Faster, cheaper
    code_generation: "gpt-4"       # Good balance
```

### 5. Validation Customization

```yaml
# Strict validation for production
validation:
  strict_mode: true
  thresholds:
    min_test_coverage: 95
    max_complexity_score: 30

  custom_rules:
    - name: "memory_safety"
      pattern: "unsafe|fixed|pointer"
      severity: "error"
      message: "Unsafe code patterns detected"
```

### 6. Integration Testing

```python
# test_peripheral.robot
*** Settings ***
Library    Renode

*** Test Cases ***
Test GPIO Interrupts
    Create Machine
    Load Platform    ${CURDIR}/platform.repl

    # Configure GPIO
    Execute Command    sysbus.gpio InterruptEnabled 0x1

    # Trigger interrupt
    Execute Command    sysbus.gpio TogglePin 0

    # Verify interrupt fired
    Should Contain    ${LOG}    GPIO interrupt on pin 0
```

### 7. Continuous Improvement

```bash
# Track generation accuracy
python main.py show-metrics

# Update knowledge base
python main.py update-knowledge --source https://github.com/renode/renode

# Retrain with feedback
python main.py train --feedback-dir user_feedback/
```

## Common Patterns

### Pattern 1: Register Definition

```csharp
private void DefineRegisters()
{
    Registers.Control.Define(this)
        .WithFlag(0, out enableFlag, name: "EN")
        .WithFlag(1, out interruptEnable, name: "IE")
        .WithReservedBits(2, 30);

    Registers.Status.Define(this)
        .WithFlag(0, FieldMode.Read, valueProviderCallback: _ => busy, name: "BUSY")
        .WithFlag(1, out interruptFlag, FieldMode.Read | FieldMode.WriteOneToClear, name: "IF")
        .WithReservedBits(2, 30);
}
```

### Pattern 2: Interrupt Handling

```csharp
private void UpdateInterrupts()
{
    var shouldTrigger = interruptEnable.Value && interruptFlag.Value;
    IRQ.Set(shouldTrigger);
}
```

### Pattern 3: DMA Integration

```csharp
public void ConfigureDMA(IDMA dma, int channel)
{
    this.dmaEngine = dma;
    this.dmaChannel = channel;

    dmaEngine.OnTransferCompleted += (sender, e) =>
    {
        if (e.Channel == dmaChannel)
        {
            HandleDMAComplete();
        }
    };
}
```

## Troubleshooting Examples

### Issue 1: Generation Timeout

```bash
# Increase timeouts
export REQUEST_TIMEOUT=300

# Or modify config
vim config.yaml
# pipeline.timeouts.implementation: 300
```

### Issue 2: Validation Failures

```bash
# Get detailed validation report
python main.py validate peripheral.cs --verbose --output report.html

# Common fixes:
# - Add missing using statements
# - Implement required interfaces
# - Add proper error handling
```

### Issue 3: Integration Problems

```python
# Debug in Renode
(monitor) logLevel 3 sysbus.gpio
(monitor) sysbus.gpio DebugLog true

# Watch register access
(monitor) watch sysbus.gpio 0x0 0x100
```

## Next Steps

1. **Explore Templates**: Check `renode_knowledge/` for example implementations
2. **Customize Generation**: Modify `config.yaml` for your needs
3. **Contribute**: Share your generated peripherals and improvements
4. **Get Help**: Use `--help` flag or check documentation

Remember: The quality of generated code depends on the specificity and clarity of your queries. Take time to formulate detailed requirements for best results.
