### Chatper 25 Nexus Development Interface

## 25.1 Introduction

The MPC5553/MPC5554 microcontroller contains multiple Nexus clients that communicate over a single IEEE ® -ISTO  5001™-2003  Nexus  class  3  combined  JTAG  IEEE ® 1149.1/auxiliary  out  interface. Combined, all of the Nexus clients are referred to as the Nexus development interface (NDI). Class 3 Nexus allows for program, data, and ownership trace of the microcontroller execution without access to the external data and address buses.

This chapter is organized in the following manner:

- · The chapter opens with sections that provide a high level view of the Nexus development interface: Section 25.1, 'Introduction' through Section 25.8, 'NPC Initialization/Application Information.'

The remainder of the chapter contains sections that discuss the remaining three modules of the Nexus development interface:

- · Nexus dual-eTPU development interface (NDEDI). The MPC5554 has two eTPU engines, whereas the MPC5553 has one eTPU engine. Refer to Section 25.9, 'Nexus Dual eTPU Development Interface (NDEDI)' and the eTPU Reference Manual for information about the NDEDI.
- · Nexus e200z6 core interface (NZ6C3). In this chapter, the NZ6C3 interface is discussed in Section 25.10, 'e200z6 Class 3 Nexus Module (NZ6C3) through Section 25.11, 'NZ6C3 Memory Map/Register Definition.'
- · Nexus crossbar eDMA interface (NXDM). Refer to Section 25.12, 'Nexus Crossbar eDMA Interface (NXDM)'

Communication to the NDI is handled via the auxiliary port and the JTAG port.

- · The auxiliary port is comprised of 9 or 17 output pins and 1 input pin.  The output pins include 1 message clock out (MCKO) pin, 4 or 12 message data out (MDO) pins, 2 message start/end out (MSEO) pins, 1 ready (RDY) pin, and 1 event out (EVTO) pin. Event in (EVTI) is the only input pin for the auxiliary port.
- · The JTAG port consists of four inputs and one output.  These pins include JTAG compliance select (JCOMP), test data input (TDI), test data output (TDO), test mode select (TMS), and test clock input (TCK). TDI, TDO, TMS, and TCK are compliant with the IEEE ® 1149.1-2001 standard and are shared with the NDI through the test access port (TAP) interface.  JCOMP along with power-on reset and the TAP state machine are used to control reset for the NDI module. Ownership of the TAP is achieved by loading the appropriate enable instruction for the desired Nexus client in the JTAG controller (JTAGC) when JCOMP is asserted. See Table 25-4 for the JTAGC opcodes to access the different Nexus clients.

## 25.1.1 Block Diagram

<!-- image -->

* The MPC5553 has only one eTPU engine; the MPC5554 has two eTPU engines.

Figure 25-1. NDI Block Diagram

## 25.1.2 Features

The  NDI  module  is  compliant  with  the  IEEE-ISTO  5001-2003  standard.  The  following  features  are implemented:

- · 15 or 23 bit full duplex pin interface for medium and high visibility throughput.
- · One of two modes selected by register configuration: full port mode (FPM) and reduced port mode (RPM). FPM comprises 12 MDO pins, and RPM comprises 4 MDO pins.
- · Auxiliary output port.
- - 1 MCKO (message clock out) pin
- - 4 or 12 MDO (message data out) pins
- - 2 MSEO (message start/end out) pins
- - 1 RDY (ready) pin
- - 1 EVTO (event out) pin

- · Auxiliary input port.
- - 1 EVTI (event in) pin
- - 5 pin JTAG port (JCOMP, TDI, TDO, TMS, and TCK)
- · Host processor (e200z6) development support features (NZ6C3).
- - IEEE-ISTO 5001-2003 standard class 3 compliant.
- - Data trace via data write messaging (DWM) and data read messaging (DRM). This allows the development tool to trace reads and/or writes to selected internal memory resources.
- - Ownership trace via ownership trace messaging (OTM). OTM facilitates ownership trace by providing visibility of which process ID or operating system task is activated. An ownership trace message is transmitted when a new process/task is activated, allowing development tools to trace ownership flow.
- - Program trace via branch trace messaging (BTM). Branch trace messaging displays program flow discontinuities (direct branches, indirect branches, exceptions, etc.), allowing the development tool to interpolate what transpires between the discontinuities. Thus, static code can be traced.
- - Watchpoint messaging (WPM) via the auxiliary port.
- - Watchpoint trigger enable of program and/or data trace messaging.
- - Data tracing of instruction fetches via private opcodes.
- - Subset of PowerPC Book E software debug facilities with OnCE block (Nexus class 1 features).
- · eDMA development support features (NXDM).
- - Data trace via data write messaging (DWM) and data read messaging (DRM). This allows the development tool to trace DMA generated reads and/or writes to selected address ranges in the MPC5554's memory map.
- - Watchpoint messaging (WPM) via the auxiliary port.
- - Watchpoint trigger enable/disable of data trace messaging.
- · eTPU development support features (NDEDI).
- - IEEE-ISTO 5001-2002 standard Class 3 compliant for the eTPU engines.
- - Data trace via data write messaging and data read messaging. This allows the development tool to trace reads and writes to selected shared parameter RAM (SPRAM) address ranges. Four data trace windows are shared between the two eTPU engines.
- - Ownership trace via ownership trace messaging (OTM). OTM facilitates ownership trace by providing visibility of which channel is being serviced. An ownership trace message is transmitted to indicate when a new channel service request is scheduled, allowing the development tools to trace task flow. A special OTM is sent when the engine enters in idle state, meaning that all requests were serviced and no new requests are yet scheduled.
- - Program trace via branch trace messaging. BTM displays program flow discontinuities (start, jumps, return, etc.), allowing the development tool to interpolate what transpires between the discontinuities. Thus static code can be traced. The branch trace messaging method uses the branch/predicate method to reduce the number of generated messages.
- - Watchpoint messaging via the auxiliary port. WPM provides visibility of the occurrence of the eTPUs' watchpoints and breakpoints.
- - Nexus based breakpoint/watchpoint configuration and single step support.
- · Run-time access to the on-chip memory map via the Nexus read/write access protocol. This feature supports accesses for run-time internal visibility, calibration variable acquisition, calibration constant tuning, and external rapid prototyping for powertrain automotive development systems.
- · All features are independently configurable and controllable via the IEEE ® 1149.1 I/O port.

## Nexus Development Interface

- · The NDI block reset is controlled with JCOMP, power-on reset, and the TAP state machine. These sources are independent of system reset.
- · System clock locked status indication via MDO0 following power-on reset.

## 25.1.3 Modes of Operation

The NDI block is in reset when the TAP controller state machine is in the TEST-LOGIC-RESET state. The TEST-LOGIC-RESET state is entered on the assertion of the power-on reset signal, negation of JCOMP, or through state machine transitions controlled by TMS. Assertion of JCOMP allows the NDI to move out of the reset state, and is a prerequisite to grant Nexus clients control of the TAP. Ownership of the TAP is achieved by loading the appropriate enable instruction for the desired Nexus client in the JTAGC controller (JTAGC) block when JCOMP is asserted.

Following negation of power-on reset, the NPC remains in reset until the system clock achieves lock. In PLL  bypass  mode,  the  NDI  can  transition  out  of  the  reset  state  immediately  following  negation  of power-on reset. Refer to Section 25.4.5, 'System Clock Locked Indication' for more details.

## 25.1.3.1 Nexus Reset Mode

In Nexus reset mode, the following actions occur:

- · Register values default back to their reset values.
- · The message queues are marked as empty.
- · The auxiliary output port pins are negated if the NDI controls the pads.
- · The TDO output buffer is disabled if the NDI has control of the TAP.
- · The TDI, TMS, and TCK inputs are ignored.
- · The NDI block indicates to the MCU that it is not using the auxiliary output port. This indication can be used to three-state the output pins or use them for another function.

## 25.1.3.2 Full-Port Mode

In full-port mode, all the available MDO pins are used to transmit messages. All trace features are enabled or can be enabled by writing the configuration registers via the JTAG port. The number of MDO pins available is 12.

## 25.1.3.3 Reduced-Port Mode

In reduced-port mode, a subset of the available MDO pins are used to transmit messages. All trace features are enabled or can be enabled by writing the configuration registers via the JTAG port. The number of MDO pins  available  is  4.  Unused  MDO  (MDO[11:4])  pins  can  be  used  as  GPIO.  Details  on  GPIO functionality configuration can be found in Chapter 6, 'System Integration Unit (SIU).'

## 25.1.3.4 Disabled-Port Mode

In disabled-port mode, message transmission is disabled. Any debug feature that generates messages can not be used. The primary features available are class 1 features and read/write access.

## 25.1.3.5 Censored Mode

When the device is in censored mode, reading the contents of internal flash externally is not allowed. To prevent  Nexus  modules  from  violating  censorship,  the  NPC  is  held  in  reset  when  in  censored  mode,

asynchronously  holding  all  other  Nexus  modules  in  reset  as  well.  This  prevents  Nexus  read/write  to memory  mapped  resources  and  the  transmission  of  Nexus  trace  messages.  Refer  to  Table 13-17  for information on Nexus port enabling and disabling regarding censorship.

## 25.2 External Signal Description

The auxiliary and JTAG pin interfaces provide for the transmission of messages from Nexus modules to the  external  development  tools  and  for  access  to  Nexus  client  registers.  The  auxiliary/JTAG    pin definitions are outlined in Table 25-1.

Table 25-1. Signal Properties

| Name                  | Port      | Function                                | Reset State   |
|-----------------------|-----------|-----------------------------------------|---------------|
| EVTO                  | Auxiliary | Event Out pin                           | Negated       |
| EVTI                  | Auxiliary | Event In pin                            | Pulled Up     |
| MCKO                  | Auxiliary | Message Clock Out pin (from NPC)        | Enabled       |
| MDO[3:0] or MDO[11:0] | Auxiliary | Message Data Out pins                   | Driven Low 1  |
| MSEO[1:0]             | Auxiliary | Message Start/End Out pins              | Negated       |
| RDY                   | Auxiliary | Ready Out pin                           | Negated       |
| JCOMP                 | JTAG      | JTAG Compliancy and TAP Sharing Control | Pulled Down   |
| TCK                   | JTAG      | Test Clock Input                        | Pulled Up     |
| TDI                   | JTAG      | Test Data Input                         | Pulled Up     |
| TDO                   | JTAG      | Test Data Output                        | Pulled Up     |
| TMS                   | JTAG      | Test Mode Select Input                  | Pulled Up     |

1 Following a power-on reset, MDO0 remains asserted until power-on reset is exited and the system clock achieves lock.

## 25.2.1 Detailed Signal Descriptions

This section describes each of the signals listed in Table 25-1 in more detail.

## 25.2.1.1 Event Out (EVTO )

EVTO is an output pin that is asserted upon breakpoint occurrence to provide breakpoint status indication or to signify that an event has occurred. The EVTO output of the NPC is generated based on the values of the individual EVTO signals from all Nexus modules that implement the signal.

## 25.2.1.2 Event In (EVTI )

EVTI is used to initiate program and data trace synchronization messages or to generate a breakpoint. EVTI is edge-sensitive for synchronization and breakpoint generation.

## 25.2.1.3 Message Data Out (MDO[3:0/11:0])

Message data out (MDO) are output pins used for uploading OTM, BTM, DTM, and other messages to the development tool. The development tool should sample MDO on the rising edge of MCKO. The width of the MDO bus used is determined by the Nexus PCR[FPM] configuration.

Following a power-on reset, MDO0 remains asserted until power-on reset is exited and the system clock achieves lock.

## 25.2.1.4 Message Start/End Out (MSEO[1:0])

MSEO[1:0] are output pins that indicates when a message on the MDO pins has started, when a variable length packet has ended, or when the message has ended. The development tool should sample the MSEO pins on the rising edge of MCKO.

## 25.2.1.5 Ready (RDY)

RDY is an output pin that indicates when a device is ready for the next access.

## 25.2.1.6 JTAG Compliancy (JCOMP)

The JCOMP signal enables or disables the TAP controller. The TAP controller is enabled when JCOMP asserted, otherwise the TAP controller remains in reset.

## 25.2.1.7 Test Data Output (TDO)

The TDO pin transmits serial output for instructions and data. TDO is tri-stateable and is actively driven in the SHIFT-IR and SHIFT-DR controller states. TDO is updated on the falling edge of TCK and sampled by the development tool on the rising edge of TCK.

## 25.2.1.8 Test Clock Input (TCK)

The TCK pin is used to synchronize the test logic and control register access through the JTAG port.

## 25.2.1.9 Test Data Input (TDI)

The TDI pin receives serial test instruction and data. TDI is sampled on the rising edge of TCK.

## 25.2.1.10 Test Mode Select (TMS)

The TMS pin is used to sequence the IEEE ® 1149.1-2001 TAP controller state machine. TMS is sampled on the rising edge of TCK.

## 25.3 Memory Map

The NDI block contains no memory mapped registers. Nexus registers are accessed by the development tool via the JTAG port using a register index and a client select value. The client select is controlled by loading the correct access instruction into the JTAG controller; refer to Section 25.4.1. OnCE registers are accessed by loading the appropriate value in the RS[0:6] field of the OnCE command register (OCMD) via the JTAG port.

Table 25-2 shows the NDI registers by client select and index values. Table 25-3 shows the OnCE register addressing.

Table 25-2. NDI Registers

| Client Select                   | Index                           | Register                                        |
|---------------------------------|---------------------------------|-------------------------------------------------|
| e200z6 Control/Status Registers | e200z6 Control/Status Registers | e200z6 Control/Status Registers                 |
| 0bxxxx                          | 0                               | Device ID (DID)                                 |
| 0b0000                          | 2                               | e200z6 Development Control1 (PPC_DC1)           |
| 0b0000                          | 3                               | e200z6 Development Control2 (PPC_DC2)           |
| 0b0000                          | 4                               | e200z6 Development Status (PPC_DS)              |
| 0b0000                          | 6                               | e200z6 User Base Address (PPC_UBA)              |
| 0b0000                          | 7                               | Read/Write Access Control/Status (RWCS)         |
| 0b0000                          | 9                               | Read/Write Access Address (RWA)                 |
| 0b0000                          | 10                              | Read/Write Access Data (RWD)                    |
| 0b0000                          | 11                              | e200z6 Watchpoint Trigger (PPC_WT)              |
| 0b0000                          | 13                              | e200z6 Data Trace Control (PPC_DTC)             |
| 0b0000                          | 14                              | e200z6 Data Trace Start Address 0 (PPC_DTSA1)   |
| 0b0000                          | 15                              | e200z6 Data Trace Start Address 1 (PPC_DTSA2)   |
| 0b0000                          | 18                              | e200z6 Data Trace End Address 0 (PPC_DTEA1)     |
| 0b0000                          | 19                              | e200z6 Data Trace End Address 1 (PPC_DTEA2)     |
| 0bxxxx                          | 127                             | Port Configuration Register (PCR)               |
| eDMA Control/Status Registers   | eDMA Control/Status Registers   | eDMA Control/Status Registers                   |
| 0b0001                          | 2                               | eDMA Development Control (AHB_DC)               |
| 0b0001                          | 11                              | eDMA Watchpoint Trigger (AHB_WT)                |
| 0b0001                          | 13                              | eDMA Data Trace Control (AHB_DTC)               |
| 0b0001                          | 14                              | eDMA Data Trace Start Address 0 (AHB_DTSA1)     |
| 0b0001                          | 15                              | eDMA Data Trace Start Address 1 (AHB_DTSA2)     |
| 0b0001                          | 18                              | eDMA Data Trace End Address 0 (AHB_DTEA1)       |
| 0b0001                          | 19                              | eDMA Data Trace End Address 1 (AHB_DTEA2)       |
| 0b0001                          | 22                              | eDMA Breakpoint/Watchpoint Control 1 (AHB_BWC1) |
| 0b0001                          | 23                              | eDMA Breakpoint/Watchpoint Control 2 (AHB_BWC2) |
| 0b0001                          | 30                              | eDMA Breakpoint/Watchpoint Address 1 (AHB_BWA1) |
| 0b0001                          | 31                              | eDMA Breakpoint/Watchpoint Address 2 (AHB_BWA2) |
| 0bxxxx                          | 127                             | Port Configuration Register (PCR)               |

Table 25-2. NDI Registers (continued)

| Client Select                                 | Index                                         | Register                                                    |
|-----------------------------------------------|-----------------------------------------------|-------------------------------------------------------------|
| eTPU1 Control/Status Registers                | eTPU1 Control/Status Registers                | eTPU1 Control/Status Registers                              |
| 0bxxxx                                        | 0                                             | Device ID (DID)                                             |
| 0b0010                                        | 2                                             | eTPU1 Development Control (NDI_eTPU1_DC)                    |
| 0b0010                                        | 4                                             | eTPU1 Development Status (NDEDI_eTPU1_DS)                   |
| 0b0000                                        | 7                                             | Read/Write Access Control/Status (RWCS)                     |
| 0b0000                                        | 9                                             | Read/Write Access Address (RWA)                             |
| 0b0000                                        | 10                                            | Read/Write Access Data (RWD)                                |
| 0b0010                                        | 11                                            | eTPU1 Watchpoint Trigger (NDI_eTPU1_WT)                     |
| 0b0010                                        | 13                                            | eTPU1 Data Trace Control (NDI_eTPU1_DTC)                    |
| 0b0010                                        | 22                                            | eTPU1 Breakpoint/Watchpoint Control 1 (NDEDI_eTPU1_BWC1)    |
| 0b0010                                        | 23                                            | eTPU1 Breakpoint/Watchpoint Control 2 (NDEDI_eTPU1_BWC2)    |
| 0b0010                                        | 24                                            | eTPU1 Breakpoint/Watchpoint Control 3 (NDEDI_eTPU1_BWC3)    |
| 0b0010                                        | 30                                            | eTPU1 Breakpoint/Watchpoint Address 1 (NDEDI_eTPU1_BWA1)    |
| 0b0010                                        | 31                                            | eTPU1 Breakpoint/Watchpoint Address 2 (NDEDI_eTPU1_BWA2)    |
| 0b0010                                        | 38                                            | eTPU1 Breakpoint/Watchpoint Data 1 (NDEDI_eTPU1_BWD1)       |
| 0b0010                                        | 39                                            | eTPU1 Breakpoint/Watchpoint Data 1 (NDEDI_eTPU1_BWD2)       |
| 0b0010                                        | 64                                            | eTPU1 Program Trace Channel Enable (NDI_eTPU1_PTCE)         |
| 0b0010                                        | 69                                            | eTPU1 Microinstruction Debug Register (NDEDI_eTPU1_INST)    |
| 0b0010                                        | 70                                            | eTPU1 Microprogram Counter Debug Register (NDEDI_eTPU1_MPC) |
| 0b0010                                        | 71                                            | eTPU1 Channel Flag Status Register (NDEDI_eTPU1_CFSR)       |
| 0bxxxx                                        | 127                                           | Port Configuration Register (PCR)                           |
| eTPU2 Control/Status Registers (MPC5554 Only) | eTPU2 Control/Status Registers (MPC5554 Only) | eTPU2 Control/Status Registers (MPC5554 Only)               |
| 0bxxxx                                        | 0                                             | Device ID (DID)                                             |
| 0b0011                                        | 2                                             | eTPU2 Development Control (NDI_eTPU2_DC)                    |
| 0b0011                                        | 4                                             | eTPU2 Development Status (NDEDI_eTPU2_DS)                   |
| 0b0000                                        | 7                                             | Read/Write Access Control/Status (RWCS)                     |
| 0b0000                                        | 9                                             | Read/Write Access Address (RWA)                             |
| 0b0000                                        | 10                                            | Read/Write Access Data (RWD)                                |
| 0b0011                                        | 11                                            | eTPU2 Watchpoint Trigger (NDI_eTPU2_WT)                     |
| 0b0011                                        | 13                                            | eTPU2 Data Trace Control (NDI_eTPU2_DTC)                    |
| 0b0011                                        | 22                                            | eTPU2 Breakpoint/Watchpoint Control 1 (NDEDI_eTPU2_BWC1)    |
| 0b0011                                        | 23                                            | eTPU2 Breakpoint/Watchpoint Control 2 (NDEDI_eTPU2_BWC2)    |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 25-2. NDI Registers (continued)

| Client Select                                   | Index                                           | Register                                                    |
|-------------------------------------------------|-------------------------------------------------|-------------------------------------------------------------|
| 0b0011                                          | 24                                              | eTPU2 Breakpoint/Watchpoint Control 3 (NDEDI_eTPU2_BWC3)    |
| 0b0011                                          | 30                                              | eTPU2 Breakpoint/Watchpoint Address 1 (NDEDI_eTPU2_BWA1)    |
| 0b0011                                          | 31                                              | eTPU2 Breakpoint/Watchpoint Address 2 (NDEDI_eTPU2_BWA2)    |
| 0b0011                                          | 38                                              | eTPU2 Breakpoint/Watchpoint Data 1 (NDEDI_eTPU2_BWD1)       |
| 0b0011                                          | 39                                              | eTPU2 Breakpoint/Watchpoint Data 1 (NDEDI_eTPU2_BWD2)       |
| 0b0011                                          | 64                                              | eTPU2 Program Trace Channel Enable (NDI_eTPU2_PTCE)         |
| 0b0011                                          | 69                                              | eTPU2 Microinstruction Debug Register (NDEDI_eTPU2_INST)    |
| 0b0011                                          | 70                                              | eTPU2 Microprogram Counter Debug Register (NDEDI_eTPU2_MPC) |
| 0b0011                                          | 71                                              | eTPU2 Channel Flag Status Register (NDEDI_eTPU2_CFSR)       |
| 0bxxxx                                          | 127                                             | Port Configuration Register (PCR)                           |
| eTPU CDC Control/Status Registers               | eTPU CDC Control/Status Registers               | eTPU CDC Control/Status Registers                           |
| 0b0100                                          | 13                                              | eTPU CDC Data Trace Control (NDEDI_CDC_DTC)                 |
| eTPU1/eTPU2/CDC Shared Control/Status Registers | eTPU1/eTPU2/CDC Shared Control/Status Registers | eTPU1/eTPU2/CDC Shared Control/Status Registers             |
| 0b0010 or 0b0011 or 0b0100                      | 65                                              | eTPU Data Trace Address Range 0 (eTPU_DTAR0)                |
| 0b0010 or 0b0011 or 0b0100                      | 66                                              | eTPU Data Trace Address Range 1 (eTPU_DTAR1)                |
| 0b0010 or 0b0011 0r 0b0100                      | 67                                              | eTPU Data Trace Address Range 2 (eTPU_DTAR2)                |
| 0b0010 or 0b0011 0r 0b0100                      | 68                                              | eTPU Data Trace Address Range 3 (eTPU_DTAR3)                |

Table 25-3. OnCE Register Addressing

| OCMD, RS[0:6]       | Register Selected             |
|---------------------|-------------------------------|
| 000 0000            | Reserved                      |
| 000 0001            | Reserved                      |
| 000 0010            | JTAG ID (read-only)           |
| 000 0011 - 000 1111 | Reserved                      |
| 001 0000            | CPU Scan Register (CPUSCR)    |
| 001 0001            | No Register Selected (Bypass) |
| 001 0010            | OnCE Control Register (OCR)   |
| 001 0011            | Reserved                      |
| 001 0100 - 001 1111 | Reserved                      |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 25-3. OnCE Register Addressing (continued)

| OCMD, RS[0:6]       | Register Selected                       |
|---------------------|-----------------------------------------|
| 010 0000            | Instruction Address Compare 1 (IAC1)    |
| 010 0001            | Instruction Address Compare 2 (IAC2)    |
| 010 0010            | Instruction Address Compare 3 (IAC3)    |
| 010 0011            | Instruction Address Compare 4 (IAC4)    |
| 010 0100            | Data Address Compare 1 (DAC1)           |
| 010 0101            | Data Address Compare 2 (DAC2)           |
| 010 0110            | Reserved                                |
| 010 0111            | Reserved                                |
| 010 1000 - 010 1011 | Reserved                                |
| 010 1100            | Debug Counter Register (DBCNT)          |
| 010 1101            | Debug PCFIFO (PCFIFO) (read-only)       |
| 010 1110 - 010 1111 | Reserved                                |
| 011 0000            | Debug Status Register (DBSR)            |
| 011 0001            | Debug Control Register 0 (DBCR0)        |
| 011 0010            | Debug Control Register 1 (DBCR1)        |
| 011 0011            | Debug Control Register 2 (DBCR2)        |
| 011 0100            | Debug Control Register 3 (DBCR3)        |
| 011 0101 - 101 1111 | Reserved (do not access)                |
| 111 0000 - 111 1011 | General Purpose Register Selects [0:11] |
| 111 1100            | Nexus3-Access                           |
| 111 1101            | LSRL Select                             |
| 111 1110            | Enable_OnCE (and Bypass)                |
| 111 1111            | Bypass                                  |

## 25.4 NDI Functional Description

## 25.4.1 Enabling Nexus Clients for TAP Access

Once the NDI is out of the reset state, the loading of a specific instruction in the JTAG controller (JTAGC) block is required to grant the NDI ownership of the TAP. Each Nexus client has its own JTAGC instruction opcode for ownership of the TAP, granting that client the means to read/write its registers. The JTAGC instruction opcode for each Nexus client is shown in Table 25-4. Once the JTAGC opcode for a client has been loaded, the client is enabled by loading its NEXUS-ENABLE instruction. The NEXUS-ENABLE

instruction  opcode  for  each  Nexus  client  is  listed  in  Table 25-5.  Opcodes  for  all  other  instructions supported by Nexus clients can be found in the relevant sections of this chapter.

Table 25-4. JTAG Client Select Instructions

| JTAGC Instruction    |   Opcode | Description                                      |
|----------------------|----------|--------------------------------------------------|
| ACCESS_AUX_TAP_NPC   |    10000 | Enables access to the NPC TAP controller         |
| ACCESS_AUX_TAP_ONCE  |    10001 | Enables access to the e200z6 OnCE TAP controller |
| ACCESS_AUX_TAP_eTPU  |    10010 | Enables access to the eTPU Nexus TAP controller  |
| ACCESS_AUX_TAP_DMAN3 |    10011 | Enables access to the eDMA Nexus TAP controller  |

Table 25-5. Nexus Client JTAG Instructions

| Instruction                            | Description                                              | Opcode                                 |
|----------------------------------------|----------------------------------------------------------|----------------------------------------|
| NPC JTAG Instruction Opcodes           | NPC JTAG Instruction Opcodes                             | NPC JTAG Instruction Opcodes           |
| NEXUS_ENABLE                           | Opcode for NPC Nexus Enable instruction (4-bits)         | 0x0                                    |
| BYPASS                                 | Opcode for the NPC BYPASS instruction (4-bits)           | 0xF                                    |
| e200z6 OnCE JTAG Instruction Opcodes 1 | e200z6 OnCE JTAG Instruction Opcodes 1                   | e200z6 OnCE JTAG Instruction Opcodes 1 |
| NEXUS3_ACCESS                          | Opcode for e200z6 OnCENexus Enable instruction (10-bits) | 0x7C                                   |
| BYPASS                                 | Opcode for the e200z6 OnCE BYPASS instruction (10-bits)  | 0x7F                                   |
| NDEDI JTAG Instruction Opcodes         | NDEDI JTAG Instruction Opcodes                           | NDEDI JTAG Instruction Opcodes         |
| NEXUS_ENABLE                           | Opcode for NDEDI Nexus Enable instruction (4-bits)       | 0x0                                    |
| BYPASS                                 | Opcode for the NDEDI BYPASS instruction (4-bits)         | 0xF                                    |
| eDMA Nexus JTAG Instruction Opcodes    | eDMA Nexus JTAG Instruction Opcodes                      | eDMA Nexus JTAG Instruction Opcodes    |
| NEXUS_ACCESS                           | Opcode for eDMA Nexus Enable instruction (4-bits)        | 0x0                                    |
| BYPASS                                 | Opcode for the eDMA Nexus BYPASS instruction (4-bits)    | 0xF                                    |

1 Refer to the e200Z6 Reference Manual  for a complete list of available OnCE instructions.

## 25.4.2 Configuring the NDI for Nexus Messaging

The NDI is placed in disabled mode upon exit of power-on reset. If message transmission via the auxiliary port is desired, a write to the port configuration register (PCR) located in the NPC is then required to enable the NDI and select the mode of operation. Asserting MCKO\_EN in the PCR places the NDI in enabled mode  and  enables  MCKO.  The  frequency  of  MCKO  is  selected  by  writing  the  MCKO\_DIV  field. Asserting or negating the FPM bit selects full-port or reduced-port mode, respectively. When writing to the PCR, the PCR lsb must be written to a logic 0. Setting the lsb of the PCR enables factory debug mode and prevents the transmission of Nexus messages.

Figure 25-6 describes the NDI configuration options.

Table 25-6. NDI Configuration Options

| JCOMP Asserted   | MCKO_EN bit of the Port Configuration Register   | FPM bit of the Port Configuration Register   | Configuration     |
|------------------|--------------------------------------------------|----------------------------------------------|-------------------|
| No               | X                                                | X                                            | Reset             |
| Yes              | 0                                                | X                                            | Disabled          |
| Yes              | 1                                                | 1                                            | Full-Port Mode    |
| Yes              | 1                                                | 0                                            | Reduced-Port Mode |

## 25.4.3 Programmable MCKO Frequency

MCKO is an output clock to the development tools used for the timing of MSEO and MDO pin functions. MCKO is derived from the system clock, and its frequency is determined by the value of the MCKO\_DIV field in the port configuration register (PCR) located in the NPC. Possible operating frequencies include one-half, one-quarter, and one-eighth system clock speed.

Figure 25-7  shows  the  MCKO\_DIV  encodings.  In  this  table,  SYS\_CLK  represents  the  system  clock frequency. The default value selected if a reserved encoding is programmed is SYS\_CLK/2.

Table 25-7. MCKO\_DIV Values

| MCKO_DIV[2:0]   | MCKO Frequency   |
|-----------------|------------------|
| 0b000           | Reserved         |
| 0b001           | SYS_CLK/2        |
| 0b010           | Reserved         |
| 0b011           | SYS_CLK/4        |
| 0b100           | Reserved         |
| 0b101           | Reserved         |
| 0b110           | Reserved         |
| 0b111           | SYS_CLK/8        |

## 25.4.4 Nexus Messaging

Most of the messages transmitted by the NDI include a SRC field. This field is used to identify which source generated the message. Figure 25-8 shows the values used for the SRC field by the different clients on the MPC5553/MPC5554. These 4-bit values are specific to the MPC5553/MPC5554.  The same values are used for the client select values written to the client select control register.

Table 25-8. SRC Packet Encodings

| SRC[3:0]   | Client              |
|------------|---------------------|
| 0b0000     | e200z6              |
| 0b0001     | eDMA                |
| 0b0010     | eTPU1 (ENGINE1_SRC) |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 25-8. SRC Packet Encodings

| SRC[3:0]      | Client                |
|---------------|-----------------------|
| 0b0011        | eTPU2 (ENGINE2_SRC) 1 |
| 0b0100        | eTPU CDC 2 (CDC_SRC)  |
| 0b0101-0b1111 | Reserved              |

1 MPC5554 only, not in the MPC5553.

2 CDC is the eTPU Coherent Dual-Parameter Controller. Refer to the eTPU Reference Manual for more information.

## 25.4.5 System Clock Locked Indication

Following a power-on reset, the lsb of the auxiliary output port pins (MDO0) can be monitored to provide the lock status of the system clock. MDO0 is driven to a logic 1 until the system clock achieves lock after exiting power-on reset. Once the system clock is locked, MDO0 is negated and tools may begin Nexus configuration. Loss of lock conditions that occur subsequent to the exit of power-on reset and the initial lock of the system clock do not cause a Nexus reset, and therefore do not result in MDO0 driven high.

## 25.5 Nexus Port Controller (NPC)

The  Nexus  port  controller  (NPC)  is  that  part  of  the  NDI  that  controls  access  and  arbitration  of  the MPC5553/MPC5554's internal Nexus modules. The NPC contains the port configuration register (PCR) and the device identification register (DID). The contents of the DID are the same as the JTAGC device identification register.

## 25.5.1 Overview

The MPC5553/MPC5554 incorporates multiple modules that require development support. Each of these modules implements a development interface based on the IEEE-ISTO 5001-2001 standard and must share the input and output ports that interface with the development tool. The NPC controls the usage of these  ports  in  a  manner  that  allows  the  individual  modules  to  share  the  ports,  while  appearing  to  the development tool as a single module.

## 25.5.2 Features

The NPC performs the following functions:

- · Controls arbitration for ownership of the Nexus auxiliary output port
- · Nexus device identification register and messaging
- · Generates MCKO enable and frequency division control signals
- · Controls sharing of EVTO
- · Control of the device-wide debug mode
- · Generates asynchronous reset signal for Nexus modules based on JCOMP input,  censorship status, and power-on reset status
- · System clock locked status indication via MDO0 during Nexus reset
- · Provides Nexus support for censorship mode

## 25.6 Memory Map/Register Definition

This section provides a detailed description of the NPC registers accessible to the end user. Individual bit-level descriptions and reset states of the registers are included.

## 25.6.1 Memory Map

Table 25-9 shows the NPC registers by index values. The registers are not memory-mapped and can only be accessed via the TAP. The NPC does not implement the client select control register because the value does not matter when accessing the registers. Note that the bypass register (refer to Section 25.6.2.1) and instruction register (refer to Section 25.6.2.2) have no index values. These registers are not accessed in the same manner as Nexus client registers.

Table 25-9. NPC Memory Map

|   Index | Register Name   | Register Description        |   Size (bits) |
|---------|-----------------|-----------------------------|---------------|
|       0 | DID             | Device ID register          |            32 |
|     127 | PCR             | Port configuration register |            32 |

## 25.6.2 Register Descriptions

This section consists of NPC register descriptions. Additional information regarding  references to the TAP controller state may be found in Section 24.4.3, 'TAP Controller State Machine.'

## 25.6.2.1 Bypass Register

The bypass register is a single-bit shift register path selected for serial data transfer between TDI and TDO when  the  BYPASS  instruction  or  any  unimplemented  instructions  are  active.  After  entry  into  the Capture-DR state, the single-bit shift register is set to a logic 0. Therefore, the first bit shifted out after selecting the bypass register is always a logic 0.

## 25.6.2.2 Instruction Register

The NPC uses a 4-bit instruction register as shown in Figure 25-2. The instruction register is accessed via the SELECT\_IR\_SCAN path of the tap controller state machine, and allows instructions to be loaded into the module to enable the NPC for register access (NEXUS\_ENABLE) or select the bypass register as the shift path from TDI to TDO (BYPASS or unimplemented instructions).

Instructions are shifted in through TDI while the TAP controller is in the Shift-IR state, and latched on the falling edge of TCK in the Update-IR state. The latched instruction value can only be changed in the Update-IR  and  test-logic-reset  TAP  controller  states.  Synchronous  entry  into  the  test-logic-reset  state results in synchronous loading of the BYPASS instruction. Asynchronous entry into the test-logic-reset state results in asynchronous loading of the BYPASS instruction. During the Capture-IR TAP controller state, the instruction register is loaded with the value of the previously executed instruction, making this value the register's read value when the TAP controller is sequenced into the Shift-IR state.

Figure 25-2. 4-Bit Instruction Register

<!-- image -->

|        | 3                               | 2                               |
|--------|---------------------------------|---------------------------------|
| R      | Previous Instruction Opcode     | Previous Instruction Opcode     |
| W      | Instruction Opcode              | Instruction Opcode              |
| Reset: | BYPASS Instruction Opcode (0xF) | BYPASS Instruction Opcode (0xF) |

## 25.6.2.3 Nexus Device ID Register (DID)

The NPC device identification register, shown in Figure 25-3, allows the part revision number, design center, part identification number, and manufacturer identity code of the part to be determined through the auxiliary output port.

Figure 25-3. Nexus Device ID Register (DID)

|                   | 31   | 30   | 29   | 28   | 27   | 26   | 25   | 24   | 23   | 22   | 21   | 20   | 19   | 18   | 17   | 16   |
|-------------------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| R                 | PRN  | PRN  | PRN  |      | DC   | DC   | DC   | DC   | DC   | DC   | PIN  | PIN  | PIN  | PIN  | PIN  | PIN  |
| W                 |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |
| Reset for MPC5553 | 0    | 0    | 0    | 0    | 1    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 1    | 0    | 1    |
| Reset for MPC5554 | 0    | 0    | 0    | 1    | 1    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |
| Reg Index         | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |
|                   | 15   | 14   | 13   | 12   | 11   | 10   | 9    | 8    | 7    | 6    | 5    | 4    | 3    | 2    | 1    | 0    |
| R                 | PIN  | PIN  | PIN  | PIN  | MIC  | MIC  | MIC  | MIC  | MIC  | MIC  | MIC  | MIC  | MIC  | MIC  | MIC  | 1    |
| W                 |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |
| Reset for MPC5553 | 0    | 0    | 1    | 1    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 1    | 1    | 1    | 0    | 1    |
| Reset for MPC5554 | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 1    | 1    | 1    | 0    | 1    |
| Reg Index         | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |

## Table 25-10. DID Register Field Descriptions

| Bits   | Name   | Description                                                                                                                     |
|--------|--------|---------------------------------------------------------------------------------------------------------------------------------|
| 31-28  | PRN    | Part revision number. Contains the revision number of the part. This field changes with each revision of the device or module.  |
| 27-22  | DC     | Design center. Indicates the Freescale design center. For both the MPC5554 and MPC5553, this value is 0x20.                     |
| 21-12  | PIN    | Part identification number. Contains the part number of the device. The PIN for the MPC5553 is 0x53, for the MPC5554 it is 0x0. |

Table 25-10. DID Register Field Descriptions (continued)

| Bits   | Name   | Description                                                                                                               |
|--------|--------|---------------------------------------------------------------------------------------------------------------------------|
| 11-1   | MIC    | Manufacturer identity code. Contains the reduced Joint Electron Device Engineering Council (JEDEC) ID for Freescale, 0xE. |
| 0      | -      | Fixed per JTAG 1149.1 1 Always set                                                                                        |

## 25.6.2.4 Port Configuration Register (PCR)

The PCR, shown in Figure 25-4, is used to select the NPC mode of operation, enable MCKO and select the MCKO frequency, and enable or disable MCKO gating. This register should be configured as soon as the NPC is enabled.

## NOTE

The mode (MCKO\_GT) or clock division (MCKO\_DIV) bits  must not be modified  after  MCKO  has  been  enabled.  Changing  the  mode  or  clock division while MCKO is enabled can produce unpredictable results.

Figure 25-4. Port Configuration Register (PCR)

|           | 31   | 30       | 29       | 28   | 27       | 26   | 25   | 24   | 23   | 22   | 21   | 20   | 19   | 18   | 17   | 16    |
|-----------|------|----------|----------|------|----------|------|------|------|------|------|------|------|------|------|------|-------|
| R         | FPM  | MCKO_ GT | MCKO_ EN |      | MCKO_DIV |      | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0     |
| W         |      |          |          |      |          |      |      |      |      |      |      |      |      |      |      |       |
| Reset     | 0    | 0        | 0        | 0    | 0        | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0     |
| Reg Index | 127  | 127      | 127      | 127  | 127      | 127  | 127  | 127  | 127  | 127  | 127  | 127  | 127  | 127  | 127  | 127   |
|           | 15   | 14       | 13       | 12   | 11       | 10   | 9    | 8    | 7    | 6    | 5    | 4    | 3    | 2    | 1    | 0     |
| R         | 0    | 0        | 0        | 0    | 0        | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | PSTAT |
| W         |      |          |          |      |          |      |      |      |      |      |      |      |      |      |      | _EN   |
| Reset     | 0    | 0        | 0        | 0    | 0        | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0     |
| Reg Index | 127  | 127      | 127      | 127  | 127      | 127  | 127  | 127  | 127  | 127  | 127  | 127  | 127  | 127  | 127  | 127   |

Table 25-11. PCR Field Descriptions

|   Bits | Name    | Description                                                                                                                                                                                                                                                                                                                                                                                            |
|--------|---------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|     31 | FPM     | Full port mode. Determines if the auxiliary output port uses the full MDOport or a reduced MDO port to transmit messages. 0 The subset of MDO[3:0] pins are used to transmit messages. 1 All MDO[11:0] pins are used to transmit messages.                                                                                                                                                             |
|     30 | MCKO_GT | MCKO clock gating control. Enables or disables MCKO clock gating. If clock gating is enabled, the MCKO clock is gated when the NPC is in enabled mode but not actively transmitting messages on the auxiliary output port. When clock gating is disabled, MCKO is allowed to run even if no auxiliary output port messages are being transmitted. 0 MCKO gating is disabled. 1 MCKO gating is enabled. |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## Table 25-11. PCR Field Descriptions (continued)

| Bits   | Name           | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
|--------|----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 29     | MCKO_EN        | MCKO enable. Enables the MCKO clock. When enabled, the frequency of MCKO is determined by the MCKO_DIV field. 0 MCKO clock is driven to zero. 1 MCKO clock is enabled.                                                                                                                                                                                                                                                                                                                 | MCKO enable. Enables the MCKO clock. When enabled, the frequency of MCKO is determined by the MCKO_DIV field. 0 MCKO clock is driven to zero. 1 MCKO clock is enabled.                                                                                                                                                                                                                                                                                                                 |
| 28-26  | MCKO_DIV [2:0] | MCKO division factor. Determines the frequency of MCKO relative to the system clock frequency when MCKO_EN is asserted. The table below shows the meaning of MCKO_DIV values. In this table, SYS_CLK represents the system clock frequency.                                                                                                                                                                                                                                            | MCKO division factor. Determines the frequency of MCKO relative to the system clock frequency when MCKO_EN is asserted. The table below shows the meaning of MCKO_DIV values. In this table, SYS_CLK represents the system clock frequency.                                                                                                                                                                                                                                            |
|        |                |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | MCKO_DIV[2:0]                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
|        |                |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | 0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
|        |                |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | 1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
|        |                |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | 2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
|        |                |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | 3                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
|        |                |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | 4                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
|        |                |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | 5                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
|        |                |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | 6                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
|        |                |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | 7                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| 25-1   | -              | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| 0      | PSTAT_EN       | Processor status mode enable. Enables processor status (PSTAT) mode. In PSTAT mode, all auxiliary output port MDO pins are used to transmit processor status information, and Nexus messaging is unavailable. 0 PSTAT mode disabled 1 PSTAT mode enabled Note: PSTAT mode is intended for factory processor debug only. The PSTAT_EN bit should be written to disable PSTAT mode by the customer. No Nexus messages are transmitted under any circumstances when PSTAT mode is enabled | Processor status mode enable. Enables processor status (PSTAT) mode. In PSTAT mode, all auxiliary output port MDO pins are used to transmit processor status information, and Nexus messaging is unavailable. 0 PSTAT mode disabled 1 PSTAT mode enabled Note: PSTAT mode is intended for factory processor debug only. The PSTAT_EN bit should be written to disable PSTAT mode by the customer. No Nexus messages are transmitted under any circumstances when PSTAT mode is enabled |

## 25.7 NPC Functional Description

## 25.7.1 NPC Reset Configuration

The NPC is placed in disabled mode upon exit of reset. If message transmission via the auxiliary port is desired, a write to the PCR is then required to enable the NPC and select the mode of operation. Asserting MCKO\_EN places the NPC in enabled mode and enables MCKO. The frequency of MCKO is selected by writing the MCKO\_DIV field. Asserting or negating the FPM bit selects full-port or reduced-port mode, respectively.

Table 25-12 describes the NPC reset configuration options.

Table 25-12. NPC Reset Configuration Options

| JCOMP Asserted?   | PCR[MCKO_EN]   | PCR[FPM]   | Configuration   |
|-------------------|----------------|------------|-----------------|
| No                | X              | X          | Reset           |
| Yes               | 0              | X          | Disabled        |

Table 25-12. NPC Reset Configuration Options  (continued)

| JCOMP Asserted?   |   PCR[MCKO_EN] |   PCR[FPM] | Configuration     |
|-------------------|----------------|------------|-------------------|
| Yes               |              1 |          1 | Full-Port Mode    |
| Yes               |              1 |          0 | Reduced-Port Mode |

## 25.7.2 Auxiliary Output Port

The auxiliary output port is shared by each of the Nexus modules on the device. The NPC communicates with each of the individual modules and arbitrates for access to the port. Additional information about the auxiliary port is found in Section 25.2, 'External Signal Description.'

## 25.7.2.1 Output Message Protocol

The protocol for transmitting messages via the auxiliary port is accomplished with the MSEO functions. The MSEO pins are used to signal the end of variable-length packets and the end of messages. They are not required to indicate the end of fixed-length packets. MDO and MSEO are sampled on the rising edge of MCKO.

Figure 25-5 illustrates the state diagram for MSEO transfers. All transitions not included in the figure are reserved, and must not be used.

Figure 25-5. MSEO Transfers

<!-- image -->

## 25.7.2.2 Output Messages

In addition to sending out messages generated in other Nexus modules, the NPC can also output the device ID message contained in the device ID register on the MDO pins. The device ID message can also be sent out serially through TDO.

Table 25-13 describes the device ID message that the NPC can transmit on the auxiliary port. The TCODE is the first packet transmitted.

Table 25-13. NPC Output Messages

| Message Name      |   Min. Packet Size (bits) |   MaxPacket Size (bits) | Packet Type   | Packet Name   | Packet Description    |
|-------------------|---------------------------|-------------------------|---------------|---------------|-----------------------|
| Device ID Message |                         6 |                       6 | Fixed         | TCODE         | Value = 1             |
| Device ID Message |                        32 |                      32 | Fixed         | ID            | DID register contents |

Figure 25-6 shows the various message formats that the pin interface formatter has to encounter.

Figure 25-6. Message Field Sizes

| Message           |   TCODE | Field #1   | Field #2   | Field #3   | Field #4   | Field #5   |   Min. Size 1 (bits) |   Max Size 2 (bits) |
|-------------------|---------|------------|------------|------------|------------|------------|----------------------|---------------------|
| Device ID Message |       1 | Fixed = 32 | NA         | NA         | NA         | NA         |                   38 |                  38 |

1 Minimum information size. The actual number of bits transmitted depends on the number of MDO pins

2 Maximum information size. The actual number of bits transmitted depends on the number of MDO pins

The double edges in Figure 25-6 indicate the starts and ends of messages. Fields without shaded areas between  them  are  grouped  into  super-fields  and  can  be  transmitted  together  without  end-of-packet indications between them.

## 25.7.2.2.1 Rules of Messages

The rules of messages include the following:

- · A variable-sized field within a message must end on a port boundary. (Port boundaries depend on the number of MDO pins active with the current reset configuration.)
- · A variable-sized field may start within a port boundary only when following a fixed-length field.
- · Super-fields must end on a port boundary.
- · When a variable-length field is sized such that it does not end on a port boundary, it is necessary to extend and zero fill the remaining bits after the highest order bit so that it can end on a port boundary.
- · Multiple fixed-length packets may start and/or end on a single clock.
- · When any packet follows a variable-length packet, it must start on a port boundary.
- · The field containing the TCODE number is always transferred out first, followed by subsequent fields of information.
- · Within a field, the lowest significant bits are shifted out first. Figure 25-7 shows the transmission sequence of a message that is made up of a TCODE followed by three fields.

Figure 25-7. Transmission Sequence of Messages

<!-- image -->

## 25.7.2.3 IEEE ® 1149.1-2001 (JTAG) TAP

The NPC uses the IEEE ® 1149.1-2001 TAP for accessing registers. Each of the individual Nexus modules on the device implements a TAP controller for accessing its registers as well. TAP signals include TCK, TDI, TMS, and TDO. Detailed information about the TAP controller state machine may be found in Section 24.4.3, 'TAP Controller State Machine.'

The IEEE ® 1149.1-2001 specification may be ordered for further detail on electrical and pin protocol compliance requirements.

The NPC implements a Nexus controller state machine that transitions based on the state of the IEEE ® 1149.1-2001 state machine shown in Figure 25-5. The Nexus controller state machine is defined by the IEEE-ISTO 5001-2003 standard. It is shown in Figure 25-9.

The instructions implemented by the NPC TAP controller are listed in Table 25-14. The value of the NEXUS-ENABLE  instruction  is  0b0000.  Each  unimplemented  instruction  acts  like  the  BYPASS instruction. The size of the NPC instruction register is 4-bits.

Table 25-14. Implemented Instructions

| Instruction Name   | Private/Public   | Opcode   | Description                                                                       |
|--------------------|------------------|----------|-----------------------------------------------------------------------------------|
| NEXUS-ENABLE       | Public           | 0x0      | Activate Nexus controller state machine to read and write NPC registers.          |
| BYPASS             | Private          | 0xF      | NPC BYPASS instruction. Also the value loaded into the NPC IR upon exit of reset. |

Data is shifted between TDI and TDO starting with the least significant bit as illustrated in Figure 25-8. This applies for the instruction register and all Nexus tool-mapped registers.

Figure 25-8. Shifting Data Into a Register

<!-- image -->

## 25.7.2.3.1 Enabling the NPC TAP Controller

Assertion of the power-on reset signal, entry into censored mode, or negating JCOMP resets the NPC TAP controller. When not in power-on reset or censored mode, the NPC TAP controller is enabled by asserting JCOMP  and loading the ACCESS\_AUX\_TAP\_NPC  instruction in the JTAGC. Loading the NEXUS-ENABLE instruction then grants access to NPC registers.

## 25.7.2.3.2 Retrieving Device IDCODE

The  Nexus  TAP  controller  does  not  implement  the  IDCODE  instruction.  However,  the  device identification message can be output by the NPC through the auxiliary output port or shifted out serially by accessing the NPC device ID register through the TAP. If the NPC is enabled, transmission of the device identification message on the auxiliary output port MDO pins occurs immediately after a write to the PCR. Transmission of the device identification message serially through TDO is achieved by performing a read of the register contents as described in Section 25.7.2.3.4.

## 25.7.2.3.3 Loading NEXUS-ENABLE Instruction

Access to the NPC registers is enabled by loading the NPC NEXUS-ENABLE instruction when NPC has ownership of the TAP. This instruction is shifted in via the SELECT-IR-SCAN path and loaded in the UPDATE-IR state. At this point, the Nexus controller state machine, shown in Figure 25-9, transitions to the  REG\_SELECT state. The Nexus controller has three states:  idle,  register  select,  and  data  access. Table 25-15 illustrates the IEEE ® 1149.1 sequence to load the NEXUS-ENABLE instruction.

Figure 25-9. NEXUS Controller State Machine

<!-- image -->

Table 25-15. Loading NEXUS-ENABLE Instruction

| Clock   | TDI   |   TMS | IEEE ® 1149.1 State   | Nexus State   | Description                                                                                                                     |
|---------|-------|-------|-----------------------|---------------|---------------------------------------------------------------------------------------------------------------------------------|
| 0       | -     |     0 | RUN-TEST/IDLE         | IDLE          | IEEE 1149.1-2001 TAP controller in idle state                                                                                   |
| 1       | -     |     1 | SELECT-DR-SCAN        | IDLE          | Transitional state                                                                                                              |
| 2       | -     |     1 | SELECT-IR-SCAN        | IDLE          | Transitional state                                                                                                              |
| 3       | -     |     0 | CAPTURE-IR            | IDLE          | Internal shifter loaded with current instruction                                                                                |
| 4       | -     |     0 | SHIFT-IR              | IDLE          | TDO becomes active, and the IEEE ® 1149.1-2001 shifter is ready. Shift in all but the last bit of the NEXUS_ENABLE instruction. |
| 5-7     | 0     |     0 | 3 TCKS in SHIFT-IR    | IDLE          | TDO becomes active, and the IEEE ® 1149.1-2001 shifter is ready. Shift in all but the last bit of the NEXUS_ENABLE instruction. |
| 8       | 0     |     1 | EXIT1-IR              | IDLE          | Last bit of instruction shifted in                                                                                              |
| 9       | -     |     1 | UPDATE-IR             | IDLE          | NEXUS-ENABLE loaded into instruction register                                                                                   |
| 10      | -     |     0 | RUN-TEST/IDLE         | REG_SELECT    | Ready to be read/write Nexus registers                                                                                          |

## 25.7.2.3.4 Selecting a Nexus Client Register

When  the  NEXUS-ENABLE  instruction  is  decoded  by  the  TAP  controller,  the  input  port  allows development tool access to all Nexus registers. Each register has a 7-bit address index.

All  register  access  is  performed  via  the  SELECT-DR-SCAN  path  of  the  IEEE ® 1149.1-2001  TAP controller  state  machine.  The  Nexus  controller  defaults  to  the  REG\_SELECT  state  when  enabled. Accessing a register requires two passes through the SELECT-DR-SCAN path: one pass to select the register and the second pass to read/write the register.

The first pass through the SELECT-DR-SCAN path is used to enter an 8-bit Nexus command consisting of  a  read/write  control  bit  in  the  lsb  followed  by  a  7-bit  register  address  index,  as  illustrated  in Figure 25-10. The read/write control bit is set to 1 for writes and 0 for reads.

| msb                  | lsb   |
|----------------------|-------|
| 7-bit register index | R/W   |

## Figure 25-10. IEEE ® 1149.1 Controller Command Input

The second pass through the SELECT-DR-SCAN path is used to read or write the register data by shifting in the data (lsb first) during the SHIFT-DR state. When reading a register, the register value is loaded into the IEEE ® 1149.1-2001 shifter during the CAPTURE-DR state. When writing a register, the value is loaded from the IEEE ® 1149.1-2001 shifter to the register during the UPDATE-DR state. When reading a register, there is no requirement to shift out the entire register contents. Shifting may be terminated once the required number of bits have been acquired.

Table 25-16 illustrates a sequence that writes a 32-bit value to a register.

Table 25-16. Write to a 32-Bit Nexus Client Register

| Clock   | TMS     | IEEE 1149.1 State   | Nexus State   | Description                                                                                          |
|---------|---------|---------------------|---------------|------------------------------------------------------------------------------------------------------|
| 0       | 0       | RUN-TEST/IDLE       | REG_SELECT    | IEEE 1149.1-2001 TAP controller in idle state                                                        |
| 1       | 1       | SELECT-DR-SCAN      | REG_SELECT    | First pass through SELECT-DR-SCAN path                                                               |
| 2       | 0       | CAPTURE-DR          | REG_SELECT    | Internal shifter loaded with current value of controller command input.                              |
| 3       | 0       | SHIFT-DR            | REG_SELECT    | TDO becomes active, and write bit and 6 bits of register index shifted in.                           |
| 7 TCKs  | 7 TCKs  | 7 TCKs              | 7 TCKs        | TDO becomes active, and write bit and 6 bits of register index shifted in.                           |
| 11      | 1       | EXIT1-DR            | REG_SELECT    | Last bit of register index shifted into TDI                                                          |
| 12      | 1       | UPDATE-DR           | REG_SELECT    | Controller decodes and selects register                                                              |
| 13      | 1       | SELECT-DR-SCAN      | DATA_ACCESS   | Second pass through SELECT-DR-SCAN path                                                              |
| 14      | 0       | CAPTURE-DR          | DATA_ACCESS   | Internal shifter loaded with current value of register                                               |
| 15      | 0       | SHIFT-DR            | DATA_ACCESS   | TDO becomes active, and outputs current value of register while new value is shifted in through TDI  |
| 31 TCKs | 31 TCKs | 31 TCKs             | 31 TCKs       | TDO becomes active, and outputs current value of register while new value is shifted in through TDI  |
| 47      | 1       | EXIT1-DR            | DATA_ACCESS   | Last bit of current value shifted out TDO. Last bit of new value shifted in TDI.                     |
| 48      | 1       | UPDATE-DR           | DATA_ACCESS   | Value written to register                                                                            |
| 49      | 0       | RUN-TEST/IDLE       | REG_SELECT    | Controller returned to idle state. It could also return to SELECT-DR-SCAN to write another register. |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## 25.7.2.4 Nexus Auxiliary Port Sharing

Each of the Nexus modules on the MCU implements a request/grant scheme to arbitrate for control of the Nexus auxiliary port when Nexus data is ready to be transmitted.

All  modules  arbitrating  for  the  port  are  given  fixed  priority  levels  relative  to  each  other.  If  multiple modules have the same request level, this priority level is used as a tie-breaker. To avoid monopolization of the port, the module given the highest priority level alternates following each grant. Immediately out of reset the order of priority, from highest to lowest, is: NPC, NZ6C3, NDEDI, and NXDM. This arbitration mechanism is controlled internally and is not programmable by tools or the user.

## 25.7.2.5 Nexus JTAG Port Sharing

Each  of  the  individual  Nexus  modules  on  the  device  implements  a  TAP  controller  for  accessing  its registers. When JCOMP is asserted, only the module whose ACCESS\_AUX\_TAP instruction is loaded has control of the TAP (See Section 24.4.4, 'JTAGC Instructions'). This allows the interface to all of these individual TAP controllers to appear to be a single port from outside the device. Once a Nexus module has ownership of the TAP, that module acts like a single-bit shift register, or bypass register, if no register is selected as the shift path.

## 25.7.2.6 MCKO

MCKO is an output clock to the development tools used for the timing of MSEO and MDO pin functions. MCKO  is  derived  from  the  system  clock  and  its  frequency  is  determined  by  the  value  of  the MCKO\_DIV[2:0] field in the PCR. Possible operating frequencies include one-half, one-quarter,  and one-eighth system clock speed. MCKO is enabled by setting the MCKO\_EN bit in the PCR.

The NPC also controls dynamic MCKO clock gating when in full- or reduced-port modes. The setting of the  MCKO\_GT bit inside the PCR determines whether or not MCKO gating control is enabled. The MCKO\_GT bit resets to a logic 0. In this state gating of MCKO is disabled. To enable gating of MCKO, the MCKO\_GT bit in the PCR is written to a logic 1. When MCKO gating is enabled, MCKO is driven to a logic 0 if the auxiliary port is enabled but not transmitting messages and there are no pending messages from Nexus clients.

## 25.7.2.7 EVTO Sharing

The NPC controls sharing of the EVTO output between all Nexus clients that produce an EVTO signal. EVTO is driven for one MCKO period whenever any module drives its EVTO. When there is no active MCKO, such as in disabled mode, the NPC assumes an MCKO frequency of one-half system clock speed when driving EVTO. EVTO sharing is active as long as the NPC is not in reset.

## 25.7.2.8 Nexus Reset Control

The JCOMP input that is used as the primary reset signal for the NPC is also used by the NPC to generate a single-bit reset signal for other Nexus modules. If JCOMP is negated, an internal reset signal is asserted, indicating that all Nexus modules should be held in reset. This internal reset signal is also asserted during a power-on reset, or if nex\_disable is asserted, indicating the device is in censored mode. This single bit reset signal functions much like the IEEE ® 1149.1-2001 defined TRST signal and allows JCOMP reset information to be provided to the Nexus modules without each module having to sense the JCOMP signal directly or monitor the status of censored mode.

## 25.8 NPC Initialization/Application Information

## 25.8.1 Accessing NPC Tool-Mapped Registers

To initialize the TAP for NPC register accesses, the following sequence is required:

- 1. Enable the NPC TAP controller. This is achieved by asserting JCOMP and loading the ACCESS\_AUX\_TAP\_NPC instruction in the JTAGC.
- 2. Load the TAP controller with the NEXUS-ENABLE instruction.

To write control data to NPC tool-mapped registers, the following sequence is required:

- 1. Write the 7-bit register index and set the write bit to select the register with a pass through the SELECT-DR-SCAN path in the TAP controller state machine.
- 2. Write the register value with a second pass through the SELECT-DR-SCAN path. Note that the prior value of this register is shifted out during the write.

To read status and control data from NPC tool-mapped registers, the following sequence is required:

- 1. Write the 7-bit register index and clear the write bit to select register with a pass through SELECT-DR-SCAN path in the TAP controller state machine.
- 2. Read the register value with a second pass through the SELECT-DR-SCAN path. Data shifted in is ignored.

See the IEEE ® -ISTO 5001-2003 standard for more detail.

## 25.9 Nexus Dual eTPU Development Interface (NDEDI)

The enhanced timing processor unit (eTPU) has its own Nexus class 3 interface, the Nexus dual eTPU development  interface  (NDEDI).  The  two  (MPC5554)  eTPU  engines  and  a  coherent  dual  parameter controller  (CDC) appear as three separate Nexus clients. Refer to the Enhanced Time Processor Unit Reference Manual for more information about the NDEDI module.

Figure 25-11. NDEDI Device ID Register (DID)

<!-- image -->

|                   | 31   | 30   | 29   | 28   | 27   | 26   | 25   | 24   | 23   | 22   | 21   | 20   | 19   | 18   | 17   | 16   |
|-------------------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| R                 | PRN  | PRN  | PRN  |      | DC   | DC   | DC   | DC   | DC   | DC   | PIN  | PIN  | PIN  | PIN  | PIN  | PIN  |
| W                 |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |
| Reset for MPC5553 | 0    | 0    | 0    | 1    | 1    | 0    | 0    | 0    | 0    | 0    | 0    | 1    | 0    | 0    | 1    | 0    |
| Reset for MPC5554 | 0    | 0    | 0    | 1    | 1    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |
| Reg Index         | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |
|                   | 15   | 14   | 13   | 12   | 11   | 10   | 9    | 8    | 7    | 6    | 5    | 4    | 3    | 2    | 1    | 0    |
| R                 | PIN  | PIN  | PIN  | PIN  | MIC  | MIC  | MIC  | MIC  | MIC  | MIC  | MIC  | MIC  | MIC  | MIC  | MIC  | 1    |
| W                 |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |
| Reset for MPC5553 | 0    | 1    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 1    | 1    | 1    | 0    | 1    |
| Reset for MPC5554 | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 1    | 1    | 1    | 0    | 1    |
| Reg Index         | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |

Table 25-17. NDEDI DID Register Field Descriptions

| Bits   | Name   | Description                                                                                                                    |
|--------|--------|--------------------------------------------------------------------------------------------------------------------------------|
| 31-28  | PRN    | Part revision number. Contains the revision number of the part. This field changes with each revision of the device or module. |
| 27-22  | DC     | Design center. Indicates the Freescale design center. For both the MPC5554 and MPC5553, this value is 0x20.                    |
| 21-12  | PIN    | Part identification number. Contains the part number of the device.                                                            |
| 11-1   | MIC    | Manufacturer identity code. Contains the reduced Joint Electron Device Engineering Council (JEDEC) ID for Freescale, 0xE.      |
| 0      | -      | Fixed per JTAG 1149.1 1 Always set                                                                                             |

## 25.10 e200z6 Class 3 Nexus Module (NZ6C3)

The NZ6C3 module provides real-time development capabilities for the MPC5553/MPC5554 core in compliance  with  the  IEEE ® -ISTO  Nexus  5001-2003  standard.  This  module  provides  development support capabilities without requiring the use of address and data pins for internal visibility.

## 25.10.1 Introduction

This section defines the auxiliary pin functions, transfer protocols and standard development features of the  NZ6C3  module.  The  development  features  supported  are  Program  trace,  data  trace,  watchpoint messaging, ownership trace, and read/write access via the JTAG interface.

## NOTE

Throughout this section references are made to the auxiliary port and its specific signals, such as MCKO, MSEO[0:1], MDO[11:0] and others. In actual use the MPC5553/MPC5554 NPC module arbitrates the access of the single  auxiliary  port.  To  simplify  the  description  of  the  function  of  the NZ6C3 module, the interaction  of  the  NPC  is  omitted  and  the  behavior described  as  if  the  module  has  its  own  dedicated  auxiliary  port.  The auxiliary port is fully described in Section 25.2, 'External Signal Description,' on page 25-5.

## 25.10.2 Block Diagram

<!-- image -->

- Nexus1 Module (within e200z6 CPU)

Figure 25-12. e200z6 Nexus3 Functional Block Diagram

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## 25.10.3 Overview

Table 25-18 contains a set of terms and definitions associated with the NZ6C3 module.

Table 25-18. Terms and Definitions

| Term                          | Description                                                                                                                                                                                                                                           |
|-------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| IEEE ® -ISTO 5001             | Consortium and standard for real-time embedded system design. World wide Web documentation at http://www.ieee-isto.org/Nexus5001                                                                                                                      |
| Auxiliary Port                | Refers to Nexus auxiliary port. Used as auxiliary port to the IEEE ® 1149.1 JTAG interface.                                                                                                                                                           |
| Branch Trace Messaging (BTM)  | Visibility of addresses for taken branches and exceptions, and the number of sequential instructions executed between each taken branch.                                                                                                              |
| Client                        | A functional block on an embedded processor which requires development visibility and controllability. Examples are a central processing unit (CPU) or an intelligent peripheral.                                                                     |
| Data Read Message (DRM)       | External visibility of data reads to memory-mapped resources.                                                                                                                                                                                         |
| Data Write Message (DWM)      | External visibility of data writes to memory-mapped resources.                                                                                                                                                                                        |
| Data Trace Messaging (DTM)    | External visibility of how data flows through the embedded system. This may include DRM and/or DWM.                                                                                                                                                   |
| JTAG Compliant                | Device complying to IEEE ® 1149.1 JTAG standard                                                                                                                                                                                                       |
| JTAG IR & DR Sequence         | JTAG instruction register (IR) scan to load an opcode value for selecting a development register. The JTAG IR corresponds to the OnCE command register (OCMD). The selected development register is then accessed via a JTAG data register (DR) scan. |
| Nexus1                        | The e200z6 (OnCE) debug module. This module integrated with each e200z6 processor provides all static (core halted) debug functionality. This module is compliant with Class1 of the IEEE ® -ISTO 5001 standard.                                      |
| Ownership Trace Message (OTM) | Visibility of process/function that is currently executing.                                                                                                                                                                                           |
| Public Messages               | Messages on the auxiliary pins for accomplishing common visibility and controllability requirements                                                                                                                                                   |
| Standard                      | The phrase 'according to the standard' is used to indicate according to the IEEE ® -ISTO 5001 standard.                                                                                                                                               |
| Transfer Code (TCODE)         | Message header that identifies the number and/or size of packets to be transferred, and how to interpret each of the packets.                                                                                                                         |
| Watchpoint                    | A data or instruction breakpoint which does not cause the processor to halt. Instead, a pin is used to signal that the condition occurred. A watchpoint message is also generated.                                                                    |

## 25.10.4 Features

The NZ6C3 module is compliant with Class 3 of the IEEE ® -ISTO 5001-2003 standard. The following features are implemented:

- · Program trace via branch trace messaging (BTM). Branch trace messaging displays program flow discontinuities (direct and indirect branches, exceptions, etc.), allowing the development tool to interpolate what transpires between the discontinuities. Thus static code may be traced.

## Nexus Development Interface

- · Data trace via data write messaging (DWM) and data read messaging (DRM). This provides the capability for the development tool to trace reads and/or writes to selected internal memory resources.
- · Ownership trace via ownership trace messaging (OTM). OTM facilitates ownership trace by providing visibility of which process ID or operating system task is activated. An ownership trace message is transmitted when a new process/task is activated, allowing the development tool to trace ownership flow.
- · Run-time access to embedded processor registers and memory map via the JTAG port. This allows for enhanced download/upload capabilities.
- · Watchpoint messaging via the auxiliary pins.
- · Watchpoint trigger enable of program and/or data trace messaging.
- · Higher speed data input/output via the auxiliary port.
- · Registers for program trace, data trace, ownership trace and watchpoint trigger.
- · All features controllable and configurable via the JTAG port.

## 25.10.5 Enabling Nexus3 Operation

The Nexus module is enabled by loading a single instruction (ACCESS\_AUX\_TAP\_ONCE, as shown in Table 25-4) into the JTAGC instruction register (IR), and then loading the corresponding OnCE OCMD register  with  the  NEXUS3\_ACCESS instruction (refer to  Table 25-5).  For  the  e200z6  Class  3  Nexus module, the OCMD value is 0b00\_0111\_1100. Once enabled, the module will be ready to accept control input  via  the  JTAG  pins.  See  Section 25.4.1,  'Enabling  Nexus  Clients  for  TAP  Access'  for  more information.

The Nexus module is disabled when the JTAG state machine reaches the test-logic-reset state. This state can be reached by the assertion of the JCOMP pin or by cycling through the state machine using the TMS pin. The Nexus module will also be disabled if a power-on-reset (POR) event occurs. If the Nexus3 module is disabled, no trace output will be provided, and the module will disable (drive inactive) auxiliary port output pins MDO[n:0], MSEO[1:0], MCKO. Nexus registers will not be available for reads or writes.

## 25.10.6 TCODEs Supported by NZ63C

The Nexus3 pins allow for flexible transfer operations via public messages. A TCODE defines the transfer format, the number and/or size of the packets to be transferred, and the purpose of each packet. The IEEE ® -ISTO 5001-2003 standard defines a set of public messages. The NZ6C3 module supports the public TCODEs seen in Table 25-19. Each message contains multiple packets transmitted in the order shown in the table.

Table 25-19. Public TCODEs Supported by NZ63C

| Message Name   | Packet Size (bits)   | Packet Size (bits)   | Packet Name   | Packet Type   | Packet Description                |
|----------------|----------------------|----------------------|---------------|---------------|-----------------------------------|
| Message Name   | Min                  | Max                  | Packet Name   | Packet Type   | Packet Description                |
| Debug Status   | 6                    | 6                    | TCODE         | Fixed         | TCODE number = 0 (0x00)           |
| Debug Status   | 4                    | 4                    | SRC           | Fixed         | source processor identifier       |
| Debug Status   | 8                    | 8                    | STATUS        | Fixed         | Debug status register (DS[31:24]) |

Table 25-19. Public TCODEs Supported by NZ63C  (continued)

| Message Name                                    | Packet Size (bits)   | Packet Size (bits)   | Packet Name   | Packet Type   | Packet Description                                                  |
|-------------------------------------------------|----------------------|----------------------|---------------|---------------|---------------------------------------------------------------------|
| Message Name                                    | Min                  | Max                  | Packet Name   | Packet Type   | Packet Description                                                  |
| Ownership Trace Message                         | 6                    | 6                    | TCODE         | Fixed         | TCODE number = 2 (0x02)                                             |
| Ownership Trace Message                         | 4                    | 4                    | SRC           | Fixed         | source processor identifier                                         |
| Ownership Trace Message                         | 32                   | 32                   | PROCESS       | Fixed         | Task/Process ID tag                                                 |
| Program Trace - Direct Branch Message 1         | 6                    | 6                    | TCODE         | Fixed         | TCODE number = 3 (0x03)                                             |
| Program Trace - Direct Branch Message 1         | 4                    | 4                    | SRC           | Fixed         | source processor identifier                                         |
| Program Trace - Direct Branch Message 1         | 1                    | 8                    | I-CNT         | Variable      | # sequential instructions executed since last taken branch          |
| Program Trace - Indirect Branch Message 1       | 6                    | 6                    | TCODE         | Fixed         | TCODE number = 4 (0x04)                                             |
| Program Trace - Indirect Branch Message 1       | 4                    | 4                    | SRC           | Fixed         | source processor identifier                                         |
| Program Trace - Indirect Branch Message 1       | 1                    | 8                    | I-CNT         | Variable      | # sequential instructions executed since last taken branch          |
| Program Trace - Indirect Branch Message 1       | 1                    | 32                   | U-ADDR        | Variable      | unique part of target address for taken branches/exceptions         |
| Data Trace - Data Write Message                 | 6                    | 6                    | TCODE         | Fixed         | TCODE number = 5 (0x05)                                             |
| Data Trace - Data Write Message                 | 4                    | 4                    | SRC           | Fixed         | source processor identifier                                         |
| Data Trace - Data Write Message                 | 3                    | 3                    | DSIZ          | Fixed         | data size (Refer to Table 25-23)                                    |
| Data Trace - Data Write Message                 | 1                    | 32                   | U-ADDR        | Variable      | unique portion of the data write address                            |
| Data Trace - Data Write Message                 | 1                    | 64                   | DATA          | Variable      | data write values (see Section 25.11.13, 'Data Trace,' for details) |
| Data Trace - Data Read Message                  | 6                    | 6                    | TCODE         | Fixed         | TCODE number = 6 (0x06)                                             |
| Data Trace - Data Read Message                  | 4                    | 4                    | SRC           | Fixed         | source processor identifier                                         |
| Data Trace - Data Read Message                  | 3                    | 3                    | DSIZ          | Fixed         | data size (Refer to Table 25-23)                                    |
| Data Trace - Data Read Message                  | 1                    | 32                   | U-ADDR        | Variable      | unique portion of the data read address                             |
| Data Trace - Data Read Message                  | 1                    | 64                   | DATA          | Variable      | data read values (see Section 25.11.13, 'Data Trace,' for details)  |
| Error Message                                   | 6                    | 6                    | TCODE         | Fixed         | TCODE number = 8 (0x08)                                             |
| Error Message                                   | 4                    | 4                    | SRC           | Fixed         | source processor identifier                                         |
| Error Message                                   | 5                    | 5                    | ECODE         | Fixed         | error code                                                          |
| Program Trace - Direct Branch Message w/ Sync 1 | 6                    | 6                    | TCODE         | Fixed         | TCODE number = 11 (0x0B)                                            |
| Program Trace - Direct Branch Message w/ Sync 1 | 4                    | 4                    | SRC           | Fixed         | source processor identifier                                         |
| Program Trace - Direct Branch Message w/ Sync 1 | 1                    | 8                    | I-CNT         | Variable      | # sequential instructions executed since last taken branch          |
| Program Trace - Direct Branch Message w/ Sync 1 | 1                    | 32                   | F-ADDR        | Variable      | full target address (leading zeros truncated)                       |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 25-19. Public TCODEs Supported by NZ63C  (continued)

| Message Name                                      | Packet Size (bits)   | Packet Size (bits)   | Packet Name   | Packet Type   | Packet Description                                                                                           |
|---------------------------------------------------|----------------------|----------------------|---------------|---------------|--------------------------------------------------------------------------------------------------------------|
| Message Name                                      | Min                  | Max                  | Packet Name   | Packet Type   | Packet Description                                                                                           |
| Program Trace - Indirect Branch Message w/ Sync 1 | 6                    | 6                    | TCODE         | Fixed         | TCODE number = 12 (0x0C)                                                                                     |
| Program Trace - Indirect Branch Message w/ Sync 1 | 4                    | 4                    | SRC           | Fixed         | source processor identifier                                                                                  |
| Program Trace - Indirect Branch Message w/ Sync 1 | 1                    | 8                    | I-CNT         | Variable      | # sequential instructions executed since last taken branch                                                   |
| Program Trace - Indirect Branch Message w/ Sync 1 | 1                    | 32                   | F-ADDR        | Variable      | full target address (leading zeros truncated)                                                                |
| Data Trace - Data Write Message w/ Sync           | 6                    | 6                    | TCODE         | Fixed         | TCODE number = 13 (0x0D)                                                                                     |
| Data Trace - Data Write Message w/ Sync           | 4                    | 4                    | SRC           | Fixed         | source processor identifier                                                                                  |
| Data Trace - Data Write Message w/ Sync           | 3                    | 3                    | DSZ           | Fixed         | data size (Refer to Table 25-23)                                                                             |
| Data Trace - Data Write Message w/ Sync           | 1                    | 32                   | F-ADDR        | Variable      | full access address (leading zeros truncated)                                                                |
| Data Trace - Data Write Message w/ Sync           | 1                    | 64                   | DATA          | Variable      | data write values (see Section 25.11.13, 'Data Trace,' for details)                                          |
| Data Trace - Data ReadMessage w/ Sync             | 6                    | 6                    | TCODE         | Fixed         | TCODE number = 14 (0x0E)                                                                                     |
| Data Trace - Data ReadMessage w/ Sync             | 4                    | 4                    | SRC           | Fixed         | source processor identifier                                                                                  |
| Data Trace - Data ReadMessage w/ Sync             | 3                    | 3                    | DSZ           | Fixed         | data size (Refer to Table 25-23)                                                                             |
| Data Trace - Data ReadMessage w/ Sync             | 1                    | 32                   | F-ADDR        | Variable      | full access address (leading zeros truncated)                                                                |
| Data Trace - Data ReadMessage w/ Sync             | 1                    | 64                   | DATA          | Variable      | data read values (see Section 25.11.13, 'Data Trace,' for details)                                           |
| Watchpoint Message                                | 6                    | 6                    | TCODE         | Fixed         | TCODE number = 15 (0x0F)                                                                                     |
| Watchpoint Message                                | 4                    | 4                    | SRC           | Fixed         | source processor identifier                                                                                  |
| Watchpoint Message                                | 4                    | 4                    | WPHIT         | Fixed         | # indicating watchpoint sources                                                                              |
| Resource Full Message                             | 6                    | 6                    | TCODE         | Fixed         | TCODE number = 27 (0x1B)                                                                                     |
| Resource Full Message                             | 4                    | 4                    | SRC           | Fixed         | source processor identifier                                                                                  |
| Resource Full Message                             | 4                    | 4                    | RCODE         | Fixed         | resource code (Refer to RCODE values in Table 25-21) - indicates which resource is the cause of this message |
| Resource Full Message                             | 1                    | 32                   | HIST          | Variable      | branch / predicate instruction history (see Section 25.11.12.1, 'Branch Trace Messaging (BTM)')              |
| Program Trace - Indirect Branch History Message   | 6                    | 6                    | TCODE         | Fixed         | TCODE number = 28 (0x1C) (see footnote 1 below)                                                              |
| Program Trace - Indirect Branch History Message   | 4                    | 4                    | SRC           | Fixed         | source processor identifier                                                                                  |
| Program Trace - Indirect Branch History Message   | 1                    | 8                    | I-CNT         | Variable      | # sequential instructions executed since last taken branch                                                   |
| Program Trace - Indirect Branch History Message   | 1                    | 32                   | U-ADDR        | Variable      | unique part of target address for taken branches/exceptions                                                  |
| Program Trace - Indirect Branch History Message   | 1                    | 32                   | HIST          | Variable      | branch / predicate instruction history (see Section 25.11.12.1, 'Branch Trace Messaging (BTM)')              |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 25-19. Public TCODEs Supported by NZ63C  (continued)

| Message Name                                            | Packet Size (bits)   | Packet Size (bits)   | Packet Name   | Packet Type   | Packet Description                                                                              |
|---------------------------------------------------------|----------------------|----------------------|---------------|---------------|-------------------------------------------------------------------------------------------------|
| Message Name                                            | Min                  | Max                  | Packet Name   | Packet Type   | Packet Description                                                                              |
| Program Trace - Indirect Branch History Message w/ Sync | 6                    | 6                    | TCODE         | Fixed         | TCODE number = 29 (0x1D) (see footnote 1 below)                                                 |
| Program Trace - Indirect Branch History Message w/ Sync | 4                    | 4                    | SRC           | Fixed         | source processor identifier                                                                     |
| Program Trace - Indirect Branch History Message w/ Sync | 1                    | 8                    | I-CNT         | Variable      | # sequential instructions executed since last taken branch                                      |
| Program Trace - Indirect Branch History Message w/ Sync | 1                    | 32                   | F-ADDR        | Variable      | full target address (leading zero (0) truncated)                                                |
| Program Trace - Indirect Branch History Message w/ Sync | 1                    | 32                   | HIST          | Variable      | branch / predicate instruction history (see Section 25.11.12.1, 'Branch Trace Messaging (BTM)') |
| Program Trace - ProgramCorrelation Message              | 6                    | 6                    | TCODE         | Fixed         | TCODE number = 33 (0x21)                                                                        |
| Program Trace - ProgramCorrelation Message              | 4                    | 4                    | SRC           | Fixed         | source processor identifier                                                                     |
| Program Trace - ProgramCorrelation Message              | 4                    | 4                    | EVCODE        | Fixed         | event correlated w/ program flow (Refer to Table 25-22)                                         |
| Program Trace - ProgramCorrelation Message              | 1                    | 8                    | I-CNT         | Variable      | # sequential instructions executed since last taken branch                                      |
| Program Trace - ProgramCorrelation Message              | 1                    | 32                   | HIST          | Variable      | branch / predicate instruction history (see Section 25.11.12.1, 'Branch Trace Messaging (BTM)') |

1 The user can select between the two types of program trace. The advantages for each are discussed in Section 25.11.12.1, 'Branch Trace Messaging (BTM). If the branch history method is selected, the shaded TCODES above will not be messaged out.

Table 25-20 shows the error code encodings used when reporting an error via the Nexus3 Error Message.

Table 25-20. Error Code Encoding (TCODE = 8)

| Error Code (ECODE)   | Description                                                             |
|----------------------|-------------------------------------------------------------------------|
| 00000                | Ownership trace overrun                                                 |
| 00001                | Program trace overrun                                                   |
| 00010                | Data trace overrun                                                      |
| 00011                | Read/write access error                                                 |
| 00101                | Invalid access opcode (Nexus register unimplemented)                    |
| 00110                | Watchpoint overrun                                                      |
| 00111                | (Program trace or data trace) and ownership trace overrun               |
| 01000                | (Program trace or data trace or ownership trace) and watchpoint overrun |
| 01001-0111           | Reserved                                                                |
| 11000                | BTM lost due to collision w/ higher priority message                    |
| 11001-11111          | Reserved                                                                |

Table 25-21 shows the encodings used for resource codes for certain messages.

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 25-21. RCODE values (TCODE = 27)

|   Resource Code (RCODE) | Description                                                                                                                                 |
|-------------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
|                    0001 | Program trace, branch / predicate instruction history. This type of packet is terminated by a stop bit set to 1 after the last history bit. |

Table 25-22 shows the event code encodings used for certain messages.

Table 25-22. Event Code Encoding (TCODE = 33)

| Event Code (EVCODE)   | Description                          |
|-----------------------|--------------------------------------|
| 0000                  | Entry into debug mode                |
| 0001                  | Entry into low power mode (CPU only) |
| 0010-1111             | Reserved for future functionality    |

Table 25-23 shows the data trace size encodings used for certain messages.

Table 25-23. Data Trace Size Encodings (TCODE = 5, 6, 13, 14)

| DTM Size Encoding   | Transfer Size         |
|---------------------|-----------------------|
| 000                 | Byte                  |
| 001                 | Half-word (2 bytes)   |
| 010                 | Word (4 bytes)        |
| 011                 | Double-word (8 bytes) |
| 100                 | String (3 bytes)      |
| 101-111             | Reserved              |

## 25.11 NZ6C3 Memory Map/Register Definition

This  section  describes  the  NZ6C3  programmer's  model.  NZ6C3  registers  are  accessed  using  the JTAG/OnCE port in compliance with IEEE ® 1149.1. See Section 25.11.10, ' NZ6C3 Register Access via JTAG / OnCE' for details on NZ6C3 register access.

## NOTE

NZ6C3 registers and output signals are numbered using bit 0 as the least significant bit. This bit ordering is consistent with the ordering defined by the IEEE ® -ISTO 5001 standard.

Table 25-24 details the register map for the NZ6C3 module.

Table 25-24. NZ6C3 Memory Map

| Access Opcode   | Register Name   | Register Description          | Read Address   | Write Address   |
|-----------------|-----------------|-------------------------------|----------------|-----------------|
| 0x1             | CSC             | Client select control 1       | 0x02           | -               |
| See NPC         | PCR             | Port configuration register 1 | -              | -               |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 25-24. NZ6C3 Memory Map (continued)

| Access Opcode   | Register Name   | Register Description             | Read Address   | Write Address   |
|-----------------|-----------------|----------------------------------|----------------|-----------------|
| 0x2             | DC1             | Development control 1            | 0x04           | 0x05            |
| 0x3             | DC2             | Development control 2            | 0x06           | 0x07            |
| 0x4             | DS              | Development status               | 0x08           | -               |
| 0x7             | RWCS            | Read/write access control/status | 0x0E           | 0x0F            |
| 0x9             | RWA             | Read/write access address        | 0x12           | 0x13            |
| 0xA             | RWD             | Read/write access data           | 0x14           | 0x15            |
| 0xB             | WT              | Watchpoint trigger               | 0x16           | 0x17            |
| 0xD             | DTC             | Data trace control               | 0x1A           | 0x1B            |
| 0xE             | DTSA1           | Data trace start address 1       | 0x1C           | 0x1D            |
| 0xF             | DTSA2           | Data trace start address 2       | 0x1E           | 0x1F            |
| 0x12            | DTEA1           | Data trace end address 1         | 0x24           | 0x25            |
| 0x13            | DTEA2           | Data trace end address 2         | 0x26           | 0x27            |
| 0x14 -> 0x3F    | -               | Reserved                         | 0x28->0x7E     | 0x29->0x7F      |

- 1 The CSC and PCR registers are shown in this table as part of the Nexus programmer's model. They are only present at the top level Nexus3 controller (NPC), not in the NZ6C3 module. The device's CSC register is readable through Nexus3, but the PCR is shown for reference only.

## 25.11.1 Development Control Register 1, 2 (DC1, DC2)

The  development  control  registers  are  used  to  control  the  basic  development  features  of  the  NZ6C3 module.  Development  control  register  1  is  shown  in  Figure 25-13  and  its  fields  are  described  in Table 25-25.

Figure 25-13. Development Control Register 1 (DC1)

<!-- image -->

|           | 31   | 30      | 29      | 28   | 27   | 26   | 25   | 24   | 23   | 22   | 21   | 20   | 19   | 18   | 17   | 16   |
|-----------|------|---------|---------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| R         | OPC  | MCK_DIV | MCK_DIV | EOC  | EOC  | 0    | PTM  | WEN  | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |
| W         |      |         |         |      |      |      |      |      |      |      |      |      |      |      |      |      |
| Reset     | 0    | 0       | 0       | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |
| Nexus Reg | 0x2  | 0x2     | 0x2     | 0x2  | 0x2  | 0x2  | 0x2  | 0x2  | 0x2  | 0x2  | 0x2  | 0x2  | 0x2  | 0x2  | 0x2  | 0x2  |
|           | 15   | 14      | 13      | 12   | 11   | 10   | 9    | 8    | 7    | 6    | 5    | 4    | 3    | 2    | 1    | 0    |
| R         | 0    | 0       | 0       | 0    | 0    | 0    | 0    | 0    |      | OVC  | OVC  | EIC  | EIC  | TM   | TM   |      |
| W         |      |         |         |      |      |      |      |      |      |      |      |      |      |      |      |      |
| Reset     | 0    | 0       | 0       | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |
| Nexus Reg | 0x2  | 0x2     | 0x2     | 0x2  | 0x2  | 0x2  | 0x2  | 0x2  | 0x2  | 0x2  | 0x2  | 0x2  | 0x2  | 0x2  | 0x2  | 0x2  |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 25-25. DC1 Field Descriptions

| Bits   | Name            | Description                                                                                                                                                                    |
|--------|-----------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 31     | OPC 1           | Output port mode control. 0 Reduced-port mode configuration (4 MDO pins) 1 Full-port mode configuration (12 MDO pins)                                                          |
| 30-29  | MCK_DIV [1:0] 1 | MCKO clock divide ratio. 00 MCKO is 1x processor clock freq. 01 MCKO is 1/2x processor clock freq. 10 MCKO is 1/4x processor clock freq. 11 MCKO is 1/8x processor clock freq. |
| 28-27  | EOC [1:0]       | EVTO control. 00 EVTO upon occurrence of watchpoints (configured in DC2) 01 EVTO upon entry into debug mode 10 EVTO upon timestamping event 11 Reserved                        |
| 26     | -               | Reserved.                                                                                                                                                                      |
| 25     | PTM             | Program trace method. 0 Program trace uses traditional branch messages 1 Program trace uses branch history messages                                                            |
| 24     | WEN             | Watchpoint trace enable. 0 Watchpoint Messaging disabled 1 Watchpoint Messaging enabled                                                                                        |
| 23-8   | -               | Reserved.                                                                                                                                                                      |
| 7-5    | OVC [2:0]       | Overrun control. 000 Generate overrun messages 001-010 mReserved 011 Delay processor for BTM / DTM / OTM overruns 1XX Reserved                                                 |
| 4-3    | EIC [1:0]       | EVTI control. 00 EVTI is used for synchronization (program trace/ data trace) 01 EVTI is used for debug request 1X Reserved                                                    |
| 2-0    | TM [2:0]        | Trace mode. Any or all of the TM bits may set, enabling one or more traces. 000 No trace 1XX Program trace enabled X1X Data trace enabled XX1 Ownership trace enabled          |

1 The output port mode control bit (OPC) and MCKO divide bits (MCK\_DIV) are shown for clarity. These functions are controlled globally by the NPC port control register (PCR).

Development control register 2 is shown in Figure 25-14 and its fields are described in Table 25-26.

Figure 25-14. Development Control Register 2 (DC2)

<!-- image -->

|           | 31   | 30   | 29   | 28   | 27   | 26   | 25   | 24   | 23   | 22   | 21   | 20   | 19   | 18   | 17   | 16   |
|-----------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| R         |      |      |      | EWC  |      |      |      |      | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |
| W         |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |
| Reset     | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |
| Nexus Reg | 0x3  | 0x3  | 0x3  | 0x3  | 0x3  | 0x3  | 0x3  | 0x3  | 0x3  | 0x3  | 0x3  | 0x3  | 0x3  | 0x3  | 0x3  | 0x3  |
|           | 15   | 14   | 13   | 12   | 11   | 10   | 9    | 8    | 7    | 6    | 5    | 4    | 3    | 2    | 1    | 0    |
| R         | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |
| W         |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |
| Reset     | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |
| Nexus Reg | 0x3  | 0x3  | 0x3  | 0x3  | 0x3  | 0x3  | 0x3  | 0x3  | 0x3  | 0x3  | 0x3  | 0x3  | 0x3  | 0x3  | 0x3  | 0x3  |

## Table 25-26. DC2 Field Descriptions

| Bits   | Name      | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
|--------|-----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 31-24  | EWC [7:0] | EVTO watchpoint configuration. Any or all of the bits in EWC may be set to configure the EVTO watchpoint. 00000000No Watchpoints trigger EVTO 1XXXXXXXWatchpoint #0 (IAC1 from Nexus1) triggers EVTO X1XXXXXXWatchpoint #1 (IAC2 from Nexus1) triggers EVTO XX1XXXXXWatchpoint #2 (IAC3 from Nexus1) triggers EVTO XXX1XXXXWatchpoint #3 (IAC4 from Nexus1) triggers EVTO XXXX1XXXWatchpoint #4 (DAC1 from Nexus1) triggers EVTO XXXXX1XXWatchpoint #5 (DAC2 from Nexus1) triggers EVTO XXXXXX1XWatchpoint #6 (DCNT1 from Nexus1) triggers EVTO XXXXXXX1Watchpoint #7 (DCNT2 from Nexus1) triggers EVTO |
| 23-0   | -         | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |

## NOTE

The EOC bits in DC1 must be programmed to trigger EVTO on watchpoint occurrence for the EWC bits to have any effect.

## 25.11.2 Development Status Register (DS)

The development status register is used to report system debug status. When debug mode is entered or exited,  or  an  e200z6-defined  low  power  mode  is  entered,  a  debug  status  message  is  transmitted  with DS[31:24]. The external tool can read this register at any time.

Figure 25-15. Development Status Register (DS)

|           | 31   | 30   | 29   | 28   | 27   | 26   | 25   | 24   | 23   | 22   | 21   | 20   | 19   | 18   | 17   | 16   |
|-----------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| R         | DBG  | 0    | 0    | 0    | LPC  | LPC  | CHK  | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |
| W         |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |
| Reset     | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |
| Nexus Reg | 0x4  | 0x4  | 0x4  | 0x4  | 0x4  | 0x4  | 0x4  | 0x4  | 0x4  | 0x4  | 0x4  | 0x4  | 0x4  | 0x4  | 0x4  | 0x4  |
|           | 15   | 14   | 13   | 12   | 11   | 10   | 9    | 8    | 7    | 6    | 5    | 4    | 3    | 2    | 1    | 0    |
| R         | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |
| W         |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |
| Reset     | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |
| Nexus Reg | 0x4  | 0x4  | 0x4  | 0x4  | 0x4  | 0x4  | 0x4  | 0x4  | 0x4  | 0x4  | 0x4  | 0x4  | 0x4  | 0x4  | 0x4  | 0x4  |

Table 25-27. DS Field Descriptions

| Bits   | Name      | Description                                                                                                       |
|--------|-----------|-------------------------------------------------------------------------------------------------------------------|
| 31-28  | DBG       | e200z6 CPU debug mode status. 0 CPU not in debug mode 1 CPU in debug mode                                         |
| 27-26  | LPC [1:0] | e200z6 CPU low power mode status. 00 Normal (run) mode 01 CPU in halted state 10 CPU in stopped state 11 Reserved |
| 25     | CHK       | e200z6 CPU checkstop status. 0 CPU not in checkstop state 1 CPU in checkstop state                                |
| 24-0   | -         | Reserved.                                                                                                         |

## 25.11.3 Read/Write Access Control/Status (RWCS)

The read write access control/status register provides control for read/write access. Read/write access provides DMA-like access to memory-mapped resources on the  system bus either while the processor is halted, or during runtime. The RWCS register also provides read/write access status information as  shown in Table 25-29.

Figure 25-16. Read/Write Access Control/Status Register (RWCS)

<!-- image -->

|           | 31         | 30         | 29         | 28         | 27         | 26         | 25         | 24         | 23         | 22         | 21         | 20         | 19         | 18         | 17         | 16         |
|-----------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|
| R         | AC         | RW         | SZ         | SZ         | SZ         | MAP        | MAP        | MAP        | PR         | PR         | BST        | 0          | 0          | 0          | 0          | 0          |
| W         |            |            |            |            |            |            |            |            |            |            |            |            |            |            |            |            |
| Reset     | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          |
| Nexus Reg | 0x7        | 0x7        | 0x7        | 0x7        | 0x7        | 0x7        | 0x7        | 0x7        | 0x7        | 0x7        | 0x7        | 0x7        | 0x7        | 0x7        | 0x7        | 0x7        |
|           | 15         | 14         | 13         | 12         | 11         | 10         | 9          | 8          | 7          | 6          | 5          | 4          | 3          | 2          | 1          | 0          |
| R         | CNT ERR DV | CNT ERR DV | CNT ERR DV | CNT ERR DV | CNT ERR DV | CNT ERR DV | CNT ERR DV | CNT ERR DV | CNT ERR DV | CNT ERR DV | CNT ERR DV | CNT ERR DV | CNT ERR DV | CNT ERR DV | CNT ERR DV | CNT ERR DV |
| W         |            |            |            |            |            |            |            |            |            |            |            |            |            |            |            |            |
| Reset     | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          |
| Nexus Reg | 0x7        | 0x7        | 0x7        | 0x7        | 0x7        | 0x7        | 0x7        | 0x7        | 0x7        | 0x7        | 0x7        | 0x7        | 0x7        | 0x7        | 0x7        | 0x7        |

Table 25-28. RWCS Field Description

| Bits   | Name       | Description                                                                                                                                                        |
|--------|------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 31     | AC         | Access control. 0 End access 1 Start access                                                                                                                        |
| 30     | RW         | Read/write select. 0 Read access 1 Write access                                                                                                                    |
| 29-27  | SZ [2:0]   | Word size. 000 8-bit (byte) 001 6-bit (half-word) 010 32-bit (word) 011 64-bit (double-word - only in burst mode) 100-111 Reserved (default to word)               |
| 26-24  | MAP [2:0]  | MAP select. 000 Primary memory map 001-111 Reserved                                                                                                                |
| 23-22  | PR [1:0]   | Read/write access priority. 00 Lowest access priority 01 Reserved (default to lowest priority) 10 Reserved (default to lowest priority) 11 Highest access priority |
| 21     | BST        | Burst control. 0 Module accesses are single bus cycle at a time. 1 Module accesses are performed as burst operation.                                               |
| 20-16  | -          | Reserved.                                                                                                                                                          |
| 15-2   | CNT [13:0] | Access control count. Number of accesses of word size SZ                                                                                                           |
| 1      | ERR        | Read/write access error. See Table 25-29.                                                                                                                          |
| 0      | DV         | Read/write access data valid. See Table 25-29.                                                                                                                     |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 25-29 details the status bit encodings.

Table 25-29. Read/Write Access Status Bit Encoding

| Read Action                         | Write Action                         |   ERR |   DV |
|-------------------------------------|--------------------------------------|-------|------|
| Read access has not completed       | Write access completed without error |     0 |    0 |
| Read access error has occurred      | Write access error has occurred      |     1 |    0 |
| Read access completed without error | Write access has not completed       |     0 |    1 |
| Not allowed                         | Not allowed                          |     1 |    1 |

## 25.11.4 Read/Write Access Data (RWD)

The read/write access data register provides the data to/from system bus memory-mapped locations when initiating a read or a write access.

Figure 25-17. Read/Write Access Data Register (RWD)

<!-- image -->

|           | 31              | 30              | 29              | 28              | 27              | 26              | 25              | 24              | 23              | 22              | 21              | 20              | 19              | 18              | 17              | 16              |
|-----------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|
| R         | Read/Write Data | Read/Write Data | Read/Write Data | Read/Write Data | Read/Write Data | Read/Write Data | Read/Write Data | Read/Write Data | Read/Write Data | Read/Write Data | Read/Write Data | Read/Write Data | Read/Write Data | Read/Write Data | Read/Write Data | Read/Write Data |
| Reset     | 0               | 0               | 0               | 0               | 0               | 0               | 0               | 0               | 0               | 0               | 0               | 0               | 0               | 0               | 0               | 0               |
| Nexus Reg | 0x9             | 0x9             | 0x9             | 0x9             | 0x9             | 0x9             | 0x9             | 0x9             | 0x9             | 0x9             | 0x9             | 0x9             | 0x9             | 0x9             | 0x9             | 0x9             |
|           | 15              | 14              | 13              | 12              | 11              | 10              | 9               | 8               | 7               | 6               | 5               | 4               | 3               | 2               | 1               | 0               |
| R         | Read/Write Data | Read/Write Data | Read/Write Data | Read/Write Data | Read/Write Data | Read/Write Data | Read/Write Data | Read/Write Data | Read/Write Data | Read/Write Data | Read/Write Data | Read/Write Data | Read/Write Data | Read/Write Data | Read/Write Data | Read/Write Data |
| W Reset   | 0               | 0               | 0               | 0               | 0               | 0               | 0               | 0               | 0               | 0               | 0               | 0               | 0               | 0               | 0               | 0               |
| Nexus Reg | 0x9             | 0x9             | 0x9             | 0x9             | 0x9             | 0x9             | 0x9             | 0x9             | 0x9             | 0x9             | 0x9             | 0x9             | 0x9             | 0x9             | 0x9             | 0x9             |

## 25.11.5 Read/Write Access Address (RWA)

The read/write access address register provides the system bus address to be accessed when initiating a read or a write access.

Figure 25-18. Read/Write Access Address Register (RWA)

<!-- image -->

|           | 31                 | 30                 | 29                 | 28                 | 27                 | 26                 | 25                 | 24                 | 23                 | 22                 | 21                 | 20                 | 19                 | 18                 | 17                 | 16                 |
|-----------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|
| R         | Read/Write Address | Read/Write Address | Read/Write Address | Read/Write Address | Read/Write Address | Read/Write Address | Read/Write Address | Read/Write Address | Read/Write Address | Read/Write Address | Read/Write Address | Read/Write Address | Read/Write Address | Read/Write Address | Read/Write Address | Read/Write Address |
| W Reset   | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  |
| Nexus Reg | 0xA                | 0xA                | 0xA                | 0xA                | 0xA                | 0xA                | 0xA                | 0xA                | 0xA                | 0xA                | 0xA                | 0xA                | 0xA                | 0xA                | 0xA                | 0xA                |
|           | 15                 | 14                 | 13                 | 12                 | 11                 | 10                 | 9                  | 8                  | 7                  | 6                  | 5                  | 4                  | 3                  | 2                  | 1                  | 0                  |
| R         | Read/Write Address | Read/Write Address | Read/Write Address | Read/Write Address | Read/Write Address | Read/Write Address | Read/Write Address | Read/Write Address | Read/Write Address | Read/Write Address | Read/Write Address | Read/Write Address | Read/Write Address | Read/Write Address | Read/Write Address | Read/Write Address |
| W         |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |
| Reset     | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  |
| Nexus Reg | 0xA                | 0xA                | 0xA                | 0xA                | 0xA                | 0xA                | 0xA                | 0xA                | 0xA                | 0xA                | 0xA                | 0xA                | 0xA                | 0xA                | 0xA                | 0xA                |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## 25.11.6 Watchpoint Trigger Register (WT)

The watchpoint trigger register allows the watchpoints defined within the e200z6 Nexus1 logic to trigger actions. These watchpoints can control program and/or data trace enable and disable. The WT bits can be used to produce an address related 'window' for triggering trace messages.

Figure 25-19. Watchpoint Trigger Register (WT)

<!-- image -->

|           | 31   | 30   | 29   | 28   | 27   | 26   | 25   | 24   | 23   | 22   | 21   | 20   | 19   | 18   | 17   | 16   |
|-----------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| R         | PTS  | PTS  | PTS  | PTE  | PTE  | PTE  | DTS  | DTS  | DTS  | DTE  | DTE  | DTE  | 0    | 0    | 0    | 0    |
| W         |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |
| Reset     | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |
| Nexus Reg | 0xB  | 0xB  | 0xB  | 0xB  | 0xB  | 0xB  | 0xB  | 0xB  | 0xB  | 0xB  | 0xB  | 0xB  | 0xB  | 0xB  | 0xB  | 0xB  |
|           | 15   | 14   | 13   | 12   | 11   | 10   | 9    | 8    | 7    | 6    | 5    | 4    | 3    | 2    | 1    | 0    |
| R         | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |
| W         |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |
| Reset     | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |
| Nexus Reg | 0xB  | 0xB  | 0xB  | 0xB  | 0xB  | 0xB  | 0xB  | 0xB  | 0xB  | 0xB  | 0xB  | 0xB  | 0xB  | 0xB  | 0xB  | 0xB  |

Table 25-30 details the watchpoint trigger register fields.

Table 25-30. WT Field Descriptions

| Bits   | Name      | Description                                                                                                                                                                                                                                                                                                                                                      |
|--------|-----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 31-29  | PTS [2:0] | Program trace start control. 000 Trigger disabled 001 Use watchpoint #0 (IAC1 from Nexus1) 010 Use watchpoint #1 (IAC2 from Nexus1) 011 Use watchpoint #2 (IAC3 from Nexus1) 100 Use watchpoint #3 (IAC4 from Nexus1) 101 Use watchpoint #4 (DAC1 from Nexus1) 110 Use watchpoint #5 (DAC2 from Nexus1) 111 Use watchpoint #6 or #7 (DCNT1 or DCNT2 from Nexus1) |
| 28-26  | PTE [2:0] | Program trace end control. 000 Trigger disabled 001 Use watchpoint #0 (IAC1 from Nexus1) 010 Use watchpoint #1 (IAC2 from Nexus1) 011 Use watchpoint #2 (IAC3 from Nexus1) 100 Use watchpoint #3 (IAC4 from Nexus1) 101 Use watchpoint #4 (DAC1 from Nexus1) 110 Use watchpoint #5 (DAC2 from Nexus1) 111 Use watchpoint #6 or #7 (DCNT1 or DCNT2 from Nexus1)   |

Table 25-30. WT Field Descriptions (continued)

| Bits   | Name      | Description                                                                                                                                                                                                                                                                                                                                                   |
|--------|-----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 25-23  | DTS [2:0] | Data trace start control. 000 Trigger disabled 001 Use watchpoint #0 (IAC1 from Nexus1) 010 Use watchpoint #1 (IAC2 from Nexus1) 011 Use watchpoint #2 (IAC3 from Nexus1) 100 Use watchpoint #3 (IAC4 from Nexus1) 101 Use watchpoint #4 (DAC1 from Nexus1) 110 Use watchpoint #5 (DAC2 from Nexus1) 111 Use watchpoint #6 or #7 (DCNT1 or DCNT2 from Nexus1) |
| 22-20  | DTE [2:0] | Data trace end control. 000 Trigger disabled 001 Use watchpoint #0 (IAC1 from Nexus1) 010 Use watchpoint #1 (IAC2 from Nexus1) 011 Use watchpoint #2 (IAC3 from Nexus1) 100 Use watchpoint #3 (IAC4 from Nexus1) 101 Use watchpoint #4 (DAC1 from Nexus1) 110 Use watchpoint #5 (DAC2 from Nexus1) 111 Use watchpoint #6 or #7 (DCNT1 or DCNT2 from Nexus1)   |
| 19-0   | -         | Reserved.                                                                                                                                                                                                                                                                                                                                                     |

## NOTE

The  WT bits  will  only  control  program/data  trace  if  the  TM  bits  in  the development control register 1 (DC1) have not already been set to enable program and data trace, respectively.

## 25.11.7 Data Trace Control Register (DTC)

The data trace control register controls whether DTM messages are restricted to reads, writes, or both for a user programmable address range. There are two data trace channels controlled by the DTC for the Nexus3 module. Each channel can also be programmed to trace data accesses or instruction accesses.

Figure 25-20. Data Trace Control Register (DTC)

<!-- image -->

|           | 31   | 30   | 29   | 28   | 27   | 26   | 25   | 24   | 23   | 22   | 21   | 20   | 19   | 18   | 17   | 16   |
|-----------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| R         | RWT1 | RWT1 | RWT2 | RWT2 | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |
| W         |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |
| Reset     | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |
| Nexus Reg | 0xD  | 0xD  | 0xD  | 0xD  | 0xD  | 0xD  | 0xD  | 0xD  | 0xD  | 0xD  | 0xD  | 0xD  | 0xD  | 0xD  | 0xD  | 0xD  |
|           | 15   | 14   | 13   | 12   | 11   | 10   | 9    | 8    | 7    | 6    | 5    | 4    | 3    | 2    | 1    | 0    |
| R         | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | RC1  | RC2  | 0    | 0    | DI1  | DI2  | 0    | 0    |
| W         |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |
| Reset     | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |
| Nexus Reg | 0xD  | 0xD  | 0xD  | 0xD  | 0xD  | 0xD  | 0xD  | 0xD  | 0xD  | 0xD  | 0xD  | 0xD  | 0xD  | 0xD  | 0xD  | 0xD  |

Table 25-31 details the data trace control register fields.

## Table 25-31. DTC Field Description

| Bits   | Name       | Description                                                                                                          |
|--------|------------|----------------------------------------------------------------------------------------------------------------------|
| 31-30  | RWT1 [1:0] | Read/write trace 1. 00 No trace enabled X1 Enable data read trace 1X Enable data write trace                         |
| 29-28  | RWT2 [1:0] | Read/write trace 2. 00 No trace enabled X1 Enable data read trace 1X Enable data write trace                         |
| 27-8   | -          | Reserved.                                                                                                            |
| 7      | RC1        | Range control 1. 0 Condition trace on address within range 1 Condition trace on address outside of range             |
| 6      | RC2        | Range control 2 0 Condition trace on address within range 1 Condition trace on address outside of range              |
| 5-4    | -          | Reserved.                                                                                                            |
| 3      | DI1        | Data access/instruction access trace 1. 0 Condition trace on data accesses 1 Condition trace on instruction accesses |
| 2      | DI2        | Data access/instruction access trace 2 0 Condition trace on data accesses 1 Condition trace on instruction accesses  |
| 1-0    | -          | Reserved.                                                                                                            |

## 25.11.8 Data Trace Start Address Registers 1 and 2 (DTSA n )

The data trace start address registers define the start addresses for each trace channel.

Figure 25-21. Data Trace Start Address Register 1 (DTSA1)

<!-- image -->

|           | 31                       | 30                       | 29                       | 28                       | 27                       | 26                       | 25                       | 24                       | 23                       | 22                       | 21                       | 20                       | 19                       | 18                       | 17                       | 16                       |
|-----------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|
| R         | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address |
| W Reset   | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        |
| Nexus Reg | 0xE                      | 0xE                      | 0xE                      | 0xE                      | 0xE                      | 0xE                      | 0xE                      | 0xE                      | 0xE                      | 0xE                      | 0xE                      | 0xE                      | 0xE                      | 0xE                      | 0xE                      | 0xE                      |
|           | 15                       | 14                       | 13                       | 12                       | 11                       | 10                       | 9                        | 8                        | 7                        | 6                        | 5                        | 4                        | 3                        | 2                        | 1                        | 0                        |
| R         | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address |
| W         |                          |                          |                          |                          |                          |                          |                          |                          |                          |                          |                          |                          |                          |                          |                          |                          |
| Reset     | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        |
| Nexus Reg | 0xE                      | 0xE                      | 0xE                      | 0xE                      | 0xE                      | 0xE                      | 0xE                      | 0xE                      | 0xE                      | 0xE                      | 0xE                      | 0xE                      | 0xE                      | 0xE                      | 0xE                      | 0xE                      |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Figure 25-22. Data Trace Start Address Register 2 (DTSA2)

<!-- image -->

|           | 31                       | 30                       | 29                       | 28                       | 27                       | 26                       | 25                       | 24                       | 23                       | 22                       | 21                       | 20                       | 19                       | 18                       | 17                       | 16                       |
|-----------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|
| R         | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address |
| W Reset   | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        |
| Nexus Reg | 0xF                      | 0xF                      | 0xF                      | 0xF                      | 0xF                      | 0xF                      | 0xF                      | 0xF                      | 0xF                      | 0xF                      | 0xF                      | 0xF                      | 0xF                      | 0xF                      | 0xF                      | 0xF                      |
|           | 15                       | 14                       | 13                       | 12                       | 11                       | 10                       | 9                        | 8                        | 7                        | 6                        | 5                        | 4                        | 3                        | 2                        | 1                        | 0                        |
| R         | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address | Data Trace Start Address |
| W         |                          |                          |                          |                          |                          |                          |                          |                          |                          |                          |                          |                          |                          |                          |                          |                          |
| Reset     | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        | 0                        |
| Nexus Reg | 0xF                      | 0xF                      | 0xF                      | 0xF                      | 0xF                      | 0xF                      | 0xF                      | 0xF                      | 0xF                      | 0xF                      | 0xF                      | 0xF                      | 0xF                      | 0xF                      | 0xF                      | 0xF                      |

## 25.11.9 Data Trace End Address Registers 1 and 2 (DTEA n )

The data trace end address registers define the end addresses for each trace channel.

Figure 25-23. Data Trace End Address Register 1 (DTEA1)

<!-- image -->

|           | 31                     | 30                     | 29                     | 28                     | 27                     | 26                     | 25                     | 24                     | 23                     | 22                     | 21                     | 20                     | 19                     | 18                     | 17                     | 16                     |
|-----------|------------------------|------------------------|------------------------|------------------------|------------------------|------------------------|------------------------|------------------------|------------------------|------------------------|------------------------|------------------------|------------------------|------------------------|------------------------|------------------------|
| R         | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address |
| W Reset   | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      |
| Nexus Reg | 0x12                   | 0x12                   | 0x12                   | 0x12                   | 0x12                   | 0x12                   | 0x12                   | 0x12                   | 0x12                   | 0x12                   | 0x12                   | 0x12                   | 0x12                   | 0x12                   | 0x12                   | 0x12                   |
|           | 15                     | 14                     | 13                     | 12                     | 11                     | 10                     | 9                      | 8                      | 7                      | 6                      | 5                      | 4                      | 3                      | 2                      | 1                      | 0                      |
| R         | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address |
| W         |                        |                        |                        |                        |                        |                        |                        |                        |                        |                        |                        |                        |                        |                        |                        |                        |
| Reset     | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      |
| Nexus Reg | 0x12                   | 0x12                   | 0x12                   | 0x12                   | 0x12                   | 0x12                   | 0x12                   | 0x12                   | 0x12                   | 0x12                   | 0x12                   | 0x12                   | 0x12                   | 0x12                   | 0x12                   | 0x12                   |

Figure 25-24. Data Trace End Address Register 2 (DTEA2)

<!-- image -->

|           | 31                     | 30                     | 29                     | 28                     | 27                     | 26                     | 25                     | 24                     | 23                     | 22                     | 21                     | 20                     | 19                     | 18                     | 17                     | 16                     |
|-----------|------------------------|------------------------|------------------------|------------------------|------------------------|------------------------|------------------------|------------------------|------------------------|------------------------|------------------------|------------------------|------------------------|------------------------|------------------------|------------------------|
| R         | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address |
| W Reset   | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      |
| Nexus Reg | 0x13                   | 0x13                   | 0x13                   | 0x13                   | 0x13                   | 0x13                   | 0x13                   | 0x13                   | 0x13                   | 0x13                   | 0x13                   | 0x13                   | 0x13                   | 0x13                   | 0x13                   | 0x13                   |
|           | 15                     | 14                     | 13                     | 12                     | 11                     | 10                     | 9                      | 8                      | 7                      | 6                      | 5                      | 4                      | 3                      | 2                      | 1                      | 0                      |
| R         | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address | Data Trace End Address |
| W Reset   | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      | 0                      |
| Nexus Reg | 0x13                   | 0x13                   | 0x13                   | 0x13                   | 0x13                   | 0x13                   | 0x13                   | 0x13                   | 0x13                   | 0x13                   | 0x13                   | 0x13                   | 0x13                   | 0x13                   | 0x13                   | 0x13                   |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 25-32 illustrates the range that will be selected for data trace for various cases of DTSA being less than, greater than, or equal to DTEA.

Table 25-32. Data Trace-Address Range Options

| Programmed Values   | Range Control Bit Value   | Range Selected         |
|---------------------|---------------------------|------------------------|
| DTSA < DTEA         | 0                         | DTSA -> <- DTEA        |
| DTSA < DTEA         | 1                         | <- DTSA DTEA ->        |
| DTSA > DTEA         | N/A                       | Invalid range-no trace |
| DTSA = DTEA         | N/A                       | Invalid range-no trace |

## NOTE

DTSA must be less than DTEA in order to guarantee correct data write/read traces. Data trace ranges are exclusive of the DTSA and DTEA addresses.

## 25.11.10 NZ6C3 Register Access via JTAG / OnCE

Access to Nexus3 register resources is enabled by loading a single instruction (ACCESS\_AUX\_TAP\_ONCE)  into  the  JTAGC  instruction  register  (IR),  and  then  loading  the corresponding OnCE OCMD register with the NEXUS3\_ACCESS instruction (refer to Table 25-5). For the NZ6C3 module, the OCMD value is 0b00\_0111\_1100.

Once  the  ACCESS\_AUX\_TAP\_ONCE  instruction  has  been  loaded,  the  JTAG/OnCE  port  allows tool/target communications with all Nexus3 registers according to the register map in Table 25-24.

Reading/writing of a NZ6C3 register then requires two (2) passes through the data-scan (DR) path of the JTAG state machine (see Section 25.11.17).

- 1. The first pass through the DR selects the NZ6C3 register to be accessed by providing an index (see Table 25-24), and the direction (read/write). This is achieved by loading an 8-bit value into the JTAG data register (DR). This register has the following format:

(7-bits)

(1-bit)

Nexus Register Index

R/W

RESET Value: 0x00

Nexus Register Index:

Selected from values in Table 25-24

Read/Write (R/W):

0 Read

1 Write

- 2. The second pass through the DR then shifts the data in or out of the JTAG port, lsb first.
- a) During a read access, data is latched from the selected Nexus register when the JTAG state machine passes through the capture-DR state.
- b) During a write access, data is latched into the selected Nexus register when the JTAG state machine passes through the update-DR state.

## 25.11.11Ownership Trace

This section details the ownership trace features of the NZ6C3 module.

## 25.11.11.1Overview

Ownership trace provides a macroscopic view, such as task flow reconstruction, when debugging software written in a high level (or object-oriented) language. It offers the highest level of abstraction for tracking operating system software execution. This is especially useful when the developer is not interested in debugging at lower levels.

## 25.11.11.2Ownership Trace Messaging (OTM)

Ownership trace information is messaged via the auxiliary port using an ownership trace message (OTM). The e200z6 processor contains a PowerPC Book E defined process ID register within the CPU.

The  process  ID  register  is  updated  by  the  operating  system  software  to  provide  task/process  ID information. The contents of this register are replicated on the pins of the processor and connected to Nexus. The process ID register value can be accessed using the mfspr mtspr / instructions. Please refer to the e200z6 PowerPC TM Core Reference Manual for more details on the process ID register.

There are two conditions which will cause an ownership trace message.

- 1. When new information is updated in the OTR register or process ID register by the e200z6 processor, the data is latched within Nexus, and is messaged out via the auxiliary port, allowing development tools to trace ownership flow.
- 2. When the periodic (255) OTM message counter expires (after 255 queued messages without an OTM), an OTM will be sent. The data will be sent from either the latched OTR data or the latched process ID data. This allows processors using virtual memory to be regularly updated with the latest process ID.

Ownership trace information is messaged out in the following format:

Figure 25-25. Ownership Trace Message Format

<!-- image -->

## 25.11.11.3OTM Error Messages

An error message occurs when a new message cannot be queued due to the message queue being full. The FIFO will discard incoming messages until it has completely emptied the queue. Once emptied, an error message will be queued. The error encoding will indicate which types of messages attempted to be queued while the FIFO was being emptied.

If only an OTM message attempts to enter the queue while it is being emptied, the error message will incorporate  the  OTM  only  error  encoding  (00000).  If  both  OTM  and  either  BTM  or  DTM  messages attempt to enter the queue, the error message will incorporate the OTM and (program or data) trace error encoding (00111). If a watchpoint also attempts to be queued while the FIFO is being emptied, then the error message will incorporate error encoding (01000).

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Freescale Semiconductor

## NOTE

The OVC bits within the DC1 register can be set to delay the CPU in order to alleviate (but not eliminate) potential overrun situations.

Error information is messaged out in the following format (see Table 25-20)

Figure 25-26. Error Message Format

<!-- image -->

## 25.11.11.4 OTM Flow

Ownership trace messages are generated when the operating system writes to the e200z6 process ID register or the memory mapped ownership trace register.

The following flow describes the OTM process:

- 1. The process ID register is a system control register. It is internal to the e200z6 processor and can be accessed by using PPC instructions mtspr and mfspr . The contents of this register are replicated on the pins of the processor and connected to Nexus.
- 2. OTR/process ID register reads do not cause ownership trace messages to be transmitted by the NZ6C3 module.
- 3. If the periodic OTM message counter expires (after 255 queued messages without an OTM), an OTM is sent using the latched data from the previous OTM or process ID register write.

## 25.11.12 Program Trace

This section details the program trace mechanism supported by NZ6C3 for the e200z6 processor. Program trace  is  implemented  via  branch  trace  messaging  (BTM)  as  per  the  Class  3  IEEE ® -ISTO 5001-2003 standard  definition.  Branch  trace  messaging  for  e200z6  processors  is  accomplished  by  snooping  the e200z6 virtual address bus (between the CPU and MMU), attribute signals, and CPU status.

## 25.11.12.1Branch Trace Messaging (BTM)

Traditional  branch  trace  messaging  facilitates  program  trace  by  providing  the  following  types  of information:

- · Messaging for taken direct branches includes how many sequential instructions were executed since the last taken branch or exception. Direct (or indirect) branches not taken are counted as sequential instructions.
- · Messaging for taken indirect branches and exceptions includes how many sequential instructions were executed since the last taken branch or exception and the unique portion of the branch target address or exception vector address.

Branch history messaging facilitates program trace by providing the following information:

- · Messaging for taken indirect branches and exceptions includes how many sequential instructions were executed since the last predicate instruction, taken indirect branch, or exception, the unique

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

portion of the branch target address or exception vector address, as well as a branch/predicate instruction history field. Each bit in the history field represents a direct branch or predicated instruction where a value of one (1) indicates taken, and a value of zero (0) indicates not taken. Certain instructions ( evsel ) generate a pair of predicate bits which are both reported as consecutive bits in the history field.

## 25.11.12.1.1 e200z6 Indirect Branch Message Instructions (PowerPC Book E)

Table 25-33 shows the types of instructions and events which cause indirect branch messages or branch history messages to be encoded.

Table 25-33. Indirect Branch Message Sources

| Source of Indirect Branch Message         | Instructions                  |
|-------------------------------------------|-------------------------------|
| Taken branch relative to a register value | bcctr , bcctrl , bclr , bclrl |
| System Call / Trap exceptions taken       | sc , tw , twi                 |
| Return from interrupts / exceptions       | rfi , rfci , rfdi             |

## 25.11.12.1.2 e200z6 Direct Branch Message Instructions (PowerPC Book E)

Table 25-34 shows the types of instructions which will cause direct branch messages or will toggle a bit in the instruction history buffer to be messaged out in a resource full message or branch history message.

Table 25-34. Direct Branch Message Sources

| Source of Direct Branch Message   | Instructions                              |
|-----------------------------------|-------------------------------------------|
| Taken direct branch instructions  | b , ba , bl , bla , bc , bca , bcl , bcla |
| Instruction Synchronize           | isync                                     |

## 25.11.12.1.3 BTM Using Branch History Messages

Traditional BTM messaging can accurately track the number of sequential instructions between branches, but cannot accurately indicate which instructions were conditionally executed, and which were not.

Branch history messaging solves this problem by providing a predicated instruction history field in each indirect branch message. Each bit in the history represents a predicated instruction or direct branch. A value of one (1) indicates the conditional instruction was executed or the direct branch was taken. A value of  zero  (0)  indicates  the  conditional  instruction  was  not  executed  or  the  direct  branch  was  not  taken. Certain instructions ( evsel ) generate a pair of predicate bits which are both reported as consecutive bits in the history field.

Branch history messages solve predicated instruction tracking and save bandwidth since only indirect branches cause messages to be queued.

## 25.11.12.1.4 BTM Using Traditional Program Trace Messages

Based on the PTM bit in the DC register (DC[PTM]), program tracing can utilize either branch history messages (DC[PTM] = 1) or traditional direct/indirect branch messages (DC[PTM] = 0).

Branch history will save bandwidth and keep consistency between methods of program trace, yet may lose temporal  order  between  BTM  messages  and  other  types  of  messages.  Since  direct  branches  are  not messaged, but are instead included in the history field of the indirect branch history message, other types

of  messages  may  enter  the  FIFO  between  branch  history  messages.  The  development  tool  cannot determine the ordering of 'events' that occurred with respect to direct branches simply by the order in which messages are sent out.

Traditional BTM messages maintain their temporal ordering because each event that can cause a message to be queued will enter the FIFO in the order it occurred and will be messaged out maintaining that order.

## 25.11.12.2BTM Message Formats

The  e200z6  Nexus3  module  supports  three  types  of  traditional  BTM  messages-direct,  indirect,  and synchronization  messages.  It  supports  two  types  of  branch  history  BTM  messages-indirect  branch history,  and  indirect  branch  history  with  synchronization  messages.  Debug  status  messages  and  error messages are also supported.

## 25.11.12.2.1 Indirect Branch Messages (History)

Indirect branches include all taken branches whose destination is determined at run time, interrupts and exceptions. If DC[PTM] is set, indirect branch information is messaged out in the following format:

Figure 25-27. Indirect Branch Message (History) Format

<!-- image -->

## 25.11.12.2.2 Indirect Branch Messages (Traditional)

If DC[PTM] is cleared, indirect branch information is messaged out in the following format:

<!-- image -->

Max length = 50 bits; Min length = 12 bits

Figure 25-28. Indirect Branch Message Format

## 25.11.12.2.3 Direct Branch Messages (Traditional)

Direct branches (conditional or unconditional) are all taken branches whose destination is fixed in the instruction opcode. Direct branch information is messaged out in the following format:

<!-- image -->

Max length = 18 bits; Min length = 11 bits

Figure 25-29. Direct Branch Message Format

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## NOTE

When  DC[PTM]  is  set,  direct  branch  messages  will  not  be  transmitted. Instead, each direct branch or predicated instruction will toggle a bit in the history buffer.

## 25.11.12.2.4 Resource Full Messages

The resource full message is used in conjunction with the branch history messages. The resource full message is generated when the internal branch/predicate history buffer is full. If synchronization is needed at the time this message is generated, the synchronization is delayed until the next branch trace message that is not a resource full message.

The current value of the history buffer is transmitted as part of the resource full message. This information can be concatenated by the tool with the branch/predicate history information from subsequent messages to obtain the complete branch history for a message. The internal history value is reset by this message, and the I-CNT value is reset as a result of a bit being added to the history buffer.

<!-- image -->

Max length = 46 bits; Min length = 15 bits

Figure 25-30. Resource Full Message Format

## 25.11.12.2.5 Debug Status Messages

Debug status messages report low power mode and debug status. Entering/exiting debug mode as well as entering a low power mode will trigger a debug status message. Debug status information is sent out in the following format:

Figure 25-31. Debug Status Message Format

<!-- image -->

## 25.11.12.2.6 Program Correlation Messages

Program correlation messages are used to correlate events to the program flow that may not be associated with the instruction stream. In order to maintain accurate instruction tracing information when entering debug mode or a CPU low power mode (where tracing may be disabled), this message is sent upon entry into one of these two modes and includes the instruction count and branch history. Program correlation is messaged out in the following format:

Figure 25-32. Program Correlation Message Format

<!-- image -->

## 25.11.12.2.7 BTM Overflow Error Messages

An error message occurs when a new message cannot be queued due to the message queue being full. The FIFO will discard incoming messages until it has completely emptied the queue. Once emptied, an error message will be queued. The error encoding will indicate which types of messages attempted to be queued while the FIFO was being emptied.

If only a program trace message attempts to enter the queue while it is being emptied, the error message will incorporate the program trace only error encoding (00001). If both OTM and program trace messages attempt to enter the queue, the error message will incorporate the OTM and program trace error encoding (00111).  If  a  watchpoint  also  attempts  to  be  queued  while  the  FIFO  is  being  emptied,  then  the  error message will incorporate error encoding (01000).

## NOTE

The OVC bits within the DC1 register can be set to delay the CPU in order to alleviate (but not eliminate) potential overrun situations.

Error information is messaged out in the following format

:

Figure 25-33. Error Message Format

<!-- image -->

## 25.11.12.2.8 Program Trace Synchronization Messages

A program trace direct/indirect branch with sync message is messaged via the auxiliary port (provided program trace is enabled) for the following conditions (see Table 25-35):

- · Initial program trace message upon the first direct/indirect branch after exit from system reset or whenever program trace is enabled
- · Upon direct/indirect branch after returning from a CPU low power state
- · Upon direct/indirect branch after returning from debug mode
- · Upon direct/indirect branch after occurrence of queue overrun (can be caused by any trace message), provided program trace is enabled
- · Upon direct/indirect branch after the periodic program trace counter has expired indicating 255 without-sync program trace messages have occurred since the last with-sync message occurred
- · Upon direct/indirect branch after assertion of the event in (EVTI) pin if the EIC bits within the DC1 register have enabled this feature

## Nexus Development Interface

- · Upon direct/indirect branch after the sequential instruction counter has expired indicating 255 instructions have occurred between branches
- · Upon direct/indirect branch after a BTM message was lost due to an attempted access to a secure memory location.
- · Upon direct/indirect branch after a BTM message was lost due to a collision entering the FIFO between the BTM message and either a watchpoint message or an ownership trace message

If the NZ6C3 module is enabled at reset, a EVTI assertion initiates a program trace direct/indirect branch with  sync  message  (if  program  trace  is  enabled)  upon  the  first  direct/indirect  branch.  The  format  for program trace direct/indirect branch with sync messages is as follows:

<!-- image -->

Max length = 50 bits; Min length = 12 bits

Figure 25-34. Direct/Indirect Branch with Sync Message Format

The formats for program trace direct/indirect branch with sync. messages and indirect branch history with sync. messages are as follows

:

<!-- image -->

Max length = 82 bits; Min length = 13 bits

Figure 25-35. Indirect Branch History with Sync. Message Format

Exception conditions that result in program trace synchronization are summarized in Table 25-35.

Table 25-35. Program Trace Exception Summary

| Exception Condition       | Exception Handling                                                                                                                                                                                                                                                                                                                                                                                                                 |
|---------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| System Reset Negation     | At the negation of JTAG reset (JCOMP), queue pointers, counters, state machines, and registers within the NZ6C3 module are reset. Upon the first branch out of system reset (if program trace is enabled), the first program trace message is a direct/indirect branch with sync. message.                                                                                                                                         |
| Program Trace Enabled     | The first program trace message (after program trace has been enabled) is a synchronization message.                                                                                                                                                                                                                                                                                                                               |
| Exit from Low Power/Debug | Upon exit from a low power mode or debug mode the next direct/indirect branch will be converted to a direct/indirect branch with sync. message.                                                                                                                                                                                                                                                                                    |
| Queue Overrun             | An error message occurs when a new message cannot be queued due to the message queue being full. The FIFO will discard messages until it has completely emptied the queue. Once emptied, an error message will be queued. The error encoding will indicate which types of messages attempted to be queued while the FIFO was being emptied. The next BTM message in the queue will be a direct/indirect branch with sync. message. |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 25-35. Program Trace Exception Summary (continued)

| Exception Condition                   | Exception Handling                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
|---------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Periodic Program Trace Sync.          | A forced synchronization occurs periodically after 255 program trace messages have been queued. Adirect/indirect branch with sync. message is queued. The periodic program trace message counter then resets.                                                                                                                                                                                                                                                                                                                                                                                               |
| Event In                              | If the Nexus module is enabled, an EVTI assertion initiates a direct/indirect branch with sync. message upon the next direct/indirect branch (if program trace is enabled and the EIC bits of the DC1 register have enabled this feature).                                                                                                                                                                                                                                                                                                                                                                  |
| Sequential Instruction Count Overflow | When the sequential instruction counter reaches its maximum count (up to 255 sequential instructions may be executed), a forced synchronization occurs. The sequential counter then resets. A program trace direct/indirect branch with sync.message is queued upon execution of the next branch.                                                                                                                                                                                                                                                                                                           |
| Attempted Access to Secure Memory     | For devices which implement security, any attempted branch to secure memory locations will temporarily disable program trace & cause the corresponding BTMto be lost. The following direct/indirect branch will queue a direct/indirect branch with sync. message. The count value within this message will be inaccurate since the re-enable of program trace is not necessarily aligned on an instruction boundary.                                                                                                                                                                                       |
| Collision Priority                    | All messages have the following priority: WPM -> OTM -> BTM -> DTM. A BTM message which attempts to enter the queue at the same time as a watchpoint message or ownership trace message will be lost. An error message will be sent indicating the BTM was lost. The following direct/indirect branch will queue a direct/indirect branch with sync. message. The count value within this message will reflect the number of sequential instructions executed after the last successful BTMMessage was generated. This count will include the branch which did not generate a message due to the collision. |

## 25.11.12.3BTM Operation

## 25.11.12.3.1 Enabling Program Trace

Both types of branch trace messaging can be enabled in one of two ways:

- · Setting the TM field of the DC1 register to enable program trace (DC1[TM])
- · Using the PTS field of the WT register to enable program trace on watchpoint hits (e200z6 watchpoints are configured within the CPU)

## 25.11.12.3.2 Relative Addressing

The relative address feature is compliant with the IEEE ® -ISTO 5001-2003 standard recommendations, and is designed to reduce the number of bits transmitted for addresses of indirect branch messages.

The address transmitted is relative to the target address of the instruction which triggered the previous indirect branch (or sync) message. It is generated by XOR'ing the new address with the previous address, and then using only the results up to the most significant 1 in the result. To recreate this address, an XOR of the (most-significant 0-padded) message address with the previously decoded address gives the current address.

Previous address (A1) =0x0003FC01, New address (A2) = 0x0003F365

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Message Generation: A1 = 0000 0000 0000 0011 1111 1100 0000 0001 A2 = 0000 0000 0000 0011 1111 0011 0110 0101 A1     A2 = 0000 0000 0000 0000 0000 1111 0110 0100 Address Message (M1) = 1111 0110 0100 Address Re-creation: A1     M1 = A2 A1 = 0000 0000 0000 0011 1111 1100 0000 0001 M1 = 0000 0000 0000 0000 0000 1111 0110 0100 A2 = 0000 0000 0000 0011 1111 0011 0110 0101

Figure 25-36. Relative Address Generation and Re-creation

## 25.11.12.3.3 Branch/Predicate Instruction History (HIST)

If DC[PTM] is set, BTM messaging will use the branch history format. The branch history (HIST) packet in these messages provides a history of direct branch execution used for reconstructing the program flow. This packet is implemented as a left-shifting shift register. The register is always pre-loaded with a value of one (1). This bit acts as a stop bit so that the development tools can determine which bit is the end of the history information. The pre-loaded bit itself is not part of the history, but is transmitted with the packet.

A value of one (1) is shifted into the history buffer on a taken branch (condition or unconditional) and on any instruction whose predicate condition executed as true. A value of zero (0) is shifted into the history buffer on any instruction whose predicate condition executed as false as well as on branches not taken. This will include indirect as well as direct branches not taken. For the evsel instruction, two bits are shifted in, corresponding to the low element (shifted in first) and the high element (shifted in second) conditions.

## 25.11.12.3.4 Sequential Instruction Count (I-CNT)

The I-CNT packet, is present in all BTM messages. For traditional branch messages, I-CNT represents the number of sequential instructions, or non-taken branches in between direct/indirect branch messages.

For  branch  history  messages,  I-CNT  represents  the  number  of  instructions  executed  since  the  last taken/non-taken direct branch, last taken indirect branch or exception. Not taken indirect branches are considered sequential instructions and cause the instruction count to increment. I-CNT also represents the number of instructions executed since the last predicate instruction.

The sequential instruction counter overflows when its value reaches 255. The next BTM message will be converted to a synchronization type message.

## 25.11.12.3.5 Program Trace Queueing

NZ6C3 implements a message queue. Messages that enter the queue are transmitted via the auxiliary pins in the order in which they are queued.

## NOTE

If multiple trace messages need to be queued at the same time, Watchpoint Messages will have the highest priority (WPM -&gt; OTM -&gt; BTM -&gt; DTM).

## 25.11.12.4Program Trace Timing Diagrams

<!-- image -->

TCODE = 4

Source Processor = 0b0000

Number of Sequence Instructions = 128

Relative Address = 0xA5

Figure 25-37. Program Trace (MDO = 12)-Indirect Branch Message (Traditional)

<!-- image -->

TCODE = 28

Source Processor = 0b0000

Number of Sequential Instructions = 0

Relative Address = 0xA5

Branch History = 0b1010\_0101 (with Stop)

Figure 25-38. Program Trace (MDO = 2)-Indirect Branch Message (History)

<!-- image -->

Figure 25-39. Program Trace-Direct Branch (Traditional) and Error Messages

<!-- image -->

TCODE = 12

Source Processor = 0b0000

Number of Sequential Instructions = 3

Full Target Address = 0xDEAD\_FACE

Figure 25-40. Program Trace-Indirect Branch with Sync. Message

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## 25.11.13 Data Trace

This  section  deals  with  the  data  trace  mechanism  supported  by  the  NZ6C3  module.  Data  trace  is implemented via data write messaging (DWM) and data read messaging (DRM), as per the IEEE ® -ISTO 5001-2003 standard.

## 25.11.13.1Data Trace Messaging (DTM)

Data trace messaging for e200z6 is accomplished by snooping the e200z6 virtual data bus (between the CPU and MMU), and storing the information for qualifying accesses (based on enabled features and matching target addresses). The NZ6C3 module traces all data access that meet the selected range and attributes.

## NOTE

Data trace is only performed on the e200z6 virtual data bus. This allows for data visibility for the incorporated data cache. Only e200z6 CPU initiated accesses will be traced. No DMA accesses to the AHB system bus will be traced.

Data trace messaging can be enabled in one of two ways:

- · Setting the TM field of the DC1 register to enable data trace (DC1[TM]).
- · Using WT[DTS] to enable data trace on watchpoint hits (e200z6 watchpoints are configured within the Nexus1 module)

## 25.11.13.2 DTM Message Formats

The  Nexus3  module  supports  five  types  of  DTM  messages:  data  write,  data  read,  data  write synchronization, data read synchronization and error messages.

## 25.11.13.2.1 Data Write Messages

The data write message contains the data write value and the address of the write access, relative to the previous data trace message. Data write message information is messaged out in the following format:

<!-- image -->

Max length = 109 bits; Min length = 15 bits

Figure 25-41. Data Write Message Format

## 25.11.13.2.2 Data Read Messages

The data read message contains the data read value and the address of the read access, relative to the previous data trace message. Data read message information is messaged out in the following format:

Figure 25-42. Data Read Message Format

<!-- image -->

## NOTE

For the e200z6 based CPU, the double-word encoding (data size = 0b000) will indicate a double-word access and will be sent out as a single data trace message with a single 64-bit data value.

## 25.11.13.2.3 DTM Overflow Error Messages

An error message occurs when a new message cannot be queued due to the message queue being full. The FIFO will discard incoming messages until it has completely emptied the queue. Once emptied, an error message will be queued. The error encoding will indicate which types of messages attempted to be queued while the FIFO was being emptied.

If only a data trace message attempts to enter the queue while it is being emptied, the error message will incorporate the data trace only error encoding (00010). If both OTM and data trace messages attempt to enter the queue, the error message will incorporate the OTM and data trace error encoding (00111). If a watchpoint also attempts to be queued while the FIFO is being emptied, then the error message will incorporate error encoding (01000).

## NOTE

The OVC bits within the DC1 register can be set to delay the CPU in order to alleviate (but not eliminate) potential overrun situations.

Error information is messaged out in the following format:

Figure 25-43. Error Message Format

<!-- image -->

## 25.11.13.2.4 Data Trace Synchronization Messages

A data trace write/read with sync. message is messaged via the auxiliary port (provided data trace is enabled) for the following conditions (see Table 25-36):

- · Initial data trace message after exit from system reset or whenever data trace is enabled
- · Upon exiting debug mode
- · After occurrence of queue overrun (can be caused by any trace message), provided data trace is enabled
- · After the periodic data trace counter has expired indicating 255 without-sync data trace messages have occurred since the last with-sync message occurred

## Nexus Development Interface

- · Upon assertion of the event in (EVTI) pin, the first data trace message will be a synchronization message if the EIC bits of the DC1 register have enabled this feature
- · Upon data trace write/read after the previous DTM message was lost due to an attempted access to a secure memory location
- · Upon data trace write/read after the previous DTM message was lost due to a collision entering the FIFO between the DTM message and any of the following: watchpoint message, ownership trace message, or branch trace message

Data  trace  synchronization  messages  provide  the  full  address  (without  leading  zeros)  and  insure  that development  tools  fully  synchronize  with  data  trace  regularly.  Synchronization  messages  provide  a reference address for subsequent data messages, in which only the unique portion of the data trace address is transmitted. The format for data trace write/read with sync. messages is as follows:

Figure 25-44. Data Write/Read with Sync. Message Format

<!-- image -->

Exception conditions that result in data trace synchronization are summarized in Table 25-36.

Table 25-36. Data Trace Exception Summary

| Exception Condition            | Exception Handling                                                                                                                                                                                                                                                                                                                                                                                                          |
|--------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| System Reset Negation          | At the negation of JTAGreset (JCOMP), queue pointers, counters, state machines, and registers within the NZ6C3 module are reset. If data trace is enabled, the first data trace message is a data write/read with sync. message.                                                                                                                                                                                            |
| Data Trace Enabled             | The first data trace message (after data trace has been enabled) is a synchronization message.                                                                                                                                                                                                                                                                                                                              |
| Exit from Low Power/Debug      | Upon exit from a low power mode or debug mode the next data trace message will be converted to a data write/read with sync. message.                                                                                                                                                                                                                                                                                        |
| Queue Overrun                  | An error message occurs when a new message cannot be queued due to the message queue being full. The FIFO will discard messages until it has completely emptied the queue. Once emptied, an error message will be queued. The error encoding will indicate which types of messages attempted to be queued while the FIFO was being emptied. The next DTM message in the queue will be a data write/read with sync. message. |
| Periodic Data Trace Sync.      | A forced synchronization occurs periodically after 255 data trace messages have been queued. A data write/read with sync. message is queued. The periodic data trace message counter then resets.                                                                                                                                                                                                                           |
| Event In                       | If the Nexus module is enabled, a EVTI assertion initiates a data trace write/read with sync. message upon the next data write/read (if data trace is enabled and the EIC bits of the DC1 register have enabled this feature).                                                                                                                                                                                              |
| AttemptedAccesstoSecure Memory | For devices which implement security, any attempted read or write to secure memory locations will temporarily disable data trace & cause the corresponding DTM to be lost. A subsequent read/write will queue a data trace read/write with sync. message.                                                                                                                                                                   |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 25-36. Data Trace Exception Summary (continued)

| Exception Condition   | Exception Handling                                                                                                                                                                                                                                                                                           |
|-----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Collision Priority    | All messages have the following priority: WPM -> OTM -> BTM -> DTM. A DTM message which attempts to enter the queue at the same time as a watchpoint message or ownership trace message or branch trace message will be lost. A subsequent read/write will queue a data trace read/write with sync. message. |

## 25.11.13.3DTM Operation

## 25.11.13.3.1 DTM Queueing

NZ6C3 implements a message queue for DTM messages. Messages that enter the queue are transmitted via the auxiliary pins in the order in which they are queued.

## NOTE

If multiple trace messages need to be queued at the same time, watchpoint messages will have the highest priority (WPM -&gt; OTM -&gt; BTM -&gt; DTM).

## 25.11.13.3.2 Relative Addressing

The relative address feature is compliant with the IEEE ® -ISTO 5001-2003 standard recommendations, and is designed to reduce the number of bits transmitted for addresses of data trace messages. Refer to Section 25.11.12.3.2, ' Relative Addressing for details.

## 25.11.13.3.3 Data Trace Windowing

Data write/read messages are enabled via the RWT1(2) field in the data trace control register (DTC) for each DTM channel. Data trace windowing is achieved via the address range defined by the DTEA and DTSA registers and by the RC1(2) field in the DTC. All e200z6 initiated read/write accesses which fall inside or outside these address ranges, as programmed, are candidates to be traced.

## 25.11.13.3.4 Data Access/Instruction Access Data Tracing

The Nexus3 module is capable of tracing both instruction access data or data access data. Each trace window can be configured for either type of data trace by setting the DI1(2) field within the data trace control register for each DTM channel.

## 25.11.13.3.5 e200z6 Bus Cycle Special Cases

Table 25-37. e200z6 Bus Cycle Cases

| Special Case                             | Action                       |
|------------------------------------------|------------------------------|
| e200z6 bus cycle aborted                 | Cycle ignored                |
| e200z6 bus cycle with data error (TEA)   | Data Trace Message discarded |
| e200z6 bus cycle completed without error | Cycle captured & transmitted |
| e200z6 bus cycle initiated by NZ6C3      | Cycle ignored                |
| e200z6 bus cycle is an instruction fetch | Cycle ignored                |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 25-37. e200z6 Bus Cycle Cases (continued)

| Special Case                                                                                                                                        | Action                                                    |
|-----------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------|
| e200z6 bus cycle accesses misaligned data (across 64-bit boundary)-both 1st & 2nd transactions within data trace range                              | 1st & 2nd cycle captured & 2 DTM's transmitted (see Note) |
| e200z6 bus cycle accesses misaligned data (across 64-bit boundary)-1st transaction within data trace range; 2nd transaction out of data trace range | 1st cycle captured and transmitted; 2nd cycle ignored     |
| e200z6 bus cycle accesses misaligned data (across 64-bit boundary)-1st transaction out of data trace range; 2nd transaction within data trace range | 1st cycle ignored; 2nd cycle capture and transmitted      |

## NOTE

For misaligned accesses (crossing 64-bit boundary), the access is broken into  two  accesses.  If  both  accesses  are  within  the  data  trace  range,  two DTMs will be  sent:  one  with  a  size  encoding  indicating  the  size  of  the original access (that is, word), and one with a size encoding for the portion which crossed the boundary (that is, 3-byte).

## NOTE

An STM to the cache's store buffer within the data trace range will initiate a  DTM message. If the corresponding memory access causes an error, a checkstop condition will occur. The debug/development tool should use this indication to invalidate the previous DTM.

## 25.11.13.4 Data Trace Timing Diagrams (8 MDO Configuration)

<!-- image -->

TCODE = 5 Source Processor = 0b0000 Data Size = 010 (Half-Word) Relative Address = 0xA5 Write Data = 0xBEEF

Figure 25-45. Data Trace-Data Write Message

Figure 25-46. Data Trace-Data Read with Sync Message

00001110

11000000

01011001

11010001

00101000

00000000

01011100

MCKO

MSEO\_B[1:0]

TCODE = 14 Source Processor = 0b0000 Data Size = 000 (Byte) Full Access Address = 0x0146\_8ACE

00

MDO[7:0]

11

Write Data = 0x5C

01

11

MCKO

MSEO\_B[1:0]

TCODE = 8

Source Processor = 0b0000

Error Code = 2 (Queue Overrun - DTM Only)

00

MDO[7:0]

11

11

xx

00001000

00001000

xxxxxxxx

Figure 25-47. Error Message (Data Trace only encoded)

## 25.11.14 Watchpoint Support

This section details the watchpoint features of the NZ6C3 module.

## 25.11.14.1Overview

The NZ6C3 module provides watchpoint messaging via the auxiliary pins, as defined by the IEEE ® -ISTO 5001-2003 standard.

NZ6C3 is not compliant with Class4 breakpoint/watchpoint requirements defined in the standard. The breakpoint/watchpoint control register is not implemented.

## 25.11.14.2Watchpoint Messaging

Enabling watchpoint messaging is done by setting the watchpoint enable bit in the DC1 register. Setting the individual watchpoint sources is supported through the e200z6 Nexus1 module. The e200z6 Nexus1 module is capable of setting multiple address and/or data watchpoints. Please refer to the e200z6 Core Reference Manual for more information on watchpoint initialization.

When these watchpoints occur, a watchpoint event signal from the Nexus1 module causes a message to be sent to the queue to be messaged out. This message includes the watchpoint number indicating which watchpoint caused the message.

The occurrence of any of the e200z6 defined watchpoints can be programmed to assert the event out EVTO pin for one (1) period of the output clock (MCKO).

Watchpoint information is messaged out in the following format

Figure 25-48. Watchpoint Message Format.

<!-- image -->

Table 25-38. Watchpoint Source Encoding

|   Watchpoint Source (8 bits) | Watchpoint Description                   |
|------------------------------|------------------------------------------|
|                     00000001 | e200z6 Watchpoint #0 (IAC1 from Nexus1)  |
|                     00000010 | e200z6 Watchpoint #1 (IAC2 from Nexus1)  |
|                     00000100 | e200z6 Watchpoint #2 (IAC3 from Nexus1)  |
|                     00001000 | e200z6 Watchpoint #3 (IAC4 from Nexus1)  |
|                     00010000 | e200z6 Watchpoint #4 (DAC1 from Nexus1)  |
|                     00100000 | e200z6 Watchpoint #5 (DAC2 from Nexus1)  |
|                     01000000 | e200z6 Watchpoint #6 (DCNT1 from Nexus1) |
|                     10000000 | e200z6 Watchpoint #7 (DCNT2 from Nexus1) |

## 25.11.14.3Watchpoint Error Message

An error message occurs when a new message cannot be queued due to the message queue being full. The FIFO will discard messages until it has completely emptied the queue. Once emptied, an error message will be queued. The error encoding will indicate which types of messages attempted to be queued while the FIFO was being emptied.

If only a watchpoint message attempts to enter the queue while it is being emptied, the error message will incorporate the watchpoint only error encoding (00110). If an OTM and/or program trace and/or data trace message also attempts to enter the queue while it is being emptied, the error message will incorporate error encoding (01000).

## NOTE

The OVC bits within the DC1 register can be set to delay the CPU in order to alleviate (but not eliminate) potential overrun situations.

Error information is messaged out in the following format (see Table 25-20)

:

Figure 25-49. Error Message Format

<!-- image -->

## 25.11.14.4Watchpoint Timing Diagram (2 MDO/1 MSEO Configuration)

Figure 25-50. Watchpoint Message &amp; Watchpoint Error Message

<!-- image -->

## 25.11.15 NZ6C3 Read/Write Access to Memory-Mapped Resources

The read/write access feature allows access to memory-mapped resources via the JTAG/OnCE port. The read/write mechanism supports single as well as block reads and writes to e200z6 system bus resources.

The  NZ6C3  module  is  capable  of  accessing  resources  on  the  e200z6  system  bus,  with  multiple configurable priority levels. Memory-mapped registers and other non-cached memory can be accessed via the standard memory map settings.

All accesses are setup and initiated by the read/write access control/status register (RWCS), as well as the read/write access address (RWA) and read/write access data registers (RWD).

## Nexus Development Interface

Using the read/write access registers (RWCS/RWA/RWD), memory-mapped e200z6 system bus resources can be accessed through NZ6C3. The following subsections describe the steps which are required to access memory-mapped resources.

## NOTE

Read/write access can only access memory mapped resources when system reset is de-asserted.

Misaligned accesses are NOT supported in the e200z6 Nexus3 module.

## 25.11.15.1Single Write Access

- 1. Initialize the read/write access address register (RWA) through the access method outlined in Section 25.11.10, ' NZ6C3 Register Access via JTAG / OnCE' using the Nexus register index of 0x9 (see Table 25-24). Configure as follows:
- -Write Address -&gt; 0xnnnnnnnn (write address)
- 2. Initialize the read/write access control/status register (RWCS) through the access method outlined in Section 25.11.10, ' NZ6C3 Register Access via JTAG / OnCE,' using the Nexus Register Index of 0x7(see Table 25-24). Configure the bits as follows:

- Access Control RWCS[AC]

-&gt; 0b1 (to indicate start access)

-

Map Select RWCS[MAP] -&gt; 0b000 (primary memory map)

-

Access Priority RWCS[PR] -&gt; 0b00 (lowest priority)

- Read/Write RWCS[RW]

-&gt; 0b1 (write access)

- Word Size RWCS[SZ]

-&gt; 0b0xx (32-bit, 16-bit, 8-bit)

- Access Count RWCS[CNT]

-&gt; 0x0000 or 0x0001 (single access)

## NOTE

Access  count  RWCS[CNT]  of  0x0000  or  0x0001  will  perform  a  single access.

- 3. Initialize the read/write access data register (RWD) through the access method outlined in Section 25.11.10, ' NZ6C3 Register Access via JTAG / OnCE,' using the Nexus register index of 0xA (see Table 25-24). Configure as follows:
- -Write Data -&gt; 0xnnnnnnnn (write data)
- 4. The NZ6C3 module will then arbitrate for the system bus and transfer the data value from the data buffer RWD register to the memory mapped address in the read/write access address register (RWA). When the access has completed without error (ERR=1'b0), NZ6C3 asserts the RDY pin and clears the DV bit in the RWCS register. This indicates that the device is ready for the next access.

## NOTE

Only the RDY pin as well as the DV and ERR bits within the RWCS provide read/write access status to the external development tool.

## 25.11.15.2Block Write Access (Non-Burst Mode)

- 1. For a non-burst block write access, follow Steps 1, 2, and 3 outlined in Section 25.11.15.1, 'Single Write Access to initialize the registers,' but using a value greater than one (0x1) for the RWCS[CNT] field.
- 2. The NZ6C3 module will then arbitrate for the system bus and transfer the first data value from the RWD register to the memory mapped address in the read/write access address register (RWA). When the transfer has completed without error (ERR = 0), the address from the RWA register is incremented to the next word size (specified in the SZ field) and the number from the CNT field is decremented. Nexus will then assert the RDY pin. This indicates that the device is ready for the next access.
- 3. Repeat step 3 in Section 25.11.15.1, 'Single Write Access' until the internal CNT value is zero (0). When this occurs, the DV bit within the RWCS will be cleared to indicate the end of the block write access.

## 25.11.15.3Block Write Access (Burst Mode)

- 1. For a burst block write access, follow Steps 1 and 2 outlined in Section 25.11.15.1, 'Single Write Access' to initialize the registers, using a value of four (double-words) for the CNT field and a RWCS[SZ] field indicating 64-bit access.
- 2. Initialize the burst data buffer (read/write access data register) through the access method outlined in Section 25.11.10, ' NZ6C3 Register Access via JTAG / OnCE,' using the Nexus register Index of 0xA (see Table 25-24).
- 3. Repeat step 2 until all double-word values are written to the buffer.

## NOTE

The  data  values  must  be  shifted  in  32-bits  at  a  time  lsb  first  (that  is, double-word write = two word writes to the RWD).

- 4. The Nexus module will then arbitrate for the system bus and transfer the burst data values from the data buffer to the system bus beginning from the memory mapped address in the read/write access address register (RWA). For each access within the burst, the address from the RWA register is incremented to the next double-word size (specified in the SZ field) modulo the length of the burst, and the number from the CNT field is decremented.
- 5. When the entire burst transfer has completed without error (ERR = 0), NZ6C3 will then assert the RDY pin, and the DV bit within the RWCS will be cleared to indicate the end of the block write access.

## NOTE

The actual RWA value as well as the CNT field within the RWCS are not changed  when  executing  a  block  write  access  (burst  or  non-burst).  The original values can be read by the external development tool at any time.

## 25.11.15.4Single Read Access

- 1. Initialize the read/write access address register (RWA) through the access method outlined in Section 25.11.10, ' NZ6C3 Register Access via JTAG / OnCE,' using the Nexus register index of 0x9 (see Table 25-24). Configure as follows:
- -Read Address
- -&gt; 0xnnnnnnnn (read address)
- 2. Initialize the read/write access control/status register (RWCS) through the access method outlined in Section 25.11.10, ' NZ6C3 Register Access via JTAG / OnCE,' using the Nexus register index of 0x7 (see Table 25-24). Configure the bits as follows:
- -
- Access Control RWCS[AC]
- -&gt; 0b1 (to indicate start access)
- -Map Select RWCS[MAP]
- -Access Priority RWCS[PR]
- -Read/Write RWCS[RW]
- -Word Size RWCS[SZ]
- -Access Count RWCS[CNT]
- -&gt; 0b000 (primary memory map)
- -&gt; 0b00 (lowest priority)
- -&gt; 0b0 (read access)
- -&gt; 0b0xx (32-bit, 16-bit, 8-bit)
- -&gt; 0x0000 or 0x0001 (single access)

## NOTE

Access Count (CNT) of 0x0000 or 0x0001 will perform a single access.

- 3. The NZ6C3 module will then arbitrate for the system bus and the read data will be transferred from the system bus to the RWD register. When the transfer is completed without error (ERR = 0), Nexus asserts the RDY pin and sets the DV bit in the RWCS register. This indicates that the device is ready for the next access.
- 4. The data can then be read from the read/write access data register (RWD) through the access method outlined in Section 25.11.10, ' NZ6C3 Register Access via JTAG / OnCE,' using the Nexus register index of 0xA (see Table 25-24).

## NOTE

Only the RDY pin as well as the DV and ERR bits within the RWCS provide Read/Write Access status to the external development tool.

## 25.11.15.5Block Read Access (Non-Burst Mode)

- 1. For a non-burst block read access, follow Steps 1 and 2 outlined in Section 25.11.15.4, 'Single Read Access' to initialize the registers, but using a value greater than one (0x1) for the CNT field in the RWCS register.
- 2. The NZ6C3 module will then arbitrate for the system bus and the read data will be transferred from the system bus to the RWD register. When the transfer has completed without error (ERR=0b0), the address from the RWA register is incremented to the next word size (specified in the SZ field) and the number from the CNT field is decremented. Nexus will then assert the RDY pin. This indicates that the device is ready for the next access.
- 3. The data can then be read from the read/write access data register (RWD) through the access method outlined in Section 25.11.10, ' NZ6C3 Register Access via JTAG / OnCE,' using the Nexus register index of 0xA (see Table 25-24).

- 4. Repeat steps 3 and 4 in Section 25.11.15.4, 'Single Read Access' until the CNT value is zero (0). When this occurs, the DV bit within the RWCS is set to indicate the end of the block read access.

## 25.11.15.6Block Read Access (Burst Mode)

- 5. For a burst block read access, follow Steps 1 and 2 outlined in Section 25.11.15.4, 'Single Read Access' to initialize the registers, using a value of four (double-words) for the CNT field and an RWCS[SZ] field indicating 64-bit access.
- 6. The NZ6C3 module will then arbitrate for the system bus and the burst read data will be transferred from the system bus to the data buffer (RWD register). For each access within the burst, the address from the RWA register is incremented to the next double-word (specified in the SZ field) and the number from the CNT field is decremented.
- 7. When the entire burst transfer has completed without error (ERR = 0), Nexus will then assert the RDY pin and the DV bit within the RWCS will be set to indicate the end of the block read access.
- 8. The data can then be read from the burst data buffer (read/write access data register) through the access method outlined in Section 25.11.10, ' NZ6C3 Register Access via JTAG / OnCE,' using the Nexus register index of 0xA (see Table 25-24).
- 9. Repeat step 3 until all double-word values are read from the buffer.

## NOTE

The  data  values  must  be  shifted  out  32-bits  at  a  time  lsb  first  (that  is, double-word read = two word reads from the RWD).

## NOTE

The actual RWA value as well as the CNT field within the RWCS are not changed  when  executing  a  block  read  access  (burst  or  non-burst).  The original values can be read by the external development tool at any time.

## 25.11.15.7Error Handling

The NZ6C3 module handles various error conditions as follows:

## 25.11.15.7.1 System Bus Read/Write Error

All address and data errors that occur on read/write accesses to the e200z6 system bus will return a transfer error. If this occurs:

- 1. The access is terminated without re-trying (AC bit is cleared).
- 2. The ERR bit in the RWCS register is set.
- 3. The error message is sent (TCODE = 8) indicating read/write error.

## 25.11.15.7.2 Access Termination

The following cases are defined for sequences of the read/write protocol that differ from those described in the above sections:

- 1. If the AC bit in the RWCS register is set to start read/write accesses and invalid values are loaded into the RWD and/or RWA, then a system bus access error may occur. This is handled as described above.

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## Nexus Development Interface

- 2. If a block access is in progress (all cycles not completed), and the RWCS register is written, then the original block access is terminated at the boundary of the nearest completed access.
- a) If the RWCS is written with the AC bit set, the next read/write access will begin and the RWD can be written to/ read from.
- b) If the RWCS is written with the AC bit cleared, the read/write access is terminated at the nearest completed access. This method can be used to break (early terminate) block accesses.

## 25.11.15.8 Read/Write Access Error Message

The read/write access error  message  is  sent  out  when  an  system  bus  access  error  (read  or  write)  has occurred.

Error information is messaged out in the following format:

Figure 25-51. Error Message Format

<!-- image -->

## 25.11.16 Examples

The following are examples of program trace and data trace messages.

Table 25-39 illustrates an example indirect branch message with an 8 MDO / 2 MSEO configuration.

Note that T0 and S0 are the least significant bits where:

- · Tx = TCODE number (fixed)
- · Sx = Source processor (fixed)
- · Ix = Number of instructions (variable)
- · Ax = Unique portion of the address (variable)

Table 25-39. Indirect Branch Message Example (12 MDO / 2 MSEO)

| Clock   | MDO[11:0]   | MDO[11:0]   | MDO[11:0]   | MDO[11:0]   | MDO[11:0]   | MDO[11:0]   | MDO[11:0]   | MDO[11:0]   | MDO[11:0]   | MDO[11:0]   | MDO[11:0]   | MDO[11:0]   |    |    | State                         |
|---------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|----|----|-------------------------------|
| Clock   | 11          | 10          | 9           | 8           | 7           | 6           | 5           | 4           | 3           | 2           | 1           | 0           |    |    | State                         |
| 0       | X           | X           | X           | X           | X           | X           | X           | X           | X           | X           | X           | X           | 1  | 1  | Idle (or end of last message) |
| 1       | I1          | I0          | S3          | S2          | S1          | S0          | T5          | T4          | T3          | T2          | T1          | T0          | 0  | 0  | Start Message                 |
| 2       | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | I5          | I4          | I3          | I2          | 0  | 1  | End Packet                    |
| 3       | 0           | A10         | A9          | A8          | A7          | A6          | A5          | A4          | A3          | A2          | A1          | A0          | 1  | 1  | End Packet/End Message        |
| 4       | X           | X           | S3          | S2          | S1          | S0          | T5          | T4          | T3          | T2          | T1          | T0          | 0  | 0  | Start of Next Message         |

Table 25-40 illustrates an example of direct branch message with 12 MDO / 2 MSEO.

Note that T0 and I0 are the least significant bits where:

- · Tx = TCODE number (fixed)
- · Sx = Source processor (fixed)
- · Ix = Number of instructions (variable)

## Table 25-40. Direct Branch Message Example (12 MDO / 2 MSEO)

| Clock   | MDO[11:0]   | MDO[11:0]   | MDO[11:0]   | MDO[11:0]   | MDO[11:0]   | MDO[11:0]   | MDO[11:0]   | MDO[11:0]   | MDO[11:0]   | MDO[11:0]   | MDO[11:0]   |   MDO[11:0] | MSEO[1:0]   | State                         |
|---------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------------------------|
| Clock   | 11          | 10          | 9           | 8           | 7           | 6           | 5           | 4           | 3           | 2           | 1           |           0 |             | State                         |
| 0       | X           | X           | X           | X           | X           | X           | X           | X           | X X         | X           | X           |           1 | 1           | Idle (or end of last message) |
| 1       | I1          | I0          | S3          | S2          | S1          | S0          | T5          | T4          | T3 T2       | T1          | T0          |           0 | 0           | Start Message                 |
| 2       | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0 0         | I3          | I2          |           1 | 1           | End Packet/End Message        |
| 3       | X           | X           | X           | X           | S1          | S0          | T5          | T4          | T3 T2       | T1          | T0          |           0 | 0           | Start of Next Message         |

Table 25-41 an example data write message with 12 MDO / 2 MSEO configuration

Note that T0, A0, D0 are the least significant bits where:

- · Tx = TCODE number (fixed)
- · Sx = Source processor (fixed)
- · Zx = Data size (fixed)
- · Ax = Unique portion of the address (variable)
- · Dx = Write data (variable - 8, 16 or 32-bit)

Table 25-41. Direct Write Message Example (12 MDO / 2 MSEO)

| Clock   | MDO[11:0]   | MDO[11:0]   | MDO[11:0]   | MDO[11:0]   | MDO[11:0]   | MDO[11:0]   | MDO[11:0]   | MDO[11:0]   | MDO[11:0]   | MDO[11:0]   | MDO[11:0]   | MDO[11:0]   | MSEO[1:0]   | State                         |
|---------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------------------------|
| Clock   | 11          | 10          | 9           | 8           | 7           | 6           | 5           | 4           | 3           | 2           | 1 0         |             |             | State                         |
| 0       | X           | X           | X           | X           | X           | X           | X           | X           | X X         | X           | X           | 1           | 1           | Idle (or end of last message) |
| 1       | Z1          | Z0          | S3          | S2          | S1          | S0          | T5          | T4          | T3 T2       | T1          | T0          | 0           | 0           | Start Message                 |
| 2       | 0           | 0           | 0           | 0           | 0           | 0           | 0           | A3          | A2 A1       | A0          | Z2          | 0           | 1           | End Packet                    |
| 3       | X           | X           | X           | X           | D7          | D6          | D5          | D4          | D3 D2       | D1          | D0          | 1           | 1           | End Packet/End Message        |

## 25.11.17 IEEE ® 1149.1 (JTAG) RD/WR Sequences

This section contains example JTAG/OnCE sequences used to access resources.

## 25.11.17.1JTAG Sequence for Accessing Internal Nexus Registers

Table 25-42. Accessing Internal Nexus3 Registers via JTAG/OnCE

|   Step # |   TMS Pin | Description                                                                                  |
|----------|-----------|----------------------------------------------------------------------------------------------|
|        1 |         1 | IDLE -> SELECT-DR_SCAN                                                                       |
|        2 |         0 | SELECT-DR_SCAN -> CAPTURE-DR (Nexus command register value loaded in shifter)                |
|        3 |         0 | CAPTURE-DR -> SHIFT-DR                                                                       |
|        4 |         0 | (7) TCK clocks issued to shift in direction (rd/wr) bit and first 6 bits of Nexus reg. addr. |
|        5 |         1 | SHIFT-DR -> EXIT1-DR (7th bit of Nexus reg. shifted in)                                      |
|        6 |         1 | EXIT1-DR -> UPDATE-DR (Nexus shifter is transferred to Nexus command register)               |
|        7 |         1 | UPDATE-DR -> SELECT-DR_SCAN                                                                  |
|        8 |         0 | SELECT-DR_SCAN -> CAPTURE-DR (Register value is transferred to Nexus shifter)                |
|        9 |         0 | CAPTURE-DR -> SHIFT-DR                                                                       |
|       10 |         0 | (31) TCK clocks issued to transfer register value to TDO pin while shifting in TDI value     |
|       11 |         1 | SHIFT-DR -> EXIT1-DR (msb of value is shifted in/out of shifter)                             |
|       12 |         1 | EXIT1-DR -> UPDATE -DR (if access is write, shifter is transferred to register)              |
|       13 |         0 | UPDATE-DR -> RUN-TEST/IDLE (transfer complete - Nexus controller to reg. select state)       |

## 25.11.17.2 JTAG Sequence for Read Access of Memory-Mapped Resources

Table 25-43. Accessing Memory-Mapped Resources (Reads)

|   Step # | TCLK clocks   | Description                                                              |
|----------|---------------|--------------------------------------------------------------------------|
|        1 | 13            | Nexus Command = write to read/write access address register (RWA)        |
|        2 | 37            | Write RWA (initialize starting read address-data input on TDI)           |
|        3 | 13            | Nexus Command = write to read/write control/status register (RWCS)       |
|        4 | 37            | Write RWCS (initialize read access mode and CNT value-data input on TDI) |
|        5 | -             | Wait for falling edge of RDY pin                                         |
|        6 | 13            | Nexus Command = read read/write access data register (RWD)               |
|        7 | 37            | Read RWD (data output on TDO)                                            |
|        8 | -             | If CNT > 0, go back to Step #5                                           |

## 25.11.17.3JTAG Sequence for Write Access of Memory-Mapped Resources

## Table 25-44. Accessing Memory-Mapped Resources (Writes)

|   Step # | TCLK clocks   | Description                                                               |
|----------|---------------|---------------------------------------------------------------------------|
|        1 | 13            | Nexus Command = write to read/write access control/status register (RWCS) |
|        2 | 37            | Write RWCS (initialize write access mode and CNT value-data input on TDI) |
|        3 | 13            | Nexus Command = write to read/write address register (RWA)                |
|        4 | 37            | Write RWA (initialize starting write address-data input on TDI)           |
|        5 | 13            | Nexus Command = read read/write access data register (RWD)                |
|        6 | 37            | Write RWD (data output on TDO)                                            |
|        7 | -             | Wait for falling edge of RDY pin                                          |
|        8 | -             | If CNT > 0, go back to Step #5                                            |

## 25.12 Nexus Crossbar eDMA Interface (NXDM)

The third module of the MPC5553/MPC5554 NDI interface is the e200z6 eDMA Nexus module (NXDM) which is compliant with the Class 3 defined data trace feature of the IEEE ® -ISTO 5001-2003 standard. The NXDM can be programmed to trace data accesses for the eDMA module on the system bus. This eDMA module as well as the Nexus module are components of the e200z6 platform. All output messages and register accesses are compliant with the protocol defined in the IEEE ® -ISTO 5001 standard.

## NOTE

Throughout this section references are made to the auxiliary port and its specific signals, such as MCKO, MSEO[1:0], MDO[12:0] and others. In actual use the MPC5553/MPC5554 NPC module arbitrates the access of the single  auxiliary  port.  To  simplify  the  description  of  the  function  of  the NXDM module, the interaction of the NPC is omitted and the behavior described  as  if  the  module  has  its  own  dedicated  auxiliary  port.  The auxiliary port function is fully described in Section 25.2, 'External Signal Description.'

## 25.12.1 Block Diagram

Figure 25-52 shows a block diagram of the NXDM.

Figure 25-52. NXDM Block Diagram

<!-- image -->

## 25.12.2 Features

Feautures include the following:

- · Data trace via data write messaging (DWM) and data read messaging (DRM). This provides the capability for the development tool to trace reads and/or writes through the eDMA module to (selected) internal memory resources.
- · Watchpoint messaging via the auxiliary pins.
- · Watchpoint trigger enable of data trace messaging (DTM).
- · Registers for data trace, watchpoint generation, and watchpoint trigger.
- · All features controllable and configurable via the JTAG port.
- · Power management.
- - Low power design
- - Dynamic power management of FIFOs and control logic

## 25.13 External Signal Description

The NXDM module uses the same pins and pin protocol as defined in Section 25.2.

## 25.13.1 Rules for Output Messages

The NXDM module observes the same rules for output messages as the NPC. See  Section 25.7.2.2.1, 'Rules of Messages.'

## 25.13.2 Auxiliary Port Arbitration

The NXDM module arbitrates for the shared Nexus port. This arbitration is handled by the NPC (See Section 25.5) based on prioritized requests from the NXDM and the other Nexus clients sharing the port.

## 25.14 NXDM Programmers Model

This section describes the NXDM programmers model. Nexus registers are accessed using the JTAG port in compliance with IEEE ® 1149.1. See Chapter 24, 'IEEE 1149.1 Test Access Port Controller (JTAGC)' and Section 25.7.2.3 for details on Nexus register access.

## 25.14.1 NXDM Nexus Register Map

Table 25-45. NXDM Register Map

| Nexus Register                      | NexusAccess Opcode   | Read/Write   | Read Address   | Write Address   |
|-------------------------------------|----------------------|--------------|----------------|-----------------|
| Client Select Control (CSC) 1       | 0x1                  | R            | 0x02           | -               |
| Port Configuration Register (PCR) 1 | See NPC              | R/W          | -              | -               |
| Development Control 1 (DC1)         | 0x2                  | R/W          | 0x04           | 0x05            |
| Development Control 2 (DC2)         | 0x3                  | R/W          | 0x05           | 0x06            |
| Watchpoint Trigger (WT)             | 0xB                  | R/W          | 0x16           | 0x17            |
| Data Trace Control (DTC)            | 0xD                  | R/W          | 0x1A           | 0x1B            |
| Data Trace Start Address 1 (DTSA1)  | 0xE                  | R/W          | 0x1C           | 0x1D            |
| Data Trace Start Address 2 (DTSA2)  | 0xF                  | R/W          | 0x1E           | 0x1F            |

Table 25-45. NXDM Register Map (continued)

| Nexus Register                                  | NexusAccess Opcode   | Read/Write   | Read Address   | Write Address   |
|-------------------------------------------------|----------------------|--------------|----------------|-----------------|
| Data Trace End Address 1 (DTEA1)                | 0x12                 | R/W          | 0x24           | 0x25            |
| Data Trace End Address 2 (DTEA2)                | 0x13                 | R/W          | 0x26           | 0x27            |
| Breakpoint/Watchpoint Control Register 1 (BWC1) | 0x16                 | R/W          | 0x2C           | 0x2D            |
| Breakpoint/Watchpoint Control Register 2 (BWC2) | 0x17                 | R/W          | 0x2E           | 0x2F            |
| Breakpoint/Watchpoint Address Register 1 (BWA1) | 0x1E                 | R/W          | 0x3C           | 0x3D            |
| Breakpoint/Watchpoint Address Register 2 (BWA2) | 0x1F                 | R/W          | 0x3E           | 0x3F            |
| Reserved                                        | 0x20-0x3F            | -            | 0x40-0x7E      | 0x41-0x7F       |

1 The CSC and PCR registers are shown in this table as part of the Nexus programmer's model. They are only present at the top level Nexus3 controller (NPC), not in the NXDM module. The device's CSC register is readable through Nexus3; the PCR is shown for reference only.

## 25.14.2 NXDM Registers

Detailed register definitions for the NXDM implementation are as follows:

## 25.14.2.1 Development Control Registers (DC1 and DC2)

The development control registers control the basic development features of the NXDM  module.

Figure 25-53. Development Control Register 1 (DC1)

<!-- image -->

|       | 31   | 30      | 29      | 28   | 27   | 26   | 25   | 24   | 23   | 22   | 21   | 20   | 19   | 18   | 17   | 16   |
|-------|------|---------|---------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| R     | OPC  | MCK_DIV | MCK_DIV | EOC  | EOC  | 0    | 0    | WEN  | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |
| W     |      |         |         |      |      |      |      |      |      |      |      |      |      |      |      |      |
| Reset | 0    | 0       | 0       | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |
|       | 15   | 14      | 13      | 12   | 11   | 10   | 9    | 8    | 7    | 6    | 5    | 4    | 3    | 2    | 1    | 0    |
| R     | 0    | 0       | 0       | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | EIC  |      | TM   |      |      |
| W     |      |         |         |      |      |      |      |      |      |      |      |      |      |      |      |      |
| Reset | 0    | 0       | 0       | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |

## Table 25-46. DC1 Field Description

| Bit   | Name      | Description                                                                                                                                                                                          |
|-------|-----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 31    | OPC 1     | Output port mode control 0 Reduced port mode configuration 1 Full port mode configuration                                                                                                            |
| 30-29 | MCK_DIV 1 | MCK_DIV - nexus message clock divide ratio 00 MCKO is 1x system bus clock freq. 01 MCKO is 1/2x system bus clock freq. 10 MCKO is 1/4x system bus clock freq. 11 MCKO is 1/8x system bus clock freq. |
| 28-27 | EOC       | EVTO control 00 EVTO upon occurrence of watchpoint (internal or external) 01 EVTO upon entry into system-level debug mode (ipg_debug) 1X Reserved                                                    |
| 26-25 | -         | Reserved, read as 0.                                                                                                                                                                                 |
| 24    | WEN       | Watchpoint trace enable 0 Watchpoint messaging disabled 1 Watchpoint messaging enabled.                                                                                                              |
| 23-5  | -         | Reserved, read as 0.                                                                                                                                                                                 |
| 4-3   | EIC       | EVTI control 00 EVTI for synchronization (Data Trace) 01 Reserved 10 EVTI disabled for this module 11 Reserved                                                                                       |
| 2-0   | TM        | Trace mode 000 No Trace 1XX Reserved X1X Data trace enabled XX1 Reserved                                                                                                                             |

- 1 The output port mode control bit (OPC) and MCKO divide bits (MCK\_DIV) are shown for clarity. These functions are controlled globally by the NPC port control register (PCR).

Figure 25-54. Development Control Register 2 (DC2)

<!-- image -->

|       | 31   | 30   | 29   | 28   | 27   | 26   | 25   | 24   | 23   | 22   | 21   | 20   | 19   | 18   | 17   | 16   |
|-------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| R     |      |      |      | EWC  |      |      |      |      | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |
| W     |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |
| Reset | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |
|       | 15   | 14   | 13   | 12   | 11   | 10   | 9    | 8    | 7    | 6    | 5    | 4    | 3    | 2    | 1    | 0    |
| R     | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |
| W     |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |
| Reset | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |

Table 25-47. DC2 Field Description

| Bit   | Name   | Description                                                                                                                                                                                                                                                                                  |
|-------|--------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 31-24 | EWC 1  | EVTO Watchpoint Configuration 00000000 = No watchpoints trigger EVTO 1XXXXXXX = Reserved X1XXXXXX = Reserved XX1XXXXX = Reserved XXX1XXXX = Reserved XXXX1XXX = Internal watchpoint #1 triggers EVTO XXXXX1XX = Internal watchpoint #2 triggers EVTO XXXXXX1X = Reserved XXXXXXX1 = Reserved |
| 23-0  | -      | Reserved, read as 0.                                                                                                                                                                                                                                                                         |

1 The EOC bits in DC1 must be programmed to trigger EVTO on watchpoint occurence for the EWC bits to have any effect.

## 25.14.2.2 Watchpoint Trigger Register (WT)

The watchpoint trigger register allows the watchpoints defined internally to the NXDM module to trigger actions. These watchpoints can control data trace enable and disable. The WT bits can be used to produce an address related window for triggering trace messages.

Figure 25-55. Watchpoint Trigger Register (WT)

<!-- image -->

|       | 31   | 30   | 29   | 28   | 27   | 26   | 25   | 24   | 23   | 22   | 21   | 20   | 19   | 18   | 17   | 16   |
|-------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| R     | 0    | 0    | 0    | 0    | 0    | 0    |      | DTS  |      | DTE  | DTE  | DTE  | 0    | 0    | 0    | 0    |
| W     |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |
| Reset | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |
|       | 15   | 14   | 13   | 12   | 11   | 10   | 9    | 8    | 7    | 6    | 5    | 4    | 3    | 2    | 1    | 0    |
| R     | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |
| W     |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |
| Reset | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |

Table 25-48. WT Field Description

| Bit   | Name   | Description                                                                                                                                                                     |
|-------|--------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 31-26 | -      | Reserved, read as 0.                                                                                                                                                            |
| 25-23 | DTS    | DTS - Data trace start control 000 Trigger disabled 001-100 Reserved 101 Use internal watchpoint #1 (BWA1 register) 110 Use internal watchpoint #2 (BWA2 register) 111 Reserved |

Table 25-48. WT Field Description  (continued)

| Bit   | Name   | Description                                                                                                                                                                   |
|-------|--------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 22-20 | DTE    | DTE - Data trace end control 000 Trigger disabled 001-100 Reserved 101 Use internal watchpoint #1 (BWA1 register) 110 Use internal watchpoint #2 (BWA2 register) 111 Reserved |
| 19-0  | -      | Reserved, read as 0.                                                                                                                                                          |

## NOTE

The  WT  bits  will  ONLY  enable  data  trace  if  the  tm  bits  within  the development control register (DC) have not already been set to enable data trace.

## 25.14.2.3 Data Trace Control Register (DTC)

The data trace control register controls whether DTM Messages are restricted to reads, writes or both for a user programmable address range. There are two data trace channels controlled by the DTC for the NXDM module.

Figure 25-56. Data Trace Control Register (DTC)

<!-- image -->

|       | 31   | 30   | 29   | 28   | 27   | 26   | 25   | 24   | 23   | 22   | 21   | 20   | 19   | 18   | 17   | 16   |
|-------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| R     | RWT1 | RWT1 | RWT2 | RWT2 |      |      |      |      | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |
| W     |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |
| Reset | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |
|       | 15   | 14   | 13   | 12   | 11   | 10   | 9    | 8    | 7    | 6    | 5    | 4    | 3    | 2    | 1    | 0    |
| R     | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | RC1  | RC2  | 0    | 0    | 0    | 0    | 0    | 0    |
| W     |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |
| Reset | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |

Table 25-49. DTC Field Description

| Bit   | Name   | Description                                                                                            |
|-------|--------|--------------------------------------------------------------------------------------------------------|
| 31-30 | RWT1   | Read/write trace 1 00 No trace messages generated X1 Enable data read trace 1X Enable data write trace |
| 29-28 | RWT2   | Read/write trace 2 00 No trace messages generated X1 Enable data read trace 1X Enable data write trace |
| 27-8  | -      | Reserved, read as 0.                                                                                   |

## Table 25-49. DTC Field Description  (continued)

| Bit   | Name   | Description                                                                                                                                         |
|-------|--------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| 7     | RC1    | Range control 1 0 Condition trace on address within range (endpoints inclusive) 1 Condition trace on address outside of range (endpoints exclusive) |
| 6     | RC2    | Range control 2 0 Condition trace on address within range (endpoints inclusive) 1 Condition trace on address outside of range (endpoints exclusive) |
| 5-0   | -      | Reserved, read as 0.                                                                                                                                |

## 25.14.2.4 Data Trace Start Address Registers 1 and 2 (DTSA1 and DTSA2)

The data trace start address registers define the start addresses for each trace channel.

Figure 25-57. Data Trace Start Address Registers (DTSA1, DTSA2)

<!-- image -->

## 25.14.2.5 Data Trace End Address Registers 1 and 2 (DTEA1 and DTEA2)

The data trace end address registers define the end addresses for each trace channel.

Figure 25-58. Data Trace Start Address Registers (DTEA1, DTEA2)

<!-- image -->

Table 25-50 below illustrates the range that will be selected for data trace for various cases of DTSA being less than, greater than, or equal to DTEA.

Table 25-50. Data Trace - Address Range Options

| Programmed Values   | Range Control Bit Value   | Range Selected          |
|---------------------|---------------------------|-------------------------|
| DTSA < or = DTEA    | 0                         | DTSA-> <-DTEA           |
| DTSA < or = DTEA    | 1                         | <- DTSA DTEA ->         |
| DTSA > DTEA         | N/A                       | Invalid range, no trace |

## NOTE

DTSA must be less than (or equal to) DTEA in order to guarantee correct data  write/read  traces.  When  the  range  control  bit  is  0  (internal  range), accesses  to  DTSA  and  DTEA addresses  will  be  traced.  When  the  range control bit is 1 (external range), accesses to DTSA and DTEA will not be traced.

## 25.14.2.6 Breakpoint / Watchpoint Control Register 1 (BWC1)

Breakpoint/watchpoint control register 1 controls attributes for generation of NXDM Watchpoint#1.

Figure 25-59. Break / Watchpoint Control Register 1 (BWC1)

<!-- image -->

|       | 31   | 30   | 29   | 28   | 27   | 26   | 25   | 24   | 23   | 22   | 21   | 20   | 19   | 18   | 17   | 16   |
|-------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| R     | BWE1 | BWE1 | BRW1 | BRW1 | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | BWR1 | BWR1 |
| W     |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |
| Reset | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |
|       | 15   | 14   | 13   | 12   | 11   | 10   | 9    | 8    | 7    | 6    | 5    | 4    | 3    | 2    | 1    | 0    |
| R     | BWT1 | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |
| W     |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |
| Reset | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |

Table 25-51. BWC1 Field Description

| Bit   | Name   | Description                                                                                                                                                                    |
|-------|--------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 31-30 | BWE1   | Breakpoint/watchpoint #1 enable 00 Internal Nexus watchpoint #1 disabled 01-10 Reserved 11 Internal Nexus watchpoint #1 enabled                                                |
| 29-28 | BRW1   | Breakpoint/watchpoint #1 read/write select 00 Watchpoint #1 hit on read accesses 01 Watchpoint #1 hit on write accesses 10 Watchpoint #1 on read or write accesses 11 Reserved |
| 27-18 | -      | Reserved, read as 0.                                                                                                                                                           |

Table 25-51. BWC1 Field Description  (continued)

| Bit   | Name   | Description                                                                                                                                       |
|-------|--------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| 17-16 | BWR1   | Breakpoint/watchpoint #1 register compare 00 No register compare (same as BWC1[31:30] = 2'b00) 01 Reserved 10 Compare with BWA1 value 11 Reserved |
| 15    | BWT1   | Breakpoint/watchpoint #1 type 0 Reserved 1 Watchpoint #1 on data accesses                                                                         |
| 14-0  | -      | Reserved, read as 0.                                                                                                                              |

## 25.14.2.7 Breakpoint / Watchpoint Control Register 2 (BWC2)

Breakpoint/watchpoint control register2 controls attributes for generation of nxdm watchpoint #2.

Figure 25-60. Break / Watchpoint Control Register 2 (BWC2)

<!-- image -->

|       | 31   | 30   | 29   | 28   | 27   | 26   | 25   | 24   | 23   | 22   | 21   | 20   | 19   | 18   | 17   | 16   |
|-------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| R     | BWE2 | BWE2 | BRW2 | BRW2 | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | BWR2 | BWR2 |
| W     |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |
| Reset | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |
|       | 15   | 14   | 13   | 12   | 11   | 10   | 9    | 8    | 7    | 6    | 5    | 4    | 3    | 2    | 1    | 0    |
| R     | BWT2 | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |
| W     |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |
| Reset | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |

Table 25-52. BWC2 Field Description

| Bit   | Name   | Description                                                                                                                                                                    |
|-------|--------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 31-30 | BWE2   | Breakpoint/watchpoint #2 enable 00Internal Nexus watchpoint #2 disabled 01-10 Reserved 11 Internal Nexus watchpoint #2 enabled                                                 |
| 29-28 | BRW2   | Breakpoint/watchpoint #2 read/write select 00 Watchpoint #2 hit on read accesses 01 Watchpoint #2 hit on write accesses 10 Watchpoint #2 on read or write accesses 11 Reserved |
| 27-18 | -      | Reserved, read as 0.                                                                                                                                                           |
| 17-16 | BWR2   | Breakpoint/watchpoint #2 register compare 00 No register compare (same as BWC1[31:30] = 2'b00) 01 Reserved 10 Compare with BWA2 value 11 Reserved                              |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 25-52. BWC2 Field Description  (continued)

| Bit   | Name   | Description                                                               |
|-------|--------|---------------------------------------------------------------------------|
| 15    | BWT2   | Breakpoint/watchpoint #2 Type 0 Reserved 1 Watchpoint #2 on data accesses |
| 14-0  | -      | Reserved, read as 0.                                                      |

## 25.14.2.8 Breakpoint/Watchpoint Address Registers 1 and 2 (BWA1 and  BWA2)

The breakpoint/watchpoint address registers are compared with bus addresses in order to generate internal watchpoints.

Figure 25-61. Breakpoint / Watchpoint Address Registers (BWA1, BWA2)

<!-- image -->

## 25.14.2.9 Unimplemented Registers

Unimplemented registers are those with client select and index value combinations other than those listed in  Table 25-45.  For  unimplemented  registers,  the  NXDM  module  will  drive  TDO  to  zero  during  the 'SHIFT-DR' state. It will also transmit an error message with the invalid access opcode encoding.

## 25.14.2.10 Programming Considerations (RESET)

If Nexus3 register configuration is to occur during system reset (as opposed to debug mode), all NXDM configuration should be completed between the negation of JCOMP and system reset de-assertion, after the JTAG ID Register has been read by the tool.

## 25.14.2.11 IEEE ® 1149.1 (JTAG) Test Access Port

The NXDM module uses the IEEE ® 1149.1 TAP controller for accessing Nexus resources. The JTAG signals themselves are shared by all TAP controllers on the device. Refer to Chapter 24, 'IEEE 1149.1 Test Access Port Controller (JTAGC)  for more information on the JTAG interface.

The NXDM module implements a 4-bit instruction register (IR). The valid instructions and method for register access are outlined in Section 25.7.2.3 .

## 25.14.2.11.1 NXDM JTAG ID Register

This JTAG ID register that is included in the NXDM module provides key development attributes to the development tool concerning the NXDM block. The register is accessed through the standard JTAG IR/DR paths. See Chapter 23, 'Voltage Regulator Controller (VRC) and POR Module.'

Figure 25-62. NXDM JTAG ID Register

<!-- image -->

|       | 31   | 30   | 29   | 28   | 27   | 26   | 25   | 24   | 23   | 22   | 21   | 20   | 19   | 18   | 17   | 16   |
|-------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| R     | PRN  | PRN  | PRN  | DC   | DC   | DC   | DC   | DC   | DC   | DC   | PIN  | PIN  | PIN  | PIN  | PIN  | PIN  |
| W     |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |
| Reset | 0    | 0    | 0    | 0    | 0    | 1    | 1    | 1    | 1    | 1    | 0    | 0    | 0    | 1    | 1    | 0    |
|       | 15   | 14   | 13   | 12   | 11   | 10   | 9    | 8    | 7    | 6    | 5    | 4    | 3    | 2    | 1    | 0    |
| R     | PIN  | PIN  | PIN  | PIN  | MIC  | MIC  | MIC  | MIC  | MIC  | MIC  | MIC  | MIC  | MIC  | MIC  | MIC  | 1    |
| W     |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |
| Reset | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 1    | 1    | 1    | 0    | 1    |

Table 25-53. NXDM JTAG ID Field Descriptions

| Bit   | Name   | Description                                                             |
|-------|--------|-------------------------------------------------------------------------|
| 31-28 | PRN 1  | Embedded part revision number (0x0)                                     |
| 27-22 | DC     | Freescale design center ID number (0x1F)                                |
| 21-12 | PIN    | NXDMmodule part identification number, defines the features set. (0x60) |
| 11-1  | MIC    | Manufacturer identity code 0x00E Freescale                              |
| 0     | -      | Fixed per JTAG 1149.1 1 Always set                                      |

1 The revision number is initially 0 and could change in the future.

## 25.14.2.11.2 Enabling the NXDM TAP Controller

Assertion of a power-on-reset signal or assertion of the JCOMP pin resets all TAP controllers on the MPC5553/MPC5554 device. Upon exit from the test-logic-reset state, the IR value is loaded with the JTAG ID. When the NXDM TAP is accessed, this information will help the development tool obtain information about the Nexus module it is accessing, such as version, sequence, feature set, etc.

## 25.14.2.11.3 NXDM Register Access via JTAG

Access to Nexus register resources is enabled by loading a single instruction (NEXUS\_ACCESS) into the JTAG Instruction Register (IR). This IR is part of the IEEE ® 1149.1 TAP controller within the NXDM module. See Section 24.4.4, 'JTAGC Instructions.'

Once  the  JTAG  NEXUS\_ACCESS  instruction  has  been  loaded,  the  JTAG  port  allows  tool/target communications with all Nexus registers according to the map in Table 25-45.

Reading/writing of a Nexus register then requires two (2) passes through the data-scan (DR) path of the JTAG state machine (see Chapter 24, 'IEEE 1149.1 Test Access Port Controller (JTAGC)').

- 1. The first pass through the DR selects the Nexus register to be accessed by providing an index (see Table 25-45), and the direction (read/write). This is achieved by loading an 8-bit value into the JTAG data register (DR). This register has the following format:
- 2. The second pass through the DR then shifts the data in or out of the JTAG port, lsb first.
- a) During a read access, data is latched from the selected Nexus register when the JTAG state machine passes through the capture-DR state.
- b) During a write access, data is latched into the selected Nexus register when the JTAG state machine passes through the update-DR state.

Figure 25-63. JTAG DR for NEXUS Register Access

<!-- image -->

Table 25-54. DR Read/Write Encoding

| Nexus Register Index   | Selected from Values in Table 3-1   |
|------------------------|-------------------------------------|
| Read/Write (R/W)       | 0 Read 1 Write                      |

## 25.14.3 Functional Description

## 25.14.4 Enabling NXDM Operation

The NXDM module is enabled by loading a single instruction (ACCESS\_AUX\_TAP\_DMAN3, as shown in Table 25-4) into the JTAG instruction register (IR), and then loading the corresponding OnCE OCMD register with the NEXUS\_ACCESS instruction (refer to Table 25-5). Once enabled, the module will be ready to accept control input via the JTAG pins.

The Nexus module is disabled when the  JTAG state machine reaches the test-logic-reset state. This state can be reached by the  assertion of the JCOMP pin or by cycling through the state machine using the TMS pin. The  Nexus module will also be disabled if a power-on reset (POR) event occurs.

If the NXDM  module is disabled, no trace output will be provided, and the module will disable (drive inactive)  auxiliary  port  output  pins  (MDO[11:0],  MSEO[1:0],  MCKO).  Nexus  registers  will      not  be available for reads or writes.

## 25.14.5 TCODEs Supported by NXDM

The NXDM pins allow for flexible transfer operations via public messages. A TCODE  defines the transfer format, the number and/or size of the packets to be transferred, and the  purpose of each packet. The IEEE ® -ISTO 5001-2003 standard defines a set of public  messages. The NXDM block currently supports the public TCODEs seen in Table 25-55.

## Table 25-55. Public TCODEs Supported

| Message Name                            | Packet Size (bits)   | Packet Size (bits)   | Packet Name   | Packet Type   | Packet Description                                         |
|-----------------------------------------|----------------------|----------------------|---------------|---------------|------------------------------------------------------------|
| Message Name                            | Min                  | Max                  | Packet Name   | Packet Type   | Packet Description                                         |
| Data Trace - Date Write Message         | 6                    | 6                    | TCODE         | Fixed         | TCODE number = 5                                           |
| Data Trace - Date Write Message         | 4                    | 4                    | SRC           | Fixed         | source processor identifier                                |
| Data Trace - Date Write Message         | 3                    | 3                    | DSZ           | Fixed         | data size (refer to Table 25-57)                           |
| Data Trace - Date Write Message         | 1                    | 32                   | U-ADDR        | Variable      | unique portion of the data write value                     |
| Data Trace - Date Write Message         | 1                    | 64                   | DATA          | Variable      | data write value                                           |
| Data Trace - Data Read Message          | 6                    | 6                    | TCODE         | Fixed         | TCODE number = 6                                           |
| Data Trace - Data Read Message          | 4                    | 4                    | SRC           | Fixed         | source processor identifier                                |
| Data Trace - Data Read Message          | 3                    | 3                    | DSZ           | Fixed         | data size (refer to Table 25-57)                           |
| Data Trace - Data Read Message          | 1                    | 32                   | U-ADDR        | Variable      | unique portion of the data read value                      |
| Data Trace - Data Read Message          | 1                    | 64                   | DATA          | Variable      | data read value                                            |
| Error Message                           | 6                    | 6                    | TCODE         | Fixed         | TCODE number = 8                                           |
| Error Message                           | 4                    | 4                    | SRC           | Fixed         | source processor identifier (mulitple Nexus configuration) |
| Error Message                           | 5                    | 5                    | ECODE         | Fixed         | error code (refer to Table 25-56)                          |
| Data Trace - Data Write Message w/ Sync | 6                    | 6                    | TCODE         | Fixed         | TCODE number = 13 (0xD)                                    |
| Data Trace - Data Write Message w/ Sync | 4                    | 4                    | SRC           | Fixed         | source processor identifier (mulitple Nexus configuration) |
| Data Trace - Data Write Message w/ Sync | 3                    | 3                    | DSZ           | Fixed         | data size (refer to Table 25-57)                           |
| Data Trace - Data Write Message w/ Sync | 1                    | 32                   | F-ADDR        | Variable      | full access address (leading zero (0) truncated)           |
| Data Trace - Data Write Message w/ Sync | 1                    | 64                   | DATA          | Variable      | data write value                                           |
| Data Trace - Data Read Message w/ Sync  | 6                    | 6                    | TCODE         | Fixed         | TCODE number = 14 (0xE)                                    |
| Data Trace - Data Read Message w/ Sync  | 4                    | 4                    | SRC           | Fixed         | source processor identifier (mulitple Nexus configuration) |
| Data Trace - Data Read Message w/ Sync  | 3                    | 3                    | DSZ           | Fixed         | data size (refer to Table 25-57)                           |
| Data Trace - Data Read Message w/ Sync  | 1                    | 32                   | F-ADDR        | Variable      | full access address (leading zero (0) truncated)           |
| Data Trace - Data Read Message w/ Sync  | 1                    | 64                   | DATA          | Variable      | data read valued                                           |
| Watchpoint Message                      | 6                    | 6                    | TCODE         | Fixed         | TCODE number = 15 (0xF)                                    |
| Watchpoint Message                      | 4                    | 4                    | SRC           | Fixed         | source processor identifier (mulitple Nexus configuration) |
| Watchpoint Message                      | 4                    | 4                    | WPHIT         | Fixed         | # indicating watchpoint sources                            |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 25-56. Error Code (ECODE) Encoding (TCODE = 8)

| Error Code (ECODE)   | Description                                          |
|----------------------|------------------------------------------------------|
| 00000                | Reserved                                             |
| 00001                | Reserved                                             |
| 00010                | Data Trace overrun                                   |
| 00011                | Reserved                                             |
| 00100                | Reserved                                             |
| 00101                | Invalid access opcode (Nexus Register unimplemented) |
| 00110                | Watchpoint overrun                                   |
| 00111                | Reserved                                             |
| 01000                | Data Trace and Watchpoint overrun                    |
| 01001-11111          | Reserved                                             |

Table 25-57. Data Trace Size (DSZ) Encodings (TCODE = 5,6,13,14)

| DTM Size Encoding   | Transfer Size        |
|---------------------|----------------------|
| 000                 | Byte                 |
| 001                 | Halfword (2 bytes)   |
| 010                 | Word (4 bytes)       |
| 011                 | Doubleword (8 bytes) |
| 100-111             | Reserved             |

## 25.14.5.1 Data Trace

This  section  deals  with  the  data  trace  mechanism  supported  by  the  NXDM  module.  Data  trace  is implemented via data write messaging (DWM) and data read messaging (DRM).

## 25.14.5.2  Data Trace Messaging (DTM)

NXDM  data  trace  messaging  is  accomplished  by  snooping  the  NXDM  data  bus,  and  storing  the information  for  qualifying  accesses  (based  on  enabled  features  and  matching  target  addresses).  The NXDM module traces all data access that meet the selected range and attributes.

## NOTE

Data trace is ONLY performed on DMA accesses to the system bus.

## 25.14.5.3 DTM Message Formats

The  NXDM  block  supports  five  types  of  DTM  Messages  -  data  write,  data  read,  data  write synchronization, data read synchronization and error messages.

## 25.14.5.3.1 Data Write and Data Read Messages

The data write and data read messages contain the data write/read value and the address of the write/read access, relative to the previous data trace message. Data write message and data read message information is messaged out in the following format:

<!-- image -->

Max length = 109 bits; Min length = 15 bits

Figure 25-64. Data Write/Read Message Format

## 25.14.5.3.2 DTM Overflow Error Messages

An error message occurs when a new message cannot be queued due to the message queue being full. The FIFO will discard incoming messages until it has completely emptied the queue. Once emptied, an error message will be queued. The error encoding will indicate which types of messages attempted to be queued while the FIFO was being emptied.

If only a data trace message attempts to enter the queue while it is being emptied, the error message will incorporate the data trace only error encoding (00010). If a watchpoint also attempts to be queued while the fifo is being emptied, then the error message will incorporate error encoding (01000).

Error information is messaged out in the following format:

Figure 25-65. Error Message Format

<!-- image -->

## 25.14.5.3.3 Data Trace Synchronization Messages

A data trace write/read w/ sync. Message is messaged via the auxiliary port (provided data trace is enabled) for the following conditions (see Table 25-58):

- · Initial data trace message upon exit from system reset or whenever data trace is enabled will be a synchronization message.
- · Upon returning from a low power state, the first data trace message will be a synchronization message.
- · Upon returning from debug mode, the first data trace message will be a synchronization message.
- · After occurrence of queue overrun (can be caused by any trace message), the first data trace message will be a synchronization message.
- · After the periodic data trace counter has expired indicating 255 without-sync data trace messages have occurred since the last with-sync message occurred.
- · Upon assertion of the Event In (EVTI) pin, the first data trace message will be a synchronization message if the eic bits of the dc register have enabled this feature.

- · Upon data trace write/read after the previous dtm message was lost due to an attempted access to a secure memory location.
- · Upon data trace write/read after the previous dtm message was lost due to a collision entering the fifo between the dtm message and any of the following: error message, or watchpoint message.

Data Trace synchronization messages provide the full address (without leading zeros) and insure that development  tools  fully  synchronize  with  data  trace  regularly.  Synchronization  messages  provide  a reference address for subsequent DTMs, in which only the unique portion of the data trace address is transmitted. The format for data trace write/read w/ sync. Messages is as follows:

<!-- image -->

Max length = 109 bits; Min length = 15 bits

Figure 25-66. Data Write/Read w/ Sync Message Format

Exception conditions that result in data trace synchronization are summarized in Table 25-58., 'Data Trace Exception Summary.'

Table 25-58. Data Trace Exception Summary

| Exception Condition                 | Exception Handling                                                                                                                                                                                                                                                                                                                                                                                                        |
|-------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| System Reset Negation               | At the negation of JTAG reset (JCOMP), queue pointers, counters, state machines, and registers within the NXDM module are reset. If data trace is enabled, the first data trace message is a data write/read w/ sync. message.                                                                                                                                                                                            |
| Data Trace Enabled                  | The first data trace message (after data trace has been enabled) is a synchronization message.                                                                                                                                                                                                                                                                                                                            |
| Exit from Low Power/Debug           | Upon exit from a low power mode or debug mode the next data trace message will be converted to a data write/read w/ sync. message.                                                                                                                                                                                                                                                                                        |
| Queue Overrun                       | An error message occurs when a new message cannot be queued due to the message queue being full. The FIFO will discard messages until it has completely emptied the queue. Once emptied, an error message will be queued. The error encoding will indicate which types of messages attempted to be queued while the FIFO was being emptied. The next DTM message in the queue will be a data write/read w/ sync. message. |
| Periodic Data Trace Synchronization | A forced synchronization occurs periodically after 255 data trace messages have been queued. A data write/read w/ sync. message is queued. The periodic data trace message counter then resets.                                                                                                                                                                                                                           |
| Event In                            | if the nexus module is enabled, an evti assertion initiates a data trace write/read w/ sync. message upon the next data write/read (if data trace is enabled and the eic bits of the dc register have enabled this feature).                                                                                                                                                                                              |
| Attempted Access to Secure Memory   | Any attempted read or write to secure memory locations will temporarily disable data trace & cause the corresponding DTMto be lost. A subsequent read/write will queue a data trace read/write w/ sync. message.                                                                                                                                                                                                          |
| Collision Priority                  | All messages have the following priority: Error -> WPM -> DTM. A DTM message which attempts to enter the queue at the same time as an error message, or watchpoint message will be lost. A subsequent read/write will queue a data trace read/write w/ sync. message.                                                                                                                                                     |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## 25.14.5.4 DTM Operation

## 25.14.5.4.1 Enabling Data Trace Messaging

Data trace messaging can be enabled in one of two ways.

- · Setting the DC1[TM] field to enable data trace
- · Using the WT[DTS] field to enable data trace on watchpoint hits

## 25.14.5.4.2 DTM Queueing

NXDM implements a programmable depth queue for queuing all messages. Messages that enter the queue are transmitted via the auxiliary pins in the order in which they are queued.

## NOTE

If multiple trace messages need to be queued at the same time, watchpoint messages will have the highest priority (WPM -&gt; DTM).

## 25.14.5.4.3 Relative Addressing

The relative address feature is compliant with IEEE ® -ISTO Nexus 5001-2003 and is designed to reduce the number of bits transmitted for addresses of data trace messages. Relative addressing is the same as described for the NZ6C3 in Section 25.11.12.3.2, ' Relative Addressing.'

## 25.14.5.4.4 Data Trace Windowing

Data write/read messages are enabled via the RWT1(2) field in the data trace control register (DTC) for each DTM channel. Data trace windowing is achieved via the address range defined by the DTEA and DTSA registers and by the RC1(2) field in the DTC. All eDMA initiated read/write accesses which fall inside or outside these address ranges, as programmed, are candidates to be traced.

## 25.14.5.4.5 System Bus Cycle Special Cases

Table 25-59. System Bus Cycle Special Cases

| Special Case                               | Action                         |
|--------------------------------------------|--------------------------------|
| System bus cycle aborted (DABORT asserted) | Cycle ignored                  |
| System bus cycle with data error           | Data Trace Message discarded   |
| System bus cycle completed without error   | Cycle captured and transmitted |
| System bus cycle is an instruction fetch   | Cycle ignored                  |

## 25.14.5.5 Data Trace Timing Diagrams (8 MDO configuration)

Data trace timing for the NXDM is the same as for the NZ6C3. See Section Section 25.11.13.4, ' Data Trace Timing Diagrams (8 MDO Configuration).'

## 25.14.6 Watchpoint Support

The NXDM module provides watchpoint messaging via the auxiliary pins, as defined by IEEE ® -ISTO 5001-2003.

Watchpoint messages can be generated using the NXDM defined internal watchpoints.

## 25.14.6.1 Watchpoint Messaging

Enabling  watchpoint  messaging  is  accomplished  by  setting  the  watchpoint  messaging  enable  bit, DC1[WEN]. Using the BWC1 and BWC2 registers, two independently controlled internal watchpoints can be initialized. When a DMA access address matches on BWA1 or BWA2, a watchpoint message will be transmitted.

The Nexus module provides watchpoint messaging using the TCODE. When either of the  two possible watchpoint sources asserts, a message will be sent to the queue to be messaged out. This message indicates the watchpoint number.

Figure 25-67. Watchpoint Message Format

<!-- image -->

Table 25-60. Watchpoint Source Description

| Watchpoint Source (4 bits)   | Watchpoint Description              |
|------------------------------|-------------------------------------|
| XXX1                         | Reserved                            |
| XX1X                         | Reserved                            |
| X1XX                         | Internal Watchpoint #1 (BWA1 match) |
| 1XXX                         | Internal Watchpoint #2 (BWA2 match) |

## 25.14.6.2 Watchpoint Error Message

An error message occurs when a new message cannot be queued due to the message queue being full. The FIFO will discard messages until it has completely emptied the queue. Once emptied, an error message will be queued. The error encoding will indicate which types of messages attempted to be queued while the FIFO was being emptied.

If only a watchpoint message attempts to enter the queue while it is being emptied, the error message will incorporate the watchpoint only error encoding (00110). If a data trace message also attempts to enter the queue while it is being emptied, the error message will incorporate error encoding (01000).

Error information is messaged out in the following format (see Figure 25-68).

<!-- image -->

## 25.15 Revision History

## Substantive Changes since Rev 3.0

Fixed title of Table 25-52 to be BWC2 rather than BWC1.

Table 25-18: fixed cross references to other sections, removed notes about Multiple Nesux Configurations since all parts do have multiple Nexus modules.

## Appendix A MPC5553/MPC5554 Register Map

Table A-1. Module Base Addresses

| Module                                              | Base Address                                                                          | Page      |
|-----------------------------------------------------|---------------------------------------------------------------------------------------|-----------|
| Peripheral Bridge A (PBRIDGEA)                      | 0xC3F0_0000                                                                           | Page A-2  |
| Frequency Modulated Phase-Locked Loop (FMPLL)       | 0xC3F8_0000                                                                           | Page A-2  |
| External Bus Interface (EBI)                        | 0xC3F8_4000                                                                           | Page A-2  |
| Flash Module and Flash Bus Interface Unit (FLASH)   | 0xC3F8_8000                                                                           | Page A-3  |
| System Integration Unit (SIU)                       | 0xC3F9_0000                                                                           | Page A-3  |
| Enhanced Modular Input/Output Subsystem (eMIOS)     | 0xC3FA_0000                                                                           | Page A-25 |
| Enhanced Time Processing Unit (eTPU)                | 0xC3FC_0000                                                                           | Page A-25 |
| Peripheral Bridge B (PBRIDGEB)                      | 0xFFF0_0000                                                                           | Page A-35 |
| System Bus Crossbar Switch (XBAR)                   | 0xFFF0_4000                                                                           | Page A-36 |
| Error Correction Status Module (ECSM)               | 0xFFF4_0000                                                                           | Page A-37 |
| Enhanced Direct Memory Access (eDMA)                | 0xFFF4_4000                                                                           | Page A-38 |
| Interrupt Controller (INTC)                         | 0xFFF4_8000                                                                           | Page A-42 |
| Fast Ethernet Controller (FEC) -in MPC5553 only     | 0xFFF4_C000                                                                           | Page A-53 |
| Enhanced Queued Analog-to-Digital Converter (eQADC) | 0xFFF8_0000                                                                           | Page A-54 |
| Deserial / Serial Peripheral Interface (DSPIx)      | 0xFFF9_0000 (DSPI A) 1 0xFFF9_4000 (DSPI B) 0xFFF9_8000 (DSPI C) 0xFFF9_C000 (DSPI D) | Page A-58 |
| Enhanced Serial Communication Interface (eSCIx)     | 0xFFFB_0000 (A) 0xFFFB_4000 (B)                                                       | Page A-59 |
| FlexCAN2 Controller Area Network (CANx)             | 0xFFFC_0000 (FlexCAN A) 0xFFFC_4000 (FlexCAN B) 1 0xFFFC_8000 (FlexCAN C)             | Page A-59 |
| Boot Assist Module (BAM)                            | 0xFFFF_C000                                                                           | Page A-60 |

1 MPC5554 Only

## Table A-2. MPC5554 / MPC5553 Detailed Register Map

| Register Description                                                  | Register Name                                 | Used Size   | Address                      | Reference                                                                      |
|-----------------------------------------------------------------------|-----------------------------------------------|-------------|------------------------------|--------------------------------------------------------------------------------|
| Peripheral Bridge A (PBRIDGEA)                                        | Peripheral Bridge A (PBRIDGEA)                |             | 0xC3F0_0000                  | Chapter 5, 'PeripheralBridge (PBRIDGE_A, PBRIDGE_B)'                           |
| Peripheral bridge A master privilege control register                 | PBRIDGEA_MPCR                                 | 32-bit      | Base + 0x0000                |                                                                                |
| Reserved                                                              | -                                             | -           | Base + (0x0004-0x001F)       |                                                                                |
| Peripheral bridge A peripheral access control register 0              | PBRIDGEA_PACR0                                | 32-bit      | Base + 0x0020                |                                                                                |
| Reserved                                                              | -                                             | -           | Base + (0x0024-0x003F)       |                                                                                |
| Peripheral bridge A off-platform peripheral access control register 0 | PBRIDGEA_OPACR0                               | 32-bit      | Base + 0x0040                |                                                                                |
| Peripheral bridge A off-platform peripheral access control register 1 | PBRIDGEA_OPACR1                               | 32-bit      | Base + 0x0044                |                                                                                |
| Peripheral bridge A off-platform peripheral access control register 2 | PBRIDGEA_OPACR2                               | 32-bit      | Base + 0x0048                |                                                                                |
| Reserved                                                              | -                                             | -           | Base + (0x004C- 0xC3F7_FFFF) |                                                                                |
| Frequency Modulated Phase-Locked Loop (FMPLL)                         | Frequency Modulated Phase-Locked Loop (FMPLL) |             | 0xC3F8_0000                  | Chapter 11, 'Frequency Modulated Phase Locked Loop (FMPLL) and System Clocks ' |
| Synthesizer control register                                          | FMPLL_SYNCR                                   | 32-bit      | Base + 0x0000                |                                                                                |
| Synthesizer status register                                           | FMPLL_SYNSR                                   | 32-bit      | Base + 0x0004                |                                                                                |
| Reserved                                                              | -                                             | -           | (Base + 0x0008)- 0xC3F8_3FFF |                                                                                |
| External Bus Interface (EBI)                                          | External Bus Interface (EBI)                  |             | 0xC3F8_4000                  | Chapter 12, 'External Bus Interface (EBI)'                                     |
| Module configuration register                                         | EBI_MCR                                       | 32-bit      | Base + 0x0000                |                                                                                |
| Reserved                                                              | -                                             | -           | Base + (0x0004-0x0007)       |                                                                                |
| Transfer error status register                                        | EBI_TESR                                      | 32-bit      | Base + 0x0008                |                                                                                |
| Bus monitor control register                                          | EBI_BMCR                                      | 32-bit      | Base + 0x000C                |                                                                                |
| Base register bank 0                                                  | EBI_BR0                                       | 32-bit      | Base + 0x0010                |                                                                                |
| Option register bank 0                                                | EBI_OR0                                       | 32-bit      | Base + 0x0014                |                                                                                |
| Base register bank 1                                                  | EBI_BR1                                       | 32-bit      | Base + 0x0018                |                                                                                |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description                                   | Register Name                                     | Used Size   | Address                       | Reference                                  |
|--------------------------------------------------------|---------------------------------------------------|-------------|-------------------------------|--------------------------------------------|
| Option register bank 1                                 | EBI_OR1                                           | 32-bit      | Base + 0x001C                 |                                            |
| Base register bank 2                                   | EBI_BR2                                           | 32-bit      | Base + 0x0020                 |                                            |
| Option register bank 2                                 | EBI_OR2                                           | 32-bit      | Base + 0x0024                 |                                            |
| Base register bank 3                                   | EBI_BR3                                           | 32-bit      | Base + 0x0028                 |                                            |
| Option register bank 3                                 | EBI_OR3                                           | 32-bit      | Base + 0x002C                 |                                            |
| EBI Calibration Base Register Bank 0                   | EBI_CAL_BR0                                       | 32-bit      | Base + 0x0040                 |                                            |
| EBI Calibration Option Register Bank 0                 | EBI_CAL_OR0                                       | 32-bit      | Base + 0x0044                 |                                            |
| EBI Calibration Base Register Bank 1                   | EBI_CAL_BR1                                       | 32-bit      | Base + 0x0048                 |                                            |
| EBI Calibration Option Register Bank 1                 | EBI_CAL_OR1                                       | 32-bit      | Base + 0x004C                 |                                            |
| EBI Calibration Base Register Bank 2                   | EBI_CAL_BR2                                       | 32-bit      | Base + 0x0050                 |                                            |
| EBI Calibration Option Register Bank 2                 | EBI_CAL_OR2                                       | 32-bit      | Base + 0x0054                 |                                            |
| EBI Calibration Base Register Bank 3                   | EBI_CAL_BR3                                       | 32-bit      | Base + 0x0058                 |                                            |
| EBI Calibration Option Register Bank 3                 | EBI_CAL_OR3                                       | 32-bit      | Base + 0x005C                 |                                            |
| Flash Module and Flash Bus Interface Unit (FLASH)      | Flash Module and Flash Bus Interface Unit (FLASH) |             | 0xC3F8_8000                   | Chapter 13, 'Flash Memory'                 |
| Module configuration register                          | FLASH_MCR                                         | 32-bit      | Base + 0x0000                 |                                            |
| Low/mid address space block locking register           | FLASH_LMLR                                        | 32-bit      | Base + 0x0004                 |                                            |
| High address space block locking register              | FLASH_HLR                                         | 32-bit      | Base + 0x0008                 |                                            |
| Secondary low/mid address space block locking register | FLASH_SLMLR                                       | 32-bit      | Base + 0x000C                 |                                            |
| Low/mid address block select register                  | FLASH_LMSR                                        | 32-bit      | Base + 0x0010                 |                                            |
| High address space block select register               | FLASH_HSR                                         | 32-bit      | Base + 0x0014                 |                                            |
| Address register                                       | FLASH_AR                                          | 32-bit      | Base + 0x0018                 |                                            |
| Bus interface unit control register                    | FLASH_BIUCR                                       | 32-bit      | Base + 0x001C                 |                                            |
| Bus interface unit access protection register          | FLASH_BIUAPR                                      | 32-bit      | Base + 0x0020                 |                                            |
| Reserved                                               | -                                                 | -           | (Base + 0x0024)- 0xC3F8_FFFF) |                                            |
| System Integration Unit (SIU)                          | System Integration Unit (SIU)                     |             | 0xC3F9_0000                   | Chapter 6, 'System Integration Unit (SIU)' |
| MCU ID Register                                        | SIU_MIDR                                          |             | Base + 0x0004                 |                                            |
| Reserved                                               | -                                                 | -           | Base + (0x0008-0x000B)        |                                            |
| Reset status register SIU_RSR                          | Reset status register SIU_RSR                     |             | Base + 0x000C                 |                                            |

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description                   | Register Name   | Used Size   | Address                | Reference   |
|----------------------------------------|-----------------|-------------|------------------------|-------------|
| System reset control register          | SIU_SRCR        |             | Base + 0x0010          |             |
| External interrupt status register     | SIU_EISR        |             | Base + 0x0014          |             |
| DMA/Interrupt request enable register  | SIU_DIRER       |             | Base + 0x0018          |             |
| DMA/Interrupt request status register  | SIU_DIRSR       |             | Base + 0x001C          |             |
| Overrun status register                | SIU_OSR         |             | Base + 0x0020          |             |
| Overrun request enable register        | SIU_ORER        |             | Base + 0x0024          |             |
| IRQ rising-edge event enable register  | SIU_IREER       |             | Base + 0x0028          |             |
| IRQ falling-edge event enable register | SIU_IFEER       |             | Base + 0x002C          |             |
| IRQ digital filter register            | SIU_IDFR        |             | Base + 0x0030          |             |
| Reserved                               | -               | -           | Base + (0x0034-0x003F) |             |
| Pad configuration register 0 (CS0)     | SIU_PCR0        | 16-bits     | Base + 0x0040          |             |
| Pad configuration register 1 (CS1)     | SIU_PCR1        | 16-bits     | Base + 0x0042          |             |
| Pad configuration register 2 (CS2)     | SIU_PCR2        | 16-bits     | Base + 0x0044          |             |
| Pad configuration register 3 (CS3)     | SIU_PCR3        | 16-bits     | Base + 0x0046          |             |
| Pad configuration register 4 (ADDR8)   | SIU_PCR4        | 16-bits     | Base + 0x0048          |             |
| Pad configuration register 5 (ADDR9)   | SIU_PCR5        | 16-bits     | Base + 0x004A          |             |
| Pad configuration register 6 (ADDR10)  | SIU_PCR6        | 16-bits     | Base + 0x004C          |             |
| Pad configuration register 7 (ADDR11)  | SIU_PCR7        | 16-bits     | Base + 0x004E          |             |
| Pad configuration register 8 (ADDR12)  | SIU_PCR8        | 16-bits     | Base + 0x0050          |             |
| Pad configuration register 9 (ADDR13)  | SIU_PCR9        | 16-bits     | Base + 0x0052          |             |
| Pad configuration register 10 (ADDR14) | SIU_PCR10       | 16-bits     | Base + 0x0054          |             |
| Pad configuration register 11 (ADDR15) | SIU_PCR11       | 16-bits     | Base + 0x0056          |             |
| Pad configuration register 12 (ADDR16) | SIU_PCR12       | 16-bits     | Base + 0x0058          |             |
| Pad configuration register 13 (ADDR17) | SIU_PCR13       | 16-bits     | Base + 0x005A          |             |
| Pad configuration register 14 (ADDR18) | SIU_PCR14       | 16-bits     | Base + 0x005C          |             |
| Pad configuration register 15 (ADDR19) | SIU_PCR15       | 16-bits     | Base + 0x005E          |             |
| Pad configuration register 16 (ADDR20) | SIU_PCR16       | 16-bits     | Base + 0x0060          |             |
| Pad configuration register 17 (ADDR21) | SIU_PCR17       | 16-bits     | Base + 0x0062          |             |
| Pad configuration register 18 (ADDR22) | SIU_PCR18       | 16-bits     | Base + 0x0064          |             |
| Pad configuration register 19 (ADDR23) | SIU_PCR19       | 16-bits     | Base + 0x0066          |             |
| Pad configuration register 20 (ADDR24) | SIU_PCR20       | 16-bits     | Base + 0x0068          |             |
| Pad configuration register 21 (ADDR25) | SIU_PCR21       | 16-bits     | Base + 0x006A          |             |

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description                   | Register Name   | Used Size   | Address       | Reference   |
|----------------------------------------|-----------------|-------------|---------------|-------------|
| Pad configuration register 22 (ADDR26) | SIU_PCR22       | 16-bits     | Base + 0x006C |             |
| Pad configuration register 23 (ADDR27) | SIU_PCR23       | 16-bits     | Base + 0x006E |             |
| Pad configuration register 24 (ADDR28) | SIU_PCR24       | 16-bits     | Base + 0x0070 |             |
| Pad configuration register 25 (ADDR29) | SIU_PCR25       | 16-bits     | Base + 0x0072 |             |
| Pad configuration register 26 (ADDR30) | SIU_PCR26       | 16-bits     | Base + 0x0074 |             |
| Pad configuration register 27 (ADDR31) | SIU_PCR27       | 16-bits     | Base + 0x0076 |             |
| Pad configuration register 28 (DATA0)  | SIU_PCR28       | 16-bits     | Base + 0x0078 |             |
| Pad configuration register 29 (DATA1)  | SIU_PCR29       | 16-bits     | Base + 0x007A |             |
| Pad configuration register 30 (DATA2)  | SIU_PCR30       | 16-bits     | Base + 0x007C |             |
| Pad configuration register 31 (DATA3)  | SIU_PCR31       | 16-bits     | Base + 0x007E |             |
| Pad configuration register 32 (DATA4)  | SIU_PCR32       | 16-bits     | Base + 0x0080 |             |
| Pad configuration register 33 (DATA5)  | SIU_PCR33       | 16-bits     | Base + 0x0082 |             |
| Pad configuration register 34 (DATA6)  | SIU_PCR34       | 16-bits     | Base + 0x0084 |             |
| Pad configuration register 35 (DATA7)  | SIU_PCR35       | 16-bits     | Base + 0x0086 |             |
| Pad configuration register 36 (DATA8)  | SIU_PCR36       | 16-bits     | Base + 0x0088 |             |
| Pad configuration register 37 (DATA9)  | SIU_PCR37       | 16-bits     | Base + 0x008A |             |
| Pad configuration register 38 (DATA10) | SIU_PCR38       | 16-bits     | Base + 0x008C |             |
| Pad configuration register 39 (DATA11) | SIU_PCR39       | 16-bits     | Base + 0x008E |             |
| Pad configuration register 40 (DATA12) | SIU_PCR40       | 16-bits     | Base + 0x0090 |             |
| Pad configuration register 41 (DATA13) | SIU_PCR41       | 16-bits     | Base + 0x0092 |             |
| Pad configuration register 42 (DATA14) | SIU_PCR42       | 16-bits     | Base + 0x0094 |             |
| Pad configuration register 43 (DATA15) | SIU_PCR43       | 16-bits     | Base + 0x0096 |             |
| Pad configuration register 44 (DATA16) | SIU_PCR44       | 16-bits     | Base + 0x0098 |             |
| Pad configuration register 45 (DATA17) | SIU_PCR45       | 16-bits     | Base + 0x009A |             |
| Pad configuration register 46 (DATA18) | SIU_PCR46       | 16-bits     | Base + 0x009C |             |
| Pad configuration register 47 (DATA19) | SIU_PCR47       | 16-bits     | Base + 0x009E |             |
| Pad configuration register 48 (DATA20) | SIU_PCR48       | 16-bits     | Base + 0x00A0 |             |
| Pad configuration register 49 (DATA21) | SIU_PCR49       | 16-bits     | Base + 0x00A2 |             |
| Pad configuration register 50 (DATA22) | SIU_PCR50       | 16-bits     | Base + 0x00A4 |             |
| Pad configuration register 51 (DATA23) | SIU_PCR51       | 16-bits     | Base + 0x00A6 |             |
| Pad configuration register 52 (DATA24) | SIU_PCR52       | 16-bits     | Base + 0x00A8 |             |
| Pad configuration register 53 (DATA25) | SIU_PCR53       | 16-bits     | Base + 0x00AA |             |

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description                   | Register Name   | Used Size   | Address       | Reference   |
|----------------------------------------|-----------------|-------------|---------------|-------------|
| Pad configuration register 54 (DATA26) | SIU_PCR54       | 16-bits     | Base + 0x00AC |             |
| Pad configuration register 55 (DATA27) | SIU_PCR55       | 16-bits     | Base + 0x00AE |             |
| Pad configuration register 56 (DATA28) | SIU_PCR56       | 16-bits     | Base + 0x00B0 |             |
| Pad configuration register 57 (DATA29) | SIU_PCR57       | 16-bits     | Base + 0x00B2 |             |
| Pad configuration register 58 (DATA30) | SIU_PCR58       | 16-bits     | Base + 0x00B4 |             |
| Pad configuration register 59 (DATA31) | SIU_PCR59       | 16-bits     | Base + 0x00B6 |             |
| Pad configuration register 60 (TSIZ0)  | SIU_PCR60       | 16-bits     | Base + 0x00B8 |             |
| Pad configuration register 61 (TSIZ1)  | SIU_PCR61       | 16-bits     | Base + 0x00BA |             |
| Pad configuration register 62 (RD_WR)  | SIU_PCR62       | 16-bits     | Base + 0x00BC |             |
| Pad configuration register 63 (BDIP)   | SIU_PCR63       | 16-bits     | Base + 0x00BE |             |
| Pad configuration register 64 (WE0)    | SIU_PCR64       | 16-bits     | Base + 0x00C0 |             |
| Pad configuration register 65 (WE1)    | SIU_PCR65       | 16-bits     | Base + 0x00C2 |             |
| Pad configuration register 66 (WE2)    | SIU_PCR66       | 16-bits     | Base + 0x00C4 |             |
| Pad configuration register 67 (WE3)    | SIU_PCR67       | 16-bits     | Base + 0x00C6 |             |
| Pad configuration register 68 (OE)     | SIU_PCR68       | 16-bits     | Base + 0x00C8 |             |
| Pad configuration register 69 (TS)     | SIU_PCR69       | 16-bits     | Base + 0x00CA |             |
| Pad configuration register 70 (TA)     | SIU_PCR70       | 16-bits     | Base + 0x00CC |             |
| Pad configuration register 71 (TEA)    | SIU_PCR71       | 16-bits     | Base + 0x00CE |             |
| Pad configuration register 72 (BR)     | SIU_PCR72       | 16-bits     | Base + 0x00D0 |             |
| Pad configuration register 73 (BG)     | SIU_PCR73       | 16-bits     | Base + 0x00D2 |             |
| Pad configuration register 74 (BB)     | SIU_PCR74       | 16-bits     | Base + 0x00D4 |             |
| Pad configuration register 75 (MDO4)   | SIU_PCR75       | 16-bits     | Base + 0x00D6 |             |
| Pad configuration register 76 (MDO5)   | SIU_PCR76       | 16-bits     | Base + 0x00D8 |             |
| Pad configuration register 77 (MDO6)   | SIU_PCR77       | 16-bits     | Base + 0x00DA |             |
| Pad configuration register 78 (MDO7)   | SIU_PCR78       | 16-bits     | Base + 0x00DC |             |
| Pad configuration register 79 (MDO8)   | SIU_PCR79       | 16-bits     | Base + 0x00DE |             |
| Pad configuration register 80 (MDO9)   | SIU_PCR80       | 16-bits     | Base + 0x00E0 |             |
| Pad configuration register 81 (MDO10)  | SIU_PCR81       | 16-bits     | Base + 0x00E2 |             |
| Pad configuration register 82 (MDO11)  | SIU_PCR82       | 16-bits     | Base + 0x00E4 |             |
| Pad configuration register 83 (CNTXA)  | SIU_PCR83       | 16-bits     | Base + 0x00E6 |             |
| Pad configuration register 84 (CNRXA)  | SIU_PCR84       | 16-bits     | Base + 0x00E8 |             |
| Pad configuration register 85 (CNTXB)  | SIU_PCR85       | 16-bits     | Base + 0x00EA |             |

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description                     | Register Name   | Used Size   | Address       | Reference   |
|------------------------------------------|-----------------|-------------|---------------|-------------|
| Pad configuration register 86 (CNRXB)    | SIU_PCR86       | 16-bits     | Base + 0x00EC |             |
| Pad configuration register 87 (CNTXC)    | SIU_PCR87       | 16-bits     | Base + 0x00EE |             |
| Pad configuration register 88 (CNRXC)    | SIU_PCR88       | 16-bits     | Base + 0x00F0 |             |
| Pad configuration register 89 (TXDA)     | SIU_PCR89       | 16-bits     | Base + 0x00F2 |             |
| Pad configuration register 90 (RXDA)     | SIU_PCR90       | 16-bits     | Base + 0x00F4 |             |
| Pad configuration register 91 (TXDB)     | SIU_PCR91       | 16-bits     | Base + 0x00F6 |             |
| Pad configuration register 92 (RXDB)     | SIU_PCR92       | 16-bits     | Base + 0x00F8 |             |
| Pad configuration register 93 (SCKA)     | SIU_PCR93       | 16-bits     | Base + 0x00FA |             |
| Pad configuration register 94 (SINA)     | SIU_PCR94       | 16-bits     | Base + 0x00FC |             |
| Pad configuration register 95 (SOUTA)    | SIU_PCR95       | 16-bits     | Base + 0x00FE |             |
| Pad configuration register 96 (PCSA0)    | SIU_PCR96       | 16-bits     | Base + 0x0100 |             |
| Pad configuration register 97 (PCSA1)    | SIU_PCR97       | 16-bits     | Base + 0x0102 |             |
| Pad configuration register 98 (PCSA2)    | SIU_PCR98       | 16-bits     | Base + 0x0104 |             |
| Pad configuration register 99 (PCSA3)    | SIU_PCR99       | 16-bits     | Base + 0x0106 |             |
| Pad configuration register 100 (PCSA4)   | SIU_PCR100      | 16-bits     | Base + 0x0108 |             |
| Pad configuration register 101 (PCSA6)   | SIU_PCR101      | 16-bits     | Base + 0x010A |             |
| Pad configuration register 102 (SCKB)    | SIU_PCR102      | 16-bits     | Base + 0x010C |             |
| Pad configuration register 103 (SINB)    | SIU_PCR103      | 16-bits     | Base + 0x010E |             |
| Pad configuration register 104 (SOUTB)   | SIU_PCR104      | 16-bits     | Base + 0x0110 |             |
| Pad configuration register 105 (PCSB0)   | SIU_PCR105      | 16-bits     | Base + 0x0112 |             |
| Pad configuration register 106 (PCSB1)   | SIU_PCR106      | 16-bits     | Base + 0x0114 |             |
| Pad configuration register 107 (PCSB2)   | SIU_PCR107      | 16-bits     | Base + 0x0116 |             |
| Pad configuration register 108 (PCSB3)   | SIU_PCR108      | 16-bits     | Base + 0x0118 |             |
| Pad configuration register 109 (PCSB4)   | SIU_PCR109      | 16-bits     | Base + 0x011A |             |
| Pad configuration register 110 (PCSB5)   | SIU_PCR110      | 16-bits     | Base + 0x011C |             |
| Pad configuration register 111 (ETRIG0)  | SIU_PCR9111     | 16-bits     | Base + 0x011E |             |
| Pad configuration register 112 (ETRIG1)  | SIU_PCR112      | 16-bits     | Base + 0x0120 |             |
| Pad configuration register 113 (TCRCLKA) | SIU_PCR113      | 16-bits     | Base + 0x0122 |             |
| Pad configuration register 114 (ETPUA0)  | SIU_PCR114      | 16-bits     | Base + 0x0124 |             |
| Pad configuration register 115 (ETPUA1)  | SIU_PCR115      | 16-bits     | Base + 0x0126 |             |
| Pad configuration register 116 (ETPUA2)  | SIU_PCR116      | 16-bits     | Base + 0x0128 |             |
| Pad configuration register 117 (ETPUA3)  | SIU_PCR117      | 16-bits     | Base + 0x012A |             |

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description                     | Register Name   | Used Size   | Address       | Reference   |
|------------------------------------------|-----------------|-------------|---------------|-------------|
| Pad configuration register 118 (ETPUA4)  | SIU_PCR118      | 16-bits     | Base + 0x012C |             |
| Pad configuration register 119 (ETPUA5)  | SIU_PCR119      | 16-bits     | Base + 0x012E |             |
| Pad configuration register 120 (ETPUA6)  | SIU_PCR120      | 16-bits     | Base + 0x0130 |             |
| Pad configuration register 121 (ETPUA7)  | SIU_PCR121      | 16-bits     | Base + 0x0132 |             |
| Pad configuration register 122 (ETPUA8)  | SIU_PCR122      | 16-bits     | Base + 0x0134 |             |
| Pad configuration register 123 (ETPUA9)  | SIU_PCR123      | 16-bits     | Base + 0x0136 |             |
| Pad configuration register 124 (ETPUA10) | SIU_PCR124      | 16-bits     | Base + 0x0138 |             |
| Pad configuration register 125 (ETPUA11) | SIU_PCR125      | 16-bits     | Base + 0x013A |             |
| Pad configuration register 126 (ETPUA12) | SIU_PCR126      | 16-bits     | Base + 0x013C |             |
| Pad configuration register 127 (ETPUA13) | SIU_PCR127      | 16-bits     | Base + 0x013E |             |
| Pad configuration register 128 (ETPUA14) | SIU_PCR128      | 16-bits     | Base + 0x0140 |             |
| Pad configuration register 129 (ETPUA15) | SIU_PCR129      | 16-bits     | Base + 0x0142 |             |
| Pad configuration register 130 (ETPUA16) | SIU_PCR130      | 16-bits     | Base + 0x0144 |             |
| Pad configuration register 131 (ETPUA17) | SIU_PCR131      | 16-bits     | Base + 0x0146 |             |
| Pad configuration register 132 (ETPUA18) | SIU_PCR132      | 16-bits     | Base + 0x0148 |             |
| Pad configuration register 133 (ETPUA19) | SIU_PCR133      | 16-bits     | Base + 0x014A |             |
| Pad configuration register 134 (ETPUA20) | SIU_PCR134      | 16-bits     | Base + 0x014C |             |
| Pad configuration register 135 (ETPUA21) | SIU_PCR135      | 16-bits     | Base + 0x014E |             |
| Pad configuration register 136 (ETPUA22) | SIU_PCR136      | 16-bits     | Base + 0x0150 |             |
| Pad configuration register 137 (ETPUA23) | SIU_PCR137      | 16-bits     | Base + 0x0152 |             |
| Pad configuration register 138 (ETPUA24) | SIU_PCR138      | 16-bits     | Base + 0x0154 |             |
| Pad configuration register 139 (ETPUA25) | SIU_PCR139      | 16-bits     | Base + 0x0156 |             |
| Pad configuration register 140 (ETPUA26) | SIU_PCR140      | 16-bits     | Base + 0x0158 |             |
| Pad configuration register 141 (ETPUA27) | SIU_PCR141      | 16-bits     | Base + 0x015A |             |
| Pad configuration register 142 (ETPUA28) | SIU_PCR142      | 16-bits     | Base + 0x015C |             |
| Pad configuration register 143 (ETPUA29) | SIU_PCR143      | 16-bits     | Base + 0x015E |             |
| Pad configuration register 144 (ETPUA30) | SIU_PCR144      | 16-bits     | Base + 0x0160 |             |
| Pad configuration register 145 (ETPUA31) | SIU_PCR145      | 16-bits     | Base + 0x0162 |             |
| Pad configuration register 146 (TCRCLKB) | SIU_PCR146      | 16-bits     | Base + 0x0164 |             |
| Pad configuration register 147 (ETPUB0)  | SIU_PCR147      | 16-bits     | Base + 0x0166 |             |
| Pad configuration register 148 (ETPUB1)  | SIU_PCR148      | 16-bits     | Base + 0x0168 |             |
| Pad configuration register 149 (ETPUB2)  | SIU_PCR149      | 16-bits     | Base + 0x016A |             |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description                               | Register Name         | Used Size       | Address       | Reference   |
|----------------------------------------------------|-----------------------|-----------------|---------------|-------------|
| Pad configuration register 150 (ETPUB3)            | SIU_PCR150            | 16-bits         | Base + 0x016C |             |
| Pad configuration register 151 (ETPUB4)            | SIU_PCR151            | 16-bits         | Base + 0x016E |             |
| Pad configuration register 152 (ETPUB5)            | SIU_PCR152            | 16-bits         | Base + 0x0170 |             |
| Pad configuration register 153 (ETPUB6)            | SIU_PCR153            | 16-bits         | Base + 0x0172 |             |
| Pad configuration register 154 (ETPUB7)            | SIU_PCR154            | 16-bits         | Base + 0x0174 |             |
| Pad configuration register 155 (ETPUB8)            | SIU_PCR155            | 16-bits         | Base + 0x0176 |             |
| Pad configuration register 156 (ETPUB9)            | SIU_PCR156            | 16-bits         | Base + 0x0178 |             |
| Pad configuration register 157 (ETPUB10)           | SIU_PCR157            | 16-bits         | Base + 0x017A |             |
| Pad configuration register 158 (ETPUB11)           | SIU_PCR158            | 16-bits         | Base + 0x017C |             |
| Pad configuration register 159 (ETPUB12)           | SIU_PCR159            | 16-bits         | Base + 0x017E |             |
| Pad configuration register 160 (ETPUB13)           | SIU_PCR160            | 16-bits         | Base + 0x0180 |             |
| Pad configuration register 161 (ETPUB14)           | SIU_PCR161            | 16-bits         | Base + 0x0182 |             |
| Pad configuration register 162 (ETPUB15)           | SIU_PCR162            | 16-bits         | Base + 0x0184 |             |
| Pad configuration register 163 (ETPUB16)           | SIU_PCR163            | 16-bits         | Base + 0x0186 |             |
| Pad configuration register 164 (ETPUB17)           | SIU_PCR164            | 16-bits         | Base + 0x0188 |             |
| Pad configuration register 165 (ETPUB18)           | SIU_PCR165            | 16-bits         | Base + 0x018A |             |
| Pad configuration register 166 (ETPUB19)           | SIU_PCR166            | 16-bits         | Base + 0x018C |             |
| Pad configuration register 167 (ETPUB20)           | SIU_PCR167            | 16-bits         | Base + 0x018E |             |
| Pad configuration register 168 (ETPUB21)           | SIU_PCR168            | 16-bits         | Base + 0x0190 |             |
| Pad configuration register 169 (ETPUB22)           | SIU_PCR169            | 16-bits         | Base + 0x0192 |             |
| Pad configuration register 170 (ETPUB23)           | SIU_PCR170            | 16-bits         | Base + 0x0194 |             |
| Pad configuration register 171 (ETPUB24)           | SIU_PCR171            | 16-bits         | Base + 0x0196 |             |
| Pad configuration register 172 (ETPUB25)           | SIU_PCR172            | 16-bits         | Base + 0x0198 |             |
| Pad configuration register 173 (ETPUB26)           | SIU_PCR173            | 16-bits         | Base + 0x019A |             |
| Pad configuration register 174 (ETPUB27)           | SIU_PCR174            | 16-bits         | Base + 0x019C |             |
| Pad configuration register 175 (ETPUB28)           | SIU_PCR175            | 16-bits         | Base + 0x019E |             |
| Pad configuration register 176 (ETPUB29)           | SIU_PCR176            | 16-bits         | Base + 0x01A0 |             |
| Pad configuration register 177                     |                       |                 | Base + 0x01A2 |             |
| (ETPUB30) Pad configuration register 178 (ETPUB31) | SIU_PCR177 SIU_PCR178 | 16-bits 16-bits | Base + 0x01A4 |             |
| Pad configuration register 179 (EMIOS0)            | SIU_PCR179            | 16-bits         | Base + 0x01A6 |             |
| Pad configuration register 180 (EMIOS1)            | SIU_PCR180            | 16-bits         | Base + 0x01A8 |             |
| Pad configuration register 181 (EMIOS2)            | SIU_PCR181            | 16-bits         | Base + 0x01AA |             |

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description                      | Register Name   | Used Size   | Address       | Reference   |
|-------------------------------------------|-----------------|-------------|---------------|-------------|
| Pad configuration register 182 (EMIOS3)   | SIU_PCR182      | 16-bits     | Base + 0x01AC |             |
| Pad configuration register 183 (EMIOS4)   | SIU_PCR183      | 16-bits     | Base + 0x01AE |             |
| Pad configuration register 184 (EMIOS5)   | SIU_PCR184      | 16-bits     | Base + 0x01B0 |             |
| Pad configuration register 185 (EMIOS6)   | SIU_PCR185      | 16-bits     | Base + 0x01B2 |             |
| Pad configuration register 186 (EMIOS7)   | SIU_PCR186      | 16-bits     | Base + 0x01B4 |             |
| Pad configuration register 187 (EMIOS8)   | SIU_PCR187      | 16-bits     | Base + 0x01B6 |             |
| Pad configuration register 188 (EMIOS9)   | SIU_PCR188      | 16-bits     | Base + 0x01B8 |             |
| Pad configuration register 189 (EMIOS10)  | SIU_PCR189      | 16-bits     | Base + 0x01BA |             |
| Pad configuration register 190 (EMIOS11)  | SIU_PCR190      | 16-bits     | Base + 0x01BC |             |
| Pad configuration register 191 (EMIOS12)  | SIU_PCR191      | 16-bits     | Base + 0x01BE |             |
| Pad configuration register 192 (EMIOS13)  | SIU_PCR192      | 16-bits     | Base + 0x01C0 |             |
| Pad configuration register 193 (EMIOS14)  | SIU_PCR193      | 16-bits     | Base + 0x01C2 |             |
| Pad configuration register 194 (EMIOS15)  | SIU_PCR194      | 16-bits     | Base + 0x01C4 |             |
| Pad configuration register 195 (EMIOS16)  | SIU_PCR195      | 16-bits     | Base + 0x01C6 |             |
| Pad configuration register 196 (EMIOS17)  | SIU_PCR196      | 16-bits     | Base + 0x01C8 |             |
| Pad configuration register 197 (EMIOS18)  | SIU_PCR197      | 16-bits     | Base + 0x01CA |             |
| Pad configuration register 198 (EMIOS19)  | SIU_PCR198      | 16-bits     | Base + 0x01CC |             |
| Pad configuration register 199 (EMIOS20)  | SIU_PCR199      | 16-bits     | Base + 0x01CE |             |
| Pad configuration register 200 (EMIOS21)  | SIU_PCR200      | 16-bits     | Base + 0x01D0 |             |
| Pad configuration register 201 (EMIOS22)  | SIU_PCR201      | 16-bits     | Base + 0x01D2 |             |
| Pad configuration register 202 (EMIOS23)  | SIU_PCR202      | 16-bits     | Base + 0x01D4 |             |
| Pad configuration register 203 (GPIO203)  | SIU_PCR203      | 16-bits     | Base + 0x01D6 |             |
| Pad configuration register 204 (GPIO204)  | SIU_PCR204      | 16-bits     | Base + 0x01D8 |             |
| Pad configuration register 205 (GPIO205)  | SIU_PCR205      | 16-bits     | Base + 0x01DA |             |
| Pad configuration register 206 (GPIO206)  | SIU_PCR206      | 16-bits     | Base + 0x01DC |             |
| Pad configuration register 207 (GPIO207)  | SIU_PCR207      | 16-bits     | Base + 0x01DE |             |
| Pad configuration register 208 (PLLCFG0)  | SIU_PCR208      | 16-bits     | Base + 0x01E0 |             |
| Pad configuration register 209 (PLLCFG1)  | SIU_PCR209      | 16-bits     | Base + 0x01E2 |             |
| Pad configuration register 210 (RSTCFG)   | SIU_PCR210      | 16-bits     | Base + 0x01E4 |             |
| Pad configuration register 211 (BOOTCFG0) | SIU_PCR211      | 16-bits     | Base + 0x01E6 |             |
| Pad configuration register 212 (BOOTCFG1) | SIU_PCR212      | 16-bits     | Base + 0x01E8 |             |
| Pad configuration register 213 (WKPCFG)   | SIU_PCR213      | 16-bits     | Base + 0x01EA |             |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description                    | Register Name   | Used Size   | Address                | Reference   |
|-----------------------------------------|-----------------|-------------|------------------------|-------------|
| Pad configuration register 214 (ENGCLK) | SIU_PCR214      | 16-bits     | Base + 0x01EC          |             |
| Pad configuration register 215 (AN12)   | SIU_PCR215      | 16-bits     | Base + 0x01EE          |             |
| Pad configuration register 216 (AN13)   | SIU_PCR216      | 16-bits     | Base + 0x01F0          |             |
| Pad configuration register 217 (AN14)   | SIU_PCR217      | 16-bits     | Base + 0x01F2          |             |
| Pad configuration register 218 (AN15)   | SIU_PCR218      | 16-bits     | Base + 0x01F4          |             |
| Pad configuration register 219 (MCKO)   | SIU_PCR219      | 16-bits     | Base + 0x01F6          |             |
| Pad configuration register 220 (MDO0)   | SIU_PCR220      | 16-bits     | Base + 0x01F8          |             |
| Pad configuration register 221 (MDO1)   | SIU_PCR221      | 16-bits     | Base + 0x01FA          |             |
| Pad configuration register 222 (MDO2)   | SIU_PCR222      | 16-bits     | Base + 0x01FC          |             |
| Pad configuration register 223 (MDO3)   | SIU_PCR223      | 16-bits     | Base + 0x01FE          |             |
| Pad configuration register 224 (MSEO0)  | SIU_PCR224      | 16-bits     | Base + 0x0200          |             |
| Pad configuration register 225 (MSEO1)  | SIU_PCR225      | 16-bits     | Base + 0x0202          |             |
| Pad configuration register 226 (RDY)    | SIU_PCR226      | 16-bits     | Base + 0x0204          |             |
| Pad configuration register 227 (EVTO)   | SIU_PCR227      | 16-bits     | Base + 0x0206          |             |
| Pad configuration register 228 (TDO)    | SIU_PCR228      | 16-bits     | Base + 0x0208          |             |
| Pad configuration register 229 (CLKOUT) | SIU_PCR229      | 16-bits     | Base + 0x020A          |             |
| Pad configuration register 230 (RSTOUT) | SIU_PCR230      | 16-bits     | Base + 0x020C          |             |
| Reserved                                | -               | -           | Base + (0x020E-0x05FF) |             |
| GPIO pin data output register 0         | SIU_GPDO0       | 8-bits      | Base + 0x0600          |             |
| GPIO pin data output register 1         | SIU_GPDO1       | 8-bits      | Base + 0x0601          |             |
| GPIO pin data output register 2         | SIU_GPDO2       | 8-bits      | Base + 0x0602          |             |
| GPIO pin data output register 3         | SIU_GPDO3       | 8-bits      | Base + 0x0603          |             |
| GPIO pin data output register 4         | SIU_GPDO4       | 8-bits      | Base + 0x0604          |             |
| GPIO pin data output register 5         | SIU_GPDO5       | 8-bits      | Base + 0x0605          |             |
| GPIO pin data output register 6         | SIU_GPDO6       | 8-bits      | Base + 0x0606          |             |
| GPIO pin data output register 7         | SIU_GPDO7       | 8-bits      | Base + 0x0607          |             |
| GPIO pin data output register 8         | SIU_GPDO8       | 8-bits      | Base + 0x0608          |             |
| GPIO pin data output register 9         | SIU_GPDO9       | 8-bits      | Base + 0x0609          |             |
| GPIO pin data output register 10        | SIU_GPDO10      | 8-bits      | Base + 0x060A          |             |
| GPIO pin data output register 11        | SIU_GPDO11      | 8-bits      | Base + 0x060B          |             |
| GPIO pin data output register 12        | SIU_GPDO12      | 8-bits      | Base + 0x060C          |             |
| GPIO pin data output register 13        | SIU_GPDO13      | 8-bits      | Base + 0x060D          |             |

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description             | Register Name   | Used Size   | Address       | Reference   |
|----------------------------------|-----------------|-------------|---------------|-------------|
| GPIO pin data output register 14 | SIU_GPDO14      | 8-bits      | Base + 0x060E |             |
| GPIO pin data output register 15 | SIU_GPDO15      | 8-bits      | Base + 0x060F |             |
| GPIO pin data output register 16 | SIU_GPDO16      | 8-bits      | Base + 0x0610 |             |
| GPIO pin data output register 17 | SIU_GPDO17      | 8-bits      | Base + 0x0611 |             |
| GPIO pin data output register 18 | SIU_GPDO18      | 8-bits      | Base + 0x0612 |             |
| GPIO pin data output register 19 | SIU_GPDO19      | 8-bits      | Base + 0x0613 |             |
| GPIO pin data output register 20 | SIU_GPDO20      | 8-bits      | Base + 0x0614 |             |
| GPIO pin data output register 21 | SIU_GPDO21      | 8-bits      | Base + 0x0615 |             |
| GPIO pin data output register 22 | SIU_GPDO22      | 8-bits      | Base + 0x0616 |             |
| GPIO pin data output register 23 | SIU_GPDO23      | 8-bits      | Base + 0x0617 |             |
| GPIO pin data output register 24 | SIU_GPDO24      | 8-bits      | Base + 0x0618 |             |
| GPIO pin data output register 25 | SIU_GPDO25      | 8-bits      | Base + 0x0619 |             |
| GPIO pin data output register 26 | SIU_GPDO26      | 8-bits      | Base + 0x061A |             |
| GPIO pin data output register 27 | SIU_GPDO27      | 8-bits      | Base + 0x061B |             |
| GPIO pin data output register 28 | SIU_GPDO28      | 8-bits      | Base + 0x061C |             |
| GPIO pin data output register 29 | SIU_GPDO29      | 8-bits      | Base + 0x061D |             |
| GPIO pin data output register 30 | SIU_GPDO30      | 8-bits      | Base + 0x061E |             |
| GPIO pin data output register 31 | SIU_GPDO31      | 8-bits      | Base + 0x061F |             |
| GPIO pin data output register 32 | SIU_GPDO32      | 8-bits      | Base + 0x0620 |             |
| GPIO pin data output register 33 | SIU_GPDO33      | 8-bits      | Base + 0x0621 |             |
| GPIO pin data output register 34 | SIU_GPDO34      | 8-bits      | Base + 0x0622 |             |
| GPIO pin data output register 35 | SIU_GPDO35      | 8-bits      | Base + 0x0623 |             |
| GPIO pin data output register 36 | SIU_GPDO36      | 8-bits      | Base + 0x0624 |             |
| GPIO pin data output register 37 | SIU_GPDO37      | 8-bits      | Base + 0x0625 |             |
| GPIO pin data output register 38 | SIU_GPDO38      | 8-bits      | Base + 0x0626 |             |
| GPIO pin data output register 39 | SIU_GPDO39      | 8-bits      | Base + 0x0627 |             |
| GPIO pin data output register 40 | SIU_GPDO40      | 8-bits      | Base + 0x0628 |             |
| GPIO pin data output register 41 | SIU_GPDO41      | 8-bits      | Base + 0x0629 |             |
| GPIO pin data output register 42 | SIU_GPDO42      | 8-bits      | Base + 0x062A |             |
| GPIO pin data output register 43 | SIU_GPDO43      | 8-bits      | Base + 0x062B |             |
| GPIO pin data output register 44 | SIU_GPDO44      | 8-bits      | Base + 0x062C |             |
| GPIO pin data output register 45 | SIU_GPDO45      | 8-bits      | Base + 0x062D |             |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description             | Register Name   | Used Size   | Address       | Reference   |
|----------------------------------|-----------------|-------------|---------------|-------------|
| GPIO pin data output register 46 | SIU_GPDO46      | 8-bits      | Base + 0x062E |             |
| GPIO pin data output register 47 | SIU_GPDO47      | 8-bits      | Base + 0x062F |             |
| GPIO pin data output register 48 | SIU_GPDO48      | 8-bits      | Base + 0x0630 |             |
| GPIO pin data output register 49 | SIU_GPDO49      | 8-bits      | Base + 0x0631 |             |
| GPIO pin data output register 50 | SIU_GPDO50      | 8-bits      | Base + 0x0632 |             |
| GPIO pin data output register 51 | SIU_GPDO51      | 8-bits      | Base + 0x0633 |             |
| GPIO pin data output register 52 | SIU_GPDO52      | 8-bits      | Base + 0x0634 |             |
| GPIO pin data output register 53 | SIU_GPDO53      | 8-bits      | Base + 0x0635 |             |
| GPIO pin data output register 54 | SIU_GPDO54      | 8-bits      | Base + 0x0636 |             |
| GPIO pin data output register 55 | SIU_GPDO55      | 8-bits      | Base + 0x0637 |             |
| GPIO pin data output register 56 | SIU_GPDO56      | 8-bits      | Base + 0x0638 |             |
| GPIO pin data output register 57 | SIU_GPDO57      | 8-bits      | Base + 0x0639 |             |
| GPIO pin data output register 58 | SIU_GPDO58      | 8-bits      | Base + 0x063A |             |
| GPIO pin data output register 59 | SIU_GPDO59      | 8-bits      | Base + 0x063B |             |
| GPIO pin data output register 60 | SIU_GPDO60      | 8-bits      | Base + 0x063C |             |
| GPIO pin data output register 61 | SIU_GPDO61      | 8-bits      | Base + 0x063D |             |
| GPIO pin data output register 62 | SIU_GPDO62      | 8-bits      | Base + 0x063E |             |
| GPIO pin data output register 63 | SIU_GPDO63      | 8-bits      | Base + 0x063F |             |
| GPIO pin data output register 64 | SIU_GPDO64      | 8-bits      | Base + 0x0640 |             |
| GPIO pin data output register 65 | SIU_GPDO65      | 8-bits      | Base + 0x0641 |             |
| GPIO pin data output register 66 | SIU_GPDO66      | 8-bits      | Base + 0x0642 |             |
| GPIO pin data output register 67 | SIU_GPDO67      | 8-bits      | Base + 0x0643 |             |
| GPIO pin data output register 68 | SIU_GPDO68      | 8-bits      | Base + 0x0644 |             |
| GPIO pin data output register 69 | SIU_GPDO69      | 8-bits      | Base + 0x0645 |             |
| GPIO pin data output register 70 | SIU_GPDO70      | 8-bits      | Base + 0x0646 |             |
| GPIO pin data output register 71 | SIU_GPDO71      | 8-bits      | Base + 0x0647 |             |
| GPIO pin data output register 72 | SIU_GPDO72      | 8-bits      | Base + 0x0648 |             |
| GPIO pin data output register 73 | SIU_GPDO73      | 8-bits      | Base + 0x0649 |             |
| GPIO pin data output register 74 | SIU_GPDO74      | 8-bits      | Base + 0x064A |             |
| GPIO pin data output register 75 | SIU_GPDO75      | 8-bits      | Base + 0x064B |             |
| GPIO pin data output register 76 | SIU_GPDO76      | 8-bits      | Base + 0x064C |             |
| GPIO pin data output register 77 | SIU_GPDO77      | 8-bits      | Base + 0x064D |             |

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description              | Register Name   | Used Size   | Address       | Reference   |
|-----------------------------------|-----------------|-------------|---------------|-------------|
| GPIO pin data output register 78  | SIU_GPDO78      | 8-bits      | Base + 0x064E |             |
| GPIO pin data output register 79  | SIU_GPDO79      | 8-bits      | Base + 0x064F |             |
| GPIO pin data output register 80  | SIU_GPDO80      | 8-bits      | Base + 0x0650 |             |
| GPIO pin data output register 81  | SIU_GPDO81      | 8-bits      | Base + 0x0651 |             |
| GPIO pin data output register 82  | SIU_GPDO82      | 8-bits      | Base + 0x0652 |             |
| GPIO pin data output register 83  | SIU_GPDO83      | 8-bits      | Base + 0x0653 |             |
| GPIO pin data output register 84  | SIU_GPDO84      | 8-bits      | Base + 0x0654 |             |
| GPIO pin data output register 85  | SIU_GPDO85      | 8-bits      | Base + 0x0655 |             |
| GPIO pin data output register 86  | SIU_GPDO86      | 8-bits      | Base + 0x0656 |             |
| GPIO pin data output register 87  | SIU_GPDO87      | 8-bits      | Base + 0x0657 |             |
| GPIO pin data output register 88  | SIU_GPDO88      | 8-bits      | Base + 0x0658 |             |
| GPIO pin data output register 89  | SIU_GPDO89      | 8-bits      | Base + 0x0659 |             |
| GPIO pin data output register 90  | SIU_GPDO90      | 8-bits      | Base + 0x065A |             |
| GPIO pin data output register 91  | SIU_GPDO91      | 8-bits      | Base + 0x065B |             |
| GPIO pin data output register 92  | SIU_GPDO92      | 8-bits      | Base + 0x065C |             |
| GPIO pin data output register 93  | SIU_GPDO93      | 8-bits      | Base + 0x065D |             |
| GPIO pin data output register 94  | SIU_GPDO94      | 8-bits      | Base + 0x065E |             |
| GPIO pin data output register 95  | SIU_GPDO95      | 8-bits      | Base + 0x065F |             |
| GPIO pin data output register 96  | SIU_GPDO96      | 8-bits      | Base + 0x0660 |             |
| GPIO pin data output register 97  | SIU_GPDO97      | 8-bits      | Base + 0x0661 |             |
| GPIO pin data output register 98  | SIU_GPDO98      | 8-bits      | Base + 0x0662 |             |
| GPIO pin data output register 99  | SIU_GPDO99      | 8-bits      | Base + 0x0663 |             |
| GPIO pin data output register 100 | SIU_GPDO100     | 8-bits      | Base + 0x0664 |             |
| GPIO pin data output register 101 | SIU_GPDO101     | 8-bits      | Base + 0x0665 |             |
| GPIO pin data output register 102 | SIU_GPDO102     | 8-bits      | Base + 0x0666 |             |
| GPIO pin data output register 103 | SIU_GPDO103     | 8-bits      | Base + 0x0667 |             |
| GPIO pin data output register 104 | SIU_GPDO104     | 8-bits      | Base + 0x0668 |             |
| GPIO pin data output register 105 | SIU_GPDO105     | 8-bits      | Base + 0x0669 |             |
| GPIO pin data output register 106 | SIU_GPDO106     | 8-bits      | Base + 0x066A |             |
| GPIO pin data output register 107 | SIU_GPDO107     | 8-bits      | Base + 0x066B |             |
| GPIO pin data output register 108 | SIU_GPDO108     | 8-bits      | Base + 0x066C |             |
| GPIO pin data output register 109 | SIU_GPDO109     | 8-bits      | Base + 0x066D |             |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description              | Register Name   | Used Size   | Address       | Reference   |
|-----------------------------------|-----------------|-------------|---------------|-------------|
| GPIO pin data output register 110 | SIU_GPDO110     | 8-bits      | Base + 0x066E |             |
| GPIO pin data output register 111 | SIU_GPDO111     | 8-bits      | Base + 0x066F |             |
| GPIO pin data output register 112 | SIU_GPDO112     | 8-bits      | Base + 0x0670 |             |
| GPIO pin data output register 113 | SIU_GPDO113     | 8-bits      | Base + 0x0671 |             |
| GPIO pin data output register 114 | SIU_GPDO114     | 8-bits      | Base + 0x0672 |             |
| GPIO pin data output register 115 | SIU_GPDO115     | 8-bits      | Base + 0x0673 |             |
| GPIO pin data output register 116 | SIU_GPDO116     | 8-bits      | Base + 0x0674 |             |
| GPIO pin data output register 117 | SIU_GPDO117     | 8-bits      | Base + 0x0675 |             |
| GPIO pin data output register 118 | SIU_GPDO118     | 8-bits      | Base + 0x0676 |             |
| GPIO pin data output register 119 | SIU_GPDO119     | 8-bits      | Base + 0x0677 |             |
| GPIO pin data output register 120 | SIU_GPDO120     | 8-bits      | Base + 0x0678 |             |
| GPIO pin data output register 121 | SIU_GPDO121     | 8-bits      | Base + 0x0679 |             |
| GPIO pin data output register 122 | SIU_GPDO122     | 8-bits      | Base + 0x067A |             |
| GPIO pin data output register 123 | SIU_GPDO123     | 8-bits      | Base + 0x067B |             |
| GPIO pin data output register 124 | SIU_GPDO124     | 8-bits      | Base + 0x067C |             |
| GPIO pin data output register 125 | SIU_GPDO125     | 8-bits      | Base + 0x067D |             |
| GPIO pin data output register 126 | SIU_GPDO126     | 8-bits      | Base + 0x067E |             |
| GPIO pin data output register 127 | SIU_GPDO127     | 8-bits      | Base + 0x067F |             |
| GPIO pin data output register 128 | SIU_GPDO128     | 8-bits      | Base + 0x0680 |             |
| GPIO pin data output register 129 | SIU_GPDO129     | 8-bits      | Base + 0x0681 |             |
| GPIO pin data output register 130 | SIU_GPDO130     | 8-bits      | Base + 0x0682 |             |
| GPIO pin data output register 131 | SIU_GPDO131     | 8-bits      | Base + 0x0683 |             |
| GPIO pin data output register 132 | SIU_GPDO132     | 8-bits      | Base + 0x0684 |             |
| GPIO pin data output register 133 | SIU_GPDO133     | 8-bits      | Base + 0x0685 |             |
| GPIO pin data output register 134 | SIU_GPDO134     | 8-bits      | Base + 0x0686 |             |
| GPIO pin data output register 135 | SIU_GPDO135     | 8-bits      | Base + 0x0687 |             |
| GPIO pin data output register 136 | SIU_GPDO136     | 8-bits      | Base + 0x0688 |             |
| GPIO pin data output register 137 | SIU_GPDO137     | 8-bits      | Base + 0x0689 |             |
| GPIO pin data output register 138 | SIU_GPDO138     | 8-bits      | Base + 0x068A |             |
| GPIO pin data output register 139 | SIU_GPDO139     | 8-bits      | Base + 0x068B |             |
| GPIO pin data output register 140 | SIU_GPDO140     | 8-bits      | Base + 0x068C |             |
| GPIO pin data output register 141 | SIU_GPDO141     | 8-bits      | Base + 0x068D |             |

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description              | Register Name   | Used Size   | Address       | Reference   |
|-----------------------------------|-----------------|-------------|---------------|-------------|
| GPIO pin data output register 142 | SIU_GPDO142     | 8-bits      | Base + 0x068E |             |
| GPIO pin data output register 143 | SIU_GPDO143     | 8-bits      | Base + 0x068F |             |
| GPIO pin data output register 144 | SIU_GPDO144     | 8-bits      | Base + 0x0690 |             |
| GPIO pin data output register 145 | SIU_GPDO145     | 8-bits      | Base + 0x0691 |             |
| GPIO pin data output register 146 | SIU_GPDO146     | 8-bits      | Base + 0x0692 |             |
| GPIO pin data output register 147 | SIU_GPDO147     | 8-bits      | Base + 0x0693 |             |
| GPIO pin data output register 148 | SIU_GPDO148     | 8-bits      | Base + 0x0694 |             |
| GPIO pin data output register 149 | SIU_GPDO149     | 8-bits      | Base + 0x0695 |             |
| GPIO pin data output register 150 | SIU_GPDO150     | 8-bits      | Base + 0x0696 |             |
| GPIO pin data output register 151 | SIU_GPDO151     | 8-bits      | Base + 0x0697 |             |
| GPIO pin data output register 152 | SIU_GPDO152     | 8-bits      | Base + 0x0698 |             |
| GPIO pin data output register 153 | SIU_GPDO153     | 8-bits      | Base + 0x0699 |             |
| GPIO pin data output register 154 | SIU_GPDO154     | 8-bits      | Base + 0x069A |             |
| GPIO pin data output register 155 | SIU_GPDO155     | 8-bits      | Base + 0x069B |             |
| GPIO pin data output register 156 | SIU_GPDO156     | 8-bits      | Base + 0x069C |             |
| GPIO pin data output register 157 | SIU_GPDO157     | 8-bits      | Base + 0x069D |             |
| GPIO pin data output register 158 | SIU_GPDO158     | 8-bits      | Base + 0x069E |             |
| GPIO pin data output register 159 | SIU_GPDO159     | 8-bits      | Base + 0x069F |             |
| GPIO pin data output register 160 | SIU_GPDO160     | 8-bits      | Base + 0x06A0 |             |
| GPIO pin data output register 161 | SIU_GPDO161     | 8-bits      | Base + 0x06A1 |             |
| GPIO pin data output register 162 | SIU_GPDO162     | 8-bits      | Base + 0x06A2 |             |
| GPIO pin data output register 163 | SIU_GPDO163     | 8-bits      | Base + 0x06A3 |             |
| GPIO pin data output register 164 | SIU_GPDO164     | 8-bits      | Base + 0x06A4 |             |
| GPIO pin data output register 165 | SIU_GPDO165     | 8-bits      | Base + 0x06A5 |             |
| GPIO pin data output register 166 | SIU_GPDO166     | 8-bits      | Base + 0x06A6 |             |
| GPIO pin data output register 167 | SIU_GPDO167     | 8-bits      | Base + 0x06A7 |             |
| GPIO pin data output register 168 | SIU_GPDO168     | 8-bits      | Base + 0x06A8 |             |
| GPIO pin data output register 169 | SIU_GPDO169     | 8-bits      | Base + 0x06A9 |             |
| GPIO pin data output register 170 | SIU_GPDO170     | 8-bits      | Base + 0x06AA |             |
| GPIO pin data output register 171 | SIU_GPDO171     | 8-bits      | Base + 0x06AB |             |
| GPIO pin data output register 172 | SIU_GPDO172     | 8-bits      | Base + 0x06AC |             |
| GPIO pin data output register 173 | SIU_GPDO173     | 8-bits      | Base + 0x06AD |             |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description              | Register Name   | Used Size   | Address       | Reference   |
|-----------------------------------|-----------------|-------------|---------------|-------------|
| GPIO pin data output register 174 | SIU_GPDO174     | 8-bits      | Base + 0x06AE |             |
| GPIO pin data output register 175 | SIU_GPDO175     | 8-bits      | Base + 0x06AF |             |
| GPIO pin data output register 176 | SIU_GPDO176     | 8-bits      | Base + 0x06B0 |             |
| GPIO pin data output register 177 | SIU_GPDO177     | 8-bits      | Base + 0x06B1 |             |
| GPIO pin data output register 178 | SIU_GPDO178     | 8-bits      | Base + 0x06B2 |             |
| GPIO pin data output register 179 | SIU_GPDO179     | 8-bits      | Base + 0x06B3 |             |
| GPIO pin data output register 180 | SIU_GPDO180     | 8-bits      | Base + 0x06B4 |             |
| GPIO pin data output register 181 | SIU_GPDO181     | 8-bits      | Base + 0x06B5 |             |
| GPIO pin data output register 182 | SIU_GPDO182     | 8-bits      | Base + 0x06B6 |             |
| GPIO pin data output register 183 | SIU_GPDO183     | 8-bits      | Base + 0x06B7 |             |
| GPIO pin data output register 184 | SIU_GPDO184     | 8-bits      | Base + 0x06B8 |             |
| GPIO pin data output register 185 | SIU_GPDO185     | 8-bits      | Base + 0x06B9 |             |
| GPIO pin data output register 186 | SIU_GPDO186     | 8-bits      | Base + 0x06BA |             |
| GPIO pin data output register 187 | SIU_GPDO187     | 8-bits      | Base + 0x06BB |             |
| GPIO pin data output register 188 | SIU_GPDO188     | 8-bits      | Base + 0x06BC |             |
| GPIO pin data output register 189 | SIU_GPDO189     | 8-bits      | Base + 0x06BD |             |
| GPIO pin data output register 190 | SIU_GPDO190     | 8-bits      | Base + 0x06BE |             |
| GPIO pin data output register 191 | SIU_GPDO191     | 8-bits      | Base + 0x06BF |             |
| GPIO pin data output register 192 | SIU_GPDO192     | 8-bits      | Base + 0x06C0 |             |
| GPIO pin data output register 193 | SIU_GPDO193     | 8-bits      | Base + 0x06C1 |             |
| GPIO pin data output register 194 | SIU_GPDO194     | 8-bits      | Base + 0x06C2 |             |
| GPIO pin data output register 195 | SIU_GPDO195     | 8-bits      | Base + 0x06C3 |             |
| GPIO pin data output register 196 | SIU_GPDO196     | 8-bits      | Base + 0x06C4 |             |
| GPIO pin data output register 197 | SIU_GPDO197     | 8-bits      | Base + 0x06C5 |             |
| GPIO pin data output register 198 | SIU_GPDO198     | 8-bits      | Base + 0x06C6 |             |
| GPIO pin data output register 199 | SIU_GPDO199     | 8-bits      | Base + 0x06C7 |             |
| GPIO pin data output register 200 | SIU_GPDO200     | 8-bits      | Base + 0x06C8 |             |
| GPIO pin data output register 201 | SIU_GPDO201     | 8-bits      | Base + 0x06C9 |             |
| GPIO pin data output register 202 | SIU_GPDO202     | 8-bits      | Base + 0x06CA |             |
| GPIO pin data output register 203 | SIU_GPDO203     | 8-bits      | Base + 0x06CB |             |
| GPIO pin data output register 204 | SIU_GPDO204     | 8-bits      | Base + 0x06CC |             |
| GPIO pin data output register 205 | SIU_GPDO205     | 8-bits      | Base + 0x06CD |             |

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description              | Register Name   | Used Size   | Address                | Reference   |
|-----------------------------------|-----------------|-------------|------------------------|-------------|
| GPIO pin data output register 206 | SIU_GPDO206     | 8-bits      | Base + 0x06CE          |             |
| GPIO pin data output register 207 | SIU_GPDO207     | 8-bits      | Base + 0x06CF          |             |
| GPIO pin data output register 208 | SIU_GPDO208     | 8-bits      | Base + 0x06D0          |             |
| GPIO pin data output register 209 | SIU_GPDO209     | 8-bits      | Base + 0x06D1          |             |
| GPIO pin data output register 210 | SIU_GPDO210     | 8-bits      | Base + 0x06D2          |             |
| GPIO pin data output register 211 | SIU_GPDO211     | 8-bits      | Base + 0x06D3          |             |
| GPIO pin data output register 212 | SIU_GPDO212     | 8-bits      | Base + 0x06D4          |             |
| GPIO pin data output register 213 | SIU_GPDO213     | 8-bits      | Base + 0x06D5          |             |
| Reserved                          | -               | -           | Base + (0x06D6-0x07FF) |             |
| GPIO pin data input register 0    | SIU_GPDI0       | 8-bits      | Base + 0x0800          |             |
| GPIO pin data input register 1    | SIU_GPDI1       | 8-bits      | Base + 0x0801          |             |
| GPIO pin data input register 2    | SIU_GPDI2       | 8-bits      | Base + 0x0802          |             |
| GPIO pin data input register 3    | SIU_GPDI3       | 8-bits      | Base + 0x0803          |             |
| GPIO pin data input register 4    | SIU_GPDI4       | 8-bits      | Base + 0x0804          |             |
| GPIO pin data input register 5    | SIU_GPDI5       | 8-bits      | Base + 0x0805          |             |
| GPIO pin data input register 6    | SIU_GPDI6       | 8-bits      | Base + 0x0806          |             |
| GPIO pin data input register 7    | SIU_GPDI7       | 8-bits      | Base + 0x0807          |             |
| GPIO pin data input register 8    | SIU_GPDI8       | 8-bits      | Base + 0x0808          |             |
| GPIO pin data input register 9    | SIU_GPDI9       | 8-bits      | Base + 0x0809          |             |
| GPIO pin data input register 10   | SIU_GPDI10      | 8-bits      | Base + 0x080A          |             |
| GPIO pin data input register 11   | SIU_GPDI11      | 8-bits      | Base + 0x080B          |             |
| GPIO pin data input register 12   | SIU_GPDI12      | 8-bits      | Base + 0x080C          |             |
| GPIO pin data input register 13   | SIU_GPDI13      | 8-bits      | Base + 0x080D          |             |
| GPIO pin data input register 14   | SIU_GPDI14      | 8-bits      | Base + 0x080E          |             |
| GPIO pin data input register 15   | SIU_GPDI15      | 8-bits      | Base + 0x080F          |             |
| GPIO pin data input register 16   | SIU_GPDI16      | 8-bits      | Base + 0x0810          |             |
| GPIO pin data input register 17   | SIU_GPDI17      | 8-bits      | Base + 0x0811          |             |
| GPIO pin data input register 18   | SIU_GPDI18      | 8-bits      | Base + 0x0812          |             |
| GPIO pin data input register 19   | SIU_GPDI19      | 8-bits      | Base + 0x0813          |             |
| GPIO pin data input register 20   | SIU_GPDI20      | 8-bits      | Base + 0x0814          |             |
| GPIO pin data input register 21   | SIU_GPDI21      | 8-bits      | Base + 0x0815          |             |
| GPIO pin data input register 22   | SIU_GPDI22      | 8-bits      | Base + 0x0816          |             |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description            | Register Name   | Used Size   | Address       | Reference   |
|---------------------------------|-----------------|-------------|---------------|-------------|
| GPIO pin data input register 23 | SIU_GPDI23      | 8-bits      | Base + 0x0817 |             |
| GPIO pin data input register 24 | SIU_GPDI24      | 8-bits      | Base + 0x0818 |             |
| GPIO pin data input register 25 | SIU_GPDI25      | 8-bits      | Base + 0x0819 |             |
| GPIO pin data input register 26 | SIU_GPDI26      | 8-bits      | Base + 0x081A |             |
| GPIO pin data input register 27 | SIU_GPDI27      | 8-bits      | Base + 0x081B |             |
| GPIO pin data input register 28 | SIU_GPDI28      | 8-bits      | Base + 0x081C |             |
| GPIO pin data input register 29 | SIU_GPDI29      | 8-bits      | Base + 0x081D |             |
| GPIO pin data input register 30 | SIU_GPDI30      | 8-bits      | Base + 0x081E |             |
| GPIO pin data input register 31 | SIU_GPDI31      | 8-bits      | Base + 0x081F |             |
| GPIO pin data input register 32 | SIU_GPDI32      | 8-bits      | Base + 0x0820 |             |
| GPIO pin data input register 33 | SIU_GPDI33      | 8-bits      | Base + 0x0821 |             |
| GPIO pin data input register 34 | SIU_GPDI34      | 8-bits      | Base + 0x0822 |             |
| GPIO pin data input register 35 | SIU_GPDI35      | 8-bits      | Base + 0x0823 |             |
| GPIO pin data input register 36 | SIU_GPDI36      | 8-bits      | Base + 0x0824 |             |
| GPIO pin data input register 37 | SIU_GPDI37      | 8-bits      | Base + 0x0825 |             |
| GPIO pin data input register 38 | SIU_GPDI38      | 8-bits      | Base + 0x0826 |             |
| GPIO pin data input register 39 | SIU_GPDI39      | 8-bits      | Base + 0x0827 |             |
| GPIO pin data input register 40 | SIU_GPDI40      | 8-bits      | Base + 0x0828 |             |
| GPIO pin data input register 41 | SIU_GPDI41      | 8-bits      | Base + 0x0829 |             |
| GPIO pin data input register 42 | SIU_GPDI42      | 8-bits      | Base + 0x082A |             |
| GPIO pin data input register 43 | SIU_GPDI43      | 8-bits      | Base + 0x082B |             |
| GPIO pin data input register 44 | SIU_GPDI44      | 8-bits      | Base + 0x082C |             |
| GPIO pin data input register 45 | SIU_GPDI45      | 8-bits      | Base + 0x082D |             |
| GPIO pin data input register 46 | SIU_GPDI46      | 8-bits      | Base + 0x082E |             |
| GPIO pin data input register 47 | SIU_GPDI47      | 8-bits      | Base + 0x082F |             |
| GPIO pin data input register 48 | SIU_GPDI48      | 8-bits      | Base + 0x0830 |             |
| GPIO pin data input register 49 | SIU_GPDI49      | 8-bits      | Base + 0x0831 |             |
| GPIO pin data input register 50 | SIU_GPDI50      | 8-bits      | Base + 0x0832 |             |
| GPIO pin data input register 51 | SIU_GPDI51      | 8-bits      | Base + 0x0833 |             |
| GPIO pin data input register 52 | SIU_GPDI52      | 8-bits      | Base + 0x0834 |             |
| GPIO pin data input register 53 | SIU_GPDI53      | 8-bits      | Base + 0x0835 |             |
| GPIO pin data input register 54 | SIU_GPDI54      | 8-bits      | Base + 0x0836 |             |

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description            | Register Name   | Used Size   | Address       | Reference   |
|---------------------------------|-----------------|-------------|---------------|-------------|
| GPIO pin data input register 55 | SIU_GPDI55      | 8-bits      | Base + 0x0837 |             |
| GPIO pin data input register 56 | SIU_GPDI56      | 8-bits      | Base + 0x0838 |             |
| GPIO pin data input register 57 | SIU_GPDI57      | 8-bits      | Base + 0x0839 |             |
| GPIO pin data input register 58 | SIU_GPDI58      | 8-bits      | Base + 0x083A |             |
| GPIO pin data input register 59 | SIU_GPDI59      | 8-bits      | Base + 0x083B |             |
| GPIO pin data input register 60 | SIU_GPDI60      | 8-bits      | Base + 0x083C |             |
| GPIO pin data input register 61 | SIU_GPDI61      | 8-bits      | Base + 0x083D |             |
| GPIO pin data input register 62 | SIU_GPDI62      | 8-bits      | Base + 0x083E |             |
| GPIO pin data input register 63 | SIU_GPDI63      | 8-bits      | Base + 0x083F |             |
| GPIO pin data input register 64 | SIU_GPDI64      | 8-bits      | Base + 0x0840 |             |
| GPIO pin data input register 65 | SIU_GPDI65      | 8-bits      | Base + 0x0841 |             |
| GPIO pin data input register 66 | SIU_GPDI66      | 8-bits      | Base + 0x0842 |             |
| GPIO pin data input register 67 | SIU_GPDI67      | 8-bits      | Base + 0x0843 |             |
| GPIO pin data input register 68 | SIU_GPDI68      | 8-bits      | Base + 0x0844 |             |
| GPIO pin data input register 69 | SIU_GPDI69      | 8-bits      | Base + 0x0845 |             |
| GPIO pin data input register 70 | SIU_GPDI70      | 8-bits      | Base + 0x0846 |             |
| GPIO pin data input register 71 | SIU_GPDI71      | 8-bits      | Base + 0x0847 |             |
| GPIO pin data input register 72 | SIU_GPDI72      | 8-bits      | Base + 0x0848 |             |
| GPIO pin data input register 73 | SIU_GPDI73      | 8-bits      | Base + 0x0849 |             |
| GPIO pin data input register 74 | SIU_GPDI74      | 8-bits      | Base + 0x084A |             |
| GPIO pin data input register 75 | SIU_GPDI75      | 8-bits      | Base + 0x084B |             |
| GPIO pin data input register 76 | SIU_GPDI76      | 8-bits      | Base + 0x084C |             |
| GPIO pin data input register 77 | SIU_GPDI77      | 8-bits      | Base + 0x084D |             |
| GPIO pin data input register 78 | SIU_GPDI78      | 8-bits      | Base + 0x084E |             |
| GPIO pin data input register 79 | SIU_GPDI79      | 8-bits      | Base + 0x084F |             |
| GPIO pin data input register 80 | SIU_GPDI80      | 8-bits      | Base + 0x0850 |             |
| GPIO pin data input register 81 | SIU_GPDI81      | 8-bits      | Base + 0x0851 |             |
| GPIO pin data input register 82 | SIU_GPDI82      | 8-bits      | Base + 0x0852 |             |
| GPIO pin data input register 83 | SIU_GPDI83      | 8-bits      | Base + 0x0853 |             |
| GPIO pin data input register 84 | SIU_GPDI84      | 8-bits      | Base + 0x0854 |             |
| GPIO pin data input register 85 | SIU_GPDI85      | 8-bits      | Base + 0x0855 |             |
| GPIO pin data input register 86 | SIU_GPDI86      | 8-bits      | Base + 0x0856 |             |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description             | Register Name   | Used Size   | Address       | Reference   |
|----------------------------------|-----------------|-------------|---------------|-------------|
| GPIO pin data input register 87  | SIU_GPDI87      | 8-bits      | Base + 0x0857 |             |
| GPIO pin data input register 88  | SIU_GPDI88      | 8-bits      | Base + 0x0858 |             |
| GPIO pin data input register 89  | SIU_GPDI89      | 8-bits      | Base + 0x0859 |             |
| GPIO pin data input register 90  | SIU_GPDI90      | 8-bits      | Base + 0x085A |             |
| GPIO pin data input register 91  | SIU_GPDI91      | 8-bits      | Base + 0x085B |             |
| GPIO pin data input register 92  | SIU_GPDI92      | 8-bits      | Base + 0x085C |             |
| GPIO pin data input register 93  | SIU_GPDI93      | 8-bits      | Base + 0x085D |             |
| GPIO pin data input register 94  | SIU_GPDI94      | 8-bits      | Base + 0x085E |             |
| GPIO pin data input register 95  | SIU_GPDI95      | 8-bits      | Base + 0x085F |             |
| GPIO pin data input register 96  | SIU_GPDI96      | 8-bits      | Base + 0x0860 |             |
| GPIO pin data input register 97  | SIU_GPDI97      | 8-bits      | Base + 0x0861 |             |
| GPIO pin data input register 98  | SIU_GPDI98      | 8-bits      | Base + 0x0862 |             |
| GPIO pin data input register 99  | SIU_GPDI99      | 8-bits      | Base + 0x0863 |             |
| GPIO pin data input register 100 | SIU_GPDI100     | 8-bits      | Base + 0x0864 |             |
| GPIO pin data input register 101 | SIU_GPDI101     | 8-bits      | Base + 0x0865 |             |
| GPIO pin data input register 102 | SIU_GPDI102     | 8-bits      | Base + 0x0866 |             |
| GPIO pin data input register 103 | SIU_GPDI103     | 8-bits      | Base + 0x0867 |             |
| GPIO pin data input register 104 | SIU_GPDI104     | 8-bits      | Base + 0x0868 |             |
| GPIO pin data input register 105 | SIU_GPDI105     | 8-bits      | Base + 0x0869 |             |
| GPIO pin data input register 106 | SIU_GPDI106     | 8-bits      | Base + 0x086A |             |
| GPIO pin data input register 107 | SIU_GPDI107     | 8-bits      | Base + 0x086B |             |
| GPIO pin data input register 108 | SIU_GPDI108     | 8-bits      | Base + 0x086C |             |
| GPIO pin data input register 109 | SIU_GPDI109     | 8-bits      | Base + 0x086D |             |
| GPIO pin data input register 110 | SIU_GPDI110     | 8-bits      | Base + 0x086E |             |
| GPIO pin data input register 111 | SIU_GPDI111     | 8-bits      | Base + 0x086F |             |
| GPIO pin data input register 112 | SIU_GPDI112     | 8-bits      | Base + 0x0870 |             |
| GPIO pin data input register 113 | SIU_GPDI113     | 8-bits      | Base + 0x0871 |             |
| GPIO pin data input register 114 | SIU_GPDI114     | 8-bits      | Base + 0x0872 |             |
| GPIO pin data input register 115 | SIU_GPDI115     | 8-bits      | Base + 0x0873 |             |
| GPIO pin data input register 116 | SIU_GPDI116     | 8-bits      | Base + 0x0874 |             |
| GPIO pin data input register 117 | SIU_GPDI117     | 8-bits      | Base + 0x0875 |             |
| GPIO pin data input register 118 | SIU_GPDI118     | 8-bits      | Base + 0x0876 |             |

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description             | Register Name   | Used Size   | Address       | Reference   |
|----------------------------------|-----------------|-------------|---------------|-------------|
| GPIO pin data input register 119 | SIU_GPDI119     | 8-bits      | Base + 0x0877 |             |
| GPIO pin data input register 120 | SIU_GPDI120     | 8-bits      | Base + 0x0878 |             |
| GPIO pin data input register 121 | SIU_GPDI121     | 8-bits      | Base + 0x0879 |             |
| GPIO pin data input register 122 | SIU_GPDI122     | 8-bits      | Base + 0x087A |             |
| GPIO pin data input register 123 | SIU_GPDI123     | 8-bits      | Base + 0x087B |             |
| GPIO pin data input register 124 | SIU_GPDI124     | 8-bits      | Base + 0x087C |             |
| GPIO pin data input register 125 | SIU_GPDI125     | 8-bits      | Base + 0x087D |             |
| GPIO pin data input register 126 | SIU_GPDI126     | 8-bits      | Base + 0x087E |             |
| GPIO pin data input register 127 | SIU_GPDI127     | 8-bits      | Base + 0x087F |             |
| GPIO pin data input register 128 | SIU_GPDI128     | 8-bits      | Base + 0x0880 |             |
| GPIO pin data input register 129 | SIU_GPDI129     | 8-bits      | Base + 0x0881 |             |
| GPIO pin data input register 130 | SIU_GPDI130     | 8-bits      | Base + 0x0882 |             |
| GPIO pin data input register 131 | SIU_GPDI131     | 8-bits      | Base + 0x0883 |             |
| GPIO pin data input register 132 | SIU_GPDI132     | 8-bits      | Base + 0x0884 |             |
| GPIO pin data input register 133 | SIU_GPDI133     | 8-bits      | Base + 0x0885 |             |
| GPIO pin data input register 134 | SIU_GPDI134     | 8-bits      | Base + 0x0886 |             |
| GPIO pin data input register 135 | SIU_GPDI135     | 8-bits      | Base + 0x0887 |             |
| GPIO pin data input register 136 | SIU_GPDI136     | 8-bits      | Base + 0x0888 |             |
| GPIO pin data input register 137 | SIU_GPDI137     | 8-bits      | Base + 0x0889 |             |
| GPIO pin data input register 138 | SIU_GPDI138     | 8-bits      | Base + 0x088A |             |
| GPIO pin data input register 139 | SIU_GPDI139     | 8-bits      | Base + 0x088B |             |
| GPIO pin data input register 140 | SIU_GPDI140     | 8-bits      | Base + 0x088C |             |
| GPIO pin data input register 141 | SIU_GPDI141     | 8-bits      | Base + 0x088D |             |
| GPIO pin data input register 142 | SIU_GPDI142     | 8-bits      | Base + 0x088E |             |
| GPIO pin data input register 143 | SIU_GPDI143     | 8-bits      | Base + 0x088F |             |
| GPIO pin data input register 144 | SIU_GPDI144     | 8-bits      | Base + 0x0890 |             |
| GPIO pin data input register 145 | SIU_GPDI145     | 8-bits      | Base + 0x0891 |             |
| GPIO pin data input register 146 | SIU_GPDI146     | 8-bits      | Base + 0x0892 |             |
| GPIO pin data input register 147 | SIU_GPDI147     | 8-bits      | Base + 0x0893 |             |
| GPIO pin data input register 148 | SIU_GPDI148     | 8-bits      | Base + 0x0894 |             |
| GPIO pin data input register 149 | SIU_GPDI149     | 8-bits      | Base + 0x0895 |             |
| GPIO pin data input register 150 | SIU_GPDI150     | 8-bits      | Base + 0x0896 |             |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description             | Register Name   | Used Size   | Address       | Reference   |
|----------------------------------|-----------------|-------------|---------------|-------------|
| GPIO pin data input register 151 | SIU_GPDI151     | 8-bits      | Base + 0x0897 |             |
| GPIO pin data input register 152 | SIU_GPDI152     | 8-bits      | Base + 0x0898 |             |
| GPIO pin data input register 153 | SIU_GPDI153     | 8-bits      | Base + 0x0899 |             |
| GPIO pin data input register 154 | SIU_GPDI154     | 8-bits      | Base + 0x089A |             |
| GPIO pin data input register 155 | SIU_GPDI155     | 8-bits      | Base + 0x089B |             |
| GPIO pin data input register 156 | SIU_GPDI156     | 8-bits      | Base + 0x089C |             |
| GPIO pin data input register 157 | SIU_GPDI157     | 8-bits      | Base + 0x089D |             |
| GPIO pin data input register 158 | SIU_GPDI158     | 8-bits      | Base + 0x089E |             |
| GPIO pin data input register 159 | SIU_GPDI159     | 8-bits      | Base + 0x089F |             |
| GPIO pin data input register 160 | SIU_GPDI160     | 8-bits      | Base + 0x08A0 |             |
| GPIO pin data input register 161 | SIU_GPDI161     | 8-bits      | Base + 0x08A1 |             |
| GPIO pin data input register 162 | SIU_GPDI162     | 8-bits      | Base + 0x08A2 |             |
| GPIO pin data input register 163 | SIU_GPDI163     | 8-bits      | Base + 0x08A3 |             |
| GPIO pin data input register 164 | SIU_GPDI164     | 8-bits      | Base + 0x08A4 |             |
| GPIO pin data input register 165 | SIU_GPDI165     | 8-bits      | Base + 0x08A5 |             |
| GPIO pin data input register 166 | SIU_GPDI166     | 8-bits      | Base + 0x08A6 |             |
| GPIO pin data input register 167 | SIU_GPDI167     | 8-bits      | Base + 0x08A7 |             |
| GPIO pin data input register 168 | SIU_GPDI168     | 8-bits      | Base + 0x08A8 |             |
| GPIO pin data input register 169 | SIU_GPDI169     | 8-bits      | Base + 0x08A9 |             |
| GPIO pin data input register 170 | SIU_GPDI170     | 8-bits      | Base + 0x08AA |             |
| GPIO pin data input register 171 | SIU_GPDI171     | 8-bits      | Base + 0x08AB |             |
| GPIO pin data input register 172 | SIU_GPDI172     | 8-bits      | Base + 0x08AC |             |
| GPIO pin data input register 173 | SIU_GPDI173     | 8-bits      | Base + 0x08AD |             |
| GPIO pin data input register 174 | SIU_GPDI174     | 8-bits      | Base + 0x08AE |             |
| GPIO pin data input register 175 | SIU_GPDI175     | 8-bits      | Base + 0x08AF |             |
| GPIO pin data input register 176 | SIU_GPDI176     | 8-bits      | Base + 0x08B0 |             |
| GPIO pin data input register 177 | SIU_GPDI177     | 8-bits      | Base + 0x08B1 |             |
| GPIO pin data input register 178 | SIU_GPDI178     | 8-bits      | Base + 0x08B2 |             |
| GPIO pin data input register 179 | SIU_GPDI179     | 8-bits      | Base + 0x08B3 |             |
| GPIO pin data input register 180 | SIU_GPDI180     | 8-bits      | Base + 0x08B4 |             |
| GPIO pin data input register 181 | SIU_GPDI181     | 8-bits      | Base + 0x08B5 |             |
| GPIO pin data input register 182 | SIU_GPDI182     | 8-bits      | Base + 0x08B6 |             |

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description             | Register Name   | Used Size   | Address                | Reference   |
|----------------------------------|-----------------|-------------|------------------------|-------------|
| GPIO pin data input register 183 | SIU_GPDI183     | 8-bits      | Base + 0x08B7          |             |
| GPIO pin data input register 184 | SIU_GPDI184     | 8-bits      | Base + 0x08B8          |             |
| GPIO pin data input register 185 | SIU_GPDI185     | 8-bits      | Base + 0x08B9          |             |
| GPIO pin data input register 186 | SIU_GPDI186     | 8-bits      | Base + 0x08BA          |             |
| GPIO pin data input register 187 | SIU_GPDI187     | 8-bits      | Base + 0x08BB          |             |
| GPIO pin data input register 188 | SIU_GPDI188     | 8-bits      | Base + 0x08BC          |             |
| GPIO pin data input register 189 | SIU_GPDI189     | 8-bits      | Base + 0x08BD          |             |
| GPIO pin data input register 190 | SIU_GPDI190     | 8-bits      | Base + 0x08BE          |             |
| GPIO pin data input register 191 | SIU_GPDI191     | 8-bits      | Base + 0x08BF          |             |
| GPIO pin data input register 192 | SIU_GPDI192     | 8-bits      | Base + 0x08C0          |             |
| GPIO pin data input register 193 | SIU_GPDI193     | 8-bits      | Base + 0x08C1          |             |
| GPIO pin data input register 194 | SIU_GPDI194     | 8-bits      | Base + 0x08C2          |             |
| GPIO pin data input register 195 | SIU_GPDI195     | 8-bits      | Base + 0x08C3          |             |
| GPIO pin data input register 196 | SIU_GPDI196     | 8-bits      | Base + 0x08C4          |             |
| GPIO pin data input register 197 | SIU_GPDI197     | 8-bits      | Base + 0x08C5          |             |
| GPIO pin data input register 198 | SIU_GPDI198     | 8-bits      | Base + 0x08C6          |             |
| GPIO pin data input register 199 | SIU_GPDI199     | 8-bits      | Base + 0x08C7          |             |
| GPIO pin data input register 200 | SIU_GPDI200     | 8-bits      | Base + 0x08C8          |             |
| GPIO pin data input register 201 | SIU_GPDI201     | 8-bits      | Base + 0x08C9          |             |
| GPIO pin data input register 202 | SIU_GPDI202     | 8-bits      | Base + 0x08CA          |             |
| GPIO pin data input register 203 | SIU_GPDI203     | 8-bits      | Base + 0x08CB          |             |
| GPIO pin data input register 204 | SIU_GPDI204     | 8-bits      | Base + 0x08CC          |             |
| GPIO pin data input register 205 | SIU_GPDI205     | 8-bits      | Base + 0x08CD          |             |
| GPIO pin data input register 206 | SIU_GPDI206     | 8-bits      | Base + 0x08CE          |             |
| GPIO pin data input register 207 | SIU_GPDI207     | 8-bits      | Base + 0x08CF          |             |
| GPIO pin data input register 208 | SIU_GPDI208     | 8-bits      | Base + 0x08D0          |             |
| GPIO pin data input register 209 | SIU_GPDI209     | 8-bits      | Base + 0x08D1          |             |
| GPIO pin data input register 210 | SIU_GPDI210     | 8-bits      | Base + 0x08D2          |             |
| GPIO pin data input register 211 | SIU_GPDI211     | 8-bits      | Base + 0x08D3          |             |
| GPIO pin data input register 212 | SIU_GPDI212     | 8-bits      | Base + 0x08D4          |             |
| GPIO pin data input register 213 | SIU_GPDI213     | 8-bits      | Base + 0x08D5          |             |
| Reserved                         | -               | -           | Base + (0x08D6-0x08FF) |             |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description                            | Register Name                                   | Used Size   | Address                       | Reference                                                     |
|-------------------------------------------------|-------------------------------------------------|-------------|-------------------------------|---------------------------------------------------------------|
| eQADC trigger input select register             | SIU_ETISR                                       | 32-bits     | Base + 0x0900                 |                                                               |
| External IRQ input select register              | SIU_EIISR                                       | 32-bits     | Base + 0x0904                 |                                                               |
| DSPI input select register                      | SIU_DISR                                        | 32-bits     | Base + 0x0908                 |                                                               |
| Reserved                                        | -                                               | -           | Base + (0x090C-0x097F)        |                                                               |
| Chip configuration register                     | SIU_CCR                                         | 32-bits     | Base + 0x0980                 |                                                               |
| External clock control register                 | SIU_ECCR                                        | 32-bits     | Base + 0x0984                 |                                                               |
| Compare A high register                         | SIU_CARH                                        | 32-bits     | Base + 0x0988                 |                                                               |
| Compare A low register                          | SIU_CARL                                        | 32-bits     | Base + 0x098C                 |                                                               |
| Compare B high register                         | SIU_CBRH                                        | 32-bits     | Base + 0x0990                 |                                                               |
| Compare B low register                          | SIU_CBRL                                        | 32-bits     | Base + 0x0994                 |                                                               |
| Reserved                                        | -                                               | -           | (Base + 0x0998)- 0xC3F9_FFFF) |                                                               |
| Enhanced Modular Input/Output Subsystem (eMIOS) | Enhanced Modular Input/Output Subsystem (eMIOS) |             | 0xC3FA_0000                   | Chapter 17, 'Enhanced Modular Input/Output Subsystem (eMIOS)' |
| Module configuration register                   | EMIOS_MCR                                       | 32-bit      | Base + 0x0000                 |                                                               |
| Global flag register                            | EMIOS_GFR                                       | 32-bit      | Base+ 0x0004                  |                                                               |
| Output update disable register                  | EMIOS_OUDR                                      | 32-bit      | Base + 0x0008                 |                                                               |
| Reserved                                        | -                                               | -           | Base + (0x000C-0x001F)        |                                                               |
| Unified channel n, where n = 0-23               | UC base addresses (UCn)                         |             | Base + (0x0020 * (n+1))       |                                                               |
| Channel A data register n                       | EMIOS_CADRn                                     | 32-bit      | UCnBase + 0x00                |                                                               |
| Channel B data register n                       | EMIOS_CBDRn                                     | 32-bit      | UCnBase + 0x04                |                                                               |
| Channel counter register n                      | EMIOS_CCNTRn                                    | 32-bit      | UCnBase + 0x08                |                                                               |
| Channel control register n                      | EMIOS_CCRn                                      | 32-bit      | UCnBase + 0x0C                |                                                               |
| Channel status register n                       | EMIOS_CSRn                                      | 32-bit      | UCnBase + 0x10                |                                                               |
| Reserved                                        | -                                               | -           | (UCnBase + 0x14)- 0xC3FB_FFFF |                                                               |
| Enhanced Time Processing Unit (eTPU)            | Enhanced Time Processing Unit (eTPU)            |             | 0xC3FC_0000                   | Chapter 18, 'Enhanced Time Processing Unit (eTPU)'            |
| eTPU module configuration register              | ETPU_MCR                                        | 32-bit      | Base + 0x0000                 |                                                               |

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description                                            | Register Name    | Used Size   | Address                | Reference   |
|-----------------------------------------------------------------|------------------|-------------|------------------------|-------------|
| eTPU coherent dual-parameter controller register                | ETPU_CDCR        | 32-bit      | Base + 0x0004          |             |
| Reserved                                                        | -                | -           | Base + (0x0008-0x000B) |             |
| eTPU miscellaneous compare register                             | ETPU_MISCCMPR    | 32-bit      | Base + 0x000C          |             |
| eTPU SCM off-range data register                                | ETPU_SCMOFFDATAR | 32-bit      | Base + 0x0010          |             |
| eTPU A engine configuration register                            | ETPU_ECR_A       | 32-bit      | Base + 0x0014          |             |
| eTPU B engine Configuration register 2                          | ETPU_ECR_B 2     | 32-bit      | Base + 0x0018          |             |
| Reserved                                                        | -                | -           | Base + (0x001C-0x001F) |             |
| eTPU A time base configuration register                         | ETPU_TBCR_A      | 32-bit      | Base + 0x0020          |             |
| eTPU A time base 1                                              | ETPU_TB1R_A      | 32-bit      | Base + 0x0024          |             |
| eTPU A time base 2                                              | ETPU_TB2R_A      | 32-bit      | Base + 0x0028          |             |
| eTPU A STAC bus interface configuration register                | ETPU_REDCR_A     | 32-bit      | Base + 0x002C          |             |
| Reserved                                                        | -                | -           | Base + (0x0030-0x003F) |             |
| eTPU B time base configuration register 2                       | ETPU_TBCR_B 2    | 32-bit      | Base + 0x0040          |             |
| eTPU B time base 1                                              | ETPU_TB1R_B 2    | 32-bit      | Base + 0x0044          |             |
| eTPU B time base 2                                              | ETPU_TB2R_B 2    | 32-bit      | Base + 0x0048          |             |
| eTPU BSTACbusinterface configuration register 2                 | ETPU_REDCR_B 2   | 32-bit      | Base + 0x004C          |             |
| Reserved                                                        | -                | -           | Base + (0x0050-0x01FF) |             |
| eTPU A channel interrupt status register                        | ETPU_CISR_A      | 32-bit      | Base + 0x0200          |             |
| eTPU B channel interrupt status register 2                      | ETPU_CISR_B 2    | 32-bit      | Base + 0x0204          |             |
| Reserved                                                        | -                | -           | Base + (0x0208-0x020F) |             |
| eTPU A channel data transfer request status register            | ETPU_CDTRSR_A    | 32-bit      | Base + 0x0210          |             |
| eTPU B channel data transfer request status register 2          | ETPU_CDTRSR_B 2  | 32-bit      | Base + 0x0214          |             |
| Reserved                                                        | -                | -           | Base + (0x0218-0x021F) |             |
| eTPU A channel interrupt overflow status register               | ETPU_CIOSR_A     | 32-bit      | Base + 0x0220          |             |
| eTPUBchannelinterrupt overflow status register 2                | ETPU_CIOSR_B 2   | 32-bit      | Base + 0x0224          |             |
| Reserved                                                        | -                | -           | Base + (0x0228-0x022F) |             |
| eTPU A channel data transfer request overflow status register   | ETPU_CDTROSR_A   | 32-bit      | Base + 0x0230          |             |
| eTPU B channel data transfer request overflow status register 2 | ETPU_CDTROSR_B 2 | 32-bit      | Base + 0x0234          |             |
| Reserved                                                        | -                | -           | Base + (0x0238-0x023F) |             |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description                                   | Register Name   | Used Size   | Address                | Reference   |
|--------------------------------------------------------|-----------------|-------------|------------------------|-------------|
| eTPU A channel interrupt enable register               | ETPU_CIER_A     | 32-bit      | Base + 0x0240          |             |
| eTPU B channel interrupt enable register 2             | ETPU_CIER_B 2   | 32-bit      | Base + 0x0244          |             |
| Reserved                                               | -               | -           | Base + (0x0248-0x024F) |             |
| eTPU A channel data transfer request enable register   | ETPU_CDTRER_A   | 32-bit      | Base + 0x0250          |             |
| eTPU B channel data transfer request enable register 2 | ETPU_CDTRER_B 2 | 32-bit      | Base + 0x0254          |             |
| Reserved                                               | -               | -           | Base + (0x0258-0x027F) |             |
| eTPU A channel pending service status register         | ETPU_CPSSR_A    | 32-bit      | Base + 0x0280          |             |
| eTPU B channel pending service status register 2       | ETPU_CPSSR_B 2  | 32-bit      | Base + 0x0284          |             |
| Reserved                                               | -               | -           | Base + (0x0288-0x028F) |             |
| eTPU A channel service status register                 | ETPU_CSSR_A     | 32-bit      | Base + 0x0290          |             |
| eTPU B channel service status register 2               | ETPU_CSSR_B 2   | 32-bit      | Base + 0x0294          |             |
| Reserved                                               | -               | -           | Base + (0x0298-0x03FF) |             |
| eTPU A channel 0 configuration register                | ETPU_C0CR_A     | 32-bit      | Base + 0x0400          |             |
| eTPU A channel 0 status and control register           | ETPU_C0SCR_A    | 32-bit      | Base + 0x0404          |             |
| eTPU A channel 0 host service request register         | ETPU_C0HSRR_A   | 32-bit      | Base + 0x0408          |             |
| Reserved                                               | -               | -           | Base + (0x040C-0x040F) |             |
| eTPU A channel 1 configuration register                | ETPU_C1CR_A     | 32-bit      | Base + 0x0410          |             |
| eTPU A channel 1 status and control register           | ETPU_C1SCR_A    | 32-bit      | Base + 0x0414          |             |
| eTPU A channel 1 host service request register         | ETPU_C1HSRR_A   | 32-bit      | Base + 0x0418          |             |
| Reserved                                               | -               | -           | Base + (0x041C-0x041F) |             |
| eTPU A channel 2 configuration register                | ETPU_C2CR_A     | 32-bit      | Base + 0x0420          |             |
| eTPU A channel 2 status and control register           | ETPU_C2SCR_A    | 32-bit      | Base + 0x0424          |             |
| eTPU A channel 2 host service request register         | ETPU_C2HSRR_A   | 32-bit      | Base + 0x0428          |             |
| Reserved                                               | -               | -           | Base + (0x042C-0x042F) |             |
| eTPU A channel 3 configuration register                | ETPU_C3CR_A     | 32-bit      | Base + 0x0430          |             |
| eTPU A channel 3 status and control register           | ETPU_C3SCR_A    | 32-bit      | Base + 0x0434          |             |
| eTPU A channel 3 host service request register         | ETPU_C3HSRR_A   | 32-bit      | Base + 0x0438          |             |
| Reserved                                               | -               | -           | Base + (0x043C-0x043F) |             |
| eTPU A channel 4 configuration register                | ETPU_C4CR_A     | 32-bit      | Base + 0x0440          |             |
| eTPU A channel 4 status and control register           | ETPU_C4SCR_A    | 32-bit      | Base + 0x0444          |             |
| eTPU A channel 4 host service request register         | ETPU_C4HSRR_A   | 32-bit      | Base + 0x0448          |             |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description                            | Register Name   | Used Size   | Address                | Reference   |
|-------------------------------------------------|-----------------|-------------|------------------------|-------------|
| Reserved                                        | -               | -           | Base + (0x044C-0x044F) |             |
| eTPU A channel 5 configuration register         | ETPU_C5CR_A     | 32-bit      | Base + 0x0450          |             |
| eTPU A channel 5 status and control register    | ETPU_C5SCR_A    | 32-bit      | Base + 0x0454          |             |
| eTPU A channel 5 host service request register  | ETPU_C5HSRR_A   | 32-bit      | Base + 0x0458          |             |
| Reserved                                        | -               | -           | Base + (0x045C-0x045F) |             |
| eTPU A channel 6 configuration register         | ETPU_C6CR_A     | 32-bit      | Base + 0x0460          |             |
| eTPU A channel 6 status and control register    | ETPU_C6SCR_A    | 32-bit      | Base + 0x0464          |             |
| eTPU A channel 6 host service request register  | ETPU_C6HSRR_A   | 32-bit      | Base + 0x0468          |             |
| Reserved                                        | -               | -           | Base + (0x046C-0x046F) |             |
| eTPU A channel 7 configuration register         | ETPU_C7CR_A     | 32-bit      | Base + 0x0470          |             |
| eTPU A channel 7 status and control register    | ETPU_C7SCR_A    | 32-bit      | Base + 0x0474          |             |
| eTPU A channel 7 host service request register  | ETPU_C7HSRR_A   | 32-bit      | Base + 0x0478          |             |
| Reserved                                        | -               | -           | Base + (0x047C-0x047F) |             |
| eTPU A channel 8 configuration register         | ETPU_C8CR_A     | 32-bit      | Base + 0x0480          |             |
| eTPU A channel 8 status and control register    | ETPU_C8SCR_A    | 32-bit      | Base + 0x0484          |             |
| eTPU A channel 8 host service request register  | ETPU_C8HSRR_A   | 32-bit      | Base + 0x0488          |             |
| Reserved                                        | -               | -           | Base + (0x048C-0x048F) |             |
| eTPU A channel 9 configuration register         | ETPU_C9CR_A     | 32-bit      | Base + 0x0490          |             |
| eTPU A channel 9 status and control register    | ETPU_C9SCR_A    | 32-bit      | Base + 0x0494          |             |
| eTPU A channel 9 host service request register  | ETPU_C9HSRR_A   | 32-bit      | Base + 0x0498          |             |
| Reserved                                        | -               | -           | Base + (0x049C-0x049F) |             |
| eTPU A channel 10 configuration register        | ETPU_C10CR_A    | 32-bit      | Base + 0x04A0          |             |
| eTPU A channel 10 status and control register   | ETPU_C10SCR_A   | 32-bit      | Base + 0x04A4          |             |
| eTPU A channel 10 host service request register | ETPU_C10HSRR_A  | 32-bit      | Base + 0x04A8          |             |
| Reserved                                        | -               | -           | Base + (0x04AC-0x04AF) |             |
| eTPU A channel 11 configuration register        | ETPU_C11CR_A    | 32-bit      | Base + 0x04B0          |             |
| eTPU A channel 11 status and control register   | ETPU_C11SCR_A   | 32-bit      | Base + 0x04B4          |             |
| eTPU A channel 11 host service request register | ETPU_C11HSRR_A  | 32-bit      | Base + 0x04B8          |             |
| Reserved                                        | -               | -           | Base + (0x04BC-0x04BF) |             |
| eTPU A channel 12 configuration register        | ETPU_C12CR_A    | 32-bit      | Base + 0x04C0          |             |
| eTPU A channel 12 status and control register   | ETPU_C12SCR_A   | 32-bit      | Base + 0x04C4          |             |
| eTPU A channel 12 host service request register | ETPU_C12HSRR_A  | 32-bit      | Base + 0x04C8          |             |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description                            | Register Name   | Used Size   | Address                | Reference   |
|-------------------------------------------------|-----------------|-------------|------------------------|-------------|
| Reserved                                        | -               | -           | Base + (0x04CC-0x04CF) |             |
| eTPU A channel 13 configuration register        | ETPU_C13CR_A    | 32-bit      | Base + 0x04D0          |             |
| eTPU A channel 13 status and control register   | ETPU_C13SCR_A   | 32-bit      | Base + 0x04D4          |             |
| eTPU A channel 13 host service request register | ETPU_C13HSRR_A  | 32-bit      | Base + 0x04D8          |             |
| Reserved                                        | -               | -           | Base + (0x04DC-0x04DF) |             |
| eTPU A channel 14 configuration register        | ETPU_C14CR_A    | 32-bit      | Base + 0x04E0          |             |
| eTPU A channel 14 status and control register   | ETPU_C14SCR_A   | 32-bit      | Base + 0x04E4          |             |
| eTPU A channel 14 host service request register | ETPU_C14HSRR_A  | 32-bit      | Base + 0x04E8          |             |
| Reserved                                        | -               | -           | Base + (0x04EC-0x04EF) |             |
| eTPU A channel 15 configuration register        | ETPU_C15CR_A    | 32-bit      | Base + 0x04F0          |             |
| eTPU A channel 15 status and control register   | ETPU_C15SCR_A   | 32-bit      | Base + 0x04F4          |             |
| eTPU A channel 15 host service request register | ETPU_C15HSRR_A  | 32-bit      | Base + 0x04F8          |             |
| Reserved                                        | -               | -           | Base + (0x04FC-0x04FF) |             |
| eTPU A channel 16 configuration register        | ETPU_C16CR_A    | 32-bit      | Base + 0x0500          |             |
| eTPU A channel 16 status and control register   | ETPU_C16SCR_A   | 32-bit      | Base + 0x0504          |             |
| eTPU A channel 16 host service request register | ETPU_C16HSRR_A  | 32-bit      | Base + 0x0508          |             |
| Reserved                                        | -               | -           | Base + (0x050C-0x050F) |             |
| eTPU A channel 17 configuration register        | ETPU_C17CR_A    | 32-bit      | Base + 0x0510          |             |
| eTPU A channel 17 status and control register   | ETPU_C17SCR_A   | 32-bit      | Base + 0x0514          |             |
| eTPU A channel 17 host service request register | ETPU_C17HSRR_A  | 32-bit      | Base + 0x0518          |             |
| Reserved                                        | -               | -           | Base + (0x051C-0x051F) |             |
| eTPU A channel 18 configuration register        | ETPU_C18CR_A    | 32-bit      | Base + 0x0520          |             |
| eTPU A channel 18 status and control register   | ETPU_C18SCR_A   | 32-bit      | Base + 0x0524          |             |
| eTPU A channel 18 host service request register | ETPU_C18HSRR_A  | 32-bit      | Base + 0x0528          |             |
| Reserved                                        | -               | -           | Base + (0x052C-0x052F) |             |
| eTPU A channel 19 configuration register        | ETPU_C19CR_A    | 32-bit      | Base + 0x0530          |             |
| eTPU A channel 19 status and control register   | ETPU_C19SCR_A   | 32-bit      | Base + 0x0534          |             |
| eTPU A channel 19 host service request register | ETPU_C19HSRR_A  | 32-bit      | Base + 0x0538          |             |
| Reserved                                        | -               | -           | Base + (0x053C-0x053F) |             |
| eTPU A channel 20 configuration register        | ETPU_C20CR_A    | 32-bit      | Base + 0x0540          |             |
| eTPU A channel 20 status and control register   | ETPU_C20SCR_A   | 32-bit      | Base + 0x0544          |             |
| eTPU A channel 20 host service request register | ETPU_C20HSRR_A  | 32-bit      | Base + 0x0548          |             |

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description                            | Register Name   | Used Size   | Address                | Reference   |
|-------------------------------------------------|-----------------|-------------|------------------------|-------------|
| Reserved                                        | -               | -           | Base + (0x054C-0x054F) |             |
| eTPU A channel 21 configuration register        | ETPU_C21CR_A    | 32-bit      | Base + 0x0550          |             |
| eTPU A channel 21 status and control register   | ETPU_C21SCR_A   | 32-bit      | Base + 0x0554          |             |
| eTPU A channel 21 host service request register | ETPU_C21HSRR_A  | 32-bit      | Base + 0x0558          |             |
| Reserved                                        | -               | -           | Base + (0x055C-0x055F) |             |
| eTPU A channel 22 configuration register        | ETPU_C22CR_A    | 32-bit      | Base + 0x0560          |             |
| eTPU A channel 22 status and control register   | ETPU_C22SCR_A   | 32-bit      | Base + 0x0564          |             |
| eTPU A channel 22 host service request register | ETPU_C22HSRR_A  | 32-bit      | Base + 0x0568          |             |
| Reserved                                        | -               | -           | Base + (0x056C-0x056F) |             |
| eTPU A channel 23 configuration register        | ETPU_C23CR_A    | 32-bit      | Base + 0x0570          |             |
| eTPU A channel 23 status and control register   | ETPU_C23CR_A    | 32-bit      | Base + 0x0574          |             |
| eTPU A channel 23 host service request register | ETPU_C23HSRR_A  | 32-bit      | Base + 0x0578          |             |
| Reserved                                        | -               | -           | Base + (0x057C-0x057F) |             |
| eTPU A channel 24 configuration register        | ETPU_C24CR_A    | 32-bit      | Base + 0x0580          |             |
| eTPU A channel 24 status and control register   | ETPU_C24SCR_A   | 32-bit      | Base + 0x0584          |             |
| eTPU A channel 24 host service request register | ETPU_C24HSRR_A  | 32-bit      | Base + 0x0588          |             |
| Reserved                                        | -               | -           | Base + (0x058C-0x058F) |             |
| eTPU A channel 25 configuration register        | ETPU_C25CR_A    | 32-bit      | Base + 0x0590          |             |
| eTPU A channel 25 status and control register   | ETPU_C25SCR_A   | 32-bit      | Base + 0x0594          |             |
| eTPU A channel 25 host service request register | ETPU_C25HSRR_A  | 32-bit      | Base + 0x0598          |             |
| Reserved                                        | -               | -           | Base + (0x059C-0x059F) |             |
| eTPU A channel 26 configuration register        | ETPU_C26CR_A    | 32-bit      | Base + 0x05A0          |             |
| eTPU A channel 26 status and control register   | ETPU_C26SCR_A   | 32-bit      | Base + 0x05A4          |             |
| eTPU A channel 26 host service request register | ETPU_C26HSRR_A  | 32-bit      | Base + 0x05A8          |             |
| Reserved                                        | -               | -           | Base + (0x05AC-0x05AF) |             |
| eTPU A channel 27 configuration register        | ETPU_C27CR_A    | 32-bit      | Base + 0x05B0          |             |
| eTPU A channel 27 status and control register   | ETPU_C27SCR_A   | 32-bit      | Base + 0x05B4          |             |
| eTPU A channel 27 host service request register | ETPU_C27HSRR_A  | 32-bit      | Base + 0x05B8          |             |
| Reserved                                        | -               | -           | Base + (0x05BC-0x05BF) |             |
| eTPU A channel 28 configuration register        | ETPU_C28CR_A    | 32-bit      | Base + 0x05C0          |             |
| eTPU A channel 28 status and control register   | ETPU_C28SCR_A   | 32-bit      | Base + 0x05C4          |             |
| eTPU A channel 28 host service request register | ETPU_C28HSRR_A  | 32-bit      | Base + 0x05C8          |             |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description                             | Register Name   | Used Size   | Address                | Reference   |
|--------------------------------------------------|-----------------|-------------|------------------------|-------------|
| Reserved                                         | -               | -           | Base + (0x05CC-0x05CF) |             |
| eTPU A channel 29 configuration register         | ETPU_C29CR_A    | 32-bit      | Base + 0x05D0          |             |
| eTPU A channel 29 status and control register    | ETPU_C29SCR_A   | 32-bit      | Base + 0x05D4          |             |
| eTPU A channel 29 host service request register  | ETPU_C29HSRR_A  | 32-bit      | Base + 0x05D8          |             |
| Reserved                                         | -               | -           | Base + (0x05DC-0x05DF) |             |
| eTPU A channel 30 configuration register         | ETPU_C30CR_A    | 32-bit      | Base + 0x05E0          |             |
| eTPU A channel 30 status and control register    | ETPU_C30SCR_A   | 32-bit      | Base + 0x05E4          |             |
| eTPU A channel 30 host service request register  | ETPU_C30HSRR_A  | 32-bit      | Base + 0x05E8          |             |
| Reserved                                         | -               | -           | Base + (0x05EC-0x05EF) |             |
| eTPU A channel 31 configuration register         | ETPU_C31CR_A    | 32-bit      | Base + 0x05F0          |             |
| eTPU A channel 31 status and control register    | ETPU_C31SCR_A   | 32-bit      | Base + 0x05F4          |             |
| eTPU A channel 31 host service request register  | ETPU_C31HSRR_A  | 32-bit      | Base + 0x05F8          |             |
| Reserved                                         | -               | -           | Base + (0x05FC-0x07FF) |             |
| eTPU B channel 0 configuration register 2        | ETPU_C0CR_B 2   | 32-bit      | Base + 0x0800          |             |
| eTPU B channel 0 status and control register 2   | ETPU_C0SCR_B 2  | 32-bit      | Base + 0x0804          |             |
| eTPU B channel 0 host service request register 2 | ETPU_C0HSRR_B 2 | 32-bit      | Base + 0x0808          |             |
| Reserved                                         | -               | -           | Base + (0x080C-0x080F) |             |
| eTPU B channel 1 configuration register 2        | ETPU_C1CR_B 2   | 32-bit      | Base + 0x0810          |             |
| eTPU B channel 1 status and control register 2   | ETPU_C1SCR_B 2  | 32-bit      | Base + 0x0814          |             |
| eTPU B channel 1 host service request register 2 | ETPU_C1HSRR_B 2 | 32-bit      | Base + 0x0818          |             |
| Reserved                                         | -               | -           | Base + (0x081C-0x081F) |             |
| eTPU B channel 2 configuration register 2        | ETPU_C2CR_B 2   | 32-bit      | Base + 0x0820          |             |
| eTPU B channel 2 status and control register 2   | ETPU_C2SCR_B 2  | 32-bit      | Base + 0x0824          |             |
| eTPU B channel 2 host service request register 2 | ETPU_C2HSRR_B 2 | 32-bit      | Base + 0x0828          |             |
| Reserved                                         | -               | -           | Base + (0x082C-0x082F) |             |
| eTPU B channel 3 configuration register 2        | ETPU_C3CR_B 2   | 32-bit      | Base + 0x0830          |             |
| eTPU B channel 3 status and control register 2   | ETPU_C3SCR_B 2  | 32-bit      | Base + 0x0834          |             |
| eTPU B channel 3 host service request register 2 | ETPU_C3HSRR_B 2 | 32-bit      | Base + 0x0838          |             |
| Reserved                                         | -               | -           | Base + (0x083C-0x083F) |             |
| eTPU B channel 4 configuration register 2        | ETPU_C4CR_B 2   | 32-bit      | Base + 0x0840          |             |
| eTPU B channel 4 status and control register 2   | ETPU_C4SCR_B 2  | 32-bit      | Base + 0x0844          |             |
| eTPU B channel 4 host service request register 2 | ETPU_C4HSRR_B 2 | 32-bit      | Base + 0x0848          |             |

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description                              | Register Name    | Used Size   | Address                | Reference   |
|---------------------------------------------------|------------------|-------------|------------------------|-------------|
| Reserved                                          | -                | -           | Base + (0x084C-0x084F) |             |
| eTPU B channel 5 configuration register 2         | ETPU_C5CR_B 2    | 32-bit      | Base + 0x0850          |             |
| eTPU B channel 5 status and control register 2    | ETPU_C5SCR_B 2   | 32-bit      | Base + 0x0854          |             |
| eTPU B channel 5 host service request register 2  | ETPU_C5HSRR_B 2  | 32-bit      | Base + 0x0858          |             |
| Reserved                                          | -                | -           | Base + (0x085C-0x085F) |             |
| eTPU B channel 6 configuration register 2         | ETPU_C6CR_B 2    | 32-bit      | Base + 0x0860          |             |
| eTPU B channel 6 status and control register 2    | ETPU_C6SCR_B 2   | 32-bit      | Base + 0x0864          |             |
| eTPU B channel 6 host service request register 2  | ETPU_C6HSRR_B 2  | 32-bit      | Base + 0x0868          |             |
| Reserved                                          | -                | -           | Base + (0x086C-0x086F) |             |
| eTPU B channel 7 configuration register 2         | ETPU_C7CR_B 2    | 32-bit      | Base + 0x0870          |             |
| eTPU B channel 7 status and control register 2    | ETPU_C7SCR_B 2   | 32-bit      | Base + 0x0874          |             |
| eTPU B channel 7 host service request register 2  | ETPU_C7HSRR_B 2  | 32-bit      | Base + 0x0878          |             |
| Reserved                                          | -                | -           | Base + (0x087C-0x087F) |             |
| eTPU B channel 8 configuration register 2         | ETPU_C8CR_B 2    | 32-bit      | Base + 0x0880          |             |
| eTPU B channel 8 status and control register 2    | ETPU_C8SCR_B 2   | 32-bit      | Base + 0x0884          |             |
| eTPU B channel 8 host service request register 2  | ETPU_C8HSRR_B 2  | 32-bit      | Base + 0x0888          |             |
| Reserved                                          | -                | -           | Base + (0x088C-0088F)  |             |
| eTPU B channel 9 configuration register 2         | ETPU_C9CR_B 2    | 32-bit      | Base + 0x0890          |             |
| eTPU B channel 9 status and control register 2    | ETPU_C9SCR_B 2   | 32-bit      | Base + 0x0894          |             |
| eTPU B channel 9 host service request register 2  | ETPU_C9HSRR_B 2  | 32-bit      | Base + 0x0898          |             |
| Reserved                                          | -                | -           | Base + (0x081C-0x081F) |             |
| eTPU B channel 10 configuration register 2        | ETPU_C10CR_B 2   | 32-bit      | Base + 0x08A0          |             |
| eTPU B channel 10 status and control register 2   | ETPU_C10SCR_B 2  | 32-bit      | Base + 0x08A4          |             |
| eTPU B channel 10 host service request register 2 | ETPU_C10HSRR_B 2 | 32-bit      | Base + 0x08A8          |             |
| Reserved                                          | -                | -           | Base + (0x08AC-0x08AF) |             |
| eTPU B channel 11 configuration register 2        | ETPU_C11CR_B 2   | 32-bit      | Base + 0x08B0          |             |
| eTPU B channel 11 status and control register 2   | ETPU_C11SCR_B 2  | 32-bit      | Base + 0x08B4          |             |
| eTPU B channel 11 host service request register 2 | ETPU_C11HSRR_B 2 | 32-bit      | Base + 0x08B8          |             |
| Reserved                                          | -                | -           | Base + (0x08BC-0x08BF) |             |
| eTPU B channel 12 configuration register 2        | ETPU_C12CR_B 2   | 32-bit      | Base + 0x08C0          |             |
| eTPU B channel 12 status and control register 2   | ETPU_C12SCR_B 2  | 32-bit      | Base + 0x08C4          |             |
| eTPU B channel 12 host service request register 2 | ETPU_C12HSRR_B 2 | 32-bit      | Base + 0x08C8          |             |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description                              | Register Name    | Used Size   | Address                | Reference   |
|---------------------------------------------------|------------------|-------------|------------------------|-------------|
| Reserved                                          | -                | -           | Base + (0x08CC-0x08CF) |             |
| eTPU B channel 13 configuration register 2        | ETPU_C13CR_B 2   | 32-bit      | Base + 0x08D0          |             |
| eTPU B channel 13 status and control register 2   | ETPU_C13SCR_B 2  | 32-bit      | Base + 0x08D4          |             |
| eTPU B channel 13 host service request register 2 | ETPU_C13HSRR_B 2 | 32-bit      | Base + 0x08D8          |             |
| Reserved                                          | -                | -           | Base + (0x08DC-0x08DF) |             |
| eTPU B channel 14 configuration register 2        | ETPU_C14CR_B 2   | 32-bit      | Base + 0x08E0          |             |
| eTPU B channel 14 status and control register 2   | ETPU_C14SCR_B 2  | 32-bit      | Base + 0x08E4          |             |
| eTPU B channel 14 host service request register 2 | ETPU_C14HSRR_B 2 | 32-bit      | Base + 0x08E8          |             |
| Reserved                                          | -                | -           | Base + (0x08EC-0x08EF) |             |
| eTPU B channel 15 configuration register 2        | ETPU_C15CR_B 2   | 32-bit      | Base + 0x08F0          |             |
| eTPU B channel 15 status and control register 2   | ETPU_C15SCR_B 2  | 32-bit      | Base + 0x08F4          |             |
| eTPU B channel 15 host service request register 2 | ETPU_C15HSRR_B 2 | 32-bit      | Base + 0x08F8          |             |
| Reserved                                          | -                | -           | Base + (0x08FC-0x08FF) |             |
| eTPU B channel 16 configuration register 2        | ETPU_C16CR_B 2   | 32-bit      | Base + 0x0900          |             |
| eTPU B channel 16 status and control register 2   | ETPU_C16SCR_B 2  | 32-bit      | Base + 0x0904          |             |
| eTPU B channel 16 host service request register 2 | ETPU_C16HSRR_B 2 | 32-bit      | Base + 0x0908          |             |
| Reserved                                          | -                | -           | Base + (0x090C-0x090F) |             |
| eTPU B channel 17 configuration register 2        | ETPU_C17CR_B 2   | 32-bit      | Base + 0x0910          |             |
| eTPU B channel 17 status and control register 2   | ETPU_C17SCR_B 2  | 32-bit      | Base + 0x0914          |             |
| eTPU B channel 17 host service request register 2 | ETPU_C17HSRR_B 2 | 32-bit      | Base + 0x0918          |             |
| Reserved                                          | -                | -           | Base + (0x091C-0x091F) |             |
| eTPU B channel 18 configuration register 2        | ETPU_C18CR_B 2   | 32-bit      | Base + 0x0920          |             |
| eTPU B channel 18 status and control register 2   | ETPU_C18SCR_B 2  | 32-bit      | Base + 0x0924          |             |
| eTPU B channel 18 host service request register 2 | ETPU_C18HSRR_B 2 | 32-bit      | Base + 0x0928          |             |
| Reserved                                          | -                | -           | Base + (0x092C-0x092F) |             |
| eTPU B channel 19 configuration register 2        | ETPU_C19CR_B 2   | 32-bit      | Base + 0x0930          |             |
| eTPU B channel 19 status and control register 2   | ETPU_C19SCR_B 2  | 32-bit      | Base + 0x0934          |             |
| eTPU B channel 19 host service request register 2 | ETPU_C19HSRR_B 2 | 32-bit      | Base + 0x0938          |             |
| Reserved                                          | -                | -           | Base + (0x093C-0x093F) |             |
| eTPU B channel 20 configuration register 2        | ETPU_C20CR_B 2   | 32-bit      | Base + 0x0940          |             |
| eTPU B channel 20 status and control register 2   | ETPU_C20SCR_B 2  | 32-bit      | Base + 0x0944          |             |
| eTPU B channel 20 host service request register 2 | ETPU_C20HSRR_B 2 | 32-bit      | Base + 0x0948          |             |

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description                              | Register Name    | Used Size   | Address                | Reference   |
|---------------------------------------------------|------------------|-------------|------------------------|-------------|
| Reserved                                          | -                | -           | Base + (0x094C-0x094F) |             |
| eTPU B channel 21 configuration register 2        | ETPU_C21CR_B 2   | 32-bit      | Base + 0x0950          |             |
| eTPU B channel 21 status and control register 2   | ETPU_C21SCR_B 2  | 32-bit      | Base + 0x0954          |             |
| eTPU B channel 21 host service request register 2 | ETPU_C21HSRR_B 2 | 32-bit      | Base + 0x0958          |             |
| Reserved                                          | -                | -           | Base + (0x095C-0x095F) |             |
| eTPU B channel 22 configuration register 2        | ETPU_C22CR_B 2   | 32-bit      | Base + 0x0960          |             |
| eTPU B channel 22 status and control register 2   | ETPU_C22SCR_B 2  | 32-bit      | Base + 0x0964          |             |
| eTPU B channel 22 host service request register 2 | ETPU_C22HSRR_B 2 | 32-bit      | Base + 0x0968          |             |
| Reserved                                          | -                | -           | Base + (0x096C-0x096F) |             |
| eTPU B channel 23 configuration register 2        | ETPU_C23CR_B 2   | 32-bit      | Base + 0x0970          |             |
| eTPU B channel 23 status and control register 2   | ETPU_C23SCR_B 2  | 32-bit      | Base + 0x0974          |             |
| eTPU B channel 23 host service request register 2 | ETPU_C23HSRR_B 2 | 32-bit      | Base + 0x0978          |             |
| Reserved                                          | -                | -           | Base + (0x097C-0x097F) |             |
| eTPU B channel 24 configuration register 2        | ETPU_C24CR_B 2   | 32-bit      | Base + 0x0980          |             |
| eTPU B channel 24 status and control register 2   | ETPU_C24SCR_B 2  | 32-bit      | Base + 0x0984          |             |
| eTPU B channel 24 host service request register 2 | ETPU_C24HSRR_B 2 | 32-bit      | Base + 0x0988          |             |
| Reserved                                          | -                | -           | Base + (0x098C-0x098F) |             |
| eTPU B channel 25 configuration register 2        | ETPU_C25CR_B 2   | 32-bit      | Base + 0x0990          |             |
| eTPU B channel 25 status and control register 2   | ETPU_C25SCR_B 2  | 32-bit      | Base + 0x0994          |             |
| eTPU B channel 25 host service request register 2 | ETPU_C25HSRR_B 2 | 32-bit      | Base + 0x0998          |             |
| Reserved                                          | -                | -           | Base + (0x099C-0x099F) |             |
| eTPU B channel 26 configuration register 2        | ETPU_C26CR_B 2   | 32-bit      | Base + 0x09A0          |             |
| eTPU B channel 26 status and control register 2   | ETPU_C26SCR_B 2  | 32-bit      | Base + 0x09A4          |             |
| eTPU B channel 26 host service request register 2 | ETPU_C26HSRR_B 2 | 32-bit      | Base + 0x09A8          |             |
| Reserved                                          | -                | -           | Base + (0x09AC-0x09AF) |             |
| eTPU B channel 27 configuration register 2        | ETPU_C27CR_B 2   | 32-bit      | Base + 0x09B0          |             |
| eTPU B channel 27 status and control register 2   | ETPU_C27SCR_B 2  | 32-bit      | Base + 0x09B4          |             |
| eTPU B channel 27 host service request register 2 | ETPU_C27HSRR_B 2 | 32-bit      | Base + 0x09B8          |             |
| Reserved                                          | -                | -           | Base + (0x09BC-0x09BF) |             |
| eTPU B channel 28 configuration register 2        | ETPU_C28CR_B 2   | 32-bit      | Base + 0x09C0          |             |
| eTPU B channel 28 status and control register 2   | ETPU_C28SCR_B 2  | 32-bit      | Base + 0x09C4          |             |
| eTPU B channel 28 host service request register 2 | ETPU_C28HSRR_B 2 | 32-bit      | Base + 0x09C8          |             |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description                                     | Register Name                  | Used Size                     | Address                                                          | Reference                                            |
|----------------------------------------------------------|--------------------------------|-------------------------------|------------------------------------------------------------------|------------------------------------------------------|
| Reserved                                                 | -                              | -                             | Base + (0x09CC-0x09CF)                                           |                                                      |
| eTPU B channel 29 configuration register 2               | ETPU_C29CR_B 2                 | 32-bit                        | Base + 0x09D0                                                    |                                                      |
| eTPU B channel 29 status and control register 2          | ETPU_C29SCR_B 2                | 32-bit                        | Base + 0x09D4                                                    |                                                      |
| eTPU B channel 29 host service request register 2        | ETPU_C29HSRR_B 2               | 32-bit                        | Base + 0x09D8                                                    |                                                      |
| Reserved                                                 | -                              | -                             | Base + (0x09DC-0x09DF)                                           |                                                      |
| eTPU B channel 30 configuration register 2               | ETPU_C30CR_B 2                 | 32-bit                        | Base + 0x09E0                                                    |                                                      |
| eTPU B channel 30 status and control register 2          | ETPU_C30SCR_B 2                | 32-bit                        | Base + 0x09E4                                                    |                                                      |
| eTPU B channel 30 host service request register 2        | ETPU_C30HSRR_B 2               | 32-bit                        | Base + 0x09E8                                                    |                                                      |
| Reserved                                                 | -                              | -                             | Base + (0x09EC-0x09EF)                                           |                                                      |
| eTPU B channel 31 configuration register 2               | ETPU_C31CR_B 2                 | 32-bit                        | Base + 0x09F0                                                    |                                                      |
| eTPU B channel 31 status and control register 2          | ETPU_C31SCR_B 2                | 32-bit                        | Base + 0x09F4                                                    |                                                      |
| eTPU B channel 31 host service request register 2        | ETPU_C31HSRR_B 2               | 32-bit                        | Base + 0x09F8                                                    |                                                      |
| Reserved                                                 | -                              | -                             | Base + (0x09FC-0x7FFF)                                           |                                                      |
| Shared data memory (parameter RAM)                       | SDM                            | 3Kbyte                        | Base + (0x8000-0x8BFF)                                           |                                                      |
| Reserved                                                 | -                              | -                             | Base + (0x8C00-0xBFFF)                                           |                                                      |
| SDM PSE mirror                                           |                                |                               | Base + (0xC000-0xCBFF)                                           |                                                      |
| Reserved                                                 | -                              | -                             | Base + (0xCC00-0xFFFF)                                           |                                                      |
| Shared code memory                                       | SCM                            | 16Kbyte (5554) 12Kbyte (5553) | Base + (0x1_0000-1_3FFF) (MPC5554) + (0x1_0000-1_2FFF) (MPC5553) |                                                      |
| Reserved                                                 | -                              | -                             | Base + (0x1_4000- FFEF_FFFF)                                     |                                                      |
| Peripheral Bridge B (PBRIDGEB)                           | Peripheral Bridge B (PBRIDGEB) |                               | 0xFFF0_0000                                                      | Chapter 5, 'PeripheralBridge (PBRIDGE_A, PBRIDGE_B)' |
| Peripheral bridge B master privilege control register    | PBRIDGEB_MPCR                  | 32-bit                        | Base + 0x0000                                                    |                                                      |
| Reserved                                                 | -                              | -                             | Base + (0x0004-0x001F)                                           |                                                      |
| Peripheral bridge B peripheral access control register 0 | PBRIDGEB_PACR0                 | 32-bit                        | Base + 0x0020                                                    |                                                      |
| Reserved                                                 | -                              | -                             | Base + (0x0024-0x0027)                                           |                                                      |
| Peripheral bridge B peripheral access control register 2 | PBRIDGEB_PACR2                 | 32-bit                        | Base + 0x0028                                                    |                                                      |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description                                                  | Register Name                     | Used Size   | Address                       | Reference                           |
|-----------------------------------------------------------------------|-----------------------------------|-------------|-------------------------------|-------------------------------------|
| Reserved                                                              | -                                 | -           | Base + (0x002C-0x003F)        |                                     |
| Peripheral bridge B off-platform peripheral access control register 0 | PBRIDGEB_OPACR0                   | 32-bit      | Base + 0x0040                 |                                     |
| Peripheral bridge B off-platform peripheral access control register 1 | PBRIDGEB_OPACR1                   | 32-bit      | Base + 0x0044                 |                                     |
| Peripheral bridge B off-platform peripheral access control register 2 | PBRIDGEB_OPACR2                   | 32-bit      | Base + 0x0048                 |                                     |
| Peripheral bridge B off-platform peripheral access control register 3 | PBRIDGEB_OPACR3                   | 32-bit      | Base + 0x004C                 |                                     |
| Reserved                                                              | -                                 | -           | (Base + 0x0050)- 0xFFF0_3FFF) |                                     |
| System Bus Crossbar Switch (XBAR)                                     | System Bus Crossbar Switch (XBAR) |             | 0xFFF0_4000                   | Chapter 7, 'Crossbar Switch (XBAR)' |
| Master priority register 0                                            | XBAR_MPR0                         | 32-bit      | Base + 0x0000                 |                                     |
| Reserved                                                              | -                                 | -           | Base + (0x0004-0x000F)        |                                     |
| Slave general purpose control register 0                              | XBAR_SGPCR0                       | 32-bit      | Base + 0x0010                 |                                     |
| Reserved                                                              | -                                 | -           | Base + (0x0014-0x00FF)        |                                     |
| Master priority register 1                                            | XBAR_MPR1                         | 32-bit      | Base + 0x0100                 |                                     |
| Reserved                                                              | -                                 | -           | Base + (0x0104-0x010F)        |                                     |
| Slave general purpose control register 1                              | XBAR_SGPCR1                       | 32-bit      | Base + 0x0110                 |                                     |
| Reserved                                                              | -                                 | -           | Base + (0x0114-0x02FF)        |                                     |
| Master priority register 3                                            | XBAR_MPR3                         | 32-bit      | Base + 0x0300                 |                                     |
| Reserved                                                              | -                                 | -           | Base + (0x0304-0x030F)        |                                     |
| Slave general purpose control register 3                              | XBAR_SGPCR3                       | 32-bit      | Base + 0x0310                 |                                     |
| Reserved                                                              | -                                 | -           | Base + (0x0314-0x05FF)        |                                     |
| Master priority register 6                                            | XBAR_MPR6                         | 32-bit      | Base + 0x0600                 |                                     |
| Reserved                                                              | -                                 | -           | Base + (0x0604-0x060F)        |                                     |
| Slave general purpose control register 6                              | XBAR_SGPCR6                       | 32-bit      | Base + 0x0610                 |                                     |
| Reserved                                                              | -                                 | -           | Base + (0x0614-0x06FF)        |                                     |
| Master priority register 7                                            | XBAR_MPR7                         | 32-bit      | Base + 0x0700                 |                                     |
| Reserved                                                              | -                                 | -           | Base + (0x0704-0x070F)        |                                     |
| Slave general purpose control register 7                              | XBAR_SGPCR7                       | 32-bit      | Base + 0x0710                 |                                     |
| Reserved                                                              | -                                 | -           | (Base + 0x0714)- 0xFFF4_3FFF) |                                     |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description                           | Register Name                         | Used Size   | Address                      | Reference   |
|------------------------------------------------|---------------------------------------|-------------|------------------------------|-------------|
| Error Correction Status Module (ECSM)          | Error Correction Status Module (ECSM) |             | 0xFFF4_0000                  |             |
| Reserved                                       | -                                     | -           | Base + (0x0000-0x0015)       |             |
| Software watchdog timer control register       | ECSM_SWTCR 1                          | 16-bit      | Base + 0x0016                |             |
| Reserved                                       | -                                     | -           | Base + (0x0018-0x001A)       |             |
| Software watchdog timer service register       | ECSM_SWTSR 1                          | 8-bit       | Base + 0x001B                |             |
| Reserved                                       | -                                     | -           | Base + (0x001C-0x001E)       |             |
| Software watchdog timer interrupt register     | ECSM_SWTIR 1                          | 8-bit       | Base + 0x001F                |             |
| Reserved                                       | -                                     |             | Base + (0x0020-0x0023)       |             |
| FEC Burst Optimization Master Control register | FBOMCR                                | 32-bit      | Base + 0x0024                |             |
| Reserved                                       | -                                     | -           | Base + (0x0028-0x0042)       |             |
| ECC configuration register                     | ECSM_ECR                              | 8-bit       | Base + 0x0043                |             |
| Reserved                                       | -                                     | -           | Base + (0x0044-0x0046)       |             |
| ECC status register                            | ECSM_ESR                              | 8-bit       | Base + 0x0047                |             |
| Reserved                                       | -                                     | -           | Base + (0x0048-0x0049)       |             |
| ECC error generation register                  | ECSM_EEGR                             | 16-bit      | Base + 0x004A                |             |
| Reserved                                       | -                                     | -           | Base + (0x004C-0x004F)       |             |
| Flash ECC address register                     | ECSM_FEAR                             | 32-bit      | Base + 0x0050                |             |
| Reserved                                       | -                                     | -           | Base + (0x0054-0x0055)       |             |
| Flash ECC master number register               | ECSM_FEMR                             | 8-bit       | Base + 0x0056                |             |
| Flash ECC attributes register                  | ECSM_FEAT                             | 8-bit       | Base + 0x0057                |             |
| Flash ECC data register high                   | ECSM_FEDRH                            | 32-bit      | Base + 0x0058                |             |
| Flash ECC data register low                    | ECSM_FEDRL                            | 32-bit      | Base + 0x005C                |             |
| RAM ECC address register                       | ECSM_REAR                             | 32-bit      | Base + 0x0060                |             |
| Reserved                                       | -                                     | -           | Base + (0x0064-0x0065)       |             |
| RAM ECC master number register                 | ECSM_REMR                             | 8-bit       | Base + 0x0066                |             |
| RAM ECC attributes register                    | ECSM_REAT                             | 8-bit       | Base + 0x0067                |             |
| RAM ECC data register high                     | ECSM_REDRH                            | 32-bit      | Base + 0x0068                |             |
| RAM ECC data register low                      | ECSM_REDRL                            | 32-bit      | Base + 0x006C                |             |
| Reserved                                       | -                                     | -           | (Base + 0x0070)- 0xFFF4_3FFF |             |

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description                                | Register Name                        | Used Size   | Address                | Reference                                         |
|-----------------------------------------------------|--------------------------------------|-------------|------------------------|---------------------------------------------------|
| Enhanced Direct Memory Access (eDMA)                | Enhanced Direct Memory Access (eDMA) |             | 0xFFF4_4000            | Chapter 9, 'Enhanced Direct Memory Access (eDMA)' |
| Control register                                    | EDMA_CR                              | 32-bit      | Base + 0x0000          |                                                   |
| Error status register                               | EDMA_ESR                             | 32-bit      | Base + 0x0004          |                                                   |
| Enable request register high (MPC5554 only)         | EDMA_ERQRH                           | 32-bit      | Base + 0x0008          |                                                   |
| Enable request register low                         | EDMA_ERQRL                           | 32-bit      | Base + 0x000C          |                                                   |
| Enable error interrupt register high (MPC5554 only) | EDMA_EEIRH                           | 32-bit      | Base + 0x0010          |                                                   |
| Enable error interrupt register low                 | EDMA_EEIRL                           | 32-bit      | Base + 0x0014          |                                                   |
| Set enable request register                         | EDMA_SERQR                           | 8-bit       | Base + 0x0018          |                                                   |
| Clear enable request register                       | EDMA_CERQR                           | 8-bit       | Base + 0x0019          |                                                   |
| Set enable error interrupt register                 | EDMA_SEEIR                           | 8-bit       | Base + 0x001A          |                                                   |
| Clear enable error interrupt request register       | EDMA_CEEIR                           | 8-bit       | Base + 0x001B          |                                                   |
| Clear interrupt request register                    | EDMA_CIRQR                           | 8-bit       | Base + 0x001C          |                                                   |
| Clear error register                                | EDMA_CER                             | 8-bit       | Base + 0x001D          |                                                   |
| Set START bit register                              | EDMA_SSBR                            | 8-bit       | Base + 0x001E          |                                                   |
| Clear DONE status bit register                      | EDMA_CDSBR                           | 8-bit       | Base + 0x001F          |                                                   |
| Interrupt request register high (MPC5554 only)      | EDMA_IRQRH                           | 32-bit      | Base + 0x0020          |                                                   |
| Interrupt request register low                      | EDMA_IRQRL                           | 32-bit      | Base + 0x0024          |                                                   |
| Error register high (MPC5554 only)                  | EDMA_ERH                             | 32-bit      | Base + 0x0028          |                                                   |
| Error register low                                  | EDMA_ERL                             | 32-bit      | Base + 0x002C          |                                                   |
| Reserved                                            | -                                    | -           | Base + (0x0030-0x00FF) |                                                   |
| Channel priority register 0                         | EDMA_CPR0                            | 8-bit       | Base + 0x0100          |                                                   |
| Channel priority register 1                         | EDMA_CPR1                            | 8-bit       | Base + 0x0101          |                                                   |
| Channel priority register 2                         | EDMA_CPR2                            | 8-bit       | Base + 0x0102          |                                                   |
| Channel priority register 3                         | EDMA_CPR3                            | 8-bit       | Base + 0x0103          |                                                   |
| Channel priority register 4                         | EDMA_CPR4                            | 8-bit       | Base + 0x0104          |                                                   |
| Channel priority register 5                         | EDMA_CPR5                            | 8-bit       | Base + 0x0105          |                                                   |
| Channel priority register 6                         | EDMA_CPR6                            | 8-bit       | Base + 0x0106          |                                                   |
| Channel priority register 7                         | EDMA_CPR7                            | 8-bit       | Base + 0x0107          |                                                   |
| Channel priority register 8                         | EDMA_CPR8                            | 8-bit       | Base + 0x0108          |                                                   |

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description         | Register Name   | Used Size   | Address       | Reference   |
|------------------------------|-----------------|-------------|---------------|-------------|
| Channel priority register 9  | EDMA_CPR9       | 8-bit       | Base + 0x0109 |             |
| Channel priority register 10 | EDMA_CPR10      | 8-bit       | Base + 0x010A |             |
| Channel priority register 11 | EDMA_CPR11      | 8-bit       | Base + 0x010B |             |
| Channel priority register 12 | EDMA_CPR12      | 8-bit       | Base + 0x010C |             |
| Channel priority register 13 | EDMA_CPR13      | 8-bit       | Base + 0x010D |             |
| Channel priority register 14 | EDMA_CPR14      | 8-bit       | Base + 0x010E |             |
| Channel priority register 15 | EDMA_CPR15      | 8-bit       | Base + 0x010F |             |
| Channel priority register 16 | EDMA_CPR16      | 8-bit       | Base + 0x0110 |             |
| Channel priority register 17 | EDMA_CPR17      | 8-bit       | Base + 0x0111 |             |
| Channel priority register 18 | EDMA_CPR18      | 8-bit       | Base + 0x0112 |             |
| Channel priority register 19 | EDMA_CPR19      | 8-bit       | Base + 0x0113 |             |
| Channel priority register 20 | EDMA_CPR20      | 8-bit       | Base + 0x0114 |             |
| Channel priority register 21 | EDMA_CPR21      | 8-bit       | Base + 0x0115 |             |
| Channel priority register 22 | EDMA_CPR22      | 8-bit       | Base + 0x0116 |             |
| Channel priority register 23 | EDMA_CPR23      | 8-bit       | Base + 0x0117 |             |
| Channel priority register 24 | EDMA_CPR24      | 8-bit       | Base + 0x0118 |             |
| Channel priority register 25 | EDMA_CPR25      | 8-bit       | Base + 0x0119 |             |
| Channel priority register 26 | EDMA_CPR26      | 8-bit       | Base + 0x011A |             |
| Channel priority register 27 | EDMA_CPR27      | 8-bit       | Base + 0x011B |             |
| Channel priority register 28 | EDMA_CPR28      | 8-bit       | Base + 0x011C |             |
| Channel priority register 29 | EDMA_CPR29      | 8-bit       | Base + 0x011D |             |
| Channel priority register 30 | EDMA_CPR30      | 8-bit       | Base + 0x011E |             |
| Channel priority register 31 | EDMA_CPR31      | 8-bit       | Base + 0x011F |             |
| Channel priority register 32 | EDMA_CPR32      | 8-bit       | Base + 0x0120 |             |
| Channel priority register 33 | EDMA_CPR33      | 8-bit       | Base + 0x0121 |             |
| Channel priority register 34 | EDMA_CPR34      | 8-bit       | Base + 0x0122 |             |
| Channel priority register 35 | EDMA_CPR35      | 8-bit       | Base + 0x0123 |             |
| Channel priority register 36 | EDMA_CPR36      | 8-bit       | Base + 0x0124 |             |
| Channel priority register 37 | EDMA_CPR37      | 8-bit       | Base + 0x0125 |             |
| Channel priority register 38 | EDMA_CPR38      | 8-bit       | Base + 0x0126 |             |
| Channel priority register 39 | EDMA_CPR39      | 8-bit       | Base + 0x0127 |             |
| Channel priority register 40 | EDMA_CPR40      | 8-bit       | Base + 0x0128 |             |

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description                   | Register Name   | Used Size   | Address                | Reference   |
|----------------------------------------|-----------------|-------------|------------------------|-------------|
| Channel priority register 41           | EDMA_CPR41      | 8-bit       | Base + 0x0129          |             |
| Channel priority register 42           | EDMA_CPR42      | 8-bit       | Base + 0x012A          |             |
| Channel priority register 43           | EDMA_CPR43      | 8-bit       | Base + 0x012B          |             |
| Channel priority register 44           | EDMA_CPR44      | 8-bit       | Base + 0x012C          |             |
| Channel priority register 45           | EDMA_CPR45      | 8-bit       | Base + 0x012D          |             |
| Channel priority register 46           | EDMA_CPR46      | 8-bit       | Base + 0x012E          |             |
| Channel priority register 47           | EDMA_CPR47      | 8-bit       | Base + 0x012F          |             |
| Channel priority register 48           | EDMA_CPR48      | 8-bit       | Base + 0x0130          |             |
| Channel priority register 49           | EDMA_CPR49      | 8-bit       | Base + 0x0131          |             |
| Channel priority register 50           | EDMA_CPR50      | 8-bit       | Base + 0x0132          |             |
| Channel priority register 51           | EDMA_CPR51      | 8-bit       | Base + 0x0133          |             |
| Channel priority register 52           | EDMA_CPR52      | 8-bit       | Base + 0x0134          |             |
| Channel priority register 53           | EDMA_CPR53      | 8-bit       | Base + 0x0135          |             |
| Channel priority register 54           | EDMA_CPR54      | 8-bit       | Base + 0x0136          |             |
| Channel priority register 55           | EDMA_CPR55      | 8-bit       | Base + 0x0137          |             |
| Channel priority register 56           | EDMA_CPR56      | 8-bit       | Base + 0x0138          |             |
| Channel priority register 57           | EDMA_CPR57      | 8-bit       | Base + 0x0139          |             |
| Channel priority register 58           | EDMA_CPR58      | 8-bit       | Base + 0x013A          |             |
| Channel priority register 59           | EDMA_CPR59      | 8-bit       | Base + 0x013B          |             |
| Channel priority register 60           | EDMA_CPR60      | 8-bit       | Base + 0x013C          |             |
| Channel priority register 61           | EDMA_CPR61      | 8-bit       | Base + 0x013D          |             |
| Channel priority register 62           | EDMA_CPR62      | 8-bit       | Base + 0x013E          |             |
| Channel priority register 63           | EDMA_CPR63      | 8-bit       | Base + 0x013F          |             |
| Reserved                               | -               | -           | Base + (0x0140-0x0FFF) |             |
| Transfer control descriptor register 0 | TCD0            | 256-bit     | Base + 0x1000          |             |
| Transfer control descriptor register 1 | TCD1            | 256-bit     | Base + 0x1020          |             |
| Transfer control descriptor register 2 | TCD2            | 256-bit     | Base + 0x1040          |             |
| Transfer control descriptor register 3 | TCD3            | 256-bit     | Base + 0x1060          |             |
| Transfer control descriptor register 4 | TCD4            | 256-bit     | Base + 0x1080          |             |
| Transfer control descriptor register 5 | TCD5            | 256-bit     | Base + 0x10A0          |             |
| Transfer control descriptor register 6 | TCD6            | 256-bit     | Base + 0x10C0          |             |
| Transfer control descriptor register 7 | TCD7            | 256-bit     | Base + 0x10E0          |             |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description                    | Register Name   | Used Size   | Address       | Reference   |
|-----------------------------------------|-----------------|-------------|---------------|-------------|
| Transfer control descriptor register 8  | TCD8            | 256-bit     | Base + 0x1100 |             |
| Transfer control descriptor register 9  | TCD9            | 256-bit     | Base + 0x1120 |             |
| Transfer control descriptor register 10 | TCD10           | 256-bit     | Base + 0x1140 |             |
| Transfer control descriptor register 11 | TCD11           | 256-bit     | Base + 0x1160 |             |
| Transfer control descriptor register 12 | TCD12           | 256-bit     | Base + 0x1180 |             |
| Transfer control descriptor register 13 | TCD13           | 256-bit     | Base + 0x11A0 |             |
| Transfer control descriptor register 14 | TCD14           | 256-bit     | Base + 0x11C0 |             |
| Transfer control descriptor register 15 | TCD15           | 256-bit     | Base + 0x11E0 |             |
| Transfer control descriptor register 16 | TCD16           | 256-bit     | Base + 0x1200 |             |
| Transfer control descriptor register 17 | TCD17           | 256-bit     | Base + 0x1220 |             |
| Transfer control descriptor register 18 | TCD18           | 256-bit     | Base + 0x1240 |             |
| Transfer control descriptor register 19 | TCD19           | 256-bit     | Base + 0x1260 |             |
| Transfer control descriptor register 20 | TCD20           | 256-bit     | Base + 0x1280 |             |
| Transfer control descriptor register 21 | TCD21           | 256-bit     | Base + 0x12A0 |             |
| Transfer control descriptor register 22 | TCD22           | 256-bit     | Base + 0x12C0 |             |
| Transfer control descriptor register 23 | TCD23           | 256-bit     | Base + 0x12E0 |             |
| Transfer control descriptor register 24 | TCD24           | 256-bit     | Base + 0x1300 |             |
| Transfer control descriptor register 25 | TCD25           | 256-bit     | Base + 0x1320 |             |
| Transfer control descriptor register 26 | TCD26           | 256-bit     | Base + 0x1340 |             |
| Transfer control descriptor register 27 | TCD27           | 256-bit     | Base + 0x1360 |             |
| Transfer control descriptor register 28 | TCD28           | 256-bit     | Base + 0x1380 |             |
| Transfer control descriptor register 29 | TCD29           | 256-bit     | Base + 0x13A0 |             |
| Transfer control descriptor register 30 | TCD30           | 256-bit     | Base + 0x13C0 |             |
| Transfer control descriptor register 31 | TCD31           | 256-bit     | Base + 0x13E0 |             |
| Transfer control descriptor register 32 | TCD32           | 256-bit     | Base + 0x1400 |             |
| Transfer control descriptor register 33 | TCD33           | 256-bit     | Base + 0x1420 |             |
| Transfer control descriptor register 34 | TCD34           | 256-bit     | Base + 0x1440 |             |
| Transfer control descriptor register 35 | TCD35           | 256-bit     | Base + 0x1460 |             |
| Transfer control descriptor register 36 | TCD36           | 256-bit     | Base + 0x1480 |             |
| Transfer control descriptor register 37 | TCD37           | 256-bit     | Base + 0x14A0 |             |
| Transfer control descriptor register 38 | TCD38           | 256-bit     | Base + 0x14C0 |             |
| Transfer control descriptor register 39 | TCD39           | 256-bit     | Base + 0x14E0 |             |

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description                    | Register Name               | Used Size   | Address                      | Reference                                 |
|-----------------------------------------|-----------------------------|-------------|------------------------------|-------------------------------------------|
| Transfer control descriptor register 40 | TCD40                       | 256-bit     | Base + 0x1500                |                                           |
| Transfer control descriptor register 41 | TCD41                       | 256-bit     | Base + 0x1520                |                                           |
| Transfer control descriptor register 42 | TCD42                       | 256-bit     | Base + 0x1540                |                                           |
| Transfer control descriptor register 43 | TCD43                       | 256-bit     | Base + 0x1560                |                                           |
| Transfer control descriptor register 44 | TCD44                       | 256-bit     | Base + 0x1580                |                                           |
| Transfer control descriptor register 45 | TCD45                       | 256-bit     | Base + 0x15A0                |                                           |
| Transfer control descriptor register 46 | TCD46                       | 256-bit     | Base + 0x15C0                |                                           |
| Transfer control descriptor register 47 | TCD47                       | 256-bit     | Base + 0x15E0                |                                           |
| Transfer control descriptor register 48 | TCD48                       | 256-bit     | Base + 0x1600                |                                           |
| Transfer control descriptor register 49 | TCD49                       | 256-bit     | Base + 0x1620                |                                           |
| Transfer control descriptor register 50 | TCD50                       | 256-bit     | Base + 0x1640                |                                           |
| Transfer control descriptor register 51 | TCD51                       | 256-bit     | Base + 0x1660                |                                           |
| Transfer control descriptor register 52 | TCD52                       | 256-bit     | Base + 0x1680                |                                           |
| Transfer control descriptor register 53 | TCD53                       | 256-bit     | Base + 0x16A0                |                                           |
| Transfer control descriptor register 54 | TCD54                       | 256-bit     | Base + 0x16C0                |                                           |
| Transfer control descriptor register 55 | TCD55                       | 256-bit     | Base + 0x16E0                |                                           |
| Transfer control descriptor register 56 | TCD56                       | 256-bit     | Base + 0x1700                |                                           |
| Transfer control descriptor register 57 | TCD57                       | 256-bit     | Base + 0x1720                |                                           |
| Transfer control descriptor register 58 | TCD58                       | 256-bit     | Base + 0x1740                |                                           |
| Transfer control descriptor register 59 | TCD59                       | 256-bit     | Base + 0x1760                |                                           |
| Transfer control descriptor register 60 | TCD60                       | 256-bit     | Base + 0x1780                |                                           |
| Transfer control descriptor register 61 | TCD61                       | 256-bit     | Base + 0x17A0                |                                           |
| Transfer control descriptor register 62 | TCD62                       | 256-bit     | Base + 0x17C0                |                                           |
| Transfer control descriptor register 63 | TCD63                       | 256-bit     | Base + 0x17E0                |                                           |
| Reserved                                | -                           | -           | (Base + 0x1800)- 0xFFF4_7FFF |                                           |
| Interrupt Controller (INTC)             | Interrupt Controller (INTC) |             | 0xFFF4_8000                  | Chapter 10, 'Interrupt Controller (INTC)' |
| Module configuration register           | INTC_MCR                    | 32-bit      | Base + 0x0000                |                                           |
| Reserved                                | -                           | -           | Base + (0x0004-0x0007)       |                                           |
| Current priority register               | INTC_CPR                    | 32-bit      | Base + 0x0008                |                                           |
| Reserved                                | -                           | -           | Base + (0x000C-0x000F)       |                                           |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description                    | Register Name   | Used Size   | Address                | Reference   |
|-----------------------------------------|-----------------|-------------|------------------------|-------------|
| interrupt acknowledge register          | INTC_IACKR      | 32-bit      | Base + 0x0010          |             |
| Reserved                                | -               | -           | Base + (0x0014-0x0017) |             |
| End of interrupt register               | INTC_EOIR       | 32-bit      | Base + 0x0018          |             |
| Reserved                                | -               | -           | Base + (0x001C-0x001F) |             |
| Software set/clear interrupt register 0 | INTC_SSCIR0     | 8-bit       | Base + 0x0020          |             |
| Software set/clear interrupt register 1 | INTC_SSCIR1     | 8-bit       | Base + 0x0021          |             |
| Software set/clear interrupt register 2 | INTC_SSCIR2     | 8-bit       | Base + 0x0022          |             |
| Software set/clear interrupt register 3 | INTC_SSCIR3     | 8-bit       | Base + 0x0023          |             |
| Software set/clear interrupt register 4 | INTC_SSCIR4     | 8-bit       | Base + 0x0024          |             |
| Software set/clear interrupt register 5 | INTC_SSCIR5     | 8-bit       | Base + 0x0025          |             |
| Software set/clear interrupt register 6 | INTC_SSCIR6     | 8-bit       | Base + 0x0026          |             |
| Software set/clear interrupt register 7 | INTC_SSCIR7     | 8-bit       | Base + 0x0027          |             |
| Reserved                                | -               | -           | Base + (0x0028-0x003F) |             |
| Priority select register 0              | INTC_PSR0       | 8-bit       | Base + 0x0040          |             |
| Priority select register 1              | INTC_PSR1       | 8-bit       | Base + 0x0041          |             |
| Priority select register 2              | INTC_PSR2       | 8-bit       | Base + 0x0042          |             |
| Priority select register 3              | INTC_PSR3       | 8-bit       | Base + 0x0043          |             |
| Priority select register 4              | INTC_PSR4       | 8-bit       | Base + 0x0044          |             |
| Priority select register 5              | INTC_PSR5       | 8-bit       | Base + 0x0045          |             |
| Priority select register 6              | INTC_PSR6       | 8-bit       | Base + 0x0046          |             |
| Priority select register 7              | INTC_PSR7       | 8-bit       | Base + 0x0047          |             |
| Priority select register 8              | INTC_PSR8       | 8-bit       | Base + 0x0048          |             |
| Priority select register 9              | INTC_PSR9       | 8-bit       | Base + 0x0049          |             |
| Priority select register 10             | INTC_PSR10      | 8-bit       | Base + 0x004A          |             |
| Priority select register 11             | INTC_PSR11      | 8-bit       | Base + 0x004B          |             |
| Priority select register 12             | INTC_PSR12      | 8-bit       | Base + 0x004C          |             |
| Priority select register 13             | INTC_PSR13      | 8-bit       | Base + 0x004D          |             |
| Priority select register 14             | INTC_PSR14      | 8-bit       | Base + 0x004E          |             |
| Priority select register 15             | INTC_PSR15      | 8-bit       | Base + 0x004F          |             |
| Priority select register 16             | INTC_PSR16      | 8-bit       | Base + 0x0050          |             |
| Priority select register 17             | INTC_PSR17      | 8-bit       | Base + 0x0051          |             |
| Priority select register 18             | INTC_PSR18      | 8-bit       | Base + 0x0052          |             |

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description        | Register Name   | Used Size   | Address       | Reference   |
|-----------------------------|-----------------|-------------|---------------|-------------|
| Priority select register 19 | INTC_PSR19      | 8-bit       | Base + 0x0053 |             |
| Priority select register 20 | INTC_PSR20      | 8-bit       | Base + 0x0054 |             |
| Priority select register 21 | INTC_PSR21      | 8-bit       | Base + 0x0055 |             |
| Priority select register 22 | INTC_PSR22      | 8-bit       | Base + 0x0056 |             |
| Priority select register 23 | INTC_PSR23      | 8-bit       | Base + 0x0057 |             |
| Priority select register 24 | INTC_PSR24      | 8-bit       | Base + 0x0058 |             |
| Priority select register 25 | INTC_PSR25      | 8-bit       | Base + 0x0059 |             |
| Priority select register 26 | INTC_PSR26      | 8-bit       | Base + 0x005A |             |
| Priority select register 27 | INTC_PSR27      | 8-bit       | Base + 0x005B |             |
| Priority select register 28 | INTC_PSR28      | 8-bit       | Base + 0x005C |             |
| Priority select register 29 | INTC_PSR29      | 8-bit       | Base + 0x005D |             |
| Priority select register 30 | INTC_PSR30      | 8-bit       | Base + 0x005E |             |
| Priority select register 31 | INTC_PSR31      | 8-bit       | Base + 0x005F |             |
| Priority select register 32 | INTC_PSR32      | 8-bit       | Base + 0x0060 |             |
| Priority select register 33 | INTC_PSR33      | 8-bit       | Base + 0x0061 |             |
| Priority select register 34 | INTC_PSR34      | 8-bit       | Base + 0x0062 |             |
| Priority select register 35 | INTC_PSR35      | 8-bit       | Base + 0x0063 |             |
| Priority select register 36 | INTC_PSR36      | 8-bit       | Base + 0x0064 |             |
| Priority select register 37 | INTC_PSR37      | 8-bit       | Base + 0x0065 |             |
| Priority select register 38 | INTC_PSR38      | 8-bit       | Base + 0x0066 |             |
| Priority select register 39 | INTC_PSR39      | 8-bit       | Base + 0x0067 |             |
| Priority select register 40 | INTC_PSR40      | 8-bit       | Base + 0x0068 |             |
| Priority select register 41 | INTC_PSR41      | 8-bit       | Base + 0x0069 |             |
| Priority select register 42 | INTC_PSR42      | 8-bit       | Base + 0x006A |             |
| Priority select register 43 | INTC_PSR43      | 8-bit       | Base + 0x006B |             |
| Priority select register 44 | INTC_PSR44      | 8-bit       | Base + 0x006C |             |
| Priority select register 45 | INTC_PSR45      | 8-bit       | Base + 0x006D |             |
| Priority select register 46 | INTC_PSR46      | 8-bit       | Base + 0x006E |             |
| Priority select register 47 | INTC_PSR47      | 8-bit       | Base + 0x006F |             |
| Priority select register 48 | INTC_PSR48      | 8-bit       | Base + 0x0070 |             |
| Priority select register 49 | INTC_PSR49      | 8-bit       | Base + 0x0071 |             |
| Priority select register 50 | INTC_PSR50      | 8-bit       | Base + 0x0072 |             |

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description        | Register Name   | Used Size   | Address       | Reference   |
|-----------------------------|-----------------|-------------|---------------|-------------|
| Priority select register 51 | INTC_PSR51      | 8-bit       | Base + 0x0073 |             |
| Priority select register 52 | INTC_PSR52      | 8-bit       | Base + 0x0074 |             |
| Priority select register 53 | INTC_PSR53      | 8-bit       | Base + 0x0075 |             |
| Priority select register 54 | INTC_PSR54      | 8-bit       | Base + 0x0076 |             |
| Priority select register 55 | INTC_PSR55      | 8-bit       | Base + 0x0077 |             |
| Priority select register 56 | INTC_PSR56      | 8-bit       | Base + 0x0078 |             |
| Priority select register 57 | INTC_PSR57      | 8-bit       | Base + 0x0079 |             |
| Priority select register 58 | INTC_PSR58      | 8-bit       | Base + 0x007A |             |
| Priority select register 59 | INTC_PSR59      | 8-bit       | Base + 0x007B |             |
| Priority select register 60 | INTC_PSR60      | 8-bit       | Base + 0x007C |             |
| Priority select register 61 | INTC_PSR61      | 8-bit       | Base + 0x007D |             |
| Priority select register 62 | INTC_PSR62      | 8-bit       | Base + 0x007E |             |
| Priority select register 63 | INTC_PSR63      | 8-bit       | Base + 0x007F |             |
| Priority select register 64 | INTC_PSR64      | 8-bit       | Base + 0x0080 |             |
| Priority select register 65 | INTC_PSR65      | 8-bit       | Base + 0x0081 |             |
| Priority select register 66 | INTC_PSR66      | 8-bit       | Base + 0x0082 |             |
| Priority select register 67 | INTC_PSR67      | 8-bit       | Base + 0x0083 |             |
| Priority select register 68 | INTC_PSR68      | 8-bit       | Base + 0x0084 |             |
| Priority select register 69 | INTC_PSR69      | 8-bit       | Base + 0x0085 |             |
| Priority select register 70 | INTC_PSR70      | 8-bit       | Base + 0x0086 |             |
| Priority select register 71 | INTC_PSR71      | 8-bit       | Base + 0x0087 |             |
| Priority select register 72 | INTC_PSR72      | 8-bit       | Base + 0x0088 |             |
| Priority select register 73 | INTC_PSR73      | 8-bit       | Base + 0x0089 |             |
| Priority select register 74 | INTC_PSR74      | 8-bit       | Base + 0x008A |             |
| Priority select register 75 | INTC_PSR75      | 8-bit       | Base + 0x008B |             |
| Priority select register 76 | INTC_PSR76      | 8-bit       | Base + 0x008C |             |
| Priority select register 77 | INTC_PSR77      | 8-bit       | Base + 0x008D |             |
| Priority select register 78 | INTC_PSR78      | 8-bit       | Base + 0x008E |             |
| Priority select register 79 | INTC_PSR79      | 8-bit       | Base + 0x008F |             |
| Priority select register 80 | INTC_PSR80      | 8-bit       | Base + 0x0090 |             |
| Priority select register 81 | INTC_PSR81      | 8-bit       | Base + 0x0091 |             |
| Priority select register 82 | INTC_PSR82      | 8-bit       | Base + 0x0092 |             |

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description         | Register Name   | Used Size   | Address       | Reference   |
|------------------------------|-----------------|-------------|---------------|-------------|
| Priority select register 83  | INTC_PSR83      | 8-bit       | Base + 0x0093 |             |
| Priority select register 84  | INTC_PSR84      | 8-bit       | Base + 0x0094 |             |
| Priority select register 85  | INTC_PSR85      | 8-bit       | Base + 0x0095 |             |
| Priority select register 86  | INTC_PSR86      | 8-bit       | Base + 0x0096 |             |
| Priority select register 87  | INTC_PSR87      | 8-bit       | Base + 0x0097 |             |
| Priority select register 88  | INTC_PSR88      | 8-bit       | Base + 0x0098 |             |
| Priority select register 89  | INTC_PSR89      | 8-bit       | Base + 0x0099 |             |
| Priority select register 90  | INTC_PSR90      | 8-bit       | Base + 0x009A |             |
| Priority select register 91  | INTC_PSR91      | 8-bit       | Base + 0x009B |             |
| Priority select register 92  | INTC_PSR92      | 8-bit       | Base + 0x009C |             |
| Priority select register 93  | INTC_PSR93      | 8-bit       | Base + 0x009D |             |
| Priority select register 94  | INTC_PSR94      | 8-bit       | Base + 0x009E |             |
| Priority select register 95  | INTC_PSR95      | 8-bit       | Base + 0x009F |             |
| Priority select register 96  | INTC_PSR96      | 8-bit       | Base + 0x00A0 |             |
| Priority select register 97  | INTC_PSR97      | 8-bit       | Base + 0x00A1 |             |
| Priority select register 98  | INTC_PSR98      | 8-bit       | Base + 0x00A2 |             |
| Priority select register 99  | INTC_PSR99      | 8-bit       | Base + 0x00A3 |             |
| Priority select register 100 | INTC_PSR100     | 8-bit       | Base + 0x00A4 |             |
| Priority select register 101 | INTC_PSR101     | 8-bit       | Base + 0x00A5 |             |
| Priority select register 102 | INTC_PSR102     | 8-bit       | Base + 0x00A6 |             |
| Priority select register 103 | INTC_PSR103     | 8-bit       | Base + 0x00A7 |             |
| Priority select register 104 | INTC_PSR104     | 8-bit       | Base + 0x00A8 |             |
| Priority select register 105 | INTC_PSR105     | 8-bit       | Base + 0x00A9 |             |
| Priority select register 106 | INTC_PSR106     | 8-bit       | Base + 0x00AA |             |
| Priority select register 107 | INTC_PSR107     | 8-bit       | Base + 0x00AB |             |
| Priority select register 108 | INTC_PSR108     | 8-bit       | Base + 0x00AC |             |
| Priority select register 109 | INTC_PSR109     | 8-bit       | Base + 0x00AD |             |
| Priority select register 110 | INTC_PSR110     | 8-bit       | Base + 0x00AE |             |
| Priority select register 111 | INTC_PSR111     | 8-bit       | Base + 0x00AF |             |
| Priority select register 112 | INTC_PSR112     | 8-bit       | Base + 0x00B0 |             |
| Priority select register 113 | INTC_PSR113     | 8-bit       | Base + 0x00B1 |             |
| Priority select register 114 | INTC_PSR114     | 8-bit       | Base + 0x00B2 |             |

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description         | Register Name   | Used Size   | Address       | Reference   |
|------------------------------|-----------------|-------------|---------------|-------------|
| Priority select register 115 | INTC_PSR115     | 8-bit       | Base + 0x00B3 |             |
| Priority select register 116 | INTC_PSR116     | 8-bit       | Base + 0x00B4 |             |
| Priority select register 117 | INTC_PSR117     | 8-bit       | Base + 0x00B5 |             |
| Priority select register 118 | INTC_PSR118     | 8-bit       | Base + 0x00B6 |             |
| Priority select register 119 | INTC_PSR119     | 8-bit       | Base + 0x00B7 |             |
| Priority select register 120 | INTC_PSR120     | 8-bit       | Base + 0x00B8 |             |
| Priority select register 121 | INTC_PSR121     | 8-bit       | Base + 0x00B9 |             |
| Priority select register 122 | INTC_PSR122     | 8-bit       | Base + 0x00BA |             |
| Priority select register 123 | INTC_PSR123     | 8-bit       | Base + 0x00BB |             |
| Priority select register 124 | INTC_PSR124     | 8-bit       | Base + 0x00BC |             |
| Priority select register 125 | INTC_PSR125     | 8-bit       | Base + 0x00BD |             |
| Priority select register 126 | INTC_PSR126     | 8-bit       | Base + 0x00BE |             |
| Priority select register 127 | INTC_PSR127     | 8-bit       | Base + 0x00BF |             |
| Priority select register 128 | INTC_PSR128     | 8-bit       | Base + 0x00C0 |             |
| Priority select register 129 | INTC_PSR129     | 8-bit       | Base + 0x00C1 |             |
| Priority select register 130 | INTC_PSR130     | 8-bit       | Base + 0x00C2 |             |
| Priority select register 131 | INTC_PSR131     | 8-bit       | Base + 0x00C3 |             |
| Priority select register 132 | INTC_PSR132     | 8-bit       | Base + 0x00C4 |             |
| Priority select register 133 | INTC_PSR133     | 8-bit       | Base + 0x00C5 |             |
| Priority select register 134 | INTC_PSR134     | 8-bit       | Base + 0x00C6 |             |
| Priority select register 135 | INTC_PSR135     | 8-bit       | Base + 0x00C7 |             |
| Priority select register 136 | INTC_PSR136     | 8-bit       | Base + 0x00C8 |             |
| Priority select register 137 | INTC_PSR137     | 8-bit       | Base + 0x00C9 |             |
| Priority select register 138 | INTC_PSR138     | 8-bit       | Base + 0x00CA |             |
| Priority select register 139 | INTC_PSR139     | 8-bit       | Base + 0x00CB |             |
| Priority select register 140 | INTC_PSR140     | 8-bit       | Base + 0x00CC |             |
| Priority select register 141 | INTC_PSR141     | 8-bit       | Base + 0x00CD |             |
| Priority select register 142 | INTC_PSR142     | 8-bit       | Base + 0x00CE |             |
| Priority select register 143 | INTC_PSR143     | 8-bit       | Base + 0x00CF |             |
| Priority select register 144 | INTC_PSR144     | 8-bit       | Base + 0x00D0 |             |
| Priority select register 145 | INTC_PSR145     | 8-bit       | Base + 0x00D1 |             |
| Priority select register 146 | INTC_PSR146     | 8-bit       | Base + 0x00D2 |             |

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description         | Register Name   | Used Size   | Address       | Reference   |
|------------------------------|-----------------|-------------|---------------|-------------|
| Priority select register 147 | INTC_PSR147     | 8-bit       | Base + 0x00D3 |             |
| Priority select register 148 | INTC_PSR148     | 8-bit       | Base + 0x00D4 |             |
| Priority select register 149 | INTC_PSR149     | 8-bit       | Base + 0x00D5 |             |
| Priority select register 150 | INTC_PSR150     | 8-bit       | Base + 0x00D6 |             |
| Priority select register 151 | INTC_PSR151     | 8-bit       | Base + 0x00D7 |             |
| Priority select register 152 | INTC_PSR152     | 8-bit       | Base + 0x00D8 |             |
| Priority select register 153 | INTC_PSR153     | 8-bit       | Base + 0x00D9 |             |
| Priority select register 154 | INTC_PSR154     | 8-bit       | Base + 0x00DA |             |
| Priority select register 155 | INTC_PSR155     | 8-bit       | Base + 0x00DB |             |
| Priority select register 156 | INTC_PSR156     | 8-bit       | Base + 0x00DC |             |
| Priority select register 157 | INTC_PSR157     | 8-bit       | Base + 0x00DD |             |
| Priority select register 158 | INTC_PSR158     | 8-bit       | Base + 0x00DE |             |
| Priority select register 159 | INTC_PSR159     | 8-bit       | Base + 0x00DF |             |
| Priority select register 160 | INTC_PSR160     | 8-bit       | Base + 0x00E0 |             |
| Priority select register 161 | INTC_PSR161     | 8-bit       | Base + 0x00E1 |             |
| Priority select register 162 | INTC_PSR162     | 8-bit       | Base + 0x00E2 |             |
| Priority select register 163 | INTC_PSR163     | 8-bit       | Base + 0x00E3 |             |
| Priority select register 164 | INTC_PSR164     | 8-bit       | Base + 0x00E4 |             |
| Priority select register 165 | INTC_PSR165     | 8-bit       | Base + 0x00E5 |             |
| Priority select register 166 | INTC_PSR166     | 8-bit       | Base + 0x00E6 |             |
| Priority select register 167 | INTC_PSR167     | 8-bit       | Base + 0x00E7 |             |
| Priority select register 168 | INTC_PSR168     | 8-bit       | Base + 0x00E8 |             |
| Priority select register 169 | INTC_PSR169     | 8-bit       | Base + 0x00E9 |             |
| Priority select register 170 | INTC_PSR170     | 8-bit       | Base + 0x00EA |             |
| Priority select register 171 | INTC_PSR171     | 8-bit       | Base + 0x00EB |             |
| Priority select register 172 | INTC_PSR172     | 8-bit       | Base + 0x00EC |             |
| Priority select register 173 | INTC_PSR173     | 8-bit       | Base + 0x00ED |             |
| Priority select register 174 | INTC_PSR174     | 8-bit       | Base + 0x00EE |             |
| Priority select register 175 | INTC_PSR175     | 8-bit       | Base + 0x00EF |             |
| Priority select register 176 | INTC_PSR176     | 8-bit       | Base + 0x00F0 |             |
| Priority select register 177 | INTC_PSR177     | 8-bit       | Base + 0x00F1 |             |
| Priority select register 178 | INTC_PSR178     | 8-bit       | Base + 0x00F2 |             |

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description         | Register Name   | Used Size   | Address       | Reference   |
|------------------------------|-----------------|-------------|---------------|-------------|
| Priority select register 179 | INTC_PSR179     | 8-bit       | Base + 0x00F3 |             |
| Priority select register 180 | INTC_PSR180     | 8-bit       | Base + 0x00F4 |             |
| Priority select register 181 | INTC_PSR181     | 8-bit       | Base + 0x00F5 |             |
| Priority select register 182 | INTC_PSR182     | 8-bit       | Base + 0x00F6 |             |
| Priority select register 183 | INTC_PSR183     | 8-bit       | Base + 0x00F7 |             |
| Priority select register 184 | INTC_PSR184     | 8-bit       | Base + 0x00F8 |             |
| Priority select register 185 | INTC_PSR185     | 8-bit       | Base + 0x00F9 |             |
| Priority select register 186 | INTC_PSR186     | 8-bit       | Base + 0x00FA |             |
| Priority select register 187 | INTC_PSR187     | 8-bit       | Base + 0x00FB |             |
| Priority select register 188 | INTC_PSR188     | 8-bit       | Base + 0x00FC |             |
| Priority select register 189 | INTC_PSR189     | 8-bit       | Base + 0x00FD |             |
| Priority select register 190 | INTC_PSR190     | 8-bit       | Base + 0x00FE |             |
| Priority select register 191 | INTC_PSR191     | 8-bit       | Base + 0x00FF |             |
| Priority select register 192 | INTC_PSR192     | 8-bit       | Base + 0x0100 |             |
| Priority select register 193 | INTC_PSR193     | 8-bit       | Base + 0x0101 |             |
| Priority select register 194 | INTC_PSR194     | 8-bit       | Base + 0x0102 |             |
| Priority select register 195 | INTC_PSR195     | 8-bit       | Base + 0x0103 |             |
| Priority select register 196 | INTC_PSR196     | 8-bit       | Base + 0x0104 |             |
| Priority select register 197 | INTC_PSR197     | 8-bit       | Base + 0x0105 |             |
| Priority select register 198 | INTC_PSR198     | 8-bit       | Base + 0x0106 |             |
| Priority select register 199 | INTC_PSR199     | 8-bit       | Base + 0x0107 |             |
| Priority select register 200 | INTC_PSR200     | 8-bit       | Base + 0x0108 |             |
| Priority select register 201 | INTC_PSR201     | 8-bit       | Base + 0x0109 |             |
| Priority select register 202 | INTC_PSR202     | 8-bit       | Base + 0x010A |             |
| Priority select register 203 | INTC_PSR203     | 8-bit       | Base + 0x010B |             |
| Priority select register 204 | INTC_PSR204     | 8-bit       | Base + 0x010C |             |
| Priority select register 205 | INTC_PSR205     | 8-bit       | Base + 0x010D |             |
| Priority select register 206 | INTC_PSR206     | 8-bit       | Base + 0x010E |             |
| Priority select register 207 | INTC_PSR207     | 8-bit       | Base + 0x010F |             |
| Priority select register 208 | INTC_PSR208     | 8-bit       | Base + 0x0110 |             |
| Priority select register 209 | INTC_PSR209     | 8-bit       | Base + 0x0111 |             |
| Priority select register 210 | INTC_PSR210     | 8-bit       | Base + 0x0112 |             |

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description         | Register Name   | Used Size   | Address       | Reference   |
|------------------------------|-----------------|-------------|---------------|-------------|
| Priority select register 211 | INTC_PSR211     | 8-bit       | Base + 0x0113 |             |
| Priority select register 212 | INTC_PSR212     | 8-bit       | Base + 0x0114 |             |
| Priority select register 213 | INTC_PSR213     | 8-bit       | Base + 0x0115 |             |
| Priority select register 214 | INTC_PSR214     | 8-bit       | Base + 0x0116 |             |
| Priority select register 215 | INTC_PSR215     | 8-bit       | Base + 0x0117 |             |
| Priority select register 216 | INTC_PSR216     | 8-bit       | Base + 0x0118 |             |
| Priority select register 217 | INTC_PSR217     | 8-bit       | Base + 0x0119 |             |
| Priority select register 218 | INTC_PSR218     | 8-bit       | Base + 0x011A |             |
| Priority select register 219 | INTC_PSR219     | 8-bit       | Base + 0x011B |             |
| Priority select register 220 | INTC_PSR220     | 8-bit       | Base + 0x011C |             |
| Priority select register 221 | INTC_PSR221     | 8-bit       | Base + 0x011D |             |
| Priority select register 222 | INTC_PSR222     | 8-bit       | Base + 0x011E |             |
| Priority select register 223 | INTC_PSR223     | 8-bit       | Base + 0x011F |             |
| Priority select register 224 | INTC_PSR224     | 8-bit       | Base + 0x0120 |             |
| Priority select register 225 | INTC_PSR225     | 8-bit       | Base + 0x0121 |             |
| Priority select register 226 | INTC_PSR226     | 8-bit       | Base + 0x0122 |             |
| Priority select register 227 | INTC_PSR227     | 8-bit       | Base + 0x0123 |             |
| Priority select register 228 | INTC_PSR228     | 8-bit       | Base + 0x0124 |             |
| Priority select register 229 | INTC_PSR229     | 8-bit       | Base + 0x0125 |             |
| Priority select register 230 | INTC_PSR230     | 8-bit       | Base + 0x0126 |             |
| Priority select register 231 | INTC_PSR231     | 8-bit       | Base + 0x0127 |             |
| Priority select register 232 | INTC_PSR232     | 8-bit       | Base + 0x0128 |             |
| Priority select register 233 | INTC_PSR233     | 8-bit       | Base + 0x0129 |             |
| Priority select register 234 | INTC_PSR234     | 8-bit       | Base + 0x012A |             |
| Priority select register 235 | INTC_PSR234     | 8-bit       | Base + 0x012B |             |
| Priority select register 236 | INTC_PSR236     | 8-bit       | Base + 0x012C |             |
| Priority select register 237 | INTC_PSR237     | 8-bit       | Base + 0x012D |             |
| Priority select register 238 | INTC_PSR238     | 8-bit       | Base + 0x012E |             |
| Priority select register 239 | INTC_PSR239     | 8-bit       | Base + 0x012F |             |
| Priority select register 240 | INTC_PSR240     | 8-bit       | Base + 0x0130 |             |
| Priority select register 241 | INTC_PSR241     | 8-bit       | Base + 0x0131 |             |
| Priority select register 242 | INTC_PSR242     | 8-bit       | Base + 0x0132 |             |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description         | Register Name   | Used Size   | Address       | Reference   |
|------------------------------|-----------------|-------------|---------------|-------------|
| Priority select register 243 | INTC_PSR243     | 8-bit       | Base + 0x0133 |             |
| Priority select register 244 | INTC_PSR244     | 8-bit       | Base + 0x0134 |             |
| Priority select register 245 | INTC_PSR245     | 8-bit       | Base + 0x0135 |             |
| Priority select register 246 | INTC_PSR246     | 8-bit       | Base + 0x0136 |             |
| Priority select register 247 | INTC_PSR247     | 8-bit       | Base + 0x0137 |             |
| Priority select register 248 | INTC_PSR248     | 8-bit       | Base + 0x0138 |             |
| Priority select register 249 | INTC_PSR249     | 8-bit       | Base + 0x0139 |             |
| Priority select register 250 | INTC_PSR250     | 8-bit       | Base + 0x013A |             |
| Priority select register 251 | INTC_PSR251     | 8-bit       | Base + 0x013B |             |
| Priority select register 252 | INTC_PSR252     | 8-bit       | Base + 0x013C |             |
| Priority select register 253 | INTC_PSR253     | 8-bit       | Base + 0x013D |             |
| Priority select register 254 | INTC_PSR254     | 8-bit       | Base + 0x013E |             |
| Priority select register 255 | INTC_PSR255     | 8-bit       | Base + 0x013F |             |
| Priority select register 256 | INTC_PSR256     | 8-bit       | Base + 0x0140 |             |
| Priority select register 257 | INTC_PSR257     | 8-bit       | Base + 0x0141 |             |
| Priority select register 258 | INTC_PSR258     | 8-bit       | Base + 0x0142 |             |
| Priority select register 259 | INTC_PSR259     | 8-bit       | Base + 0x0143 |             |
| Priority select register 260 | INTC_PSR260     | 8-bit       | Base + 0x0144 |             |
| Priority select register 261 | INTC_PSR261     | 8-bit       | Base + 0x0145 |             |
| Priority select register 262 | INTC_PSR262     | 8-bit       | Base + 0x0146 |             |
| Priority select register 263 | INTC_PSR263     | 8-bit       | Base + 0x0147 |             |
| Priority select register 264 | INTC_PSR264     | 8-bit       | Base + 0x0148 |             |
| Priority select register 265 | INTC_PSR265     | 8-bit       | Base + 0x0149 |             |
| Priority select register 266 | INTC_PSR266     | 8-bit       | Base + 0x014A |             |
| Priority select register 267 | INTC_PSR267     | 8-bit       | Base + 0x014B |             |
| Priority select register 268 | INTC_PSR268     | 8-bit       | Base + 0x014C |             |
| Priority select register 269 | INTC_PSR269     | 8-bit       | Base + 0x014D |             |
| Priority select register 270 | INTC_PSR270     | 8-bit       | Base + 0x014E |             |
| Priority select register 271 | INTC_PSR271     | 8-bit       | Base + 0x014F |             |
| Priority select register 272 | INTC_PSR272     | 8-bit       | Base + 0x0150 |             |
| Priority select register 273 | INTC_PSR273     | 8-bit       | Base + 0x0151 |             |
| Priority select register 274 | INTC_PSR274     | 8-bit       | Base + 0x0152 |             |

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description         | Register Name   | Used Size   | Address       | Reference   |
|------------------------------|-----------------|-------------|---------------|-------------|
| Priority select register 275 | INTC_PSR275     | 8-bit       | Base + 0x0153 |             |
| Priority select register 276 | INTC_PSR276     | 8-bit       | Base + 0x0154 |             |
| Priority select register 277 | INTC_PSR277     | 8-bit       | Base + 0x0155 |             |
| Priority select register 278 | INTC_PSR278     | 8-bit       | Base + 0x0156 |             |
| Priority select register 279 | INTC_PSR279     | 8-bit       | Base + 0x0157 |             |
| Priority select register 280 | INTC_PSR280     | 8-bit       | Base + 0x0158 |             |
| Priority select register 281 | INTC_PSR281     | 8-bit       | Base + 0x0159 |             |
| Priority select register 282 | INTC_PSR282     | 8-bit       | Base + 0x015A |             |
| Priority select register 283 | INTC_PSR283     | 8-bit       | Base + 0x015B |             |
| Priority select register 284 | INTC_PSR284     | 8-bit       | Base + 0x015C |             |
| Priority select register 285 | INTC_PSR285     | 8-bit       | Base + 0x015D |             |
| Priority select register 286 | INTC_PSR286     | 8-bit       | Base + 0x015E |             |
| Priority select register 287 | INTC_PSR287     | 8-bit       | Base + 0x015F |             |
| Priority select register 288 | INTC_PSR288     | 8-bit       | Base + 0x0160 |             |
| Priority select register 289 | INTC_PSR289     | 8-bit       | Base + 0x0161 |             |
| Priority select register 290 | INTC_PSR290     | 8-bit       | Base + 0x0162 |             |
| Priority select register 291 | INTC_PSR291     | 8-bit       | Base + 0x0163 |             |
| Priority select register 292 | INTC_PSR292     | 8-bit       | Base + 0x0164 |             |
| Priority select register 293 | INTC_PSR293     | 8-bit       | Base + 0x0165 |             |
| Priority select register 294 | INTC_PSR294     | 8-bit       | Base + 0x0166 |             |
| Priority select register 295 | INTC_PSR295     | 8-bit       | Base + 0x0167 |             |
| Priority select register 296 | INTC_PSR296     | 8-bit       | Base + 0x0168 |             |
| Priority select register 297 | INTC_PSR297     | 8-bit       | Base + 0x0169 |             |
| Priority select register 298 | INTC_PSR298     | 8-bit       | Base + 0x016A |             |
| Priority select register 299 | INTC_PSR299     | 8-bit       | Base + 0x016B |             |
| Priority select register 300 | INTC_PSR300     | 8-bit       | Base + 0x016C |             |
| Priority select register 301 | INTC_PSR301     | 8-bit       | Base + 0x016D |             |
| Priority select register 302 | INTC_PSR302     | 8-bit       | Base + 0x016E |             |
| Priority select register 303 | INTC_PSR303     | 8-bit       | Base + 0x016F |             |
| Priority select register 304 | INTC_PSR304     | 8-bit       | Base + 0x0170 |             |
| Priority select register 305 | INTC_PSR305     | 8-bit       | Base + 0x0171 |             |
| Priority select register 306 | INTC_PSR306     | 8-bit       | Base + 0x0172 |             |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description                    | Register Name                  | Used Size   | Address               | Reference                                   |
|-----------------------------------------|--------------------------------|-------------|-----------------------|---------------------------------------------|
| Priority select register 307            | INTC_PSR307                    | 8-bit       | Base + 0x0173         |                                             |
| Fast Ethernet Controller (FEC)          | Fast Ethernet Controller (FEC) |             | 0xFFF4_C000           | Chapter 14 'Fast Ethernet Controller (FEC)' |
| Interrupt Event Register                | EIR                            | 32-bit      | Base + 0x0004         |                                             |
| Interrupt Mask Register                 | EIMR                           | 32-bit      | Base + 0x0008         |                                             |
| Receive Descriptor Active Register      | RDAR                           | 32-bit      | Base + 0x0010         |                                             |
| Transmit Descriptor Active Register     | TDAR                           | 32-bit      | Base + 0x0014         |                                             |
| Ethernet Control Register               | ECR                            | 32-bit      | Base + 0x0024         |                                             |
| MII Management Frame Regsiter           | MMFR                           | 32-bit      | Base + 0x0040         |                                             |
| MII Speed Control Register              | MSCR                           | 32-bit      | Base + 0x0044         |                                             |
| MIB Control/Status Register             | MIBC                           | 32-bit      | Base + 0x0064         |                                             |
| Receive Control Register                | RCR                            | 32-bit      | Base + 0x0084         |                                             |
| Transmit Control Register               | TCR                            | 32-bit      | Base + 0x00C4         |                                             |
| MAC Address Low Register                | PALR                           | 32-bit      | Base + 0x00E4         |                                             |
| MAC Address Upper Register + Type Field | PAUR                           | 32-bit      | Base + 0x00E8         |                                             |
| Opcode + Pause Duration                 | OPD                            | 32-bit      | Base + 0x00EC         |                                             |
| Upper 32 bits of Individual Hash Table  | IAUR                           | 32-bit      | Base + 0x0118         |                                             |
| Lower 32 Bits of Individual Hash Table  | IALR                           | 32-bit      | Base + 0x011C         |                                             |
| Upper 32 bits of Group Hash Table       | GAUR                           | 32-bit      | Base + 0x0120         |                                             |
| Lower 32 bits of Group Hash Table       | GALR                           | 32-bit      | Base + 0x0124         |                                             |
| Transmit FIFO Watermark                 | TFWR                           | 32-bit      | Base + 0x0144         |                                             |
| FIFO Receive Bound Register             | FRBR                           | 32-bit      | Base + 0x014C         |                                             |
| FIFO Receive FIFO Start Registers       | FRSR                           | 32-bit      | Base + 0x0150         |                                             |
| Pointer to Receive Descriptor Ring      | ERDSR                          | 32-bit      | Base + 0x0180         |                                             |
| Pointer to Transmit Descriptor Ring     | ETDSR                          | 32-bit      | Base + 0x0184         |                                             |
| Maximum Receive Buffer Size             | EMRBR                          | 32-bit      | Base + 0x0188         |                                             |
| MIB Block Counters                      | MIB                            |             | FFF4_C200             |                                             |
| Reserved                                | -                              | -           | Base + (0xFFF0__8000) |                                             |
| Reserved                                | -                              | -           | Base + (0xFFF1_0000)  |                                             |

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description                                | Register Name                                       | Used Size   | Address                | Reference                                                         |
|-----------------------------------------------------|-----------------------------------------------------|-------------|------------------------|-------------------------------------------------------------------|
| Enhanced Queued Analog-to-Digital Converter (eQADC) | Enhanced Queued Analog-to-Digital Converter (eQADC) |             | 0xFFF8_0000            | Chapter 19, 'Enhanced Queued Analog-to-Digital Converter (eQADC)' |
| Module configuration register                       | EQADC_MCR                                           | 32-bit      | Base + 0x0000          |                                                                   |
| Reserved                                            | -                                                   | -           | Base + (0x0004-0x0007) |                                                                   |
| Null message send format register                   | EQADC_NMSFR                                         | 32-bit      | Base + 0x0008          |                                                                   |
| External trigger digital filter register            | EQADC_ETDFR                                         | 32-bit      | Base + 0x000C          |                                                                   |
| CFIFO push register 0                               | EQADC_CFPR0                                         | 32-bit      | Base +0x0010           |                                                                   |
| CFIFO push register 1                               | EQADC_CFPR1                                         | 32-bit      | Base +0x0014           |                                                                   |
| CFIFO push register 2                               | EQADC_CFPR2                                         | 32-bit      | Base +0x0018           |                                                                   |
| CFIFO push register 3                               | EQADC_CFPR3                                         | 32-bit      | Base +0x001C           |                                                                   |
| CFIFO push register 4                               | EQADC_CFPR4                                         | 32-bit      | Base +0x0020           |                                                                   |
| CFIFO push register 5                               | EQADC_CFPR5                                         | 32-bit      | Base +0x0024           |                                                                   |
| Reserved                                            | -                                                   | -           | Base + (0x0028-0x002F) |                                                                   |
| Result FIFO pop register 0                          | EQADC_RFPR0                                         | 32-bit      | Base + 0x0030          |                                                                   |
| Result FIFO pop register 1                          | EQADC_RFPR1                                         | 32-bit      | Base + 0x0034          |                                                                   |
| Result FIFO pop register 2                          | EQADC_RFPR2                                         | 32-bit      | Base + 0x0038          |                                                                   |
| Result FIFO pop register 3                          | EQADC_RFPR3                                         | 32-bit      | Base + 0x003C          |                                                                   |
| Result FIFO pop register 4                          | EQADC_RFPR4                                         | 32-bit      | Base + 0x0040          |                                                                   |
| Result FIFO pop register 5                          | EQADC_RFPR5                                         | 32-bit      | Base + 0x0044          |                                                                   |
| Reserved                                            | -                                                   | -           | Base + (0x0048-0x004F) |                                                                   |
| CFIFO control register 0                            | EQADC_CFCR0                                         | 16-bit      | Base + 0x0050          |                                                                   |
| CFIFO control register 1                            | EQADC_CFCR1                                         | 16-bit      | Base + 0x0052          |                                                                   |
| CFIFO control register 2                            | EQADC_CFCR2                                         | 16-bit      | Base + 0x0054          |                                                                   |
| CFIFO control register 3                            | EQADC_CFCR3                                         | 16-bit      | Base + 0x0056          |                                                                   |
| CFIFO control register 4                            | EQADC_CFCR4                                         | 16-bit      | Base + 0x0058          |                                                                   |
| CFIFO control register 5                            | EQADC_CFCR5                                         | 16-bit      | Base + 0x005A          |                                                                   |
| Reserved                                            | -                                                   | -           | Base + (0x005C-0x005F) |                                                                   |
| Interrupt and DMA control register 0                | EQADC_IDCR0                                         | 16-bit      | Base + 0x0060          |                                                                   |
| Interrupt and DMA control register 1                | EQADC_IDCR1                                         | 16-bit      | Base + 0x0062          |                                                                   |
| Interrupt and DMA control register 2                | EQADC_IDCR2                                         | 16-bit      | Base + 0x0064          |                                                                   |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description                 | Register Name   | Used Size   | Address                | Reference   |
|--------------------------------------|-----------------|-------------|------------------------|-------------|
| Interrupt and DMA control register 3 | EQADC_IDCR3     | 16-bit      | Base + 0x0066          |             |
| Interrupt and DMA control register 4 | EQADC_IDCR4     | 16-bit      | Base + 0x0068          |             |
| Interrupt and DMA control register 5 | EQADC_IDCR5     | 16-bit      | Base + 0x006A          |             |
| Reserved                             | -               | -           | Base + (0x006C-0x006F) |             |
| FIFO and interrupt status register 0 | EQADC_FISR0     | 32-bit      | Base + 0x0070          |             |
| FIFO and interrupt status register 1 | EQADC_FISR1     | 32-bit      | Base + 0x0074          |             |
| FIFO and interrupt status register 2 | EQADC_FISR2     | 32-bit      | Base + 0x0078          |             |
| FIFO and interrupt status register 3 | EQADC_FISR3     | 32-bit      | Base + 0x007C          |             |
| FIFO and interrupt status register 4 | EQADC_FISR4     | 32-bit      | Base + 0x0080          |             |
| FIFO and interrupt status register 5 | EQADC_FISR5     | 32-bit      | Base + 0x0084          |             |
| Reserved                             | -               | -           | Base + (0x0088-0x008F) |             |
| CFIFO transfer counter register 0    | EQADC_CFTCR0    | 16-bit      | Base + 0x0090          |             |
| CFIFO transfer counter register 1    | EQADC_CFTCR1    | 16-bit      | Base + 0x0092          |             |
| CFIFO transfer counter register 2    | EQADC_CFTCR2    | 16-bit      | Base + 0x0094          |             |
| CFIFO transfer counter register 3    | EQADC_CFTCR3    | 16-bit      | Base + 0x0096          |             |
| CFIFO transfer counter register 4    | EQADC_CFTCR4    | 16-bit      | Base + 0x0098          |             |
| CFIFO transfer counter register 5    | EQADC_CFTCR5    | 16-bit      | Base + 0x009A          |             |
| Reserved                             | -               | -           | Base + (0x009C-0x009F) |             |
| CFIFO status snapshot register 0     | EQADC_CFSSR0    | 32-bit      | Base + 0x00A0          |             |
| CFIFO status snapshot register 1     | EQADC_CFSSR1    | 32-bit      | Base + 0x00A4          |             |
| CFIFO status snapshot register 2     | EQADC_CFSSR2    | 32-bit      | Base + 0x00A8          |             |
| CFIFO status register                | EQADC_CFSR      | 32-bit      | Base + 0x00AC          |             |
| Reserved                             | -               | -           | Base + (0x00B0-0x00B3  |             |
| SSI control register                 | EQADC_SSICR     | 32-bit      | Base + 0x00B4          |             |
| SSI receive data register            | EQADC_SSIRDR    | 32-bit      | Base + 0x00B8          |             |
| Reserved                             | -               | -           | Base + (0x00BC-0x00FF) |             |
| CFIFO 0 register 0                   | EQADC_CF0R0     | 32-bit      | Base + 0x0100          |             |
| CFIFO 0 register 1                   | EQADC_CF0R1     | 32-bit      | Base + 0x0104          |             |
| CFIFO 0 register 2                   | EQADC_CF0R2     | 32-bit      | Base + 0x0108          |             |
| CFIFO 0 register 3                   | EQADC_CF0R3     | 32-bit      | Base + 0x010C          |             |
| Reserved                             | -               | -           | Base + (0x0110-0x013F) |             |
| CFIFO 1 register 0                   | EQADC_CF1R0     | 32-bit      | Base + 0x0140          |             |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description   | Register Name   | Used Size   | Address                | Reference   |
|------------------------|-----------------|-------------|------------------------|-------------|
| CFIFO 1 register 1     | EQADC_CF1R1     | 32-bit      | Base + 0x0144          |             |
| CFIFO 1 register 2     | EQADC_CF1R2     | 32-bit      | Base + 0x0148          |             |
| CFIFO 1 register 3     | EQADC_CF1R3     | 32-bit      | Base + 0x014C          |             |
| Reserved               | -               | -           | Base + (0x0150-0x017F) |             |
| CFIFO 2 register 0     | EQADC_CF2R0     | 32-bit      | Base + 0x0180          |             |
| CFIFO 2 register 1     | EQADC_CF2R1     | 32-bit      | Base + 0x0184          |             |
| CFIFO 2 register 2     | EQADC_CF2R2     | 32-bit      | Base + 0x0188          |             |
| CFIFO 2 register 3     | EQADC_CF2R3     | 32-bit      | Base + 0x018C          |             |
| Reserved               | -               | -           | Base + (0x0190-0x01BF) |             |
| CFIFO 3 register 0     | EQADC_CF3R0     | 32-bit      | Base + 0x01C0          |             |
| CFIFO 3 register 1     | EQADC_CF3R1     | 32-bit      | Base + 0x01C4          |             |
| CFIFO 3 register 2     | EQADC_CF3R2     | 32-bit      | Base + 0x01C8          |             |
| CFIFO 3 register 3     | EQADC_CF3R3     | 32-bit      | Base + 0x01CC          |             |
| Reserved               | -               | -           | Base + (0x01D0-0x01FF) |             |
| CFIFO 4 register 0     | EQADC_CF4R0     | 32-bit      | Base + 0x0200          |             |
| CFIFO 4 register 1     | EQADC_CF4R1     | 32-bit      | Base + 0x0204          |             |
| CFIFO 4 register 2     | EQADC_CF4R2     | 32-bit      | Base + 0x0208          |             |
| CFIFO 4 register 3     | EQADC_CF4R3     | 32-bit      | Base + 0x020C          |             |
| Reserved               | -               | -           | Base + (0x0210-0x023F) |             |
| CFIFO 5 register 0     | EQADC_CF5R0     | 32-bit      | Base + 0x0240          |             |
| CFIFO 5 register 1     | EQADC_CF5R1     | 32-bit      | Base + 0x0244          |             |
| CFIFO 5 register 2     | EQADC_CF5R2     | 32-bit      | Base + 0x0248          |             |
| CFIFO 5 register 3     | EQADC_CF5R3     | 32-bit      | Base + 0x024C          |             |
| Reserved               | -               | -           | Base + (0x0250-0x02FF) |             |
| RFIFO 0 register 0     | EQADC_RF0R0     | 32-bit      | Base + 0x0300          |             |
| RFIFO 0 register 1     | EQADC_RF0R1     | 32-bit      | Base + 0x0304          |             |
| RFIFO 0 register 2     | EQADC_RF0R2     | 32-bit      | Base + 0x0308          |             |
| RFIFO 0 register 3     | EQADC_RF0R3     | 32-bit      | Base + 0x030C          |             |
| Reserved               | -               | -           | Base + (0x0310-0x033F) |             |
| RFIFO 1 register 0     | EQADC_RF1R0     | 32-bit      | Base + 0x0340          |             |
| RFIFO 1 register 1     | EQADC_RF1R1     | 32-bit      | Base + 0x0344          |             |
| RFIFO 1 register 2     | EQADC_RF1R2     | 32-bit      | Base + 0x0348          |             |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description                      | Register Name   | Used Size   | Address                      | Reference   |
|-------------------------------------------|-----------------|-------------|------------------------------|-------------|
| RFIFO 1 register 3                        | EQADC_RF1R3     | 32-bit      | Base + 0x034C                |             |
| Reserved                                  | -               | -           | Base + (0x0350-0x037F)       |             |
| RFIFO 2 register 0                        | EQADC_RF2R0     | 32-bit      | Base + 0x0380                |             |
| RFIFO 2 register 1                        | EQADC_RF2R1     | 32-bit      | Base + 0x0384                |             |
| RFIFO 2 register 2                        | EQADC_RF2R2     | 32-bit      | Base + 0x0388                |             |
| RFIFO 2 register 3                        | EQADC_RF2R3     | 32-bit      | Base + 0x038C                |             |
| Reserved                                  | -               | -           | Base + (0x0390-0x03BF)       |             |
| RFIFO 3 register 0                        | EQADC_RF3R0     | 32-bit      | Base + 0x03C0                |             |
| RFIFO 3 register 1                        | EQADC_RF3R1     | 32-bit      | Base + 0x03C4                |             |
| RFIFO 3 register 2                        | EQADC_RF3R2     | 32-bit      | Base + 0x03C8                |             |
| RFIFO 3 register 3                        | EQADC_RF3R3     | 32-bit      | Base + 0x03CC                |             |
| Reserved                                  | -               | -           | Base + (0x03D0-0x03FF)       |             |
| RFIFO 4 register 0                        | EQADC_RF4R0     | 32-bit      | Base + 0x0400                |             |
| RFIFO 4 register 1                        | EQADC_RF4R1     | 32-bit      | Base + 0x0404                |             |
| RFIFO 4 register 2                        | EQADC_RF4R2     | 32-bit      | Base + 0x0408                |             |
| RFIFO 4 register 3                        | EQADC_RF4R3     | 32-bit      | Base + 0x040C                |             |
| Reserved                                  | -               | -           | Base + (0x0410-0x043F)       |             |
| RFIFO 5 register 0                        | EQADC_RF5R0     | 32-bit      | Base + 0x0440                |             |
| RFIFO 5 register 1                        | EQADC_RF5R1     | 32-bit      | Base + 0x0444                |             |
| RFIFO 5 register 2                        | EQADC_RF5R2     | 32-bit      | Base + 0x0448                |             |
| RFIFO 5 register 3                        | EQADC_RF5R3     | 32-bit      | Base + 0x044C                |             |
| Reserved                                  | -               | -           | Base + (0x0450-0x07FF)       |             |
| ADC0 control register                     | ADC0_CR         |             | No memory mapped access      |             |
| ADC1 control register                     | ADC1_CR         |             | No memory mapped access      |             |
| ADC time stamp control register           | ADC_TSCR        |             | No memory mapped access      |             |
| ADC time base counter register            | ADC_TBCR        |             | No memory mapped access      |             |
| ADC0 gain calibration constant register   | ADC0_GCCR       |             | No memory mapped access      |             |
| ADC1 gain calibration constant register   | ADC1_GCCR       |             | No memory mapped access      |             |
| ADC0 offset calibration constant register | ADC0_OCCR       |             | No memory mapped access      |             |
| ADC1 offset calibration constant register | ADC1_OCCR       |             | No memory mapped access      |             |
| Reserved                                  | -               | -           | (Base + 0x0800)- 0xFFF8_FFFF |             |

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description                             | Register Name                                  | Used Size   | Address                                                                               | Reference            |
|--------------------------------------------------|------------------------------------------------|-------------|---------------------------------------------------------------------------------------|----------------------|
| Deserial / Serial Peripheral Interface (DSPIx)   | Deserial / Serial Peripheral Interface (DSPIx) |             | 0xFFF9_0000 (DSPI A) 2 0xFFF9_4000 (DSPI B) 0xFFF9_8000 (DSPI C) 0xFFF9_C000 (DSPI D) | 20.1, 'Introduction' |
| Module configuration register                    | DSPIx_MCR                                      | 32-bit      | Base + 0x0000                                                                         |                      |
| Reserved                                         | -                                              | -           | Base + (0x0004-0x0007)                                                                |                      |
| Transfer count register                          | DSPIx_TCR                                      | 32-bit      | Base + 0x0008                                                                         |                      |
| Clock and transfer attribute register 0          | DSPIx_CTAR0                                    | 32-bit      | Base + 0x000C                                                                         |                      |
| Clock and transfer attribute register 1          | DSPIx_CTAR1                                    | 32-bit      | Base + 0x0010                                                                         |                      |
| Clock and transfer attribute register 2          | DSPIx_CTAR2                                    | 32-bit      | Base + 0x0014                                                                         |                      |
| Clock and transfer attribute register 3          | DSPIx_CTAR3                                    | 32-bit      | Base + 0x0018                                                                         |                      |
| Clock and transfer attribute register 4          | DSPIx_CTAR4                                    | 32-bit      | Base + 0x001C                                                                         |                      |
| Clock and transfer attribute register 5          | DSPIx_CTAR5                                    | 32-bit      | Base + 0x0020                                                                         |                      |
| Clock and transfer attribute register 6          | DSPIx_CTAR6                                    | 32-bit      | Base + 0x0024                                                                         |                      |
| Clock and transfer attribute register 7          | DSPIx_CTAR7                                    | 32-bit      | Base + 0x0028                                                                         |                      |
| Status register                                  | DSPIx_SR                                       | 32-bit      | Base + 0x002C                                                                         |                      |
| DMA/interrupt request select and enable register | DSPIx_RSER                                     | 32-bit      | Base + 0x0030                                                                         |                      |
| Push TX FIFO register                            | DSPIx_PUSHR                                    | 32-bit      | Base + 0x0034                                                                         |                      |
| Pop RX FIFO register                             | DSPIx_POPR                                     | 32-bit      | Base + 0x0038                                                                         |                      |
| Transmit FIFO registers 0                        | DSPIx_TXFR0                                    | 32-bit      | Base + 0x003C                                                                         |                      |
| Transmit FIFO registers 1                        | DSPIx_TXFR1                                    | 32-bit      | Base + 0x0040                                                                         |                      |
| Transmit FIFO registers 2                        | DSPIx_TXFR2                                    | 32-bit      | Base + 0x0044                                                                         |                      |
| Transmit FIFO registers 3                        | DSPIx_TXFR3                                    | 32-bit      | Base + 0x0048                                                                         |                      |
| Reserved                                         | -                                              | -           | Base + (0x004C-0x007B)                                                                |                      |
| Receive FIFO registers 0                         | DSPIx_RXFR0                                    | 32-bit      | Base + 0x007C                                                                         |                      |
| Receive FIFO registers 1                         | DSPIx_RXFR1                                    | 32-bit      | Base + 0x0080                                                                         |                      |
| Receive FIFO registers 2                         | DSPIx_RXFR2                                    | 32-bit      | Base + 0x0084                                                                         |                      |
| Receive FIFO registers 3                         | DSPIx_RXFR3                                    | 32-bit      | Base + 0x0088                                                                         |                      |
| Reserved                                         | -                                              | -           | Base + (0x008C-0x00BB)                                                                |                      |
| DSI configuration register                       | DSPIx_DSICR                                    | 32-bit      | Base + 0x00BC                                                                         |                      |
| DSI serialization data register                  | DSPIx_SDR                                      | 32-bit      | Base + 0x00C0                                                                         |                      |
| DSI alternate serialization data register        | DSPIx_ASDR                                     | 32-bit      | Base + 0x00C4                                                                         |                      |
| DSI transmit comparison register                 | DSPIx_COMPR                                    | 32-bit      | Base + 0x00C8                                                                         |                      |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description                            | Register Name                                   | Used Size   | Address                                                                                 | Reference                                                    |
|-------------------------------------------------|-------------------------------------------------|-------------|-----------------------------------------------------------------------------------------|--------------------------------------------------------------|
| DSI deserialization data register               | DSPIx_DDR                                       | 32-bit      | Base + 0x00CC                                                                           |                                                              |
| Reserved                                        | -                                               | -           | (Base +0x00D0)- (0xFFF9_3FFF) (A) (0xFFF9_7FFF) (B) (0xFFF9_BFFF) (C) (0xFFFA_FFFF) (D) |                                                              |
| Enhanced Serial Communication Interface (eSCIx) | Enhanced Serial Communication Interface (eSCIx) |             | 0xFFFB_0000 (A) 0xFFFB_4000 (B)                                                         | Chapter 21, 'Enhanced Serial Communication Interface (eSCI)' |
| Control register 1                              | ESCIx_CR1                                       | 32-bit      | Base + 0x0000                                                                           |                                                              |
| Control register 2                              | ESCIx_CR2                                       | 16-bit      | Base + 0x0004                                                                           |                                                              |
| Data register                                   | ESCIx_DR                                        | 16-bit      | Base + 0x0006                                                                           |                                                              |
| Status register                                 | ESCIx_SR                                        | 32-bit      | Base + 0x0008                                                                           |                                                              |
| LIN control register                            | ESCIx_LCR                                       | 32-bit      | Base + 0x000C                                                                           |                                                              |
| LIN transmit register                           | ESCIx_LTR                                       | 32-bit      | Base + 0x0010                                                                           |                                                              |
| LIN receive register                            | ESCIx_LRR                                       | 32-bit      | Base + 0x0014                                                                           |                                                              |
| LIN CRC polynomial register                     | ESCIx_LPR                                       | 32-bit      | Base + 0x0018                                                                           |                                                              |
| Reserved                                        | -                                               | -           | (Base +0x001C)- (0xFFFB_3FFF) (A) (0xFFFB_7FFF) (B)                                     |                                                              |
| FlexCAN2 Controller Area Network (CANx)         | FlexCAN2 Controller Area Network (CANx)         |             | 0xFFFC_0000 (FlexCAN A) 0xFFFC_4000(FlexCANB) 2 0xFFFC_8000 (FlexCAN C)                 | Chapter 22, 'FlexCAN2 Controller Area Network'               |
| Module configuration register                   | CANx_MCR                                        | 32-bit      | Base + 0x0000                                                                           |                                                              |
| Control register                                | CANx_CR                                         | 32-bit      | Base + 0x0004                                                                           |                                                              |
| Free running timer register                     | CANx_TIMER                                      | 32-bit      | Base + 0x0008                                                                           |                                                              |
| Reserved                                        | -                                               | -           | Base + (0x000C-0x000F)                                                                  |                                                              |
| Receive global mask register                    | CANx_RXGMASK                                    | 32-bit      | Base + 0x0010                                                                           |                                                              |
| Receive buffer 14 mask register                 | CANx_RX14MASK                                   | 32-bit      | Base + 0x0014                                                                           |                                                              |
| Receive buffer 15 mask register                 | CANx_RX15MASK                                   | 32-bit      | Base + 0x0018                                                                           |                                                              |
| Error counter register                          | CANx_ECR                                        | 32-bit      | Base + 0x001C                                                                           |                                                              |
| Error and status register                       | CANx_ESR                                        | 32-bit      | Base + 0x0020                                                                           |                                                              |
| Interrupt mask register high                    | CANx_IMRH                                       | 32-bit      | Base + 0x0024                                                                           |                                                              |
| Interrupt mask register low                     | CANx_IMRL                                       | 32-bit      | Base + 0x0028                                                                           |                                                              |

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description         | Register Name            | Used Size   | Address                | Reference                              |
|------------------------------|--------------------------|-------------|------------------------|----------------------------------------|
| Interrupt flag register high | CANx_IFRH                | 32-bit      | Base + 0x002C          |                                        |
| Interrupt flag register low  | CANx_IFRL                | 32-bit      | Base + 0x0030          |                                        |
| Reserved                     | -                        | -           | Base + (0x0034-0x007F) |                                        |
| Boot Assist Module (BAM)     | Boot Assist Module (BAM) |             | 0xFFFF_C000            | Chapter 16, 'Boot Assist Module (BAM)' |
| Message buffer 0             | MB0                      | 16-bit      | Base + 0x0080          |                                        |
| Message buffer 1             | MB1                      | 16-bit      | Base + 0x0090          |                                        |
| Message buffer 2             | MB2                      | 16-bit      | Base + 0x00A0          |                                        |
| Message buffer 3             | MB3                      | 16-bit      | Base + 0x00B0          |                                        |
| Message buffer 4             | MB4                      | 16-bit      | Base + 0x00C0          |                                        |
| Message buffer 5             | MB5                      | 16-bit      | Base + 0x00D0          |                                        |
| Message buffer 6             | MB6                      | 16-bit      | Base + 0x00E0          |                                        |
| Message buffer 7             | MB7                      | 16-bit      | Base + 0x00F0          |                                        |
| Message buffer 8             | MB8                      | 16-bit      | Base + 0x0100          |                                        |
| Message buffer 9             | MB9                      | 16-bit      | Base + 0x0110          |                                        |
| Message buffer 10            | MB10                     | 16-bit      | Base + 0x0120          |                                        |
| Message buffer 11            | MB11                     | 16-bit      | Base + 0x0130          |                                        |
| Message buffer 12            | MB12                     | 16-bit      | Base + 0x0140          |                                        |
| Message buffer 13            | MB13                     | 16-bit      | Base + 0x0150          |                                        |
| Message buffer 14            | MB14                     | 16-bit      | Base + 0x0160          |                                        |
| Message buffer 15            | MB15                     | 16-bit      | Base + 0x0170          |                                        |
| Message buffer 16            | MB16                     | 16-bit      | Base + 0x0180          |                                        |
| Message buffer 17            | MB17                     | 16-bit      | Base + 0x0190          |                                        |
| Message buffer 18            | MB18                     | 16-bit      | Base + 0x01A0          |                                        |
| Message buffer 19            | MB19                     | 16-bit      | Base + 0x01B0          |                                        |
| Message buffer 20            | MB20                     | 16-bit      | Base + 0x01C0          |                                        |
| Message buffer 21            | MB21                     | 16-bit      | Base + 0x01D0          |                                        |
| Message buffer 22            | MB22                     | 16-bit      | Base + 0x01E0          |                                        |
| Message buffer 23            | MB23                     | 16-bit      | Base + 0x01F0          |                                        |
| Message buffer 24            | MB24                     | 16-bit      | Base + 0x0200          |                                        |
| Message buffer 25            | MB25                     | 16-bit      | Base + 0x0210          |                                        |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description   | Register Name   | Used Size   | Address       | Reference   |
|------------------------|-----------------|-------------|---------------|-------------|
| Message buffer 26      | MB26            | 16-bit      | Base + 0x0220 |             |
| Message buffer 27      | MB27            | 16-bit      | Base + 0x0230 |             |
| Message buffer 28      | MB28            | 16-bit      | Base + 0x0240 |             |
| Message buffer 29      | MB29            | 16-bit      | Base + 0x0250 |             |
| Message buffer 30      | MB30            | 16-bit      | Base + 0x0260 |             |
| Message buffer 31      | MB31            | 16-bit      | Base + 0x0270 |             |
| Message buffer 32      | MB32            | 16-bit      | Base + 0x0280 |             |
| Message buffer 33      | MB33            | 16-bit      | Base + 0x0290 |             |
| Message buffer 34      | MB34            | 16-bit      | Base + 0x02A0 |             |
| Message buffer 35      | MB35            | 16-bit      | Base + 0x02B0 |             |
| Message buffer 36      | MB36            | 16-bit      | Base + 0x02C0 |             |
| Message buffer 37      | MB37            | 16-bit      | Base + 0x02D0 |             |
| Message buffer 38      | MB38            | 16-bit      | Base + 0x02E0 |             |
| Message buffer 39      | MB39            | 16-bit      | Base + 0x02F0 |             |
| Message buffer 40      | MB40            | 16-bit      | Base + 0x0300 |             |
| Message buffer 41      | MB41            | 16-bit      | Base + 0x0310 |             |
| Message buffer 42      | MB42            | 16-bit      | Base + 0x0320 |             |
| Message buffer 43      | MB43            | 16-bit      | Base + 0x0330 |             |
| Message buffer 44      | MB44            | 16-bit      | Base + 0x0340 |             |
| Message buffer 45      | MB45            | 16-bit      | Base + 0x0350 |             |
| Message buffer 46      | MB46            | 16-bit      | Base + 0x0360 |             |
| Message buffer 47      | MB47            | 16-bit      | Base + 0x0370 |             |
| Message buffer 48      | MB48            | 16-bit      | Base + 0x0380 |             |
| Message buffer 49      | MB49            | 16-bit      | Base + 0x0390 |             |
| Message buffer 50      | MB50            | 16-bit      | Base + 0x03A0 |             |
| Message buffer 51      | MB51            | 16-bit      | Base + 0x03B0 |             |
| Message buffer 52      | MB52            | 16-bit      | Base + 0x03C0 |             |
| Message buffer 53      | MB53            | 16-bit      | Base + 0x03D0 |             |
| Message buffer 54      | MB54            | 16-bit      | Base + 0x03E0 |             |
| Message buffer 55      | MB55            | 16-bit      | Base + 0x03F0 |             |
| Message buffer 56      | MB56            | 16-bit      | Base + 0x0400 |             |
| Message buffer 57      | MB57            | 16-bit      | Base + 0x0410 |             |

Table A-2. MPC5554 / MPC5553 Detailed Register Map (continued)

| Register Description   | Register Name   | Used Size   | Address                                                          | Reference   |
|------------------------|-----------------|-------------|------------------------------------------------------------------|-------------|
| Message buffer 58      | MB58            | 16-bit      | Base + 0x0420                                                    |             |
| Message buffer 59      | MB59            | 16-bit      | Base + 0x0430                                                    |             |
| Message buffer 60      | MB60            | 16-bit      | Base + 0x0440                                                    |             |
| Message buffer 61      | MB61            | 16-bit      | Base + 0x0450                                                    |             |
| Message buffer 62      | MB62            | 16-bit      | Base + 0x0460                                                    |             |
| Message buffer 63      | MB63            | 16-bit      | Base + 0x0470                                                    |             |
| Reserved               | -               | -           | (Base + 0x0480)- 0xFFFC_3FFF (A) 0xFFFC_7FFF (B) 0xFFFF_FFFF (C) | -           |

- 1 The registers mapped in the ECSM module (0xFFF4\_0014-0xFFF4\_001F) provide control and configuration for a software watchdog timer, and are included as part of a standard Freescale ECSM block incorporated in the MPC5554. The eSys e200z6 core also provides this functionality and is the preferred method for watchdog implementation. In order to optimize code portability to other members of the eSys MPU family, use of the watchdog registers in the ECSM is not recommended.
- 2 MPC5554 Only

Table A-3. e200z6 Core SPR Numbers (Supervisor Mode)

| Register                             | Description                             | SPR (decimal)                        |
|--------------------------------------|-----------------------------------------|--------------------------------------|
| General Registers                    | General Registers                       | General Registers                    |
| XER                                  | Integer Exception Register              | 1                                    |
| LR                                   | Link Register                           | 8                                    |
| CTR                                  | Count Register                          | 9                                    |
| GPR0-GPR31                           | General Purpose Registers               | N/A                                  |
| Special Purpose Registers            | Special Purpose Registers               | Special Purpose Registers            |
| SPRG0                                | Special Purpose Register 0              | 272                                  |
| SPRG1                                | Special Purpose Register 1              | 273                                  |
| SPRG2                                | Special Purpose Register 2              | 274                                  |
| SPRG3                                | Special Purpose Register 3              | 275                                  |
| SPRG4                                | Special Purpose Register 4              | 276                                  |
| SPRG5                                | Special Purpose Register 5              | 277                                  |
| SPRG6                                | Special Purpose Register 6              | 278                                  |
| SPRG7                                | Special Purpose Register 7              | 279                                  |
| USPRG0                               | User Special Purpose Register           | 256                                  |
| BUCSR                                | Branch Unit Control and Status Register | 1013                                 |
| Exception Handling/Control Registers | Exception Handling/Control Registers    | Exception Handling/Control Registers |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table A-3. e200z6 Core SPR Numbers (Supervisor Mode)  (continued)

| Register                    | Description                          | SPR (decimal)               |
|-----------------------------|--------------------------------------|-----------------------------|
| SRR0                        | Save and Restore Register 0          | 26                          |
| SRR1                        | Save and Restore Register 1          | 27                          |
| CSRR0                       | Critical Save and Restore Register 0 | 58                          |
| CSRR1                       | Critical Save and Restore Register 1 | 59                          |
| DSRR0                       | Debug Save and Restore Register 0    | 574                         |
| DSRR1                       | Debug Save and Restore Register 1    | 575                         |
| ESR                         | Exception Syndrome Register          | 62                          |
| MCSR                        | Machine Check Syndrome Register      | 572                         |
| DEAR                        | Data Exception Address Register      | 61                          |
| IVPR                        | Interrupt Vector Prefix Register     | 63                          |
| IVOR1                       | Interrupt Vector Offset Register 1   | 401                         |
| IVOR2                       | Interrupt Vector Offset Register 2   | 402                         |
| IVOR3                       | Interrupt Vector Offset Register 3   | 403                         |
| IVOR4                       | Interrupt Vector Offset Register 4   | 404                         |
| IVOR5                       | Interrupt Vector Offset Register 5   | 405                         |
| IVOR6                       | Interrupt Vector Offset Register 6   | 406                         |
| IVOR7                       | Interrupt Vector Offset Register 7   | 407                         |
| IVOR8                       | Interrupt Vector Offset Register 8   | 408                         |
| IVOR9                       | Not Supported                        | -                           |
| IVOR10                      | Interrupt Vector Offset Register 10  | 410                         |
| IVOR11                      | Interrupt Vector Offset Register 11  | 411                         |
| IVOR12                      | Interrupt Vector Offset Register 12  | 412                         |
| IVOR13                      | Interrupt Vector Offset Register 13  | 413                         |
| IVOR14                      | Interrupt Vector Offset Register 14  | 414                         |
| IVOR15                      | Interrupt Vector Offset Register 15  | 415                         |
| IVOR32                      | Interrupt Vector Offset Register 32  | 528                         |
| IVOR33                      | Interrupt Vector Offset Register 33  | 529                         |
| IVOR34                      | Interrupt Vector Offset Register 34  | 530                         |
| Processor Control Registers | Processor Control Registers          | Processor Control Registers |
| MSR                         | Machine State Register               | N/A                         |
| PVR                         | Processor Version Register           | 287                         |
| PIR                         | Processor ID Register                | 286                         |
| SVR                         | System Version Register              | 1023                        |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table A-3. e200z6 Core SPR Numbers (Supervisor Mode)  (continued)

| Register                    | Description                                  | SPR (decimal)               |
|-----------------------------|----------------------------------------------|-----------------------------|
| HID0                        | Hardware Implementation Dependent Register 0 | 1008                        |
| HID1                        | Hardware Implementation Dependent Register 1 | 1009                        |
| Timer Registers             | Timer Registers                              | Timer Registers             |
| TBL                         | Time Base Lower Register                     | 284                         |
| TBU                         | Time Base Upper Register                     | 285                         |
| TCR                         | Timer Control Register                       | 340                         |
| TSR                         | Timer Status Register                        | 336                         |
| DEC                         | Decrementer Register                         | 22                          |
| DECAR                       | Decrementer Auto-reload Register             | 54                          |
| Debug Registers             | Debug Registers                              | Debug Registers             |
| DBCR0                       | Debug Control Register 0                     | 308                         |
| DBCR1                       | Debug Control Register 1                     | 309                         |
| DBCR2                       | Debug Control Register 2                     | 310                         |
| DBCR3                       | Debug Control Register 3                     | 561                         |
| DBSR                        | Debug Status Register                        | 304                         |
| DBCNT                       | Debug Counter Register                       | 562                         |
| IAC1                        | Instruction Address Compare Register 1       | 312                         |
| IAC2                        | Instruction Address Compare Register 2       | 313                         |
| IAC3                        | Instruction Address Compare Register 3       | 314                         |
| IAC4                        | Instruction Address Compare Register 4       | 315                         |
| DAC1                        | Data Address Compare Register 1              | 316                         |
| DAC2                        | Data Address Compare Register 2              | 317                         |
| Memory Management Registers | Memory Management Registers                  | Memory Management Registers |
| MAS0                        | MMU Assist Register 0                        | 624                         |
| MAS1                        | MMU Assist Register 1                        | 625                         |
| MAS2                        | MMU Assist Register 2r                       | 626                         |
| MAS3                        | MMU Assist Register 3                        | 627                         |
| MAS4                        | MMU Assist Register 4                        | 628                         |
| MAS6                        | MMU Assist Register 6                        | 630                         |
| PID0                        | Process ID Register                          | 48                          |
| MMUCSR0                     | MMU Control and Status Register 0            | 1012                        |
| MMUCFG                      | MMU Configuration Register                   | 1015                        |
| TLB0CFG                     | TLB 0 Configuration Register                 | 688                         |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table A-3. e200z6 Core SPR Numbers (Supervisor Mode)  (continued)

| Register        | Description                                      | SPR (decimal)   |
|-----------------|--------------------------------------------------|-----------------|
| TLB1CFG         | TLB 1 Configuration Register                     | 689             |
| Cache Registers | Cache Registers                                  | Cache Registers |
| L1CFG0          | L1 Cache Configuration Register                  | 515             |
| L1CSR0          | L1 Cache Control and Status Register 0           | 1010            |
| L1FINV0         | L1 Cache Flush and Invalidate Control Register 0 | 1016            |
| APU Registers   | APU Registers                                    | APU Registers   |
| SPEFSCR         | SPE APU Status and Control Register              | 512             |

Table A-4. e200z6 Core SPR Numbers (User Mode)

| Register                  | Description                         | SPR (decimal)             |
|---------------------------|-------------------------------------|---------------------------|
| General Registers         | General Registers                   | General Registers         |
| CTR                       | Count Register                      | 9                         |
| LR                        | Link Register                       | 8                         |
| XER                       | Integer Exception Register          | 1                         |
| GPR0-GPR31                | General Purpose Registers           | N/A                       |
| Special Purpose Registers | Special Purpose Registers           | Special Purpose Registers |
| SPRG4                     | Special Purpose Register 4          | 260                       |
| SPRG5                     | Special Purpose Register 5          | 261                       |
| SPRG6                     | Special Purpose Register 6          | 262                       |
| SPRG7                     | Special Purpose Register 7          | 263                       |
| USPRG0                    | User Special Purpose Register       | 256                       |
| Timer Registers           | Timer Registers                     | Timer Registers           |
| TBL                       | Time Base Lower Register            | 268                       |
| TBU                       | Time Base Upper Register            | 269                       |
| Cache Registers           | Cache Registers                     | Cache Registers           |
| L1CFG0                    | L1 Cache Configuration Register     | 515                       |
| APU Registers             | APU Registers                       | APU Registers             |
| SPEFSCR                   | SPE APU Status and Control Register | 512                       |

## A.1 Revision History

## Substantive Changes since Rev 3.0

For the FEC module, changed MDATA to MMFR as well as name of register to MII Management Frame Regsiter.

## Appendix B Calibration

## B.1 Overview

The MPC5500 family of microcontrollers includes various specialized features to support automotive calibration.  Many  of  these  calibration  features  are  not  intended  to  be  available  for  use  by  the  final application software, and some MPC5500 devices support calibration signals which are not available in the standard 208, 324, and 416 BGA packages. Special calibration packaged devices with increased signal bond out are used to provide full access to all calibration resources for all MPC5500 variants.

Calibration hardware which makes use of these calibration packaged devices is detailed in Figure B-1. Freescale-produced 'VertiCal bases' use the calibration-packaged MPC5500 device mounted on a small circuit board with a footprint which is compatible with that of the production BGA packaged MPC5500 device. A 156 way 'VertiCal connector' on the top side of the VertiCal base allows VertiCal compliant 'top board' hardware to be attached. Various types of top board hardware to support calibration and debug is available from Freescale and 3 rd parties.

The VertiCal connector standard defines a set of signals which are used for communication between the microcontroller on the VertiCal Base Board and any attached calibration tools or 'top boards'. There are some differences in signal availability or sourcing for the VertiCal connector depending on the MPC5500 device variant being used.

The calibration system is illustrated in Figure B-1 and the VertiCal Base is illustrated in Figure B-2.

Figure B-1. Calibration System

<!-- image -->

Figure B-2. VertiCal Base

<!-- image -->

<!-- image -->

## B.2 Calibration Bus

The calibration bus is made up of address bus, data bus, bus control and clock signals, and is used by any tool which includes additional memory to hold calibration data or other code or data being developed. See Table B-1 for calibration bus signals. A 16-bit data bus and 19-bit address bus is included giving a basic addressing range of 1 MByte. Alternatively, the maximum memory addressable using just one chip select is 4 Mbytes. Refer to Table B-2.

The VertiCal connector supports up to 4 chip selects signals, although the actual number of chip selects available  depends  on  which  device  of  the  MPC5500  family  is  used.  The  CAL\_CS[0]  chip  select  is available for all MPC5500 devices, and should be used as the default chip select for calibration use to ensure maximum portability of calibration tools across devices. These additional chip selects signals are configured and function like the non-calibration chip selects. The four chip selects, CAL\_CS[0:3], have a higher priority in address decoding than the non-calibration chip selects, CS[0:3]. Refer to Section B.6, 'Application Information,' for application information on the number of calibration chip selects.

The additional CAL\_CS[0:3] chip selects also have alternate functions as additional address bits, allowing a flexible choice between increased addressing range or increased chip select availability. Devices which support less than 4 calibration chip selects are designed to support this means of extending the contiguous calibration addressing range by omitting chip selects starting from CS1. For this reason CS1 is selected as the single unimplemented chip select on the MPC5553.

Table B-1. Calibration Bus Signals

| VertiCal Signal Name    | Function                 | Device Implementation Signal Name   | Device Implementation Signal Name              |
|-------------------------|--------------------------|-------------------------------------|------------------------------------------------|
| VertiCal Signal Name    | Function                 | MPC5554                             | MPC5553                                        |
| Address/Data Bus (44)   | Address/Data Bus (44)    | Address/Data Bus (44)               | Address/Data Bus (44)                          |
| CAL_ADDR[12:26]         | Address bus              | ADDR[12:26]_ GPIO[8:22]             | ADDR[12:26]_ GPIO[8:22]                        |
| CAL_ADDR[27:30]         | Address bus              | ADDR[27:30]_ GPIO[23:26]            | ADDR[8:11]_ CAL_ADDR[27:30]_ GPIO[4:7]         |
| CAL_CS[3]               | Chip Selects             | CS[3]_ ADDR[11]_ GPIO[3]            | CAL_ADDR11_ MDIO_CAL_CS3_ GPIO73               |
| CAL_CS[2]               | Chip Select              | CS[2]_ ADDR[10]_ GPIO[2]            | CAL_ADDR10_ MDC_CAL_CS2_ GPIO72                |
| CAL_CS[1]               | Chip Select              | CS[1]_ ADDR[9]_ GPIO[1]             | No Connect                                     |
| CAL_CS[0]               | Chip Select              | CS[0]_ ADDR[8]_ GPIO[0]             | TEA_CAL_CS0_ GPIO71                            |
| CAL_DATA[0:15]          | Data Bus                 | DATA[0:15]_ GPIO[28:43]             | DATA[16:31]_ a _ CAL_DATA[0:15]_ GPIO[44:59] 1 |
| CAL_OE                  | Output Enable            | OE_GPIO68                           | OE_GPIO68                                      |
| CAL_RD_WR               | Read/Write               | RD_WR_ GPIO62                       | RD_WR_ GPIO62                                  |
| CAL_TS                  | Transfer Start           | TS_GPIO69                           | TS_GPIO69                                      |
| CAL_WE[0:1] CAL_BE[0:1] | Write Enable Byte Enable | WE[0:1]_ BE[64:65]_ GPIO[64:65]     | WE[2:3]_BE[2:3]_ CAL_WE[0:1]_ GPIO[66:67]      |
| Clock Synthesizer (1)   | Clock Synthesizer (1)    | Clock Synthesizer (1)               | Clock Synthesizer (1)                          |
| CLKOUT                  | System Clock Output      | CLKOUT                              | CLKOUT                                         |

1 For these signals, ' a ' refers to the alternate function, see Table 2-1 for these alternate pin functions.

## B.3 Device Specific Information

The  various  address  bus,  data  bus  and  bus  control  signals  are  sourced  from  different  device  signals depending on the MPC5500 family being used as detailed in the following sections.

## B.3.1 MPC5554 Calibration Bus Implementation

On the MPC5554 device there are no signals dedicated for calibration usage, and instead signals which are available for normal application usage must be shared for calibration. The calibration bus signals on the VertiCal connector (CAL\_DATA, CAL\_ADDR, CAL\_CS etc.) are connected to the equivalent signals on the standard MPC5554 EBI. To allow calibration, all of the MPC5554 EBI signals included in the VertiCal connector and used by attached VertiCal top board must be available and configured for their primary EBI mode of operation. This requirement prohibits the use of required EBI signals as general purpose IO (GPIO)  by  the  application.  If  the  application  itself  uses  the  EBI  to  access  external  memory  mapped devices, the application design must ensure that sufficient resources such as chip selects and addressing range are left available for calibration use. Since the calibration bus is shared with the standard device system bus, the bus loading of the pins may need to be adjusted for pins that are connected to both the standard bus and the calibration bus. The bus load for each signal is adjustable in the Pad Configuration Register for that pin.

## B.3.2 MPC5553 Calibration Bus Implementation

The MPC5553 device is similar to the MPC5554 in that no signals are dedicated for calibration usage. Instead,  signals  which  are  available  for  normal  application  usage  must  be  shared  for  calibration.  The MPC5553 differs in that the calibration bus signals on the VertiCal connector are not all directly connected to the equivalent signals on the standard EBI. Instead some calibration pins are implemented as secondary functions on pins that are not normally needed. The purpose of this is to minimize the number of signals which must be reserved for calibration on applications which use the 324 BGA packaged device.

## B.4 Signals and Pads

The following sections detail the signal descriptions for the calibration bus.

## B.4.1 CAL\_CS[0:3] - Calibration Chip Selects 0 - 3

CAL\_CS[n] is asserted by the master to indicate that this transaction is targeted for a particular calibration memory bank.

The calibration chip selects are driven by the EBI. CAL\_CS[n] is driven in the same clock as the assertion of TS and valid address, and is kept valid until the cycle is terminated. Bus timing is identical to standard EBI timing.

## B.4.1.1 Number of Chip Selects and Maximum Memory Size

The trade-off  between  calibration  chip  selects  and  address  lines  is  the  same  as  the  trade-off  between non-calibration chip selects and address lines for the 324 pin package.

Table B-2. Number of Calibration Chip Selects Versus Memory Size

| CAL_CS[0]   | CAL_CS[2]/ CAL_ADDR[10]   | CAL_CS[3]/ CAL_ADDR[11]   |   CAL_CS[0] maximum memory size (Mbytes) | CAL_CS[2] maximum memory size (Mbytes)   | CAL_CS[3] maximum memory size (Mbytes)   |
|-------------|---------------------------|---------------------------|------------------------------------------|------------------------------------------|------------------------------------------|
| CAL_CS[0]   | CAL_ADDR[10]              | CAL_ADDR[11]              |                                        4 | -                                        | -                                        |
| CAL_CS[0]   | CAL_CS[2]                 | CAL_ADDR[11]              |                                        2 | 2                                        | -                                        |
| CAL_CS[0]   | CAL_CS[2]                 | CAL_CS[3]                 |                                        1 | 1                                        | 1                                        |

## B.4.2 Pad Ring

This section provides a list  of  the  calibration  pins  and  associated  pad  configuration  registers  (PCRs), including links to the detailed PCR information for each pin or pin group.

Refer to Table B-1 for device signal names.

For MPC5553, see:

- · CAL\_ADDR[27:30]: Section 6.3.1.12.2, 'MPC5553: Pad Configuration Registers 4 - 7 (SIU\_PCR4 - SIU\_PCR7),' on page 6-21
- · CAL\_DATA[0:15]: Section 6.3.1.12.5, 'MPC5553: Pad Configuration Register 44 (SIU\_PCR44),' on page 6-23 through Section 6.3.1.12.20, 'MPC5553: Pad Configuration Register 59 (SIU\_PCR59),' on page 6-31
- · CAL\_WE[0:1]\_CAL\_BE[0:1]: Section 6.3.1.12.25, 'MPC5553: Pad Configuration Registers 66 67 (SIU\_PCR66 - SIU\_PCR67),' on page 6-33
- · CAL\_CS[0]: Section 6.3.1.12.30, 'MPC5553: Pad Configuration Register 71 (SIU\_PCR71),' on page 6-36
- · CAL\_CS[2]: Section 6.3.1.12.32, 'MPC5553: Pad Configuration Register 72 (SIU\_PCR72),' on page 6-38
- · CAL\_CS[3]: Section 6.3.1.12.34, 'MPC5553: Pad Configuration Register 73 (SIU\_PCR73),' on page 6-39
- · CLKOUT: Section 6.3.1.12.114, 'Pad Configuration Register 229 (SIU\_PCR229),' on page 6-78

## For MPC5554, see:

- · Address Bus pins: Section 6.3.1.12.3, 'MPC5554: Pad Configuration Registers 4 - 27 (SIU\_PCR4 - SIU\_PCR27),' on page 6-21
- · Data Bus pins: Section 6.3.1.12.4, 'Pad Configuration Registers 28 - 59 (SIU\_PCR28 -SIU\_PCR59),' on page 6-22
- · CAL\_WE[0:1]\_CAL\_BE[0:1]: Section 6.3.1.12.26, 'MPC5554: Pad Configuration Registers 64 67 (SIU\_PCR64 - SIU\_PCR67),' on page 6-34
- · Chip Selects CS[0:3]: Section 6.3.1.12.1, 'Pad Configuration Registers 0 - 3 (SIU\_PCR0 -SIU\_PCR3),' on page 6-20
- · CLKOUT: Section 6.3.1.12.114, 'Pad Configuration Register 229 (SIU\_PCR229),' on page 6-78

The drive strength of the calibration pins may be adjusted in the PCRs.

## B.4.3 CLKOUT

CLKOUT is supplied by the clock control block, not the EBI. Nevertheless, the same CLKOUT is used for both the non-calibration and calibration bus.

A drawback of having just one CLKOUT is that while the difference in board timing can be compensated by the adjustment in the drive strength, the CLKOUT timing, and hence the timing of the non-calibration bus, can have minor differences with a calibration tool from the production package.

## B.5 Packaging

The addition of the calibration bus means that the device has more pads than can be connected to the balls on a 416 pin package. Therefore, the die is assembled in a 496 pin chip scale package (CSP) and this package is used in the VertiCal base assembly.

## B.6 Application Information

## B.6.1 Communication With Development Tool Using I/O

The development tool can require some I/Os for communication between the MCU and the development tool on the VertiCal connector. ETRIG[0:1] and GPIO[205] are available only in the 416 pin package. Since the application can not use these pins in the 208 and 324 pin packages, they are candidates for development tool use in a VertiCal connector. Using ETRIG[1] and GPIO[205] still leaves ETRIG[0] for the application in the 416 package.

## B.6.2 Matching Access Delay to Internal Flash With Calibration Memory

One use of VertiCal in the Automotive environment is engine calibration. For this application, an SRAM Top Board is added onto the VertiCal connector. This allows the engine calibrator to modify settings in SRAM, possibly using the Nexus interface or even by using the SCI port or a CAN interface.

See Table 13-2 'Internal Flash External Emulation Mode.'

After the data is calibrated, it can be copied into the internal flash. The internal flash can be accessed faster than the calibration memory and this change in calibration data access time could change the overall system performance. To mitigate this change in system performance, the internal flash memory includes a feature that allows accesses to portions of the flash to be slowed down by adding extra wait states. This is done by multiply mapping the internal flash at different locations with different number of wait states. For example, the physical address of the flash array is 0x0000\_0000 to 0x00FF\_FFFF (depending on array size). That same flash data can be accessed at address 0x0100\_0000 to 0x01FF\_FFFF but accesses will be 1 clock cycle slower. That same flash data can be accessed at addresses 0x0200\_0000 to 0x02FF\_FFFF but accesses will be 2 clock cycles slower. This pattern is repeated through the memory map to addresses 0x1F00\_0000 to 0x1FFF\_FFFF where accesses will be 31 clock cycles slower.

The application would use this feature by mapping the calibration data to a region of the flash memory that has  access  timing  to  match  the  timing  of  the  calibration  RAM  used  when  calibrating  the  data.  This remapping of calibration data can be achieved by either using the translation feature of the MMU or rebuilding the code with a modified link file.

## B.7 Revision History

Substantive Changes since Rev 3.0

Initial release of Appendix B, 'Calibration.'