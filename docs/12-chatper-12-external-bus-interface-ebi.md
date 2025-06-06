### Chatper 12 External Bus Interface (EBI)

## 12.1 Introduction

This chapter describes the external bus interface (EBI) of the MPC5553/MPC5554, which handles the transfer of information between the internal buses and the memories or peripherals in the external address space and enables an external master to access internal address space. For an overview of how the EBI used in the MPC5553/MPC5554 differs from the EBI used in MPC5xx devices, refer to Section 12.5.6, 'Summary of Differences from MPC5xx.'

## 12.1.1 Block Diagram

Figure 12-1 is a block diagram of the EBI. The signals shown are external pins to the MCU. All signals are implemented in the MPC5554 and in the 416 and 324 BGA of the MPC5553 except where noted . The MPC5553 208 BGA does not have EBI signals pinned out.

Figure 12-1. EBI Block Diagram

<!-- image -->

## 12.1.2 Overview

The EBI includes a memory controller that generates interface signals to support a variety of external memories. This includes single data rate (SDR) burst mode Flash, external SRAM, and asynchronous memories. It supports up to four regions (via chip selects), each with its own programmed attributes.

## 12.1.3 Features

Features include the following:

- · 1.8-3.3 V I/O
- · 32-bit address bus with transfer size indication, but
- - 24 bits available in the MPC5554 and in the MPC5553 416 BGA package
- - Only 20 bits available in the MPC5553 324 BGA package
- - No external bus in the MPC5553 208 BGA package
- - Table 12-1 shows the address bus packages supported:

## Table 12-1. Address Bus Size in MPC5554 and MPC5553

|          | MPC5553       | MPC5553   | MPC5553   |
|----------|---------------|-----------|-----------|
|          | MPC5554 416   | 324       | 208       |
| Bus Size | 24 bit 24 bit | 20 bit    | None      |

- · 32-bit data bus available for both external memory accesses and transactions involving an external master, but
- - 32 bits available in the MPC5554 and in the MPC5553 416 BGA package
- - 16 bits available in the MPC5553 324 BGA package
- - No external bus in the MPC5553 208 BGA package
- - Table 12-2 shows the data bus packages supported:
- 1 In both the MPC5554 and in the 416 BGA of the MPC5553, a 16-bit mode is available. See Section 12.1.4.5, '16-Bit Data Bus Mode.'
- · Support for external master accesses to internal addresses (MPC5554 only)
- · Memory controller with support for various memory types:
- - Synchronous burst SDR Flash
- - Asynchronous/legacy Flash
- · Burst support (wrapped only)
- · Bus monitor
- · Port size configuration per chip select (16 or 32 bits)
- · Configurable wait states
- · Four chip select (CS[0:3]) signals; but the MPC5553 has no CS signals in the 208 BGA package.
- · Support for dynamic calibration with up to three calibration chip selects (CAL\_CS[0] and CAL\_CS[2:3])(MPC5553 only)

Table 12-2. Data Bus Size in MPC5554 and MPC5553

|          | MPC5553   | MPC5553   | MPC5553   | MPC5553   |
|----------|-----------|-----------|-----------|-----------|
|          | MPC5554   | 416       | 324       | 208       |
| Bus Size | 32 bit    | 32 bit    | None      | None      |
| Bus Size | 16 bit 1  | 16 bit 1  | 16 bit    | None      |

- · Write/byte enable (WE[0:3]/BE[0:3]) signals
- - The MPC5554 has four WE/BE signals  (WE[0:3]/BE[0:3])
- - The MPC5553 has the following WE/BE signals depending on the package:
- -416 BGA: four WE/BE signals  (WE[0:3]/BE[0:3])
- -324 BGA: two WE/BE signals (WE[0:1]/BE[0:1])
- -208 BGA: no WE/BE signals
- · Configurable bus speed modes (1/2 or 1/4 of system clock frequency)
- · Module disable modes for power savings
- · Optional automatic CLKOUT gating to save power and reduce EMI (not available on 208 BGA of MPC5553)
- · Compatible with MPC5xx external bus (See Section 12.4.1.18, 'Compatible with MPC5xx External Bus (with Some Limitations).')

## 12.1.4 Modes of Operation

The mode of the EBI is determined by the MDIS and EXTM bits in the EBI\_MCR. See Section 12.3.1.3, 'EBI Module Configuration Register (EBI\_MCR)' for details. Configurable bus speed modes and debug mode  are  modes  that  the  MCU  may  enter,  in  parallel  to  the  EBI  being  configured  in  one  of  its module-specific modes.

## 12.1.4.1 Single Master Mode

In single master mode, the EBI responds to internal requests matching one of its regions, but ignores all externally-initiated  bus  requests.  The  MCU  is  the  only  master  allowed  to  initiate  transactions  on  the external bus in this mode; therefore, it acts as a parked master and does not have to arbitrate for the bus before starting each cycle. The BR, BG, and BB signals are not used by the EBI in this mode, and are available for use in an alternate function by another module of the MCU. Single master mode is entered when EXTM = 0 and MDIS = 0 in the EBI\_MCR.

## 12.1.4.2 External Master Mode

When the MPC5554 is in external master mode, the EBI responds to internal requests matching one of its regions, and also to external master accesses to internal address space. In this mode, the BR, BG, and BB signals are all used by the EBI to handle arbitration between the MCU and an external master. External master mode is entered when EXTM = 1 and MDIS = 0 in the EBI\_MCR register.

External master mode support is limited in the MPC5553. See Section 12.5.5, 'Dual-MCU Operation with Reduced Pinout MCUs.'

External master mode operation is described in Section 12.4.2.10, 'Bus Operation in External Master Mode.'

## 12.1.4.3 Module Disable Mode

The module disable mode is used for MCU power management. The clock to the non-memory mapped logic in the EBI is stopped while in module disable mode. Requests (other than to memory-mapped logic) must not be made to the EBI while it is in module disable mode, even if the clocks have not yet been shut off.  In  this  case,  the  behavior  is  undefined.  Module  disable  mode  is  entered  when  MDIS = 1  in  the EBI\_MCR.

## 12.1.4.4 Configurable Bus Speed Modes

In configurable bus speed modes, the external CLKOUT frequency is divided down from the internal system clock. The EBI behavior remains dictated by the mode of the EBI, except that the EBI drives and samples signals at the scaled CLKOUT rather than the internal system clock. This mode is selected by writing  the  external  clock  control  register  in  the  system  integration  module  (SIU\_ECCR).  The configurable bus speed modes supports both 1/2 or 1/4 speed modes, meaning that the external CLKOUT frequency is scaled down (by 2 or 4) compared with that of the internal system clock, which is unchanged.

## NOTE

In a multi-master system (where the PLL is in dual-controller mode) only 1/2 speed mode is supported.

## 12.1.4.5 16-Bit Data Bus Mode

For MCUs that have only 16 data bus signals pinned out, or for systems where the use of a different multiplexed function (e.g. GPIO) is desired on 16 of the 32 data pins, the EBI supports a 16-bit data bus mode. In this mode, DATA[0:15] are the only data signals used by the EBI.

For EBI-mastered accesses, the operation in 16-bit data bus mode (EBI\_MCR[DBM] = 1, EBI\_BR [PS] = x)  is  similar  to  a  chip  select  access  to  a  16-bit  port  in  32-bit  data  bus  mode n (EBI\_MCR[DBM] = 0, EBI\_BR [PS] = 1), except for the case of an EBI-mastered non-chip select access n of exactly 32-bit size.

External master accesses and EBI-mastered non-chip select accesses of exactly 32-bit size are supported via a two (16-bit) beat burst for both reads and writes. See Section 12.4.2.11, 'Non-Chip-Select Burst in 16-bit Data Bus Mode.' Non-chip select transfers of non-32-bit size are supported in standard non-burst fashion.

16-bit data bus mode is entered when EBI\_MCR[DBM] = 1. Note that DBM = 0 out of reset.

## 12.1.4.6 Debug Mode

When the MCU is in debug mode, the EBI behavior is unaffected and remains dictated by the mode of the EBI.

## 12.2 External Signal Description

Table 12-3 alphabetically lists the external signals used by the EBI.

Table 12-3. Signal Properties

| Name        | I/O Type   | Function               | Pull 1   | MPC5553 Package   | MPC5554   |
|-------------|------------|------------------------|----------|-------------------|-----------|
| ADDR[8:11]  | I/O        | Address Bus            | -        | 416               | Yes       |
| ADDR[12:31] | I/O        | Address Bus            | -        | 416, 324          | Yes       |
| BB          | I/O        | Bus Busy               | Up       | None              | Yes       |
| BDIP        | Output     | Burst Data in Progress | Up       | 416, 324          | Yes       |
| BG          | I/O        | Bus Grant              | Up       | None              | Yes       |
| BR          | I/O        | Bus Request            | Up       | None              | Yes       |

Table 12-3. Signal Properties (continued)

| Name                  | I/O Type   | Function                   | Pull 1   | MPC5553 Package   | MPC5554   |
|-----------------------|------------|----------------------------|----------|-------------------|-----------|
| CLKOUT 2              | Output     | Clockout                   | -        | 416, 324          | Yes       |
| CS[0:3]               | Output     | Chip Selects               | Up       | 416, 324          | Yes       |
| CAL_CS[0] CAL_CS[2:3] | Output     | Calibration Chip Selects   | Up       | 416, 324          | No        |
| DATA[0:15]            | I/O        | Data Bus                   | -        | 416, 324          | Yes       |
| DATA[16:31]           | I/O        | Data Bus                   | -        | 416               | Yes       |
| OE                    | Output     | Output Enable              | Up       | 416, 324          | Yes       |
| RD_WR                 | I/O        | Read_Write                 | Up       | 416, 324          | Yes       |
| TA                    | I/O        | Transfer Acknowledge       | Up       | 416, 324          | Yes       |
| TEA                   | I/O        | Transfer Error Acknowledge | Up       | 416               | Yes       |
| TS                    | I/O        | Transfer Start             | Up       | 416, 324          | Yes       |
| TSIZ[0:1]             | I/O        | Transfer Size              | -        | None              | Yes       |
| WE[0:1]/BE[0:1]       | Output     | Write/Byte Enables         | Up       | 416, 324          | Yes       |
| WE[2:3]/BE[2:3]       | Output     | Write/Byte Enables         | Up       | 416               | Yes       |

1 This column shows which signals require a weak pull-up or pull-down. The EBI module does not contain these pull-up/pull-down devices within the module, but instead are controlled by the pad configuration registers in the System Integration Module (SIU\_PCRs).

2 The CLKOUT signal is driven by the FMPLL Module.

## 12.2.1 Detailed Signal Descriptions

The MPC5554 and the 416 and 324 BGA packages of the MPC5553 have pinned out EBI signals. The 208 BGA package of the MPC5553 does not pin out these signals.

## 12.2.1.1 Address Lines 8-31 (ADDR[8:31])

The  ADDR[8:31]  signals  specify  the  physical  address  of  the  bus  transaction.  The  24  address  lines correspond to bits 8-31 of the EBI's 32-bit internal address bus. Bits 0-7 are internally driven by the EBI for externally initiated accesses depending on which internal slave is to be accessed. See Section 12.4.2.10.1, 'Address Decoding for External Master Accesses,' for more details. ADDR[8:31] is driven by the EBI or an external master depending on who owns the external bus.

Note that the 324 package of the MPC5553 uses only ADDR[12:31].

## 12.2.1.2 Bus Busy (BB) - MPC5554 Only

BB is asserted to indicate that the current bus master is using the bus. The BB signal is only used by the EBI when the EBI is in external master mode. In single master mode, the BB signal is never asserted or sampled by the EBI.

When configured for internal arbitration, the EBI asserts BB to indicate that it is currently using the bus. An external master must not begin a transfer until this signal is negated for two cycles. The EBI does not

negate this signal until its transfer is complete. When not driving BB, the EBI samples this signal to get an indication of when the external master is no longer using the bus (BB negated for two cycles).

When configured for external arbitration, the EBI asserts this signal when it is ready to start the transaction after the external arbiter has granted ownership of the bus to the MCU. When not driving BB, the EBI samples this signal to properly qualify the BG line when an external bus transaction is to be executed by the MCU.

## 12.2.1.3 Burst Data in Progress (BDIP)

BDIP is asserted to indicate that the master is requesting another data beat following the current one.

BDIP is driven by the EBI or an external master depending on who owns the external bus. This signal is driven by the EBI on all EBI-mastered external burst cycles, but is only sampled by burst mode memories that have a corresponding pin. See Section 12.4.2.5, 'Burst Transfer.'

## 12.2.1.4 Bus Grant (BG) - MPC5554 Only

BG is asserted to grant ownership of the external bus to the requesting master. The BG signal is only used by the EBI when the EBI is in external master mode. In single master mode, the BG signal is never asserted or sampled by the EBI.

When configured for internal arbitration, BG is output only and is asserted by the EBI to indicate that an external  master  may  assume  ownership  of  the  bus.  The  BG  signal  should  be  qualified  by  the  master requesting the bus in order to ensure it is the bus owner before beginning a bus transaction: Qualified bus grant = BG and ~BB. The EBI negates BG following the negation of BR if it has an internal request for the external bus pending. Otherwise, it keeps BG asserted to park the bus for the external master. The parked  external  master  could  then  assert  BB  to  run  subsequent  transactions  without  the  normal requirement to assert BR.

When configured for external arbitration, BG is input only and is sampled and qualified (Qualified BG = ~ BB and BG) by the EBI when an external bus transaction is to be executed by the MCU.

## 12.2.1.5 Bus Request (BR) - MPC5554 Only

BR is asserted to request ownership of the external bus. The BR signal is only used by the EBI when the EBI is in external master mode. In single master mode, the BR signal is never asserted or sampled by the EBI.

When configured for internal arbitration, BR is input only and is asserted by an external master when it is requesting the bus.

When configured for external arbitration, BR is output only and is asserted by the EBI when it is requesting the bus. The EBI negates BR as soon as it is granted the bus and the bus is not busy, provided it has no other internal requests pending. If more requests are pending, the EBI keeps BR asserted as long as needed.

## 12.2.1.6 Clockout (CLKOUT)

CLKOUT is a general-purpose clock output signal to connect to the clock input of SDR external memories and in some cases to the input clock of another MCU in multi-master configurations.

## 12.2.1.7 Chip Selects 0-3 (CS[0:3])

CSx is asserted by the master to indicate that this transaction is targeted for a particular memory bank.

The chip selects are driven by the EBI or an external master depending on who owns the external bus. CS is driven in the same clock as the assertion of TS and valid address, and is kept valid until the cycle is terminated.  See  Section 12.4.1.5,  'Memory  Controller  with  Support  for  Various  Memory  Types'  for details on chip select operation.

## 12.2.1.8 Calibration Chip Selects 0, 2-3 (CAL\_CS [0], CAL\_CS [2:3]) - MPC5553 Only

CAL\_CSx is asserted by the master to indicate that this transaction is targeted for a particular memory bank on the calibration external bus.

The calibration chip selects are driven only by the EBI. External master accesses on the calibration bus are not supported. In all other aspects, the calibration chip selects behave exactly as the primary chip selects. See Section 12.4.1.5, 'Memory Controller with Support for Various Memory Types  for details on chip select operation.

## 12.2.1.9 Data Lines 0-31 (DATA[0:31])

In  the  416-pin  package  of  the  MPC5553/MPC5554,  the  DATA[0:31]  signals  contain  the  data  to  be transferred for the current transaction. In the 324-pin package of the MPC5553, DATA[0:15] carry the data.

DATA[0:31] is driven by the EBI when it owns the external bus and it initiates a write transaction to an external device. The EBI also drives DATA[0:31] when an external master owns the external bus and initiates a read transaction to an internal module.

DATA[0:31] is driven by an external device during a read transaction from the EBI. An external master drives DATA[0:31] when it owns the bus and initiates a write transaction to an internal module or shared external memory.

For 8-bit and 16-bit transactions, the byte lanes not selected for the transfer do not supply valid data.

## 12.2.1.10 Output Enable (OE)

OE is used to indicate when an external memory is permitted to drive back read data. External memories must have their data output buffers off when OE is negated. OE is only asserted for chip select accesses.

OE is driven by the EBI or an external master depending on who owns the external bus. For read cycles, OE is asserted one clock after TS assertion and held until the termination of the transfer. For write cycles,

- OE is negated throughout the cycle.

## 12.2.1.11 Read / Write (RD\_WR)

RD\_WR indicates whether the current transaction is a read access or a write access.

RD\_WR is driven by the EBI or an external master depending on who owns the external bus. RD\_WR is driven in the same clock as the assertion of TS and valid address, and is kept valid until the cycle is terminated.

## 12.2.1.12 Transfer Acknowledge (TA)

TA is asserted to indicate that the slave has received the data (and completed the access) for a write cycle, or returned data for a read cycle. If the transaction is a burst read, TA is asserted for each one of the

transaction beats. For write transactions, TA is only asserted once at access completion, even if more than one write data beat is transferred.

TA is driven by the EBI when the access is controlled by the chip selects or when an external master initiated the transaction to an internal module. Otherwise, TA is driven by the slave device to which the current transaction was addressed.

See Section 12.4.2.9, 'Termination Signals Protocol' for more details.

## 12.2.1.13 Transfer Error Acknowledge (TEA)

In the 416-pin package of the MPC5553/MPC5554, TEA is asserted by either the EBI or an external device to indicate that an error condition has occurred during the bus cycle. TEA assertion terminates the cycle immediately, overriding the value of the TA signal.

TEA is asserted by the EBI when the internal bus monitor detected a timeout error, or when an external master initiated a transaction to an internal module and an internal error was detected.

The 324 BGA package of the MPC5553 has no TEA signal.

See Section 12.4.2.9, 'Termination Signals Protocol' for more details.

## 12.2.1.14 Transfer Start (TS)

TS is asserted by the current bus owner to indicate the start of a transaction on the external bus.

TS is driven by the EBI or an external master depending on who owns the external bus. TS is only asserted for the first clock cycle of the transaction, and is negated in the successive clock cycles until the end of the transaction.

## 12.2.1.15 Transfer Size 0-1 (TSIZ[0:1]) - MPC5554 Only

TSIZ[0:1] indicates the size of the requested data transfer.

TSIZ[0:1] is  driven  by  the  EBI  or  an  external  master  depending  on  who  owns  the  external  bus.  The TSIZ[0:1] signals may be used with ADDR[30:31] to determine which byte lanes of the data bus are involved in the transfer. For non-burst transfers, the TSIZ[0:1] signals specify the number of bytes starting from the byte location addressed by ADDR[30:31]. In burst transfers, the value of TSIZ[0:1] is always 00.

## Table 12-4. TSIZ[0:1] Encoding

| Burst Cycle   |   TSIZ[0:1] | Transfer Size   |
|---------------|-------------|-----------------|
| N             |          01 | Byte            |
| N             |          10 | 16-bit          |
| N             |          11 | Reserved        |
| N             |          00 | 32-bit          |
| Y             |          00 | Burst           |

If the SIZEN bit in the EBI\_MCR is 1, then TSIZ[0:1] is ignored by the EBI as an input for external master transactions and the size is instead determined by the SIZE field in the EBI\_MCR. The SIZEN bit has no effect  on  the  EBI  when  it  is  mastering  a  transaction  on  the  external  bus.  TSIZ[0:1]  is  still  driven appropriately by the EBI and may or may not be used by the external master depending on the SIZEN

setting  for  the  external  master's  EBI.  See  Section 12.3.1.3,  'EBI  Module  Configuration  Register (EBI\_MCR).'

## 12.2.1.16 Write/Byte Enables (WE / BE)

Write enables are used to enable program operations to a particular memory. These signals can also be used as byte enables for read and write operation by setting the WEBS bit in the appropriate base register. WE / BE are only asserted for chip select accesses.

WE / BE are driven by the EBI or an external master depending on who owns the external bus. See Section 12.4.1.13,  'Four  Write/Byte  Enable  (WE/BE)  Signals  -  Only  MPC5554  and  416  BGA  of MPC5553' for more details on WE / BE functionality.

The MPC5554 and the 416 BGA package of the MPC5553 use WE[0:3]/ BE[0:3].  The 324 BGA of the MPC5553 uses only WE[0:1]/ BE[0:1].  The 208 BGA of the MPC5553 has no write/byte enable signals.

## 12.2.2 Signal Function/Direction by Mode

Depending on the mode of operation, some or all of the EBI external signals may not be used by the EBI. When a signal is configured for non-EBI function in the EBI\_MCR, the EBI always negates the signal if the EBI controls the corresponding pad (determined by SIU configuration). Table 12-5 lists the function and direction of the external signals in each of the EBI modes of operation. The clock signals are not included because they are output only (from the FMPLL module) and are not affected by EBI modes. See Section 12.3.1.3, 'EBI Module Configuration Register (EBI\_MCR)' for details on the EXTM and MDIS bits.

Table 12-5. Signal Function by Mode

|                       | Device                      | Device                                  | Modes                                             | Modes                                                        | Modes                                                          |
|-----------------------|-----------------------------|-----------------------------------------|---------------------------------------------------|--------------------------------------------------------------|----------------------------------------------------------------|
| Signal Name           | MPC5554 Containsthe Signal? | MPC5553 Package That Containsthe Signal | Module Disable Mode Function (EXTM = X, MDIS = 1) | Single Master Mode Function (Direction) (EXTM = 0, MDIS = 0) | External Master Mode Function (Direction) (EXTM = 1, MDIS = 0) |
| ADDR[8:11]            | Yes                         | 416                                     | non-EBI function                                  | Address bus (Output)                                         | Address bus (I/O)                                              |
| ADDR[12:31]           | Yes                         | 416, 324                                | non-EBI function                                  | Address bus (Output)                                         | Address bus (I/O)                                              |
| BB                    | Yes                         | None                                    | non-EBI function                                  | non-EBI function                                             | Bus Busy (I/O)                                                 |
| BDIP                  | Yes                         | 416, 324                                | non-EBI function                                  | Burst Data in Progress (Output)                              | Burst Data in Progress (Output)                                |
| BG                    | Yes                         | None                                    | non-EBI function                                  | non-EBI function                                             | Bus Grant (I/O)                                                |
| BR                    | Yes                         | None                                    | non-EBI function                                  | non-EBI function                                             | Bus Request (I/O)                                              |
| CS[0:3]               | Yes                         | 416, 324                                | non-EBI function                                  | Chip Selects (Output)                                        | Chip Selects (Output)                                          |
| DATA[0:15]            | Yes                         | 416, 324                                | non-EBI function                                  | Data bus (I/O)                                               | Data bus (I/O)                                                 |
| DATA[16:31]           | Yes                         | 416                                     | non-EBI function                                  | Data bus (I/O)                                               | Data bus (I/O)                                                 |
| OE                    | Yes                         | 416, 324                                | non-EBI function                                  | Output Enable (Output)                                       | Output Enable (Output)                                         |
| RD_WR                 | Yes                         | 416, 324                                | non-EBI function                                  | Read_Write (Output)                                          | Read_Write (I/O)                                               |
| TA                    | Yes                         | 416, 324                                | non-EBI function                                  | Transfer Acknowledge (I/O)                                   | Transfer Acknowledge (I/O)                                     |
| TEA                   | Yes                         | 416                                     | non-EBI function                                  | Transfer Error Acknowledge (I/O)                             | Transfer Error Acknowledge (I/O)                               |
| TS                    | Yes                         | 416, 324                                | non-EBI function                                  | Transfer Start (Output)                                      | Transfer Start (I/O)                                           |
| TSIZ[0:1]             | Yes                         | None                                    | non-EBI function                                  | Transfer Size (Output)                                       | Transfer Size (I/O)                                            |
| WE[0:]/BE[0:1]        | Yes                         | 416, 324                                | non-EBI function                                  | Write/Byte Enables (Output)                                  | Write/Byte Enables (Output)                                    |
| WE[2:3]/BE[2:3]       | Yes                         | 416                                     | non-EBI function                                  | Write/Byte Enables (Output)                                  | Write/Byte Enables (Output)                                    |
| CAL_CS[0] CAL_CS[2:3] | No                          | 416                                     | non-EBI function                                  | Chip Selects (Output)                                        | Chip Selects (Output)                                          |

## 12.2.3 Signal Pad Configuration by Mode

Depending on the mode of operation, many external signals must have their pads configured to operate as push/pull signals for correct system operation. This configuration is done in the SIU module.

The open drain mode of the pads configuration module is not used for any EBI signals. For a description of  how  signals  are  driven  by  multiple  devices  in  external  master  mode,  see  Section 12.4.2.10,  'Bus Operation in External Master Mode.'

Table 12-6 shows how each EBI signal must have its pad configured prior to operating in each of the EBI modes. See Section 12.3.1.3, 'EBI Module Configuration Register (EBI\_MCR)' for details on the EXTM and MDIS bits.

Table 12-6. Required EBI Pad Configuration by Mode

| Signal Name           | MPC5553 Package Type   | MPC5554 and MPC5553                      | MPC5554 and MPC5553                     | MPC5554 and MPC5553                       |
|-----------------------|------------------------|------------------------------------------|-----------------------------------------|-------------------------------------------|
| Signal Name           | MPC5553 Package Type   | Module Disable Mode (EXTM = X, MDIS = 1) | Single Master Mode (EXTM = 0, MDIS = 0) | External Master Mode (EXTM = 1, MDIS = 0) |
| ADDR[8:11]            | 416                    | X 1                                      | Push/Pull                               | Push/Pull Three-stateable                 |
| ADDR[12:31]           | 416, 324               | X                                        | Push/Pull                               | Push/Pull Three-stateable                 |
| BB                    | None                   | X                                        | X                                       | Push/Pull, Three-stateable                |
| BDIP                  | 416, 324               | X                                        | Push/Pull                               | Push/Pull Three-stateable                 |
| BG                    | None                   | X                                        | X                                       | Push/Pull, Three-stateable                |
| BR                    | None                   | X                                        | X                                       | Push/Pull, Three-stateable                |
| CS[0:3]               | 416, 324               | X                                        | Push/Pull                               | Push/Pull, Three-stateable                |
| CAL_CS[0] CAL_CS[2:3] | 416                    | X                                        | Push/Pull                               | N.A.                                      |
| DATA[0:15]            | 416, 324               | X                                        | Push/Pull, Three-stateable              | Push/Pull, Three-stateable                |
| DATA[16:31]           | 416                    | X                                        | Push/Pull, Three-stateable              | Push/Pull, Three-stateable                |
| OE                    | 416, 324, 208          | X                                        | Push/Pull                               | Push/Pull, Three-stateable                |
| RD_WR                 | 416, 324               | X                                        | Push/Pull                               | Push/Pull, Three-stateable                |
| TA                    | 416, 324               | X                                        | Push/Pull, Three-stateable              | Push/Pull, Three-stateable                |
| TEA                   | 416                    | X                                        | Push/Pull, Three-stateable              | Push/Pull, Three-stateable                |
| TS                    | 416, 324               | X                                        | Push/Pull                               | Push/Pull, Three-stateable                |

Table 12-6. Required EBI Pad Configuration by Mode (continued)

|                 | MPC5553      | MPC5554 and MPC5553                      | MPC5554 and MPC5553                     | MPC5554 and MPC5553                       |
|-----------------|--------------|------------------------------------------|-----------------------------------------|-------------------------------------------|
| Signal Name     | Package Type | Module Disable Mode (EXTM = X, MDIS = 1) | Single Master Mode (EXTM = 0, MDIS = 0) | External Master Mode (EXTM = 1, MDIS = 0) |
| TSIZ[0:1]       | None         | X                                        | Push/Pull                               | Push/Pull, Three-stateable                |
| WE[0:]/BE[0:1]  | 416, 324     | X                                        | Push/Pull                               | Push/Pull, Three-stateable                |
| WE[2:3]/BE[2:3] | 416          | X                                        | Push/Pull                               | Push/Pull, Three-stateable                |

1 'X' indicates the pad configuration is a don't care, because the signal is not used by the EBI in this mode.

## 12.3 Memory Map/Register Definition

Table 12-7 is a memory map of the EBI registers.

Table 12-7. EBI Memory Map

| Address                             | Register Name                       | Register Description                   | Size (bits)                         |
|-------------------------------------|-------------------------------------|----------------------------------------|-------------------------------------|
| Base (0xC3F8_4000)                  | EBI_MCR                             | EBI module configuration register      | 32                                  |
| Base + 0x0004                       | -                                   | Reserved                               | -                                   |
| Base + 0x0008                       | EBI_TESR                            | EBI transfer error status register     | 32                                  |
| Base + 0x000C                       | EBI_BMCR                            | EBI bus monitor control register       | 32                                  |
| Base + 0x0010                       | EBI_BR0                             | EBI base register bank 0               | 32                                  |
| Base + 0x0014                       | EBI_OR0                             | EBI option register bank 0             | 32                                  |
| Base + 0x0018                       | EBI_BR1                             | EBI base register bank 1               | 32                                  |
| Base + 0x001C                       | EBI_OR1                             | EBI option register bank 1             | 32                                  |
| Base + 0x0020                       | EBI_BR2                             | EBI base register bank 2               | 32                                  |
| Base + 0x0024                       | EBI_OR2                             | EBI option register bank 2             | 32                                  |
| Base + 0x0028                       | EBI_BR3                             | EBI base register bank 3               | 32                                  |
| Base + 0x002C                       | EBI_OR3                             | EBI option register bank 3             | 32                                  |
| MPC5553-Only Calibration Registers: | MPC5553-Only Calibration Registers: | MPC5553-Only Calibration Registers:    | MPC5553-Only Calibration Registers: |
| Base + 0x30 - Base + 0x3C           | -                                   | Reserved                               | -                                   |
| Base + 0x0040                       | EBI_CAL_BR0                         | EBI Calibration Base Register Bank 0   | 32                                  |
| Base + 0x0044                       | EBI_CAL_OR0                         | EBI Calibration Option Register Bank 0 | 32                                  |
| Base + 0x0048                       | EBI_CAL_BR1                         | EBI Calibration Base Register Bank 1   | 32                                  |
| Base + 0x004C                       | EBI_CAL_OR1                         | EBI Calibration Option Register Bank 1 | 32                                  |
| Base + 0x0050                       | EBI_CAL_BR2                         | EBI Calibration Base Register Bank 2   | 32                                  |
| Base + 0x0054                       | EBI_CAL_OR2                         | EBI Calibration Option Register Bank 2 | 32                                  |
| Base + 0x0058                       | EBI_CAL_BR3                         | EBI Calibration Base Register Bank 3   | 32                                  |
| Base + 0x005C                       | EBI_CAL_OR3                         | EBI Calibration Option Register Bank 3 | 32                                  |

## 12.3.1 Register Descriptions

## 12.3.1.1 Writing EBI Registers While a Transaction is in Progress

Other than the exceptions noted below, EBI registers must not be written while a transaction to the EBI (from internal or external master) is in progress (or within 2 CLKOUT cycles after a transaction has just completed, to allow internal state machines to go IDLE). In such cases, the behavior is undefined.

Exceptions that can be written while an EBI transaction is in progress are the following:

- · All bits in EBI\_TESR

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## · SIZE, SIZEN fields in EBI\_MCR

See Section 12.5.1, 'Booting from External Memory' for additional information.

## 12.3.1.2 Separate Input Clock for Registers

The EBI registers are accessed with a clock signal separate from the clock used by the rest of the EBI. In module disable mode, the clock used by the non-register portion of the EBI is disabled to reduce power consumption. The clock signal dedicated to the registers, however, allows access to the registers even while the EBI is in the module disable mode. Flag bits in the EBI transfer error status register (EBI\_TESR), however, are set and cleared with the clock used by the non-register portion of the EBI. Consequently, in module disable mode, the EBI\_TESR does not have a clock signal and is therefore not writable.

## 12.3.1.3 EBI Module Configuration Register (EBI\_MCR)

The EBI\_MCR contains bits that configure various attributes associated with EBI operation.

Figure 12-2. EBI Module Configuration Register (EBI\_MCR)

<!-- image -->

|          | 0                  | 1                  | 2                  | 3                  | 4                  | 5                  | 6 7                | 6 7                | 8                  | 9                  | 10                 | 11                 | 12                 | 13                 | 14                 | 15                 |
|----------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|
| R        | 0                  | 0                  | 0                  | 0                  | 0                  | SIZEN              | SIZE               | SIZE               | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  |
| W        |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |
| Reset    | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  |
| Reg Addr | Base (0xC3F8_4000) | Base (0xC3F8_4000) | Base (0xC3F8_4000) | Base (0xC3F8_4000) | Base (0xC3F8_4000) | Base (0xC3F8_4000) | Base (0xC3F8_4000) | Base (0xC3F8_4000) | Base (0xC3F8_4000) | Base (0xC3F8_4000) | Base (0xC3F8_4000) | Base (0xC3F8_4000) | Base (0xC3F8_4000) | Base (0xC3F8_4000) | Base (0xC3F8_4000) | Base (0xC3F8_4000) |
|          | 16                 | 17                 | 18                 | 19                 | 20                 | 21                 | 22                 | 23                 | 24                 | 25                 | 26                 | 27                 | 28                 | 29                 | 30                 | 31                 |
| R        | ACGE               | EXTM               | EARB               | EARP               |                    | 0                  | 0                  | 0                  | 0                  | MDIS               | 0                  | 0                  | 0                  | 0                  | 0                  | DBM                |
| W        |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |
| Reset    | 0                  | 0                  | 0                  | 0                  | 1                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  |
| Reg Addr | Base (0xC3F8_4000) | Base (0xC3F8_4000) | Base (0xC3F8_4000) | Base (0xC3F8_4000) | Base (0xC3F8_4000) | Base (0xC3F8_4000) | Base (0xC3F8_4000) | Base (0xC3F8_4000) | Base (0xC3F8_4000) | Base (0xC3F8_4000) | Base (0xC3F8_4000) | Base (0xC3F8_4000) | Base (0xC3F8_4000) | Base (0xC3F8_4000) | Base (0xC3F8_4000) | Base (0xC3F8_4000) |

Table 12-8. EBI\_MCR Field Descriptions

| Bits   | Name   | Description                                                                                                                                                                                                                                                            |
|--------|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-4    | -      | Reserved.                                                                                                                                                                                                                                                              |
| 5      | SIZEN  | SIZE enable. The SIZEN bit enables the control of transfer size by the SIZE field (as opposed to external TSIZ pins) for external master transactions to internal address space. 0 Transfer size controlled by TSIZ[0:1] pins 1 Transfer size controlled by SIZE field |
| 6-7    | SIZE   | Transfer size. The SIZE field determines the transfer size of external master transactions to internal address space when SIZEN=1. This field is ignored when SIZEN=0. SIZE encoding: 00 32-bit 01 Byte 10 16-bit 11 Reserved                                          |

Table 12-8. EBI\_MCR Field Descriptions (continued)

| Bits   | Name       | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
|--------|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 16     | ACGE       | Automatic CLKOUTgating enable. Enables the EBI feature of turning off CLKOUT(holding it high) during idle periods in-between external bus accesses. 0 Automatic CLKOUT gating is disabled 1 Automatic CLKOUT gating is enabled                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| 17     | EXTM       | External master mode. Enables the external master mode of operation when MDIS = 0. WhenMDIS = 1, the EXTMbit is a don't care, and is treated as 0. In external master mode, an external master on the external bus can access any internal memory-mapped space while the internal e200z6 core is fully operational. When EXTM = 0, only internal masters can access the internal memory space. This bit also determines the functionality of the BR, BG, and BB signals. Note: The SIU PCRregisters must configure BR, BG, and BBfor EBI function (as opposed to default GPIO) prior to EXTM being set to 1, or erroneous behavior may result. 0 External master mode is inactive (single master mode) 1 External master mode is active Note: In the MPC5553, only master/slave systems support the EXTM functionality. Refer to 12.5.5. |
| 18     | EARB       | External arbitration. See Section 12.4.2.8, 'Arbitration,' for details on internal and external arbitration. When EXTM = 0, the EARB bit is a don't care, and is treated as 0. 0 Internal arbitration is used. 1 External arbitration is used.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| 19-20  | EARP [0:1] | External arbitration request priority. Defines the priority of an external master's arbitration request (0-2), with 2 being the highest priority level (EARP = 3 is reserved). This field is valid only when EARB = 0 (internal arbitration). The internal masters of the MCU have a fixed priority of 1. By default, internal and external masters have equal priority. See Section 12.4.2.8.2, 'Internal Bus Arbiter,' for the internal and external priority detailed description. 00 MCU has priority 01 Equal priority, round robin used 10 External master has priority 11 Reserved                                                                                                                                                                                                                                                |
| 21-24  | -          | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| 25     | MDIS       | Module disable mode. Allows the clock to be stopped to the non-memory mapped logic in the EBI, effectively putting the EBI in a software controlled power-saving state. See Section 12.1.4.3, 'Module Disable Mode,' for more information. No external bus accesses can be performed when the EBI is in module disable mode (MDIS = 1). 0 Module disable mode is inactive 1 Module disable mode is active                                                                                                                                                                                                                                                                                                                                                                                                                                |
| 26-30  | -          | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| 31     | DBM        | Data bus mode. Controls whether the EBI is in 32-bit or 16-bit data bus mode. 0 32-bit data bus mode is used 1 16-bit data bus mode is used                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## 12.3.1.4 EBI Transfer Error Status Register (EBI\_TESR)

The EBI\_TESR contains a bit for each type of transfer error on the external bus. A bit set to logic 1 indicates what type of transfer error occurred since the last time the bits were cleared. Each bit can be cleared by reset or by writing a 1 to it. Writing a 0 has no effect.

This register is not writable in module disable mode due to the use of power saving clock modes.

<!-- image -->

|          | 0             | 1             | 2             | 3             | 4             | 5             | 6             | 7             | 8             | 9             | 10            | 11            | 12            | 13            | 14            | 15            |
|----------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| R        | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| W        |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset    | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Reg Addr | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 |
|          | 16            | 17            | 18            | 19            | 20            | 21            | 22            | 23            | 24            | 25            | 26            | 27            | 28            | 29            | 30            | 31            |
| R        | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | TEAF          | BMTF          |
| W        |               |               |               |               |               |               |               |               |               |               |               |               |               |               | w1c           | w1c           |
| Reset    | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Reg Addr | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 |

Note: w1c means 'write 1 to clear' and is explained in the Preface.

Figure 12-3. EBI Transfer Error Status Register (EBI\_TESR)

## Table 12-9. EBI\_TESR Field Descriptions

| Bits   | Name   | Description                                                                                                                                                                              |
|--------|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-29   | -      | Reserved.                                                                                                                                                                                |
| 30     | TEAF   | Transfer error acknowledge flag. Set if the cycle was terminated by an externally generated TEA signal. 0 No error 1 External TEA occurred This bit can be cleared by writing a 1 to it. |
| 31     | BMTF   | Bus monitor timeout flag. Set if the cycle was terminated by a bus monitor timeout. 0 No error 1 Bus monitor timeout occurred This bit can be cleared by writing a 1 to it.              |

## 12.3.1.5 EBI Bus Monitor Control Register (EBI\_BMCR)

The EBI\_BMCR controls the timeout period of the bus monitor and whether it is enabled or disabled.

Figure 12-4. EBI Bus Monitor Control Register (EBI\_BMCR)

<!-- image -->

|          | 0             | 1             | 2             | 3             | 4             | 5             | 6             | 7             | 8             | 9             | 10            | 11            | 12            | 13            | 14            | 15            |
|----------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| R        | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| W        |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset    | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Reg Addr | Base + 0x000C | Base + 0x000C | Base + 0x000C | Base + 0x000C | Base + 0x000C | Base + 0x000C | Base + 0x000C | Base + 0x000C | Base + 0x000C | Base + 0x000C | Base + 0x000C | Base + 0x000C | Base + 0x000C | Base + 0x000C | Base + 0x000C | Base + 0x000C |
|          | 16            | 17            | 18            | 19            | 20            | 21            | 22            | 23            | 24            | 25            | 26            | 27            | 28            | 29            | 30            | 31            |
| R        | BMT           | BMT           | BMT           | BMT           | BMT           | BMT           | BMT           | BMT           | BME           | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| W        |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset    | 1             | 1             | 1             | 1             | 1             | 1             | 1             | 1             | 1             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Reg Addr | Base + 0x000C | Base + 0x000C | Base + 0x000C | Base + 0x000C | Base + 0x000C | Base + 0x000C | Base + 0x000C | Base + 0x000C | Base + 0x000C | Base + 0x000C | Base + 0x000C | Base + 0x000C | Base + 0x000C | Base + 0x000C | Base + 0x000C | Base + 0x000C |

Table 12-10. EBI\_BMCR Field Descriptions

| Bits   | Name      | Description                                                                                                                                                                                                                                                                                                                                                    |
|--------|-----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-15   | -         | Reserved.                                                                                                                                                                                                                                                                                                                                                      |
| 16-23  | BMT [0:7] | Bus monitor timing. Defines the timeout period, in 8 external bus clock resolution, for the Bus Monitor. See Section 12.4.1.7, 'Bus Monitor,' for more details on bus monitor operation. Timeout Period 2 + (8 BMT) × External Bus Clock Frequency ---------------------------------------- ---------------------------------------- =                         |
| 24     | BME       | Bus monitor enable. Controls whether the bus monitor is enabled for internal to external bus cycles. Regardless of the BMEvalue, the bus monitor is always disabled for chip select accesses, since these always use internal TA and thus have no danger of hanging the system. 0 Disable bus monitor 1 Enable bus monitor (for non-chip select accesses only) |
| 25-31  | -         | Reserved.                                                                                                                                                                                                                                                                                                                                                      |

## 12.3.1.6 EBI Base Registers 0-3 (EBI\_BR n ) and EBI Calibration Base Registers 0-3 (EBI\_CAL\_BR n )

The EBI\_BR  are used to define the base address and other attributes for the corresponding chip select. n The EBI\_CAL\_BR  appear in the MPC5553 only and are used to define the base address and other n attributes for the corresponding calibration chip select.

Figure 12-5. EBI Base Registers 0-3 (EBI\_BR n ) and EBI Calibration Base Registers 0-3 (EBI\_CAL\_BR n )

<!-- image -->

Table 12-11. EBI\_BR n and EBI\_CAL\_BR n Field Descriptions

| Bits   | Name      | Description                                                                                                                                                                                                                                                                                                                                                                                              |
|--------|-----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-16   | BA [0:16] | Base address. Compared to the corresponding unmasked address signals among ADDR[0:16] of the internal address bus to determine if a memory bank controlled by the memory controller is being accessed by an internal bus master. Note: The upper 3 bits of the base address (BA) field, EBI_BR n [0:2], and EBI_CAL_BR n [0:2], are tied to a fixed value of 001. These bits reset to their fixed value. |
| 17-19  | -         | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                |
| 20     | PS        | Port size. Determines the data bus width of transactions to this chip select bank. 1 0 32-bit port 1 16-bit port Note: The calibration port size must be 16-bits wide.                                                                                                                                                                                                                                   |
| 21-24  | -         | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                |
| 25     | BL        | Burst length. Determines the amount of data transferred in a burst for this chip select, measured in 32-bit words. The number of beats in a burst is automatically determined by the EBI to be 4, 8, or 16 according to the port size so that the burst fetches the number of words chosen by BL. 0 8-word burst length 1 4-word burst length                                                            |
| 26     | WEBS      | Write enable/byte select. Controls the functionality of the WE[0:3]/BE[0:3] signals. 0 The WE[0:3]/BE[0:3] signals function as WE[0:3]. 1 The WE[0:3]/BE[0:3] signals function as BE[0:3].                                                                                                                                                                                                               |

Table 12-11. EBI\_BR n and EBI\_CAL\_BR n Field Descriptions (continued)

| Bits   | Name   | Description                                                                                                                                                                                                                                                                                                                                                                  |
|--------|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 27     | TBDIP  | Toggle burst data in progress. Determines how long the BDIP signal is asserted for each data beat in a burst cycle. See Section 12.4.2.5.1, 'TBDIP Effect on Burst Transfer,' for details. 0 Assert BDIP throughout the burst cycle, regardless of wait state configuration. 1 Only assert BDIP (BSCY + 1) external bus cycles before expecting subsequent burst data beats. |
| 28-29  | -      | Reserved.                                                                                                                                                                                                                                                                                                                                                                    |
| 30     | BI     | Burst inhibit. Determines whether or not burst read accesses are allowed for this chip select bank. 0 Enable burst accesses for this bank. 1 Disable burst accesses for this bank. This is the default value out of reset.                                                                                                                                                   |
| 31     | V      | Valid bit. Indicates that the contents of this base register and option register pair are valid. The appropriate CS signal does not assert unless the corresponding V-bit is set. 0 This bank is not valid. 1 This bank is valid.                                                                                                                                            |

- 1 In the case where EBI\_MCR[DBM] is set for 16-bit data bus mode, the PS bit value is ignored and is always treated as a 1  (16-bit port).

## 12.3.1.7 EBI Option Registers 0-3 (EBI\_OR n ) and EBI Calibration Option Registers 0-3 (EBI\_CAL\_OR n )

The EBI\_OR  registers are used to define the address mask and other attributes for the corresponding chip n select. The EBI\_CAL\_OR n registers appear in the MPC5553 only and are used to define the address mask and other attributes for the corresponding calibration chip select.

Figure 12-6. EBI Option Registers 0-3 (EBI\_OR n ) and EBI Calibration Option Registers

<!-- image -->

## Table 12-12. EBI\_OR n and EBI\_CAL\_OR n Field Descriptions

| Bits   | Name       | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
|--------|------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-16   | AM [0:16]  | Address mask. Allows masking of any corresponding bits in the associated base register. Masking the address independently allows external devices of different size address ranges to be used. Any clear bit masks the corresponding address bit. Any set bit causes the corresponding address bit to be used in comparison with the address pins. Address mask bits can be set or cleared in any order in the field, allowing a resource to reside in more than one area of the address map. This field can be read or written at any time. Note: The upper 3 bits of the address mask (AM) field, EBI_ORx[0:2], are tied to a fixed value of 111. These bits reset to their fixed value.                                                                                                                     |
| 17-23  | -          | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| 24-27  | SCY [0:3]  | Cycle length in clocks. Represents the number of wait states (external bus cycles) inserted after the address phase in the single cycle case, or in the first beat of a burst, when the memory controller handles the external memory access. Values range from 0 to 15. This is the main parameter for determining the length of the cycle. GLYPH<127> The total cycle length for the first beat (including the TS cycle): See Section 12.5.3.1, 'Example Wait State Calculation'. (2 + SCY) external clock cycles                                                                                                                                                                                                                                                                                            |
| 28     | -          | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| 29-30  | BSCY [0:1] | Burst beats length in clocks. This field determines the number of wait states (external bus cycles) inserted in all burst beats except the first, when the memory controller starts handling the external memory access and thus is using SCY[0:3] to determine the length of the first beat. GLYPH<127> Total memory access length for each beat: GLYPH<127> Total cycle length (including the TS cycle): Note: The number of beats (4, 8, 16) is determined by BL and PS bits in the base register. 00 0-clock cycle wait states (1 clock per data beat) 01 1-clock cycle wait states (2 clocks per data beat) 10 2-clock cycle wait states (3 clocks per data beat) 11 3-clock cycle wait states (4 clocks per data beat) (1 + BSCY) External Clock Cycles (2 + SCY) + [(Number of Beats - 1) x (BSCY + 1)] |

## 12.4 Functional Description

## 12.4.1 External Bus Interface Features

## 12.4.1.1 32-Bit Address Bus with Transfer Size Indication

The transfer size for an external transaction is indicated by the TSIZ[0:1] signals during the clock where address is valid. Valid transaction sizes are 8, 16, and 32 bits. In the MPC5554 and in the 416 BGA package of the MPC5553, only 24 address lines are pinned out externally, but a full 32-bit decode is done internally

to determine the target of the transaction and whether a chip select should be asserted. The 324 BGA package of the MPC5553 has 20 address lines penned out.  The 208 package has no external bus.

## 12.4.1.2 32-Bit Data Bus

The entire 32-bit data bus is available for both external memory accesses and transactions involving an external master in the MPC5554 and in the 416 BGA package of the MPC5553.  In  the 324 BGA package of the MPC5553, the data bus is 16 bits.

## 12.4.1.3 16-Bit Data Bus

A 16-bit data bus mode is available via the DBM bit in EBI\_MCR. See Section 12.1.4.5, '16-Bit Data Bus Mode.'

## 12.4.1.4 Support for External Master Accesses to Internal Addresses

The EBI allows an external master to access internal address space when the EBI is configured for external master mode in the EBI\_MCR. External master operations are described in detail in Section 12.4.2.10, 'Bus Operation in External Master Mode.'

## 12.4.1.5 Memory Controller with Support for Various Memory Types

The EBI contains a memory controller that supports a variety of memory types, including synchronous burst  mode  Flash  and  external  SRAM,  and  asynchronous/legacy  Flash  and  external  SRAM  with  a compatible interface.

Each CS bank is configured via its own pair of base and option registers. Each time an internal to external bus cycle access is requested, the internal address is compared with the base address of each valid base register (with 17 bits having mask). See Figure 12-7. If a match is found, the attributes defined for this bank in its BR and OR are used to control the memory access. If a match is found in more than one bank, the lowest bank matched handles the memory access. For example, bank 0 is selected over bank 1.

Figure 12-7. Bank Base Address and Match Structure

<!-- image -->

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

A match on a valid calibration chip select register overrides a match on any non-calibration chip select register,  with  CAL\_CS0  having  the  highest  priority.  Thus  the  full  priority  of  the  chip  selects  is: CAL\_CS0....CAL\_CS3, CS0....CS3.

When a match is found on one of the chip select banks, all its attributes (from the appropriate base and option registers) are selected for the functional operation of the external memory access, such as:

- · Number of wait states for a single memory access, and for any beat in a burst access
- · Burst enable
- · Port size for the external accessed device

See  Section 12.3.1.6,  'EBI  Base  Registers  0-3  (EBI\_BRn)  and  EBI  Calibration  Base  Registers  0-3 (EBI\_CAL\_BRn),' and Section 12.3.1.7, 'EBI Option Registers 0-3 (EBI\_ORn) and EBI Calibration Option Registers 0-3 (EBI\_CAL\_ORn),' for a full description of all chip select attributes.

When  no  match  is  found  on  any  of  the  chip  select  banks,  the  default  transfer  attributes  shown  in Table 12-13 are used.

Table 12-13. Default Attributes for Non-Chip Select Transfers

| CS Attribute   |   Default Value | Comment                                            |
|----------------|-----------------|----------------------------------------------------|
| PS             |               0 | 32-bit port size                                   |
| BL             |               0 | Burst length is don't care since burst is disabled |
| WEBS           |               0 | Write enables                                      |
| TBDIP          |               0 | Don't care since burst is disabled                 |
| BI             |               1 | Burst inhibited                                    |
| SCY            |               0 | Don't care since external TA is used               |
| BSCY           |               0 | Don't care since external TA is used               |

## 12.4.1.6 Burst Support (Wrapped Only)

The  EBI  supports  burst  read  accesses  of  external  burstable  memory.  To  enable  bursts  to  a  particular memory region, clear the BI (Burst Inhibit) bit in the appropriate base register. External burst lengths of 4 and 8 words are supported. Burst length is configured for each chip select by using the BL bit in the appropriate base register. See Section 12.4.2.5, 'Burst Transfer' for more details.

In 16-bit data bus mode (EBI\_MCR[DBM]=1), a special 2-beat burst case is supported for reads and writes for 32-bit non-chip select accesses only. This is to allow 32-bit coherent accesses to another MCU. See Section 12.4.2.11, 'Non-Chip-Select Burst in 16-bit Data Bus Mode'.

Bursting of accesses that are not controlled by the chip selects is not supported for any other case besides the special case of 32-bit accesses in 16-bit data bus mode.

Burst writes are not supported for any other case besides the special case of 32-bit non-chip select writes in 16-bit data bus mode. Internal requests to write more than 32 bits (such as a cache line) externally are broken  up  into  separate  32-bit  or 16-bit external transactions according  to  the  port size. See Section 12.4.2.6, 'Small Accesses (Small Port Size and Short Burst Length)' for more detail on these cases.

## 12.4.1.7 Bus Monitor

When enabled (via the BME bit in the EBI\_BMCR), the bus monitor detects when no TA assertion is received within a maximum timeout period for non-chip select accesses (that is, accesses that use external TA). The timeout for the bus monitor is specified by the BMT field in the EBI\_BMCR. Each time a timeout error  occurs,  the  BMTF  bit  is  set  in  the  EBI\_TESR.  The  timeout  period  is  measured  in  external  bus (CLKOUT) cycles. Thus the effective real-time period is multiplied (by 2 or 4) when a configurable bus speed mode is used, even though the BMT field itself is unchanged.

## 12.4.1.8 Port Size Configuration per Chip Select (16 or 32 Bits)

The EBI supports memories with data widths of 16 or 32 bits. The port size for a particular chip select is configured by writing the PS bit in the corresponding base register.

## 12.4.1.9 Port Size Configuration per Calibration Chip Select (16 Bits)

The port size for calibration must be 16 bits wide.

## 12.4.1.10 Configurable Wait States

From 0 to 15 wait states can be programmed for any cycle that the memory controller generates, via the SCY bits in the appropriate option register. From zero to three wait states between burst beats can be programmed using the BSCY bits in the appropriate option register.

## 12.4.1.11 Four Chip Select (CS[0:3]) Signals

The EBI  contains four chip select signals, controlling four independent memory  banks. See Section 12.4.1.5, 'Memory Controller with Support for Various Memory Types,' for more details on chip select bank configuration.

## 12.4.1.12 Support for Dynamic Calibration with Up to 4 Chip Selects

The EBI contains four calibration chip select signals, controlling four independent memory banks on an optional  second  external  bus  for  calibration.  See  Section 12.4.2.12,  'Calibration  Bus  Operation  MPC5553 Only' for more details on using the calibration bus.

## 12.4.1.13 Four Write/Byte Enable (WE/BE) Signals - Only MPC5554 and 416 BGA of MPC5553

In the MPC5554 and in the 416 BGA of the MPC5553, the functionality of the WE[0:3]/BE[0:3] signals depends on the value of the WEBS bit in the corresponding base register. Setting WEBS to 1 configures these pins as BE[0:3], while resetting it to 0 configures them as WE[0:3]. WE[0:3] are asserted only during write  accesses,  while  BE[0:3]  is  asserted  for  both  read  and  write  accesses.  The  timing  of  the WE[0:3]/BE[0:3] signals remains the same in either case.

The upper write/byte enable (WE0/BE0) indicates that the upper eight bits of the data bus (DATA[0:7]) contain valid data during a write/read cycle. The upper middle write/byte enable (WE1/BE1) indicates that the upper middle eight bits of the data bus (DATA[8:15]) contain valid data during a write/read cycle. The lower middle write/byte enable (WE2/BE2) indicates that the lower middle eight bits of the data bus (DATA[16:23]) contain valid data during a write/read cycle. The lower write/byte enable (WE3/BE3) indicates that the lower eight bits of the data bus (DATA[24:31]) contain valid data during a write/read cycle.

The write/byte enable lines affected in a transaction for a 32-bit port (PS = 0) and a 16-bit port (PS = 1) are shown in Table 12-14. Only big endian byte ordering is supported by the EBI.

Table 12-14. Write/Byte Enable Signals Function -- 416 BGA

| Transfer Size   | TSIZ[0:1]   | Address   | Address   | 32-Bit Port Size   | 32-Bit Port Size   | 32-Bit Port Size   | 32-Bit Port Size   | 16-Bit Port Size 1   | 16-Bit Port Size 1   | 16-Bit Port Size 1   | 16-Bit Port Size 1   |
|-----------------|-------------|-----------|-----------|--------------------|--------------------|--------------------|--------------------|----------------------|----------------------|----------------------|----------------------|
| Transfer Size   | TSIZ[0:1]   | A30       | A31       | WE0/ BE0           | WE1/ BE1           | WE2/ BE2           | WE3/ BE3           | WE0/ BE0             | WE1/ BE1             | WE2/ BE2             | WE3/ BE3             |
| Byte            | 01          | 0         | 0         | X                  | -                  | -                  | -                  | X                    | -                    | -                    | -                    |
| Byte            | 01          | 0         | 1         | -                  | X                  | -                  | -                  | -                    | X                    | -                    | -                    |
| Byte            | 01          | 1         | 0         | -                  | -                  | X                  | -                  | X                    | -                    | -                    | -                    |
| Byte            | 01          | 1         | 1         | -                  | -                  | -                  | X                  |                      | X                    | -                    | -                    |
| 16-bit          | 10          | 0         | 0         | X                  | X                  | -                  | -                  | X                    | X                    | -                    | -                    |
| 16-bit          | 10          | 1         | 0         | -                  | -                  | X                  | X                  | X                    | X                    | -                    | -                    |
| 32-bit          | 00          | 0         | 0         | X                  | X                  | X                  | X                  | X 2                  | X 2                  | -                    | -                    |
| Burst           | 00          | 0         | 0         | X                  | X                  | X                  | X                  | X                    | X                    | -                    | -                    |

1 Also applies when DBM=1 for 16-bit data bus mode.

- 2 This case consists of two 16-bit external transactions, but for both transactions the WE[0:1]/BE[0:1] signals are the only WE/BE signals affected.

NOTE: All areas of the table, both shaded and clear, apply to the 416 BGA package of the MPC5553 and to the MPC5554.

NOTE: 'X' indicates that valid data is transferred on these bits.

## 12.4.1.14 Two Write/Byte Enable (WE/BE) Signals - 324 BGA of MPC5553 Only

In the 324 BGA of the MPC5553, the functionality of the WE[0:1]/BE[0:1] signals depends on the value of the WEBS bit in the corresponding base register.  Setting WEBS to 1 configures these pins as BE[0:1], while resetting it to 0 configures them as WE[0:1].  WE[0:1] are asserted only during write accesses, while BE[0:1] is asserted for both read and write accesses.  The timing of the WE[0:1]/BE[0:1] signals remains the same in either case.

The upper write/byte enable (WE0/BE0) indicates that the upper eight bits of the data bus (DATA[0:7]) contain valid data during a write/read cycle.  The lower write/byte enable (WE1/BE1) indicates that the lower eight bits of the data bus (DATA[8:15]) contain valid data during a write/read cycle.

The write/byte enable lines affected in a transaction are shown below in Table 12-15. Only big endian byte ordering is supported by the EBI.

Table 12-15. Write/Byte Enable Signals Function -- 324 BGA

| Transfer Size   | TSIZ[0:1]   | Address   | Address   | 16-Bit Port Size 1   | 16-Bit Port Size 1   |
|-----------------|-------------|-----------|-----------|----------------------|----------------------|
| Transfer Size   | TSIZ[0:1]   | A30       | A31       | WE0/ BE0             | WE1/ BE1             |
| Byte            | 01          | 0         | 0         | X                    | -                    |
| Byte            | 01          | 0         | 1         | -                    | X                    |
| Byte            | 01          | 1         | 0         | X                    | -                    |
| Byte            | 01          | 1         | 1         | -                    | X                    |
| 16-bit          | 10          | 0         | 0         | X                    | X                    |
| 16-bit          | 10          | 1         | 0         | X                    | X                    |
| 32-bit          | 00          | 0         | 0         | X 2                  | X 2                  |
| Burst           | 00          | 0         | 0         | X                    | X                    |

- 1 Also applies when DBM=1 for 16-bit data bus mode.
- 2 This case consists of two 16-bit external transactions, but for both transactions the WE[0:1]/BE[0:1] signals are the only WE/BE signals affected.

NOTE: 'X' indicates that valid data is transferred on these bits.

## 12.4.1.15 Configurable Bus Speed Clock Modes

The EBI supports configurable bus speed clock modes. Refer to Section 12.1.4.4, 'Configurable Bus Speed Modes,' for more details on this feature.

## 12.4.1.16 Stop and Module Disable Modes for Power Savings

See Section 12.1.4, 'Modes of Operation,' for a description of the power saving modes.

## 12.4.1.17 Optional Automatic CLKOUT Gating

The EBI has the ability to hold the external CLKOUT pin high when the EBI's internal master state machine is idle and no requests are pending. The EBI outputs a signal to the pads logic in the MCU to disable CLKOUT. This feature is disabled out of reset, and can be enabled or disabled by the ACGE bit in the EBI\_MCR.

## NOTE

This feature must be disabled for multi-master systems. In those cases, one master is getting its clock source from the other master and needs the other master  to stay valid continuously.

## 12.4.1.18 Compatible with MPC5xx External Bus (with Some Limitations)

The EBI is compatible with the external bus of the MPC5xx parts, meaning that it supports most devices supported by the MPC5xx family of parts. However, there are some differences between this EBI and that of the MPC5xx parts that the user needs to be aware of before assuming that an MPC5xx-compatible device works with this EBI. See Section 12.5.6, 'Summary of Differences from MPC5xx,' for details.

## NOTE

Due  to  testing  and  complexity  concerns,  multi-master  (or  master/slave) operation between an eSys MCU and MPC5xx is not guaranteed.

## 12.4.2 External Bus Operations

The following sections provide a functional description of the external bus, the bus cycles provided for data transfer operations, bus arbitration, and error conditions.

## 12.4.2.1 External Clocking

The CLKOUT signal sets the frequency of operation for the bus interface directly. Internally, the MCU uses a phase-locked loop (PLL) circuit to generate a master clock for all of the MCU circuitry (including the EBI) which is phase-locked to the CLKOUT signal. In general, all signals for the EBI are specified with respect to the rising-edge of the CLKOUT signal, and they are guaranteed to be sampled as inputs or changed as outputs with respect to that edge.

## 12.4.2.2 Reset

Upon detection of internal reset, the EBI immediately terminates all transactions.

## 12.4.2.3 Basic Transfer Protocol

The basic transfer protocol defines the sequence of actions that must occur on the external bus to perform a complete bus transaction. A simplified scheme of the basic transfer protocol is shown in Figure 12-8.

Arbitration

Address Transfer

Data Transfer

Termination

## Figure 12-8. Basic Transfer Protocol

The arbitration phase is where bus ownership is requested and granted. This phase is not needed in single master mode because the EBI is the permanent bus owner in this mode. Arbitration is discussed in detail in Section 12.4.2.8, 'Arbitration.'

The address transfer phase specifies the address for the transaction and the transfer attributes that describe the  transaction.  The  signals  related  to  the  address  transfer  phase  are  TS,  ADDR,  CS[0:3],  RD\_WR, TSIZ[0:1], and BDIP. The address and its related signals (with the exception of TS, BDIP) are driven on the bus with the assertion of the TS signal, and kept valid until the bus master receives TA asserted (the EBI holds them one cycle beyond TA for writes and external TA accesses). Note that for writes with internal TA, RD\_WR is not held one cycle past TA.

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

The data transfer phase performs the transfer of data, from master to slave (in write cycles) or from slave to master (on read cycles), if any is to be transferred. The data phase may transfer a single beat of data (1-4 bytes) for non-burst operations or a 2-beat (special EBI\_MCR[DBM]=1 case only), 4-beat, 8-beat, or 16-beat burst of data (2 or 4 bytes per beat depending on port size) when burst is enabled. On a write cycle, the master must not drive write data until after the address transfer phase is complete. This is to avoid electrical contentions when switching between drivers. The master must start driving write data one cycle after the address transfer cycle. The master can stop driving the data bus as soon as it samples the TA line asserted on the rising edge of CLKOUT. To facilitate asynchronous write support, the EBI keeps driving valid write data on the data bus until 1 clock after the rising edge where RD\_WR and WE are negated (for chip select accesses only). See Figure 12-14 for an example of write timing. On a read cycle, the master accepts the data bus contents as valid on the rising edge of the CLKOUT in which the TA signal is sampled asserted. See Figure 12-10 for an example of read timing.

The termination phase is where the cycle is terminated by the assertion of either TA (normal termination) or  TEA  (termination  with  error).  Termination  is  discussed  in  detail  in  Section 12.4.2.9,  'Termination Signals Protocol.'

## 12.4.2.4 Single Beat Transfer

The flow and timing diagrams in this section assume that the EBI is configured in single master mode. Therefore, arbitration is not needed and is not shown in these diagrams. Refer to Section 12.4.2.10, 'Bus Operation in External Master Mode,' to see how the flow and timing diagrams change for external master mode.

## 12.4.2.4.1 Single Beat Read Flow

The handshakes for a single beat read cycle are illustrated in the following flow and timing diagrams.

Figure 12-9. Basic Flow Diagram of a Single Beat Read Cycle

<!-- image -->

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Figure 12-10. Single Beat 32-bit Read Cycle, CS Access, Zero Wait States

<!-- image -->

Figure 12-11. Single Beat 32-bit Read Cycle, CS Access, One Wait State

<!-- image -->

<!-- image -->

- The EBI drives address and control signals an extra cycle because it uses a latched version of the external TA (1 cycle delayed) to terminate the cycle. *

Figure 12-12. Single Beat 32-bit Read Cycle, Non-CS Access, Zero Wait States

## 12.4.2.4.2 Single Beat Write Flow

The handshakes for a single beat write cycle are illustrated in the following flow and timing diagrams.

Figure 12-13. Basic Flow Diagram of a Single Beat Write Cycle

<!-- image -->

Figure 12-14. Single Beat 32-bit Write Cycle, CS Access, Zero Wait States

<!-- image -->

Figure 12-15. Single Beat 32-bit Write Cycle, CS Access, One Wait State

<!-- image -->

<!-- image -->

- The EBI drives address and control signals an extra cycle because it uses a latched version of the external TA (1 cycle delayed) to terminate the cycle. *

Figure 12-16. Single Beat 32-bit Write Cycle, Non-CS Access, Zero Wait States

## 12.4.2.4.3 Back-to-Back Accesses

Due to internal bus protocol, one dead cycle is necessary between back-to-back external bus accesses that are not part of a set of small accesses (see Section 12.4.2.6, 'Small Accesses (Small Port Size and Short Burst Length)' for small access timing). Besides this dead cycle, in most cases, back-to-back accesses on the external bus do not cause any change in the timing from that shown in the previous diagrams, and the two transactions are independent of each other. The only exceptions to this are as follows:

- · Back-to-back accesses where the first access ends with an externally-driven TA or TEA. In these cases, an extra cycle is required between the end of the first access and the TS assertion of the second access. See Section 12.4.2.9, 'Termination Signals Protocol,' for more details.

The following diagrams show a few examples of back-to-back accesses on the external bus.

Figure 12-17. Back-to-Back 32-bit Reads to the Same CS Bank

<!-- image -->

Figure 12-18. Back-to-Back 32-bit Reads to Different CS Banks

<!-- image -->

Figure 12-19. Write After Read to the Same CS Bank

<!-- image -->

Figure 12-20. Back-to-Back 32-bit Writes to the Same CS Bank

<!-- image -->

## 12.4.2.5 Burst Transfer

The EBI supports wrapping 32-byte critical-doubleword-first burst transfers. Bursting is supported only for  internally-requested  cache-line  size  (32-byte)  read  accesses  to  external  devices  that  use  the  chip selects 1 . Accesses from an external master or to devices operating without a chip select are always single

1. Except for the special case of a 32-bit non-chip select access in 16-bit data bus mode. See Section 12.4.2.11.

## External Bus Interface (EBI)

beat. If an internal request to the EBI indicates a size of less than 32 bytes, the request is fulfilled by running one or more single-beat external transfers, not by an external burst transfer.

An 8-word wrapping burst reads eight 32-bit words by supplying a starting address that points to one of the words (doubleword aligned) and requiring the memory device to sequentially drive each word on the data bus. The selected slave device must internally increment ADDR[27:29] (also ADDR30 in the case of a 16-bit port size device) of the supplied address for each transfer, until the address reaches an 8-word boundary, and then wrap the address to the beginning of the 8-word boundary. The address and transfer attributes supplied by the EBI remain stable during the transfers, and the EBI terminates each beat transfer by asserting TA. The EBI requires that addresses be aligned to a doubleword boundary on all burst cycles.

Table 12-16 shows the burst order of beats returned for an 8-word burst to a 32-bit port.

Table 12-16. Wrap Bursts Order

|   Burst Starting Address ADDR[27:28] | Burst Order (Assuming 32-bit Port Size)                              |
|--------------------------------------|----------------------------------------------------------------------|
|                                   00 | word0 -> word1 -> word2 -> word3 -> word4 -> word5 -> word6 -> word7 |
|                                   01 | word2 -> word3 -> word4 -> word5 -> word6 -> word7 -> word0 -> word1 |
|                                   10 | word4 -> word5 -> word6 -> word7 -> word0 -> word1 -> word2 -> word3 |
|                                   11 | word6 -> word7 -> word0 -> word1 -> word2 -> word3 -> word4 -> word5 |

The general case of burst transfers assumes that the external memory has 32-bit port size and 8-word burst length. The EBI can also burst from 16-bit port size memories, taking twice as many external beats to fetch the data as compared to a 32-bit port with the same burst length. The EBI can also burst from 16-bit or 32-bit memories that have a 4-word burst length (BL = 1 in the appropriate base register). In this case, two external 4-word burst transfers (wrapping on 4-word boundary) are performed to fulfill the internal 8-word request. This operation is considered atomic by the EBI, so the EBI does not allow other unrelated master accesses or bus arbitration to intervene between the transfers. For more details and a timing diagram, see Section 12.4.2.6.3, 'Small Access Example #3: 32-byte Read to 32-bit Port with BL = 1.'

During burst cycles, the BDIP (burst data in progress) signal is used to indicate the duration of the burst data. During the data phase of a burst read cycle, the EBI receives data from the addressed slave. If the EBI needs more than one data, it asserts the BDIP signal. Upon receiving the data prior to the last data, the EBI negates BDIP. Thus, the slave stops driving new data after it receives the negation of BDIP on the rising edge of the clock. Some slave devices have their burst length and timing configurable internally and thus may not support connecting to a BDIP pin. In this case, BDIP is driven by the EBI normally, but the output is ignored by the memory and the burst data behavior is determined by the internal configuration of the EBI and slave device. When the TBDIP bit is set in the appropriate base register, the timing for BDIP is altered. See Section 12.4.2.5.1, 'TBDIP Effect on Burst Transfer,' for this timing.

Since burst writes are not supported by the EBI , the EBI negates BDIP during write cycles. 1

1. Except for the special case of a 32-bit non-chip select access in 16-bit data bus mode. See Section 12.4.2.11.

## Functional Description

Figure 12-21. Basic Flow Diagram of a Burst Read Cycle

<!-- image -->

Figure 12-22. Burst 32-bit Read Cycle, Zero Wait States

<!-- image -->

Figure 12-23. Burst 32-bit Read Cycle, One Initial Wait State

<!-- image -->

## 12.4.2.5.1 TBDIP Effect on Burst Transfer

Some memories require different timing on the BDIP signal than the default to run burst cycles. Using the default value of TBDIP = 0 in the appropriate EBI base register results in BDIP being asserted (SCY+1) cycles after the address transfer phase, and being held asserted throughout the cycle regardless of the wait

states between beats (BSCY). Figure 12-24 shows an example of the TBDIP = 0 timing for a 4-beat burst with BSCY = 1.

Figure 12-24. Burst 32-bit Read Cycle, One Wait State between Beats, TBDIP = 0

<!-- image -->

When using  TBDIP = 1,  the  BDIP  behavior  changes  to  toggle  between  every  beat  when  BSCY  is  a non-zero value. Figure 12-25 shows an example of the TBDIP = 1 timing for the same four-beat burst shown in Figure 12-24.

Figure 12-25. Burst 32-bit Read Cycle, One Wait State between Beats, TBDIP = 1

<!-- image -->

## 12.4.2.6 Small Accesses (Small Port Size and Short Burst Length)

In this context, a small access refers to an access whose burst length and port size are such that the number of bytes requested by the internal master cannot all be fetched (or written) in one external transaction. This is the case when the base register's burst length bit (EBI\_BR n [BL]) and port size bit (EBI\_BR n [PS]) are set such that one of two situations occur:

- · Burst accesses are inhibited and the number of bytes requested by the master is greater than the port size (16 or 32 bit) can accommodate in a single access.
- · Burst accesses are enabled and the number of bytes requested by the master is greater than the selected burst length (4 words or 8 words).

If this is the case, the EBI initiates multiple transactions until all the requested data is transferred. It should be  noted  that  all  the  transactions  initiated  to  complete  the  data  transfer  are  considered  as  an  atomic transaction, so the EBI does not allow other unrelated master accesses to intervene between the transfers. In external master mode, this means that the EBI keeps BB asserted and does not grant the bus to another master until the atomic transaction is complete.

Table 12-17 shows all the combinations of burst length, port size, and requested byte count that cause the EBI to run multiple external transactions to fulfill the request.

Table 12-17. Small Access Cases

| Byte Count Requested by Internal Master                          | Burst Length                                                     | Port Size                                                        | # External Accesses to Fulfill Request                           |
|------------------------------------------------------------------|------------------------------------------------------------------|------------------------------------------------------------------|------------------------------------------------------------------|
| Non-Burstable Chip-Select Banks (BI=1) or Non-Chip-Select Access | Non-Burstable Chip-Select Banks (BI=1) or Non-Chip-Select Access | Non-Burstable Chip-Select Banks (BI=1) or Non-Chip-Select Access | Non-Burstable Chip-Select Banks (BI=1) or Non-Chip-Select Access |
| 4                                                                | 1 beat                                                           | 16-bit                                                           | 2/1 1                                                            |
| 8                                                                | 1 beat                                                           | 32-bit                                                           | 2                                                                |
| 8                                                                | 1 beat                                                           | 16-bit                                                           | 4                                                                |
| 32                                                               | 1 beat                                                           | 32-bit                                                           | 8                                                                |
| 32                                                               | 1 beat                                                           | 16-bit                                                           | 16                                                               |
| Burstable Chip-Select Banks (BI=0)                               | Burstable Chip-Select Banks (BI=0)                               | Burstable Chip-Select Banks (BI=0)                               | Burstable Chip-Select Banks (BI=0)                               |
| 32                                                               | 4 words                                                          | 16-bit (8 beats), 32-bit (4 beats)                               | 2                                                                |

1 In 32-bit data bus mode (DBM=0 in EBI\_MCR), two accesses are performed. In 16-bit data bus mode (DBM=1), one 2-beat burst access is performed and this is not considered a small access case. See Section 12.4.2.11, 'Non-Chip-Select Burst in 16-bit Data Bus Mode' for this special DBM=1 case.

In most cases, the timing for small accesses is the same as for normal single-beat and burst accesses, except that multiple back-to-back external transfers are executed for each internal request. These transfers have no additional dead cycles in-between that are not present for back-to-back stand-alone transfers except for the case of writes with an internal request size greater than 64 bits, discussed in Section 12.4.2.6.2, 'Small Access Example #2: 32-byte Write with External TA.'

The following sections show a few examples of small accesses. The timing for the remaining cases in Table 12-17 can be extrapolated from these and the other timing diagrams in this document.

## 12.4.2.6.1 Small Access Example #1: 32-bit Write to 16-bit Port

Figure 12-26 shows an example of a 32-bit write to a 16-bit port, requiring two 16-bit external transactions.

Figure 12-26. Single Beat 32-bit Write Cycle, 16-bit Port Size, Basic Timing

<!-- image -->

## 12.4.2.6.2 Small Access Example #2: 32-byte Write with External TA

Figure 12-27 shows an example of a 32-byte write to a non-chip select device, such as an external master, using external TA, requiring eight 32-bit external transactions. Note that due to the use of external TA, RD\_WR does not toggle between the accesses unless that access is the end of a 64-bit boundary. In this case, an extra cycle is required between TA and the next TS in order to get the next 64-bits of write data internally and RD\_WR negates during this extra cycle.

<!-- image -->

- This extra cycle is required after accesses 2, 4, and 6 in order to get the next 64-bits of internal write data. *
- Four more external accesses (not shown) are required to complete the internal 32-byte request. The timing of these is the same as accesses 1-4 shown in this diagram. **

Figure 12-27. 32-Byte Write Cycle with External TA, Basic Timing

## 12.4.2.6.3 Small Access Example #3: 32-byte Read to 32-bit Port with BL = 1

Figure 12-28 shows an example of a 32-byte read to a 32-bit burst enabled port with burst length of 4 words, requiring two 16-byte external transactions. For this case, the address for the second 4-word burst access is calculated by adding 0x10 to the lower 5 bits of the first address (no carry), and then masking out the lower 4 bits to fix them at zero.

Table 12-18. Examples of 4-word Burst Addresses

| 1st Address   | Lower 5 bits of 1st Address + 0x10 (no carry)   | Final 2nd Address (After Masking Lower 4 Bits)   |
|---------------|-------------------------------------------------|--------------------------------------------------|
| 0x000         | 0x10                                            | 0x10                                             |
| 0x008         | 0x18                                            | 0x10                                             |
| 0x010         | 0x00                                            | 0x00                                             |
| 0x018         | 0x08                                            | 0x00                                             |
| 0x020         | 0x30                                            | 0x30                                             |
| 0x028         | 0x38                                            | 0x30                                             |
| 0x030         | 0x20                                            | 0x20                                             |
| 0x038         | 0x28                                            | 0x20                                             |

Figure 12-28. 32-Byte Read with Back-to-Back 16-Byte Bursts to 32-bit Port, Zero Wait States

<!-- image -->

## 12.4.2.7 Size, Alignment, and Packaging on Transfers

Table 12-19 shows the allowed sizes that an internal or external master can request from the EBI. The behavior of the EBI for request sizes not shown below is undefined. No error signal is asserted for these erroneous cases.

Table 12-19. Transaction Sizes Supported by EBI

|   No. Bytes (Internal Master) | No. Bytes (External Master)   |
|-------------------------------|-------------------------------|
|                             1 | 1                             |
|                             2 | 2                             |
|                             4 | 4                             |
|                             8 |                               |
|                            32 |                               |

The EBI supports only natural address alignment:

- · Byte access can have any address.
- · 16-bit access, address bit 31 must be 0.
- · 32-bit access, address bits 30-31 must be 0.
- · For burst accesses of any size, address bits 29-31 must be 0.

The EBI does not support misaligned accesses. If a misaligned access to the EBI is attempted by an internal master,  the  EBI  errors  the  access  on  the  internal  bus  and  does  not  start  the  access  (nor  assert  TEA) externally. This means the EBI never generates a misaligned external access, so a multi-master system with two  eSys  MCUs  can  never  have  a  misaligned  external  access.  In  the  erroneous  case  that  an externally-initiated misaligned access does occur, the EBI errors the access (by asserting TEA externally) and does not initiate the access on the internal bus.

## External Bus Interface (EBI)

The bus requires that the portion of the data bus used for a transfer to/from a particular port size be fixed. A 32-bit port must reside on data bus bits 0-31, and a 16-bit port must reside on bits 0-15.

In the following figures and tables the following convention is adopted:

- · The most significant byte of a 32-bit operand is OP0, and OP3 is the least significant byte.
- · The two bytes of a 16-bit operand are OP0 (most significant) and OP1, or OP2 (most significant) and OP3, depending on the address of the access.
- · The single byte of a byte-length operand is OP0, OP1, OP2, or OP3, depending on the address of the access.

The convention can be seen in Figure 12-29.

Figure 12-29. Internal Operand Representation

<!-- image -->

Figure 12-30 shows the device connections on the DATA[0:31] bus.

Figure 12-30. Interface to Different Port Size Devices

<!-- image -->

Table 12-20 lists the bytes required on the data bus for read cycles. The bytes indicated as '-' are not required during that read cycle.

Table 12-20. Data Bus Requirements for Read Cycles

| Transfer Size   | TSIZ[0:1]   | Address   | Address   | 32-Bit Port Size   | 32-Bit Port Size   | 32-Bit Port Size   | 32-Bit Port Size   | 16-Bit Port Size 1   | 16-Bit Port Size 1   |
|-----------------|-------------|-----------|-----------|--------------------|--------------------|--------------------|--------------------|----------------------|----------------------|
| Transfer Size   | TSIZ[0:1]   | A30       | A31       | D0:D7              | D8:D15             | D16:D23            | D24:D31            | D0:D7                | D8:D15               |
| Byte            | 01          | 0         | 0         | OP0                | -                  | -                  | -                  | OP0                  | -                    |
| Byte            | 01          | 0         | 1         | -                  | OP1                | -                  | -                  | -                    | OP1                  |
| Byte            | 01          | 1         | 0         | -                  | -                  | OP2                | -                  | OP2                  | -                    |
| Byte            | 01          | 1         | 1         | -                  | -                  | -                  | OP3                | -                    | OP3                  |
| 16-bit          | 10          | 0         | 0         | OP0                | OP1                | -                  | -                  | OP0                  | OP1                  |
| 16-bit          | 10          | 1         | 0         | -                  | -                  | OP2                | OP3                | OP2                  | OP3                  |
| 32-bit          | 00          | 0         | 0         | OP0                | OP1                | OP2                | OP3                | OP0/OP2 2            | OP1/OP3              |

1 Also applies when DBM=1 for 16-bit data bus mode.

2 This case consists of two 16-bit external transactions, the first fetching OP0 and OP1, the second fetching OP2 and OP3.

Table 12-21 lists the patterns of the data transfer for write cycles when accesses are initiated by the MCU. The bytes indicated as '-' are not driven during that write cycle.

Table 12-21. Data Bus Contents for Write Cycles

| Transfer Size   | TSIZ[0:1]   | Address   | Address   | 32-Bit Port Size   | 32-Bit Port Size   | 32-Bit Port Size   | 32-Bit Port Size   | 16-Bit Port Size 1   | 16-Bit Port Size 1   |
|-----------------|-------------|-----------|-----------|--------------------|--------------------|--------------------|--------------------|----------------------|----------------------|
| Transfer Size   | TSIZ[0:1]   | A30       | A31       | D0:D7              | D8:D15             | D16:D23            | D24:D31            | D0:D7                | D8:D15               |
| Byte            | 01          | 0         | 0         | OP0                | -                  | -                  | -                  | OP0                  | -                    |
| Byte            | 01          | 0         | 1         | OP1                | OP1                | -                  | -                  | -                    | OP1                  |
| Byte            | 01          | 1         | 0         | OP2                | -                  | OP2                | -                  | OP2                  | -                    |
| Byte            | 01          | 1         | 1         | OP3                | OP3                | -                  | OP3                | -                    | OP3                  |
| 16-bit          | 10          | 0         | 0         | OP0                | OP1                | -                  | -                  | OP0                  | OP1                  |
| 16-bit          | 10          | 1         | 0         | OP2                | OP3                | OP2                | OP3                | OP2                  | OP3                  |
| 32-bit          | 00          | 0         | 0         | OP0                | OP1                | OP2                | OP3                | OP0/OP2 2            | OP1/OP3              |

1 Also applies when DBM=1 for 16-bit data bus mode.

2 This case consists of two 16-bit external transactions, the first writing OP0 and OP1, the second writing OP2 and OP3.

## 12.4.2.8 Arbitration

The external bus design provides for a single bus master at any one time, either the MCU or an external device. One of the external devices on the bus has the capability of becoming bus master for the external bus. Bus arbitration may be handled either by an external central bus arbiter or by the internal on-chip arbiter. The arbitration configuration (external or internal) is set via the EARB bit in the EBI\_MCR.

Each bus master must have bus request, bus grant, and bus busy signals. The signals are described in detail in Section 12.2.1, 'Detailed Signal Descriptions.' The device that needs the bus asserts the bus request (BR) signal. The device then waits for the arbiter to assert the bus grant (BG) signal. In addition, the new master must sample the bus busy (BB) signal to ensure that no other master is driving the bus before it can

assert bus busy to assume ownership of the bus. The new master must sample bus busy negated for two cycles before asserting bus busy, to avoid any potential conflicts. Any time the arbiter has taken the bus grant away from the master, and the master wants to execute a new cycle, the master must re-arbitrate before  a  new  cycle  can  begin.  The  EBI,  however,  whether  the  internal  or  external  arbiter  is  used, guarantees data coherency for access to a small port size and for decomposed bursts. This means that the EBI does not release the bus before the completion of the transactions which are considered as atomic.

Figure 12-31 describes the basic protocol for bus arbitration.

Figure 12-31. Bus Arbitration Flow Chart

<!-- image -->

## 12.4.2.8.1 External (or Central) Bus Arbiter

The external arbiter can be either another MCU in a two master system, or a separate central arbiter device. When an MCU is configured to use external arbitration, that MCU asserts BR when it needs ownership of the external bus, and it waits for BG to be asserted from the external arbiter. For timing reasons, a latched (1 cycle delayed) version of BG is used by the EBI in external arbitration mode. This is not a requirement of the protocol. After BG assertion is received and BB is sampled negated for two cycles, the MCU asserts BB and initiates the  transaction.  An  MCU  operating  under  external arbitration  may  run  back-to-back accesses  without  rearbitrating  as  long  as  it  is  still  receiving  BG  asserted.  If  BG  is  negated  during  a transaction, the MCU must rearbitrate for the bus before the next transaction. The determination of priority between masters is determined entirely by the external arbiter in this mode.

Figure 12-32 shows example timing for the case of two masters connected to a central arbiter. In this case, the BR0 and BR1 signals shown are inputs to the arbiter from the BR pin of each master. The BG0 and BG1 signals are outputs from the arbiter that connect to the BG pin of each master.

Figure 12-32. Central Arbitration Timing Diagram

<!-- image -->

## 12.4.2.8.2 Internal Bus Arbiter

When an MCU is configured to use the internal bus arbiter, that MCU is parked on the bus. The parking feature allows the MCU to skip the bus request phase, and if BB is negated, assert BB, and initiate the transaction  without  waiting  for  bus  grant  from  the  arbiter.  The  priority  between  internal  and  external masters over the external bus is determined by the EARP field of the EBI\_MCR. See Table 12-8 for the EARP field description.

By default, internal and external masters are treated with equal priority, with each having to relinquish the bus after the current transaction if another master is requesting it. If internal and external requests for the bus occur in the same cycle, the internal arbiter grants the bus to the master who least recently used the bus. If no other master is requesting the bus, the bus continues to be granted to the current master, and the current master may start another access without re-arbitrating for the bus.

If the priority field is configured for unequal priority between internal and external masters, then whenever requests are pending from both masters, the one with higher priority is always granted the bus. However, in all cases, a transaction in progress (or that has already been granted, for example MCU bus wait and external bus wait states) is allowed to complete, even when a request from a higher priority master is pending.

There is a minimum of one cycle between the positive edge CLKOUT that a BR assertion is sampled by the EBI and the positive edge CLKOUT where BG is driven out asserted by the EBI. This is to avoid timing problems that would otherwise limit the frequency of operation in external master mode.

The external master is given 2 cycles to start its access after a posed CLKOUT in which bus grant was given to it by the internal arbiter (BG asserted, BB negated for 2 cycles). This means when BG is negated (to take away bus grant from the external master), the EBI does not start an access of its own for 3 cycles (1 extra cycle in order to detect external BB assertion). If the external master jumps on the bus (by asserting

BB) during the 2-cycle window, the EBI detects the BB assertion and delays starting its access until the external master access has completed (BB negated for 2 cycles). Figure 12-33 shows this 2-cycle window of opportunity.

I

<!-- image -->

- Earliest cycle M0 can assert BB if M1 has not asseretd BB yet. *

Figure 12-33. Internal Arbitration, 2-Cycle Window-of-Opportunity

Figure 12-34 shows example timing for the case of one master using internal arbitration (master 0), while another master is configured for external arbitration (master 1). In this case, the BR signals of each master are connected together, since only master 1 drives BR. The BG signals of each master are also connected together, since only master 0 drives BG. See Figure 12-37 for an example of these connections.

Figure 12-34. Internal/External Arbitration Timing Diagram (EARP = 1)

<!-- image -->

Table 12-22 shows a description of the states defined for the internal arbiter protocol.

## Table 12-22. Internal Arbiter State Descriptions

| State          | Description                                                                                                  | Outputs          |
|----------------|--------------------------------------------------------------------------------------------------------------|------------------|
| MCU Owner Idle | MCU owns bus, but is not currently running a transaction                                                     | BG = 1, BB = hiZ |
| Ext. Owner     | Ext. master owns bus, may or may not be running a transaction                                                | BG = 0, BB = hiZ |
| MCU Bus Wait   | MCUownsbusfornexttransaction, waiting for ext. owner to negate BB from current transaction in progress       | BG = 1, BB = hiZ |
| MCU Owner Busy | MCU owns bus, and is currently running a transaction                                                         | BG = 1, BB = 0/1 |
| Ext. Bus Wait  | Ext. master owns bus for next transaction, waiting for MCU to negate BB from current transaction in progress | BG = 0, BB = 0/1 |

Table 12-23 shows the truth table for the internal arbiter protocol.

## Table 12-23. Internal Arbiter Truth Table

| State          | Outputs   | Outputs   | Inputs           | Inputs           | Inputs                                          | Inputs                               | Inputs                                                            | Inputs            | Next State     |
|----------------|-----------|-----------|------------------|------------------|-------------------------------------------------|--------------------------------------|-------------------------------------------------------------------|-------------------|----------------|
| State          | BG        | BB 1      | BR 2 (previ ous) | BB 3 (previ ous) | MCU Internal Request Pending (IRP) 4 (previous) | External has Higher Priority (EHP) 5 | MCU Ext. Transaction in Progress (or starting next cycle) (ETP) 6 | Recent BG (RBG) 7 | Next State     |
| MCU Owner Idle | 1         | hiZ       | 1                | X                | 0                                               | 0                                    | 0                                                                 | X 8               | MCU Owner Idle |
| MCU Owner Idle | 1         | hiZ       | X                | X                | 0                                               | 1                                    | 0                                                                 | X 9               | Ext. Owner     |
| MCU Owner Idle | 1         | hiZ       | 0                | X                | 0                                               | X                                    | 0                                                                 | X                 | Ext. Owner     |
| MCU Owner Idle | 1         | hiZ       | 0                | X                | X                                               | 1                                    | 0                                                                 | X                 | Ext. Owner     |
| MCU Owner Idle | 1         | hiZ       | X                | X                | 1                                               | 0                                    | X                                                                 | X                 | MCU Owner Busy |
| MCU Owner Idle | 1         | hiZ       | 1                | X                | 1                                               | X                                    | X                                                                 | X                 | MCU Owner Busy |
| MCU Owner Idle | 1         | hiZ       | X                | X                | X                                               | X                                    | 1                                                                 | X                 | MCU Owner Busy |
| Ext. Owner     | 0         | hiZ       | X                | X                | 0                                               | X                                    | X 10                                                              | X 11              | Ext. Owner     |
| Ext. Owner     | 0         | hiZ       | 0                | X                | X                                               | 1                                    | X                                                                 | X                 | Ext. Owner     |
| Ext. Owner     | 0         | hiZ       | X                | X                | 1                                               | 0                                    | X                                                                 | X                 | MCU Bus Wait   |
| Ext. Owner     | 0         | hiZ       | 1                | X                | 1                                               | X                                    | X                                                                 | X                 | MCU Bus Wait   |
| MCU Bus Wait   | 1         | hiZ       | X                | 0                | X 12                                            | X                                    | X 10                                                              | X                 | MCU Bus Wait   |
| MCU Bus Wait   | 1         | hiZ       | X                | X                | X                                               | X                                    | X                                                                 | 1                 | MCU Bus Wait   |
| MCU Bus Wait   | 1         | hiZ       | X                | 1                | X                                               | X                                    | X                                                                 | 0                 | MCU Owner Busy |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 12-23. Internal Arbiter Truth Table  (continued)

| State          | Outputs   | Outputs   | Inputs           | Inputs           | Inputs                                          | Inputs                               | Inputs                                                            | Inputs            |                |
|----------------|-----------|-----------|------------------|------------------|-------------------------------------------------|--------------------------------------|-------------------------------------------------------------------|-------------------|----------------|
| State          | BG        | BB 1      | BR 2 (previ ous) | BB 3 (previ ous) | MCU Internal Request Pending (IRP) 4 (previous) | External has Higher Priority (EHP) 5 | MCU Ext. Transaction in Progress (or starting next cycle) (ETP) 6 | Recent BG (RBG) 7 | Next State     |
| MCU Owner Busy | 1         | 0/1 13    | 1                | X                | X                                               | X                                    | 1                                                                 | X 8               | MCU Owner Busy |
| MCU Owner Busy | 1         | 0/1       | 1                | X                | 1                                               | X                                    | X                                                                 | X                 | MCU Owner Busy |
| MCU Owner Busy | 1         | 0/1       | X                | X                | 1                                               | 0                                    | X                                                                 | X                 | MCU Owner Busy |
| MCU Owner Busy | 1         | 0/1       | 0                | X                | X                                               | 1                                    | 1                                                                 | X                 | Ext. Bus Wait  |
| MCU Owner Busy | 1         | 0/1       | 0                | X                | 0                                               | X                                    | 1                                                                 | X                 | Ext. Bus Wait  |
| MCU Owner Busy | 1         | 0/1       | 0                | X                | X                                               | 1                                    | 0                                                                 | X                 | Ext. Owner     |
| MCU Owner Busy | 1         | 0/1       | 0                | X                | 0                                               | X                                    | 0                                                                 | X                 | Ext. Owner     |
| MCU Owner Busy | 1         | 0/1       | 1                | X                | 0                                               | X                                    | 0                                                                 | X                 | MCU Owner Idle |
| Ext. Bus Wait  | 0         | 0/1 13    | X 14             | X                | X                                               | X                                    | 1                                                                 | X 8               | Ext. Bus Wait  |
| Ext. Bus Wait  | 0         | 0/1       | X                | X                | X                                               | X                                    | 0                                                                 | X                 | Ext. Owner     |

- 1 The Output column for BB shows the value EBI drives on BB for each state.
- 2 The Input column for BR shows the value driven on BR the previous cycle from an external source. The state machine uses the previous clock value to avoid potential speed paths with trying to calculate bus grant based on a late-arriving external BR signal.
- 3 The Input column for BB shows the value driven on BB the previous cycle from an external source. The state machine uses the previous clock value to ensure adequate switching time between masters driving the same signal and to avoid potential speed paths.
- 4 This represents an internal EBI signal that indicates whether an internal request for use of the external bus is pending. Once a transaction for a pending request has been started on the external bus, this internal signal is cleared. The state machine uses the previous clock value to avoid potential speed paths with trying to calculate bus grant based on a late-arriving internal request signal.
- 5 This represents an internal EBI signal that indicates whether the internal MCU (0) or external master (1) currently has higher priority.
- 6 This represents an internal EBI signal that indicates whether an EBI-mastered transaction on the bus is in progress this cycle or is going to start the next cycle (and thus has already been committed internally).
- 7 This represents an internal EBI signal that indicates whether the bus was granted to an external master (BG = 0, previous BB = 1) during the previous 3 cycles.
- 8 RGB is always low in this state, thus it is ignored in the transition logic.
- 9 RGB is always low in this state, thus it is ignored in the transition logic.
- 10 The ETP signal is never asserted in states where it is shown as an 'X' for all transitions.
- 11 RGB is always high in this state, thus it is ignored in the transition logic.

- 12 IRP is ignored (treated as 1) in the MCU\_WAIT state because the EBI does not optimally support an internal master cancelling its bus request. If IRP is negated in this state, the EBI still grants the internal master the bus as if IRP was still asserted, and a few cycles may be wasted before the external master may be able to grab the bus again (depending on BR, BB, etc., according to normal transition logic).
- 13 The default BB output is 0 for this state. However, anytime the EBI transitions from a state where BB = 0 to a state where BB = hiZ, there is one external cycle (in this state) where the EBI drives BB = 1 to actively negate the pin before letting go to hiZ. In the case where a second granted internal request (IRP = 1, ETP=1) is ready to start just before the transition to the hiZ state would otherwise have occurred (during the BB = 1active negate cycle), then BB is driven back to 0 to start the next access without ever leaving this state or going to hiZ.
- 14 BR is ignored (treated as 0) in the EXT\_WAIT state because the EBI does not optimally support an external master cancelling its bus request. If BR is negated in this state, the EBI still grants the external master the bus as if BR was still asserted, and a few cycles may be wasted while the external master 'window-of-opportunity' is satisfied before the internal master may be able to grab the bus again (depending on BR, BB, etc., according to normal transition logic).

Figure 12-35 shows the internal finite state machine that implements the arbiter protocol.

Figure 12-35. Internal Bus Arbitration State Machine

<!-- image -->

## 12.4.2.9 Termination Signals Protocol

The termination signals protocol was defined in order to avoid electrical contention on lines that can be driven by various sources. In order to do that, a slave must not drive signals associated with the data transfer until the address phase is completed and it recognizes the address as its own. The slave must disconnect from signals immediately after it acknowledges the cycle and not later than the termination of the next address phase cycle.

For EBI-mastered non-chip select accesses, the EBI requires assertion of TA from an external device to signal that the bus cycle is complete. The EBI uses a latched version of TA (1 cycle delayed) for these accesses to help make timing at high frequencies. This results in the EBI driving the address and control signals 1 cycle longer than required, as seen in Figure 12-36. However, the DATA does not need to be held 1 cycle longer by the slave, because the EBI latches DATA every cycle during non-chip select accesses. During these accesses, the EBI does not drive the TA signal, leaving it up to an external device (or weak internal pull-up) to drive TA.

For EBI-mastered chip select accesses, the EBI drives TA the entire cycle, asserting according to internal wait state counters to terminate the cycle. During idle periods on the external bus, the EBI drives TA negated as long as it is granted the bus; when it no longer owns the bus it lets go of TA. When an external master does a transaction to internal address space, the EBI only drives TA for the cycle it asserts TA to return data and for 1 cycle afterwards to ensure fast negation.

If no device responds by asserting TA within the programmed timeout period (BMT in EBI\_BMCR) after the EBI initiates the bus cycle, the internal bus monitor (if enabled) asserts TEA to terminate the cycle. An external device may also drive TEA when it detects an error on an external transaction. TEA assertion causes the cycle to terminate and the processor to enter exception processing for the error condition. To properly control termination of a bus cycle for a bus error with external circuitry, TEA must be asserted at the same time or before (external) TA is asserted. TEA must be negated before the second rising edge after it was sampled asserted in order to avoid the detection of an error for the following bus cycle initiated. TEA is only driven by the EBI during the cycle where the EBI is asserting TEA and the cycle immediately following this assertion (for fast negation). During all other cycles, the EBI relies on a weak internal pull-up to hold TEA negated. This allows an external device to assert TEA when it needs to indicate an error. External devices must follow the same protocol as the EBI, only driving TEA during the assertion cycle and 1 cycle afterwards for negation.

## NOTE

In the case where an external master asserts TEA to timeout a transaction to an  internal  address  on  this  MCU,  the  EBI  has  no  way  to  terminate  the transfer internally. Therefore, any subsequent TS assertions by the external master  are  ignored  by  the  EBI  until  the  original  transfer  has  completed internally and the EBI has returned to an idle state. The expectation is that the internal slaves will always respond with either valid data or an error indication within a reasonable period of time to avoid hanging the system.

When TEA is asserted from an external source, the EBI uses a latched version of TEA (1 cycle delayed) to help make timing at high frequencies. This means that for any accesses where the EBI drives TA (chip select accesses and external master accesses to EBI), a TEA assertion that occurs 1 cycle before or during the last TA of the access could be ignored by the EBI, since it will have completed the access internally before it detects the latched TEA assertion. This means that non-burst chip select accesses with no wait states (SCY = 0) cannot be reliably terminated by external TEA. If external error termination is required for such a device, the EBI must be configured for SCY ≥ 1.

## NOTE

For  the  cases  discussed  above  where  TEA  could  be  ignored,  this  is  not guaranteed. For some small access cases (which always use chip select and internally-driven TA), a TEA that occurs 1 cycle before or during the TA cycle or for SCY = 0 may in fact lead to terminating the cycle with error. However, proper error termination is not guaranteed for these cases, so TEA must always be asserted at least 2 cycles before an internally-driven TA cycle for proper error termination.

External TEA assertion that occurs during the same cycle that TS is asserted by the EBI is always treated as an error (terminating the access) regardless of SCY.

Table 12-24 summarizes how the EBI recognizes the termination signals provided from an external device.

Table 12-24. Termination Signals Protocol

| TEA 1    | TA 1     | Action                      |
|----------|----------|-----------------------------|
| Negated  | Negated  | No Termination              |
| Asserted | X        | Transfer Error Termination  |
| Negated  | Asserted | Normal Transfer Termination |

- 1 Latched version (1 cycle delayed) used for externally driven TEA and TA.

Figure 12-36 shows an example of the termination signals protocol for back-to-back reads to two different slave devices who properly take turns driving the termination signals. This assumes a system using slave devices that drive termination signals.

<!-- image -->

Figure 12-36. Termination Signals Protocol Timing Diagram

## 12.4.2.10 Bus Operation in External Master Mode

In the MPC5554, external master mode enables an external master to access the internal address space of the MCU. Figure 12-37 shows how to connect an MCU to an external master (2nd MCU) and a shared SDR  memory  to  operate  in  external  master  mode.  Only  master/slave  systems  are  supported  in  the MPC5553; master to master systems are not supported. Refer to 12.5.5.

<!-- image -->

* Only ADDR[8:29] are connected to the 32-bit SDR memory.

Figure 12-37. MCU Connected to External Master and SDR Memory

When the external master requires external bus accesses, it takes ownership on the external bus, and the direction of most of the bus signals is inverted, relative to its direction when the MCU owns the bus.

To operate two masters in external master mode, one must be configured for internal arbitration and the other must be configured for external arbitration. Connecting three or more masters together in the same system is not supported by this EBI.

Most of the bidirectional signals shown in Figure 12-37 are only driven by the EBI when the EBI owns the external bus. The only exceptions are the TA and TEA signals (described in Section 12.4.2.9, 'Termination Signals Protocol') and the DATA bus, which are driven by the EBI for external master reads to internal address space. As long as the external master device follows the same protocol for driving signals as this EBI, there is no need to use the open drain mode of the pads configuration module for any EBI pins.

The PowerPC storage reservation protocol is not supported by the EBI. Coherency between multiple masters must be maintained via software techniques, such as event passing.

## External Bus Interface (EBI)

The EBI does not provide memory controller services to an external master that accesses shared external memories. Each master must properly configure its own memory controller and drive its own chip selects when sharing a memory between two masters.

The EBI does not support burst accesses from an external master; only single accesses of 8, 16, or 32 bits can be performed. 1

## 12.4.2.10.1 Address Decoding for External Master Accesses

The EBI allows external masters to access internal address space when the EBI is configured for external master mode. The external address is compared for any external master access, in order to determine if EBI operation is required. Because only 24 address bits are available on the external bus, special decoding logic is required to allow an external master to access on-chip locations whose upper 8 address bits are non-zero. This is done by using the upper 4 external address bits (ADDR[8:11]) as a code to determine whether the access is on-chip and if so, which internal slave it is targeted for.

Below is the address compare sequence:

- · External master access to another device - If ADDR[8] = 0, then the access is assumed to be to another device and is ignored by the EBI.
- · External master access to valid internal slave - If ADDR[8] = 1, then ADDR[9:11] are checked versus a list of 3-bit codes  to determine which internal slave to forward the access to. The upper 8 internal address bits are set appropriately by the EBI according to this 3-bit code, and internal address bits [8:11] are set appropriately to match the internal slave selected.
- · External master access to invalid internal slave - If the 3-bit code does not match a valid internal slave, then the EBI responds with a bus error.

Table 12-25 shows the possible 3-bit codes that are associated with various slaves in the MCU, as well as the  resulting  upper  12  address  bits  required  to  appropriately  match up  with  the  memory  map  of  each internal slave.

Table 12-25. EBI Internal Slave Address Decoding

| Internal Slave       | External ADDR[8:11] 1   | Internal Addr [0:7] 2   | Internal Addr [8:11] 3   |
|----------------------|-------------------------|-------------------------|--------------------------|
| - (off-chip)         | 0b0xxx                  | -                       | -                        |
| Internal Flash       | 0b10xx                  | 0b0000_0000             | 0b00, ADDR[10:11]        |
|                      | 0b1100                  | 0b0100_0000             | 0b0000                   |
| Reserved             | 0b1101                  | 0b0110_0000             | 0b0000                   |
| Bridge A Peripherals | 0b1110                  | 0b1100_0011             | 0b1111                   |
| Bridge B Peripherals | 0b1111                  | 0b1111_1111             | 0b1111                   |

1 Value on upper 4 bits of 24-bit external address bus ADDR[8:31]. ADDR[8] determines whether the access is on or off chip.

2 Value on upper 8 bits of 32-bit internal address bus.

3 Value on bits 8:11 of 32-bit internal address bus.

1. Except for the special case of a 32-bit non-chip select access in 16-bit data bus mode. See Section 12.4.2.11, 'Non-Chip-Select Burst in 16-bit Data Bus Mode'.

## 12.4.2.10.2 Bus Transfers Initiated by an External Master

The external master gets ownership of the bus (see Section 12.4.2.8, 'Arbitration') and asserts TS in order to initiate an external master access. The access is directed to the internal bus only if the input address matches to the internal address space. The access is terminated with either TA or TEA. If the access was successfully completed, the MCU asserts TA, and the external master can proceed with another external master access, or relinquish the bus. If an address or data error was detected internally, the MCU asserts TEA for one clock.

Figure 12-38 and Figure 12-39 illustrate the basic flow of read and write external master accesses.

<!-- image -->

- External arbiter is the EBI unless a central arbiter device is used. **

Determined by the internal arbiter of the external master device. ***

Figure 12-38. Basic Flow Diagram of an External Master Read Access

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

<!-- image -->

- This refers to whether the external master device is configured for external or internal arbitration. *
- External arbiter is the EBI unless a central arbiter device is used. **
- Determined by the internal arbiter of the external master device. ***

Figure 12-39. Basic Flow Diagram of an External Master Write Cycle

Figure 12-40 and Figure 12-41 describe read and write cycles from an external master accessing internal space in the MCU. Note that the minimal latency for an external master access is 3 clock cycles. The actual

latency of an external to internal cycle varies depending on which internal module is being accessed and how much internal bus traffic is going on at the time of the access.

<!-- image -->

- If the external master is another MCU with this EBI, then BB and other control pins are turned off * as shown due to use of latched TA internally. This extra cycle is not required by the slave EBI.

Figure 12-40. External Master Read from MCU

<!-- image -->

- If the external master is another MCU with this EBI, then BB and other control pins are turned off * as shown due to use of latched TA internally. This extra cycle is not required by the slave EBI.
- If the external master is another MCU with this EBI, then DATA remains valid as shown due to use of latched TA internally. These extra data valid cycles (past TA) are not required by the slave EBI. **

Figure 12-41. External Master Write to MCU

## 12.4.2.10.3 Bus Transfers Initiated by the EBI in External Master Mode

The flow and timing for EBI-mastered transactions in external master mode is identical to that described in earlier sections for single master mode, with the exception that the EBI must now arbitrate for the bus before each transaction. The flow and timing diagrams below show the arbitration sequence added to Figure 12-9 and Figure 12-10 for the basic single beat read case. The remaining cases (writes, bursts, etc.) can be obtained by adding the arbitration sequence to the flow and timing diagrams shown for single master mode in earlier sections. See Section 12.4.2.4, 'Single Beat Transfer,' and Section 12.4.2.5, 'Burst Transfer.'

## Functional Description

Figure 12-42. Basic Flow Diagram of an EBI Read Access in External Master Mode

<!-- image -->

Figure 12-43. Single Beat CS Read Cycle in External Master Mode, Zero Wait States

<!-- image -->

## 12.4.2.10.4 Back-to-Back Transfers in External Master Mode

The following timing diagrams show examples of back-to-back accesses in external master mode. In these examples, the reads and writes shown are to a shared external memory, and the EBI is assumed to be configured for internal arbitration while the external master is configured for external arbitration.

Figure 12-44 shows an external master read followed by an MCU read to the same chip select bank. Figure 12-45 shows an MCU read followed by an external master read to a different chip select bank. Figure 12-46 shows an external master read followed by an external master write to a different chip select bank. This case assumes the MCU has no higher priority internal request pending and is able to park the external master on the bus.

Figure 12-44. External Master Read followed by MCU Read to Same CS Bank

<!-- image -->

## External Bus Interface (EBI)

Figure 12-45. MCU Read followed by External Master Read to Different CS Bank

<!-- image -->

Figure 12-46. External Master Read followed by External Master Write to Different CS Bank

<!-- image -->

## 12.4.2.11 Non-Chip-Select Burst in 16-bit Data Bus Mode

The timing diagrams in this section apply only to the special case of a non-chip select 32-bit access in 16-bit data bus mode. They specify the behavior for both the EBI-master and EBI-slave, as the external master is expected to be another MCU with this EBI.

For  this  case,  a  special  2-beat  burst  protocol  is  used  for  reads  and  writes,  so  that  the  EBI-slave  can internally generate one 32-bit read or write access (thus 32-bit coherent), as opposed to two separate 16-bit accesses.

Figure 12-47 shows a 32-bit read from an external master in 16-bit data bus mode.

Figure 12-48 shows a 32-bit write from an external master in 16-bit data bus mode.

Figure 12-47. External Master 32-bit Read from MCU with DBM=1

<!-- image -->

Figure 12-48. External Master 32-bit Write to MCU with DBM=1

<!-- image -->

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## 12.4.2.12 Calibration Bus Operation - MPC5553 Only

The MPC5553 EBI has a second external bus, intended for calibration use. This bus consists of a second set of the same signals present on the primary external bus, except that arbitration, (and optionally other signals also) are excluded. Both busses are supported by the EBI by using the calibration chip selects to steer accesses to the calibration bus instead of to the primary external bus.

Because the calibration bus has no arbitration signals, the arbitration on the primary bus controls accesses on the calibration bus as well, and no external master accesses can be performed on the calibration bus. Accesses cannot be performed in parallel on both external busses. However, back-to-back accesses can switch from one bus to the other, as determined by the type of chip select each address matches.

The timing diagrams and protocol for the calibration bus is identical to the primary bus, except that some signals are missing on the calibration bus.

There is an inherent dead cycle between a calibration chip select access and a non-calibration access (chip select or non-chip select), just like the one between accesses to two different non-calibration chip selects (described in Section 12.4.2.4.3, 'Back-to-Back Accesses').

Figure 12-49 shows an example of a non-calibration chip select read access followed by a calibration chip select  read  access.  Note  that  this  figure  is  identical  to  Figure 12-18,  except  the  CSy  is  replaced  by CAL\_CSy. Timing for other cases on the calibration bus can similarly be derived from other figures in this document (by replacing CS with CAL\_CS).

Figure 12-49. Back-to-Back 32-bit Reads to CS, CAL\_CS Banks

<!-- image -->

## 12.5 Initialization/Application Information

## 12.5.1 Booting from External Memory

The EBI block does not support booting directly to external memory (i.e. fetching the first instruction after reset externally). The MPC5553 and MPC5554 use an internal boot assist module, which executes after each reset. The BAM code performs basic configuration of the EBI block, allowing for external boot if desired. Refer to Chapter 16, 'Boot Assist Module (BAM)' for detail information about the boot modes supported by the MPC5554.

If code in external memory needs to write EBI registers, this must be done in a way that avoids modifying EBI registers while external accesses are being performed, such as the following method:

- · Copy the code that is doing the register writes (plus a return branch) to internal SRAM
- · Branch to internal SRAM to run this code, ending with a branch back to external flash

## 12.5.2 Running with SDR (Single Data Rate) Burst Memories

This includes FLASH and external SRAM memories with a compatible burst interface. BDIP is required only for some SDR memories. Figure 12-47 shows a block diagram of an MCU connected to a 32-bit SDR burst memory.

<!-- image -->

- *May or may not be connected, depending on the memory used.
- Flash memories typically use one WE signal as shown, RAMs use 2 or 4 (16-bit or 32-bit). **
- *** MPC5553 Only

Figure 12-50. MCU Connected to SDR Burst Memory

Refer to Figure 12-22 for an example of the timing of a typical burst read operation to an SDR burst memory. Refer to Figure 12-14 for an example of the timing of a typical single write operation to SDR memory.

## 12.5.3 Running with Asynchronous Memories

The EBI also supports asychronous memories. In this case, the CLKOUT, TS, and BDIP pins are not used by the memory and bursting is not supported. However, the EBI still drives these outputs, and always drives and latches all signals at positive edge CLKOUT (i.e., there is no asynchronous mode for the EBI). The data timing is controlled by setting the SCY bits in the appropriate option register to the proper number

of wait states to work with the access time of the asynchronous memory, just as done for a synchronous memory.

## 12.5.3.1 Example Wait State Calculation

This example applies to any chip select memory, synchronous or asynchronous.

As an example, say  we  have  a  memory  with  50ns  access  time,  and  we  are  running  the  external  bus @66MHz (CLKOUT period: 15.2ns). Assume the input data spec for the MCU is 4ns.

number of wait states = (access time) / (CLKOUT period) + (0 or 1) (depending on setup time)

50/15.2 = 3 with 4.4ns remaining (so we need at least three wait states, now check setup time)

15.2-4.4=10.8ns (this is the achieved input data setup time)

Because  actual  input  setup  (10.8ns)  is  greater  than  the  input  setup  spec  (4.0ns),  three  wait  states  is sufficient. If the actual input setup was less than 4.0ns, we would have to use four wait states instead.

## 12.5.3.2 Timing and Connections for Asynchronous Memories

The connections to an asynchronous memory are the same as for a synchronous memory, except that the CLKOUT, TS, and BDIP signals are not used. Figure 12-51 shows a block diagram of an MCU connected to an asynchronous memory.

<!-- image -->

- Flash memories typically use one WE signal as shown, RAMs use 2 or 4 (16-bit or 32-bit). *

Figure 12-51. MCU Connected to Asynchronous Memory

Figure 12-52 shows a timing diagram of a read operation to a 16-bit asynchronous memory using three wait states. Figure 12-53 shows a timing diagram of a write operation to a 16-bit asynchronous memory using three wait states.

Figure 12-52. Read Operation to Asynchronous Memory, Three Initial Wait States

<!-- image -->

Figure 12-53. Write Operation to Asynchronous Memory, Three Initial Wait States

<!-- image -->

## 12.5.4 Connecting an MCU to Multiple Memories

The MCU can be connected to more than one memory at a time.

Figure 12-54 shows an example of how two memories could be connected to one MCU.

<!-- image -->

- *May or may not be connected, depending on the memory used.
- Flash memories typically use one WE signal as shown, RAMs use 2 or 4 (16-bit or 32-bit). **

Figure 12-54. MCU Connected to Multiple Memories

## 12.5.5 Dual-MCU Operation with Reduced Pinout MCUs

Some MCUs with this EBI may not have all the pins described in this document pinned out for a particular package. Some of the most common pins to be removed are DATA[16:31], arbitration pins (BB, BG, BR), and TSIZ[0:1]. This section describes how to configure dual-MCU systems for each of these scenarios. More than one section may apply if the applicable pins are not present on one or both MCUs.

## 12.5.5.1 Connecting 16-bit MCU to 32-bit MCU (Master/Master or Master/Slave)

This scenario is straightforward. Simply connect DATA[0:15] between both MCUs, and configure both for 16-bit  data  bus  mode  operation  (DBM=1  in  EBI\_MCR).  Note  that  32-bit  external  memories  are  not supported in this scenario.

## 12.5.5.2 Arbitration with No Arb Pins (Master/Slave only)

Without arbitration pins, a dual-master system is impossible, because these is no way for the two masters to take turns driving the external bus without conflicts. However, a master/slave system is possible, as described below.

To implement a master/slave system with an MCU that has no arbitration pins (BB, BG, BR), the user must configure  the  master  MCU  for  internal  arbitration  (EARB=0  in  EBI\_MCR)  and  the  slave  MCU  for external arbitration (EARB=1). Internally on an MCU with no arbitration pins, the BR, BG, and BB signals to the EBI will be tied negated. This means that the slave MCU will never receive bus grant asserted, so it will never attempt to start an access on the external bus. The master MCU will never receive bus request or  bus  busy  asserted,  so  it  will  maintain  ownership  of  the  bus  without  any  arbitration  delays.  In  the erroneous case that the slave MCU executes internal code that attempts to access external address space, that access will never get external and will eventually time-out in the slave MCU.

## 12.5.5.3 Transfer Size with No TSIZ Pins (Master/Master or Master/Slave)

Since there are no TSIZ pins to communicate transfer size from master MCU to slave MCU, the internal SIZE field of the EBI\_MCR must be used on the slave MCU (by setting SIZEN=1 in slave's EBI\_MCR). Anytime the master MCU needs to read or write the slave MCU with a different transfer size than the current value of the slave's SIZE field, the master MCU must first write the slave's SIZE field with the correct size for the subsequent transaction.

## 12.5.5.4 No Transfer Acknowledge (TA) Pin

If an MCU has no TA pin available, this restricts the MCU to chip select accesses only. Non-chip select accesses have no way for the EBI to know which cycle to latch the data. The EBI has no built-in protection to prevent non-chip select accesses in this scenario; it is up to the user to make certain they set up chip selects and external memories correctly to ensure all external accesses fall in a valid chip select region.

## 12.5.5.5 No Transfer Error (TEA) Pin

If an MCU has no TEA pin available, this eliminates the feature of terminating an access with TEA. This means if an access times out in the EBI bus monitor, the EBI (master) will still terminate the access early, but there will be no external visibility of this termination, so the slave device might end up driving data much later, when a subsequent access is already underway. Therefore, the EBI bus monitor should be disabled when no TEA pin exists.

## 12.5.5.6 No Burst Data in Progress (BDIP) Pin

If an MCU has no BDIP pin available, this eliminates burst support only if the burstable memory being used requires BDIP to burst. Many external memories use a self-timed configurable burst mechanism that does not require a dynamic burst indicator. Check the applicable external memory specification to see if BDIP is required in your system.

## 12.5.6 Summary of Differences from MPC5xx

Below is a summary list of the significant differences between this EBI used in the MPC5553/MPC5554 and that of the MPC5xx parts:

- · SETA feature is no longer available
- - Chip select devices cannot use external TA, instead must use wait state configuration.

- · No memory controller support for external masters
- - Must configure each master in multi-master system to drive its own chip selects
- · Changes in bit fields:
- - Removed these variable timing attributes from option register: CSNT, ACS, TRLX, EHTR
- - Removed LBDIP base register bit, now late BDIP assertion is default behavior
- - Modified TSIZ[0:1] functionality to only indicate size of current transfer, not give information on ensuing transfers that may be part of the same atomic sequence
- - The BL field of the base register has inverted logic from the MPC56x devices (0 = 8-beat burst on the MPC5500, 1 = 8-beat burst on the MPC56x)
- · Removed reservation support on external bus
- · Removed address type (AT), write-protect (WP), and dual-mapping features because these functions can be replicated by memory management unit (MMU) in e200z6 core
- · Removed support for 8-bit ports
- · Removed boot chip select operation - On-chip boot assist module (BAM) handles boot (and configuration of EBI registers)
- · Open drain mode and pull-up resistors no longer required for multi-master systems, extra cycle needed to switch between masters
- · Modified arbitration protocol to require extra cycles when switching between masters
- · Added support for 32-bit coherent read and write non-chip select accesses in 16-bit data bus mode
- · Misaligned accesses are not supported
- · The MPC5553 has calibration features implemented by four calibration chip selects
- · Removed support for 3-master systems
- · Address decoding for external master accesses uses 4-bit code to determine internal slave instead of straight address decode

## 12.6 Revision History

| Substantive Changes since Rev 3.0                                                              |
|------------------------------------------------------------------------------------------------|
| In Section 12.1.2, 'Overview,' changed 'internal SRAM' t o 'external SRAM'.                    |
| Changed references to 4 CAL_CS chip selects CAL_CS[0:3] to 3 CAL_CS chip selects [0] and [2:3] |

External Bus Interface (EBI)
