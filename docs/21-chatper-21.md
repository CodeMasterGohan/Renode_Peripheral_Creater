### Chatper 21

## Enhanced Serial Communication Interface (eSCI)

## 21.1 Introduction

This section gives an overview of the MPC5553/MPC5554's eSCI module, and presents a block diagram, its features and its modes of operation.

## 21.1.1 Block Diagram

Figure 21-1. eSCI Block Diagram

<!-- image -->

## 21.1.2 Overview

The eSCI allows asynchronous serial communications with peripheral devices and other CPUs. The eSCI has special features which allow the eSCI to operate as a LIN bus master, complying with the LIN 2.0 specification.

Enhanced Serial Communication Interface (eSCI)

Each of the eSCI modules can be independently disabled by writing to the module disable (MDIS) bit in the module's control register 2 (ESCI x \_CR2). Disabling the module turns off the clock to the module, although some of the module registers may be accessed by the core via the slave bus. The MDIS bit is intended to be used when the module is not required in the application.

## 21.1.3 Features

The eSCI includes these distinctive features:

- · Full-duplex operation
- · Standard mark/space non-return-to-zero (NRZ) format
- · Configurable baud rate
- · Programmable 8-bit or 9-bit data format
- · LIN master node support
- · Configurable CRC detection for LIN
- · Separately enabled transmitter and receiver
- · Programmable transmitter output parity
- · Two receiver wake-up methods:
- - Idle line wake-up
- - Address mark wake-up
- · Interrupt-driven operation
- · Receiver framing error detection
- · Hardware parity checking
- · 1/16 bit-time noise detection
- · Two-channel DMA interface

## 21.1.4 Modes of Operation

The eSCI functions the same in normal, special, and emulation modes. It has a low-power module disable mode.

## 21.2 External Signal Description

This section provides a description of all module signals external to the MCU.

## 21.2.1 Overview

Each eSCI module has two I/O signals connected to the external MCU pins. These signals are summarized in Table 21-1 and described in more detail in the following sections.

Table 21-1. eSCI Signals

| Signal Name 1   | I/O   | Description   |
|-----------------|-------|---------------|
| RXD x           | I     | eSCI Receive  |
| TXD x           | O     | eSCI Transmit |

1 x indicates eSCI module A or B

## 21.2.2 Detailed Signal Description

## 21.2.2.1 SCI Transmit (TXD x )

This pin serves as transmit data output of eSCI.

## 21.2.2.2 SCI Receive Pin (RXD x )

This pin serves as receive data input of the eSCI.

## 21.3 Memory Map/Register Definition

## 21.3.1 Overview

This section provides a detailed description of all memory and registers.

## 21.3.2 Module Memory Map

The memory map for the eSCI module is given below in Table 21-2. The address offset is listed for each register.  The  total  address  for  each  register  is  the  sum  of  the  base  address  for  the  eSCI  module (ESCI \_base)  and x the address offset for each register. There are two eSCI  modules  on  the MPC5553/MPC5554: the base is 0xFFFB\_0000 for eSCIA and 0xFFFB\_4000 for eSCIB.

Table 21-2. Module Memory Map

| Address                              | Register Name   | Register Description    |   Size (bits) |
|--------------------------------------|-----------------|-------------------------|---------------|
| Base 0xFFFB_0000 (A) 0xFFFB_4000 (B) | ESCI x _CR1     | eSCI control register 1 |            32 |
| Base + 0x04                          | ESCI x _CR2     | eSCI control register 2 |            16 |
| Base + 0x06                          | ESCI x _DR      | eSCI data register      |            16 |

Table 21-2. Module Memory Map (continued)

| Address     | Register Name   | Register Description                            |   Size (bits) |
|-------------|-----------------|-------------------------------------------------|---------------|
| Base + 0x08 | ESCI x _SR      | eSCI status register                            |            32 |
| Base + 0x0C | ESCI x _LCR     | LIN control register                            |            32 |
| Base + 0x10 | ESCI x _LTR     | LIN transmit register                           |            32 |
| Base + 0x14 | ESCI x _LRR     | LIN receive register                            |            32 |
| Base + 0x18 | ESCI x _LPR     | LIN cyclic redundancy check polynomial register |            32 |

## 21.3.3 Register Definition

This section consists of register descriptions in address order. Each description includes a standard register diagram with an associated figure number. Details of register bit and field function follow the register diagrams, in bit order.

## 21.3.3.1 eSCI Control Register 1 (ESCI x \_CR1)

Figure 21-2. eSCI Control Register 1 (ESCI x \_CR1)

<!-- image -->

|          | 0          | 1          | 2          | 3          | 4          | 5          | 6          | 7          | 8          | 9          | 10         | 11         | 12         | 13         | 14         | 15         |
|----------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|
| R        | 0          | 0          | 0          | SBR        | SBR        | SBR        | SBR 3      | SBR 4      | SBR 5      | SBR        | SBR 7      | SBR 8      | SBR 9      | SBR 10     | SBR 11     | SBR        |
| W        |            |            |            | 0          | 1          | 2          |            |            |            | 6          |            |            |            |            |            | 12         |
| Reset    | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 1          | 0          | 0          |
| Reg Addr | Base + 0x0 | Base + 0x0 | Base + 0x0 | Base + 0x0 | Base + 0x0 | Base + 0x0 | Base + 0x0 | Base + 0x0 | Base + 0x0 | Base + 0x0 | Base + 0x0 | Base + 0x0 | Base + 0x0 | Base + 0x0 | Base + 0x0 | Base + 0x0 |
|          | 16         | 17         | 18         | 19         | 20         | 21         | 22         | 23         | 24         | 25         | 26         | 27         | 28         | 29         | 30         | 31         |
| R        | LOOPS      | 0          | RSRC       | M          | WAKE       | ILT        | PE         | PT         | TIE        | TCIE       | RIE        | ILIE       | TE         | RE         | RWU        | SBK        |
| W        |            |            |            |            |            |            |            |            |            |            |            |            |            |            |            |            |
| Reset    | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          |
| Reg Addr | Base + 0x0 | Base + 0x0 | Base + 0x0 | Base + 0x0 | Base + 0x0 | Base + 0x0 | Base + 0x0 | Base + 0x0 | Base + 0x0 | Base + 0x0 | Base + 0x0 | Base + 0x0 | Base + 0x0 | Base + 0x0 | Base + 0x0 | Base + 0x0 |

Table 21-3. ESCI x \_CR1 Field Descriptions

| Bits   | Name   | Description                                                                                                                                                                                                                                                                                                                                                                                                                |
|--------|--------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-2    | -      | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                  |
| 3-15   | SBR n  | SCI baud rate. Used by the counter to determine the baud rate of the eSCI. The formula for calculating the baud rate is: where BR is the content of the eSCI control register 1 (ESCI x _CR1), bits SBR0-SBR12. SBR0-SBR12 can contain a value from 1 to 8191. Also refer to the ESCIx_LCR[WU] bit description on page 21-13. SCI baud rate eSCI system clock 16 BR × ------------------------- ------------------------ = |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## Table 21-3. ESCI x \_CR1 Field Descriptions

|   Bits | Name   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
|--------|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|     16 | LOOPS  | Loop select. Enables loop operation. In loop operation, the RXD pin is disconnected from the eSCI and the transmitter output is internally connected to the receiver input. Both the transmitter and the receiver must be enabled to use the loop function. 0 Normal operation enabled, loop operation disabled 1 Loop operation enabled Note: The receiver input is determined by the RSRC bit.                                                                                                                                                     | Loop select. Enables loop operation. In loop operation, the RXD pin is disconnected from the eSCI and the transmitter output is internally connected to the receiver input. Both the transmitter and the receiver must be enabled to use the loop function. 0 Normal operation enabled, loop operation disabled 1 Loop operation enabled Note: The receiver input is determined by the RSRC bit.                                                                                                                                                     | Loop select. Enables loop operation. In loop operation, the RXD pin is disconnected from the eSCI and the transmitter output is internally connected to the receiver input. Both the transmitter and the receiver must be enabled to use the loop function. 0 Normal operation enabled, loop operation disabled 1 Loop operation enabled Note: The receiver input is determined by the RSRC bit.                                                                                                                                                     |
|     17 | -      | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
|     18 | RSRC   | Receiver source. When LOOPS = 1, the RSRC bit determines the source for the receiver shift register input. 0 Receiver input internally connected to transmitter output 1 Receiver input connected externally to transmitter The table below shows how LOOPS and RSRC determine the loop function of the eSCI.                                                                                                                                                                                                                                        | Receiver source. When LOOPS = 1, the RSRC bit determines the source for the receiver shift register input. 0 Receiver input internally connected to transmitter output 1 Receiver input connected externally to transmitter The table below shows how LOOPS and RSRC determine the loop function of the eSCI.                                                                                                                                                                                                                                        | Receiver source. When LOOPS = 1, the RSRC bit determines the source for the receiver shift register input. 0 Receiver input internally connected to transmitter output 1 Receiver input connected externally to transmitter The table below shows how LOOPS and RSRC determine the loop function of the eSCI.                                                                                                                                                                                                                                        |
|     18 | RSRC   | LOOPS                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | RSRC                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Function                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
|     18 | RSRC   | 0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | x                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | Normal operation                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
|     18 | RSRC   | 1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | 0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | Loop mode with RXDinput internally connected to TXDoutput                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
|     18 | RSRC   | 1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | 1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | Single-wire mode with RXD input connected to TXD                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
|     19 | M      | Data format mode. Determines whether data characters are 8 or 9 bits long. 0 1 start bit, 8 data bits, 1 stop bit                                                                                                                                                                                                                                                                                                                                                                                                                                    | Data format mode. Determines whether data characters are 8 or 9 bits long. 0 1 start bit, 8 data bits, 1 stop bit                                                                                                                                                                                                                                                                                                                                                                                                                                    | Data format mode. Determines whether data characters are 8 or 9 bits long. 0 1 start bit, 8 data bits, 1 stop bit                                                                                                                                                                                                                                                                                                                                                                                                                                    |
|     20 | WAKE   | Wake-up condition. Determines which condition wakes up the eSCI: a logic 1 (address mark) in the most significant bit position of a received data character or an idle condition on the RXD. 0 Idle line wake-up 1 Address mark wake-up                                                                                                                                                                                                                                                                                                              | Wake-up condition. Determines which condition wakes up the eSCI: a logic 1 (address mark) in the most significant bit position of a received data character or an idle condition on the RXD. 0 Idle line wake-up 1 Address mark wake-up                                                                                                                                                                                                                                                                                                              | Wake-up condition. Determines which condition wakes up the eSCI: a logic 1 (address mark) in the most significant bit position of a received data character or an idle condition on the RXD. 0 Idle line wake-up 1 Address mark wake-up                                                                                                                                                                                                                                                                                                              |
|     21 | ILT    | Idle line type. Determines when the receiver starts counting logic 1s as idle character bits. The counting begins either after the start bit or after the stop bit. If the count begins after the start bit, then a string of logic 1s preceding the stop bit may cause false recognition of an idle character. Beginning the count after the stop bit avoids false idle character recognition, but requires properly synchronized transmissions. 0 Idle character bit count begins after start bit 1 Idle character bit count begins after stop bit | Idle line type. Determines when the receiver starts counting logic 1s as idle character bits. The counting begins either after the start bit or after the stop bit. If the count begins after the start bit, then a string of logic 1s preceding the stop bit may cause false recognition of an idle character. Beginning the count after the stop bit avoids false idle character recognition, but requires properly synchronized transmissions. 0 Idle character bit count begins after start bit 1 Idle character bit count begins after stop bit | Idle line type. Determines when the receiver starts counting logic 1s as idle character bits. The counting begins either after the start bit or after the stop bit. If the count begins after the start bit, then a string of logic 1s preceding the stop bit may cause false recognition of an idle character. Beginning the count after the stop bit avoids false idle character recognition, but requires properly synchronized transmissions. 0 Idle character bit count begins after start bit 1 Idle character bit count begins after stop bit |
|     22 | PE     | Parity enable. Enables the parity function. When enabled, the parity function inserts a parity bit in the most significant bit position of the transmitted word. During reception, the received parity bit will be verified in the most significant bit position. The received parity bit will not be masked out. 0 Parity function disabled                                                                                                                                                                                                         | Parity enable. Enables the parity function. When enabled, the parity function inserts a parity bit in the most significant bit position of the transmitted word. During reception, the received parity bit will be verified in the most significant bit position. The received parity bit will not be masked out. 0 Parity function disabled                                                                                                                                                                                                         | Parity enable. Enables the parity function. When enabled, the parity function inserts a parity bit in the most significant bit position of the transmitted word. During reception, the received parity bit will be verified in the most significant bit position. The received parity bit will not be masked out. 0 Parity function disabled                                                                                                                                                                                                         |

Table 21-3. ESCI x \_CR1 Field Descriptions

|   Bits | Name   | Description                                                                                                                                                                                                                                                                                                                                                  |
|--------|--------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|     23 | PT     | Parity type. Determines whether the eSCI generates and checks for even parity or odd parity. With even parity, an even number of 1s clears the parity bit and an odd number of 1s sets the parity bit. With odd parity, an odd number of 1s clears the parity bit and an even number of 1s sets the parity bit. 0 Even parity 1 Odd parity                   |
|     24 | TIE    | Transmitter interrupt enable. Enables the transmit data register empty flag ESCI x _SR[TDRE] to generate interrupt requests. The interrupt is suppressed in TX DMA mode. 0 TDRE interrupt requests disabled 1 TDRE interrupt requests enabled                                                                                                                |
|     25 | TCIE   | Transmission complete interrupt enable. Enables the transmission complete flag ESCIx_SR[TC] to generate interrupt requests. The interrupt is suppressed in TX DMA mode. 0 TC interrupt requests disabled 1 TC interrupt requests enabled                                                                                                                     |
|     26 | RIE    | Receiver full interrupt enable. Enables the receive data register full flag ESCIx_SR[RDRF] and the overrun flag ESCIx_SR[OR] to generate interrupt requests. The interrupt is suppressed in RX DMA mode. 0 RDRF and OR interrupt requests disabled 1 RDRF and OR interrupt requests enabled                                                                  |
|     27 | ILIE   | Idle line interrupt enable. Enables the idle line flag ESCIx_SR[IDLE] to generate interrupt requests. 0 IDLE interrupt requests disabled 1 IDLE interrupt requests enabled                                                                                                                                                                                   |
|     28 | TE     | Transmitter enable. Enables the eSCI transmitter and configures the TXD pin as being controlled by the eSCI. The TE bit can be used to queue an idle preamble. 0 Transmitter disabled 1 Transmitter enabled                                                                                                                                                  |
|     29 | RE     | Receiver enable. Enables the eSCI receiver. 0 Receiver disabled 1 Receiver enabled                                                                                                                                                                                                                                                                           |
|     30 | RWU    | Receiver wake-up. Standby state. 0 Normal operation. 1 RWU enables the wake-up function and inhibits further receiver interrupt requests. Normally, hardware wakes the receiver by automatically clearing RWU.                                                                                                                                               |
|     31 | SBK    | Send break. Toggling SBK sends one break character (see the description of ESCI x _CR2[BRK13] for break character length). Toggling implies clearing the SBK bit before the break character has finished transmitting. As long as SBK is set, the transmitter continues to send complete break characters. 0 No break characters 1 Transmit break characters |

## NOTES

After reset, the baud rate generator is disabled until the TE bit or the RE bit is set for the first time.

The baud rate generator is disabled when SBR0-SBR12 = 0x0.

Normally the baud rate should be written with a single write. If 8-bit writes are  used,  writing  to  ESCI x \_CR1[0-7]  has  no  effect  without  writing  to ESCI \_CR1[8-15], since writing to ESCI \_CR1[0-7] puts the data in a x x temporary location until ESCI x \_CR1[8-15] is written to.

During reception, when parity is enabled, the received parity bit will appear in the data register.

## 21.3.3.2 eSCI Control Register 2 (ESCI x \_CR2)

## NOTE

DMA requests are negated when in module disable mode.

Figure 21-3. eSCI Control Register 2 (ESCIx\_CR2)

<!-- image -->

Table 21-4. ESCI x \_CR2 Field Description

|   Bits | Name   | Description                                                                                                                                                                                                                                                           |
|--------|--------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|      0 | MDIS   | Module disable. By default the module is enabled, but can be disabled by writing a 1 to this bit. DMA requests are negated if the device is in module disable mode. 0 Module enabled 1 Module disabled                                                                |
|      1 | FBR    | Fast bit error detection. Handles bit error detection on a per bit basis. If this is not enabled, bit errors will be detected on a per byte basis.                                                                                                                    |
|      2 | BSTP   | Bit error/physical bus error stop. Causes DMA TX requests to be suppressed, as long as the bit error and physical bus error flags are not cleared. This stops further DMA writes, which would otherwise cause data bytes to be interpreted as LIN header information. |
|      3 | IEBERR | Enable bit error interrupt. Generates an interrupt, when a LIN bit error is detected. For a list of interrupt enables and flags, see Table 21-21.                                                                                                                     |
|      4 | RXDMA  | Activate RX DMAchannel. If this bit is enabled and the eSCI has received data, it will raise a DMA RX request.                                                                                                                                                        |
|      5 | TXDMA  | Activate TX DMA channel. Whenever the eSCI is able to transmit data, it will raise a DMA TX request.                                                                                                                                                                  |

<!-- image -->

Table 21-4. ESCI x \_CR2 Field Description (continued)

| Bits   | Name   | Description                                                                                                                                                                                                                                                    | Description                                                                                                                                                                                                                                                    | Description                                                                                                                                                                                                                                                    | Description                                                                                                                                                                                                                                                    |
|--------|--------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 6      | BRK13  | Break transmit character length. Determines whether the transmit break character is 10/11 or 13/14 bits long. The detection of a framing error is not affected by this bit.                                                                                    | Break transmit character length. Determines whether the transmit break character is 10/11 or 13/14 bits long. The detection of a framing error is not affected by this bit.                                                                                    | Break transmit character length. Determines whether the transmit break character is 10/11 or 13/14 bits long. The detection of a framing error is not affected by this bit.                                                                                    | Break transmit character length. Determines whether the transmit break character is 10/11 or 13/14 bits long. The detection of a framing error is not affected by this bit.                                                                                    |
| 6      | BRK13  |                                                                                                                                                                                                                                                                |                                                                                                                                                                                                                                                                |                                                                                                                                                                                                                                                                | ESCI x _CR1[M]                                                                                                                                                                                                                                                 |
| 6      | BRK13  |                                                                                                                                                                                                                                                                |                                                                                                                                                                                                                                                                |                                                                                                                                                                                                                                                                | 1                                                                                                                                                                                                                                                              |
| 6      | BRK13  |                                                                                                                                                                                                                                                                | BRK13                                                                                                                                                                                                                                                          | 0                                                                                                                                                                                                                                                              | 11                                                                                                                                                                                                                                                             |
| 6      | BRK13  | 0 Break Character is 10 or 11 bits long 1 Break character is 13 or 14 bits long Note: LIN 2.0 now requires that a break character is always 13 bits long, so this bit should always be set to 1. The eSCI will work with BRK13=0, but it will violate LIN 2.0. | 0 Break Character is 10 or 11 bits long 1 Break character is 13 or 14 bits long Note: LIN 2.0 now requires that a break character is always 13 bits long, so this bit should always be set to 1. The eSCI will work with BRK13=0, but it will violate LIN 2.0. | 0 Break Character is 10 or 11 bits long 1 Break character is 13 or 14 bits long Note: LIN 2.0 now requires that a break character is always 13 bits long, so this bit should always be set to 1. The eSCI will work with BRK13=0, but it will violate LIN 2.0. | 0 Break Character is 10 or 11 bits long 1 Break character is 13 or 14 bits long Note: LIN 2.0 now requires that a break character is always 13 bits long, so this bit should always be set to 1. The eSCI will work with BRK13=0, but it will violate LIN 2.0. |
| 7      | -      | Reserved. This bit is readable/writable, but has no effect on the operation of the eSCI module.                                                                                                                                                                | Reserved. This bit is readable/writable, but has no effect on the operation of the eSCI module.                                                                                                                                                                | Reserved. This bit is readable/writable, but has no effect on the operation of the eSCI module.                                                                                                                                                                | Reserved. This bit is readable/writable, but has no effect on the operation of the eSCI module.                                                                                                                                                                |
| 8      | BESM13 | Bit error sample mode, bit 13. Determines when to sample the incoming bit in order to detect a bit error. (This is only relevant when FBR is set.) 0 Sample at RT clock 9 1 Sample at RT clock 13 (see Section 21.4.5.3, 'Data Sampling')                      | Bit error sample mode, bit 13. Determines when to sample the incoming bit in order to detect a bit error. (This is only relevant when FBR is set.) 0 Sample at RT clock 9 1 Sample at RT clock 13 (see Section 21.4.5.3, 'Data Sampling')                      | Bit error sample mode, bit 13. Determines when to sample the incoming bit in order to detect a bit error. (This is only relevant when FBR is set.) 0 Sample at RT clock 9 1 Sample at RT clock 13 (see Section 21.4.5.3, 'Data Sampling')                      | Bit error sample mode, bit 13. Determines when to sample the incoming bit in order to detect a bit error. (This is only relevant when FBR is set.) 0 Sample at RT clock 9 1 Sample at RT clock 13 (see Section 21.4.5.3, 'Data Sampling')                      |
| 9      | SBSTP  | SCI bit error stop. Stops the SCI when a bit error is asserted. This allows to stop driving the LIN bus quickly after a bit error has been detected. 0 Byte is completely transmitted 1 Byte is partially transmitted                                          | SCI bit error stop. Stops the SCI when a bit error is asserted. This allows to stop driving the LIN bus quickly after a bit error has been detected. 0 Byte is completely transmitted 1 Byte is partially transmitted                                          | SCI bit error stop. Stops the SCI when a bit error is asserted. This allows to stop driving the LIN bus quickly after a bit error has been detected. 0 Byte is completely transmitted 1 Byte is partially transmitted                                          | SCI bit error stop. Stops the SCI when a bit error is asserted. This allows to stop driving the LIN bus quickly after a bit error has been detected. 0 Byte is completely transmitted 1 Byte is partially transmitted                                          |
| 10-11  | -      | Reserved.                                                                                                                                                                                                                                                      | Reserved.                                                                                                                                                                                                                                                      | Reserved.                                                                                                                                                                                                                                                      | Reserved.                                                                                                                                                                                                                                                      |
| 12     | ORIE   | Overrun error interrupt enable. Generates an interrupt, when a frame error is detected. For a list of interrupt enables and flags, see Table 21-21.                                                                                                            | Overrun error interrupt enable. Generates an interrupt, when a frame error is detected. For a list of interrupt enables and flags, see Table 21-21.                                                                                                            | Overrun error interrupt enable. Generates an interrupt, when a frame error is detected. For a list of interrupt enables and flags, see Table 21-21.                                                                                                            | Overrun error interrupt enable. Generates an interrupt, when a frame error is detected. For a list of interrupt enables and flags, see Table 21-21.                                                                                                            |
| 13     | NFIE   | Noise flag interrupt enable. Generates an interrupt, when noise flag is set. For a list of interrupt enables and flags, see Table 21-21.                                                                                                                       | Noise flag interrupt enable. Generates an interrupt, when noise flag is set. For a list of interrupt enables and flags, see Table 21-21.                                                                                                                       | Noise flag interrupt enable. Generates an interrupt, when noise flag is set. For a list of interrupt enables and flags, see Table 21-21.                                                                                                                       | Noise flag interrupt enable. Generates an interrupt, when noise flag is set. For a list of interrupt enables and flags, see Table 21-21.                                                                                                                       |
| 14     | FEIE   | Frame error interrupt enable. Generates an interrupt, when a frame error is detected. For a list of interrupt enables and flags, see Table 21-21.                                                                                                              | Frame error interrupt enable. Generates an interrupt, when a frame error is detected. For a list of interrupt enables and flags, see Table 21-21.                                                                                                              | Frame error interrupt enable. Generates an interrupt, when a frame error is detected. For a list of interrupt enables and flags, see Table 21-21.                                                                                                              | Frame error interrupt enable. Generates an interrupt, when a frame error is detected. For a list of interrupt enables and flags, see Table 21-21.                                                                                                              |
| 15     | PFIE   | Parity flag interrupt enable. Generates an interrupt, when parity flag is set. For a list of interrupt enables and flags, see Table 21-21.                                                                                                                     | Parity flag interrupt enable. Generates an interrupt, when parity flag is set. For a list of interrupt enables and flags, see Table 21-21.                                                                                                                     | Parity flag interrupt enable. Generates an interrupt, when parity flag is set. For a list of interrupt enables and flags, see Table 21-21.                                                                                                                     | Parity flag interrupt enable. Generates an interrupt, when parity flag is set. For a list of interrupt enables and flags, see Table 21-21.                                                                                                                     |

## 21.3.3.3 eSCI Data Register (ESCI x \_DR)

Figure 21-4. eSCI Data Register (ESCI x \_DR)

<!-- image -->

## Table 21-5. ESCI x \_DR Field Description

| Bits   | Name          | Description                                                                                                                                                                                                                                                                 |
|--------|---------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0      | R8            | Received bit 8. R8 is the ninth data bit received when the eSCI is configured for 9-bit data format (M = 1).                                                                                                                                                                |
| 1      | T8            | Transmit bit 8. T8 is the ninth data bit transmitted when the eSCI is configured for 9-bit data format (M = 1). Note: If the value of T8 is the same as in the previous transmission, T8 does not have to be rewritten.The same value is transmitted until T8 is rewritten. |
| 2-7    | -             | Reserved.                                                                                                                                                                                                                                                                   |
| 8-15   | R7-R0 / T7-T0 | Received bits/transmit bits 7-0 for 9-bit or 8-bit formats. Bits 7-0 from SCI communication may be read from ESCI x _DR[8-15] (provided that SCI communication was successful). Writing to ESCI x _DR [8-15] provides bits 7-0 for SCI transmission.                        |

## NOTES

In 8-bit data format, only bits 8-15 of ESCI x \_DR need to be accessed.

When transmitting in 9-bit data format and using 8-bit write instructions, write first to ESCI \_DR[0-7], x then ESCI \_DR[8-15]. x For 9-bit transmissions, a single write may also be used.

ESCI \_DR should  not  be  used  in  LIN  mode,  writes  to  this  register  are x blocked in LIN mode.

Even if parity generation/checking is enabled via ESCIx\_CR[PE], the parity bit will not be masked out.

## 21.3.3.4 eSCI Status Register (ESCI x \_SR)

The ESCI \_SR indicates the current status. The status flags can be polled, and some can also be used to x generate interrupts. All bits in ESCI x \_SR except for RAF are cleared by writing 1 to them.

Figure 21-5. eSCI Status Register (ESCI x \_SR)

|          | 0          | 1          | 2          | 3          | 4          | 5          | 6          | 7          | 8          | 9          | 10         | 11         | 12         | 13         | 14         | 15         |
|----------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|
| R        | TDRE       | TC         | RDRF       | IDLE       | OR         | NF         | FE         | PF         | 0          | 0          | 0          | BERR       | 0          | 0          | 0          | RAF        |
| W        | w1c        | w1c        | w1c        | w1c        | w1c        | w1c        | w1c        | w1c        |            |            |            | w1c        |            |            |            |            |
| Reset    | 1          | 1          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          |
| Reg Addr | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 |
|          | 16         | 17         | 18         | 19         | 20         | 21         | 22         | 23         | 24         | 25         | 26         | 27         | 28         | 29         | 30         | 31         |
| R        | RXRDY      | TXRDY      | LWAKE      | STO        | PBERR      | CERR       | CKERR      | FRC        | 0          | 0          | 0          | 0          | 0          | 0          | 0          | OVFL       |
| W        | w1c        | w1c        | w1c        | w1c        | w1c        | w1c        | w1c        | w1c        |            |            |            |            |            |            |            | w1c        |
| Reset    | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          |
| Reg Addr | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 |

Table 21-6. ESCI x \_SR Field Descriptions

|   Bits | Name   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
|--------|--------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|      0 | TDRE   | Transmit data register empty flag. TDRE is set when the transmit shift register receives a byte from the eSCI data register. When TDRE is 1, the data register (ESCI x _DR) is empty and can receive a new value to transmit. Clear TDRE by writing 1 to it. 0 No byte transferred to transmit shift register 1 Byte transferred to transmit shift register; transmit data register empty                                                                                                                                                                                                                                                                                                               |
|      1 | TC     | Transmit complete flag. TC is set low when there is a transmission in progress or when a preamble or break character is loaded. TC is set high when the TDRE flag is set and no data, preamble, or break character is being transmitted. When TC is set, the TXDout signal becomes idle (logic 1). After the device is switched on (by clearing the MDIS bit, see Section 21.3.3.2, 'eSCI Control Register 2 (ESCIx_CR2),' a preamble is transmitted; if no byte is written to the the SCI data register then the completion of the preamble can be monitored using the TC flag. Clear TC by writing 1 to it. 0 Transmission in progress 1 No transmission in progress. Indicates that TXD out is idle. |
|      2 | RDRF   | Receive data register full flag. RDRF is set when the data in the receive shift register transfers to the eSCI data register. Clear RDRF by writing 1 to it. 0 Data not available in eSCI data register 1 Received data available in eSCI data register                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|      3 | IDLE   | Idle line flag. IDLE is set when 10 consecutive logic 1s (if M=0) or 11 consecutive logic 1s (if M=1) appear on the receiver input. Once the IDLE flag is cleared, a valid frame must again set the RDRF flag before an idle condition can set the IDLE flag. Clear IDLE by writing 1 to it. 0 Receiver input is either active now or has never become active since the IDLE flag was last cleared 1 Receiver input has become idle Note: When the receiver wake-up bit (RWU) is set, an idle line condition does not set the IDLE flag.                                                                                                                                                                |

Table 21-6. ESCI x \_SR Field Descriptions (continued)

| Bits   | Name   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|--------|--------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 4      | OR     | Overrun flag. OR is set when software fails to read the eSCI data register before the receive shift register receives the next frame. The ORbit is set immediately after the stop bit has been completely received for the second frame. The data in the shift register is lost, but the data already in the eSCI data registers is not affected. Clear OR by writing 1 to it. 0 No overrun 1 Overrun                                                                                                                                                                                                                       |
| 5      | NF     | Noise flag. NF is set when the eSCI detects noise on the receiver input. NF bit is set during the same cycle as the RDRF flag but does not get set in the case of an overrun. Clear NF by writing 1 to it. 0 No noise 1 Noise                                                                                                                                                                                                                                                                                                                                                                                               |
| 6      | FE     | Framing error flag. FE is set when a logic 0 is accepted as the stop bit. FE bit is set during the same cycle as the RDRF flag but does not get set in the case of an overrun. Clear FE by writing 1 to it. 0 No framing error 1 Framing error                                                                                                                                                                                                                                                                                                                                                                              |
| 7      | PF     | Parity error flag. PF is set when the parity enable bit, PE, is set and the parity of the received data does not match its parity bit. Clear PE by writing 1 to it. 0 No parity error 1 Parity error                                                                                                                                                                                                                                                                                                                                                                                                                        |
| 8-10   | -      | Reserved, should be cleared.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| 11     | BERR   | Bit error. Indicates a bit on the bus did not match the transmitted bit. If FBR=0, checking happens after a complete byte has been transmitted and received again. If FBR = 1, checking happens bit by bit. This bit is only used for LIN mode. BERR is also set if an unrequested byte is received (i.e. a byte that is not part of an RX frame) that is not recognized as a wake-up flag. (Because the data on the RX line does not match the idle state that was assigned to the TX line.) Clear BERR by writing 1 to it. Abit error causes the LIN finite state machine (FSM) to reset unless ESCI x _LCR[LDBG] is set. |
| 12-14  | -      | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| 15     | RAF    | Receiver active flag. RAF is set when the receiver detects a logic 0 during the RT1 time period of the start bit search. RAF is cleared when the receiver detects an idle character. 0 No reception in progress. 1 Reception in progress.                                                                                                                                                                                                                                                                                                                                                                                   |
| 16     | RXRDY  | The eSCI has received LIN data. This bit is set when the ESCI x _LCR receives a byte. Clear RXRDY by writing it with 1.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| 17     | TXRDY  | The LIN FSM can accept another write to ESCI x _LTR. This bit is set when the ESCI x _LTR register becomes free. Clear TXRDY by writing it with 1.                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 18     | LWAKE  | Received LIN wake-up signal. A LIN slave has sent a wake-up signal on the bus. When this signal is detected, the LIN FSMwill reset. If the setup of a frame had already started, it therefore must be repeated. LWAKEwill also be set if ESCI receives a LIN 2.0 wake-up signal (in which the baud rate is lower than 32K baud). See the WUbit.                                                                                                                                                                                                                                                                             |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 21-6. ESCI x \_SR Field Descriptions (continued)

| Bits   | Name   | Description                                                                                                                                                                                                                   |
|--------|--------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 19     | STO    | Slave time out. Represents a NO_RESPONSE_ERROR. This is set if a slave does not complete a frame within the specified maximum frame length. For LIN 1.3 the following formula is used: TFRAME_MAX 10 NDATA 44 + × ( ) 1.4 × = |
| 20     | PBERR  | Physical bus error. No valid message can be generated on the bus. This is set if, after the start of a byte transmission, the input remains unchanged for 31 cycles. This will reset the LIN FSM.                             |
| 21     | CERR   | CRC error. The CRC pattern received with an extended frame was not correct. 0 No error 1 CRC error                                                                                                                            |
| 22     | CKERR  | Checksum error. Checksum error on a received frame.                                                                                                                                                                           |
| 23     | FRC    | Frame complete. LIN frame completely transmitted. All LIN data bytes received.                                                                                                                                                |
| 24-30  | -      | Reserved.                                                                                                                                                                                                                     |
| 31     | OVFL   | ESCI x _LRR overflow. The LIN receive register has not been read before a new data byte, CRC, or checksum byte has been received from the LIN bus. Set when the condition is detected, and cleared by writing 1 to it.        |

## 21.3.3.5 LIN Control Register (ESCI x \_LCR)

ESCI \_LCR can be written only when there are no ongoing transmissions. x

Figure 21-6. LIN Control Register (ESCI x \_LCR)

<!-- image -->

|          | 0          | 1          | 2          | 3          | 4          | 5          | 6          | 7          | 8          | 9          | 10         | 11         | 12         | 13         | 14         | 15         |
|----------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|
| R        | LRES       | 0          | WUD0       | WUD1       | LDBG       | DSF        | PRTY       | LIN        | RXIE       | TXIE       | WUIE       | STIE       | PBIE       | CIE        | CKIE       | FCIE       |
| W        |            | WU         |            |            |            |            |            |            |            |            |            |            |            |            |            |            |
| Reset    | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          |
| Reg Addr | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC |
|          | 16         | 17         | 18         | 19         | 20         | 21         | 22         | 23         | 24         | 25         | 26         | 27         | 28         | 29         | 30         | 31         |
| R        | 0          | 0          | 0          | 0          | 0          | 0          | 0          | OFIE       | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          |
| W        |            |            |            |            |            |            |            |            |            |            |            |            |            |            |            |            |
| Reset    | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          |
| Reg Addr | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC |

Table 21-7. ESCI x \_LCR Field Descriptions

| Bits   | Name      | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                         | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                         | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|--------|-----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0      | LRES      | LIN resynchronize. Causes the LIN protocol engine to return to start state. This happens automatically after bit errors, but software may force a return to start state manually via this bit. The bit first must be set then cleared, so that the protocol engine is operational again.                                                                                                                                                                            | LIN resynchronize. Causes the LIN protocol engine to return to start state. This happens automatically after bit errors, but software may force a return to start state manually via this bit. The bit first must be set then cleared, so that the protocol engine is operational again.                                                                                                                                                                            | LIN resynchronize. Causes the LIN protocol engine to return to start state. This happens automatically after bit errors, but software may force a return to start state manually via this bit. The bit first must be set then cleared, so that the protocol engine is operational again.                                                                                                                                                                            |
| 1      | WU        | LIN bus wake-up. Generates a wake-up signal on the LIN bus. This must be set before a transmission, if the bus is in sleep mode. This bit will auto-clear, so a read from this bit will always return 0. According to LIN 2.0, generating a valid wake-up character requires programming the SCI baud rate to a range of 32K baud down to 1.6K baud.                                                                                                                | LIN bus wake-up. Generates a wake-up signal on the LIN bus. This must be set before a transmission, if the bus is in sleep mode. This bit will auto-clear, so a read from this bit will always return 0. According to LIN 2.0, generating a valid wake-up character requires programming the SCI baud rate to a range of 32K baud down to 1.6K baud.                                                                                                                | LIN bus wake-up. Generates a wake-up signal on the LIN bus. This must be set before a transmission, if the bus is in sleep mode. This bit will auto-clear, so a read from this bit will always return 0. According to LIN 2.0, generating a valid wake-up character requires programming the SCI baud rate to a range of 32K baud down to 1.6K baud.                                                                                                                |
| 2-3    | WUD [0:1] | Wake-up delimiter time. Determines how long the LIN engine waits after generating a wake-up signal, before starting a new frame. The eSCI will not set ESCIx_SR[TXRDY] before this time expires. Note that in addition to this delimiter time, the CPU and the eSCI will require some setup time to start a new transmission and typically there is an additional bit time delay. The table below shows how the values for WUD0 and WUD1 affect the delimiter time. | Wake-up delimiter time. Determines how long the LIN engine waits after generating a wake-up signal, before starting a new frame. The eSCI will not set ESCIx_SR[TXRDY] before this time expires. Note that in addition to this delimiter time, the CPU and the eSCI will require some setup time to start a new transmission and typically there is an additional bit time delay. The table below shows how the values for WUD0 and WUD1 affect the delimiter time. | Wake-up delimiter time. Determines how long the LIN engine waits after generating a wake-up signal, before starting a new frame. The eSCI will not set ESCIx_SR[TXRDY] before this time expires. Note that in addition to this delimiter time, the CPU and the eSCI will require some setup time to start a new transmission and typically there is an additional bit time delay. The table below shows how the values for WUD0 and WUD1 affect the delimiter time. |
| 2-3    | WUD [0:1] |                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | WUD0                                                                                                                                                                                                                                                                                                                                                                                                                                                                | WUD1                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| 2-3    | WUD [0:1] |                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | 0                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | 0                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| 2-3    | WUD [0:1] |                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | 0                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | 1                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| 2-3    | WUD [0:1] |                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | 1                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | 0                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| 2-3    | WUD [0:1] |                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | 1                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | 1                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| 4      | LDBG      | LIN debug mode. Prevents the LIN FSM from automatically resetting, after an exception (bit error, physical bus error, wake-up flag) has been received. This is for debug purposes                                                                                                                                                                                                                                                                                   | LIN debug mode. Prevents the LIN FSM from automatically resetting, after an exception (bit error, physical bus error, wake-up flag) has been received. This is for debug purposes                                                                                                                                                                                                                                                                                   | LIN debug mode. Prevents the LIN FSM from automatically resetting, after an exception (bit error, physical bus error, wake-up flag) has been received. This is for debug purposes                                                                                                                                                                                                                                                                                   |
| 5      | DSF       | Double stop flags. When a bit error has been detected, this will add an additional stop flag to the byte in which the error occurred.                                                                                                                                                                                                                                                                                                                               | Double stop flags. When a bit error has been detected, this will add an additional stop flag to the byte in which the error occurred.                                                                                                                                                                                                                                                                                                                               | Double stop flags. When a bit error has been detected, this will add an additional stop flag to the byte in which the error occurred.                                                                                                                                                                                                                                                                                                                               |
| 6      | PRTY      | Activating parity generation. Generate the two parity bits in the LIN header.                                                                                                                                                                                                                                                                                                                                                                                       | Activating parity generation. Generate the two parity bits in the LIN header.                                                                                                                                                                                                                                                                                                                                                                                       | Activating parity generation. Generate the two parity bits in the LIN header.                                                                                                                                                                                                                                                                                                                                                                                       |
| 7      | LIN       | LIN mode. Switch device into LIN mode. 0 LIN disabled 1 LIN enabled                                                                                                                                                                                                                                                                                                                                                                                                 | LIN mode. Switch device into LIN mode. 0 LIN disabled 1 LIN enabled                                                                                                                                                                                                                                                                                                                                                                                                 | LIN mode. Switch device into LIN mode. 0 LIN disabled 1 LIN enabled                                                                                                                                                                                                                                                                                                                                                                                                 |
| 8      | RXIE      | LIN RXREG ready interrupt enable. Generates an Interrupt when new data is available in the LIN RXREG. For a list of interrupt enables and flags, see Table 21-21.                                                                                                                                                                                                                                                                                                   | LIN RXREG ready interrupt enable. Generates an Interrupt when new data is available in the LIN RXREG. For a list of interrupt enables and flags, see Table 21-21.                                                                                                                                                                                                                                                                                                   | LIN RXREG ready interrupt enable. Generates an Interrupt when new data is available in the LIN RXREG. For a list of interrupt enables and flags, see Table 21-21.                                                                                                                                                                                                                                                                                                   |
| 9      | TXIE      | LIN TXREG ready interrupt enable. Generates an Interrupt when new data can be written to the LIN TXREG. For a list of interrupt enables and flags, see Table 21-21.                                                                                                                                                                                                                                                                                                 | LIN TXREG ready interrupt enable. Generates an Interrupt when new data can be written to the LIN TXREG. For a list of interrupt enables and flags, see Table 21-21.                                                                                                                                                                                                                                                                                                 | LIN TXREG ready interrupt enable. Generates an Interrupt when new data can be written to the LIN TXREG. For a list of interrupt enables and flags, see Table 21-21.                                                                                                                                                                                                                                                                                                 |
| 10     | WUIE      | RXwake-up interrupt enable. Generates an Interrupt when a wake-up flag from a LIN slave has been received. For a list of interrupt enables and flags, see Table 21-21.                                                                                                                                                                                                                                                                                              | RXwake-up interrupt enable. Generates an Interrupt when a wake-up flag from a LIN slave has been received. For a list of interrupt enables and flags, see Table 21-21.                                                                                                                                                                                                                                                                                              | RXwake-up interrupt enable. Generates an Interrupt when a wake-up flag from a LIN slave has been received. For a list of interrupt enables and flags, see Table 21-21.                                                                                                                                                                                                                                                                                              |
| 11     | STIE      | Slave timeout error interrupt enable. Generates an Interrupt when the slave response is too slow. For a list of interrupt enables and flags, see Table 21-21.                                                                                                                                                                                                                                                                                                       | Slave timeout error interrupt enable. Generates an Interrupt when the slave response is too slow. For a list of interrupt enables and flags, see Table 21-21.                                                                                                                                                                                                                                                                                                       | Slave timeout error interrupt enable. Generates an Interrupt when the slave response is too slow. For a list of interrupt enables and flags, see Table 21-21.                                                                                                                                                                                                                                                                                                       |
| 12     | PBIE      | Physical bus error interrupt enable. Generates an Interrupt when no valid message can be generated on the bus. For a list of interrupt enables and flags, see Table 21-21.                                                                                                                                                                                                                                                                                          | Physical bus error interrupt enable. Generates an Interrupt when no valid message can be generated on the bus. For a list of interrupt enables and flags, see Table 21-21.                                                                                                                                                                                                                                                                                          | Physical bus error interrupt enable. Generates an Interrupt when no valid message can be generated on the bus. For a list of interrupt enables and flags, see Table 21-21.                                                                                                                                                                                                                                                                                          |
| 13     | CIE       | CRC error interrupt enable. Generates an Interrupt when a CRC error on a received extended frame is detected. For a list of interrupt enables and flags, see Table 21-21.                                                                                                                                                                                                                                                                                           | CRC error interrupt enable. Generates an Interrupt when a CRC error on a received extended frame is detected. For a list of interrupt enables and flags, see Table 21-21.                                                                                                                                                                                                                                                                                           | CRC error interrupt enable. Generates an Interrupt when a CRC error on a received extended frame is detected. For a list of interrupt enables and flags, see Table 21-21.                                                                                                                                                                                                                                                                                           |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## Table 21-7. ESCI x \_LCR Field Descriptions (continued)

| Bits   | Name   | Description                                                                                                                                                                                                                                                                                             |
|--------|--------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 14     | CKIE   | Checksum error interrupt enable. Generates an Interrupt on a detected checksum error. For a list of interrupt enables and flags, see Table 21-21.                                                                                                                                                       |
| 15     | FCIE   | Frame complete interrupt enable. Generates an Interrupt after complete transmission of a TX frame, or after the last byte of an RX frame is received. (The complete frame includes all header, data, CRC and checksum bytes as applicable.) For a list of interrupt enables and flags, see Table 21-21. |
| 16-22  | -      | Reserved.                                                                                                                                                                                                                                                                                               |
| 23     | OFIE   | Overflow interrupt enable. Generates an Interrupt when a data byte in the ESCIx_LRR has not been read before the next data byte is received. For a list of interrupt enables and flags, see Table 21-21.                                                                                                |
| 24-31  | -      | Reserved.                                                                                                                                                                                                                                                                                               |

## 21.3.3.6 LIN Transmit Register (ESCI x \_LTR)

ESCI \_LTR can be written to only when TXRDY is set. The first byte written to the register selects the x transmit address, the second byte determines the frame length, the third and fourth byte set various frame options  and  determine  the  timeout  counter.  Header  parity  will  be  automatically  generated  if  the ESCI \_LCR[PRTY] bit is set. For TX frames, the fourth byte (bits T7-T0) is skipped, since the timeout x function does not apply. All following bytes are data bytes for the frame. CRC and checksum bytes will be automatically appended when the appropriate options are selected.

When a bit error is detected, an interrupt is set and the transmission aborted. The register can only be written again once the interrupt is cleared. Afterwards a new frame starts, and the first byte needs to contain a header again.

Additionally it is possible to flush the ESCI x \_LTR by setting the ESCI x \_LCR[LRES] bit.

## NOTE

Not all values written to the ESCI x \_LTR will generate valid LIN frames. The values are determined according to the LIN specification.

Figure 21-7. LIN Transmit Register (ESCI x \_LTR)

<!-- image -->

|          | 0                     | 1                    | 2                    | 3                   | 4                    | 5                    | 6                   | 7                   | 8           | 9           | 10          | 11          | 12          | 13          | 14          | 15          |
|----------|-----------------------|----------------------|----------------------|---------------------|----------------------|----------------------|---------------------|---------------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|
| R        |                       |                      |                      |                     |                      |                      |                     |                     | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           |
| W        | P1/ L7/ HDCHK/ T7/ D7 | P0/ L6/ CSUM/ T6/ D6 | ID5/ L5/ CRC/ T5/ D5 | ID4/ L4/ TX/ T4/ D4 | ID3/ L3/ T11/ T3/ D3 | ID2/ L2/ T10/ T2/ D2 | ID1/ L1/ T9/ T1/ D1 | ID0/ L0/ T8/ T0/ D0 |             |             |             |             |             |             |             |             |
| Reset    | 0                     | 0                    | 0                    | 0                   | 0                    | 0                    | 0                   | 0                   | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           |
| Reg Addr | Base + 0x10           | Base + 0x10          | Base + 0x10          | Base + 0x10         | Base + 0x10          | Base + 0x10          | Base + 0x10         | Base + 0x10         | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 |
|          | 16                    | 17                   | 18                   | 19                  | 20                   | 21                   | 22                  | 23                  | 24          | 25          | 26          | 27          | 28          | 29          | 30          | 31          |
| R        | 0                     | 0                    | 0                    | 0                   | 0                    | 0                    | 0                   | 0                   | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           |
| W        |                       |                      |                      |                     |                      |                      |                     |                     |             |             |             |             |             |             |             |             |
| Reset    | 0                     | 0                    | 0                    | 0                   | 0                    | 0                    | 0                   | 0                   | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           |
| Reg Addr | Base + 0x10           | Base + 0x10          | Base + 0x10          | Base + 0x10         | Base + 0x10          | Base + 0x10          | Base + 0x10         | Base + 0x10         | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 |

Figure 21-8. LIN Transmit Register (ESCIx\_LTR) Alternate Diagram

<!-- image -->

|                           | 0                    | 1                    | 2                    | 3                    | 4                    | 5                    | 6                    | 7                    |
|---------------------------|----------------------|----------------------|----------------------|----------------------|----------------------|----------------------|----------------------|----------------------|
| R                         |                      |                      |                      |                      |                      |                      |                      |                      |
| 1st Write (Table 21-8) W  | P[1:0]               | P[1:0]               | ID[5:0]              | ID[5:0]              | ID[5:0]              | ID[5:0]              | ID[5:0]              | ID[5:0]              |
| 2nd Write (Table 21-9) W  | L[7:0]               | L[7:0]               | L[7:0]               | L[7:0]               | L[7:0]               | L[7:0]               | L[7:0]               | L[7:0]               |
| 3rd Write (Table 21-10) W | HDCHK                | CSUM                 | CRC                  | TX (RX)              | T[11:8]              | T[11:8]              | T[11:8]              | T[11:8]              |
| 4th Write (Table 21-11) W | T[7:0]               | T[7:0]               | T[7:0]               | T[7:0]               | T[7:0]               | T[7:0]               | T[7:0]               | T[7:0]               |
| 5th Write (Table 21-12) W | D[7:0]               | D[7:0]               | D[7:0]               | D[7:0]               | D[7:0]               | D[7:0]               | D[7:0]               | D[7:0]               |
| Reset                     | 0                    | 0                    | 0                    | 0                    | 0                    | 0                    | 0                    | 0                    |
| Reg Addr                  | eSCI x Base + 0x0010 | eSCI x Base + 0x0010 | eSCI x Base + 0x0010 | eSCI x Base + 0x0010 | eSCI x Base + 0x0010 | eSCI x Base + 0x0010 | eSCI x Base + 0x0010 | eSCI x Base + 0x0010 |

## Table 21-8. ESCI x \_LTR First Byte Field Description

| Bits   | Name   | Description                                                                                                                                                                         | Description                                                                                                                                                                         | Description                                                                                                                                                                         |
|--------|--------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-1    | P n    | Parity bit n . When parity generation is enabled (ESCI x _LCR[PRTY] = 1), the parity bits are generated automatically. Otherwise they must be provided in this field.               | Parity bit n . When parity generation is enabled (ESCI x _LCR[PRTY] = 1), the parity bits are generated automatically. Otherwise they must be provided in this field.               | Parity bit n . When parity generation is enabled (ESCI x _LCR[PRTY] = 1), the parity bits are generated automatically. Otherwise they must be provided in this field.               |
| 2-7    | ID n 1 | Header bit n . The LIN address, for LIN 1.x standard frames the length bits must be appropriately (see the table below), extended frames are recognized by their specific patterns. | Header bit n . The LIN address, for LIN 1.x standard frames the length bits must be appropriately (see the table below), extended frames are recognized by their specific patterns. | Header bit n . The LIN address, for LIN 1.x standard frames the length bits must be appropriately (see the table below), extended frames are recognized by their specific patterns. |
|        |        |                                                                                                                                                                                     | ID5                                                                                                                                                                                 | ID4                                                                                                                                                                                 |
|        |        |                                                                                                                                                                                     | 0                                                                                                                                                                                   | 0                                                                                                                                                                                   |
|        |        |                                                                                                                                                                                     | 0                                                                                                                                                                                   | 1                                                                                                                                                                                   |
|        |        |                                                                                                                                                                                     | 1                                                                                                                                                                                   | 0                                                                                                                                                                                   |
|        |        |                                                                                                                                                                                     | 1                                                                                                                                                                                   | 1                                                                                                                                                                                   |
| 8-31   | -      | Reserved.                                                                                                                                                                           | Reserved.                                                                                                                                                                           | Reserved.                                                                                                                                                                           |

1 The values 3C, 3D, 3E and 3F of the ID-field (ID0-5) indicate command and extended frames.Refer to LIN Specification Package Revision 2.0.

## Table 21-9. ESCI x \_LTR Second Byte Field Descriptions

| Bits   | Name   | Description                                                                                                                                                                                                                                              |
|--------|--------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-7    | L n    | Length bit n . Defines the length of the frame (0 to 255 data bytes). This information is needed by the LIN state machine in order to insert the checksum or CRC pattern as required. LIN 1.x slaves will only accept frames with 2, 4, or 8 data bytes. |
| 8-31   | -      | Reserved.                                                                                                                                                                                                                                                |

## Table 21-10. ESCI x \_LTR Third Byte Field Descriptions

|   Bits | Name   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
|--------|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|      0 | HDCHK  | Header checksum enable. Include the header fields into the mod 256 checksum of the standard frames.                                                                                                                                                                                                                                                                                                                                                                                |
|      1 | CSUM   | Checksum enable. Append a checksum byte to the end of a TXframe. Verify the checksum byte of a RX frame.                                                                                                                                                                                                                                                                                                                                                                           |
|      2 | CRC    | CRC enable. Append two CRC bytes to the end of a TX frame. Verify the two CRC bytes of a RXframe are correct. If both CSUMandCRCbitsareset, the LIN FSMwill first append the CRC bytes, then the checksum byte, and will expect them in this order, as well. If HDCHK is set, the CRC calculation will include header and data bytes, otherwise just the data bytes. CRC bytes are not part of the LIN standard; they are normal data bytes and belong to a higher-level protocol. |
|      3 | TX     | Transmit direction. Indicates a TX frame; that is, the eSCI will transmit data to a slave. Otherwise, an RX frame is assumed, and the eSCI only transmits the header. The data bytes are received from the slave. 0 RX frame 1 TX frame                                                                                                                                                                                                                                            |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## Table 21-10. ESCI x \_LTR Third Byte Field Descriptions (continued)

| Bits   | Name   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|--------|--------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 4-7    | T n    | Timeout bit n . Sets the counter to determine a NO_RESPONSE_ERROR, if the frame is a read access to a LIN slave. Following LIN standard rev 1.3, the value (10 × N DATA + 45) × 1.4 is recommended. For transmissions, this counter has to be set to 0. The timeout bits 7-0 will not be written on a TX frame. For TX frames, the fourth byte written to the LIN transmit register (ESCI x _LTR) is the first data byte, for RX frames it contains timeout bits 7-0.The time is specified in multiples of bit times. The timeout period starts with the transmission of the LIN break character. |
| 8-31   | -      | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |

## Table 21-11. ESCI x \_LTR Rx Frame Fourth Byte Field Descriptions

| Bits   | Name   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
|--------|--------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-7    | T n    | Timeout bit n . Sets the counter to determine a NO_RESPONSE_ERROR, if the frame is a read access to a LIN slave. Following LIN standard rev 1.3, the value (10 × N DATA + 45) × 1.4 is recommended. For transmissions, this counter has to be set to 0. The timeout bits 7-0 will not be written on a TX frame. For TX frames, the fourth byte written to the LIN transmit register (ESCI x _LTR) is the first data byte. For RX frames, it contains timeout bits 7-0.The time is specified in multiples of bit times. The timeout period starts with the transmission of the LIN break character. |
| 8-31   | -      | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |

Table 21-12. ESCI x \_LTR Tx Frame Fourth+ Byte/ Rx Frame Fifth+ Byte Field Description

| Bits   | Name   | Description                 |
|--------|--------|-----------------------------|
| 0-7    | D n    | Data bits for transmission. |
| 8-31   | -      | Reserved.                   |

## 21.3.3.7 LIN Receive Register (ESCI x \_LRR)

ESCI \_LRR can be ready only when ESCI \_SR[RXRDY] is set. x x

## NOTE

Application software must ensure that ESCI x \_LRR be read before new data or checksum bytes or CRCs are received from the LIN bus.

Figure 21-9. LIN Receive Register (ESCI x \_LRR)

|          | 0           | 1           | 2           | 3           | 4           | 5           | 6           | 7           | 8           | 9           | 10          | 11          | 12          | 13          | 14          | 15          |
|----------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|
| R        | D7          | D6          | D5          | D4          | D3          | D2          | D1          | D0          | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           |
| W        |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |
| Reset    | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           |
| Reg Addr | Base + 0x14 | Base + 0x14 | Base + 0x14 | Base + 0x14 | Base + 0x14 | Base + 0x14 | Base + 0x14 | Base + 0x14 | Base + 0x14 | Base + 0x14 | Base + 0x14 | Base + 0x14 | Base + 0x14 | Base + 0x14 | Base + 0x14 | Base + 0x14 |
|          | 16          | 17          | 18          | 19          | 20          | 21          | 22          | 23          | 24          | 25          | 26          | 27          | 28          | 29          | 30          | 31          |
| R        | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           |
| W        |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |
| Reset    | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           |
| Reg Addr | Base + 0x14 | Base + 0x14 | Base + 0x14 | Base + 0x14 | Base + 0x14 | Base + 0x14 | Base + 0x14 | Base + 0x14 | Base + 0x14 | Base + 0x14 | Base + 0x14 | Base + 0x14 | Base + 0x14 | Base + 0x14 | Base + 0x14 | Base + 0x14 |

## Table 21-13. ESCI x \_LRR Field Descriptions

| Bits   | Name   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|--------|--------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-7    | D n    | Data bit n . Provides received data bytes from RX frames. Data is only valid when the ESCI x _SR[RXRDY] flag is set. CRC and checksum information will not be available in the ESCI x _LRR unless they are treated as data. It is possible to treat CRC and checksum bytes as data by deactivating the CSUM respectively CRC control bits in the ESCI x _LTR; however, then CRC and CSUM checking has to be performed by software. Data bytes must be read from the ESCI x _LRR (by CPU or DMA) before any new bytes (including CRCor checksum) are received from the LIN bus otherwise the data byte is lost and OVFL is set. Note: The data must be collected and the LIN frame finished (including CRC and checksum if applicable) before a wake-up character can be sent. |
| 8-31   | -      | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |

## 21.3.3.8 LIN CRC Polynomial Register (ESCI x \_LPR)

ESCI \_LPR x n can be written when there are no ongoing transmissions.

Figure 21-10. LIN CRC Polynomial Register (ESCI x \_LPR)

<!-- image -->

|          | 0           | 1           | 2           | 3           | 4           | 5           | 6           | 7           | 8           | 9           | 10          | 11          | 12          | 13          | 14          | 15          |
|----------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|
| R        | P15         | P14         | P13         | P12         | P11         | P10         | P9          | P8          | P7          | P6          | P5          | P4          | P3          | P2          | P1          | P0          |
| Reset    | 1           | 1           | 0           | 0           | 0           | 1           | 0           | 1           | 1           | 0           | 0           | 1           | 1           | 0           | 0           | 1           |
|          | 16          | 17          | 18          | 19          | 20          | 21          | 22          | 23          | 24          | 25          | 26          | 27          | 28          | 29          | 30          | 31          |
| R        | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           |
| W        |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |
| Reset    | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           |
| Reg Addr | Base + 0x18 | Base + 0x18 | Base + 0x18 | Base + 0x18 | Base + 0x18 | Base + 0x18 | Base + 0x18 | Base + 0x18 | Base + 0x18 | Base + 0x18 | Base + 0x18 | Base + 0x18 | Base + 0x18 | Base + 0x18 | Base + 0x18 | Base + 0x18 |

Table 21-14. ESCI x \_LPR Field Description

| Bits   | Name   | Description                                                                                                                                                                     |
|--------|--------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-15   | P n    | Polynomial bit x n . Bits P15-P0 are used to define the LIN polynomial - standard is x 15 + x 14 + x 10 + x 8 + x 7 + x 4 + x 3 + 1 (the polynomial used for the CAN protocol). |
| 16-31  | -      | Reserved.                                                                                                                                                                       |

## 21.4 Functional Description

## 21.4.1 Overview

This section provides a complete functional description of the eSCI module, detailing the operation of the design from the end user perspective in a number of subsections.

Figure 21-11 shows the structure of the eSCI module. The eSCI allows full duplex, asynchronous, NRZ serial communication between the CPU and remote devices, including other CPUs. The eSCI transmitter and receiver operate independently, although they use the same baud rate generator. The CPU monitors the status of the eSCI, writes the data to be transmitted, and processes received data.

Figure 21-11. eSCI Operation Block Diagram

<!-- image -->

## 21.4.2 Data Format

The eSCI uses the standard NRZ mark/space data format. Each data character is contained in a frame that includes a start bit, eight or nine data bits, and a stop bit. Clearing the M bit in eSCI control register 1

configures the eSCI for 8-bit data characters. A frame with eight data bits has a total of 10 bits. Setting the M bit configures the eSCI for 9-bit data characters. A frame with nine data bits has a total of 11 bits.

When the eSCI is configured for 9-bit data characters, the ninth data bit is the T8 bit in the eSCI data register  (ESCI x \_DR).  It  remains  unchanged  after  transmission  and  can  be  used  repeatedly  without rewriting it. A frame with nine data bits has a total of 11 bits.

The two different data formats are illustrated  in  Figure 21-12.  Table 21-15  and  Table 21-16  show  the number of each type of bit in 8-bit data format and 9-bit data format, respectively.

<!-- image -->

Bit

Figure 21-12. eSCI Data Formats

Table 21-15. Example of 8-bit Data Formats

|   Start Bit |   Data Bits | Address Bits   |   Parity Bits |   Stop Bit |
|-------------|-------------|----------------|---------------|------------|
|           1 |           8 | 0              |             0 |          1 |
|           1 |           7 | 0              |             1 |          1 |
|           1 |           7 | 1 1            |             0 |          1 |

1 The address bit identifies the frame as an address char- acter. See Section 21.4.5.6, 'Receiver Wake-up.'

Table 21-16. Example of 9-Bit Data Formats

|   Start Bit |   Data Bits | Address Bits   |   Parity Bits |   Stop Bit |
|-------------|-------------|----------------|---------------|------------|
|           1 |           9 | 0              |             0 |          1 |
|           1 |           8 | 0              |             1 |          1 |
|           1 |           8 | 1 1            |             0 |          1 |

1 The address bit identifies the frame as an address character. See Section 21.4.5.6, 'Receiver Wake-up.'

## 21.4.3 Baud Rate Generation

A 13-bit modulus counter in the baud rate generator derives the baud rate for both the receiver and the transmitter. The value, 1 to 8191, written to the SBR0-SBR12 bits determines the system clock divider. The SBR bits are in the eSCI control register 1 (ESCI x \_CR1). The baud rate clock is synchronized with the system clock and drives the receiver. The baud rate clock divided by 16 drives the transmitter. The receiver has an acquisition rate of 16 samples per bit time.

Baud rate generation is subject to one source of error:

- · Integer division of the system clock may not give the exact target frequency.

Table 21-17 lists some examples of achieving target baud rates with a system clock frequency of 128 MHz.

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

<!-- formula-not-decoded -->

## Table 21-17. Baud Rates (Example: System Clock = 128 Mhz)

| Bits SBR[0:12]   | Receiver Clock (Hz)   | Transmitter Clock (Hz)   | TargetBaud Rate   |   Error (%) |
|------------------|-----------------------|--------------------------|-------------------|-------------|
| 0x0023           | 3,657,143             | 228,571                  | 230,400           |       -0.79 |
| 0x0045           | 1,855,072             | 115,942                  | 115,200           |        0.64 |
| 0x008B           | 920,863               | 57,554                   | 57,600            |       -0.01 |
| 0x00D0           | 615,385               | 38,462                   | 38,400            |        0.16 |
| 0x01A1           | 306,954               | 19,185                   | 19,200            |       -0.08 |
| 0x022C           | 230,216               | 14,388                   | 14,400            |       -0.08 |
| 0x0341           | 153,661               | 9,604                    | 9600              |        0.04 |
| 0x0683           | 76,785                | 4,799                    | 4800              |       -0.02 |
| 0x0D05           | 38,404                | 2,400.2                  | 2400              |        0.01 |
| 0x1A0A           | 19,202                | 1,200.1                  | 1200              |        0.01 |

## 21.4.4 Transmitter

Figure 21-13 illustrates the features of the eSCI transmitter.

Internal Bus

Figure 21-13. eSCI Transmitter Block Diagram

<!-- image -->

## 21.4.4.1 Transmitter Character Length

The eSCI transmitter can accommodate either 8-bit or 9-bit data characters. The state of the M bit in eSCI control register 1 (ESCI x \_CR1) determines the length of data characters. When transmitting 9-bit data, bit T8 in the eSCI data register (ESCI x \_DR) is the ninth bit (bit 8).

## 21.4.4.2 Character Transmission

To transmit data, the MCU writes the data bits to the eSCI data register (ESCI x \_DR), which in turn are transferred to the transmit shift register. The transmit shift register then shifts a frame out through the TXD signal, after it has prefaced them with a start bit and appended them with a stop bit. The eSCI data register (ESCI \_DR) is the buffer (write-only during transmit) between the internal data bus and the transmit shift x register.

The eSCI also sets a flag, the transmit data register empty flag (TDRE), every time it transfers data from the buffer (ESCI x \_DR) to the transmit shift register. The transmit driver routine may respond to this flag by writing another byte to the transmitter buffer (ESCI x \_DR), while the shift register is still shifting out the first byte.

To initiate an eSCI transmission:

- 1. Configure the eSCI:
- a) Turn on the module by clearing ESCI x \_CR2[MDIS] if this bit is set.
- b) Select a baud rate. Write this value to the eSCI control register 1 (ESCI x \_CR1) to start the baud rate generator. Remember that the baud rate generator is disabled when the ESCI \_CR1[SBR] field is zero. When using 8-bit writes, writes to the ESCI x x \_CR1[0-7] have no effect without also writing to ESCI x \_CR1[8-15].
- c) Write to ESCIx\_CR1 to configure word length, parity, and other configuration bits (LOOPS, RSRC, M, WAKE, ILT, PE, PT).
- d) Enable the transmitter, interrupts, receive, and wake-up as required, by writing to the ESCI \_CR1 register bits (TIE, TCIE, RIE, ILIE, TE, RE, RWU, SBK). A preamble or idle x character will now be shifted out of the transmitter shift register.
- 2. Transmit procedure for each byte:
- a) Poll the TDRE flag by reading the ESCI x \_SR or responding to the TDRE interrupt. Keep in mind that the TDRE bit resets to 1.
- b) If the TDRE flag is set, write the data to be transmitted to ESCI x \_DR, where the ninth bit is written to the T8 bit in ESCI x \_DR if the eSCI is in 9-bit data format. A new transmission will not result until the TDRE flag has been cleared.
- 3. Repeat step 2 for each subsequent transmission.

## NOTE

The TDRE flag is set when the shift register is loaded with the next data to be  transmitted  from  ESCI x \_DR,  which  occurs  approximately  half-way through the stop bit of the previous frame. Specifically, this transfer occurs 9/16ths of a bit time AFTER the start of the stop bit of the previous frame.

Toggling the TE bit from 0 to 1 automatically loads the transmit shift register with a preamble of 10 logic 1s (if M = 0) or 11 logic 1s (if M = 1). After the preamble shifts out, control logic transfers the data from the eSCI data register into the transmit shift register. A logic 0 start bit automatically goes into the least

significant bit position of the transmit shift register. A logic 1 stop bit goes into the most significant bit position.

The eSCI hardware supports odd or even parity. When parity is enabled, the most significant bit (Msb) of the data character is the parity bit.

The transmit data register empty flag, TDRE, in the eSCI status register (ESCI x \_SR) becomes set when the eSCI data register transfers a byte to the transmit shift register. The TDRE flag indicates that the eSCI data register can accept new data from the internal data bus. If the transmit interrupt enable bit, TIE, in eSCI control register 1 (ESCI x \_CR1) is also set, the TDRE flag generates a transmitter interrupt request.

When the transmit shift register is not transmitting a frame, the TXD output goes to the idle condition, logic 1. If at any time software clears the TE bit in eSCI control register 1 (ESCI x \_CR1), the transmitter enable signal goes low and the TXD output goes idle.

If software clears TE while a transmission is in progress (ESCI x \_CR1[TC] = 0), the frame in the transmit shift register continues to shift out. To avoid accidentally cutting off the last frame in a message, always wait for TDRE to go high after the last frame before clearing TE.

To separate messages with preambles with minimum idle line time, use the following sequence between messages:

- 1. Write the last byte of the first message to ESCI x \_DR.
- 2. Wait for the TDRE flag to go high, indicating the transfer of the last frame to the transmit shift register.
- 3. Queue a preamble by clearing and then setting the TE bit.
- 4. Write the first byte of the second message to ESCI x \_DR.

## 21.4.4.3 Break Characters

Setting the break bit, SBK, in eSCI control register 1 (ESCI x \_CR1) loads the transmit shift register with a break character. A break character contains all logic 0s and has no start, stop, or parity bit. Break character length depends on the M bit in the eSCI control register 1 (ESCI x \_CR1) and on the BRK13 bit in the eSCI control register 2 (ESCI x \_CR2). As long as SBK is set, the transmitter logic continuously loads break characters into the transmit shift register. After software clears the SBK bit, the shift register finishes transmitting the last break character and then transmits at least one logic 1. The automatic logic 1 at the end of a break character guarantees the recognition of the start bit of the next frame.

## NOTE

LIN 2.0 now requires that a break character is always 13 bits long, so the BRK13 bit should always be set to 1. The eSCI will work with BRK13=0, but it will violate LIN 2.0.

The eSCI recognizes a break character when a start bit is followed by eight or nine logic 0 data bits and a logic  0  where  the  stop  bit  should  be.  Receiving  a  break  character  has  the  following  effects  on  eSCI registers:

- · Sets the framing error flag, FE.
- · Sets the receive data register full flag, RDRF.
- · Clears the eSCI data register (ESCI x \_DR).
- · May set the overrun flag, OR, noise flag, NF, parity error flag, PF, or the receiver active flag, RAF. For more details, see Section 21.3.3.4, 'eSCI Status Register (ESCIx\_SR).'

## 21.4.4.4 Idle Characters

An idle character contains all logic 1s and has no start, stop, or parity bit. Idle character length depends on the M bit in eSCI control register 1 (ESCI x \_CR1). The preamble is a synchronizing idle character that begins the first transmission initiated after toggling the TE bit from 0 to 1.

If  the  TE  bit  is  cleared  during  a  transmission,  the  TXD  output becomes idle  after  completion  of  the transmission  in  progress.  Clearing  and  then  setting  the  TE  bit  during  a  transmission  queues  an  idle character to be sent after the frame currently being transmitted.

## NOTE

When queueing an idle character, return the TE bit to logic 1 before the stop bit of the current frame shifts out through the TXD output. Setting the TE bit  after  the  stop  bit  shifts  out  through  the  TXD  output causes  data previously written to the eSCI data register to be lost. Toggle the TE bit for a queued idle character while the TDRE flag is set and immediately before writing the next byte to the eSCI data register.

## 21.4.4.5 Fast Bit Error Detection in LIN Mode

Fast bit error detection has been designed to allow flagging of LIN bit errors while they occur, rather than flagging them after a byte transmission has completed. In order to use this feature, it is assumed a physical interface connects to the LIN bus as shown in Figure 21-14.

Figure 21-14. Fast Bit Error Detection on a LIN Bus

<!-- image -->

If fast bit error detection is enabled (FBR = 1), the eSCI will compare the transmitted and the received data stream when the transmitter is active (not idle). Once a mismatch between the transmitted data and the received data is detected the following actions are performed:

- · The LIN frame is aborted (provided LDBG=0).
- · The bit error flag BERR will be set.
- · If SBSTP is 0, the remainder of the byte will be transmitted normally.
- · If SBSTP is 1, the remaining bits in the byte after the error bit are transmitted as 1s (idle).

To adjust to different bus loads the sample point at which the incoming bit is compared to the one which was transmitted can be selected with the BESM13 bit (see Figure 21-15). If set, the comparison will be performed at RT clock 13, otherwise at RT clock 9 (also see Section 21.4.5.3, 'Data Sampling.').

Figure 21-15. Fast Bit Error Detection Timing Diagram

<!-- image -->

## 21.4.5 Receiver

Figure 21-16 illustrates the eSCI receiver.

Figure 21-16. eSCI Receiver Block Diagram

<!-- image -->

## 21.4.5.1 Receiver Character Length

The eSCI receiver can accommodate either 8-bit or 9-bit data characters. The state of the M bit in eSCI control register 1 (ESCI x \_CR1) determines the length of data characters. When receiving 9-bit data, bit R8 in the eSCI data register (ESCI x \_DR) is the ninth bit (bit 8).

## 21.4.5.2 Character Reception

During an eSCI reception, the receive shift register shifts a frame in from the RXD input signal. The eSCI data register is the buffer (read-only during receive) between the internal data bus and the receive shift register.

After a complete frame shifts into the receive shift register, the data portion of the frame transfers to the eSCI data register. The receive data register full flag, RDRF, in eSCI status register (ESCI x \_SR) is then set, indicating that the received byte can be read. If the receive interrupt enable bit, RIE, in eSCI control register 1 (ESCI x \_CR1) is also set, the RDRF flag generates an RDRF interrupt request.

## 21.4.5.3 Data Sampling

The receiver uses a sampling clock to sample the RXD input signal at the 16 times the baud-rate frequency. This  sampling  clock  is  called  the  RT  clock.  To  adjust  for  baud  rate  mismatch,  the  RT  clock  (see Figure 21-17) is re-synchronized:

- · After every start bit.
- · After the receiver detects a data bit change from logic 1 to logic 0. This data bit change is detected when a majority of data samples return a valid logic 1 and a majority of the next data samples return a valid logic 0. Data samples are taken at RT8, RT9, and RT10, as shown in Figure 21-17.

To locate the start bit, eSCI data recovery logic performs an asynchronous search for a logic 0 preceded by three logic 1s. When the falling edge of a possible start bit occurs, the RT clock begins to count to 16.

Figure 21-17. Receiver Data Sampling

<!-- image -->

To verify the start bit and to detect noise, the eSCI data recovery logic takes samples at RT3, RT5, and RT7. Table 21-18 summarizes the results of the start bit verification samples.

Table 21-18. Start Bit Verification

|   RT3, RT5, and RT7 Samples | Start Bit Verification   |   Noise Flag |
|-----------------------------|--------------------------|--------------|
|                         000 | Yes                      |            0 |
|                         001 | Yes                      |            1 |
|                         010 | Yes                      |            1 |
|                         011 | No                       |            0 |
|                         100 | Yes                      |            1 |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 21-18. Start Bit Verification (continued)

|   RT3, RT5, and RT7 Samples | Start Bit Verification   |   Noise Flag |
|-----------------------------|--------------------------|--------------|
|                         101 | No                       |            0 |
|                         110 | No                       |            0 |
|                         111 | No                       |            0 |

If start bit verification is not successful, the RT clock is reset and a new search for a start bit begins.

To determine the value of a data bit and to detect noise, eSCI recovery logic takes samples at RT8, RT9, and RT10. Table 21-19 summarizes the results of the data bit samples.

Table 21-19. Data Bit Recovery

|   RT8, RT9, and RT10 Samples |   Data Bit Determination |   Noise Flag |
|------------------------------|--------------------------|--------------|
|                          000 |                        0 |            0 |
|                          001 |                        0 |            1 |
|                          010 |                        0 |            1 |
|                          011 |                        1 |            1 |
|                          100 |                        0 |            1 |
|                          101 |                        1 |            1 |
|                          110 |                        1 |            1 |
|                          111 |                        1 |            0 |

## NOTE

The RT8, RT9, and RT10 samples do not affect start bit verification. If any or all of the RT8, RT9, and RT10 start bit samples are logic 1s following a successful start bit verification, the noise flag (NF) is set.

To verify a stop bit and to detect noise, recovery logic takes samples at RT8, RT9, and RT10. Table 21-20 summarizes the results of the stop bit samples.

Table 21-20. Stop Bit Recovery

|   RT8, RT9, and RT10 Samples |   Framing Error Flag |   Noise Flag |
|------------------------------|----------------------|--------------|
|                          000 |                    1 |            0 |
|                          001 |                    1 |            1 |
|                          010 |                    1 |            1 |
|                          011 |                    0 |            1 |
|                          100 |                    1 |            1 |
|                          101 |                    0 |            1 |
|                          110 |                    0 |            1 |
|                          111 |                    0 |            0 |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

In Figure 21-18 the verification samples RT3 and RT5 determine that the first low detected was noise and not the beginning of a start bit. The RT clock is reset and the start bit search begins again. The noise flag is not set because the noise occurred before the start bit was found.

<!-- image -->

## 21.4.5.4 Framing Errors

If the data recovery logic sets the framing error flag, ESCI x \_SR[FE], it does not detect a logic 1 where the stop bit should be in an incoming frame. A break character also sets the FE flag because a break character has no stop bit. The FE flag is set at the same time that the RDRF flag is set.

## 21.4.5.5 Baud Rate Tolerance

A transmitting device may be operating at a baud rate below or above the receiver baud rate. Accumulated bit time misalignment can cause one of the three stop bit data samples (RT8, RT9, and RT10) to fall outside the actual stop bit. A noise error will occur if the RT8, RT9, and RT10 samples are not all the same logical values. A framing error will occur if the receiver clock is misaligned in such a way that the majority of the RT8, RT9, and RT10 stop bit samples are a logic zero.

As the receiver samples an incoming frame and re-synchronizes the RT clock on any valid falling edge within the frame. Re-synchronization within frames will correct a misalignment between transmitter bit times and receiver bit times.

## 21.4.5.5.1 Slow Data Tolerance

Figure 21-19 shows how much a slow received frame can be misaligned without causing a noise error or a framing error. The slow stop bit begins at RT8 instead of RT1 but arrives in time for the stop bit data samples at RT8, RT9, and RT10.

Figure 21-19. Slow Data

<!-- image -->

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

For an 8-bit data character, data sampling of the stop bit takes the receiver RT clock 151 clock cycles, as is shown below:

9 bit times 16 RT cycles + 7 RT cycles × 151 RT cycles =

With the misaligned character shown in Figure 21-19, the receiver counts 151 RT cycles at the point when the count of the transmitting device is 9 bit times x 16 RT cycles = 147 RT cycles.

The maximum percent difference between the receiver count and the transmitter count of a slow 8-bit data character with no errors is 4.63%, as is shown below:

<!-- formula-not-decoded -->

For a 9-bit data character, data sampling of the stop bit takes the receiver 167 RT cycles, as is shown below:

10 bit times 16 RT cycles + 7 RT cycles × 167 RT cycles =

With the misaligned character shown in Figure 21-19, the receiver counts 167 RT cycles at the point when the count of the transmitting device is 10 bit times x 16 RT cycles cycles = 160 RT cycles.

The maximum percent difference between the receiver count and the transmitter count of a slow 9-bit character with no errors is 4.19%, as is shown below:

<!-- formula-not-decoded -->

## 21.4.5.5.2 Fast Data Tolerance

Figure 21-20 shows how much a fast received frame can be misaligned. The fast stop bit ends at RT10 instead of RT16 but is still sampled at RT8, RT9, and RT10.

Figure 21-20. Fast Data

<!-- image -->

For an 8-bit data character, data sampling of the stop bit takes the receiver 154 RT cycles, as is shown below:

9 bit times 16 RT cycles + 10 RT cycles × 154 RT cycles =

With the misaligned character shown in Figure 21-20, the receiver counts 154 RT cycles at the point when the count of the transmitting device is 10 bit times x 16 RT cycles = 160 RT cycles.

The maximum percent difference between the receiver count and the transmitter count of a fast 8-bit character with no errors is 3.40%, as is shown below:

<!-- formula-not-decoded -->

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Enhanced Serial Communication Interface (eSCI)

For a 9-bit data character, data sampling of the stop bit takes the receiver 170 RT cycles, as shown below:

<!-- formula-not-decoded -->

With the misaligned character shown in Figure 21-20, the receiver counts 170 RT cycles at the point when the count of the transmitting device is 11 bit times x 16 RT cycles = 176 RT cycles.

The maximum percent difference between the receiver count and the transmitter count of a fast 9-bit character with no errors is 3.40%, as is shown below:

<!-- formula-not-decoded -->

## 21.4.5.6 Receiver Wake-up

The receiver can be put into a standby state, which enables the eSCI to ignore transmissions intended only for other receivers in multiple-receiver systems. Setting the receiver wake-up bit, ESCI x \_CR1[RWU], in eSCI control register 1 (ESCI x \_CR1) puts the receiver into standby state during which receiver interrupts are disabled. The eSCI will still load the received data into the ESCI x \_DR, but it will not set the receive data register full, RDRF, flag.

The transmitting device can address messages to selected receivers by including addressing information (address bits) in the initial frame or frames of each message. See section Section 21.4.2, 'Data Format,' for an example of address bits.

The WAKE bit in eSCI control register 1 (ESCI x \_CR1) determines how the eSCI is brought out of the standby state to process an incoming message. The WAKE bit enables either idle line wake-up or address mark wake-up.

## 21.4.5.6.1 Idle Input Line Wake-up (WAKE = 0)

Using the receiver idle input line wake-up method allows an idle condition on the RXD signal clears the ESCI \_CR1[RWU] bit and wakes up the eSCI. The initial frame or frames of every message contain x addressing information. All receivers evaluate the addressing information, and receivers for which the message is addressed process the frames that follow. Any receiver for which a message is not addressed can set its RWU bit and return to the standby state. The RWU bit remains set and the receiver remains on standby until another idle character appears on the RXD signal.

Idle line wake-up requires that messages be separated by at least one idle character and that no message contains idle characters.

The idle character that wakes a receiver does not set the receiver idle bit, ESCI x \_SR[IDLE], or the receive data register full flag, RDRF.

The idle line type bit, ESCI x \_CR1[ILT], determines whether the receiver begins counting logic 1s as idle character bits after the start bit or after the stop bit.

## 21.4.5.6.2 Address Mark Wake-up (WAKE = 1)

Using the address mark wake-up method allows a logic 1 in the most significant bit (msb) position of a frame to clear the RWU bit and wake-up the eSCI. The logic 1 in the msb position marks a frame as an address frame that contains addressing information. All receivers evaluate the addressing information, and the receivers for which the message is addressed process the frames that follow. Any receiver for which a

Freescale Semiconductor

message is not addressed can set its RWU bit and return to the standby state. The RWU bit remains set and the receiver remains on standby until another address frame appears on the RXD signal.

The logic 1 msb of an address frame clears the receiver's RWU bit before the stop bit is received and sets the RDRF flag.

Address mark wake-up allows messages to contain idle characters but requires that the msb be reserved for use in address frames.

## NOTE

With the WAKE bit clear, setting the RWU bit after the RXD signal has been idle can cause the receiver to wake-up immediately.

## 21.4.6 Single-Wire Operation

Normally, the eSCI uses two pins for transmitting and receiving. In single-wire operation, the RXD pin is disconnected from the eSCI. The eSCI uses the TXD pin for both receiving and transmitting.

Figure 21-21. Single-Wire Operation (LOOPS = 1, RSRC = 1)

<!-- image -->

Enable single-wire operation by setting the LOOPS bit and the receiver source bit, RSRC, in eSCI control register 1 (ESCI x \_CR1). Setting the LOOPS bit disables the path from the RXD signal to the receiver. Setting the RSRC bit connects the receiver input to the output of the TXD pin driver.

During  reception,  both  the  transmitter  and  receiver  must  be  enabled  (TE = 1  and  RE = 1).  The SIU\_PCR89[PA] and SIU\_PCR91[PA] bits must be set to select the TXD function for the relevant eSCI module, and the TXD pin should be set for open drain operation (SIU\_PCR nn [ODE] = 1). Weak pull-up may optionally be enabled if the external transmitting device is also open drain. See Section 6.3.1.12, 'Pad Configuration Registers (SIU\_PCR)'.

During transmission,  the transmitter must be enabled (TE=1); the receiver may be enabled or disabled. If the receiver is enabled (RE=1), transmissions will be echoed back on the receiver. Set or clear open drain output enable depending on desired operation.

## 21.4.7 Loop Operation

In loop operation the transmitter output goes to the receiver input. The RXD signal is disconnected from the eSCI.

## Enhanced Serial Communication Interface (eSCI)

Figure 21-22. Loop Operation (LOOPS = 1, RSRC = 0)

<!-- image -->

Enable loop operation by setting the LOOPS bit and clearing the RSRC bit in eSCI control register 1 (ESCI \_CR1). Setting the LOOPS bit disables the path from the RXD signal to the receiver. Clearing the x RSRC bit connects the transmitter output to the receiver input. Both the transmitter and receiver must be enabled (TE = 1 and RE = 1).

## 21.4.8 Modes of Operation

## 21.4.8.1 Run Mode

This is the normal mode of operation.

## NOTE

The eSCI does not support a freeze mode. If the device is being operated in debug mode, the eSCI will continue to shift data if the e200z6 core asserts a freeze.

## 21.4.8.2 Disabling the eSCI

The module disable bit (ESCIx\_CR2[MDIS]) in the eSCI control register 2 can be used to turn off the eSCI. This will save power by stopping the eSCI core from being clocked.By default the eSCI is enabled (ESCIx\_CR2[MDIS]=0).

## 21.4.9 Interrupt Operation

## 21.4.9.1 Interrupt Sources

There are several interrupt sources that can generate an eSCI interrupt to the CPU. They are listed with details and descriptions in Table 21-21.

Table 21-21. eSCI Interrupt Flags, Sources, Mask Bits, and Descriptions

| Interrupt Source   | Flag   | Source        | Local Enable   | Description                                                                         |
|--------------------|--------|---------------|----------------|-------------------------------------------------------------------------------------|
| Transmitter        | TDRE   | ESCI x _SR[0] | TIE            | Indicates that a byte was transferred from ESCIx_DR to the transmit shift register. |
| Transmitter        | TC     | ESCI x _SR[1] | TCIE           | Indicates that a transmit is complete.                                              |
| Receiver           | RDRF   | ESCI x _SR[2] | RIE            | Indicates that received data is available in the eSCI data register.                |
| Receiver           | IDLE   | ESCI x _SR[3] | ILIE           | Indicates that receiver input has become idle.                                      |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 21-21. eSCI Interrupt Flags, Sources, Mask Bits, and Descriptions (continued)

| Interrupt Source   | Flag   | Source         | Local Enable   | Description                                                                   |
|--------------------|--------|----------------|----------------|-------------------------------------------------------------------------------|
| Receiver           | OR     | ESCI x _SR[4]  | ORIE           | Indicates that an overrun condition has occurred.                             |
| Receiver           | NF     | ESCI x _SR[5]  | NFIE           | Detect noise error on receiver input.                                         |
| Receiver           | FE     | ESCI x _SR[6]  | FEIE           | Framing error has occurred.                                                   |
| Receiver           | PF     | ESCI x _SR[7]  | PFIE           | Parity of received data does not match parity bit; parity error has occurred. |
| LIN                | BERR   | ESCI x _SR[11] | IEBERR         | Detected a bit error, only valid in LIN mode.                                 |
| LIN                | RXRDY  | ESCI x _SR[16] | RXIE           | Indicates LIN hardware has received a data byte.                              |
| LIN                | TXRDY  | ESCI x _SR[17] | TXIE           | Indicates LIN hardware can accept a control or data byte.                     |
| LIN                | LWAKE  | ESCI x _SR[18] | WUIE           | A wake-up character has been received from a LIN frame.                       |
| LIN                | STO    | ESCI x _SR[19] | STIE           | The response of the slave has been too slow (slave timeout).                  |
| LIN                | PBERR  | ESCI x _SR[20] | PBIE           | Physical bus error detected.                                                  |
| LIN                | CERR   | ESCI x _SR[21] | CIE            | CRC error detected.                                                           |
| LIN                | CKERR  | ESCI x _SR[22] | CKIE           | Checksum error detected.                                                      |
| LIN                | FRC    | ESCI x _SR[23] | FCIE           | LIN frame completed.                                                          |
| LIN                | OVFL   | ESCI x _SR[31] | OFIE           | ESCIx_LRR overflow.                                                           |

The eSCI only originates interrupt requests. The following sections describe how the eSCI generates a request and how the MCU acknowledges that request. The eSCI only has a single interrupt line (eSCI interrupt signal, active high operation) and all the following interrupts, when generated, are ORed together and issued through that port.

## 21.4.9.2 Interrupt Flags

## 21.4.9.2.1 TDRE Description

The transmit data register empty (TDRE) interrupt is set high by the eSCI when the transmit shift register receives data, 8 or 9 bits, from the eSCI data register, ESCI x \_DR. A TDRE interrupt indicates that the transmit data register (ESCI x \_DR) is empty and that a new data can be written to the ESCI x \_DR for transmission. The TDRE bit is cleared by writing a one to the TDRE bit location in the ESCI x \_SR.

## 21.4.9.2.2 TC Description

The transmit complete (TC) interrupt is set by the eSCI when a transmission has completed. A TC interrupt indicates that there is no transmission in progress. TC is set high when the TDRE flag is set and no data, preamble, or break character is being transmitted. When TC is set, the TXD pin becomes idle (logic 1). The TC bit is cleared by writing a one to the TC bit location in the ESCI x \_SR.

## 21.4.9.2.3 RDRF Description

The receive data register full (RDRF) interrupt is set when the data in the receive shift register transfers to the eSCI data register. An RDRF interrupt indicates that the received data has been transferred to the eSCI data register and that the received data can now be read by the MCU. The RDRF bit is cleared by writing a one to the RDRF bit location in the ESCI x \_SR.

## 21.4.9.2.4 OR Description

The overrun (OR) interrupt is set when software fails to read the eSCI data register before the receive shift register receives the next frame. The newly acquired data in the shift register is lost in this case, but the data already in the eSCI data registers is not affected.The OR bit is cleared by writing a one to the OR bit location in the ESCI x \_SR.

## 21.4.9.2.5 IDLE Description

The idle line (IDLE) interrupt is set when 10 consecutive logic 1s (if M = 0) or 11 consecutive logic 1s (if M=1) appear on the receiver input. Once the IDLE is cleared, a valid frame must again set the RDRF flag before an idle condition can set the IDLE flag. The IDLE bit is cleared by writing a one to the IDLE bit location in the ESCI x \_SR.

## 21.4.9.2.6 PF Description

The interrupt is set when the parity of the received data is not correct. PF is cleared by writing it with 1.

## 21.4.9.2.7 FE Description

The interrupt is set when the stop bit is read as a 0; which violates the SCI protocol. FE is cleared by writing it with 1.

## 21.4.9.2.8 NF Description

The NF interrupt is set when the eSCI detects noise on the receiver input.

## 21.4.9.2.9 BERR Description

While  the  eSCI  is  in  LIN  mode,  the  bit  error  (BERR)  flag  is  set  when  one  or  more  bits  in  the  last transmitted byte is not read back with the same value. The BERR flag is cleared by writing a 1 to the bit. A bit error will cause the LIN FSM to reset. The BERR flag is cleared by writing a 1 to the bit.

## 21.4.9.2.10 RXRDY Description

While in LIN mode, the receiver ready (RXRDY) flag is set when the eSCI receives a valid data byte in an RX frame. RXRDY will not be set for bytes which the receiver obtains by reading back the data which the LIN finite state machine (FSM) has sent out. The RXRDY flag is cleared by writing a 1 to the bit.

## 21.4.9.2.11 TXRDY Description

While in LIN mode, the transmitter ready (TXRDY) flag is set when the eSCI can accept a control or data byte. The TXRDY flag is cleared by writing a 1 to the bit.

## 21.4.9.2.12 LWAKE Description

The LIN wake-up (LWAKE) flag is set when the LIN hardware receives a wake-up character sent by one of the LIN slaves. This occurs only when the LIN bus is in sleep mode. The LWAKE flag is cleared by writing a 1 to the bit.

## 21.4.9.2.13 STO Description

The slave timeout (STO) flag is set during an RX frame when the LIN slave has not transmitted all requested data bytes before the specified timeout period. The STO flag is cleared by writing a 1 to the bit.

## 21.4.9.2.14 PBERR Description

If the RXD input remains stuck at a fixed value for 15 cycles after a transmission has started, the LIN hardware sets the physical bus error (PBERR) flag. The PBERR flag is cleared by writing a 1 to the bit.

## 21.4.9.2.15 CERR Description

If an RX frame has the CRC checking flag set and the two CRC bytes do not match the calculated CRC pattern, the CRC error (CERR) flag is set. The CERR flag is cleared by writing a 1 to the bit.

## 21.4.9.2.16 CKERR Description

If  an  RX  frame  has  the  checksum  checking  flag  set  and  the  last  byte  does  not  match  the  calculated checksum, the checksum error (CKERR) flag is set. The CKERR flag is cleared by writing a 1 to the bit.

## 21.4.9.2.17 FRC Description

The frame complete (FRC) flag is set after the last byte of a TX frame is sent out, or after the last byte of an RX frame is received. The FRC flag is cleared by writing a 1 to the bit.

## NOTE

The last  byte  of  a  TX  frame  being  sent  or  an  RX  frame  being  received indicates that the checksum comparison has taken place.

## NOTE

The FRC flag is used to indicate to the CPU that the next frame can be set up.  However,  it  should  be  noted  that  it  might  be  set  before  the  DMA controller has transferred the last byte from the eSCI to system memory. The FRC flag should not be used if the intention is to process data. Instead, the appropriate interrupt of the DMA controller should be used.

## 21.4.9.2.18 OVFL Description

The overflow (OVFL) flag is set when a byte is received in the ESCI x \_LRR before the previous byte is read. Since the system is responsible for reading the register before the next byte arrives, this condition indicates a problem with CPU load. The OVFL flag is cleared by writing a 1 to the bit.

## 21.4.10 Using the LIN Hardware

The eSCI provides special support for the LIN protocol. It can be used to automate most tasks of a LIN master. In conjunction with the DMA interface it is possible to transmit entire frames (or sequences of

Enhanced Serial Communication Interface (eSCI)

frames) and receive data from LIN slaves without any CPU intervention. There is no special support for LIN slave mode. If required, LIN slave mode may be implemented in software.

A LIN frame consists of a break character (10 or 13 bits), a sync field, an ID field, n data fields ( n could be 0) and a checksum field. The data and checksum bytes are either provided by the LIN master (TX frame) or by the LIN slave (RX frame). The header fields will always be generated by the LIN master.

Break

Sync

ID

Data

Data

CSum

...

Figure 21-23. Typical LIN frame

The LIN hardware is highly configurable. This configurability allows the eSCI's LIN hardware to generate frames for LIN slaves from all revisions of the LIN standard. The settings are adjusted according to the capabilities of the slave device.

In order to activate the LIN hardware, the LIN mode bit in the ESCI x \_LCR needs to be set. Other settings, such as double stop flags after bit errors and automatic parity bit generation, are also available for use in LIN mode.

The eSCI settings must be made according to the LIN specification. The eSCI must be configured for 2-wire operation (2 wires connected to the LIN transceiver) with 8 data bytes and no parity. Normally a 13-bit break is used, but the eSCI can also be configured for 10-bit breaks as required by the application.

## 21.4.10.1 Features of the LIN Hardware

The  eSCI's  LIN  hardware  has  several  features  to  support  different  revisions  of  the  LIN  slaves.  The ESCI \_LTR can be configured to include or not include header bits in the checksum on a frame by frame x basis. This feature supports LIN slaves with different LIN revisions. The LIN control register allows the user to decide whether the parity bits in the ID field should be calculated automatically and whether double stop flags should be inserted after a bit error. The BRK13 bit in ESCI x \_CR2 decides whether to generate 10 or 13 bit break characters.

## NOTE

LIN 2.0 now requires that a break character is always 13 bits long, so the BRK13 bit should always be set to 1. The eSCI will work with BRK13=0, but it will violate LIN 2.0.

The application software can decide to turn off the checksum generation/verification on a per frame basis and handle that function on its own. The application software can also decide to let the LIN hardware append two CRC bytes (Figure 21-24). The CRC bytes are not part of the LIN standard, but could be part of the application layer, that is they would be treated as data bytes by the LIN protocol. This can be useful when very long frames are transmitted. By default the CRC polynomial used is the same polynomial as for the CAN protocol.

Break

Sync

ID

Data

Data

CRC1

CRC2

CSum

• • •

Figure 21-24. LIN Frame with CRC bytes

<!-- image -->

It is possible to force a resync of the LIN FSM, with the LRES bit in the LIN control register. However, under normal circumstances, the LIN hardware will automatically abort a frame after detecting a bit error.

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Freescale Semiconductor

## 21.4.10.2 Generating a TX Frame

The following procedure describes how a basic TX frame is generated.

The frame is controlled via the LIN transmit register (ESCI x \_LTR). Initially, the application software will need to check the TXRDY bit (either using an interrupt, the TX DMA interface, or by polling the LIN status register). If TXRDY is set, the register is writable. Before each write, TXRDY must be checked (though this step is performed automatically in DMA mode). The first write to the ESCI x \_LTR must contain the LIN ID field. The next write to ESCI x \_LTR specifies the length of the frame (0 to 255 Bytes). The third write to ESCI x \_LTR contains the control byte (frame direction, checksum/CRC settings). Note that timeout bits are not included in TX frames, since they only refer to LIN slaves. The three previously mentioned writes to the ESCI x \_LTR specify the LIN frame data. Once the LIN frame data is specified, the eSCI LIN hardware starts to generate a LIN frame.

First, the eSCI transmits a break field. The sync field is transmitted next. The third field is the ID field. After  these  three  fields  have  been  broadcast,  the  ESCIx\_LTR  accepts  data  bytes;  the  LIN  hardware transmits these data bytes as soon as they are available and can be sent out. After the last step the LIN hardware automatically appends the checksum field.

It  is  possible  to  set  up  a  DMA  channel  to  handle  all  the  tasks  required  to  send  a  TX  frame.  (See Figure 21-25 for more information.) For this operation, the TX DMA channel must be activated by setting the ESCI \_CR2[TXDMA] bit. The control information for the LIN frame (ID, message length, TX/RX x type, timeout, etc.) and the data bytes are stored at an appropriate memory location. The DMA controller is  then  set  up  to  transfer  this  block  of  memory  to  a  location  (the  ESCI x \_LTR). After transmission is complete, either the DMA controller or the LIN hardware can generate an interrupt to the CPU.

## NOTE

In  contrast  to  the  standard  software  implementation  where  each  byte transmission  requires  several  interrupts,  the  DMA  controller  and  eSCI handle communication, bit error and physical bus error checking, checksum, and CRC generation (checking on the RX side).

Figure 21-25. DMA Transfer of a TX frame

<!-- image -->

## 21.4.10.3 Generating an RX Frame

For RX frames the header information is provided by the LIN master. The data, CRC and checksum bytes (as enabled) are provided by the LIN slave. The LIN master verifies CRC and checksum bytes transmitted by the slave.

For a RX frame, control information must be written to the ESCI x \_LTR in the same manner as for the TX frames. Additionally the timeout bits, which define the time to complete the entire frame, must be written. Then the ESCI \_SR[RXRDY] bit must be checked (either with an interrupt, RX DMA interface, or by x polling) to detect incoming data bytes. The checksum byte normally does not appear in the ESCI x \_LRR, instead the LIN hardware will verify the checksum and issue an interrupt, if the checksum value is not correct.

Two  DMA  channels  can  be  used  when  executing  a  RX  frame:  one  to  transfer  the  header/control information from a memory location to the ESCI x \_LTR, and one to transfer the incoming data bytes from the ESCI \_LRR to a table in memory. See Figure 21-26 for more information. After the last byte from the x RX frame has been stored, the DMA controller can indicate completion to the CPU.

## NOTE

It  is  also  possible to setup a whole sequence of RX and TX frames, and generate a single event at the end of that sequence.

Figure 21-26. DMA Transfer of a RX frame

<!-- image -->

## 21.4.10.4 LIN Error Handling

The LIN hardware can detect several error conditions of the LIN protocol. LIN hardware will receive every byte that was transmitted, and compare it with the intended values. If there is a mismatch, a bit error is issued, and the LIN FSM will return to its start state.

For a RX frame the LIN hardware can detect a slave timeout error. The exact slave timeout error value can be set via the timeout bits in the ESCI x \_LTR. If the frame is not complete within the number of clock cycles specified in the register, the LIN FSM will return to its start state, and the STO interrupt is issued.

The LIN protocol supports a sleep mode. After 25,000 bus cycles of inactivity the bus is assumed to be in sleep mode. Normally entering sleep mode can be avoided, if the LIN master is regularly creating some bus activity. Otherwise the timeout state needs to be detected by the application software, for example by setting a timer.

Both LIN masters and LIN slaves can cause the bus to exit sleep mode by sending a break signal. The LIN hardware will generate such a break, when WU bit in the LIN control register is written. After transmitting this break the LIN hardware will not send out data (that is not raise the TXRDY flag) before the wake-up delimiter period has expired. This period can be selected by setting the WUD bits in the LIN control register.

Break signals sent by a LIN slave are received by the LIN hardware, and so indicated by setting the WAKE flag in the LIN status register.

A physical bus error (LIN bus is permanently stuck at a fixed value) will set several error flags. If the input is permanently low, the eSCI will set the framing error (FE) flag in the eSCI status register. If the RXD input remains stuck at a fixed value for 15 cycles, after a transmission has started, the LIN hardware will set the PBERR flag in the LIN status register. In addition a bit error may be generated.

## 21.4.10.5 LIN Setup

Since the eSCI is for general-purpose use, some of the settings are not applicable for LIN operation. The following setup applies for most applications, regardless of which kind of LIN slave is addressed:

- a) The module is enabled by writing the ESCI x \_CR2[MDIS] bit to 0.
- b) Both transmitter and receiver are enabled (ESCI x \_CR1[TE] = 1, ESCI \_CR1[RE] = 1). x
- c) The data format bit ESCI x \_CR1[M], is set to 0 (8 data bits), and the parity is disabled (PE = 0).
- d) ESCI \_CR1[TIE], ESCI \_CR1[TCIE], ESCI \_CR1[RIE] interrupt enable bits should be x x x inactive. Instead, the LIN interrupts should be used.
- e) Switch eSCI to LIN mode (ESCI \_LCR[LIN] = 1). x
- f) The LIN standard requires that the break character always be 13 bits long (ESCI \_CR2[BRK13] = 1). The eSCI will work with BRK13=0, but it will violate LIN 2.0. x
- g) Normally, bit errors should cause the LIN FSM to reset, stop driving the bus immediately, and stop further DMA requests until the BERR flag has been cleared. Set  ESCI x \_LCR[LDBG] = 0, ESCI \_CR2[SBSTP] = 1, and ESCI \_CR2[BSTP] = 1 to accomplish these functions. x x
- h) Fast bit error detection provides superior error checking, so ESCI x \_CR2[FBR] should be set; normally it will be used with ESCI x \_CR2[BESM13] = 1.
- i) If available, a pulldown should be enabled on the RX input.  (Thus if the transceiver fails, the RX pin will not float).
- j) The error indicators NF, FE, BERR, STO, PBERR, CERR, CKERR, and OVFL should be enabled.
- k) Initially a wake-up character may need to be transmitted on the LIN bus, so that the LIN slaves activate.

Other settings like baud rate, length of break character etc., depend on the LIN slaves to which the eSCI is connected.

## 21.5 Revision History

Substantive Changes since Rev 3.0

No changes.
