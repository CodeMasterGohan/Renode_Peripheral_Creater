### Chatper 22 FlexCAN2 Controller Area Network

## 22.1 Introduction

The MPC5554 MCU contains three controller area network (FlexCAN2) modules; the MPC5553 contains two FlexCAN2 modules. Each FlexCAN2 module is a communication controller implementing the CAN protocol according to CAN Specification version 2.0B and ISO Standard 11898. Each FlexCAN2 module contains a 1024-byte embedded memory, capable of storing 64 message buffers (MBs). The respective functions are described in subsequent sections.

## 22.1.1 Block Diagram

A general block diagram is shown in Figure 22-1, which describes the main submodules implemented in the FlexCAN2 module, including an embedded RAM for up to 64 message buffers.

## FlexCAN2

Figure 22-1. FlexCAN2 Block Diagram

<!-- image -->

## 22.1.2 Overview

The CAN protocol was designed primarily, but not exclusively, to be used as a vehicle serial data bus, meeting  the  specific  requirements  of  this  field:  real-time  processing,  reliable  operation  in  the  EMI environment of a vehicle, cost-effectiveness and required bandwidth. The FlexCAN2 module is a full implementation  of  the  CAN  protocol  specification,  Version  2.0  B,  which  supports  both  standard  and extended message frames. Sixty-four message buffers (MBs) are stored in an embedded 1024-byte RAM dedicated to the FlexCAN2 module.

The CAN protocol interface (CPI) manages the serial communication on the CAN bus, requesting RAM access for receiving and transmitting message frames, validating received messages and performing error handling. The message buffer management (MBM) handles message buffer selection for reception and transmission, taking care of arbitration and ID matching algorithms. The bus interface unit (BIU) controls the access to and from the internal interface bus, in order to establish connection to the CPU and to any other modules. Clocks, address and data buses, interrupt outputs and test signals are accessed through the bus interface unit.

## 22.1.3 Features

The FlexCAN2 module includes these distinctive features:

- · Based on and includes all existing features of the Freescale TouCAN module
- · Full implementation of the CAN protocol specification, version 2.0B
- - Standard data and remote frames
- - Extended data and remote frames
- - Data length of 0 to 8 bytes
- - Programmable bit rate up to 1 Mb/sec
- · Content-related addressing
- · 64 flexible message buffers of 0 to 8 bytes data length
- · Each MB configurable as RX or TX, all supporting standard and extended messages
- · Includes 1024 bytes of RAM used for MB storage
- · Programmable clock source to the CAN protocol interface, either system clock or oscillator clock
- · Listen-only mode capability
- · Programmable loop-back mode supporting self-test operation
- · Three programmable mask registers
- · Programmable transmit-first scheme: lowest ID or lowest buffer number
- · Time stamp based on 16-bit free-running timer
- · Global network time, synchronized by a specific message
- · Maskable interrupts
- · Independent of the transmission medium (an external transceiver is assumed)
- · Multi master concept
- · High immunity to EMI
- · Short latency time due to an arbitration scheme for high-priority messages

## 22.1.4 Modes of Operation

The  MPC5553/MPC5554  supports  four  FlexCAN  functional  modes:  normal,  freeze,  listen-only  and loop-back. Just one of the low power modes-module disabled-is supported.

## 22.1.4.1 Normal Mode

In normal mode, the module operates receiving and/or transmitting message frames, errors are handled normally  and  all  the  CAN  protocol  functions  are  enabled.  In  the  MPC5553/MPC5554,  there  is  no distinction between user and supervisor modes.

## 22.1.4.2 Freeze Mode

Freeze mode is entered when the FRZ bit in the module configuration register (CAN x \_MCR) is asserted while the HALT bit in the CAN x \_MCR is set or debug mode is requested by the NPC. In freeze mode no transmission  or  reception  of  frames  is  done,  and  synchronization  with  the  CAN  bus  is  lost.  See Section 22.4.6.1, 'Freeze Mode,' for more information.

## 22.1.4.3 Listen-Only Mode

The module enters this mode when the LOM bit in the CAN \_CR is asserted. In this mode, FlexCAN x operates in a CAN error passive mode, freezing all error counters and receiving messages without sending acknowledgments.

## 22.1.4.4 Loop-Back Mode

The module enters this mode when the LPB bit in the CAN \_CR is asserted. In this mode, FlexCAN x performs  an  internal  loop  back  that  can  be  used  for  self  test  operation.  The  bit  stream  output  of  the transmitter is internally fed back to the receiver input. The CAN receive input pin (CNRX x ) is ignored and the transmit output (CNTX x ) goes to the recessive state (logic 1). FlexCAN behaves as it normally does when transmitting, and treats its own transmitted message as a message received from a remote node. In this mode, FlexCAN ignores the bit sent during the ACK slot in the CAN frame acknowledge field to ensure proper reception of its own message. Both transmit and receive interrupts are generated.

## 22.1.4.5 Module Disabled Mode

This low power mode is entered when the MDIS bit in the CAN\_MCR is asserted. When disabled, the module shuts down the clocks to the CAN protocol interface and message buffer management submodules. Exit  from  this  mode  is  done  by  negating  the  CAN\_MCR[MDIS]  bit.  See  Section 22.4.6.2,  'Module Disabled Mode,' for more information.

## 22.2 External Signal Description

## 22.2.1 Overview

The  FlexCAN2  module  has  two  I/O  signals  connected  to  the  external  MCU  pins.  These  signals  are summarized in Table 22-1 and described in more detail in the next sub-sections.

Table 22-1. FlexCAN2 Signals

| Signal Name 1   | Direction   | Description   |
|-----------------|-------------|---------------|
| CNRX x          | I           | CAN receive   |
| CNTX x          | O           | CAN transmit  |

1 In the MPC5554, x indicates FlexCAN2 module A, B or C, whereas in the MPC5553, x indicates FlexCAN2 module A and C.

## 22.2.2 Detailed Signal Description

## 22.2.2.1 CNRX x

This pin is the receive pin to the CAN bus transceiver. The dominant state is represented by logic level 0. The recessive state is represented by logic level 1.

## 22.2.2.2 CNTX x

This pin is the transmit pin to the CAN bus transceiver. The dominant state is represented by logic level 0. The recessive state is represented by logic level 1.

## 22.3 Memory Map/Register Definition

This section describes the registers and data structures in the FlexCAN2 module. The addresses presented here are relative to the base address of the module.

The address space occupied by FlexCAN2 is continuous: 128 bytes for registers starting at the module base address, extra space for MB storage, and 1024 bytes for 64 MBs.

## 22.3.1 Memory Map

The complete memory map for a FlexCAN2 module with its 64 MBs is shown in Table 22-2. Except for the base addresses, the three (MPC5554) or two (MPC5553) FlexCAN2 modules have identical memory maps. Each individual register is identified by its complete name and the corresponding mnemonic.

Table 22-2. Module Memory Map

| Address                                                                                            | Register Name   | Register Description          | Size (bits)   |
|----------------------------------------------------------------------------------------------------|-----------------|-------------------------------|---------------|
| Base = 0xFFFC_0000 (FlexCAN A) 1 Base = 0xFFFC_4000 (FlexCAN B) 1 Base = 0xFFFC_8000 (FlexCAN C) 1 | CAN x _MCR      | Module configuration register | 32            |
| Base + 0x0004                                                                                      | CAN x _CR       | Control register              | 32            |
| Base + 0x0008                                                                                      | CAN x _TIMER    | Free running timer            | 32            |
| Base + 0x000C                                                                                      | -               | Reserved                      | -             |
| Base + 0x0010                                                                                      | CAN x _RXGMASK  | RX global mask                | 32            |
| Base + 0x0014                                                                                      | CAN x _RX14MASK | RX buffer 14 mask             | 32            |
| Base + 0x0018                                                                                      | CAN x _RX15MASK | RX buffer 15 mask             | 32            |
| Base + 0x001C                                                                                      | CAN x _ECR      | Error counter register        | 32            |
| Base + 0x0020                                                                                      | CAN x _ESR      | Error and status register     | 32            |
| Base + 0x0024                                                                                      | CAN x _IMRH     | Interrupt masks high register | 32            |
| Base + 0x0028                                                                                      | CAN x _IMRL     | Interrupt masks low register  | 32            |
| Base + 0x002C                                                                                      | CAN x _IFRH     | Interrupt flags high register | 32            |
| Base + 0x0030                                                                                      | CAN x _IFRL     | Interrupt flags low register  | 32            |
| Base + 0x0034- Base + 0x005F                                                                       | -               | Reserved                      | -             |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 22-2. Module Memory Map (continued)

| Base + 0x0060- Base + 0x007F   | -           | Reserved              | -               |
|--------------------------------|-------------|-----------------------|-----------------|
| Base + 0x0080- Base + 0x017F   | MB0 - MB15  | Message buffers 0-15  | 128 bits per MB |
| Base + 0x0180- Base + 0x027F   | MB16-MB31   | Message buffers 16-31 | 128 bits per MB |
| Base + 0x0280- Base + 0x047F   | MB32 - MB63 | Message buffers 32-63 | 128 bits per MB |

1 The MPC5554 has FlexCAN2 modules A, B, and C, whereas the MPC5553 only has FlexCAN2 modules A and C.

The FlexCAN2 module stores CAN messages for transmission and reception using a message buffer structure. Each individual MB is formed by 16 bytes mapped in memory as described in Table 22-3. The FlexCAN2 module can manage up to 64 message buffers.  Table 22-3 shows a standard/extended message buffer (MB0) memory map, using 16 bytes (0x80 0x8F) total space. -

Table 22-3. Message Buffer MB0 Memory Mapping

| Address Offset   | MB Field                        |
|------------------|---------------------------------|
| 0x80             | Control and Status (C/S)        |
| 0x84             | Identifier Field                |
| 0x88 - 0x8F      | Data fields 0 - 7 (1 byte each) |

## NOTE

Reading the C/S word of a message buffer (the first word of each MB) will lock it, preventing it from receiving further messages until it is unlocked either by reading another MB or by reading the timer.

## 22.3.2 Message Buffer Structure

The message buffer structure used by the FlexCAN2 module is represented in Figure 22-2. Both extended and standard frames (29-bit identifier and 11-bit identifier, respectively) used in the CAN specification (version 2.0 Part B) are represented.

0

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

Figure 22-2. Message Buffer Structure

| 0x0   | CODE        | CODE                   | SRR IDE RTR            | LENGTH                 | LENGTH        | TIME STAMP    |
|-------|-------------|------------------------|------------------------|------------------------|---------------|---------------|
| 0x4   |             | ID (Extended/Standard) | ID (Extended/Standard) | ID (Extended/Standard) | ID (Extended) | ID (Extended) |
| 0x8   | Data Byte 0 | Data Byte 0            | Data Byte 0            | Data Byte 1            | Data Byte 1   | Data Byte 2   |
| 0xC   | Data Byte 4 | Data Byte 4            | Data Byte 4            | Data Byte 5            | Data Byte 5   | Data Byte 6   |

Table 22-4. Message Buffer Field Descriptions

| Name       | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
|------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| CODE       | Message buffer code. This 4-bit field can be accessed (read or write) by the CPU and by the FlexCAN2 module itself, as part of the message buffer matching and arbitration process. The encoding is shown in Table 22-5 and Table 22-6. See Section 22.4, 'Functional Description,' for additional information.                                                                                                                                                                                                                                                                                    |
| SRR        | Substitute remote request. Fixed recessive bit, used only in extended format. It must be set to '1' by the user for transmission (TX Buffers) and will be stored with the value received on the CANbus for RX receiving buffers. It can be received as either recessive or dominant. If FlexCAN2 receives this bit as dominant, then it is interpreted as arbitration loss. 0 Dominant is not a valid value for transmission in extended format frames 1 Recessive value is compulsory for transmission in extended format frames                                                                  |
| IDE        | ID extended bit. This bit identifies whether the frame format is standard or extended. 0 Frame format is standard 1 Frame format is extended                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| RTR        | Remote transmission request. This bit is used for requesting transmissions of a data frame. If FlexCAN2 transmits this bit as '1' (recessive) and receives it as '0' (dominant), it is interpreted as arbitration loss. If this bit is transmitted as '0' (dominant), then if it is received as '1' (recessive), the FlexCAN2 module treats it as bit error. If the value received matches the value transmitted, it is considered as a successful bit transmission. 0 Indicates the current MB has a data frame to be transmitted 1 Indicates the current MB has a remote frame to be transmitted |
| LENGTH     | Length of data in bytes. This 4-bit field is the length (in bytes) of the RXor TX data, which is located in offset 0x8 through 0xF of the MBspace (see Figure 22-2). In reception, this field is written by the FlexCAN2 module, copied from the DLC (data length code) field of the received frame. In transmission, this field is written by the CPU and corresponds to the DLC field value of the frame to be transmitted. When RTR = 1, the Frame to be transmitted is a remote frame and does not include the data field, regardless of the length field.                                     |
| TIME STAMP | Free-running counter time stamp. This 16-bit field is a copy of the free-running timer, captured for Tx and Rx frames at the time when the beginning of the Identifier field appears on the CAN bus.                                                                                                                                                                                                                                                                                                                                                                                               |
| ID         | Frame identifier. In standard frame format, only the 11 most significant bits (28 to 18) are used for frame identification in both receive and transmit cases. The 18 least significant bits are ignored. In extended frame format, all bits are used for frame identification in both receive and transmit cases.                                                                                                                                                                                                                                                                                 |
| DATA       | Data field. Up to eight bytes can be used for a data frame. For RX frames, the data is stored as it is received from the CAN bus. For TX frames, the CPU prepares the data field to be transmitted within the frame.                                                                                                                                                                                                                                                                                                                                                                               |

Table 22-5. Message Buffer Code for RX buffers

|   RX Code before RX New Frame | Description                    | RX Code after RX New Frame   | Comment                                                                                                                    |
|-------------------------------|--------------------------------|------------------------------|----------------------------------------------------------------------------------------------------------------------------|
|                          0000 | NOT ACTIVE: MB is not active.  | -                            | MB does not participate in the matching process.                                                                           |
|                          0100 | EMPTY: MB is active and empty. | 0010                         | MB participates in the matching process. When a frame is received successfully, the code is automatically updated to FULL. |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

c

Table 22-5. Message Buffer Code for RX buffers (continued)

| RX Code before RX New Frame   | Description                                                                       |   RX Code after RX New Frame | Comment                                                                                                                                                                                                                                   |
|-------------------------------|-----------------------------------------------------------------------------------|------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0010                          | FULL: MB is full.                                                                 |                         0010 | The act of reading the C/S word followed by unlocking the MB does not make the code return to EMPTY.It remains FULL. If a new frame is written to the MBafter the C/S word was read and the MB was unlocked, the code still remains FULL. |
| 0010                          | FULL: MB is full.                                                                 |                         0110 | If the MB is FULL and a new frame is overwritten to this MBbeforetheCPUhad time to read it, the code is automatically updated to OVERRUN. Refer to Section 22.4.3.1, 'Matching Process for details about overrun behavior.                |
| 0110                          | OVERRUN: A frame was overwritten into a full buffer.                              |                         0010 | If the code indicates OVERRUN but the CPU reads the C/S word and then unlocks the MB, when a new frame is written to the MB the code returns to FULL.                                                                                     |
| 0110                          | OVERRUN: A frame was overwritten into a full buffer.                              |                         0110 | If the code already indicates OVERRUN, and yet another new frame must be written, the MB will be overwritten again, and the code will remain OVERRUN. Refer to Section 22.4.3.1, 'Matching Process for details about overrun behavior.    |
| 0XY1 1                        | BUSY: FlexCAN is updating the contents of the MB. The CPU must not access the MB. |                         0010 | An EMPTY buffer was written with a new frame (XY was 01).                                                                                                                                                                                 |
| 0XY1 1                        | BUSY: FlexCAN is updating the contents of the MB. The CPU must not access the MB. |                         0110 | A FULL/OVERRUN buffer was overwritten (XY was 11).                                                                                                                                                                                        |

1 Note that for TX MBs (see Table 22-6), the BUSY bit should be ignored upon read.

Table 22-6. Message Buffer Code for TX buffers

| RTR   |   Initial TX Code | Code after Successful Transmission   | Description                                                                                                              |
|-------|-------------------|--------------------------------------|--------------------------------------------------------------------------------------------------------------------------|
| X     |              1000 | -                                    | INACTIVE: MB does not participate in the arbitration process.                                                            |
| 0     |              1100 | 1000                                 | Transmit data frame unconditionally once. After transmission, the MB automatically returns to the INACTIVE state..       |
| 1     |              1100 | 0100                                 | Transmit remote frame unconditionally once. After transmission, the MB automatically becomes and RX MB with the same ID. |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 22-6. Message Buffer Code for TX buffers (continued)

|   RTR |   Initial TX Code |   Code after Successful Transmission | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|-------|-------------------|--------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|     0 |              1010 |                                 1010 | Transmit a data frame whenever a remote request frame with the same ID is received. This MBparticipates simultaneously in both the matching and arbitration processes. The matching process compares the ID of the incoming remote request frame with the ID of the MB. If a match occurs this MB is allowed to participate in the current arbitration process and the CODE field is automatically updated to '1110' to allow the MB to participate in future arbitration runs. When the frame is eventually transmitted successfully, the Code automatically returns to '1010' to restart the process again. |
|     0 |              1110 |                                 1010 | the MBM as a result of match to a remote request frame. The data frame will be transmitted unconditionally once and then the code will automatically return to '1010'. The CPU can also write this code with the same effect.                                                                                                                                                                                                                                                                                                                                                                                 |

## 22.3.3 Register Descriptions

The FlexCAN2 registers are described in this section. Note that there are three (or two in the MPC5553) separate, identical FlexCAN2 modules. Each register in the following sections is denoted with an ' x ' that represents the specified module, A, B, or C.

## 22.3.3.1 Module Configuration Register (CAN x \_MCR)

CAN \_MCR defines global system configurations, such as the module operation mode and maximum x message buffer configuration. Most of the fields in this register can be accessed at any time, except the MAXMB field, which should only be changed while the module is in freeze mode.

Figure 22-3. Module Configuration Register (CAN x \_MCR)

<!-- image -->

|          | 0             | 1             | 2             | 3             | 4             | 5             | 6             | 7             | 8             | 9             | 10            | 11            | 12            | 13            | 14            | 15            |
|----------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| R        | MDIS          | FRZ           | 0             | HALT          | NOT RDY       | 0             | SOFT RST      | FRZ ACK       | 0             | 0             | 0             | MDIS ACK      | 0             | 0             | 0             | 0             |
| W        |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset    | 0             | 1             | 0             | 1             | 1             | 0             | 0             | 1             | 1             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Reg Addr | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 |
|          | 16            | 17            | 18            | 19            | 20            | 21            | 22            | 23            | 24            | 25            | 26            | 27            | 28            | 29            | 30            | 31            |
| R        | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |               |               | MAXMB         |               |               |               |
| W        |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset    | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 1             | 1             | 1             | 1             |
| Reg Addr | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 | Base + 0x0000 |

## Table 22-7. CAN x \_MCR Field Descriptions

|   Bits | Name   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
|--------|--------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|      0 | MDIS   | Module disable. Controls whether FlexCAN2 is enabled or not. When disabled, FlexCAN2 shuts down the clock to the CAN protocol interface and message buffer management submodules. This is the only bit in CAN x _MCR not affected by soft reset. See Section 22.4.6.2, 'Module Disabled Mode,' for more information. 0 Enable the FlexCAN2 module 1 Disable the FlexCAN2 module                                                                                                                                                                                                 |
|      1 | FRZ    | Freeze enable. Specifies the FlexCAN2 behavior when the HALT bit in the CAN x _MCR is set or when debug mode is requested at MCU level. When FRZ is asserted, FlexCAN2 is enabled to enter freeze mode. Negation of this bit field causes FlexCAN2 to exit from freeze mode. 0 Not enabled to enter freeze mode 1 Enabled to enter freeze mode                                                                                                                                                                                                                                  |
|      2 | -      | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|      3 | HALT   | Halt FlexCAN. Assertion of this bit puts the FlexCAN2 module into freeze mode if FRZ is asserted. The CPU should clear it after initializing the message buffers and CAN x _CR. If FRZ is set, no reception or transmission is performed by FlexCAN2 before this bit is cleared. While in freeze mode, the CPU has write access to the CAN x _ECR, that is otherwise read-only. Freeze mode cannot be entered while FlexCAN2 is disabled. See Section 22.4.6.1, 'Freeze Mode,' for more information. 0 No freeze mode request. 1 Enters freeze mode if the FRZ bit is asserted. |
|      4 | NOTRDY | FlexCAN2 not ready. Indicates that FlexCAN2 is either disabled or in freeze mode. It is negated once FlexCAN2 has exited these modes. 0 FlexCAN2 module is either in normal mode, listen-only mode or loop-back mode 1 FlexCAN2 module is either disabled or freeze mode                                                                                                                                                                                                                                                                                                        |
|      5 | -      | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |

## Table 22-7. CAN x \_MCR Field Descriptions (continued)

| Bits   | Name        | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
|--------|-------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 6      | SOFTRST     | Soft reset. When asserted, FlexCAN2 resets its internal state machines and some of the memory-mapped registers. The following registers are affected by soft reset: GLYPH<127> CAN x _MCR (except the MDIS bit), GLYPH<127> CAN x _TIMER, GLYPH<127> CAN x _ECR, GLYPH<127> CAN x _ESR, GLYPH<127> CAN x _IMRL, GLYPH<127> CAN x _IMRH, GLYPH<127> CAN x _IFRL, GLYPH<127> CAN x _IFRH. Configuration registers that control the interface to the CAN bus are not affected by soft reset. The following registers are unaffected: GLYPH<127> CANx_CR GLYPH<127> CAN x _RXGMASK GLYPH<127> CAN x _RX14MASK GLYPH<127> CAN x _RX15MASK GLYPH<127> all Message buffers The SOFTRST bit can be asserted directly by the CPU when it writes to the CAN x _MCR, but it is also asserted when global soft reset is requested at MCUlevel. Because soft reset is synchronous and has to follow a request/acknowledge procedure across clock domains, it may take some time to fully propagate its effect. The SOFTRST bit remains asserted while reset is pending, and is automatically negated when reset completes. Therefore, software can poll this bit to know when the soft reset has completed. 0 No reset request 1 Resets values in registers indicated above. |
| 7      | FRZACK      | Freeze mode acknowledge. Indicates that FlexCAN2 is in freeze mode and its prescaler is stopped. The freeze mode request cannot be granted until current transmission and reception processes have finished. Therefore the software can poll the FRZACK bit to know when FlexCAN2 has actually entered freeze mode. If freeze mode request is negated, then this bit is negated once the FlexCAN2 prescaler is running again. If freeze mode is requested while FlexCAN2 is disabled, then the FRZACK bit will only be set when the low power mode is exited. See Section 22.4.6.1, 'Freeze Mode,' for more information. 0 FlexCAN2 not in freeze mode, prescaler running 1 FlexCAN2 in freeze mode, prescaler stopped                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 8-10   | -           | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| 11     | MDISACK     | Low power mode acknowledge. Indicates whether FlexCAN2 is disabled. This cannot be performed until all current transmission and reception processes have finished, so the CPU can poll the MDISACK bit to know when FlexCAN2 has actually been disabled. See Section 22.4.6.2, 'Module Disabled Mode,' for more information. 0 FlexCAN2 not disabled 1 FlexCAN2 is disabled                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| 12-25  | -           | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| 26-31  | MAXMB [0:5] | Maximum number of message buffers. This 6-bit field defines the maximum number of message buffers of the FlexCAN2 module. The reset value (0x0F) is equivalent to 16 MB configuration. This field should be changed only while the module is in freeze mode. Note: MAXMB has to be programmed with a value smaller or equal to the number of available message buffers, otherwise FlexCAN2 will not transmit or receive frames. Maximum MBs in use MAXMB 1 + =                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## 22.3.3.2 Control Register (CAN x \_CR)

CAN \_CR is defined for specific FlexCAN2 control features related to the CAN bus, such as bit-rate, x programmable sampling point within an RX bit, loop-back mode, listen-only mode, bus off recovery behavior, and interrupt enabling (for example, bus-off, error). It also determines the division factor for the clock prescaler. Most of the fields in this register should only be changed while the module is disabled or in freeze mode. Exceptions are the BOFFMSK, ERRMSK, and BOFFREC bits, which can be accessed at any time. Note that CANx\_CR is unaffected by soft reset (which occurs when CAN\_MCR[SOFTRST] is asserted).

<!-- image -->

Figure 22-4. Control Register (CAN x \_CR)

## Table 22-8. CAN x \_CR Field Descriptions

| Bits   | Name          | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|--------|---------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-7    | PRESDIV [0:7] | Prescaler division factor. Defines the ratio between the CPI clock frequency and the serial clock (SCK) frequency. The SCK period defines the time quantum of the CAN protocol. For the reset value, the SCKfrequency is equal to the CPI clock frequency. The maximum value of this register is 0xFF, that gives a minimum SCK frequency equal to the CPI clock frequency divided by 256. For more information, refer to Section 22.4.5.4, 'Protocol Timing.' S-clock frequency CPI clock frequency PRESDIV 1 + --------------------------- -------------------------- = |
| 8-9    | RJW [0:1]     | Resync jump width. Defines the maximum number of time quanta 1 that a bit time can be changed by one re-synchronization. The valid programmable values are 0 - 3. Resync Jump Width RJW + 1 =                                                                                                                                                                                                                                                                                                                                                                             |
| 10-12  | PSEG1 [0:2]   | Phase segment 1. Defines the length of phase buffer segment 1 in the bit time. The valid programmable values are 0 - 7. Phase Buffer Segment 1 PSEG1 + 1 ( ) Time Quanta × =                                                                                                                                                                                                                                                                                                                                                                                              |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 22-8. CAN x \_CR Field Descriptions

| Bits   | Name        | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|--------|-------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 13-15  | PSEG2 [0:2] | Phase segment 2. Defines the length of phase buffer segment 2 in the bit time. The valid programmable values are 1 - 7. Phase Buffer Segment 2 PSEG2 + 1 ( ) Time Quanta × =                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| 16     | BOFFMSK     | Bus off mask. Provides a mask for the bus off interrupt. 0 Bus off interrupt disabled 1 Bus off interrupt enabled                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| 17     | ERRMSK      | Error mask. Provides a mask for the error interrupt. 0 Error interrupt disabled 1 Error interrupt enabled                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| 18     | CLK_SRC     | CAN engine clock source. Selects the clock source to the CAN Protocol Interface (CPI) to be either the system clock (driven by the PLL) or the crystal oscillator clock. The selected clock is the one fed to the prescaler to generate the serial clock (SCK). In order to guarantee reliable operation, this bit should only be changed while the module is disabled. 0 = The CAN engine clock source is the oscillator clock 1 = The CAN engine clock source is the system clock                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| 19     | LPB         | Loop back. Configures FlexCAN2 to operate in loop-back mode. See Section 22.1.4, 'Modes of Operation' for information about this operating mode. 0 Loop back disabled 1 Loop back enabled                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| 20-23  | -           | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| 24     | SMP         | Sampling mode. Defines the sampling mode of each bit in the receiving messages (RX). 0 Just one sample is used to determine the RX bit value 1 Three samples are used to determine the value of the received bit: the regular one (sample point) and 2 preceding samples, a majority rule is used                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| 25     | BOFFREC     | Bus off recovery mode. Defines how FlexCAN2 recovers from bus off state. If this bit is negated, automatic recovering from bus off state occurs according to the CAN Specification 2.0B. If the bit is asserted, automatic recovering from bus off is disabled and the module remains in bus off state until the bit is negated by the user. If the negation occurs before 128 sequences of 11 recessive bits are detected on the CANbus, then bus off recovery happens as if the BOFFREC bit had never been asserted. If the negation occurs after 128 sequences of 11 recessive bits occurred, then FlexCAN2 will re-synchronize to the bus by waiting for 11 recessive bits before joining the bus. After negation, the BOFFREC bit can be re-asserted again during bus off, but it will only be effective the next time the module enters bus off. If BOFFREC was negated when the module entered bus off, asserting it during bus off will not be effective for the current bus off recovery. 0 Automatic recovering from bus off state enabled, according to CAN Spec 2.0 part B 1 Automatic recovering from bus off state disabled |
| 26     | TSYN        | Timer sync mode. Enables a mechanism that resets the free-running timer each time a message is received in message buffer 0. This feature provides means to synchronize multiple FlexCAN2 stations with a special SYNC message (that is, global network time). 0 Timer sync feature disabled 1 Timer sync feature enabled Note: There is a possibility of 4 - 5 ticks count skew between the different FlexCAN2 stations that would operate in this mode.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 22-8. CAN x \_CR Field Descriptions

| Bits   | Name          | Description                                                                                                                                                                                                                                                                                                                                            |
|--------|---------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 27     | LBUF          | Lowest buffer transmitted first. This bit defines the ordering mechanism for message buffer transmission. 0 Buffer with lowest ID is transmitted first 1 Lowest number buffer is transmitted first                                                                                                                                                     |
| 28     | LOM           | Listen-only mode. Configures FlexCAN2 to operate in listen-only mode. In this mode, the FlexCAN2 module receives messages without giving any acknowledge. It is not possible to transmit any message in this mode. 0 FlexCAN2 module is in normal active operation, listen only mode is deactivated 1 FlexCAN2 module is in listen only mode operation |
| 29-31  | PROPSEG [0:2] | Propagation segment. Defines the length of the propagation segment in the bit time. The valid programmable values are 0 - 7. Propagation Segment Time (PROPSEG + 1) Time Quanta × = Time Quantum = one S clock period                                                                                                                                  |

1 One time quantum is equal to the S clock period.

## 22.3.3.3 Free Running Timer (CAN x \_TIMER)

CAN \_TIMER represents a 16-bit free running counter that can be read and written by the CPU. The timer x starts from 0x0000 after Reset, counts linearly to 0xFFFF, and wraps around.

The timer is clocked by the FlexCAN2 bit-clock (which defines the baud rate on the CAN bus). During a message transmission/reception, it increments by one for each bit that is received or transmitted. When there is no message on the bus, it counts using the previously programmed baud rate. During freeze mode, the timer is not incremented.

The timer value is captured at the beginning of the identifier field of any frame on the CAN bus. This captured value is written into the TIME STAMP entry in a message buffer after a successful reception or transmission of a message.

Writing to the timer is an indirect operation. The data is first written to an auxiliary register and then an internal request/acknowledge procedure across clock domains is executed. All this is transparent to the user, except for the fact that the data will take some time to be actually written to the register. If desired, software can poll the register to discover when the data was actually written.

Figure 22-5. Free Running Timer (CAN x \_TIMER)

<!-- image -->

|          | 0             | 1             | 2             | 3             | 4             | 5             | 6             | 7             | 8             | 9             | 10            | 11            | 12            | 13            | 14            | 15            |
|----------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| R        | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| W        |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset    | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Reg Addr | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 |
|          | 16            | 17            | 18            | 19            | 20            | 21            | 22            | 23            | 24            | 25            | 26            | 27            | 28            | 29            | 30            | 31            |
| R        | TIMER         | TIMER         | TIMER         | TIMER         | TIMER         | TIMER         | TIMER         | TIMER         | TIMER         | TIMER         | TIMER         | TIMER         | TIMER         | TIMER         | TIMER         | TIMER         |
| W        |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset    | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Reg Addr | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 | Base + 0x0008 |

## 22.3.3.4 RX Mask Registers

These registers are used as acceptance masks for received frame ID. Three masks are defined: a global mask, used for RX buffers 0 13 and 16 63, and two extra masks dedicated for buffers 14 and 15. The --meaning of each mask bit is the following:

- · Mask bit = 0: the corresponding incoming ID bit is 'don't care.'
- · Mask bit = 1: the corresponding ID bit is checked against the incoming ID bit, to see if a match exists.

Note that these masks are used both for standard and extended ID formats. The value of mask registers should not be changed while in normal operation. Locked frames which had matched a MB through a mask may be transferred into the MB (upon release) but may no longer match. Table 22-9 shows some examples of ID masking for standard and extended message buffers.

Table 22-9. Mask Examples for Standard/Extended Message Buffers

|                | Base ID ID28.................ID18   | IDE   | Extended ID ID17......................................ID0   | Match   |
|----------------|-------------------------------------|-------|-------------------------------------------------------------|---------|
| MB2 ID         | 1 1 1 1 1 1 1 1 0 0 0               | 0     |                                                             |         |
| MB3 ID         | 1 1 1 1 1 1 1 1 0 0 0               | 1     | 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1                         |         |
| MB4 ID         | 0 0 0 0 0 0 1 1 1 1 1               | 0     |                                                             |         |
| MB5 ID         | 0 0 0 0 0 0 1 1 1 0 1               | 1     | 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1                         |         |
| MB14 ID        | 1 1 1 1 1 1 1 1 0 0 0               | 1     | 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1                         |         |
| RX Global Mask | 1 1 1 1 1 1 1 1 1 1 0               |       | 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 1                         |         |
| RX Msg in 1    | 1 1 1 1 1 1 1 1 0 0 1               | 1     | 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1                         | 3       |
| RX Msg in 2    | 1 1 1 1 1 1 1 1 0 0 1               | 0     |                                                             | 2       |
| RX Msg in 3    | 1 1 1 1 1 1 1 1 0 0 1               | 1     | 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 0                         |         |
| RX Msg in 4    | 0 1 1 1 1 1 1 1 0 0 0               | 0     |                                                             |         |
| RX Msg in 5    | 0 1 1 1 1 1 1 1 0 0 0               | 1     | 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1                         | 14      |
| RX 14 Mask     | 0 1 1 1 1 1 1 1 1 1 1               |       | 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0                         |         |

Table 22-9. Mask Examples for Standard/Extended Message Buffers (continued)

|             | Base ID ID28.................ID18   |   IDE | Extended ID ID17......................................ID0   | Match   |
|-------------|-------------------------------------|-------|-------------------------------------------------------------|---------|
| RX Msg in 6 | 1 0 1 1 1 1 1 1 0 0 0               |     1 | 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1                         |         |
| RX Msg in 7 | 0 1 1 1 1 1 1 1 0 0 0               |     1 | 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1                         | 14      |

- 1 Match for Extended Format (MB3).
- 2 Match for Standard Format. (MB2).
- 3 Mismatch for MB3 because of ID0.
- 4 Mismatch for MB2 because of ID28.
- 5 Mismatch for MB3 because of ID28, Match for MB14 (uses RX14MASK).
- 6 Mismatch for MB14 because of ID27 (uses RX14MASK).
- 7 Match for MB14 (uses RX14MASK).

## 22.3.3.4.1 RX Global Mask (CAN x \_RXGMASK)

The RX global mask bits are applied to all RX identifiers excluding RX buffers 14 15, that have their -specific  RX  mask  registers.  Access  to  this  register  is  unrestricted.  Note  that  CANx\_RXGMASK  is unaffected by soft reset (which occurs when CAN\_MCR[SOFTRST] is asserted).

<!-- image -->

Figure 22-6. RX Global Mask Register (CAN x \_RXGMASK)

Table 22-10. CAN x \_RXGMASK Field Descriptions

| Bits   | Names   | Description                                                                                     |
|--------|---------|-------------------------------------------------------------------------------------------------|
| 0-2    | -       | Reserved, should be cleared.                                                                    |
| 3-13   | MI n    | Standard ID mask bits. These bits are the same mask bits for the standard and extended formats. |
| 14-31  | MI n    | Extended ID mask bits. These bits are used to mask comparison only in extended format.          |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## 22.3.3.4.2 RX 14 Mask (CAN x \_RX14MASK)

The CAN \_RX14MASK register has the same structure as the RX global mask register and is used to x mask  message  buffer  14.  Access  to  this  register  is  unrestricted.  Note  that  CANx\_RX14MASK  is unaffected by soft reset (which occurs when CAN\_MCR[SOFTRST] is asserted).

- · Address offset: 0x14
- · Reset value: 0x1FFF\_FFFF

## 22.3.3.4.3 RX 15 Mask (CAN x \_RX15MASK)

The CAN \_RX15MASK register has the same structure as the RX global mask register and is used to x mask  message  buffer  15.  Access  to  this  register  is  unrestricted.  Note  that  CANx\_RX15MASK  is unaffected by soft reset (which occurs when CAN\_MCR[SOFTRST] is asserted).

- · Address offset: 0x18
- · Reset value: 0x1FFF\_FFFF

## 22.3.3.5 Error Counter Register (CAN x \_ECR)

CAN \_ECR has two 8-bit fields reflecting the value of two FlexCAN2 error counters: the transmit error x counter  (TXECTR  field)  and  receive  error  counter  (RXECTR  field) . The  rules  for  increasing  and decreasing  these  counters  are  described  in  the  CAN  protocol  and  are  completely  implemented  in  the FlexCAN2 module. Both counters are read only except in freeze mode, where they can be written by the CPU.

Writing to the CAN \_ECR while in freeze mode is an indirect operation. The data is first written to an x auxiliary register and then an internal request/acknowledge procedure across clock domains is executed. All this is transparent to the user, except for the fact that the data will take some time to be actually written to the register. If desired, software can poll the register to discover when the data was actually written.

FlexCAN2 responds to any bus state as described in the protocol: transmitting, for example, an 'error active'  or  'error  passive'  flag,  delaying  its  transmission  start  time  ('error  passive'),  and  avoiding  any influence on the bus when in the bus off state. The following are the basic rules for FlexCAN2 bus state transitions:

- · If the value of TXECTR or RXECTR increases to be greater than or equal to 128, the FLTCONF field in the CAN x \_ESR is updated to reflect the 'error passive' state.
- · If the FlexCAN2 state is 'error passive,' and either TXECTR or RXECTR decrements to a value less than or equal to 127 while the other already satisfies this condition, the FLTCONF field in the CAN \_ESR is updated to reflect the 'error active' state. x
- · If the value of TXECTR increases to be greater than 255, the FLTCONF field in the CAN x \_ESR is updated to reflect the bus off state, and an interrupt may be issued. The value of TXECTR is then reset to zero.
- · If FlexCAN2 is in the bus off state, then TXECTR is cascaded together with another internal counter to count the 128th occurrences of 11 consecutive recessive bits on the bus. Hence, TXECTR is reset to zero and counts in a manner where the internal counter counts 11 such bits and then wraps around while incrementing the TXECTR. When TXECTR reaches the value of 128, the FLTCONF field in CAN \_ESR is updated to be 'error active' and both error counters are reset to x zero. At any instance of dominant bit following a stream of less than 11 consecutive recessive bits, the internal counter resets itself to zero without affecting the TXECTR value.
- · If during system start-up, only one node is operating, then its TXECTR increases in each message it is trying to transmit, as a result of acknowledge errors (indicated by the ACKERR bit in

CAN \_ESR). After the transition to the 'error passive' state, the TXECTR does not increment x anymore by acknowledge errors. Therefore the device never goes to the bus off state.

- · If the RXECTR increases to a value greater than 127, it is not incremented further, even if more errors are detected while being a receiver. At the next successful message reception, the counter is set to a value between 119 and 127 to resume to 'error active' state.

Figure 22-7. Error Counter Register (CAN x \_ECR)

<!-- image -->

|          | 0             | 1             | 2             | 3             | 4             | 5             | 6             | 7             | 8             | 9             | 10            | 11            | 12            | 13            | 14            | 15            |
|----------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| R        | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| W        |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset    | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Reg Addr | Base + 0x001C | Base + 0x001C | Base + 0x001C | Base + 0x001C | Base + 0x001C | Base + 0x001C | Base + 0x001C | Base + 0x001C | Base + 0x001C | Base + 0x001C | Base + 0x001C | Base + 0x001C | Base + 0x001C | Base + 0x001C | Base + 0x001C | Base + 0x001C |
|          | 16            | 17            | 18            | 19            | 20            | 21            | 22            | 23            | 24            | 25            | 26            | 27            | 28            | 29            | 30            | 31            |
| R        | RXECTR TXECTR | RXECTR TXECTR | RXECTR TXECTR | RXECTR TXECTR | RXECTR TXECTR | RXECTR TXECTR | RXECTR TXECTR | RXECTR TXECTR | RXECTR TXECTR | RXECTR TXECTR | RXECTR TXECTR | RXECTR TXECTR | RXECTR TXECTR | RXECTR TXECTR | RXECTR TXECTR | RXECTR TXECTR |
| W        |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset    | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Reg Addr | Base + 0x001C | Base + 0x001C | Base + 0x001C | Base + 0x001C | Base + 0x001C | Base + 0x001C | Base + 0x001C | Base + 0x001C | Base + 0x001C | Base + 0x001C | Base + 0x001C | Base + 0x001C | Base + 0x001C | Base + 0x001C | Base + 0x001C | Base + 0x001C |

## 22.3.3.6 Error and Status Register (CAN x \_ESR)

CAN \_ESR reflects various error conditions, some general status of the device, and it is the source of two x interrupts to the CPU. The reported error conditions (bits 16-21) are those that occurred since the last time the  CPU  read  this  register.  The  CPU  read  action  clears  BIT1ERR,  BIT0ERR,  ACKERR,  CRCERR, FRMERR, and STFERR.  TXWRN, RXWRN, IDLE, TXRX, FLTCONF, BOFFINT, and ERRINT are status bits.

Most bits in this register are read-only, except BOFFINT and ERRINT, which are interrupt flags that can be cleared by writing 1 to them (writing 0 has no effect). See Section 22.4.7, 'Interrupts,' for more details.

## NOTE

A read clears BIT1ERR, BIT0ERR, ACKERR, CRCERR, FRMERR, and STFERR, therefore these bits must not be read speculatively. For future compatibility, the TLB entry covering the CAN x \_ESR must be configured to be guarded.

Figure 22-8. Error and Status Register (CAN x \_ESR)

<!-- image -->

|          | 0             | 1             | 2             | 3             | 4             | 5             | 6             | 7             | 8             | 9             | 10            | 11            | 12            | 13            | 14            | 15            |
|----------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| R        | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| W        |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |               |
| Reset    | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Reg Addr | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 |
|          | 16            | 17            | 18            | 19            | 20            | 21            | 22            | 23            | 24            | 25            | 26            | 27            | 28            | 29            | 30            | 31            |
| R        | BIT1 ERR      | BIT0 ERR      | ACK ERR       | CRC ERR       | FRM ERR       | STF ERR       | TX WRN        | RX WRN        | IDLE          | TXRX          | FLTCONF       |               | 0             | BOFF INT      | ERR INT       | 0             |
| W        |               |               |               |               |               |               |               |               |               |               |               |               |               | w1c           | w1c           |               |
| Reset    | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Reg Addr | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 | Base + 0x0020 |

Table 22-11. CAN x \_ESR Field Descriptions

| Bits   | Name    | Description                                                                                                                                                                                                                                                                                                                                                                                |
|--------|---------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-15   | -       | Reserved.                                                                                                                                                                                                                                                                                                                                                                                  |
| 16     | BIT1ERR | Bit 1 error. Indicates when an inconsistency occurs between the transmitted and the received message in a bit. A read clears BIT1ERR. 0 No such occurrence 1 At least one bit sent as recessive is received as dominant Note: This bit is not set by a transmitter in case of arbitration field or ACK slot, or in case of a node sending a passive error flag that detects dominant bits. |
| 17     | BIT0ERR | Bit 0 error. Indicates when an inconsistency occurs between the transmitted and the received message in a bit. A read clears BIT0ERR. 0 No such occurrence 1 At least one bit sent as dominant is received as recessive                                                                                                                                                                    |
| 18     | ACKERR  | Acknowledge error. Indicates that an acknowledge error has been detected by the transmitter node; that is, a dominant bit has not been detected during the ACK SLOT. A read clears ACKERR. 0 No such occurrence 1 An ACK error occurred since last read of this register                                                                                                                   |
| 19     | CRCERR  | Cyclic redundancy code error. Indicates that a CRC error has been detected by the receiver node; that is, the calculated CRC is different from the received. A read clears CRCERR. 0 No such occurrence 1 A CRC error occurred since last read of this register.                                                                                                                           |
| 20     | FRMERR  | Form error. Indicates that a form error has been detected by the receiver node; that is, a fixed-form bit field contains at least one illegal bit. A read clears FRMERR. 0 No such occurrence 1 A form error occurred since last read of this register                                                                                                                                     |
| 21     | STFERR  | Stuffing error. Indicates that a stuffing error has been detected. A read clears STFERR. 0 No such occurrence. 1 A stuffing error occurred since last read of this register.                                                                                                                                                                                                               |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 22-11. CAN x \_ESR Field Descriptions (continued)

| Bits   | Name          | Description                                                                                                                                                                                                                                                                                                                                                                  |
|--------|---------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 22     | TXWRN         | TX error counter. This status bit indicates that repetitive errors are occurring during message transmission. 0 No such occurrence 1 TXECTR ≥ 96                                                                                                                                                                                                                             |
| 23     | RXWRN         | RX error counter. This status bit indicates when repetitive errors are occurring during messages reception. 0 No such occurrence 1 RXECTR ≥ 96                                                                                                                                                                                                                               |
| 24     | IDLE          | CAN bus IDLE state. This status bit indicates when CAN bus is in IDLE state. 0 No such occurrence 1 CAN bus is now IDLE                                                                                                                                                                                                                                                      |
| 25     | TXRX          | Current FlexCAN2 status (transmitting/receiving). This status bit indicates if FlexCAN2 is transmitting or receiving a message when the CAN bus is not in IDLE state. This bit has no meaning when IDLE is asserted. 0 FlexCAN2 is receiving a message (IDLE = 0) 1 FlexCAN2 is transmitting a message (IDLE = 0)                                                            |
| 26-27  | FLTCONF [0:1] | Fault confinement state. This status bit indicates the confinement state of the FlexCAN2 module. If the LOMbit in the CAN x _CRis asserted, the FLTCONF field will indicate 'Error Passive'. Since the CAN x _CR is not affected by soft reset, the FLTCONF field will not be affected by soft reset if the LOM bit is asserted. 00 Error active 01 Error passive 1X Bus off |
| 28     | -             | Reserved.                                                                                                                                                                                                                                                                                                                                                                    |
| 29     | BOFFINT       | Bus off interrupt. This status bit is set when FlexCAN2 is in the bus off state. If CAN x _CR[BOFFMSK] is set, an interrupt is generated to the CPU. This bit is cleared by writing it to 1. Writing 0 has no effect. 0 No such occurrence 1 FlexCAN2 module is in 'Bus Off' state                                                                                           |
| 30     | ERRINT        | Error interrupt. This status bit indicates that at least one of the error bits (bits 16-21) is set. If CAN x _CR[ERRMSK] is set, an interrupt is generated to the CPU. This bit is cleared by writing it to 1. Writing 0 has no effect. 0 No such occurrence 1 Indicates setting of any error bit in the CAN x _ESR                                                          |
| 31     | -             | Reserved.                                                                                                                                                                                                                                                                                                                                                                    |

## 22.3.3.7 Interrupt Masks High Register (ICAN x \_IMRH)

CAN \_IMRH allows any number of a range of 32 message buffer interrupts to be enabled or disabled. It x contains  one  interrupt  mask  bit  per  buffer,  enabling  the  CPU  to  determine  which  buffer  generates  an interrupt after a successful transmission or reception (that is,  when the corresponding IFRH bit is set).

Figure 22-9. Interrupt Masks High Register (CAN x \_IMRH)

<!-- image -->

Table 22-12. CAN x \_IMRH Field Descriptions

| Bits   | Name    | Description                                                                                                                                                                                                                                                                                                                |
|--------|---------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-31   | BUF n M | Message buffer n mask. Enables or disables the respective FlexCAN2 message buffer (MB63 to MB32) Interrupt. 0 The corresponding buffer Interrupt is disabled 1 The corresponding buffer Interrupt is enabled Note: Setting or clearing a bit in the IMRH register can assert or negate an interrupt request, respectively. |

## 22.3.3.8 Interrupt Masks Low Register (CAN x \_IMRL)

CAN \_IMRL allows enabling or disabling any number of a range of 32 message buffer interrupts. It x contains  one  interrupt  mask  bit  per  buffer,  enabling  the  CPU  to  determine  which  buffer  generates  an interrupt after a successful transmission or reception (that is, when the corresponding IFRL bit is set).

Figure 22-10. Interrupt Mask Low Register (CAN x \_IMRL)

<!-- image -->

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 22-13. CAN x \_IMRL Field Descriptions

| Bits   | Name    | Description                                                                                                                                                                                                                                                                                                               |
|--------|---------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-31   | BUF n M | Message buffer n mask. Enables or disables the respective FlexCAN2 message buffer (MB31 to MB0) Interrupt. 0 The corresponding buffer Interrupt is disabled 1 The corresponding buffer Interrupt is enabled Note: Setting or clearing a bit in the IMRL register can assert or negate an interrupt request, respectively. |

## 22.3.3.9 Interrupt Flags High Register (CAN x \_IFRH)

CAN \_IFRH defines the flags for 32 message buffer interrupts. It contains one interrupt flag bit per buffer. x Each successful transmission or reception sets the corresponding IFRH bit. If the corresponding IMRH bit is set, an interrupt will be generated. The interrupt flag may be cleared by writing it to 1. Writing 0 has no effect.

Figure 22-11. Interrupt Flags High Register (CAN x \_IFRH)

<!-- image -->

|          | 0             | 1             | 2             | 3             | 4             | 5             | 6             | 7             | 8             | 9             | 10            | 11            | 12            | 13            | 14            | 15            |
|----------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| R        | BUF 63I       | BUF 62I       | BUF 61I       | BUF 60I       | BUF 59I       | BUF 58I       | BUF 57I       | BUF 56I       | BUF 55I       | BUF 54I       | BUF 53I       | BUF 52I       | BUF 51I       | BUF 50I       | BUF 49I       | BUF 48I       |
| W        | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           |
| Reset    | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Reg Addr | Base + 0x002C | Base + 0x002C | Base + 0x002C | Base + 0x002C | Base + 0x002C | Base + 0x002C | Base + 0x002C | Base + 0x002C | Base + 0x002C | Base + 0x002C | Base + 0x002C | Base + 0x002C | Base + 0x002C | Base + 0x002C | Base + 0x002C | Base + 0x002C |
|          | 16            | 17            | 18            | 19            | 20            | 21            | 22            | 23            | 24            | 25            | 26            | 27            | 28            | 29            | 30            | 31            |
| R        | BUF 47I       | BUF 46I       | BUF 45I       | BUF 44I       | BUF 43I       | BUF 42I       | BUF 41I       | BUF 40I       | BUF 39I       | BUF 38I       | BUF 37I       | BUF 36I       | BUF 35I       | BUF 34I       | BUF 33I       | BUF 32I       |
| W        | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           |
| Reset    | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Reg Addr | Base + 0x002C | Base + 0x002C | Base + 0x002C | Base + 0x002C | Base + 0x002C | Base + 0x002C | Base + 0x002C | Base + 0x002C | Base + 0x002C | Base + 0x002C | Base + 0x002C | Base + 0x002C | Base + 0x002C | Base + 0x002C | Base + 0x002C | Base + 0x002C |

Table 22-14. CAN x \_IFRH Field Descriptions

| Bits   | Name    | Description                                                                                                                                                                                                                           |
|--------|---------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-31   | BUF n I | Message buffer n interrupt. Each bit represents the respective FlexCAN2 message buffer (MB63-MB32) interrupt. Write 1 to clear. 0 No such occurrence 1 The corresponding buffer has successfully completed transmission or reception. |

## 22.3.3.10 Interrupt Flags Low Register (CAN x \_IFRL)

CAN \_IFRL defines the flags for 32 message buffer interrupts. It contains one interrupt flag bit per buffer. x Each successful transmission or reception sets the corresponding IFRL bit. If the corresponding IMRL bit is set, an interrupt will be generated. The interrupt flag may be cleared by writing it to 1. Writing 0 has no effect.

Figure 22-12. Interrupt Flags Low Register (CAN x \_IFRL)

<!-- image -->

|          | 0             | 1             | 2             | 3             | 4             | 5             | 6             | 7             | 8             | 9             | 10            | 11            | 12            | 13            | 14            | 15            |
|----------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| R        | BUF 31I       | BUF 30I       | BUF 29I       | BUF 28I       | BUF 27I       | BUF 26I       | BUF 25        | BUF 24I       | BUF 23I       | BUF 22I       | BUF 21I       | BUF 20I       | BUF 19I       | BUF 18I       | BUF 17I       | BUF 16I       |
| W        | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           |
| Reset    | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Reg Addr | Base + 0x0030 | Base + 0x0030 | Base + 0x0030 | Base + 0x0030 | Base + 0x0030 | Base + 0x0030 | Base + 0x0030 | Base + 0x0030 | Base + 0x0030 | Base + 0x0030 | Base + 0x0030 | Base + 0x0030 | Base + 0x0030 | Base + 0x0030 | Base + 0x0030 | Base + 0x0030 |
|          | 16            | 17            | 18            | 19            | 20            | 21            | 22            | 23            | 24            | 25            | 26            | 27            | 28            | 29            | 30            | 31            |
| R        | BUF 15I       | BUF 14I       | BUF 13I       | BUF 12I       | BUF 11I       | BUF 10I       | BUF 09I       | BUF 08I       | BUF 07I       | BUF 06I       | BUF 05I       | BUF 04I       | BUF 03I       | BUF 02I       | BUF 01I       | BUF 00I       |
| W        | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           | w1c           |
| Reset    | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             | 0             |
| Reg Addr | Base + 0x0030 | Base + 0x0030 | Base + 0x0030 | Base + 0x0030 | Base + 0x0030 | Base + 0x0030 | Base + 0x0030 | Base + 0x0030 | Base + 0x0030 | Base + 0x0030 | Base + 0x0030 | Base + 0x0030 | Base + 0x0030 | Base + 0x0030 | Base + 0x0030 | Base + 0x0030 |

## Table 22-15. CAN x \_IFRL Field Descriptions

| Bits   | Name    | Description                                                                                                                                                                                                                             |
|--------|---------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-31   | BUF n I | Message buffer n interrupt. Each bit represents the respective FlexCAN2 message buffer (MB31 to MB0) interrupt. Write 1 to clear. 0 No such occurrence 1 The corresponding buffer has successfully completed transmission or reception. |

## 22.4 Functional Description

## 22.4.1 Overview

The  FlexCAN2 module is a CAN protocol engine with a very flexible  message  buffer  configuration scheme. The module can have up to 64 message buffers, any of which can be assigned as either a TX buffer or an RX buffer. Each message buffer has an assigned interrupt flag to indicate successful completion of transmission or reception.

## 22.4.2 Transmit Process

The CPU prepares a message buffer for transmission by executing the following steps:

- · Write the CODE field of the control and status word to keep the TX MB inactive (code = 1000).
- · Write the ID word.
- · Write the DATA bytes.
- · Write the LENGTH and CODE fields of the control and status word to activate the TX MB.

The first and last steps are mandatory.

## 22.4.2.1 Arbitration process

This process selects which will be the next MB to be transmitted. All MBs programmed as transmit buffers will  be  scanned  to  find  the  lowest  ID 1 or  the  lowest  MB  number,  depending on the LBUF bit in the CAN \_CR. The selected MB will be transferred to an internal serial message buffer (SMB), which is not x user accessible, and then transmitted.

The arbitration process is triggered in the following events:

- · During the CRC field of the CAN frame
- · During the error delimiter field of the CAN frame
- · During Intermission, if the winner MB defined in a previous arbitration was deactivated, or if there was no MB to transmit, but the CPU wrote to the C/S word of any MB after the previous arbitration finished
- · When MBM is in idle or bus off state and the CPU writes to the C/S word of any MB
- · Upon leaving freeze mode

When the arbitration is over, and there is a winner MB for transmission, the frame is transferred to the SMB for  transmission.  This  is  called  'move  out.'  After  move  out,  the  CAN  transmit  machine  will  start  to transmit the frame according to the CAN protocol rules. FlexCAN2 transmits up to eight data bytes, even if the data length code (DLC) value is bigger.

At the end of a successful transmission, the value of the free running timer at the beginning of the identifier field is written into the TIME STAMP field in the MB, the CODE field in the control and status word of the MB is updated, a status flag is set in CAN x \_IFRL or CAN \_IFRH, and an MB interrupt is generated x if allowed by the corresponding interrupt mask register bit.

## 22.4.3 Receive Process

The CPU prepares a message buffer for frame reception by executing the following steps:

1. If LBUF is negated, the arbitration considers not only the ID, but also the RTR and IDE bits placed inside the ID at the same positions they are transmitted in the CAN frame.

- · Write the CODE field of the control and status word to keep the RX MB inactive (CODE = 0000).
- · Write the ID word.
- · Write the CODE field of the control and status word to mark the MB as 'receive active and empty.'

The first and last steps are mandatory.

## 22.4.3.1 Matching Process

After a MB is marked as 'RX active and empty,' it will participate in the internal matching process, which takes place every time the receiver receives an error free frame. In this process, all active RX buffers compare their ID value to the newly received one, and if a match occurs, the frame is transferred (move in) to the first (that is, lowest entry) matching MB. The value of the free running timer is written into the TIME STAMP field in the MB. The ID field, the DATA field (8 bytes at most), and the LENGTH field are stored, the CODE field is updated, and a status flag is set in CAN x \_IFRL or CAN \_IFRH, and an interrupt x is generated if the corresponding interrupt mask is enabled in CAN x \_IMRL/H.

The CPU should read an RX frame from its MB in the following way:

- · Control and status word (mandatory, activates internal lock for this buffer)
- · ID (optional, needed only if a mask was used)
- · DATA field words
- · Free running timer (optional, releases internal lock)

Reading the free running timer is not mandatory. If not executed, the MB remains locked, unless the CPU starts reading another MB. Note that only a single MB is locked at a time. The only mandatory CPU read operation is of the control and status word, to assure data coherency. If the BUSY bit is set in the CODE field, then the CPU should defer the access to the MB until this bit is negated.

The CPU should synchronize to frame reception by the status flag bit for the specific MB in one of the CANx\_IFRH and CANx\_IFRL registers and not by the control and status word code field of that MB. Polling the CODE field does not work because once a frame was received and the CPU services the MB (by reading the C/S word followed by unlocking the MB), the CODE field will not return to EMPTY. It will remain FULL, as explained in Table 22-5. If the CPU tries to workaround this behavior by writing to the C/S word to force an EMPTY code after reading the MB, the MB is actually deactivated from any currently ongoing matching process. As a result, a newly received frame matching the ID of that MB may be lost. In summary: never do polling by reading directly the C/S word of the MBs. Instead, read the CANx\_IFRH and CANx\_IFRL registers.

Note that the received ID field is always stored in the matching MB, thus the contents of the ID field in a MB can change if the match was due to mask.

## 22.4.3.2 Self Received Frames

FlexCAN2 receives frames transmitted by itself if there exists an RX matching MB, but only if an ACK is generated by an external node or if loop-back mode is enabled.

## 22.4.4 Message Buffer Handling

In  order  to  maintain  data  coherency  and  FlexCAN2  proper  operation,  the  CPU  must  obey  the  rules described in Section 22.4.2, 'Transmit Process,' and Section 22.4.3, 'Receive Process.' Any form of CPU accessing a MB structure within FlexCAN2 other than those specified can cause FlexCAN2 to behave in an unpredictable way.

Deactivation of a message buffer is a CPU action that causes that MB to be excluded from FlexCAN2 transmit  or  receive  processes  during  the  current  match/arbitration  round.  Any  CPU  write  access  to  a control and status word of the MB structure deactivates that MB, excluding it from the current RX/TX process.  However,  deactivation  is  not  permanent.  The  MB  that  was  deactivated  during  the  current match/arbitration round will be available for transmission or reception in the next round.

The purpose of deactivation is data coherency. The match/arbitration process scans the MBs to decide which MB to transmit or receive. If the CPU updates the MB in the middle of a match or arbitration process, the data of that MB may no longer be coherent, therefore that MB is deactivated.

Match and arbitration are one-pass processes. After scanning all MBs, a winner is determined. If MBs are changed after they are scanned, no re-evaluation is done to determine a new match/winner; and a frame may be lost because the winner may have been deactivated. If two RX MBs have a matching ID to a received  frame,  then  it  is  not  guaranteed  reception  if  the  user  deactivated  the  matching  MB  after FlexCAN2 has scanned the second.

## 22.4.4.1 Notes on TX Message Buffer Deactivation

There is a point in time until which the deactivation of a TX MB causes it not to be transmitted (end of move out). After this point, it is transmitted but no interrupt is issued and the CODE field is not updated.

If a TX MB containing the lowest ID (or lowest buffer if LBUF is set) is deactivated after FlexCAN2 has scanned it while in arbitration process, then FlexCAN2 can transmit a MB with ID that may not be the lowest at the time.

## 22.4.4.2 Notes on RX Message Buffer Deactivation

If the deactivation occurs during move in, the move operation is aborted and no interrupt is issued, but the MB contains mixed data from two different frames.

In case the CPU writes data into RX MB data words while it is being moved in, the move operation is aborted and no interrupt will be issued, but the control/status word may be changed to reflect FULL or OVRN. This action should be avoided.

## 22.4.4.3 Data Coherency Mechanisms

The FlexCAN2 module has a mechanism to assure data coherency in both receive and transmit processes. The mechanism includes a lock status for MBs and two internal storage areas, called serial message buffers (SMB), to buffer frame transfers within FlexCAN. The details of the mechanism are the following:

- · CPU reading a control and status word of an MB triggers a lock for that MB; that is, a new RX frame which matches this MB, cannot be written into this MB.
- · In order to release a locked MB, the CPU should either lock another MB (by reading its control and status word), or globally release any locked MB (by reading the free-running timer).
- · If while a MB is locked, an RX frame with a matching ID is received, then it cannot be stored within that MB and it remains in the SMB. There is no indication in the CAN x \_ESR of that situation.
- · If while a MB is locked, two or more RX frames with matching ID are received, then the last received one is kept within the SMB, while all preceding ones are lost. There is no indication that the preceding ones were lost in the CAN x \_ESR.
- · If a locked MB is released, and there exists a matching frame within the SMB, this frame is then transferred to the matching MB.

- · If the CPU reads a RX MB while it is being transferred into (from) SMB, then the BUSY bit is set in the CODE field of the control and status word. In order to assure data coherency, the CPU should wait until this bit is negated before further reading from that MB. Note that in this case such MB is not locked.
- · If the CPU deactivates a locked RX MB, then its lock status is negated, but no data is transferred into that MB.

## 22.4.5 CAN Protocol Related Features

## 22.4.5.1 Remote Frames

A remote frame is a special kind of frame. The user can program a MB to be a request remote frame by writing  the  MB  as  transmit  with  the  RTR  bit  set  to  1.  After  the  remote  request  frame  is  transmitted successfully, the MB becomes a receive message buffer, with the same ID as before.

When a remote request frame is received by FlexCAN, its ID is compared to the IDs of the transmit message buffers with the CODE field '1010'. If there is a matching ID, then this MB frame will be transmitted. Note that if the matching MB has the RTR bit set, then FlexCAN2 will transmit a remote frame as a response.

A received remote request frame is not stored in a receive buffer. It is only used to trigger a transmission of a frame in response. The mask registers are not used in remote frame matching, and all ID bits (except RTR) of the incoming received frame should match.

In the case that a remote request frame was received and matched a MB, this message buffer immediately enters the internal arbitration process, but is considered as normal TX MB, with no higher priority. The data length of this frame is independent of the DLC field in the remote frame that initiated its transmission.

## 22.4.5.2 Overload Frames

FlexCAN2 will transmit overload frames due to detection of following conditions on CAN bus:

- · Detection of a dominant bit in the first/second bit of intermission
- · Detection of a dominant bit at the 7th bit (last) of end of frame field (RX frames)
- · Detection of a dominant bit at the 8th bit (last) of error frame delimiter or overload frame delimiter

## 22.4.5.3 Time Stamp

The value of the free running timer is sampled at the beginning of the identifier field on the CAN bus, and is stored at the end of 'move in' in the TIME STAMP field, providing network behavior with respect to time.

Note that the free running timer can be reset upon a specific frame reception, enabling network time synchronization. Refer to TSYN description in Section 22.3.3.2, 'Control Register (CANx\_CR).'

## 22.4.5.4 Protocol Timing

The clock source to the CAN protocol interface (CPI) can be either the system clock or a direct feed from the oscillator pin EXTAL. The clock source is selected by the CLK\_SRC bit in the CAN\_CR.  The clock is fed to the prescaler to generate the serial clock (SCK).

## FlexCAN2 Controller Area Network

The FlexCAN2 module supports a variety of means to setup bit timing parameters that are required by the CAN  protocol.  The  CAN \_CR  has  various  fields  used  to  control  bit  timing  parameters:  PRESDIV, x PROPSEG, PSEG1, PSEG2 and RJW. See Section 22.3.3.2, 'Control Register (CANx\_CR).'

The PRESDIV field controls a prescaler that generates the serial clock (SCK), whose period defines the 'time quantum' used to compose the CAN waveform. A time quantum is the atomic unit of time handled by FlexCAN.

<!-- formula-not-decoded -->

A bit time is subdivided into three segments 1 (reference Figure 22-13 and Table 22-16):

- · SYNCSEG: This segment has a fixed length of one time quantum. Signal edges are expected to happen within this section.
- · Time segment 1: This segment includes the propagation segment and the phase segment 1 of the CAN standard. It can be programmed by setting the PROPSEG and the PSEG1 fields of the CTRL register so that their sum (plus 2) is in the range of 4 to 16 time quanta.
- · Time segment 2: This segment represents the phase segment 2 of the CAN standard. It can be programmed by setting the PSEG2 field of the CTRL register (plus 1) to be 2 to 8 time quanta long.

<!-- formula-not-decoded -->

Figure 22-13. Segments within the Bit Time

<!-- image -->

Table 22-16. Time Segment Syntax

| Syntax   | Description                                                        |
|----------|--------------------------------------------------------------------|
| SYNCSEG  | System expects transitions to occur on the bus during this period. |

1. For further explanation of the underlying concepts please refer to ISO/DIS 11519 -1, Section 10.3. Reference also the Bosch CAN 2.0A/B protocol specification dated September 1991 for bit timing.

Table 22-16. Time Segment Syntax

| Transmit Point   | A node in transmit mode transfers a new value to the CAN bus at this point.                                                                                    |
|------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Sample Point     | A node in receive mode samples the bus at this point. If the three samples per bit option is selected, then this point marks the position of the third sample. |

Table 22-17 gives an overview of the CAN compliant segment settings and the related parameter values.

## NOTE

It is the user's responsibility to ensure the bit time settings are in compliance with the CAN standard.

Table 22-17. CAN Standard Compliant Bit Time Segment Settings

| Time Segment 1   |   Time Segment 2 | Resynchronization Jump Width   |
|------------------|------------------|--------------------------------|
| 5 .. 10          |                2 | 1 .. 2                         |
| 4 .. 11          |                3 | 1 .. 3                         |
| 5 .. 12          |                4 | 1 .. 4                         |
| 6 .. 13          |                5 | 1 .. 4                         |
| 7 .. 14          |                6 | 1 .. 4                         |
| 8 .. 15          |                7 | 1 .. 4                         |
| 9 .. 16          |                8 | 1 .. 4                         |

## 22.4.5.5 Arbitration and Matching Timing

During normal transmission or reception of frames, the arbitration, match, move in and move out processes are executed during certain time windows inside the CAN frame, as shown in Figure 22-14. When doing matching and arbitration, FlexCAN2 needs to span the whole message buffer memory during the available time slot. In order to have sufficient time to do that, the following restrictions must be observed:

- · A valid CAN bit timing must be programmed, as indicated in Figure 22-14.
- · The system clock frequency cannot be smaller than the oscillator clock frequency, i.e. the PLL cannot be programmed to divide down the oscillator clock.
- · There must be a minimum ratio of 16 between the system clock frequency and the CAN bit rate.

Figure 22-14. Arbitration, Match and Move Time Windows

<!-- image -->

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## 22.4.6 Modes of Operation Details

## 22.4.6.1 Freeze Mode

This mode is entered by asserting the HALT bit in the CAN x \_MCR or when the MCU is put into debug mode. In both cases it is also necessary that the FRZ bit is asserted in the CAN x \_MCR. When freeze mode is requested during transmission or reception, FlexCAN2 does the following:

- · Waits to be in either intermission, passive error, bus off or idle state
- · Waits for all internal activities like move in or move out to finish
- · Ignores the RX input pin and drives the TX pin as recessive
- · Stops the prescaler, thus halting all CAN protocol activities
- · Grants write access to the CAN x \_ECR, which is read-only in other modes
- · Sets the NOTRDY and FRZACK bits in CAN \_MCR x

After requesting freeze mode, the user must wait for the FRZACK bit to be asserted in CAN x \_MCR before executing any other action, otherwise FlexCAN2 can operate in an unpredictable way. In freeze mode, all memory mapped registers are accessible.

Exiting freeze mode is done in one of the following ways:

- · CPU negates the FRZ bit in the CAN x \_MCR.
- · The MCU exits debug mode and/or the HALT bit is negated.

Once out of freeze mode, FlexCAN2 tries to re-synchronize to the CAN bus by waiting for 11 consecutive recessive bits.

## 22.4.6.2 Module Disabled Mode

This low power mode is entered when the CAN \_MCR[MDIS] bit is asserted. If the module is disabled x during freeze mode,  it shuts down  the clocks to the CPI  and MBM  sub-modules,  sets  the CAN \_MCR[MDISACK] bit and negates  the  CAN \_MCR[FRZACK]  bit.  If  the  module  is  disabled x x during transmission or reception, FlexCAN2 does the following:

- · Waits to be in either idle or bus off state, or else waits for the third bit of intermission and then checks it to be recessive
- · Waits for all internal activities like move in or move out to finish
- · Ignores its RX input pin and drives its TX pin as recessive
- · Shuts down the clocks to the CPI and MBM sub-modules
- · Sets the NOTRDY and MDISACK bits in CAN \_MCR x

The bus interface unit continues to operate, enabling the CPU to access memory mapped registers except the free running timer, the CAN x \_ECR and the message buffers, which cannot be accessed when the module is disabled. Exiting from this mode is done by negating the CAN x \_MCR[MDIS] bit, which will resume the clocks and negate the CAN x \_MCR[MDISACK] bit.

## 22.4.7 Interrupts

The module can generate interrupts from 20 interrupt sources (16 interrupts due to message buffers, two interrupts  due  to  bus  off  and  error  conditions  and  two  interrupts  for  the  OR'd  MB16-MB31  and MB32-63).

Each  of  the  64  message  buffers  can  be  an  interrupt  source,  if  its  corresponding  CAN x \_IMRH  or CAN \_IMRL bit is set. There is no distinction between TX and RX interrupts for a particular buffer, under x

the assumption that the buffer is initialized for either transmission or reception. Each of the buffers has assigned a flag bit in the CAN x \_IFRH or CAN \_IFRL registers. The bit is set when the corresponding x buffer completes a successful transmission/reception and is cleared when the CPU writes it to 1.

A combined interrupt for each of two MB groups, MB16-MB31 and MB32-MB63, is also generated by an OR of all the interrupt sources from the associated MBs. This interrupt gets generated when any of the MBs generates an interrupt. In this case the CPU must read the CAN x \_IFRH and CAN \_IFRL registers x to determine which MB caused the interrupt.

The other two interrupt sources (bus off and error) generate interrupts like the MB interrupt sources, and can be read from CAN \_ESR. The bus off and error interrupt mask bits are located in the CAN x x \_CR.

## 22.4.8 Bus Interface

The CPU access to FlexCAN2 registers are subject to the following rules:

- · Read and write access to unimplemented or reserved address space also results in access error. Any access to unimplemented MB locations results in access error.
- · For a FlexCAN2 configuration that uses less than the total number of MBs and MAXMB is set accordingly, the remaining MB space can be used as general-purpose RAM space. Byte, word and long word accesses are allowed to the unused MB space.

## 22.5 Initialization/Application Information

This section provides instructions for initializing the FlexCAN2 module.

## 22.5.1 FlexCAN2 Initialization Sequence

The FlexCAN2 module can be reset in three ways:

- · MCU-level hard reset, which resets all memory mapped registers asynchronously
- · MCU-level soft reset, which resets some of the memory mapped registers synchronously (refer to Table 22-2 to see what registers are affected by soft reset)
- · SOFTRST bit in CAN \_MCR, which has the same effect as the MCU level soft reset x

Soft  reset  is  synchronous  and  has  to  follow  an  internal  request/acknowledge  procedure  across  clock domains. Therefore,  it  may  take  some  time  to  fully  propagate  its  effects.  The  SOFTRST  bit  remains asserted while soft reset is pending, so software can poll this bit to know when the reset has completed.

After the module is enabled (CAN x \_MCR[MDIS] bit negated), FlexCAN2 should be put into freeze mode before doing any configuration. In freeze mode, FlexCAN2 is un-synchronized to the CAN bus, the HALT and FRZ bits in CAN \_MCR are set, the internal state machines are disabled and the FRZACK and x NOTRDY bits in the CAN \_MCR are set. The CNTX pin is in recessive state and FlexCAN2 does not x initiate  frame  transmission  nor  receives  any  frames  from  the  CAN  bus.  Note  that  the  message  buffer contents are not affected by reset, so they are not automatically initialized.

For any configuration change/initialization, it is required that FlexCAN2 is put into freeze mode (see Section 22.4.6.1,  'Freeze  Mode). The following is a generic initialization sequence applicable for the FlexCAN2 module:

- · Initialize CANx\_CR.
- - Determine bit timing parameters: PROPSEG, PSEG1, PSEG2, RJW.
- - Determine the bit rate by programming the PRESDIV field.
- - Determine internal arbitration mode (LBUF bit).

## FlexCAN2 Controller Area Network

- · Initialize message buffers.
- - The control and status word of all message buffers may be written either as active or inactive.
- - Other entries in each message buffer should be initialized as required.
- · Initialize CANx\_RXGMASK, CANx\_RX14MASK, and CANx\_RX15MASK registers for acceptance mask as needed.
- · Set required mask bits in CAN x \_IMRH and CAN \_IMRL registers (for all MBs interrupts), and x in CAN \_CR (for bus off and error interrupts). x
- · Negate the CAN \_MCR[HALT] bit. x

Starting with this last event, FlexCAN2 attempts to synchronize with the CAN bus.

## 22.5.2 FlexCAN2 Addressing and RAM Size

There are 1024 bytes of RAM for a maximum of 64 message buffers.  The user can program the maximum number of message buffers (MBs) using the MAXMB field in the CAN \_MCR.  For this 1024-byte RAM x configuration, MAXMB can be any number from 0 63. -

## 22.6 Revision History

Substantive Changes since Rev 3.0

No changes.
