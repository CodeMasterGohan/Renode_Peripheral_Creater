# Renode Peripheral Templates

This directory contains 8 peripheral templates that can be used as starting points for creating new Renode peripherals.

## Available Templates

- **BasePeripheral** - Base template for a Renode peripheral)
- **GPIOController** - GPIO controller with pin management)
- **TimerPeripheral** - Timer peripheral)
- **UARTController** - UART controller)
- **DMAController** - DMA controller)
- **InterruptController** - Interrupt controller)
- **SPIController** - SPI controller)
- **I2CController** - I2C controller)

## Usage

1. Choose a template that matches your peripheral type
2. Copy the template file and rename it
3. Modify the class name and namespace
4. Implement the specific functionality for your peripheral
5. Add appropriate registers and logic

## Template Structure

Each template includes:
- Basic peripheral structure
- Common register implementations
- Interrupt handling (where applicable)
- Logging setup
- Documentation comments

## Customization Tips

- Replace TODO comments with actual implementation
- Add peripheral-specific registers
- Implement proper reset behavior
- Add validation for register values
- Include appropriate logging

## Contributing

To add new templates, ensure they follow the established patterns and include comprehensive documentation.
