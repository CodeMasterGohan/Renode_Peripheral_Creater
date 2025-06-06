### Chatper 1 Overview

## 1.1 Introduction

The MPC5553 and MPC5554 microcontrollers (MCU) are the first members of the MPC5500 family of next generation powertrain microcontrollers based on the PowerPC Book E architecture. The MPC5500 family contains a PowerPC™ processor core. This family of parts contains many new features coupled with  high  performance  CMOS  technology  to  provide  significant  performance  improvement  over  the MPC565.

The e200z6 CPU of the MPC5500 family is based on the PowerPC Book E architecture. It is 100% user mode compatible  (with  floating  point  library)  with  the  classic  PowerPC  instruction  set.  The  Book  E architecture has enhancements that improve the PowerPC architecture's fit in embedded applications. This core also has additional instructions, including digital signal processing (DSP) instructions, beyond the classic PowerPC instruction set.

The MPC5553 and MPC5554 of the MPC5500 family have two levels of memory hierarchy. The fastest accesses are to the unified cache (32-kilobytes in the MPC5554, 8-kilobytes in the MPC5553). The next level in the hierarchy contains the 96-kilobyte internal SRAM and internal Flash memory (2 Mbytes Flash in the MPC5554, 1.5 Mbytes in the MPC5553). Both the internal SRAM and the Flash memory can hold instructions  and  data.  The  external  bus  interface  has  been  designed  to  support  most  of  the  standard memories used with the MPC5xx family.

The complex I/O timer functions of the MPC5500 family are performed by an enhanced time processor unit  engines  (eTPU)  -  two  in  the  MPC5554,  one  in  the  MPC5553.  Each  eTPU  engine  controls  32 hardware channels. The eTPU has been enhanced over the TPU by providing 24-bit timers, double action hardware channels, variable  number  of  parameters  per  channel,  angle  clock  hardware,  and  additional control  and  arithmetic  instructions.  The  eTPU  can  be  programmed  using  a  high-level  programming language.

The  less  complex  timer  functions  of  the  MPC5500  family  are  performed  by  the  enhanced  modular input/output system (eMIOS). The eMIOS' 24 hardware channels are capable of single action, double action, pulse width modulation (PWM) and modulus counter operation. Motor control capabilities include edge-aligned and center-aligned PWM.

Off-chip communication is performed by a suite of serial protocols including controller area networks (FlexCANs) - three FlexCANs in the MPC5554 and two in the MPC5553, an enhanced deserial/serial peripheral interface  (DSPI) - four in the MPC5554 and three in the MPC5553, and enhanced serial communications interfaces (eSCIs). The DSPIs support pin reduction through hardware serialization and deserialization of timer channels and general-purpose input/output (GPIO) signals.

The MCU of the MPC5553 and MPC5554 has an on-chip 40-channel enhanced queued dual analog to digital converter (eQADC).

The system integration unit (SIU) performs several chip-wide configuration functions. Pad configuration and general-purpose input and output (GPIO) are controlled from the SIU. External interrupts and reset control are also found in the SIU. The internal multiplexer submodule (SIU\_DISR) provides multiplexing of eQADC trigger sources, daisy chaining the DSPIs, and external interrupt signal multiplexing.

The MPC5553 has a fast Ethernet controller (FEC) with a built-in FIFO and a DMA controller.

Figure 1-1  is  a  block  diagram  of  the  MPC5554  (MPC5500  family  MCU),  and  Figure 1-2  is  a  block diagram of the MPC5553.

<!-- image -->

LEGEND

## MPC5500 Device Module Acronyms

e200z6 Core Component Acronyms

CAN

- Controller area network (FlexCAN)

DSPI

- Deserial/serial peripheral interface

DMA

- Enhanced direct memory access

eMIOS

- Enhanced modular I/O system

eQADC

- Enhanced queued analog/digital converter

eSCI

- Enhanced serial communications interface

eTPU

- Enhanced time processing units

FMPLL

- Frequency modulated phase-locked loop

SRAM

- Static RAM

DEC

- Decrementer

FIT

- Fixed interval timer

TB

- Time base

WDT

- Watchdog timer

Figure 1-1. MPC5554 Block Diagram

<!-- image -->

LEGEND

MPC5500 Device Module Acronyms

e200z6 Core Component Acronyms

CAN

- Controller area network (FlexCAN)

DSPI

- Deserial/serial peripheral interface

DMA

- Enhanced direct memory access

eMIOS

- Enhanced modular I/O system

eQADC

- Enhanced queued analog/digital converter

eSCI

- Enhanced serial communications interface

eTPU

- Enhanced time processing units

FMPLL

- Frequency modulated phase-locked loop

SRAM

- Static RAM

DEC - Decrementer

FIT

- Fixed interval timer

TB

- Time base

WDT

- Watchdog timer

Figure 1-2. MPC5553 Block Diagram

## 1.2 Features

This section provides a high-level description of the features found in the MPC5553 and MPC5554:

- · Operating parameters
- - Fully static operation, 23.3 -132 MHz
- - -40  to 150  C junction temperature ° °
- - Low power design
- -Less than 1.2 Watts power dissipation
- -Designed for dynamic power management of core and peripherals
- -Software-controlled clock gating of peripherals
- -Separate power supply for stand-by operation for portion of internal SRAM
- - Fabricated in 0.13 µ m process
- - 1.5V internal logic
- - Input and output pins with 3.0V 5.5V range -
- -35%/65% V DDE  CMOS switch levels (with hysteresis)
- -Selectable hysteresis
- -Selectable slew rate control
- - External bus and Nexus pins support 1.62V 3.6V operation -
- -Selectable drive strength control
- -Unused pins configurable as GPIO
- - Designed with EMI reduction techniques
- -Frequency modulated phase-locked loop
- -On-chip bypass capacitance
- -Selectable slew rate and drive strength
- · High performance e200z6 core processor
- - 32-bit PowerPC Book E compliant CPU
- - Thirty-two 64-bit general-purpose registers (GPRs)
- - Memory management unit (MMU) with 32-entry fully-associative translation look-aside buffer (TLB)
- - Branch processing unit
- - Fully pipelined load/store unit
- - 32 kilobyte unified cache (in the MPC5554), 8 kilobyte unified cache (in the MPC5553) with line locking
- -8-way set associative in the MPC5554, 2-way set associative in the MPC5553
- -Two 32-bit fetches per clock
- -8-entry store buffer
- -Way locking
- -Supports assigning cache as instruction or data only on a per way basis
- -Supports tag and data parity
- - Vectored interrupt support

- - Interrupt latency &lt; 70 ns @132MHz (measured from interrupt request to execution of first instruction of interrupt exception handler)
- - Reservation instructions for implementing read-modify-write constructs (internal SRAM and Flash)
- - Signal processing engine (SPE) auxiliary processing unit (APU) operating on 64-bit GPRs
- - Floating point
- -IEEE ® 754 compatible with software wrapper
- -Single precision in hardware, double precision with software library
- -Conversion instructions between single precision floating point and fixed point
- - Long cycle time instructions, except for guarded loads, do not increase interrupt latency in the MPC5554/MPC5553.  To reduce latency in both the MPC5553 and the MPC5554, long cycle time instructions are aborted upon interrupt requests.
- - Extensive system development support through Nexus debug module
- · System bus crossbar switch (XBAR)
- - 3 master ports in the MPC5554, 4 master ports in the MPC5553; 5 slave ports
- - 32-bit address bus, 64-bit data bus
- - Simultaneous accesses from different masters to different slaves (there is no clock penalty when a parked master accesses a slave)
- · Enhanced direct memory access (eDMA) controller
- - 64 channels (MPC5554) or 32 channels (MPC5553) support independent 8-, 16-, 32-, or 64-bit single value or block transfers.
- - Supports variable sized queues and circular queues.
- - Source and destination address registers are independently configured to post-increment or remain constant.
- - Each transfer is initiated by a peripheral, CPU, or eDMA channel request.
- - Each eDMA channel can optionally send an interrupt request to the CPU on completion of a single value or block transfer.
- · Interrupt controller (INTC)
- - 308 total interrupt vectors (MPC5554) or 212 total interrupt vectors (MPC5553)
- -278 (MPC5554) or 191 (MPC5553) peripheral interrupt requests
- -plus 8 software settable sources
- -plus 22 reserved interrupts in the MPC5554, 13 reserved in the MPC5553
- - Unique 9-bit vector per interrupt source
- - 16 priority levels with fixed hardware arbitration within priority levels for each interrupt source
- - Priority elevation for shared resources
- · Frequency modulated phase-locked loop (FMPLL)
- - Input clock frequency from 8 MHz to 20 MHz
- - Current controlled oscillator (ICO) range from 50 MHz to maximum device frequency
- - Reduced frequency divider (RFD) for reduced frequency operation without re-lock
- - Four selectable modes of operation
- - Programmable frequency modulation
- - Lock detect circuitry continuously monitors lock status
- - Loss of clock (LOC) detection for reference and feedback clocks

## Overview

- - Self-clocked mode (SCM) operation
- - On-chip loop filter (reduces number of external components required)
- - Engineering clock output
- · External bus interface (EBI)
- - 1.8V 3.3V I/O nominal I/O voltage -
- - Memory controller with support for various memory types
- - MPC5554 specifications:
- -32-bit data bus,  24-bit address bus with transfer size indication
- - MPC5553 specifications:
- -416 BGA: 32-bit data bus, 24-bit address bus without transfer size indication
- -324 BGA: 16-bit data bus, 20-bit address bus
- -208 MAPBGA: no external bus
- - Selectable drive strength
- - Configurable bus speed modes
- - Support for external master accesses to internal addresses
- - Burst support
- - Bus monitor
- - Chip selects
- -In both the MPC5553 and MPC5554, four chip select (CS[0:3]) signals; but the MPC5553 has no CS signals in the 208 MAPBGA package.
- -In the MPC5553 only, support for dynamic calibration with up to three calibration chip selects (CAL\_CS[0] and CAL\_CS[2:3])
- - Configurable wait states
- · System integration unit (SIU)
- - Centralized GPIO control of 214 (MPC5554) or 198 (MPC5553) I/O and bus pins
- - Centralized pad control on a per-pin basis
- - System reset monitoring and generation
- - External interrupt inputs, filtering and control
- - Internal multiplexer submodule (SIU\_DISR, SIU\_ETISR, SIU\_EIISR)
- · Error correction status module (ECSM)
- - Configurable error-correcting codes (ECC) reporting for internal SRAM and Flash memories
- · On-chip FLASH
- - 2Mbytes (MPC5554) or 1.5 Mbytes (MPC5553) burst Flash memory
- - 256K   64 bit configuration ×
- - Censorship protection scheme to prevent Flash content visibility
- - Hardware read-while-write feature that allows blocks to be erased/programmed while other blocks are being read (used for EEPROM emulation and data calibration)
- - 20 blocks (MPC5554) or 16 blocks (MPC5553) with sizes ranging from 16 Kbytes to 128 Kbytes to support features such as boot block, operating system block, and EEPROM emulation
- - Read while write with multiple partitions
- - Parallel programming mode to support rapid end of line programming

- - Hardware programming state machine
- · Configurable cache memory, 32 kilobyte (MPC5554) / 0 - 8 kilobyte (MPC5553)
- - 8-way set-associative, unified (instruction and data) cache in the MPC5554
- - 2-way set-associative unified (instruction and data) cache in the MPC5553
- · On-chip internal static RAM (SRAM)
- - 64 kilobyte general-purpose RAM of which 32 kilobytes are on standby power
- - ECC performs single bit correction, double bit error detection
- · Boot assist module (BAM)
- - Enables and manages the transition of MCU from reset to user code execution in the following configurations:
- -User application can boot from internal or external Flash memory
- -Download and execution of code via FlexCAN or eSCI
- · Enhanced modular I/O system (eMIOS)
- - 24 orthogonal channels with double action, PWM, and modulus counter functionality
- - Supports all DASM and PWM modes of MIOS14 (MPC5xx)
- - Four selectable time bases plus shared time or angle counter bus
- - DMA and interrupt request support
- - Motor control capability
- · Enhanced time processor unit (eTPU)
- - MPC5554 has two eTPU engines, MPC5553 has one engine
- - Each eTPU engine is an event-triggered timer subsystem
- - High level assembler/compiler
- - 32 channels per engine
- - 24-bit timer resolution
- - 16 kilobyte shared code memory  in the MPC5554, 12 kilobyte shared code memory in the MPC5553
- - 3 kilobyte (MPC5554) or 2.5 kilobyte (MPC5553)Shared data memory
- - Variable number of parameters allocatable per channel
- - Double match/capture channels
- - Angle clock hardware support
- - Shared time or angle counter bus for all eTPU and eMIOS modules
- - DMA and interrupt request support
- - Nexus class 3 debug support (with some class 4 support)
- · Enhanced queued analog/digital converter (eQADC)
- - 2 independent ADCs with 12-bit A/D resolution
- - Common mode conversion range of 0-5V
- - 40 single-ended inputs channels, expandable to 65 channels with external multiplexers on 416 and 324 BGA packages
- - 34 single-ended inputs channels, expandable to 57 channels with external multiplexers on 208 BGA packages
- - 8 channels can be used as 4 pairs of differential analog input channels
- - 10-bit accuracy at 400 ksamples/s, 8-bit accuracy at 800 ksamples/s
- - Supports six FIFO queues with fixed priority.

## Overview

- - Queue modes with priority-based preemption; initiated by software command,  internal (eTPU and eMIOS), or external triggers
- - DMA and interrupt request support
- - Supports all functional modes from QADC (MPC5xx family)
- · 4 (MPC5554) or 3 (MPC5553) deserial serial peripheral interface modules (DSPI)
- - SPI
- -Full duplex communication ports with interrupt and eDMA request support
- -Supports all functional modes from QSPI submodule of QSMCM (MPC5xx family)
- -Support for queues in RAM
- -6 chip selects, expandable to 64 with external demultiplexers
- -Programmable frame size, baud rate, clock delay and clock phase on a per frame basis
- -Modified SPI mode for interfacing to peripherals with longer setup time requirements
- - Deserial serial interface (DSI)
- -Pin reduction by hardware serialization and deserialization of eTPU and eMIOS channels
- -Chaining of DSI submodules
- -Triggered transfer control and change in data transfer control (for reduced EMI)
- · 2 enhanced serial communication interface (eSCI) modules
- - UART mode provides NRZ format and half or full duplex interface
- - eSCI bit rate up to 1 Mbps
- - Advanced error detection, and optional parity generation and detection
- - Word length programmable as 8 or 9 bits
- - Separately enabled transmitter and receiver
- - LIN Support
- - DMA support
- - Interrupt request support
- · 3 (MPC5554) or 2 (MPC5553) FlexCANs
- - 64 message buffers each
- - Full implementation of the CAN protocol specification, Version 2.0B
- - Based on and including all existing features of the Freescale TouCAN module
- - Programmable acceptance filters
- - Short latency time for high priority transmit messages
- - Arbitration scheme according to message ID or message buffer number
- - Listen only mode capabilities
- - Programmable clock source:  system clock or oscillator clock
- · Nexus development interface (NDI)
- - Per IEEE ® -ISTO 5001-2003
- - Real time development support for PowerPC core and eTPU engines through Nexus class 3 (some Class 4 support)
- - Data trace of eDMA accesses
- - Read and write access
- - Configured via the IEEE ® 1149.1 (JTAG) port
- - High bandwidth mode for fast message transmission

- - Reduced bandwidth mode for reduced pin usage
- · IEEE ® 1149.1 JTAG controller (JTAGC)
- - IEEE ® 1149.1-2001 test access port (TAP) interface
- - A JCOMP input that provides the ability to share the TAP. Selectable modes of operation include JTAGC/debug or normal system operation.
- - A 5-bit instruction register that supports IEEE ® 1149.1-2001 defined instructions.
- - A 5-bit instruction register that supports additional public instructions.
- - Three test data registers: a bypass register, a boundary scan register, and a device identification register.
- - A TAP controller state machine that controls the operation of the data registers, instruction register and associated circuitry.
- · Voltage regulator controller
- - Provides a low cost solution to power the core logic. It reduces the number of power supplies required from the customer power supply chip.
- · POR block
- - Provides initial reset condition up to the voltage at which pins (RESET) can be read safely. It does not guarantee the safe operation of the chip at specified minimum operating voltages.

## 1.3 MPC5553-Specific Modules

The MPC5553 has one module not found on the MPC5554, a Fast Ethernet Controller (FEC) module that supports the following features:

- - IEEE ® 802.3 MAC (compliant with IEEE ® 802.3 1998 edition)
- - Built-in FIFO and DMA controller
- - Support for different Ethernet physical interfaces:
- -100Mbps IEEE ® 802.3 MII
- -10Mbps IEEE ® 802.3 MII
- -10Mbps 7-wire interface (industry standard)

## 1.4 MPC5500 Family Comparison

Table 1-1. MPC5500 Family Comparison

| MPC5500 Device                     | MPC5554     | MPC5553     |
|------------------------------------|-------------|-------------|
| Core                               | e200z6      | e200z6      |
| Cache                              | 32k         | 8k          |
| Memory Management Unit             | 32 entry    | 32 entry    |
| Crossbar                           | 3x5         | 4x5         |
| Core Nexus                         | NZ6C3 (3+)  | NZ6C3 (3+)  |
| SRAM                               | 64k         | 64k         |
| Flash                              | 2M          | 1.5M        |
| External bus (EBI)                 | 32 bit      | 32 bit      |
| Direct Memory Access (eDMA)        | 64 channel  | 32 channel  |
| DMA Nexus                          | Class 3     | Class 3     |
| Serial                             | 2           | 2           |
| eSCI_A                             | yes         | yes         |
| eSCI_B                             | yes         | yes         |
| Controller Area Network (CAN)      | 3           | 2           |
| CAN_A                              | 64 buf      | 64 buf      |
| CAN_B                              | 64 buf      | no          |
| CAN_C                              | 64 buf      | 64 buf      |
| DSPI                               | 4           | 3           |
| DSPI_A                             | yes         | no          |
| DSPI_B                             | yes         | yes         |
| DSPI_C                             | yes         | yes         |
| DSPI_D                             | yes         | yes         |
| eMIOS                              | 24 channel  | 24 channel  |
| eTPU                               | 64 channel  | 32 channel  |
| eTPU_A                             | yes         | yes         |
| eTPU_B                             | yes         | no          |
| Code memory                        | 16k         | 12k         |
| Parameter RAM                      | 3k          | 2.5k        |
| Interrupt controller               | 300 channel | 200 channel |
| Analog to Digital Converter        | 40 channel  | 40 channel  |
| ADC_A                              | yes         | yes         |
| ADC_B                              | yes         | yes         |
| Phase Lock Loop (PLL)              | FM          | FM          |
| Voltage Regulator Controller (VRC) | yes         | yes         |

## 1.5 Detailed Features

The following sections provided detailed information about each of the on-chip modules.

## 1.5.1 e200z6 Core Overview

The MPC5553 and MPC5554 use the e200z6 core explained in detail in the e200z6 PowerPC TM Core Reference  Manual .  The  e200z6  CPU  utilizes  a  seven  stage  pipeline  for  instruction  execution.  The instruction fetch 1, instruction fetch 2, instruction decode/register file read, execute1, execute2/memory access1,  execute3/memory  access2,  and  register  writeback  stages  operate  in  an  overlapped  fashion, allowing single clock instruction execution for most instructions.

The integer execution unit consists of a 32-bit arithmetic unit (AU), a logic unit (LU), a 32-bit barrel shifter, a mask-insertion unit (MIU), a condition register manipulation unit (CRU), a count-leading-zeros unit (CLZ), a 32x32 hardware multiplier array, result feed-forward hardware, and support hardware for division.

Most arithmetic and logical operations are executed in a single cycle with the exception of multiply, which is implemented with a pipelined hardware array, and the divide instructions. The CLZ unit operates in a single clock cycle.

The instruction unit contains a program counter (PC) incrementer and a dedicated branch address adder to minimize delays during change of flow operations. Sequential prefetching is performed to ensure a supply of  instructions  into  the  execution  pipeline.  Branch  target  prefetching  is  performed  to  accelerate  taken branches. Prefetched instructions are placed into an instruction buffer capable of holding 6 sequential instructions and 2 branch target instructions.

Branch target addresses are calculated in parallel with branch instruction decode, resulting in execution time of three clocks. Conditional branches which are not taken execute in a single clock. Branches with successful lookahead and target prefetching have an effective execution time of one clock.

Memory load and store operations are provided for byte, halfword, word (32-bit), and doubleword data with automatic zero or sign extension of byte and halfword load data. These instructions can be pipelined to allow effective single cycle throughput. Load and store multiple word instructions allow low overhead context save and restore operations. The load/store unit contains a dedicated effective address adder to allow effective address generation to be optimized.

The condition register unit supports the condition register (CR) and condition register operations defined by the PowerPC architecture. The condition register consists of eight 4-bit fields that reflect the results of certain operations, such as move, integer and floating-point compare, arithmetic, and logical instructions, and provide a mechanism for testing and branching.

Vectored and auto-vectored interrupts are supported by the CPU. Vectored interrupt support is provided to allow multiple interrupt sources to have unique interrupt handlers invoked with no software overhead.

The signal processing extension (SPE) APU supports vector instructions (SIMD) operating on 16- and 32-bit fixed-point data types, as well as 32-bit IEEE ® -754 single-precision floating-point formats, and supports  single-precision  floating-point  operations  in  a  pipelined  fashion.  The  64-bit  general-purpose register  file  is  used  for  source  and  destination  operands,  and  there  is  a  unified  storage  model  for single-precision floating-point data types of 32-bits and the normal integer type. Low latency fixed-point and floating-point add, subtract, multiply, divide, compare, and conversion operations are provided, and most operations can be pipelined.

## 1.5.2 System Bus Crossbar Switch

The  system  bus's  XBAR  multi-port  crossbar  switch  supports  simultaneous  connections  between three(MPC5554) or four (MPC5553) master ports and five slave ports. The crossbar supports a 32-bit address bus width and a 64-bit data bus width at all master and slave ports.

The crossbar allows for concurrent transactions to occur from any master port to any slave port. It is possible for all master ports and slave ports to be in use at the same time as a result of independent master requests. If a slave port is simultaneously requested by more than one master port, arbitration logic will select the higher priority master and grant it ownership of the slave port. All other masters requesting that slave port will be stalled until the higher priority master completes its transactions. By default, requesting masters will be treated with equal priority and will be granted access to a slave port in round-robin fashion, based upon the ID of the last master to be granted access.

## 1.5.3 eDMA

The  enhanced  direct  memory  access  (eDMA)  controller  is  a  second-generation  module  capable  of performing complex data movements via 64 (MPC5554) or 32 (MPC5553) programmable channels, with minimal intervention from the  CPU. The hardware micro architecture includes a DMA engine which performs source and destination address calculations, and the actual data movement operations, along with an  SRAM-based  memory  containing  the  transfer  control  descriptors  (TCD)  for  the  channels.  This implementation is utilized to minimize the overall module size.

## 1.5.4 INTC

The  interrupt  controller  (INTC)  provides  priority-based  preemptive  scheduling  of  interrupt  requests, suitable for statically scheduled real-time systems. The INTC allows interrupt request servicing from 308 (MPC5554)/212(MPC5553) interrupt sources.

For high priority interrupt requests, the time from the assertion of the interrupt request from the peripheral to when the processor is executing the interrupt service routine (ISR) has been minimized. The INTC provides a unique vector for each interrupt request source for quick determination of which ISR needs to be executed. It also provides an ample number of priorities so that lower priority ISRs do not delay the execution of higher priority ISRs. To allow the appropriate priorities for each source of interrupt request, the priority of each interrupt request is software configurable.

When multiple tasks share a resource, coherent accesses to that resource must be supported. The INTC supports the priority ceiling protocol for coherent accesses. By providing a modifiable priority mask, the priority  level  can  be  raised  temporarily  so  that  no  task  can  prempt  another  task  that  shares  the  same resource.

Multiple processors can assert interrupt requests to each other through software settable interrupt requests (by using application software to assert requests). These maskable interrupt requests can be used to split the software into a high priority portion and a low priority portion for servicing the interrupt requests. The high priority portion is initiated by a peripheral interrupt request, but then the ISR asserts a software settable interrupt request to finish the servicing in a lower priority ISR.

## 1.5.5 FMPLL

The frequency modulated PLL (FMPLL) allows the user to generate high speed system clocks from an 8MHz  to  20MHz  crystal  oscillator  or external clock generator. Further, the FMPLL  supports programmable frequency modulation of the system clock. The PLL multiplication factor, output clock divider ratio, modulation depth, and modulation rate are all software configurable.

## 1.5.6 EBI

The external bus interface (EBI) controls data transfer across the crossbar switch to/from memories or peripherals  in  the  external  address  space.  The  EBI  also  enables  an  external  master  to  access  internal address space. The EBI includes a memory controller that generates interface signals to support a variety of  external  memories. The EBI memory controller supports single data rate (SDR) burst mode Flash, external SRAM, and asynchronous memories. In addition, the EBI supports up to 4 regions (via chip selects), along with programmed region-specific attributes.

## 1.5.7 SIU

The  MPC5553/MPC5554  system  integration  unit  (SIU)  controls  MCU  reset  configuration,  pad configuration, external interrupt, general-purpose I/O (GPIO), internal peripheral multiplexing, and the system reset operation. The reset configuration module contains the external pin boot configuration logic. The pad configuration module controls the static electrical characteristics of I/O pins. The GPIO module provides  uniform  and  discrete  input/output  control  of  the  I/O  pins  of  the  MCU.  The  reset  controller performs reset monitoring of internal and external reset sources, and drives the RSTOUT pin. The SIU is accessed by the e200z6 core through the crossbar switch.

## 1.5.8 ECSM

The error correction status module (ECSM) provides status information regarding platform memory errors reported by error-correcting codes.

## 1.5.9 Flash

The MPC5554 provides 2 Mbytes of programmable, non-volatile, Flash memory storage. The MPC5553 provides 1.5 Mbytes of Flash memory.  The non-volatile memory (NVM) can be used for instruction and/or data storage.

The MPC5553/MPC5554 Flash also contains a Flash bus interface unit (FBIU) that interfaces the system bus to a dedicated Flash memory array controller. The FBIU supports a 64-bit data bus width at the system bus port, and a 256-bit read data interface to Flash memory. The FBIU contains two 256-bit prefetch buffers, and a prefetch controller that prefetches sequential lines of data from the Flash array into the buffer. Prefetch buffer hits allow no-wait responses. Normal Flash array accesses are registered in the FBIU and are forwarded to the system bus on the following cycle, incurring three wait-states. Prefetch operations  may  be  automatically  controlled,  and  may  be  restricted  to  servicing  a  single  bus  master. Prefetches may also be restricted to being triggered for instruction or data accesses.

## 1.5.10 Cache

The e200z6 core supports a 32-Kbyte (MPC5554) / 8-Kbyte (MPC5553), 8-way (MPC5554) / 2-way (MPC5553)  set-associative,  unified  (instruction  and  data)  cache  with  a  32-byte  line  size.  The  cache improves system performance by providing low-latency data to the e200z6 instruction and data pipelines, which decouples processor performance from system memory performance. The cache is virtually indexed and  physically  tagged.  The  e200z6  does  not  provide  hardware  support  for  cache  coherency  in  a multi-master environment. Software must be used to maintain cache coherency with other possible bus masters.

Both instruction and data accesses are performed using a single bus connected to the cache. Addresses from  the  processor  to  the  cache  are  virtual  addresses  used  to  index  the  cache  array.  The  memory management unit (MMU) provides the virtual to physical translation for use in performing the cache tag

## Overview

compare. The MMU may also be configured so that virtual addresses are passed through to the cache as the physical address untranslated. If the physical address matches a valid cache tag entry, the access hits in the cache. For a read operation, the cache supplies the data to the processor, and for a write operation, the data from the processor updates the cache. If the access does not match a valid cache tag entry (misses in the cache) or a write access must be written through to memory, the cache performs a bus cycle on the system bus.

## 1.5.11 SRAM

The MPC5500 family's internal SRAM module provides a general-purpose 96-Kbyte memory block that supports mapped read/write accesses from any master. Included within the 96-Kbyte SRAM block is a 32-Kbyte  block  powered  by  a  separate  supply  for  standby  operation,  and  ECC  error  correction  and detection.

## 1.5.12 BAM

The boot assist module (BAM) is a block of read-only memory that is programmed once by Freescale and is identical for all MCUs with an e200z6 core. The BAM program is executed every time the MCU is powered-on or reset in normal mode. The BAM supports the following four modes of booting:

- · Booting from internal Flash memory
- · Single master booting from external memory
- · Multi master booting from external memory with either no arbitration or external arbitration
- · Serial boot loading (a program is downloaded into RAM via eSCI or the FlexCAN and then executed).

The BAM also reads the reset configuration half word (RCHW) from Flash memory (either internal or external) and configures the MPC5553 and MPC5554 hardware accordingly.

## 1.5.13 eMIOS

The enhanced modular I/O system (eMIOS) module provides the functionality to generate or measure time events. A unified channel (UC) module is employed that provides a superset of the functionality of all the MIOS channels, while providing a consistent user interface. This allows more flexibility as each unified channel can be programmed for different functions in different applications. In order to identify up to two timed events, each UC contains two comparators, a time base selector and registers. This structure is able to produce match events, which can be configured to measure or generate a waveform. Alternatively, input events can be used to capture the time base, allowing measurement of an input signal.

## 1.5.14 eTPU

The enhanced time processing  unit  (eTPU)  is  an  enhanced  co-processor  designed  for  timing  control. Operating in parallel with the CPU, the eTPU processes instructions and real-time input events, performs output waveform generation, and accesses shared data without host intervention. Consequently, for each timer event, the CPU setup and service times are minimized or eliminated. In the MPC5554 MCU, two eTPU engines  are  grouped  together  with  shared  instruction  and  data  RAM  to  form  a  powerful  time processing  subsystem.  The  MPC5553  has  one  eTPU  engine.  High-level  assembler/compiler  and documentation allows customers to develop their own functions on the eTPU. The eTPU supports several features of older TPU versions, making it easy to port older applications.

## 1.5.15 eQADC

The enhanced queued analog to digital converter (eQADC) module provides accurate and fast conversions for a wide range of applications. The eQADC provides a parallel interface to two on-chip analog to digital converters (ADCs), and a single master-to-single slave serial interface to an off-chip external device. The two on-chip ADCs are architected to allow access to all the analog channels.

The eQADC transfers commands from multiple command FIFOs (CFIFOs) to the on-chip ADCs or to the external device. The module can also receive data from the on-chip ADCs or from an off-chip external device  into  multiple  result  FIFOs  (RFIFOs)  in  parallel,  independently  of  the  CFIFOs.  The  eQADC supports software and external hardware triggers from other modules to initiate transfers of commands from the CFIFOs to the on-chip ADCs or to the external device. It also monitors the fullness of CFIFOs and RFIFOs, and accordingly generates eDMA or interrupt requests to control data movement between the FIFOs and the system memory, which is external to the eQADC.

## 1.5.16 DSPI

The  deserial  serial  peripheral  interface  (DSPI)  module  provides  a  synchronous  serial  interface  for communication between the MCU and external devices. The DSPI supports pin count reduction through serialization and deserialization of eTPU channels, eMIOS channels and memory-mapped registers. The channels and register content are transmitted using a SPI-like protocol. There are four identical DSPI modules (DSPI\_A, DSPI\_B, DSPI\_C, and DSPI\_D) on the MPC5554 MCU. The MPC5553 has three DSPI modules (DSPI\_B, DSPI\_C, and DSPI\_D).

The DSPIs have three configurations:

- · Serial peripheral interface (SPI) configuration where the DSPI operates as a SPI with support for queues
- · Deserial serial interface (DSI) configuration where the DSPI serializes eTPU and eMIOS output channels and deserializes the received data by placing it on the eTPU and eMIOS input channels
- · Combined serial interface (CSI) configuration where the DSPI operates in both SPI and DSI configurations interleaving DSI frames with SPI frames, giving priority to SPI frames

For queued operations, the SPI queues reside in system memory external to the DSPI. Data transfers between the memory and the DSPI FIFOs are accomplished through the use of the eDMA controller or through host software.

## 1.5.17 eSCI

The enhanced serial communications interface (eSCI) allows asynchronous serial communications with peripheral devices and other MCUs. It includes special support to interface to local interconnect network (LIN) slave devices.

## 1.5.18 FlexCAN

The MCU contains three (MPC5554) or two (MPC5553) controller area network (FlexCAN) modules. Each FlexCAN module is a communication controller implementing the CAN protocol according to CAN Specification version 2.0B. The CAN protocol was designed to be used primarily as a vehicle serial data bus, meeting the specific requirements of this field: real-time processing, reliable operation in the EMI environment of a vehicle, cost-effectiveness and required bandwidth. Each FlexCAN module contains 64 message buffers (MB).

## 1.5.19 NDI

The Nexus development interface (NDI) module provides real-time development support capabilities for the MPC5500 family's PowerPC-based MCU in compliance with the IEEE ® -ISTO 5001-2003 standard. This development support is supplied for MCUs without requiring external address and data pins for internal visibility. The NDI module is an integration of several individual Nexus modules that are selected to provide the development support interface for the MPC5500 family. The NDI module interfaces to the host processor, to one or dual eTPU processors, and internal buses to provide development support as per the IEEE ® -ISTO 5001-2003 standard. The development support provided includes program trace, data trace, watchpoint trace, ownership trace, run-time access to the MCU's internal memory map, and access to the PowerPC and eTPU internal registers during halt, via the auxiliary port. The Nexus interface also supports a JTAG only mode using only the JTAG pins.

## 1.5.20 JTAGC

The JTAG controller (JTAGC) module provides the means to test chip functionality and connectivity while remaining transparent to system logic when not in test mode. Testing is performed via a boundary scan technique, as defined in the IEEE ® 1149.1-2001 standard. All data input to and output from the JTAGC module is communicated in serial format. The JTAGC module is compliant with the IEEE ® 1149.1-2001 standard.

## 1.5.21 FEC (MPC5553 Only)

The fast Ethernet controller (FEC) of the MPC5553 supports several standard MAC-PHY interfaces to connect to an external Ethernet transceiver:

- · 10/100 Mbps MII interface
- · 10 Mbps 7-Wire interface that uses a subset of the MII pins

## 1.6 MPC5500 Family Memory Map

This section describes the MPC5500 family memory map. All addresses in the device, including those that are reserved, are identified in the tables. The addresses represent the physical addresses assigned to each module. Logical addresses are translated by the MMU into physical addresses.

Under software control of the MMU, the logical addresses allocated to modules may be changed on a minimum of a 4-Kbyte boundary. Peripheral modules may be redundantly mapped. The customer must use the MMU to prevent corruption.

Table 1-2 shows a detailed memory map.

Table 1-2. Detailed MPC5554/MPC5553 Family Memory Map

| Address Range 1                                                     | Allocated Size 1 (bytes)                                          | Used Size (bytes)                       | Use                                                  |
|---------------------------------------------------------------------|-------------------------------------------------------------------|-----------------------------------------|------------------------------------------------------|
| 0x0000_0000-0x001F_FFFF (MPC5554) 0x0000_0000-0x0017_FFFF (MPC5553) | 2 Mbytes                                                          | 2 Mbytes (MPC5554) 1.5 Mbytes (MPC5553) | FLASH Memory Array                                   |
| 0x0020_0000-0x00FF_FBFF (MPC5554) 0x0018_0000-0x00FF_FBFF (MPC5553) | (14 Mbytes - 1 Kbyte) (MPC5554) (14.5 Mbytes - 1 Kbyte) (MPC5553) | N/A                                     | Reserved                                             |
| 0x00FF_FC00-0x00FF_FFFF                                             | 1024                                                              | 1024 bytes                              | FLASH Shadow Row                                     |
| 0x0100_0000-0x1FFF_FFFF                                             | 496 Mbytes                                                        | 2 Mbytes                                | emulation mapping of FLASH Array                     |
| 0x2000_0000-0x3FFF_FFFF                                             | 512 Mbytes                                                        | N/A                                     | External Memory                                      |
| 0x4000_0000-0x4000_7FFF                                             | 32 Kbytes                                                         | 32 Kbytes                               | Internal SRAM Array, Standby Powered                 |
| 0x4000_8000-0x4000_FFFF                                             | 32 Kbytes                                                         | 32 Kbytes                               | Internal SRAM Array                                  |
| 0x4001_0000-0xBFFF_FFFF                                             | (2048Mbytes-64 Kbytes)                                            | N/A                                     | Reserved                                             |
| Bridge A Peripherals                                                | Bridge A Peripherals                                              | Bridge A Peripherals                    | Bridge A Peripherals                                 |
| 0xC000_0000-0xC3EF_FFFF                                             | 63 M                                                              | N/A                                     | Reserved                                             |
| 0xC3F0_0000-0xC3F0_3FFF                                             | 16 K                                                              | -                                       | Bridge A Registers                                   |
| 0xC3F0_4000-0xC3F7_FFFF                                             | 496K                                                              | N/A                                     | Reserved                                             |
| 0xC3F8_0000-0xC3F8_3FFF                                             | 16 Kbytes                                                         | -                                       | FMPLL Registers                                      |
| 0xC3F8_4000-0xC3F8_7FFF                                             | 16 Kbytes                                                         | 48                                      | External Bus Interface (EBI) Configuration Registers |
| 0xC3F8_8000-0xC3F8_BFFF                                             | 16 Kbytes                                                         | 28                                      | Flash Configuration Registers                        |
| 0xC3F8_C000-0xC3F8_FFFF                                             | 16 Kbytes                                                         | N/A                                     | Reserved                                             |
| 0xC3F9_0000-0xC3F9_3FFF                                             | 16 Kbytes                                                         | 2.5 Kbytes                              | System Integration Unit (SIU)                        |
| 0xC3F9_4000-0xC3F9_FFFF                                             | 48 Kbytes                                                         | N/A                                     | Reserved                                             |
| 0xC3FA_0000-0xC3FA_3FFF                                             | 16 Kbytes                                                         | 1056                                    | Modular Timer System (eMIOS/MTS)                     |
| 0xC3FA_4000-0xC3FB_FFFF                                             | 112 Kbytes                                                        | N/A                                     | Reserved                                             |
| 0xC3FC_0000-0xC3FC_3FFF                                             | 16 Kbytes                                                         | 3 Kbytes                                | Enhanced Time Processing Unit (eTPU) Registers       |
| 0xC3FC_4000-0xC3FC_7FFF                                             | 16 Kbytes                                                         | N/A                                     | Reserved                                             |
| 0xC3FC_8000-0xC3FC_BFFF                                             | 16 Kbytes                                                         | 3 Kbytes (MPC5554) 2.5 Kbytes (MPC5553) | eTPU Shared Data Memory (Parameter RAM)              |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 1-2. Detailed MPC5554/MPC5553 Family Memory Map (continued)

| Address Range 1          | Allocated Size 1 (bytes)   | Used Size (bytes)                       | Use                                                 |
|--------------------------|----------------------------|-----------------------------------------|-----------------------------------------------------|
| 0xC3FC_C000-0xC3FC_FFFF  | 16 Kbytes                  | 3 Kbytes (MPC5554) 2.5 Kbytes (MPC5553) | eTPU Shared Data Memory (Parameter RAM) mirror      |
| 0xC3FD_0000-0xC3FD_3FFF  | 16 Kbytes                  | 16 Kbytes (MPC5554) 12 Kbytes (MPC5553) | eTPU Shared Code RAM                                |
| 0xC3FD_4000-0xC3FF_FFFF  | 176 Kbytes                 | N/A                                     | Reserved                                            |
| 0xC400_0000-0xDFFF_FFFF  | (512 Mbytes-64 Mbytes)     | N/A                                     | Reserved                                            |
| Bridge B Peripherals     | Bridge B Peripherals       | Bridge B Peripherals                    | Bridge B Peripherals                                |
| 0xE000_0000-0xFBFF_FFFF  | (512 Mbytes-64 Mbytes)     | N/A                                     | Reserved                                            |
| 0xFC00_0000-0xFFEF_FFFF  | 63 Mbytes                  | N/A                                     | Reserved                                            |
| 0xFFF0_0000-0xFFF0_3FFF  | 16 K                       | N/A                                     | Bridge B Registers                                  |
| 0xFFF0_4000-0xFFF0_7FFF  | 16 K                       | N/A                                     | System Bus Crossbar Switch (XBAR)                   |
| 0xFFF0__8000-0xFFF0_FFFF | 32 K                       | N/A                                     | Reserved                                            |
| 0xFFF1_0000-0xFFF3_FFFF  | 192 K                      | N/A                                     | Reserved                                            |
| 0xFFF4_0000-0xFFF4_3FFF  | 16 K                       | N/A                                     | ECSM                                                |
| 0xFFF4_4000-0xFFF4_7FFF  | 16 K                       | N/A                                     | DMA Controller 2 (eDMA)                             |
| 0xFFF4_8000-0xFFF4_BFFF  | 16 K                       | N/A                                     | Interrupt Controller (INTC)                         |
| 0xFFF4_C000-0xFFF4_FFFF  | 16 K                       | N/A                                     | Fast Ethernet Controller (FEC) 2 MPC5553 Only       |
| 0xFFFC_0000-0xFFF4_FFFF  | 15 K                       | N/A                                     | Reserved -- MPC5554 Only                            |
| 0xFFF5_0000-0xFFF7_FFFF  | 192 K                      | N/A                                     | Reserved                                            |
| 0xFFF8_0000-0xFFF8_3FFF  | 16 Kbytes                  | 164                                     | Enhanced Queued Analog-to-Digital Converter (eQADC) |
| 0xFFF8_4000-0xFFF8_FFFF  | 48 Kbytes                  | N/A                                     | Reserved                                            |
| 0xFFF9_0000-0xFFF9_3FFF  | 16 Kbytes                  | 200                                     | Deserial Serial Peripheral Interface (DSPI_A) 3     |
| 0xFFF9_4000-0xFFF9_7FFF  | 16 Kbytes                  | 200                                     | Deserial Serial Peripheral Interface (DSPI_B)       |
| 0xFFF9_8000-0xFFF9_BFFF  | 16 Kbytes                  | 200                                     | Deserial Serial Peripheral Interface (DSPI_C)       |
| 0xFFF9_C000-0xFFF9_FFFF  | 16 Kbytes                  | 200                                     | Deserial Serial Peripheral Interface (DSPI_D)       |
| 0xFFFA_0000-0xFFFA_FFFF  | 64 Kbytes                  | N/A                                     | Reserved                                            |
| 0xFFFB_0000-0xFFFB_3FFF  | 16 Kbytes                  | 44                                      | Serial Communications Interface (SCI_A)             |
| 0xFFFB_4000-0xFFFB_7FFF  | 16 Kbytes                  | 44                                      | Serial Communications Interface (SCI_B)             |
| 0xFFFB_8000-0xFFFB_FFFF  | 32 Kbytes                  | N/A                                     | Reserved                                            |
| 0xFFFC_0000-0xFFFC_3FFF  | 16 Kbytes                  | 1152                                    | Controller Area Network (FlexCAN_A)                 |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 1-2. Detailed MPC5554/MPC5553 Family Memory Map (continued)

| Address Range 1           | Allocated Size 1 (bytes)   | Used Size (bytes)   | Use                                   |
|---------------------------|----------------------------|---------------------|---------------------------------------|
| 0xFFFC_4000-0xFFFC_7FFF   | 16 Kbytes                  | 1152                | Controller Area Network (FlexCAN_B) 3 |
| 0xFFFC_8000-0xFFFC_BFFF   | 16 Kbytes                  | 1152                | Controller Area Network (FlexCAN_C)   |
| 0xFFFC_C000-0xFFFF_BFFF   | 192 Kbytes                 | N/A                 | Reserved                              |
| 0xFFFF_C000-0xFFFF_FFFF 4 | 16 Kbytes                  | 16 Kbytes           | Boot Assist Module (BAM)              |

- 1 If allocated size &gt; used size, then the base address for the module is the lowest address of the listed address range, unless noted otherwise.
- 2 MPC5553 only, not in MPC5554
- 3 MPC5554 only, not in MPC5553
- 4 BAM address range is configured so that 4Kbyte BAM occupies 0xFFFF\_F000-0xFFFF\_FFFF

## 1.7 Multi-Master Operation Memory Map

When the MPC5553/MPC5554 MCU acts as a slave in a multi-master system, the external bus interface (EBI) translates  the  24-bit  external  address  to  a  32-bit  internal  address.  Table 1-3  lists  the  translation parameters.

Table 1-3. External to Internal Memory Map Translation Table for Slave Mode

| Ext Addr[8:11] 1   | Internal Addr[0:11]   | Size (bytes)   | Internal Slave       | Internal Address Range    |
|--------------------|-----------------------|----------------|----------------------|---------------------------|
| 0b0xxx             | N/A                   | 8 Mbytes       | N/A                  | N/A-Off-chip Flash access |
| 0b10xx             | 0b0000_0000_00xx      | 4 Mbytes       | Internal FLASH Array | 0x0000_0000-0x003F_FFFF   |
| 0b1100             | 0b0100_0000_0000      | 1 Mbyte        | Internal SRAM        | 0x4000_0000-0x400F_FFFF   |
| 0b1101             | 0b0110_0000_0000      | 1 Mbyte        | Reserved 2           | 0x6000_0000-0x600F_FFFF   |
| 0b1110             | 0b1100_0011_1111      | 1 Mbyte        | Bridge A Peripherals | 0xC3F0_0000-0xC3FF_FFFF   |
| 0b1111             | 0b1111_1111_1111      | 1 Mbyte        | Bridge B Peripherals | 0xFFF0_0000-0xFFFF_FFFF   |

- 1 Only the lower 24 address signals (addr[8:31]) are available off-chip.
- 2 Reserved for a future module that requires its own crossbar slave port.

Table 1-4 shows the memory map for the MPC5553/MPC5554 MCU acting as a slave in a multi-master system from the point of view of the external master.

Table 1-4. MPC5500 Family Slave Memory Map as Seen from an External Master

| External Address Range 1                                   | Size (bytes)                          | Use                                   |
|------------------------------------------------------------|---------------------------------------|---------------------------------------|
| 0x00_0000 2 -0x7F_FFFF                                     | 8 Mbytes                              | N/A-Used for off-chip memory accesses |
| 0x80_0000-0x9F_FFFF(MPC5554) 0x80_0000-0x97_FFFF(MPC5553)  | 2 Mbytes(MPC5554) 1.5 Mbytes(MPC5553) | Slave FLASH 3                         |
| 0xA0_0000-0xBF_FFFF(MPC5554)0x98_0 000 -0xBF_FFFF(MPC5553) | 2 Mbytes(MPC5554) 2.5 Mbytes(MPC5553) | Reserved                              |
| 0xC0_0000-0xC0_FFFF                                        | 64 Kbytes                             | Slave Internal SRAM                   |
| 0xC1_0000-0xCF_FFFF                                        | (1 Mbytes-64 Kbytes)                  | Reserved                              |
| 0xD0_0000-0xDF_FFFF                                        | 1 Mbytes                              | Reserved                              |
| 0xE0_0000-0xEF_FFFF                                        | 1 Mbytes                              | Slave Bridge A Peripherals            |
| 0xF0_0000-0xFF_FFFF                                        | 1 Mbytes                              | Slave Bridge B Peripherals            |

1 Only the lower 24 address signals (addr[8:31]) are available off-chip.

2 This address range is not part of the MPC5500 family slave memory map, rather it is shown to illustrate the addressing scheme for off-chip accesses in multi-master mode.

3 The shadow row of the slave FLASH is not accessible by an external master.

Table 1-5 shows the memory map for the MPC5553 and MPC5554family MCU configured as a master in multi-master system with another MPC5500 family MCU acting as the slave.

Table 1-5. MPC5500 Family Master Memory Map (Multi Master Mode)

| Base Address            | Size (bytes)                                      | Use                        |
|-------------------------|---------------------------------------------------|----------------------------|
| On-Chip                 | On-Chip                                           | On-Chip                    |
| 0x0000_0000             | 2 Mbytes(MPC55545) 1.5 Mbytes(MPC5553)            | FLASH Array                |
| 0x0020_0000 0x0018_0000 | (14 Mbytes-1024 bytes) (14.5 Mbytes - 1024 bytes) | Reserved                   |
| 0x00FF_FC00             | 1024                                              | FLASH Shadow Row           |
| 0x0100_0000             | 496 Mbytes                                        | emulation mapping Flash    |
| Off-Chip                | Off-Chip                                          | Off-Chip                   |
| 0x2000_0000             | 8 Mbytes 1                                        | External Memory            |
| 0x2080_0000             | 2 Mbytes                                          | Slave FLASH                |
| 0x20A0_0000 0x2098_0000 | 2 Mbytes                                          | Reserved                   |
| Not Addressable         | 1024                                              | Slave FLASH Shadow Row     |
| 0x20C0_0000             | 64 Kbytes                                         | Slave Internal SRAM        |
| 0x20C1_0000             | (2 Mbytes-64 Kbytes)                              | Reserved                   |
| 0x20E0_0000             | 1 Mbytes                                          | Slave Bridge A Peripherals |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 1-5. MPC5500 Family Master Memory Map (Multi Master Mode)  (continued)

| Base Address   | Size (bytes)             | Use                        |
|----------------|--------------------------|----------------------------|
| 0x20F0_0000    | 1 Mbytes                 | Slave Bridge B Peripherals |
| On-Chip        | On-Chip                  | On-Chip                    |
| 0x4000_0000    | 96 Kbytes                | Internal SRAM              |
| 0x4001_8000    | (2048 Mbytes-96 Kbytes)  | Reserved                   |
| 0xC000_0000    | 63 Mbytes                | Reserved                   |
| 0xC3F0_0000    | 1 Mbytes                 | Bridge A Peripherals       |
| 0xC400_0000    | (1024 Mbytes-128 Mbytes) | Reserved                   |
| 0xFC00_0000    | 63 Mbytes                | Reserved                   |
| 0xFFF0_0000    | 1 Mbyte                  | Bridge B Peripherals       |

- 1 By using the 4 chip select signals, 32 Mbytes of external memory can be accessed by the master in a multi-master system.

## 1.8 Revision History

| Substantive Changes since Rev 3.0                                                                                         |
|---------------------------------------------------------------------------------------------------------------------------|
| Features list - changed '40%/70% V DDE CMOS switch levels (with hysteresis)' to be 35%/65%                                |
| Fixed reference to CAL_CS[0:2]. On MPC5553, CAL_CS[1] is not implemented.                                                 |
| Fixed a typo - '308212 interrupts' - split it to 308 for MPC5554 and 212 for MPC5553.                                     |
| Updated both MPC5553 and MPC5554 block diagrams.                                                                          |
| In features list, changed '96 kilobyte general-purpose RAM of which 32 kilobytes are on standby power' to be 64 kilobyte. |

## Overview
