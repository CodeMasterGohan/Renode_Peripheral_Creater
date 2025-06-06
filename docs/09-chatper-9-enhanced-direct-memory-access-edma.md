### Chatper 9 Enhanced Direct Memory Access (eDMA)

## 9.1 Introduction

This chapter describes the MPC5553/MPC5554's enhanced direct memory access (eDMA) controller, a second-generation module capable of performing complex data transfers with minimal intervention from a host processor.

## 9.1.1 Block Diagram

Figure 9-1 is a block diagram of the eDMA module.

<!-- image -->

Request

Figure 9-1. eDMA Block Diagram

## 9.1.2 Overview

The enhanced direct memory access (eDMA) controller hardware microarchitecture includes a DMA engine  which  performs  source  and  destination  address  calculations,  and  the  actual  data  movement operations, along with SRAM-based local memory containing the transfer control descriptors (TCD) for the channels.

## 9.1.3 Features

The eDMA is a highly-programmable data transfer engine, which has been optimized to minimize the required intervention from the host processor. It is intended for use in applications where the data size to be transferred is statically known, and is not defined within the data packet itself. The eDMA module features:

- · All data movement via dual-address transfers: read from source, write to destination
- - Programmable source, destination addresses, transfer size, plus support for enhanced addressing modes

- · 64-channel (MPC5554) or 32-channel (MPC5553) implementation performs complex data transfers with minimal intervention from a host processor
- - 32 bytes of data registers, used as temporary storage to support burst transfers (refer to SSIZE bit)
- - Connections to the crossbar switch for bus mastering the data movement
- · Transfer control descriptor (TCD) organized to support two-deep, nested transfer operations - 32-byte TCD per channel stored in local memory
- - An inner data transfer loop defined by a minor byte transfer count
- - An outer data transfer loop defined by a major iteration count
- · Channel activation via one of three methods:
- - Explicit software initiation
- - Initiation via a channel-to-channel linking mechanism for continual transfers
- - Peripheral-paced hardware requests (one per channel)

## NOTE

For all three methods, one activation per execution of the minor loop is required

- · Support for fixed-priority and round-robin channel arbitration
- · Channel completion reported via optional interrupt requests
- - One interrupt per channel, optionally asserted at completion of major iteration count
- - Error terminations are enabled per channel, and logically summed together to form two optional error interrupts (MPC5554) or a single error interrupt (MPC5553).
- · Support for scatter/gather DMA processing
- · Any channel can be programmed so that it can be suspended by a higher priority channel's activation, before completion of a minor loop.

Throughout this chapter, n is used to reference the channel number. Additionally, data sizes are defined as byte (8-bit), half-word (16-bit), word (32-bit) and double-word (64-bit).

## 9.1.4 Modes of Operation

## 9.1.4.1 Normal Mode

In normal mode, the eDMA is used to transfer data between a source and a destination. The source and destination can be a memory block or an I/O block capable of operation with the eDMA.

## 9.1.4.2 Debug Mode

If enabled by EDMA\_CR[EDBG] and the CPU enters debug mode, the eDMA will not honor any service requests when the debug input signal is asserted. If the signal is asserted during transfer of a block of data described by a minor loop in the current active channel's TCD, the eDMA will continue operation until completion of the minor loop.

## 9.2 External Signal Description

The eDMA has no external signals.

## 9.3 Memory Map/Register Definition

The eDMA's programming model is partitioned into two regions: the first region defines a number of registers providing control functions, while the second region corresponds to the local transfer control descriptor memory.

Some registers are implemented as two 32-bit registers, and include an 'H' and 'L' suffix, signaling the 'high' and 'low' portions of the control function. Table 9-1 is a 32-bit view of the eDMA's memory map.

Table 9-1. eDMA 32-bit Memory Map

| Address                      | Register Name   | Register Description                                     | Size (bits)   |
|------------------------------|-----------------|----------------------------------------------------------|---------------|
| Base (0xFFF4_4000)           | EDMA_CR         | eDMA control register                                    | 32            |
| Base + 0x0004                | EDMA_ESR        | eDMA error status register                               | 32            |
| Base + 0x0008                | EDMA_ERQRH      | eDMA enable request high register (MPC5554 only)         | 32            |
| Base + 0x000C                | EDMA_ERQRL      | eDMA enable request low register                         | 32            |
| Base + 0x0010                | EDMA_EEIRH      | eDMA enable error interrupt high register (MPC5554 only) | 32            |
| Base + 0x0014                | EDMA_EEIRL      | eDMA enable error interrupt low register                 | 32            |
| Base + 0x0018                | EDMA_SERQR      | eDMA set enable request register                         | 8             |
| Base + 0x0019                | EDMA_CERQR      | eDMA clear enable request register                       | 8             |
| Base + 0x001A                | EDMA_SEEIR      | eDMA set enable error interrupt register                 | 8             |
| Base + 0x001B                | EDMA_CEEIR      | eDMA clear enable error interrupt register               | 8             |
| Base + 0x001C                | EDMA_CIRQR      | eDMA clear interrupt request register                    | 8             |
| Base + 0x001D                | EDMA_CER        | eDMA clear error register                                | 8             |
| Base + 0x001E                | EDMA_SSBR       | eDMA set start bit register                              | 8             |
| Base + 0x001F                | EDMA_CDSBR      | eDMA clear done status bit register                      | 8             |
| Base + 0x0020                | EDMA_IRQRH      | eDMA interrupt request high register (MPC5554 only)      | 32            |
| Base + 0x0024                | EDMA_IRQRL      | eDMA interrupt request low register                      | 32            |
| Base + 0x0028                | EDMA_ERH        | eDMA error high register (MPC5554 only)                  | 32            |
| Base + 0x002C                | EDMA_ERL        | eDMA error low register                                  | 32            |
| Base + 0x0030- Base + 0x00FF | -               | Reserved                                                 | -             |
| Base + 0x0100                | EDMA_CPR0       | eDMA channel 0 priority register                         | 8             |
| Base + 0x0101                | EDMA_CPR1       | eDMA channel 1 priority register                         | 8             |
| Base + 0x0102                | EDMA_CPR2       | eDMA channel 2 priority register                         | 8             |
| Base + 0x0103                | EDMA_CPR3       | eDMA channel 3 priority register                         | 8             |
| Base + 0x0104                | EDMA_CPR4       | eDMA channel 4 priority register                         | 8             |
| Base + 0x0105                | EDMA_CPR5       | eDMA channel 5 priority register                         | 8             |
| Base + 0x0106                | EDMA_CPR6       | eDMA channel 6 priority register                         | 8             |
| Base + 0x0107                | EDMA_CPR7       | eDMA channel 7 priority register                         | 8             |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 9-1. eDMA 32-bit Memory Map (continued)

| Address                                                | Register Name                                          | Register Description                                   | Size (bits)                                            |
|--------------------------------------------------------|--------------------------------------------------------|--------------------------------------------------------|--------------------------------------------------------|
| Base + 0x0108                                          | EDMA_CPR8                                              | eDMA channel 8 priority register                       | 8                                                      |
| Base + 0x0109                                          | EDMA_CPR9                                              | eDMA channel 9 priority register                       | 8                                                      |
| Base + 0x010A                                          | EDMA_CPR10                                             | eDMA channel 10 priority register                      | 8                                                      |
| Base + 0x010B                                          | EDMA_CPR11                                             | eDMA channel 11 priority register                      | 8                                                      |
| Base + 0x010C                                          | EDMA_CPR12                                             | eDMA channel 12 priority register                      | 8                                                      |
| Base + 0x010D                                          | EDMA_CPR13                                             | eDMA channel 13 priority register                      | 8                                                      |
| Base + 0x010E                                          | EDMA_CPR14                                             | eDMA channel 14 priority register                      | 8                                                      |
| Base + 0x010F                                          | EDMA_CPR15                                             | eDMA channel 15 priority register                      | 8                                                      |
| Base + 0x0110                                          | EDMA_CPR16                                             | eDMA channel 16 priority register                      | 8                                                      |
| Base + 0x0111                                          | EDMA_CPR17                                             | eDMA channel 17 priority register                      | 8                                                      |
| Base + 0x0112                                          | EDMA_CPR18                                             | eDMA channel 18 priority register                      | 8                                                      |
| Base + 0x0113                                          | EDMA_CPR19                                             | eDMA channel 19 priority register                      | 8                                                      |
| Base + 0x0114                                          | EDMA_CPR20                                             | eDMA channel 20 priority register                      | 8                                                      |
| Base + 0x0115                                          | EDMA_CPR21                                             | eDMA channel 21 priority register                      | 8                                                      |
| Base + 0x0116                                          | EDMA_CPR22                                             | eDMA channel 22 priority register                      | 8                                                      |
| Base + 0x0117                                          | EDMA_CPR23                                             | eDMA channel 23 priority register                      | 8                                                      |
| Base + 0x0118                                          | EDMA_CPR24                                             | eDMA channel 24 priority register                      | 8                                                      |
| Base + 0x0119                                          | EDMA_CPR25                                             | eDMA channel 25 priority register                      | 8                                                      |
| Base + 0x011A                                          | EDMA_CPR26                                             | eDMA channel 26 priority register                      | 8                                                      |
| Base + 0x011B                                          | EDMA_CPR27                                             | eDMA channel 27 priority register                      | 8                                                      |
| Base + 0x011C                                          | EDMA_CPR28                                             | eDMA channel 28 priority register                      | 8                                                      |
| Base + 0x011D                                          | EDMA_CPR29                                             | eDMA channel 29 priority register                      | 8                                                      |
| Base + 0x011E                                          | EDMA_CPR30                                             | eDMA channel 30 priority register                      | 8                                                      |
| Base + 0x011F                                          | EDMA_CPR31                                             | eDMA channel 31 priority register                      | 8                                                      |
| NOTE: Channels 32-63 Are Available only in the MPC5554 | NOTE: Channels 32-63 Are Available only in the MPC5554 | NOTE: Channels 32-63 Are Available only in the MPC5554 | NOTE: Channels 32-63 Are Available only in the MPC5554 |
| Base + 0x0120                                          | EDMA_CPR32                                             | eDMA channel 32 priority register                      | 8                                                      |
| Base + 0x0121                                          | EDMA_CPR33                                             | eDMA channel 33 priority register                      | 8                                                      |
| Base + 0x0122                                          | EDMA_CPR34                                             | eDMA channel 34 priority register                      | 8                                                      |
| Base + 0x0123                                          | EDMA_CPR35                                             | eDMA channel 35 priority register                      | 8                                                      |
| Base + 0x0124                                          | EDMA_CPR36                                             | eDMA channel 36 priority register                      | 8                                                      |
| Base + 0x0125                                          | EDMA_CPR37                                             | eDMA channel 37 priority register                      | 8                                                      |
| Base + 0x0126                                          | EDMA_CPR38                                             | eDMA channel 38 priority register                      | 8                                                      |
| Base + 0x0127                                          | EDMA_CPR39                                             | eDMA channel 39 priority register                      | 8                                                      |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 9-1. eDMA 32-bit Memory Map (continued)

| Address                      | Register Name   | Register Description                | Size (bits)   |
|------------------------------|-----------------|-------------------------------------|---------------|
| Base + 0x0128                | EDMA_CPR40      | eDMA channel 40 priority register   | 8             |
| Base + 0x0129                | EDMA_CPR41      | eDMA channel 41 priority register   | 8             |
| Base + 0x012A                | EDMA_CPR42      | eDMA channel 42 priority register   | 8             |
| Base + 0x012B                | EDMA_CPR43      | eDMA channel 43 priority register   | 8             |
| Base + 0x012C                | EDMA_CPR44      | eDMA channel 44 priority register   | 8             |
| Base + 0x012D                | EDMA_CPR45      | eDMA channel 45 priority register   | 8             |
| Base + 0x012E                | EDMA_CPR46      | eDMA channel 46 priority register   | 8             |
| Base + 0x012F                | EDMA_CPR47      | eDMA channel 47 priority register   | 8             |
| Base + 0x0130                | EDMA_CPR48      | eDMA channel 48 priority register   | 8             |
| Base + 0x0131                | EDMA_CPR49      | eDMA channel 49 priority register   | 8             |
| Base + 0x0132                | EDMA_CPR50      | eDMA channel 50 priority register   | 8             |
| Base + 0x0133                | EDMA_CPR51      | eDMA channel 51 priority register   | 8             |
| Base + 0x0134                | EDMA_CPR52      | eDMA channel 52 priority register   | 8             |
| Base + 0x0135                | EDMA_CPR53      | eDMA channel 53 priority register   | 8             |
| Base + 0x0136                | EDMA_CPR54      | eDMA channel 54 priority register   | 8             |
| Base + 0x0137                | EDMA_CPR55      | eDMA channel 55 priority register   | 8             |
| Base + 0x0138                | EDMA_CPR56      | eDMA channel 56 priority register   | 8             |
| Base + 0x0139                | EDMA_CPR57      | eDMA channel 57 priority register   | 8             |
| Base + 0x013A                | EDMA_CPR58      | eDMA channel 58 priority register   | 8             |
| Base + 0x013B                | EDMA_CPR59      | eDMA channel 59 priority register   | 8             |
| Base + 0x013C                | EDMA_CPR60      | eDMA channel 60 priority register   | 8             |
| Base + 0x013D                | EDMA_CPR61      | eDMA channel 61 priority register   | 8             |
| Base + 0x013E                | EDMA_CPR62      | eDMA channel 62 priority register   | 8             |
| Base + 0x013F                | EDMA_CPR63      | eDMA channel 63 priority register   | 8             |
| Base + 0x0140- Base + 0x0FFF | -               | Reserved                            | -             |
| Base + 0x1000                | TCD00           | eDMA transfer control descriptor 00 | 256           |
| Base + 0x1020                | TCD01           | eDMA transfer control descriptor 01 | 256           |
| Base + 0x1040                | TCD02           | eDMA transfer control descriptor 02 | 256           |
| Base + 0x1060                | TCD03           | eDMA transfer control descriptor 03 | 256           |
| Base + 0x1080                | TCD04           | eDMA transfer control descriptor 04 | 256           |
| Base + 0x10A0                | TCD05           | eDMA transfer control descriptor 05 | 256           |
| Base + 0x10C0                | TCD06           | eDMA transfer control descriptor 06 | 256           |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 9-1. eDMA 32-bit Memory Map (continued)

| Address                                                                    | Register Name                                                              | Register Description                                                       | Size (bits)                                                                |
|----------------------------------------------------------------------------|----------------------------------------------------------------------------|----------------------------------------------------------------------------|----------------------------------------------------------------------------|
| Base + 0x10E0                                                              | TCD07                                                                      | eDMA transfer control descriptor 07                                        | 256                                                                        |
| Base + 0x1100                                                              | TCD08                                                                      | eDMA transfer control descriptor 08                                        | 256                                                                        |
| Base + 0x1120                                                              | TCD09                                                                      | eDMA transfer control descriptor 09                                        | 256                                                                        |
| Base + 0x1140                                                              | TCD10                                                                      | eDMA transfer control descriptor 10                                        | 256                                                                        |
| Base + 0x1160                                                              | TCD11                                                                      | eDMA transfer control descriptor 11                                        | 256                                                                        |
| Base + 0x1180                                                              | TCD12                                                                      | eDMA transfer control descriptor 12                                        | 256                                                                        |
| Base + 0x11A0                                                              | TCD13                                                                      | eDMA transfer control descriptor 13                                        | 256                                                                        |
| Base + 0x11C0                                                              | TCD14                                                                      | eDMA transfer control descriptor 14                                        | 256                                                                        |
| Base + 0x11E0                                                              | TCD15                                                                      | eDMA transfer control descriptor 15                                        | 256                                                                        |
| Base + 0x1200                                                              | TCD16                                                                      | eDMA transfer control descriptor 16                                        | 256                                                                        |
| Base + 0x1220                                                              | TCD17                                                                      | eDMA transfer control descriptor 17                                        | 256                                                                        |
| Base + 0x1240                                                              | TCD18                                                                      | eDMA transfer control descriptor 18                                        | 256                                                                        |
| Base + 0x1260                                                              | TCD19                                                                      | eDMA transfer control descriptor 19                                        | 256                                                                        |
| Base + 0x1280                                                              | TCD20                                                                      | eDMA transfer control descriptor 20                                        | 256                                                                        |
| Base + 0x12A0                                                              | TCD21                                                                      | eDMA transfer control descriptor 21                                        | 256                                                                        |
| Base + 0x12C0                                                              | TCD22                                                                      | eDMA transfer control descriptor 22                                        | 256                                                                        |
| Base + 0x12E0                                                              | TCD23                                                                      | eDMA transfer control descriptor 23                                        | 256                                                                        |
| Base + 0x1300                                                              | TCD24                                                                      | eDMA transfer control descriptor 24                                        | 256                                                                        |
| Base + 0x1320                                                              | TCD25                                                                      | eDMA transfer control descriptor 25                                        | 256                                                                        |
| Base + 0x1340                                                              | TCD26                                                                      | eDMA transfer control descriptor 26                                        | 256                                                                        |
| Base + 0x1360                                                              | TCD27                                                                      | eDMA transfer control descriptor 27                                        | 256                                                                        |
| Base + 0x1380                                                              | TCD28                                                                      | eDMA transfer control descriptor 28                                        | 256                                                                        |
| Base + 0x13A0                                                              | TCD29                                                                      | eDMA transfer control descriptor 29                                        | 256                                                                        |
| Base + 0x13C0                                                              | TCD30                                                                      | eDMA transfer control descriptor 30                                        | 256                                                                        |
| Base + 0x13E0                                                              | TCD31                                                                      | eDMA transfer control descriptor 31                                        | 256                                                                        |
| NOTE: Transfer Control Descriptors 32-63 Are Available only in the MPC5554 | NOTE: Transfer Control Descriptors 32-63 Are Available only in the MPC5554 | NOTE: Transfer Control Descriptors 32-63 Are Available only in the MPC5554 | NOTE: Transfer Control Descriptors 32-63 Are Available only in the MPC5554 |
| Base + 0x1400                                                              | TCD32                                                                      | eDMA transfer control descriptor 32                                        | 256                                                                        |
| Base + 0x1420                                                              | TCD33                                                                      | eDMA transfer control descriptor 33                                        | 256                                                                        |
| Base + 0x1440                                                              | TCD34                                                                      | eDMA transfer control descriptor 34                                        | 256                                                                        |
| Base + 0x1460                                                              | TCD35                                                                      | eDMA transfer control descriptor 35                                        | 256                                                                        |
| Base + 0x1480                                                              | TCD36                                                                      | eDMA transfer control descriptor 36                                        | 256                                                                        |
| Base + 0x14A0                                                              | TCD37                                                                      | eDMA transfer control descriptor 37                                        | 256                                                                        |
| Base + 0x14C0                                                              | TCD38                                                                      | eDMA transfer control descriptor 38                                        | 256                                                                        |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 9-1. eDMA 32-bit Memory Map (continued)

| Address       | Register Name   | Register Description                |   Size (bits) |
|---------------|-----------------|-------------------------------------|---------------|
| Base + 0x14E0 | TCD39           | eDMA transfer control descriptor 39 |           256 |
| Base + 0x1500 | TCD43           | eDMA transfer control descriptor 40 |           256 |
| Base + 0x1520 | TCD41           | eDMA transfer control descriptor 41 |           256 |
| Base + 0x1540 | TCD42           | eDMA transfer control descriptor 42 |           256 |
| Base + 0x1560 | TCD43           | eDMA transfer control descriptor 43 |           256 |
| Base + 0x1580 | TCD44           | eDMA transfer control descriptor 44 |           256 |
| Base + 0x15A0 | TCD45           | eDMA transfer control descriptor 45 |           256 |
| Base + 0x15C0 | TCD46           | eDMA transfer control descriptor 46 |           256 |
| Base + 0x15E0 | TCD47           | eDMA transfer control descriptor 47 |           256 |
| Base + 0x1600 | TCD48           | eDMA transfer control descriptor 48 |           256 |
| Base + 0x1620 | TCD49           | eDMA transfer control descriptor 49 |           256 |
| Base + 0x1640 | TCD50           | eDMA transfer control descriptor 50 |           256 |
| Base + 0x1660 | TCD51           | eDMA transfer control descriptor 51 |           256 |
| Base + 0x1680 | TCD52           | eDMA transfer control descriptor 52 |           256 |
| Base + 0x16A0 | TCD53           | eDMA transfer control descriptor 53 |           256 |
| Base + 0x16C0 | TCD54           | eDMA transfer control descriptor 54 |           256 |
| Base + 0x16E0 | TCD55           | eDMA transfer control descriptor 55 |           256 |
| Base + 0x1700 | TCD56           | eDMA transfer control descriptor 56 |           256 |
| Base + 0x1720 | TCD57           | eDMA transfer control descriptor 57 |           256 |
| Base + 0x1740 | TCD58           | eDMA transfer control descriptor 58 |           256 |
| Base + 0x1760 | TCD59           | eDMA transfer control descriptor 59 |           256 |
| Base + 0x1780 | TCD60           | eDMA transfer control descriptor 60 |           256 |
| Base + 0x17A0 | TCD61           | eDMA transfer control descriptor 61 |           256 |
| Base + 0x17C0 | TCD62           | eDMA transfer control descriptor 62 |           256 |
| Base + 0x17E0 | TCD63           | eDMA transfer control descriptor 63 |           256 |

## 9.3.1 Register Descriptions

Reading reserved bits in a register will return the value of zero. Writes to reserved bits in a register will be ignored. Reading or writing to a reserved memory location will generate a bus error.

Many of the control registers have a bit width that matches the number of channels implemented in the module, or 64-bits in size. These registers are implemented as two 32-bit registers, and include an 'H' and 'L' suffixes, signaling the 'high' and 'low' portions of the control function. Note that for the MPC5553, only the Low register is implemented for its 32 channels. High (H) registers are reserved on the MPC5553 and accessing them will generate a bus error.

## 9.3.1.1 eDMA Control Register (EDMA\_CR)

The 32-bit EDMA\_CR defines the basic operating configuration of the eDMA.

For the MPC5554  the eDMA arbitrates channel service requests in four groups (0, 1, 2, 3) of 16 channels each; the MPC5553 arbitrates channel service requests in two groups (0, 1). For the MPC5553/MPC5554, group 0 contains channels 0-15 and group 1 contains channels 16-31; but for the MPC5554 only, group 2 contains channels 32-47, and group 3 contains channels 48-63.

Arbitration within a group can be configured to use either a fixed priority or a round robin.    In fixed priority arbitration, the highest priority channel requesting service is selected to execute. The priorities are assigned  by  the  channel  priority  registers  (see  Section 9.3.1.15).  In  round  robin  arbitration  mode,  the channel priorities are ignored and the channels within each group are cycled through, from channel 15 down to channel 0,  without regard to priority.

The group priorities operate in a similar fashion. In group fixed priority arbitration mode, channel service requests in the highest priority group are executed first where priority level 3 (in the MPC5554; priority level 1 for the MPC5553) is the highest and priority level 0 is the lowest. The group priorities are assigned in the GRP n PRI fields of the eDMA control register (EDMA\_CR). All group priorities must have unique values prior to any channel service requests occur, otherwise a configuration error will be reported. In group round robin mode, the group priorities are ignored and the groups are cycled through, from group 3 down to group 0, without regard to priority.

Figure 9-2. eDMA Control Register (EDMA\_CR)

<!-- image -->

|          | 0             | 1             | 2             | 3             | 4             | 5             | 6             | 7             | 8             | 9             | 10            | 11            | 12            | 13            | 14            | 15            |
|----------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| R        | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| W        |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset    | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Reg Addr | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 |
|          | 16            | 17            | 18            | 19            | 20            | 21            | 22            | 23            | 24            | 25            | 26            | 27            | 28            | 29            | 30            | 31            |
| R        | GRP3PRI 1     | GRP3PRI 1     | GRP2PRI 1     | GRP2PRI 1     | GRP1PRI 2     | GRP1PRI 2     | GRP0PRI 3     | GRP0PRI 3     | 0             | 0             | 0             | 0             | ERGA          | ERCA          | EDBG          | 0             |
| W        |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset    | 1             | 1             | 1             | 0             | 0             | 1             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Reg Addr | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 |

- 1 Available only in the MPC5554.
- 2 In the MPC5553, only bit 21 is used
- 3 In the MPC5553, only bit 23 is used

Table 9-2. EDMA\_CR Field Descriptions

| Bits   | Name    | Description                                                                                                                            |
|--------|---------|----------------------------------------------------------------------------------------------------------------------------------------|
| 0-15   | -       | Reserved.                                                                                                                              |
| 16-17  | GRP3PRI | Channel group 3 priority. Group 3 priority level when fixed priority group arbitration is enabled. Note: Available only in the MPC5554 |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 9-2. EDMA\_CR Field Descriptions (continued)

| Bits   | Name    | Description                                                                                                                                                                                                                                                                                                                                    |
|--------|---------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 18-19  | GRP2PRI | Channel group 2 priority. Group 2 priority level when fixed priority group arbitration is enabled. Note: Available only in the MPC5554                                                                                                                                                                                                         |
| 20-21  | GRP1PRI | Channel group 1 priority. Group 1 priority level when fixed priority group arbitration is enabled. Note: In the MPC5553, only bit 21 is used                                                                                                                                                                                                   |
| 22-23  | GRP0PRI | Channel group 0 priority. Group 0 priority level when fixed priority group arbitration is enabled. Note: In the MPC5553, only bit 23 is used                                                                                                                                                                                                   |
| 24-27  | -       | Reserved.                                                                                                                                                                                                                                                                                                                                      |
| 28     | ERGA    | Enable round robin group arbitration. 0 Fixed priority arbitration is used for selection among the groups. 1 Round robin arbitration is used for selection among the groups.                                                                                                                                                                   |
| 29     | ERCA    | Enable round robin channel arbitration. 0 Fixed priority arbitration is used for channel selection within each group. 1 Round robin arbitration is used for channel selection within each group.                                                                                                                                               |
| 30     | EDBG    | Enable debug. 0 The assertion of the system debug control input is ignored. 1 The assertion of the system debug control input causes the eDMA to stall the start of a new channel. Executing channels are allowed to complete. Channel execution will resume when either the system debug control input is negated or the EDBG bit is cleared. |
| 31     | -       | Reserved.                                                                                                                                                                                                                                                                                                                                      |

## 9.3.1.2 eDMA Error Status Register (EDMA\_ESR)

The EDMA\_ESR provides information concerning the last recorded channel error. Channel errors can be caused by a configuration error (an illegal setting in the transfer control descriptor or an illegal priority register setting in fixed arbitration mode) or an error termination to a bus master read or write cycle.

A configuration error is caused when the starting source or destination address, source or destination offsets, minor loop byte count, and the transfer size represent an inconsistent state. The addresses and offsets must be aligned on 0-modulo-transfer\_size boundaries, and the minor loop byte count must be a multiple  of  the  source  and  destination  transfer  sizes.  All  source  reads  and  destination  writes  must  be configured to the natural boundary of the programmed transfer size respectively.

In fixed arbitration mode, a configuration error is caused by any two channel priorities being equal within a  group,  or  any  group  priority  levels  being  equal  among  the  groups.  For  either  type  of  priority configuration error, the ERRCHN field is undefined. All channel priority levels within a group must be unique and all group priority levels among the groups must be unique when fixed arbitration mode is enabled.

If a scatter/gather operation is enabled upon channel completion, a configuration error is reported if the scatter/gather address (DLAST\_SGA) is not aligned on a 32-byte boundary. If minor loop channel linking is enabled upon channel completion, a configuration error is reported when the link is attempted if the TCD.CITER.E\_LINK bit does not equal the TCD.BITER.E\_LINK bit. All configuration error conditions except scatter/gather and minor loop link error are reported as the channel is activated and assert an error interrupt request if enabled. When properly enabled, a scatter/gather configuration error is reported when

the scatter/gather operation begins at major loop completion. A minor loop channel link configuration error is reported when the link operation is serviced at minor loop completion.

If a system bus read or write is terminated with an error, the data transfer is immediately stopped and the appropriate bus error flag is set. In this case, the state of the channel's transfer control descriptor is updated by the eDMA engine with the current source address, destination address, and minor loop byte count at the point of the fault. If a bus error occurs on the last read prior to beginning the write sequence, the write will execute using the data captured during the bus error. If a bus error occurs on the last write prior to switching to the next read sequence, the read sequence will execute before the channel is terminated due to the destination bus error.

The occurrence of any type of error causes the eDMA engine to stop the active channel, and the appropriate channel bit in the eDMA error register to be asserted. At the same time, the details of the error condition are  loaded  into  the  EDMA\_ESR.  The  major  loop  complete    indicators,  setting  the  transfer  control descriptor DONE flag and the possible assertion of an interrupt request, are not affected when an error is detected. Once the error status has been updated, the eDMA engine continues to operate by servicing the next appropriate channel. A channel that experiences an error condition is not automatically disabled. If a channel is terminated by an error and then issues another service request before the error is fixed, that channel will execute and terminate with the same error condition.

Figure 9-3. eDMA Error Status Register (EDMA\_ESR)

<!-- image -->

|          | 0             | 1             | 2             | 3             | 4             | 5             | 6             | 7             | 8             | 9             | 10            | 11            | 12            | 13            | 14            | 15            |
|----------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| R        | VLD           | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| W        |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset    | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Reg Addr | Base + 0x0004 | Base + 0x0004 | Base + 0x0004 | Base + 0x0004 | Base + 0x0004 | Base + 0x0004 | Base + 0x0004 | Base + 0x0004 | Base + 0x0004 | Base + 0x0004 | Base + 0x0004 | Base + 0x0004 | Base + 0x0004 | Base + 0x0004 | Base + 0x0004 | Base + 0x0004 |
|          | 16            | 17            | 18            | 19            | 20            | 21            | 22            | 23            | 24            | 25            | 26            | 27            | 28            | 29            | 30            | 31            |
| R        | GPE           | CPE           | ERRCHN        | ERRCHN        | ERRCHN        | ERRCHN        | ERRCHN        | ERRCHN        | SAE           | SOE           | DAE           | DOE           | NCE           | SGE           | SBE           | DBE           |
| W        |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset    | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Reg Addr | Base + 0x0004 | Base + 0x0004 | Base + 0x0004 | Base + 0x0004 | Base + 0x0004 | Base + 0x0004 | Base + 0x0004 | Base + 0x0004 | Base + 0x0004 | Base + 0x0004 | Base + 0x0004 | Base + 0x0004 | Base + 0x0004 | Base + 0x0004 | Base + 0x0004 | Base + 0x0004 |

Table 9-3. EDMA\_ESR Field Descriptions

| Bits   | Name   | Description                                                                                                                                                                                                         |
|--------|--------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0      | VLD    | Logical OR of all EDMA_ERH and EDMA_ERL status bits. 0 No EDMA_ER bits are set. 1 At least one EDMA_ERbit is set indicating a valid error exists that has not been cleared.                                         |
| 1-15   | -      | Reserved.                                                                                                                                                                                                           |
| 16     | GPE    | Group priority error. 0 No group priority error. 1 The last recorded error was a configuration error among the group priorities indicating not all group priorities are unique.                                     |
| 17     | CPE    | Channel priority error. 0 No channel priority error. 1 The last recorded error was a configuration error in the channel priorities within a group, indicating not all channel priorities within a group are unique. |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 9-3. EDMA\_ESR Field Descriptions (continued)

| Bits   | Name         | Description                                                                                                                                                                                                                                                                                                                                                                                            |
|--------|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 18-23  | ERRCHN [0:5] | Error channel number -this is the channel number of the last recorded error (excluding GPE and CPE errors) Note: Donot rely on the number in the ERRCHNfield for group and channel priority errors. Group and channel priority errors need to be resolved by inspection. The application code must interrogate the priority registers to find groups or channels with duplicate priority level.        |
| 24     | SAE          | Source address error. 0 No source address configuration error. 1 The last recorded error was a configuration error detected in the TCD.SADDR field, indicating TCD.SADDR is inconsistent with TCD.SSIZE.                                                                                                                                                                                               |
| 25     | SOE          | Source offset error. 0 No source offset configuration error. 1 The last recorded error was a configuration error detected in the TCD.SOFF field, indicating TCD.SOFF is inconsistent with TCD.SSIZE.                                                                                                                                                                                                   |
| 26     | DAE          | Destination address error. 0 No destination address configuration error. 1 The last recorded error was a configuration error detected in the TCD.DADDR field, indicating TCD.DADDR is inconsistent with TCD.DSIZE.                                                                                                                                                                                     |
| 27     | DOE          | Destination offset error. 0 No destination offset configuration error. 1 The last recorded error was a configuration error detected in the TCD.DOFF field, indicating TCD.DOFF is inconsistent with TCD.DSIZE.                                                                                                                                                                                         |
| 28     | NCE          | NBYTES/CITER configuration error. 0 No NBYTES/CITER configuration error. 1 The last recorded error was a configuration error detected in the TCD.NBYTES or TCD.CITER fields, indicating the following conditions exist: GLYPH<127> TCD.NBYTES is not a multiple of TCD.SSIZE and TCD.DSIZE, or GLYPH<127> TCD.CITER is equal to zero, or GLYPH<127> TCD.CITER.E_LINK is not equal to TCD.BITER.E_LINK. |
| 29     | SGE          | Scatter/gather configuration error. 0 No scatter/gather configuration error. 1 The last recorded error was a configuration error detected in the TCD.DLAST_SGA field, indicating TCD.DLAST_SGA is not on a 32-byte boundary. This field is checked at the beginning of a scatter/gather operation after major loop completion if TCD.E_SG is enabled.                                                  |
| 30     | SBE          | Source bus error. 0 No source bus error. 1 The last recorded error was a bus error on a source read.                                                                                                                                                                                                                                                                                                   |
| 31     | DBE          | Destination bus error. 0 No destination bus error. 1 The last recorded error was a bus error on a destination write.                                                                                                                                                                                                                                                                                   |

## 9.3.1.3 eDMA Enable Request Registers (EDMA\_ERQRH, EDMA\_ERQRL)

The EDMA\_ERQRH and EDMA\_ERQRL provide a bit map for the 64 (MPC5554) or 32 (MPC5553) implemented channels to enable the request signal for each channel. For the MPC5554, EDMA\_ERQRH supports channels 63-32, while EDMA\_ERQRL  covers  channels 31-00. For the MPC5553,

EDMA\_ERQRL maps to channels 31-0. EDMA\_ERQRH is reserved on the MPC5553 and accessing it will result in a bus error.

The state of any given channel enable is directly affected by writes to these registers; the state is also affected by writes to the EDMA\_SERQR  and EDMA\_CERQR.  The EDMA\_CERQR  and EDMA\_SERQR are provided so that the request enable for a single channel can easily be modified without the need to perform a read-modify-write sequence to the EDMA\_ERQRH and EDMA\_ERQRL.

Both  the  DMA  request  input  signal  and  this  enable  request  flag  must  be  asserted  before  a  channel's hardware service request is accepted. The state of the eDMA enable request flag does not affect a channel service request made explicitly through software or a linked channel request.

Figure 9-5. eDMA Enable Request Low Register (EDMA\_ERQRL)

|          | 0             | 1             | 2             | 3             | 4             | 5             | 6             | 7             | 8             | 9             | 10            | 11            | 12            | 13            | 14            | 15            |
|----------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| R W      | ERQ 63        | ERQ 62        | ERQ 61        | ERQ 60        | ERQ 59        | ERQ 58        | ERQ 57        | ERQ 56        | ERQ 55        | ERQ 54        | ERQ 53        | ERQ 52        | ERQ 51        | ERQ 50        | ERQ 49        | ERQ 48        |
| Reset    | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Reg Addr | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 |
|          | 16            | 17            | 18            | 19            | 20            | 21            | 22            | 23            | 24            | 25            | 26            | 27            | 28            | 29            | 30            | 31            |
| R W      | ERQ 47        | ERQ 46        | ERQ 45        | ERQ 44        | ERQ 43        | ERQ 42        | ERQ 41        | ERQ 40        | ERQ 39        | ERQ 38        | ERQ 37        | ERQ 36        | ERQ 35        | ERQ 34        | ERQ 33        | ERQ 32        |
| Reset    | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Reg Addr | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 |

<!-- image -->

Table 9-4. EDMA\_ERQRH, EDMA\_ERQRL Field Descriptions

| Bits   | Name   | Description                                                                                                                                   |
|--------|--------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| 0-31   | ERQ n  | Enable DMA hardware service request n. 0 The DMA request signal for channel n is disabled. 1 The DMA request signal for channel n is enabled. |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

As a given channel completes the processing of its major iteration count, there is a flag in the transfer control  descriptor  that  may  affect  the  ending  state  of  the  EDMA\_ERQR  bit  for  that  channel.  If  the TCD.D\_REQ bit is  set,  then  the  corresponding  EDMA\_ERQR  bit  is  cleared  after  the  major  loop  is complete, disabling the DMA hardware request. Otherwise if the D\_REQ bit is cleared, the state of the EDMA\_ERQR bit is unaffected.

## 9.3.1.4 eDMA Enable Error Interrupt Registers (EDMA\_EEIRH, EDMA\_EEIRL)

The EDMA\_EEIRH and EDMA\_EEIRL provide a bit map for the 64 channels (32 in the MPC5553) to enable the error interrupt signal for each channel. For the MPC5554, EDMA\_EEIRH supports channels 63-32, while EDMA\_EEIRL covers channels 31-00. For the MPC5553, EDMA\_EEIRL maps to channels 31-0. EDMA\_EEIRH is reserved on the MPC5553 and accessing it will result in a bus error.

The state of any given channel's error interrupt enable is directly affected by writes to these registers; it is also affected by writes to the EDMA\_SEEIR  and  EDMA\_CEEIR.  The  EDMA\_SEEIR  and EDMA\_CEEIR are provided so that the error interrupt enable for a single channel can easily be modified without the need to perform a read-modify-write sequence to the EDMA\_EEIRH and EDMA\_EEIRL.

Both the DMA error indicator and this error interrupt enable flag must be asserted before an error interrupt request for a given channel is asserted.

Figure 9-6. eDMA Enable Error Interrupt High Register (EDMA\_EEIRH)-MPC5554 Only

<!-- image -->

Figure 9-7. eDMA Enable Error Interrupt Low Register (EDMA\_EEIRL)

<!-- image -->

Table 9-5. EDMA\_EEIRH, EDMA\_EEIRL Field Descriptions

| Bits   | Name   | Description                                                                                                                                                                             |
|--------|--------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-31   | EEI n  | Enable error interrupt n. 0 The error signal for channel n does not generate an error interrupt. 1 The assertion of the error signal for channel n generate an error interrupt request. |

## 9.3.1.5 eDMA Set Enable Request Register (EDMA\_SERQR)

The  EDMA\_SERQR  provides  a  simple  memory-mapped  mechanism  to  set  a  given  bit  in  the EDMA\_ERQRH or EDMA\_ERQRL to enable the DMA request for a given channel. The data value on a register write causes the corresponding bit in the EDMA\_ERQRH  or EDMA\_ERQRL to be set. Setting bit  1  (SERQ n )  provides  a  global  set  function,  forcing  the  entire  contents  of  EDMA\_ERQRH  and EDMA\_ERQRL to be asserted. Reads of this register return all zeroes. For the MPC5553, bit 2 (SERQ1) is not used.

Figure 9-8. eDMA Set Enable Request Register (EDMA\_SERQR)

<!-- image -->

Table 9-6. EDMA\_SERQR Field Descriptions

| Bits   | Name       | Description                                                                                                                     |
|--------|------------|---------------------------------------------------------------------------------------------------------------------------------|
| 0      | -          | Reserved.                                                                                                                       |
| 1-7    | SERQ [0:6] | Set enable request. 0-63 Set the corresponding bit in EDMA_ERQRH or EDMA_ERQRL 64-127 Set all bits in EDMA_ERQRH and EDMA_ERQRL |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## 9.3.1.6 eDMA Clear Enable Request Register (EDMA\_CERQR)

The  EDMA\_CERQR  provides  a  simple  memory-mapped  mechanism  to  clear  a  given  bit  in  the EDMA\_ERQRH or EDMA\_ERQRL to disable the DMA request for a given channel. The data value on a register write causes the corresponding bit in the EDMA\_ERQRH or EDMA\_ERQRL to be cleared. Setting bit 1 (CERQ n ) provides a global clear function, forcing the entire contents of the EDMA\_ERQRH and EDMA\_ERQRL to be zeroed, disabling all DMA request inputs. Reads of this register return all zeroes. For the MPC5553, bit 2 (CERQ1)  is not used.

Figure 9-9. eDMA Clear Enable Request Register (EDMA\_CERQR)

<!-- image -->

|          | 0             | 1             | 2             | 3             | 4             | 5             | 6             | 7             |
|----------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| R        | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| W        | CERQ[0:6]     | CERQ[0:6]     | CERQ[0:6]     | CERQ[0:6]     | CERQ[0:6]     | CERQ[0:6]     | CERQ[0:6]     | CERQ[0:6]     |
| Reset    | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Reg Addr | Base + 0x0019 | Base + 0x0019 | Base + 0x0019 | Base + 0x0019 | Base + 0x0019 | Base + 0x0019 | Base + 0x0019 | Base + 0x0019 |

Table 9-7. EDMA\_CERQR Field Descriptions

| Bits   | Name       | Description                                                                                                                       |
|--------|------------|-----------------------------------------------------------------------------------------------------------------------------------|
| 0      | -          | Reserved.                                                                                                                         |
| 1-7    | CERQ [0:6] | Clear enable request. 0-63 Clear corresponding bit in EDMA_ERQRH or EDMA_ERQRL 64-127 Clear all bits in EDMA_ERQRH and EDMA_ERQRL |

## 9.3.1.7 eDMA Set Enable Error Interrupt Register (EDMA\_SEEIR)

The  EDMA\_SEEIR  provides  a  simple  memory-mapped  mechanism  to  set  a  given  bit  in  the EDMA\_EEIRH or EDMA\_EEIRL to enable the error interrupt for a given channel. The data value on a register write causes the corresponding bit in the EDMA\_EEIRH or EDMA\_EEIRL to be set. Setting bit 1 (SEEI n ) provides a global set function, forcing the entire contents of EDMA\_EEIRH or EDMA\_EEIRL to be asserted. Reads of this register return all zeroes. For the MPC5553, bit 2 (SEEI1)  is not used.

Figure 9-10. eDMA Set Enable Error Interrupt Register (EDMA\_SEEIR)

<!-- image -->

|          | 0             | 1             | 2             | 3             | 4             | 5             | 6             | 7             |
|----------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| R        | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| W        | SEEI[0:6]     | SEEI[0:6]     | SEEI[0:6]     | SEEI[0:6]     | SEEI[0:6]     | SEEI[0:6]     | SEEI[0:6]     | SEEI[0:6]     |
| Reset    | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Reg Addr | Base + 0x001A | Base + 0x001A | Base + 0x001A | Base + 0x001A | Base + 0x001A | Base + 0x001A | Base + 0x001A | Base + 0x001A |

Table 9-8. EDMA\_SEEIR Field Descriptions

| Bits   | Name       | Description                                                                                                                             |
|--------|------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| 0      | -          | Reserved.                                                                                                                               |
| 1-7    | SEEI [0:6] | Set enable error interrupt. 0-63 Set the corresponding bit in EDMA_EEIRH or EDMA_EEIRL 64-127 Set all bits in EDMA_EEIRH and EDMA_EEIRL |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## 9.3.1.8 eDMA Clear Enable Error Interrupt Register (EDMA\_CEEIR)

The  EDMA\_CEEIR  provides  a  simple  memory-mapped  mechanism  to  clear  a  given  bit  in  the EDMA\_EEIRH or EDMA\_EEIRL to disable the error interrupt for a given channel. The data value on a register write causes the corresponding bit in the EDMA\_EEIRH or EDMA\_EEIRL to be cleared. Setting bit  1  (CEEI n )  provides  a  global  clear  function,  forcing  the  entire  contents  of  the  EDMA\_EEIRH  or EDMA\_EEIRL to be zeroed, disabling error interrupts for all channels. Reads of this register return all zeroes.  For the MPC5553, bit 2 (CEEI1)  is not used.

Figure 9-11. eDMA Clear Enable Error Interrupt Register (EDMA\_CEEIR)

<!-- image -->

|          | 0             | 1             | 2             | 3             | 4             | 5             | 6             | 7             |
|----------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| R        | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| W        | CEEI[0:6]     | CEEI[0:6]     | CEEI[0:6]     | CEEI[0:6]     | CEEI[0:6]     | CEEI[0:6]     | CEEI[0:6]     | CEEI[0:6]     |
| Reset    | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Reg Addr | Base + 0x001B | Base + 0x001B | Base + 0x001B | Base + 0x001B | Base + 0x001B | Base + 0x001B | Base + 0x001B | Base + 0x001B |

Table 9-9. EDMA\_CEEIR Field Descriptions

| Bits   | Name       | Description                                                                                                                              |
|--------|------------|------------------------------------------------------------------------------------------------------------------------------------------|
| 0      | -          | Reserved.                                                                                                                                |
| 1-7    | CEEI [0:6] | Clear enable error interrupt 0-63 Clear corresponding bit in EDMA_EEIRH or EDMA_EEIRL 64-127 Clear all bits in EDMA_EEIRH and EDMA_EEIRL |

## 9.3.1.9 eDMA Clear Interrupt Request Register (EDMA\_CIRQR)

The  EDMA\_CIRQR  provides  a  simple  memory-mapped  mechanism  to  clear  a  given  bit  in  the EDMA\_IRQRH or EDMA\_IRQRL to disable the interrupt request for a given channel. The given value on a register write causes the corresponding bit in the EDMA\_IRQRH or EDMA\_IRQRL to be cleared. Setting bit 1 (CINT n ) provides a global clear function, forcing the entire contents of the EDMA\_IRQRH or EDMA\_IRQRL to be zeroed, disabling all DMA interrupt requests. Reads of this register return all zeroes.   For the MPC5553, bit 2 (CINT1)  is not used.

Figure 9-12. eDMA Clear Interrupt Request (EDMA\_CIRQR) Fields

<!-- image -->

Table 9-10. EDMA\_CIRQR Field Descriptions

| Bits   | Name       | Description                                                                                                                             |
|--------|------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| 0      | -          | Reserved.                                                                                                                               |
| 1-7    | CINT [0:6] | Clear interrupt request. 0-63 Clear the corresponding bit in EDMA_IRQRH or EDMA_IRQRL 64-127 Clear all bits in EDMA_IRQRH or EDMA_IRQRL |

## 9.3.1.10 eDMA Clear Error Register (EDMA\_CER)

The EDMA\_CER provides a simple memory-mapped mechanism to clear a given bit in the EDMA\_ERH or EDMA\_ERL to disable the error condition flag for a given channel. The given value on a register write causes the corresponding bit in the EDMA\_ERH or EDMA\_ERL to be cleared. Setting bit 1 (CERR n ) provides a global clear function, forcing the entire contents of the EDMA\_ERH and EDMA\_ERL to be zeroed, clearing all channel error indicators. Reads of this register return all zeroes.  For the MPC5553, bit 2 (CERR1)  is not used.

Figure 9-13. eDMA Clear Error Register (EDMA\_CER)

<!-- image -->

Table 9-11. EDMA\_CER Field Descriptions

| Bits   | Name       | Description                                                                                                                |
|--------|------------|----------------------------------------------------------------------------------------------------------------------------|
| 0      | -          | Reserved.                                                                                                                  |
| 1-7    | CERR [0:6] | Clear error indicator. 0-63 Clear corresponding bit in EDMA_ERH or EDMA_ERL 64-127 Clear all bits in EDMA_ERH and EDMA_ERL |

## 9.3.1.11 eDMA Set START Bit Register (EDMA\_SSBR)

The EDMA\_SSBR provides a simple memory-mapped mechanism to set the START bit in the TCD of the given channel. The data value on a register write causes the START bit in the corresponding transfer control descriptor to be set. Setting bit 1 (SSB n ) provides a global set function, forcing all START bits to be set. Reads of this register return all zeroes.  For the MPC5553, bit 2 (SSB1)  is not used.

Figure 9-14. eDMA Set START Bit Register (EDMA\_SSBR)

<!-- image -->

Table 9-12. EDMA\_SSBR Field Descriptions

| Bits   | Name      | Description                                                                                                           |
|--------|-----------|-----------------------------------------------------------------------------------------------------------------------|
| 0      | -         | Reserved.                                                                                                             |
| 1-7    | SSB [0:6] | Set START bit (channel service request). 0-63 Set the corresponding channel's TCD.START 64-127 Set all TCD.START bits |

## 9.3.1.12 eDMA Clear DONE Status Bit Register (EDMA\_CDSBR)

The EDMA\_CDSBR provides a simple memory-mapped mechanism to clear the DONE bit in the TCD of the given channel. The data value on a register write causes the DONE bit in the corresponding transfer control descriptor to be cleared. Setting bit 1 (CDSB n ) provides a global clear function, forcing all DONE bits to be cleared. Reads of this register return all zeroes.  For the MPC5553, bit 2 (CDSB1)  is not used.

Figure 9-15. eDMA Clear DONE Status Bit Register (EDMA\_CDSBR)

<!-- image -->

Table 9-13. EDMA\_CDSBR Field Descriptions

| Bits   | Name       | Description                                                                                           |
|--------|------------|-------------------------------------------------------------------------------------------------------|
| 0      | -          | Reserved.                                                                                             |
| 1-7    | CDSB [0:6] | Clear DONE status bit. 0-63 Clear the corresponding channel's DONE bit 64-127 Clear all TCD DONE bits |

## 9.3.1.13 eDMA Interrupt Request Registers (EDMA\_IRQRH, EDMA\_IRQRL)

The EDMA\_IRQRH and EDMA\_IRQRL provide a bit map for the 64 channels signaling the presence of an interrupt request for each channel.  For the MPC5554, EDMA\_IRQRH supports channels 63-32, while EDMA\_IRQRL covers  channels  31-00.  For  the  MPC5553,  EDMA\_IRQRL  maps  to  channels  31-0. EDMA\_IRQRH is reserved on the MPC5553 and accessing it will result in a bus error.

The eDMA engine signals the occurrence of a programmed interrupt upon the completion of a data transfer as defined in the transfer control descriptor by setting the appropriate bit in this register. The outputs of this register are directly routed to the interrupt controller (INTC). During the execution of the interrupt service routine associated with any given channel, it is software's responsibility to clear the appropriate bit, negating the interrupt request. Typically, a write to the EDMA\_CIRQR in the interrupt service routine is used for this purpose.

The state of any given channel's interrupt request is directly affected by writes to this register; it is also affected by writes to the EDMA\_CIRQR. On writes to the EDMA\_IRQRH or EDMA\_IRQRL, a 1 in any bit position clears the corresponding channel's interrupt request. A 0 in any bit position has no affect on the  corresponding  channel's  current  interrupt  status.  The  EDMA\_CIRQR  is  provided  so  the  interrupt

request  for  a single channel  can  easily  be  cleared  without  the  need  to  perform  a  read-modify-write sequence to the EDMA\_IRQRH and EDMA\_IRQRL.

Figure 9-16. eDMA Interrupt Request High Register (EDMA\_IRQRH)-MPC5554 Only

<!-- image -->

|          | 0             | 1             | 2             | 3             | 4             | 5             | 6             | 7             | 8             | 9             | 10            | 11            | 12            | 13            | 14            | 15            |
|----------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| R W      | INT 63        | INT 62        | INT 61        | INT 60        | INT 59        | INT 58        | INT 57        | INT 56        | INT 55        | INT 54        | INT 53        | INT 52        | INT 51        | INT 50        | INT 49        | INT 48        |
| Reset    | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Reg Addr | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 |
|          | 16            | 17            | 18            | 19            | 20            | 21            | 22            | 23            | 24            | 25            | 26            | 27            | 28            | 29            | 30            | 31            |
| R W      | INT 47        | INT 46        | INT 45        | INT 44        | INT 43        | INT 42        | INT 41        | INT 40        | INT 39        | INT 38        | INT 37        | INT 36        | INT 35        | INT 34        | INT 33        | INT 32        |
| Reset    | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Reg Addr | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 |

Figure 9-17. eDMA Interrupt Request Low Register (EDMA\_IRQRL)

<!-- image -->

Table 9-14. EDMA\_IRQRH, EDMA\_IRQRL Field Descriptions

| Bits   | Name   | Description                                                                                                                  |
|--------|--------|------------------------------------------------------------------------------------------------------------------------------|
| 0-31   | INT n  | eDMA interrupt request n. 0 The interrupt request for channel n is cleared. 1 The interrupt request for channel n is active. |

## 9.3.1.14 eDMA Error Registers (EDMA\_ERH, EDMA\_ERL)

The EDMA\_ERH and EDMA\_ERL provide a bit map for the 64 channels signaling the presence of an error for each channel.  For the MPC5554, EDMA\_ERH supports channels 63-32, while EDMA\_ERL covers channels 31-00. For the MPC5553, EDMA\_ERL maps to channels 31-0. EDMA\_ERH is reserved on the MPC5553 and accessing it will result in a bus error.

The eDMA engine signals the occurrence of a error condition by setting the appropriate bit in this register. The outputs of this register are enabled by the contents of the EDMA\_EEIR, then logically summed across groups of 16, 32, and 64 channels (MPC5554) or 16 and 32 channels (MPC5553) to form several group

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

error interrupt requests which is then routed to the interrupt controller. During the execution of the interrupt service routine associated with any DMA errors, it is software's responsibility to clear the appropriate bit, negating the error interrupt request. Typically, a write to the EDMA\_CER in the interrupt service routine is used for this purpose. Recall the normal DMA channel completion indicators, setting the transfer control descriptor DONE flag and the possible assertion of an interrupt request, are not affected when an error is detected.

The contents of this register can also be polled and a non-zero value indicates the presence of a channel error, regardless of the state of the EDMA\_EEIR. The EDMA\_ESR[VLD] bit is a logical OR of all bits in this register and it provides a single bit indication of any errors. The state of any given channel's error indicators is affected by writes to this register; it is also affected by writes to the EDMA\_CER. On writes to EDMA\_ERH or EDMA\_ERL, a 1 in any bit position clears the corresponding channel's error status. A 0 in any bit position has no affect on the corresponding channel's current error status. The EDMA\_CER is provided so the error indicator for a single channel can easily be cleared.

Figure 9-19. eDMA Error Low Register (EDMA\_ERL)

<!-- image -->

Table 9-15. EDMA\_ERH, EDMA\_ERL Field Descriptions

| Bits   | Name   | Description                                                                                   |
|--------|--------|-----------------------------------------------------------------------------------------------|
| 0-31   | ERR n  | eDMA Error n. 0 An error in channel n has not occurred. 1 An error in channel n has occurred. |

## 9.3.1.15 eDMA Channel n Priority Registers (EDMA\_CPR n )

When the fixed-priority channel arbitration mode is enabled (EDMA\_CR[ERCA] = 0), the contents of these  registers  define  the  unique  priorities  associated  with  each  channel  within  a  group.  The  channel priorities are evaluated by numeric value; that is, 0 is the lowest priority, 1 is the next higher priority, then 2, 3, etc. Software must program the channel priorities with unique values, otherwise a configuration error will be reported. The range of the priority value is limited to the values of 0 through 15. When read, the GRPPRI bits of the EDMA\_CPR  register reflect the current priority level of the group of channels in n which the corresponding channel resides. GRPPRI bits are not affected by writes to the EDMA\_CPR n registers.  The  group  priority  is  assigned  in  the  EDMA\_CR.  See  Figure 9-2  and  Table 9-2  for  the EDMA\_CR definition.

Channel preemption is enabled on a per-channel basis by setting the ECP bit in the EDMA\_CPR n register. Channel preemption allows the executing channel's data transfers to be temporarily suspended in favor of starting a higher priority channel. Once the preempting channel has completed all of its minor loop data transfers, the preempted channel is restored and resumes execution. After the restored channel completes one read/write sequence, it is again eligible for preemption. If any higher priority channel is requesting service, the restored channel will be suspended and the higher priority channel will be serviced. Nested preemption (attempting to preempt a preempting channel) is not supported. Once a preempting channel begins execution, it cannot be preempted. Preemption is only available when fixed arbitration is selected for both group and channel arbitration modes.

<!-- image -->

1 The reset value for the group and channel priority fields, GRPPRI[0-1] and CHPRI[0-3], is equal to the corresponding channel number for each priority register; that is, EDMA\_CPR31[GRPPRI] = 0b01 and EDMA\_CPR31[CHPRI] = 0b1111.

Figure 9-20. eDMA Channel n Priority Register (EDMA\_CPR n )

Table 9-16. EDMA\_CPR n Field Descriptions

|   Bits | Name   | Description                                                                                                                                                                                              |
|--------|--------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|      0 | ECP    | Enable channel preemption. 0 Channel n cannot be suspended by a higher priority channel's service request. 1 Channel n can be temporarily suspended by the service request of a higher priority channel. |
|      1 | -      | Reserved.                                                                                                                                                                                                |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 9-16. EDMA\_CPR n Field Descriptions (continued)

| Bits   | Name         | Description                                                                                                                                                                   |
|--------|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 2-3    | GRPPRI [0:1] | Channel n current group priority. Group priority assigned to this channel group when fixed-priority arbitration is enabled. These two bits are read only; writes are ignored. |
| 4-7    | CHPRI [0:3]  | Channel n arbitration priority. Channel priority when fixed-priority arbitration is enabled.                                                                                  |

## 9.3.1.16 Transfer Control Descriptor (TCD)

Each  channel  requires  a  256-bit  transfer  control  descriptor  for  defining  the  desired  data  movement operation. The channel descriptors are stored in the local memory in sequential order: channel 0, channel 1,... channel 63 (MPC5554) or channel 0, channel 1,... channel 31 (MPC5553). The definitions of the TCD are presented as twenty-three variable-length fields. Table 9-17 is field list of the basic TCD structure.

Table 9-17. TCD n 32-bit Memory Structure

| eDMA Bit Offset         |   Lengt h | TCD n Field Name                                             | TCD n Abbreviation    |
|-------------------------|-----------|--------------------------------------------------------------|-----------------------|
| 0x1000 + (32 x n) + 0   |        32 | Source Address                                               | SADDR                 |
| 0x1000 + (32 x n) + 32  |         5 | Source address modulo                                        | SMOD                  |
| 0x1000 + (32 x n) + 37  |         3 | Source data transfer size                                    | SSIZE                 |
| 0x1000 + (32 x n) + 40  |         5 | Destination address modulo                                   | DMOD                  |
| 0x1000 + (32 x n) + 45  |         3 | Destination data transfer size                               | DSIZE                 |
| 0x1000 + (32 x n) + 48  |        16 | Signed Source Address Offset                                 | SOFF                  |
| 0x1000 + (32 x n) + 64  |        32 | Inner Minor Byte Count                                       | NBYTES                |
| 0x1000 + (32 x n) + 96  |        32 | Last Source Address Adjustment                               | SLAST                 |
| 0x1000 + (32 x n) + 128 |        32 | Destination Address                                          | DADDR                 |
| 0x1000 + (32 x n) + 160 |         1 | Channel-to-channel Linking on Minor Loop Complete            | CITER.E_LINK          |
| 0x1000 + (32 x n) + 161 |         6 | Current 'Major' Iteration Count or Link Channel Number       | CITER or CITER.LINKCH |
| 0x1000 + (32 x n) + 167 |         9 | Current Major Iteration Count                                | CITER                 |
| 0x1000 + (32 x n) + 176 |        16 | Destination Address Offset (Signed)                          | DOFF                  |
| 0x1000 + (32 x n) + 192 |        32 | Last Destination Address Adjustment / Scatter Gather Address | DLAST_SGA             |
| 0x1000 + (32 x n) + 224 |         1 | Channel-to-channel Linking on Minor Loop Complete            | BITER.E_LINK          |
| 0x1000 + (32 x n) + 225 |         6 | Starting Major Iteration Count or Link Channel Number        | BITER or BITER.LINKCH |
| 0x1000 + (32 x n) + 231 |         9 | Starting Major Iteration Count                               | BITER                 |
| 0x1000 + (32 x n) +240  |         2 | Bandwidth Control                                            | BWC                   |
| 0x1000 + (32 x n) + 242 |         6 | Link Channel Number                                          | MAJOR.LINKCH          |
| 0x1000 + (32 x n) + 248 |         1 | Channel Done                                                 | DONE                  |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## Table 9-17. TCD n 32-bit Memory Structure (continued)

Figure 9-21 and Table 9-18 define the fields of the TCDn structure.

| 0x1000 + (32 x n) + 249   |   1 | Channel Active                                                               | ACTIVE       |
|---------------------------|-----|------------------------------------------------------------------------------|--------------|
| 0x1000 + (32 x n) + 250   |   1 | Channel-to-channel Linking on Major Loop Complete                            | MAJOR.E_LINK |
| 0x1000 + (32 x n) + 251   |   1 | Enable Scatter/Gather Processing                                             | E_SG         |
| 0x1000 + (32 x n) + 252   |   1 | Disable Request                                                              | D_REQ        |
| 0x1000 + (32 x n) + 253   |   1 | Channel Interrupt Enable When Current Major Iteration Count is Half Complete | INT_HALF     |
| 0x1000 + (32 x n) + 254   |   1 | Channel Interrupt Enable When Current Major Iteration Count Complete         | INT_MAJ      |
| 0x1000 + (32 x n) + 255   |   1 | Channel Start                                                                | START        |

Word

Figure 9-21. TCD Structure

<!-- image -->

| Offset   | 0 6 7 8 9                  | 1 15 18 21 22                    | 2 3   | 4 5          | 10 11   | 12 13 14   | 16 17     | 19 20        | 23 24   | 26 27             | 30      | 31   |          |
|----------|----------------------------|----------------------------------|-------|--------------|---------|------------|-----------|--------------|---------|-------------------|---------|------|----------|
| 0x0      | SADDR                      |                                  |       |              |         |            |           |              |         |                   |         |      |          |
| 0x4      | SMOD SSIZE DMOD DSIZE SOFF |                                  |       |              |         |            |           |              |         |                   |         |      |          |
| 0x8      | NBYTES                     |                                  |       |              |         |            |           |              |         |                   |         |      |          |
| 0xC      | SLAST                      |                                  |       |              |         |            |           |              |         |                   |         |      |          |
| 0x10     | DADDR                      |                                  |       |              |         |            |           |              |         |                   |         |      |          |
| 0x14     | LINK                       | CITER or CITER.LINKCH CITER DOFF |       |              |         |            |           |              |         |                   |         |      |          |
| 0x18     | CITER.E_                   |                                  |       |              |         |            | DLAST_SGA |              |         |                   |         |      |          |
| 0x1C     |                            |                                  |       |              |         |            |           |              |         |                   |         |      |          |
|          | BITER.E_                   |                                  |       |              |         |            |           |              |         |                   |         |      |          |
|          | LINK                       | BITER or                         |       | BITER.LINKCH | BITER   |            | BWC       | MAJOR LINKCH | ACTIVE  |                   | INT_MAJ |      |          |
|          |                            |                                  |       |              |         |            |           |              | DONE    | MAJOR.E_LINK E_SG |         |      |          |
|          |                            |                                  |       |              |         |            |           |              |         |                   |         |      | START    |
|          |                            |                                  |       |              |         |            |           |              |         | D_REQ             |         |      | INT_HALF |

## NOTE

The  TCD  structures  for  the  eDMA  channels  shown  in  Figure 9-21  are implemented in internal SRAM. These structures are not initialized at reset. Therefore, all channel TCD  parameters  must  be  initialized by the application code before activating that channel.

## Table 9-18. TCD n Field Descriptions

| Bits / Word Offset [n:n]   | Name          | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|----------------------------|---------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-31 / 0x0 [0:31]          | SADDR [0:31]  | Source address. Memory address pointing to the source data. Word 0x0, bits 0-31.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 32-36 / 0x4 [0:4]          | SMOD [0:4]    | Source address modulo. 0 Source address modulo feature is disabled. non-0 This value defines a specific address range which is specified to be either the value after SADDR + SOFF calculation is performed or the original register value. The setting of this field provides the ability to easily implement a circular data queue. For data queues requiring power-of-2 'size' bytes, the queue should start at a 0-modulo-size address and the SMOD field should be set to the appropriate value for the queue, freezing the desired number of upper address bits. The value programmed into this field specifies the number of lower address bits that are allowed to change. For this circular queue application, the SOFF is typically set to the transfer size to implement post-increment addressing with the SMOD function constraining the addresses to a 0-modulo-size range. |
| 37-39 / 0x4 [5:7]          | SSIZE [0:2]   | Source data transfer size. 000 8-bit 001 16-bit 010 32-bit 011 64-bit 100 Reserved 101 32-byte burst (64-bit x 4) 110 Reserved 111 Reserved The attempted specification of a 'reserved' encoding will cause a configuration                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| 40-44 / 0x4 [8:12]         | DMOD [0:4]    | Destination address modulo. See the SMOD[0:5] definition.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| 45-47 / 0x4 [13:15]        | DSIZE [0:2]   | Destination data transfer size. See the SSIZE[0:2] definition.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| 48-63 / 0x4 [16:31]        | SOFF [0:15]   | Source address signed offset. Sign-extended offset applied to the current source address to form the next-state value as each source read is completed.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| 64-95 / 0x8 [0:31]         | NBYTES [0:31] | Inner 'minor' byte transfer count. Number of bytes to be transferred in each service request of the channel. As a channel is activated, the contents of the appropriate TCD is loaded into the eDMA engine, and the appropriate reads and writes performed until the complete byte transfer count has been transferred. This is an indivisible operation and cannot be stalled or halted. Once the minor count is exhausted, the current values of the SADDR and DADDR are written back into the local memory, the major iteration count is decremented and restored to the local memory. If the major iteration count is completed, additional processing is performed. Note: The NBYTES value of 0x0000_0000 is interpreted as 0x1_0000_0000, thus specifying a 4 GByte transfer.                                                                                                       |
| 96-127 / 0xC [0:31]        | SLAST [0:31]  | Last source address adjustment. Adjustment value added to the source address at the completion of the outer major iteration count. This value can be applied to 'restore' the source address to the initial value, or adjust the address to reference the next data structure.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## Table 9-18. TCD n Field Descriptions (continued)

| Bits / Word Offset [n:n]   | Name                              | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
|----------------------------|-----------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 128-159 / 0x10 [0:31]      | DADDR [0:31]                      | Destination address. Memory address pointing to the destination data.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| 160 / 0x14 [0]             | CITER.E_LINK                      | Enable channel-to-channel linking on minor loop completion. As the channel completes the inner minor loop, this flag enables the linking to another channel, defined by CITER.LINKCH[0:5]. The link target channel initiates a channel service request via an internal mechanism that sets the TCD.START bit of the specified channel. If channel linking is disabled, the CITER value is extended to 15 bits in place of a link channel number. If the major loop is exhausted, this link mechanism is suppressed in favor of the MAJOR.E_LINK channel linking. 0 The channel-to-channel linking is disabled. 1 The channel-to-channel linking is enabled. Note: This bit must be equal to the BITER.E_LINK bit otherwise a configuration error will be reported.                                                                                     |
| 161-166 / 0x14 [1:6]       | CITER [0:5] or CITER.LINKCH [0:5] | Current 'major' iteration count or link channel number. If channel-to-channel linking is disabled (TCD.CITER.E_LINK = 0), then GLYPH<127> No channel-to-channel linking (or chaining) is performed after the inner minor loop is exhausted. TCD bits [161:175] are used to form a 15-bit CITER field. otherwise GLYPH<127> After the minor loop is exhausted, the eDMA engine initiates a channel service request at the channel defined by CITER.LINKCH[0:5] by setting that channel's TCD.START bit.                                                                                                                                                                                                                                                                                                                                                 |
| 167-175 / 0x14 [7:15]      | CITER [6:14]                      | Current 'major' iteration count. This 9 or 15-bit count represents the current major loop count for the channel. It is decremented each time the minor loop is completed and updated in the transfer control descriptor memory. Once the major iteration count is exhausted, the channel performs a number of operations (for example, final source and destination address calculations), optionally generating an interrupt to signal channel completion before reloading the CITER field from the beginning iteration count (BITER) field. Note: When the CITER field is initially loaded by software, it must be set to the same value as that contained in the BITER field. Note: If the channel is configured to execute a single service request, the initial values of BITER and CITER should be 0x0001.                                       |
| 176-191 / 0x14 [16:31]     | DOFF [0:15]                       | Destination address signed offset. Sign-extended offset applied to the current destination address to form the next-state value as each destination write is completed.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| 192-223 / 0x18 [0:31]      | DLAST_SGA [0:31]                  | Last destination address adjustment or the memory address for the next transfer control descriptor to be loaded into this channel (scatter/gather). If scatter/gather processing for the channel is disabled (TCD.E_SG = 0) then GLYPH<127> Adjustment value added to the destination address at the completion of the outer major iteration count. This value can be applied to 'restore' the destination address to the initial value, or adjust the address to reference the next data structure. Otherwise GLYPH<127> This address points to the beginning of a 0-modulo-32 byte region containing the next transfer control descriptor to be loaded into this channel. This channel reload is performed as the major iteration count completes. The scatter/gather address must be 0-modulo-32 byte, otherwise a configuration error is reported. |

## Table 9-18. TCD n Field Descriptions (continued)

| Bits / Word Offset [n:n]   | Name                              | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|----------------------------|-----------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 224 / 0x1C [0]             | BITER.E_LINK                      | Enables channel-to-channel linking on minor loop complete. As the channel completes the inner minor loop, this flag enables the linking to another channel, defined by BITER.LINKCH[0:5]. The link target channel initiates a channel service request via an internal mechanism that sets the TCD.START bit of the specified channel. If channel linking is disabled, the BITER value is extended to 15 bits in place of a link channel number. If the major loop is exhausted, this link mechanism is suppressed in favor of the MAJOR.E_LINK channel linking. 0 The channel-to-channel linking is disabled. 1 The channel-to-channel linking is enabled. Note: When the TCD is first loaded by software, this field must be set equal to the corresponding CITER field, otherwise a configuration error will be reported. As the major iteration count is exhausted, the contents of this field is reloaded into the CITER field. |
| 225-230 / 0x1C [1:6]       | BITER [0:5] or BITER.LINKCH[ 0:5] | Starting 'major' iteration count or link channel number. If channel-to-channel linking is disabled (TCD.BITER.E_LINK = 0), then GLYPH<127> No channel-to-channel linking (or chaining) is performed after the inner minor loop is exhausted. TCD bits [225:239] are used to form a 15-bit BITER field. Otherwise GLYPH<127> After the minor loop is exhausted, the eDMA engine initiates a channel service request at the channel, defined by BITER.LINKCH[0:5], by setting that channel's TCD.START bit. Note: When the TCD is first loaded by software, this field must be set equal to the corresponding CITER field, otherwise a configuration error will be reported. As the major iteration count is exhausted, the contents of this field is reloaded into the CITER field.                                                                                                                                                  |
| 231-239 / 0x1C [7:15]      | BITER [6:14]                      | Starting major iteration count. As the transfer control descriptor is first loaded by software, this field must be equal to the value in the CITER field. As the major iteration count is exhausted, the contents of this field is reloaded into the CITER field. Note: If the channel is configured to execute a single service request, the initial values of BITER and CITER should be 0x0001.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| 240-241 / 0x1C [16:17]     | BWC [0:1]                         | Bandwidth control. This two-bit field provides a mechanism to effectively throttle the amount of bus bandwidth consumed by the eDMA. In general, as the eDMA processes the inner minor loop, it continuously generates read/write sequences until the minor count is exhausted. This field forces the eDMA to stall after the completion of each read/write access to control the bus request bandwidth seen by the system bus crossbar switch (XBAR). 00 No eDMA engine stalls 01 Reserved 10 eDMA engine stalls for 4 cycles after each r/w 11 eDMA engine stalls for 8 cycles after each r/w                                                                                                                                                                                                                                                                                                                                     |
| 242-247 / 0x1C [18:23]     | MAJOR.LINKC H [0:5]               | Link channel number. If channel-to-channel linking on major loop complete is disabled (TCD.MAJOR.E_LINK = 0) then GLYPH<127> No channel-to-channel linking (or chaining) is performed after the outer major loop counter is exhausted. Otherwise GLYPH<127> After the major loop counter is exhausted, the eDMA engine initiates a channel service request at the channel defined by MAJOR.LINKCH[0:5] by setting that channel's TCD.START bit.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 9-18. TCD n Field Descriptions (continued)

| Bits / Word Offset [n:n]   | Name         | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|----------------------------|--------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 248 / 0x1C [24]            | DONE         | Channel done. This flag indicates the eDMA has completed the outer major loop. It is set by the eDMA engine as the CITER count reaches zero; it is cleared by software or hardware when the channel is activated (when the channel has begun to be processed by the eDMA engine, not when the first data tranfer occurs). Note: This bit must be cleared in order to write the MAJOR.E_LINK or E_SG bits.                                                                                                                                                                                                                                                                                                                                                                                    |
| 249 / 0x1C [25]            | ACTIVE       | Channel active. This flag signals the channel is currently in execution. It is set when channel service begins, and is cleared by the eDMAengine as the inner minor loop completes or if any error condition is detected.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| 250 / 0x1C [26]            | MAJOR.E_LINK | Enable channel-to-channel linking on major loop completion. As the channel completes the outer major loop, this flag enables the linking to another channel, defined by MAJOR.LINKCH[0:5]. The link target channel initiates a channel service request via an internal mechanism that sets the TCD.START bit of the specified channel. NOTE: To support the dynamic linking coherency model, this field is forced to zero when written to while the TCD.DONE bit is set. 0 The channel-to-channel linking is disabled. 1 The channel-to-channel linking is enabled.                                                                                                                                                                                                                          |
| 251 / 0x1C [27]            | E_SG         | Enable scatter/gather processing. As the channel completes the outer major loop, this flag enables scatter/gather processing in the current channel. If enabled, the eDMA engine uses DLAST_SGA as a memory pointer to a 0-modulo-32 address containing a 32-byte data structure which is loaded as the transfer control descriptor into the local memory. NOTE: To support the dynamic scatter/gather coherency model, this field is forced to zero when written to while the TCD.DONE bit is set. 0 The current channel's TCD is 'normal' format. 1 The current channel's TCD specifies a scatter gather format. The DLAST_SGA field provides a memory pointer to the next TCD to be loaded into this channel after the outer major loop completes its execution.                          |
| 252 / 0x1C [28]            | D_REQ        | Disable hardware request. If this flag is set, the eDMA hardware automatically clears the corresponding EDMA_ERQH or EDMA_ERQL bit when the current major iteration count reaches zero. 0 The channel's EDMA_ERQH or EDMA_ERQL bit is not affected. 1 The channel's EDMA_ERQH or EDMA_ERQL bit is cleared when the outer major loop is complete.                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 253 / 0x1C [29]            | INT_HALF     | Enable an interrupt when major counter is half complete. If this flag is set, the channel generates an interrupt request by setting the appropriate bit in the EDMA_ERQHor EDMA_ERQLwhen the current major iteration count reaches the halfway point. Specifically, the comparison performed by the eDMA engine is (CITER == (BITER >> 1)). This halfway point interrupt request is provided to support double-buffered (aka ping-pong) schemes, or other types of data movement where the processor needs an early indication of the transfer's progress. CITER = BITER = 1 with INT_HALF enabled will generate an interrupt as it satisfies the equation (CITER == (BITER >> 1)) after a single activation. 0 The half-point interrupt is disabled. 1 The half-point interrupt is enabled. |

Table 9-18. TCD n Field Descriptions (continued)

| Bits / Word Offset [n:n]   | Name    | Description                                                                                                                                                                                                                                                                                                                              |
|----------------------------|---------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 254 / 0x1C [30]            | INT_MAJ | Enable an interrupt when major iteration count completes. If this flag is set, the channel generates an interrupt request by setting the appropriate bit in the EDMA_ERQH or EDMA_ERQL when the current major iteration count reaches zero. 0 The end-of-major loop interrupt is disabled. 1 The end-of-major loop interrupt is enabled. |
| 255 / 0x1C [31]            | START   | Channel start. If this flag is set, the channel is requesting service. The eDMA hardware automatically clears this flag after the channel begins execution. 0 The channel is not explicitly started. 1 The channel is explicitly started via a software initiated service request.                                                       |

## 9.4 Functional Description

This section provides an overview of the microarchitecture and functional operation of the eDMA module.

## 9.4.1 eDMA Microarchitecture

The eDMA module is partitioned into two major modules: the eDMA engine and the transfer control descriptor  local  memory.  Additionally,  the  eDMA  engine  is  further  partitioned  into  four  submodules, which are detailed below.

- · eDMA engine
- - Address path: This module implements registered versions of two channel transfer control descriptors: channel 'x' and channel 'y,' and is responsible for all the master bus address calculations. All the implemented channels provide the exact same functionality. This hardware structure allows the data transfers associated with one channel to be preempted after the completion of a read/write sequence if a higher priority channel service request is asserted while the first channel is active. Once a channel is activated, it runs until the minor loop is completed unless preempted by a higher priority channel. This capability provides a mechanism (optionally enabled by EDMA\_CPR n [ECP]) where a large data move operation can be preempted to minimize the time another channel is blocked from execution.
- When any other channel is activated, the contents of its transfer control descriptor is read from the local memory and loaded into the registers of the other address path channel{x,y}. Once the inner minor loop completes execution, the address path hardware writes the new values for the TCD .{SADDR, DADDR, CITER} back into the local memory. If the major iteration n count is exhausted, additional processing is performed, including the final address pointer updates, reloading the TCDn.CITER field, and a possible fetch of the next TCDn from memory as part of a scatter/gather operation.
- - Data path: This module implements the actual bus master read/write datapath. It includes 32 bytes of register storage (matching the maximum transfer size) and the necessary mux logic to support any required data alignment. The system read data bus is the primary input, and the system write data bus is the primary output.
- The address and data path modules directly support the 2-stage pipelined system bus. The address path module represents the 1st stage of the bus pipeline (the address phase), while the data path module implements the 2nd stage of the pipeline (the data phase).

## Enhanced Direct Memory Access (eDMA)

- - Program model/channel arbitration: This module implements the first section of eDMA's programming model as well as the channel arbitration logic. The programming model registers are connected to the slave bus (not shown). The eDMA peripheral request inputs and eDMA interrupt request outputs are also connected to this module (via the Control logic).
- - Control: This module provides all the control functions for the eDMA engine. For data transfers where the source and destination sizes are equal, the eDMA engine performs a series of source read, destination write operations until the number of bytes specified in the inner 'minor loop' byte count has been moved.

A minor loop interation is defined as the number of bytes to transfer ( n bytes) divided  by the transfer size. Transfer size is defined as the following'

if (ssize &lt; dsize)

transfer size = destination transfer size (# of bytes)

else transfer size = source transfer size (# of bytes)

Minor loop TCD variables are soff, smod, doff, dmod, nbytes, saddr, daddr, bwc, active,  and start . Major loop TCD variables are dlast, slast, citer, biter, done, d\_req, int\_maj,  major\_lnkch, and int\_half.

For descriptors where the sizes are not equal, multiple access of the smaller size data are required for each reference of the larger size. As an example, if the source size references 16-bit data and the destination is 32-bit data, two reads are performed, then one 32-bit write.

## · TCD local memory

- - Memory controller: This logic implements the required dual-ported controller, handling accesses from both the eDMA engine as well as references from the slave bus. As noted earlier, in the event of simultaneous accesses, the eDMA engine is given priority and the slave transaction is stalled. The hooks to a BIST controller for the local TCD memory are included in this module.
- - Memory array: The TCD is implemented using a single-ported, synchronous compiled RAM memory array.

## 9.4.2 eDMA Basic Data Flow

The basic flow of a data transfer can be partitioned into three segments. As shown in Figure 9-22, the first segment involves the channel service request. In the diagram, this example uses the assertion of the eDMA peripheral request signal to request service for channel n . Channel service request via software and the TCDn.START bit follows the same basic flow as an eDMA peripheral request. The eDMA peripheral request input signal is registered internally and then routed to through the eDMA engine, first through the control module, then into the program model/channel arbitration module. In the next cycle, the channel arbitration is performed, either using the fixed-priority or round-robin algorithm. After the arbitration is complete, the activated channel number is sent through the address path and converted into the required address to access the TCD local memory. Next, the TCD memory is accessed and the required descriptor read from the local memory and loaded into the eDMA engine address path channel{x,y} registers. The TCD memory is organized 64-bits in width to minimize the time needed to fetch the activated channel's descriptor and load it into the eDMA engine address path channel{x,y} registers.

<!-- image -->

eDMA Done Handshake

Figure 9-22. eDMA Operation, Part 1

In the second part of the basic data flow as shown in Figure 9-23, the modules associated with the data transfer (address path, data path and control) sequence through the required source reads and destination writes  to  perform  the  actual  data  movement.  The  source  reads  are  initiated  and  the  fetched  data  is temporarily stored in the data path module until it is gated onto the system bus during the destination write.

This  source  read/destination  write  processing  continues  until  the  inner  minor  byte  count  has  been transferred. The eDMA Done Handshake signal is asserted at the end of the minor byte count transfer.

Figure 9-23. eDMA Operation, Part 2

<!-- image -->

Once the inner minor byte count has been moved, the final phase of the basic data flow is performed. In this segment, the address path logic performs the required updates to certain fields in the channel's TCD: for example., SADDR, DADDR, CITER. If the outer major iteration count is exhausted, then there are additional operations which are performed. These include the final address adjustments and reloading of the BITER field into the CITER. Additionally, assertion of an optional interrupt request occurs at this time, as does a possible fetch of a new TCD from memory using the scatter/gather address pointer included in

the descriptor. The updates to the TCD memory and the assertion of an interrupt request are shown in Figure 9-24.

Figure 9-24. eDMA Operation, Part 3

<!-- image -->

## 9.4.3 eDMA Performance

This section addresses the performance of the eDMA module, focusing on two separate metrics. In the traditional data movement context, performance is best expressed as the peak data transfer rates achieved using the eDMA. In most implementations, this transfer rate is limited by the speed of the source and destination  address  spaces.  In  a  second  context  where  device-paced  movement  of  single  data  values to/from peripherals is dominant, a measure of the requests that can be serviced in a fixed time is a more useful  metric.  In  this  environment,  the  speed  of  the  source  and  destination  address  spaces  remains important, but the microarchitecture of the eDMA also factors significantly into the resulting metric.

The peak transfer rates for several different source and destination transfers are shown in Table 9-19. The following assumptions apply to Table 9-19 and Table 9-20:

- · Internal SRAM can be accessed with zero wait-states when viewed from the system bus data phase.
- · All slave reads require two wait-states, and slave writes three wait-states, again viewed from the system bus data phase.
- · All slave accesses are 32-bits in size.

Table 9-19 presents a peak transfer rate comparison, measured in Mbytes per second.

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 9-19. eDMA Peak Transfer Rates (Mbytes/Sec)

| System Speed, Width   |   Internal SRAM-to- Internal SRAM |   32-Bit Slave-to- Internal SRAM |   Internal SRAM-to- 32-Bit Slave |
|-----------------------|-----------------------------------|----------------------------------|----------------------------------|
| 66.7 MHz, 32 bit      |                             133.3 |                             66.7 |                             53.3 |
| 66.7 MHz, 64 bit      |                             266.7 |                             66.6 |                             53.3 |
| 83.3 MHz, 32 bit      |                             166.7 |                             83.3 |                             66.7 |
| 83.3 MHz, 64 bit      |                             333.3 |                             83.3 |                             66.7 |
| 100.0 MHz, 32 bit     |                             200   |                            100   |                             80   |
| 100.0 MHz, 64 bit     |                             400   |                            100   |                             80   |
| 133.3 MHz, 32 bit     |                             266.7 |                            133.3 |                            106.7 |
| 133.3 MHz, 64 bit     |                             533.3 |                            133.3 |                            106.7 |
| 150.0 MHz, 32 bit     |                             300   |                            150   |                            120   |
| 150.0 MHz, 64 bit     |                             600   |                            150   |                            120   |

Where the internal-SRAM-to-internal-SRAM transfers occur at the core's datapath width; that is, either 32- or 64-bits per access. For all transfers involving the slave bus, 32-bit transfer sizes are used. In all cases, the transfer rate includes the time to read the source plus the time to write the destination.

The second performance metric is a measure of the number of DMA requests that can be serviced in a given amount of time. For this metric, it is assumed the peripheral request causes the channel to move a single slave-mapped operand to/from internal SRAM. The same timing assumptions used in the previous example apply to this calculation. In particular, this metric also reflects the time required to activate the channel. The eDMA design supports the following hardware service request sequence:

- · Cycle 1: eDMA peripheral request is asserted.
- · Cycle 2: The eDMA peripheral request is registered locally in the eDMA module and qualified. (TCD.START bit initiated requests start at this point with the registering of the slave write to TCD bit 255).
- · Cycle 3: Channel arbitration begins.
- · Cycle 4: Channel arbitration completes. The transfer control descriptor local memory read is initiated.
- · Cycle 5 - 6: The first two parts of the activated channel's TCD is read from the local memory. The memory width to the eDMA engine is 64 bits, so the entire descriptor can be accessed in four cycles.
- · Cycle 7: The first system bus read cycle is initiated, as the third part of the channel's TCD is read from the local memory. Depending on the state of the  crossbar switch, arbitration at the system bus may insert an additional cycle of delay here.
- : The last part of the TCD is read in. This cycle represents the 1st data phase for the
- · Cycle 8 n read, and the address phase for the destination write.
- The exact timing from this point is a function of the response times for the channel's read and write accesses. In this case of an slave read and internal SRAM write, the combined data phase time is 4 cycles. For an SRAM read and slave write, it is 5 cycles.
- · Cycle n + 1: This cycle represents the data phase of the last destination write.
- · Cycle n + 2: The eDMA engine completes the execution of the inner minor loop and prepares to write back the required TCDn fields into the local memory. The control/status fields at word offset

0x1C in TCDn are read. If the major loop is complete, the MAJOR.E\_LINK and E\_SG bits are checked and processed if enabled.

- · Cycle n + 3: The appropriate fields in the first part of the TCDn are written back into the local memory.
- · Cycle n + 4: The fields in the second part of the TCDn are written back into the local memory. This cycle coincides with the next channel arbitration cycle start.
- · Cycle n + 5: The next channel to be activated performs the read of the first part of its TCD from the local memory. This is equivalent to Cycle 4 for the first channel's service request.

Assuming zero wait states on the system bus, DMA requests can be processed every 9 cycles. Assuming an average of the access times associated with slave-to-SRAM (4 cycles) and SRAM-to-slave (5 cycles), DMA requests can be processed every 11.5 cycles (4 + (4+5)/2 + 3). This is the time from Cycle 4 to Cycle ' n + 5.' The resulting peak request rate, as a function of the system frequency, is shown in Table 9-20. This metric represents millions of requests per second.

## Table 9-20. eDMA Peak Request Rate (MReq/Sec)

|   System Frequency (MHz) |   Request Rate (Zero Wait States) |   Request Rate (with Wait States) |
|--------------------------|-----------------------------------|-----------------------------------|
|                     66.6 |                               7.4 |                               5.8 |
|                     83.3 |                               9.2 |                               7.2 |
|                    100   |                              11.1 |                               8.7 |
|                    133.3 |                              14.8 |                              11.6 |
|                    150   |                              16.6 |                              13   |

A general formula to compute the peak request rate (with overlapping requests) is:

PEAKreq = freq / [ entry + (1 + read\_ws) + (1 + write\_ws) + exit ]

where:

PEAKreq - peak request rate freq - system frequency entry - channel startup (4 cycles) read\_ws - wait states seen during the system bus read data phase write\_ws - wait states seen during the system bus write data phase exit - channel shutdown (3 cycles)

For example: consider a system with the following characteristics:

- · Internal SRAM can be accessed with one wait-state when viewed from the system bus data phase.
- · All slave reads require two wait-states, and slave writes three wait-states, again viewed from the system bus data phase.
- · System operates at 150 MHz.

For an SRAM to slave transfer,

PEAKreq = 150 MHz / [ 4 + (1 + 1) + (1 + 3) + 3 ] cycles = 11.5 Mreq/sec

For an slave to SRAM transfer,

PEAKreq = 150 MHz / [ 4 + (1 + 2) + (1 + 1) + 3 ] cycles = 12.5 Mreq/sec

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## Enhanced Direct Memory Access (eDMA)

Assuming an even distribution of the two transfer types, the average peak request rate would be:

PEAKreq = (11.5 Mreq/sec + 12.5 Mreq/sec) / 2 = 12.0 Mreq/sec

The minimum number of cycles to perform a single read/write, zero wait states on the system bus, from a cold start (where no channel is executing, eDMA is idle) are the following:

- · 11 cycles for a software (TCD.START bit) request
- · 12 cycles for a hardware (eDMA peripheral request signal) request

Two cycles account for the arbitration pipeline and one extra cycle on the hardware request resulting from the internal registering of the eDMA peripheral request signals. For the peak request rate calculations above, the arbitration and request registering is absorbed in or overlap the previous executing channel.

## NOTE

When channel  linking  or  scatter/gather  is  enabled,  a  two-cycle  delay  is imposed  on  the  next  channel  selection  and  startup.  This  allows  the  link channel or the scatter/gather channel to be eligible and considered in the arbitration pool for next channel selection.

## 9.5 Initialization / Application Information

## 9.5.1 eDMA Initialization

A typical initialization of the eDMA would have the following sequence:

- 1. Write the EDMA\_CR if a configuration other than the default is desired.
- 2. Write the channel priority levels into the EDMA\_CPR n registers if a configuration other than the default is desired.
- 3. Enable error interrupts in the EDMA\_EEIRL and/or EDMA\_EEIRH registers if so desired.
- 4. Write the 32-byte TCD for each channel that may request service.
- 5. Enable any hardware service requests via the EDMA\_ERQRH and/or EDMA\_ERQRL registers.
- 6. Request channel service by either software (setting the TCD.START bit) or by hardware (slave device asserting its eDMA peripheral request signal).

Once any channel requests service, a channel is selected for execution based on the arbitration and priority levels written into the programmer's model. The eDMA engine will read the entire TCD, including the primary transfer control parameter shown in Table 9-21,  for the selected channel into its internal address path  module.  As  the  TCD  is  being  read,  the  first  transfer  is  initiated  on  the  system  bus  unless  a configuration error is detected. Transfers from the source (as defined by the source address, TCD.SADDR) to  the  destination  (as  defined  by  the  destination  address,  TCD.DADDR)  continue  until  the  specified number  of  bytes  (TCD.NBYTES)  have  been  transferred.  When  the  transfer  is  complete,  the  eDMA engine's local TCD.SADDR, TCD.DADDR, and TCD.CITER are written back to the main TCD memory and any minor loop channel linking is performed, if enabled. If the major loop is exhausted, further post processing is executed: for example, interrupts, major loop channel linking, and scatter/gather operations, if enabled.

Table 9-21. TCD Primary Control and Status Fields

| TCD Field Name   | Description                                                                                                             |
|------------------|-------------------------------------------------------------------------------------------------------------------------|
| START            | Control bit to explicitly start channel when using a software initiated DMA service (Automatically cleared by hardware) |
| ACTIVE           | Status bit indicating the channel is currently in execution                                                             |
| DONE             | Status bit indicating major loop completion (Cleared by software when using a software initiated DMA service)           |
| D_REQ            | Control bit to disable DMA request at end of major loop completion when using a hardware-initiated DMA service          |
| BWC              | Control bits for 'throttling' bandwidth control of a channel                                                            |
| E_SG             | Control bit to enable scatter-gather feature                                                                            |
| INT_HALF         | Control bit to enable interrupt when major loop is half complete                                                        |
| INT_MAJ          | Control bit to enable interrupt when major loop completes                                                               |

Figure 9-25  shows  how  each  DMA  request  initiates  one  minor  loop  transfer  (iteration)  without  CPU intervention.  DMA  arbitration  can  occur  after  each  minor  loop,  and  one  level  of  minor  loop  DMA preemption is allowed. The number of minor loops in a major loop is specified by the beginning iteration count (biter).

Figure 9-25. Example of Multiple Loop Iterations

| Example Memory Array   | Example Memory Array   |   Current Major Loop Iteration Count (CITER) |    |
|------------------------|------------------------|----------------------------------------------|----|
| DMA Request            | Minor Loop             |                                            3 |    |
| DMA Request            | Minor Loop             |                                            2 |    |
| DMA Request            | Minor Loop             |                                            1 |    |

Figure 9-26 lists the memory array terms and how the TCD settings interrelate.

Figure 9-26. Memory Array Terms

| xADDR: (Starting Address)                                                                      | xSIZE: (Size of one data transfer) • • •   | Minor Loop (NBYTES in Minor Loop, often the same value as xSIZE)   | Offset (xOFF): Number of bytes added to current address after each transfer (Often the same value as xSIZE)                                     |
|------------------------------------------------------------------------------------------------|--------------------------------------------|--------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| • • •                                                                                          | • • •                                      | Minor Loop                                                         | Each DMA Source (S) and Destination (D) has its own: • Address (xADDR) • Size (xSIZE) • Offset (xOFF) • Modulo (xMOD) • Last Address Adjustment |
| xLAST: Number of bytes added to current address after Major Loop (Typically used to loop back) | • • •                                      | Last Minor Loop                                                    | Peripheral queues typically have size and offset equal to NBYTES (xLAST) where x = S or D                                                       |

## 9.5.2 DMA Programming Errors

The eDMA performs various tests on the transfer control descriptor to verify consistency in the descriptor data. Most programming errors are reported on a per channel basis with the exception of two errors: group priority error and channel priority error, or EDMA\_ESR[GPE] and EDMA\_ESR[CPE], respectively.

For all error types other than group or channel priority errors, the channel number causing the error is recorded in the EDMA\_ESR. If the error source is not removed before the next activation of the problem channel, the error will be detected and recorded again.

Channel priority errors are identified within a group once that group has been selected as the active group. For the example below, all of the channel priorities in group 1 are unique, but some of the channel priorities in group 0 are the same:

- 1. The eDMA is configured for fixed group and fixed channel arbitration modes.
- 2. Group 1 is the highest priority and all channels are unique in that group.
- 3. Group 0 is the next highest priority and has two channels with the same priority level.
- 4. If group 1 has any service requests, those requests will be executed.
- 5. Once all of group 1 requests have completed, group 0 will be the next active group.
- 6. If Group 0 has a service request, then an undefined channel in group 0 will be selected and a channel priority error will occur.
- 7. This will repeat until the all of group 0 requests have been removed or a higher priority group 1 request comes in.

In  this  sequence,  for  item  2,  the  eDMA  acknowledge lines  will  assert  only  if  the  selected  channel  is requesting service via the eDMA peripheral request signal. If interrupts are enabled for all channels, the user will receive an error interrupt, but the channel number for the EDMA\_ER and the error interrupt request line are undetermined because they reflect the 'undefined' channel. A group priority error is global and any request in any group will cause a group priority error.

If priority levels are not unique, the highest (channel/group) priority that has an active request will be selected, but the lowest numbered (channel/group) with that priority will be selected by arbitration and executed by the eDMA engine. The hardware service request handshake signals, error interrupts and error reporting will be associated with the selected channel.

## 9.5.3 DMA Request Assignments

The assignments between the DMA requests from the modules to the channels of the eDMA are shown in Table 9-22. The source column is written in C language syntax. The syntax is module\_instance.register[bit].

Note that the MPC5554 has 64 channels but the MPC5553 has 32 channels, and in Table 9-22 channels 0-31 function for both the MPC5553/MPC5554, but only channels 32-63 function for the MPC5554.

Table 9-22. DMA Request Summary for eDMA

| DMA Request       |   Channel | Source                                            | Description                                                                                                                 |
|-------------------|-----------|---------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| eQADC_FISR0_CFFF0 |         0 | EQADC.FISR0[CFFF0]                                | eQADC Command FIFO 0 Fill Flag                                                                                              |
| eQADC_FISR0_RFDF0 |         1 | EQADC.FISR0[RFDF0]                                | eQADC Receive FIFO 0 Drain Flag                                                                                             |
| eQADC_FISR1_CFFF1 |         2 | EQADC.FISR1[CFFF1]                                | eQADC Command FIFO 1 Fill Flag                                                                                              |
| eQADC_FISR1_RFDF1 |         3 | EQADC.FISR1[RFDF1]                                | eQADC Receive FIFO 1 Drain Flag                                                                                             |
| eQADC_FISR2_CFFF2 |         4 | EQADC.FISR2[CFFF2]                                | eQADC Command FIFO 2 Fill Flag                                                                                              |
| eQADC_FISR2_RFDF2 |         5 | EQADC.FISR2[RFDF2]                                | eQADC Receive FIFO 2 Drain Flag                                                                                             |
| eQADC_FISR3_CFFF3 |         6 | EQADC.FISR3[CFFF3]                                | eQADC Command FIFO 3 Fill Flag                                                                                              |
| eQADC_FISR3_RFDF3 |         7 | EQADC.FISR3[RFDF3]                                | eQADC Receive FIFO 3 Drain Flag                                                                                             |
| eQADC_FISR4_CFFF4 |         8 | EQADC.FISR4[CFFF4]                                | eQADC Command FIFO 4 Fill Flag                                                                                              |
| eQADC_FISR4_RFDF4 |         9 | EQADC.FISR4[RFDF4]                                | eQADC Receive FIFO 4 Drain Flag                                                                                             |
| eQADC_FISR5_CFFF5 |        10 | EQADC.FISR5[CFFF5]                                | eQADC Command FIFO 5 Fill Flag                                                                                              |
| eQADC_FISR5_RFDF5 |        11 | EQADC.FISR5[RFDF5]                                | eQADC Receive FIFO 5 Drain Flag                                                                                             |
| DSPIB_SR_TFFF     |        12 | DSPIB.SR[TFFF]                                    | DSPIB Transmit FIFO Fill Flag                                                                                               |
| DSPIB_SR_RFDF     |        13 | DSPIB.SR[RFDF]                                    | DSPIB Receive FIFO Drain Flag                                                                                               |
| DSPIC_SR_TFFF     |        14 | DSPIC.SR[TFFF]                                    | DSPIC Transmit FIFO Fill Flag                                                                                               |
| DSPIC_SR_RFDF     |        15 | DSPIC.SR[RFDF]                                    | DSPIC Receive FIFO Drain Flag                                                                                               |
| DSPID_SR_TFFF     |        16 | DSPID.SR[TFFF]                                    | DSPID Transmit FIFO Fill Flag                                                                                               |
| DSPID_SR_RFDF     |        17 | DSPID.SR[RFDF]                                    | DSPID Receive FIFO Drain Flag                                                                                               |
| eSCIA_COMBTX      |        18 | ESCIA.SR[TDRE] || ESCIA.SR[TC] || ESCIA.SR[TXRDY] | eSCIA combined DMA request of the Transmit Data Register Empty, Transmit Complete, and LIN Transmit Data Ready DMA requests |
| eSCIA_COMBRX      |        19 | ESCIA.SR[RDRF] || ESCIA.SR[RXRDY]                 | eSCIA combined DMA request of the Receive Data Register Full and LIN Receive Data Ready DMA requests                        |
| eMIOS_GFR_F0      |        20 | EMIOS.GFR[F0]                                     | eMIOS channel 0 Flag                                                                                                        |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## Table 9-22. DMA Request Summary for eDMA (continued)

| DMA Request                                          | Channel                                              | Source                                               | Description                                                                                                                 |
|------------------------------------------------------|------------------------------------------------------|------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| eMIOS_GFR_F1                                         | 21                                                   | EMIOS.GFR[F1]                                        | eMIOS channel 1 Flag                                                                                                        |
| eMIOS_GFR_F2                                         | 22                                                   | EMIOS.GFR[F2]                                        | eMIOS channel 2 Flag                                                                                                        |
| eMIOS_GFR_F3                                         | 23                                                   | EMIOS.GFR[F3]                                        | eMIOS channel 3 Flag                                                                                                        |
| eMIOS_GFR_F4                                         | 24                                                   | EMIOS.GFR[F4]                                        | eMIOS channel 4 Flag                                                                                                        |
| eMIOS_GFR_F8                                         | 25                                                   | EMIOS.GFR[F8]                                        | eMIOS channel 8 Flag                                                                                                        |
| eMIOS_GFR_F9                                         | 26                                                   | EMIOS.GFR[F9]                                        | eMIOS channel 9 Flag                                                                                                        |
| eTPU_CDTRSR_A_DTRS0                                  | 27                                                   | ETPU.CDTRSR_A[DTRS0]                                 | eTPUA Channel 0 Data Transfer Request Status                                                                                |
| eTPU_CDTRSR_A_DTRS1                                  | 28                                                   | ETPU.CDTRSR_A[DTRS1]                                 | eTPUA Channel 1 Data Transfer Request Status                                                                                |
| eTPU_CDTRSR_A_DTRS2                                  | 29                                                   | ETPU.CDTRSR_A[DTRS2]                                 | eTPUA Channel 2 Data Transfer Request Status                                                                                |
| eTPU_CDTRSR_A_DTRS14                                 | 30                                                   | ETPU.CDTRSR_A[DTRS14]                                | eTPUA Channel 14 Data Transfer Request Status                                                                               |
| eTPU_CDTRSR_A_DTRS15                                 | 31                                                   | ETPU.CDTRSR_A[DTRS15]                                | eTPUA Channel 15 Data Transfer Request Status                                                                               |
| The Below Requests Are Only Available in the MPC5554 | The Below Requests Are Only Available in the MPC5554 | The Below Requests Are Only Available in the MPC5554 | The Below Requests Are Only Available in the MPC5554                                                                        |
| DSPIA_SR_TFFF                                        | 32                                                   | DSPIAISR[TFFF]                                       | DSPIA Transmit FIFO Fill Flag                                                                                               |
| DSPIA_SR_RFDF                                        | 33                                                   | DSPIA.SR[RFDF]                                       | DSPIA Receive FIFO Drain Flag                                                                                               |
| eSCIB_COMBTX                                         | 34                                                   | ESCIB.SR[TDRE] || ESCIB.SR[TC] || ESCIB.SR[TXRDY]    | eSCIB combined DMA request of the Transmit Data Register Empty, Transmit Complete, and LIN Transmit Data Ready DMA requests |
| eSCIB_COMBRX                                         | 35                                                   | ESCIB.SR[RDRF] || ESCIB.SR[RXRDY]                    | eSCIB combined DMA request of the Receive Data Register Full and LIN Receive Data Ready DMA requests                        |
| eMIOS_GFR_F6                                         | 36                                                   | EMIOS.GFR[F6]                                        | eMIOS channel 6 Flag                                                                                                        |
| eMIOS_GFR_F7                                         | 37                                                   | EMIOS.GFR[F7]                                        | eMIOS channel 7 Flag                                                                                                        |
| eMIOS_GFR_F10                                        | 38                                                   | EMIOS.GFR[F10]                                       | eMIOS channel 10 Flag                                                                                                       |
| eMIOS_GFR_F11                                        | 39                                                   | EMIOS.GFR[F11]                                       | eMIOS channel 11 Flag                                                                                                       |
| eMIOS_GFR_F16                                        | 40                                                   | EMIOS.GFR[F16]                                       | eMIOS channel 16 Flag                                                                                                       |
| eMIOS_GFR_F17                                        | 41                                                   | EMIOS.GFR[F17]                                       | eMIOS channel 17 Flag                                                                                                       |
| eMIOS_GFR_F18                                        | 42                                                   | EMIOS.GFR[F18]                                       | eMIOS channel 18 Flag                                                                                                       |
| eMIOS_GFR_F19                                        | 43                                                   | EMIOS.GFR[F19]                                       | eMIOS channel 19 Flag                                                                                                       |
| eTPU_CDTRSR_A_DTRS12                                 | 44                                                   | ETPU.CDTRSR_A[DTRS12]                                | eTPUA Channel 12 Data Transfer Request Status                                                                               |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 9-22. DMA Request Summary for eDMA (continued)

| DMA Request          |   Channel | Source                | Description                                   |
|----------------------|-----------|-----------------------|-----------------------------------------------|
| eTPU_CDTRSR_A_DTRS13 |        45 | ETPU.CDTRSR_A[DTRS13] | eTPUA Channel 13 Data Transfer Request Status |
| eTPU_CDTRSR_A_DTRS28 |        46 | ETPU.CDTRSR_A[DTRS28] | eTPUA Channel 28 Data Transfer Request Status |
| eTPU_CDTRSR_A_DTRS29 |        47 | ETPU.CDTRSR_A[DTRS29] | eTPUA Channel 29 Data Transfer Request Status |
| SIU_EISR_EIF0        |        48 | SIU.SIU_EISR[EIF0]    | SIU External Interrupt Flag 0                 |
| SIU_EISR_EIF1        |        49 | SIU.SIU_EISR[EIF1]    | SIU External Interrupt Flag 1                 |
| SIU_EISR_EIF2        |        50 | SIU.SIU_EISR[EIF2]    | SIU External Interrupt Flag 2                 |
| SIU_EISR_EIF3        |        51 | SIU.SIU_EISR[EIF3]    | SIU External Interrupt Flag 3                 |
| eTPU_CDTRSR_B_DTRS0  |        52 | ETPU.CDTRSR_B[DTRS0]  | eTPUB Channel 0 Data Transfer Request Status  |
| eTPU_CDTRSR_B_DTRS1  |        53 | ETPU.CDTRSR_B[DTRS1]  | eTPUB Channel 1 Data Transfer Request Status  |
| eTPU_CDTRSR_B_DTRS2  |        54 | ETPU.CDTRSR_B[DTRS2]  | eTPUB Channel 2 Data Transfer Request Status  |
| eTPU_CDTRSR_B_DTRS3  |        55 | ETPU.CDTRSR_B[DTRS3]  | eTPUB Channel 3 Data Transfer Request Status  |
| eTPU_CDTRSR_B_DTRS12 |        56 | ETPU.CDTRSR_B[DTRS12] | eTPUB Channel 12 Data Transfer Request Status |
| eTPU_CDTRSR_B_DTRS13 |        57 | ETPU.CDTRSR_B[DTRS13] | eTPUB Channel 13 Data Transfer Request Status |
| eTPU_CDTRSR_B_DTRS14 |        58 | ETPU.CDTRSR_B[DTRS14] | eTPUB Channel 14 Data Transfer Request Status |
| eTPU_CDTRSR_B_DTRS15 |        59 | ETPU.CDTRSR_B[DTRS15] | eTPUB Channel 15 Data Transfer Request Status |
| eTPU_CDTRSR_B_DTRS28 |        60 | ETPU.CDTRSR_B[DTRS28] | eTPUB Channel 28 Data Transfer Request Status |
| eTPU_CDTRSR_B_DTRS29 |        61 | ETPU.CDTRSR_B[DTRS29] | eTPUB Channel 29 Data Transfer Request Status |
| eTPU_CDTRSR_B_DTRS30 |        62 | ETPU.CDTRSR_B[DTRS30] | eTPUB Channel 30 Data Transfer Request Status |
| eTPU_CDTRSR_B_DTRS31 |        63 | ETPU.CDTRSR_B[DTRS31] | eTPUB Channel 31 Data Transfer Request Status |

## 9.5.4 DMA Arbitration Mode Considerations

## 9.5.4.1 Fixed Group Arbitration, Fixed Channel Arbitration

In this mode, the channel service request from the highest priority channel in the highest priority group will be selected to execute. If the eDMA is programmed so the channels within one group use 'fixed' priorities, and that group is assigned the highest 'fixed' priority of all groups, it is possible for that group to take all the bandwidth of the eDMA controller; that is, no other groups will be serviced if there is always at least one DMA request pending on a channel in the highest priority group when the controller arbitrates the next DMA request. The advantage of this scenario is that latency can be small for channels that need to be serviced quickly. Preemption is available in this scenario only.

## 9.5.4.2 Round Robin Group Arbitration, Fixed Channel Arbitration

The occurrence of one or more DMA requests from one or more groups, the channel with the highest priority from a specific group will be serviced first. Groups are serviced starting with the highest group number with a service request  and  rotating  through  to  the  lowest  group  number  containing  a  service request.

Once the channel request is serviced, the group round robin algorithm will select the highest pending request  from  the  next  group  in  the  round  robin  sequence.  Servicing  continues  round  robin,  always servicing the highest priority channel in the next group in the sequence, or just skipping a group if it has no pending requests.

If a channel requests service at a rate that equals or exceeds the round robin service rate, then that channel will always be serviced before lower priority channels in the same group, and thus the lower priority channels will never be serviced. The advantage of this scenario is that no one group will consume all the eDMA bandwidth. The highest priority channel selection latency is potentially greater than fixed/fixed arbitration. Excessive request rates on high priority channels could prevent the servicing of lower priority channels in the same group.

## 9.5.4.3 Round Robin Group Arbitration, Round Robin Channel Arbitration

Groups will be serviced as described in Section 9.5.4.2, but this time channels will be serviced in channel number order. Only one channel is serviced from each requesting group for each round robin pass through the groups.

Within each group, channels are serviced starting with the highest channel number and rotating through to the lowest channel number without regard to channel priority levels.

Because channels are serviced in round robin manner, any channel that generates DMA requests faster than a combination of the group round robin service rate and the channel service rate for its group will not prevent the servicing of other channels in its group. Any DMA requests that are not serviced are simply lost, but at least one channel will be serviced.

This scenario ensures that all channels will be guaranteed service at some point, regardless of the request rates. However, the potential latency could be quite high. All channels are treated equally. Priority levels are not used in round robin/round robin mode.

## 9.5.4.4 Fixed Group Arbitration, Round Robin Channel Arbitration

The highest priority group with a request will be serviced. Lower priority groups will be serviced if no pending requests exist in the higher priority groups.

Within each group, channels are serviced starting with the highest channel number and rotating through to the lowest channel number without regard to the channel priority levels assigned within the group.

This scenario could cause the same bandwidth consumption problem as indicated in Section 9.5.4.1, but all the channels in the highest priority group will get serviced. Service latency will be short on the highest priority group, but could potentially get very much longer and longer as the group priority decreases.

## 9.5.5 DMA Transfer

## 9.5.5.1 Single Request

To perform a simple transfer of ' n ' bytes of data with one activation, set the major loop to 1 (TCD.CITER = TCD.BITER = 1). The data transfer will begin after the channel service request is acknowledged and the channel  is  selected  to  execute.  Once  the  transfer  is  complete,  the  TCD.DONE  bit  will  be  set  and  an interrupt will be generated if properly enabled.

For  example,  the  following  TCD  entry  is  configured  to  transfer  16  bytes  of  data.  The  eDMA  is programmed for one iteration of the major loop transferring 16 bytes per iteration. The source memory has a byte wide memory port located at 0x1000. The destination memory has a word wide port located at 0x2000. The address offsets are programmed in increments to match the size of the transfer; one byte for the source and four bytes for the destination. The final source and destination addresses are adjusted to return to their beginning values.

TCD.CITER = TCD.BITER = 1

TCD.NBYTES = 16

TCD.SADDR = 0x1000

TCD.SOFF = 1

TCD.SSIZE = 0

TCD.SLAST = -16

TCD.DADDR = 0x2000

TCD.DOFF = 4

TCD.DSIZE = 2

TCD.DLAST\_SGA= -16

TCD.INT\_MAJ = 1

TCD.START = 1 (Should be written last after all other fields have been initialized)

All other TCD fields = 0

This would generate the following sequence of events:

- 1. Slave write to the TCD.START bit requests channel service.
- 2. The channel is selected by arbitration for servicing.
- 3. eDMA engine writes: TCD.DONE = 0, TCD.START = 0, TCD.ACTIVE = 1.
- 4. eDMA engine reads: channel TCD data from local memory to internal register file.
- 5. The source to destination transfers are executed as follows:
- a) read\_byte(0x1000), read\_byte(0x1001), read\_byte(0x1002), read\_byte(0x1003)
- b) write\_word(0x2000) -&gt; first iteration of the minor loop
- c) read\_byte(0x1004), read\_byte(0x1005), read\_byte(0x1006), read\_byte(0x1007)

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

- d) write\_word(0x2004) -&gt; second iteration of the minor loop
- e) read\_byte(0x1008), read\_byte(0x1009), read\_byte(0x100a), read\_byte(0x100b)
- f) write\_word(0x2008) -&gt; third iteration of the minor loop
- g) read\_byte(0x100c), read\_byte(0x100d), read\_byte(0x100e), read\_byte(0x100f)
- h) write\_word(0x200c) -&gt; last iteration of the minor loop -&gt; major loop complete
- 6. eDMA engine writes: TCD.SADDR = 0x1000, TCD.DADDR = 0x2000, TCD.CITER = 1 (TCD.BITER).
- 7. eDMA engine writes: TCD.ACTIVE = 0, TCD.DONE = 1, EDMA\_IRQR n = 1.
- 8. The channel retires.

The eDMA goes idle or services the next channel.

## 9.5.5.2 Multiple Requests

The next example is the same as previous with the exception of transferring 32 bytes via two hardware requests. The only fields that change are the major loop iteration count and the final address offsets. The eDMA is programmed for two iterations of the major loop transferring 16 bytes per iteration. After the channel's hardware requests are enabled in the EDMA\_ERQR, channel service requests are initiated by the slave device (ERQR should be set after TCD). Note that TCD.START = 0.

TCD.CITER = TCD.BITER = 2

TCD.NBYTES = 16

TCD.SADDR = 0x1000

TCD.SOFF = 1

TCD.SSIZE = 0

TCD.SLAST = -32

TCD.DADDR = 0x2000

TCD.DOFF = 4

TCD.DSIZE = 2

TCD.DLAST\_SGA= -32

TCD.INT\_MAJ = 1

TCD.START = 0 (Should be written last after all other fields have been initialized)

All other TCD fields = 0

This would generate the following sequence of events:

- 1. First hardware (eDMA peripheral request) request for channel service.
- 2. The channel is selected by arbitration for servicing.
- 3. eDMA engine writes: TCD.DONE = 0, TCD.START = 0, TCD.ACTIVE = 1.
- 4. eDMA engine reads: channel TCD data from local memory to internal register file.
- 5. The source to destination transfers are executed as follows:
- a) read\_byte(0x1000), read\_byte(0x1001), read\_byte(0x1002), read\_byte(0x1003)
- b) write\_word(0x2000) -&gt; first iteration of the minor loop
- c) read\_byte(0x1004), read\_byte(0x1005), read\_byte(0x1006), read\_byte(0x1007)

- d) write\_word(0x2004) -&gt; second iteration of the minor loop
- e) read\_byte(0x1008), read\_byte(0x1009), read\_byte(0x100a), read\_byte(0x100b)
- f) write\_word(0x2008) -&gt; third iteration of the minor loop
- g) read\_byte(0x100c), read\_byte(0x100d), read\_byte(0x100e), read\_byte(0x100f)
- h) write\_word(0x200c) -&gt; last iteration of the minor loop
- 6. eDMA engine writes: TCD.SADDR = 0x1010, TCD.DADDR = 0x2010, TCD.CITER = 1.
- 7. eDMA engine writes: TCD.ACTIVE = 0.
- 8. The channel retires -&gt; one iteration of the major loop.

The eDMA goes idle or services the next channel.

- 9. Second hardware (eDMA peripheral request) requests channel service.
- 10. The channel is selected by arbitration for servicing.
- 11. eDMA engine writes: TCD.DONE = 0, TCD.START = 0, TCD.ACTIVE = 1.
- 12. eDMA engine reads: channel TCD data from local memory to internal register file.
- 13. The source to destination transfers are executed as follows:
- a) read\_byte(0x1010), read\_byte(0x1011), read\_byte(0x1012), read\_byte(0x1013)
- b) write\_word(0x2010) -&gt; first iteration of the minor loop
- c) read\_byte(0x1014), read\_byte(0x1015), read\_byte(0x1016), read\_byte(0x1017)
- d) write\_word(0x2014) -&gt; second iteration of the minor loop
- e) read\_byte(0x1018), read\_byte(0x1019), read\_byte(0x101a), read\_byte(0x101b)
- f) write\_word(0x2018) -&gt; third iteration of the minor loop
- g) read\_byte(0x101c), read\_byte(0x101d), read\_byte(0x101e), read\_byte(0x101f)
- h) write\_word(0x201c) -&gt; last iteration of the minor loop -&gt; major loop complete
- 14. eDMA engine writes: TCD.SADDR = 0x1000, TCD.DADDR = 0x2000, TCD.CITER = 2 (TCD.BITER).
- 15. eDMA engine writes: TCD.ACTIVE = 0, TCD.DONE = 1, EDMA\_IRQR n = 1.
- 16. The channel retires -&gt; major loop complete.

The eDMA goes idle or services the next channel.

## 9.5.5.3 Modulo Feature

The modulo feature of the eDMA provides the ability to easily implement a circular data queue in which the size of the queue is a power of 2.  MOD is a 5-bit bitfield for both the source and destination in the TCD, and it specifies which lower address bits are allowed to increment from their original value after the address + offset calculation.  All upper address bits remain the same as in the original value. A setting of 0 for this field disables the modulo feature.

Table 9-23 shows how the transfer addresses are specified based on the setting of the MOD field. Here a circular buffer is created where the address wraps to the original value while the 28 upper address bits (0x1234567x) retain their original value. In this example the source address is set to 0x12345670, the offset is set to 4 bytes and the mod field is set to 4, allowing for a 2 4 byte (16-byte) size queue.

Table 9-23. Modulo Feature Example

|   Transfer Number | Address    |
|-------------------|------------|
|                 1 | 0x12345670 |
|                 2 | 0x12345674 |
|                 3 | 0x12345678 |
|                 4 | 0x1234567C |
|                 5 | 0x12345670 |
|                 6 | 0x12345674 |

## 9.5.6 TCD Status

## 9.5.6.1 Minor Loop Complete

There are two methods to test for minor loop completion when using software initiated service requests. The first method is to read the TCD.CITER field and test for a change. Another method may be extracted from  the  sequence  shown  below.  The  second  method  is  to  test  the  TCD.START  bit  AND  the TCD.ACTIVE bit. The minor loop complete condition is indicated by both bits reading zero after the TCD.START was written to a one. Polling the TCD.ACTIVE bit may be inconclusive because the active status may be missed if the channel execution is short in duration.

The TCD status bits execute the following sequence for a software activated channel:

- 1. TCD.START = 1, TCD.ACTIVE = 0, TCD.DONE = 0 (channel service request via software)
- 2. TCD.START = 0, TCD.ACTIVE = 1, TCD.DONE = 0 (channel is executing)
- 3. TCD.START = 0, TCD.ACTIVE = 0, TCD.DONE = 0 (channel has completed the minor loop and is idle) or
- 4. TCD.START = 0, TCD.ACTIVE = 0, TCD.DONE = 1 (channel has completed the major loop and is idle)

The best method to test for minor loop completion when using hardware initiated service requests is to read the TCD.CITER field and test for a change. The hardware request and acknowledge handshakes signals are not visible in the programmer's model.

The TCD status bits execute the following sequence for a hardware activated channel:

- 1. eDMA peripheral request asserts (channel service request via hardware)
- 2. TCD.START = 0, TCD.ACTIVE = 1, TCD.DONE = 0 (channel is executing)
- 3. TCD.START = 0, TCD.ACTIVE = 0, TCD.DONE = 0 (channel has completed the minor loop and is idle) or
- 4. TCD.START = 0, TCD.ACTIVE = 0, TCD.DONE = 1 (channel has completed the major loop and is idle)

For both activation types, the major loop complete status is explicitly indicated via the TCD.DONE bit.

The TCD.START bit is cleared automatically when the channel begins execution regardless of how the channel was activated.

## 9.5.6.2 Active Channel TCD Reads

The eDMA will read back the true TCD.SADDR, TCD.DADDR, and TCD.NBYTES values if read while a channel is executing. The true values of the SADDR, DADDR, and NBYTES are the values the eDMA engine is currently using in its internal register file and not the values in the TCD local memory for that channel.  The  addresses  (SADDR  and  DADDR)  and  NBYTES  (decrements  to  zero  as  the  transfer progresses) can give an indication of the progress of the transfer. All other values are read back from the TCD local memory.

## 9.5.6.3 Preemption Status

Preemption is only available when fixed arbitration is selected for both group and channel arbitration modes. A preempt-able situation is  one  in  which  a  preempt-enabled  channel  is  running  and  a  higher priority request becomes active. When the eDMA engine is not operating in fixed group, fixed channel arbitration mode, the determination of the relative priority of the actively running and the outstanding requests  become  undefined.  Channel  and/or  group  priorities  are  treated  as  equal  (or  more  exactly, constantly rotating) when round-robin arbitration mode is selected.

The  TCD.ACTIVE  bit  for  the  preempted  channel  remains  asserted  throughout  the  preemption.  The preempted channel is temporarily suspended while the preempting channel executes one iteration of the major loop. Two TCD.ACTIVE bits set at the same time in the overall TCD map indicates a higher priority channel is actively preempting a lower priority channel.

## 9.5.7 Channel Linking

Channel linking (or chaining) is a mechanism where one channel sets the TCD.START bit of another channel  (or  itself)  thus  initiating  a  service  request  for  that  channel.  This  operation  is  automatically performed by the eDMA engine at the conclusion of the major or minor loop when properly enabled.

The minor loop channel linking occurs at the completion of the minor loop (or one iteration of the major loop). The TCD.CITER.E\_LINK field are used to determine whether a minor loop link is requested. When enabled, the channel link is made after each iteration of the minor loop except for the last. When the major loop is exhausted, only the major loop channel link fields are used to determine if a channel link should be made. For example, with the initial fields of:

TCD.CITER.E\_LINK = 1

TCD.CITER.LINKCH = 0xC

TCD.CITER value = 0x4

TCD.MAJOR.E\_LINK = 1

TCD.MAJOR.LINKCH = 0x7

## will execute as:

- 1. Minor loop done -&gt; set channel 12 TCD.START bit
- 2. Minor loop done -&gt; set channel 12 TCD.START bit
- 3. Minor loop done -&gt; set channel 12 TCD.START bit
- 4. Minor loop done, major loop done -&gt; set channel 7 TCD.START bit

When minor loop linking is enabled (TCD.CITER.E\_LINK = 1), the TCD.CITER field uses a nine bit vector to form the current iteration count.

## Enhanced Direct Memory Access (eDMA)

When minor loop linking is disabled (TCD.CITER.E\_LINK = 0), the TCD.CITER field uses a 15-bit vector to form the current iteration count. The bits associated with the TCD.CITER.LINKCH field are concatenated onto the CITER value to increase the range of the CITER.

## NOTE

After configuration, the TCD.CITER.E\_LINK bit and the TCD.BITER.E\_LINK bit must be equal or a configuration error will be reported. The CITER and BITER vector widths must be equal in order to calculate the major loop, half-way done interrupt point.

Table 9-24  summarizes  how  a  DMA  channel  can  'link'  to  another  DMA  channel,  i.e,  use  another channel's TCD, at the end of a loop.

Table 9-24. Channel Linking Parameters

| Desired Link Behavior     | TCD Control Field Name   | Description                                                                    |
|---------------------------|--------------------------|--------------------------------------------------------------------------------|
| Link at end of Minor Loop | citer.e_link             | Enable channel-to-channel linking on minor loop completion (current iteration) |
| Link at end of Minor Loop | citer.linkch             | Link channel number when linking at end of minor loop (current iteration)      |
| Link at end of Major Loop | major.e_link             | Enable channel-to-channel linking on major loop completion                     |
| Link at end of Major Loop | major.linkch             | Link channel number when linking at end of major loop                          |

## 9.5.8 Dynamic Programming

This section provides recommended methods to change the programming model during channel execution.

## 9.5.8.1 Dynamic Channel Linking and Dynamic Scatter/Gather

Dynamic channel linking and dynamic scatter/gather is the process of changing the TCD.MAJOR.E\_LINK or TCD.E\_SG bits during channel execution. These bits are read from the TCD local memory at the end of channel execution thus allowing the user to enable either feature during channel execution.

Because the user is allowed to change the configuration during execution, a coherency model is needed. Consider  the  scenario  where  the  user  attempts  to  execute  a  dynamic  channel  link  by  enabling  the TCD.MAJOR.E\_LINK  bit  at  the  same  time the eDMA  engine  is retiring the channel. The TCD.MAJOR.E\_LINK would be set in the programmer's model, but it would be unclear whether the actual link was made before the channel retired.

The following coherency model is recommended when executing a dynamic channel link or dynamic scatter/gather request:

- 1. Set the TCD.MAJOR.E\_LINK bit
- 2. Read back the TCD.MAJOR.E\_LINK bit
- 3. Test the TCD.MAJOR.E\_LINK request status:
- a) If the bit is set, the dynamic link attempt was successful.

- b) If the bit is cleared, the attempted dynamic link did not succeed, the channel was already retiring.

This same coherency model is true for dynamic scatter/gather operations. For both dynamic requests, the TCD local memory controller forces the TCD.MAJOR.E\_LINK and TCD.E\_SG bits to zero on any writes to a channel's TCD once that channel's TCD.DONE bit is set indicating the major loop is complete.

## NOTE

The user must clear the TCD.DONE bit before writing the TCD.MAJOR.E\_LINK or TCD.E\_SG bits. The TCD.DONE bit is cleared automatically by the eDMA engine once a channel begins execution.

## 9.6 Revision History

## Substantive Changes since Rev 3.0

Changed 2 instances of EDMA\_INTR to be 'EDMA\_ERQH or EDMA\_ERQL'.

## Enhanced Direct Memory Access (eDMA)
