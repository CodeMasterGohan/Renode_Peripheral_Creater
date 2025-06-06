### Chatper 10 Interrupt Controller (INTC)

## 10.1 Introduction

This chapter describes the interrupt controller (INTC), which schedules interrupt requests (IRQs) from software  and  internal  peripherals  to  the  e200z6  core.  The  INTC  provides  interrupt  prioritization  and preemption, interrupt masking, interrupt priority elevation, and protocol support.

Interrupts implemented by the MPC5553 and the MPC5554 are defined in the e200z6 PowerPC tm Core Reference Manual , Rev 0.

## 10.1.1 Block Diagram

Figure 4-1 shows details of the interrupt controller.

<!-- image -->

Figure 10-1. INTC Block Diagram

## 10.1.2 Overview

Interrupt functionality for the MPC5553/MPC5554 is handled between the e200z6 core and the interrupt controller. The CPU core has 19 exception sources, each of which can interrupt the core. One exception source is from the interrupt controller (INTC). The INTC provides priority-based preemptive scheduling of interrupt requests. This scheduling scheme is suitable for statically scheduled hard real-time systems. The INTC is optimized for a large number of interrupt requests. It is targeted to work with a PowerPC book E processor and automotive powertrain applications where the ISRs nest to multiple levels.

Figure 10-2 displays the interrupt sources for the MPC5553. Figure 10-3 displays the interrupt sources for the MPC5554. Refer to Table 10-9 for interrupt source vector details.

Figure 10-3. MPC5554 INTC Software Vector Mode

<!-- image -->

Two modes are available to determine the vector for the interrupt request source: software vector mode and hardware vector mode. In software vector mode, as shown in Figure 10-2, the e200z6 branches to a common interrupt exception handler whose location is determined by an address derived from special purpose registers IVPR and IVOR4. The interrupt exception handler reads the INTC\_IACKR to determine

the vector of the interrupt request source. Typical program flow for software vector mode is shown in Figure 10-4.

Figure 10-4. Program Flow - Software Vector Mode

<!-- image -->

In hardware vector mode, the e200z6 branches to a unique interrupt exception handler whose location is unique for each interrupt request source. Typical program flow for hardware vector mode is shown in Figure 10-5.

Figure 10-5. Program Flow - Hardware Vector Mode

<!-- image -->

For high priority interrupt requests in these target applications, the time from the assertion of the interrupt request from the peripheral to when the processor is performing useful work to service the interrupt request needs to be minimized. The INTC may be optimized to support this goal through the hardware vector mode, where a unique vector is provided for each interrupt request source. It also provides 16 priorities so that  lower  priority  ISRs  do  not  delay  the  execution  of  higher  priority  ISRs.  Since  each  individual application will have different priorities for each source of interrupt request, the priority of each interrupt request is configurable.

When multiple tasks share a resource, coherent accesses to that resource need to be supported. The INTC supports the priority ceiling protocol for coherent accesses. By providing a modifiable priority mask, the priority level can be raised temporarily so that no task can preempt another task that shares the same resource.

Multiple processors can assert interrupt requests to each other through software settable interrupt requests, i.e., by using application software to assert an interrupt request. These same software settable interrupt requests also can be used to break the work involved in servicing an interrupt request into a high priority portion and a low priority portion. The high priority portion is initiated by a peripheral interrupt request, but then the ISR can assert a software settable interrupt request to finish the servicing in a lower priority ISR.

## 10.1.3 Features

Features include the following:

- · Total number of interrupt vectors is 308 (MPC5554) or 212 (MPC5553) of which
- - 278 (MPC5554) or 191 (MPC5553) are peripheral interrupt request sources,
- - 8 are software settable sources, and
- - 22 (MPC5554) or 13 (MPC5553) are reserved sources.
- · 9-bit unique vector for each interrupt request source in hardware vector mode.
- · Each interrupt source can be programmed to one of 16 priorities.
- · Preemption.
- - Preemptive prioritized interrupt requests to processor.
- - ISR at a higher priority preempts ISRs or tasks at lower priorities.
- - Automatic pushing or popping of preempted priority to or from a LIFO.
- - Ability to modify the ISR or task priority. Modifying the priority can be used to implement the priority ceiling protocol for accessing shared resources.
- · Low latency - three clocks from receipt of interrupt request from peripheral to interrupt request to processor.

## 10.1.4 Modes of Operation

The  interrupt  controller  has  two  handshaking  modes  with  the  processor:  software  vector  mode  and hardware vector mode. The state of the hardware vector enable bit, INTC\_MCR[HVEN], determines which mode is used.

In debug mode the interrupt controller operation is identical to its normal operation of software vector mode or hardware vector mode.

## 10.1.4.1 Software Vector Mode

In software vector mode, there is a common interrupt exception handler address which is calculated by hardware as shown in Figure 10-6. The upper half of the interrupt vector prefix register (IVPR) is added to the offset contained in the external input interrupt vector offset register (IVOR4). Note that since bits IVOR4[28:31] are not part of the offset value, the vector offset must be located on a quad-word (16-byte) aligned location in memory.

In  software  vector  mode,  the  interrupt  exception  handler  software  must  read  the  INTC  interrupt acknowledge register (INTC\_IACKR) to obtain the vector associated with the corresponding peripheral or software interrupt request. The INTC\_ACKR contains a 32-bit address composed of a vector table base address (VTBA) plus an offset which is the interrupt vector (INTVEC). The address is then used to branch to the corresponding routine for that peripheral or software interrupt source.

Figure 10-6. Software Vector Mode: Interrupt Exception Handler Address Calculation

<!-- image -->

Reading the INTC\_IACKR acknowledges the INTC's interrupt request and negates the interrupt request to the processor. The interrupt request to the processor will not clear if a higher priority interrupt request arrives. Even in this case, INTVEC will not update to the higher priority request until the lower priority interrupt request is acknowledged by reading the INTC\_IACKR. The reading also pushes the PRI value in the INTC current priority register (INTC\_CPR) onto the LIFO and updates PRI in the INTC\_CPR with the priority of the interrupt request. The INTC\_CPR masks any peripheral or software settable interrupt request at the same or lower priority of the current value of the PRI field in INTC\_CPR from generating an interrupt request to the processor.

The  last  actions  of  the  interrupt  exception  handler  must  be  the  write  to  the  end-of-interrupt  register (INTC\_EOIR). Writing to the INTC\_EOIR signals the end of the servicing of the interrupt request. The INTC's LIFO is popped into the INTC\_CPR's PRI field by writing to the INTC\_EOIR, and the size of a write does not affect the operation of the write. Those values and sizes written to this register neither update the INTC\_EOIR contents nor affect whether the LIFO pops. For possible future compatibility, write four bytes of all 0s to the INTC\_EOIR. The timing relationship between popping the LIFO and disabling recognition of external input has no restriction. The writes can happen in either order.

However, disabling recognition of the external input before popping the LIFO eases the calculation of the maximum pipe depth at the cost of postponing the servicing of the next interrupt request.

## 10.1.4.2 Hardware Vector Mode

In hardware vector mode, the interrupt exception handler address is specific to the peripheral or software settable  interrupt  source  rather  than  being  common  to  all  of  them.  No  IVOR  is  used.  The  interrupt exception  handler  address  is  calculated  by  hardware  as  shown  in  Figure 10-7.  The  upper  half  of  the interrupt vector prefix register (IVPR) is added to an offset which corresponds to the peripheral or software interrupt source which caused the interrupt request. The offset matches the value in the Interrupt Vector field,  INTC\_IACKR[INTVEC].  Each  interrupt  exception  handler  address  is  aligned  on  a  quad  word (16-byte) boundary. IVOR4 is unused in this mode, and software does not need to read INTC\_IACKR to get the interrupt vector number.

Figure 10-7. Hardware Vector Mode: Interrupt Exception Handler Address Calculation

<!-- image -->

The processor negates INTC's interrupt request when automatically acknowledging the interrupt request. However, the interrupt request to the processor will not negate if a higher priority interrupt request arrives. Even in this case, the interrupt vector number will not update to the higher priority request until the lower priority request is acknowledged by the processor.

The assertion of the interrupt acknowledge signal pushes the PRI value in the INTC\_CPR onto the LIFO and updates PRI in the INTC\_CPR with the new priority.

## 10.2 External Signal Description

The INTC does not have any direct external MCU signals. However, there are sixteen external pins which can be configured in the SIU as external interrupt request input pins. When configured in this function, an interrupt on the pin sets a corresponding SIU external interrupt flag. These flags can cause one of five peripheral interrupt requests to the interrupt controller. See Table 10-1 for a list of the external interrupt pins. See the SIU chapter for more information on these pins.

Table 10-1. External Interrupt Signals

| Signal/Range Abbreviation 1   | Pin        | P/A/G 2   | Function 3                          | Description                                                 | I/O Type   | Reset Function/ State 4   | Post Reset Function/ State 5   |
|-------------------------------|------------|-----------|-------------------------------------|-------------------------------------------------------------|------------|---------------------------|--------------------------------|
| EMIOS[14:15]                  | AF19: AD18 | P A G     | EMIOS[14:15] IRQ[0:1] GPIO[193:194] | eMIOS channel (output only) External interrupt request GPIO | O I I/O    | -/ WKPCFG                 | -/ WKPCFG                      |
| BOOTCFG[0:1]                  | AA25: Y24  | P A G     | BOOTCFG[0:1] IRQ[2:3] GPIO[211:212] | Boot configuration input External interrupt request GPIO    | I I I/O    | BOOTCFG/ Down             | -/ Down                        |
| PLLCFG0                       | AB25:      | P A G     | PLLCFG0 IRQ4 GPIO208                | FMPLL mode selection External Interrupt Request GPIO        | I I I/O    | PLLCFG / Up               | -/ Up                          |

Table 10-1. External Interrupt Signals (continued)

| Signal/Range Abbreviation 1   | Pin    | P/A/G 2   | Function 3    | Description                  | I/O Type   | Reset Function/ State 4   | Post Reset Function/ State 5   |
|-------------------------------|--------|-----------|---------------|------------------------------|------------|---------------------------|--------------------------------|
| PLLCFG1                       | AA24   | P         | PLLCFG1       | FMPLL mode selection         | I          | PLLCFG /                  | -/ Up                          |
| PLLCFG1                       |        | A         | IRQ5          | External Interrupt Request   | I          | Up                        |                                |
| PLLCFG1                       |        | A2        | SOUTD         | DSPI D Data Output           | O          |                           |                                |
| PLLCFG1                       |        | G         | GPIO209       | GPIO                         | I/O        |                           |                                |
| TCRCLKB 6                     | M23    | P         | TCRCLKB       | eTPU B TCR clock             | I          | -/ Up                     | -/ Up                          |
| TCRCLKB 6                     |        | A         | IRQ6          | External Interrupt Request   | I          |                           |                                |
| TCRCLKB 6                     |        | G         | GPIO146       | GPIO                         | I/O        |                           |                                |
| TCRCLKA                       | N4     | P         | TCRCLKA       | eTPU A TCR clock             | I          | -/ Up                     | -/ Up                          |
| TCRCLKA                       |        | A         | IRQ7          | External interrupt request   | I          |                           |                                |
| TCRCLKA                       |        | G         | GPIO113       | GPIO                         | I/O        |                           |                                |
| ETPUA[20:23]                  | H1:G4  | P         | ETPUA[20:23]  | eTPU A channel               | I/O        | -/                        | -/                             |
| ETPUA[20:23]                  | G2:G1  | A         | IRQ[8:11]     | External interrupt request   | I          | WKPCFG                    | WKPCFG                         |
| ETPUA[20:23]                  |        | G         | GPIO[134:137] | GPIO                         | I/O        |                           |                                |
| ETPUA[24:26]                  | F1:G3: | P         | ETPUA[24:26]  | eTPU A channel (output only) | O          | -                         | -                              |
| ETPUA[24:26]                  | F3     | A         | IRQ[12:14]    | External interrupt request   | I          | /WKPCFG                   | /WKPCFG                        |
| ETPUA[24:26]                  |        | G         | GPIO[138:140] | GPIO                         | I/O        |                           |                                |
| ETPUA27                       | F2     | P         | ETPUA27       | eTPU A channel (output only) | O          | -                         | -                              |
| ETPUA27                       |        | A         | IRQ15         | External interrupt request   | I          | /WKPCFG                   | /WKPCFG                        |
| ETPUA27                       |        | G         | GPIO141       | GPIO                         | I/O        |                           |                                |

- 1 This is the name that appears on the PBGA pinout.
- 2 Primary, alternate, or GPIO function.
- 3 For each pin in the table, each line in the function column is a separate function of the pin. For all MPC5554/MPC5553 I/O pins the selection of primary, secondary or tertiary function is done in the MPC5554/MPC5553 SIU except where explicitly noted.
- 4 Terminology is O - output, I - input, Up - weak pull up enabled, Down - weak pull down enabled, Low - output driven low, High - output driven high.
- 5 Function after reset of GPI is general-purpose input.
- 6 This signal appears only in the MPC5554, it is not implemented in the MPC5553.

## 10.3 Memory Map/Register Definition

Table 10-2  is  the INTC  memory  map.  INTC\_BASE  for  the  MPC5553/MPC5554  is  located  at 0xFFF4\_8000.

## Table 10-2. INTC Memory Map

| Address            | Register Name   | Register Description               | Size (bits)   |
|--------------------|-----------------|------------------------------------|---------------|
| Base (0xFFF4_8000) | INTC_MCR        | INTC module configuration register | 32            |
| Base + 0x4         | -               | Reserved                           | -             |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 10-2. INTC Memory Map (continued)

| Address                                                       | Register Name   | Register Description                                                                                | Size (bits)   |
|---------------------------------------------------------------|-----------------|-----------------------------------------------------------------------------------------------------|---------------|
| Base + 0x8                                                    | INTC_CPR        | INTC current priority register                                                                      | 32            |
| Base + 0xC                                                    | -               | Reserved                                                                                            | -             |
| Base + 0x10                                                   | INTC_IACKR      | INTC interrupt acknowledge register 1                                                               | 32            |
| Base + 0x14                                                   | -               | Reserved                                                                                            | -             |
| Base + 0x18                                                   | INTC_EOIR       | INTC end-of-interrupt register                                                                      | 32            |
| Base + 0x1C                                                   | -               | Reserved                                                                                            | -             |
| Base + 0x20                                                   | INTC_SSCIR0     | INTC software set/clear interrupt register 0                                                        | 8             |
| Base + 0x21                                                   | INTC_SSCIR1     | INTC software set/clear interrupt register 1                                                        | 8             |
| Base + 0x22                                                   | INTC_SSCIR2     | INTC software set/clear interrupt register 2                                                        | 8             |
| Base + 0x23                                                   | INTC_SSCIR3     | INTC software set/clear interrupt register 3                                                        | 8             |
| Base + 0x24                                                   | INTC_SSCIR4     | INTC software set/clear interrupt register 4                                                        | 8             |
| Base + 0x25                                                   | INTC_SSCIR5     | INTC software set/clear interrupt register 5                                                        | 8             |
| Base + 0x26                                                   | INTC_SSCIR6     | INTC software set/clear interrupt register 6                                                        | 8             |
| Base + 0x27                                                   | INTC_SSCIR7     | INTC software set/clear interrupt register 7                                                        | 8             |
| Base + 0x28- Base + 0x3C                                      | -               | Reserved                                                                                            | -             |
| Base + 0x40- Base + 0x173 (MPC5554) or Base + 0x110 (MPC5553) | INTC_PSR n      | INTC priority select register 0 - 307 (MPC5554) 2 INTC priority select register 0 - 211 (MPC5553) 3 | 8             |

1 When the HVEN bit in the INTC\_MCR is asserted, a read of the INTC\_IACKR has no side effects.

2 In the MPC5554, the PRI fields are reserved for peripheral interrupt requests whose vectors are 147, 148, 150, 151, 154, 175, 194-201, 282 and 301-307.

3 In the MPC5553, the PRI fields are reserved for peripheral interrupt requests whose vectors are 147, 148, 150, 151, 154, 175, 197-201, 210, 211.

## 10.3.1 Register Descriptions

With the exception of the INTC\_SSCI n and INTC\_PSR  registers, all of the registers are 32 bits in width. n Any combination of accessing the 4 bytes of a register with a single access is supported, provided that the access does not cross a register boundary. These supported accesses include types and sizes of 8 bits, aligned 16 bits,  and aligned 32 bits.

Although INTC\_SSCI  and INTC\_PSR n n and 8 bits wide, they can be accessed with a single 16-bit or 32-bit access, provided that the access does not cross a 32-bit boundary.

In  software  vector  mode,  the  side  effects  of  a  read  of  the  INTC  interrupt  acknowledge  register (INTC\_IACKR) are the same regardless of the size of the read. In either software or hardware vector mode, the size of a write to the INTC end-of-interrupt register (INTC\_EOIR) does not affect the operation of the write.

## 10.3.1.1 INTC Module Configuration Register (INTC\_MCR)

The INTC\_MCR is used to configure options of the INTC.

Figure 10-8. INTC Module Configuration Register (INTC\_MCR)

|          | 0                  | 1                  | 2                  | 3                  | 4                  | 5                  | 6                  | 7                  | 8                  | 9                  | 10                 | 11                 | 12                 | 13                 | 14                 | 15                 |
|----------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|
| R        | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  |
| W        |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |
| Reset    | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  |
| Reg Addr | Base (0xFFF4_8000) | Base (0xFFF4_8000) | Base (0xFFF4_8000) | Base (0xFFF4_8000) | Base (0xFFF4_8000) | Base (0xFFF4_8000) | Base (0xFFF4_8000) | Base (0xFFF4_8000) | Base (0xFFF4_8000) | Base (0xFFF4_8000) | Base (0xFFF4_8000) | Base (0xFFF4_8000) | Base (0xFFF4_8000) | Base (0xFFF4_8000) | Base (0xFFF4_8000) | Base (0xFFF4_8000) |
|          | 16                 | 17                 | 18                 | 19                 | 20                 | 21                 | 22                 | 23                 | 24                 | 25                 | 26                 | 27                 | 28                 | 29                 | 30                 | 31                 |
| R        | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | VTES               | 0                  | 0                  | 0                  | 0                  | HVEN               |
| W        |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |
| Reset    | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  | 0                  |
| Reg Addr | Base (0xFFF4_8000) | Base (0xFFF4_8000) | Base (0xFFF4_8000) | Base (0xFFF4_8000) | Base (0xFFF4_8000) | Base (0xFFF4_8000) | Base (0xFFF4_8000) | Base (0xFFF4_8000) | Base (0xFFF4_8000) | Base (0xFFF4_8000) | Base (0xFFF4_8000) | Base (0xFFF4_8000) | Base (0xFFF4_8000) | Base (0xFFF4_8000) | Base (0xFFF4_8000) | Base (0xFFF4_8000) |

Table 10-3. INTC\_MCR Field Descriptions

| Bits   | Name   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
|--------|--------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-25   | -      | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 26     | VTES   | Vector table entry size. Controls the number of '0's to the right of INTVEC in Section 10.3.1.3, 'INTC Interrupt Acknowledge Register (INTC_IACKR). If the contents of INTC_IACKR are used as an address of an entry in a vector table as in software vector mode, then the number of rightmost '0's will determine the size of each vector table entry. VTES impacts software vector mode operation but also affects INTC_IACKR[INTVEC] position in both hardware vector mode and software vector mode. 0 4 bytes (Normal expected use) 1 8 bytes |
| 27-30  | -      | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 31     | HVEN   | Hardware vector enable. Controls whether the INTC is in hardware vector mode or software vector mode. Refer to Section 10.1.4, 'Modes of Operation', for the details of the handshaking with the processor in each mode. 0 Software vector mode 1 Hardware vector mode                                                                                                                                                                                                                                                                             |

## 10.3.1.2 INTC Current Priority Register (INTC\_CPR)

The INTC\_CPR masks any peripheral or software settable interrupt request set at the same or lower priority  as  the  current  value  of  the  INTC\_CPR[PRI] field  from  generating  an  interrupt  request  to  the processor.  When the INTC interrupt acknowledge register (INTC\_IACKR) is read in software vector mode or the interrupt acknowledge signal from the processor is asserted in hardware vector mode, the value of PRI is pushed onto the LIFO, and PRI is updated with the priority of the preempting interrupt request. When the INTC end-of-interrupt register (INTC\_EOIR) is written, the LIFO is popped into the INTC\_CPR's PRI field.

The masking priority can be raised or lowered by writing to the PRI field, supporting the PCP. Refer to Section 10.5.5, 'Priority Ceiling Protocol.'

## NOTE

On some eSys MCUs, a store to raise the PRI field which closely precedes an access to a shared resource can result in a non-coherent access to that resource  unless  an mbar or msync followed  by  an isync sequence  of instructions is executed  between  the  accesses.  An mbar or msync instruction is also necessary after accessing the resource but before lowering the PRI field. Refer to Section 10.5.5.2, 'Ensuring Coherency.'

Figure 10-9. INTC Current Priority Register (INTC\_CPR)

<!-- image -->

|          | 0          | 1          | 2          | 3          | 4          | 5          | 6          | 7          | 8          | 9          | 10         | 11         | 12         | 13         | 14         | 15         |
|----------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|
| R        | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          |
| W        |            |            |            |            |            |            |            |            |            |            |            |            |            |            |            |            |
| Reset    | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          |
| Reg Addr | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 |
|          | 16         | 17         | 18         | 19         | 20         | 21         | 22         | 23         | 24         | 25         | 26         | 27         | 28         | 29         | 30         | 31         |
| R        | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          |            | PRI        |            |            |
| W        |            |            |            |            |            |            |            |            |            |            |            |            |            |            |            |            |
| Reset    | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 1          | 1          | 1          | 1          |
| Reg Addr | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 | Base + 0x8 |

## Table 10-4. INTC\_CPR Field Descriptions

| Bits   | Name      | Description                                                                                                       |
|--------|-----------|-------------------------------------------------------------------------------------------------------------------|
| 0-27   | -         | Reserved.                                                                                                         |
| 28-31  | PRI [0:3] | Priority. PRI is the priority of the currently executing ISR according to the field values defined in Table 10-5. |

## Table 10-5. PRI Values

|   PRI | Meaning                        |
|-------|--------------------------------|
|  1111 | Priority 15 (highest priority) |
|  1110 | Priority 14                    |
|  1101 | Priority 13                    |
|  1100 | Priority 12                    |
|  1011 | Priority 11                    |
|  1010 | Priority 10                    |
|  1001 | Priority 9                     |
|  1000 | Priority 8                     |

## Table 10-5. PRI Values  (continued)

|   PRI | Meaning                      |
|-------|------------------------------|
|  0111 | Priority 7                   |
|  0110 | Priority 6                   |
|  0101 | Priority 5                   |
|  0100 | Priority 4                   |
|  0011 | Priority 3                   |
|  0010 | Priority 2                   |
|  0001 | Priority 1                   |
|  0000 | Priority 0 (lowest priority) |

## 10.3.1.3 INTC Interrupt Acknowledge Register (INTC\_IACKR)

The INTC\_IACKR provides a value that can be used to load the address of an ISR from a vector table. The vector table can be composed of addresses of the ISRs specific to their respective interrupt vectors.

Also, in software vector mode, the INTC\_IACKR has side effects from reads. The side effects are the same regardless of the size of the read. Reading the INTC\_IACKR does not have side effects in hardware vector mode.

## NOTE

The INTC\_IACKR must not be read speculatively while in software vector mode.  Therefore,  for  future  compatibility,  the  TLB  entry  covering  the INTC\_IACKR must be configured to be guarded.

In  software  vector  mode,  the  INTC\_IACKR must be read before setting MSR[EE].  No  synchronization  instruction  is  needed  after  reading  the INTC\_IACKR and before setting MSR[EE].

However, the time for the processor to recognize the assertion or negation of the external input to it is not defined by the book E architecture and can be greater than 0. Therefore, insert instructions between the reading of the INTC\_IACKR and the setting of MSR[EE] that will consume at least two processor clock cycles. This length of time will allow the negation of the interrupt request to propagate through the processor before MSR[EE] is set.

Figure 10-10. INTC Interrupt Acknowledge Register (INTC\_IACKR)

<!-- image -->

Table 10-6. INTC\_IACKR Field Descriptions

| Bits   | Name   | Description                                                                                                                                                                                                                                                                                                                                                                                                           |
|--------|--------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-20   | VTBA   | Vector table base address. Can be the base address of a vector table of addresses of ISRs. The VTBA only uses the leftmost 20 bits when the VTES bit in INTC_MCR is asserted.                                                                                                                                                                                                                                         |
| 21-29  | INTVEC | Interrupt vector. Vector of the peripheral or software settable interrupt request that caused the interrupt request to the processor. When the interrupt request to the processor asserts, the INTVEC is updated, whether the INTC is in software or hardware vector mode. Note: If INTC_MCR[VTES] = 1, then INTVEC field is shifted left one position to bits 20-28. VTBA is then shortened by one bit to bits 0-19. |
| 30-31  | -      | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                             |

## 10.3.1.4 INTC End-of-Interrupt Register (INTC\_EOIR)

Writing to the INTC\_EOIR signals the end of the servicing of the interrupt request. When the INTC\_EOIR is written, the priority last pushed on the LIFO is popped into INTC\_CPR. The values and size of data written to the INTC\_EOIR are ignored. Those values and sizes written to this register neither update the INTC\_EOIR contents or affect whether the LIFO pops. For possible future compatibility, write four bytes of all 0's to the INTC\_EOIR.

Reading the INTC\_EOIR has no effect on the LIFO.

Figure 10-11. INTC End-of-Interrupt Register (INTC\_EOIR)

<!-- image -->

|          | 0           | 1           | 2           | 3           | 4           | 5           | 6           | 7           | 8           | 9           | 10          | 11          | 12          | 13          | 14          | 15          |
|----------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|
| R        | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           |
| W        |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |
| Reset    | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           |
| Reg Addr | Base + 0x18 | Base + 0x18 | Base + 0x18 | Base + 0x18 | Base + 0x18 | Base + 0x18 | Base + 0x18 | Base + 0x18 | Base + 0x18 | Base + 0x18 | Base + 0x18 | Base + 0x18 | Base + 0x18 | Base + 0x18 | Base + 0x18 | Base + 0x18 |
|          | 16          | 17          | 18          | 19          | 20          | 21          | 22          | 23          | 24          | 25          | 26          | 27          | 28          | 29          | 30          | 31          |
| R        | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           |
| W        |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |
| Reset    | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           |
| Reg Addr | Base + 0x18 | Base + 0x18 | Base + 0x18 | Base + 0x18 | Base + 0x18 | Base + 0x18 | Base + 0x18 | Base + 0x18 | Base + 0x18 | Base + 0x18 | Base + 0x18 | Base + 0x18 | Base + 0x18 | Base + 0x18 | Base + 0x18 | Base + 0x18 |

## 10.3.1.5 INTC Software Set/Clear Interrupt Registers (INTC\_SSCIR0 - INTC\_SSCIR7)

The INTC\_SSCIR  support the setting or clearing of software settable interrupt requests. These registers n contain  eight  independent  sets  of  bits  to  set  and  clear  a  corresponding  flag  bit  by  software.  With  the exception of being set by software, this flag bit behaves the same as a flag bit set within a peripheral. This flag bit generates an interrupt request within the INTC just like a peripheral interrupt request. Writing a 1 to SET n will leave SET n unchanged at 0 but will set CLR n . Writing a 0 to SET n will have no effect. CLR n is the flag bit. Writing a 1 to CLR n will clear it. Writing a 0 to CLR n will have no effect. If a 1 is written to a pair SET n and CLR n bits at the same time, CLR n will be asserted, regardless of whether CLR n was asserted before the write.

Although INTC\_SSCI n is 8 bits wide, it can be accessed with a single 16-bit or 32-bit access, provided that the access does not cross a 32-bit boundary.

Figure 10-12. INTC Software Set/Clear Interrupt Register 0-7 (INTC\_SSCIR0-INTC\_SSCIR7)

<!-- image -->

Table 10-7. INTC\_SSCIR0-INTC\_SSCIR7 Field Descriptions

| Bits   | Name   | Description   |
|--------|--------|---------------|
| 0-5    | -      | Reserved.     |

## Table 10-7. INTC\_SSCIR0-INTC\_SSCIR7 Field Descriptions (continued)

|   Bits | Name   | Description                                                                                                                                                                                                                                                                                |
|--------|--------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|      6 | SET n  | Set flag bits. Writing a 1 will set the corresponding CLR n bit. Writing a 0 will have no effect. Each SET n always will be read as a 0.                                                                                                                                                   |
|      7 | CLR n  | Clear flag bits. CLR n is the flag bit. Writing a 1 to CLR n will clear it provided that a 1 is not written simultaneously to its corresponding SET n bit. Writing a 0 to CLR n will have no effect. 0 Interrupt request not pending within INTC. 1 Interrupt request pending within INTC. |

## 10.3.1.6 INTC Priority Select Registers (INTC\_PSR0 - INTC\_PSR307)

The INTC\_PSR  support the selection of an individual priority for each source of interrupt request. The n unique vector of each peripheral or software settable interrupt request determines which INTC\_PSR n is assigned to that interrupt request. The software settable interrupt requests 0-7 are assigned vectors 0-7, and their priorities  are  configured  in  INTC\_PSR0-INTC\_PSR7, respectively. The peripheral interrupt requests are assigned vectors 8-307 (MPC5554)/8-211 (MPC5553) and their priorities are configured in INTC\_PSR8 through INTC\_PSR307 (MPC5554) / INTC\_PSR8 through INTC\_PSR211 (MPC5553), respectively.

Although INTC\_PSR  is 8 bits wide, it can be accessed with a single 16-bit or 32-bit access, provided that n the access does not cross a 32-bit boundary.

## NOTE

The  PRI   field  of  an  INTC\_PSR   must  not  be  modified  while  its n n corresponding peripheral or software settable interrupt request is asserted.

Figure 10-13. INTC Priority Select Register (INTC\_PSR0-INTC\_PSR307)

<!-- image -->

Table 10-8. INTC\_PSR0-INTC\_PSR307 Field Descriptions

| Bits   | Name   | Description                                                                                                |
|--------|--------|------------------------------------------------------------------------------------------------------------|
| 0-3    | -      | Reserved.                                                                                                  |
| 4-7    | PRI n  | Priority select. Selects the priority for the interrupt requests. Refer to the field values in Table 10-5. |

## 10.4 Functional Description

## 10.4.1 Interrupt Request Sources

The INTC has two types of interrupt requests, peripheral and software settable. The assignments between the interrupt requests from the modules to the vectors for input to the e200z6 are shown in Table 10-9. The Offset column lists the IRQ specific offsets when using hardware vector mode. The Source column is written  in  C  language  syntax.  The  syntax  is  'module\_register[bit].'  Interrupt  requests  from  the  same module location or ORed together. The individual interrupt priorities are selected in INTC\_PSR n , where the specific select register is assigned according to the vector.

Table 10-9. INTC: Interrupt Request Sources

| Offset         | Vector         | Source 1 MPC5553              | Source 1 MPC5554              | Description                                                                                           |
|----------------|----------------|-------------------------------|-------------------------------|-------------------------------------------------------------------------------------------------------|
| Software       | Software       | Software                      | Software                      | Software                                                                                              |
| 0x0000         | 0              | INTC_SSCIR0[CLR0]             | INTC_SSCIR0[CLR0]             | INTC software settable Clear flag 0                                                                   |
| 0x0010         | 1              | INTC_SSCIR1[CLR1]             | INTC_SSCIR1[CLR1]             | INTC software settable Clear flag 1                                                                   |
| 0x0020         | 2              | INTC_SSCIR2[CLR2]             | INTC_SSCIR2[CLR2]             | INTC software settable Clear flag 2                                                                   |
| 0x0030         | 3              | INTC_SSCIR3[CLR3]             | INTC_SSCIR3[CLR3]             | INTC software settable Clear flag 3                                                                   |
| 0x0040         | 4              | INTC_SSCIR4[CLR4]             | INTC_SSCIR4[CLR4]             | INTC software settable Clear flag 4                                                                   |
| 0x0050         | 5              | INTC_SSCIR5[CLR5]             | INTC_SSCIR5[CLR5]             | INTC software settable Clear flag 5                                                                   |
| 0x0060         | 6              | INTC_SSCIR6[CLR6]             | INTC_SSCIR6[CLR6]             | INTC software settable Clear flag 6                                                                   |
| 0x0070         | 7              | INTC_SSCIR7[CLR7]             | INTC_SSCIR7[CLR7]             | INTC software settable Clear flag 7                                                                   |
| Watchdog / ECC | Watchdog / ECC | Watchdog / ECC                | Watchdog / ECC                | Watchdog / ECC                                                                                        |
| 0x0080         | 8              | ECSM_SWTIR[SWTIC]             | ECSM_SWTIR[SWTIC]             | ECSM Software Watchdog Interrupt flag                                                                 |
| 0x0090         | 9              | ECSM_ESR[RNCE] ECSM_ESR[FNCE] | ECSM_ESR[RNCE] ECSM_ESR[FNCE] | ECSM combined interrupt requests: Internal SRAM Non-Correctable Error and Flash Non-Correctable Error |
| eDMAC          | eDMAC          | eDMAC                         | eDMAC                         | eDMAC                                                                                                 |
| 0x00A0         | 10             | EDMA_ERL[ERR31:ERR0]          | EDMA_ERL[ERR31:ERR0]          | eDMA channel Error flags 31-0                                                                         |
| 0x00B0         | 11             | EDMA_IRQRL[INT00]             | EDMA_IRQRL[INT00]             | eDMA channel Interrupt 0                                                                              |
| 0x00C0         | 12             | EDMA_IRQRL[INT01]             | EDMA_IRQRL[INT01]             | eDMA channel Interrupt 1                                                                              |
| 0x00D0         | 13             | EDMA_IRQRL[INT02]             | EDMA_IRQRL[INT02]             | eDMA channel Interrupt 2                                                                              |
| 0x00E0         | 14             | EDMA_IRQRL[INT03]             | EDMA_IRQRL[INT03]             | eDMA channel Interrupt 3                                                                              |
| 0x00F0         | 15             | EDMA_IRQRL[INT04]             | EDMA_IRQRL[INT04]             | eDMA channel Interrupt 4                                                                              |
| 0x0100         | 16             | EDMA_IRQRL[INT05]             | EDMA_IRQRL[INT05]             | eDMA channel Interrupt 5                                                                              |
| 0x0110         | 17             | EDMA_IRQRL[INT06]             | EDMA_IRQRL[INT06]             | eDMA channel Interrupt 6                                                                              |
| 0x0120         | 18             | EDMA_IRQRL[INT07]             | EDMA_IRQRL[INT07]             | eDMA channel Interrupt 7                                                                              |
| 0x0130         | 19             | EDMA_IRQRL[INT08]             | EDMA_IRQRL[INT08]             | eDMA channel Interrupt 8                                                                              |

## Functional Description

Table 10-9. INTC: Interrupt Request Sources (continued)

| Offset   | Vector   | Source 1 MPC5553    | Source 1 MPC5554    | Description                                                                     |
|----------|----------|---------------------|---------------------|---------------------------------------------------------------------------------|
| 0x0140   | 20       | EDMA_IRQRL[INT09]   | EDMA_IRQRL[INT09]   | eDMA channel Interrupt 9                                                        |
| 0x0150   | 21       | EDMA_IRQRL[INT10]   | EDMA_IRQRL[INT10]   | eDMA channel Interrupt 10                                                       |
| 0x0160   | 22       | EDMA_IRQRL[INT11]   | EDMA_IRQRL[INT11]   | eDMA channel Interrupt 11                                                       |
| 0x0170   | 23       | EDMA_IRQRL[INT12]   | EDMA_IRQRL[INT12]   | eDMA channel Interrupt 12                                                       |
| 0x0180   | 24       | EDMA_IRQRL[INT13]   | EDMA_IRQRL[INT13]   | eDMA channel Interrupt 13                                                       |
| 0x0190   | 25       | EDMA_IRQRL[INT14]   | EDMA_IRQRL[INT14]   | eDMA channel Interrupt 14                                                       |
| 0x01A0   | 26       | EDMA_IRQRL[INT15]   | EDMA_IRQRL[INT15]   | eDMA channel Interrupt 15                                                       |
| 0x01B0   | 27       | EDMA_IRQRL[INT16]   | EDMA_IRQRL[INT16]   | eDMA channel Interrupt 16                                                       |
| 0x01C0   | 28       | EDMA_IRQRL[INT17]   | EDMA_IRQRL[INT17]   | eDMA channel Interrupt 17                                                       |
| 0x01D0   | 29       | EDMA_IRQRL[INT18]   | EDMA_IRQRL[INT18]   | eDMA channel Interrupt 18                                                       |
| 0x01E0   | 30       | EDMA_IRQRL[INT19]   | EDMA_IRQRL[INT19]   | eDMA channel Interrupt 19                                                       |
| 0x01F0   | 31       | EDMA_IRQRL[INT20]   | EDMA_IRQRL[INT20]   | eDMA channel Interrupt 20                                                       |
| 0x0200   | 32       | EDMA_IRQRL[INT21]   | EDMA_IRQRL[INT21]   | eDMA channel Interrupt 21                                                       |
| 0x0210   | 33       | EDMA_IRQRL[INT22]   | EDMA_IRQRL[INT22]   | eDMA channel Interrupt 22                                                       |
| 0x0220   | 34       | EDMA_IRQRL[INT23]   | EDMA_IRQRL[INT23]   | eDMA channel Interrupt 23                                                       |
| 0x0230   | 35       | EDMA_IRQRL[INT24]   | EDMA_IRQRL[INT24]   | eDMA channel Interrupt 24                                                       |
| 0x0240   | 36       | EDMA_IRQRL[INT25]   | EDMA_IRQRL[INT25]   | eDMA channel Interrupt 25                                                       |
| 0x0250   | 37       | EDMA_IRQRL[INT26]   | EDMA_IRQRL[INT26]   | eDMA channel Interrupt 26                                                       |
| 0x0260   | 38       | EDMA_IRQRL[INT27]   | EDMA_IRQRL[INT27]   | eDMA channel Interrupt 27                                                       |
| 0x0270   | 39       | EDMA_IRQRL[INT28]   | EDMA_IRQRL[INT28]   | eDMA channel Interrupt 28                                                       |
| 0x0280   | 40       | EDMA_IRQRL[INT29]   | EDMA_IRQRL[INT29]   | eDMA channel Interrupt 29                                                       |
| 0x0290   | 41       | EDMA_IRQRL[INT30]   | EDMA_IRQRL[INT30]   | eDMA channel Interrupt 30                                                       |
| 0x02A0   | 42       | EDMA_IRQRL[INT31]   | EDMA_IRQRL[INT31]   | eDMA channel Interrupt 31                                                       |
| PLL      | PLL      | PLL                 | PLL                 | PLL                                                                             |
| 0x02B0   | 43       | FMPLL_SYNSR[LOCF]   | FMPLL_SYNSR[LOCF]   | FMPLL Loss of Clock Flag                                                        |
| 0x02C0   | 44       | FMPLL_SYNSR[LOLF]   | FMPLL_SYNSR[LOLF]   | FMPLL Loss of Lock Flag                                                         |
| SIU      | SIU      | SIU                 | SIU                 | SIU                                                                             |
| 0x02D0   | 45       | SIU_OSR[OVF15:OVF0] | SIU_OSR[OVF15:OVF0] | SIU combined overrun interrupt requests of the external interrupt Overrun Flags |
| 0x02E0   | 46       | SIU_EIISR[EIF0]     | SIU_EIISR[EIF0]     | SIU External Interrupt Flag 0                                                   |
| 0x02F0   | 47       | SIU_EIISR[EIF1]     | SIU_EIISR[EIF1]     | SIU External Interrupt Flag 1                                                   |
| 0x0300   | 48       | SIU_EIISR[EIF2]     | SIU_EIISR[EIF2]     | SIU External Interrupt Flag 2                                                   |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 10-9. INTC: Interrupt Request Sources (continued)

| Offset   | Vector   | Source 1 MPC5553                                                              | Source 1 MPC5554                                                              | Description                              |
|----------|----------|-------------------------------------------------------------------------------|-------------------------------------------------------------------------------|------------------------------------------|
| 0x0310   | 49       | SIU_EIISR[EIF3]                                                               | SIU_EIISR[EIF3]                                                               | SIU External Interrupt Flag 3            |
| 0x0320   | 50       | SIU_EIISR[EIF15:EIF4]                                                         | SIU_EIISR[EIF15:EIF4]                                                         | SIU External Interrupt Flags 15-4        |
| eMIOS    | eMIOS    | eMIOS                                                                         | eMIOS                                                                         | eMIOS                                    |
| 0x0330   | 51       | EMIOS_GFR[F0]                                                                 | EMIOS_GFR[F0]                                                                 | eMIOS channel 0 Flag                     |
| 0x0340   | 52       | EMIOS_GFR[F1]                                                                 | EMIOS_GFR[F1]                                                                 | eMIOS channel 1 Flag                     |
| 0x0350   | 53       | EMIOS_GFR[F2]                                                                 | EMIOS_GFR[F2]                                                                 | eMIOS channel 2 Flag                     |
| 0x0360   | 54       | EMIOS_GFR[F3]                                                                 | EMIOS_GFR[F3]                                                                 | eMIOS channel 3 Flag                     |
| 0x0370   | 55       | EMIOS_GFR[F4]                                                                 | EMIOS_GFR[F4]                                                                 | eMIOS channel 4 Flag                     |
| 0x0380   | 56       | EMIOS_GFR[F5]                                                                 | EMIOS_GFR[F5]                                                                 | eMIOS channel 5 Flag                     |
| 0x0390   | 57       | EMIOS_GFR[F6]                                                                 | EMIOS_GFR[F6]                                                                 | eMIOS channel 6 Flag                     |
| 0x03A0   | 58       | EMIOS_GFR[F7]                                                                 | EMIOS_GFR[F7]                                                                 | eMIOS channel 7 Flag                     |
| 0x03B0   | 59       | EMIOS_GFR[F8]                                                                 | EMIOS_GFR[F8]                                                                 | eMIOS channel 8 Flag                     |
| 0x03C0   | 60       | EMIOS_GFR[F9]                                                                 | EMIOS_GFR[F9]                                                                 | eMIOS channel 9 Flag                     |
| 0x03D0   | 61       | EMIOS_GFR[F10]                                                                | EMIOS_GFR[F10]                                                                | eMIOS channel 10 Flag                    |
| 0x03E0   | 62       | EMIOS_GFR[F11]                                                                | EMIOS_GFR[F11]                                                                | eMIOS channel 11 Flag                    |
| 0x03F0   | 63       | EMIOS_GFR[F12]                                                                | EMIOS_GFR[F12]                                                                | eMIOS channel 12 Flag                    |
| 0x0400   | 64       | EMIOS_GFR[F13]                                                                | EMIOS_GFR[F13]                                                                | eMIOS channel 13 Flag                    |
| 0x0410   | 65       | EMIOS_GFR[F14]                                                                | EMIOS_GFR[F14]                                                                | eMIOS channel 14 Flag                    |
| 0x0420   | 66       | EMIOS_GFR[F15]                                                                | EMIOS_GFR[F15]                                                                | eMIOS channel 15 Flag                    |
| eTPU_A   | eTPU_A   | eTPU_A                                                                        | eTPU_A                                                                        | eTPU_A                                   |
| 0x0430   | 67       | ETPU_MCR[MGEA] ETPU_MCR[MGEB] ETPU_MCR[ILFA] ETPU_MCR[ILFB] ETPU_MCR[SCMMISF] | ETPU_MCR[MGEA] ETPU_MCR[MGEB] ETPU_MCR[ILFA] ETPU_MCR[ILFB] ETPU_MCR[SCMMISF] | eTPU Global Exception                    |
| 0x0440   | 68       | ETPU_CISR_A[CIS0]                                                             | ETPU_CISR_A[CIS0]                                                             | eTPU Engine A Channel 0 Interrupt Status |
| 0x0450   | 69       | ETPU_CISR_A[CIS1]                                                             | ETPU_CISR_A[CIS1]                                                             | eTPU Engine A Channel 1 Interrupt Status |
| 0x0460   | 70       | ETPU_CISR_A[CIS2]                                                             | ETPU_CISR_A[CIS2]                                                             | eTPU Engine A Channel 2 Interrupt Status |
| 0x0470   | 71       | ETPU_CISR_A[CIS3]                                                             | ETPU_CISR_A[CIS3]                                                             | eTPU Engine A Channel 3 Interrupt Status |
| 0x0480   | 72       | ETPU_CISR_A[CIS4]                                                             | ETPU_CISR_A[CIS4]                                                             | eTPU Engine A Channel 4 Interrupt Status |
| 0x0490   | 73       | ETPU_CISR_A[CIS5]                                                             | ETPU_CISR_A[CIS5]                                                             | eTPU Engine A Channel 5 Interrupt Status |
| 0x04A0   | 74       | ETPU_CISR_A[CIS6]                                                             | ETPU_CISR_A[CIS6]                                                             | eTPU Engine A Channel 6 Interrupt Status |
| 0x04B0   | 75       | ETPU_CISR_A[CIS7]                                                             | ETPU_CISR_A[CIS7]                                                             | eTPU Engine A Channel 7 Interrupt Status |
| 0x04C0   | 76       | ETPU_CISR_A[CIS8]                                                             | ETPU_CISR_A[CIS8]                                                             | eTPU Engine A Channel 8 Interrupt Status |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## Functional Description

Table 10-9. INTC: Interrupt Request Sources (continued)

| Offset   | Vector   | Source 1 MPC5553                                            | Source 1 MPC5554                                            | Description                                                                                                                      |
|----------|----------|-------------------------------------------------------------|-------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------|
| 0x04D0   | 77       | ETPU_CISR_A[CIS9]                                           | ETPU_CISR_A[CIS9]                                           | eTPU Engine A Channel 9 Interrupt Status                                                                                         |
| 0x04E0   | 78       | ETPU_CISR_A[CIS10]                                          | ETPU_CISR_A[CIS10]                                          | eTPU Engine A Channel 10 Interrupt Status                                                                                        |
| 0x04F0   | 79       | ETPU_CISR_A[CIS11]                                          | ETPU_CISR_A[CIS11]                                          | eTPU Engine A Channel 11 Interrupt Status                                                                                        |
| 0x0500   | 80       | ETPU_CISR_A[CIS12]                                          | ETPU_CISR_A[CIS12]                                          | eTPU Engine A Channel 12 Interrupt Status                                                                                        |
| 0x0510   | 81       | ETPU_CISR_A[CIS13]                                          | ETPU_CISR_A[CIS13]                                          | eTPU Engine A Channel 13 Interrupt Status                                                                                        |
| 0x0520   | 82       | ETPU_CISR_A[CIS14]                                          | ETPU_CISR_A[CIS14]                                          | eTPU Engine A Channel 14 Interrupt Status                                                                                        |
| 0x0530   | 83       | ETPU_CISR_A[CIS15]                                          | ETPU_CISR_A[CIS15]                                          | eTPU Engine A Channel 15 Interrupt Status                                                                                        |
| 0x0540   | 84       | ETPU_CISR_A[CIS16]                                          | ETPU_CISR_A[CIS16]                                          | eTPU Engine A Channel 16 Interrupt Status                                                                                        |
| 0x0550   | 85       | ETPU_CISR_A[CIS17]                                          | ETPU_CISR_A[CIS17]                                          | eTPU Engine A Channel 17 Interrupt Status                                                                                        |
| 0x0560   | 86       | ETPU_CISR_A[CIS18]                                          | ETPU_CISR_A[CIS18]                                          | eTPU Engine A Channel 18 Interrupt Status                                                                                        |
| 0x0570   | 87       | ETPU_CISR_A[CIS19]                                          | ETPU_CISR_A[CIS19]                                          | eTPU Engine A Channel 19 Interrupt Status                                                                                        |
| 0x0580   | 88       | ETPU_CISR_A[CIS20]                                          | ETPU_CISR_A[CIS20]                                          | eTPU Engine A Channel 20 Interrupt Status                                                                                        |
| 0x0590   | 89       | ETPU_CISR_A[CIS21]                                          | ETPU_CISR_A[CIS21]                                          | eTPU Engine A Channel 21 Interrupt Status                                                                                        |
| 0x05A0   | 90       | ETPU_CISR_A[CIS22]                                          | ETPU_CISR_A[CIS22]                                          | eTPU Engine A Channel 22 Interrupt Status                                                                                        |
| 0x05B0   | 91       | ETPU_CISR_A[CIS23]                                          | ETPU_CISR_A[CIS23]                                          | eTPU Engine A Channel 23 Interrupt Status                                                                                        |
| 0x05C0   | 92       | ETPU_CISR_A[CIS24]                                          | ETPU_CISR_A[CIS24]                                          | eTPU Engine A Channel 24 Interrupt Status                                                                                        |
| 0x05D0   | 93       | ETPU_CISR_A[CIS25]                                          | ETPU_CISR_A[CIS25]                                          | eTPU Engine A Channel 25 Interrupt Status                                                                                        |
| 0x05E0   | 94       | ETPU_CISR_A[CIS26]                                          | ETPU_CISR_A[CIS26]                                          | eTPU Engine A Channel 26 Interrupt Status                                                                                        |
| 0x05F0   | 95       | ETPU_CISR_A[CIS27]                                          | ETPU_CISR_A[CIS27]                                          | eTPU Engine A Channel 27 Interrupt Status                                                                                        |
| 0x0600   | 96       | ETPU_CISR_A[CIS28]                                          | ETPU_CISR_A[CIS28]                                          | eTPU Engine A Channel 28 Interrupt Status                                                                                        |
| 0x0610   | 97       | ETPU_CISR_A[CIS29]                                          | ETPU_CISR_A[CIS29]                                          | eTPU Engine A Channel 29 Interrupt Status                                                                                        |
| 0x0620   | 98       | ETPU_CISR_A[CIS30]                                          | ETPU_CISR_A[CIS30]                                          | eTPU Engine A Channel 30 Interrupt Status                                                                                        |
| 0x0630   | 99       | ETPU_CISR_A[CIS31]                                          | ETPU_CISR_A[CIS31]                                          | eTPU Engine A Channel 31 Interrupt Status                                                                                        |
| eQADC    | eQADC    | eQADC                                                       | eQADC                                                       | eQADC                                                                                                                            |
| 0x0640   | 100      | EQADC_FISR x [TORF] EQADC_FISR x [RFOF] EQADC_FISR x [CFUF] | EQADC_FISR x [TORF] EQADC_FISR x [RFOF] EQADC_FISR x [CFUF] | eQADCcombinedoverruninterruptrequest s from all of the FIFOs: Trigger Overrun, Receive FIFO Overflow, and command FIFO Underflow |
| 0x0650   | 101      | EQADC_FISR0[NCF]                                            | EQADC_FISR0[NCF]                                            | eQADC command FIFO 0 Non-Coherency Flag                                                                                          |
| 0x0660   | 102      | EQADC_FISR0[PF]                                             | EQADC_FISR0[PF]                                             | eQADC command FIFO 0 Pause Flag                                                                                                  |
| 0x0670   | 103      | EQADC_FISR0[EOQF]                                           | EQADC_FISR0[EOQF]                                           | eQADCcommandFIFO0commandqueueEndof Queue Flag                                                                                    |
| 0x0680   | 104      | EQADC_FISR0[CFFF]                                           | EQADC_FISR0[CFFF]                                           | eQADC Command FIFO 0 Fill Flag                                                                                                   |
| 0x0690   | 105      | EQADC_FISR0[RFDF]                                           | EQADC_FISR0[RFDF]                                           | eQADC Receive FIFO 0 Drain Flag                                                                                                  |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## Table 10-9. INTC: Interrupt Request Sources (continued)

| Offset   | Vector   | Source 1 MPC5553              | Source 1 MPC5554              | Description                                                                                   |
|----------|----------|-------------------------------|-------------------------------|-----------------------------------------------------------------------------------------------|
| 0x06A0   | 106      | EQADC_FISR1[NCF]              | EQADC_FISR1[NCF]              | eQADC command FIFO 1 Non-Coherency Flag                                                       |
| 0x06B0   | 107      | EQADC_FISR1[PF]               | EQADC_FISR1[PF]               | eQADC command FIFO 1 Pause Flag                                                               |
| 0x06C0   | 108      | EQADC_FISR1[EOQF]             | EQADC_FISR1[EOQF]             | eQADCcommandFIFO1commandqueueEndof Queue Flag                                                 |
| 0x06D0   | 109      | EQADC_FISR1[CFFF]             | EQADC_FISR1[CFFF]             | eQADC Command FIFO 1 Fill Flag                                                                |
| 0x06E0   | 110      | EQADC_FISR1[RFDF]             | EQADC_FISR1[RFDF]             | eQADC Receive FIFO 1 Drain Flag                                                               |
| 0x06F0   | 111      | EQADC_FISR2[NCF]              | EQADC_FISR2[NCF]              | eQADC command FIFO 2 Non-Coherency Flag                                                       |
| 0x0700   | 112      | EQADC_FISR2[PF]               | EQADC_FISR2[PF]               | eQADC command FIFO 2 Pause Flag                                                               |
| 0x0710   | 113      | EQADC_FISR2[EOQF]             | EQADC_FISR2[EOQF]             | eQADCcommandFIFO2commandqueueEndof Queue Flag                                                 |
| 0x0720   | 114      | EQADC_FISR2[CFFF]             | EQADC_FISR2[CFFF]             | eQADC Command FIFO 2 Fill Flag                                                                |
| 0x0730   | 115      | EQADC_FISR2[RFDF]             | EQADC_FISR2[RFDF]             | eQADC Receive FIFO 2 Drain Flag                                                               |
| 0x0740   | 116      | EQADC_FISR3[NCF]              | EQADC_FISR3[NCF]              | eQADC command FIFO 3 Non-Coherency Flag                                                       |
| 0x0750   | 117      | EQADC_FISR3[PF]               | EQADC_FISR3[PF]               | eQADC command FIFO 3 Pause Flag                                                               |
| 0x0760   | 118      | EQADC_FISR3[EOQF]             | EQADC_FISR3[EOQF]             | eQADCcommandFIFO3commandqueueEndof Queue Flag                                                 |
| 0x0770   | 119      | EQADC_FISR3[CFFF]             | EQADC_FISR3[CFFF]             | eQADC Command FIFO 3 Fill Flag                                                                |
| 0x0780   | 120      | EQADC_FISR3[RFDF]             | EQADC_FISR3[RFDF]             | eQADC Receive FIFO 3 Drain Flag                                                               |
| 0x0790   | 121      | EQADC_FISR4[NCF]              | EQADC_FISR4[NCF]              | eQADC command FIFO 4 Non-Coherency Flag                                                       |
| 0x07A0   | 122      | EQADC_FISR4[PF]               | EQADC_FISR4[PF]               | eQADC command FIFO 4 Pause Flag                                                               |
| 0x07B0   | 123      | EQADC_FISR4[EOQF]             | EQADC_FISR4[EOQF]             | eQADCcommandFIFO4commandqueueEndof Queue Flag                                                 |
| 0x07C0   | 124      | EQADC_FISR4[CFFF]             | EQADC_FISR4[CFFF]             | eQADC Command FIFO 4 Fill Flag                                                                |
| 0x07D0   | 125      | EQADC_FISR4[RFDF]             | EQADC_FISR4[RFDF]             | eQADC Receive FIFO 4 Drain Flag                                                               |
| 0x07E0   | 126      | EQADC_FISR5[NCF]              | EQADC_FISR5[NCF]              | eQADC command FIFO 5 Non-Coherency Flag                                                       |
| 0x07F0   | 127      | EQADC_FISR5[PF]               | EQADC_FISR5[PF]               | eQADC command FIFO 5 Pause Flag                                                               |
| 0x0800   | 128      | EQADC_FISR5[EOQF]             | EQADC_FISR5[EOQF]             | eQADCcommandFIFO5commandqueueEndof Queue Flag                                                 |
| 0x0810   | 129      | EQADC_FISR5[CFFF]             | EQADC_FISR5[CFFF]             | eQADC Command FIFO 5 Fill Flag                                                                |
| 0x0820   | 130      | EQADC_FISR5[RFDF]             | EQADC_FISR5[RFDF]             | eQADC Receive FIFO 5 Drain Flag                                                               |
| DSPI     | DSPI     | DSPI                          | DSPI                          | DSPI                                                                                          |
| 0x0830   | 131      | DSPI_BSR[TFUF] DSPI_BSR[RFOF] | DSPI_BSR[TFUF] DSPI_BSR[RFOF] | DSPI_B combined overrun interrupt requests: Transmit FIFO Underflow and Receive FIFO Overflow |
| 0x0840   | 132      | DSPI_BSR[EOQF]                | DSPI_BSR[EOQF]                | DSPI_B transmit FIFO End of Queue Flag                                                        |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## Table 10-9. INTC: Interrupt Request Sources (continued)

| Offset   |   Vector | Source 1 MPC5553                                                                                                                                                                                                                                                       | Source 1 MPC5554                                                                                                                                                                                                                                                       | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|----------|----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0x0850   |      133 | DSPI_BSR[TFFF]                                                                                                                                                                                                                                                         | DSPI_BSR[TFFF]                                                                                                                                                                                                                                                         | DSPI_B Transmit FIFO Fill Flag                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| 0x0860   |      134 | DSPI_BSR[TCF]                                                                                                                                                                                                                                                          | DSPI_BSR[TCF]                                                                                                                                                                                                                                                          | DSPI_B Transfer Complete Flag                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| 0x0870   |      135 | DSPI_BSR[RFDF]                                                                                                                                                                                                                                                         | DSPI_BSR[RFDF]                                                                                                                                                                                                                                                         | DSPI_B Receive FIFO Drain Flag                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| 0x0880   |      136 | DSPI_CSR[TFUF] DSPI_CSR[RFOF]                                                                                                                                                                                                                                          | DSPI_CSR[TFUF] DSPI_CSR[RFOF]                                                                                                                                                                                                                                          | DSPI_C combined overrun interrupt requests: Transmit FIFO Underflow and Receive FIFO Overflow                                                                                                                                                                                                                                                                                                                                                                                                                                |
| 0x0890   |      137 | DSPI_CSR[EOQF]                                                                                                                                                                                                                                                         | DSPI_CSR[EOQF]                                                                                                                                                                                                                                                         | DSPI_C transmit FIFO End of Queue Flag                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| 0x08A0   |      138 | DSPI_CSR[TFFF]                                                                                                                                                                                                                                                         | DSPI_CSR[TFFF]                                                                                                                                                                                                                                                         | DSPI_C Transmit FIFO Fill Flag                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| 0x08B0   |      139 | DSPI_CSR[TCF]                                                                                                                                                                                                                                                          | DSPI_CSR[TCF]                                                                                                                                                                                                                                                          | DSPI_C Transfer Complete Flag                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| 0x08C0   |      140 | DSPI_CSR[RFDF]                                                                                                                                                                                                                                                         | DSPI_CSR[RFDF]                                                                                                                                                                                                                                                         | DSPI_C Receive FIFO Drain Flag                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| 0x08D0   |      141 | DSPI_DSR[TFUF] DSPI_DSR[RFOF]                                                                                                                                                                                                                                          | DSPI_DSR[TFUF] DSPI_DSR[RFOF]                                                                                                                                                                                                                                          | DSPI_D combined overrun interrupt requests: Transmit FIFO Underflow and Receive FIFO Overflow                                                                                                                                                                                                                                                                                                                                                                                                                                |
| 0x08E0   |      142 | DSPI_DSR[EOQF]                                                                                                                                                                                                                                                         | DSPI_DSR[EOQF]                                                                                                                                                                                                                                                         | DSPI_D transmit FIFO End of Queue Flag                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| 0x08F0   |      143 | DSPI_DSR[TFFF]                                                                                                                                                                                                                                                         | DSPI_DSR[TFFF]                                                                                                                                                                                                                                                         | DSPI_D Transmit FIFO Fill Flag                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| 0x0900   |      144 | DSPI_DSR[TCF]                                                                                                                                                                                                                                                          | DSPI_DSR[TCF]                                                                                                                                                                                                                                                          | DSPI_D Transfer Complete Flag                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| 0x0910   |      145 | DSPI_DSR[RFDF]                                                                                                                                                                                                                                                         | DSPI_DSR[RFDF]                                                                                                                                                                                                                                                         | DSPI_D Receive FIFO Drain Flag                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| 0x0920   |      146 | ESCIA_SR[TDRE] ESCIA_SR[TC] ESCIA_SR[RDRF] ESCIA_SR[IDLE] ESCIA_SR[OR] ESCIA_SR[NF] ESCIA_SR[FE] ESCIA_SR[PF] ESCIA_SR[BERR] ESCIA_SR[RXRDY] ESCIA_SR[TXRDY] ESCIA_SR[LWAKE] ESCIA_SR[STO] ESCIA_SR[PBERR] ESCIA_SR[CERR] ESCIA_SR[CKERR] ESCIA_SR[FRC] ESCIA_SR[OVFL] | ESCIA_SR[TDRE] ESCIA_SR[TC] ESCIA_SR[RDRF] ESCIA_SR[IDLE] ESCIA_SR[OR] ESCIA_SR[NF] ESCIA_SR[FE] ESCIA_SR[PF] ESCIA_SR[BERR] ESCIA_SR[RXRDY] ESCIA_SR[TXRDY] ESCIA_SR[LWAKE] ESCIA_SR[STO] ESCIA_SR[PBERR] ESCIA_SR[CERR] ESCIA_SR[CKERR] ESCIA_SR[FRC] ESCIA_SR[OVFL] | Combined Interrupt Requests of ESCI Module A: Transmit Data Register Empty, Transmit Complete, Receive Data Register Full, Idle line, Overrun, Noise Flag, Framing Error Flag, and Parity Error Flag interrupt requests, SCI Status Register 2 Bit Error interrupt request, LIN Status Register 1 Receive Data Ready, Transmit Data Ready, Received LIN Wakeup Signal, Slave TimeOut, Physical Bus Error, CRC Error, Checksum Error, Frame Complete interrupts requests, and LIN Status Register 2 Receive Register Overflow |
| 0x0930   |      147 | Reserved                                                                                                                                                                                                                                                               | Reserved                                                                                                                                                                                                                                                               | Reserved                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| 0x0940   |      148 | Reserved                                                                                                                                                                                                                                                               | Reserved                                                                                                                                                                                                                                                               | Reserved                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 10-9. INTC: Interrupt Request Sources (continued)

| Offset                  | Vector                  | Source 1 MPC5553                                                                                                                                                                                                                                        | Source 1 MPC5554                                                                                                                                                                                                                                        | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|-------------------------|-------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0x0950                  | 149                     | ESCIB_SR[TDRE] ESCIB_SR[TC] ESCIB_SR[RDRF] ESCIB_SR[IDLE] ESCIB_SR[OR] ESCIB_SR[NF] ESCIB_SR[FE] ESCIB_SR[PF] ESCIB_SR[BERR] ESCIB_SR[RXRDY] ESCIB_SR[TXRDY] ESCIB_SR[LWAKE] ESCIB_SR[STO] ESCIB_SR[PBERR] ESCIB_SR[CERR] ESCIB_SR[CKERR] ESCIB_SR[FRC] | ESCIB_SR[TDRE] ESCIB_SR[TC] ESCIB_SR[RDRF] ESCIB_SR[IDLE] ESCIB_SR[OR] ESCIB_SR[NF] ESCIB_SR[FE] ESCIB_SR[PF] ESCIB_SR[BERR] ESCIB_SR[RXRDY] ESCIB_SR[TXRDY] ESCIB_SR[LWAKE] ESCIB_SR[STO] ESCIB_SR[PBERR] ESCIB_SR[CERR] ESCIB_SR[CKERR] ESCIB_SR[FRC] | Combined Interrupt Requests of ESCI Module B: Transmit Data Register Empty, Transmit Complete, Receive Data Register Full, Idle line, Overrun, Noise Flag, Framing Error Flag, and Parity Error Flag interrupt requests, SCI Status Register 2 Bit Error interrupt request, LIN Status Register 1 Receive Data Ready, Transmit Data Ready, Received LIN Wakeup Signal, Slave TimeOut, Physical Bus Error, CRC Error, Checksum Error, Frame Complete interrupts requests, and LIN Status Register 2 Receive Register Overflow |
| 0x0960                  | 150                     | Reserved                                                                                                                                                                                                                                                | Reserved                                                                                                                                                                                                                                                | Reserved                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| 0x0970                  | 151                     | Reserved                                                                                                                                                                                                                                                | Reserved                                                                                                                                                                                                                                                | Reserved                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| FlexCAN_A and FlexCAN_B | FlexCAN_A and FlexCAN_B | FlexCAN_A and FlexCAN_B                                                                                                                                                                                                                                 | FlexCAN_A and FlexCAN_B                                                                                                                                                                                                                                 | FlexCAN_A and FlexCAN_B                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| 0x0980                  | 152                     | CANA_ESR[BOFF_INT]                                                                                                                                                                                                                                      | CANA_ESR[BOFF_INT]                                                                                                                                                                                                                                      | FLEXCAN_A Bus off Interrupt                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| 0x0990                  | 153                     | CANA_ESR[ERR_INT]                                                                                                                                                                                                                                       | CANA_ESR[ERR_INT]                                                                                                                                                                                                                                       | FLEXCAN_A Error Interrupt                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| 0x09A0                  | 154                     | Reserved                                                                                                                                                                                                                                                | Reserved                                                                                                                                                                                                                                                | Reserved                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| 0x09B0                  | 155                     | CANA_IFRL[BUF0]                                                                                                                                                                                                                                         | CANA_IFRL[BUF0]                                                                                                                                                                                                                                         | FLEXCAN_A Buffer 0 Interrupt                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| 0x09C0                  | 156                     | CANA_IFRL[BUF1]                                                                                                                                                                                                                                         | CANA_IFRL[BUF1]                                                                                                                                                                                                                                         | FLEXCAN_A Buffer 1 Interrupt                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| 0x09D0                  | 157                     | CANA_IFRL[BUF2]                                                                                                                                                                                                                                         | CANA_IFRL[BUF2]                                                                                                                                                                                                                                         | FLEXCAN_A Buffer 2 Interrupt                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| 0x09E0                  | 158                     | CANA_IFRL[BUF3]                                                                                                                                                                                                                                         | CANA_IFRL[BUF3]                                                                                                                                                                                                                                         | FLEXCAN_A Buffer 3 Interrupt                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| 0x09F0                  | 159                     | CANA_IFRL[BUF4]                                                                                                                                                                                                                                         | CANA_IFRL[BUF4]                                                                                                                                                                                                                                         | FLEXCAN_A Buffer 4 Interrupt                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| 0x0A00                  | 160                     | CANA_IFRL[BUF5]                                                                                                                                                                                                                                         | CANA_IFRL[BUF5]                                                                                                                                                                                                                                         | FLEXCAN_A Buffer 5 Interrupt                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| 0x0A10                  | 161                     | CANA_IFRL[BUF6]                                                                                                                                                                                                                                         | CANA_IFRL[BUF6]                                                                                                                                                                                                                                         | FLEXCAN_A Buffer 6 Interrupt                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| 0x0A20                  | 162                     | CANA_IFRL[BUF7]                                                                                                                                                                                                                                         | CANA_IFRL[BUF7]                                                                                                                                                                                                                                         | FLEXCAN_A Buffer 7 Interrupt                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| 0x0A30                  | 163                     | CANA_IFRL[BUF8]                                                                                                                                                                                                                                         | CANA_IFRL[BUF8]                                                                                                                                                                                                                                         | FLEXCAN_A Buffer 8 Interrupt                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| 0x0A40                  | 164                     | CANA_IFRL[BUF9]                                                                                                                                                                                                                                         | CANA_IFRL[BUF9]                                                                                                                                                                                                                                         | FLEXCAN_A Buffer 9 Interrupt                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| 0x0A50                  | 165                     | CANA_IFRL[BUF10]                                                                                                                                                                                                                                        | CANA_IFRL[BUF10]                                                                                                                                                                                                                                        | FLEXCAN_A Buffer 10 Interrupt                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| 0x0A60                  | 166                     | CANA_IFRL[BUF11]                                                                                                                                                                                                                                        | CANA_IFRL[BUF11]                                                                                                                                                                                                                                        | FLEXCAN_A Buffer 11 Interrupt                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| 0x0A70                  | 167                     | CANA_IFRL[BUF12]                                                                                                                                                                                                                                        | CANA_IFRL[BUF12]                                                                                                                                                                                                                                        | FLEXCAN_A Buffer 12 Interrupt                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| 0x0A80                  | 168                     | CANA_IFRL[BUF13]                                                                                                                                                                                                                                        | CANA_IFRL[BUF13]                                                                                                                                                                                                                                        | FLEXCAN_A Buffer 13 Interrupt                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| 0x0A90                  | 169                     | CANA_IFRL[BUF14]                                                                                                                                                                                                                                        | CANA_IFRL[BUF14]                                                                                                                                                                                                                                        | FLEXCAN_A Buffer 14 Interrupt                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## Functional Description

## Table 10-9. INTC: Interrupt Request Sources (continued)

| Offset   | Vector   | Source 1 MPC5553        | Source 1 MPC5554        | Description                          |
|----------|----------|-------------------------|-------------------------|--------------------------------------|
| 0x0AA0   | 170      | CANA_IFRL[BUF15]        | CANA_IFRL[BUF15]        | FLEXCAN_A Buffer 15 Interrupt        |
| 0x0AB0   | 171      | CANA_IFRL[BUF31I:BUF16] | CANA_IFRL[BUF31I:BUF16] | FLEXCAN_A Buffers 31 - 16 Interrupts |
| 0x0AC0   | 172      | CANA_IFRH[BUF63I:BUF32] | CANA_IFRH[BUF63I:BUF32] | FLEXCAN_A Buffers 63 - 32 Interrupts |
| 0x0AD0   | 173      | CANC_ESR[BOFF_INT]      | CANC_ESR[BOFF_INT]      | FLEXCAN_C Bus off Interrupt          |
| 0x0AE0   | 174      | CANC_ESR[ERR_INT]       | CANC_ESR[ERR_INT]       | FLEXCAN_C Error Interrupt            |
| 0x0AF0   | 175      | Reserved                | Reserved                | Reserved                             |
| 0x0B00   | 176      | CANC_IFRL[BUF0]         | CANC_IFRL[BUF0]         | FLEXCAN_C Buffer 0 Interrupt         |
| 0x0B10   | 177      | CANC_IFRL[BUF1]         | CANC_IFRL[BUF1]         | FLEXCAN_C Buffer 1 Interrupt         |
| 0x0B20   | 178      | CANC_IFRL[BUF2]         | CANC_IFRL[BUF2]         | FLEXCAN_C Buffer 2 Interrupt         |
| 0x0B30   | 179      | CANC_IFRL[BUF3]         | CANC_IFRL[BUF3]         | FLEXCAN_C Buffer 3 Interrupt         |
| 0x0B40   | 180      | CANC_IFRL[BUF4]         | CANC_IFRL[BUF4]         | FLEXCAN_C Buffer 4 Interrupt         |
| 0x0B50   | 181      | CANC_IFRL[BUF5]         | CANC_IFRL[BUF5]         | FLEXCAN_C Buffer 5 Interrupt         |
| 0x0B60   | 182      | CANC_IFRL[BUF6]         | CANC_IFRL[BUF6]         | FLEXCAN_C Buffer 6 Interrupt         |
| 0x0B70   | 183      | CANC_IFRL[BUF7]         | CANC_IFRL[BUF7]         | FLEXCAN_C Buffer 7 Interrupt         |
| 0x0B80   | 184      | CANC_IFRL[BUF8]         | CANC_IFRL[BUF8]         | FLEXCAN_C Buffer 8 Interrupt         |
| 0x0B90   | 185      | CANC_IFRL[BUF9]         | CANC_IFRL[BUF9]         | FLEXCAN_C Buffer 9 Interrupt         |
| 0x0BA0   | 186      | CANC_IFRL[BUF10]        | CANC_IFRL[BUF10]        | FLEXCAN_C Buffer 10 Interrupt        |
| 0x0BB0   | 187      | CANC_IFRL[BUF11]        | CANC_IFRL[BUF11]        | FLEXCAN_C Buffer 11 Interrupt        |
| 0x0BC0   | 188      | CANC_IFRL[BUF12]        | CANC_IFRL[BUF12]        | FLEXCAN_C Buffer 12 Interrupt        |
| 0x0BD0   | 189      | CANC_IFRL[BUF13]        | CANC_IFRL[BUF13]        | FLEXCAN_C Buffer 13 Interrupt        |
| 0x0BE0   | 190      | CANC_IFRL[BUF14]        | CANC_IFRL[BUF14]        | FLEXCAN_C Buffer 14 Interrupt        |
| 0x0BF0   | 191      | CANC_IFRL[BUF15]        | CANC_IFRL[BUF15]        | FLEXCAN_C Buffer 15 Interrupt        |
| 0x0C00   | 192      | CANC_IFRL[BUF31:BUF16]  | CANC_IFRL[BUF31:BUF16]  | FLEXCAN_C Buffers 31 - 16 Interrupts |
| 0x0C10   | 193      | CANC_IFRH[BUF63:BUF32]  | CANC_IFRH[BUF63:BUF32]  | FLEXCAN_C Buffers 63 - 32 Interrupts |
| FEC      | FEC      | FEC                     | FEC                     | FEC                                  |
| 0x0C20   | 194      | EIR[TXF]                | Reserved                | FEC Transmit Frame flag              |
| 0x0C30   | 195      | EIR[RXF]                | Reserved                | FEC Receive Frame flag               |

Table 10-9. INTC: Interrupt Request Sources (continued)

| Offset   | Vector   | Source 1 MPC5553                                                                                      | Source 1 MPC5554       | Description                                                                                                                                                                                                                                                                                                            |
|----------|----------|-------------------------------------------------------------------------------------------------------|------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0x0C40   | 196      | EIR[HBERR] EIR[BABR] EIR[BABT] EIR[GRA] EIR[TXB] EIR[RXB] EIR[MII] EIR[EBERR] EIR[LC] EIR[RL] EIR[UN] | Reserved               | Combined Interrupt Requests of the FECEthernet Interrupt Event Register: Heartbeat Error, Babbling Receive Error, Babbling Transmit Error, Graceful Stop Complete, Transmit Buffer, Receive Buffer, Media Independent Interface, Ethernet Bus Error, Late Collision, Collision Retry Limit, and Transmit FIFO Underrun |
| 0x0C50   | 197      | Reserved                                                                                              | Reserved               | Reserved                                                                                                                                                                                                                                                                                                               |
| 0x0C60   | 198      | Reserved                                                                                              | Reserved               | Reserved                                                                                                                                                                                                                                                                                                               |
| 0x0C70   | 199      | Reserved                                                                                              | Reserved               | Reserved                                                                                                                                                                                                                                                                                                               |
| 0x0C80   | 200      | Reserved                                                                                              | Reserved               | Reserved                                                                                                                                                                                                                                                                                                               |
| 0x0C90   | 201      | Reserved                                                                                              | Reserved               | Reserved                                                                                                                                                                                                                                                                                                               |
| eMIOS    | eMIOS    | eMIOS                                                                                                 | eMIOS                  | eMIOS                                                                                                                                                                                                                                                                                                                  |
| 0x0CA0   | 202      | EMIOS_GFR[F16]                                                                                        | EMIOS_GFR[F16]         | eMIOS channel 16 Flag                                                                                                                                                                                                                                                                                                  |
| 0x0CB0   | 203      | EMIOS_GFR[F17]                                                                                        | EMIOS_GFR[F17]         | eMIOS channel 17 Flag                                                                                                                                                                                                                                                                                                  |
| 0x0CC0   | 204      | EMIOS_GFR[F18]                                                                                        | EMIOS_GFR[F18]         | eMIOS channel 18 Flag                                                                                                                                                                                                                                                                                                  |
| 0x0CD0   | 205      | EMIOS_GFR[F19]                                                                                        | EMIOS_GFR[F19]         | eMIOS channel 19 Flag                                                                                                                                                                                                                                                                                                  |
| 0x0CE0   | 206      | EMIOS_GFR[F20]                                                                                        | EMIOS_GFR[F20]         | eMIOS channel 20 Flag                                                                                                                                                                                                                                                                                                  |
| 0x0CF0   | 207      | EMIOS_GFR[F21]                                                                                        | EMIOS_GFR[F21]         | eMIOS channel 21 Flag                                                                                                                                                                                                                                                                                                  |
| 0x0D00   | 208      | EMIOS_GFR[F22]                                                                                        | EMIOS_GFR[F22]         | eMIOS channel 22 Flag                                                                                                                                                                                                                                                                                                  |
| 0x0D10   | 209      | EMIOS_GFR[F23]                                                                                        | EMIOS_GFR[F23]         | eMIOS channel 23 Flag                                                                                                                                                                                                                                                                                                  |
| eDMA     | eDMA     | eDMA                                                                                                  | eDMA                   | eDMA                                                                                                                                                                                                                                                                                                                   |
| 0x0D20   | 210      | Reserved                                                                                              | EDMA_ERRH[ERR63:ERR32] | eDMA channel Error flags 63 - 32                                                                                                                                                                                                                                                                                       |
| 0x0D30   | 211      | Reserved                                                                                              | EDMA_IRQRH[INT32]      | eDMA channel Interrupt 32                                                                                                                                                                                                                                                                                              |
| 0x0D40   | 212      | -                                                                                                     | EDMA_IRQRH[INT33]      | eDMA channel Interrupt 33                                                                                                                                                                                                                                                                                              |
| 0x0D50   | 213      | -                                                                                                     | EDMA_IRQRH[INT34]      | eDMA channel Interrupt 34                                                                                                                                                                                                                                                                                              |
| 0x0D60   | 214      | -                                                                                                     | EDMA_IRQRH[INT35]      | eDMA channel Interrupt 35                                                                                                                                                                                                                                                                                              |
| 0x0D70   | 215      | -                                                                                                     | EDMA_IRQRH[INT36]      | eDMA channel Interrupt 36                                                                                                                                                                                                                                                                                              |
| 0x0D80   | 216      | -                                                                                                     | EDMA_IRQRH[INT37]      | eDMA channel Interrupt 37                                                                                                                                                                                                                                                                                              |
| 0x0D90   | 217      | -                                                                                                     | EDMA_IRQRH[INT38]      | eDMA channel Interrupt 38                                                                                                                                                                                                                                                                                              |
| 0x0DA0   | 218      | -                                                                                                     | EDMA_IRQRH[INT39]      | eDMA channel Interrupt 39                                                                                                                                                                                                                                                                                              |
| 0x0DB0   | 219      | -                                                                                                     | EDMA_IRQRH[INT40]      | eDMA channel Interrupt 40                                                                                                                                                                                                                                                                                              |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## Functional Description

Table 10-9. INTC: Interrupt Request Sources (continued)

| Offset   | Vector   | Source 1 MPC5553   | Source 1 MPC5554   | Description                              |
|----------|----------|--------------------|--------------------|------------------------------------------|
| 0x0DC0   | 220      | -                  | EDMA_IRQRH[INT41]  | eDMA channel Interrupt 41                |
| 0x0DD0   | 221      | -                  | EDMA_IRQRH[INT42]  | eDMA channel Interrupt 42                |
| 0x0DE0   | 222      | -                  | EDMA_IRQRH[INT43]  | eDMA channel Interrupt 43                |
| 0x0DF0   | 223      | -                  | EDMA_IRQRH[INT44]  | eDMA channel Interrupt 44                |
| 0x0E00   | 224      | -                  | EDMA_IRQRH[INT45]  | eDMA channel Interrupt 45                |
| 0x0E10   | 225      | -                  | EDMA_IRQRH[INT46]  | eDMA channel Interrupt 46                |
| 0x0E20   | 226      | -                  | EDMA_IRQRH[INT47]  | eDMA channel Interrupt 47                |
| 0x0E30   | 227      | -                  | EDMA_IRQRH[INT48]  | eDMA channel Interrupt 48                |
| 0x0E40   | 228      | -                  | EDMA_IRQRH[INT49]  | eDMA channel Interrupt 49                |
| 0x0E50   | 229      | -                  | EDMA_IRQRH[INT50]  | eDMA channel Interrupt 50                |
| 0x0E60   | 230      | -                  | EDMA_IRQRH[INT51]  | eDMA channel Interrupt 51                |
| 0x0E70   | 231      | -                  | EDMA_IRQRH[INT52]  | eDMA channel Interrupt 52                |
| 0x0E80   | 232      | -                  | EDMA_IRQRH[INT53]  | eDMA channel Interrupt 53                |
| 0x0E90   | 233      | -                  | EDMA_IRQRH[INT54]  | eDMA channel Interrupt 54                |
| 0x0EA0   | 234      | -                  | EDMA_IRQRH[INT55]  | eDMA channel Interrupt 55                |
| 0x0EB0   | 235      | -                  | EDMA_IRQRH[INT56]  | eDMA channel Interrupt 56                |
| 0x0EC0   | 236      | -                  | EDMA_IRQRH[INT57]  | eDMA channel Interrupt 57                |
| 0x0ED0   | 237      | -                  | EDMA_IRQRH[INT58]  | eDMA channel Interrupt 58                |
| 0x0EE0   | 238      | -                  | EDMA_IRQRH[INT59]  | eDMA channel Interrupt 59                |
| 0x0EF0   | 239      | -                  | EDMA_IRQRH[INT60]  | eDMA channel Interrupt 60                |
| 0x0F00   | 240      | -                  | EDMA_IRQRH[INT61]  | eDMA channel Interrupt 61                |
| 0x0F10   | 241      | -                  | EDMA_IRQRH[INT62]  | eDMA channel Interrupt 62                |
| 0x0F20   | 242      | -                  | EDMA_IRQRH[INT63]  | eDMA channel Interrupt 63                |
| eTPU_B   | eTPU_B   | eTPU_B             | eTPU_B             | eTPU_B                                   |
| 0x0F30   | 243      | -                  | ETPU_CISR_B[CIS0]  | eTPU Engine B Channel 0 Interrupt Status |
| 0x0F40   | 244      | -                  | ETPU_CISR_B[CIS1]  | eTPU Engine B Channel 1 Interrupt Status |
| 0x0F50   | 245      | -                  | ETPU_CISR_B[CIS2]  | eTPU Engine B Channel 2 Interrupt Status |
| 0x0F60   | 246      | -                  | ETPU_CISR_B[CIS3]  | eTPU Engine B Channel 3 Interrupt Status |
| 0x0F70   | 247      | -                  | ETPU_CISR_B[CIS4]  | eTPU Engine B Channel 4 Interrupt Status |
| 0x0F80   | 248      | -                  | ETPU_CISR_B[CIS5]  | eTPU Engine B Channel 5 Interrupt Status |
| 0x0F90   | 249      | -                  | ETPU_CISR_B[CIS6]  | eTPU Engine B Channel 6 Interrupt Status |
| 0x0FA0   | 250      | -                  | ETPU_CISR_B[CIS7]  | eTPU Engine B Channel 7 Interrupt Status |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 10-9. INTC: Interrupt Request Sources (continued)

| Offset    | Vector    | Source 1 MPC5553   | Source 1 MPC5554                | Description                                                                                   |
|-----------|-----------|--------------------|---------------------------------|-----------------------------------------------------------------------------------------------|
| 0x0FB0    | 251       | -                  | ETPU_CISR_B[CIS8]               | eTPU Engine B Channel 8 Interrupt Status                                                      |
| 0x0FC0    | 252       | -                  | ETPU_CISR_B[CIS9]               | eTPU Engine B Channel 9 Interrupt Status                                                      |
| 0x0fd0    | 253       | -                  | ETPU_CISR_B[CIS10]              | eTPU Engine B Channel 10 Interrupt Status                                                     |
| 0x0fe0    | 254       | -                  | ETPU_CISR_B[CIS11]              | eTPU Engine B Channel 11 Interrupt Status                                                     |
| 0x0ff0    | 255       | -                  | ETPU_CISR_B[CIS12]              | eTPU Engine B Channel 12 Interrupt Status                                                     |
| 0x1000    | 256       | -                  | ETPU_CISR_B[CIS13]              | eTPU Engine B Channel 13 Interrupt Status                                                     |
| 0x1010    | 257       | -                  | ETPU_CISR_B[CIS14]              | eTPU Engine B Channel 14 Interrupt Status                                                     |
| 0x1020    | 258       | -                  | ETPU_CISR_B[CIS15]              | eTPU Engine B Channel 15 Interrupt Status                                                     |
| 0x1030    | 259       | -                  | ETPU_CISR_B[CIS16]              | eTPU Engine B Channel 16 Interrupt Status                                                     |
| 0x1040    | 260       | -                  | ETPU_CISR_B[CIS17]              | eTPU Engine B Channel 17 Interrupt Status                                                     |
| 0x1050    | 261       | -                  | ETPU_CISR_B[CIS18]              | eTPU Engine B Channel 18 Interrupt Status                                                     |
| 0x1060    | 262       | -                  | ETPU_CISR_B[CIS19]              | eTPU Engine B Channel 19 Interrupt Status                                                     |
| 0x1070    | 263       | -                  | ETPU_CISR_B[CIS20]              | eTPU Engine B Channel 20 Interrupt Status                                                     |
| 0x1080    | 264       | -                  | ETPU_CISR_B[CIS21]              | eTPU Engine B Channel 21 Interrupt Status                                                     |
| 0x1090    | 265       | -                  | ETPU_CISR_B[CIS22]              | eTPU Engine B Channel 22 Interrupt Status                                                     |
| 0x10A0    | 266       | -                  | ETPU_CISR_B[CIS23]              | eTPU Engine B Channel 23 Interrupt Status                                                     |
| 0x10B0    | 267       | -                  | ETPU_CISR_B[CIS24]              | eTPU Engine B Channel 24 Interrupt Status                                                     |
| 0x10C0    | 268       | -                  | ETPU_CISR_B[CIS25]              | eTPU Engine B Channel 25 Interrupt Status                                                     |
| 0x10D0    | 269       | -                  | ETPU_CISR_B[CIS26]              | eTPU Engine B Channel 26 Interrupt Status                                                     |
| 0x10E0    | 270       | -                  | ETPU_CISR_B[CIS27]              | eTPU Engine B Channel 27 Interrupt Status                                                     |
| 0x10F0    | 271       | -                  | ETPU_CISR_B[CIS28]              | eTPU Engine B Channel 28 Interrupt Status                                                     |
| 0x1100    | 272       | -                  | ETPU_CISR_B[CIS29]              | eTPU Engine B Channel 29 Interrupt Status                                                     |
| 0x1110    | 273       | -                  | ETPU_CISR_B[CIS30]              | eTPU Engine B Channel 30 Interrupt Status                                                     |
| 0x1120    | 274       | -                  | ETPU_CISR_B[CIS31]              | eTPU Engine B Channel 31 Interrupt Status                                                     |
| DSPI_A    | DSPI_A    | DSPI_A             | DSPI_A                          | DSPI_A                                                                                        |
| 0x1130    | 275       | -                  | DSPIA_ISR[TFUF] DSPIA_ISR[RFOF] | DSPI_A combined overrun interrupt requests: Transmit FIFO Underflow and Receive FIFO Overflow |
| 0x1140    | 276       | -                  | DSPIA_ISR[EOQF]                 | DSPI_A transmit FIFO End of Queue Flag                                                        |
| 0x1150    | 277       | -                  | DSPIA_ISR[TFFF]                 | DSPI_A Transmit FIFO Fill Flag                                                                |
| 0x1160    | 278       | -                  | DSPIA_ISR[TCF]                  | DSPI_A Transfer Complete Flag                                                                 |
| 0x1170    | 279       | -                  | DSPIA_ISR[RFDF]                 | DSPI_A Receive FIFO Drain Flag                                                                |
| FlexCAN_B | FlexCAN_B | FlexCAN_B          | FlexCAN_B                       | FlexCAN_B                                                                                     |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## Functional Description

Table 10-9. INTC: Interrupt Request Sources (continued)

| Offset   |   Vector | Source 1 MPC5553   | Source 1 MPC5554       | Description                          |
|----------|----------|--------------------|------------------------|--------------------------------------|
| 0x1180   |      280 | -                  | CANB_ESR[BOFF_INT]     | FLEXCAN_B Bus off Interrupt          |
| 0x1190   |      281 | -                  | CANB_ESR[ERR_INT]      | FLEXCAN_B Error Interrupt            |
| 0x11A0   |      282 | -                  | Reserved               | Reserved                             |
| 0x11B0   |      283 | -                  | CANB_IFRL[BUF0]        | FLEXCAN_B Buffer 0 Interrupt         |
| 0x11C0   |      284 | -                  | CANB_IFRL[BUF1]        | FLEXCAN_B Buffer 1 Interrupt         |
| 0x11D0   |      285 | -                  | CANB_IFRL[BUF2]        | FLEXCAN_B Buffer 2 Interrupt         |
| 0x11E0   |      286 | -                  | CANB_IFRL[BUF3]        | FLEXCAN_B Buffer 3 Interrupt         |
| 0x11F0   |      287 | -                  | CANB_IFRL[BUF4]        | FLEXCAN_B Buffer 4 Interrupt         |
| 0x1200   |      288 | -                  | CANB_IFRL[BUF5]        | FLEXCAN_B Buffer 5 Interrupt         |
| 0x1210   |      289 | -                  | CANB_IFRL[BUF6]        | FLEXCAN_B Buffer 6 Interrupt         |
| 0x1220   |      290 | -                  | CANB_IFRL[BUF7]        | FLEXCAN_B Buffer 7 Interrupt         |
| 0x1230   |      291 | -                  | CANB_IFRL[BUF8]        | FLEXCAN_B Buffer 8 Interrupt         |
| 0x1240   |      292 | -                  | CANB_IFRL[BUF9]        | FLEXCAN_B Buffer 9 Interrupt         |
| 0x1250   |      293 | -                  | CANB_IFRL[BUF10]       | FLEXCAN_B Buffer 10 Interrupt        |
| 0x1260   |      294 | -                  | CANB_IFRL[BUF11]       | FLEXCAN_B Buffer 11 Interrupt        |
| 0x1270   |      295 | -                  | CANB_IFRL[BUF12]       | FLEXCAN_B Buffer 12 Interrupt        |
| 0x1280   |      296 | -                  | CANB_IFRL[BUF13]       | FLEXCAN_B Buffer 13 Interrupt        |
| 0x1290   |      297 | -                  | CANB_IFRL[BUF14]       | FLEXCAN_B Buffer 14 Interrupt        |
| 0x12A0   |      298 | -                  | CANB_IFRL[BUF15]       | FLEXCAN_B Buffer 15 Interrupt        |
| 0x12B0   |      299 | -                  | CANB_IFRL[BUF31:BUF16] | FLEXCAN_B Buffers 31 - 16 Interrupts |
| 0x12C0   |      300 | -                  | CANB_IFRH[BUF63:BUF32] | FLEXCAN_B Buffers 63 - 32 Interrupts |
| 0x12D0   |      301 | -                  | Reserved               | Reserved                             |
| 0x12E0   |      302 | -                  | Reserved               | Reserved                             |
| 0x12F0   |      303 | -                  | Reserved               | Reserved                             |
| 0x1300   |      304 | -                  | Reserved               | Reserved                             |
| 0x1310   |      305 | -                  | Reserved               | Reserved                             |
| 0x1320   |      306 | -                  | Reserved               | Reserved                             |
| 0x1330   |      307 | -                  | Reserved               | Reserved                             |

- 1 Interrupt requests from the same module location are ORed together.

## NOTE

The  INTC  has  no  spurious  vector  support.  Therefore,  if  an  asserted peripheral  or  software  settable  interrupt  request,  whose  PRI n value  in INTC\_PSR0-INTC\_PSR307 is higher than the PRI value in INTC\_CPR, negates before the interrupt request to the processor for that peripheral or software settable interrupt request is acknowledged, the interrupt request to the processor still can assert or will remain asserted for that peripheral or software  settable  interrupt  request.  In  this  case,  the  interrupt  vector  will correspond to that peripheral or software settable interrupt request. Also, the PRI value in the INTC\_CPR will be updated with the corresponding PRI n value in INTC\_PSR n .

Furthermore,  clearing  the  peripheral  interrupt  request's  enable  bit  in  the peripheral or, alternatively, setting its mask bit has the same consequences as clearing its flag bit. Setting its enable bit or clearing its mask bit while its flag bit is asserted has the same effect on the INTC as an interrupt event setting the flag bit.

## 10.4.1.1 Peripheral Interrupt Requests

An interrupt event in a peripheral's hardware sets a flag bit which resides in that peripheral. The interrupt request from the peripheral is driven by that flag bit.

The time from when the peripheral starts to drive its peripheral interrupt request to the INTC to the time that the INTC starts to drive the interrupt request to the processor is three clocks.

## 10.4.1.2 Software Settable Interrupt Requests

The  software  set/clear interrupt registers (INTC\_SSCIR x\_x ) support the setting or clearing of software-settable interrupt requests. These registers contain eight independent sets of bits to set and clear a corresponding flag bit by software. With the exception of being set by software, this flag bit behaves the same as a flag bit set within a peripheral. This flag bit generates an interrupt request within the INTC just like a peripheral interrupt request.

An interrupt  request  is  triggered  by  software  writing  a  1  to  the  SET n bit  in  INTC  software  set/clear interrupt registers (INTC\_SSCIR0-INTC\_SSCIR7). This write sets the corresponding CLR n bit, which is a flag bit, resulting in the interrupt request. The interrupt request is cleared by writing a 1 to the CLR n bit. Specific behavior includes the following:

- · Writing a 1 to SET n leaves SET n unchanged at '0' but sets the flag bit (which is the CLR n bit).
- · Writing a 0 to SET n has no effect.
- · Writing a 1 to CLR n clears the flag (CLRx) bit.
- · Writing a 0 to CLR n has no effect.
- · If a 1 is written to a pair of SET n and CLR n bits at the same time, the flag (CLRx) is set, regardless of whether CLR n was asserted before the write.

The time from the write to the SET n bit to the time that the INTC starts to drive the interrupt request to the processor is four clocks.

## 10.4.1.3 Unique Vector for Each Interrupt Request Source

Each  peripheral  and  software  settable  interrupt  request  is  assigned  a  hardwired  unique  9-bit  vector. Software settable interrupts 0-7 are assigned vectors 0-7, respectively. The peripheral interrupt requests are assigned vectors 8 to as high as needed to cover all of the peripheral interrupt requests.

## 10.4.2 Priority Management

The asserted interrupt requests are compared to each other based on their PRI n values in INTC priority select registers (INTC\_PSR0-INTC\_PSR307). The result of that comparison also is compared to PRI in INTC current priority register (INTC\_CPR). The results of those comparisons are used to manage the priority of the ISR being executed by the processor. The LIFO also assists in managing that priority.

## 10.4.2.1 Current Priority and Preemption

The priority arbitrator, selector, encoder, and comparator submodules shown in Figure 10-1 are used to compare the priority of the asserted interrupt requests to the current priority. If the priority of any asserted peripheral or software settable interrupt request is higher than the current priority, then the interrupt request to  the  processor  is  asserted.  Also,  a  unique  vector  for  the  preempting  peripheral  or  software  settable interrupt request is generated for INTC interrupt acknowledge register (INTC\_IACKR), and if in hardware vector mode, for the interrupt vector provided to the processor.

## 10.4.2.1.1 Priority Arbitrator Submodule

The priority arbitrator submodule compares all the priorities of all of the asserted interrupt requests, both peripheral and software settable. The output of the priority arbitrator submodule is the highest of those priorities. Also, any interrupt requests which have this highest priority are output as asserted interrupt requests to the request selector submodule.

## 10.4.2.1.2 Request Selector Submodule

If only one interrupt request from the priority arbitrator submodule is asserted, then it is passed as asserted to the vector encoder submodule. If multiple interrupt requests from the priority arbitrator submodule are asserted, then only the one with the lowest vector is passed as asserted to the vector encoder submodule. The lower vector is chosen regardless of the time order of the assertions of the peripheral or software settable interrupt requests.

## 10.4.2.1.3 Vector Encoder Submodule

The vector encoder submodule generates the unique 9-bit vector for the asserted interrupt request from the request selector submodule.

## 10.4.2.1.4 Priority Comparator Submodule

The  priority  comparator  submodule  compares  the  highest  priority  output  from  the  priority  arbitrator submodule with PRI in INTC\_CPR. If the priority comparator submodule detects that this highest priority is higher than the current priority, then it asserts the interrupt request to the processor. This interrupt request to the processor asserts whether this highest priority is raised above the value of PRI in INTC\_CPR or the PRI value in INTC\_CPR is lowered below this highest priority. This highest priority then becomes the new priority  which  will  be  written  to  PRI  in  INTC\_CPR  when  the  interrupt  request  to  the  processor  is acknowledged.  Interrupt  requests  whose  PRI n in  INTC\_PSR n are  zero  will  not  cause  a  preemption because their PRI n will not be higher than PRI in INTC\_CPR.

## 10.4.2.2 LIFO

The LIFO stores the preempted PRI values from the INTC\_CPR. Therefore, because these priorities are stacked within the INTC, if interrupts need to be enabled during the ISR, at the beginning of the interrupt exception handler the PRI value in the INTC\_CPR does not need to be loaded from the INTC\_CPR and stored onto the context stack. Likewise at the end of the interrupt exception handler, the priority does not need to be loaded from the context stack and stored into the INTC\_CPR.

The PRI value in the INTC\_CPR is pushed onto the LIFO when the INTC\_IACKR is read in software vector mode or the interrupt acknowledge signal from the processor is asserted in hardware vector mode. The priority is popped into PRI in the INTC\_CPR whenever the INTC\_EOIR is written.

Although the INTC supports 16 priorities, an ISR executing with PRI in the INTC\_CPR equal to 15 will not be preempted. Therefore, the LIFO supports the stacking of 15 priorities. However, the LIFO is only 14 entries deep. An entry for a priority of 0 is not needed because of how pushing onto a full LIFO and popping an empty LIFO are treated. If the LIFO is pushed 15 or more times than it is popped, the priorities first pushed are overwritten. A priority of 0 would be an overwritten priority. However, the LIFO will pop '0's if it is popped more times than it is pushed. Therefore, although a priority of 0 was overwritten, it is regenerated with the popping of an empty LIFO.

The LIFO is not memory mapped.

## 10.4.3 Details on Handshaking with Processor

## 10.4.3.1 Software Vector Mode Handshaking

## 10.4.3.1.1 Acknowledging Interrupt Request to Processor

A timing diagram of the interrupt request and acknowledge handshaking in software vector mode, along with the handshaking near the end of the interrupt exception handler, is shown in Figure 10-14. The INTC examines the peripheral and software settable interrupt requests. When it finds an asserted peripheral or software  settable  interrupt  request  with  a  higher  priority  than  PRI  in  INTC  current  priority  register (INTC\_CPR),  it  asserts  the  interrupt  request  to  the  processor.  The  INTVEC  field  in  INTC  interrupt acknowledge register (INTC\_IACKR) is updated with the preempting interrupt request's vector when the interrupt request to the processor is asserted. The INTVEC field retains that value until the next time the interrupt request to the processor is asserted. The rest of the handshaking is described in Section 10.1.4.1, 'Software Vector Mode.'

## 10.4.3.1.2 End-of-Interrupt Exception Handler

Before the interrupt exception handling completes, INTC end-of-interrupt register (INTC\_EOIR) must be written. When it is written, the LIFO is popped so that the preempted priority is restored into PRI of the INTC\_CPR. Before it is written, the peripheral or software settable flag bit must be cleared so that the peripheral or software settable interrupt request is negated.

## NOTE

To  ensure  proper  operation  across  all  eSys  MCUs,  execute  an mbar or msync instruction between the access to clear the flag bit and the write to the INTC\_EOIR.

When returning from the preemption, the INTC does not search for the peripheral or software settable interrupt request whose ISR was preempted. Depending on how much the ISR progressed, that interrupt request  may  no  longer  even  be  asserted.  When  PRI  in  INTC\_CPR  is  lowered  to  the  priority  of  the

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Freescale Semiconductor

preempted ISR, the interrupt request for the preempted ISR or any other asserted peripheral or software settable interrupt request at or below that priority will not cause a preemption. Instead, after the restoration of the preempted context, the processor will return to the instruction address that it was to next execute before it was preempted. This next instruction is part of the preempted ISR or the interrupt exception handler's prolog or epilog.

Figure 10-14. Software Vector Mode Handshaking Timing Diagram

<!-- image -->

## 10.4.3.2 Hardware Vector Mode Handshaking

A timing diagram of the interrupt request and acknowledge handshaking in hardware vector mode, along with the handshaking near the end of the interrupt exception handler, is shown in Figure 10-15. As in software vector mode, the INTC examines the peripheral and software settable interrupt requests, and when it finds an asserted one with a higher priority than PRI in INTC\_CPR, it asserts the interrupt request to the processor. The INTVEC field in the INTC\_IACKR is updated with the preempting peripheral or software settable interrupt request's vector when the interrupt request to the processor is asserted. The INTVEC field retains that value until the next time the interrupt request to the processor is asserted. In addition, the value of the interrupt vector to the processor matches the value of the INTVEC field in the INTC\_IACKR. The rest of the handshaking is described in Section 10.1.4.2, 'Hardware Vector Mode.'

The handshaking near the end of the interrupt exception handler, that is the writing to the INTC\_EOIR, is the same as in software vector mode. Refer to Section 10.4.3.1.2, 'End-of-Interrupt Exception Handler.'

Figure 10-15. Hardware Vector Mode Handshaking Timing Diagram

<!-- image -->

## 10.5 Initialization/Application Information

## 10.5.1 Initialization Flow

After exiting reset, all of the PRI n fields in INTC priority select registers (INTC\_PSR0-INTC\_PSR307) will be zero, and PRI in INTC current priority register (INTC\_CPR) will be 15. These reset values will prevent the INTC from asserting the interrupt request to the processor. The enable or mask bits in the peripherals are reset such that the peripheral interrupt requests are negated. An initialization sequence for allowing  the  peripheral  and  software  settable  interrupt  requests  to  cause  an  interrupt  request  to  the processor is:

interrupt\_request\_initialization: configure VTES and HVEN in INTC\_MCR configure VTBA in INTC\_IACKR raise the PRI n fields in INTC\_PSR n set the enable bits or clear the mask bits for the peripheral interrupt requests lower PRI in INTC\_CPR to zero enable processor recognition of interrupts

## 10.5.2 Interrupt Exception Handler

These example interrupt exception handlers use PowerPC Book E assembly code.

## 10.5.2.1 Software Vector Mode

interrupt\_exception\_handler:

code to create stack frame, save working register, and save SRR0 and SRR1

lis

r3,INTC\_IACKR@ha

# form adjusted upper half of INTC\_IACKR address

lwz

r3,INTC\_IACKR@l(r3)

# load INTC\_IACKR, which clears request to processor

lwz

r3,0x0(r3)

# load address of ISR from vector table

wrteei

1

# enable processor recognition of interrupts

code to save rest of context required by e500 EABI

mtlr r3

- # move INTC\_IACKR contents into link register

blrl

- # branch to ISR; link register updated with epilog
- # address

epilog:

code to restore most of context required by e500 EABI

- # Popping the LIFO after the restoration of most of the context and the disabling of processor

# recognition of interrupts eases the calculation of the maximum stack depth at the cost of

- # postponing the servicing of the next interrupt request.

mbar

- # ensure store to clear flag bit has completed

lis li

wrteei r3,INTC\_EOIR@ha

r4,0x0

0

- # form adjusted upper half of INTC\_EOIR address
- # form 0 to write to INTC\_EOIR
- # disable processor recognition of interrupts

stw r4,INTC\_EOIR@l(r3)

- # store to INTC\_EOIR, informing INTC to lower priority

code to restore SRR0 and SRR1, restore working registers, and delete stack frame rfi

vector\_table\_base\_address: address of ISR for interrupt with vector 0

address of ISR for interrupt with vector 1

.

.

.

address of ISR for interrupt with vector 510

address of ISR for interrupt with vector 511

```
ISR : x code to service the interrupt event code to clear flag bit which drives interrupt request to INTC blr # return to epilog
```

## 10.5.2.2 Hardware Vector Mode

This interrupt exception handler is useful with processor and system bus implementations that support a hardware vector. This example assumes that each interrupt\_exception\_handler x only has space for four instructions, and therefore a branch to interrupt\_ exception\_handler\_continued x is needed.

interrupt\_exception\_handler : x b interrupt\_exception\_handler\_continued x

# 4 instructions available, branch to continue interrupt\_exception\_handler\_continued x :

code to create stack frame, save working register, and save SRR0 and SRR1

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

```
wrteei 1 # enable processor recognition of interrupts code to save rest of context required by e500 EABI bl ISR x # branch to ISR for interrupt with vector x epilog: code to restore most of context required by e500 EABI # Popping the LIFO after the restoration of most of the context and the disabling of processor # recognition of interrupts eases the calculation of the maximum stack depth at the cost of # postponing the servicing of the next interrupt request. mbar # ensure store to clear flag bit has completed lis r3,INTC_EOIR@ha # form adjusted upper half of INTC_EOIR address li r4,0x0 # form 0 to write to INTC_EOIR wrteei 0 # disable processor recognition of interrupts stw r4,INTC_EOIR@l(r3) # store to INTC_EOIR, informing INTC to lower priority code to restore SRR0 and SRR1, restore working registers, and delete stack frame rfi ISR : x code to service the interrupt event code to clear flag bit which drives interrupt request to INTC
```

```
blr # branch to epilog
```

## 10.5.3 ISR, RTOS, and Task Hierarchy

The RTOS and all of the tasks under its control typically execute with PRI in INTC current priority register (INTC\_CPR) having a value of 0. The RTOS will execute the tasks according to whatever priority scheme that it may have, but that priority scheme is independent and has a lower priority of execution than the priority scheme of the INTC. In other words, the ISRs execute above INTC\_CPR priority 0 and outside the control of the RTOS, the RTOS executes at INTC\_CPR priority 0, and while the tasks execute at different priorities under the control of the RTOS, they also execute at INTC\_CPR priority 0.

If a task shares a resource with an ISR and the PCP is being used to manage that shared resource, then the task's priority can be elevated in the INTC\_CPR while the shared resource is being accessed.

An ISR whose PRI n in INTC priority select registers (INTC\_PSR0-INTC\_PSR307) has a value of 0 will not cause an interrupt request to the processor, even if its peripheral or software settable interrupt request is asserted. For a peripheral interrupt request, not setting its enable bit or disabling the mask bit will cause it to remain negated, which consequently also will not cause an interrupt request to the processor. Since the ISRs are outside the control of the RTOS, this ISR will not run unless called by another ISR or the interrupt exception handler, perhaps after executing another ISR.

## 10.5.4 Order of Execution

An ISR with a higher priority can preempt an ISR with a lower priority, regardless of the unique vectors associated  with  each  of  their  peripheral  or  software  settable  interrupt  requests.  However,  if  multiple peripheral or software settable interrupt requests are asserted, more than one has the highest priority, and that priority is high enough to cause preemption, the INTC selects the one with the lowest unique vector

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

regardless  of  the  order  in  time  that  they  asserted.  However,  the  ability  to  meet  deadlines  with  this scheduling scheme is no less than if the ISRs execute in the time order that their peripheral or software settable interrupt requests asserted.

The example in Table 10-10 shows the order of execution of both ISRs with different priorities and the same priority.

Table 10-10. Order of ISR Execution Example

|      |                                                                                                         | Code Executing At End of Step   | Code Executing At End of Step   | Code Executing At End of Step   | Code Executing At End of Step   | Code Executing At End of Step   | Code Executing At End of Step   | PRI in INTC_CPR at End of   |
|------|---------------------------------------------------------------------------------------------------------|---------------------------------|---------------------------------|---------------------------------|---------------------------------|---------------------------------|---------------------------------|-----------------------------|
| Step | Step Description                                                                                        | RTOS                            | ISR108 1                        | ISR208                          | ISR308                          | ISR408                          | Interrupt Exception Handler     | Step                        |
| 1    | RTOS at priority 0 is executing.                                                                        | X                               |                                 |                                 |                                 |                                 |                                 | 0                           |
| 2    | Peripheral interrupt request 100 at priority 1 asserts. Interrupt taken.                                |                                 | X                               |                                 |                                 |                                 |                                 | 1                           |
| 3    | Peripheral interrupt request 400 at priority 4 is asserts. Interrupt taken.                             |                                 |                                 |                                 |                                 | X                               |                                 | 4                           |
| 4    | Peripheral interrupt request 300 at priority 3 is asserts.                                              |                                 |                                 |                                 |                                 | X                               |                                 | 4                           |
| 5    | Peripheral interrupt request 200 at priority 3 is asserts.                                              |                                 |                                 |                                 |                                 | X                               |                                 | 4                           |
| 6    | ISR408 completes. Interrupt exception handler writes to INTC_EOIR.                                      |                                 |                                 |                                 |                                 |                                 | X                               | 1                           |
| 7    | Interrupt taken. ISR208 starts to execute, even though peripheral interrupt request 300 asserted first. |                                 |                                 | X                               |                                 |                                 |                                 | 3                           |
| 8    | ISR208 completes. Interrupt exception handler writes to INTC_EOIR.                                      |                                 |                                 |                                 |                                 |                                 | X                               | 1                           |
| 9    | Interrupt taken. ISR308 starts to execute.                                                              |                                 |                                 |                                 | X                               |                                 |                                 | 3                           |
| 10   | ISR308 completes. Interrupt exception handler writes to INTC_EOIR.                                      |                                 |                                 |                                 |                                 |                                 | X                               | 1                           |
| 11   | ISR108 completes. Interrupt exception handler writes to INTC_EOIR.                                      |                                 |                                 |                                 |                                 |                                 | X                               | 0                           |
| 12   | RTOS continues execution.                                                                               | X                               |                                 |                                 |                                 |                                 |                                 | 0                           |

1 ISR108 executes for peripheral interrupt request 100 because the first eight ISRs are for software settable interrupt requests.

## 10.5.5 Priority Ceiling Protocol

## 10.5.5.1 Elevating Priority

The PRI field in INTC current priority register (INTC\_CPR) is elevated in the OSEK PCP to the ceiling of all of the priorities of the ISRs that share a resource. This protocol therefore allows coherent accesses of the ISRs to that shared resource.

For example, ISR1 has a priority of 1, ISR2 has a priority of 2, and ISR3 has a priority of 3. They all share the  same  resource.  Before  ISR1  or  ISR2  can  access  that  resource,  they  must  raise  the  PRI  value  in INTC\_CPR to 3, the ceiling of all of the ISR priorities. After they release the resource, they must lower the PRI value in INTC\_CPR to prevent further priority inversion. If they do not raise their priority, then ISR2 can preempt ISR1, and ISR3 can preempt ISR1 or ISR2, possibly corrupting the shared resource. Another possible failure mechanism is deadlock if the higher priority ISR needs the lower priority ISR to release the resource before it can continue, but the lower priority ISR can not release the resource until the higher priority ISR completes and execution returns to the lower priority ISR.

Using the PCP instead of disabling processor recognition of all interrupts reduces the priority inversion time  when  accessing  a  shared  resource.  For  example,  while  ISR3  can  not  preempt  ISR1  while  it  is accessing the shared resource, all of the ISRs with a priority higher than 3 can preempt ISR1.

## 10.5.5.2 Ensuring Coherency

A scenario can exist that can cause non-coherent accesses to the shared resource. As an example, ISR1 and ISR2 both share a resource. ISR1 has a lower priority than ISR2. ISR1 is executing, and it writes to the INTC\_CPR. The instruction following this store is a store to a value in a shared coherent data block. Either just before or at the same time as the first store, the INTC asserts the interrupt request to the processor because  the  peripheral  interrupt  request  for  ISR2  has  asserted.  As  the  processor  is  responding  to  the interrupt request from the INTC, and as it is aborting transactions and flushing its pipeline, it is possible that both of these stores will be executed. ISR2 thereby thinks that it can access the data block coherently, but the data block has been corrupted.

OSEK uses the GetResource and ReleaseResource system services to manage access to a shared resource. To prevent this corruption of a coherent data block, modifications to PRI in INTC\_CPR can be made by those system services with the following code sequences.

```
GetResource: raise PRI mbar isync ReleaseResource: mbar
```

lower PRI

## 10.5.6 Selecting Priorities According to Request Rates and Deadlines

The selection of the priorities for the ISRs can be made using rate monotonic scheduling or a superset of it,  deadline  monotonic  scheduling.  In  RMS,  the  ISRs  which  have  higher  request  rates  have  higher priorities. In DMS, if the deadline is before the next time the ISR is requested, then the ISR is assigned a priority according to the time from the request for the ISR to the deadline, not from the time of the request for the ISR to the next request for it.

For example, ISR1 executes every 100 µ s, ISR2 executes every 200 µ s, and ISR3 executes every 300 µ s. ISR1 has a higher priority than ISR2 which has a higher priority than ISR3. However, if ISR3 has a deadline of 150 µ s, then it has a higher priority than ISR2.

The INTC has 16 priorities, which could be much less than the number of ISRs. In this case, the ISRs should be grouped with other ISRs that have similar deadlines. For example, a priority could be allocated for every time the request rate doubles. ISRs with request rates around 1 ms would share a priority, ISRs with request rates around 500 µ s would share a priority, ISRs with request rates around 250 µ s would share a priority, etc. With this approach, a range of ISR request rates of 2 16 could be covered, regardless of the number of ISRs.

Reducing the number of priorities does cause some priority inversion which reduces the processor's ability to meet its deadlines. It also allows easier management of ISRs with similar deadlines that share a resource. They can be placed at the same priority without any further priority inversion, and they do not need to use the PCP to access the shared resource.

## 10.5.7 Software Settable Interrupt Requests

The software settable interrupt requests can be used in two ways. They can be used to schedule a lower priority portion of an ISR and for processors to interrupt other processors in a multiple processor system.

## 10.5.7.1 Scheduling a Lower Priority Portion of an ISR

A  portion  of  an  ISR  needs  to  be  executed  at  the  PRI n value  in  INTC  priority  select  registers (INTC\_PSR0-INTC\_PSR307),  which  becomes  the  PRI  value  in  INTC  current  priority  register (INTC\_CPR) with the interrupt acknowledgement. The ISR, however, can have a portion of it which does not need to be executed at this higher priority. Therefore, executing this later portion which does not need to be executed at this higher priority can block the execution of ISRs which do not have a higher priority than the earlier portion of the ISR but do have a higher priority than what the later portion of the ISR needs. This priority inversion reduces the processor's ability to meet its deadlines.

One option is for the ISR to complete the earlier higher priority portion, but then schedule through the RTOS a task to execute the later lower priority portion. However, some RTOSs can require a large amount of time for an ISR to schedule a task. Therefore, a second option is for the ISR, after completing the higher priority portion, to set a SET n bit in INTC software set/clear interrupt registers (INTC\_SSCIR0-INTC\_SSCIR7). Writing a 1 to SET n causes a software settable interrupt request. This software  settable  interrupt  request,  which  usually  will  have  a  lower  PRI n value  in  the  INTC\_PSR n , therefore will not cause priority inversion.

## 10.5.7.2 Scheduling an ISR on Another Processor

Since the SET n bits in the INTC\_SSCIR n are memory mapped, processors in multiple processor systems can schedule ISRs on the other processors. One application is that one processor simply wants to command another processor to perform a piece of work, and the initiating processor does not need to use the results of that work. If the initiating processor is concerned that processor executing the software settable ISR has not completed the work before asking it to again execute that ISR, it can check if the corresponding CLR n bit in INTC\_SSCIR n is asserted before again writing a 1 to the SET n bit.

Another  application  is  the  sharing  of  a  block  of  data.  For  example,  a  first  processor  has  completed accessing a block of data and wants a second processor to then access it. Furthermore, after the second processor has completed accessing the block of data, the first processor again wants to access it. The accesses to the block of data must be done coherently. The procedure is that the first processor writes a 1 to a SET n bit on the second processor. The second processor, after accessing the block of data, clears the

Interrupt Controller (INTC)

corresponding CLR n bit and then writes 1 to a SET n bit on the first processor, informing it that it now can access the block of data.

## 10.5.8 Lowering Priority Within an ISR

In  implementations  without  the  software-settable  interrupt  requests  in  the  INTC  software  set/clear interrupt registers (INTC\_SSCIR0-INTC\_SSCIR7), the only way-besides scheduling a task through an RTOS-to prevent priority inversion with an ISR whose work spans multiple priorities (as described in Section 10.5.7.1,  'Scheduling  a  Lower  Priority  Portion  of  an  ISR,')  is  to  lower  the  current  priority. However, the INTC has a LIFO whose depth is determined by the number of priorities.

## NOTE

Lowering  the  PRI  value  in  INTC  current  priority  register  (INTC\_CPR) within an ISR to below the ISR's corresponding PRI value in INTC priority select  registers  (INTC\_PSR0-INTC\_PSR307)  allows  more  preemptions than the depth of the LIFO can support.

Therefore, the INTC does not support lowering the current priority within an ISR as a way to avoid priority inversion.

## 10.5.9 Negating an Interrupt Request Outside of its ISR

## 10.5.9.1 Negating an Interrupt Request as a Side Effect of an ISR

Some peripherals have flag bits which can be cleared as a side effect of servicing a peripheral interrupt request.  For  example,  reading  a  specific  register  can  clear  the  flag  bits,  and  consequently  their corresponding interrupt  requests  too.  This  clearing  as  a  side  effect  of  servicing  a  peripheral  interrupt request can cause the negation of other peripheral interrupt requests besides the peripheral interrupt request whose ISR presently is executing. This negating of a peripheral interrupt request outside of its ISR can be a desired effect.

## 10.5.9.2 Negating Multiple Interrupt Requests in One ISR

An ISR can clear other flag bits besides its own flag bit. One reason that an ISR clears multiple flag bits is because it serviced those other flag bits, and therefore the ISRs for these other flag bits do not need to be executed.

## 10.5.9.3 Proper Setting of Interrupt Request Priority

Whether an interrupt request negates outside of its own ISR due to the side effect of an ISR execution or the intentional clearing a flag bit, the priorities of the peripheral or software settable interrupt requests for these  other  flag  bits  must  be  selected  properly.  Their  PRI n values  in  INTC  priority  select  registers (INTC\_PSR0-INTC\_PSR307) must be selected to be at or lower than the priority of the ISR that cleared their flag bits. Otherwise, those flag bits still can cause the interrupt request to the processor to assert. Furthermore, the clearing of these other flag bits also has the same timing relationship to the writing to INTC end-of-interrupt register (INTC\_EOIR) as the clearing of the flag bit that caused the present ISR to be executed. Refer to Section 10.4.3.1.2, 'End-of-Interrupt Exception Handler,' for more information.

A flag bit whose enable bit or mask bit is negating its peripheral interrupt request can be cleared at any time, regardless of the peripheral interrupt request's PRI n value in INTC\_PSR n .

## 10.5.10 Examining LIFO contents

Normally the user does not need to know the contents of the LIFO. One may not even know how deeply the LIFO is nested. However, if one should want to read the contents,  they are not memory mapped. The contents still can be read by popping the LIFO and reading the PRI field in the INTC current priority register (INTC\_CPR). The code sequence is:

```
pop_lifo: store to INTC_EOIR load INTC_CPR, examine PRI, and store onto stack if PRI is not zero or value when interrupts were enabled, branch to pop_lifo
```

When the examination is complete, the LIFO can be restored using this code sequence:

```
push_lifo: load stacked PRI value and store to INTC_CPR load INTC_IACKR if stacked PRI values are not depleted, branch to push_lifo
```

## 10.6 Revision History

## Substantive Changes since Rev 3.0

In section Section 10.1.4.1, 'Software Vector Mode,' third paragraph, after the sentence, "The interrupt request to the processor will not clear if a higher priority interrupt request arrives," added the sentence "Even in this case, INTVEC will not update to the higher priority request until the lower priority interrupt request is acknowledged by reading the INTC\_IACKR."

In section Section 10.1.4.2, 'Hardware Vector Mode,' second paragraph, changed the sentence, "Even if a higher priority interrupt request arrives while waiting for this interrupt acknowledge, the interrupt request to the processor will negate for at least one clock," to "However, the interrupt request to the processor will not negate if a higher priority interrupt request arrives. Even in this case, the interrupt vector number will not update to the higher priority request until the lower priority request is acknowledged by the processor."

Updated Table 10-9 to reflect MPC5553 interrupt sources.

Interrupt Controller (INTC)
