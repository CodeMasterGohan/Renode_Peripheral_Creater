### Chatper 8

## Error Correction Status Module (ECSM)

## 8.1 Introduction

The MPC5553/MPC5554 includes error-correcting code (ECC) implementations to improve the quality and reliability of internal SRAM and internal flash memories. The error correction status module (ECSM), provides a means for the application to collect information on memory errors reported by ECC and/or generic access error information.

## 8.1.1 Overview

The ECSM provides a set of registers that configure and report ECC errors for the MPC5553/MPC5554 device including accesses to SRAM and Flash memory. The application may configure the device for the types of memory errors to be reported, and then query a set of read-only status and information registers to identify any errors that have been signalled.

There are two types of ECC errors: correctable and non-correctable. A correctable ECC error is generated when only one bit is wrong in a 64-bit double word. In this case it is corrected automatically by hardware, and no flags or other indication is set that the error occurred. A non-correctable ECC error is generated when 2 bits in a 64-bit double word are incorrect. Non-correctable ECC errors cause an interrupt, and if enabled, additional error details are available in the ECSM.

Error correction is implemented on 64 bits of data at a time, using 8 bits for ECC for every 64-bit double word. ECC is checked on reads, and calculated on writes per the following:

- 1. 64 bits containing the desired byte / half word / word or double word in memory is read, and ECC checked.
- 2. If the access is a write, then
- - The new byte / half word / word / double word is merged into the 64 bits.
- - New ECC bits are calculated.
- - The 64 bits and the new ECC bits are written back.

In order to use ECC with SRAM, the SRAM memory must be written to before ECC is enabled. See Section 15.5, 'Initialization/Application Information.'

## 8.1.2 Features

The ECSM includes these features:

- · Configurable for reporting non-correctable errors
- · Registers for capturing ECC information for RAM access errors
- · Registers for capturing ECC information for Flash access errors

## 8.2 Memory Map/Register Definition

This section details the programming model for the ECSM. Table 8-1 is the memory map for the ECSM registers.

## Table 8-2. ECSM Memory Map

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

| Address                                  | Register Name   | Register Description                                          | Size (bits)   |
|------------------------------------------|-----------------|---------------------------------------------------------------|---------------|
| Base (0xFFF4_0000) + 0x016               | ECSM_SWTCR      | Software watchdog timer control register 1                    | 16            |
| Base + 0x018- Base + 0x01A               | -               | Reserved                                                      | -             |
| Base + 0x01B                             | ECSM_SWTSR      | Software watchdog timer service register 1                    | 8             |
| Base + 0x01C- Base + 0x01E               | -               | Reserved                                                      | -             |
| Base + 0x01F                             | ECSM_SWTIR      | Software watchdog timer interrupt register 1                  | 8             |
| Base + 0x020- Base + 0x023               | -               | Reserved                                                      | -             |
| Base (0xFFF4_0000) + 0x024- Base + 0x027 | FBOMCR          | FEC Burst Optimization Master Control Register (MPC5553 Only) | 32            |
| Base + 0x028- Base + 0x042               | -               | Reserved                                                      | -             |
| Base (0xFFF4_0000) + 0x043               | ECSM_ECR        | ECC configuration register                                    | 8             |
| Base + 0x044- Base + 0x046               | -               | Reserved                                                      | -             |
| Base + 0x047                             | ECSM_ESR        | ECC status register                                           | 8             |
| Base + 0x048- Base + 0x049               | -               | Reserved                                                      | -             |
| Base + 0x04A                             | ECSM_EEGR       | ECC error generation register                                 | 16            |
| Base + 0x04B- Base + 0x04F               | -               | Reserved                                                      | -             |
| Base + 0x050                             | ECSM_FEAR       | Flash ECC address register                                    | 32            |
| Base + 0x054- Base + 0x055               | -               | Reserved                                                      | -             |
| Base + 0x056                             | ECSM_FEMR       | Flash ECC master register                                     | 8             |
| Base + 0x057                             | ECSM_FEAT       | Flash ECC attribute register                                  | 8             |
| Base + 0x058                             | ECSM_FEDRH      | Flash ECC data high register                                  | 32            |
| Base + 0x05C                             | ECSM_FEDRL      | Flash ECC data low register                                   | 32            |
| Base + 0x060                             | ECSM_REAR       | RAM ECC address register                                      | 32            |
| Base + 0x064- Base + 0x065               | -               | Reserved                                                      | -             |
| Base + 0x066                             | ECSM_REMR       | RAM ECC master register                                       | 8             |
| Base + 0x067                             | ECSM_REAT       | RAM ECC attributes register                                   | 8             |
| Base + 0x068                             | ECSM_REDRH      | RAM ECC data high register                                    | 32            |
| Base + 0x06C                             | ECSM_REDRL      | RAM ECC data low register                                     | 32            |
| Base + 0x070- Base + 0x07F               | -               | Reserved                                                      | -             |

- 1 These registers provide control and configuration for a software watchdog timer, and are included as part of a standard Freescale ECSM module incorporated in the MPC5553/MPC5554. The e200z6 core also provides this functionality and is the preferred method for watchdog implementation. See Section 8.2.1.1.

## 8.2.1 Register Descriptions

Attempted  accesses  to  reserved  addresses  result  in  an  error  termination,  while  attempted  writes  to read-only registers are ignored and do not terminate with an error. Unless noted otherwise, writes to the programming model must match the size of the register; for example, an n -bit register only supports n -bit writes, etc. Attempted writes of a different size than the register width produce an error termination of the bus cycle and no change to the targeted register.

## 8.2.1.1 Software Watchdog Timer Control, Service, and Interrupt Registers (ECSM\_SWTCR, ECSM\_SWTSR, and ECSM\_SWTIR)

These registers provide control and configuration for a software watchdog timer, and are included as part of a standard Freescale ECSM module incorporated in the MPC5553/MPC5554. The e200z6 core also provides this functionality and is the preferred method for watchdog implementation. In order to optimize code portability to other members of this eSys-based MPU family, use of the watchdog registers in the ECSM is not recommended.

The values in these registers should be left in their reset state. Any change from reset values may cause an unintentional ECSM\_SWTIR\_SWTIC interrupt.

## 8.2.1.2 ECC Registers

There are a number of program-visible registers for the sole purpose of reporting and logging of memory failures. These registers include the following:

- · ECC configuration register (ECSM\_ECR)
- · ECC status register (ECSM\_ESR)
- · Flash ECC address register (ECSM\_FEAR)
- · Flash ECC master number register (ECSM\_FEMR)
- · Flash ECC attributes register (ECSM\_FEAT)
- · Flash ECC data register (ECSM\_FEDR)
- · RAM ECC address register (ECSM\_REAR)
- · RAM ECC master number register (ECSM\_REMR)
- · RAM ECC attributes register (ECSM\_REAT)
- · RAM ECC data register (ECSM\_REDR)

The details on the ECC registers are provided in the subsequent sections.

## 8.2.1.3 ECC Configuration Register (ECSM\_ECR)

The ECSM\_ECR is an 8-bit control register for specifying whether memory errors are reported during RAM or  Flash  accesses.  The  occurrence  of  a  non-correctable  error  causes  the  current  access  to  be terminated  with  an  error  condition.  In  many  cases,  this  error  termination  is  reported  directly  by  the initiating  bus  master.  The  ECC  reporting  logic  in  the  ECSM  provides  an  optional  error  interrupt mechanism to signal non-correctable memory errors. In addition to the interrupt generation, the ECSM captures specific information (memory address, attributes and data, bus master number, etc.) which may be useful for subsequent failure analysis.

Figure 8-1. ECC Configuration Register (ECSM\_ECR)

<!-- image -->

|          | 0                         | 1                         | 2                         | 3                         | 4                         | 5                         | 6                         | 7                         |
|----------|---------------------------|---------------------------|---------------------------|---------------------------|---------------------------|---------------------------|---------------------------|---------------------------|
| R        | 0                         | 0                         | 0                         | 0                         | 0                         | 0                         | ERNCR                     | EFNCR                     |
| W        |                           |                           |                           |                           |                           |                           |                           |                           |
| Reset    | 0                         | 0                         | 0                         | 0                         | 0                         | 0                         | 0                         | 0                         |
| Reg Addr | Base (0xFFF4_0000) + 0x43 | Base (0xFFF4_0000) + 0x43 | Base (0xFFF4_0000) + 0x43 | Base (0xFFF4_0000) + 0x43 | Base (0xFFF4_0000) + 0x43 | Base (0xFFF4_0000) + 0x43 | Base (0xFFF4_0000) + 0x43 | Base (0xFFF4_0000) + 0x43 |

Table 8-3. ECSM\_ECR Field Definitions

| Bits   | Name   | Description                                                                                                                                                                                                                                                                                                                                                                                                        |
|--------|--------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-5    | -      | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                          |
| 6      | ERNCR  | Enable RAMnon-correctable reporting. The occurrence of a non-correctable multi-bit RAM error generates a ECSM ECC interrupt request as signalled by the assertion of ECSM_ESR[RNCE]. The faulting address, attributes and data are also captured in the REAR, REMR, REAT and REDR registers. 0 Reporting of non-correctable RAM errors is disabled. 1 Reporting of non-correctable RAM errors is enabled.          |
| 7      | EFNCR  | Enable Flash non-correctable reporting. The occurrence of a non-correctable multi-bit Flash error generates a ECSM ECC interrupt request as signalled by the assertion of ECSM_ESR[FNCE]. The faulting address, attributes and data are also captured in the FEAR, FEMR, FEAT and FEDR registers. 0 Reporting of non-correctable Flash errors is disabled. 1 Reporting of non-correctable Flash errors is enabled. |

## 8.2.1.4 ECC Status Register (ECSM\_ESR)

The ECSM\_ESR is an 8-bit control register for signaling which types of properly-enabled ECC events have  been  detected.  The  ESR  signals  the  last,  properly-enabled  memory  event  to  be  detected.  The generation of the ECSM ECC interrupt request is defined by the boolean equation:

```
ECSM_ECC_IRQ =  ECSM_ECR[ERNCR] &  ECSM_ESR[RNCE] |  ECSM_ECR[EFNCR] &  ECSM_ESR[FNCE]
```

```
// ram,   noncorrectable error // Flash, noncorrectable error
```

where  the  combination  of  a  properly-enabled  category  in  the  ECSM\_ECR  and  the  detection  of  the corresponding condition in the ECSM\_ESR produces the interrupt request.

The ECSM allows a maximum of one bit of the ECSM\_ESR to be asserted at any given time. This preserves the association between the ECSM\_ESR and the corresponding address and attribute registers, which  are  loaded  on  each  occurrence  of  an  properly-enabled  ECC  event.  If  there  is  a  pending  ECC interrupt and another properly-enabled ECC event occurs, the ECSM hardware automatically handles the ECSM\_ESR reporting, clearing the previous data and loading the new state and thus guaranteeing that only a single flag is asserted.

To maintain the coherent software view of the reported event, the following sequence in the ECSM error interrupt service routine is suggested:

- 1. Read the ECSM\_ESR and save it.
- 2. Read and save all the address and attribute reporting registers.

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

- 3. Re-read the ECSM\_ESR and verify the current contents matches the original contents. If the two values are different, go back to step 1 and repeat.
- 4. When the values are identical, write a 1 to the asserted ECSM\_ESR flag to negate the interrupt request.

In the event that multiple status flags are signaled simultaneously, ECSM records the event with the RNCE as highest priority, and then FNCE.

Figure 8-2. ECC Status Register (ECSM\_ESR)

|          | 0           | 1           | 2           | 3           | 4           | 5           | 6           | 7           |
|----------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|
| R        | 0           | 0           | 0           | 0           | 0           | 0           | RNCE        | FNCE        |
| W        |             |             |             |             |             |             | w1c         | w1c         |
| Reset    | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           |
| Reg Addr | Base + 0x47 | Base + 0x47 | Base + 0x47 | Base + 0x47 | Base + 0x47 | Base + 0x47 | Base + 0x47 | Base + 0x47 |

Table 8-4. ECSM\_ESR Field Definitions

| Bits   | Name   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|--------|--------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-5    | -      | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| 6      | RNCE   | RAM non-correctable error. The occurrence of a properly-enabled non-correctable RAM error generates an ECSMECCinterrupt request. The faulting address, attributes and data are also captured in the REAR, REMR, REAT and REDR registers. To clear this interrupt flag, write a 1 to this bit. Writing a 0 has no effect. 0 No reportable non-correctable RAM error has been detected. 1 A reportable non-correctable RAM error has been detected.         |
| 7      | FNCE   | Flash non-correctable error. The occurrence of a properly-enabled non-correctable Flash error generates an ECSMECCinterrupt request. The faulting address, attributes and data are also captured in the FEAR, FEMR, FEAT and FEDR registers. To clear this interrupt flag, write a 1 to this bit. Writing a 0 has no effect. 0 No reportable non-correctable Flash error has been detected. 1 A reportable non-correctable Flash error has been detected. |

## 8.2.1.5 ECC Error Generation Register (ECSM\_EEGR)

The ECSM\_EEGR is a 16-bit control register used to force the generation of double-bit data errors in the internal SRAM. This capability provides a mechanism to allow testing of the software service routines associated with memory error logging.The intent is to generate errors during data write cycles, such that subsequent reads of the corrupted address locations generate ECC events, double-bit noncorrectable errors that are terminated with an error response.

If an attempt to force a non-correctable error (by asserting ECSM\_EEGR[FRCNCI] or ECSM\_EEGR[FRC1NCI]) and ECSM\_EEGR[ERRBIT] equals 64, then no data error will be generated.

## NOTE

The only allowable values for the 2 control bit enables {FRCNCI, FR1NCI} are {0,0}, {1,0} and {0,1}. The value {1,1} results in undefined behavior.

Figure 8-3. ECC Error Generation (ECSM\_EEGR) Register

<!-- image -->

Table 8-5. ECSM\_EEGR Field Definitions

| Bits   | Name   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
|--------|--------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-5    | -      | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| 6      | FRCNCI | Force internal SRAM continuous noncorrectable data errors. 0 No internal SRAM continuous 2-bit data errors are generated. 1 2-bit data errors in the internal SRAM are continuously generated. The assertion of this bit forces the internal SRAMcontroller to create 2-bit data errors, as defined by the bit position specified in ERRBIT[0:6] and the overall odd parity bit, continuously on every write operation. The normal ECCgeneration takes place in the RAMcontroller, but then the polarity of the bit position defined by ERRBIT and the overall odd parity bit are inverted to introduce a 2-bit ECC error in the RAM.                                                                                                                                                                                                                   |
| 7      | FR1NCI | Force internal SRAM one noncorrectable data errors. 0 No internal SRAM single 2-bit data errors are generated. 1 One 2-bit data error in the internal SRAM is generated. The assertion of this bit forces the internal SRAM controller to create one 2-bit data error, as defined by the bit position specified in ERRBIT[0:6] and the overall odd parity bit, on the first write operation after this bit is set. The normal ECC generation takes place in the internal SRAM controller, but then the polarity of the bit position defined by ERRBIT and the overall odd parity bit are inverted to introduce a 2-bit ECC error in the RAM. After this bit has been enabled to generate a single 2-bit error, it must be cleared before being set again to properly re-enable the error generation logic.                                              |
| 8      | -      | Reserved                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| 9-15   | ERRBIT | Error bit position. Defines the bit position which is complemented to create the data error on the write operation. The bit specified by this field plus the odd parity bit of the ECC code are inverted. The internal SRAM controller follows a vector bit ordering scheme where LSB=0. Errors in the ECC syndrome bits can be generated by setting this field to a value greater than the internal SRAMwidth. The following association between the ERRBIT field and the corrupted memory bit is defined: if ERRBIT = 0, then RAM[0] is inverted if ERRBIT = 1, then RAM[1] is inverted ... if ERRBIT = 63, then RAM[63] is inverted if ERRBIT = 64, then ECC Parity[0] is inverted if ERRBIT = 65, then ECC Parity[1] is inverted ... if ERRBIT = 71, then ECC Parity[7] is inverted For ERRBIT values greater than 71, no bit position is inverted. |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## 8.2.1.6 Flash ECC Address Register (ECSM\_FEAR)

The ECSM\_FEAR is a 32-bit register for capturing the address of the last, properly-enabled ECC event in the Flash memory. Depending on the state of the ECSM\_ECR, an ECC event in the Flash causes the address, attributes and data associated with the access to be loaded into the ECSM\_FEAR, ECSM\_FEMR, ECSM\_FEAT, and ECSM\_FEDR registers, and the appropriate flag (F1BC or FNCE) in the ECSM\_ESR to be asserted.

The address that is captured in ECSM\_FEAR is the Flash page address as seen on the system bus. Refer to Section 13.3.2.7, 'Address Register (FLASH\_AR)' to retrieve the double word address.

|          | 0           | 1           | 2           | 3           | 4           | 5           | 6           | 7           | 8           | 9           | 10          | 11          | 12          | 13          | 14          | 15          |
|----------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|
| R        | FEAR        | FEAR        | FEAR        | FEAR        | FEAR        | FEAR        | FEAR        | FEAR        | FEAR        | FEAR        | FEAR        | FEAR        | FEAR        | FEAR        | FEAR        | FEAR        |
| W        |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |
| Reset    | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           |
| Reg Addr | Base + 0x50 | Base + 0x50 | Base + 0x50 | Base + 0x50 | Base + 0x50 | Base + 0x50 | Base + 0x50 | Base + 0x50 | Base + 0x50 | Base + 0x50 | Base + 0x50 | Base + 0x50 | Base + 0x50 | Base + 0x50 | Base + 0x50 | Base + 0x50 |

|          | 16          | 17          | 18          | 19          | 20          | 21          | 22          | 23          | 24          | 25          | 26          | 27          | 28          | 29          | 30          | 31          |
|----------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|
| R        | FEAR        | FEAR        | FEAR        | FEAR        | FEAR        | FEAR        | FEAR        | FEAR        | FEAR        | FEAR        | FEAR        | FEAR        | FEAR        | FEAR        | FEAR        | FEAR        |
| W        |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |
| Reset    | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           |
| Reg Addr | Base + 0x50 | Base + 0x50 | Base + 0x50 | Base + 0x50 | Base + 0x50 | Base + 0x50 | Base + 0x50 | Base + 0x50 | Base + 0x50 | Base + 0x50 | Base + 0x50 | Base + 0x50 | Base + 0x50 | Base + 0x50 | Base + 0x50 | Base + 0x50 |

<!-- image -->

Figure 8-4. Flash ECC Address Register (ECSM\_FEAR)

Table 8-6. ECSM\_FEAR Field Descriptions

| Bits   | Name        | Description                                                                                            |
|--------|-------------|--------------------------------------------------------------------------------------------------------|
| 0-31   | FEAR [0:31] | Flash ECC address. Contains the faulting access address of the last, properly-enabled Flash ECC event. |

## 8.2.1.7 Flash ECC Master Number Register (ECSM\_FEMR)

The FEMR is an 8-bit register for capturing the XBAR bus master number of the last, properly-enabled ECC event in the Flash memory. Depending on the state of the ECSM\_ECR, an ECC event in the Flash causes the address, attributes and data associated with the access to be loaded into the ECSM\_FEAR, ECSM\_FEMR,  ECSM\_FEAT  and  ECSM\_FEDR  registers,  and  the  appropriate  flag  (FNCE)  in  the ECSM\_ESR to be asserted.

<!-- image -->

|          | 0   | 1   | 2   | 3                | 4                | 5    | 6   | 7   |
|----------|-----|-----|-----|------------------|------------------|------|-----|-----|
| R        | 0   | 0   | 0   | 0                |                  | FEMR |     |     |
| W        |     |     |     |                  |                  |      |     |     |
| Reset    | 0   | 0   | 0   | 0                | U                | U    | U   | U   |
| Reg Addr |     |     |     | ECSM Base + 0x56 | ECSM Base + 0x56 |      |     |     |

1 'U' signifies a bit that is uninitialized. Refer to the Preface of the book.

Figure 8-5. Flash ECC Master Number Register (ECSM\_FEMR)

Table 8-7. ECSM\_FEMR Field Descriptions

| Name   | Descriptio n   | Value                                                                                                                                                                          |
|--------|----------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-3    | -              | Reserved.                                                                                                                                                                      |
| 4-7    | FEMR [0:3]     | Flash ECC master number. Contains the XBAR bus master number of the faulting access of the last, properly-enabled Flash ECC event. The reset value of this field is undefined. |

## 8.2.1.8 Flash ECC Attributes Register (ECSM\_FEAT)

The  ECSM\_FEAT  is  an  8-bit  register  for  capturing  the  XBAR  bus  master  attributes  of  the  last, properly-enabled ECC event in the Flash memory. Depending on the state of the ECSM\_ECR register, an ECC event in the Flash causes the address, attributes, and data associated with the access to be loaded into the ECSM\_FEAR, ECSM\_FEMR, ECSM\_FEAT, and ECSM\_FEDRs, and the appropriate flag (FNCE) in the ECSM\_ESR to be asserted.

<!-- image -->

Figure 8-6. Flash ECC Attributes Register (ECSM\_FEAT)

Table 8-8. ECSM\_FEAT Field Descriptions

| Bits   | Name       | Description                                                                                                                                                                       |
|--------|------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0      | WRITE      | Write. The reset value of this field is undefined. 0 System bus read access 1 System bus write access                                                                             |
| 1-3    | SIZE [0:2] | Size. The reset value of this field is undefined. 000 8-bit System bus access 001 16-bit System bus access 010 32-bit System bus access 011 64-bit System bus access 1xx Reserved |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 8-8. ECSM\_FEAT Field Descriptions (continued)

|   Bits | Name   | Description                                                                                   |
|--------|--------|-----------------------------------------------------------------------------------------------|
|      4 | PROT0  | Protection: cache. The reset value of this field is undefined. 0 Non-cacheable 1 Cacheable    |
|      5 | PROT1  | Protection: buffer. The reset value of this field is undefined. 0 Non-bufferable 1 Bufferable |
|      6 | PROT2  | Protection: mode. The reset value of this field is undefined. 0 User mode 1 Supervisor mode   |
|      7 | PROT3  | Protection: type. The reset value of this field is undefined. 0 I-Fetch 1 Data                |

## 8.2.1.9 Flash ECC Data High Register (ECSM\_FEDRH)

The ECSM\_FEDRH and ECSM\_FEDRL are 32-bit registers for capturing the data associated with the last, properly-enabled ECC event in the Flash memory. Depending on the state of the ECSM\_ECR, an ECC event in the Flash causes the address, attributes and data associated with the access to be loaded into the ECSM\_FEAR, ECSM\_FEMR, ECSM\_FEAT and ECSM\_FEDRs, and the appropriate flag (FNCE) in the ECSM\_ESR to be asserted.

The data captured on a multi-bit non-correctable ECC error is undefined.

|          | 0           | 1           | 2           | 3           | 4           | 5           | 6           | 7           | 8           | 9           | 10          | 11          | 12          | 13          | 14          | 15          |
|----------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|
| R        | FEDH        | FEDH        | FEDH        | FEDH        | FEDH        | FEDH        | FEDH        | FEDH        | FEDH        | FEDH        | FEDH        | FEDH        | FEDH        | FEDH        | FEDH        | FEDH        |
| W        |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |
| Reset    | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           |
| Reg Addr | Base + 0x58 | Base + 0x58 | Base + 0x58 | Base + 0x58 | Base + 0x58 | Base + 0x58 | Base + 0x58 | Base + 0x58 | Base + 0x58 | Base + 0x58 | Base + 0x58 | Base + 0x58 | Base + 0x58 | Base + 0x58 | Base + 0x58 | Base + 0x58 |
|          | 16          | 17          | 18          | 19          | 20          | 21          | 22          | 23          | 24          | 25          | 26          | 27          | 28          | 29          | 30          | 31          |
| R        | FEDH        | FEDH        | FEDH        | FEDH        | FEDH        | FEDH        | FEDH        | FEDH        | FEDH        | FEDH        | FEDH        | FEDH        | FEDH        | FEDH        | FEDH        | FEDH        |
| W        |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |
| Reset    | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           |
| Reg Addr | Base + 0x58 | Base + 0x58 | Base + 0x58 | Base + 0x58 | Base + 0x58 | Base + 0x58 | Base + 0x58 | Base + 0x58 | Base + 0x58 | Base + 0x58 | Base + 0x58 | Base + 0x58 | Base + 0x58 | Base + 0x58 | Base + 0x58 | Base + 0x58 |

1 'U' signifies a bit that is uninitialized. Refer to the Preface of the book.

Figure 8-7. Flash ECC Data High Register (ECSM\_FEDRH)

Table 8-9. ECSM\_FEDRH Field Descriptions

| Bits   | Name        | Description                                                                                                                                                                                                                            |
|--------|-------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-31   | FEDH [0:31] | Flash ECC data. Contains the data associated with the faulting access of the last, properly-enabled Flash ECCevent. The register contains the data value taken directly from the data bus. The reset value of this field is undefined. |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## 8.2.1.10 Flash ECC Data Low Registers (ECSM\_FEDRL)

The ECSM\_FEDRH and ECSM\_FEDRL are 32-bit registers for capturing the data associated with the last, properly-enabled ECC event in the Flash memory. Depending on the state of the ECSM\_ECR, an ECC event in the Flash causes the address, attributes and data associated with the access to be loaded into the ECSM\_FEAR, ECSM\_FEMR, ECSM\_FEAT and ECSM\_FEDRs, and the appropriate flag (FNCE) in the ECSM\_ESR to be asserted.

The data captured on a multi-bit non-correctable ECC error is undefined.

<!-- image -->

|          | 0           | 1           | 2           | 3           | 4           | 5           | 6           | 7           | 8           | 9           | 10          | 11          | 12          | 13          | 14          | 15          |
|----------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|
| R        | FEDL        | FEDL        | FEDL        | FEDL        | FEDL        | FEDL        | FEDL        | FEDL        | FEDL        | FEDL        | FEDL        | FEDL        | FEDL        | FEDL        | FEDL        | FEDL        |
| W        |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |
| Reset    | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           |
| Reg Addr | Base + 0x5C | Base + 0x5C | Base + 0x5C | Base + 0x5C | Base + 0x5C | Base + 0x5C | Base + 0x5C | Base + 0x5C | Base + 0x5C | Base + 0x5C | Base + 0x5C | Base + 0x5C | Base + 0x5C | Base + 0x5C | Base + 0x5C | Base + 0x5C |
|          | 16          | 17          | 18          | 19          | 20          | 21          | 22          | 23          | 24          | 25          | 26          | 27          | 28          | 29          | 30          | 31          |
| R        | FEDL        | FEDL        | FEDL        | FEDL        | FEDL        | FEDL        | FEDL        | FEDL        | FEDL        | FEDL        | FEDL        | FEDL        | FEDL        | FEDL        | FEDL        | FEDL        |
| W        |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |
| Reset    | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           |
| Reg Addr | Base + 0x5C | Base + 0x5C | Base + 0x5C | Base + 0x5C | Base + 0x5C | Base + 0x5C | Base + 0x5C | Base + 0x5C | Base + 0x5C | Base + 0x5C | Base + 0x5C | Base + 0x5C | Base + 0x5C | Base + 0x5C | Base + 0x5C | Base + 0x5C |

1 'U' signifies a bit that is uninitialized. Refer to the Preface of the book.

Figure 8-8. Flash ECC Data Low Register (ECSM\_FEDRL)

Table 8-10. ECSM\_FEDRL Field Descriptions

| Bits   | Name        | Description                                                                                                                                                                                                                            |
|--------|-------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-31   | FEDL [0:31] | Flash ECC data. Contains the data associated with the faulting access of the last, properly-enabled Flash ECCevent. The register contains the data value taken directly from the data bus. The reset value of this field is undefined. |

## 8.2.1.11 RAM ECC Address Register (ECSM\_REAR)

The ECSM\_REAR is a 32-bit register for capturing the address of the last, properly-enabled ECC event in the RAM memory. Depending on the state of the ECSM\_ECR, an ECC event in the RAM causes the address, attributes and data associated with the access to be loaded into the ECSM\_REAR, ECSM\_REMR, ECSM\_REAT and ECSM\_REDRs, and the appropriate flag (RNCE) in the ECSM\_ESR to be asserted.

<!-- image -->

|          | 0           | 1           | 2           | 3           | 4           | 5           | 6           | 7           | 8           | 9           | 10          | 11          | 12          | 13          | 14          | 15          |
|----------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|
| R        | REAR        | REAR        | REAR        | REAR        | REAR        | REAR        | REAR        | REAR        | REAR        | REAR        | REAR        | REAR        | REAR        | REAR        | REAR        | REAR        |
| W        |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |
| Reset    | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           |
| Reg Addr | Base + 0x60 | Base + 0x60 | Base + 0x60 | Base + 0x60 | Base + 0x60 | Base + 0x60 | Base + 0x60 | Base + 0x60 | Base + 0x60 | Base + 0x60 | Base + 0x60 | Base + 0x60 | Base + 0x60 | Base + 0x60 | Base + 0x60 | Base + 0x60 |
|          | 16          | 17          | 18          | 19          | 20          | 21          | 22          | 23          | 24          | 25          | 26          | 27          | 28          | 29          | 30          | 31          |
| R        | REAR        | REAR        | REAR        | REAR        | REAR        | REAR        | REAR        | REAR        | REAR        | REAR        | REAR        | REAR        | REAR        | REAR        | REAR        | REAR        |
| W        |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |
| Reset    | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           |
| Reg Addr | Base + 0x60 | Base + 0x60 | Base + 0x60 | Base + 0x60 | Base + 0x60 | Base + 0x60 | Base + 0x60 | Base + 0x60 | Base + 0x60 | Base + 0x60 | Base + 0x60 | Base + 0x60 | Base + 0x60 | Base + 0x60 | Base + 0x60 | Base + 0x60 |

1 'U' signifies a bit that is uninitialized. Refer to the Preface of the book.

Figure 8-9. RAM ECC Address Register (ECSM\_REAR)

Table 8-11. ECSM\_REAR Field Descriptions

| Bits   | Name        | Description                                                                                                                                    |
|--------|-------------|------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-31   | REAR [0:31] | RAM ECC address. Contains the faulting access address of the last, properly-enabled RAM ECC event. The reset value of this field is undefined. |

## 8.2.1.12 RAM ECC Master Number Register (ECSM\_REMR)

The REMR is an 8-bit register for capturing the XBAR bus master number of the last, properly-enabled ECC event in the RAM memory. Depending on the state of the ECSM\_ECR, an ECC event in the RAM causes the address, attributes and data associated with the access to be loaded into the ECSM\_REAR, ECSM\_REMR, ECSM\_REAT and ECSM\_REDRs, and the appropriate flag (RNCE) in the ECSM\_ESR to be asserted.

<!-- image -->

|          | 0   | 1   | 2   | 3   | 4           | 5    | 6   | 7   |
|----------|-----|-----|-----|-----|-------------|------|-----|-----|
| R        | 0   | 0   | 0   | 0   |             | REMR |     |     |
| W        |     |     |     |     |             |      |     |     |
| Reset    | 0   | 0   | 0   | 0   | U           | U    | U   | U   |
| Reg Addr |     |     |     |     | Base + 0x66 |      |     |     |

1 'U' signifies a bit that is uninitialized. Refer to the Preface of the book.

Figure 8-10. RAM ECC Master Number Register (ECSM\_REMR)

Table 8-12. ECSM\_REMR Field Descriptions

| Bits   | Name       | Description                                                                                                                                                                |
|--------|------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-3    | -          | Reserved.                                                                                                                                                                  |
| 4-7    | REMR [0:3] | RAM ECC master number. Contains the XBAR bus master number of the faulting access of the last, properly-enabled RAM ECC event. The reset value of this field is undefined. |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## 8.2.1.13 RAM ECC Attributes Register (ECSM\_REAT)

The  ECSM\_REAT  is  an  8-bit  register  for  capturing  the  XBAR  bus  master  attributes  of  the  last, properly-enabled ECC event in the RAM memory. Depending on the state of the ECSM\_ECR, an ECC event in the RAM causes the address, attributes and data associated with the access to be loaded into the ECSM\_REAR, ECSM\_REMR, ECSM\_REAT and ECSM\_REDRs, and the appropriate flag (RNCE) in the ECSM\_ESR to be asserted.

<!-- image -->

|          | 0     | 1   | 2    | 3           | 4     | 5     | 6     | 7     |
|----------|-------|-----|------|-------------|-------|-------|-------|-------|
| R        | WRITE |     | SIZE |             | PROT0 | PROT1 | PROT2 | PROT3 |
| W        |       |     |      |             |       |       |       |       |
| Reset    | U     | U   | U    | U           | U     | U     | U     | U     |
| Reg Addr |       |     |      | Base + 0x67 |       |       |       |       |

1 'U' signifies a bit that is uninitialized. Refer to the Preface of the book.

Figure 8-11. RAM ECC Attributes Register (ECSM\_REAT)

Table 8-13. ECSM\_REAT Field Descriptions

| Bits   | Name       | Description                                                                                                                                                                       |
|--------|------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0      | WRITE      | Write. The reset value of this field is undefined. 0 System bus read access 1 System bus write access                                                                             |
| 1-3    | SIZE [0:2] | Size. The reset value of this field is undefined. 000 8-bit system bus access 001 16-bit system bus access 010 32-bit system bus access 011 64-bit system bus access 1xx Reserved |
| 4      | PROT0      | Protection: cache. The reset value of this field is undefined. 0 Non-cacheable 1 Cacheable                                                                                        |
| 5      | PROT1      | Protection: buffer. The reset value of this field is undefined. 0 Non-bufferable 1 Bufferable                                                                                     |
| 6      | PROT2      | Protection: mode. The reset value of this field is undefined. 0 User mode 1 Supervisor mode                                                                                       |
| 7      | PROT3      | Protection: type. The reset value of this field is undefined. 0 I-Fetch 1 Data                                                                                                    |

## 8.2.1.14 RAM ECC Data High Register (ECSM\_REDRH)

The ECSM\_REDRH and ECSM\_REDRL are 32-bit registers for capturing the data associated with the last, properly-enabled ECC event in the RAM memory. Depending on the state of the ECSM\_ECR, an ECC event in the RAM causes the address, attributes and data associated with the access to be loaded into

the  ECSM\_REAR, ECSM\_REMR, ECSM\_REAT, and ECSM\_REDRH and ECSM\_REDRL, and the appropriate flag (RFNCE) in the ECSM\_ESR to be asserted.

The data captured on a multi-bit non-correctable ECC error is undefined.

<!-- image -->

|          | 0           | 1           | 2           | 3           | 4           | 5           | 6           | 7           | 8           | 9           | 10          | 11          | 12          | 13          | 14          | 15          |
|----------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|
| R        | REDH        | REDH        | REDH        | REDH        | REDH        | REDH        | REDH        | REDH        | REDH        | REDH        | REDH        | REDH        | REDH        | REDH        | REDH        | REDH        |
| W        |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |
| Reset    | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           |
| Reg Addr | Base + 0x68 | Base + 0x68 | Base + 0x68 | Base + 0x68 | Base + 0x68 | Base + 0x68 | Base + 0x68 | Base + 0x68 | Base + 0x68 | Base + 0x68 | Base + 0x68 | Base + 0x68 | Base + 0x68 | Base + 0x68 | Base + 0x68 | Base + 0x68 |
|          | 16          | 17          | 18          | 19          | 20          | 21          | 22          | 23          | 24          | 25          | 26          | 27          | 28          | 29          | 30          | 31          |
| R        | REDH        | REDH        | REDH        | REDH        | REDH        | REDH        | REDH        | REDH        | REDH        | REDH        | REDH        | REDH        | REDH        | REDH        | REDH        | REDH        |
| W        |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |
| Reset    | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           | U           |
| Reg Addr | Base + 0x68 | Base + 0x68 | Base + 0x68 | Base + 0x68 | Base + 0x68 | Base + 0x68 | Base + 0x68 | Base + 0x68 | Base + 0x68 | Base + 0x68 | Base + 0x68 | Base + 0x68 | Base + 0x68 | Base + 0x68 | Base + 0x68 | Base + 0x68 |

1 'U' signifies a bit that is uninitialized. Refer to the Preface of the book.

Figure 8-12. RAM ECC Data High Register (ECSM\_REDRH)

## Table 8-14. ECSM\_REDRH Field Descriptions

| Bits   | Name        | Description                                                                                                                                                                                                                       |
|--------|-------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-31   | REDH [0:31] | RAM ECC data. Contains the data associated with the faulting access of the last, properly-enabled RAMECCevent. The register contains the data value taken directly from the data bus. The reset value of this field is undefined. |

## 8.2.1.15 RAM ECC Data Low Registers (ECSM\_REDRL)

The ECSM\_REDRH and ECSM\_REDRL are 32-bit registers for capturing the data associated with the last, properly-enabled ECC event in the RAM memory. Depending on the state of the ECSM\_ECR, an ECC event in the RAM causes the address, attributes and data associated with the access to be loaded into the  ECSM\_REAR,  ECSM\_REMR,  ECSM\_REAT,  ECSM\_REDRH,  and  ECSM\_REDRL,  and  the appropriate flag (RFNCE) in the ECSM\_ESR to be asserted.

The data captured on a multi-bit non-correctable ECC error is undefined.

<!-- image -->

|          | 0                | 1                | 2                | 3                | 4                | 5                | 6                | 7                | 8                | 9                | 10               | 11               | 12               | 13               | 14               | 15               |
|----------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|
| R        | REDL             | REDL             | REDL             | REDL             | REDL             | REDL             | REDL             | REDL             | REDL             | REDL             | REDL             | REDL             | REDL             | REDL             | REDL             | REDL             |
| W        |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |
| Reset    | U                | U                | U                | U                | U                | U                | U                | U                | U                | U                | U                | U                | U                | U                | U                | U                |
| Reg Addr | ECSM Base + 0x6C | ECSM Base + 0x6C | ECSM Base + 0x6C | ECSM Base + 0x6C | ECSM Base + 0x6C | ECSM Base + 0x6C | ECSM Base + 0x6C | ECSM Base + 0x6C | ECSM Base + 0x6C | ECSM Base + 0x6C | ECSM Base + 0x6C | ECSM Base + 0x6C | ECSM Base + 0x6C | ECSM Base + 0x6C | ECSM Base + 0x6C | ECSM Base + 0x6C |
|          | 16               | 17               | 18               | 19               | 20               | 21               | 22               | 23               | 24               | 25               | 26               | 27               | 28               | 29               | 30               | 31               |
| R        | REDL             | REDL             | REDL             | REDL             | REDL             | REDL             | REDL             | REDL             | REDL             | REDL             | REDL             | REDL             | REDL             | REDL             | REDL             | REDL             |
| W        |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |
| Reset    | U                | U                | U                | U                | U                | U                | U                | U                | U                | U                | U                | U                | U                | U                | U                | U                |
| Reg Addr | ECSM Base + 0x6C | ECSM Base + 0x6C | ECSM Base + 0x6C | ECSM Base + 0x6C | ECSM Base + 0x6C | ECSM Base + 0x6C | ECSM Base + 0x6C | ECSM Base + 0x6C | ECSM Base + 0x6C | ECSM Base + 0x6C | ECSM Base + 0x6C | ECSM Base + 0x6C | ECSM Base + 0x6C | ECSM Base + 0x6C | ECSM Base + 0x6C | ECSM Base + 0x6C |

1 'U' signifies a bit that is uninitialized. Refer to the Preface of the book.

Figure 8-13. RAM ECC Data Low Register (ECSM\_REDRL)

Table 8-15. ECSM\_REDRL Field Descriptions

| Bits   | Name        | Description                                                                                                                                                                                                                       |
|--------|-------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-31   | REDL [0:31] | RAM ECC data. Contains the data associated with the faulting access of the last, properly-enabled RAMECCevent. The register contains the data value taken directly from the data bus. The reset value of this field is undefined. |

## 8.3 Initialization/Application Information

In order to use the ECC mechanism for internal SRAM accesses, it is essential for the ECC check bits to be initialized after power on. See Section 15.5, 'Initialization/Application Information.'

All non-correctable  ECC  errors  cause  a  data  storage  interrupt  (IVOR2)  regardless  of  whether non-correctable reporting is enabled. A data storage interrupt handler can determine:

- - The destination asserted an error, the ESR[XTE] bit will be set.
- - The address where the error occurred, using the data exception address register (DEAR).

However, details of the ECC error are not reported unless non-correctable reporting is enabled by setting bits ERNCR and EFNCR in the ECSM\_ECR. When these bits are set and a non-correctable ECC error occurs, error information is recorded in other ECSM registers and an interrupt request is generated on vector 9 of the INTC. If properly enabled, this INTC vector 9 can cause an external interrupt (IVOR4) along with the data storage interrupt (IVOR2).

To avoid the external interrupt (IVOR4) being generated, the application enables non-correctable reporting in the ECSM, but does not enable that its interrupt be recognized. The INTC\_PSR[PRI] value for the ECC error interrupt request is left at its reset value of 0. The 0 priority level is the lowest priority and is never recognized, resulting in only the data storage interrupt (IVOR2) being taken.

## 8.4 Revision History

## Substantive Changes since Rev 3.0

Added Section 8.2.1.5, 'ECC Error Generation Register (ECSM\_EEGR) as well as updated memory map to show EEGR.

Error Correction Status Module (ECSM)
