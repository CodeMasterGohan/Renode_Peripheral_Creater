### Chatper 16 Boot Assist Module (BAM)

## 16.1 Introduction

This chapter describes the boot assist module (BAM).

## 16.1.1 Block Diagram

Figure 16-1 is a block diagram of the BAM.

Figure 16-1. BAM Block Diagram

<!-- image -->

## 16.1.2 Overview

The MPC5553/MPC5554 BAM contains the MCU boot program code, identical for all eSys MCUs with an e200z6 core. The BAM control block is connected to peripheral bridge B and occupies the last 16 Kbytes of the  MCU memory space. The BAM program supports four different booting modes: from internal Flash, from external memory without bus arbitration, from external memory with bus arbitration, serial boot via SCI or CAN interfaces. The BAM program is executed by the e200z6 core just after the MCU reset. Depending on the boot mode, the program initializes appropriate minimum MCU resources to start user code execution.

## 16.1.3 Features

The BAM program provides:

- · Initial e200z6 core MMU setup with minimum address translation for all internal MCU resources and external memory address space
- · Location and detection of user boot code
- · Automatic switch to serial boot mode if internal or external Flash is blank or invalid
- · User programmable 64-bit password protection for serial boot mode
- · Booting user code from internal Flash module, from external memory without arbitration and from external memory with arbitration
- · Serial boot by loading user program via CAN bus or eSCI to the internal SRAM
- · Censorship protection for internal flash module

- · An option to enable the e200z6 core watchdog timer
- · An option to configure the external data bus to 16- or 32-bits wide (416 PBGA package only)

## 16.1.4 Modes of Operation

## 16.1.4.1 Normal Mode

In normal operation the BAM responds to all read requests within its address space. The BAM program is executed following the negation of reset.

## 16.1.4.2 Debug Mode

The BAM program is not executed when the MCU comes out of reset in OnCE debug mode. The user should provide the required MCU initialization using the development tool before accessing the MCU resources.

## 16.1.4.3 Internal Boot Mode

This mode of operation is intended for systems that boot from internal Flash memory. The internal Flash is  used  for  all  code  and  all  boot  configuration  data.  Once  the  BAM  program  has  completed  the  boot process, user code may enable the external bus interface if required.

## 16.1.4.4 External Boot Modes

This mode of operation is intended for systems that have user code and configuration information in an external memory device connected to the external bus. The bus arbitration can be enabled to allow a boot option for multiprocessor systems.

Note that external boot mode should not be chosen for devices that do not have an external bus.

## 16.1.4.5 Serial Boot Mode

This mode of operation is intended to load a user program into internal SRAM using either the eSCI or CAN serial interface, then to execute that program. The program can then be used to control the download of data and erasing/programming of the internal or external Flash memory.

## 16.2 Memory Map/Register Definition

The BAM occupies 16 Kbytes of memory space, 0xFFFF\_C000 to 0xFFFF\_FFFF. The actual code size of the BAM program is less than 4 Kbytes and starts at 0xFFFF\_F000, repeating itself down every 4 Kbytes in the BAM address space. The CPU starts the BAM program execution at its reset vector from address 0xFFFF\_FFFC. Table 16-1 shows the BAM address map.

Table 16-1. BAM Memory Map

| Address                   | Description          |
|---------------------------|----------------------|
| 0xFFFF_C000 - 0xFFFF_CFFF | BAM Program Mirrored |
| 0xFFFF_D000 - 0xFFFF_DFFF | BAM Program Mirrored |

## Table 16-1. BAM Memory Map  (continued)

| 0xFFFF_E000 - 0xFFFF_EFFF   | BAM Program Mirrored   |
|-----------------------------|------------------------|
| 0xFFFF_F000 - 0xFFFF_FFFF   | BAM Program            |

## 16.3 Functional Description

## 16.3.1 BAM Program Resources

The BAM program uses/initializes following MCU resources:

- · The BOOTCFG field in the reset status register (SIU\_RSR) to determine the boot option.
- · The location and value of the reset configuration half word (RCHW) to determine the location of boot code and the boot configuration options. Refer to Chapter 4, 'Reset' for information about the RCHW.
- · The DISNEX bit in the SIU\_CCR to determine if the Nexus port is enabled.
- · The MMU to allow core access to the MCU internal resources and external bus.
- · The EBI registers and external bus pads, when performing external boot modes.
- · The CAN\_A, eSCI\_A and their pads, when performing serial boot mode.
- · The eDMA during serial boot mode.

## 16.3.2 BAM Program Operation

BAM is accessed by the MCU core after the negation of RSTOUT, before user code starts.

First, the BAM program configures e200z6 core MMU to allow access to all MCU internal resources and external memory space, according the Table 16-2. This MMU setup remains the same for internal Flash Boot mode.

Table 16-2. MMU Configuration for Internal Flash Boot

|   TLB Entry | Region                      | Logical Base Address   | Physical Base Address   | Size       | Attributes                                          |
|-------------|-----------------------------|------------------------|-------------------------|------------|-----------------------------------------------------|
|           0 | Peripheral Bridge B and BAM | 0xFFF0_0000            | 0xFFF0_0000             | 1 Mbyte    | Cache inhibited Guarded Big Endian Global PID       |
|           1 | Internal Flash              | 0x0000_0000            | 0x0000_0000             | 16 Mbytes  | Cache enabled Not guarded Big Endian Global PID     |
|           2 | EBI                         | 0x2000_0000            | 0x0000_0000             | 16 Mbytes  | Cache enabled Not guarded Big Endian Global PID     |
|           3 | Internal SRAM               | 0x4000_0000            | 0x4000_0000             | 256 Kbytes | Cache inhibited Not guarded Big Endian Global PID   |
|           4 | Peripheral Bridge A         | 0xC3F0_0000            | 0xC3F0_0000             | 1 Mbyte    | Cache inhibited Not Guarded 1 Big Endian Global PID |

1 For future compatibility, configure peripheral bridge A as guarded.

The MMU regions are mapped with logical address the same as physical address except for the external bus interface (EBI). The logical EBI address space is mapped to physical addresses of the internal Flash memory. This allows a code, written to run from external memory, to be executed from internal Flash

Then  the  BAM  program  reads  the  status  of  the  two  BOOTCFG  pins  from  the  reset  status  register (SIU\_RSR) and the appropriate boot sequence is started as shown in the Table 16-3.

Depending on the values stored in the censorship word and serial boot control word in the shadow row of internal Flash memory, the internal Flash memory can be enabled or disabled, the Nexus port can be enabled or disabled, the password received in serial boot mode is compared with a fixed public password or compared to a user programmable password in the internal Flash memory. The Table 16-3 summarizes all these possibilities.

Table 16-3. Boot Modes

|   BOOTCFG [0:1] | Censorship Control 0x00FF_FDE0   | Serial Boot Control 0x00FF_FDE2   | Boot Mode Name    | Internal Flash State   | Nexus State   | Serial Password   |
|-----------------|----------------------------------|-----------------------------------|-------------------|------------------------|---------------|-------------------|
|              00 | !0x55AA                          | Don't care                        | Internal-Censored | Enabled                | Disabled      | Flash             |
|              00 | 0x55AA                           | Don't care                        | Internal-Public   | Enabled                | Enabled       | Public            |

Note: '!' = 'NOT', meaning any value other than the value specified. Values 0x0000 and 0xFFFF should not be used.

Table 16-3. Boot Modes (continued)

| 01   | Don't care   | 0x55AA     | Serial-Flash Password                   | Enabled   | Disabled   | Flash   |
|------|--------------|------------|-----------------------------------------|-----------|------------|---------|
|      |              | !0x55AA    | Serial-Public Password                  | Disabled  | Enabled    | Public  |
| 10   | !0x55AA      | Don't care | External-No Arbitration-Censored        | Disabled  | Enabled    | Public  |
|      | 0x55AA       |            | External-No Arbitration-Public          | Enabled   | Enabled    | Public  |
| 11   | !0x55AA      | Don't care | External-External Arbitration -Censored | Disabled  | Enabled    | Public  |
|      | 0x55AA       |            | External-External Arbitration -Public   | Enabled   | Enabled    | Public  |

Note: '!' = 'NOT', meaning any value other than the value specified. Values 0x0000 and 0xFFFF should not be used.

The censorship word is a 32-bit word of data stored in the shadow row of internal Flash memory. This memory location is read and interpreted by hardware as part of the boot process and is used in conjunction with  the  BOOTCFG  pins  to  enable/disable  the  internal  Flash  memory  and  the  Nexus  interface.  The memory address of the censorship word is 0x00FF\_FDE0. The censorship word consists of two fields: censorship control and serial boot control. The censorship word is programmed during manufacturing to be 0x55AA\_55AA. This results in a device that is not censored and uses a Flash-based password for serial boot mode.

## Censorship Word at 0x00FF\_FDE0

Figure 16-2. Censorship Word

<!-- image -->

The BAM program uses the state of the DISNEX bit to determine whether the serial password received in serial boot mode should be compared to a public password (fixed value of the 0xFEED\_FACE\_CAFE\_BEEF) or needs to be compared to a Flash password - 64 bits data, stored in the shadow row of internal Flash at address 0x00FF\_FDD8.

## Flash Password at 0x00FF\_FDD8

<!-- image -->

| 0                                                             | 1                                                             | 2                                                             | 3                                                             | 4                                                             | 5                                                             | 6                                                             | 7                                                             | 8                                                             | 9                                                             | 10                                                            | 11                                                            | 12                                                            | 13                                                            | 14                                                            | 15                                                            |
|---------------------------------------------------------------|---------------------------------------------------------------|---------------------------------------------------------------|---------------------------------------------------------------|---------------------------------------------------------------|---------------------------------------------------------------|---------------------------------------------------------------|---------------------------------------------------------------|---------------------------------------------------------------|---------------------------------------------------------------|---------------------------------------------------------------|---------------------------------------------------------------|---------------------------------------------------------------|---------------------------------------------------------------|---------------------------------------------------------------|---------------------------------------------------------------|
| 1                                                             | 1                                                             | 1                                                             | 1                                                             | 1                                                             | 1                                                             | 1                                                             | 0                                                             | 1                                                             | 1                                                             | 1                                                             | 0                                                             | 1                                                             | 0                                                             | 1                                                             | 0                                                             |
| Serial Boot Password (0x00FF_FDD8) - 0xFEED (Factory Default) | Serial Boot Password (0x00FF_FDD8) - 0xFEED (Factory Default) | Serial Boot Password (0x00FF_FDD8) - 0xFEED (Factory Default) | Serial Boot Password (0x00FF_FDD8) - 0xFEED (Factory Default) | Serial Boot Password (0x00FF_FDD8) - 0xFEED (Factory Default) | Serial Boot Password (0x00FF_FDD8) - 0xFEED (Factory Default) | Serial Boot Password (0x00FF_FDD8) - 0xFEED (Factory Default) | Serial Boot Password (0x00FF_FDD8) - 0xFEED (Factory Default) | Serial Boot Password (0x00FF_FDD8) - 0xFEED (Factory Default) | Serial Boot Password (0x00FF_FDD8) - 0xFEED (Factory Default) | Serial Boot Password (0x00FF_FDD8) - 0xFEED (Factory Default) | Serial Boot Password (0x00FF_FDD8) - 0xFEED (Factory Default) | Serial Boot Password (0x00FF_FDD8) - 0xFEED (Factory Default) | Serial Boot Password (0x00FF_FDD8) - 0xFEED (Factory Default) | Serial Boot Password (0x00FF_FDD8) - 0xFEED (Factory Default) | Serial Boot Password (0x00FF_FDD8) - 0xFEED (Factory Default) |
| 16                                                            | 17                                                            | 18                                                            | 19                                                            | 20                                                            | 21                                                            | 22                                                            | 23                                                            | 24                                                            | 25                                                            | 26                                                            | 27                                                            | 28                                                            | 29                                                            | 30                                                            | 31                                                            |
| 1                                                             | 1                                                             | 1                                                             | 1                                                             | 1                                                             | 0                                                             | 1                                                             | 0                                                             | 1                                                             | 1                                                             | 0                                                             | 0                                                             | 1                                                             | 1                                                             | 1                                                             | 0                                                             |
| Serial Boot Password (0x00FF_FDDA) - 0xFACE (Factory Default) | Serial Boot Password (0x00FF_FDDA) - 0xFACE (Factory Default) | Serial Boot Password (0x00FF_FDDA) - 0xFACE (Factory Default) | Serial Boot Password (0x00FF_FDDA) - 0xFACE (Factory Default) | Serial Boot Password (0x00FF_FDDA) - 0xFACE (Factory Default) | Serial Boot Password (0x00FF_FDDA) - 0xFACE (Factory Default) | Serial Boot Password (0x00FF_FDDA) - 0xFACE (Factory Default) | Serial Boot Password (0x00FF_FDDA) - 0xFACE (Factory Default) | Serial Boot Password (0x00FF_FDDA) - 0xFACE (Factory Default) | Serial Boot Password (0x00FF_FDDA) - 0xFACE (Factory Default) | Serial Boot Password (0x00FF_FDDA) - 0xFACE (Factory Default) | Serial Boot Password (0x00FF_FDDA) - 0xFACE (Factory Default) | Serial Boot Password (0x00FF_FDDA) - 0xFACE (Factory Default) | Serial Boot Password (0x00FF_FDDA) - 0xFACE (Factory Default) | Serial Boot Password (0x00FF_FDDA) - 0xFACE (Factory Default) | Serial Boot Password (0x00FF_FDDA) - 0xFACE (Factory Default) |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Figure 16-3. Serial Boot Flash Password

<!-- image -->

| 32                                                            | 33                                                            | 34                                                            | 35                                                            | 36                                                            | 37                                                            | 38                                                            | 39                                                            | 40                                                            | 41                                                            | 42                                                            | 43                                                            | 44                                                            | 45                                                            | 46                                                            | 47                                                            |
|---------------------------------------------------------------|---------------------------------------------------------------|---------------------------------------------------------------|---------------------------------------------------------------|---------------------------------------------------------------|---------------------------------------------------------------|---------------------------------------------------------------|---------------------------------------------------------------|---------------------------------------------------------------|---------------------------------------------------------------|---------------------------------------------------------------|---------------------------------------------------------------|---------------------------------------------------------------|---------------------------------------------------------------|---------------------------------------------------------------|---------------------------------------------------------------|
| 1                                                             | 1                                                             | 0                                                             | 0                                                             | 1                                                             | 0                                                             | 1                                                             | 0                                                             | 1                                                             | 1                                                             | 1                                                             | 1                                                             | 1                                                             | 1                                                             | 1                                                             | 0                                                             |
| Serial Boot Password (0x00FF_FDDC) - 0xCAFE (Factory Default) | Serial Boot Password (0x00FF_FDDC) - 0xCAFE (Factory Default) | Serial Boot Password (0x00FF_FDDC) - 0xCAFE (Factory Default) | Serial Boot Password (0x00FF_FDDC) - 0xCAFE (Factory Default) | Serial Boot Password (0x00FF_FDDC) - 0xCAFE (Factory Default) | Serial Boot Password (0x00FF_FDDC) - 0xCAFE (Factory Default) | Serial Boot Password (0x00FF_FDDC) - 0xCAFE (Factory Default) | Serial Boot Password (0x00FF_FDDC) - 0xCAFE (Factory Default) | Serial Boot Password (0x00FF_FDDC) - 0xCAFE (Factory Default) | Serial Boot Password (0x00FF_FDDC) - 0xCAFE (Factory Default) | Serial Boot Password (0x00FF_FDDC) - 0xCAFE (Factory Default) | Serial Boot Password (0x00FF_FDDC) - 0xCAFE (Factory Default) | Serial Boot Password (0x00FF_FDDC) - 0xCAFE (Factory Default) | Serial Boot Password (0x00FF_FDDC) - 0xCAFE (Factory Default) | Serial Boot Password (0x00FF_FDDC) - 0xCAFE (Factory Default) | Serial Boot Password (0x00FF_FDDC) - 0xCAFE (Factory Default) |
| 48                                                            | 49                                                            | 50                                                            | 51                                                            | 52                                                            | 53                                                            | 54                                                            | 55                                                            | 56                                                            | 57                                                            | 58                                                            | 59                                                            | 60                                                            | 61                                                            | 62                                                            | 63                                                            |
| 1                                                             | 0                                                             | 1                                                             | 1                                                             | 1                                                             | 1                                                             | 1                                                             | 0                                                             | 1                                                             | 1                                                             | 1                                                             | 0                                                             | 1                                                             | 1                                                             | 1                                                             | 1                                                             |
| Serial Boot Password (0x00FF_FDDE) - 0xBEEF (Factory Default) | Serial Boot Password (0x00FF_FDDE) - 0xBEEF (Factory Default) | Serial Boot Password (0x00FF_FDDE) - 0xBEEF (Factory Default) | Serial Boot Password (0x00FF_FDDE) - 0xBEEF (Factory Default) | Serial Boot Password (0x00FF_FDDE) - 0xBEEF (Factory Default) | Serial Boot Password (0x00FF_FDDE) - 0xBEEF (Factory Default) | Serial Boot Password (0x00FF_FDDE) - 0xBEEF (Factory Default) | Serial Boot Password (0x00FF_FDDE) - 0xBEEF (Factory Default) | Serial Boot Password (0x00FF_FDDE) - 0xBEEF (Factory Default) | Serial Boot Password (0x00FF_FDDE) - 0xBEEF (Factory Default) | Serial Boot Password (0x00FF_FDDE) - 0xBEEF (Factory Default) | Serial Boot Password (0x00FF_FDDE) - 0xBEEF (Factory Default) | Serial Boot Password (0x00FF_FDDE) - 0xBEEF (Factory Default) | Serial Boot Password (0x00FF_FDDE) - 0xBEEF (Factory Default) | Serial Boot Password (0x00FF_FDDE) - 0xBEEF (Factory Default) | Serial Boot Password (0x00FF_FDDE) - 0xBEEF (Factory Default) |

The BAM program continues to make specific initialization in one of the four boot modes.

## 16.3.2.1 Internal Boot Mode Flow

When the BAM software detects internal Flash boot mode, it sets up a bus error exception handler because it will be accessing Flash memory locations that may be corrupted and cause a bus error. Then the BAM program tries to find a valid RCHW in six predefined locations. If a valid RCHW is found, the BAM program enables the e200z6 watchdog timer with the RCHW[WTE] bit. If a valid RCHW is not found, the BAM program proceeds to the serial boot mode.

## 16.3.2.1.1 Finding Reset Configuration Half Word

The BAM searches the internal Flash memory for a valid reset configuration half word (RCHW). A valid RCHW is a 16-bit  value  that  contains  a  fixed  8-bit  boot  identifier  and  some  configuration  bits  (see Section 4.4.3.5.1, 'Reset Configuration Half Word Definition'). The RCHW is expected to be the first half word in one of the low address space Flash blocks as shown in Table 16-4.

Table 16-4. Low Address Space (LAS) Block Memory Addresses

|   Block | Address     |
|---------|-------------|
|       0 | 0x0000_0000 |
|       1 | 0x0000_4000 |
|       2 | 0x0001_0000 |
|       3 | 0x0001_C000 |
|       4 | 0x0002_0000 |
|       5 | 0x0003_0000 |

BOOT\_BLOCK\_ADDRESS is the first address from Table 16-4, where the BAM program finds a valid RCHW.

If the BAM program does find a valid RCHW, the watchdog is enabled with the RCHW[WTE] bit, the BAM program fetches the reset vector from the address of the BOOT\_BLOCK\_ADDRESS + 0x4, and branches to the reset boot vector. A user application should have a valid instruction at the reset boot vector address.

BOOT\_BLOCK\_ADDRESS + 0x0000\_0004

<!-- image -->

| 0   | 1   | 2   | 3   | 4   | 5   | 6   | 7   | 8   | 9   | 10   | 11   | 12   | 13   | 14   | 15   |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|------|------|------|------|------|------|
| A0  | A1  | A2  | A3  | A4  | A5  | A6  | A7  | A8  | A9  | A10  | A11  | A12  | A13  | A14  | A15  |
| 16  | 17  | 18  | 19  | 20  | 21  | 22  | 23  | 24  | 25  | 26   | 27   | 28   | 29   | 30   | 31   |
| A16 | A17 | A18 | A19 | A20 | A21 | A22 | A23 | A24 | A25 | A26  | A27  | A28  | A29  | A30  | A31  |

Figure 16-4. Reset Boot Vector

The watchdog timeout is set to 2.5 × 2 17 system clock periods if the watchdog is enabled.

## 16.3.2.2 External Boot Modes Flow.

The external boot mode is used to boot a user application from an external asynchronous memory that is connected to the MCU external bus; it is controlled by CS0.

## 16.3.2.2.1 External Boot MMU Configuration

As shown in Table 16-5 , the BAM program sets up the two MMU regions differently than in internal Flash boot mode. The internal Flash logical address space is mapped to the physical addresses of the EBI.

Table 16-5. MMU Configuration for an External Boot

|   TLB Entry | Region                | Logical Base Address   | Physical Base Address   | Size      | Attributes                                                                                  |
|-------------|-----------------------|------------------------|-------------------------|-----------|---------------------------------------------------------------------------------------------|
|           1 | Internal Flash Memory | 0x0000_0000            | 0x2000_0000             | 16 Mbytes | GLYPH<127> Cache enabled GLYPH<127> Not guarded GLYPH<127> Big Endian GLYPH<127> Global PID |
|           2 | EBI                   | 0x2000_0000            | 0x2000_0000             | 16 Mbytes | GLYPH<127> Cache enabled GLYPH<127> Not guarded GLYPH<127> Big Endian GLYPH<127> Global PID |

This allows a code, written to run from internal Flash memory, to be executed from the external memory.

## 16.3.2.2.2 Single Bus Master or Multiple Bus Masters

External boot mode has two options for booting:

- · External boot with no arbitration - This option is a single master system where the MCU is the only bus master in the system and therefore does not need to consider arbitration of the external bus.
- · External boot with external arbitration - This option is where there is another bus master on the external bus and arbitration of the bus is handled external to the MCU.

These two modes are selected based on the state of the two BOOTCFG pins.

In a multiple master system where both are booting from the same external bus memory, one boots in external boot with no arbitration mode while the other boots in external boot with external arbitration mode.

The configuration of the EBI is different for the two modes.

## 16.3.2.2.3 External Boot-Single Master with no Arbitration EBI Configuration

The BAM program configures:

- 1. Chip select CS0 region as a 16-bit port with a base address of 0x2000\_0000, no burst, 15 wait states, 8 Mbyte size.
- 2. EBI for no external master (clear EXTM bit).
- 3. Enables the EBI for normal operation.
- 4. Configures the following I/O pins as bus signals: address signals[8:31]; data[0:15]; WE0; OE; TS; CS0. Data[16:31] is also configured if RCHW[PS0] = 0. See for more information.

## 16.3.2.2.4 External Boot with External Arbitration EBI Configuration

In the external boot mode with external arbitration the BAM program also does the following:

- 1. Sets the EXTM bit, enabling the EBI for external master operation.
- 2. Configures EBI for external arbitration (sets the EARB bit).
- 3. Configures the additional I/O signals BB, BG, BR for bus function . See Table 16-6.

Table 16-6. External Bus Interface Configuration

| Pins             | Reset    | Serial Boot Mode 1 or Internal Boot Mode   | External Boot with no Arbitration 2 (Single Master Mode)   | External Boot with no Arbitration 2 (Single Master Mode)   | External Boot with External Arbitration 2 (Multi Master Mode)   | External Boot with External Arbitration 2 (Multi Master Mode)   |
|------------------|----------|--------------------------------------------|------------------------------------------------------------|------------------------------------------------------------|-----------------------------------------------------------------|-----------------------------------------------------------------|
| Pins             | Function | Function                                   | Function                                                   | PCR                                                        | Function                                                        | PCR                                                             |
| ADDR[8:31]       | GPIO     | GPIO                                       | ADDR[8:31]                                                 | 0x0440                                                     | ADDR[8:31]                                                      | 0X0440                                                          |
| DATA[16:31]      | GPIO     | GPIO                                       | GPIO 3                                                     | Default 3                                                  | GPIO 3                                                          | Default 3                                                       |
| DATA[0:15]       | GPIO     | GPIO                                       | DATA[0:15]                                                 | 0X0440                                                     | DATA[0:15]                                                      | 0X0440                                                          |
| BB               | GPIO     | GPIO                                       | GPIO                                                       | Default                                                    | BB                                                              | 0X0443                                                          |
| BG               | GPIO     | GPIO                                       | GPIO                                                       | Default                                                    | BG                                                              | 0X0443                                                          |
| BR               | GPIO     | GPIO                                       | GPIO                                                       | Default                                                    | BR                                                              | 0X0443                                                          |
| TSIZ[0:1]        | GPIO     | GPIO                                       | GPIO                                                       | Default                                                    | GPIO                                                            | Default                                                         |
| TEA              | GPIO     | GPIO                                       | GPIO                                                       | Default                                                    | GPIO                                                            | Default                                                         |
| CS0              | GPIO     | GPIO                                       | CS0                                                        | 0X0443                                                     | CS0                                                             | 0X0443                                                          |
| WE0_BE0          | GPIO     | GPIO                                       | WE0                                                        | 0X0443                                                     | WE0_BE0                                                         | 0X0443                                                          |
| OE               | GPIO     | GPIO                                       | OE                                                         | 0X0443                                                     | OE                                                              | 0X0443                                                          |
| TS               | GPIO     | GPIO                                       | TS                                                         | 0X0443                                                     | TS                                                              | 0X0443                                                          |
| TA               | GPIO     | GPIO                                       | GPIO                                                       | Default                                                    | GPIO                                                            | Default                                                         |
| RD_WR            | GPIO     | GPIO                                       | GPIO                                                       | Default                                                    | GPIO                                                            | Default                                                         |
| CS[1:3]          | GPIO     | GPIO                                       | GPIO                                                       | Default                                                    | GPIO                                                            | Default                                                         |
| BDIP             | GPIO     | GPIO                                       | GPIO                                                       | Default                                                    | GPIO                                                            | Default                                                         |
| WE[1:3]_ BE[1:3] | GPIO     | GPIO                                       | GPIO                                                       | Default                                                    | GPIO                                                            | Default                                                         |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

- 1 This column is for serial boot mode only when entered directly using the BOOTCFG signals (See note 2).
- 2 If serial boot is entered indirectly from either external boot mode because a valid RCHW was not found, the EBI remains configured according to these columns.
- 3 If the BAM reads a valid RCHW with the PS0 bit clear, data[16:31] are reconfigured from GPIO to data bus signals by writing 0x0440 to the PCRs.

## 16.3.2.2.5 Reset Configuration Half Word Read

The BAM program checks for a valid reset configuration half word (RCHW, see Figure 16-4) at the first location in external memory, i.e address 0x2000\_0000.

If the BAM program fails to find a valid RCHW, it assumes the external memory does not contain a user application and switches to serial boot mode.

If the BAM program does find a valid RCHW, it configures data pins and CS0 port size according to the RCHW[PS0] bit and the e200z6 core watchdog according to the RCHW[WTE] bit. The watchdog timeout is set to 2.5 × 2 17 system clock periods. Then the BAM program reads the reset vector (Figure 16-4) from the address 0x2000\_0004 and branches to that reset vector address, starting user program execution.

## 16.3.2.3 Serial Boot Mode Operation

In this mode of operation, the CAN\_A and the eSCI\_A GPIO signals are reconfigured, unused message buffers  in  CAN\_A  are  used  as  scratch  pad  RAM,  the  MMU  is  setup;  the  watchdog  is  enabled.  No exceptions are used.

## 16.3.2.3.1 Serial Boot Mode MMU and EBI Configuration

The BAM program sets up the MPC5553/MPC5554 MMU for all peripheral and memory regions in one of two different modes and sets up the EBI in one of three different modes; depending on how serial boot mode was entered.

If serial boot mode is entered directly by choosing the mode with the BOOTCFG signals, or was entered indirectly from internal boot mode because no valid RCHW was found, then the MMU is configured the same way as for internal boot mode. See Table 16-3 for more information. The EBI is disabled and all bus pins function as GPIO.

If serial boot mode  is entered indirectly from either external boot/single master or external boot/multimaster/external arbitration because no valid RCHW was found, then the MMU and EBI are configured the same way as for one of the external boot modes with a 16-bit data bus. See Table 16-5 for more information.

## 16.3.2.3.2 CAN and eSCI Configuration

In  serial  boot  mode,  the  BAM  program  configures  CAN\_A  and  eSCI\_A  to  receive  messages.  The CNRX\_A signal and the RXD\_A signals are configured as inputs to the CAN and eSCI modules. The CNTX\_A signal is configured as an output from the CAN module. The TXD\_A signal of the eSCI\_A remains configured as GPIO input. The BAM program writes the e200z6 core timebase registers (TB) to 0x0000\_0000\_0000\_0000 and enables the e200z6 core watchdog timer to use the system clock and to cause a reset after a time-out period of 3 x 2 28  system clock cycles. (See Table 16-7 for examples of time out periods.)

The CAN controller is configured to operate at a baud rate equal to the system clock frequency divided by 60 with one message buffer (MB) using the standard 11-bit identifier format detailed in the CAN 2.0A specification. If the PLL is enabled out of reset, the default system clock is 1.5 times the crystal frequency.

(See Chapter 11, 'Frequency Modulated Phase Locked Loop (FMPLL) and System Clocks,' for more information.) So with the PLL enabled, the baud rate is equal to the crystal frequency divided by 40. (See Table 16-7 for examples of baud rates)

The BAM ignores the following errors:

- · Bit1 errors
- · Bit0 errors
- · Acknowledge errors
- · Cyclic redundancy code errors
- · Form errors
- · Stuffing errors
- · TX error counter errors
- · Rx error counter errors

All data received is assumed to be good and is echoed out on the CNTX\_A signal.

## NOTE

It is the responsibility of the host computer to compare the 'echoes' with the sent data and restart the process if an error is detected.

See Figure 16-5 for details of CAN bit timing.

1 time Quanta = 5 system clock periods = 3 1/3 crystal clock periods (with PLL enabled)

<!-- image -->

Figure 16-5. CAN Bit Timing

The eSCI is configured for 1 start bit, 8 data bits, no parity and 1 stop bit and to operate at a baud rate equal to the system clock divided by 1250. See Table 16-7 for examples of baud rates.

The BAM ignores the following eSCI errors:

- · Overrun errors
- · Noise errors
- · Framing errors
- · Parity errors

All data received is assumed to be good and is echoed out on the TXD signal. It is the responsibility of the host computer to compare the echoes with the sent data and restart the process if an error is detected.

Table 16-7. Serial Boot Mode-Baud Rate and Watchdog Summary

| Crystal Frequency (MHz)   | System Clock Frequency (MHz)   | SCI Baud Rate (baud)   | CAN Baud Rate (baud)   | Watchdog Timeout period (seconds)   |
|---------------------------|--------------------------------|------------------------|------------------------|-------------------------------------|
| f xtal                    | f sys =1.5 * f xtal            | f sys / 1250           | f sys / 60             | 2.5 * 2 27 / f sys                  |
| 8                         | 12                             | 9600                   | 200K                   | 67.1                                |
| 12                        | 18                             | 14400                  | 300K                   | 44.7                                |
| 16                        | 24                             | 19200                  | 400K                   | 33.6                                |
| 20                        | 30                             | 24000                  | 500K                   | 26.8                                |

Upon reception of either a valid CAN message with an ID equal to 0x011 and containing 8 bytes of data or a valid eSCI message, the BAM moves to one of two serial boot submodes: either CAN serial boot mode or eSCI serial boot mode.

In  CAN serial boot mode, the eSCI\_A signal RXD\_A reverts to GPIO input. The ensuing download protocol is assumed to be all on the CAN bus; eSCI messages are ignored.

In eSCI serial boot mode, the CAN\_A signals CNRX\_A and CNTX\_A revert to GPIO inputs and the TXD\_A signal is configured as an output. The ensuing download protocol is assumed to be on the eSCI bus and CAN messages are ignored.

Table 16-8. CAN/eSCI Reset Configuration for CAN/eSCI Boot

| Pins   | Reset Function   | Initial Serial Boot Mode   | Serial Boot Mode after a valid CANmessagereceived   | Serial Boot Mode after a valid eSCI message received   |
|--------|------------------|----------------------------|-----------------------------------------------------|--------------------------------------------------------|
| CNTX_A | GPIO             | CNTX_A                     | CNTX_A                                              | GPIO                                                   |
| CNRX_A | GPIO             | CNRX_A                     | CNRX_A                                              | GPIO                                                   |
| TXD_A  | GPIO             | GPIO                       | GPIO                                                | TXD_A                                                  |
| RXD_A  | GPIO             | RXD_A                      | GPIO                                                | RXD_A                                                  |

## Table 16-9. CAN/eSCI Reset Pin Configuration

| Pins           | I/O    | Weak Pull-Up State   | Hysteresis   | Driver Configuration   | Slew Rate   | Input Buffer Enable   |
|----------------|--------|----------------------|--------------|------------------------|-------------|-----------------------|
| CNTX_A / TXD_A | Output | Enabled/Up           | -            | Push/Pull              | Medium      | N                     |
| CNRX_A / RXD_A | Input  | Enabled/Up           | Y            | -                      | -           | -                     |
| GPIO           | Input  | Enabled/Up           | Y            | -                      | -           | -                     |

## 16.3.2.3.3 CAN Serial Boot Mode Download Protocol

The download protocol follows 4 steps:

- 1. Download 64-bit password
- 2. Download start address and size of download

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

- 3. Download data
- 4. Execute code from start address

Each step must complete before the next step starts.

- 1. Download 64-bit password
- The host computer must send a CAN message with ID = 0x011 and containing the 64-bit serial download password. CAN messages with other IDs or fewer bytes of data are ignored. When a valid message has been received, the BAM transmits a CAN message using ID  = 0x001 and containing the data received. The host should not send a second CAN message until the echo of the first message has been received. A CAN message sent before the echo is received is ignored.

The received 64-bit password is checked for validity. It is checked to ensure that none of the 4 x 16-bit half words are 0x0000 or 0xFFFF. These are considered illegal passwords. A password must have at least one 0 and one 1 in each half word lane to be considered legal.

The BAM program then checks the censorship status of the MCU by checking the DISNEX bit in the SIU\_CCR. If Nexus is disabled, the MCU is considered to be censored and the password is compared with a password stored in the shadow row in internal Flash memory.

If Nexus is enabled, the MCU is considered to be not censored or booting from external Flash and the password is compared to the fixed value = 0xFEED\_FACE\_CAFE\_BEEF.

If the password fails any of these validity tests, the MCU stops responding to all stimulus. To repeat boot operation the MCU needs to be reset by external reset or by watchdog. If the password is valid, the BAM program refreshes the e200z6 watchdog timer and the next step in the protocol can be performed.

- 2. Download start address and size of download
- The host computer must send a CAN message with ID = 0x012 and containing a 32 bit address in internal SRAM, indicating where the following data should be stored in the memory map of the MCU; and a 32 bit number indicating how many bytes of data are to be received and stored in memory before switching to execute the code just loaded. The start address is assumed to be on a word boundary (4 bytes), therefore the least significant 2 bits of the address are ignored. CAN messages with other IDs or fewer bytes of data are ignored. When a valid message has been received, the BAM transmits a CAN message using ID = 0x002 and containing the data received. The host should not send a another CAN message until the echo of the previous message has been received by the host. A CAN message sent before the echo is received is ignored.

## 3. Download data

The host computer must send a succession of CAN messages with ID = 0x013 (The data length is variable) and containing raw binary data. Each byte of data received is stored in the MCU's memory, starting at the address specified in the previous protocol step and incrementing through memory until the number of bytes of data received and stored in memory matches the number specified in the previous protocol step. CAN messages with other IDs are ignored. When a valid message has been received, the BAM transmits a CAN message using ID = 0x003 and containing the data received. The host should not send another CAN message until the echo of the previous message has been received by the host. A CAN message sent before the echo is received is ignored.

## NOTE

Internal SRAM is protected by 64 bit wide error correction coding hardware (ECC). This means that any write to uninitialized internal SRAM must be 64 bits wide, otherwise an ECC error  occurs. Therefore the BAM buffers downloaded data until 8 bytes have been received then does a single 64 bit wide write. Only internal SRAM supports 64 bit writes therefore attempting to download data to other RAM apart from internal SRAM causes errors. If the start address of the downloaded data is not on an 8 byte boundary, the BAM writes  0x00  to  the  memory  locations  from  the  preceeding  8  byte boundary to the start address (maximum 4 bytes). The BAM also writes 0x00 to all memory locations from the last byte of data downloaded to the following 8 byte boundary (maximum 7 bytes)

## 4. Execute code

The BAM waits for the last CAN message transmission to complete. Then the CAN controller is disabled. CNTX\_A and CNRX\_A revert to GPIO inputs. Then the BAM switches execution to the downloaded code by branching to the first address in which code is stored, as specified in step 2 of the protocol.

## NOTE

The code that is downloaded and executed must periodically refresh the e200z6 watchdog timer or change the timeout period to a value that does not cause resets during normal operation.

Table 16-10. CAN Serial Boot Mode Download Protocol

|   Protocol Step | Host Sent Message                                            | MCU Response Message                                         | Action                                                                                                                                                                                                                       |
|-----------------|--------------------------------------------------------------|--------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|               1 | CAN ID 0x011 + 64-bit password                               | CAN ID 0x001 + 64-bit password                               | Password checked for validity and compared against stored password. e200z6 Watchdog timer is refreshed if the password check is successful                                                                                   |
|               2 | CAN ID 0x012 + 32-bit store address + 32-bit number of bytes | CAN ID 0x002 + 32-bit store address + 32-bit number of bytes | Load address and size of download are stored for future use                                                                                                                                                                  |
|               3 | CAN ID 0x013 + 8 to 64 bits of raw binary data               | CAN ID 0x003 + 8 to 64 bits of raw binary data               | Each byte of data received is store in MCU memory, starting at the address specified in the previous step and incrementing until the amount of data received and stored, matched the size as specified in the previous step. |
|               4 | None                                                         | None                                                         | The BAMprogram returns I/O pins and CANmodule to their reset state, then branches to the first address the data was stored to (As specified in step 2)                                                                       |

## 16.3.2.3.4 eSCI Serial Boot Mode Protocol

The download protocol follows four steps:

- 1. Download 64-bit password
- 2. Download start address and size of download
- 3. Download data
- 4. Execute code from start address

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## Boot Assist Module (BAM)

Each step must complete before the next step starts. The eSCI operates in half duplex mode where the host sends a byte of data, then waits for the echo back from the MCU before proceeding with the next byte. Bytes sent from the host before the previous echo from the MCU is received, are ignored.

- 1. Download 64-bit password

The first 8 bytes of eSCI data the host computer sends must contain the 64-bit serial download password. For each valid eSCI message received, the BAM transmits the same data on the eSCI\_A TXD\_A signal.

The received 64-bit password is checked for validity. It is checked to ensure that none of the 4 x 16-bit half words are 0x0000 or 0xFFFF, which are considered illegal passwords. A password must have at least one 0 and one 1 in each half word lane to be considered legal.

The BAM program then checks the censorship status of the MCU by checking the DISNEX bit in the SIU\_CCR. If Nexus is disabled, the MCU is considered to be censored and the password is compared with a password stored in the shadow row in internal Flash memory.

If Nexus is enabled, the MCU is considered to be not censored or is booting from external Flash and the password is compared to the fixed value of 0xFEED\_FACE\_CAFE\_BEEF.

If the password fails any of these validity tests, the MCU stops responding to all stimulus. To repeat the boot operation the only options are to assert the RESET signal or wait for watchdog reset the MCU. If the password is valid, the BAM refreshes the e200z6 watchdog timer and the next step in the protocol can be performed.

- 2. Download start address and size of download

The next 8 bytes of eSCI data the host computer sends must contain a 32-bit address in internal SRAM, indicating where the following data should be stored in the memory map of the MCU; and a 32-bit number indicating how many bytes of data are to be received and stored in memory before switching to execute the code just loaded. The start address is assumed to be on a word boundary (4 bytes), therefore the least significant 2 bits of the address are ignored. For each valid eSCI message received, the BAM transmits the same data on the eSCI\_A TXD\_A signal.

## 3. Download data

The host computer must then send a succession of eSCI messages, each containing raw binary data. Each byte of data received is stored in the MCU's memory, starting at the address specified in the previous protocol step and incrementing through memory until the number of bytes of data received and stored in memory matches the number specified in the previous protocol step. For each valid eSCI message received, the BAM transmits the same data on the eSCI\_A TXD\_A signal.

## NOTE

Internal SRAM is protected by 64 bit wide error correction coding hardware (ECC). This means that any write to uninitialized internal SRAM must be 64 bits wide, otherwise an ECC error  occurs. Therefore the BAM buffers downloaded data until 8 bytes have been received then does a single 64 bit wide write. Only internal SRAM supports 64 bit writes therefore attempting to download data to other RAM apart from internal SRAM causes errors. If the start address of the downloaded data is not on an 8 byte boundary, the BAM writes  0x00  to  the  memory  locations  from  the  preceeding  8  byte boundary to the start address (maximum 4 bytes). The BAM also writes 0x00 to all memory locations from the last byte of data downloaded to the following 8 byte boundary (maximum 7 bytes).

- 4. Execute code

The BAM waits for the last eSCI message transmission to complete and then the eSCI is disabled. TXD\_A and RXD\_A revert to general-purpose inputs. The BAM switches execution to the downloaded code by branching to the first address in which code was stored, as specified in step 2 of the protocol.

## NOTE

The code that is downloaded and executed must periodically refresh the e200z6 watchdog timer or change the timeout period to a value that does not cause resets during normal operation.

Table 16-11. eSCI Serial Boot Mode Download Protocol

|   Protocol Step | Host Sent Message                                       | BAM Response Message                          | Action                                                                                                                                                                                                                             |
|-----------------|---------------------------------------------------------|-----------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|               1 | 64-bit password MSB first                               | 64-bit password                               | Password checked for validity and compared against stored password. e200z6 watchdog timer is refreshed if the password check is successful                                                                                         |
|               2 | 32-bit store address + 32-bit number of bytes MSB first | 32-bit store address + 32-bit number of bytes | Load address and size of download are stored for future use                                                                                                                                                                        |
|               3 | 8 bits of raw binary data                               | 8 bits of raw binary data                     | Each byte of data received is store in MCUmemory, starting at the address specified in the previous step and incrementing until the amount of data received and stored, matched the size as specified in the previous step.        |
|               4 | None                                                    | None                                          | The BAM returns I/O pins and the eSCI module to their reset state, with the exception that ESCI_A_CR2[MDIS] is asserted rather than negated. Then it branches to the first address the data was stored to (as specified in step 2) |

## 16.3.3 Interrupts

No interrupts are generated by or are enabled by the BAM.

## 16.4 Revision History

## Substantive Changes since Rev 3.0

- GLYPH&lt;127&gt; Section 16.3.2.1.1, 'Finding Reset Configuration Half Word,' changed 2 18  to be 2.5 × 2 17
- GLYPH&lt;127&gt; Section 16.3.2.2.5, 'Reset Configuration Half Word Read,' changed 2 18  to be 2.5 × 2 17
- GLYPH&lt;127&gt; Table 16-7 changed 3* 2 28 / f sys  to be 2.5 * 2 27 / f sys
