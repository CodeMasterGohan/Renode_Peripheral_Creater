### Chatper 11 Frequency Modulated Phase Locked Loop (FMPLL) and System Clocks

## 11.1 Introduction

This section describes the features and function of the FMPLL module.

## 11.1.1 Block Diagrams

This section contains block diagrams that illustrate the FMPLL, the clock architecture, and the various FMPLL and clock configurations that are available on the MPC5553/MPC5554. The following diagrams are provided:

- · Figure 11-1, 'FMPLL and Clock Architecture'
- · Figure 11-2, 'FMPLL Bypass Mode'
- · Figure 11-3, 'FMPLL External Reference Mode'
- · Figure 11-4, 'FMPLL Crystal Reference Mode Without FM'
- · Figure 11-5, 'FMPLL Crystal Reference Mode With FM'
- · Figure 11-6, 'FMPLL Dual-Controller (1:1) Mode'

## 11.1.1.1 FMPLL and Clock Architecture

|   RSTCFG | PLLCFG [0]          | PLLCFG [1]          | Clock Mode            |   MODE |   PLLSEL |   PLLREF |
|----------|---------------------|---------------------|-----------------------|--------|----------|----------|
|        1 | PLLCFG Pins Ignored | PLLCFG Pins Ignored | Crystal Ref (Default) |      1 |        1 |        1 |
|        0 | 0                   | 0                   | Bypass Mode           |      0 |        0 |        0 |
|        0 | 0                   | 1                   | External Ref          |      1 |        1 |        0 |
|        0 | 1                   | 0                   | Crystal Ref           |      1 |        1 |        1 |
|        0 | 1                   | 1                   | 1:1 Mode              |      1 |        0 |        0 |

Figure 11-1. FMPLL Block and Clock Architecture

<!-- image -->

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## 11.1.1.2 FMPLL Bypass Mode

|   RSTCFG | PLLCFG [0]          | PLLCFG [1]          | Clock Mode            |   MODE |   PLLSEL |   PLLREF 1 |
|----------|---------------------|---------------------|-----------------------|--------|----------|------------|
|        1 | PLLCFG Pins Ignored | PLLCFG Pins Ignored | Crystal Ref (Default) |      1 |        1 |          1 |
|        0 | 0                   | 0                   | Bypass Mode           |      0 |        0 |          0 |
|        0 | 0                   | 1                   | External Ref          |      1 |        1 |          0 |
|        0 | 1                   | 0                   | Crystal Ref           |      1 |        1 |          1 |
|        0 | 1                   | 1                   | 1:1 Mode              |      1 |        0 |          0 |

Figure 11-2. FMPLL Bypass Mode

<!-- image -->

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## 11.1.1.3 FMPLL External Reference Mode

|   RSTCFG | PLLCFG [0]          | PLLCFG [1]          | Clock Mode            |   MODE |   PLLSEL |   PLLREF 1 |
|----------|---------------------|---------------------|-----------------------|--------|----------|------------|
|        1 | PLLCFG Pins Ignored | PLLCFG Pins Ignored | Crystal Ref (Default) |      1 |        1 |          1 |
|        0 | 0                   | 0                   | Bypass Mode           |      0 |        0 |          0 |
|        0 | 0                   | 1                   | External Ref          |      1 |        1 |          0 |
|        0 | 1                   | 0                   | Crystal Ref           |      1 |        1 |          1 |
|        0 | 1                   | 1                   | 1:1 Mode              |      1 |        0 |          0 |

Figure 11-3. FMPLL External Reference Mode

<!-- image -->

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## 11.1.1.4 FMPLL Crystal Reference Mode Without FM

|   RSTCFG | PLLCFG [0]          | PLLCFG [1]          | Clock Mode            |   MODE |   PLLSEL |   PLLREF 1 |
|----------|---------------------|---------------------|-----------------------|--------|----------|------------|
|        1 | PLLCFG Pins Ignored | PLLCFG Pins Ignored | Crystal Ref (Default) |      1 |        1 |          1 |
|        0 | 0                   | 0                   | Bypass Mode           |      0 |        0 |          0 |
|        0 | 0                   | 1                   | External Ref          |      1 |        1 |          0 |
|        0 | 1                   | 0                   | Crystal Ref           |      1 |        1 |          1 |
|        0 | 1                   | 1                   | 1:1 Mode              |      1 |        0 |          0 |

Figure 11-4. FMPLL Crystal Reference Mode without FM

<!-- image -->

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## 11.1.1.5 FMPLL Crystal Reference Mode With FM

|   RSTCFG | PLLCFG [0]          | PLLCFG [1]          | Clock Mode            |   MODE |   PLLSEL |   PLLREF 1 |
|----------|---------------------|---------------------|-----------------------|--------|----------|------------|
|        1 | PLLCFG Pins Ignored | PLLCFG Pins Ignored | Crystal Ref (Default) |      1 |        1 |          1 |
|        0 | 0                   | 0                   | Bypass Mode           |      0 |        0 |          0 |
|        0 | 0                   | 1                   | External Ref          |      1 |        1 |          0 |
|        0 | 1                   | 0                   | Crystal Ref           |      1 |        1 |          1 |
|        0 | 1                   | 1                   | 1:1 Mode              |      1 |        0 |          0 |

Figure 11-5. FMPLL Crystal Reference Mode with FM

<!-- image -->

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## 11.1.1.6 FMPLL Dual-Controller Mode (1:1)

|   RSTCFG | PLLCFG [0]          | PLLCFG [1]          | Clock Mode            |   MODE |   PLLSEL |   PLLREF 1 |
|----------|---------------------|---------------------|-----------------------|--------|----------|------------|
|        1 | PLLCFG Pins Ignored | PLLCFG Pins Ignored | Crystal Ref (Default) |      1 |        1 |          1 |
|        0 | 0                   | 0                   | Bypass Mode           |      0 |        0 |          0 |
|        0 | 0                   | 1                   | External Ref          |      1 |        1 |          0 |
|        0 | 1                   | 0                   | Crystal Ref           |      1 |        1 |          1 |
|        0 | 1                   | 1                   | 1:1 Mode              |      1 |        0 |          0 |

Figure 11-6. FMPLL Dual Controller (1:1) Mode

<!-- image -->

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## 11.1.2 Overview

The frequency modulated phase locked loop (FMPLL) allows the user to generate high speed system clocks from an 8 MHz to 20 MHz crystal oscillator or external clock generator. Further, the FMPLL supports programmable frequency modulation of the system clock. The FMPLL multiplication factor, output  clock  divider  ratio,  modulation  depth,  and  modulation  rate  are  all  controllable  through  a  bus interface.

## 11.1.3 Features

The FMPLL has the following major features:

- · Input clock frequency from 8 MHz to 20 MHz
- · Current controlled oscillator (ICO) range from 48 MHz to 132 MHz
- · Reference frequency pre-divider (PREDIV) for finer frequency synthesis resolution
- · Reduced frequency divider (RFD) for reduced frequency operation without forcing the FMPLL to re-lock
- · Four modes of operation:
- - Bypass mode.
- - Crystal reference mode (default mode for MPC5554 and 324 and 416 packages of the MPC5553). Refer to Section 11.1.4.1, 'Crystal Reference (Default Mode).'
- - External reference mode. Refer to Section 11.1.4.2, 'External Reference Mode.'
- - PLL dual-controller (1:1) mode for EXTAL\_EXTCLK to CLKOUT skew minimization.
- · Programmable frequency modulation
- - Modulation enabled/disabled via bus interface
- - Triangle wave modulation
- - Register programmable modulation depth (+/-1%-2% deviation from center frequency)
- - Register programmable modulation frequency dependent on reference frequency
- · Lock detect circuitry reports when the FMPLL has achieved frequency lock and continuously monitors lock status to report loss of lock conditions
- - User-selectable ability to generate an interrupt request upon loss of lock. (See Chapter 10, 'Interrupt Controller (INTC),' for details.)
- - User-selectable ability to generate a system reset upon loss of lock. (See Chapter 4, 'Reset,' for details.)
- · Loss of clock (LOC) detection for reference and feedback clocks
- - User-selectable ability to generate an interrupt request upon loss of clock. (See Chapter 10, 'Interrupt Controller (INTC),' for details.)
- - User-selectable ability to generate a system reset upon loss of clock (See Chapter 4, 'Reset,' for details.)
- · Self-clocked mode (SCM) operation in event of input clock failure

## 11.1.4 FMPLL Modes of Operation

The FMPLL operational mode is configured during reset. For the MPC5554, the FMPLL mode defaults to crystal reference mode. The 324 and 416 package sizes of the MPC5553 also default to crystal reference mode.  For the MPC5554 and the 324 and 416 package sizes of the MPC5553, if the user should desire to change from this mode, the RSTCFG and PLLCFG[0:1] package pins must be driven to the appropriate state for the desired mode from the time RSTOUT asserts until it negates. As shown in Table 11-1, if RSTCFG is not asserted during reset, the state of the PLLCFG package pins is ignored, and the FMPLL will operate in the default crystal reference mode. The table also shows that to enter any other mode RSTCFG must be asserted during reset.

Note that because the 208 package size of the MPC5553 has no RSTCFG pin, after reset the 208 resets to the values of PLLCFG before reset. The device does not reset to the crystal reference mode as do the other MPC5553/MPC5554 packages.

Table 11-1 shows clock mode selection during reset configuration for the MPC5554 and for the 416 and 324 pin packages of the MPC5553. Additional information on reset configuration options for the FMPLL can be found in Chapter 4, 'Reset.'

Table 11-1. Clock Mode Selection in 416 Pin and 324 Pin Packages

| Package Pins   | Package Pins         | Package Pins         | Clock Mode                       | Synthesizer Status Register (FMPLL_SYNSR) 1 Bits   | Synthesizer Status Register (FMPLL_SYNSR) 1 Bits   | Synthesizer Status Register (FMPLL_SYNSR) 1 Bits   |
|----------------|----------------------|----------------------|----------------------------------|----------------------------------------------------|----------------------------------------------------|----------------------------------------------------|
| RSTCFG         | PLLCFG[0]            | PLLCFG[1]            | Clock Mode                       | MODE                                               | PLLSEL                                             | PLLREF                                             |
| 1              | PLLCFG pins ignored. | PLLCFG pins ignored. | Crystal reference (default mode) | 1                                                  | 1                                                  | 1                                                  |
| 0              | 1                    | 0                    | Crystal reference (default mode) | 1                                                  | 1                                                  | 1                                                  |
| 0              | 0                    | 1                    | External reference               | 1                                                  | 1                                                  | 0                                                  |
| 0              | 0                    | 0                    | Bypass Mode                      | 0                                                  | 0                                                  | 0                                                  |
| 0              | 1                    | 1                    | Dual-Controller Mode             | 1                                                  | 0                                                  | 0                                                  |

1 See Section 11.3.1.2, 'Synthesizer Status Register (FMPLL\_SYNSR)' for more information on these bits.

Table 11-2 shows clock mode selection for the MPC5553 208 pin package.

Table 11-2. Clock Mode Selection in 208 Pin Package

| Package Pins   | Package Pins   | Clock Mode         | Synthesizer Status Register (FMPLL_SYNSR) 1 Bits   | Synthesizer Status Register (FMPLL_SYNSR) 1 Bits   | Synthesizer Status Register (FMPLL_SYNSR) 1 Bits   |
|----------------|----------------|--------------------|----------------------------------------------------|----------------------------------------------------|----------------------------------------------------|
| PLLCFG[0]      | PLLCFG[1]      | Clock Mode         | MODE                                               | PLLSEL                                             | PLLREF                                             |
| 1              | 0              | Crystal Reference  | 1                                                  | 1                                                  | 1                                                  |
| 0              | 1              | External Reference | 1                                                  | 1                                                  | 0                                                  |
| 0              | 0              | Bypass             | 0                                                  | 0                                                  | 0                                                  |
| 1              | 1              | Dual-Controller    | 1                                                  | 0                                                  | 0                                                  |

- 1 See Section 11.3.1.2, 'Synthesizer Status Register (FMPLL\_SYNSR)' for more information on these bits.

## 11.1.4.1 Crystal Reference (Default Mode)

In  crystal  reference  mode,  the  FMPLL  receives  an  input  clock  frequency  (EXTAL)  from  the  crystal oscillator circuit (and, in the MPC5553, the pre-divider) and multiplies the frequency to create the FMPLL output clock. The user must supply a crystal oscillator that is within the appropriate input frequency range, the crystal manufacture's recommended external support circuitry, and short signal route from the MCU to the crystal.

The external  support  circuitry  for  the  crystal  oscillator  is  shown  in  Figure 11-7.  Example  component values are shown as well. Note that the actual circuit should be reviewed with the crystal manufacturer. A block diagram illustrating crystal reference mode is shown in Figure 11-4.

Figure 11-7. Crystal Oscillator Network

<!-- image -->

In crystal reference mode, the FMPLL can generate a frequency modulated clock or a non-modulated clock (locked on a single frequency). The modulation rate, modulation depth, output clock divide ratio (RFD), and whether the FMPLL is modulating or not can be programmed by writing to the FMPLL registers. Crystal reference is the default clock mode for the MPC5554 and the 324 and 416 packages of the MPC5553. It is not necessary to force PLLCFG[0:1] to enter this mode. In the 208 package size, because it has no RSTCFG pin, the crystal reference mode can only be selected through the PLLCFG pins.

## 11.1.4.2 External Reference Mode

This external reference mode functions the same as crystal reference mode except that EXTAL\_EXTCLK is driven by an external clock generator rather than a crystal oscillator. Also, the input frequency range in external reference mode is the same as in the crystal reference mode. To enter external clock mode, the default FMPLL configuration must be overridden by following the procedure outlined in Section 11.1.4, 'FMPLL  Modes  of  Operation.'    A  block  diagram  illustrating  external  reference  mode  is  shown  in Figure 11-3.

## NOTE

In addition to supplying power for the CLKOUT signal, when the FMPLL is  configured  for  external  clock  mode  of  operation,  the  V DDE5  supply voltage also controls the voltage level at which the signal presented to the EXTAL\_EXTCLK  pin  causes  a  switch  in  the  clock  logic  levels.  The EXTAL\_EXTCLK will accept a clock source with a voltage range of 1.6V to  3.6V,  however  the  transition  voltage  is  determined  by  V DDE5   supply voltage divided by 2. As an example, if V DDE5  is 3.3V, then the clock will transition at approximately 1.6V. The V DDE5  supply voltage and the voltage level of the external clock reference must be compatible, or the device will not clock properly.

## 11.1.4.3 Bypass Mode

In FMPLL bypass mode, the FMPLL is completely bypassed and the user must supply an external clock on the EXTAL\_EXTCLK pin. The external clock is used directly to produce the internal system clocks. In bypass mode, the analog portion of the FMPLL is disabled and no clocks are generated at the FMPLL output. Consequently, frequency modulation is not available. In bypass mode the pre-divider is bypassed and has no effect on the system clock.

To enter bypass mode, the default FMPLL configuration must be overridden by following the procedure outlined in Section 11.1.4, 'FMPLL Modes of Operation.' A block diagram illustrating bypass mode is shown in Figure 11-2.

## 11.1.4.4 Dual-Controller Mode (1:1)

FMPLL dual-controller mode is used by the slave MCU device of a dual-controller system. The slave FMPLL will facilitate skew reduction between the input and output clock signals. To enter dual-controller mode, the default FMPLL configuration must be overridden by the procedure outlined in Section 11.1.4, 'FMPLL Modes of Operation.'

In this mode, the system clock runs at twice the frequency of the EXTAL\_EXTCLK input pin and is phase aligned. Note that crystal operation is not supported in dual-controller mode and an external clock must be provided.  In  this  mode,  the  frequency  and  phase  of  the  signal  at  the  EXTAL\_EXTCLK  pin  and  the CLKOUT pin of the slave MCU are matched. A block diagram illustrating dual-controller mode (1:1) is shown in Figure 11-6.

Frequency modulation is not available when configured for dual-controller mode for both the master and slave devices. Enabling frequency modulation on the device supplying the reference clock to the slave in dual-controller mode will produce unreliable clocks on the slave.

## NOTE

When configured for dual-controller mode, the CLKOUT clock divider on the slave device must not be changed from its reset state of divide-by-2. Increasing or decreasing this divide ratio will produce unpredictable results from the FMPLL.

## 11.2 External Signal Description

Table 11-3 lists external signals used by the FMPLL during normal operation.

## Table 11-3. PLL External Pin Interface

| Name            | I/O Type   | Function                                               | Pull   |
|-----------------|------------|--------------------------------------------------------|--------|
| PLLCFG0_GPIO208 | I/O        | Configures the mode during reset. GPIO used otherwise. | Up     |
| PLLCFG1_GPIO209 | I/O        | Configures the mode during reset. GPIO used otherwise. | Up     |
| XTAL            | Output     | Output drive for external crystal                      | -      |
| EXTAL_EXTCLK    | Input      | Crystal/external clock input                           | -      |
| V DDSYN         | Power      | Analog power supply (3.3V +/-10%)                      | -      |
| V SSSYN         | Ground     | Analog ground                                          | -      |

## 11.3 Memory Map/Register Definition

Table 11-4 shows the FMPLL memory map locations.

## Table 11-4. FMPLL Module Memory Map

| Address            | Register Name   | Register Description         | Size (bits)   |
|--------------------|-----------------|------------------------------|---------------|
| Base (0xC3F8_0000) | FMPLL_SYNCR     | Synthesizer control register | 32            |
| Base + 0x04        | FMPLL_SYNSR     | Synthesizer status register  | 32            |
| Base + 0x08        | -               | Reserved                     | -             |
| Base + 0x0C        | -               | Reserved                     | -             |
| Base + 0x10        | -               | Reserved                     | -             |
| Base + 0x14        | -               | Reserved                     | -             |
| Base + 0x18        | -               | Reserved                     | -             |
| Base + 0x1C        | -               | Reserved                     | -             |

## 11.3.1 Register Descriptions

The clock  operation  is  controlled  by  the  synthesizer  control  register  (FMPLL\_SYNCR)  and  status  is reported  in  the  synthesizer  status  register  (FMPLL\_SYNSR).  The  following  sections  describe  these registers in detail.

## 11.3.1.1 Synthesizer Control Register (FMPLL\_SYNCR)

The synthesizer control register (FMPLL\_SYNCR) contains bits for defining the clock operation for the system.

## NOTE

To ensure proper operation across all MPC5500 MCUs, execute an mbar  or msync  instruction between the write to change the FMPLL\_SYNCR[MFD] and the read to check the lock status shown by FMPLL\_SYNSR[LOCK].

Furthermore, buffering writes to the FMPLL, as controlled by PBRIDGE\_A\_OPACR[BW0], must be disabled.

Figure 11-8. Synthesizer Control Register (FMPLL\_SYNCR)

<!-- image -->

|          | 0             | 1             | 2             | 3             | 4             | 5             | 6             | 7             | 8             | 9             | 10            | 11            | 12            | 13            | 14            | 15            |
|----------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| R        | 0             | PREDIV        | PREDIV        | PREDIV        | MFD           | MFD           | MFD           | MFD           | MFD           | 0             |               | RFD           |               | LOC           | LOL           | LOC           |
| W        |               |               |               |               |               |               |               |               |               |               |               |               |               | EN            | RE            | RE            |
| Reset    | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 1             | 0             | 0             | 0             | 1             | 0             | 0             | 0             | 0             |
| Reg Addr | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 |
|          | 16            | 17            | 18            | 19            | 20            | 21            | 22            | 23            | 24            | 25            | 26            | 27            | 28            | 29            | 30            | 31            |
| R W      | DIS CLK       | LOL IRQ       | LOC IRQ       | RATE          | DEPTH         | DEPTH         | EXP           | EXP           | EXP           | EXP           | EXP           | EXP           | EXP           | EXP           | EXP           | EXP           |
| Reset    | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Reg Addr | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 |

Table 11-5. FMPLL\_SYNCR Field Descriptions

| Bits   | Name         | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
|--------|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0      | -            | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| 1-3    | PREDIV [0:2] | The PREDIV bits control the value of the divider on the input clock. The output of the pre-divider circuit generates the reference clock to the FMPLL analog loop. When the PREDIV bits are changed, the FMPLL will immediately lose lock. To prevent an immediate reset, the LOLRE bit must be cleared before writing the PREDIV bits. In 1:1 (dual-controller) mode, the PREDIV bits are ignored and the input clock is fed directly to the analog loop. 000 Divide by 1 001 Divide by 2 010 Divide by 3 011 Divide by 4 100 Divide by 5 101-111Reserved Note: Programming a PREDIV value such that the ICO operates outside its specified range will cause unpredictable results and the FMPLL will not lock. Refer to the MPC5553/MPC5554 Data Sheet for details on the ICO range. Note: To avoid unintentional interrupt requests, disable LOLIRQ before changing PREDIV and then reenable it after acquiring lock. |

## Table 11-5. FMPLL\_SYNCR Field Descriptions (continued)

| Bits   | Name      | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
|--------|-----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 4-8    | MFD [0:4] | Multiplication factor divider. The MFD bits control the value of the divider in the FMPLL feedback loop. The value specified by the MFD bits establish the multiplication factor applied to the reference frequency. The decimal equivalent of the MFD binary number is substituted into the equation from Table 11-10 for F sys to determine the equivalent multiplication factor. When the MFD bits are changed, the FMPLL loses lock. At this point, if modulation is enabled, the calibration sequence is reinitialized. To prevent an immediate reset, the LOLRE bit must be cleared before writing the MFD bits. In dual-controller mode, the MFD bits are ignored and the multiplication factor is equivalent to 2X. In bypass mode the MFD bits have no effect. Note: Programming an MFD value such that the ICO operates outside its specified range will cause unpredictable results and the FMPLL will not lock. Refer to the MPC5553/MPC5554 Data Sheet for details on the ICO range. Note: To avoid unintentional interrupt requests, disable LOLIRQ before changing MFD |
| 9      | -         | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 10-12  | RFD [0:2] | Reduced frequency divider. The RFDbits control a divider at the output of the FMPLL. The value specified by the RFD bits establish the divisor applied to the FMPLL frequency.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| 10-12  | RFD [0:2] |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| 10-12  | RFD [0:2] |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| 10-12  | RFD [0:2] |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| 10-12  | RFD [0:2] |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| 10-12  | RFD [0:2] |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| 10-12  | RFD [0:2] |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| 10-12  | RFD [0:2] |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| 10-12  | RFD [0:2] |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| 10-12  | RFD [0:2] |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| 10-12  | RFD [0:2] | Changing the RFD bits does not affect the FMPLL; hence, no re-lock delay is incurred. Resulting changes in clock frequency are synchronized to the next falling edge of the current system clock. However these bits must only be written when the lock bit (LOCK) is set, to avoid exceeding the allowable system operating frequency. In bypass mode, the RFD bits have no effect.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| 13     | LOCEN     | Loss-of-clock enable. The LOCEN bit determines whether the loss of clock function is operational. See Section 11.4.2.6, 'Loss-of-Clock Detection' and Section 11.4.2.6.1, 'Alternate/Backup Clock Selection' for more information. In bypass mode, this bit has no effect.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |

## Table 11-5. FMPLL\_SYNCR Field Descriptions (continued)

|   Bits | Name   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
|--------|--------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|     14 | LOLRE  | Loss-of-lock reset enable. The LOLREbit determines how the integration module (the SIU) handles a loss of lock indication. When operating in crystal reference, external reference, or dual-controller mode, the FMPLL must be locked before setting the LOLRE bit. Otherwise reset is immediately asserted. The LOLRE bit has no effect in bypass mode. 0 Ignore loss of lock - reset not asserted. 1 Assert reset on loss of lock. Reset will remain asserted, regardless of the source of reset, until after the FMPLL has locked. |
|     15 | LOCRE  | Loss-of-clock reset enable. The LOCRE bit determines how the integration module (the SIU) handles a loss of clock condition when LOCEN=1. LOCRE has no effect when LOCEN=0. If the LOCF bit in the SYNSR indicates a loss of clock condition, setting the LOCRE bit causes an immediate reset. In bypass mode LOCRE has no effect. 0 Ignore loss of clock - reset not asserted. 1 Assert reset on loss of clock.                                                                                                                      |
|     16 | DISCLK | Disable CLKOUT. The DISCLK bit determines whether CLKOUT is active. When CLKOUT is disabled it is driven low. 0 CLKOUT driven normally                                                                                                                                                                                                                                                                                                                                                                                                |
|     17 | LOLIRQ | Loss-of-lock interrupt request. The LOLIRQ bit enables an interrupt request for LOLFwhen it (LOLIRQ) is asserted and when LOLF is asserted. If either LOLF or LOLIRQ is negated, the interrupt request is negated. When operating in crystal reference, external reference, or dual-controller mode, the FMPLL must be locked before setting the LOLIRQ bit. Otherwise an interrupt is immediately requested. The LOLIRQ bit has no effect in bypass mode 0 Ignore loss of lock - interrupt not requested                             |
|     18 | LOCIRQ | Loss-of-clock interrupt request. The LOCIRQ bit determines how the integration module (the SIU) handles a loss of clock condition when LOCEN=1. LOCIRQ has no effect when LOCEN=0. If the LOCF bit in the SYNSR indicates a loss of clock condition, setting (or having previously set) the LOCIRQ bit causes an interrupt request. In bypass mode LOCIRQ has no effect. 0 Ignore loss of clock - interrupt not requested 1 Request interrupt on loss of clock.                                                                       |
|     19 | RATE   | Modulation rate. Controls the rate of frequency modulation applied to the system frequency. The allowable modulation rates are shown below. Changing the rate by writing to the RATE bit will initiate the FM calibration sequence.                                                                                                                                                                                                                                                                                                   |
|     19 | RATE   |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|     19 | RATE   |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|     19 | RATE   |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|     19 |        | Note: To avoid unintentional interrupt requests, clear LOLIRQ before changing RATE.                                                                                                                                                                                                                                                                                                                                                                                                                                                   |

Table 11-5. FMPLL\_SYNCR Field Descriptions (continued)

| Bits   | Name        | Description                                                                                                                                                                                                                                                                                                                                                      | Description                                                                                                                                                                                                                                                                                                                                                      |
|--------|-------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 20-21  | DEPTH [0:1] | Controls the frequency modulation depth and enables the frequency modulation. When programmed to a value other than 0x0, the frequency modulation is automatically enabled. The programmable frequency deviations from the system frequency are shown below. Upon a change in the depth value to other than 0x0, the calibration sequence will be reinitialized. | Controls the frequency modulation depth and enables the frequency modulation. When programmed to a value other than 0x0, the frequency modulation is automatically enabled. The programmable frequency deviations from the system frequency are shown below. Upon a change in the depth value to other than 0x0, the calibration sequence will be reinitialized. |
|        |             |                                                                                                                                                                                                                                                                                                                                                                  | DEPTH[1]                                                                                                                                                                                                                                                                                                                                                         |
|        |             |                                                                                                                                                                                                                                                                                                                                                                  | 0                                                                                                                                                                                                                                                                                                                                                                |
|        |             |                                                                                                                                                                                                                                                                                                                                                                  | 0                                                                                                                                                                                                                                                                                                                                                                |
|        |             |                                                                                                                                                                                                                                                                                                                                                                  | 1                                                                                                                                                                                                                                                                                                                                                                |
|        |             |                                                                                                                                                                                                                                                                                                                                                                  | 1                                                                                                                                                                                                                                                                                                                                                                |
|        |             | Note: To avoid unintentional interrupt requests, clear LOLIRQ before changing DEPTH.                                                                                                                                                                                                                                                                             | Note: To avoid unintentional interrupt requests, clear LOLIRQ before changing DEPTH.                                                                                                                                                                                                                                                                             |
| 22-31  | EXP [0:9]   | Expected difference value. Holds the expected value of the difference of the reference and the feedback counters. See Section 11.4.3.3, 'FM Calibration Routine' to determine the value of these bits. This field is written by the application before entering calibration mode.                                                                                | Expected difference value. Holds the expected value of the difference of the reference and the feedback counters. See Section 11.4.3.3, 'FM Calibration Routine' to determine the value of these bits. This field is written by the application before entering calibration mode.                                                                                |

## 11.3.1.2 Synthesizer Status Register (FMPLL\_SYNSR)

The synthesizer status register (FMPLL\_SYNSR) is a 32-bit register. Only the LOLF and LOCF flag bits are writable in this register. Writes to bits other than the LOLF and LOCF have no effect.

<!-- image -->

|          | 0                   | 1                   | 2                   | 3                   | 4                   | 5                   | 6                   | 7                   | 8                   | 9                   | 10                  | 11                  | 12                  | 13                  | 14                  | 15            |
|----------|---------------------|---------------------|---------------------|---------------------|---------------------|---------------------|---------------------|---------------------|---------------------|---------------------|---------------------|---------------------|---------------------|---------------------|---------------------|---------------|
| R        | 0                   | 0                   | 0                   | 0                   | 0                   | 0                   | 0                   | 0                   | 0                   | 0                   | 0                   | 0                   | 0                   | 0                   | 0                   | 0             |
| W        |                     |                     |                     |                     |                     |                     |                     |                     |                     |                     |                     |                     |                     |                     |                     |               |
| Reset    | 0                   | 0                   | 0                   | 0                   | 0                   | 0                   | 0                   | 0                   | 0                   | 0                   | 0                   | 0                   | 0                   | 0                   | 0                   | 0             |
| Reg Addr | Base + 0x0004       | Base + 0x0004       | Base + 0x0004       | Base + 0x0004       | Base + 0x0004       | Base + 0x0004       | Base + 0x0004       | Base + 0x0004       | Base + 0x0004       | Base + 0x0004       | Base + 0x0004       | Base + 0x0004       | Base + 0x0004       | Base + 0x0004       | Base + 0x0004       | Base + 0x0004 |
|          | 16                  | 17                  | 18                  | 19                  | 20                  | 21                  | 22                  | 23                  | 24                  | 25                  | 26                  | 27                  | 28                  | 29                  | 30                  | 31            |
| R        | 0                   | 0                   | 0                   | 0                   | 0                   | 0                   | LOLF                | LOC                 | MODE                | PLL                 | PLL                 | LOCKS               | LOCK                | LOCF                | CALD                | CAL           |
| W        | SEL REF ONE w1c w1c | SEL REF ONE w1c w1c | SEL REF ONE w1c w1c | SEL REF ONE w1c w1c | SEL REF ONE w1c w1c | SEL REF ONE w1c w1c | SEL REF ONE w1c w1c | SEL REF ONE w1c w1c | SEL REF ONE w1c w1c | SEL REF ONE w1c w1c | SEL REF ONE w1c w1c | SEL REF ONE w1c w1c | SEL REF ONE w1c w1c | SEL REF ONE w1c w1c | SEL REF ONE w1c w1c | PASS          |
| Reset    | 0                   | 0                   | 0                   | 0                   | 0                   | 0                   | 0                   | 0                   | - 1                 | - 1                 | - 1                 | - 1                 | - 2                 | 0                   | 0                   | 0             |
| Reg Addr | Base + 0x0004       | Base + 0x0004       | Base + 0x0004       | Base + 0x0004       | Base + 0x0004       | Base + 0x0004       | Base + 0x0004       | Base + 0x0004       | Base + 0x0004       | Base + 0x0004       | Base + 0x0004       | Base + 0x0004       | Base + 0x0004       | Base + 0x0004       | Base + 0x0004       | Base + 0x0004 |

- 1 Reset state determined during reset configuration. (See Section 11.1.4, 'FMPLL Modes of Operation,' for more information.)
- 2 Reset state determined during reset.
- 3 'w1c' signifies that this bit is cleared by writing a 1 to it.

Figure 11-9. Synthesizer Status Register (FMPLL\_SYNSR)

Table 11-6. FMPLL\_SYNSR Field Descriptions

| Bits   | Name   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
|--------|--------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-21   | -      | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| 22     | LOLF   | Loss-of-lock flag. Provides the interrupt request flag. This is a write 1 to clear (w1c) bit; to clear the flag, the user must write a 1 to the bit. Writing 0 has no effect. This flag will not be set, and an interrupt will not be requested, if the loss of lock condition was caused by a system reset, a write to the FMPLL_SYNCR which modifies the MFD bits, or enabling frequency modulation. If the flag is set due to a system failure, writing the MFD bits or enabling FM will not clear the flag. Asserting reset will clear the flag. This flag bit is sticky in the sense that if lock is reacquired, the bit will remain set until either a write 1 or reset is asserted. 0 Interrupt service not requested 1 Interrupt service requested Note: Upon a loss of lock that is not generated by a system reset, a write to the FMPLL_SYNCR that modifies the MFD or PREDIV bits, or an enabling of frequency modulation, the LOLF will be set if LOLIRQ is set. If the FMPLL reacquires lock and at that point either of the three above steps are executed, the LOLF will again be set. To avoid an unintentional interrupt from being generated, LOLIRQ must be cleared prior to changing MFD or PREDIV, or prior to enabling FM after a previous interrupt and relock occurred. |
| 23     | LOC    | Loss-of-clock status. Indicates whether a loss-of-clock condition is present when operating in crystal reference, external reference, or dual-controller mode, If LOC = 0, the system clocks are operating normally. If LOC = 1, the system clocks have failed due to a reference failure or a FMPLL failure. If the read of the LOC bit and the loss-of-clock condition occur simultaneously, the bit does not reflect the current loss of clock condition. If a loss-of-clock condition occurs which sets this bit and the clocks later return to normal, this bit will be cleared. A loss of clock condition can only be detected if LOCEN = 1. LOC is always 0 in bypass mode. 0 Clocks are operating normally 1 Clocks are not operating normally.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 24     | MODE   | Clock mode. Determined at reset, this bit indicates which clock mode the system is utilizing. See Chapter 4, 'Reset,' for details on how to configure the system clock mode during reset. 0 PLL bypass mode. 1 PLL clock mode.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| 25     | PLLSEL | PLL mode select. Determined at reset, this bit indicates in which mode the FMPLL operates. This bit is cleared in dual-controller and bypass mode. See Chapter 4, 'Reset,' for details on how to configure the system clock mode during reset. See Table 11-1 for more information. 0 Dual-controller mode. 1 Crystal reference or external reference mode.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| 26     | PLLREF | PLL clock reference source. Determined at reset, this bit indicates whether the PLL reference source is an external clock or a crystal reference. This bit is cleared in dual controller mode and bypass mode. See Chapter 4, 'Reset,' for details on how to configure the system clock mode during reset. 0 External clock reference chosen. 1 Crystal clock reference chosen.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |

## Table 11-6. FMPLL\_SYNSR Field Descriptions (continued)

|   Bits | Name    | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|--------|---------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|     27 | LOCKS   | Sticky FMPLL lock status bit. A sticky indication of FMPLL lock status. LOCKS is set by the lock detect circuitry when the FMPLL acquires lock after one of the following: GLYPH<127> a system reset GLYPH<127> a write to the FMPLL_SYNCR which modifies the MFD bits GLYPH<127> the enabling of frequency modulation Whenever the FMPLL loses lock, LOCKS is cleared. LOCKS remains cleared even after the FMPLL relocks, until one of the three previously-stated conditions occurs. Furthermore, if the LOCKS bit is read when the FMPLL simultaneously loses lock, the bit does not reflect the current loss of lock condition. If operating in bypass mode, LOCKS remains cleared after reset. In crystal reference, external reference, and dual-controller mode, LOCKS is set after reset. 0 PLL has lost lock since last system reset, a write to FMPLL_SYNCR to modify the MFD bit field, or frequency modulation enabled. 1 PLL has not lost lock since last system reset, a write to FMPLL_SYNCR to modify the MFD bit field, or frequency modulation enabled. |
|     28 | LOCK    | PLL lock status bit. Indicates whether the FMPLL has acquired lock. FMPLL lock occurs when the synthesized frequency matches to within approximately 0.75% of the programmed frequency. The FMPLL loses lock when a frequency deviation of greater than approximately 1.5% occurs. If the LOCK bit is read when the FMPLL simultaneously loses lock or acquires lock, the bit does not reflect the current condition of the FMPLL. If operating in bypass mode, LOCK remains cleared after reset. 0 PLL is unlocked. 1 PLL is locked.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
|     29 | LOCF    | Loss-of-clock flag. This bit provides the interrupt request flag. This is a write 1 to clear (w1c) bit; to clear the flag, the user must write a 1 to the bit. Writing 0 has no effect. Asserting reset will clear the flag. This flag is sticky in the sense that if clocks return to normal after the flag has been set, the bit will remain set until cleared by either writing 1 or asserting reset. 0 Interrupt service not requested 1 Interrupt service requested                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|     30 | CALDONE | Calibration complete. Indicates whether the calibration sequence has been completed since the last time modulation was enabled. If CALDONE = 0 then the calibration sequence is either in progress or modulation is disabled. If CALDONE = 1 then the calibration sequence has been completed, and frequency modulation is operating. 0 Calibration not complete. 1 Calibration complete. Note: FM relocking does not start until calibration is complete.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|     31 | CALPASS | Calibration passed. Indicates whether the calibration routine was successful. If CALPASS = 1 and CALDONE = 1 then the routine was successful. If CALPASS = 0 and CALDONE = 1, then the routine was unsuccessful. When the calibration routine is initiated the CALPASS is asserted. CALPASS remains asserted until either modulation is disabled by clearing the DEPTH bits in the FMPLL_SYNCR or a failure occurs within the FMPLL calibration sequence. 0 Calibration unsuccessful. 1 Calibration successful. If calibration is unsuccessful, then actual depth is not guaranteed to match the desired depth.                                                                                                                                                                                                                                                                                                                                                                                                                                                            |

## 11.4 Functional Description

This section explains clock architecture, clock operation, and clock configuration.

## 11.4.1 Clock Architecture

This section describes the clocks and clock architecture in the MPC5553/MPC5554 MCU.

## 11.4.1.1 Overview

The MPC5553/MPC5554 system clocks are generated from one of four FMPLL modes: crystal reference mode,  external  reference  mode,  dual-controller  (1:1)  mode,  and  bypass  mode.  See  Section 11.1, 'Introduction'  for  information  on  the  different  clocking  modes  available  in  the  MPC5553/MPC5554 FMPLL.

The MPC5553/MPC5554 peripheral IP modules have been designed to allow software to gate the clocks to the non-memory-mapped logic of the modules.

The  MPC5553/MPC5554  MCU  has  three  clock  output  pins  that  are  driven  by  programmable  clock dividers. The clock dividers divide the system clock down by even integer values. The three clock output pins are the following:

- · CLKOUT - External address/data bus clock
- · MCKO - Nexus auxiliary port clock
- · ENGCLK - Engineering clock

The MPC5553/MPC5554 MCU has been designed so that the oscillator clock can be selected as the clock source for the CAN interface in the FlexCAN blocks resulting in very low jitter performance.

Figure 11-1 shows a block diagram of the FMPLL and the system clock architecture.

## 11.4.1.2 Software Controlled Power Management/Clock Gating

Some of the IP modules on MPC5553/MPC5554 support software controlled power management/clock gating whereby the application software can disable the non-memory-mapped portions of the modules by writing to module disable (MDIS) bits in registers within the modules. The memory-mapped portions of the modules are clocked by the system clock when they are being accessed. The NPC can be configured to disable the MCKO signal when there are no Nexus messages pending. The H7FA Flash array can be disabled by writing to a bit in the Flash register map.

The  modules  that  implemented  software  controlled  power  management/clock  gating  are  listed  in Table 11-7 along with the registers and bits that disable each module. The software controlled clocks are enabled when the MPC5553/MPC5554 MCU comes out of reset.

Table 11-7. Software Controlled Power Management/Clock Gating Support

| Module Name   | Register Name   | Bit Names   |
|---------------|-----------------|-------------|
| DSPI A 1      | DSPI_A_MCR      | MDIS        |
| DSPI B        | DSPI_B_MCR      | MDIS        |
| DSPI C        | DSPI_C_MCR      | MDIS        |
| DSPI D        | DSPI_D_MCR      | MDIS        |
| EBI           | EBI_MCR         | MDIS        |

Table 11-7. Software Controlled Power Management/Clock Gating Support

| Module Name   | Register Name   | Bit Names          |
|---------------|-----------------|--------------------|
| eTPU Engine A | ETPUECR_1       | MDIS               |
| eTPU Engine B | ETPUECR_2       | MDIS               |
| FlexCAN A     | FLEXCAN_A_MCR   | MDIS               |
| FlexCAN B 1   | FLEXCAN_B_MCR   | MDIS               |
| FlexCAN C     | FLEXCAN_C_MCR   | MDIS               |
| EMIOS         | EMIOS_MCR       | MDIS               |
| ESCI_A        | ESCIA_CR2       | MDIS               |
| ESCI_B        | ESCIB_CR2       | MDIS               |
| NPC           | NPC_PCR         | MCKO_EN, MCKO_GT 2 |
| Flash Array   | FLASH_MCR       | STOP 3             |

- 1 Shaded areas indicate that module is only offered on the MPC5554, not on the MPC5553.
- 2 See Chapter 25, 'Nexus Development Interface.'
- 3 See Chapter 13, 'Flash Memory.'

## 11.4.1.3 Clock Dividers

Each of the CLKOUT, MCKO, and ENGCLK dividers provides a nominal 50% duty cycle clock to an output  pin.  There  is  no  guaranteed  phase  relationship  between  CLKOUT,  MCKO,  and  ENGCLK. ENGCLK is not synchronized to any I/O pins.

## 11.4.1.3.1 External Bus Clock (CLKOUT)

The external bus clock (CLKOUT) divider can be programmed to divide the system clock by two or four based on the settings of the EBDF bit field in the SIU external clock control register (SIU\_ECCR). The reset value of the EBDF selects a CLKOUT frequency of one half of the system clock frequency. The EBI supports  gating  of  the  CLKOUT  signal  when  there  are  no  external  bus  accesses  in  progress.  See  the Chapter 6, 'System Integration Unit (SIU)' for more information on CLKOUT.

The hold-time for the external bus pins can be changed by writing to the external bus tap select (EBTS) bit in the SIU\_ECCR. See Chapter 6, 'System Integration Unit (SIU)' for more information.

## 11.4.1.3.2 Nexus Message Clock (MCKO)

The Nexus message clock (MCKO) divider can be programmed to divide the system clock by two, four or eight  based  on  the  MCKO\_DIV  bit  field  in  the  port  configuration  register  (PCR)  in  the  Nexus  port controller (NPC). The reset value of the MCKO\_DIV selects an MCKO clock frequency one half of the system clock frequency. The MCKO divider is configured by writing to the NPC through the JTAG port. See Chapter 25, 'Nexus Development Interface' for more information.

## 11.4.1.3.3 Engineering Clock (ENGCLK)

The engineering clock (ENGCLK) divider can be programmed to divide the system clock by factors from 2 to 128 in increments of two. The ENGDIV bit field in the SIU\_ECCR determines the divide factor. The reset value of ENGDIV selects an ENGCLK frequency of system clock divided by 32.

## 11.4.1.3.4 FlexCAN\_  Clock Domains x

The FlexCAN modules have two distinct software controlled clock domains. One of the clock domains is always derived from the system clock. This clock domain includes the message buffer logic. The source for  the  second  clock  domain  can  be  either  the  system  clock  or  a  direct  feed  from  the  oscillator  pin EXTAL\_EXTCLK. The logic in the second clock domain controls the CAN interface pins. The CLK\_SRC bit in the FlexCAN CTRL register selects between the system clock and the oscillator clock as the clock source for the second domain. Selecting the oscillator as the clock source ensures very low jitter on the CAN bus. System software can gate both clocks by writing to the MDIS bit in the FlexCAN MCR register. Figure 11-1 shows the two clock domains in the FlexCAN modules.

See Chapter 22, 'FlexCAN2 Controller Area Network' for more information on the FlexCAN modules.

## 11.4.1.3.5 FEC Clocks

In the MPC5553, the FEC TX\_CLK and RX\_CLK are inputs. An external source provides the clocks to these pins.

## 11.4.2 Clock Operation

## 11.4.2.1 Input Clock Frequency

The FMPLL is designed to operate over an input clock frequency range as determined by the operating mode. The operating ranges for each mode are given in Table 11-8.

Table 11-8. Input Clock Frequency

| Mode                                 | Input Frequency Range   |
|--------------------------------------|-------------------------|
| Crystal Reference External Reference | 8 MHz -20 MHz           |
| Bypass                               | 0 Hz-132MHz             |
| Dual-Controller (1:1)                | 25 MHz-66 MHz           |

## 11.4.2.2 Reduced Frequency Divider (RFD)

The RFD may be used for reducing the FMPLL system clock frequency. The RFD must be programmed to be ≥ 1 when changing MFD or PREDIV or when enabling frequency modulation.

## 11.4.2.3 Programmable Frequency Modulation

The FMPLL provides for frequency modulation of the system clock. The modulation is applied as a triangular waveform with modulation depth and rate controlled by fields in the FMPLL\_SYNCR. The modulation depth can be set to +/-1% or +/-2% of the system frequency. The modulation rate is dependent on the reference clock frequency.

Complete details for configuring the programmable frequency modulation is given in Section 11.4.3.2, 'Programming System Clock Frequency with Frequency Modulation.'

## 11.4.2.4 FMPLL Lock Detection

A pair of counters monitor the reference and feedback clocks to determine when the system has acquired frequency lock. Once the FMPLL has locked, the counters continue to monitor the reference and feedback clocks and will report if/when the FMPLL has lost lock. The FMPLL\_SYNCR provides the flexibility to select whether to generate an interrupt, assert system reset, or do nothing in the event that the FMPLL loses lock. See Section 11.3.1.1, 'Synthesizer Control Register (FMPLL\_SYNCR) for details.

When the frequency modulation is enabled, the loss of lock continues to function as described but with the lock and loss of lock criteria reduced to ensure that false loss of lock conditions are not detected.

In bypass mode, the FMPLL cannot lock since the FMPLL is disabled.

## 11.4.2.5 FMPLL Loss-of-Lock Conditions

Once the FMPLL acquires lock after reset, the FMPLL\_SYNSR[LOCK] and FMPLL\_SYNSR[LOCKS] status bits are set. If the MFD is changed or if an unexpected loss of lock condition occurs, the LOCK and LOCKS status bits are negated. While the FMPLL is in an unlocked condition, the system clocks continue to be sourced from the FMPLL as the FMPLL attempts to re-lock. Consequently, during the re-locking process, the system clock frequency is not well defined and may exceed the maximum system frequency thereby  violating  the  system  clock  timing  specifications  (when  changing  MFD,  this  is  avoided  by following the procedure detailed in Section 11.4.3, 'Clock Configuration'). Because this condition can arise during unexpected loss of lock events, it is recommended to use the loss of lock reset functionality, see Section 11.4.2.5.1, 'FMPLL Loss-of-Lock Reset,' below. However, LOLRE must be cleared while changing the MFD otherwise a reset will occur.

Once the FMPLL has relocked, the LOCK bit is set. The LOCKS bit remains cleared if the loss of lock was unexpected. The LOCKS bit is set to 1 when the loss of lock was caused by changing the MFD.

## 11.4.2.5.1 FMPLL Loss-of-Lock Reset

The FMPLL provides the ability to assert reset when a loss of lock condition occurs by programming the FMPLL\_SYNCR[LOLRE] bit. Reset is asserted if LOLRE is set and loss of lock occurs. Because the FMPLL\_SYNSR[LOCK] and FMPLL\_SYNSR[LOCKS] bits are reinitialized after reset, the system reset status register (SIU\_RSR) must be read to determine that a loss of lock condition occurred.

To exit reset, the reference must be present and the FMPLL must acquire lock. In bypass mode, the FMPLL cannot lock. Therefore a loss of lock condition cannot occur, and LOLRE has no effect.

## 11.4.2.5.2 FMPLL Loss-of-Lock Interrupt Request

The  FMPLL  provides  the  ability  to  request  an  interrupt  when  a  loss  of  lock  condition  occurs  by programming the FMPLL\_SYNCR[LOLIRQ] bit. An interrupt is requested by the FMPLL if LOLIRQ is set and loss of lock occurs.

In bypass mode, the FMPLL cannot lock. Therefore a loss of lock condition cannot occur, and the LOLIRQ bit has no effect.

## 11.4.2.6 Loss-of-Clock Detection

The FMPLL continuously monitors the reference and feedback clocks. In the event either of the clocks fall below a threshold frequency, the system will report a loss of clock condition. The user may enable a feature to have the FMPLL switch the system clocks to a backup clock in the event of such a failure. Additionally, the user may select to have the system enter reset, assert an interrupt request, or do nothing if/when the FMPLL reports this condition.

## 11.4.2.6.1 Alternate/Backup Clock Selection

If the user enables loss of clock by setting FMPLL.SYNCR[LOCEN] =1, then the FMPLL will transition system clocks to a backup clock source in the event of a clock failure as per Table 11-9.

If  loss  of  clock  is  enabled  and  the  reference  clock  is  the  source  of  the  failure,  the  FMPLL  will  enter self-clock mode (SCM). The exact frequency during self-clock mode operation is indeterminate due to process, voltage, and temperature variation but is guaranteed to be below the maximum system frequency. If the FMPLL clocks have failed, the FMPLL will transition the system clock source to the reference clock.

The FMPLL remains in SCM until the next reset. Note that when the FMPLL is operated in SCM the system frequency is dependent upon the value in RFD[0:2]. The SCM system frequency stated in the MPC5553/MPC5554 Data Sheet assumes that the RFD has been programmed to 0x0. If the loss-of-clock condition is due to a FMPLL failure (for example, loss of feedback clock), the FMPLL reference becomes the system clocks source until the next reset, even if the FMPLL regains itself and re-locks.

Table 11-9. Loss of Clock Summary

| Clock Mode   | System Clock Source before Failure   | REFERENCE FAILURE Alternate Clock Selected byLOC Circuitry until Reset   | PLL FAILURE Alternate Clock Selected by LOC Circuitry until Reset   |
|--------------|--------------------------------------|--------------------------------------------------------------------------|---------------------------------------------------------------------|
| PLL          | PLL                                  | PLL Self-Clocked Mode                                                    | PLL reference                                                       |
| PLL bypass   | Ext. Clock(s)                        | None                                                                     | NA                                                                  |

A special loss of clock condition occurs when both the reference and the FMPLL fail. The failures may be simultaneous or the FMPLL may fail first. In either case, the reference clock failure takes priority and the FMPLL attempts to operate in SCM. If successful, the FMPLL remains in SCM until the next reset. During SCM, modulation is always disabled. If the FMPLL cannot operate in SCM, the system remains static until the next reset. Both the reference and the FMPLL must be functioning properly to exit reset.

## 11.4.2.6.2 Loss-of-Clock Reset

When a loss of clock condition is recognized, reset is asserted if the FMPLL\_SYNCR[LOCRE] bit is set. The LOCF and LOC bits in FMPLL\_SYNSR are cleared after reset, therefore, the SIU\_RSR must be read to determine that a loss of clock condition occurred. LOCRE has no effect in bypass mode.

To exit reset in FMPLL mode, the reference must be present and the FMPLL must acquire lock.

## 11.4.2.6.3 Loss-of-Clock Interrupt Request

When  a  loss of clock condition is recognized, the FMPLL  will  request an interrupt if the FMPLL\_SYNCR[LOCIRQ]  bit  is  set.  The  LOCIRQ  bit  has  no  effect  in  bypass  mode  or  if FMPLL\_SYNCR[LOCEN] = 0.

## 11.4.3 Clock Configuration

In crystal reference and external reference clock mode, the default system frequency is determined by the MFD, RFD, and PREDIV  reset values. See Section 11.3.1.1, 'Synthesizer Control Register (FMPLL\_SYNCR).' The frequency multiplier is determined by the RFD, PREDIV, and multiplication frequency divisor (MFD) bits in FMPLL\_SYNCR.

Table 11-10 shows the clock-out to clock-in frequency relationships for the possible clock modes.

Table 11-10. Clock-out vs. Clock-in Relationships

| Clock Mode                                                                         | PLL Option                                                                                                            |
|------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|
| Crystal Reference Mode and External Reference Mode (Frequency modulation disabled) | F sys F ref MFD 4 + ( ) PREDIV 1 + ( ) 2 RFD × ( ) ------------------------------- ------------------------------ • = |
| Dual Controller (1:1) Mode                                                         | F sys 2F ref =                                                                                                        |
| Bypass Mode                                                                        | F sys F ref =                                                                                                         |

## NOTES:

F sys = System frequency

F ref = Clock frequency at the EXTAL signal. (See Figure 11-1)

MFD ranges from 0 to 31

RFD ranges from 0 to 7

PREDIV normal reset value is 0. Caution: Programming a PREDIV value such that the ICO operates outside its specified range will cause unpredictable results and the FMPLL will not lock. Refer to the MPC5553/MPC5554 Data Sheet for details on the ICO range.

When programming the FMPLL, be sure not to violate the maximum system clocks frequency or max/min ICO frequency specifications. For determining the MFD value, RFD should be assumed zero (that is, divide by 1). This will insure that the FMPLL does not have to synthesize a frequency out of its range. See the MPC5553/MPC5554 Data Sheet for more information.

## 11.4.3.1 Programming System Clock Frequency Without Frequency Modulation

The  following  steps  are  required  to  accommodate  the  frequency  overshoot  that  may  occur  when  the PREDIV or MFD bits are changed. If frequency modulation is going to be enabled the maximum allowable frequency must be reduced by the programmed ∆ F m .

## NOTE

Following these steps will produce immediate changes in supply current, thus the user should ensure that the power supply is sufficiently decoupled with low ESR capacitors.

Here are the steps to program the clock frequency without frequency modulation:

- 1. Determine the appropriate value for the PREDIV, MFD, and RFD fields in the synthesizer control register (FMPLL\_SYNCR). Remember to include the ∆ F m  if frequency modulation is to be enabled. Note that the amount of jitter in the system clocks can be minimized by selecting the

maximum MFD factor that can be paired with an RFD factor to provide the desired frequency. The maximum MFD value that can be used is determined by the ICO range. See the MPC5553/MPC5554 Data Sheet for the maximum frequency of the ICO.

- 2. Change the following in FMPLL\_SYNCR:
- a) Make sure frequency modulation is disabled (FMPLL\_SYNCR[DEPTH] = 00).  A change to PREDIV, MFD, or RATE while modulation is enabled will invalidate the previous calibration results.
- b) Clear  FMPLL\_SYNCR[LOLRE]. If this bit is set, the MCU will go into reset when MFD is written.
- c) Initialize the FMPLL for less than the desired final system frequency:
- - Disable LOLIRQ.
- - Write  FMPLL\_SYNCR[PREDIV] for the desired final value.
- - Write  FMPLL\_SYNCR[MFD] for the desired final value.
- - Write the RFD control field for 1 + the desired final RFD value.
- 3. Wait for the FMPLL to lock by monitoring the FMPLL\_SYNSR[LOCK] bit. Refer to Section 11.3.1.1, 'Synthesizer Control Register (FMPLL\_SYNCR),' for memory synchronization between changing FMPLL\_SYNCR[MFD] and monitoring the lock status.
- 4. Initialize the FMPLL for the desired final system frequency by changing FMPLL\_SYNCR[RFD] to its desired final value. Note that the FMPLL will not need to re-lock when only changing the RFD, and that RFD must be programmed to be &gt;1 to protect from overshoot.
- 5. Re-enable LOLIRQ.

## NOTE

This first register write will cause the FMPLL to switch to an initial system frequency which is less than the final one. Keeping the change of frequency to  a  lower  initial  value  helps  minimize  the  current  surge  to  the  external power supply caused by change of frequency. The last step will be to only change the RFD to get to the desired final frequency.

## NOTE

Changing the MFD or PREDIV values causes the FMPLL to perform a search  for  the  lock  frequency  that  results  in  the  system  clock  frequency changing rapidly across the complete frequency range. All MCU peripherals, including the external bus will be subjected to this frequency sweep. Operation of timers and serial communications during this search sequence will produce unpredictable results.

## 11.4.3.2 Programming System Clock Frequency with Frequency Modulation

In crystal reference and external reference clock modes, the default mode is without frequency modulation enabled. When frequency modulation is enabled, however, three parameters must be set to generate the desired level of modulation: the RATE, DEPTH, and EXP bit fields of the FMPLL\_SYNCR. RATE and DEPTH  determine  the  modulation  rate  and  the  modulation  depth.  The  EXP  field  controls  the  FM calibration routine. Section 11.4.3.3, 'FM Calibration Routine,' shows how to obtain the values to be programmed for EXP. Figure 11-10 illustrates the effects of the parameters and the modulation waveform built into the modulation hardware. The modulation waveform is always a triangle wave and its shape is not programmable.

## Frequency Modulated Phase Locked Loop (FMPLL) and System Clocks

Note, the modulation rates given are specific to a reference frequency of 8 MHz.

F mod  = F ref / Q (PREDIV + 1) where Q = {40,80} giving modulation rates of 200 kHz and 100 kHz.

## NOTE

The  following  relationship  between  F mod   and  modulation  rates  must  be maintained:

<!-- formula-not-decoded -->

Therefore, the utilization of a non 8 MHz reference will result in scaled modulation rates.

Here are the steps to program the clock frequency with frequency modulation. These steps ensure proper operation of the calibration routine and prevent frequency overshoot from the sequence:

- 1. Change the following in FMPLL\_SYNCR:
- a) Make sure frequency modulation is disabled (FMPLL\_SYNCR[DEPTH] = 00).  A change to PREDIV, MFD, or RATE while modulation is enabled will invalidate the previous calibration results.
- b) Clear  FMPLL\_SYNCR[LOLRE]. If this bit is set, the MCU will go into reset when MFD is written.
- c) Initialize the FMPLL for less than the desired final frequency:
- - Disable LOLIRQ.
- - Write  FMPLL\_SYNCR[PREDIV] for the desired final value.
- - Write  FMPLL\_SYNCR[MFD] for the desired final value.
- - Write FMPLL\_SYNCR[EXP] for the desired final value.
- - Write FMPLL\_SYNCR[RATE] for the desired final value.
- - Write the RFD control field for 1 + the desired final RFD value (RFD must be programmed to be &gt;1 to protect from overshoot).
- 2. Wait for the FMPLL to lock by monitoring the FMPLL\_SYNSR[LOCK] bit. Refer to Section 11.3.1.1, 'Synthesizer Control Register (FMPLL\_SYNCR),' for memory synchronization between changing FMPLL\_SYNCR[MFD] and monitoring the lock status.
- 3. If using the frequency modulation feature, then:
- a) Enable FM by setting FMPLL\_SYNCR[DEPTH] =1 or 2.
- b) Also set FMPLL\_SYNCR[RATE] if not done previously in step 2.
- 4. Calibration starts. After calibration is done, then the FMPLL will re-lock. Wait for the FMPLL to re-lock by monitoring the FMPLL\_SYNSR[LOCK] bit.
- 5. Verify FM calibration completed and was successful by testing the FMPLL\_SYNSR[CALDONE] and FMPLL\_SYNSR[CALPASS] bitfields.
- 6. If FM calibration did not complete or was not successful, attempt again by going back to step 1.
- 7. Initialize the FMPLL for the desired final frequency by changing FMPLL\_SYNCR[RFD] to its desired final value.Note that the FMPLL will not need to re-lock when only changing the RFD.
- 8. Re-enable LOLIRQ.

## NOTE

This  first  register  write  will  cause  the  FMPLL  to  switch  to  an  initial frequency which is less than the final one. Keeping the change of frequency to  a  lower  initial  value  helps  minimize  the  current  surge  to  the  external power supply caused by change of frequency. The last step will be to only change the RFD to get to the desired final frequency.

## NOTE

Changing the MFD or PREDIV values causes the FMPLL to perform a search  for  the  lock  frequency  that  results  in  the  system  clock  frequency changing rapidly across the complete frequency range. All MCU peripherals, including the external bus will be subjected to this frequency sweep. Operation of timers and serial communications during this search sequence will produce unpredictable results.

Note  that  the  frequency  modulation  system  is  dependent  upon  several  factors:  the  accuracies  of  the VDDSYN /V SSSYN  voltage, of the crystal oscillator frequency, and of the manufacturing variation.

For example, if a 5% accurate supply voltage is utilized, then a 5% modulation depth error will result. If the  crystal  oscillator  frequency  is  skewed  from  8  MHz  the  resulting  modulation  frequency  will  be proportionally skewed. Finally, the error due to the manufacturing and environment variation alone can cause the frequency modulation depth error to be greater than 20%.

Figure 11-10. Frequency Modulation Waveform

<!-- image -->

## 11.4.3.3 FM Calibration Routine

Upon  enabling  frequency  modulation,  a  new  calibration  routine  is  performed.  This  routine  tunes  a reference current into the modulation D/A so that the modulation depth (F max  and F min ) remains within specification.

## Frequency Modulated Phase Locked Loop (FMPLL) and System Clocks

Entering the FM calibration mode requires the user to program SYNCR[EXP]. The EXP is the expected value of the difference between the reference and feedback counters used in the calibration of the FM equation:

<!-- formula-not-decoded -->

For example, if 80 MHz is the desired final frequency and 8 MHz crystal is used, the final values of MFD=6 and RFD=0 will produce the desired 80 MHz.  For a desired frequency modulation with a 1% depth, then EXP is calulated using P = 1, MFD = 6 and M = 480. Refer to Table 11-11 for a complete list of values to be used for the variable (M) based on MFD setting. To obtain a percent modulation (P) of 1%, the EXP field would have to be set at: EXP = 6 + 4 ( ) ⋅ 640 1 ⋅ ( ) / 100 48 =

Rounding this value to the closest integer yields the value of 48 that should be entered into the EXP field for this example.

Table 11-11. Multiplied Factor Dividers with M Values

| MFD   |   M |
|-------|-----|
| 0-2   | 960 |
| 3-5   | 640 |
| 6-8   | 480 |
| 9-14  | 320 |
| 15-20 | 240 |
| 21-31 | 160 |

This routine will correct for process variations, but as temperature can change after the calibration has been performed, variation due to temperature drift is not eliminated. This frequency modulation calibration system is also voltage dependent, so if supply changes after the sequence takes place, error incurred will not be corrected. The calibration system reuses the two counters in the lock detect circuit, the reference and feedback counters. The reference counter is still clocked by the reference clock, but the feedback counter is clocked by the ICO clock.

When  the  calibration  routine  is  initiated  by  writing  to  the  DEPTH  bits,  the  CALPASS  status  bit  is immediately set and the CALDONE status bit is immediately cleared.

When calibration is induced, the ICO is given time to settle. Then both the feedback and reference counters start counting. Full ICO clock cycles are counted by the feedback counter during this time to give the initial center frequency count. When the reference counter has counted to the programmed number of reference count cycles, the input to the feedback counter is disabled and the result is placed in the COUNT0 register. The calibration system then enables modulation at programmed ∆ Fm. The ICO is given time to settle. Both counters are reset and restarted. The feedback counter begins to count full ICO clock cycles again to obtain the delta-frequency count. When the reference counter has counted to the new programmed number of reference count cycles, the feedback counter is stopped again.

The  delta-frequency  count  minus  the  center  frequency  count  (COUNT0)  results  in  a  delta  count proportional to the reference current into the modulation D/A. That delta count is subtracted from the expected value given in the EXP field of the FMPLL\_SYNCR  resulting in an error count. The sign of this error count determines the direction taken by the calibration D/A to update the calibration current. After obtaining the error count for the present iteration, both counters are cleared. The stored count of COUNT0

is  preserved  while  a  new  feedback  count  is  obtained,  and  the  process  to  determine  the  error  count  is repeated. The calibration system repeats this process eight times, once for each bit of the calibration D/A.

After the last decision is made, the CALDONE bit of the SYNSR is written to a 1. If an error occurs during the calibration routine, then CALPASS is immediately written to a 0. If the routine completed successfully then CALPASS remains a 1.

Figure 11-11 shows a block diagram of the calibration circuitry and its associated registers. Figure 11-12 shows a flow chart showing the steps taken by the calibration circuit.

Figure 11-11. FM Auto-Calibration Data Flow

<!-- image -->

## Frequency Modulated Phase Locked Loop (FMPLL) and System Clocks

Figure 11-12. FM Auto-Calibration Flow Chart

<!-- image -->

## 11.5 Revision History

## Substantive Changes since Rev 3.0

Updated Section 11.4.3.3, 'FM Calibration Routine.' Section 11.4.3.3, just before table 11-11, gives the formula for EXP as EXP = ((4+4).640.1)/100, should be EXP = ((6+4).480.1)/100 = 48. Changed following line of text to "...yeilds the value of 48..."

Added note to Section 11.3.1.1, 'Synthesizer Control Register (FMPLL\_SYNCR),' that says 'To ensure proper operation across all MPC5500 MCUs, execute an mbar  or msync  instruction between the write to change the FMPLL\_SYNCR[MFD] and the read to check the lock status shown by FMPLL\_SYNSR[LOCK]. Furthermore, buffering writes to the FMPLL, as controlled by PBRIDGE\_A\_OPACR[BW0], must be disabled' Added cross ref to this section from procedures outlined in Section 11.4.3.1, 'Programming System Clock Frequency Without Frequency Modulation' and Section 11.4.3.2, 'Programming System Clock Frequency with Frequency Modulation.'

Added 'Caution: Programming a PREDIV value such that the ICO operates outside its specified range will cause unpredictable results and the FMPLL will not lock. Refer to the MPC5553/MPC5554 Data Sheet for details on the ICO range.' to Table 11-10 (Clock-out vs. Clock-in Relationships).

Frequency Modulated Phase Locked Loop (FMPLL) and System Clocks
