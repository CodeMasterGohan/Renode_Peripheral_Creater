### Chatper 15 Internal Static RAM (SRAM)

## 15.1 Introduction

## 15.1.1 Block Diagram

The internal SRAM block diagram is shown in Figure 15-1

Figure 15-1. Internal SRAM Block Diagram

<!-- image -->

## 15.1.2 Overview

The SRAM provides 64 Kbytes of general-purpose system SRAM. The first 32-Kbyte block of the SRAM is powered by its own power supply pin for standby operation.

## 15.1.3 Features

The SRAM controller includes the following features:

- · Supports read/write accesses mapped to the SRAM memory from any master
- · 32-Kbyte block powered by separate supply for standby operation
- · Byte, halfword, word, and doubleword addressable
- · ECC performs single bit correction, double bit error detection

## 15.2 External Signal Description

The only external signal used by the SRAM is the V STBY  RAM power supply. If not used,   V STBY  is tied toV SS .

## 15.3 Memory Map/Register Definition

The SRAM occupies 64 Kbytes of address space. See Table 1-3.

Table 15-1 shows the SRAM memory map.

## Table 15-1. SRAM Memory Map

| Address            | Register Name   | Register Description            | Size      |
|--------------------|-----------------|---------------------------------|-----------|
| Base (0x4000_0000) | -               | 32-Kbyte RAM, Powered by V STBY | 32 Kbytes |
| Base + 0x8000      | -               | 32-Kbyte RAM                    | 32 Kbytes |

## 15.3.1 Register Descriptions

The internal SRAM has no registers. Registers associated with the SRAM ECC are located in the ECSM. See Section 8.2.1, 'Register Descriptions.'

## 15.4 Functional Description

The RAM BIU generates a 72-bit code word based upon a 64-bit data write. The ECC scheme will correct all single bit corrections, and flag all double-bit errors. Some bit errors greater than 2 bits will be flagged as multiple bit errors. The codeword of 72'b0 and 72'b1 will cause a multi-bit error. Detected multiple bit errors will assert an error indication with the bus cycle, as well as setting a flag.

## 15.4.1 SRAM ECC Mechanism

The ECC is calculated for each 64-bits of data. For example, for a byte write:

- 1. The 64-bit word (double word-aligned) is read, which causes a check of ECC on all 64-bits. If a correctable error is detected, it will be corrected prior to merging in the write data. If a non-correctable error occurs during the read portion of the write operation, then the write will not be performed.
- 2. The byte data is merged and the ECC is generated for the new 64-bit data value.
- 3. The data and ECC bits are written back.

In the case of a 64-bit write, the 64-bit word is not read for the merge operation. Instead, the ECC is generated for the 64-bit word data then both data and ECC bits are written. Because the ECC bits will contain random data after power on, the 64-bit write mechanism is used to initialize the SRAM and insure that the ECC bits are valid. See Section 15.5, 'Initialization/Application Information.'

## 15.4.2 Access Timing

The system bus is a two-stage pipelined bus, which makes the timing of any access dependent on the access during the previous clock. Table 15-2 shows the wait states for accesses, column Current is the access being measured, and column Previous is the RAM access during the previous clock.

Table 15-2. Wait States During RAM Access

| Current        | Previous          | Waits                                   |
|----------------|-------------------|-----------------------------------------|
| Read           | Idle              | 1                                       |
| Read           | Pipelined Read    | 1                                       |
| Read           | Burst Read        | 1                                       |
| Read           | 64-bit Write      | 2                                       |
| Read           | 8/16/32-bit Write | 0(if reading from the same address)     |
| Read           | 8/16/32-bit Write | 1 (if reading from a different address) |
| Pipelined Read | Read              | 0                                       |
| Burst Read     | idle              | 1,0,0,0                                 |

Table 15-2. Wait States During RAM Access (continued)

| Current                     | Previous                    | Waits                               |
|-----------------------------|-----------------------------|-------------------------------------|
| 8/16/32-bit Write           | idle                        | 1                                   |
| 8/16/32-bit Write           | Read                        | 1                                   |
| 8/16/32-bit Write           | Pipelined 8/16/32-bit write | 2                                   |
| 8/16/32-bit Write           | 64-bit write                | 2                                   |
| 8/16/32-bit Write           | 8/16/32-bit write           | 0 (if writing to the same addrerss) |
| Pipelined 8/16/32-bit Write | 8/16/32-bit Write           | 0                                   |
| 64-bit Write                | idle                        | 0                                   |
| 64-bit Write                | 64-bit Write                | 0                                   |
| 64-bit Write                | Read                        | 0                                   |
| 64-bit Burst Write          | idle                        | 0,0,0,0                             |
| 64-bit Burst Write          | 64-bit Write                | 0,0,0,0                             |
| 64-bit Burst Write          | Read                        | 0,0,0,0                             |

## 15.4.3 Reset Operation

When a reset event asserts while an access to system memory is in progress, the access will either complete successfully, or will not occur, depending on the cycle at which the reset occurs. Any data stored during such an access will be the intended data, and no other address locations will be accessed or changed. If the system RAM is cached, dirty cache lines may not be completely written to memory unless the region is set for write through mode.

## 15.5 Initialization/Application Information

In order to use the SRAM, it is essential for the ECC check bits to be initialized after power on. A 64-bit cache inhibited write to each location in SRAM should be used to initialize the SRAM array as part of the application initialization code. The write transfer must be 64 bits in size, otherwise the write transfer will generate  a  read  /  modify  /  write  operation  which  will  check  the  ECC  value  upon  the  read.  See Section 15.4.1, 'SRAM ECC Mechanism.'

## NOTE

The SRAM must be initialized, even if the application does not use ECC reporting.

## 15.5.1 Example Code

For  proper  initialization,  a  64-bit  write  must  be  made  to  all  SRAM  locations.  The  PowerPC  BookE instruction set provides the store multiple word ( stmw) instruction to implement 64-bit writes. The stmw instruction concatenates two 32-bit registers for use as a single 64-bit write. To insure that the writes are

## Internal Static RAM (SRAM)

64-bit, the writes must be made on 64-bit word aligned boundaries, and an even number of registers should be specified.

The following example code illustrates the use of the stmw instruction to initialize the SRAM ECC bits.

init\_L2RAM:

```
lis r11,0x4000 # base address of the L2SRAM, 64-bit word aligned ori r11,r11,0 # not needed for this address but could be forothers li r12,512 # loop counter to get all of L2SRAM; # 64k/4 bytes/32 GPRs = 512 mtctr r12 init_l2ram_loop: stmw r0,0(r11) # write all 32 GPRs to L2SRAM addi r11,r11,128 # inc the ram ptr; 32 GPRs * 4 bytes = 128 bdnz init_l2ram_loop # loop for 64k of L2SRAM blr # done
```

## 15.6 Revision History

## Substantive Changes since Rev 3.0

```
Added Section 15.4.3, 'Reset Operation.'
```
