### Chatper 6

## System Integration Unit (SIU)

## 6.1 Introduction

This chapter describes the MPC5553/MPC5554 system integration unit (SIU), which controls MCU reset configuration,  pad  configuration,  external  interrupt,  general-purpose  I/O  (GPIO),  internal  peripheral multiplexing, and the system reset operation.

## 6.1.1 Block Diagram

Figure 6-1 is a block diagram of the SIU. The signals shown are external pins to the device. The SIU registers are accessed through the crossbar switch. Note that the power-on reset detection module, pad interface/pad ring module, and peripheral I/O channels are external to the SIU.

Figure 6-1. SIU Block Diagram

<!-- image -->

## 6.1.2 Overview

The  MPC5553/MPC5554  system  integration  unit  (SIU)  controls  MCU  reset  configuration,  pad configuration, external interrupt, general-purpose I/O (GPIO), internal peripheral multiplexing, and the system reset operation. The reset configuration module contains the external pin boot configuration logic. The pad configuration module controls the static electrical characteristics of I/O pins. The GPIO module provides  uniform  and  discrete  input/output  control  of  the  I/O  pins  of  the  MCU.  The  reset  controller performs reset monitoring of internal and external reset sources, and drives the RSTOUT pin. The SIU is accessed by the e200z6 core through the system bus crossbar switch (XBAR) and the peripheral bridge A (PBRIDGE\_A).

## 6.1.3 Features

Features include the following:

- · System configuration
- - MCU reset configuration via external pins
- - Pad configuration control
- · System reset monitoring and generation
- - Power-on reset support
- - Reset status register providing last reset source to software
- - Glitch detection on reset input
- - Software controlled reset assertion
- · External Interrupt
- - 16 (MPC5554) or 16 (MPC5553) interrupt requests
- - Rising or falling edge event detection
- - Programmable digital filter for glitch rejection
- · GPIO
- - GPIO function on 214 I/O pins (MPC5554). There are 177 GPIO pins in the MPC5553.
- - Dedicated input and output registers for each GPIO pin.
- · Internal Multiplexing
- - Allows serial and parallel chaining of DSPIs
- - Allows flexible selection of eQADC trigger inputs
- - Allows selection of interrupt requests between external pins and DSPI

## 6.1.4 Modes of Operation

## 6.1.5 Normal Mode

In normal mode, the SIU provides the register interface and logic that controls system configuration, the reset controller, and GPIO. The SIU continues operation with no changes in stop mode.

## 6.1.6 Debug Mode

SIU operation in debug mode is identical to operation in normal mode.

## 6.2 External Signal Description

Table 6-1 lists the external pins used by the SIU.

## Table 6-1. SIU Signal Properties

| Name   | I/O Type   | Pad Type   | Function     | Pull Up/Down 1   |
|--------|------------|------------|--------------|------------------|
| Resets | Resets     | Resets     | Resets       | Resets           |
| RESET  | Input      | -          | Reset Input  | Up               |
| RSTOUT | Output     | Slow       | Reset Output | -                |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 6-1. SIU Signal Properties (continued)

| Name                 | I/O Type             | Pad Type             | Function                                          | Pull Up/Down 1       |
|----------------------|----------------------|----------------------|---------------------------------------------------|----------------------|
| System Configuration | System Configuration | System Configuration | System Configuration                              | System Configuration |
| GPIO[0:210]          | I/O                  | Slow                 | General-Purpose I/O                               | Up/Down              |
| BOOTCFG0_ GPIO211    | Input I/O            | Slow                 | Boot Configuration Input / General-Purpose I/O    | Down Up/Down         |
| BOOTCFG1_ GPIO212    | Input I/O            | Slow                 | Boot Configuration Input / General-Purpose I/O    | Down Up/Down         |
| WKPCFG GPIO213       | Input I/O            | Slow                 | Weak Pull Configuration Pin / General-Purpose I/O | Up Up/Down           |
| External Interrupt   | External Interrupt   | External Interrupt   | External Interrupt                                | External Interrupt   |
| IRQ[0:15] 2          | Input                | Slow                 | External Interrupt Request Input                  | - 3                  |

1 Internal weak pull up/down. The reset weak pull up/down state is given by the pull up/down state for the primary pin function. For example, the reset weak pull up/down state of the BOOTCFG0\_GPIO211 pin is weak pull up enabled.

2 The IRQ pins are multiplexed with other functions on the chip.

- 3 The weak pull up/down state at reset for the IRQ[0:15] depends on the pins that they are shared with. The weak pull up/down state for these pins is as follows: IRQ[0,1,4,5,6,7,12,13,14]: Up, IRQ[2,3,15]: Down, IRQ[8:11]: WKPCFG.

## 6.2.1 Detailed Signal Descriptions

## 6.2.1.1 Reset Input (RESET)

The RESET pin is an active low input. The RESET pin is asserted by an external device during a power-on or  external  reset.  The  internal  reset  signal  asserts  only  if  the  RESET  pin  asserts  for  10  clock  cycles. Assertion of the RESET pin while the device is in reset causes the reset cycle to start over. The RESET pin has a glitch detector which detects spikes greater than 2 clock cycles in duration that fall below the switch  point  of  the  input  buffer  logic  of  the  VDDEH  input  pins.  The  switch  point  lies  between  the maximum VIL and minimum VIH specifications for the VDDEH input pins.

## 6.2.1.2 Reset Output (RSTOUT)

The RSTOUT pin is an active low output that uses a push/pull configuration. The RSTOUT pin is driven to the low state by the MCU for all internal and external reset sources. After the negation of the RESET input, RSTOUT is asserted for 2404 clock cycles; except that if the PLL is configured for dual-controller mode, RSTOUT is asserted for 16004 clocks.

The RSTOUT pin can also be asserted for 2400 clock cycles by a write to the SER bit of the system reset control register (SIU\_SRCR).

## NOTE

During a power on reset, RSTOUT is tri-stated.

## 6.2.1.3 General-Purpose I/O Pins (GPIO[0:210])

The  GPIO  pins  provide  general-purpose  input  and  output  function.  The  GPIO  pins  are  generally multiplexed with other I/O pin functions. Each GPIO input and output is separately controlled by an eight-bit input (SIU\_GPDI) or output (SIU\_GPDO) register. See Section 6.3.1.13, 'GPIO Pin Data Output Registers 0-213  (SIU\_GPDOn)'  and  Section 6.3.1.14,  'GPIO  Pin  Data  Input  Registers  0-213 (SIU\_GPDIn)'.

## 6.2.1.4 Boot Configuration Pins (BOOTCFG[0:1])

The boot configuration pins specify the boot mode initiated by the boot assist module (BAM) program. BOOTCFG[0:1] are input pins that are sampled 4 clock cycles before the negation of the RSTOUT pin, and the values latched are stored in the reset status register (SIU\_RSR). This occurs for all reset sources except a debug port reset and a software external reset. The BOOTCFG[0:1] pins are only sampled if the RSTCFG  pin  is  asserted  during  reset.  Otherwise,  if  the  RSTCFG  pin  is  negated  during  reset,  the BOOTCFG[0:1] pins are not sampled, the BAM defaults to boot from internal Flash, and the BOOTCFG field in the SIU\_RSR is set to the boot from internal Flash value (0b00). The latched BOOTCFG[0:1] values are also driven as output signals from the SIU.

The BOOTCFG pin values are used only if the RSTCFG pin is asserted during the assertion of RSTOUT. Otherwise, the default values for the BOOTCFG bits in the SIU\_RSR are used.

## 6.2.1.5 I/O Pin Weak Pull Up Reset Configuration Pin (WKPCFG)

The WKPCFG pin is applied at the assertion of the internal reset signal (indicated by the assertion of RSTOUT), and is sampled 4 clock cycles before the negation of the RSTOUT pin. The value is used to configure whether the eTPU and eMIOS pins are connected to internal weak pull up or weak pull down devices after reset. The value latched on the WKPCFG pin at reset is stored in the reset status register (SIU\_RSR), and is updated for all reset sources except the debug port reset and software external reset.

## 6.2.1.6 External Interrupt Request Input Pins (IRQ[0:15])

The IRQ[0:15] connect to the SIU IRQ inputs. SIU\_ETISR select register 1 is used to select the IRQ[0:15] pins  as  inputs  to  the  IRQs.  The  counter  operates  independently  of  IRQ  or  overrun  flag  bit  clearing. Clearing an IRQ or overrun flag bit does not clear or reload the counter.

Rising or falling  edge  events  are  enabled  by  setting  the  corresponding  bits  in  the  SIU\_IREER  or  the SIU\_IFEER. If the same bit location is set in both registers, both rising and falling edge events will cause the corresponding IRQ Flag bit in Section 6.3.1.4, 'External Interrupt Status Register (SIU\_EISR)' to be set.

## 6.2.1.6.1 External Interrupts

The IRQ  pins map to 16 independent interrupt request outputs from the SIU. An interrupt request is n asserted when the corresponding IRQ flag bit is set in Section 6.3.1.4, 'External Interrupt Status Register (SIU\_EISR)' with the corresponding dma/interrupt request enable bit set in Section 6.3.1.5, 'DMA/Interrupt Request Enable Register (SIU\_DIRER),' and the corresponding dma/interrupt select bit cleared in Section 6.3.1.6, 'DMA/Interrupt Request Select Register (SIU\_DIRSR).' The IRQ flag bit is set when  an  event  as  defined  by  the  Section 6.3.1.9,  'IRQ  Rising-Edge  Event  Enable  Register (SIU\_IREER),' occurs on the corresponding IRQ n pin.

## 6.2.1.6.2 DMA Transfers

The IRQ  pins map to 16 independent DMA request outputs from the SIU. A DMA request is asserted n when  the  corresponding  IRQ  flag  bit  is  set  in  Section 6.3.1.4,  'External  Interrupt  Status  Register (SIU\_EISR),' with the corresponding dma/interrupt request enable bit set in Section 6.3.1.5, 'DMA/Interrupt Request Enable Register (SIU\_DIRER),' and the corresponding dma/interrupt select bit set in Section 6.3.1.6, 'DMA/Interrupt Request Select Register (SIU\_DIRSR).' A DMA done signal is input  to  the  SIU  for  each  DMA  request  output.  The  assertion  of  a  DMA  done  signal  clears  the corresponding IRQ Flag bit.

## 6.2.1.6.3 Overruns

An overrun interrupt request exists for each overrun flag in the SIU. In addition, there is one overrun interrupt request output from the SIU which is the logical OR of all of the overrun interrupt requests. An overrun interrupt request is asserted if any of the same bit locations are set in Section 6.3.1.7, 'Overrun Status Register (SIU\_OSR),' and Section 6.3.1.8, 'Overrun Request Enable Register (SIU\_ORER).' An overrun occurs if an edge triggered event occurs on an IRQ n pin while the corresponding IRQ flag bit is set in Section 6.3.1.4, 'External Interrupt Status Register (SIU\_EISR).'

## 6.2.1.6.4 Edge Detects

The IRQ  pins can be used as edge detect pins. Edge detect operation is enabled by selecting rising or n falling  edge  events  in  Section 6.3.1.9,  'IRQ  Rising-Edge  Event  Enable  Register  (SIU\_IREER),'  with dma/interrupt requests disabled. The external IRQ status register reflects whether the desired edge has been captured on each pin.

## 6.3 Memory Map/Register Definition

Table 6-2 is the address map for the SIU registers. All register addresses are given as an offset of the SIU base address.

Table 6-2. SIU Address Map

| Address            | Register Name   | Register Description                   | Size (bits)   |
|--------------------|-----------------|----------------------------------------|---------------|
| Base (0xC3F9_0000) | -               | Reserved                               | -             |
| Base + 0x4         | SIU_MIDR        | MCU ID register                        | 32            |
| Base + 0x8         | -               | Reserved                               | -             |
| Base + 0xC         | SIU_RSR         | Reset status register                  | 32            |
| Base + 0x10        | SIU_SRCR        | System reset control register          | 32            |
| Base + 0x14        | SIU_EISR        | SIU external interrupt status register | 32            |
| Base + 0x18        | SIU_DIRER       | DMA/interrupt request enable register  | 32            |
| Base + 0x1C        | SIU_DIRSR       | DMA/interrupt request select register  | 32            |
| Base + 0x20        | SIU_OSR         | Overrun status register                | 32            |
| Base + 0x24        | SIU_ORER        | Overrun request enable register        | 32            |
| Base + 0x28        | SIU_IREER       | IRQ rising-edge event enable register  | 32            |
| Base + 0x2C        | SIU_IFEER       | IRQ falling-edge event enable register | 32            |

Table 6-2. SIU Address Map (continued)

| Address                    | Register Name          | Register Description                 | Size (bits)   |
|----------------------------|------------------------|--------------------------------------|---------------|
| Base + 0x30                | SIU_IDFR               | IRQ digital filter register          | 32            |
| Base + 0x34- Base + 0x3F   | -                      | Reserved                             | -             |
| Base + 0x40- Base + 0x20C  | SIU_PCR0- SIU_PCR230   | Pad configuration registers 0-230    | 16            |
| Base + 0x20E- Base + 0x5FF | -                      | Reserved                             | -             |
| Base + 0x600- Base + 0x6D5 | SIU_GPDO0- SIU_GPDO213 | GPIO pin data output registers 0-213 | 8             |
| Base + 0x6D6- Base + 0x7FF | -                      | Reserved                             | -             |
| Base + 0x800- Base + 0x8D5 | SIU_GPDI0- SIU_GPDI213 | GPIO pin data input registers 0-213  | 8             |
| Base + 0x8D6- Base + 0x8FF | -                      | Reserved                             | -             |
| Base + 0x900- Base + 0x903 | SIU_ETISR              | eQADC trigger input select register  | 32            |
| Base + 0x904- Base + 0x907 | SIU_EIISR              | External IRQ input select register   | 32            |
| Base + 0x908- Base + 0x90B | SIU_DISR               | DSPI input select register           | 32            |
| Base + 0x90C- Base + 0x97F | -                      | Reserved                             | -             |
| Base + 0x980               | SIU_CCR                | Chip configuration register          | 32            |
| Base + 0x984               | SIU_ECCR               | External clock control register      | 32            |
| Base + 0x988               | SIU_CARH               | Compare A high register              | 32            |
| Base + 0x98C               | SIU_CARL               | Compare A low register               | 32            |
| Base + 0x990               | SIU_CBRH               | Compare B high register              | 32            |
| Base + 0x994               | SIU_CBRL               | Compare B low register               | 32            |
| Base + 0x998- Base + 0x9FF | -                      | Reserved                             | -             |

## 6.3.1 Register Descriptions

## 6.3.1.1 MCU ID Register (SIU\_MIDR)

The SIU\_MIDR contains the part identification number and mask revision number specific to the device. The part number is a read-only field that is mask programmed with the part number of the device. The part number is changed if a new module is added to the device or a memory size is changed, for example. It is not  changed  for  bug  fixes  or  process  changes.  The  mask  number  is  a  read-only  field  that  is  mask

programmed with the specific mask revision level of the device. The current value applies to revision 0 and will be updated for each mask revision.

Figure 6-2. MCU ID Register (SIU\_MIDR)

<!-- image -->

|                       | 0          | 1          | 2          | 3          | 4          | 5          | 6          | 7          | 8             | 9             | 10            | 11            | 12            | 13            | 14            | 15            |
|-----------------------|------------|------------|------------|------------|------------|------------|------------|------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| R                     | PARTNUM    | PARTNUM    | PARTNUM    | PARTNUM    | PARTNUM    | PARTNUM    | PARTNUM    | PARTNUM    | PARTNUM       | PARTNUM       | PARTNUM       | PARTNUM       | PARTNUM       | PARTNUM       | PARTNUM       | PARTNUM       |
| W                     |            |            |            |            |            |            |            |            |               |               |               |               |               |               |               |               |
| Reset MPC5553         | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0             | 1             | 0             | 1             | 0             | 0             | 1             | 1             |
| Reset MPC5554         | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Reg Addr              | Base + 0x4 | Base + 0x4 | Base + 0x4 | Base + 0x4 | Base + 0x4 | Base + 0x4 | Base + 0x4 | Base + 0x4 | Base + 0x4    | Base + 0x4    | Base + 0x4    | Base + 0x4    | Base + 0x4    | Base + 0x4    | Base + 0x4    | Base + 0x4    |
|                       | 16         | 17         | 18         | 19         | 20         | 21         | 22         | 23         | 24            | 25            | 26            | 27            | 28            | 29            | 30            | 31            |
| R                     | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | MASKNUM_MAJOR | MASKNUM_MAJOR | MASKNUM_MAJOR | MASKNUM_MAJOR | MASKNUM_MINOR | MASKNUM_MINOR | MASKNUM_MINOR | MASKNUM_MINOR |
| W Reset               | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| MPC5553 Reset MPC5554 | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Reg Addr              | Base + 0x4 | Base + 0x4 | Base + 0x4 | Base + 0x4 | Base + 0x4 | Base + 0x4 | Base + 0x4 | Base + 0x4 | Base + 0x4    | Base + 0x4    | Base + 0x4    | Base + 0x4    | Base + 0x4    | Base + 0x4    | Base + 0x4    | Base + 0x4    |

Table 6-3. SIU\_MIDR Field Descriptions

| Bits   | Name                | Description                                                                                                                                                                                             |
|--------|---------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-15   | PARTNUM [0:15]      | MCU part number. Read-only, mask programmed part identification number of the MCU. Reads 0x00 for the MPC5554. For the MPC5553 the value is 0x53.                                                       |
| 16-23  | -                   | Reserved                                                                                                                                                                                                |
| 24-27  | MASKNUM_MAJOR [0:3] | Major revision number of MCUmask. Read-only, mask programmed mask number of the MCU. Reads 0x0 for the initial mask set of the MPC5554 and the MPC5553, and will change sequentially for each mask set. |
| 28-31  | MASKNUM_MINOR [0:3] | Minor revision number of MCUmask. Read-only, mask programmed mask number of the MCU. Reads 0x0 for the initial mask set of the MPC5554 and the MPC5553, and will change sequentially for each mask set. |

## 6.3.1.2 Reset Status Register (SIU\_RSR)

The SIU\_RSR reflects the most recent source, or sources of reset, and the state of configuration pins at reset. This register contains one bit for each reset source, indicating that the last reset was power-on reset (POR), external, software system, software external reset, watchdog, loss of PLL lock, loss of clock or checkstop reset. A reset status bit set to logic one indicates the type of reset that occurred. Once set, the

reset source status bits in the SIU\_RSR remain set until another reset occurs. In the following cases more than one reset bit is set:

- 1. If a power-on reset request has negated and the MPC5553/MPC5554 is still in the resulting reset, and then an external reset is requested, both the power-on and external reset status bits will be set. In this case, the MPC5553/MPC5554 started the reset sequence due to a power-on reset request, but it ended the reset sequence after an external reset request.
- 2. If a software external reset is requested, the SERF flag bit is set, but no previously set bits in the SIU\_RSR will be cleared. The SERF bit is cleared by writing a 1 to the bit location or when another reset source is asserted.
- 3. If any of the loss of clock, loss of lock, watchdog or checkstop reset requests occur on the same clock cycle, and no other higher priority reset source is requesting reset (See Table 6-4), the reset status bits for all of the requesting resets will be set.

Simultaneous reset requests are prioritized. When reset requests of different priorities occur on the same clock cycle, the lower priority reset request will be ignored. Only the highest priority reset request's status bit will be set. Except for a power-on reset request and condition 1 above, all reset requests of any priority are ignored until the MPC5553/MPC5554 exits reset.

Table 6-4. Reset Source Priorities

| Reset Source                                              | Priority   |
|-----------------------------------------------------------|------------|
| Power on reset (POR) and external reset (Group 0)         | Highest    |
| Software system reset (Group1)                            |            |
| Loss of clock, loss of lock, watchdog, checkstop (Group2) |            |
| Software external reset (Group 3)                         | Lowest     |

<!-- image -->

|          | 0          | 1          | 2          | 3          | 4          | 5          | 6          | 7          | 8          | 9          | 10         | 11         | 12         | 13         | 14         | 15         |
|----------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|
| R        | PORS       | ERS        | LLRS       | LCRS       | WDRS       | CRS        | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | SSRS       | SERF       |
| W        |            |            |            |            |            |            |            |            |            |            |            |            |            |            |            |            |
| Reset 1  | 1          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          |
| Reg Addr | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC |
|          | 16         | 17         | 18         | 19         | 20         | 21         | 22         | 23         | 24         | 25         | 26         | 27         | 28         | 29         | 30         | 31         |
| R        | WKP CFG 2  | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | BOOTCFG    | BOOTCFG    | RGF        |
| W        |            |            |            |            |            |            |            |            |            |            |            |            |            |            |            |            |
| Reset 1  | U 2 U 3    | U 2 U 3    | U 2 U 3    | U 2 U 3    | U 2 U 3    | U 2 U 3    | U 2 U 3    | U 2 U 3    | U 2 U 3    | U 2 U 3    | U 2 U 3    | U 2 U 3    | U 2 U 3    | U 2 U 3    | U 2 U 3    | 0          |
| Reg Addr | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC |

1 The reset status register receives its reset values during power-on reset.

2 The reset value of the WKPCFG bit is determined by the value on the WKPCFG pin at reset.

3 The reset value of the BOOTCFG field is determined by the values on the BOOTCFG[0:1] pins at reset.

Figure 6-3. Reset Status Register (SIU\_RSR)

Table 6-5. SIU\_RSR Field Descriptions

| Bits   | Name   | Description                                                                                                                                                                                                                                                                                                                                       |
|--------|--------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0      | PORS   | Power-on reset status. 0 Another reset source has been acknowledged by the reset controller since the last assertion of the power-on reset input. 1 The power-on reset input to the reset controller has been asserted and no other reset source has been acknowledged since that assertion of the power-on reset input except an external reset. |
| 1      | ERS    | External reset status. 0 The last reset source acknowledged by the reset controller was not a valid assertion of the RESET pin. 1 The last reset source acknowledged by the reset controller was a valid assertion of the RESET pin.                                                                                                              |
| 2      | LLRS   | Loss of lock reset status. 0 The last reset source acknowledged by the reset controller was not a loss of PLL lock reset. 1 The last reset source acknowledged by the reset controller was a loss of PLL lock reset.                                                                                                                              |
| 3      | LCRS   | Loss of clock reset status. 0 The last reset source acknowledged by the reset controller was not a loss of clock reset. 1 The last reset source acknowledged by the reset controller was a loss of clock reset.                                                                                                                                   |
| 4      | WDRS   | Watchdog timer/debug reset status. 0 The last reset source acknowledged by the reset controller was not a watchdog timer or debug reset. 1 The last reset source acknowledged by the reset controller was a watchdog timer or debug reset.                                                                                                        |
| 5      | CRS    | Checkstop reset status. 0 The last reset source acknowledged by the reset controller was not an enabled checkstop reset. 1 The last reset source acknowledged by the reset controller was an enabled checkstop reset.                                                                                                                             |
| 6-13   | -      | Reserved.                                                                                                                                                                                                                                                                                                                                         |
| 14     | SSRS   | Software system reset status. 0 The last reset source acknowledged by the reset controller was not a software system reset. 1 The last reset source acknowledged by the reset controller was a software system reset.                                                                                                                             |
| 15     | SERF   | Software external reset flag. 0 This bit has been cleared from a 1 to a 0 by a write of 1 to it when it was a 1 or the software external reset input to the reset controller has not been asserted. 1 The software external reset input to the reset controller has been asserted while this bit was a 0.                                         |
| 16     | WKPCFG | Weak pull configuration pin status 0 The WKPCFGpin latched during the last reset was a logical 0 and weak pull down is the default setting 1 The WKPCFG pin latched during the last reset was a logical 1 and weak pullup is the default setting                                                                                                  |
| 17-28  | -      | Reserved.                                                                                                                                                                                                                                                                                                                                         |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 6-5. SIU\_RSR Field Descriptions (continued)

| Bits   | Name    | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|--------|---------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 29-30  | BOOTCFG | Reset configuration pin status. Holds the value of the BOOTCFGpins that were latched on the last negation of the RSTOUT pin, if the RSTCFG pin was asserted. If the RSTCFG pin was not asserted at the last negation of RSTOUT, and the lower half or least significant half word of the censorship control word equals 0xFFFF or 0x0000, the BOOTCFG field is set to the value 0b10. Otherwise, if the RSTCFG pin was negated at the last negation of RSTOUT and the lower half of the censorship control word does not equal 0xFFFF or 0x0000, then the BOOTCFG field is set to the value 0b00. The BOOTCFG field is used by the BAM program to determine the location of the reset configuration half word. See Table 4-10 for a translation of the reset configuration half word location from the BOOTCFG field value. |
| 31     | RGF     | Reset glitch flag. Set by the reset controller when a glitch is detected on the RESET pin. This bit is cleared by the assertion of the power-on reset input to the reset controller, or a write of 1 to the RGF bit. See Section 6.4.2.1, 'RESET Pin Glitch Detect,' for more information on glitch detection. 0 No glitch has been detected on the RESET pin. 1 A glitch has been detected on the RESET pin.                                                                                                                                                                                                                                                                                                                                                                                                               |

## 6.3.1.3 System Reset Control Register (SIU\_SRCR)

The system reset control register allows software to generate either a system or external reset. The software system reset causes an internal reset, while the software external reset only causes the external RSTOUT pin to be asserted. When written to 1, the SER bit automatically clears.

|          | 0           | 1           | 2           | 3           | 4           | 5           | 6           | 7           | 8           | 9           | 10          | 11          | 12          | 13          | 14          | 15          |
|----------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|
| R        | SSR 1       | SER         | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           |
| W        |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |
| Reset    | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           |
| Reg Addr | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 |
|          | 16          | 17          | 18          | 19          | 20          | 21          | 22          | 23          | 24          | 25          | 26          | 27          | 28          | 29          | 30          | 31          |
| R        | CRE         | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           |
| W        |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |
| Reset    | 1 2         | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           |
| Reg Addr | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 |

- 1 The SSR bit always reads as 0. A write of 0 to this bit has no effect.
- 2 The CRE bit is set to 1 by POR. Other resets sources do not reset the bit value.

Figure 6-4. System Reset Control Register (SIU\_SRCR)

## Table 6-6. SIU\_SRCR Field Descriptions

| Bits   | Name   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|--------|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0      | SSR    | Software system reset. Used to generate a software system reset. Writing a 1 to this bit causes an internal reset. The software system reset is processed as a synchronous reset. The bit is automatically cleared on the assertion of any other reset source except a software external reset. 0 Do not generate a software system reset. 1 Generate a software system reset.                                                                                                                                                                                                                                                                                                                                               |
| 1      | SER    | Software external reset. Used to generate a software external reset. Writing a 1 to this bit causes the RSTOUTpin to be asserted for 2400 clocks, but the internal reset is not asserted. The bit is automatically cleared when the software external reset completes or any other reset source is asserted. Once a software external reset has been initiated, the RSTOUT pin is negated if this bit is cleared before the 2400 clock period expires. 0 Do not generate a software external reset. 1 Generate a software external reset. Note: If the PLL is configured for dual controller mode writing a 1 to SER causes the RSTOUT pin to be asserted for 16000 clocks. Refer to Section 4.2.2, 'Reset Output (RSTOUT).' |
| 2-15   | -      | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| 16     | CRE    | Checkstop reset enable. Writing a 1 to this bit enables a reset when the checkstop reset request input is asserted. The checkstop reset request input is a synchronous internal reset source. The CRE bit defaults to checkstop reset enabled at POR. If this bit is cleared, it remains cleared until the next POR. 0 No reset occurs when the checkstop reset input to the reset controller is asserted. 1 A reset occurs when the checkstop reset input to the reset controller is asserted.                                                                                                                                                                                                                              |
| 17-31  | -      | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |

## 6.3.1.4 External Interrupt Status Register (SIU\_EISR)

The external interrupt status register is used to record edge triggered events on the IRQ0 - IRQ15 inputs to the SIU. When an edge triggered event is enabled in the SIU\_IREER or SIU\_IFEER for an IRQ n input and then sensed, the corresponding SIU\_EISR flag bit is set. The IRQ flag bit is set regardless of the state of the corresponding dma/interrupt request enable bit in SIU\_DIRER. The IRQ flag bit remains set until cleared by software or through the servicing of a DMA request. The IRQ flag bits are cleared by writing a 1 to the bits. A write of 0 has no effect.

Figure 6-5. SIU External Interrupt Status Register (SIU\_EISR)

<!-- image -->

Table 6-7. SIU\_EISR Field Descriptions

| Bits   | Name   | Function                                                                                                                                                                                                                                                                   |
|--------|--------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-15   | -      | Reserved                                                                                                                                                                                                                                                                   |
| 16-31  | EIF n  | External interrupt request flag n. This bit is set when an edge triggered event occurs on the corresponding IRQ n input. 0 No edge triggered event has occurred on the corresponding IRQ n input. 1 An edge triggered event has occurred on the corresponding IRQ n input. |

## 6.3.1.5 DMA/Interrupt Request Enable Register (SIU\_DIRER)

The SIU\_DIRER allows the assertion of a DMA or interrupt request if the corresponding flag bit is set in the SIU\_EISR. The external interrupt request enable bits enable the interrupt or DMA request. There is only one interrupt request from the SIU to the interrupt controller. The EIRE bits allow selection of which external interrupt request flag bits cause assertion of the one interrupt request signal.

Figure 6-6. SIU DMA/Interrupt Request Enable Register (SIU\_DIRER)

<!-- image -->

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 6-8. SIU\_DIRER Field Descriptions

| Bits   | Name   | Function                                                                                                                                                                                                                                                              |
|--------|--------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-15   | -      | Reserved.                                                                                                                                                                                                                                                             |
| 16-31  | EIRE n | External interrupt request enable n. Enables the assertion of the interrupt request from the SIU to the interrupt controller when an edge triggered event occurs on the IRQ n pin. 0 External interrupt request is disabled. 1 External interrupt request is enabled. |

## 6.3.1.6 DMA/Interrupt Request Select Register (SIU\_DIRSR)

The SIU\_DIRSR allows selection between a DMA or interrupt request for events on the IRQ0-IRQ3 inputs. The SIU\_DIRSR selects between DMA and interrupt requests. If the corresponding bits are set in SIU\_EISR and the SIU\_DIRER, then the DMA/interrupt request select bit determines whether a DMA or interrupt request is asserted.

Figure 6-7. DMA/Interrupt Request Select Register (SIU\_DIRSR)

<!-- image -->

|          | 0           | 1           | 2           | 3           | 4           | 5           | 6           | 7           | 8           | 9           | 10          | 11          | 12          | 13          | 14          | 15          |
|----------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|
| R        | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           |
| W        |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |
| Reset    | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           |
| Reg Addr | Base + 0x1C | Base + 0x1C | Base + 0x1C | Base + 0x1C | Base + 0x1C | Base + 0x1C | Base + 0x1C | Base + 0x1C | Base + 0x1C | Base + 0x1C | Base + 0x1C | Base + 0x1C | Base + 0x1C | Base + 0x1C | Base + 0x1C | Base + 0x1C |
|          | 16          | 17          | 18          | 19          | 20          | 21          | 22          | 23          | 24          | 25          | 26          | 27          | 28          | 29          | 30          | 31          |
| R        | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | DIRS3       | DIRS2       | DIRS1       | DIRS0       |
| W        |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |
| Reset    | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           |
| Reg Addr | Base + 0x1C | Base + 0x1C | Base + 0x1C | Base + 0x1C | Base + 0x1C | Base + 0x1C | Base + 0x1C | Base + 0x1C | Base + 0x1C | Base + 0x1C | Base + 0x1C | Base + 0x1C | Base + 0x1C | Base + 0x1C | Base + 0x1C | Base + 0x1C |

Table 6-9. SIU\_DIRER Field Descriptions

| Bits   | Name   | Function                                                                                                                                                                                                 |
|--------|--------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-27   | -      | Reserved.                                                                                                                                                                                                |
| 28-31  | DIRS n | DMA/interrupt request select n. Selects between a DMAorinterrupt request when an edge triggered event occurs on the corresponding IRQ n pin. 0 Interrupt request is selected. 1 DMA request is selected. |

## 6.3.1.7 Overrun Status Register (SIU\_OSR)

The SIU\_OSR contains flag bits that record an overrun.

Figure 6-8. Overrun Status Register (SIU\_OSR)

<!-- image -->

Table 6-10. SIU\_OSR Field Descriptions

| Bits   | Name   | Function                                                                                                                                                                                                   |
|--------|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-15   | -      | Reserved.                                                                                                                                                                                                  |
| 16-31  | OVF n  | Overrun flag n. This bit is set when an overrun occurs on the corresponding IRQ n pin. 0 No overrun has occurred on the corresponding IRQ n pin. 1 An overrun has occurred on the corresponding IRQ n pin. |

## 6.3.1.8 Overrun Request Enable Register (SIU\_ORER)

The SIU\_ORER contains bits to enable an overrun if the corresponding flag bit is set in the SIU\_OSR. If any overrun request enable bit and the corresponding flag bit are set, the single combined overrun request from the SIU to the interrupt controller is asserted.

Figure 6-9. Overrun Request Enable Register (SIU\_ORER)

<!-- image -->

Table 6-11. SIU\_ORER Field Descriptions

| Bits   | Name   | Function                                                                                                                                                                                 |
|--------|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-15   | -      | Reserved.                                                                                                                                                                                |
| 16-31  | ORE n  | Overrun request enable n. E nables the corresponding overrun request when an overrun occurs on the corresponding IRQ n pin. 0 Overrun request is disabled. 1 Overrun request is enabled. |

## 6.3.1.9 IRQ Rising-Edge Event Enable Register (SIU\_IREER)

The SIU\_IREER allows rising edge triggered events to be enabled on the corresponding IRQ n pins. Rising and falling edge events can be enabled by setting the corresponding bits in both the SIU\_IREER and SIU\_IFEER.

Figure 6-10. IRQ Rising-Edge Event Enable Register (SIU\_IREER)

<!-- image -->

|          | 0           | 1           | 2           | 3           | 4           | 5           | 6           | 7           | 8           | 9           | 10          | 11          | 12          | 13          | 14          | 15          |
|----------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|
| R        | 0           | 0           | 0           | 0           |             | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           |
| W        |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |
| Reset    | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           |
| Reg Addr | Base + 0x28 | Base + 0x28 | Base + 0x28 | Base + 0x28 | Base + 0x28 | Base + 0x28 | Base + 0x28 | Base + 0x28 | Base + 0x28 | Base + 0x28 | Base + 0x28 | Base + 0x28 | Base + 0x28 | Base + 0x28 | Base + 0x28 | Base + 0x28 |
|          | 16          | 17          | 18          | 19          | 20          | 21          | 22          | 23          | 24          | 25          | 26          | 27          | 28          | 29          | 30          | 31          |
| R        | IREE 15     | IREE 14     | IREE 13     | IREE 12     | IREE 11     | IREE 10     | IREE 9      | IREE 8      | IREE 7      | IREE 6      | IREE 5      | IREE 4      | IREE 3      | IREE 2      | IREE 1      | IREE 0      |
| W        |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |
| Reset    | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           |
| Reg Addr | Base + 0x28 | Base + 0x28 | Base + 0x28 | Base + 0x28 | Base + 0x28 | Base + 0x28 | Base + 0x28 | Base + 0x28 | Base + 0x28 | Base + 0x28 | Base + 0x28 | Base + 0x28 | Base + 0x28 | Base + 0x28 | Base + 0x28 | Base + 0x28 |

Table 6-12. SIU\_IREER Field Descriptions

| Bits   | Name   | Function                                                                                                                                                              |
|--------|--------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-15   | -      | Reserved.                                                                                                                                                             |
| 16-31  | IREE n | IRQ rising-edge event enable n. Enables rising-edge triggered events on the corresponding IRQ n pin. 0 Rising edge event is disabled. 1 Rising edge event is enabled. |

## 6.3.1.10 IRQ Falling-Edge Event Enable Register (SIU\_IFEER)

The SIU\_IFEER allows falling edge triggered events to be enabled on the corresponding IRQ n pins. Rising and falling edge events can be enabled by setting the corresponding bits in both the SIU\_IREER and SIU\_IFEER.

Figure 6-11. IRQ Falling-Edge Event Enable Register (SIU\_IFEER)

<!-- image -->

Table 6-13. SIU\_IFEER Field Descriptions

| Bits   | Name   | Function                                                                                                                                                                  |
|--------|--------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-15   | -      | Reserved.                                                                                                                                                                 |
| 16-31  | IFEE n | IRQ falling-edge event enable n. Enables falling-edge triggered events on the corresponding IRQ n pin. 0 Falling edge event is disabled. 1 Falling edge event is enabled. |

## 6.3.1.11 IRQ Digital Filter Register (SIU\_IDFR)

The SIU\_IDFR specifies the amount of digital filtering on the IRQ0-IRQ15 pins. The digital filter length field specifies the number of system clocks that define the period of the digital filter and the minimum time a signal must be held in the active state on the IRQ pins to be recognized as an edge triggered event.

Figure 6-12. External IRQ Digital Filter Register (SIU\_IDFR)

<!-- image -->

|          | 0           | 1           | 2           | 3           | 4           | 5           | 6           | 7           | 8           | 9           | 10          | 11          | 12          | 13          | 14          | 15          |
|----------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|
| R        | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           |
| W        |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |
| Reset    | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           |
| Reg Addr | Base + 0x30 | Base + 0x30 | Base + 0x30 | Base + 0x30 | Base + 0x30 | Base + 0x30 | Base + 0x30 | Base + 0x30 | Base + 0x30 | Base + 0x30 | Base + 0x30 | Base + 0x30 | Base + 0x30 | Base + 0x30 | Base + 0x30 | Base + 0x30 |
|          | 16          | 17          | 18          | 19          | 20          | 21          | 22          | 23          | 24          | 25          | 26          | 27          | 28          | 29          | 30          | 31          |
| R        | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           |             | DFL         | DFL         |             |
| W        |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |
| Reset    | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           |
| Reg Addr | Base + 0x30 | Base + 0x30 | Base + 0x30 | Base + 0x30 | Base + 0x30 | Base + 0x30 | Base + 0x30 | Base + 0x30 | Base + 0x30 | Base + 0x30 | Base + 0x30 | Base + 0x30 | Base + 0x30 | Base + 0x30 | Base + 0x30 | Base + 0x30 |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 6-14. SIU\_IDFR Field Descriptions

| Bits   | Name   | Function                                                                                                                                                                                                                                                                                                                                                              |
|--------|--------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-27   | -      | Reserved.                                                                                                                                                                                                                                                                                                                                                             |
| 28-31  | DFL    | Digital filter length. Defines the digital filter period on the IRQ n inputs according to the following equation: For a 100-MHz system clock, this gives a range of 20ns to 328us. The minimum time of three clocks accounts for synchronization of the IRQ input pins with the system clock. Filter Period SystemClockPeriod 2 DFL × ( ) 1 SystemClockPeriod ( ) + = |

## 6.3.1.12 Pad Configuration Registers (SIU\_PCR)

The following subsections define the SIU\_PCRs for all device pins that allow configuration of the pin function, direction, and static electrical attributes. The information presented pertains to which bits and fields are active for a given pin or group of pins, and the reset state of the register. Note that the reset state of SIU\_PCRs given in the following sections is that prior to execution of the BAM program. The BAM program may change certain SIU\_PCRs based on the reset configuration. See the BAM section of the manual for more detail.

The  SIU\_PCRs  are  16-bit  registers  that  may  be  read  or  written  as  16-bit  values  aligned  on  16-bit boundaries, or as 32-bit values aligned on 32-bit address boundaries. Table 6-15 describes the SIU\_PCR fields.

## NOTE

Not all of the fields may be present in a given SIU\_PCR, depending on the type of pad it controls. See the specific SIU\_PCR definition.

All MPC5553/MPC5554 pin names begin with the primary function, followed by the alternate function, and then GPIO. In some cases the third function may not be GPIO. Those exceptions are noted in the documentation.  For  example,  for  SIU\_PCR85  and  the  pin  CNTXB\_PCSC3\_GPIO85,  CNTXB  is  the primary function and PCSC3 is the alternate function. For identification of the source module for primary and alternate functions, and the description of these signals, see Chapter 2, 'Signal Description' of this manual. Also see the chapter of the specific module that uses the signal for an additional signal description.

## Table 6-15. SIU\_PCR Field Descriptions

| Bits   | Name      | Description                                                                                                                                                                                                                                                                                        | Description                                                                                                                                                                                                                                                                                        | Description                                                                                                                                                                                                                                                                                        | Description                                                                                                                                                                                                                                                                                        | Description                                                                                                                                                                                                                                                                                        | Description                                                                                                                                                                                                                                                                                        | Description                                                                                                                                                                                                                                                                                        | Description                                                                                                                                                                                                                                                                                        | Description                                                                                                                                                                                                                                                                                        | Description                                                                                                                                                                                                                                                                                        |
|--------|-----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-2    | -         | Reserved.                                                                                                                                                                                                                                                                                          | Reserved.                                                                                                                                                                                                                                                                                          | Reserved.                                                                                                                                                                                                                                                                                          | Reserved.                                                                                                                                                                                                                                                                                          | Reserved.                                                                                                                                                                                                                                                                                          | Reserved.                                                                                                                                                                                                                                                                                          | Reserved.                                                                                                                                                                                                                                                                                          | Reserved.                                                                                                                                                                                                                                                                                          | Reserved.                                                                                                                                                                                                                                                                                          | Reserved.                                                                                                                                                                                                                                                                                          |
| 3-5    | PA [0:2]  | Pin assignment. Selects the function of a multiplexed pad. A separate port enable output signal from the SIU is asserted for each value of this register. The size of the field can be from 1 to 3 bits, depending on the amount of multiplexing on the pad                                        | Pin assignment. Selects the function of a multiplexed pad. A separate port enable output signal from the SIU is asserted for each value of this register. The size of the field can be from 1 to 3 bits, depending on the amount of multiplexing on the pad                                        | Pin assignment. Selects the function of a multiplexed pad. A separate port enable output signal from the SIU is asserted for each value of this register. The size of the field can be from 1 to 3 bits, depending on the amount of multiplexing on the pad                                        | Pin assignment. Selects the function of a multiplexed pad. A separate port enable output signal from the SIU is asserted for each value of this register. The size of the field can be from 1 to 3 bits, depending on the amount of multiplexing on the pad                                        | Pin assignment. Selects the function of a multiplexed pad. A separate port enable output signal from the SIU is asserted for each value of this register. The size of the field can be from 1 to 3 bits, depending on the amount of multiplexing on the pad                                        | Pin assignment. Selects the function of a multiplexed pad. A separate port enable output signal from the SIU is asserted for each value of this register. The size of the field can be from 1 to 3 bits, depending on the amount of multiplexing on the pad                                        | Pin assignment. Selects the function of a multiplexed pad. A separate port enable output signal from the SIU is asserted for each value of this register. The size of the field can be from 1 to 3 bits, depending on the amount of multiplexing on the pad                                        | Pin assignment. Selects the function of a multiplexed pad. A separate port enable output signal from the SIU is asserted for each value of this register. The size of the field can be from 1 to 3 bits, depending on the amount of multiplexing on the pad                                        | Pin assignment. Selects the function of a multiplexed pad. A separate port enable output signal from the SIU is asserted for each value of this register. The size of the field can be from 1 to 3 bits, depending on the amount of multiplexing on the pad                                        | Pin assignment. Selects the function of a multiplexed pad. A separate port enable output signal from the SIU is asserted for each value of this register. The size of the field can be from 1 to 3 bits, depending on the amount of multiplexing on the pad                                        |
|        |           | PA Bit Field                                                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                                                                                                    |                                                                                                                                                                                                                                                                                                    |                                                                                                                                                                                                                                                                                                    |                                                                                                                                                                                                                                                                                                    |                                                                                                                                                                                                                                                                                                    |                                                                                                                                                                                                                                                                                                    |                                                                                                                                                                                                                                                                                                    |                                                                                                                                                                                                                                                                                                    | Pin Function 1                                                                                                                                                                                                                                                                                     |
|        |           | 1-bit 2 (2                                                                                                                                                                                                                                                                                         | Functions)                                                                                                                                                                                                                                                                                         | Functions)                                                                                                                                                                                                                                                                                         | Functions)                                                                                                                                                                                                                                                                                         | 2-bit (3 Functions)                                                                                                                                                                                                                                                                                | 2-bit (3 Functions)                                                                                                                                                                                                                                                                                | 3-bit (4 Functions)                                                                                                                                                                                                                                                                                | 3-bit (4 Functions)                                                                                                                                                                                                                                                                                | 3-bit (4 Functions)                                                                                                                                                                                                                                                                                | Pin Function 1                                                                                                                                                                                                                                                                                     |
|        |           | 0                                                                                                                                                                                                                                                                                                  | 0                                                                                                                                                                                                                                                                                                  | 0                                                                                                                                                                                                                                                                                                  | 0                                                                                                                                                                                                                                                                                                  | 0                                                                                                                                                                                                                                                                                                  | 0                                                                                                                                                                                                                                                                                                  | 0                                                                                                                                                                                                                                                                                                  | 0                                                                                                                                                                                                                                                                                                  | 0                                                                                                                                                                                                                                                                                                  | GPIO                                                                                                                                                                                                                                                                                               |
|        |           | 0                                                                                                                                                                                                                                                                                                  | 0                                                                                                                                                                                                                                                                                                  | 1                                                                                                                                                                                                                                                                                                  | 0                                                                                                                                                                                                                                                                                                  | 0                                                                                                                                                                                                                                                                                                  | 1                                                                                                                                                                                                                                                                                                  | 0                                                                                                                                                                                                                                                                                                  | 0                                                                                                                                                                                                                                                                                                  | 1                                                                                                                                                                                                                                                                                                  | Primary Function                                                                                                                                                                                                                                                                                   |
|        |           |                                                                                                                                                                                                                                                                                                    |                                                                                                                                                                                                                                                                                                    |                                                                                                                                                                                                                                                                                                    | 0                                                                                                                                                                                                                                                                                                  | 1                                                                                                                                                                                                                                                                                                  | 0                                                                                                                                                                                                                                                                                                  | 0                                                                                                                                                                                                                                                                                                  | 1                                                                                                                                                                                                                                                                                                  | 0                                                                                                                                                                                                                                                                                                  | Alternate Function 1                                                                                                                                                                                                                                                                               |
|        |           |                                                                                                                                                                                                                                                                                                    |                                                                                                                                                                                                                                                                                                    |                                                                                                                                                                                                                                                                                                    | 0                                                                                                                                                                                                                                                                                                  | 1                                                                                                                                                                                                                                                                                                  | 1                                                                                                                                                                                                                                                                                                  | 0                                                                                                                                                                                                                                                                                                  | 1                                                                                                                                                                                                                                                                                                  | 1                                                                                                                                                                                                                                                                                                  | Primary Function                                                                                                                                                                                                                                                                                   |
|        |           |                                                                                                                                                                                                                                                                                                    |                                                                                                                                                                                                                                                                                                    |                                                                                                                                                                                                                                                                                                    |                                                                                                                                                                                                                                                                                                    |                                                                                                                                                                                                                                                                                                    |                                                                                                                                                                                                                                                                                                    | 1                                                                                                                                                                                                                                                                                                  | 0                                                                                                                                                                                                                                                                                                  | 0                                                                                                                                                                                                                                                                                                  | Alternate Function 2                                                                                                                                                                                                                                                                               |
|        |           |                                                                                                                                                                                                                                                                                                    |                                                                                                                                                                                                                                                                                                    |                                                                                                                                                                                                                                                                                                    |                                                                                                                                                                                                                                                                                                    |                                                                                                                                                                                                                                                                                                    |                                                                                                                                                                                                                                                                                                    | 1                                                                                                                                                                                                                                                                                                  | 0                                                                                                                                                                                                                                                                                                  | 1                                                                                                                                                                                                                                                                                                  | Reserved                                                                                                                                                                                                                                                                                           |
|        |           |                                                                                                                                                                                                                                                                                                    |                                                                                                                                                                                                                                                                                                    |                                                                                                                                                                                                                                                                                                    |                                                                                                                                                                                                                                                                                                    |                                                                                                                                                                                                                                                                                                    |                                                                                                                                                                                                                                                                                                    | 1                                                                                                                                                                                                                                                                                                  | 1                                                                                                                                                                                                                                                                                                  | 0                                                                                                                                                                                                                                                                                                  | Reserved                                                                                                                                                                                                                                                                                           |
|        |           |                                                                                                                                                                                                                                                                                                    | 1 For all SIU_PCRs that do not comply with these given explicitly with the SIU_PCR definition. 2 For future software compatibility, it is recommended treated as 3-bit fields, with the unused bits written 1 1 1                                                                                  | 1 For all SIU_PCRs that do not comply with these given explicitly with the SIU_PCR definition. 2 For future software compatibility, it is recommended treated as 3-bit fields, with the unused bits written 1 1 1                                                                                  | 1 For all SIU_PCRs that do not comply with these given explicitly with the SIU_PCR definition. 2 For future software compatibility, it is recommended treated as 3-bit fields, with the unused bits written 1 1 1                                                                                  | 1 For all SIU_PCRs that do not comply with these given explicitly with the SIU_PCR definition. 2 For future software compatibility, it is recommended treated as 3-bit fields, with the unused bits written 1 1 1                                                                                  | 1 For all SIU_PCRs that do not comply with these given explicitly with the SIU_PCR definition. 2 For future software compatibility, it is recommended treated as 3-bit fields, with the unused bits written 1 1 1                                                                                  | 1 For all SIU_PCRs that do not comply with these given explicitly with the SIU_PCR definition. 2 For future software compatibility, it is recommended treated as 3-bit fields, with the unused bits written 1 1 1                                                                                  | 1 For all SIU_PCRs that do not comply with these given explicitly with the SIU_PCR definition. 2 For future software compatibility, it is recommended treated as 3-bit fields, with the unused bits written 1 1 1                                                                                  | 1 For all SIU_PCRs that do not comply with these given explicitly with the SIU_PCR definition. 2 For future software compatibility, it is recommended treated as 3-bit fields, with the unused bits written 1 1 1                                                                                  | 1 For all SIU_PCRs that do not comply with these given explicitly with the SIU_PCR definition. 2 For future software compatibility, it is recommended treated as 3-bit fields, with the unused bits written 1 1 1                                                                                  |
| 6      | OBE       | Output buffer enable. Enables the pad as an output and drives the output buffer enable signal. 0 Output buffer for the pad is disabled. 1 Output buffer for the pad is enabled.                                                                                                                    | Output buffer enable. Enables the pad as an output and drives the output buffer enable signal. 0 Output buffer for the pad is disabled. 1 Output buffer for the pad is enabled.                                                                                                                    | Output buffer enable. Enables the pad as an output and drives the output buffer enable signal. 0 Output buffer for the pad is disabled. 1 Output buffer for the pad is enabled.                                                                                                                    | Output buffer enable. Enables the pad as an output and drives the output buffer enable signal. 0 Output buffer for the pad is disabled. 1 Output buffer for the pad is enabled.                                                                                                                    | Output buffer enable. Enables the pad as an output and drives the output buffer enable signal. 0 Output buffer for the pad is disabled. 1 Output buffer for the pad is enabled.                                                                                                                    | Output buffer enable. Enables the pad as an output and drives the output buffer enable signal. 0 Output buffer for the pad is disabled. 1 Output buffer for the pad is enabled.                                                                                                                    | Output buffer enable. Enables the pad as an output and drives the output buffer enable signal. 0 Output buffer for the pad is disabled. 1 Output buffer for the pad is enabled.                                                                                                                    | Output buffer enable. Enables the pad as an output and drives the output buffer enable signal. 0 Output buffer for the pad is disabled. 1 Output buffer for the pad is enabled.                                                                                                                    | Output buffer enable. Enables the pad as an output and drives the output buffer enable signal. 0 Output buffer for the pad is disabled. 1 Output buffer for the pad is enabled.                                                                                                                    | Output buffer enable. Enables the pad as an output and drives the output buffer enable signal. 0 Output buffer for the pad is disabled. 1 Output buffer for the pad is enabled.                                                                                                                    |
| 7      | IBE       | Input buffer enable. Enables the pad as an input and drives the input buffer enable signal. 0 Input buffer for the pad is disabled. 1 Input buffer for the pad is enabled.                                                                                                                         | Input buffer enable. Enables the pad as an input and drives the input buffer enable signal. 0 Input buffer for the pad is disabled. 1 Input buffer for the pad is enabled.                                                                                                                         | Input buffer enable. Enables the pad as an input and drives the input buffer enable signal. 0 Input buffer for the pad is disabled. 1 Input buffer for the pad is enabled.                                                                                                                         | Input buffer enable. Enables the pad as an input and drives the input buffer enable signal. 0 Input buffer for the pad is disabled. 1 Input buffer for the pad is enabled.                                                                                                                         | Input buffer enable. Enables the pad as an input and drives the input buffer enable signal. 0 Input buffer for the pad is disabled. 1 Input buffer for the pad is enabled.                                                                                                                         | Input buffer enable. Enables the pad as an input and drives the input buffer enable signal. 0 Input buffer for the pad is disabled. 1 Input buffer for the pad is enabled.                                                                                                                         | Input buffer enable. Enables the pad as an input and drives the input buffer enable signal. 0 Input buffer for the pad is disabled. 1 Input buffer for the pad is enabled.                                                                                                                         | Input buffer enable. Enables the pad as an input and drives the input buffer enable signal. 0 Input buffer for the pad is disabled. 1 Input buffer for the pad is enabled.                                                                                                                         | Input buffer enable. Enables the pad as an input and drives the input buffer enable signal. 0 Input buffer for the pad is disabled. 1 Input buffer for the pad is enabled.                                                                                                                         | Input buffer enable. Enables the pad as an input and drives the input buffer enable signal. 0 Input buffer for the pad is disabled. 1 Input buffer for the pad is enabled.                                                                                                                         |
| 8-9    | DSC [0:1] | Drive strength control. Controls the pad drive strength. Drive strength control pertains to pins with the fast I/O pad type. 00 10 pF Drive Strength 01 20 pF Drive Strength 10 30 pF Drive Strength 11 50 pF Drive Strength                                                                       | Drive strength control. Controls the pad drive strength. Drive strength control pertains to pins with the fast I/O pad type. 00 10 pF Drive Strength 01 20 pF Drive Strength 10 30 pF Drive Strength 11 50 pF Drive Strength                                                                       | Drive strength control. Controls the pad drive strength. Drive strength control pertains to pins with the fast I/O pad type. 00 10 pF Drive Strength 01 20 pF Drive Strength 10 30 pF Drive Strength 11 50 pF Drive Strength                                                                       | Drive strength control. Controls the pad drive strength. Drive strength control pertains to pins with the fast I/O pad type. 00 10 pF Drive Strength 01 20 pF Drive Strength 10 30 pF Drive Strength 11 50 pF Drive Strength                                                                       | Drive strength control. Controls the pad drive strength. Drive strength control pertains to pins with the fast I/O pad type. 00 10 pF Drive Strength 01 20 pF Drive Strength 10 30 pF Drive Strength 11 50 pF Drive Strength                                                                       | Drive strength control. Controls the pad drive strength. Drive strength control pertains to pins with the fast I/O pad type. 00 10 pF Drive Strength 01 20 pF Drive Strength 10 30 pF Drive Strength 11 50 pF Drive Strength                                                                       | Drive strength control. Controls the pad drive strength. Drive strength control pertains to pins with the fast I/O pad type. 00 10 pF Drive Strength 01 20 pF Drive Strength 10 30 pF Drive Strength 11 50 pF Drive Strength                                                                       | Drive strength control. Controls the pad drive strength. Drive strength control pertains to pins with the fast I/O pad type. 00 10 pF Drive Strength 01 20 pF Drive Strength 10 30 pF Drive Strength 11 50 pF Drive Strength                                                                       | Drive strength control. Controls the pad drive strength. Drive strength control pertains to pins with the fast I/O pad type. 00 10 pF Drive Strength 01 20 pF Drive Strength 10 30 pF Drive Strength 11 50 pF Drive Strength                                                                       | Drive strength control. Controls the pad drive strength. Drive strength control pertains to pins with the fast I/O pad type. 00 10 pF Drive Strength 01 20 pF Drive Strength 10 30 pF Drive Strength 11 50 pF Drive Strength                                                                       |
| 10     | ODE       | Open drain output enable. Controls output driver configuration for the pads. Either open drain or push/pull driver configurations can be selected. This feature applies to output pins only. 0 Open drain is disabled for the pad (push/pull driver enabled). 1 Open drain is enabled for the pad. | Open drain output enable. Controls output driver configuration for the pads. Either open drain or push/pull driver configurations can be selected. This feature applies to output pins only. 0 Open drain is disabled for the pad (push/pull driver enabled). 1 Open drain is enabled for the pad. | Open drain output enable. Controls output driver configuration for the pads. Either open drain or push/pull driver configurations can be selected. This feature applies to output pins only. 0 Open drain is disabled for the pad (push/pull driver enabled). 1 Open drain is enabled for the pad. | Open drain output enable. Controls output driver configuration for the pads. Either open drain or push/pull driver configurations can be selected. This feature applies to output pins only. 0 Open drain is disabled for the pad (push/pull driver enabled). 1 Open drain is enabled for the pad. | Open drain output enable. Controls output driver configuration for the pads. Either open drain or push/pull driver configurations can be selected. This feature applies to output pins only. 0 Open drain is disabled for the pad (push/pull driver enabled). 1 Open drain is enabled for the pad. | Open drain output enable. Controls output driver configuration for the pads. Either open drain or push/pull driver configurations can be selected. This feature applies to output pins only. 0 Open drain is disabled for the pad (push/pull driver enabled). 1 Open drain is enabled for the pad. | Open drain output enable. Controls output driver configuration for the pads. Either open drain or push/pull driver configurations can be selected. This feature applies to output pins only. 0 Open drain is disabled for the pad (push/pull driver enabled). 1 Open drain is enabled for the pad. | Open drain output enable. Controls output driver configuration for the pads. Either open drain or push/pull driver configurations can be selected. This feature applies to output pins only. 0 Open drain is disabled for the pad (push/pull driver enabled). 1 Open drain is enabled for the pad. | Open drain output enable. Controls output driver configuration for the pads. Either open drain or push/pull driver configurations can be selected. This feature applies to output pins only. 0 Open drain is disabled for the pad (push/pull driver enabled). 1 Open drain is enabled for the pad. | Open drain output enable. Controls output driver configuration for the pads. Either open drain or push/pull driver configurations can be selected. This feature applies to output pins only. 0 Open drain is disabled for the pad (push/pull driver enabled). 1 Open drain is enabled for the pad. |
| 11     | HYS       | Input hysteresis. Controls whether hysteresis is enabled for the pad. 0 Hysteresis is disabled for the pad. 1 Hysteresis is enabled for the pad.                                                                                                                                                   | Input hysteresis. Controls whether hysteresis is enabled for the pad. 0 Hysteresis is disabled for the pad. 1 Hysteresis is enabled for the pad.                                                                                                                                                   | Input hysteresis. Controls whether hysteresis is enabled for the pad. 0 Hysteresis is disabled for the pad. 1 Hysteresis is enabled for the pad.                                                                                                                                                   | Input hysteresis. Controls whether hysteresis is enabled for the pad. 0 Hysteresis is disabled for the pad. 1 Hysteresis is enabled for the pad.                                                                                                                                                   | Input hysteresis. Controls whether hysteresis is enabled for the pad. 0 Hysteresis is disabled for the pad. 1 Hysteresis is enabled for the pad.                                                                                                                                                   | Input hysteresis. Controls whether hysteresis is enabled for the pad. 0 Hysteresis is disabled for the pad. 1 Hysteresis is enabled for the pad.                                                                                                                                                   | Input hysteresis. Controls whether hysteresis is enabled for the pad. 0 Hysteresis is disabled for the pad. 1 Hysteresis is enabled for the pad.                                                                                                                                                   | Input hysteresis. Controls whether hysteresis is enabled for the pad. 0 Hysteresis is disabled for the pad. 1 Hysteresis is enabled for the pad.                                                                                                                                                   | Input hysteresis. Controls whether hysteresis is enabled for the pad. 0 Hysteresis is disabled for the pad. 1 Hysteresis is enabled for the pad.                                                                                                                                                   | Input hysteresis. Controls whether hysteresis is enabled for the pad. 0 Hysteresis is disabled for the pad. 1 Hysteresis is enabled for the pad.                                                                                                                                                   |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 6-15. SIU\_PCR Field Descriptions (continued)

| Bits   | Name      | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
|--------|-----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 12-13  | SRC [0:1] | Slew rate control. Controls slew rate for the pad. Slew rate control pertains to pins with slow or medium I/O pad types, and the output signals are driven according to the value of this field. Actual slew rate is dependent on the pad type and load. See the electrical specification for this information 00 Minimum slew rate 01 Medium slew rate 10 Reserved 11 Maximum slew rate                                                                                                                           |
| 14     | WPE       | Weak pull up/down enable. Controls whether the weak pull up/down devices are enabled/disabled for the pad. Pull up/down devices are enabled by default. 0 Weak pull device is disabled for the pad. 1 Weak pull device is enabled for the pad.                                                                                                                                                                                                                                                                     |
| 15     | WPS       | Weak pull up/down select. Controls whether weak pull up or weak pull down devices are used for the pad when weak pull up/down devices are enabled. The WKPCFG pin determines whether pull up or pull down devices are enabled at reset. The WPS bit determines whether weak pull up or pull down devices are used after reset, or for pads in which the WKPCFG pin does not determine the reset weak pull up/down state. 0 The pull down value is enabled for the pad. 1 The pull up value is enabled for the pad. |

## 6.3.1.12.1 Pad Configuration Registers 0 - 3 (SIU\_PCR0 - SIU\_PCR3)

The SIU\_PCR0 - SIU\_PCR3 registers control the pin function, direction, and static electrical attributes of the CS[0:3]\_ADDR[8:11]\_GPIO[0:3] pins.

## SIU\_BASE+0x40 - SIU\_BASE+0x46 (4)

<!-- image -->

|        |   0 |   1 |   2 |   3 | 4    | 5   | 6     | 7     | 8   | 9   | 10    | 11   |   12 |   13 | 14    | 15    |
|--------|-----|-----|-----|-----|------|-----|-------|-------|-----|-----|-------|------|------|------|-------|-------|
| R      |   0 |   0 |   0 |   0 | PA 1 |     | OBE 2 | IBE 3 | DSC |     | ODE 4 | HYS  |    0 |    0 | WPE 5 | WPS 5 |
| RESET: |   0 |   0 |   0 |   0 | 0    | 0   | 0     | 0     | 1   | 1   | 0     | 0    |    0 |    0 | 1     | 1     |

- 1 The PA fields in PCR0 - 3 and PCR4 - 7 must not be configured simultaneously to select ADDR[8:11] as input. Only one pin is to be configured to provide the address input.
- 2 When configured as CS[0:3] or ADDR[8:11], the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 3 When configured as CS[0:3], ADDR[8:11] (only MPC5554), or GPI, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.
- 4 When configured as CS[0:3] or ADDR[8:11] (only MPC5554), the ODE bit should be set to zero.
- 5 See the EBI section for weak pull up settings when configured as CS[0:3] or ADDR[8:11] (only MPC5554).

Figure 6-13. CS[0:3]\_ADDR[8:11]\_GPIO[0:3] Pad Configuration Registers (SIU\_PCR0 - SIU\_PCR3)

See Table 6-15 for bit field definitions.

## 6.3.1.12.2 MPC5553: Pad Configuration Registers 4 - 7 (SIU\_PCR4 - SIU\_PCR7)

The SIU\_PCR4 - SIU\_PCR7 registers control the pin function, direction, and static electrical attributes of the ADDR[8:11]\_CAL\_ADDR[27:30]\_GPIO[4:7] pins.

## SIU\_BASE+0x48 - SIU\_BASE+0x4E (4)

<!-- image -->

- 1 The PA fields in PCR0 - 3 and PCR4 - 7 must not be configured simultaneously to select ADDR[8:11] as an input. Only one pin is to be configured to provide the address input.
- 2 When configured as ADDR[8:11] or CAL\_ADDR[27:30], the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 3 When configured as ADDR[8:11], CAL\_ADDR[27:30], or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.
- 4 When configured as ADDR[8:11] or CAL\_ADDR[27:30], the ODE bit should be set to zero.
- 5 If external master operation is enabled, the HYS bit should be set to zero.
- 6 See the EBI section for weak pull up settings when configured as ADDR[8:11] or CAL\_ADDR[27:30].

## Figure 6-14. MPC5553: ADDR[8:11]\_CAL\_ADDR[27:30]\_GPIO[4:7]

Pad Configuration Registers (SIU\_PCR4 - SIU\_PCR7)

See Table 6-15 for bit field definitions. The PA field for PCR4 - PCR7 is given in Table 6-16.

Table 6-16. PCR4 - PCR7 PA Field Definition

| PA Field   | Pin Function      |
|------------|-------------------|
| 0b000      | GPIO[4:7]         |
| 0b001      | ADDR[8:11]        |
| 0b010      | Reserved          |
| 0b011      | ADDR[8:11]        |
| 0b100      | CAL_ADDR[27:30] 1 |

1 For calibration only.

## 6.3.1.12.3 MPC5554: Pad Configuration Registers 4 - 27 (SIU\_PCR4 - SIU\_PCR27)

## NOTE

The  definition  for  PCR4-PCR7  in  MPC5553  devices  differs  from  the definition given in this section. For MPC5553 devices' PCR4-PCR7, see Section 6.3.1.12.2, 'MPC5553: Pad Configuration Registers 4 -7 (SIU\_PCR4 - SIU\_PCR7).'

The SIU\_PCR4 - SIU\_PCR27 registers control the pin function, direction, and static electrical attributes of the ADDR[8:31]\_GPIO[4:27] pins (ADDR[12:31]\_GPIO[8:27] for MPC5553).

## SIU\_BASE+0x48 - SIU\_BASE+0x76 (24)

<!-- image -->

- 1 The PA fields in PCR0 - 3 and PCR4 - 7 must not be configured simultaneously to select ADDR[8:11]. Only one pin is configured to provide the address input.
- 2 When configured as ADDR[8:31] (ADDR[12;31] for MPC5553), the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 3 When configured as ADDR[8:31] (ADDR[12;31] for MPC5553) or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.
- 4 When configured as ADDR[8:31] (ADDR[12;31] for MPC5553), the ODE bit should be set to zero.
- 5 If external master operation is enabled, the HYS bit should be set to zero.
- 6 See the EBI section for weak pull up settings when configured as ADDR[8:31].

Figure 6-15. MPC5554: ADDR[8:31]\_GPIO[4:27] Pad Configuration Registers (SIU\_PCR4 - SIU\_PCR27)

See Table 6-15 for bit field definitions.

## 6.3.1.12.4 Pad Configuration Registers 28 - 59 (SIU\_PCR28 - SIU\_PCR59)

## NOTE

The definitions for PCR44-PCR59 in MPC5553 devices differs from the definition given in this section. For MPC5553 devices' PCR44-PCR59, see Section 6.3.1.12.5, 'MPC5553: Pad Configuration Register 44 (SIU\_PCR44)'  -  Section 6.3.1.12.20, 'MPC5553:  Pad  Configuration Register 59 (SIU\_PCR59)

The SIU\_PCR28 - SIU\_PCR59 registers control the pin function, direction, and static electrical attributes of the DATA[0:31]\_GPIO[28:59] pins.

## SIU\_BASE+0x78 - SIU\_BASE+0xB6 (32)

<!-- image -->

- 1 When configured as DATA[0:31], the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 2 When configured as DATA[0:31] or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.
- 3 When configured as DATA[0:31], the ODE bit should be set to zero.
- 4 If external master operation is enabled, the HYS bit should be set to zero.
- 5 See the EBI section for weak pull up settings when configured as DATA[0:31].

Figure 6-16. DATA[0:31]\_GPIO[28:59] Pad Configuration Registers (SIU\_PCR28 - SIU\_PCR59)

See Table 6-15 for bit field definitions.

## 6.3.1.12.5 MPC5553: Pad Configuration Register 44 (SIU\_PCR44)

The  SIU\_PCR44  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the DATA[16]\_TX\_CLK\_CAL\_DATA[0]\_GPIO[44] pin.

## SIU\_BASE+0x98

<!-- image -->

- 1 CAL\_DATA[0] is for calibration only.
- 2 When configured as DATA[16], TX\_CLK, or CAL\_DATA[0], the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 3 When configured as DATA[16], TX\_CLK, CAL\_DATA[0], or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.
- 4 When configured as DATA[16] or CAL\_DATA[0], the ODE bit should be set to zero.
- 5 If external master operation is enabled, the HYS bit should be set to zero.
- 6 See the EBI section for weak pull up settings when configured as DATA[16] or CAL\_DATA[0].

## Figure 6-17. MPC5553: DATA[16]\_TX\_CLK\_CAL\_DATA[0]\_GPIO[44] Pad Configuration Register (SIU\_PCR44)

See Table 6-15 for bit field definitions.

## 6.3.1.12.6 MPC5553: Pad Configuration Register 45 (SIU\_PCR45)

The  SIU\_PCR45  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the DATA[17]\_CRS\_CAL\_DATA[1]\_GPIO[45] pin.

## SIU\_BASE+0x9A

<!-- image -->

- 1 CAL\_DATA[1] is for calibration only.
- 2 When configured as DATA[17], CRS, or CAL\_DATA[1], the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 3 When configured as DATA[17], CRS, CAL\_DATA[1], or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.
- 4 When configured as DATA[17] or CAL\_DATA[1], the ODE bit should be set to zero.
- 5 If external master operation is enabled, the HYS bit should be set to zero.
- 6 See the EBI section for weak pull up settings when configured as DATA[17] or CAL\_DATA[1].

## Figure 6-18. MPC5553: DATA[17]\_CRS\_CAL\_DATA[1]\_GPIO[45] Pad Configuration Register (SIU\_PCR45)

See Table 6-15 for bit field definitions.

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## 6.3.1.12.7 MPC5553: Pad Configuration Register 46 (SIU\_PCR46)

The  SIU\_PCR46  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the DATA[18]\_TX\_ERR\_CAL\_DATA[2]\_GPIO[46] pin.

## SIU\_BASE+0x9C

<!-- image -->

- 1 CAL\_DATA[2] is for calibration only.
- 2 When configured as DATA[18], TX\_ERR, or CAL\_DATA[2], the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 3 When configured as DATA[18], TX\_ERR, CAL\_DATA[2], or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.
- 4 When configured as DATA[18] or CAL\_DATA[2], the ODE bit should be set to zero.
- 5 If external master operation is enabled, the HYS bit should be set to zero.
- 6 See the EBI section for weak pull up settings when configured as DATA[18] or CAL\_DATA[2].

## Figure 6-19. MPC5553: DATA[18]\_TX\_ERR\_CAL\_DATA[2]\_GPIO[46] Pad Configuration Register (SIU\_PCR46)

See Table 6-15 for bit field definitions.

## 6.3.1.12.8 MPC5553: Pad Configuration Register 47 (SIU\_PCR47)

The  SIU\_PCR47  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the DATA[19]\_RX\_CLK\_CAL\_DATA[3]\_GPIO[47] pin.

## SIU\_BASE+0x9E

<!-- image -->

- 1 CAL\_DATA[3] is for calibration only.
- 2 When configured as DATA[19], RX\_CLK, or CAL\_DATA[3], the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 3 When configured as DATA[19], RX\_CLK, CAL\_DATA[3], or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.
- 4 When configured as DATA[19] or CAL\_DATA[3], the ODE bit should be set to zero.
- 5 If external master operation is enabled, the HYS bit should be set to zero.
- 6 See the EBI section for weak pull up settings when configured as DATA[19] or CAL\_DATA[3].

Figure 6-20. MPC5553: DATA[19]\_RX\_CLK\_CAL\_DATA[3]\_GPIO[47] Pad Configuration Register (SIU\_PCR47)

See Table 6-15 for bit field definitions.

## 6.3.1.12.9 MPC5553: Pad Configuration Register 48 (SIU\_PCR48)

The  SIU\_PCR48  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the DATA[20]\_TXD[0]\_CAL\_DATA[4]\_GPIO[48] pin.

## SIU\_BASE+0xA0

<!-- image -->

- 1 CAL\_DATA[4] is for calibration only.
- 2 When configured as DATA[20], TXD[0], or CAL\_DATA[4], the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 3 When configured as DATA[20], TXD[0], CAL\_DATA[4], or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.
- 4 When configured as DATA[20] or CAL\_DATA[4], the ODE bit should be set to zero.
- 5 If external master operation is enabled, the HYS bit should be set to zero.
- 6 See the EBI section for weak pull up settings when configured as DATA[20] or CAL\_DATA[4].

## Figure 6-21. MPC5553: DATA[20]\_TXD[0]\_CAL\_DATA[4]\_GPIO[48] Pad Configuration Register (SIU\_PCR48)

See Table 6-15 for bit field definitions.

## 6.3.1.12.10 MPC5553: Pad Configuration Register 49 (SIU\_PCR49)

The  SIU\_PCR49  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the DATA[21]\_RX\_ERR\_CAL\_DATA[5]\_GPIO[49] pin.

## SIU\_BASE+0xA2

<!-- image -->

- 1 CAL\_DATA[5] is for calibration only.
- 2 When configured as DATA[21], RX\_ERR, or CAL\_DATA[5], the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 3 When configured as DATA[21], RX\_ERR, CAL\_DATA[5], or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.
- 4 When configured as DATA[21] or CAL\_DATA[5], the ODE bit should be set to zero.
- 5 If external master operation is enabled, the HYS bit should be set to zero.
- 6 See the EBI section for weak pull up settings when configured as DATA[21] or CAL\_DATA[5].

## Figure 6-22. MPC5553: DATA[21]\_RX\_ERR\_CAL\_DATA[5]\_GPIO[49]

## Pad Configuration Registers (SIU\_PCR49)

See Table 6-15 for bit field definitions.

## 6.3.1.12.11 MPC5553: Pad Configuration Register 50 (SIU\_PCR50)

The  SIU\_PCR50  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the DATA[22]\_RXD[0]\_CAL\_DATA[6]\_GPIO[50] pin.

## SIU\_BASE+0xA4

<!-- image -->

- 1 CAL\_DATA[6] is for calibration only.
- 2 When configured as DATA[22], RXD[0], or CAL\_DATA[6], the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 3 When configured as DATA[22], RXD[0], CAL\_DATA[6], or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.
- 4 When configured as DATA[22] or CAL\_DATA[6], the ODE bit should be set to zero.
- 5 If external master operation is enabled, the HYS bit should be set to zero.
- 6 See the EBI section for weak pull up settings when configured as DATA[22] or CAL\_DATA[6].

## Figure 6-23. MPC5553: DATA[22]\_RXD[0]\_CAL\_DATA[6]\_GPIO[50] Pad Configuration Register (SIU\_PCR50)

See Table 6-15 for bit field definitions.

## 6.3.1.12.12 MPC5553: Pad Configuration Register 51 (SIU\_PCR51)

The  SIU\_PCR51  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the DATA[23]\_TXD[3]\_CAL\_DATA[7]\_GPIO[51] pin.

## SIU\_BASE+0xA6

<!-- image -->

- 1 CAL\_DATA[7] is for calibration only.
- 2 When configured as DATA[23], TXD[3], or CAL\_DATA[7], the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 3 When configured as DATA[23], TXD[3], CAL\_DATA[7], or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.
- 4 When configured as DATA[23] or CAL\_DATA[7], the ODE bit should be set to zero.
- 5 If external master operation is enabled, the HYS bit should be set to zero.
- 6 See the EBI section for weak pull up settings when configured as DATA[23] or CAL\_DATA[7].

## Figure 6-24. MPC5553: DATA[23]\_TXD[3]\_CAL\_DATA[7]\_GPIO[51] Pad Configuration Register (SIU\_PCR51)

See Table 6-15 for bit field definitions.

## 6.3.1.12.13 MPC5553: Pad Configuration Register 52 (SIU\_PCR52)

The  SIU\_PCR52  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the DATA[24]\_COL\_CAL\_DATA[8]\_GPIO[52] pin.

## SIU\_BASE+0xA8

<!-- image -->

- 1 CAL\_DATA[8] is for calibration only.
- 2 When configured as DATA[24], COL, or CAL\_DATA[8], the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 3 When configured as DATA[24], COL, CAL\_DATA[8], or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.
- 4 When configured as DATA[24] or CAL\_DATA[8], the ODE bit should be set to zero.
- 5 If external master operation is enabled, the HYS bit should be set to zero.
- 6 See the EBI section for weak pull up settings when configured as DATA[24] or CAL\_DATA[8].

## Figure 6-25. MPC5553: DATA[24]\_COL\_CAL\_DATA[8]\_GPIO[52] Pad Configuration Register (SIU\_PCR52)

See Table 6-15 for bit field definitions.

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## 6.3.1.12.14 MPC5553: Pad Configuration Register 53 (SIU\_PCR53)

The  SIU\_PCR53  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the DATA[25]\_RX\_DV\_CAL\_DATA[9]\_GPIO[53] pin.

## SIU\_BASE+0xAA

<!-- image -->

- 1 CAL\_DATA[9] is for calibration only.
- 2 When configured as DATA[25], RX\_DV, or CAL\_DATA[9], the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 3 When configured as DATA[25], RX\_DV, CAL\_DATA[9], or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.
- 4 When configured as DATA[25] or CAL\_DATA[9], the ODE bit should be set to zero.
- 5 If external master operation is enabled, the HYS bit should be set to zero.
- 6 See the EBI section for weak pull up settings when configured as DATA[25] or CAL\_DATA[9].

## Figure 6-26. MPC5553: DATA[25]\_RX\_DV\_CAL\_DATA[9]\_GPIO[53] Pad Configuration Register (SIU\_PCR53)

See Table 6-15 for bit field definitions.

## 6.3.1.12.15 MPC5553: Pad Configuration Register 54 (SIU\_PCR54)

The  SIU\_PCR54  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the DATA[26]\_TX\_EN\_CAL\_DATA[10]\_GPIO[54] pin.

## SIU\_BASE+0xAC

<!-- image -->

- 1 CAL\_DATA[10] is for calibration only.
- 2 When configured as DATA[26], TX\_EN, or CAL\_DATA[10], the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 3 When configured as DATA[26], TX\_EN, CAL\_DATA[10], or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.
- 4 When configured as DATA[26] or CAL\_DATA[10], the ODE bit should be set to zero.
- 5 If external master operation is enabled, the HYS bit should be set to zero.
- 6 See the EBI section for weak pull up settings when configured as DATA[26] or CAL\_DATA[10].

Figure 6-27. MPC5553: DATA[26]\_TX\_EN\_CAL\_DATA[10]\_GPIO[54] Pad Configuration Register (SIU\_PCR54)

See Table 6-15 for bit field definitions.

## 6.3.1.12.16 MPC5553: Pad Configuration Register 55 (SIU\_PCR55)

The  SIU\_PCR55  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the DATA[27]\_TXD[2]\_CAL\_DATA[11]\_GPIO[55] pin.

## SIU\_BASE+0xAE

<!-- image -->

- 1 CAL\_DATA[11] is for calibration only.
- 2 When configured as DATA[27], TXD[2], or CAL\_DATA[11], the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 3 When configured as DATA[27], TXD[2], CAL\_DATA[11], or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.
- 4 When configured as DATA[27] or CAL\_DATA[11], the ODE bit should be set to zero.
- 5 If external master operation is enabled, the HYS bit should be set to zero.
- 6 See the EBI section for weak pull up settings when configured as DATA[27] or CAL\_DATA[11].

## Figure 6-28. MPC5553: DATA[27]\_TXD[2]\_CAL\_DATA[11]\_GPIO[55] Pad Configuration Register (SIU\_PCR55)

See Table 6-15 for bit field definitions.

## 6.3.1.12.17 MPC5553: Pad Configuration Register 56 (SIU\_PCR56)

The  SIU\_PCR56  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the DATA[28]\_TXD[1]\_CAL\_DATA[12]\_GPIO[56] pin.

## SIU\_BASE+0xB0

<!-- image -->

- 1 CAL\_DATA[12] is for calibration only.
- 2 When configured as DATA[28], TXD[1], or CAL\_DATA[12], the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 3 When configured as DATA[28], TXD[1], CAL\_DATA[12], or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.
- 4 When configured as DATA[28] or CAL\_DATA[12], the ODE bit should be set to zero.
- 5 If external master operation is enabled, the HYS bit should be set to zero.
- 6 See the EBI section for weak pull up settings when configured as DATA[28] or CAL\_DATA[12].

## Figure 6-29. MPC5553: DATA[28]\_TXD[1]\_CAL\_DATA[12]\_GPIO[56]

## Pad Configuration Register (SIU\_PCR56)

See Table 6-15 for bit field definitions.

## 6.3.1.12.18 MPC5553: Pad Configuration Register 57 (SIU\_PCR57)

The  SIU\_PCR57  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the DATA[29]\_RXD[1]\_CAL\_DATA[13]\_GPIO[57] pin.

## SIU\_BASE+0xB2

<!-- image -->

- 1 CAL\_DATA[13] is for calibration only.
- 2 When configured as DATA[29], RXD[1], or CAL\_DATA[13], the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 3 When configured as DATA[29], RXD[1], CAL\_DATA[13], or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.
- 4 When configured as DATA[29] or CAL\_DATA[13], the ODE bit should be set to zero.
- 5 If external master operation is enabled, the HYS bit should be set to zero.
- 6 See the EBI section for weak pull up settings when configured as DATA[29] or CAL\_DATA[13].

## Figure 6-30. MPC5553: DATA[29]\_RXD[1]\_CAL\_DATA[13]\_GPIO[57] Pad Configuration Register (SIU\_PCR57)

See Table 6-15 for bit field definitions.

## 6.3.1.12.19 MPC5553: Pad Configuration Register 58 (SIU\_PCR58)

The  SIU\_PCR58  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the DATA[30]\_RXD[2]\_CAL\_DATA[14]\_GPIO[58] pin.

## SIU\_BASE+0xB4

<!-- image -->

- 1 CAL\_DATA[14] is for calibration only.
- 2 When configured as DATA[30], RXD[2], or CAL\_DATA[14], the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 3 When configured as DATA[30], RXD[2], CAL\_DATA[14], or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.
- 4 When configured as DATA[30] or CAL\_DATA[14], the ODE bit should be set to zero.
- 5 If external master operation is enabled, the HYS bit should be set to zero.
- 6 See the EBI section for weak pull up settings when configured as DATA[30] or CAL\_DATA[14].

## Figure 6-31. MPC5553: DATA[30]\_RXD[2]\_CAL\_DATA[14]\_GPIO[58] Pad Configuration Register (SIU\_PCR58)

See Table 6-15 for bit field definitions.

## 6.3.1.12.20 MPC5553: Pad Configuration Register 59 (SIU\_PCR59)

The  SIU\_PCR59  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the DATA[31]\_RXD[3]\_CAL\_DATA[15]\_GPIO[59] pin.

## SIU\_BASE+0xB6

<!-- image -->

- 1 CAL\_DATA[15] is for calibration only.
- 2 When configured as DATA[31], RXD[3], or CAL\_DATA[15], the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 3 When configured as DATA[31], RXD[3], CAL\_DATA[15], or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.
- 4 When configured as DATA[31] or CAL\_DATA[15], the ODE bit should be set to zero.
- 5 If external master operation is enabled, the HYS bit should be set to zero.
- 6 See the EBI section for weak pull up settings when configured as DATA[31] or CAL\_DATA[15].

## Figure 6-32. MPC5553: DATA[31]\_RXD[3]\_CAL\_DATA[15]\_GPIO[59] Pad Configuration Register (SIU\_PCR59)

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

See Table 6-15 for bit field definitions.

## 6.3.1.12.21 MPC5554: Pad Configuration Registers 60 - 61 (SIU\_PCR60 - SIU\_PCR61)

## NOTE

The MPC5553 does not implement PCRs 60-61. Treat these registers as reserved space.

The SIU\_PCR60 - SIU\_PCR61 registers control the pin function, direction, and static electrical attributes of the TSIZ[0:1]\_GPIO[60:61] pins.

## SIU\_BASE+0xB8 - SIU\_BASE+0xBA (2)

<!-- image -->

- 1 When configured as TSIZ[0:1], the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 2 When configured as TSIZ[0:1] or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.
- 3 When configured as TSIZ[0:1], the ODE bit should be set to zero.
- 4 If external master operation is enabled, the HYS bit should be set to zero.
- 5 See the EBI section for weak pull up settings when configured as TSIZ[0:1].

Figure 6-33. MPC5554: TSIZ[0:1]\_GPIO[60:61] Pad Configuration Registers (SIU\_PCR60 - SIU\_PCR61)

See Table 6-15 for bit field definitions.

## 6.3.1.12.22 Pad Configuration Register 62 (SIU\_PCR62)

The  SIU\_PCR62  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the RD\_WR\_GPIO[62] pin.

## SIU\_BASE+0xBC

<!-- image -->

- 1 When configured as RD\_WR, the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 2 When configured as RD\_WR or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.
- 3 When configured as RD\_WR, the ODE bit should be set to zero.
- 4 If external master operation is enabled, the HYS bit should be set to zero.
- 5 See the EBI section for weak pull up settings when configured as RD\_WR.

## Figure 6-34. RD\_WR\_GPIO[62] Pad Configuration Register (SIU\_PCR62)

See Table 6-15 for bit field definitions.

## 6.3.1.12.23 Pad Configuration Register 63 (SIU\_PCR63)

The  SIU  PCR63  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the BDIP\_GPIO[63] pin.

## SIU\_BASE+0xBE

<!-- image -->

- 1 When configured as BDIP , the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 2 When configured as BDIP or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.
- 3 When configured as BDIP , the ODE bit should be set to zero.
- 4 See the EBI section for weak pull up settings when configured as BDIP .

Figure 6-35. BDIP\_GPIO[63] Pad Configuration Register (SIU\_PCR63)

See Table 6-15 for bit field definitions.

## 6.3.1.12.24 MPC5553: Pad Configuration Registers 64 - 65 (SIU\_PCR64 - SIU\_PCR65)

The SIU\_PCR 64 - SIU\_PCR 65 registers control the pin function, direction, and static electrical attributes of  the  WE[0:1]\_BE[0:1]\_GPIO[64:65] pins. Note that the PA bit in the PCR 64 -  65  registers  selects between the write enable/byte enable and GPIO functions. The WEBS bit in the ebi base registers selects between the write enable and byte enable function.

## SIU\_BASE+0xC0 - SIU\_BASE+0xC2 (2)

<!-- image -->

- 1 When configured as WE[0:1] or BE[0:1], the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 2 When configured as WE[0:1] or BE[0:1] or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.
- 3 When configured as WE[0:1] or BE[0:1], the ODE bit should be set to zero.
- 4 See the EBI section for weak pull up settings when configured as WE[0:1] or BE[0:1].

Figure 6-36. MPC5553: WE[0:1]\_BE[0:1]\_GPIO[64:65]

Pad Configuration Registers (SIU\_PCR64 - SIU\_PCR65)

See Table 6-15 for bit field definitions.

## 6.3.1.12.25 MPC5553: Pad Configuration Registers 66 - 67 (SIU\_PCR66 - SIU\_PCR67)

The SIU\_PCR 66 - SIU\_PCR 67 registers control the pin function, direction, and static electrical attributes of the WE[2:3]\_BE[2:3]\_CAL\_WE[0:1]\_CAL\_BE[0:1]\_GPIO[66:67] pins. Note that the PA bit in the

PCR 66 - 67 registers selects between the write enable/byte enable and GPIO functions. The WEBS bit in the EBI base registers selects between the write enable and byte enable function.

SIU\_BASE+0xC4 - SIU\_BASE+0xC6 (2)

<!-- image -->

|        |   0 |   1 |   2 | 3   | 4   | 5   | 6     | 7     | 8   | 9   | 10    | 11   |   12 |   13 | 14    | 15    |
|--------|-----|-----|-----|-----|-----|-----|-------|-------|-----|-----|-------|------|------|------|-------|-------|
| R      |   0 |   0 |   0 | PA  |     |     | OBE 1 | IBE 2 | DSC |     | ODE 3 | HYS  |    0 |    0 | WPE 4 | WPS 4 |
| RESET: |   0 |   0 |   0 | 0   | 0   | 0   | 0     | 0     | 1   | 1   | 0     | 0    |    0 |    0 | 1     | 1     |

- 1 When configured as WE[2:3], BE[2:3], CAL\_WE[0:1], or CAL\_BE[0:1], the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 2 When configured as WE[2:3], BE[2:3], CAL\_WE[0:1], CAL\_BE[0:1], or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.
- 3 When configured as WE[2:3], BE[2:3], CAL\_WE[0:1], or CAL\_BE[0:1], the ODE bit should be set to zero.
- 4 See the EBI section for weak pull up settings when configured as WE[2:3], BE[2:3], CAL\_WE[0:1], or CAL\_BE[0:1].

Figure 6-37. MPC5553: WE[2:3]\_BE[2:3]\_CAL\_WE[0:1]\_CAL\_BE[0:1]\_GPIO[66:67] Pad Configuration Registers (SIU\_PCR66 - SIU\_PCR67)

See Table 6-15 for bit field definitions. The PA field for the MPC5553's PCR66 - PCR67 is given in Table 6-17.

Table 6-17. MPC5553: PCR66 - PCR77 PA Field Definition

| PA Field   | Pin Function              |
|------------|---------------------------|
| 0b000      | GPIO[66:67]               |
| 0b001      | WE[2:3]_BE[2:3]           |
| 0b010      | Reserved                  |
| 0b011      | WE[2:3]_BE[2:3]           |
| 0b100      | CAL_WE[0:1]_CAL_BE[0:1] 1 |

1 For calibration only.

## 6.3.1.12.26 MPC5554: Pad Configuration Registers 64 - 67 (SIU\_PCR64 - SIU\_PCR67)

The SIU\_PCR 64 - SIU\_PCR 67 registers control the pin function, direction, and static electrical attributes of the WE[0:3]\_BE[0:3]\_GPIO[64:67] pins. Note that the PA bit in the PDMCR 64 -67 registers selects between the write enable/byte enable and GPIO functions. The WEBS bit in the EBI base registers selects between the write enable and byte enable function.

## SIU\_BASE+0xC0 - SIU\_BASE+0xC6 (4)

<!-- image -->

- 1 When configured as WE[0:3] or BE[0:3], the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 2 When configured as WE[0:3] or BE[0:3] or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.
- 3 When configured as WE[0:3] or BE[0:3], the ODE bit should be set to zero.
- 4 See the EBI section for weak pull up settings when configured as WE[0:3] or BE[0:3].

Figure 6-38. MPC5554: WE[0:3]\_BE[0:3]\_GPIO[64:67] Pad Configuration Registers (SIU\_PCR64 - SIU\_PCR67)

See Table 6-15 for bit field definitions.

## 6.3.1.12.27 Pad Configuration Register 68 (SIU\_PCR68)

The  SIU\_PCR68  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the OE\_GPIO[68] pin. The OE function is not available in the 208 MAP BGA package. Only the GPIO function is available on this pin in the 208 package.

## SIU\_BASE+0xC8

<!-- image -->

- 1 When configured as OE, the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 2 When configured as OE or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.
- 3 When configured as OE, the ODE bit should be set to zero.
- 4 If external master operation is enabled, the HYS bit should be set to one.
- 5 See the EBI section for weak pull up settings when configured as OE.

## Figure 6-39. OE\_GPIO[68] Pad Configuration Register (SIU\_PCR68)

See Table 6-15 for bit field definitions.

## 6.3.1.12.28 Pad Configuration Register 69 (SIU\_PCR69)

The  SIU\_PCR69  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the TS\_GPIO[69] pin.

## SIU\_BASE+0xCA

<!-- image -->

- 1 When configured as TS, the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 2 When configured as TS or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.
- 3 When configured as TS, the ODE bit should be set to zero.
- 4 If external master operation is enabled, the HYS bit should be set to zero.
- 5 See the EBI section for weak pull up settings when configured as TS.

## Figure 6-40. TS\_GPIO[69] Pad Configuration Register (SIU\_PCR69)

See Table 6-15 for bit field definitions.

## 6.3.1.12.29 Pad Configuration Register 70 (SIU\_PCR70)

The  SIU\_PCR70  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the TA\_GPIO[70] pin.

## SIU\_BASE+0xCC

<!-- image -->

- 1 When configured as TA, the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 2 When configured as TA, or GPIO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.
- 3 When configured as TA and external master operation is enabled, the ODE bit should be set to zero.
- 4 If external master operation is enabled, the HYS bit should be set to zero.
- 5 See the EBI section for weak pull up settings when configured as TA.

## Figure 6-41. TA\_GPIO[70] Pad Configuration Register (SIU\_PCR70)

See Table 6-15 for bit field definitions.

## 6.3.1.12.30 MPC5553: Pad Configuration Register 71 (SIU\_PCR71)

The  SIU\_PCR71  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the TEA\_CAL\_CS[0]\_GPIO[71] pin.

## SIU\_BASE+0xCE

<!-- image -->

- 1 When configured as TEA or CAL\_CS[0], the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 2 When configured as TEA, CAL\_CS[0], or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.
- 3 When configured as TEA and external master operation is enabled, the ODE bit should be set to zero.
- 4 If external master operation is enabled, the HYS bit should be set to zero.
- 5 See the EBI section for weak pull up settings when configured as TEA or CAL\_CS[0].

## Figure 6-42. MPC5553: TEA\_CAL\_CS[0]\_GPIO[71] Pad Configuration Register (SIU\_PCR71)

See Table 6-15 for bit field definitions. The PA field for the MPC5553's PCR71 is given in Table 6-18.

## Table 6-18. PCR71 PA Field Definition

| PA Field   | Pin Function   |
|------------|----------------|
| 0b000      | GPIO[71]       |
| 0b001      | TEA            |
| 0b010      | Reserved       |
| 0b011      | TEA            |
| 0b100      | CAL_CS[0] 1    |

- 1 For calibration only.

## 6.3.1.12.31 MPC5554: Pad Configuration Register 71 (SIU\_PCR71)

The  SIU\_PCR71  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the TEA\_GPIO[71] pin.

## SIU\_BASE+0xCE

<!-- image -->

- 1 When configured as TEA, the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 2 When configured as TEA or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.
- 3 When configured as TEA and external master operation is enabled, the ODE bit should be set to zero.
- 4 If external master operation is enabled, the HYS bit should be set to zero.
- 5 See the EBI section for weak pull up settings when configured as TEA.

## Figure 6-43. MPC5554: TEA\_GPIO[71] Pad Configuration Register (SIU\_PCR71)

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

See Table 6-15 for bit field definitions.

## 6.3.1.12.32 MPC5553: Pad Configuration Register 72 (SIU\_PCR72)

The  SIU\_PCR72  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the BR(CAL\_ADDR[10])\_MDC\_CAL\_CS[2]\_GPIO[72]  pin.  The  BR  function  is  not  available  on  the MPC5554. Instead, its PA encoding is used for CAL\_ADDR[10]. This register allows selection of the CAL\_ADDR[10], MDC, CAL\_CS[2], and GPIO functions.

## SIU\_BASE+0xD0

<!-- image -->

- 1 The BR function is not available on the MPC5554. Do not select 0b001 or 0b011 for the PA field except for CAL\_ADDR[10].
- 2 When configured as CAL\_ADDR[10], MDC, or CAL\_CS[2], the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 3 When configured as CAL\_ADDR[10], MDC, CAL\_CS[2], or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.
- 4 When configured as CAL\_ADDR[10] or CAL\_CS[2], the ODE bit should be set to zero.
- 5 If external master operation is enabled, the HYS bit should be set to zero.
- 6 See the EBI section for weak pull up settings when configured as CAL\_ADDR[10] or CAL\_CS[2].

## Figure 6-44. MPC5553: BR(CAL\_ADDR[10])\_MDC\_CAL\_CS[2]\_GPIO[72] Pad Configuration Register (SIU\_PCR72)

See Table 6-15 for bit field definitions. The PA field for MPC5553's PCR72 is given in Table 6-19.

## Table 6-19. PCR72 PA Field Definition

| PA Field   | Pin Function   |
|------------|----------------|
| 0b000      | GPIO[72]       |
| 0b001      | CAL_ADDR[10] 1 |
| 0b010      | MDC            |
| 0b011      | CAL_ADDR[10] 1 |
| 0b100      | CAL_CS[2] 1    |

1

For calibration only.

## 6.3.1.12.33 MPC5554: Pad Configuration Register 72 (SIU\_PCR72)

The  SIU\_PCR72  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the BR\_GPIO[72] pin.

## SIU\_BASE+0xD0

<!-- image -->

- 1 When configured as BR, the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 2 When configured as BR or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.
- 3 When configured as BR, and external master operation is enabled with external arbitration, the ODE bit should be set to zero.
- 4 If external master operation is enabled, the HYS bit should be set to zero.
- 5 See the EBI section for weak pull up settings when configured as BR

Figure 6-45. MPC5554: BR\_GPIO[72] Pad Configuration Register (SIU\_PCR72)

See Table 6-15 for bit field definitions.

## 6.3.1.12.34 MPC5553: Pad Configuration Register 73 (SIU\_PCR73)

The  SIU\_PCR73  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the BG(CAL\_ADDR[11])\_MDIO\_CAL\_CS[3]\_GPIO[73]  pin.  The  BG  function  is  not  available  on  the MPC5554. Instead, its PA encoding is used for CAL\_ADDR[11]. This register allows selection of the CAL\_ADDR[11], MDIO, CAL\_CS[3], and GPIO functions.

## SIU\_BASE+0xD2

<!-- image -->

- 1 The BG function is not available on the MPC5553. Do not select 0b001 or 0b011 for the PA field except for CAL\_ADDR[11].
- 2 When configured as CAL\_ADDR[11], MDIO, or CAL\_CS[3], the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 3 When configured as CAL\_ADDR[11], MDIO, CAL\_CS[3], or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.
- 4 When configured as CAL\_ADDR[11] or CAL\_CS[3], the ODE bit should be set to zero.
- 5 If external master operation is enabled, the HYS bit should be set to zero.
- 6 See the EBI section for weak pull up settings when configured as CAL\_ADDR[11] or CAL\_CS[3].

Figure 6-46. MPC5553: BG(CAL\_ADDR[11])\_MDIO\_CAL\_CS[3]\_GPIO[73] Pad Configuration Register (SIU\_PCR73)

See Table 6-15 for bit field definitions. The PA field for MPC5553's PCR73 is given in Table 6-20.

## Table 6-20. PCR73 PA Field Definition

| PA Field   | Pin Function                              |
|------------|-------------------------------------------|
| 0b000      | GPIO[73]                                  |
| 0b001      | CAL_ADDR[11] 1                            |
| 0b010      | MDIO                                      |
| 0b011      | CAL_ADDR[11]<f-helvetica><st-superscript> |
| 0b100      | CAL_CS[3] 1                               |

1 For calibration only.

## 6.3.1.12.35 MPC5554: Pad Configuration Register 73 (SIU\_PCR73)

The  SIU\_PCR73  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the BG\_GPIO[73] pin.

## SIU\_BASE+0xD2

<!-- image -->

- 1 When configured as BG, the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 2 When configured as BG or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.
- 3 When configured as BG, and external master operation is enabled with internal arbitration, the ODE bit should be set to zero.
- 4 If external master operation is enabled, the HYS bit should be set to zero.
- 5 See the EBI section for weak pull up settings when configured as BG.

## Figure 6-47. MPC5554: BG\_GPIO[73] Pad Configuration Register (SIU\_PC73)

See Table 6-15 for bit field definitions.

## 6.3.1.12.36 MPC5554: Pad Configuration Register 74 (SIU\_PCR74)

## NOTE

The MPC5553 does not implement PCR74. Treat the register like reserved space.

The  SIU\_PCR74  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the BB\_GPIO[74] pin.

## SIU\_BASE+0xD4

<!-- image -->

- 1 When configured as BB, the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 2 When configured as BB or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.
- 3 When configured as BB, and external master operation is enabled with internal arbitration, the ODE bit should be set to zero.
- 4 If external master operation is enabled, the HYS bit should be set to zero.
- 5 See the EBI section for weak pull up settings when configured as BB.

## Figure 6-48. MPC5554: BB\_GPIO[74] Pad Configuration Register (SIU\_PCR74)

See Table 6-15 for bit field definitions.

## 6.3.1.12.37 Pad Configuration Register 75 - 82 (SIU\_PCR75 - SIU\_PCR82)

The SIU\_PCR75 - SIU\_PCR82 registers control the pin function, direction, and static electrical attributes of the MDO[4:11]\_GPIO[75:82] pins. GPIO is the default function at reset for these pins. The full port mode (FPM) bit in the Nexus port controller (NPC) port configuration register controls whether the pins function as MDO[4:11] or GPIO[75:82]. The pad interface port enable for these pins is driven by the NPC block. When the FPM bit is set, the NPC enables the MDO port enable, and disables GPIO. When the FPM bit is cleared, the NPC disables the MDO port enable, and enables GPIO.

## SIU\_BASE+0xD6 - SIU\_BASE+0xE4 (8)

<!-- image -->

- 1 This bit applies only to GPIO operation. For GPO , the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register.  Setting IBE to zero reduces power consumption.
- 2 The ODE bit should be set to zero for MDO operation.
- 3 The HYS bit has no affect on MDO operation.
- 4 The WPE bit should be set to zero for MDO operation.

Figure 6-49. MDO[4:11]\_GPIO[75:82] Pad Configuration Register (SIU\_PCR75 - SIU\_PCR82)

See Table 6-15 for bit field definitions.

## 6.3.1.12.38 Pad Configuration Register 83 (SIU\_PCR83)

The  SIU\_PCR83  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the CNTXA\_GPIO[83] pin.

## SIU\_BASE+0xE6

<!-- image -->

- 1 When configured as CNTX, the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 2 When configured as CNTX or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.

Figure 6-50. CNTXA\_GPIO[83] Pad Configuration Register (SIU\_PCR83)

See Table 6-15 for bit field definitions.

## 6.3.1.12.39 Pad Configuration Register 84 (SIU\_PCR84)

The  SIU\_PCR84  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the CNRX\_A\_GPIO[84] pin.

## SIU\_BASE+0xE8

<!-- image -->

- 1 When configured as CNRX, the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 2 When configured as CNRX or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.

Figure 6-51. CNRX\_A\_GPIO[84] Pad Configuration Register (SIU\_PCR84)

See Table 6-15 for bit field definitions.

## 6.3.1.12.40 Pad Configuration Register 85 (SIU\_PCR85)

The  SIU\_PCR85  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the CNTXB\_PCSC[3]\_GPIO[85] pin. The CNTXB function is not available in the MPC5553 (this register allows selection of the PCSC[3] and GPIO functions).

## SIU\_BASE+0xEA

<!-- image -->

- 1 The CNTXB function is not available on the MPC5553. Do not select 0b01 or 0b11 for the PA field.
- 2 When configured as CNTX (MPC5554 only) or PCS, the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 3 When configured as CNTX (MPC5554 only) or PCS or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.

## Figure 6-52. CNTXB\_PCSC[3]\_GPIO[85] Pad Configuration Register (SIU\_PCR85)

See Table 6-15 for bit field definitions.

## 6.3.1.12.41 Pad Configuration Register 86 (SIU\_PCR86)

The  SIU\_PCR86  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the CNRX\_B\_PCSC[4]\_GPIO[86] pin. The CNRX\_B function is not available in MPC5553 (this register allows selection of the PCSC[4] and GPIO functions).

## SIU\_BASE+0xEC

<!-- image -->

- 1 The CNRX\_B function is not available on the MPC5553. Do not select 0b01 or 0b11 for the PA field.
- 2 When configured as CNRX or PCS, the OBE bit has no effect. When configured as GPO, the OBE bit should be set to one.
- 3 When configured as CNRX or PCS or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.

Figure 6-53. CNRX\_B\_PCSC[4]\_GPIO[86] Pad Configuration Register (SIU\_PCR86)

See Table 6-15 for bit field definitions.

## 6.3.1.12.42 Pad Configuration Register 87 (SIU\_PCR87)

The  SIU\_PCR87  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the CNTXC\_PCSD[3]\_GPIO[87] pin.

## SIU\_BASE+0xEE

<!-- image -->

- 1 When configured as CNTX or PCS, the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 2 When configured as CNTX or PCS or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.

Figure 6-54. CNTXC\_PCSD[3]\_GPIO[87] Pad Configuration Register (SIU\_PCR87)

See Table 6-15 for bit field definitions.

## 6.3.1.12.43 Pad Configuration Register 88 (SIU\_PCR88)

The  SIU\_PCR88  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the CNRX\_C\_PCSD[4]\_GPIO[88] pin.

## SIU\_BASE+0xF0

<!-- image -->

- 1 When configured as CNRX or PCS, the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 2 When configured as CNRX or PCS or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.

Figure 6-55. CNRX\_C\_PCSD[4]\_GPIO[88] Pad Configuration Register (SIU\_PCR88)

See Table 6-15 for bit field definitions.

## 6.3.1.12.44 Pad Configuration Register 89 (SIU\_PCR89)

The  SIU\_PCR89  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the TXD\_A\_GPIO[89] pin.

## SIU\_BASE+0xF2

<!-- image -->

- 1 When configured as TXD, the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 2 When configured as TXD or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. For SCI loop back operation the IBE bit must be set to one. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.

Figure 6-56. TXD\_A\_GPIO[89] Pad Configuration Register (SIU\_PCR89)

See Table 6-15 for bit field definitions.

## 6.3.1.12.45 Pad Configuration Register 90 (SIU\_PCR90)

The  SIU\_PCR90  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the RXD\_A\_GPIO[90] pin.

## SIU\_BASE+0xF4

<!-- image -->

- 1 When configured as RXD, the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 2 When configured as RXD or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.

Figure 6-57. RXD\_A\_GPIO[90] Pad Configuration Register (SIU\_PCR90)

See Table 6-15 for bit field definitions.

## 6.3.1.12.46 Pad Configuration Register 91 (SIU\_PCR91)

The  SIU\_PCR91  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the TXD\_B\_PCSD[1]\_GPIO[91] pin.

## SIU\_BASE+0xF6

<!-- image -->

- 1 When configured as TXD or PCS, the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 2 When configured as TXD or PCS or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. For SCI loop back operation the IBE bit must be set to one. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.

## Figure 6-58. TXD\_B\_PCSD[1]\_GPIO[91] Pad Configuration Register (SIU\_PCR91)

See Table 6-15 for bit field definitions.

## 6.3.1.12.47 Pad Configuration Register 92 (SIU\_PCR92)

The  SIU\_PCR92  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the RXD\_B\_PCSD[5]\_GPIO[92] pin.

## SIU\_BASE+0xF8

<!-- image -->

- 1 When configured as RXD or PCS, the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 2 When configured as RXD or PCS or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.

Figure 6-59. RXD\_B\_PCSD[5]\_GPIO[92] Pad Configuration Register (SIU\_PCR92)

See Table 6-15 for bit field definitions.

## 6.3.1.12.48 Pad Configuration Register 93 (SIU\_PCR93)

The  SIU\_PCR93  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the SCKA\_PCSC[1]\_GPIO[93] pin. The SCKA function is not available in the MPC5553 (this register allows selection of the PCSC[1] and GPIO functions).

## SIU\_BASE+0xFA

<!-- image -->

- 1 The SCKA function is not available on the MPC5553. Do not select 0b01 or 0b11 for the PA field.
- 2 When configured as SCK, the OBE bit should be set to one for master operation, and set to zero for slave operation. When configured as PCS, the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 3 When configured as SCK in slave operation, the IBE bit should be set to one. When configured as SCK in master operation, PCS, or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.

## Figure 6-60. SCKA\_PCSC[1]\_GPIO[93] Pad Configuration Register (SIU\_PCR93)

See Table 6-15 for bit field definitions.

## 6.3.1.12.49 Pad Configuration Register 94 (SIU\_PCR94)

The  SIU\_PCR94  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the SIN\_A\_PCSC[2]\_GPIO[94] pin. The SIN\_A function  is  not  available  in  the  MPC5553  (this  register allows selection of the PCSC[2] and GPIO functions).

## SIU\_BASE+0xFC

<!-- image -->

- 1 The SIN\_A function is not available on the MPC5553. Do not select 0b01 or 0b11 for the PA field.
- 2 When configured as SIN or PCS, the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 3 When configured as SIN, PCS, or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.

Figure 6-61. SIN\_A\_PCSC[2]\_GPIO[94] Pad Configuration Register (SIU\_PCR94)

See Table 6-15 for bit field definitions.

## 6.3.1.12.50 Pad Configuration Register 95 (SIU\_PCR95)

The  SIU\_PCR95  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the SOUTA\_PCSC[5]\_GPIO[95] pin. The SOUTA function is not available in the MPC5553 (this register allows selection of the PCSC[5] and GPIO functions).

## SIU\_BASE+0xFE

<!-- image -->

- 1 The SOUTA function is not available on the MPC5553. Do not select 0b01 or 0b11 for the PA field.
- 2 When configured as SOUT or PCS, the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 3 When configured as SOUT, PCS, or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.

## Figure 6-62. SOUTA\_PCSC[5]\_GPIO[95] Pad Configuration Register (SIU\_PCR95)

See Table 6-15 for bit field definitions.

## 6.3.1.12.51 Pad Configuration Registers 96 (SIU\_PCR96)

The  SIU\_PCR96  registers  control  the  pin  function,  direction,  and  static  electrical  attributes  of  the PCSA[0]\_PCSD[2]\_GPIO[96] pin. The PCSA[0] function is not available in the MPC5553 (this register allows selection of the PCSD[2] and GPIO functions).

## SIU\_BASE+0x100

<!-- image -->

- 1 The PCSA[0] function is not available on the MPC5553. Do not select 0b01 or 0b11 for the PA field.
- 2 When configured as PCSA[0], the OBE bit should be set to one for master operation, and set to zero for slave operation. When configured as PCSD[2], the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 3 When configured as PCSA[0] in slave operation, the IBE bit should be set to one. When configured as PCSA[0] in master operation, PCSD[2], or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.

Figure 6-63. PCSA[0]\_PCSD[2]\_GPIO[96] Pad Configuration Register (SIU\_PCR96)

See Table 6-15 for bit field definitions.

## 6.3.1.12.52 Pad Configuration Registers 97 (SIU\_PCR97)

The  SIU\_PCR97  registers  control  the  pin  function,  direction,  and  static  electrical  attributes  of  the PCSA[1]\_PCSB[2]\_GPIO[97] pin. The PCSA[1] function is not available in the MPC5553 (this register allows selection of the PCSB[2] and GPIO functions).

## SIU\_BASE+0x102

<!-- image -->

- 1 The PCSA[1] function is not available on the MPC5553. Do not select 0b01 or 0b11 for the PA field.
- 2 When configured as PCS, the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 3 When configured as PCS or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.

## Figure 6-64. PCSA[1]\_PCSB[2]\_GPIO[97] Pad Configuration Register (SIU\_PCR97)

See Table 6-15 for bit field definitions.

## 6.3.1.12.53 Pad Configuration Register 98 (SIU\_PCR98)

The  SIU\_PCR98  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the PCSA[2]\_SCKD\_GPIO[98] pin. The PCSA[2] function is not available in the MPC5553 (this register allows selection of the SCKD and GPIO functions).

## SIU\_BASE+0x104

<!-- image -->

- 1 The PCSA[2] function is not available on the MPC5553. Do not select 0b01 or 0b11 for the PA field.
- 2 When configured as PCS, the OBE bit has no affect. When configured as SCK, the OBE bit should be set to one for master operation, and set to zero for slave operation. When configured as GPO, the OBE bit should be set to one.
- 3 When configured as SCK in slave operation, the IBE bit should be set to one. When configured as PCS or SCK in master operation or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.

## Figure 6-65. PCSA[2]\_SCKD\_GPIO[98] Pad Configuration Register (SIU\_PCR98)

See Table 6-15 for bit field definitions.

## 6.3.1.12.54 Pad Configuration Register 99 (SIU\_PCR99)

The  SIU\_PCR99  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the PCSA[3]\_SIN\_D\_GPIO[99] pin. The PCSA[3] function is not available in the MPC5553 (this register allows selection of the SIN\_D and GPIO functions).

## SIU\_BASE+0x106

<!-- image -->

- 1 The PCSA[3] function is not available on the MPC5553. Do not select 0b01 or 0b11 for the PA field.
- 2 When configured as PCS, the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 3 When configured as PCS or SIN or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.

## Figure 6-66. PCSA[3]\_SIN\_D\_GPIO[99] Pad Configuration Register (SIU\_PCR99)

See Table 6-15 for bit field definitions.

## 6.3.1.12.55 Pad Configuration Register 100 (SIU\_PCR100)

The  SIU\_PCR100  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the PCSA[4]\_SOUTD\_GPIO[100] pin. The PCSA[4] function is not available in the MPC5553 (this register allows selection of the SOUTD and GPIO functions).

## SIU\_BASE+0x108

<!-- image -->

- 1 The PCSA[4] function is not available on the MPC5553. Do not select 0b01 or 0b11 for the PA field.
- 2 When configured as PCS or SOUT, the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 3 When configured as PCS or SOUT or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.

Figure 6-67. PCSA[4]\_SOUTD\_GPIO[100] Pad Configuration Register (SIU\_PCR100)

See Table 6-15 for bit field definitions.

## 6.3.1.12.56 Pad Configuration Registers 101 (SIU\_PCR101)

The  SIU\_PCR101  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the PCSA[5]\_PCSB[3]\_GPIO[101] pin. The PCSA[5] function is not available in the MPC5553 (this register allows selection of the PCSB[3] and GPIO functions).

## SIU\_BASE+0x10A

<!-- image -->

- 1 The PCSA[5] function is not available on the MPC5553. Do not select 0b01 or 0b11 for the PA field.
- 2 When configured as PCS, the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 3 When configured as PCS or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.

## Figure 6-68. PCSA[5]\_PCSB[3]\_GPIO[101] Pad Configuration Register (SIU\_PCR101)

See Table 6-15 for bit field definitions.

## 6.3.1.12.57 Pad Configuration Register 102 (SIU\_PCR102)

The  SIU\_PCR102  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the SCKB\_PCSC[1]\_GPIO[102] pin.

## SIU\_BASE+0x10C

<!-- image -->

- 1 When configured as SCK, the OBE bit should be set to one for master operation, and set to zero for slave operation. When configured as GPO, the OBE bit should be set to one.
- 2 When configured as SCK in slave operation the IBE bit should be set to one. When configured as SCK in master operation or PCS or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.

## Figure 6-69. SCKB\_PCSC[1]\_GPIO[102] Pad Configuration Register (SIU\_PCR102)

See Table 6-15 for bit field definitions.

## 6.3.1.12.58 Pad Configuration Register 103 (SIU\_PCR103)

The  SIU\_PCR103  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the SIN\_B\_PCSC[2]\_GPIO[103] pin.

## SIU\_BASE+0x10E

<!-- image -->

- 1 When configured as SIN, the OBE bit should be set to zero. When configured as PCS, the OBE bit should be set to one.
- 2 When configured as SIN or PCS, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.

Figure 6-70. SIN\_B\_PCSC[2]\_GPIO[103] Pad Configuration Register (SIU\_PCR103)

See Table 6-15 for bit field definitions.

## 6.3.1.12.59 Pad Configuration Register 104 (SIU\_PCR104)

The  SIU\_PCR104  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the SOUTB\_PCSC[5]\_GPIO[104] pin.

## SIU\_BASE+0x110

<!-- image -->

- 1 When configured as SOUT or PCS, the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 2 When configured as SOUT or PCS or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.

Figure 6-71. SOUTB\_PCSC[5]\_GPIO[104] Pad Configuration Register (SIU\_PCR104)

See Table 6-15 for bit field definitions.

## 6.3.1.12.60 Pad Configuration Register 105 (SIU\_PCR105)

The  SIU\_PCR105  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the PCSB[0]\_PCSD[2]\_GPIO[105] pin.

## SIU\_BASE+0x112

<!-- image -->

- 1 When configured as PCS, the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 2 When configured as PCS or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.

Figure 6-72. PCSB[0]\_PCSD[2]\_GPIO[105] Pad Configuration Register (SIU\_PCR105)

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

See Table 6-15 for bit field definitions.

## 6.3.1.12.61 Pad Configuration Register 106 (SIU\_PCR106)

The  SIU\_PCR106  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the PCSB[1]\_PCSD[0]\_GPIO[106] pin.

## SIU\_BASE+0x114

<!-- image -->

- 1 When configured as PCSB[1], the OBE bit has no affect. When configured as PCSD[0], the OBE bit should be set to one for master operation, and set to zero for slave operation. When configured as GPO, the OBE bit should be set to one.
- 2 When configured as PCSD[0] in slave operation, the IBE bit should be set to one. When configured as PCS in master operation or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.

## Figure 6-73. PCSB[1]\_PCSD[0]\_GPIO[106] Pad Configuration Register (SIU\_PCR106)

See Table 6-15 for bit field definitions.

## 6.3.1.12.62 Pad Configuration Register 107 (SIU\_PCR107)

The  SIU\_PCR107  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the PCSB[2]\_SOUTC\_GPIO[107] pin.

## SIU\_BASE+0x116

<!-- image -->

- 1 When configured as PCS or SOUT, the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 2 When configured as PCS or SOUT or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.

Figure 6-74. PCSB[2]\_SOUTC\_GPIO[107] Pad Configuration Register (SIU\_PCR107)

See Table 6-15 for bit field definitions.

## 6.3.1.12.63 Pad Configuration Register 108 (SIU\_PCR108)

The  SIU\_PCR108  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the PCSB[3]\_SIN\_C\_GPIO[108] pin.

## SIU\_BASE+0x118

<!-- image -->

- 1 When configured as PCS or SIN, the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 2 When configured as PCS or SIN or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.

Figure 6-75. PCSB[3]\_SIN\_C\_GPIO[108] Pad Configuration Register (SIU\_PCR108)

See Table 6-15 for bit field definitions.

## 6.3.1.12.64 Pad Configuration Register 109 (SIU\_PCR109)

The  SIU\_PCR109  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the PCSB[4]\_SCKC\_GPIO[109] pin.

## SIU\_BASE+0x11A

<!-- image -->

- 1 When configured as SCK, the OBE bit should be set to one for master operation, and set to zero for slave operation. When configured as PCS, the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 2 When configured as SCK in slave operation, the IBE bit should be set to one. When configured as PCS or SCK in master operation or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.

Figure 6-76. PCSB[4]\_SCKC\_GPIO[109] Pad Configuration Register (SIU\_PCR109)

See Table 6-15 for bit field definitions.

## 6.3.1.12.65 Pad Configuration Register 110 (SIU\_PCR110)

The  SIU\_PCR110  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the PCSB[5]\_PCSC[0]\_GPIO[110] pin.

## SIU\_BASE+0x11C

<!-- image -->

- 1 When configured as PCSB[5], the OBE bit has no affect. When configured as PCSC[0], the OBE bit should be set to one for master operation, and set to zero for slave operation. When configured as GPO, the OBE bit should be set to one.
- 2 When configured as PCSC[0] in slave operation, the IBE bit should be set to one. When configured as PCS in master operation or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.

Figure 6-77. PCSB[5]\_PCSC[0]\_GPIO[110] Pad Configuration Register (SIU\_PCR110)

See Table 6-15 for bit field definitions.

## 6.3.1.12.66 Pad Configuration Register 111 - 112 (SIU\_PCR111 - SIU\_PCR112)

The  SIU\_PCR111  -  SIU\_PCR112  registers  control  the  pin  function,  direction,  and  static  electrical attributes of the ETRIG[0:1]\_GPIO[111:112] pins.

## SIU\_BASE+0x11E - SIU\_BASE+0x120 (2)

<!-- image -->

- 1 When configured as ETRIG, the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 2 When configured as ETRIG or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.

Figure 6-78. ETRIG[0:1]\_GPIO[111:112] Pad Configuration Register (SIU\_PCR111 - SIU\_PCR112)

See Table 6-15 for bit field definitions.

## 6.3.1.12.67 Pad Configuration Register 113 (SIU\_PCR113)

The  SIU\_PCR113  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the TCRCLKA\_IRQ[7]\_GPIO[113] pin.

## SIU\_BASE+0x122

<!-- image -->

- 1 When configured as TCRCLKA or IRQ, the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 2 When configured as TCRCLKA or IRQ or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption.When configured as GPI, the IBE bit should be set to one.

Figure 6-79. TCRCLKA\_IRQ[7]\_GPIO[113] Pad Configuration Register (SIU\_PCR113)

See Table 6-15 for bit field definitions.

## 6.3.1.12.68 Pad Configuration Register 114 - 125 (SIU\_PCR114 - SIU\_PCR125)

The  SIU\_PCR114  -  SIU\_PCR125  registers  control  the  pin  function,  direction,  and  static  electrical attributes  of  the  ETPUA[0:11]\_ETPUA[12:23]\_GPIO[114:125]  pins.  Only  the  output  channels  of ETPUA[12:23] are connected to pins. Both the input and output channels of ETPUA[0:11] are connected to pins.

## SIU\_BASE+0x124 - SIU\_BASE+0x13A (12)

<!-- image -->

- 1 The OBE bit must be set to one for both ETPUA[0:11] and GPIO[114:125] when configured as outputs. When configured as ETPUA[12:23], the OBE bit has no affect.
- 2 The IBE bit must be set to one for both ETPUA[0:11] and GPIO[114:125] when configured as inputs. When configured as ETPUA[12:23] or when ETPUA[0:11] or GPIO[114:125] are configured as outputs, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register.
- 3 The weak pull up/down selection at reset for the ETPUA[0:11] pins is determined by the WKPCFG pin.

Figure 6-80. ETPUA[0:11]\_ETPUA[12:23]\_GPIO[114:125] Pad Configuration Register (SIU\_PCR114 - SIU\_PCR125)

See Table 6-15 for bit field definitions.

## 6.3.1.12.69 Pad Configuration Register 126 (SIU\_PCR126)

The  SIU\_PCR126  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the ETPUA[12]\_PCSB[1]\_GPIO[126] pin.

## SIU\_BASE+0x13C

<!-- image -->

- 1 When configured as PCS, the OBE bit has no affect. The OBE bit must be set to one for both ETPUA and GPIO when configured as outputs.
- 2 The IBE bit must be set to one for both ETPUA and GPIO when configured as inputs. When configured as PCS, or ETPUA or GPO outputs, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register.
- 3 The weak pull up/down selection at reset for the ETPUA[12] pin is determined by the WKPCFG pin.

## Figure 6-81. ETPUA[12]\_PCSB[1]\_GPIO[126] Pad Configuration Register (SIU\_PCR126)

See Table 6-15 for bit field definitions.

## 6.3.1.12.70 Pad Configuration Register 127 (SIU\_PCR127)

The  SIU\_PCR127  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the ETPUA[13]\_PCSB[3]\_GPIO[127] pin.

## SIU\_BASE+0x13E

<!-- image -->

- 1 When configured as PCS, the OBE bit has no affect. The OBE bit must be set to one for both ETPUA and GPIO when configured as outputs.
- 2 The IBE bit must be set to one for both ETPUA and GPIO when configured as inputs. When configured as PCS, or ETPUA or GPO outputs, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register.
- 3 The weak pull up/down selection at reset for the ETPUA[13] pin is determined by the WKPCFG pin.

Figure 6-82. ETPUA[13]\_PCSB[3]\_GPIO[127] Pad Configuration Register (SIU\_PCR127)

See Table 6-15 for bit field definitions.

## 6.3.1.12.71 Pad Configuration Register 128 (SIU\_PCR128)

The  SIU\_PCR128  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the ETPUA[14]\_PCSB[4]\_GPIO[128] pin.

## SIU\_BASE+0x140

<!-- image -->

- 1 When configured as PCS, the OBE bit has no affect. The OBE bit must be set to one for both ETPUA and GPIO when configured as outputs.
- 2 The IBE bit must be set to one for both ETPUA and GPIO when configured as inputs. When configured as PCS, or ETPUA or GPO outputs, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register.
- 3 The weak pull up/down selection at reset for the ETPUA[14] pin is determined by the WKPCFG pin.

## Figure 6-83. ETPUA[14]\_PCSB[4]\_GPIO[128] Pad Configuration Register (SIU\_PCR128)

See Table 6-15 for bit field definitions.

## 6.3.1.12.72 Pad Configuration Register 129 (SIU\_PCR129)

The  SIU\_PCR129  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the ETPUA[15]\_PCSB[5]\_GPIO[129] pin.

## SIU\_BASE+0x142

<!-- image -->

- 1 When configured as PCS, the OBE bit has no affect. The OBE bit must be set to one for both ETPUA and GPIO when configured as outputs.
- 2 The IBE bit must be set to one for both ETPUA and GPIO when configured as inputs. When configured as PCS, or ETPUA or GPO outputs, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register.
- 3 The weak pull up/down selection at reset for the ETPUA[15] pin is determined by the WKPCFG pin.

Figure 6-84. ETPUA[15]\_PCSB[5]\_GPIO[129] Pad Configuration Register (SIU\_PCR129)

See Table 6-15 for bit field definitions.

## 6.3.1.12.73 Pad Configuration Register 130 (SIU\_PCR130)

The  SIU\_PCR130  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the ETPUA[16]\_PCSD[1]\_GPIO[130] pin.

## SIU\_BASE+0x144

<!-- image -->

- 1 When configured as PCS, the OBE bit has no affect. The OBE bit must be set to one for both ETPUA and GPIO when configured as outputs.
- 2 The IBE bit must be set to one for both ETPUA and GPIO when configured as inputs. When configured as PCS, or ETPUA or GPO outputs, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register.
- 3 The weak pull up/down selection at reset for the ETPUA[16] pin is determined by the WKPCFG pin.

## Figure 6-85. ETPUA[16]\_PCSD[1]\_GPIO[130] Pad Configuration Register (SIU\_PCR130)

See Table 6-15 for bit field definitions.

## 6.3.1.12.74 Pad Configuration Register 131 (SIU\_PCR131)

The  SIU\_PCR131  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the ETPUA[17]\_PCSD[2]\_GPIO[131] pin.

## SIU\_BASE+0x146

<!-- image -->

- 1 When configured as PCS, the OBE bit has no affect. The OBE bit must be set to one for both ETPUA and GPIO when configured as outputs.
- 2 The IBE bit must be set to one for both ETPUA and GPIO when configured as inputs. When configured as PCS, or ETPUA or GPO outputs, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register.
- 3 The weak pull up/down selection at reset for the ETPUA[17] pin is determined by the WKPCFG pin.

Figure 6-86. ETPUA[17]\_PCSD[2]\_GPIO[131] Pad Configuration Register (SIU\_PCR131)

See Table 6-15 for bit field definitions.

## 6.3.1.12.75 Pad Configuration Register 132 (SIU\_PCR132)

The  SIU\_PCR132  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the ETPUA[18]\_PCSD[3]\_GPIO[132] pin.

## SIU\_BASE+0x148

<!-- image -->

- 1 When configured as PCS, the OBE bit has no affect. The OBE bit must be set to one for both ETPUA and GPIO when configured as outputs.
- 2 The IBE bit must be set to one for both ETPUA and GPIO when configured as inputs. When configured as PCS, or ETPUA or GPO outputs, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register.
- 3 The weak pull up/down selection at reset for the ETPUA[18] pin is determined by the WKPCFG pin.

Figure 6-87. ETPUA[18]\_PCSD[3]\_GPIO[132] Pad Configuration Register (SIU\_PCR132)

See Table 6-15 for bit field definitions.

## 6.3.1.12.76 Pad Configuration Register 133 (SIU\_PCR133)

The  SIU\_PCR133  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the ETPUA[19]\_PCSD[4]\_GPIO[133] pin.

## SIU\_BASE+0x14A

<!-- image -->

- 1 When configured as PCS, the OBE bit has no affect. The OBE bit must be set to one for both ETPUA and GPIO when configured as outputs.
- 2 The IBE bit must be set to one for both ETPUA and GPIO when configured as inputs. When configured as PCS, or ETPUA or GPO outputs, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register.
- 3 The weak pull up/down selection at reset for the ETPUA[19] pin is determined by the WKPCFG pin.

Figure 6-88. ETPUA[19]\_PCSD[4]\_GPIO[133] Pad Configuration Register (SIU\_PCR133)

See Table 6-15 for bit field definitions.

## 6.3.1.12.77 Pad Configuration Register 134 - 141 (SIU\_PCR134 - SIU\_PCR141)

The  SIU\_PCR134  -  SIU\_PCR141  registers  control  the  pin  function,  direction,  and  static  electrical attributes of the ETPUA[20:27]\_IRQ[8:15]\_GPIO[134:141] pins. Only the output channels of ETPUA[24:27] are connected to pins. Both the input and output channels of ETPUA[20:23] are connected to pins.

## SIU\_BASE+0x14C - SIU\_BASE+0x15A (8)

<!-- image -->

- 1 When configured as ETPUA[24:27] or IRQ, the OBE bit has no affect. The OBE bit must be set to one for both ETPUA[20:23] and GPIO[134:141] when configured as outputs.
- 2 When configured as ETPUA[24:27] or IRQ or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. The IBE bit must be set to one for both ETPUA[20:23] and GPIO[134:141] when configured as inputs.
- 3 The weak pull up/down selection at reset for the ETPUA[20:27] pins is determined by the WKPCFG pin.

Figure 6-89. ETPUA[20:27]\_IRQ[8:15]\_GPIO[134:141] Pad Configuration Register (SIU\_PCR134 - SIU\_PCR141)

See Table 6-15 for bit field definitions.

## 6.3.1.12.78 Pad Configuration Register 142 (SIU\_PCR142)

The  SIU\_PCR142  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the ETPUA[28]\_PCSC[1]\_GPIO[142] pin. Only the output channel of ETPUA[28] is connected to the pin.

## SIU\_BASE+0x15C

<!-- image -->

- 1 When configured as ETPUA or PCS, the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 2 When configured as ETPUA, PCS, or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. The IBE bit must be set to one for GPIO when configured as input.
- 3 The weak pull up/down selection at reset for the ETPUA[28] pin is determined by the WKPCFG pin

Figure 6-90. ETPUA[28]\_PCSC[1]\_GPIO[142] Pad Configuration Register (SIU\_PCR142)

See Table 6-15 for bit field definitions.

## 6.3.1.12.79 Pad Configuration Register 143 (SIU\_PCR143)

The  SIU\_PCR143  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the ETPUA[29]\_PCSC[2]\_GPIO[143] pin. Only the output channel of ETPUA[29] is connected to the pin.

## SIU\_BASE+0x15E

<!-- image -->

- 1 When configured as ETPUA or PCS, the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 2 When configured as ETPUA, PCS, or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. The IBE bit must be set to one for GPIO when configured as input.
- 3 The weak pull up/down selection at reset for the ETPUA[29] pin is determined by the WKPCFG pin

Figure 6-91. ETPUA[29]\_PCSC[2]\_GPIO[143] Pad Configuration Register (SIU\_PCR143)

See Table 6-15 for bit field definitions.

## 6.3.1.12.80 Pad Configuration Register 144 (SIU\_PCR144)

The  SIU\_PCR144  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the ETPUA[30]\_PCSC[3]\_GPIO[144] pin.

## SIU\_BASE+0x160

<!-- image -->

- 1 When configured as PCS, the OBE bit has no affect. When configured as ETPUA output or GPO, the OBE bit should be set to one.
- 2 When configured as ETPUA output, PCS, or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. The IBE bit must be set to one for ETPUA or GPIO when configured as input.
- 3 The weak pull up/down selection at reset for the ETPUA[30] pin is determined by the WKPCFG pin

## Figure 6-92. ETPUA[30]\_PCSC[3]\_GPIO[144] Pad Configuration Register (SIU\_PCR144)

See Table 6-15 for bit field definitions.

## 6.3.1.12.81 Pad Configuration Register 145 (SIU\_PCR145)

The  SIU\_PCR145  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the ETPUA[31]\_PCSC[4]\_GPIO[145] pin.

## SIU\_BASE+0x162

<!-- image -->

- 1 When configured as PCS, the OBE bit has no affect. When configured as ETPUA output or GPO, the OBE bit should be set to one.
- 2 When configured as ETPUA output, PCS, or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. The IBE bit must be set to one for ETPUA or GPIO when configured as input.
- 3 The weak pull up/down selection at reset for the ETPUA[31] pin is determined by the WKPCFG pin

Figure 6-93. ETPUA[31]\_PCSC[4]\_GPIO[145] Pad Configuration Register (SIU\_PCR145)

See Table 6-15 for bit field definitions.

## 6.3.1.12.82 MPC5554: Pad Configuration Register 146 (SIU\_PCR146)

## NOTE

The MPC5553 does not implement PCR146-178. Treat those registers as reserved space.

The  SIU\_PCR146  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the TCRCLKB\_IRQ[6]\_GPIO[146] pin.

## SIU\_BASE+0x164

<!-- image -->

- 1 When configured as TCRCLKB or IRQ, the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 2 When configured as TCRCLKB or IRQ or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.

Figure 6-94. MPC5554: TCRCLKB\_IRQ[6]\_GPIO[146] Pad Configuration Register (SIU\_PCR146)

See Table 6-15 for bit field definitions.

## 6.3.1.12.83 MPC5554: Pad Configuration Register 147 - 162 (SIU\_PCR147 - SIU\_PCR162)

## NOTE

The MPC5553 does not implement PCR146-178. Treat those registers as reserved space.

The  SIU\_PCR147  -  SIU\_PCR162  registers  control  the  pin  function,  direction,  and  static  electrical attributes of the ETPUB[0:15]\_ETPUB[16:31]\_GPIO[147:162] pins. Both the input and output channels

of ETPUB[0:15] are connected to these pins and only the output channels of ETPUB[16:31] are connected to these pins.

## SIU\_BASE+0x166 - SIU\_BASE+0x184 (16)

<!-- image -->

- 1 The OBE bit must be set to one for both ETPUB[0:15] and GPIO[147:162] when configured as outputs. When configured as ETPUB[16:31], the OBE bit has no affect.
- 2 When configured as ETPUB or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. The IBE bit must be set to one for both ETPUB[0:15] and GPIO[147:162] when configured as inputs.
- 3 The weak pull up/down selection at reset for the ETPUB[0:15] pins is determined by the WKPCFG pin.

Figure 6-95. MPC5554: ETPUB[0:15]\_ETPUB[16:31]\_GPIO[147:162] Pad Configuration Register (SIU\_PCR147 - SIU\_PCR162)

See Table 6-15 for bit field definitions.

## 6.3.1.12.84 MPC5554: Pad Configuration Register 163 (SIU\_PCR163)

## NOTE

The MPC5553 does not implement PCR146-178. Treat those registers as reserved space.

The  SIU\_PCR163  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the ETPUB[16]\_PCSA[1]\_GPIO[163] pin. Both the input and output channel of ETPUB[16] are connected to the pin.

## SIU\_BASE+0x186

<!-- image -->

- 1 The OBE bit must be set to one for both ETPUB and GPIO when configured as outputs. When configured as PCS, the OBE bit has no affect.
- 2 When configured as ETPUB or GPIO outputs, or configured as PCS, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. The IBE bit must be set to one for both ETPUB and GPIO when configured as inputs.
- 3 The weak pull up/down selection at reset for the ETPUB[16] pin is determined by the WKPCFG pin.

Figure 6-96. MPC5554: ETPUB[16]\_PCSA[1]\_GPIO[163] Pad Configuration Register (SIU\_PCR163)

See Table 6-15 for bit field definitions.

## 6.3.1.12.85 MPC5554: Pad Configuration Register 164 (SIU\_PCR164)

## NOTE

The MPC5553 does not implement PCR146-178. Treat those registers as reserved space.

The  SIU\_PCR164  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the ETPUB[17]\_PCSA[2]\_GPIO[164] pin. Both the input and output channel of ETPUB[17] are connected to the pin.

## SIU\_BASE+0x188

<!-- image -->

- 1 The OBE bit must be set to one for both ETPUB[17] and GPIO[164] when configured as outputs. When configured as PCS, the OBE bit has no affect.
- 2 When configured as ETPUB or GPIO outputs, or configured as PCS, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. The IBE bit must be set to one for both ETPUB[17] and GPIO[164] when configured as inputs.
- 3 The weak pull up/down selection at reset for the ETPUB[17] pin is determined by the WKPCFG pin.

Figure 6-97. MPC5554: ETPUB[17]\_PCSA[2]\_GPIO[164] Pad Configuration Register (SIU\_PCR164)

See Table 6-15 for bit field definitions.

## 6.3.1.12.86 MPC5554: Pad Configuration Register 165 (SIU\_PCR165)

## NOTE

The MPC5553 does not implement PCR146-178. Treat those registers as reserved space.

The  SIU\_PCR165  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the ETPUB[18]\_PCSA[3]\_GPIO[165] pin. Both the input and output channel of ETPUB[18] are connected to the pin.

## SIU\_BASE+0x18A

<!-- image -->

- 1 The OBE bit must be set to one for both ETPUB[18] and GPIO[165] when configured as outputs. When configured as PCS, the OBE bit has no affect.
- 2 When configured as ETPUB or GPIO outputs, or configured as PCS, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. The IBE bit must be set to one for both ETPUB[18] and GPIO[165] when configured as inputs.
- 3 The weak pull up/down selection at reset for the ETPUB[18] pin is determined by the WKPCFG pin.

Figure 6-98. MPC5554: ETPUB[18]\_PCSA[3]\_GPIO[165] Pad Configuration Register (SIU\_PCR165)

See Table 6-15 for bit field definitions.

## 6.3.1.12.87 Pad Configuration Register 166 (SIU\_PCR166)

## NOTE

The MPC5553 does not implement PCR146-178. Treat those registers as reserved space.

The  SIU\_PCR166  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the ETPUB[19]\_PCSA[4]\_GPIO[166] pin. Both the input and output channel of ETPUB[19] are connected to the pin.

## SIU\_BASE+0x18C

<!-- image -->

- 1 The OBE bit must be set to one for both ETPUB[19] and GPIO[166] when configured as outputs. When configured as PCS, the OBE bit has no affect.
- 2 When configured as ETPUB or GPIO outputs, or configured as PCS, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. The IBE bit must be set to one for both ETPUB[19] and GPIO[166] when configured as inputs.
- 3 The weak pull up/down selection at reset for the ETPUB[19] pin is determined by the WKPCFG pin.

Figure 6-99. ETPUB[19]\_PCSA[4]\_GPIO[166] Pad Configuration Register (SIU\_PCR166)

See Table 6-15 for bit field definitions.

## 6.3.1.12.88 MPC5554: Pad Configuration Register 167 - 178 (SIU\_PCR167 - SIU\_PCR178)

## NOTE

The MPC5553 does not implement PCR146-178. Treat those registers as reserved space.

The  SIU\_PCR167  -  SIU\_PCR178  registers  control  the  pin  function,  direction,  and  static  electrical attributes of the ETPUB[20:31]\_GPIO[167:178] pins. Both the inputs and outputs of ETPUB[20:31] are connected to these pins.

## SIU\_BASE+0x18E - SIU\_BASE+0x1A4 (12)

<!-- image -->

- 1 The OBE bit must be set to one for both ETPUB[20:31] and GPIO[167:178] when configured as outputs.
- 2 When configured as ETPUB or GPIO outputs, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. The IBE bit must be set to one for both ETPUB[20:31] and GPIO[167:178] when configured as inputs.
- 3 The weak pull up/down selection at reset for the ETPUB[20:31] pins is determined by the WKPCFG pin.

Figure 6-100. MPC5554: ETPUB[20:31]\_GPIO[167:178] Pad Configuration Register (SIU\_PCR167 - SIU\_PCR178)

See Table 6-15 for bit field definitions.

## 6.3.1.12.89 Pad Configuration Register 179 - 188 (SIU\_PCR179 - SIU\_PCR188)

The  SIU\_PCR179  -  SIU\_PCR188  registers  control  the  pin  function,  direction,  and  static  electrical attributes of the EMIOS[0:9]\_ETPUA[0:9]\_GPIO[179:188] pins. Both the input and output functions of EMIOS[0:9], and only the output channels of ETPUA[0:9] are connected to pins.

## SIU\_BASE+0x1A6 - SIU\_BASE+0x1B8 (10)

<!-- image -->

- 1 The OBE bit must be set to one for both EMIOS[0:9] and GPIO[179:188] when configured as outputs.
- 2 When configured as EMIOS, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption.The IBE bit must be set to one for both EMIOS[0:9] and GPIO[179:188] when configured as inputs.
- 3 The weak pull up/down selection at reset for the EMIOS[0:9] pins is determined by the WKPCFG pin.

Figure 6-101. EMIOS[0:9]\_ETPUA[0:9]\_GPIO[179:188] Pad Configuration Register (SIU\_PCR179 - SIU\_PCR188)

See Table 6-15 for bit field definitions.

## 6.3.1.12.90 Pad Configuration Register 189 - 190 (SIU\_PCR189 - SIU\_PCR190)

The  SIU\_PCR189  -  SIU\_PCR190  registers  control  the  pin  function,  direction,  and  static  electrical attributes of the EMIOS[10:11]\_GPIO[189:190]  pins.  Both  the input and output functions of EMIOS[10:11] are connected to pins.

## SIU\_BASE+0x1BA - SIU\_BASE+0x1BC (2)

<!-- image -->

- 1 The OBE bit must be set to one for both EMIOS[10:11] and GPIO[189:190] when configured as outputs.
- 2 When configured as EMIOS or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. The IBE bit must be set to one for both EMIOS[10:11] and GPIO[189:190] when configured as inputs.
- 3 The weak pull up/down selection at reset for the EMIOS[10:11] pins is determined by the WKPCFG pin.

Figure 6-102. EMIOS[10:11]\_GPIO[189:190] Pad Configuration Register (SIU\_PCR189 - SIU\_PCR190)

See Table 6-15 for bit field definitions.

## 6.3.1.12.91 Pad Configuration Register 191 (SIU\_PCR191)

The  SIU\_PCR191  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the EMIOS[12]\_SOUTC\_GPIO[191] pin. Only the output of EMIOS[12] is connected to the pin.

## SIU\_BASE+0x1BE

<!-- image -->

- 1 The OBE bit must be set to one for GPIO[191] when configured as an output.
- 2 When configured as EMIOS or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. The IBE bit must be set to one for GPIO[191] when configured as an input.
- 3 The weak pull up/down selection at reset for the EMIOS[12] pin is determined by the WKPCFG pin.

Figure 6-103. EMIOS[12]\_SOUTC\_GPIO[191] Pad Configuration Register (SIU\_PCR191)

See Table 6-15 for bit field definitions.

## 6.3.1.12.92 Pad Configuration Register 192 (SIU\_PCR192)

The  SIU\_PCR191  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the EMIOS[13]\_SOUTD\_GPIO[192] pin. Only the output of EMIOS[13] is connected to the pin.

## SIU\_BASE+0x1C0

<!-- image -->

- 1 The OBE bit must be set to one for GPIO[192] when configured as an output.
- 2 When configured as EMIOS or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. The IBE bit must be set to one for GPIO[192] when configured as an input.
- 3 The weak pull up/down selection at reset for the EMIOS[13] pin is determined by the WKPCFG pin.

Figure 6-104. EMIOS[13]\_SOUTD\_GPIO[192] Pad Configuration Register (SIU\_PCR192)

See Table 6-15 for bit field definitions.

## 6.3.1.12.93 Pad Configuration Register 193 - 194 (SIU\_PCR193 - SIU\_PCR194)

The  SIU\_PCR193  -  SIU\_PCR194  registers  control  the  pin  function,  direction,  and  static  electrical attributes of the EMIOS[14:15]\_IRQ[0:1]\_GPIO[193:194] pins. Only the output functions of EMIOS[14:15] are connected to pins.

## SIU\_BASE+0x1C2 - SIU\_BASE+0x1C4 (2)

<!-- image -->

- 1 The OBE bit must be set to one for GPIO[193:194] when configured as outputs.
- 2 When configured as EMIOS or IRQ or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. The IBE bit must be set to one for GPIO[193:194] when configured as inputs.
- 3 The weak pull up/down selection at reset for the EMIOS[14:15] pins is determined by the WKPCFG pin.

Figure 6-105. EMIOS[14:15]\_IRQ[0:1]\_GPIO[193:194] Pad Configuration Register (SIU\_PCR193 - SIU\_PCR194)

See Table 6-15 for bit field definitions.

## 6.3.1.12.94 Pad Configuration Register 195 - 202 (SIU\_PCR195 - SIU\_PCR202)

MPC5553 : The SIU\_PCR195 - SIU\_PCR202 registers control the pin function, direction, and static electrical attributes of the EMIOS[16:23]\_ETPUB[0:7]\_GPIO[195:202] pins. Both the input and output functions of EMIOS[16:23] are connected to pins. The secondary function, ETPUB[0:7] is unavailable.

MPC5554 :  The  SIU\_PCR195  -  SIU\_PCR202  registers  control  the  pin  function,  direction,  and  static electrical attributes of the EMIOS[16:23]\_ETPUB[0:7]\_GPIO[195:202] pins. Both the input and output functions of EMIOS[16:23], and only the output channels of ETPUB[0:7] are connected to pins.

## SIU\_BASE+0x1C6 - SIU\_BASE+0x1D4 (8)

<!-- image -->

- 1 The OBE bit must be set to one for both EMIOS[16:23] and GPIO[195:202] when configured as outputs.
- 2 When configured as EMIOS or eTPU, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption.The IBE bit must be set to one for both EMIOS[16:23] and GPIO[195:202] when configured as inputs.
- 3 The weak pull up/down selection at reset for the EMIOS[0:9] pins is determined by the WKPCFG pin.

Figure 6-106. EMIOS[16:23]\_ETPUB[0:7]\_GPIO[195:202] Pad Configuration Register (SIU\_PCR195 - SIU\_PCR202)

See Table 6-15 for bit field definitions.

## 6.3.1.12.95 Pad Configuration Register 203 - 204 (SIU\_PCR203 - SIU\_PCR204)

The  SIU\_PCR203  -  SIU\_PCR204  registers  control  the  pin  function,  direction,  and  static  electrical attributes of the GPIO[203:204]\_EMIOS[14:15] pins. Only the output functions of EMIOS[14:15] are connected to these pins. These pins are named GPIO[203:204] because other balls are already named EMIOS[14:15]. The primary function of these pins is EMIOS, however, out of reset, they are configured for GPIO use. These pins are not affected by WKPCFG (see Section 2.3.1.7, 'Weak Pull Configuration / GPIO (WKPCFG\_GPIO213)).

## SIU\_BASE+0x1D6 - SIU\_BASE+0x1D8 (2)

<!-- image -->

- 1 MPC5554 only: The PA bit should be set to one for EMIOS and cleared to zero when used as GPIO.
- 2 When configured as EMIOS the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 3 When configured as EMIOS or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.

Figure 6-107. GPIO[203:204]\_EMIOS[14:15] Pad Configuration Register (SIU\_PCR203 - SIU\_PCR204)

See Table 6-15 for bit field definitions.

## 6.3.1.12.96 Pad Configuration Registers 205 (SIU\_PCR205)

The SIU\_PCR205 register controls the direction and static electrical attributes of the GPIO[205] pin. This register is separate from the PCRs for GPIO[206:207] since GPIO[205] is a medium pad type with slew rate  control  and  GPIO[206:207]  are  fast  pad  types  with  drive  strength  control.  The  PA  bit  is  not implemented for this PCR since GPIO is the only pin function.

## SIU\_BASE+0x1DA

<!-- image -->

- 1 When configured as GPO, the OBE bit should be set to one.
- 2 When configured as GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. When configured as GPI, the IBE bit should be set to one. Setting the IBE bit to zero reduces power consumption.

Figure 6-108. GPIO[205] Pad Configuration Registers (SIU\_PCR205)

See Table 6-15 for bit field definitions.

## 6.3.1.12.97 Pad Configuration Registers 206 - 207 (SIU\_PCR206 - SIU\_PCR207)

The  SIU\_PCR206  -  SIU\_PCR207  registers  control  the  pin  function,  direction,  and  static  electrical attributes of the GPIO[206:207] pins. These registers are separate from the PCR for GPIO[205] since GPIO[206:207] are fast pad types with drive strength control and GPIO[205] is a medium pad type with slew rate control. The PA bit is not implemented for these PCRs since GPIO is the only pin function.

## NOTE

The  GPIO[206:7]  pins  have  the  capability  to  trigger  the  ADCs.  For  the ETRIG functionality,  these  GPIO  pins  need  to  be  set  as  GPIO  and  then select the GPIO ADC trigger in the (SIU\_ETISR) - see Section 6.3.1.15, 'eQADC Trigger Input Select Register (SIU\_ETISR).'

## SIU\_BASE+0x1DC - SIU\_BASE+0x1DE (2)

<!-- image -->

- 1 When configured as GPO, the OBE bit should be set to one.
- 2 When configured as GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. When configured as GPI, the IBE bit should be set to one. Setting the IBE bit to zero reduces power consumption.

Figure 6-109. GPIO[206:207] Pad Configuration Registers (SIU\_PCR206 - SIU\_PCR207)

See Table 6-15 for bit field definitions.

## 6.3.1.12.98 Pad Configuration Register 208 (SIU\_PCR208)

The  SIU\_PCR208  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the PLLCFG[0]\_IRQ[4]\_GPIO[208] pin.

## SIU\_BASE+0x1E0

<!-- image -->

- 1 The PLLCFG function applies only during reset when the RSTCFG pin is asserted during reset. The PA field should be set to 0b10 for IRQ[4] and set to 0b00 for GPIO[208].
- 2 When configured as IRQ, the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 3 When configured as IRQ or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.
- 4 When configured as IRQ, the HYS bit should be set to one.

## Figure 6-110. PLLCFG[0]\_IRQ[4]\_GPIO[208] Pad Configuration Register (SIU\_PCR208)

See Table 6-15 for bit field definitions.

## 6.3.1.12.99 Pad Configuration Register 209 (SIU\_PCR209)

The  SIU\_PCR209  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the PLLCFG[1]\_IRQ[5]\_SOUTD\_GPIO[209] pins.

## SIU\_BASE+0x1E2

<!-- image -->

- 1 The PLLCFG function applies only during reset when the RSTCFG pin is asserted during reset. The PA field should be set to 0b010 for IRQ[5], 0b100 for SOUTD, and 0b000 for GPIO[209].
- 2 When configured as IRQ, the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 3 When configured as IRQ or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.
- 4 When configured as IRQ, the HYS bit should be set to one.

## Figure 6-111. PLLCFG[1]\_IRQ[5]\_SOUTD\_GPIO[209] Pad Configuration Register (SIU\_PCR209)

See Table 6-15 for bit field definitions.

## 6.3.1.12.100Pad Configuration Register 210 (SIU\_PCR210)

The  SIU\_PCR210  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the RSTCFG\_GPIO[210] pin.

## SIU\_BASE+0x1E4

<!-- image -->

- 1 RSTCFG function is only applicable during reset. The PA bit must be set to zero for GPIO operation
- 2 When configured as GPO, the OBE bit should be set to one.
- 3 When configured as GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. When configured as GPI, the IBE bit should be set to one.

## Figure 6-112. RSTCFG\_GPIO[210] Pad Configuration Register (SIU\_PCR210)

See Table 6-15 for bit field definitions.

## 6.3.1.12.101Pad Configuration Register 211 - 212 (SIU\_PCR211 - SIU\_PCR212)

The  SIU\_PCR211  -  SIU\_PCR212  registers  control  the  pin  function,  direction,  and  static  electrical attributes of the BOOTCFG[0:1]\_IRQ[2:3]\_GPIO[211:212] pins.

## SIU\_BASE+0x1E6 - SIU\_BASE+0x1E8 (2)

<!-- image -->

- 1 The BOOTCFG function applies only during reset when the RSTCFG pin is asserted during reset. The PA field should be set to 0b10 for IRQ[2:3] and set to 0b00 for GPIO[211:212].
- 2 When configured as IRQ, the OBE bit has no affect. When configured as GPO, the OBE bit should be set to one.
- 3 When configured as IRQ or GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. Setting the IBE bit to zero reduces power consumption. When configured as GPI, the IBE bit should be set to one.
- 4 When configured as IRQ, the HYS bit should be set to one.

Figure 6-113. BOOTCFG[0:1]\_IRQ[2:3]\_GPIO[211:212] Pad Configuration Register (SIU\_PCR211 - SIU\_PCR212)

See Table 6-15 for bit field definitions.

## 6.3.1.12.102Pad Configuration Register 213 (SIU\_PCR213)

The  SIU\_PCR213  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the WKPCFG\_GPIO[213] pin.

## SIU\_BASE+0x1EA

<!-- image -->

- 1 WKPCFG function is only applicable during reset. The PA bit must be set to zero for GPIO operation
- 2 When configured as GPO, the OBE bit should be set to one.
- 3 When configured as GPO, the IBE bit may be set to one to reflect the pin state in the corresponding GPDI register. When configured as GPI, the IBE bit should be set to one.

Figure 6-114. WKPCFG\_GPIO[213] Pad Configuration Register (SIU\_PCR213)

See Table 6-15 for bit field definitions.

## 6.3.1.12.103Pad Configuration Register 214 (SIU\_PCR214)

The SIU\_PCR214 register controls the enabling/disabling and drive strength of the ENGCLK pin. The ENGCLK pin is enabled and disabled by setting and clearing the OBE bit. The ENGCLK pin is enabled during reset.

## SIU\_BASE+0x1EC

Figure 6-115. ENGLCK Pad Configuration Register (SIU\_PCR214)

<!-- image -->

See Table 6-15 for bit field definitions.

## 6.3.1.12.104Pad Configuration Register 215 (SIU\_PCR215)

The  SIU\_PCR215  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the AN[12]\_MA[0]\_SDS pin.

## SIU\_BASE+0x1EE

<!-- image -->

|        | 0   | 1   | 2   | 3   | 4   | 5   | 6   | 7   | 8   | 9   | 10   | 11   | 12   | 13   | 14   | 15   |
|--------|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|------|------|------|------|------|------|
| R      | 0   | 0   | 0   | 0   | PA  | 1   | 0   | 0   | 0   | 0   | ODE  | 0    | SRC  |      | 0    | 0    |
| W      |     |     |     |     |     |     |     |     |     |     |      |      |      |      |      |      |
| RESET: | 0   | 0   | 0   | 0   | 1   | 1   | 0   | 0   | 0   | 0   | 0    | 0    | 0    | 0    | 0    | 0    |

- 1 Input and output buffers are enabled/disabled based on PA selection. Both input and output buffer disabled for AN[12] function. Output buffer only enabled for MA[0] and SDS functions.

Figure 6-116. AN[12]\_MA[0]\_SDS Pad Configuration Register (SIU\_PCR215)

See Table 6-15 for bit field definitions. The PA field for PCR215 is given in Table 6-21.

Table 6-21. PCR215 PA Field Definition

| PA Field   | Pin Function   |
|------------|----------------|
| 0b00       | SDS            |
| 0b01       | Reserved       |
| 0b10       | MA[0]          |
| 0b11       | AN[12]         |

## 6.3.1.12.105Pad Configuration Register 216 (SIU\_PCR216)

The  SIU\_PCR216  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the AN[13]\_MA[1]\_SDO pin.

## SIU\_BASE+0x1F0

<!-- image -->

|        | 0   | 1   | 2   | 3   | 4    | 5   | 6   | 7   | 8   | 9   | 10   | 11   | 12   | 13   | 14   | 15   |
|--------|-----|-----|-----|-----|------|-----|-----|-----|-----|-----|------|------|------|------|------|------|
| R      | 0   | 0   | 0   | 0   | PA 1 |     | 0   | 0   | 0   | 0   | ODE  | 0    | SRC  |      | 0    | 0    |
| W      |     |     |     |     |      |     |     |     |     |     |      |      |      |      |      |      |
| RESET: | 0   | 0   | 0   | 0   | 1    | 1   | 0   | 0   | 0   | 0   | 0    | 0    | 0    | 0    | 0    | 0    |

1 Input and output buffers are enabled/disabled based on PA selection. Both input and output buffer disabled for AN[13] function. Output buffer only enabled for MA[1] and SDO functions.

## Figure 6-117. AN[13]\_MA[1]\_SDO Pad Configuration Register (SIU\_PCR216)

See Table 6-15 for bit field definitions. The PA field for PCR216 is given in Table 6-22.

Table 6-22. PCR216 PA Field Definition

| PA Field   | Pin Function   |
|------------|----------------|
| 0b00       | SDO            |
| 0b01       | Reserved       |
| 0b10       | MA[1]          |
| 0b11       | AN[13]         |

## 6.3.1.12.106Pad Configuration Register 217 (SIU\_PCR217)

The  SIU\_PCR217  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the AN[14]\_MA[2]\_SDI pin.

## SIU\_BASE+0x1F2

<!-- image -->

- 1 Input and output buffers are enabled/disabled based on PA selection. Both input and output buffer disabled for AN[14] function. Output buffer only enabled for MA[2] function and input buffer only enabled for SDI functions.
- 2 The WPE bit should be set to zero when configured as an analog input or MA[2], and set to one when configured as SDI.
- 3 The WPS bit should be set to one when configured as SDI.

## Figure 6-118. AN[14]\_MA[2]\_SDI Pad Configuration Register (SIU\_PCR217)

See Table 6-15 for bit field definitions. The PA field for PCR217 is given in Table 6-23.

Table 6-23. PCR217 PA Field Definition

| PA Field   | Pin Function   |
|------------|----------------|
| 0b00       | SDI            |
| 0b01       | Reserved       |
| 0b10       | MA[2]          |
| 0b11       | AN[14]         |

## 6.3.1.12.107Pad Configuration Register 218 (SIU\_PCR218)

The  SIU\_PCR218  register  controls  the  pin  function,  direction,  and  static  electrical  attributes  of  the AN[15]\_FCK pin.

## SIU\_BASE+0x1F4

<!-- image -->

- 1 Input and output buffers are enabled/disabled based on PA selection. Both input and output buffer disabled for AN[15] function. Output buffer only enabled for FCK function.

Figure 6-119. AN[15]\_FCK Pad Configuration Register (SIU\_PCR218)

See Table 6-15 for bit field definitions. The PA field for PCR218 is given in Table 6-24.

Table 6-24. PCR218 PA Field Definition

| PA Field   | Pin Function   |
|------------|----------------|
| 0b0        | FCK            |
| 0b1        | AN[15]         |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## 6.3.1.12.108Pad Configuration Register 219 (SIU\_PCR219)

The SIU\_PCR219 register controls the drive strength of the MCKO pin.

## SIU\_BASE+0x1F6

Figure 6-120. MCKO Pad Configuration Register (SIU\_PCR219)

<!-- image -->

See Table 6-15 for bit field definitions.

## 6.3.1.12.109Pad Configuration Register 220 - 223 (SIU\_PCR220 - SIU\_PCR223)

The SIU\_PCR220 - SIU\_PCR223 registers control the drive strength of the MDO[0:3] pins.

SIU\_BASE+0x1F8 -SIU\_BASE+0x1FE (4)

Figure 6-121. MDO[0:3] Pad Configuration Register (SIU\_PCR220 - SIU\_PCR223)

<!-- image -->

See Table 6-15 for bit field definitions.

## 6.3.1.12.110Pad Configuration Register 224 - 225 (SIU\_PCR224 - SIU\_PCR225)

The SIU\_PCR224 - SIU\_PCR225 registers control the drive strength of the MSEO[0:1] pins.

## SIU\_BASE+0x200 -SIU\_BASE+0x202 (2)

Figure 6-122. MSEO[0:1] Pad Configuration Register (SIU\_PCR224 - SIU\_PCR225)

<!-- image -->

See Table 6-15 for bit field definitions.

## 6.3.1.12.111Pad Configuration Register 226 (SIU\_PCR226)

The SIU\_PCR226 register controls the drive strength of the RDY pin.

## SIU\_BASE+0x204

Figure 6-123. RDY Pad Configuration Register (SIU\_PCR226)

<!-- image -->

See Table 6-15 for bit field definitions.

## 6.3.1.12.112Pad Configuration Register 227 (SIU\_PCR227)

The SIU\_PCR227 register controls the drive strength of the EVTO pin.

SIU\_BASE+0x206

Figure 6-124. EVTO Pad Configuration Register (SIU\_PCR227)

<!-- image -->

See Table 6-15 for bit field definitions.

## 6.3.1.12.113Pad Configuration Register 228 (SIU\_PCR228)

The SIU\_PCR228 register controls the drive strength of the TDO pin.

## SIU\_BASE+0x208

Figure 6-125. TDO Pad Configuration Register (SIU\_PCR228)

<!-- image -->

See Table 6-15 for bit field definitions.

## 6.3.1.12.114Pad Configuration Register 229 (SIU\_PCR229)

The SIU\_PCR229 register controls the enabling/disabling and drive strength of the CLKOUT pin. The CLKOUT pin is enabled and disabled by setting and clearing the OBE bit. The CLKOUT pin is enabled during reset.

## SIU\_BASE+0x20A

Figure 6-126. CLKOUT Pad Configuration Register (SIU\_PCR229)

<!-- image -->

See Table 6-15 for bit field definitions.

## 6.3.1.12.115Pad Configuration Register 230 (SIU\_PCR230)

The SIU\_PCR230 register controls the slew rate of the RSTOUT pin.

## SIU\_BASE+0x20C

Figure 6-127. RSTOUT Pad Configuration Register (SIU\_PCR230)

<!-- image -->

See Table 6-15 for bit field definitions.

## 6.3.1.13 GPIO Pin Data Output Registers 0-213 (SIU\_GPDO n )

The definition of the 8-bit SIU\_GPDO n registers, with each register specifying the drive data for a single GPIO  pin,  is  given  in  Figure 6-128.  The n notation  in  the  name  of  the  214  SIU\_GPDO n registers corresponds to the pins with the same GPIO pin numbers. For example, PDO0 is the pin data output bit for  the  CS0\_GPIO0 pin and is found in SIU\_GPDO0, and PDO213 is the pin data output bit for the WKPCFG\_GPIO213 pin and is found in SIU\_GPDO213. The GPDO address for a particular pin is equal to the GPIO pin number with an offset of SIU\_BASE + 0x600.

The SIU\_GPDO  registers are written to by software to drive data out on the external GPIO pin. Each n register drives a single external GPIO pin, which allows the state of the pin to be controlled independently from other GPIO pins. Writes to the SIU\_GPDO n registers have no effect on pin states if the pins are configured as inputs by the associated Pad Configuration Registers. The SIU\_GPDO n register values are automatically driven to the GPIO pins without software update if the direction of the GPIO pins is changed from input to output.

Writes to the SIU\_GPDO n registers have no effect on the state of the corresponding pins when the pins are configured for their primary function by the corresponding PCR.

Figure 6-128. GPIO Pin Data Output Register 0-213 (SIU\_GPDO n )

<!-- image -->

Table 6-25. SIU\_GPDO n Field Descriptions

| Name   | Description                                                                                                                                                                                                                                                                                                                            |
|--------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| PDO n  | Pin data out. Stores the data to be driven out on the external GPIO pin associated with the register. If the register is read, it will return the value written. 0 V OL is driven on the external GPIO pin when the pin is configured as an output. 1 V OH is driven on the external GPIO pin when the pin is configured as an output. |

## 6.3.1.14 GPIO Pin Data Input Registers 0-213 (SIU\_GPDI n )

The definition of the 8-bit SIU\_GPDI n registers, with each register specifying the drive data for a single GPIO pin, is given in Figure 6-129. The n notation in the name of the 178 (MPC5553) or 214 (MPC5554) SIU\_GPDI  registers corresponds to the pins with the same GPIO pin numbers. For example, PDI0 is the n pin data input bit for the CS0\_GPIO0 pin and is found in SIU\_GPDI0, and PDI213 is the pin data input bit for the WKPCFG\_GPIO213 pin and is found in SIU\_GPDI213. The GPDI address for a particular pin is equal to the GPIO pin number with an offset of SIU\_BASE + 0x800. Gaps exist in this memory space where the pin is not available in the package.

The SIU\_GPDI  registers are read-only registers that allow software to read the input state of an external n GPIO pin. Each register  represents  the  input  state  of  a  single  external  GPIO  pin.  If  the  GPIO  pin  is configured as an output, and the input buffer enable (IBE) bit is set in the associated pad configuration register, the SIU\_GPDI n register reflects the actual state of the output pin.

Figure 6-129. GPIO Pin Data Input Register 0-213 (SIU\_GPDI n )

<!-- image -->

Table 6-26. SIU\_GPDI n Field Description

| Name   | Description                                                                                                                                                                                                                        |
|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| PDI n  | Pin data in. This bit reflects the input state on the external GPIO pin associated with the register. If PCR n [IBE] = 1, then: 0 Signal on pin is less than or equal to V IL . 1 Signal on pin is greater than or equal to V IH . |

## 6.3.1.15 eQADC Trigger Input Select Register (SIU\_ETISR)

The  SIU\_ETISR  selects  the  source  for  the  eQADC  trigger  inputs.  The  eQADC  trigger  numbers  0-5 specified by TSEL(0-5) correspond to CFIFO numbers 0-5. To calculate the CFIFO number that each trigger  is  connected  to,  divide  the  DMA  channel  number  by  2.    So,  for  example,  eQADC  CFIFO  1 (connected to DMA channel 2) can be triggered by eTPUA[31], eMIOS[11] or ETRIG[1]. To select a trigger, the corresponding TSEL must be initialized.

When an eQADC trigger is connected,  the timer output is connected to the eQADC CFIFO trigger input. To trigger the eQADC, the eTPU output must change to the state that the eQADC recognizes as a trigger. Bear in mind there are rising or falling edges, and low or high gated trigger types, so it might be possible to have the eQADC trigger immediately if desired.

Table 6-27. Trigger Interconnections

|   TSEL Field (Trigger Number) |   eQADC CFIFO |   EQADC DMA Channel | eTPUA Channel   | eMIOS Channel   | ETRIG Input   |
|-------------------------------|---------------|---------------------|-----------------|-----------------|---------------|
|                             0 |             0 |                   0 | eTPUA30         | eMIOS10         | ETRIG0        |
|                             1 |             1 |                   2 | eTPUA31         | eMIOS11         | ETRIG1        |
|                             2 |             2 |                   4 | eTPUA29         | eMIOS15         | ETRIG0        |
|                             3 |             3 |                   6 | eTPUA28         | eMIOS14         | ETRIG1        |
|                             4 |             4 |                   8 | eTPUA27         | eMIOS13         | ETRIG0        |
|                             5 |             5 |                  10 | eTPUA26         | eMIOS12         | ETRIG1        |

Figure 6-130. eQADC Trigger Input Select Register (SIU\_ETISR)

| R        | 0 TSEL5      | 1            | 2 3 TSEL4    | 2 3 TSEL4    | 4 5 TSEL3    | 4 5 TSEL3    | 6 TSEL2      | 7            | 8 TSEL1      | 9            | 10 11 TSEL0   | 10 11 TSEL0   | 12 0         | 13           | 0            | 14 0         | 15 0         |
|----------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|---------------|---------------|--------------|--------------|--------------|--------------|--------------|
| W Reset  | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0             | 0             | 0            | 0            |              | 0            | 0            |
| Reg Addr | Base + 0x900 | Base + 0x900 | Base + 0x900 | Base + 0x900 | Base + 0x900 | Base + 0x900 | Base + 0x900 | Base + 0x900 | Base + 0x900 | Base + 0x900 | Base + 0x900  | Base + 0x900  | Base + 0x900 | Base + 0x900 | Base + 0x900 | Base + 0x900 | Base + 0x900 |
|          | 16           | 17           | 18           | 19           | 20           | 21           | 22           | 23           | 24           | 25           | 26            | 27            | 28           | 29           |              | 30           | 31           |
| R        | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0             | 0             | 0            | 0            |              | 0            | 0            |
| W        |              |              |              |              |              |              |              |              |              |              |               |               |              |              |              |              |              |
| Reset    | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0             | 0             | 0            |              | 0            | 0            | 0            |
| Reg Addr | Base + 0x900 | Base + 0x900 | Base + 0x900 | Base + 0x900 | Base + 0x900 | Base + 0x900 | Base + 0x900 | Base + 0x900 | Base + 0x900 | Base + 0x900 | Base + 0x900  | Base + 0x900  | Base + 0x900 | Base + 0x900 | Base + 0x900 | Base + 0x900 | Base + 0x900 |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 6-28. SIU\_ETISR Field Descriptions

| Bits   | Name        | Description                                                                                                                           |
|--------|-------------|---------------------------------------------------------------------------------------------------------------------------------------|
| 0-1    | TSEL5 [0:1] | eQADC trigger input select 5. Specifies the input for eQADC trigger 5. 00 GPIO207 01 ETPUA26 channel 10 EMIOS12 channel 11 ETRIG1 pin |
| 2-3    | TSEL4 [0:1] | eQADC trigger input select 4. Specifies the input for eQADC trigger 4. 00 GPIO206 01 ETPUA27 channel 10 EMIOS13 channel 11 ETRIG0 pin |
| 4-5    | TSEL3 [0:1] | eQADC trigger input select 3. Specifies the input for eQADC trigger 3. 00 GPIO207 01 ETPUA28 channel 10 EMIOS14 channel 11 ETRIG1 pin |
| 6-7    | TSEL2 [0:1] | eQADC trigger input select 2. Specifies the input for eQADC trigger 2 00 GPIO206 01 ETPUA29 channel 10 EMIOS15 channel 11 ETRIG0 pin  |
| 8-9    | TSEL1 [0:1] | eQADC trigger input select 1. Specifies the input for eQADC trigger 1 00 GPIO207 01 ETPUA31 channel 10 EMIOS11 channel 11 ETRIG1 pin  |
| 10-11  | TSEL0 [0:1] | eQADC trigger input select 0. Specifies the input for eQADC trigger 0 00 GPIO206 01 ETPUA30 channel 10 EMIOS10 channel 11 ETRIG0 pin  |
| 12-31  | -           | Reserved.                                                                                                                             |

## 6.3.1.16 External IRQ Input Select Register (SIU\_EIISR)

The SIU\_EIISR selects the source for the external interrupt/DMA inputs.

Figure 6-131. External IRQ Input Select Register 1 (SIU\_EIISR)

|          | 0            | 1            | 2            | 3            | 4            | 5            | 6            | 7            | 8            | 9            | 10           | 11           | 12           | 13           | 14           | 15           |
|----------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|
| R        | ESEL15       | ESEL15       | ESEL14       | ESEL14       | ESEL13       | ESEL13       | ESEL12       | ESEL12       | ESEL11       | ESEL11       | ESEL10       | ESEL10       | ESEL9        | ESEL9        | ESEL8        | ESEL8        |
| W        |              |              |              |              |              |              |              |              |              |              |              |              |              |              |              |              |
| Reset    | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            |
| Reg Addr | Base + 0x904 | Base + 0x904 | Base + 0x904 | Base + 0x904 | Base + 0x904 | Base + 0x904 | Base + 0x904 | Base + 0x904 | Base + 0x904 | Base + 0x904 | Base + 0x904 | Base + 0x904 | Base + 0x904 | Base + 0x904 | Base + 0x904 | Base + 0x904 |
|          | 16           | 17           | 18           | 19           | 20           | 21           | 22           | 23           | 24           | 25           | 26           | 27           | 28           | 29           | 30           | 31           |
| R        | ESEL7        | ESEL7        | ESEL6        | ESEL6        | ESEL5        | ESEL5        | ESEL4        | ESEL4        | ESEL3        | ESEL3        | ESEL2        | ESEL2        | ESEL1        | ESEL1        | ESEL0        | ESEL0        |
| W        |              |              |              |              |              |              |              |              |              |              |              |              |              |              |              |              |
| Reset    | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            |
| Reg Addr | Base + 0x904 | Base + 0x904 | Base + 0x904 | Base + 0x904 | Base + 0x904 | Base + 0x904 | Base + 0x904 | Base + 0x904 | Base + 0x904 | Base + 0x904 | Base + 0x904 | Base + 0x904 | Base + 0x904 | Base + 0x904 | Base + 0x904 | Base + 0x904 |

Table 6-29. SIU\_EIISR Field Descriptions

| Bits   | Name         | Description                                                                                                                                                                                                |
|--------|--------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-1    | ESEL15 [0:1] | External IRQ input select 15. Specifies the input for IRQ 15. 00 IRQ15 pin 01 DSPI_B15 serialized input (EMIOS12 pin) 10 DSPI_C0 serialized input (ETPUA12 pin) 11 DSPI_D1 serialized input (ETPUA20 pin)  |
| 2-3    | ESEL14 [0:1] | External IRQ input select 14. Specifies the input for IRQ14. 00 IRQ14 pin 01 DSPI_B14 serialized input (EMIOS13 pin) 10 DSPI_C15 serialized input (ETPUA11 pin) 11 DSPI_D0 serialized input (ETPUA21 pin)  |
| 4-5    | ESEL13 [0:1] | External IRQ input select 13. Specifies the input for IRQ13. 00 IRQ13 pin 01 DSPI_B13 serialized input (ETPUA24 pin) 10 DSPI_C14 serialized input (ETPUA10 pin) 11 DSPI_D15 serialized input (ETPUA24 pin) |
| 6-7    | ESEL12 [0:1] | External IRQ input select 12. Specifies the input for IRQ12. 00 IRQ12 pin 01 DSPI_B12 serialized input (ETPUA25 pin) 10 DSPI_C13 serialized input (ETPUA9 pin) 11 DSPI_D14 serialized input (ETPUA25 pin)  |
| 8-9    | ESEL11 [0:1] | External IRQ input select 11. Specifies the input for IRQ11. 00 IRQ11 pin 01 DSPI_B11 serialized input (ETPUA26 pin) 10 DSPI_C12 serialized input (ETPUA8 pin) 11 DSPI_D13 serialized input (ETPUA26 pin)  |
| 10-11  | ESEL10 [0:1] | External IRQ input select 10. Specifies the input for IRQ10. 00 IRQ10 pin 01 DSPI_B10 serialized input (ETPUA27 pin) 10 DSPI_C11 serialized input (ETPUA7 pin) 11 DSPI_D12 serialized input (ETPUA27 pin)  |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 6-29. SIU\_EIISR Field Descriptions (continued)

| Bits   | Name        | Description                                                                                                                                                                                                                                                                                                        |
|--------|-------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 12-13  | ESEL9 [0:1] | External IRQ input select 9. Specifies the input for IRQ9. 00 IRQ9 pin 01 DSPI_B9 serialized input (ETPUA28 pin) 10 DSPI_C10 serialized input (ETPUA6 pin) 11 DSPI_D11 serialized input (ETPUA28 pin)                                                                                                              |
| 14-15  | ESEL8 [0:1] | External IRQ input select 8. Specifies the input for IRQ8. 00 IRQ8 pin 01 DSPI_B8 serialized input (ETPUA29 pin) 10 DSPI_C9 serialized input (ETPUA5 pin) 11 DSPI_D10 serialized input (ETPUA29 pin)                                                                                                               |
| 16-17  | ESEL7 [0:1] | External IRQ input select 7. Specifies the input for IRQ7. 00 IRQ7 pin 01 DSPI_B7 serialized input (ETPUA16 pin) 10 DSPI_C8 serialized input (ETPUA4 pin) 11 DSPI_D9 serialized input (EMIOS12 pin)                                                                                                                |
| 18-19  | ESEL6 [0:1] | External IRQ input select 6. Specifies the input for IRQ6. 00 IRQ6 pin (for MPC5553, 0b00 is Reserved) 01 DSPI_B6 serialized input (ETPUA17 pin) 10 DSPI_C7 serialized input (ETPUA3 pin) 11 DSPI_D8 serialized input (EMIOS13 pin) Note: IRQ6 functions only on the MPC5554. It is not functional on the MPC5553. |
| 20-21  | ESEL5 [0:1] | External IRQ input select 5. Specifies the input for IRQ5. 00 IRQ5 pin 01 DSPI_B5 serialized input (ETPUA18 pin) 10 DSPI_C6 serialized input (ETPUA2 pin) 11 DSPI_D7 serialized input (EMIOS10 pin)                                                                                                                |
| 22-23  | ESEL4 [0:1] | External IRQ input select 4. Specifies the input for IRQ4. 00 IRQ4 pin 01 DSPI_B4 serialized input (ETPUA19 pin) 10 DSPI_C5 serialized input (ETPUA1 pin) 11 DSPI_D6 serialized input (EMIOS11 pin)                                                                                                                |
| 24-25  | ESEL3 [0:1] | External IRQ input select 3. Specifies the input for IRQ3. 00 IRQ3 pin 01 DSPI_B3 serialized input (ETPUA20 pin) 10 DSPI_C4 serialized input (ETPUA0 pin) 11 DSPI_D5 serialized input (ETPUA16 pin)                                                                                                                |
| 26-27  | ESEL2 [0:1] | External IRQ input select 2. Specifies the input for IRQ2. 00 IRQ2 pin 01 DSPI_B2 serialized input (ETPUA21 pin) 10 DSPI_C3 serialized input (ETPUA15 pin) 11 DSPI_D4 serialized input (ETPUA17 pin)                                                                                                               |

Table 6-29. SIU\_EIISR Field Descriptions (continued)

| Bits   | Name        | Description                                                                                                                                                               |
|--------|-------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 28-29  | ESEL1 [0:1] | External IRQ input select 1. Specifies the input for IRQ1. 00 IRQ1 pin 01 DSPI_B1 serialized input (EMIOS10 pin) 10 DSPI_C2 serialized input (ETPUA14 pin) 11 EMIOS15 pin |
| 30-31  | ESEL0 [0:1] | External IRQ input select 0. Specifies the input for IRQ0. 00 IRQ0 pin 01 DSPI_B0 serialized input (EMIOS11 pin) 10 DSPI_C1 serialized input (ETPUA5 pin) 11 EMIOS14 pin  |

## 6.3.1.17 DSPI Input Select Register (SIU\_DISR)

The SIU\_DISR specifies the source of each DSPI data input, slave select, clock input, and trigger input to allow serial and parallel chaining of the DSPI modules. For MPC5553, see Figure 6-132. For MPC5554 see Figure 6-133.

Figure 6-132. MPC5553 DSPI Input Select Register (SIU\_DISR)

<!-- image -->

Figure 6-133. MPC5554 DSPI Input Select Register (SIU\_DISR)

|          | 0            | 1            | 2            | 3            | 4            | 5            | 6            | 7            | 8            | 9            | 10           | 11           | 12           | 13           | 14           | 15           |
|----------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|
| R        | SINSELA      | SINSELA      | SSSELA       | SSSELA       | SCKSELA      | SCKSELA      | TRIGSELA     | TRIGSELA     | SINSELB      | SINSELB      | SSSELB       | SSSELB       | SCKSELB      | SCKSELB      | TRIGSELB     | TRIGSELB     |
| W        |              |              |              |              |              |              |              |              |              |              |              |              |              |              |              |              |
| Reset    | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            |
| Reg Addr | Base + 0x908 | Base + 0x908 | Base + 0x908 | Base + 0x908 | Base + 0x908 | Base + 0x908 | Base + 0x908 | Base + 0x908 | Base + 0x908 | Base + 0x908 | Base + 0x908 | Base + 0x908 | Base + 0x908 | Base + 0x908 | Base + 0x908 | Base + 0x908 |
|          | 16           | 17           | 18           | 19           | 20           | 21           | 22           | 23           | 24           | 25           | 26           | 27           | 28           | 29           | 30           | 31           |
| R        | SINSELC      | SINSELC      | SSSELC       | SSSELC       | SCKSELC      | SCKSELC      | TRIGSELC     | TRIGSELC     | SINSELD      | SINSELD      | SSSELD       | SSSELD       | SCKSELD      | SCKSELD      | TRIGSELD     | TRIGSELD     |
| W        |              |              |              |              |              |              |              |              |              |              |              |              |              |              |              |              |
| Reset    | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            |
| Reg Addr | Base + 0x908 | Base + 0x908 | Base + 0x908 | Base + 0x908 | Base + 0x908 | Base + 0x908 | Base + 0x908 | Base + 0x908 | Base + 0x908 | Base + 0x908 | Base + 0x908 | Base + 0x908 | Base + 0x908 | Base + 0x908 | Base + 0x908 | Base + 0x908 |

## Table 6-30. SIU\_DISR Field Descriptions

| Bits   | Name           | Description                                                                                                                                                                                       |
|--------|----------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-1    | SINSELA [0:1]  | DSPI_A data input select. Specifies the source of the DSPI_A data input. 00 SINA_GPIO94 pin 01 SOUTB 10 SOUTC 11 SOUTD Note: MPC5553: Bits 0-1 are reserved                                       |
| 2-3    | SSSELA [0:1]   | DSPI_A slave select input select. Specifies the source of the DSPI_A slave select input. 00 PCSA0_GPIO96 pin 01 PCSB0 (Master) 10 PCSC0 (Master) 11 PCSD0 (Master) MPC5553: Bits 2-3 are reserved |
| 4-5    | SCKSELA [0:1]  | DSPI_A clock input select. Specifies the source of the DSPI_A clock input. 00 SCKA_GPIO93 pin 01 SCKB (Master) 10 SCKC (Master) 11 SCKD (Master) MPC5553: Bits 4-5 are reserved                   |
| 6-7    | TRIGSELA [0:1] | DSPI_A trigger input select. Specifies the source of the DSPI_A trigger input. 00 No Trigger 01 PCSB4 10 PCSC4 11 PCSD4 MPC5553: Bits 6-7 are reserved                                            |
| 8-9    | SINSELB [0:1]  | DSPI_B data input select. Specifies the source of DSPI_B data input. 00 SINB_PCSC2_GPIO103 pin 01 SOUTA (not available for MPC5553) 10 SOUTC 11 SOUTD                                             |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 6-30. SIU\_DISR Field Descriptions (continued)

| Bits   | Name           | Description                                                                                                                                                                                            |
|--------|----------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 10-11  | SSSELB [0:1]   | DSPI_B slave select input select. Specifies the source of the DSPI_B slave select input. 00 PCSB0_PCSD2_GPIO105 pin 01 PCSA0 (Master) (not available for MPC5553) 10 PCSC0 (Master) 11 PCSD0 (Master)  |
| 12-13  | SCKSELB [0:1]  | DSPI_B clock input select. Specifies the source of the DSPI_B clock input. 00 SCKB_PCSC1_GPIO102 pin 01 SCKA (Master) (not available for MPC5553) 10 SCKC (Master) 11 SCKD (Master)                    |
| 14-15  | TRIGSELB [0:1] | DSPI_B trigger input select. Specifies the source of the DSPI_B trigger input for master or slave mode. 00 Reserved 01 PCSA4 (not available for MPC5553) 10 PCSC4 11 PCSD4                             |
| 16-17  | SINSELC [0:1]  | DSPI_C data input select. Specifies the source of the DSPI_C data input. 00 PCSA2_SINC_GPIO108 pin 01 SOUTA (not available for MPC5553) 10 SOUTB 11 SOUTD                                              |
| 18-19  | SSSELC [0:1]   | DSPI_C slave select input select. Specifies the source of the DSPI_C slave select input. 00 PCSB5_PCSC0_GPIO110 pin 01 PCSA0 (Master) (not available for MPC5553) 10 PCSB0 (Master) 11 PCSD0 (Master)  |
| 20-21  | SCKSELC [0:1]  | DSPI_C clock input select. Specifies the source of the DSPI_C clock input when in slave mode. 00 PCSB4_SCKC_GPIO109 pin 01 SCKA (Master) (not available for MPC5553) 10 SCKB (Master) 11 SCKD (Master) |
| 22-23  | TRIGSELC [0:1] | DSPI_C trigger input select. Specifies the source of the DSPI_C trigger input for master or slave mode. 00 Reserved 01 PCSA4 (not available for MPC5553) 10 PCSB4 11 PCSD4                             |
| 24-25  | SINSELD [0:1]  | DSPI_D data input select. Specifies the source of the DSPI_D data input. 00 PCSA3_SIND_GPIO99 pin 01 SOUTA (not available for MPC5553) 10 SOUTB 11 SOUTC                                               |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 6-30. SIU\_DISR Field Descriptions (continued)

| Bits   | Name           | Description                                                                                                                                                                                           |
|--------|----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 26-27  | SSSELD [0:1]   | DSPI_D slave select input select. Specifies the source of the DSPI_D slave select input. 00 PCSB1_PCSD0_GPIO106 pin 01 PCSA0 (Master) (not available for MPC5553) 10 PCSB0 (Master) 11 PCSC0 (Master) |
| 28-29  | SCKSELD [0:1]  | DSPI_D clock input select. Specifies the source of the DSPI_D clock input in slave mode. 00 PCSA2_SCKD_GPIO98 pin 01 SCKA (Master) (not available for MPC5553) 10 SCKB (Master) 11 SCKC (Master)      |
| 30-31  | TRIGSELD [0:1] | DSPI_D trigger input select. Specifies the source of the DSPI_D trigger input for master or slave mode. 00 Reserved 01 PCSA4 (not available for MPC5553) 10 PCSB4 11 PCSC4                            |

## 6.3.1.18 Chip Configuration Register (SIU\_CCR)

<!-- image -->

|          | 0            | 1            | 2            | 3            | 4            | 5            | 6            | 7            | 8            | 9            | 10           | 11           | 12           | 13           | 14           | 15           |
|----------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|
| R        | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | MATCH        | DISNEX       |
| W        |              |              |              |              |              |              |              |              |              |              |              |              |              |              |              |              |
| Reset    | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | X 1          |
| Reg Addr | Base + 0x980 | Base + 0x980 | Base + 0x980 | Base + 0x980 | Base + 0x980 | Base + 0x980 | Base + 0x980 | Base + 0x980 | Base + 0x980 | Base + 0x980 | Base + 0x980 | Base + 0x980 | Base + 0x980 | Base + 0x980 | Base + 0x980 | Base + 0x980 |
|          | 16           | 17           | 18           | 19           | 20           | 21           | 22           | 23           | 24           | 25           | 26           | 27           | 28           | 29           | 30           | 31           |
| R        | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | TEST 2       |
| W        |              |              |              |              |              |              |              |              |              |              |              |              |              |              |              |              |
| Reset    | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            |
| Reg Addr | Base + 0x980 | Base + 0x980 | Base + 0x980 | Base + 0x980 | Base + 0x980 | Base + 0x980 | Base + 0x980 | Base + 0x980 | Base + 0x980 | Base + 0x980 | Base + 0x980 | Base + 0x980 | Base + 0x980 | Base + 0x980 | Base + 0x980 | Base + 0x980 |

- 1 When system reset negates, the value in this bit depends on the censorship control word and the boot configuration bits.
- 2 This bit is reset with a power on reset.

Figure 6-134. Chip Configuration Register (SIU\_CCR)

Table 6-31. SIU\_CCR Field Descriptions

| Bits   | Name   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|--------|--------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-13   | -      | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| 14     | MATCH  | Compare register match. Holds the value of the match input signal to the SIU. The match input is asserted if the values in the SIU_CARH/SIU_CARL and SIU_CBRH/SIU_CBRL are equal. The MATCH bit is reset by the synchronous reset signal. 0 The content of SIU_CARH/SIU_CARL does not match the content of SIU_CBRH/SIU_CBRL 1 The content of SIU_CARH/SIU_CARL matches the content of SIU_CBRH/SIU_CBRL                                     |
| 15     | DISNEX | Disable Nexus. Holds the value of the Nexus disable input signal to the SIU. When system reset negates, the value in this bit depends on the censorship control word and the boot configuration bits. 0 Nexus disable input signal is negated. 1 Nexus disable input signal is asserted.                                                                                                                                                     |
| 16-30  | -      | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| 31     | TEST   | Test mode enable. Allows reads or writes to undocumented registers used only for production tests. Since these production test registers are undocumented, estimating the impact of errant accesses to them is impossible. The application should not change this bit from its negated state at reset. 0 Undocumented production test registers can not be read or written. 1 Undocumented production test registers can be read or written. |

## 6.3.1.19 External Clock Control Register (SIU\_ECCR)

The  SIU\_ECCR  controls  the  timing  relationship  between  the  system  clock  and  the  external  clocks ENGCLK and  CLKOUT.  All  bits  and  fields  in  the  SIU\_ECCR  are  read/write  and  are  reset  by  the synchronous reset signal.

Figure 6-135. External Clock Control Register (SIU\_ECCR)

<!-- image -->

|          | 0            | 1            | 2            | 3            | 4            | 5            | 6            | 7            | 8            | 9            | 10           | 11           | 12           | 13           | 14           | 15           |
|----------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|
| R        | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            |
| W        |              |              |              |              |              |              |              |              |              |              |              |              |              |              |              |              |
| Reset    | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            |
| Reg Addr | Base + 0x984 | Base + 0x984 | Base + 0x984 | Base + 0x984 | Base + 0x984 | Base + 0x984 | Base + 0x984 | Base + 0x984 | Base + 0x984 | Base + 0x984 | Base + 0x984 | Base + 0x984 | Base + 0x984 | Base + 0x984 | Base + 0x984 | Base + 0x984 |
|          | 16           | 17           | 18           | 19           | 20           | 21           | 22           | 23           | 24           | 25           | 26           | 27           | 28           | 29           | 30           | 31           |
| R        | 0            | 0            |              |              | ENGDIV       |              |              |              | 0            | 0            | 0            | 0            | EBTS         | 0            | EBDF         | EBDF         |
| W        |              |              |              |              |              |              |              |              |              |              |              |              |              |              |              |              |
| Reset    | 0            | 0            | 0            | 1            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 1            |
| Reg Addr | Base + 0x984 | Base + 0x984 | Base + 0x984 | Base + 0x984 | Base + 0x984 | Base + 0x984 | Base + 0x984 | Base + 0x984 | Base + 0x984 | Base + 0x984 | Base + 0x984 | Base + 0x984 | Base + 0x984 | Base + 0x984 | Base + 0x984 | Base + 0x984 |

Table 6-32. SIU\_ECCR Field Descriptions

| Bits   | Name         | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|--------|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-17   | -            | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| 18-23  | ENGDIV [0:5] | Engineering clock division factor. Specifies the frequency ratio between the system clock and ENGCLK. The ENGCLK frequency is divided from the system clock frequency according to the following equation: Note: Clearing ENGDIV to 0 is reserved. Synchronization between ENGCLK and CLKOUT cannot be guaranteed. Engineering clock frequency System clock frequency ENGDIV 2 × -------------------------------- ------------------------------- =                                                                                                                                                                                                                                                          |
| 24-27  | -            | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| 28     | EBTS         | External bus tap select. Changes the phase relationship between the system clock and CLKOUT. Changing the phase relationship so that CLKOUT is advanced in relation to the system clock increases the output hold time of the external bus signals to a non-zero value. It also increases the output delay times, increases the input hold times to non-zero values, and decreases the input setup times. Refer to the Electrical Specifications for how the EBTS bit affects the external bus timing. 0 External bus signals have zero output hold times. 1 External bus signals have non-zero output hold times. Note: The EBTS bit must not be modified while an external bus transaction is in progress. |
| 29     | -            | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| 30-31  | EBDF [0:1]   | External bus division factor. Specifies the frequency ratio between the system clock and the external clock, CLKOUT. The EBDF field must not be changed during an external bus access or while an access is pending. The CLKOUT frequency is divided from the system clock frequency according to the descriptions below. This divider must be kept as divide-by-2 when operating in dual controller mode. 00 Reserved 01 Divide by 2 10 Reserved 11 Divide by 4                                                                                                                                                                                                                                             |

## 6.3.1.20 Compare A High Register (SIU\_CARH)

The compare registers are not intended for general application use, but are used temporarily by the BAM during boot and intended optionally for communication with calibration tools. After reset, calibration tools can immediately write a non-zero value to these registers. The application code, using the registers then as read only, can read them to determine if a calibration tool is attached and operate appropriately.

The compare registers can be used just like 128 bits of memory mapped RAM that is always zero out of reset, or they can perform a 64 bit to 64 bit compare. The compare function is continuous (combinational logic - not requiring a start or stop). The compare result appears in the MATCH bit in the SIU\_CCR register.

The SIU\_CARH holds the 32-bit value that is compared against the value in the SIU\_CBRH register. The CMPAH field is read/write and is reset by the synchronous reset signal.

Figure 6-136. Compare A High Register (SIU\_CARH)

<!-- image -->

|          | 0            | 1            | 2            | 3            | 4            | 5            | 6            | 7            | 8            | 9            | 10           | 11           | 12           | 13           | 14           | 15           |
|----------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|
| R        | CMPAH        | CMPAH        | CMPAH        | CMPAH        | CMPAH        | CMPAH        | CMPAH        | CMPAH        | CMPAH        | CMPAH        | CMPAH        | CMPAH        | CMPAH        | CMPAH        | CMPAH        | CMPAH        |
| W        |              |              |              |              |              |              |              |              |              |              |              |              |              |              |              |              |
| Reset    | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            |
| Reg Addr | Base + 0x988 | Base + 0x988 | Base + 0x988 | Base + 0x988 | Base + 0x988 | Base + 0x988 | Base + 0x988 | Base + 0x988 | Base + 0x988 | Base + 0x988 | Base + 0x988 | Base + 0x988 | Base + 0x988 | Base + 0x988 | Base + 0x988 | Base + 0x988 |
|          | 16           | 17           | 18           | 19           | 20           | 21           | 22           | 23           | 24           | 25           | 26           | 27           | 28           | 29           | 30           | 31           |
| R        | CMPAH        | CMPAH        | CMPAH        | CMPAH        | CMPAH        | CMPAH        | CMPAH        | CMPAH        | CMPAH        | CMPAH        | CMPAH        | CMPAH        | CMPAH        | CMPAH        | CMPAH        | CMPAH        |
| W        |              |              |              |              |              |              |              |              |              |              |              |              |              |              |              |              |
| Reset    | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            |
| Reg Addr | Base + 0x988 | Base + 0x988 | Base + 0x988 | Base + 0x988 | Base + 0x988 | Base + 0x988 | Base + 0x988 | Base + 0x988 | Base + 0x988 | Base + 0x988 | Base + 0x988 | Base + 0x988 | Base + 0x988 | Base + 0x988 | Base + 0x988 | Base + 0x988 |

## 6.3.1.21 Compare A Low Register (SIU\_CARL)

The SIU\_CARL register holds the 32-bit value that is compared against the value in the SIU\_CBRL register. The CMPAL field is read/write and is reset by the synchronous reset signal.

Figure 6-137. Compare A Low Register (SIU\_CARL)

<!-- image -->

|          | 0            | 1            | 2            | 3            | 4            | 5            | 6            | 7            | 8            | 9            | 10           | 11           | 12           | 13           | 14           | 15           |
|----------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|
| R        | CMPAL        | CMPAL        | CMPAL        | CMPAL        | CMPAL        | CMPAL        | CMPAL        | CMPAL        | CMPAL        | CMPAL        | CMPAL        | CMPAL        | CMPAL        | CMPAL        | CMPAL        | CMPAL        |
| W Reset  | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            |
| Reg Addr | Base + 0x98C | Base + 0x98C | Base + 0x98C | Base + 0x98C | Base + 0x98C | Base + 0x98C | Base + 0x98C | Base + 0x98C | Base + 0x98C | Base + 0x98C | Base + 0x98C | Base + 0x98C | Base + 0x98C | Base + 0x98C | Base + 0x98C | Base + 0x98C |
|          | 16           | 17           | 18           | 19           | 20           | 21           | 22           | 23           | 24           | 25           | 26           | 27           | 28           | 29           | 30           | 31           |
| R        | CMPAL        | CMPAL        | CMPAL        | CMPAL        | CMPAL        | CMPAL        | CMPAL        | CMPAL        | CMPAL        | CMPAL        | CMPAL        | CMPAL        | CMPAL        | CMPAL        | CMPAL        | CMPAL        |
| Reset    | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            |
| Reg Addr | Base + 0x98C | Base + 0x98C | Base + 0x98C | Base + 0x98C | Base + 0x98C | Base + 0x98C | Base + 0x98C | Base + 0x98C | Base + 0x98C | Base + 0x98C | Base + 0x98C | Base + 0x98C | Base + 0x98C | Base + 0x98C | Base + 0x98C | Base + 0x98C |

## 6.3.1.22 Compare B High Register (SIU\_CBRH)

The SIU\_CBRH holds the 32-bit value that is compared against the value in the SIU\_CARH. The CMPBH field is read/write and is reset by the synchronous reset signal.

Figure 6-138. Compare B High Register (SIU\_CBRH)

<!-- image -->

|          | 0            | 1            | 2            | 3            | 4            | 5            | 6            | 7            | 8            | 9            | 10           | 11           | 12           | 13           | 14           | 15           |
|----------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|
| R        | CMPBH        | CMPBH        | CMPBH        | CMPBH        | CMPBH        | CMPBH        | CMPBH        | CMPBH        | CMPBH        | CMPBH        | CMPBH        | CMPBH        | CMPBH        | CMPBH        | CMPBH        | CMPBH        |
| W Reset  | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            |
| Reg Addr | Base + 0x990 | Base + 0x990 | Base + 0x990 | Base + 0x990 | Base + 0x990 | Base + 0x990 | Base + 0x990 | Base + 0x990 | Base + 0x990 | Base + 0x990 | Base + 0x990 | Base + 0x990 | Base + 0x990 | Base + 0x990 | Base + 0x990 | Base + 0x990 |
|          | 16           | 17           | 18           | 19           | 20           | 21           | 22           | 23           | 24           | 25           | 26           | 27           | 28           | 29           | 30           | 31           |
| R        | CMPBH        | CMPBH        | CMPBH        | CMPBH        | CMPBH        | CMPBH        | CMPBH        | CMPBH        | CMPBH        | CMPBH        | CMPBH        | CMPBH        | CMPBH        | CMPBH        | CMPBH        | CMPBH        |
| Reset    | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            |
| Reg Addr | Base + 0x990 | Base + 0x990 | Base + 0x990 | Base + 0x990 | Base + 0x990 | Base + 0x990 | Base + 0x990 | Base + 0x990 | Base + 0x990 | Base + 0x990 | Base + 0x990 | Base + 0x990 | Base + 0x990 | Base + 0x990 | Base + 0x990 | Base + 0x990 |

## 6.3.1.23 Compare B Low Register (SIU\_CBRL)

The SIU\_CBRL holds the 32-bit value that is compared against the value in the SIU\_CARL. The CMPBL field is read/write and is reset by the synchronous reset signal.

Figure 6-139. Compare B Low Register (SIU\_CBRL)

<!-- image -->

|          | 0            | 1            | 2            | 3            | 4            | 5            | 6            | 7            | 8            | 9            | 10           | 11           | 12           | 13           | 14           | 15           |
|----------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|
| R        | CMPBL        | CMPBL        | CMPBL        | CMPBL        | CMPBL        | CMPBL        | CMPBL        | CMPBL        | CMPBL        | CMPBL        | CMPBL        | CMPBL        | CMPBL        | CMPBL        | CMPBL        | CMPBL        |
| W        |              |              |              |              |              |              |              |              |              |              |              |              |              |              |              |              |
| Reset    | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            |
| Reg Addr | Base + 0x994 | Base + 0x994 | Base + 0x994 | Base + 0x994 | Base + 0x994 | Base + 0x994 | Base + 0x994 | Base + 0x994 | Base + 0x994 | Base + 0x994 | Base + 0x994 | Base + 0x994 | Base + 0x994 | Base + 0x994 | Base + 0x994 | Base + 0x994 |
|          | 16           | 17           | 18           | 19           | 20           | 21           | 22           | 23           | 24           | 25           | 26           | 27           | 28           | 29           | 30           | 31           |
| R        | CMPBL        | CMPBL        | CMPBL        | CMPBL        | CMPBL        | CMPBL        | CMPBL        | CMPBL        | CMPBL        | CMPBL        | CMPBL        | CMPBL        | CMPBL        | CMPBL        | CMPBL        | CMPBL        |
| W        |              |              |              |              |              |              |              |              |              |              |              |              |              |              |              |              |
| Reset    | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            |
| Reg Addr | Base + 0x994 | Base + 0x994 | Base + 0x994 | Base + 0x994 | Base + 0x994 | Base + 0x994 | Base + 0x994 | Base + 0x994 | Base + 0x994 | Base + 0x994 | Base + 0x994 | Base + 0x994 | Base + 0x994 | Base + 0x994 | Base + 0x994 | Base + 0x994 |

## 6.4 Functional Description

The following sections provide an overview of the SIU operation.

## 6.4.1 System Configuration

## 6.4.1.1 Boot Configuration

The BOOTCFG[0:1] pins are used to determine the boot mode initiated by the BAM program, and whether external  arbitration  is  selected  for  external  booting.  The  BAM  program  uses  the  BOOTCFG  field  to determine where to read the reset configuration word, and whether to initiate a CAN or SCI boot. See Section 16.3.2.2.5, 'Reset Configuration Half Word Read' of the BAM chapter for detail on the RCHW. Table 6-33 defines the boot modes specified by the BOOTCFG[0:1] pins. If the RSTCFG pin is asserted during the assertion of RSTOUT, except in the case of a software external reset, the BOOTCFG pins are latched 4 clock cycles prior to the negation of the RSTOUT pin and are used to update the SIU\_RSR and the BAM boot mode. Otherwise, if RSTCFG is negated during the assertion of RSTOUT, the BOOTCFG pins are ignored and the boot mode defaults to 'Boot from Internal Flash Memory.'

Table 6-33. BOOTCFG[0:1] Configuration

| Value   | Meaning                                          |
|---------|--------------------------------------------------|
| 0b00    | Boot from Internal Flash Memory                  |
| 0b01    | CAN/SCI Boot                                     |
| 0b10    | Boot from External Memory (No Arbitration)       |
| 0b11    | Boot from External Memory (External Arbitration) |

## 6.4.1.2 Pad Configuration

The  pad  configuration  registers  (SIU\_PCR)  in  the  SIU  allow  software  control  of  the  static  electrical characteristics of external pins. The pad configuration registers allow control over the following external pin characteristics:

- · Weak pull up/down enable/disable
- · Weak pull up/down selection
- · Slew-rate selection for outputs
- · Drive strength selection for outputs
- · Input buffer enable (when direction is configured for output)
- · Input hysteresis enable/disable
- · Open drain/push-pull output selection
- · Multiplexed function selection
- · Data direction selection

The pad configuration registers are provided to allow centralized control over external pins that are shared by more than one module. Each pad configuration register controls a single pin.

## 6.4.2 Reset Control

The reset controller logic is located in the SIU. See the Reset section of this manual for detail on reset operation.

## 6.4.2.1 RESET Pin Glitch Detect

The reset controller provides a glitch detect feature on the RESET pin. If the reset controller detects that the RESET pin is asserted for more than 2 clock cycles, the clock cycles the reset controller sets the RGF bit without affecting any of the other bits in the reset status register. The RGF bit remains set until cleared by software or the RESET pin is asserted for 10 clock cycles. The reset controller does not respond to assertions of the RESET pin if a reset cycle is already being processed.

## 6.4.3 External Interrupt

There are sixteen external interrupt inputs IRQ0-IRQ15 to the SIU. The IRQ n inputs can be configured for rising or falling edge events or both. Each IRQ n input has a corresponding flag bit in the external interrupt status register (SIU\_EISR). The flag bits for the IRQ[4:15] inputs are OR'ed together to form one interrupt request to the interrupt controller (OR function performed in the integration glue logic). The flag bits for the IRQ[0:3] inputs can generate either an interrupt request to the interrupt controller or a DMA transfer request to the DMA controller. Table 6-140 shows the DMA and interrupt request connections to the interrupt and DMA controllers.

The SIU contains an overrun request for each IRQ and one combined overrun request which is the logical OR  of the individual overrun requests. Only the combined overrun request is used in the MPC5553/MPC5554, and the individual overrun requests are not connected.

Each IRQ pin has a programmable filter for rejecting glitches on the IRQ signals. The filter length for the IRQ pins is specified in the external IRQ digital filter register (SIU\_IDFR).

Figure 6-140. SIU DMA/Interrupt Request Diagram

<!-- image -->

## 6.4.4 GPIO Operation

All GPIO functionality is provided by the SIU for the MPC5553/MPC5554. Each MPC5553/MPC5554 pin that has GPIO functionality has an associated pin configuration register in the SIU where the GPIO function is selected for the pin. In addition, each MPC5553/MPC5554 pin with GPIO functionality has an input data register (SIU\_GPDI n\_n ) and an output data register (SIU\_GPDO n\_n ).

## 6.4.5 Internal Multiplexing

The internal multiplexing select registers SIU\_ETISR, SIU\_EIISR, and SIU\_DISR provide selection of the source of the input for the eQADC external trigger inputs, the SIU external interrupts, and the DSPI signals that are used in serial and parallel chaining of the DSPI modules.

A block  diagram  of  the  internal  multiplexing  feature  is  given  in  Figure 6-141.  The  figure  shows  the multiplexing of four external signals to an output from the SIU. A two bit SEL field from an SIU select register is used to select the input of the multiplexor.

Figure 6-141. Four-to-One Internal Multiplexing Block Diagram

<!-- image -->

## 6.4.5.1 eQADC External Trigger Input Multiplexing

The six eQADC external trigger inputs can be connected to either an external pin, an eTPU channel, or an eMIOS channel. The input source for each eQADC external trigger is individually specified in the eQADC trigger input select register (SIU\_ETISR). An example of the multiplexing of an eQADC external trigger input is given in Figure 6-142. As shown in the figure, the ETRIG0 input of the eQADC can be connected to either the ETRIG0\_GPIO111 pin, the ETPUA30 channel, the EMIOS10 channel, or the GPIO206 pin. The remaining ETRIG inputs are multiplexed in the same manner (see Section 6.3.1.15, 'eQADC Trigger Input Select Register (SIU\_ETISR)' for the SIU\_ETISR[TSEL0]-SIU\_ETISR[TSEL5] bit definitions). Note that if an ETRIG input is connected to an eTPU or eMIOS channel, the external pin used by that channel can be used by the alternate function on that pin.

Figure 6-142. eQADC External Trigger Input Multiplexing

<!-- image -->

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## 6.4.5.2 SIU External Interrupt Input Multiplexing

The sixteen SIU external interrupt inputs can be connected to either an external pin or to serialized output signals from a DSPI module. The input source for each SIU external interrupt is individually specified in the external IRQ input select register (SIU\_EIISR). An example of the multiplexing of an SIU external interrupt  input  is  given  in  Figure 6-143.  As  shown  in  the  figure,  the  IRQ0  input  of  the  SIU  can  be connected to either the IRQ0\_GPIO203 pin, the DSPI\_B0 serial input signal, the DSPI\_C1 deserialized output signal, or the DSPI\_D2 deserialized output signal. The remaining IRQ inputs are multiplexed in the same manner. The inputs to the IRQ from each DSPI module are offset by one so that if more than one DSPI module is connected to the same external device type, a separate interrupt can be generated for each device. This also applies to DSPI modules connected to external devices of different type that have status bits in the same bit location of the deserialized information.

Figure 6-143. DSPI Serialized Input Multiplexing

<!-- image -->

## 6.4.5.3 Multiplexed Inputs for DSPI Multiple Transfer Operation

Each DSPI module can be combined in a serial or parallel chain (multiple transfer operation). Serial chaining allows SPI operation with an external device that has more bits than one DSPI module. An example of a serial chain is shown in Figure 6-144. In a serial chain, one DSPI module operates as a master, the second, third, or fourth DSPI modules operate as slaves. The data output (SOUT) of the master is connected to the data input (SIN) of the slave. The SOUT of a slave is connected to the SIN of subsequent slaves until the last module in the chain, where the SOUT is connected to an external pin, which connects to the input of an external SPI device. The slave DSPI and external SPI device use the master peripheral chip select (PCS) and clock (SCK). The trigger input of the master allows a slave DSPI to trigger a transfer when a data change occurs in the slave DSPI and the slave DSPI is operating in change in data mode. The trigger input of the master is connected to MTRIG output of the slave. If more than two DSPIs are chained in change in data mode, a chain must be connected of MTRIG outputs to trigger inputs through the slaves with the last slave MTRIG output connected to the master trigger input.

Parallel chaining allows the PCS and SCK from one DSPI to be used by more than one external SPI device, thus reducing pin utilization of the MPC5553/MPC5554 MCU. An example of a parallel chain is shown in Figure 6-145. In this example, the SOUT and SIN of the two DSPIs connect to separate external SPI devices, which share a common PCS and SCK.

To support multiple transfer operation of the DSPIs, an input multiplexor is required for the SIN, SS, SCK IN, and trigger signals of each DSPI. The input source for the SIN input of a DSPI can be a pin or the SOUT of any of the other three DSPIs. The input source for the SS input of a DSPI can be a pin or the PCS0 of any of the other three DSPIs. The input source for the SCK input of a DSPI can be a pin or the SCK output of any of the other three DSPIs. The input source for the trigger input can be the PCSS output of any of the other three DSPIs. The input source for each DSPI SIN, SS, SCK, and trigger signal is individually specified in the DSPI input select register (SIU\_DISR).

Figure 6-144. DSPI Serial Chaining

<!-- image -->

Figure 6-145. DSPI Parallel Chaining

<!-- image -->

## 6.5 Revision History

## Substantive Changes since Rev 3.0

Changed HYS bit footnotes to say 'set to zero' instead of 'set to one' for PCRs 4-62 and 69-74.

Removed ns values from SRC bit field in Table 6-15.

Put back in the SIU\_GPDO section description (Section 6.3.1.13, 'GPIO Pin Data Output Registers 0-213 (SIU\_GPDOn)'). It is the same as Rev2.2 of the RM now.

Bits 0-1 for SINSELA. Setting of 11 was "SOUT", changed to "SOUTD" in Table 6-30.

'Reserved' changed to 'No Trigger' in Table 6-30 for TRIGSELA bit field.

Changed ODE wording in Table 6-15 to say 'Open drain is disabled for the pad (push/pull driver enabled).'

Added Note to Section 6.3.1.12.97, 'Pad Configuration Registers 206 - 207 (SIU\_PCR206 -SIU\_PCR207)' describing ETRIG functionality. NOTE: The GPIO[206:7] pins have the capability to trigger the ADCs. For the ETRIG functionality, these GPIO pins need to be set as GPIO and then select the GPIO ADC trigger in the eQADC Trigger Input Select Register (SIU\_ETISR).'

Changed name of MPC5553 signal to be GPIO[203:204]\_EMIOS[14:15] (same as MPC5554 now) instead of the other way around and updated the description in Section 6.3.1.12.95, 'Pad Configuration Register 203 - 204 (SIU\_PCR203 - SIU\_PCR204).
