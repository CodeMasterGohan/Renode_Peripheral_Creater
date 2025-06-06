### Chatper 14 Fast Ethernet Controller (FEC)

## 14.1 Introduction

This fast ethernet control chapter of the MPC5553/MPC5554 Reference Manual provides a feature-set overview, a functional block diagram, and transceiver connection information for both the 10 and 100 Mbps MII (media independent interface), as well as the 7-wire serial interface. Additionally, detailed descriptions of operation and the programming model are included.

## NOTE

The information in this chapter applies only to the MPC5553 device. The MPC5554 device does not have an FEC block.

## 14.1.1 Block Diagram

The block diagram of the FEC is shown below. The FEC is implemented with a combination of hardware and microcode. The off-chip (Ethernet) interfaces are compliant with industry and IEEE ® 802.3 standards.

Figure 14-1. FEC Block Diagram

<!-- image -->

## 14.1.2 Overview

The  Ethernet  media  access  controller (MAC)  is  designed  to  support  both  10  and  100  Mbps Ethernet/IEEE ® 802.3 networks. An external transceiver interface and transceiver function are required to complete the interface to the media. The FEC supports three different standard MAC-PHY (physical) interfaces for connection to an external Ethernet transceiver. The FEC supports the 10/100 Mbps MII and the 10 Mbps-only 7-wire interface, which uses a subset of the MII signals.

The descriptor controller is a RISC-based controller that provides the following functions in the FEC:

- · Initialization (those internal registers not initialized by the user or hardware)
- · High level control of the DMA channels (initiating DMA transfers)
- · Interpreting buffer descriptors
- · Address recognition for receive frames
- · Random number generation for transmit collision backoff timer

## NOTE

DMA references in this section refer to the FEC's DMA engine. This DMA engine is for the transfer of FEC data only, and is not related to the DMA controller described in Chapter 9.

The RAM is the focal point of all data flow in the fast Ethernet controller and is divided into transmit and receive FIFOs. The FIFO boundaries are programmable using the FRSR register. User data flows to/from the DMA block from/to the receive/transmit FIFOs. Transmit data flows from the transmit FIFO into the transmit block and receive data flows from the receive block into the receive FIFO.

The user controls the FEC by writing, through the SIF (slave interface) module, into control registers located in each block. The CSR (control and status register) block provides global control (e.g. Ethernet reset and enable) and interrupt handling registers.

The MII block provides a serial channel for control/status communication with the external physical layer device  (transceiver).  This  serial  channel  consists  of  the  MDC  (management  data  clock)  and  MDIO (management data input/output) lines of the MII interface.

The DMA block provides multiple channels allowing transmit data, transmit descriptor, receive data, and receive descriptor accesses to run independently.

The  transmit  and  receive  blocks  provide  the  Ethernet  MAC  functionality  (with  some  assist  from microcode).

The message information block (MIB) maintains counters for a variety of network events and statistics. It is not necessary for operation of the FEC but provides valuable counters for network management. The counters supported are the RMON (RFC 1757) Ethernet Statistics groupand some of the IEEE ® 802.3 counters.

## 14.1.3 Features

The FEC incorporates the following features:

- · Support for three different Ethernet physical interfaces:
- - 100-Mbps IEEE ® 802.3 MII
- - 10-Mbps IEEE ® 802.3 MII
- - 10-Mbps 7-wire interface (industry standard)
- · Built-in FIFO and DMA controller

- · IEEE ® 802.3 MAC (compliant with IEEE ® 802.3 1998 edition)
- · IEEE ® 802.3 full duplex flow control
- · Programmable max frame length supports IEEE ® 802.1 VLAN tags and priority
- · Support for full-duplex operation (200 Mbps throughput) with a system clock rate of 100 MHz using the external TX\_CLK or RX\_CLK
- · Support for half-duplex operation (100 Mbps throughput) with a system clock rate of 50 MHz using the external TX\_CLK or RX\_CLK
- · Retransmission from transmit FIFO following a collision (no system bus utilization)
- · Automatic internal flushing of the receive FIFO for runts (collision fragments) and address recognition rejects (no system bus utilization)
- · Address recognition
- - Frames with broadcast address may be always accepted or always rejected
- - Exact match for single 48-bit individual (unicast) address
- - Hash (64-bit hash) check of individual (unicast) addresses
- - Hash (64-bit hash) check of group (multicast) addresses
- - Promiscuous mode
- · RMON and IEEE ® statistics
- · Interrupts for network activity and error conditions

## 14.2 Modes of Operation

The primary operational modes are described in this section.

## 14.2.1 Full and Half Duplex Operation

Full duplex mode is intended for use on point-to-point links between switches or end node to switch. Half duplex mode is used in connections between an end node and a repeater or between repeaters. Selection of the duplex mode is controlled by TCR[FDEN].

When configured for full duplex mode, flow control may be enabled. Refer to the TCR[RFC\_PAUSE] and TCR[TFC\_PAUSE] bits, the RCR[FCE] bit, and Section 14.4.10, 'Full Duplex Flow Control,' for more details.

Throughputs  of  200  Mbps  in  full  duplex  operations  and  100  Mbps  in  half-duplex  operations  can  be attained.

## 14.2.2 Interface Options

The following interface options are supported. A detailed discussion of the interface configurations is provided in Section 14.4.5, 'Network Interface Options'.

## 14.2.2.1 10 Mbps and 100 Mbps MII Interface

MII is the media independent interface defined by the IEEE ® 802.3 standard for 10/100 Mbps operation. The MAC-PHY interface may be configured to operate in MII mode by asserting RCR[MII\_MODE].

The speed of operation is determined by the TX\_CLK and RX\_CLK signals which are driven by the external  transceiver.  The  transceiver  will  either  auto-negotiate  the  speed  or  it  may  be  controlled  by software via the serial management interface (MDC/MDIO signals) to the transceiver. Refer to the MMFR

and MSCR register descriptions as well as the section on the MII for a description of how to read and write registers in the transceiver via this interface.

## 14.2.2.2 10 Mpbs 7-Wire Interface Operation

The  FEC  supports a 7-wire interface as used by many  10  Mbps  ethernet transceivers. The RCR[MII\_MODE] bit controls this functionality. If this bit is deasserted, the MII mode is disabled and the 10 Mbps, 7-wire mode is enabled.

## 14.2.3 Address Recognition Options

The address options supported are promiscuous, broadcast reject, individual address (hash or exact match), and multicast hash match. Address recognition options are discussed in detail in Section 14.4.8, 'Ethernet Address Recognition'.

## 14.2.4 Internal Loopback

Internal  loopback  mode  is  selected  via  RCR[LOOP].  Loopback  mode  is  discussed  in  detail  in Section 14.4.13, 'Internal and External Loopback.'

## 14.3 Programming Model

This section gives an overview of the registers, followed by a description of the buffers.

The FEC is programmed by a combination of control/status registers (CSRs) and buffer descriptors. The CSRs are used for mode control and to extract global status information. The descriptors are used to pass data buffers and related buffer information between the hardware and software.

## 14.3.1 Top Level Module Memory Map

The FEC implementation requires a 1-Kbyte memory map space. This is divided into two sections of 512 bytes each. The first is used for control/status registers. The second contains event/statistic counters held in the MIB block. Table 14-1 defines the top level memory map. All accesses to and from the FEC memory map must be via 32-bit accesses. There is no support for accesses other than 32-bit.

Table 14-1. Module Memory Map

| Address                              | Function                 |
|--------------------------------------|--------------------------|
| FFF4_C000 (Base Address) - FFF4_C1FF | Control/Status Registers |
| FFF4_C200 - FFF4_C3FF                | MIB Block Counters       |

## 14.3.2 Detailed Memory Map (Control/Status Registers)

Table 14-2 shows the FEC register memory map with each register address, name, and a brief description. The base address of the FEC registers is 0xFFF4\_C000.

## NOTE

Some memory locations are not documented. The actual FEC memory map is  from  0xFFF4\_C000  -  0xFFF4\_C5FF.  Also,  some  bits  in  otherwise documented registers are not documented. These memory locations and bits are not needed for the FEC software driver. They are used mainly by the FEC subblocks for the FEC operation and happen to be visible through the slave interface.

Errant writes to these locations can corrupt FEC operation. Because the FEC is a system bus master, errant writes also can result in the corruption of any memory mapped location in the system. However, even errant writes to documented FEC memory locations can cause the same corruption.

Table 14-2. FEC Register Memory Map

| Address Offset (Base +)   | Name   |   Width 1 | Description                             |
|---------------------------|--------|-----------|-----------------------------------------|
| 0x0004                    | EIR    |        32 | Interrupt Event Register                |
| 0x0008                    | EIMR   |        32 | Interrupt Mask Register                 |
| 0x0010                    | RDAR   |        32 | Receive Descriptor Active Register      |
| 0x0014                    | TDAR   |        32 | Transmit Descriptor Active Register     |
| 0x0024                    | ECR    |        32 | Ethernet Control Register               |
| 0x0040                    | MMFR   |        32 | MII Management Frame Register           |
| 0x0044                    | MSCR   |        32 | MII Speed Control Register              |
| 0x0064                    | MIBC   |        32 | MIB Control/Status Register             |
| 0x0084                    | RCR    |        32 | Receive Control Register                |
| 0x00C4                    | TCR    |        32 | Transmit Control Register               |
| 0x00E4                    | PALR   |        32 | MAC Address Low Register                |
| 0x00E8                    | PAUR   |        32 | MAC Address Upper Register + Type Field |
| 0x00EC                    | OPD    |        32 | Opcode + Pause Duration Fields          |
| 0x0118                    | IAUR   |        32 | Upper 32 bits of Individual Hash Table  |
| 0x011C                    | IALR   |        32 | Lower 32 Bits of Individual Hash Table  |
| 0x0120                    | GAUR   |        32 | Upper 32 bits of Group Hash Table       |
| 0x0124                    | GALR   |        32 | Lower 32 bits of Group Hash Table       |
| 0x0144                    | TFWR   |        32 | Transmit FIFO Watermark                 |
| 0x014C                    | FRBR   |        32 | FIFO Receive Bound Register             |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

-

Table 14-2. FEC Register Memory Map (continued)

| Address Offset (Base +)   | Name   |   Width 1 | Description                         |
|---------------------------|--------|-----------|-------------------------------------|
| 0x0150                    | FRSR   |        32 | FIFO Receive FIFO Start Registers   |
| 0x0180                    | ERDSR  |        32 | Pointer to Receive Descriptor Ring  |
| 0x0184                    | ETDSR  |        32 | Pointer to Transmit Descriptor Ring |
| 0x0188                    | EMRBR  |        32 | Maximum Receive Buffer Size         |

- 1 All accesses to and from the FEC memory map must be via 32-bit accesses. There is no support for accesses other than 32-bit.

## 14.3.3 MIB Block Counters Memory Map

Table 14-3 defines the MIB Counters memory map which defines the locations in the MIB RAM space where hardware-maintained counters reside. These fall in the 0xFFF4\_C200 - 0xFFF4\_C3FF address offset range. The counters are divided into two groups.

- · RMON counters are included which cover the Ethernet Statistics counters defined in RFC 1757. In addition to the counters defined in the Ethernet Statistics group, a counter is included to count truncated frames as the FEC only supports frame lengths up to 2047 bytes. The RMON counters are implemented independently for transmit and receive to insure accurate network statistics when operating in full duplex mode.
- · IEEE ® counters are included which support the Mandatory and Recommended counter packages defined in section 5 of ANSI/IEEE ® Std. 802.3 (1998 edition). The IEEE ® Basic Package objects are supported by the FEC but do not require counters in the MIB block. In addition, some of the recommended package objects which are supported do not require MIB counters. Counters for transmit and receive full duplex flow control frames are included as well.

Table 14-3. MIB Counters Memory Map

| Address Offset 1 (Base +)   | Mnemonic         | Description                              |
|-----------------------------|------------------|------------------------------------------|
| 0x0200                      | RMON_T_DROP      | Count of frames not counted correctly    |
| 0x0204                      | RMON_T_PACKETS   | RMON Tx packet count                     |
| 0x0208                      | RMON_T_BC_PKT    | RMON Tx Broadcast Packets                |
| 0x020C                      | RMON_T_MC_PKT    | RMON Tx Multicast Packets                |
| 0x0210                      | RMON_T_CRC_ALIGN | RMON Tx Packets w CRC/Align error        |
| 0x0214                      | RMON_T_UNDERSIZE | RMON Tx Packets < 64 bytes, good crc     |
| 0x0218                      | RMON_T_OVERSIZE  | RMON Tx Packets > MAX_FL bytes, good crc |
| 0x021C                      | RMON_T_FRAG      | RMON Tx Packets < 64 bytes, bad crc      |
| 0x0220                      | RMON_T_JAB       | RMON Tx Packets > MAX_FL bytes, bad crc  |
| 0x0224                      | RMON_T_COL       | RMON Tx collision count                  |
| 0x0228                      | RMON_T_P64       | RMON Tx 64 byte packets                  |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 14-3. MIB Counters Memory Map (continued)

| Address Offset 1 (Base +)   | Mnemonic           | Description                                  |
|-----------------------------|--------------------|----------------------------------------------|
| 0x022C                      | RMON_T_P65TO127    | RMON Tx 65 to 127 byte packets               |
| 0x0230                      | RMON_T_P128TO255   | RMON Tx 128 to 255 byte packets              |
| 0x0234                      | RMON_T_P256TO511   | RMON Tx 256 to 511 byte packets              |
| 0x0238                      | RMON_T_P512TO1023  | RMON Tx 512 to 1023 byte packets             |
| 0x023C                      | RMON_T_P1024TO2047 | RMON Tx 1024 to 2047 byte packets            |
| 0x0240                      | RMON_T_P_GTE2048   | RMON Tx packets w > 2048 bytes               |
| 0x0244                      | RMON_T_OCTETS      | RMON Tx Octets                               |
| 0x0248                      | IEEE_T_DROP        | Count of frames not counted correctly        |
| 0x024C                      | IEEE_T_FRAME_OK    | Frames Transmitted OK                        |
| 0x0250                      | IEEE_T_1COL        | Frames Transmitted with Single Collision     |
| 0x0254                      | IEEE_T_MCOL        | Frames Transmitted with Multiple Collisions  |
| 0x0258                      | IEEE_T_DEF         | Frames Transmitted after Deferral Delay      |
| 0x025C                      | IEEE_T_LCOL        | Frames Transmitted with Late Collision       |
| 0x0260                      | IEEE_T_EXCOL       | Frames Transmitted with Excessive Collisions |
| 0x0264                      | IEEE_T_MACERR      | Frames Transmitted with Tx FIFO Underrun     |
| 0x0268                      | IEEE_T_CSERR       | Frames Transmitted with Carrier Sense Error  |
| 0x026C                      | IEEE_T_SQE         | Frames Transmitted with SQE Error            |
| 0x0270                      | IEEE_T_FDXFC       | Flow Control Pause frames transmitted        |
| 0x0274                      | IEEE_T_OCTETS_OK   | Octet count for Frames Transmitted w/o Error |
| 0x0280                      | RMON_R_DROP        | Count of frames not counted correctly        |
| 0x0284                      | RMON_R_PACKETS     | RMON Rx packet count                         |
| 0x0288                      | RMON_R_BC_PKT      | RMON Rx Broadcast Packets                    |
| 0x028C                      | RMON_R_MC_PKT      | RMON Rx Multicast Packets                    |
| 0x0290                      | RMON_R_CRC_ALIGN   | RMON Rx Packets w CRC/Align error            |
| 0x0294                      | RMON_R_UNDERSIZE   | RMON Rx Packets < 64 bytes, good crc         |
| 0x0298                      | RMON_R_OVERSIZE    | RMON Rx Packets > MAX_FL bytes, good crc     |
| 0x029C                      | RMON_R_FRAG        | RMON Rx Packets < 64 bytes, bad crc          |
| 0x02A0                      | RMON_R_JAB         | RMON Rx Packets > MAX_FL bytes, bad crc      |
| 0x02A4                      | -                  | Reserved                                     |
| 0x02A8                      | RMON_R_P64         | RMON Rx 64 byte packets                      |
| 0x02AC                      | RMON_R_P65TO127    | RMON Rx 65 to 127 byte packets               |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 14-3. MIB Counters Memory Map (continued)

| Address Offset 1 (Base +)   | Mnemonic           | Description                           |
|-----------------------------|--------------------|---------------------------------------|
| 0x02B0                      | RMON_R_P128TO255   | RMON Rx 128 to 255 byte packets       |
| 0x02B4                      | RMON_R_P256TO511   | RMON Rx 256 to 511 byte packets       |
| 0x02B8                      | RMON_R_P512TO1023  | RMON Rx 512 to 1023 byte packets      |
| 0x02BC                      | RMON_R_P1024TO2047 | RMON Rx 1024 to 2047 byte packets     |
| 0x02C0                      | RMON_R_P_GTE2048   | RMON Rx packets w > 2048 bytes        |
| 0x02C4                      | RMON_R_OCTETS      | RMON Rx Octets                        |
| 0x02C8                      | IEEE_R_DROP        | Count of frames not counted correctly |
| 0x02CC                      | IEEE_R_FRAME_OK    | Frames Received OK                    |
| 0x02D0                      | IEEE_R_CRC         | Frames Received with CRC Error        |
| 0x02D4                      | IEEE_R_ALIGN       | Frames Received with Alignment Error  |
| 0x02D8                      | IEEE_R_MACERR      | Receive Fifo Overflow count           |
| 0x02DC                      | IEEE_R_FDXFC       | Flow Control Pause frames received    |
| 0x02E0                      | IEEE_R_OCTETS_OK   | Octet count for Frames Rcvd w/o Error |

- 1 All accesses to and from the FEC memory map must be via 32-bit accesses. There is no support for accesses other than 32-bit.

## 14.3.4 Registers

## 14.3.4.1 FEC Burst Optimization Master Control Register (FBOMCR) (MPC5553 Only)

Although not an FEC register, the FEC burst optimization master control register (FBOMCR) controls FEC  burst  optimization  behavior  on  the  system  bus,  hence  it  is  described  below.  FEC  registers  are described  in  Section 14.3.4.2.1,  'Ethernet  Interrupt  Event  Register  (EIR)'  through  Section 14.3.4.3.4, 'Receive Buffer Size Register (EMRBR).'

In order to increase throughput, the FEC interface to the system bus can accumulate read requests or writes to  burst  those  transfers  on  the  system  bus.  The FBOMCR determines the XBAR ports for which this bursting is enabled, as well as whether the bursting is for reads, writes, or both. FBOMCR also controls how errors for writes are handled. The FBOMCR address is 0xFFF4\_0024, which is the ECSM base address 0xFFF4\_0000 plus the offset of 0x0024.

Figure 14-2. FEC Burst Optimization Master Control Register (FBOMCR)

<!-- image -->

|         | 0                                                     | 1                                                     | 2                                                     | 3                                                     | 4                                                     | 5                                                     | 6                                                     | 7                                                     | 8                                                     | 9                                                     | 10                                                    | 11                                                    | 12                                                    | 13                                                    | 14                                                    | 15                                                    |
|---------|-------------------------------------------------------|-------------------------------------------------------|-------------------------------------------------------|-------------------------------------------------------|-------------------------------------------------------|-------------------------------------------------------|-------------------------------------------------------|-------------------------------------------------------|-------------------------------------------------------|-------------------------------------------------------|-------------------------------------------------------|-------------------------------------------------------|-------------------------------------------------------|-------------------------------------------------------|-------------------------------------------------------|-------------------------------------------------------|
| R W     | FXS BE0                                               | FXS BE1                                               | FXS BE2                                               | 0                                                     | 0                                                     | 0                                                     | FXS BE6                                               | FXS BE7                                               | RBEN                                                  | WBEN                                                  | ACCERR                                                | 0                                                     | 0                                                     | 0                                                     | 0                                                     | 0                                                     |
| Reset   | 0                                                     | 0                                                     | 0                                                     | 0                                                     | 0                                                     | 0                                                     | 0                                                     | 0                                                     | 0                                                     | 0                                                     | 0                                                     | 0                                                     | 0                                                     | 0                                                     | 0                                                     | 0                                                     |
| Address | ECSM Base Address: 0xFFF4_0000 + 0x0024 = 0xFFF4_0024 | ECSM Base Address: 0xFFF4_0000 + 0x0024 = 0xFFF4_0024 | ECSM Base Address: 0xFFF4_0000 + 0x0024 = 0xFFF4_0024 | ECSM Base Address: 0xFFF4_0000 + 0x0024 = 0xFFF4_0024 | ECSM Base Address: 0xFFF4_0000 + 0x0024 = 0xFFF4_0024 | ECSM Base Address: 0xFFF4_0000 + 0x0024 = 0xFFF4_0024 | ECSM Base Address: 0xFFF4_0000 + 0x0024 = 0xFFF4_0024 | ECSM Base Address: 0xFFF4_0000 + 0x0024 = 0xFFF4_0024 | ECSM Base Address: 0xFFF4_0000 + 0x0024 = 0xFFF4_0024 | ECSM Base Address: 0xFFF4_0000 + 0x0024 = 0xFFF4_0024 | ECSM Base Address: 0xFFF4_0000 + 0x0024 = 0xFFF4_0024 | ECSM Base Address: 0xFFF4_0000 + 0x0024 = 0xFFF4_0024 | ECSM Base Address: 0xFFF4_0000 + 0x0024 = 0xFFF4_0024 | ECSM Base Address: 0xFFF4_0000 + 0x0024 = 0xFFF4_0024 | ECSM Base Address: 0xFFF4_0000 + 0x0024 = 0xFFF4_0024 | ECSM Base Address: 0xFFF4_0000 + 0x0024 = 0xFFF4_0024 |
|         | 16                                                    | 17                                                    | 18                                                    | 19                                                    | 20                                                    | 21                                                    | 22                                                    | 23                                                    | 24                                                    | 25                                                    | 26                                                    | 27                                                    | 28                                                    | 29                                                    | 30                                                    | 31                                                    |
| R       | 0                                                     | 0                                                     | 0                                                     | 0                                                     | 0                                                     | 0                                                     | 0                                                     | 0                                                     | 0                                                     | 0                                                     | 0                                                     | 0                                                     | 0                                                     | 0                                                     | 0                                                     | 0                                                     |
| W       |                                                       |                                                       |                                                       |                                                       |                                                       |                                                       |                                                       |                                                       |                                                       |                                                       |                                                       |                                                       |                                                       |                                                       |                                                       |                                                       |
| Reset   | 0                                                     | 0                                                     | 0                                                     | 0                                                     | 0                                                     | 0                                                     | 0                                                     | 0                                                     | 0                                                     | 0                                                     | 0                                                     | 0                                                     | 0                                                     | 0                                                     | 0                                                     | 0                                                     |
| Address | ECSM Base Address: 0xFFF4_0000 + 0x0024 = 0xFFF4_0024 | ECSM Base Address: 0xFFF4_0000 + 0x0024 = 0xFFF4_0024 | ECSM Base Address: 0xFFF4_0000 + 0x0024 = 0xFFF4_0024 | ECSM Base Address: 0xFFF4_0000 + 0x0024 = 0xFFF4_0024 | ECSM Base Address: 0xFFF4_0000 + 0x0024 = 0xFFF4_0024 | ECSM Base Address: 0xFFF4_0000 + 0x0024 = 0xFFF4_0024 | ECSM Base Address: 0xFFF4_0000 + 0x0024 = 0xFFF4_0024 | ECSM Base Address: 0xFFF4_0000 + 0x0024 = 0xFFF4_0024 | ECSM Base Address: 0xFFF4_0000 + 0x0024 = 0xFFF4_0024 | ECSM Base Address: 0xFFF4_0000 + 0x0024 = 0xFFF4_0024 | ECSM Base Address: 0xFFF4_0000 + 0x0024 = 0xFFF4_0024 | ECSM Base Address: 0xFFF4_0000 + 0x0024 = 0xFFF4_0024 | ECSM Base Address: 0xFFF4_0000 + 0x0024 = 0xFFF4_0024 | ECSM Base Address: 0xFFF4_0000 + 0x0024 = 0xFFF4_0024 | ECSM Base Address: 0xFFF4_0000 + 0x0024 = 0xFFF4_0024 | ECSM Base Address: 0xFFF4_0000 + 0x0024 = 0xFFF4_0024 |

## Table 14-4. FBOMCR Field Descriptions

| Bits   | Name          | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
|--------|---------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-7    | FXSBE n [0:7] | FXSBE - FEC XBAR slave burst enable. FXSBE n enables bursting by the FEC interface to the XBARslave port controlled by by that respective FXSBE n bit. If FXSBE n is asserted, then that XBAR slave port enabled by the bit can accept the bursts allowed by RBEN and WBEN. Otherwise, the FEC interface will not burst to the XBAR slave port controlled by that respective FXSBE n bit. Read bursts from that XBAR slave port are enabled by RBEN. Write bursts to that XBAR slave port are enabled by WBEN. FXSBE n assignments to XBAR slave ports: FXSBE0 = Flash FXSBE1 = EBI FXSBE2 = Internal SRAM FXSBE6 = Peripheral bridge A FXSBE7 = Peripheral bridge B                                                                                                                                                                                                                                                                                                                                                                  |
| 8      | RBEN          | Global read burst enable from XBAR slave port designated by FXSBE n 0 = Read bursting from all XBAR slave ports is disabled. 1 = Read bursting is enabled from any XBAR slave port whose FXSBE n bit is asserted.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| 9      | WBEN          | Global write burst enable to XBAR slave port designated by FXSBE n 0 = Write bursting to all XBAR slave ports is disabled. 1 = Write bursting is enabled to any XBAR slave port whose FXSBE n bit is asserted.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| 10     | ACCERR        | Accumulate error - This bit determines whether an error response for the first half of the write burst is accumulated to the second half of the write burst or discarded. In order to complete the burst, the FEC interface to the system bus responds by indicating that the first half of the burst completed without error before it actually writes the data so that it can fetch the second half of the write data from the FIFO. When actually written onto the system bus, the first half of the write burst can have an error. Because this half initially responded without an error to the FIFO, the error is discarded or accumulated with the error response for the second half of the burst. 0 Any error to the first half of the write burst is discarded. 1 Any actual error response to the first half of the write burst is accumulated in the second half's response. In other words, an error response to the first half will be seen in the response to the second half, even if the second half does not error. |
| 11-31  | -             | Reserved, should be cleared.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |

## 14.3.4.2 FEC Registers

The  following  sections  describe  each  FEC  register  in  detail.  The  base  address  of  these  registers  is 0xFFF4\_C000.

## 14.3.4.2.1 Ethernet Interrupt Event Register (EIR)

When an event occurs that sets a bit in the EIR, an interrupt will be generated if the corresponding bit in the interrupt mask register (EIMR) is also set. The bit in the EIR is cleared if a one is written to that bit position; writing zero has no effect. This register is cleared upon hardware reset.

These  interrupts  can  be  divided  into  operational  interrupts,  transceiver/network  error  interrupts,  and internal error interrupts. Interrupts which may occur in normal operation are GRA, TXF, TXB, RXF, RXB, and MII. Interrupts resulting from errors/problems detected in the network or transceiver are HBERR, BABR, BABT, LC, and RL. Interrupts resulting from internal errors are HBERR and UN.

Some of the error interrupts are independently counted in the MIB block counters. Software may choose to mask off these interrupts since these errors will be visible to network management via the MIB counters:

- · HBERR - IEEE\_T\_SQE
- · BABR - RMON\_R\_OVERSIZE (good CRC), RMON\_R\_JAB (bad CRC)
- · BABT - RMON\_T\_OVERSIZE (good CRC), RMON\_T\_JAB (bad CRC)
- · LATE\_COL - IEEE\_T\_LCOL
- · COL\_RETRY\_LIM - IEEE\_T\_EXCOL
- · XFIFO\_UN - IEEET\_MACERR

<!-- image -->

|         | 0                           | 1                           | 2                           | 3                           | 4                           | 5                           | 6                           | 7                           | 8                           | 9                           | 10                          | 11                          | 12                          | 13                          | 14                          | 15                          |
|---------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|
| R       | HBERR                       | BABR                        | BABT                        | GRA                         | TXF                         | TXB                         | RXF                         | RXB                         | MII                         | EBERR                       | LC                          | RL                          | UN                          | 0                           | 0                           | 0                           |
| W       | w1c                         | w1c                         | w1c                         | w1c                         | w1c                         | w1c                         | w1c                         | w1c                         | w1c                         | w1c                         | w1c                         | w1c                         | w1c                         |                             |                             |                             |
| Reset   | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           |
| Address | Base (0xFFF4_C000) + 0x0004 | Base (0xFFF4_C000) + 0x0004 | Base (0xFFF4_C000) + 0x0004 | Base (0xFFF4_C000) + 0x0004 | Base (0xFFF4_C000) + 0x0004 | Base (0xFFF4_C000) + 0x0004 | Base (0xFFF4_C000) + 0x0004 | Base (0xFFF4_C000) + 0x0004 | Base (0xFFF4_C000) + 0x0004 | Base (0xFFF4_C000) + 0x0004 | Base (0xFFF4_C000) + 0x0004 | Base (0xFFF4_C000) + 0x0004 | Base (0xFFF4_C000) + 0x0004 | Base (0xFFF4_C000) + 0x0004 | Base (0xFFF4_C000) + 0x0004 | Base (0xFFF4_C000) + 0x0004 |
|         | 16                          | 17                          | 18                          | 19                          | 20                          | 21                          | 22                          | 23                          | 24                          | 25                          | 26                          | 27                          | 28                          | 29                          | 30                          | 31                          |
| R       | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           |
| W       |                             |                             |                             |                             |                             |                             |                             |                             |                             |                             |                             |                             |                             |                             |                             |                             |
| Reset   | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           |
| Address | Base (0xFFF4_C000) + 0x0004 | Base (0xFFF4_C000) + 0x0004 | Base (0xFFF4_C000) + 0x0004 | Base (0xFFF4_C000) + 0x0004 | Base (0xFFF4_C000) + 0x0004 | Base (0xFFF4_C000) + 0x0004 | Base (0xFFF4_C000) + 0x0004 | Base (0xFFF4_C000) + 0x0004 | Base (0xFFF4_C000) + 0x0004 | Base (0xFFF4_C000) + 0x0004 | Base (0xFFF4_C000) + 0x0004 | Base (0xFFF4_C000) + 0x0004 | Base (0xFFF4_C000) + 0x0004 | Base (0xFFF4_C000) + 0x0004 | Base (0xFFF4_C000) + 0x0004 | Base (0xFFF4_C000) + 0x0004 |

1 'w1c' signifies the bit is cleared by writing 1 to it.

Figure 14-3. Ethernet Interrupt Event Register (EIR)

## Table 14-5. EIR Field Descriptions

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

|   Bits | Name   | Description                                                                                                                                                                |
|--------|--------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|      0 | HBERR  | Heartbeat error. This interrupt indicates that HBCis set in the TCR register and that the COL input was not asserted within the Heartbeat window following a transmission. |
|      1 | BABR   | Babbling receive error. This bit indicates a frame wasreceived with length in excess of RCR[MAX_FL] bytes.                                                                 |

Table 14-5. EIR Field Descriptions  (continued)

| Bits   | Name   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
|--------|--------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 2      | BABT   | Babbling transmit error. This bit indicates that the transmitted frame length has exceeded RCR[MAX_FL]bytes. This condition is usually caused by a frame that is too long being placed into the transmit data buffers. Truncation does not occur.                                                                                                                                                                                                                                                                                                                                                                                |
| 3      | GRA    | Graceful stop complete. This interrupt will be asserted for one of three reasons. Graceful stop means that the transmitter is put into a pause state after completion of the frame currently being transmitted. 1) A graceful stop, which was initiated by the setting of the TCR[GTS] bit is now complete. 2) A graceful stop, which was initiated by the setting of the TCR[TFC_PAUSE] bit is now complete. 3) A graceful stop, which was initiated by the reception of a valid full duplex flow control 'pause' frame is now complete. Refer to the 'Full Duplex Flow Control' section of the Functional Description chapter. |
| 4      | TXF    | Transmit frame interrupt. This bit indicates that a frame has been transmitted and that the last corresponding buffer descriptor has been updated.                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| 5      | TXB    | Transmit buffer interrupt. This bit indicates that a transmit buffer descriptor has been updated.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| 6      | RXF    | Receive frame interrupt. This bit indicates that a frame has been received and that the last corresponding buffer descriptor has been updated.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| 7      | RXB    | Receive buffer interrupt. This bit indicates that a receive buffer descriptor has been updated that was not the last in the frame.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| 8      | MII    | MII interrupt. This bit indicates that the MII has completed the data transfer requested.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| 9      | EBERR  | Ethernet bus error. This bit indicates that a system bus error occurred when a DMA transaction was underway. When the EBERR bit is set, ECR[ETHER_EN] will be cleared, halting frame processing by the FEC. When this occurs software will need to insure that the FIFO controller and DMA are also soft reset.                                                                                                                                                                                                                                                                                                                  |
| 10     | LC     | Late collison. This bit indicates that a collision occurred beyond the collision window (slot time) in half duplex mode. The frame is truncated with a bad CRC and the remainder of the frame is discarded.                                                                                                                                                                                                                                                                                                                                                                                                                      |
| 11     | RL     | Collision retry limit. This bit indicates that a collision occurred on each of 16 successive attempts to transmit the frame. The frame is discarded without being transmitted and transmission of the next frame will commence. Can only occur in half duplex mode.                                                                                                                                                                                                                                                                                                                                                              |
| 12     | UN     | Transmit FIFO underrun. This bit indicates that the transmit FIFO became empty before the complete frame was transmitted. A bad CRC is appended to the frame fragment and the remainder of the frame is discarded.                                                                                                                                                                                                                                                                                                                                                                                                               |
| 13-31  | -      | Reserved, should be cleared.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## 14.3.4.2.2 Ethernet Interrupt Mask Register (EIMR)

The  EIMR  register  controls  which  interrupt  events  are  allowed  to  generate  actual  interrupts.  All implemented  bits  in  this  CSR  are  read/write.  This  register  is  cleared  upon  a  hardware  reset.  If  the corresponding bits in both the EIR and EIMR registers are set, the interrupt will be signalled to the CPU. The interrupt signal will remain asserted until a 1 is written to the EIR bit (write 1 to clear) or a 0 is written to the EIMR bit.

|         | 0             | 1             | 2             | 3             | 4             | 5             | 6             | 7             | 8             | 9             | 10            | 11            | 12            | 13            | 14            | 15            |
|---------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| R       | HBERR M       | BABR M        | BABT M        | GRA M         | TXF M         | TXB M         | RXF M         | RXB M         | MII M         | EBERR M       | LC M          | RL M          | UN M          | 0             | 0             | 0             |
| W       | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           |               |               |               |
| Reset   | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Address | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 |
|         | 16            | 17            | 18            | 19            | 20            | 21            | 22            | 23            | 24            | 25            | 26            | 27            | 28            | 29            | 30            | 31            |
| R       | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| W       |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset   | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Address | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 |

1 'w1c' signifies the bit is cleared by writing 1 to it.

Figure 14-4. Interrupt Mask Register (EIMR)

Table 14-6. EIMR Field Descriptions

| Bits   | Name                             | Description                                                                                                                                                                                                                                                                                  |
|--------|----------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-12   | See Figure 17-6 and Table 14-5 . | Interrupt mask. Each bit corresponds to an interrupt source defined by the EIR register. The corresponding EIMR bit determines whether an interrupt condition can generate an interrupt. 0 The corresponding interrupt source is masked. 1 The corresponding interrupt source is not masked. |
| 13-31  | -                                | Reserved, should be cleared.                                                                                                                                                                                                                                                                 |

## 14.3.4.2.3 Receive Descriptor Active Register (RDAR)

RDAR is a command register, written by the user, that indicates that the receive descriptor ring has been updated (empty receive buffers have been produced by the driver with the empty bit set).

Whenever the register is written, the R\_DES\_ACTIVE bit is set. This is independent of the data actually written by the user. When set, the FEC will poll the receive descriptor ring and process receive frames (provided ECR[ETHER\_EN] is also set). Once the FEC polls a receive descriptor whose empty bit is not set, then the FEC will clear R\_DES\_ACTIVE and cease receive descriptor ring polling until the user sets the bit again, signifying that additional descriptors have been placed into the receive descriptor ring.

The RDAR register is cleared at reset and when ECR[ETHER\_EN] is cleared.

Figure 14-5. Receive Descriptor Active Register (RDAR)

<!-- image -->

|         | 0             | 1             | 2             | 3             | 4             | 5             | 6             | 7             | 8             | 9             | 10            | 11            | 12            | 13            | 14            | 15            |
|---------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| R       | 0             | 0             | 0             | 0             | 0             | 0             | 0             | R_DES_ACTIVE  | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| W       |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset   | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Address | Base + 0x0010 | Base + 0x0010 | Base + 0x0010 | Base + 0x0010 | Base + 0x0010 | Base + 0x0010 | Base + 0x0010 | Base + 0x0010 | Base + 0x0010 | Base + 0x0010 | Base + 0x0010 | Base + 0x0010 | Base + 0x0010 | Base + 0x0010 | Base + 0x0010 | Base + 0x0010 |
|         | 16            | 17            | 18            | 19            | 20            | 21            | 22            | 23            | 24            | 25            | 26            | 27            | 28            | 29            | 30            | 31            |
| R       | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| W       |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset   | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Address | Base + 0x0010 | Base + 0x0010 | Base + 0x0010 | Base + 0x0010 | Base + 0x0010 | Base + 0x0010 | Base + 0x0010 | Base + 0x0010 | Base + 0x0010 | Base + 0x0010 | Base + 0x0010 | Base + 0x0010 | Base + 0x0010 | Base + 0x0010 | Base + 0x0010 | Base + 0x0010 |

Table 14-7. RDAR Field Descriptions

| Bits   | Name         | Description                                                                                                                                                                                                             |
|--------|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-6    | -            | Reserved, should be cleared.                                                                                                                                                                                            |
| 7      | R_DES_ACTIVE | Set to one when this register is written, regardless of the value written. Cleared by the FEC device whenever no additional 'empty' descriptors remain in the receive ring. Also cleared when ECR[ETHER_EN] is cleared. |
| 8-31   | -            | Reserved, should be cleared.                                                                                                                                                                                            |

## 14.3.4.2.4 Transmit Descriptor Active Register (TDAR)

The TDAR is a command register that should be written by the user to indicate that the transmit descriptor ring has been updated (transmit buffers have been produced by the driver with the ready bit set in the buffer descriptor).

Whenever the register is written, the X\_DES\_ACTIVE bit is set. This value is independent of the data actually written by the user. When set, the FEC will poll the transmit descriptor ring and process transmit frames (provided ECR[ETHER\_EN] is also set). Once the FEC polls a transmit descriptor whose ready bit is not set, then the FEC will clear X\_DES\_ACTIVE and cease transmit descriptor ring polling until the user sets the bit again, signifying additional descriptors have been placed into the transmit descriptor ring.

The TDAR register is cleared at reset, when ECR[ETHER\_EN] is cleared, or when ECR[RESET] is set.

Figure 14-6. Transmit Descriptor Active Register (TDAR)

<!-- image -->

|         | 0             | 1             | 2             | 3             | 4             | 5             | 6             | 7             | 8             | 9             | 10            | 11            | 12            | 13            | 14            | 15            |
|---------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| R       | 0             | 0             | 0             | 0             | 0             | 0             | 0             | X_DES_ACTIVE  | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| W       |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset   | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Address | Base + 0x0014 | Base + 0x0014 | Base + 0x0014 | Base + 0x0014 | Base + 0x0014 | Base + 0x0014 | Base + 0x0014 | Base + 0x0014 | Base + 0x0014 | Base + 0x0014 | Base + 0x0014 | Base + 0x0014 | Base + 0x0014 | Base + 0x0014 | Base + 0x0014 | Base + 0x0014 |
|         | 16            | 17            | 18            | 19            | 20            | 21            | 22            | 23            | 24            | 25            | 26            | 27            | 28            | 29            | 30            | 31            |
| R       | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| W       |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset   | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Address | Base + 0x0014 | Base + 0x0014 | Base + 0x0014 | Base + 0x0014 | Base + 0x0014 | Base + 0x0014 | Base + 0x0014 | Base + 0x0014 | Base + 0x0014 | Base + 0x0014 | Base + 0x0014 | Base + 0x0014 | Base + 0x0014 | Base + 0x0014 | Base + 0x0014 | Base + 0x0014 |

Table 14-8. TDAR Field Descriptions

| Bits   | Name         | Description                                                                                                                                                                                                              |
|--------|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-6    | -            | Reserved, should be cleared.                                                                                                                                                                                             |
| 7      | X_DES_ACTIVE | Set to one when this register is written, regardless of the value written. Cleared by the FEC device whenever no additional 'ready' descriptors remain in the transmit ring. Also cleared when ECR[ETHER_EN] is cleared. |
| 8-31   | -            | Reserved, should be cleared.                                                                                                                                                                                             |

## 14.3.4.2.5 Ethernet Control Register (ECR)

ECR is a read/write user register, though both fields in this register may be altered by hardware as well. The ECR is used to enable/disable the FEC.

Figure 14-7.  Ethernet Control Register (ECR)

<!-- image -->

|         | 0             | 1             | 2             | 3             | 4             | 5             | 6             | 7             | 8             | 9             | 10            | 11            | 12            | 13            | 14            | 15            |
|---------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| R       | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| W       |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset   | 1             | 1             | 1             | 1             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Address | Base + 0x0024 | Base + 0x0024 | Base + 0x0024 | Base + 0x0024 | Base + 0x0024 | Base + 0x0024 | Base + 0x0024 | Base + 0x0024 | Base + 0x0024 | Base + 0x0024 | Base + 0x0024 | Base + 0x0024 | Base + 0x0024 | Base + 0x0024 | Base + 0x0024 | Base + 0x0024 |
|         | 16            | 17            | 18            | 19            | 20            | 21            | 22            | 23            | 24            | 25            | 26            | 27            | 28            | 29            | 30            | 31            |
| R       | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | ETHER_EN      | RESET         |
| W       |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset   | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Address | Base + 0x0024 | Base + 0x0024 | Base + 0x0024 | Base + 0x0024 | Base + 0x0024 | Base + 0x0024 | Base + 0x0024 | Base + 0x0024 | Base + 0x0024 | Base + 0x0024 | Base + 0x0024 | Base + 0x0024 | Base + 0x0024 | Base + 0x0024 | Base + 0x0024 | Base + 0x0024 |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 14-9. ECR Field Descriptions

| Bits   | Name     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
|--------|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-29   | -        | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| 30     | ETHER_EN | When this bit is set, the FEC is enabled, and reception and transmission are possible. When this bit is cleared, reception is immediately stopped and transmission is stopped after a bad CRC is appended to any currently transmitted frame. The buffer descriptors for an aborted transmit frame are not updated after clearing this bit. WhenETHER_ENisdeasserted, the DMA, buffer descriptor, and FIFO control logic are reset, including the buffer descriptor and FIFO pointers. The ETHER_EN bit is altered by hardware under the following conditions: GLYPH<127> ECR[RESET] is set by software, in which case ETHER_EN will be cleared GLYPH<127> An error condition causes the EIR[EBERR] bit to set, in which case ETHER_EN will be cleared |
| 31     | RESET    | When this bit is set, the equivalent of a hardware reset is performed but it is local to the FEC. ETHER_EN is cleared and all other FEC registers take their reset values. Also, any transmission/reception currently in progress is abruptly aborted. This bit is automatically cleared by hardware during the reset sequence. The reset sequence takes approximately 8 system clock cycles after RESET is written with a 1.                                                                                                                                                                                                                                                                                                                          |

## 14.3.4.2.6 MII Management Frame Register (MMFR)

The MMFR is accessed by the user and does not reset to a defined value. The MMFR register is used to communicate with the attached MII compatible PHY devices, providing read/write access to their MII registers. Performing a write to the MMFR will cause a management frame to be sourced unless the MSCR has been programmed to 0. In the case of writing to MMFR when MSCR = 0, if the MSCR register is then written to a non-zero value, an MII frame will be generated with the data previously written to the MMFR. This allows MMFR and MSCR to be programmed in either order if MSCR is currently zero.

<!-- image -->

|         | 0             | 1             | 2             | 3             | 4             | 5             | 6             | 7             | 8             | 9             | 10            | 11            | 12            | 13            | 14            | 15            |
|---------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| R       | ST            | ST            | OP            | OP            | PA            | PA            | PA            | PA            | PA            | RA            | RA            | RA            | RA            | RA            | TA            | TA            |
| W       |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset   | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             |
| Address | Base + 0x0040 | Base + 0x0040 | Base + 0x0040 | Base + 0x0040 | Base + 0x0040 | Base + 0x0040 | Base + 0x0040 | Base + 0x0040 | Base + 0x0040 | Base + 0x0040 | Base + 0x0040 | Base + 0x0040 | Base + 0x0040 | Base + 0x0040 | Base + 0x0040 | Base + 0x0040 |
|         | 16            | 17            | 18            | 19            | 20            | 21            | 22            | 23            | 24            | 25            | 26            | 27            | 28            | 29            | 30            | 31            |
| R       | DATA          | DATA          | DATA          | DATA          | DATA          | DATA          | DATA          | DATA          | DATA          | DATA          | DATA          | DATA          | DATA          | DATA          | DATA          | DATA          |
| W       |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset   | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             |
| Address | Base + 0x0040 | Base + 0x0040 | Base + 0x0040 | Base + 0x0040 | Base + 0x0040 | Base + 0x0040 | Base + 0x0040 | Base + 0x0040 | Base + 0x0040 | Base + 0x0040 | Base + 0x0040 | Base + 0x0040 | Base + 0x0040 | Base + 0x0040 | Base + 0x0040 | Base + 0x0040 |

1 'U' signifies a bit that is uninitialized. Refer to the Preface of the book.

Figure 14-8. MII Management Frame Register (MMFR)

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## Table 14-10. MMFR Field Descriptions

| Bit   | Name   | Description                                                                                                                                                                                                                                                                |
|-------|--------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-1   | ST     | Start of frame delimiter. These bits must be programmed to 01 for a valid MII management frame.                                                                                                                                                                            |
| 2-3   | OP     | Operation code. This field must be programmed to 10 (read) or 01 (write) to generate a valid MII management frame. A value of 11 will produce 'read' frame operation while a value of 00 will produce 'write' frame operation, but these frames will not be MII compliant. |
| 4-8   | PA     | PHYaddress. This field specifies one of up to 32 attached PHY devices.                                                                                                                                                                                                     |
| 9-13  | RA     | Register address. This field specifies one of up to 32 registers within the specified PHY device.                                                                                                                                                                          |
| 14-15 | TA     | Turn around. This field must be programmed to 10 to generate a valid MII management frame.                                                                                                                                                                                 |
| 16-31 | DATA   | Management frame data. This is the field for data to be written to or read from the PHY register.                                                                                                                                                                          |

To perform a read or write operation on the MII management interface, the MMFR register must be written by the user. To generate a valid read or write management frame, the ST field must be written with a 01 pattern, and the TA field must be written with a 10. If other patterns are written to these fields, a frame will be generated but will not comply with the IEEE ® 802.3 MII definition.

To generate an IEEE ® 802.3-compliant MII management interface write frame (write to a PHY register), the user must write {01 01 PHYAD REGAD 10 DATA} to the MMFR register. Writing this pattern will cause the control logic to shift out the data in the MMFR register following a preamble generated by the control state machine. During this time the contents of the MMFR register will be altered as the contents are  serially  shifted  and  will  be  unpredictable  if  read  by  the  user.  Once  the  write  management  frame operation has completed, the MII interrupt will be generated. At this time the contents of the MMFR register will match the original value written.

To generate an MII management interface read frame (read a PHY register) the user must write {01 10 PHYAD REGAD 10 XXXX} to the MMFR register (the content of the DATA field is a don't care). Writing this pattern will cause the control logic to shift out the data in the MMFR register following a preamble generated by the control state machine. During this time the contents of the MMFR register will be altered as the contents are serially shifted, and will be unpredictable if read by the user. Once the read management frame operation has completed, the MII interrupt will be generated. At this time the contents of the MMFR register will match the original value written except for the DATA field whose contents have been replaced by the value read from the PHY register.

If the MMFR register is written while frame generation is in progress, the frame contents will be altered. Software should software should poll the EIR[MII] bit or use the EIR[MII] bit to generate an interrupt to avoid writing to the MMFR register while frame generation is in progress.

## 14.3.4.2.7 MII Speed Control Register (MSCR)

The MSCR provides control of the MII clock (MDC signal) frequency, allows a preamble drop on the MII management frame, and provides observability (intended for manufacturing test) of an internal counter used in generating the MDC clock signal.

Figure 14-9. MII Speed Control Register (MSCR)

<!-- image -->

|         | 0             | 1             | 2             | 3             | 4             | 5             | 6             | 7             | 8             | 9             | 10            | 11            | 12            | 13            | 14            | 15            |
|---------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| R       | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| W       |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset   | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Address | Base + 0x0044 | Base + 0x0044 | Base + 0x0044 | Base + 0x0044 | Base + 0x0044 | Base + 0x0044 | Base + 0x0044 | Base + 0x0044 | Base + 0x0044 | Base + 0x0044 | Base + 0x0044 | Base + 0x0044 | Base + 0x0044 | Base + 0x0044 | Base + 0x0044 | Base + 0x0044 |
|         | 16            | 17            | 18            | 19            | 20            | 21            | 22            | 23            | 24            | 25            | 26            | 27            | 28            | 29            | 30            | 31            |
| R       | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | DIS_PREAMBLE  |               | MII_SPEED     | MII_SPEED     | MII_SPEED     | MII_SPEED     |               | 0             |
| W       |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset   | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Address | Base + 0x0044 | Base + 0x0044 | Base + 0x0044 | Base + 0x0044 | Base + 0x0044 | Base + 0x0044 | Base + 0x0044 | Base + 0x0044 | Base + 0x0044 | Base + 0x0044 | Base + 0x0044 | Base + 0x0044 | Base + 0x0044 | Base + 0x0044 | Base + 0x0044 | Base + 0x0044 |

Table 14-11. MSCR Field Descriptions

| Bits   | Name         | Description                                                                                                                                                                                                                                                                                           |
|--------|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-23   | -            | Reserved, should be cleared.                                                                                                                                                                                                                                                                          |
| 24     | DIS_PREAMBLE | Asserting this bit will cause preamble (32 1's) not to be prepended to the MII management frame. The MII standard allows the preamble to be dropped if the attached PHY devices does not require it.                                                                                                  |
| 25-30  | MII_SPEED    | MII_SPEEDcontrols the frequency of the MII managementinterface clock (MDC) relative to the system clock. Avalue of 0 in this field will 'turn off' the MDC and leave it in low voltage state. Any non-zero value will result in the MDC frequency of 1/(MII_SPEED * 4) of the system clock frequency. |
| 31     | -            | Reserved, should be cleared.                                                                                                                                                                                                                                                                          |

The MII\_SPEED field must be programmed with a value to provide an MDC frequency of less than or equal to 2.5 MHz to be compliant with the IEEE ® 802.3 MII specification. The MII\_SPEED must be set to a non-zero value in order to source a read or write management frame. After the management frame is complete the MSCR register may optionally be set to zero to turn off the MDC. The MDC generated will have a 50% duty cycle except when MII\_SPEED is changed during operation (change will take effect following either a rising or falling edge of MDC).

If the system clock is 50 MHz, programming this register to 0x0000\_0005 will result in an MDC frequency of 50 MHz * 1/20 = 2.5 MHz. A table showing optimum values for MII\_SPEED as a function of system clock frequency is provided below.

Table 14-12. Programming Examples for MSCR

| System Clock Frequency   | MII_SPEED (field in reg)   | MDC frequency   |
|--------------------------|----------------------------|-----------------|
| 50 MHz                   | 0x5                        | 2.5 MHz         |
| 66 MHz                   | 0x7                        | 2.36 MHz        |
| 80 MHz                   | 0x8                        | 2.5 MHz         |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 14-12. Programming Examples for MSCR (continued)

| System Clock Frequency   | MII_SPEED (field in reg)   | MDC frequency   |
|--------------------------|----------------------------|-----------------|
| 100 MHz                  | 0xA                        | 2.5 MHz         |
| 132 MHz                  | 0xD                        | 2.5 MHz         |

## 14.3.4.2.8 MIB Control Register (MIBC)

The MIBC is a read/write register used to provide control of and to observe the state of the MIB block. This  register  is  accessed  by  user  software  if  there  is  a  need  to  disable  the  MIB  block  operation.  For example, in order to clear all MIB counters in RAM the user should disable the MIB block, then clear all the MIB RAM locations, then enable the MIB block. The MIB\_DISABLE bit is reset to 1. See Table 14-3 for the locations of the MIB counters.

Figure 14-10. MIB Control Register (MIBC)

<!-- image -->

|         | 0             | 1             | 2             | 3             | 4             | 5             | 6             | 7             | 8             | 9             | 10            | 11            | 12            | 13            | 14            | 15            |
|---------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| R       | MIB_DISABLE   | MIB_IDLE      | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| W       |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset   | 1             | 1             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Address | Base + 0x0064 | Base + 0x0064 | Base + 0x0064 | Base + 0x0064 | Base + 0x0064 | Base + 0x0064 | Base + 0x0064 | Base + 0x0064 | Base + 0x0064 | Base + 0x0064 | Base + 0x0064 | Base + 0x0064 | Base + 0x0064 | Base + 0x0064 | Base + 0x0064 | Base + 0x0064 |
|         | 16            | 17            | 18            | 19            | 20            | 21            | 22            | 23            | 24            | 25            | 26            | 27            | 28            | 29            | 30            | 31            |
| R       | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| W       |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset   | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Address | Base + 0x0064 | Base + 0x0064 | Base + 0x0064 | Base + 0x0064 | Base + 0x0064 | Base + 0x0064 | Base + 0x0064 | Base + 0x0064 | Base + 0x0064 | Base + 0x0064 | Base + 0x0064 | Base + 0x0064 | Base + 0x0064 | Base + 0x0064 | Base + 0x0064 | Base + 0x0064 |

Table 14-13. MIBC Field Descriptions

| Bits   | Name        | Description                                                                                |
|--------|-------------|--------------------------------------------------------------------------------------------|
| 0      | MIB_DISABLE | A read/write control bit. If set, the MIB logic will halt and not update any MIB counters. |
| 1      | MIB_IDLE    | A read-only status bit. If set the MIB block is not currently updating any MIB counters.   |
| 2-31   | -           | Reserved.                                                                                  |

## 14.3.4.2.9 Receive Control Register (RCR)

The RCR is programmed by the user. The RCR controls the operational mode of the receive block and should be written only when ECR[ETHER\_EN] = 0 (initialization time).

Figure 14-11. Receive Control Register (RCR)

<!-- image -->

## Table 14-14. RCR Field Descriptions

| Bits   | Name     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|--------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-4    | -        | Reserved, should be cleared.                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| 5-15   | MAX_FL   | Maximum frame length. Resets to decimal 1518. Length is measured starting at DA and includes the CRC at the end of the frame. Transmit frames longer than MAX_FL will cause the BABT interrupt to occur. Receive frames longer than MAX_FL will cause the BABR interrupt to occur and will set the LG bit in the end of frame receive buffer descriptor. The recommended default value to be programmed by the user is 1518 or 1522 (if VLAN Tags are supported). |
| 16-25  | -        | Reserved, should be cleared.                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| 26     | FCE      | Flow control enable. If asserted, the receiver will detect PAUSE frames. Upon PAUSE frame detection, the transmitter will stop transmitting data frames for a given duration.                                                                                                                                                                                                                                                                                     |
| 27     | BC_REJ   | Broadcast frame reject. If asserted, frames with DA (destination address) = FF_FF_FF_FF_FF_FF will be rejected unless the PROM bit is set. If both BC_REJ and PROM = 1, then frames with broadcast DA will be accepted and the M(MISS) bit will be set in the receive buffer descriptor.                                                                                                                                                                          |
| 28     | PROM     | Promiscuous mode. All frames are accepted regardless of address matching.                                                                                                                                                                                                                                                                                                                                                                                         |
| 29     | MII_MODE | Media independent interface mode. Selects external interface mode. Setting this bit to one selects MII mode, setting this bit equal to zero selects 7-wire mode (used only for serial 10 Mbps). This bit controls the interface mode for both transmit and receive blocks.                                                                                                                                                                                        |

## Table 14-14. RCR Field Descriptions (continued)

|   Bits | Name   | Description                                                                                                                                                                                                                                               |
|--------|--------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|     30 | DRT    | Disable receive on transmit. 0 Receive path operates independently of transmit (use for full duplex or to monitor transmit activity in half duplex mode). 1 Disable reception of frames while transmitting (normally used for half duplex mode).          |
|     31 | LOOP   | Internal loopback. If set, transmitted frames are looped back internal to the device and the transmit output signals are not asserted. The system clock is substituted for the TX_CLK when LOOP is asserted. DRT must be set to zero when asserting LOOP. |

## 14.3.4.2.10 Transmit Control Register (TCR)

The TCR is read/write and is written by the user to configure the transmit block. This register is cleared at system reset. Bits 29 and 30 should be modified only when ECR[ETHER\_EN] = 0.

Figure 14-12. Transmit Control Register (TCR)

<!-- image -->

|         | 0             | 1             | 2             | 3             | 4             | 5             | 6             | 7             | 8             | 9             | 10            | 11            | 12            | 13            | 14            | 15            |
|---------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| R       | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| W       |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset   | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Address | Base + 0x00C4 | Base + 0x00C4 | Base + 0x00C4 | Base + 0x00C4 | Base + 0x00C4 | Base + 0x00C4 | Base + 0x00C4 | Base + 0x00C4 | Base + 0x00C4 | Base + 0x00C4 | Base + 0x00C4 | Base + 0x00C4 | Base + 0x00C4 | Base + 0x00C4 | Base + 0x00C4 | Base + 0x00C4 |
|         | 16            | 17            | 18            | 19            | 20            | 21            | 22            | 23            | 24            | 25            | 26            | 27            | 28            | 29            | 30            | 31            |
| R       | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | RFC_ PAUSE    | TFC_ PAUSE    | FDEN          | HBC           | GTS           |
| W       |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset   | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Address | Base + 0x00C4 | Base + 0x00C4 | Base + 0x00C4 | Base + 0x00C4 | Base + 0x00C4 | Base + 0x00C4 | Base + 0x00C4 | Base + 0x00C4 | Base + 0x00C4 | Base + 0x00C4 | Base + 0x00C4 | Base + 0x00C4 | Base + 0x00C4 | Base + 0x00C4 | Base + 0x00C4 | Base + 0x00C4 |

## Table 14-15. TCR Field Descriptions

| Bits   | Name      | Description                                                                                                                                                                                                                                                                              |
|--------|-----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-26   | -         | Reserved, should be cleared.                                                                                                                                                                                                                                                             |
| 27     | RFC_PAUSE | Receive frame control pause. This read-only status bit will be asserted when a full duplex flow control pause frame has been received and the transmitter is paused for the duration defined in this pause frame. This bit will automatically clear when the pause duration is complete. |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 14-15. TCR Field Descriptions (continued)

|   Bits | Name      | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
|--------|-----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|     28 | TFC_PAUSE | Transmit frame control pause. Transmits a PAUSE frame when asserted. When this bit is set, the MAC will stop transmission of data frames after the current transmission is complete. At this time, the GRAinterrupt in the EIR register will be asserted. With transmission of data frames stopped, the MAC will transmit a MAC Control PAUSE frame. Next, the MAC will clear the TFC_PAUSE bit and resume transmitting data frames. Note that if the transmitter is paused due to user assertion of GTS or reception of a PAUSE frame, the MAC may still transmit a MAC Control PAUSE frame.                                                                                                                                                                                                                   |
|     29 | FDEN      | Full duplex enable. If set, frames are transmitted independent of carrier sense and collision inputs. This bit should only be modified when ETHER_EN is deasserted.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
|     30 | HBC       | Heartbeat control. If set, the heartbeat check is performed following end of transmission and the HBbit in the status register will be set if the collision input does not assert within the heartbeat window. This bit should only be modified when ETHER_EN is deasserted.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
|     31 | GTS       | Graceful transmit stop. When this bit is set, the MAC will stop transmission after any frame that is currently being transmitted is complete and the GRA interrupt in the EIR register will be asserted. If frame transmission is not currently underway, the GRA interrupt will be asserted immediately. Once transmission has completed, a 'restart' can be accomplished by clearing the GTS bit. The next frame in the transmit FIFO will then be transmitted. If an early collision occurs during transmission when GTS = 1, transmission will stop after the collision. The frame will be transmitted again once GTS is cleared. Note that there may be old frames in the transmit FIFO that will be transmitted when GTS is reasserted. To avoid this deassert ECR[ETHER_EN] following the GRA interrupt. |

## 14.3.4.2.11 Physical Address Low Register (PALR)

The PALR is written by the user. This register contains the lower 32 bits (bytes 0,1,2,3) of the 48-bit MAC address used in the address recognition process to compare with the DA (destination address) field of receive frames with an individual DA. In addition, this register is used in bytes 0 through 3 of the 6-byte source address field when transmitting PAUSE frames. This register is not reset and must be initialized by the user.

<!-- image -->

|         | 0             | 1             | 2             | 3             | 4             | 5             | 6             | 7             | 8             | 9             | 10            | 11            | 12            | 13            | 14            | 15            |
|---------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| R       | PADDR1        | PADDR1        | PADDR1        | PADDR1        | PADDR1        | PADDR1        | PADDR1        | PADDR1        | PADDR1        | PADDR1        | PADDR1        | PADDR1        | PADDR1        | PADDR1        | PADDR1        | PADDR1        |
| W       |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset   | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             |
| Address | Base + 0x00E4 | Base + 0x00E4 | Base + 0x00E4 | Base + 0x00E4 | Base + 0x00E4 | Base + 0x00E4 | Base + 0x00E4 | Base + 0x00E4 | Base + 0x00E4 | Base + 0x00E4 | Base + 0x00E4 | Base + 0x00E4 | Base + 0x00E4 | Base + 0x00E4 | Base + 0x00E4 | Base + 0x00E4 |
|         | 16            | 17            | 18            | 19            | 20            | 21            | 22            | 23            | 24            | 25            | 26            | 27            | 28            | 29            | 30            | 31            |
| R       | PADDR1        | PADDR1        | PADDR1        | PADDR1        | PADDR1        | PADDR1        | PADDR1        | PADDR1        | PADDR1        | PADDR1        | PADDR1        | PADDR1        | PADDR1        | PADDR1        | PADDR1        | PADDR1        |
| W       |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset   | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             |
| Address | Base + 0x00E4 | Base + 0x00E4 | Base + 0x00E4 | Base + 0x00E4 | Base + 0x00E4 | Base + 0x00E4 | Base + 0x00E4 | Base + 0x00E4 | Base + 0x00E4 | Base + 0x00E4 | Base + 0x00E4 | Base + 0x00E4 | Base + 0x00E4 | Base + 0x00E4 | Base + 0x00E4 | Base + 0x00E4 |

1 'U' signifies a bit that is uninitialized. Refer to the Preface of the book.

Figure 14-13. Physical Address Low Register (PALR)

Table 14-16. PALR Field Descriptions

| Bits   | Name   | Description                                                                                                                                                                     |
|--------|--------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-31   | PADDR1 | Bytes 0 (bits 0:7), 1 (bits 8:15), 2 (bits 16:23) and 3 (bits 24:31) of the 6-byte individual address to be used for exact match, and the Source Address field in PAUSE frames. |

## 14.3.4.2.12 Physical Address Upper Register (PAUR)

The PAUR is written by the user. This register contains the upper 16 bits (bytes 4 and 5) of the 48-bit MAC address used in the address recognition process to compare with the DA (destination address) field of receive frames with an individual DA. In addition, this register is used in bytes 4 and 5 of the 6-byte Source Address field  when  transmitting  PAUSE  frames.  Bits  16:31  of  PAUR  contain  a  constant  TYPE  field (0x8808) used for transmission of PAUSE frames.This register is not reset, and bits 0:15 must be initialized by the user. Refer to Section 14.4.10, 'Full Duplex Flow Control' for information on using the TYPE field.

<!-- image -->

|         | 0             | 1             | 2             | 3             | 4             | 5             | 6             | 7             | 8             | 9             | 10            | 11            | 12            | 13            | 14            | 15            |
|---------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| R       | PADDR2        | PADDR2        | PADDR2        | PADDR2        | PADDR2        | PADDR2        | PADDR2        | PADDR2        | PADDR2        | PADDR2        | PADDR2        | PADDR2        | PADDR2        | PADDR2        | PADDR2        | PADDR2        |
| W       |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset   | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             |
| Address | Base + 0x00E8 | Base + 0x00E8 | Base + 0x00E8 | Base + 0x00E8 | Base + 0x00E8 | Base + 0x00E8 | Base + 0x00E8 | Base + 0x00E8 | Base + 0x00E8 | Base + 0x00E8 | Base + 0x00E8 | Base + 0x00E8 | Base + 0x00E8 | Base + 0x00E8 | Base + 0x00E8 | Base + 0x00E8 |
|         | 16            | 17            | 18            | 19            | 20            | 21            | 22            | 23            | 24            | 25            | 26            | 27            | 28            | 29            | 30            | 31            |
| R       | TYPE          | TYPE          | TYPE          | TYPE          | TYPE          | TYPE          | TYPE          | TYPE          | TYPE          | TYPE          | TYPE          | TYPE          | TYPE          | TYPE          | TYPE          | TYPE          |
| W       |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset   | 1             | 0             | 0             | 0             | 1             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 1             | 0             | 0             | 0             |
| Address | Base + 0x00E8 | Base + 0x00E8 | Base + 0x00E8 | Base + 0x00E8 | Base + 0x00E8 | Base + 0x00E8 | Base + 0x00E8 | Base + 0x00E8 | Base + 0x00E8 | Base + 0x00E8 | Base + 0x00E8 | Base + 0x00E8 | Base + 0x00E8 | Base + 0x00E8 | Base + 0x00E8 | Base + 0x00E8 |

1 'U' signifies a bit that is uninitialized. Refer to the Preface of the book.

Figure 14-14. Physical Address Upper Register (PAUR)

Table 14-17. PAUR Field Descriptions

| BIts   | Name   | Description                                                                                                                                     |
|--------|--------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-15   | PADDR2 | Bytes 4 (bits 0:7) and 5 (bits 8:15) of the 6-byte individual address to be used for exact match, and the Source Address field in PAUSE frames. |
| 16-31  | TYPE   | The type field is used in PAUSE frames. These bits are a constant, 0x8808.                                                                      |

## 14.3.4.2.13 Opcode/Pause Duration Register (OPD)

The OPD is read/write accessible. This register contains the 16-bit OPCODE and 16-bit pause duration (PAUSE\_DUR) fields used in transmission of a PAUSE frame. The OPCODE field is a constant value, 0x0001. When another node detects a PAUSE frame, that node will pause transmission for the duration specified in the pause duration field. This register is not reset and must be initialized by the user. Refer to Section 14.4.10, 'Full Duplex Flow Control' for information on using the OPD register.

<!-- image -->

|         | 0             | 1             | 2             | 3             | 4             | 5             | 6             | 7             | 8             | 9             | 10            | 11            | 12            | 13            | 14            | 15            |
|---------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| R       | OPCODE        | OPCODE        | OPCODE        | OPCODE        | OPCODE        | OPCODE        | OPCODE        | OPCODE        | OPCODE        | OPCODE        | OPCODE        | OPCODE        | OPCODE        | OPCODE        | OPCODE        | OPCODE        |
| W       |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset   | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 1             |
| Address | Base + 0x00EC | Base + 0x00EC | Base + 0x00EC | Base + 0x00EC | Base + 0x00EC | Base + 0x00EC | Base + 0x00EC | Base + 0x00EC | Base + 0x00EC | Base + 0x00EC | Base + 0x00EC | Base + 0x00EC | Base + 0x00EC | Base + 0x00EC | Base + 0x00EC | Base + 0x00EC |
|         | 16            | 17            | 18            | 19            | 20            | 21            | 22            | 23            | 24            | 25            | 26            | 27            | 28            | 29            | 30            | 31            |
| R       | PAUSE_DUR     | PAUSE_DUR     | PAUSE_DUR     | PAUSE_DUR     | PAUSE_DUR     | PAUSE_DUR     | PAUSE_DUR     | PAUSE_DUR     | PAUSE_DUR     | PAUSE_DUR     | PAUSE_DUR     | PAUSE_DUR     | PAUSE_DUR     | PAUSE_DUR     | PAUSE_DUR     | PAUSE_DUR     |
| W       |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset   | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             |
| Address | Base + 0x00EC | Base + 0x00EC | Base + 0x00EC | Base + 0x00EC | Base + 0x00EC | Base + 0x00EC | Base + 0x00EC | Base + 0x00EC | Base + 0x00EC | Base + 0x00EC | Base + 0x00EC | Base + 0x00EC | Base + 0x00EC | Base + 0x00EC | Base + 0x00EC | Base + 0x00EC |

1 'U' signifies a bit that is uninitialized. Refer to the Preface of the book.

Figure 14-15. Opcode/Pause Duration Register (OPD)

## Table 14-18. OPD Field Descriptions

| Bits   | Name      | Description                                                           |
|--------|-----------|-----------------------------------------------------------------------|
| 0-15   | OPCODE    | Opcode field used in PAUSE frames. These bits are a constant, 0x0001. |
| 16-31  | PAUSE_DUR | Pause duration field used in PAUSE frames.                            |

## 14.3.4.2.14 Descriptor Individual Upper Address Register (IAUR)

The IAUR is written by the user. This register contains the upper 32 bits of the 64-bit individual address hash table used in the address recognition process to check for possible match with the DA field of receive frames with an individual DA. This register is not reset and must be initialized by the user.

<!-- image -->

|         | 0             | 1             | 2             | 3             | 4             | 5             | 6             | 7             | 8             | 9             | 10            | 11            | 12            | 13            | 14            | 15            |
|---------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| R       | IADDR1        | IADDR1        | IADDR1        | IADDR1        | IADDR1        | IADDR1        | IADDR1        | IADDR1        | IADDR1        | IADDR1        | IADDR1        | IADDR1        | IADDR1        | IADDR1        | IADDR1        | IADDR1        |
| W       |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset   | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             |
| Address | Base + 0x0118 | Base + 0x0118 | Base + 0x0118 | Base + 0x0118 | Base + 0x0118 | Base + 0x0118 | Base + 0x0118 | Base + 0x0118 | Base + 0x0118 | Base + 0x0118 | Base + 0x0118 | Base + 0x0118 | Base + 0x0118 | Base + 0x0118 | Base + 0x0118 | Base + 0x0118 |
|         | 16            | 17            | 18            | 19            | 20            | 21            | 22            | 23            | 24            | 25            | 26            | 27            | 28            | 29            | 30            | 31            |
| R       | IADDR1        | IADDR1        | IADDR1        | IADDR1        | IADDR1        | IADDR1        | IADDR1        | IADDR1        | IADDR1        | IADDR1        | IADDR1        | IADDR1        | IADDR1        | IADDR1        | IADDR1        | IADDR1        |
| W       |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset   | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             |
| Address | Base + 0x0118 | Base + 0x0118 | Base + 0x0118 | Base + 0x0118 | Base + 0x0118 | Base + 0x0118 | Base + 0x0118 | Base + 0x0118 | Base + 0x0118 | Base + 0x0118 | Base + 0x0118 | Base + 0x0118 | Base + 0x0118 | Base + 0x0118 | Base + 0x0118 | Base + 0x0118 |

1 'U' signifies a bit that is uninitialized. Refer to the Preface of the book.

Figure 14-16. Descriptor Individual Upper Address Register (IAUR)

## Table 14-19. IAUR Field Descriptions

| Bits   | Name   | Descriptions                                                                                                                                                                                                           |
|--------|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-31   | IADDR1 | The upper 32 bits of the 64-bit hash table used in the address recognition process for receive frames with a unicast address. Bit 31 of IADDR1 contains hash index bit 63. Bit 0 of IADDR1 contains hash index bit 32. |

## 14.3.4.2.15 Descriptor Individual Lower Address (IALR)

The IALR register is written by the user. This register contains the lower 32 bits of the 64-bit individual address hash table used in the address recognition process to check for possible match with the DA field of receive frames with an individual DA. This register is not reset and must be initialized by the user.

<!-- image -->

|         | 0             | 1             | 2             | 3             | 4             | 5             | 6             | 7             | 8             | 9             | 10            | 11            | 12            | 13            | 14            | 15            |
|---------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| R       | IADDR2        | IADDR2        | IADDR2        | IADDR2        | IADDR2        | IADDR2        | IADDR2        | IADDR2        | IADDR2        | IADDR2        | IADDR2        | IADDR2        | IADDR2        | IADDR2        | IADDR2        | IADDR2        |
| W       |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset   | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             |
| Address | Base + 0x011C | Base + 0x011C | Base + 0x011C | Base + 0x011C | Base + 0x011C | Base + 0x011C | Base + 0x011C | Base + 0x011C | Base + 0x011C | Base + 0x011C | Base + 0x011C | Base + 0x011C | Base + 0x011C | Base + 0x011C | Base + 0x011C | Base + 0x011C |
|         | 16            | 17            | 18            | 19            | 20            | 21            | 22            | 23            | 24            | 25            | 26            | 27            | 28            | 29            | 30            | 31            |
| R       | IADDR2        | IADDR2        | IADDR2        | IADDR2        | IADDR2        | IADDR2        | IADDR2        | IADDR2        | IADDR2        | IADDR2        | IADDR2        | IADDR2        | IADDR2        | IADDR2        | IADDR2        | IADDR2        |
| W       |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset   | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             |
| Address | Base + 0x011C | Base + 0x011C | Base + 0x011C | Base + 0x011C | Base + 0x011C | Base + 0x011C | Base + 0x011C | Base + 0x011C | Base + 0x011C | Base + 0x011C | Base + 0x011C | Base + 0x011C | Base + 0x011C | Base + 0x011C | Base + 0x011C | Base + 0x011C |

1 'U' signifies a bit that is uninitialized. Refer to the Preface of the book.

Figure 14-17. Descriptor Individual Lower Address Register (IALR)

## Table 14-20. IALR Field Descriptions

| Bits   | Name   | Description                                                                                                                                                                                                           |
|--------|--------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-31   | IADDR2 | The lower 32 bits of the 64-bit hash table used in the address recognition process for receive frames with a unicast address. Bit 31 of IADDR2 contains hash index bit 31. Bit 0 of IADDR2 contains hash index bit 0. |

## 14.3.4.2.16 Descriptor Group Upper Address (GAUR)

The GAUR is written by the user. This register contains the upper 32 bits of the 64-bit hash table used in the  address  recognition  process  for  receive  frames  with  a  multicast  address.  This  register  must  be initialized by the user.

<!-- image -->

|         | 0             | 1             | 2             | 3             | 4             | 5             | 6             | 7             | 8             | 9             | 10            | 11            | 12            | 13            | 14            | 15            |
|---------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| R       | GADDR1        | GADDR1        | GADDR1        | GADDR1        | GADDR1        | GADDR1        | GADDR1        | GADDR1        | GADDR1        | GADDR1        | GADDR1        | GADDR1        | GADDR1        | GADDR1        | GADDR1        | GADDR1        |
| W       |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset   | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             |
| Address | Base + 0x0120 | Base + 0x0120 | Base + 0x0120 | Base + 0x0120 | Base + 0x0120 | Base + 0x0120 | Base + 0x0120 | Base + 0x0120 | Base + 0x0120 | Base + 0x0120 | Base + 0x0120 | Base + 0x0120 | Base + 0x0120 | Base + 0x0120 | Base + 0x0120 | Base + 0x0120 |
|         | 16            | 17            | 18            | 19            | 20            | 21            | 22            | 23            | 24            | 25            | 26            | 27            | 28            | 29            | 30            | 31            |
| R       | GADDR1        | GADDR1        | GADDR1        | GADDR1        | GADDR1        | GADDR1        | GADDR1        | GADDR1        | GADDR1        | GADDR1        | GADDR1        | GADDR1        | GADDR1        | GADDR1        | GADDR1        | GADDR1        |
| W       |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset   | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             |
| Address | Base + 0x0120 | Base + 0x0120 | Base + 0x0120 | Base + 0x0120 | Base + 0x0120 | Base + 0x0120 | Base + 0x0120 | Base + 0x0120 | Base + 0x0120 | Base + 0x0120 | Base + 0x0120 | Base + 0x0120 | Base + 0x0120 | Base + 0x0120 | Base + 0x0120 | Base + 0x0120 |

1 'U' signifies a bit that is uninitialized. Refer to the Preface of the book.

Figure 14-18. Descriptor Group Upper Address Register (GAUR)

Table 14-21. GAUR Field Descriptions

| Bits   | Name   | Description                                                                                                                                                                                                                                          |
|--------|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-31   | GADDR1 | The GADDR1register contains the upper 32 bits of the 64-bit hash table used in the address recognition process for receive frames with a multicast address. Bit 31 of GADDR1 contains hash index bit 63. Bit 0 of GADDR1 contains hash index bit 32. |

## 14.3.4.2.17 Descriptor Group Lower Address (GALR)

The GALR register is written by the user. This register contains the lower 32 bits of the 64-bit hash table used in the address recognition process for receive frames with a multicast address. This register must be initialized by the user.

<!-- image -->

|         | 0             | 1             | 2             | 3             | 4             | 5             | 6             | 7             | 8             | 9             | 10            | 11            | 12            | 13            | 14            | 15            |
|---------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| R       | GADDR2        | GADDR2        | GADDR2        | GADDR2        | GADDR2        | GADDR2        | GADDR2        | GADDR2        | GADDR2        | GADDR2        | GADDR2        | GADDR2        | GADDR2        | GADDR2        | GADDR2        | GADDR2        |
| W       |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset   | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             |
| Address | Base + 0x0124 | Base + 0x0124 | Base + 0x0124 | Base + 0x0124 | Base + 0x0124 | Base + 0x0124 | Base + 0x0124 | Base + 0x0124 | Base + 0x0124 | Base + 0x0124 | Base + 0x0124 | Base + 0x0124 | Base + 0x0124 | Base + 0x0124 | Base + 0x0124 | Base + 0x0124 |
|         | 16            | 17            | 18            | 19            | 20            | 21            | 22            | 23            | 24            | 25            | 26            | 27            | 28            | 29            | 30            | 31            |
| R       | GADDR2        | GADDR2        | GADDR2        | GADDR2        | GADDR2        | GADDR2        | GADDR2        | GADDR2        | GADDR2        | GADDR2        | GADDR2        | GADDR2        | GADDR2        | GADDR2        | GADDR2        | GADDR2        |
| W       |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset   | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             |
| Address | Base + 0x0124 | Base + 0x0124 | Base + 0x0124 | Base + 0x0124 | Base + 0x0124 | Base + 0x0124 | Base + 0x0124 | Base + 0x0124 | Base + 0x0124 | Base + 0x0124 | Base + 0x0124 | Base + 0x0124 | Base + 0x0124 | Base + 0x0124 | Base + 0x0124 | Base + 0x0124 |

1 'U' signifies a bit that is uninitialized. Refer to the Preface of the book.

Figure 14-19. Descriptor Group Lower Address Register (GALR)

## Table 14-22. GALR Field Descriptions

| Bits   | Name   | Description                                                                                                                                                                                                                                         |
|--------|--------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-31   | GADDR2 | The GADDR2register contains the lower 32 bits of the 64-bit hash table used in the address recognition process for receive frames with a multicast address. Bit 31 of GADDR2 contains hash index bit 31. Bit 0 of GADDR2 contains hash index bit 0. |

## 14.3.4.2.18 FIFO Transmit FIFO Watermark Register (TFWR)

The TFWR is a 32-bit read/write register with one 2-bit field programmed by the user to control the amount of data required in the transmit FIFO before transmission of a frame can begin. This allows the user to minimize transmit latency (TFWR = 0x) or allow for larger bus access latency (TFWR = 11) due to contention for the system bus. Setting the watermark to a high value will minimize the risk of transmit FIFO underrun due to contention for the system bus. The byte counts associated with the TFWR field may need to be modified to match a given system requirement (worst case bus access latency by the transmit data DMA channel).

Figure 14-20. FIFO Transmit FIFO Watermark Register (TFWR)

<!-- image -->

|         | 0             | 1             | 2             | 3             | 4             | 5             | 6             | 7             | 8             | 9             | 10            | 11            | 12            | 13            | 14            | 15            |
|---------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| R       | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| W       |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset   | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Address | Base + 0x0144 | Base + 0x0144 | Base + 0x0144 | Base + 0x0144 | Base + 0x0144 | Base + 0x0144 | Base + 0x0144 | Base + 0x0144 | Base + 0x0144 | Base + 0x0144 | Base + 0x0144 | Base + 0x0144 | Base + 0x0144 | Base + 0x0144 | Base + 0x0144 | Base + 0x0144 |
|         | 16            | 17            | 18            | 19            | 20            | 21            | 22            | 23            | 24            | 25            | 26            | 27            | 28            | 29            | 30            | 31            |
| R       | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | X_WMRK        | X_WMRK        |
| W       |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset   | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Address | Base + 0x0144 | Base + 0x0144 | Base + 0x0144 | Base + 0x0144 | Base + 0x0144 | Base + 0x0144 | Base + 0x0144 | Base + 0x0144 | Base + 0x0144 | Base + 0x0144 | Base + 0x0144 | Base + 0x0144 | Base + 0x0144 | Base + 0x0144 | Base + 0x0144 | Base + 0x0144 |

## Table 14-23. TFWR Field Descriptions

| Bits   | Name   | Descriptions                                                                                                                                 |
|--------|--------|----------------------------------------------------------------------------------------------------------------------------------------------|
| 0-29   | -      | Reserved, should be cleared.                                                                                                                 |
| 30-31  | X_WMRK | Number of bytes written to transmit FIFO before transmission of a frame begins 0x 64 bytes written 10 128 bytes written 11 192 bytes written |

## 14.3.4.3 FIFO Receive Bound Register (FRBR)

The FRBR is a 32-bit register with one 8-bit field that the user can read to determine the upper address bound of the FIFO RAM. Drivers can use this value, along with the FRSR register,to appropriately divide the available FIFO RAM between the transmit and receive data paths.

Figure 14-21. FIFO Receive Bound Register (FRBR)

<!-- image -->

|         | 0             | 1             | 2             | 3             | 4             | 5             | 6             | 7             | 8             | 9             | 10            | 11            | 12            | 13            | 14            | 15            |
|---------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| R       | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| W       |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset   | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Address | Base + 0x014C | Base + 0x014C | Base + 0x014C | Base + 0x014C | Base + 0x014C | Base + 0x014C | Base + 0x014C | Base + 0x014C | Base + 0x014C | Base + 0x014C | Base + 0x014C | Base + 0x014C | Base + 0x014C | Base + 0x014C | Base + 0x014C | Base + 0x014C |
|         | 16            | 17            | 18            | 19            | 20            | 21            | 22            | 23            | 24            | 25            | 26            | 27            | 28            | 29            | 30            | 31            |
| R       | 0             | 0             | 0             | 0             | 0             | 0             | R_BOUND       | R_BOUND       | R_BOUND       | R_BOUND       | R_BOUND       | R_BOUND       | R_BOUND       | R_BOUND       | 0             | 0             |
| W       |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset   | 0             | 0             | 0             | 0             | 0             | 1             | 1             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Address | Base + 0x014C | Base + 0x014C | Base + 0x014C | Base + 0x014C | Base + 0x014C | Base + 0x014C | Base + 0x014C | Base + 0x014C | Base + 0x014C | Base + 0x014C | Base + 0x014C | Base + 0x014C | Base + 0x014C | Base + 0x014C | Base + 0x014C | Base + 0x014C |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## Table 14-24. FRBR Field Descriptions

| Bits   | Name    | Descriptions                                             |
|--------|---------|----------------------------------------------------------|
| 0-21   | -       | Reserved, read as 0 (except bit 10, which is read as 1). |
| 22-29  | R_BOUND | Read-only. Highest valid FIFO RAM address.               |
| 30-31  | -       | Reserved, should be cleared.                             |

## 14.3.4.3.1 FIFO Receive Start Register (FRSR)

The FRSR is a 32-bit register with one 8-bit field programmed by the user to indicate the starting address of the receive FIFO. FRSR marks the boundary between the transmit and receive FIFOs. The transmit FIFO uses addresses from the start of the FIFO to the location four bytes before the address programmed into the FRSR. The receive FIFO uses addresses from FRSR to FRBR inclusive.

The FRSR register is initialized by hardware at reset. FRSR only needs to be written to change the default value.

Figure 14-22. FIFO Receive Start Register (FRSR)

<!-- image -->

|         | 0             | 1             | 2             | 3             | 4             | 5             | 6             | 7             | 8             | 9             | 10            | 11            | 12            | 13            | 14            | 15            |
|---------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| R       | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| W       |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset   | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Address | Base + 0x0150 | Base + 0x0150 | Base + 0x0150 | Base + 0x0150 | Base + 0x0150 | Base + 0x0150 | Base + 0x0150 | Base + 0x0150 | Base + 0x0150 | Base + 0x0150 | Base + 0x0150 | Base + 0x0150 | Base + 0x0150 | Base + 0x0150 | Base + 0x0150 | Base + 0x0150 |
|         | 16            | 17            | 18            | 19            | 20            | 21            | 22            | 23            | 24            | 25            | 26            | 27            | 28            | 29            | 30            | 31            |
| R       | 0             | 0             | 0             | 0             | 0             | 0             | R_FSTART      | R_FSTART      | R_FSTART      | R_FSTART      | R_FSTART      | R_FSTART      | R_FSTART      | R_FSTART      | 0             | 0             |
| W       |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset   | 0             | 0             | 0             | 0             | 0             | 1             | 0             | 1             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Address | Base + 0x0150 | Base + 0x0150 | Base + 0x0150 | Base + 0x0150 | Base + 0x0150 | Base + 0x0150 | Base + 0x0150 | Base + 0x0150 | Base + 0x0150 | Base + 0x0150 | Base + 0x0150 | Base + 0x0150 | Base + 0x0150 | Base + 0x0150 | Base + 0x0150 | Base + 0x0150 |

## Table 14-25. FRSR Field Descriptions

| Bits   | Name     | Descriptions                                                                                  |
|--------|----------|-----------------------------------------------------------------------------------------------|
| 0-21   | -        | Reserved, read as 0 (except bit 10, which is read as 1).                                      |
| 22-29  | R_FSTART | Address of first receive FIFO location. Acts as delimiter between receive and transmit FIFOs. |
| 30-31  | -        | Reserved, read as 0.                                                                          |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## 14.3.4.3.2 Receive Descriptor Ring Start (ERDSR)

The ERDSR is written by the user. It provides a pointer to the start of the circular receive buffer descriptor queue in external memory. This pointer must be 32-bit aligned; however, it is recommended it be made 128-bit aligned (evenly divisible by 16).

This register is not reset and must be initialized by the user prior to operation.

<!-- image -->

Figure 14-23. Receive Descriptor Ring Start Register (ERDSR)

## Table 14-26. ERDSR Field Descriptions

| Bits   | Name        | Descriptions                                         |
|--------|-------------|------------------------------------------------------|
| 0-29   | R_DES_START | Pointer to start of receive buffer descriptor queue. |
| 30-31  | -           | Reserved, should be cleared.                         |

## 14.3.4.3.3 Transmit Buffer Descriptor Ring Start (ETDSR)

The ETDSR is written by the user. It provides a pointer to the start of the circular transmit buffer descriptor queue in external memory. This pointer must be 32-bit aligned; however, it is recommended it be made 128-bit aligned (evenly divisible by 16). Bits 30 and 31 should be written to 0 by the user. Non-zero values in these two bit positions are ignored by the hardware.

This register is not reset and must be initialized by the user prior to operation.

<!-- image -->

Figure 14-24. Transmit Buffer Descriptor Ring Start Register (ETDSR)

Table 14-27. ETDSR Field Descriptions

| Bits   | Name        | Descriptions                                          |
|--------|-------------|-------------------------------------------------------|
| 0-29   | X_DES_START | Pointer to start of transmit buffer descriptor queue. |
| 30-31  | -           | Reserved, should be cleared.                          |

## 14.3.4.3.4 Receive Buffer Size Register (EMRBR)

The EMRBR is a 32-bit register with one 7-bit field programmed by the user. The EMRBR register dictates the maximum size of all receive buffers. Note that because receive frames will be truncated at 2K-1 bytes, only bits 21-27 are used. This value should take into consideration that the receive CRC is always written into  the  last  receive  buffer.  To  allow  one  maximum  size  frame  per  buffer,  EMRBR  must  be  set  to RCR[MAX\_FL] or larger. The EMRBR must be evenly divisible by 16. To insure this, bits 28-31 are forced low. To minimize bus utilization (descriptor fetches) it is recommended that EMRBR be greater than or equal to 256 bytes.

The EMRBR register does not reset, and must be initialized by the user.

<!-- image -->

|         | 0             | 1             | 2             | 3             | 4             | 5             | 6             | 7             | 8             | 9             | 10            | 11            | 12            | 13            | 14            | 15            |
|---------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| R       | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| W       |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset   | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             |
| Address | Base + 0x0188 | Base + 0x0188 | Base + 0x0188 | Base + 0x0188 | Base + 0x0188 | Base + 0x0188 | Base + 0x0188 | Base + 0x0188 | Base + 0x0188 | Base + 0x0188 | Base + 0x0188 | Base + 0x0188 | Base + 0x0188 | Base + 0x0188 | Base + 0x0188 | Base + 0x0188 |
|         | 16            | 17            | 18            | 19            | 20            | 21            | 22            | 23            | 24            | 25            | 26            | 27            | 28            | 29            | 30            | 31            |
| R       | 0             | 0             | 0             | 0             | 0             |               |               | R_BUF_SIZE    | R_BUF_SIZE    | R_BUF_SIZE    | R_BUF_SIZE    |               | 0             | 0             | 0             | 0             |
| W       |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset   | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             | U             |
| Address | Base + 0x0188 | Base + 0x0188 | Base + 0x0188 | Base + 0x0188 | Base + 0x0188 | Base + 0x0188 | Base + 0x0188 | Base + 0x0188 | Base + 0x0188 | Base + 0x0188 | Base + 0x0188 | Base + 0x0188 | Base + 0x0188 | Base + 0x0188 | Base + 0x0188 | Base + 0x0188 |

1 'U' signifies a bit that is uninitialized. Refer to the Preface of the book.

Figure 14-25. Receive Buffer Size Register (EMRBR)

Table 14-28. EMRBR Field Descriptions

| Bits   | Name       | Descriptions                                            |
|--------|------------|---------------------------------------------------------|
| 0-20   | -          | Reserved, should be written to 0 by the host processor. |
| 21-27  | R_BUF_SIZE | Receive buffer size.                                    |
| 28-31  | -          | Reserved, should be written to 0 by the host processor. |

## 14.4 Functional Description

This section describes the operation of the FEC, beginning with the hardware and software initialization sequence, then the software (Ethernet driver) interface for transmitting and receiving frames.

Following the software initialization and operation sections are sections providing a detailed description of the functions of the FEC.

## 14.4.1 Initialization Sequence

This section describes which registers are reset due to hardware reset, which are reset by the FEC RISC, and what locations the user must initialize prior to enabling the FEC.

## 14.4.1.1 Hardware Controlled Initialization

In the FEC, registers and control logic that generate interrupts are reset by hardware. A hardware reset deasserts output signals and resets general configuration bits.

Other registers reset when the ECR[ETHER\_EN] bit is cleared. ECR[ETHER\_EN] is deasserted by a hard reset  or  may  be  deasserted  by  software  to  halt  operation.  By  deasserting  ECR[ETHER\_EN],  the configuration control registers such as the TCR and RCR will not be reset, but the entire data path will be reset.

Table 14-29. ECR[ETHER\_EN] De-Assertion Effect on FEC

| Register/Machine            | Reset Value                                |
|-----------------------------|--------------------------------------------|
| XMIT block                  | Transmission is aborted (bad CRC appended) |
| RECV block                  | Receive activity is aborted                |
| DMA block                   | All DMA activity is terminated             |
| RDAR                        | Cleared                                    |
| TDAR                        | Cleared                                    |
| Descriptor Controller block | Halt operation                             |

## 14.4.2 User Initialization (Prior to Asserting ECR[ETHER\_EN])

The user needs to initialize portions of the FEC prior to setting the ECR[ETHER\_EN] bit. The exact values will depend on the particular application. The sequence is not important.

Ethernet MAC registers requiring initialization are defined in Table 14-30.

Table 14-30. User Initialization (Before ECR[ETHER\_EN])

| Description                                            |
|--------------------------------------------------------|
| Initialize EIMR                                        |
| Clear EIR (write 0xFFFF_FFFF)                          |
| TFWR (optional)                                        |
| IALR / IAUR                                            |
| GAUR / GALR                                            |
| PALR / PAUR (only needed for full duplex flow control) |
| OPD (only needed for full duplex flow control)         |
| RCR                                                    |
| TCR                                                    |
| MSCR (optional)                                        |
| Clear MIB_RAM (locations Base + 0x0200 - 0x02FC)       |

FEC FIFO/DMA registers that require initialization are defined in Table 14-31.

Table 14-31. FEC User Initialization (Before ECR[ETHER\_EN])

| Description                                 |
|---------------------------------------------|
| Initialize FRSR (optional)                  |
| Initialize EMRBR                            |
| Initialize ERDSR                            |
| Initialize ETDSR                            |
| Initialize (Empty) Transmit Descriptor ring |
| Initialize (Empty) Receive Descriptor ring  |

## 14.4.3 Microcontroller Initialization

In the FEC, the descriptor control RISC initializes some registers after ECR[ETHER\_EN] is asserted. After the microcontroller initialization sequence is complete, the hardware is ready for operation.

Table 14-32 shows microcontroller initialization operations.

Table 14-32. Microcontroller Initialization

| Description                           |
|---------------------------------------|
| Initialize BackOff Random Number Seed |
| Activate Receiver                     |
| Activate Transmitter                  |
| Clear Transmit FIFO                   |
| Clear Receive FIFO                    |
| Initialize Transmit Ring Pointer      |
| Initialize Receive Ring Pointer       |
| Initialize FIFO Count Registers       |

## 14.4.4 User Initialization (After Asserting ECR[ETHER\_EN])

After asserting ECR[ETHER\_EN], the user can set up the buffer/frame descriptors and write to the TDAR and RDAR. Refer to Section 14.5, 'Buffer Descriptors' for more details.

## 14.4.5 Network Interface Options

The FEC supports both an MII interface for 10/100 Mbps Ethernet and a 7-wire serial interface for 10 Mbps  Ethernet. The interface mode  is selected by the RCR[MII\_MODE]  bit.  In  MII  mode (RCR[MII\_MODE] = 1), there are 18 signals defined by the IEEE ® 802.3 standard and supported by the EMAC. These signals are shown in Table 14-33 below.

Table 14-33. MII Mode

| Signal Description   | EMAC Signal   |
|----------------------|---------------|
| Transmit Clock       | TX_CLK        |
| Transmit Enable      | TX_EN         |
| Transmit Data        | TXD[3:0]      |
| Transmit Error       | TX_ER         |
| Collision            | COL           |
| Carrier Sense        | CRS           |
| Receive Clock        | RX_CLK        |
| Receive Data Valid   | RX_DV         |
| Receive Data         | RXD[3:0]      |
| Receive Error        | RX_ER         |

Table 14-33. MII Mode (continued)

| Signal Description           | EMAC Signal   |
|------------------------------|---------------|
| Management Data Clock        | MDC           |
| Management Data Input/Output | MDIO          |

The 7-wire serial mode interface (RCR[MII\_MODE] = 0) operates in what is generally referred to as the 'AMD' mode. 7-wire mode connections to the external transceiver are shown in Table 14-34.

Table 14-34. 7-Wire Mode Configuration

| Signal Description   | FEC Signal   |
|----------------------|--------------|
| Transmit Clock       | TX_CLK       |
| Transmit Enable      | TX_EN        |
| Transmit Data        | TXD0         |
| Collision            | COL          |
| Receive Clock        | RX_CLK       |
| Receive Data Valid   | RX_DV        |
| Receive Data         | RXD0         |

## 14.4.6 FEC Frame Transmission

The  Ethernet  transmitter  is  designed  to  work  with  almost  no  intervention  from  software.  Once ECR[ETHER\_EN] is asserted and data appears in the transmit FIFO, the Ethernet MAC is able to transmit onto the network.

When the transmit FIFO fills to the watermark (defined by the TFWR), the MAC transmit logic will assert TX\_EN and start transmitting the preamble (PA) sequence, the start frame delimiter (SFD), and then the frame information from the FIFO. However, the controller defers the transmission if the network is busy (CRS  asserts).  Before  transmitting,  the  controller  waits  for  carrier  sense  to  become  inactive,  then determines if carrier sense stays inactive for 60 bit times. If so, the transmission begins after waiting an additional 36 bit times (96 bit times after carrier sense originally became inactive). See Section 14.4.14.1, 'Transmission Errors' for more details.

If a collision occurs during transmission of the frame (half duplex mode), the Ethernet controller follows the specified backoff procedures and attempts to retransmit the frame until the retry limit is reached. The transmit FIFO stores at least the first 64 bytes of the transmit frame, so that they do not have to be retrieved from system memory in case of a collision. This improves bus utilization and latency in case immediate retransmission is necessary.

When all the frame data has been transmitted, the FCS (frame check sequence or 32-bit cyclic redundancy check, CRC) bytes are appended if the TC bit is set in the transmit frame control word. If the ABC bit is set in the transmit frame control word, a bad CRC will be appended to the frame data regardless of the TC bit  value.  Following  the  transmission  of  the  CRC,  the  Ethernet  controller  writes  the  frame  status information to the MIB block. Short frames are automatically padded by the transmit logic (if the TC bit in the transmit buffer descriptor for the end of frame buffer = 1).

Both buffer (TXB) and frame (TFINT) interrupts may be generated as determined by the settings in the EIMR.

The transmit error interrupts are HBERR, BABT, LATE\_COL, COL\_RETRY\_LIM, and XFIFO\_UN. If the transmit frame length exceeds MAX\_FL bytes, the BABT interrupt will be asserted but the entire frame will be transmitted (no truncation).

To pause transmission, set the GTS (graceful transmit stop) bit in the TCR register. When the TCR[GTS] is set, the FEC transmitter stops immediately if transmission is not in progress; otherwise, it continues transmission until the current frame either finishes or terminates with a collision. After the transmitter has stopped, the GRA (graceful stop complete) interrupt is asserted. If TCR[GTS] is cleared, the FEC resumes transmission with the next frame.

The Ethernet controller transmits bytes least significant bit first.

## 14.4.7 FEC Frame Reception

The FEC receiver is designed to work with almost no intervention from the host and can perform address recognition, CRC checking, short frame checking, and maximum frame length checking.

When the  driver  enables  the  FEC  receiver  by  asserting  ECR[ETHER\_EN],  it  will  immediately  start processing receive frames. When RXDV asserts, the receiver will first check for a valid PA/SFD header. If the PA/SFD is valid, it will be stripped and the frame will be processed by the receiver. If a valid PA/SFD is not found, the frame will be ignored.

In serial mode, the first 16 bit times of RXD0 following assertion of RXDV are ignored. Following the first 16 bit times the data sequence is checked for alternating 1/0s. If a 11 or 00 data sequence is detected during bit times 17 to 21, the remainder of the frame is ignored. After bit time 21, the data sequence is monitored for a valid SFD (11). If a 00 is detected, the frame is rejected. When a 11 is detected, the PA/SFD sequence is complete.

In MII mode, the receiver checks for at least one byte matching the SFD. Zero or more PA bytes may occur, but if a 00 bit sequence is detected prior to the SFD byte, the frame is ignored.

After the first 6 bytes of the frame have been received, the FEC performs address recognition on the frame.

Once a collision window (64 bytes) of data has been received and if address recognition has not rejected the frame, the receive FIFO is signalled that the frame is 'accepted' and may be passed on to the DMA. If the frame is a runt (due to collision) or is rejected by address recognition, the receive FIFO is notified to 'reject' the frame. Thus, no collision fragments are presented to the user except late collisions, which indicate serious LAN problems.

During reception, the Ethernet controller checks for various error conditions and once the entire frame is written into the FIFO, a 32-bit frame status word is written into the FIFO. This status word contains the M, BC, MC, LG, NO, CR, OV and TR status bits, and the frame length. See Section 14.4.14.2, 'Reception Errors' for more details.

Receive buffer (RXB) and frame interrupts (RFINT) may be generated if enabled by the EIMR register. A receive error interrupt is babbling receiver error (BABR). Receive frames are not truncated if they exceed the max frame length (MAX\_FL); however, the BABR interrupt will occur and the LG bit in the receive buffer descriptor (RxBD) will be set. See Section 14.5.2, 'Ethernet Receive Buffer Descriptor (RxBD)' for more details.

When the receive frame is complete, the FEC sets the L-bit in the RxBD, writes the other frame status bits into the RxBD, and clears the E-bit. The Ethernet controller next generates a maskable interrupt (RFINT bit in EIR, maskable by RFIEN bit in EIMR), indicating that a frame has been received and is in memory. The Ethernet controller then waits for a new frame.

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

The Ethernet controller receives serial data LSB first.

## 14.4.8 Ethernet Address Recognition

The FEC filters the received frames based on the type of destination address (DA) - individual (unicast), group (multicast), or broadcast (all-ones group address). The difference between an individual address and a  group address is determined by the I/G bit in the destination address field. A flowchart for address recognition on received frames is illustrated in the figures below.

Address recognition is accomplished through the use of the receive block and microcode running on the microcontroller. The flowchart shown in Figure 14-26 illustrates the address recognition decisions made by the receive block, while Figure 14-27 illustrates the decisions made by the microcontroller.

If the DA is a broadcast address and broadcast reject (RCR[BC\_REJ]) is deasserted, then the frame will be accepted unconditionally, as shown in Figure 14-26. Otherwise, if the DA is not a broadcast address, then the microcontroller runs the address recognition subroutine, as shown in Figure 14-27.

If the DA is a group (multicast) address and flow control is disabled, then the microcontroller will perform a group hash table lookup using the 64-entry hash table programmed in GAUR and GALR. If a hash match occurs, the receiver accepts the frame.

If flow control is enabled, the microcontroller will do an exact address match check between the DA and the designated PAUSE DA (01:80:C2:00:00:01). If the receive block determines that the received frame is a valid PAUSE frame, then the frame will be rejected. Note the receiver will detect a PAUSE frame with the DA field set to either the designated PAUSE DA or the unicast physical address.

If  the  DA  is  the  individual  (unicast)  address,  the  microcontroller  performs  an  individual  exact  match comparison between the DA and 48-bit physical address that the user programs in the PALR and PAUR registers. If an exact match occurs, the frame is accepted; otherwise, the microcontroller does an individual hash table lookup using the 64-entry hash table programmed in registers, IAUR and IALR. In the case of an individual hash match, the frame is accepted. Again, the receiver will accept or reject the frame based on PAUSE frame detection, shown in Figure 14-26.

If  neither  a  hash  match  (group or individual), nor an exact match (group or individual) occur, then if promiscuous mode is enabled (RCR[PROM] = 1), then the frame will be accepted and the MISS bit in the receive buffer descriptor is set; otherwise, the frame will be rejected.

Similarly, if the DA is a broadcast address, broadcast reject (RCR[BC\_REJ]) is asserted, and promiscuous mode is enabled, then the frame will be accepted and the MISS bit in the receive buffer descriptor is set; otherwise, the frame will be rejected.

In general, when a frame is rejected, it is flushed from the FIFO.

<!-- image -->

## NOTES:

BC\_REJ - field in RCR register (BroadCast REJect) PROM - field in RCR register (PROMiscous mode)

Pause Frame - valid Pause frame received

Figure 14-26. Ethernet Address Recognition-Receive Block Decisions

## NOTES:

<!-- image -->

FCE - field in RCR register (Flow Control Enable)

I/G - Individual/Group bit in Destination Address (least significant bit in first byte received in MAC frame)

Figure 14-27. Ethernet Address Recognition-Microcode Decisions

## 14.4.9 Hash Algorithm

The hash table algorithm used in the group and individual hash filtering operates as follows. The 48-bit destination address is mapped into one of 64 bits, which are represented by 64 bits stored in GAUR, GALR (group address hash match) or IAUR, IALR (individual address hash match). This mapping is performed by  passing  the  48-bit  address  through  the  on-chip  32-bit  CRC  generator  and  selecting  the  6  most significant bits of the CRC-encoded result to generate a number between 0 and 63. The MSB of the CRC result selects GAUR (MSB = 1) or GALR (MSB = 0). The least significant 5 bits of the hash result select the bit within the selected register. If the CRC generator selects a bit that is set in the hash table, the frame is accepted; otherwise, it is rejected.

For example, if eight group addresses are stored in the hash table and random group addresses are received, the hash table prevents roughly 56/64 (or 87.5%) of the group address frames from reaching memory. Those that do reach memory must be further filtered by the processor to determine if they truly contain one of the eight desired addresses.

The effectiveness of the hash table declines as the number of addresses increases.

The hash table registers must be initialized by the user. The CRC32 polynomial to use in computing the hash is:

<!-- formula-not-decoded -->

A table of example Destination Addresses and corresponding hash values is included below for reference.

Table 14-35. Destination Address to 6-Bit Hash

| 48-bit DA         | 6-bit Hash (in hex)   |   Hash Decimal Value |
|-------------------|-----------------------|----------------------|
| 65:ff:ff:ff:ff:ff | 0x0                   |                    0 |
| 55:ff:ff:ff:ff:ff | 0x1                   |                    1 |
| 15:ff:ff:ff:ff:ff | 0x2                   |                    2 |
| 35:ff:ff:ff:ff:ff | 0x3                   |                    3 |
| B5:ff:ff:ff:ff:ff | 0x4                   |                    4 |
| 95:ff:ff:ff:ff:ff | 0x5                   |                    5 |
| D5:ff:ff:ff:ff:ff | 0x6                   |                    6 |
| F5:ff:ff:ff:ff:ff | 0x7                   |                    7 |
| DB:ff:ff:ff:ff:ff | 0x8                   |                    8 |
| FB:ff:ff:ff:ff:ff | 0x9                   |                    9 |
| BB:ff:ff:ff:ff:ff | 0xA                   |                   10 |
| 8B:ff:ff:ff:ff:ff | 0xB                   |                   11 |
| 0B:ff:ff:ff:ff:ff | 0xC                   |                   12 |
| 3B:ff:ff:ff:ff:ff | 0xD                   |                   13 |
| 7B:ff:ff:ff:ff:ff | 0xE                   |                   14 |
| 5B:ff:ff:ff:ff:ff | 0xF                   |                   15 |
| 27:ff:ff:ff:ff:ff | 0x10                  |                   16 |
| 07:ff:ff:ff:ff:ff | 0x11                  |                   17 |
| 57:ff:ff:ff:ff:ff | 0x12                  |                   18 |
| 77:ff:ff:ff:ff:ff | 0x13                  |                   19 |
| F7:ff:ff:ff:ff:ff | 0x14                  |                   20 |
| C7:ff:ff:ff:ff:ff | 0x15                  |                   21 |
| 97:ff:ff:ff:ff:ff | 0x16                  |                   22 |
| A7:ff:ff:ff:ff:ff | 0x17                  |                   23 |
| 99:ff:ff:ff:ff:ff | 0x18                  |                   24 |
| B9:ff:ff:ff:ff:ff | 0x19                  |                   25 |
| F9:ff:ff:ff:ff:ff | 0x1A                  |                   26 |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## Table 14-35. Destination Address to 6-Bit Hash (continued)

| 48-bit DA         | 6-bit Hash (in hex)   |   Hash Decimal Value |
|-------------------|-----------------------|----------------------|
| C9:ff:ff:ff:ff:ff | 0x1B                  |                   27 |
| 59:ff:ff:ff:ff:ff | 0x1C                  |                   28 |
| 79:ff:ff:ff:ff:ff | 0x1D                  |                   29 |
| 29:ff:ff:ff:ff:ff | 0x1E                  |                   30 |
| 19:ff:ff:ff:ff:ff | 0x1F                  |                   31 |
| D1:ff:ff:ff:ff:ff | 0x20                  |                   32 |
| F1:ff:ff:ff:ff:ff | 0x21                  |                   33 |
| B1:ff:ff:ff:ff:ff | 0x22                  |                   34 |
| 91:ff:ff:ff:ff:ff | 0x23                  |                   35 |
| 11:ff:ff:ff:ff:ff | 0x24                  |                   36 |
| 31:ff:ff:ff:ff:ff | 0x25                  |                   37 |
| 71:ff:ff:ff:ff:ff | 0x26                  |                   38 |
| 51:ff:ff:ff:ff:ff | 0x27                  |                   39 |
| 7F:ff:ff:ff:ff:ff | 0x28                  |                   40 |
| 4F:ff:ff:ff:ff:ff | 0x29                  |                   41 |
| 1F:ff:ff:ff:ff:ff | 0x2A                  |                   42 |
| 3F:ff:ff:ff:ff:ff | 0x2B                  |                   43 |
| BF:ff:ff:ff:ff:ff | 0x2C                  |                   44 |
| 9F:ff:ff:ff:ff:ff | 0x2D                  |                   45 |
| DF:ff:ff:ff:ff:ff | 0x2E                  |                   46 |
| EF:ff:ff:ff:ff:ff | 0x2F                  |                   47 |
| 93:ff:ff:ff:ff:ff | 0x30                  |                   48 |
| B3:ff:ff:ff:ff:ff | 0x31                  |                   49 |
| F3:ff:ff:ff:ff:ff | 0x32                  |                   50 |
| D3:ff:ff:ff:ff:ff | 0x33                  |                   51 |
| 53:ff:ff:ff:ff:ff | 0x34                  |                   52 |
| 73:ff:ff:ff:ff:ff | 0x35                  |                   53 |
| 23:ff:ff:ff:ff:ff | 0x36                  |                   54 |
| 13:ff:ff:ff:ff:ff | 0x37                  |                   55 |
| 3D:ff:ff:ff:ff:ff | 0x38                  |                   56 |
| 0D:ff:ff:ff:ff:ff | 0x39                  |                   57 |
| 5D:ff:ff:ff:ff:ff | 0x3A                  |                   58 |

Table 14-35. Destination Address to 6-Bit Hash (continued)

| 48-bit DA         | 6-bit Hash (in hex)   |   Hash Decimal Value |
|-------------------|-----------------------|----------------------|
| 7D:ff:ff:ff:ff:ff | 0x3B                  |                   59 |
| FD:ff:ff:ff:ff:ff | 0x3C                  |                   60 |
| DD:ff:ff:ff:ff:ff | 0x3D                  |                   61 |
| 9D:ff:ff:ff:ff:ff | 0x3E                  |                   62 |
| BD:ff:ff:ff:ff:ff | 0x3F                  |                   63 |

## 14.4.10 Full Duplex Flow Control

Full-duplex flow control allows the user to transmit pause frames and to detect received pause frames. Upon detection of a pause frame, MAC data frame transmission stops for a given pause duration.

To enable pause frame detection, the FEC must operate in full-duplex mode (TCR[FDEN] asserted) and flow control enable (RCR[FCE]) must be asserted. The FEC detects a pause frame when the fields of the incoming frame match the pause frame specifications, as shown in the table below. In addition, the receive status associated with the frame should indicate that the frame is valid.

Table 14-36. PAUSE Frame Field Specification

| 48-bit Destination Address   | 0x0180_C200_0001 or Physical Address   |
|------------------------------|----------------------------------------|
| 48-bit Source Address        | Any                                    |
| 16-bit TYPE                  | 0x8808                                 |
| 16-bit OPCODE                | 0x0001                                 |
| 16-bit PAUSE_DUR             | 0x0000 to 0xFFFF                       |

Pause frame detection is performed by the receiver and microcontroller modules. The microcontroller runs an  address  recognition  subroutine  to  detect  the  specified  pause  frame  destination  address,  while  the receiver detects the TYPE and OPCODE pause frame fields. On detection of a pause frame, TCR[GTS] is asserted by the FEC internally. When transmission has paused, the EIR[GRA] interrupt is asserted and the pause  timer  begins  to  increment.  Note  that  the  pause  timer  makes  use  of  the  transmit  backoff  timer hardware, which is used for tracking the appropriate collision backoff time in half-duplex mode. The pause timer increments  once  every  slot  time,  until OPD[PAUSE\_DUR]  slot  times  have  expired.  On OPD[PAUSE\_DUR]  expiration,  TCR[GTS]  is  deasserted  allowing  MAC  data  frame  transmission  to resume. Note that the receive flow control pause (TCR[RFC\_PAUSE]) status bit is asserted while the transmitter is paused due to reception of a pause frame.

To transmit a pause frame, the FEC must operate in full-duplex mode and the user must assert flow control pause  (TCR[TFC\_PAUSE]).  On  assertion  of  transmit  flow  control  pause  (TCR[TFC\_PAUSE]),  the transmitter  asserts  TCR[GTS]  internally.  When  the  transmission  of  data  frames  stops,  the  EIR[GRA] (graceful stop complete) interrupt asserts. Following EIR[GRA] assertion, the pause frame is transmitted. On completion of pause frame transmission, flow control pause (TCR[TFC\_PAUSE]) and TCR[GTS] are deasserted internally.

The user must specify the desired pause duration in the OPD register.

Note that when the transmitter is paused due to receiver/microcontroller pause frame detection, transmit flow control pause (TCR[TFC\_PAUSE]) still may be asserted and will cause the transmission of a single pause frame. In this case, the EIR[GRA] interrupt will not be asserted.

## 14.4.11 Inter-Packet Gap (IPG) Time

The minimum inter-packet gap time for back-to-back transmission is 96 bit times. After completing a transmission or after the backoff algorithm completes, the transmitter waits for carrier sense to be negated before starting its 96 bit time IPG counter. Frame transmission may begin 96 bit times after carrier sense is negated if it stays negated for at least 60 bit times. If carrier sense asserts during the last 36 bit times, it will be ignored and a collision will occur.

The  receiver  receives  back-to-back  frames  with  a  minimum  spacing  of  at  least  28  bit  times.  If  an inter-packet gap between receive frames is less than 28 bit times, the following frame may be discarded by the receiver.

## 14.4.12 Collision Handling

If a collision occurs during frame transmission, the Ethernet controller will continue the transmission for at least 32 bit times, transmitting a JAM pattern consisting of 32 ones. If the collision occurs during the preamble sequence, the JAM pattern will be sent after the end of the preamble sequence.

If a collision occurs within 512 bit times, the retry process is initiated. The transmitter waits a random number of  slot  times.  A  slot  time  is  512  bit  times.  If  a  collision  occurs  after  512  bit  times,  then  no retransmission is performed and the end of frame buffer is closed with a late collision (LC) error indication.

## 14.4.13 Internal and External Loopback

Both internal and external loopback are supported by the Ethernet controller. In loopback mode, both of the FIFOs are used and the FEC actually operates in a full-duplex fashion. Both internal and external loopback are configured using combinations of the LOOP and DRT bits in the RCR register and the FDEN bit in the TCR register.

For both internal and external loopback set FDEN = 1.

For internal loopback set RCR[LOOP] = 1 and RCR[DRT] = 0. TX\_EN and TX\_ER will not assert during internal  loopback.  During  internal  loopback,  the  transmit/receive  data  rate  is  higher  than  in  normal operation because the internal system clock is used by the transmit and receive blocks instead of the clocks from the external transceiver. This will cause an increase in the required system bus bandwidth for transmit and receive data being DMA'd to/from external memory. It may be necessary to pace the frames on the transmit side and/or limit the size of the frames to prevent transmit FIFO underrun and receive FIFO overflow.

For external loopback set RCR[LOOP] = 0, RCR[DRT] = 0 and configure the external transceiver for loopback.

## 14.4.14 Ethernet Error-Handling Procedure

The Ethernet controller reports frame reception and transmission error conditions using the FEC RxBDs, the EIR register, and the MIB block counters.

## 14.4.14.1 Transmission Errors

## 14.4.14.1.1 Transmitter Underrun

If this error occurs, the FEC sends 32 bits that ensure a CRC error and stops transmitting. All remaining buffers for that frame are then flushed and closed. The UN bit is set in the EIR. The FEC will then continue to the next transmit buffer descriptor and begin transmitting the next frame.

The 'UN' interrupt will be asserted if enabled in the EIMR register.

## 14.4.14.1.2 Retransmission Attempts Limit Expired

When this error occurs, the FEC terminates transmission. All remaining buffers for that frame are flushed and closed, and the RL bit is set in the EIR. The FEC will then continue to the next transmit buffer descriptor and begin transmitting the next frame.

The 'RL' interrupt will be asserted if enabled in the EIMR register.

## 14.4.14.1.3 Late Collision

When  a  collision  occurs  after  the  slot  time  (512  bits  starting  at  the  preamble),  the  FEC  terminates transmission. All remaining buffers for that frame are flushed and closed, and the LC bit is set in the EIR register. The FEC will then continue to the next transmit buffer descriptor and begin transmitting the next frame.

The 'LC' interrupt will be asserted if enabled in the EIMR register.

## 14.4.14.1.4 Heartbeat

Some transceivers have a self-test feature called 'heartbeat' or 'signal quality error.' To signify a good self-test, the transceiver indicates a collision to the FEC within 4 microseconds after completion of a frame transmitted by the Ethernet controller. This indication of a collision does not imply a real collision error on the network, but is rather an indication that the transceiver still seems to be functioning properly. This is called the heartbeat condition.

If the HBC bit is set in the TCR register and the heartbeat condition is not detected by the FEC after a frame transmission, then a heartbeat error occurs. When this error occurs, the FEC closes the buffer, sets the HB bit in the EIR register, and generates the HBERR interrupt if it is enabled.

## 14.4.14.2 Reception Errors

## 14.4.14.2.1 Overrun Error

If the receive block has data to put into the receive FIFO and the receive FIFO is full, the FEC sets the OV bit in the RxBD. All subsequent data in the frame will be discarded and subsequent frames may also be discarded until the receive FIFO is serviced by the DMA and space is made available. At this point the receive frame/status word is written into the FIFO with the OV bit set. This frame must be discarded by the driver.

## 14.4.14.2.2 Non-Octet Error (Dribbling Bits)

The Ethernet controller handles up to seven dribbling bits when the receive frame terminates past an non-octet aligned boundary. Dribbling bits are not used in the CRC calculation. If there is a CRC error,

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

then the frame non-octet aligned (NO) error is reported in the RxBD. If there is no CRC error, then no error is reported.

## 14.4.14.2.3 CRC Error

When a CRC error occurs with no dribble bits, the FEC closes the buffer and sets the CR bit in the RxBD. CRC checking cannot be disabled, but the CRC error can be ignored if checking is not required.

## 14.4.14.2.4 Frame Length Violation

When the receive frame length exceeds MAX\_FL bytes the BABR interrupt will be generated, and the LG bit in the end of frame RxBD will be set. The frame is not truncated unless the frame length exceeds 2047 bytes).

## 14.4.14.2.5 Truncation

When the receive frame length exceeds 2047 bytes the frame is truncated, and the TR bit is set in the RxBD.

## 14.5 Buffer Descriptors

This section provides a description of the operation of the driver/DMA via the buffer descriptors. It is followed by a detailed description of the receive and transmit descriptor fields.

## 14.5.1 Driver/DMA Operation with Buffer Descriptors

The data for the FEC frames must reside in memory external to the FEC. The data for a frame is placed in one or more buffers. Associated with each buffer is a buffer descriptor (BD) which contains a starting address (pointer),  data  length,  and  status/control  information  (which  contains  the  current  state  for  the buffer). To permit maximum user flexibility, the BDs are also located in external memory and are read in by the FEC DMA engine.

Software 'produces' buffers by allocating/initializing memory and initializing buffer descriptors. Setting the RxBD[E] or TxBD[R] bit 'produces' the buffer. Software writing to either the TDAR or RDAR tells the  FEC  that  a  buffer  has  been  placed  in  external  memory  for  the  transmit  or  receive  data  traffic, respectively. The hardware reads the BDs and 'consumes' the buffers after they have been produced. After the data DMA is complete and the buffer descriptor status bits have been written by the DMA engine, the RxBD[E] or TxBD[R] bit will be cleared by hardware to signal that the buffer has been 'consumed.' Software may poll the BDs to detect when the buffers have been consumed or may rely on the buffer/frame interrupts. These buffers may then be processed by the driver and returned to the free list.

The ECR[ETHER\_EN] signal operates as a reset to the BD/DMA logic. When ECR[ETHER\_EN] is deasserted the DMA engine BD pointers are reset to point to the starting transmit and receive BDs. The buffer descriptors are not initialized by hardware during reset. At least one transmit and receive buffer descriptor must be initialized by software before the ECR[ETHER\_EN] bit is set.

The buffer descriptors operate as two separate rings. ERDSR defines the starting address for receive BDs and ETDSR defines the starting address for transmit BDs. The last buffer descriptor in each ring is defined by the wrap (W) bit. When set, W indicates that the next descriptor in the ring is at the location pointed to by ERDSR and ETDSR for the receive and transmit rings, respectively. Buffer descriptor rings must start on a 32-bit boundary; however, it is recommended they are made 128-bit aligned.

## 14.5.1.1 Driver/DMA Operation with Transmit BDs

Typically a transmit frame will be divided between multiple buffers. An example is to have an application payload in one buffer, TCP header in a second buffer, IP header in a third buffer, Ethernet/IEEE ® 802.3 header in a fourth buffer. The Ethernet MAC does not prepend the Ethernet header (destination address, source address, length/type fields), so this must be provided by the driver in one of the transmit buffers. The Ethernet MAC can append the Ethernet CRC to the frame. Whether the CRC is appended by the MAC or by the driver is determined by the TC bit in the transmit BD which must be set by the driver.

The driver (TxBD software producer) should set up Tx BDs in such a way that a complete transmit frame is given to the hardware at once. If a transmit frame consists of three buffers, the BDs should be initialized with pointer, length and control (W, L, TC, ABC) and then the TxBD[R] bits should be set = 1 in reverse order (3rd, 2nd, 1st BD) to insure that the complete frame is ready in memory before the DMA begins. If the TxBDs are set up in order, the DMA Controller could DMA the first BD before the 2nd was made available, potentially causing a transmit FIFO underrun.

In the FEC, the DMA is notified by the driver that new transmit frames are available by writing to the TDAR register. When this register is written to (data value is not significant) the FEC RISC will tell the DMA to read the next transmit BD in the ring. Once started, the RISC + DMA will continue to read and interpret transmit BDs in order and DMA the associated buffers, until a transmit BD is encountered with the R bit = 0. At this point the FEC will poll this BD one more time. If the R bit = 0 the second time, then the RISC will stop the transmit descriptor read process until software sets up another transmit frame and writes to TDAR.

When the DMA of each transmit buffer is complete, the DMA writes back to the BD to clear the R bit, indicating that the hardware consumer is finished with the buffer.

## 14.5.1.2 Driver/DMA Operation with Receive BDs

Unlike transmit, the length of the receive frame is unknown by the driver ahead of time. Therefore the driver must set a variable to define the length of all receive buffers. In the FEC, this variable is written to the EMRBR register.

The driver (RxBD software producer) should set up some number of 'empty' buffers for the Ethernet by initializing the address field and the E and W bits of the associated receive BDs. The hardware (receive DMA) will consume these buffers by filling them with data as frames are received and clearing the E bit and writing to the L (1 indicates last buffer in frame) bit, the frame status bits (if L = 1) and the length field.

If a receive frame spans multiple receive buffers, the L bit is only set for the last buffer in the frame. For non-last buffers, the length field in the receive BD will be written by the DMA (at the same time the E bit is cleared) with the default receive buffer length value. For end of frame buffers the receive BD will be written with L = 1 and information written to the status bits (M, BC, MC, LG, NO, CR, OV, TR). Some of the status bits are error indicators which, if set, indicate the receive frame should be discarded and not given to higher layers. The frame status/length information is written into the receive FIFO following the end of the frame (as a single 32-bit word) by the receive logic. The length field for the end of frame buffer will be written with the length of the entire frame, not just the length of the last buffer.

For simplicity the driver may assign the default receive buffer length to be large enough to contain an entire frame, keeping in mind that a malfunction on the network or out of spec implementation could result in giant frames. Frames of 2K (2048) bytes or larger are truncated by the FEC at 2047 bytes so software is guaranteed never to see a receive frame larger than 2047 bytes.

Similar to transmit, the FEC will poll the receive descriptor ring after the driver sets up receive BDs and writes to the RDAR register. As frames are received the FEC will fill receive buffers and update the associated BDs, then read the next BD in the receive descriptor ring. If the FEC reads a receive BD and

finds the E bit = 0, it will poll this BD once more. If the BD = 0 a second time the FEC will stop reading receive BDs until the driver writes to RDAR.

## 14.5.2 Ethernet Receive Buffer Descriptor (RxBD)

In the RxBD, the user initializes the E and W bits in the first word and the pointer in second word. When the buffer has been DMA'd, the Ethernet controller will modify the E, L, M, BC, MC, LG, NO, CR, OV, and TR bits and write the length of the used portion of the buffer in the first word. The M, BC, MC, LG, NO, CR, OV and TR bits in the first word of the buffer descriptor are only modified by the Ethernet controller when the L bit is set.

.

Figure 14-28. Receive Buffer Descriptor (RxBD)

<!-- image -->

|            | 0                                  | 1                                  | 2                                  | 3                                  | 4                                  | 5                                  | 6                                  | 7                                  | 8                                  | 9                                  | 10                                 | 11                                 | 12                                 | 13                                 | 14                                 | 15                                 |
|------------|------------------------------------|------------------------------------|------------------------------------|------------------------------------|------------------------------------|------------------------------------|------------------------------------|------------------------------------|------------------------------------|------------------------------------|------------------------------------|------------------------------------|------------------------------------|------------------------------------|------------------------------------|------------------------------------|
| Offset + 0 | E                                  | RO1                                | W                                  | RO2                                | L                                  | -                                  | -                                  | M                                  | BC                                 | MC                                 | LG                                 | NO                                 | -                                  | CR                                 | OV                                 | TR                                 |
| Offset + 2 | Data Length                        | Data Length                        | Data Length                        | Data Length                        | Data Length                        | Data Length                        | Data Length                        | Data Length                        | Data Length                        | Data Length                        | Data Length                        | Data Length                        | Data Length                        | Data Length                        | Data Length                        | Data Length                        |
| Offset + 4 | Tx Data Buffer Pointer - A [0:15]  | Tx Data Buffer Pointer - A [0:15]  | Tx Data Buffer Pointer - A [0:15]  | Tx Data Buffer Pointer - A [0:15]  | Tx Data Buffer Pointer - A [0:15]  | Tx Data Buffer Pointer - A [0:15]  | Tx Data Buffer Pointer - A [0:15]  | Tx Data Buffer Pointer - A [0:15]  | Tx Data Buffer Pointer - A [0:15]  | Tx Data Buffer Pointer - A [0:15]  | Tx Data Buffer Pointer - A [0:15]  | Tx Data Buffer Pointer - A [0:15]  | Tx Data Buffer Pointer - A [0:15]  | Tx Data Buffer Pointer - A [0:15]  | Tx Data Buffer Pointer - A [0:15]  | Tx Data Buffer Pointer - A [0:15]  |
| Offset + 6 | Tx Data Buffer Pointer - A [16:31] | Tx Data Buffer Pointer - A [16:31] | Tx Data Buffer Pointer - A [16:31] | Tx Data Buffer Pointer - A [16:31] | Tx Data Buffer Pointer - A [16:31] | Tx Data Buffer Pointer - A [16:31] | Tx Data Buffer Pointer - A [16:31] | Tx Data Buffer Pointer - A [16:31] | Tx Data Buffer Pointer - A [16:31] | Tx Data Buffer Pointer - A [16:31] | Tx Data Buffer Pointer - A [16:31] | Tx Data Buffer Pointer - A [16:31] | Tx Data Buffer Pointer - A [16:31] | Tx Data Buffer Pointer - A [16:31] | Tx Data Buffer Pointer - A [16:31] | Tx Data Buffer Pointer - A [16:31] |

Table 14-37. Receive Buffer Descriptor Field Definitions

| Halfword   | Location   | Field Name   | Description                                                                                                                                                                                                                                                                                                                                      |
|------------|------------|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Offset + 0 | Bit 0      | E            | Empty. Written by the FEC (=0) and user (=1). 0 The data buffer associated with this BD has been filled with received data, or data reception has been aborted due to an error condition. The status and length fields have been updated as required. 1 The data buffer associated with this BD is empty, or reception is currently in progress. |
| Offset + 0 | Bit 1      | RO1          | Receive software ownership. This field is reserved for use by software. This read/write bit will not be modified by hardware, nor will its value affect hardware.                                                                                                                                                                                |
| Offset + 0 | Bit 2      | W            | Wrap. Written by user. 0 The next buffer descriptor is found in the consecutive location 1 The next buffer descriptor is found at the location defined in ERDSR.                                                                                                                                                                                 |
| Offset + 0 | Bit 3      | RO2          | Receive software ownership. This field is reserved for use by software. This read/write bit will not be modified by hardware, nor will its value affect hardware.                                                                                                                                                                                |
| Offset + 0 | Bit 4      | L            | Last in frame. Written by the FEC. 0 The buffer is not the last in a frame. 1 The buffer is the last in a frame.                                                                                                                                                                                                                                 |
| Offset + 0 | Bits 5-6   | -            | Reserved.                                                                                                                                                                                                                                                                                                                                        |

Table 14-37. Receive Buffer Descriptor Field Definitions (continued)

| Halfword   | Location    | Field Name   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
|------------|-------------|--------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Offset + 0 | Bit 7       | M            | Miss. Written by the FEC. This bit is set by the FEC for frames that were accepted in promiscuous mode, but were flagged as a 'miss' by the internal address recognition. Thus, while in promiscuous mode, the user can use the M-bit to quickly determine whether the frame was destined to this station. This bit is valid only if the L-bit is set and the PROM bit is set. 0 The frame was received because of an address recognition hit. 1 The frame was received because of promiscuous mode. |
| Offset + 0 | Bit 8       | BC           | Will be set if the DA is broadcast (FF-FF-FF-FF-FF-FF).                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| Offset + 0 | Bit 9       | MC           | Will be set if the DA is multicast and not BC.                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| Offset + 0 | Bit 10      | LG           | Rx frame length violation. Written by the FEC. A frame length greater than RCR[MAX_FL] was recognized. This bit is valid only if the L-bit is set. The receive data is not altered in any way unless the length exceeds 2047 bytes.                                                                                                                                                                                                                                                                  |
| Offset + 0 | Bit 11      | NO           | Receive non-octet aligned frame. Written by the FEC. A frame that contained a number of bits not divisible by 8 was received, and the CRC check that occurred at the preceding byte boundary generated an error. This bit is valid only if the L-bit is set. If this bit is set the CR bit will not be set.                                                                                                                                                                                          |
| Offset + 0 | Bit 12      | -            | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| Offset + 0 | Bit 13      | CR           | Receive CRC error. Written by the FEC. This frame contains a CRCerror and is an integral number of octets in length. This bit is valid only if the L-bit is set.                                                                                                                                                                                                                                                                                                                                     |
| Offset + 0 | Bit 14      | OV           | Overrun. Written by the FEC. Areceive FIFO overrun occurred during frame reception. If this bit is set, the other status bits, M, LG, NO, CR, and CL lose their normal meaning and will be zero. This bit is valid only if the L-bit is set.                                                                                                                                                                                                                                                         |
| Offset + 0 | Bit 15      | TR           | Will be set if the receive frame is truncated (frame length > 2047 bytes). If the TR bit is set the frame should be discarded and the other error bits should be ignored as they may be incorrect.                                                                                                                                                                                                                                                                                                   |
| Offset + 2 | Bits [0:15] | Data Length  | Data length. Written by the FEC. Data length is the number of 8-bit data groups (octets) written by the FECinto this BD's data buffer if L = 0 (the value will be equal to EMRBR), or the length of the frame including CRCif L = 1. It is written by the FEConce as the BD is closed.                                                                                                                                                                                                               |
| 0ffset + 4 | Bits [0:15] | A[0:15]]     | RX data buffer pointer, bits [0:15] 1                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| Offset + 6 | Bits [0:15] | A[16:31]     | RX data buffer pointer, bits [16:31]                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |

1 The receive buffer pointer, which contains the address of the associated data buffer, must always be evenly divisible by 16. The buffer must reside in memory external to the FEC. This value is never modified by the Ethernet controller.

## NOTE

Whenever  the  software  driver  sets  an  E  bit  in  one  or  more  receive descriptors, the driver should follow that with a write to RDAR.

## 14.5.3 Ethernet Transmit Buffer Descriptor (TxBD)

Data is presented to the FEC for transmission by arranging it in buffers referenced by the channel's TxBDs. The Ethernet controller confirms transmission by clearing the ready bit (R bit) when DMA of the buffer is complete. In the TxBD the user initializes the R, W, L, and TC bits and the length (in bytes) in the first word, and the buffer pointer in the second word.

The FEC will set the R bit = 0 in the first word of the BD when the buffer has been DMA'd. Status bits for the buffer/frame are not included in the transmit buffer descriptors. Transmit frame status is indicated via individual interrupt bits (error conditions) and in statistic counters in the MIB block. See Section 14.3.3, 'MIB Block Counters Memory Map' for more details.

.

Figure 14-29. Transmit Buffer Descriptor (TxBD)

<!-- image -->

|            | 0                                  | 1                                  | 2                                  | 3                                  | 4                                  | 5                                  | 6                                  | 7                                  | 8                                  | 9                                  | 10                                 | 11                                 | 12                                 | 13                                 | 14                                 | 15                                 |
|------------|------------------------------------|------------------------------------|------------------------------------|------------------------------------|------------------------------------|------------------------------------|------------------------------------|------------------------------------|------------------------------------|------------------------------------|------------------------------------|------------------------------------|------------------------------------|------------------------------------|------------------------------------|------------------------------------|
| Offset + 0 | R                                  | TO1                                | W                                  | TO2                                | L                                  | TC                                 | ABC                                | -                                  | -                                  | -                                  | -                                  | -                                  | -                                  | -                                  | -                                  | -                                  |
| Offset + 2 | Data Length                        | Data Length                        | Data Length                        | Data Length                        | Data Length                        | Data Length                        | Data Length                        | Data Length                        | Data Length                        | Data Length                        | Data Length                        | Data Length                        | Data Length                        | Data Length                        | Data Length                        | Data Length                        |
| Offset + 4 | Tx Data Buffer Pointer - A [0:15]  | Tx Data Buffer Pointer - A [0:15]  | Tx Data Buffer Pointer - A [0:15]  | Tx Data Buffer Pointer - A [0:15]  | Tx Data Buffer Pointer - A [0:15]  | Tx Data Buffer Pointer - A [0:15]  | Tx Data Buffer Pointer - A [0:15]  | Tx Data Buffer Pointer - A [0:15]  | Tx Data Buffer Pointer - A [0:15]  | Tx Data Buffer Pointer - A [0:15]  | Tx Data Buffer Pointer - A [0:15]  | Tx Data Buffer Pointer - A [0:15]  | Tx Data Buffer Pointer - A [0:15]  | Tx Data Buffer Pointer - A [0:15]  | Tx Data Buffer Pointer - A [0:15]  | Tx Data Buffer Pointer - A [0:15]  |
| Offset + 6 | Tx Data Buffer Pointer - A [16:31] | Tx Data Buffer Pointer - A [16:31] | Tx Data Buffer Pointer - A [16:31] | Tx Data Buffer Pointer - A [16:31] | Tx Data Buffer Pointer - A [16:31] | Tx Data Buffer Pointer - A [16:31] | Tx Data Buffer Pointer - A [16:31] | Tx Data Buffer Pointer - A [16:31] | Tx Data Buffer Pointer - A [16:31] | Tx Data Buffer Pointer - A [16:31] | Tx Data Buffer Pointer - A [16:31] | Tx Data Buffer Pointer - A [16:31] | Tx Data Buffer Pointer - A [16:31] | Tx Data Buffer Pointer - A [16:31] | Tx Data Buffer Pointer - A [16:31] | Tx Data Buffer Pointer - A [16:31] |

Table 14-38. Transmit Buffer Descriptor Field Definitions

| Halfword   | Location   | Field Name   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|------------|------------|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Offset + 0 | Bit 0      | R            | Ready. Written by the FEC and the user. 0 The data buffer associated with this BD is not ready for transmission. The user is free to manipulate this BD or its associated data buffer. The FEC clears this bit after the buffer has been transmitted or after an error condition is encountered. 1 The data buffer, which has been prepared for transmission by the user, has not been transmitted or is currently being transmitted. No fields of this BD may be written by the user once this bit is set. |
| Offset + 0 | Bit 1      | TO1          | Transmit software ownership. This field is reserved for software use. This read/write bit will not be modified by hardware, nor will its value affect hardware.                                                                                                                                                                                                                                                                                                                                             |
| Offset + 0 | Bit 2      | W            | Wrap. Written by user. 0 The next buffer descriptor is found in the consecutive location 1 The next buffer descriptor is found at the location defined in ETDSR.                                                                                                                                                                                                                                                                                                                                            |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 14-38. Transmit Buffer Descriptor Field Definitions (continued)

| Halfword   | Location    | Field Name   | Description                                                                                                                                                                                                             |
|------------|-------------|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Offset + 0 | Bit 3       | TO2          | Transmit software ownership. This field is reserved for use by software. This read/write bit will not be modified by hardware, nor will its value affect hardware.                                                      |
| Offset + 0 | Bit 4       | L            | Last in frame. Written by user. 0 The buffer is not the last in the transmit frame. 1 The buffer is the last in the transmit frame.                                                                                     |
| Offset + 0 | Bit 5       | TC           | Tx CRC. Written by user (only valid if L = 1). 0 End transmission immediately after the last data byte. 1 Transmit the CRC sequence after the last data byte.                                                           |
| Offset + 0 | Bit 6       | ABC          | Append bad CRC. Written by user (only valid if L = 1). 0 No effect 1 Transmit the CRCsequence inverted after the last data byte (regardless of TC value).                                                               |
| Offset + 0 | Bits [7:15] | -            | Reserved.                                                                                                                                                                                                               |
| Offset + 2 | Bits [0:15] | Data Length  | Data length, written by user. Data length is the number of octets the FEC should transmit from this BD's data buffer. It is never modified by the FEC. Bits [0:10] are used by the DMA engine, bits[11:15] are ignored. |
| Offset + 4 | Bits [0:15] | A[0:15]      | Tx data buffer pointer, bits [0:15] 1                                                                                                                                                                                   |
| Offset + 6 | Bits [0:15] | A[16:31]     | Tx data buffer pointer, bits [16:31].                                                                                                                                                                                   |

1 The transmit buffer pointer, which contains the address of the associated data buffer, must always be evenly divisible by 4. The buffer must reside in memory external to the FEC. This value is never modified by the Ethernet controller.

## NOTE

Once the software driver has set up the buffers for a frame, it should set up the corresponding BDs. The last step in setting up the BDs for a transmit frame should be to set the R bit in the first BD for the frame. The driver should follow that with a write to TDAR which will trigger the FEC to poll the next BD in the ring.

## 14.6 Revision History

## Substantive Changes since Rev 3.0

Table 14-2 - changed MDATA to MMFR as well as name of register to MII Management Frame Regsiter.

Changed last sentence of Section 14.3.4.2.6, 'MII Management Frame Register (MMFR),' to read 'Software should software should poll the EIR[MII] bit or use the EIR[MII] bit to generate an interrupt to avoid writing to the MMFR register while frame generation is in progress.'

In Section 14.3.4.3.3, 'Transmit Buffer Descriptor Ring Start (ETDSR),' changed title and first sentence to ETDSR (was ETSDR).

Figure 14-8 - changed DATA to be R/W and not Read-only.

Added 'All accesses to and from the FEC memory map must be via 32-bit accesses. There is no support for accesses other than 32-bit.' to Section 14.3.1, 'Top Level Module Memory Map,' Table 14-2 (as a footnote), and Table 14-3 (as a footnote).

Corrected Offset + 6 range in both transmit and receive buffer descriptor to 16:31. It previously said 0:15.
