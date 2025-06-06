### Chatper 17 Enhanced Modular Input/Output Subsystem (eMIOS)

## 17.1 Introduction

This chapter describes the enhanced modular input/output subsystem (eMIOS) of the MPC5553/MPC5554, which provides functionality to generate or measure timed events.

## 17.1.1 Block Diagram

Figure 17-1 shows the block diagram of the eMIOS.

<!-- image -->

Note 1: Connection between UC[n-1] and UC n necessary to implement QDEC mode.

Note 2: On channels 12-15, there is no input from EMIOS[12:15], but only from the DSPI module.

Figure 17-1. eMIOS Block Diagram

## 17.1.2 Overview

The eMIOS builds on the MIOS concept by using a unified channel module that provides a superset of the functionality of all the individual MIOS channels, while providing a consistent user interface. This allows more flexibility as each unified channel can be programmed for different functions.

## 17.1.3 Features

- · 24 unified channels
- · Unified channels features
- - 24-bit registers for captured/match values
- - 24-bit internal counter
- - Internal prescaler
- - Dedicated output pin for buffer direction control
- - Selectable time base
- - Can generate its own time base
- · Four 24-bit wide counter buses
- - Counter bus A can be driven by unified channel 23 or by the STAC bus.
- - Counter bus B, C, and D are driven by unified channels 0, 8, and 16, respectively.
- - Counter bus A can be shared among all unified channels. UCs 0 to 7, 8 to 15, and 16 to 23 can share counter buses B, C, and D, respectively.
- · One global prescaler
- · Shared time bases through the counter buses
- · Synchronization among internal and external time bases
- · Shadow FLAG register
- · State of module can be frozen for debug purposes
- · DMA request capability for some channels
- · Motor control capability

## 17.1.4 Modes of Operation

## 17.1.4.1 eMIOS Modes

The eMIOS operates in one of the modes described below:

- · User mode
- This is the normal operating mode. When EMIOS\_MCR[FRZ] = 0, and  EMIOS\_CCR[FREN] = 0, the eMIOS is in user mode.
- · Debug mode
- Debug mode is individually programmed for each channel. When entering this mode, the UC registers' contents are frozen, but remain available for read and write access through the slave interface. After leaving debug mode, all counters that were frozen upon debug mode entry will resume at the point where they were frozen.
- In debug mode, all clocks are running and all registers are accessible; thus, this mode is not intended for power saving, but for use during software debugging.

Enhanced Modular Input/Output Subsystem (eMIOS)

- · Freeze mode

Freeze mode enables the eMIOS to freeze the registers of the unified channels when debug mode is requested at the MCU level. While in freeze mode, the eMIOS continues to operate to allow the MCU access to the unified channels' registers. The unified channel will remain frozen until the EMIOS\_MCR[FRZ] bit is written to zero, the MCU exits debug mode, or a unified channel's EMIOS\_CCR[FREN] bit is cleared.

## 17.1.4.2 Unified Channel Modes

The unified channels can be configured to operate in the following modes:

Table 17-1. Unified Channel Modes

| Mode                                                                            | MPC5554   | MPC5553   |
|---------------------------------------------------------------------------------|-----------|-----------|
| General purpose input/output                                                    | Yes       | Yes       |
| Single action input capture                                                     | Yes       | Yes       |
| Single action output compare                                                    | Yes       | Yes       |
| Input pulse width measurement                                                   | Yes       | Yes       |
| Input period measurement                                                        | Yes       | Yes       |
| Double action output compare                                                    | Yes       | Yes       |
| Pulse/edge accumulation                                                         | Yes       | Yes       |
| Pulse/edge counting                                                             | Yes       | Yes       |
| Quadrature decode                                                               | Yes       | Yes       |
| Windowed programmable time accumulation                                         | Yes       | Yes       |
| Modulus counter, normal                                                         | Yes       | Yes       |
| Modulus counter, buffered                                                       | No        | Yes       |
| Output pulse width and frequency modulation, normal                             | Yes       | Yes       |
| Output pulse width and frequency modulation, buffered                           | No        | Yes       |
| Center aligned output pulse width modulation with dead time insertion, normal   | Yes       | Yes       |
| Center aligned output pulse width modulation with dead time insertion, buffered | No        | Yes       |
| Output pulse width modulation, normal                                           | Yes       | Yes       |
| Output pulse width modulation, buffered                                         | No        | Yes       |

These modes are described in Section 17.4, 'Functional Description.'

## 17.2 External Signal Description

## 17.2.1 Overview

Each unified channel has one input and one output signal connected to the channel's I/O pin. Refer to the SIU, eTPU, and DSPI sections for details about the connection to pads and other modules.

## NOTE

On  channels  12-15,  input  can  be  from  DSPI,  but  cannot  be  from eMIOS[12:15]  because  these  are  not  pinned  out.  See  Figure 2-8  and Figure 2-9).

The internal output disable input signals 0-3 (refer to Table 17-3) are provided to implement the output disable feature needed for motor control. They are connected to EMIOS\_Flag\_Out signals according to Section 17.2.1.2, 'Output Disable Input-eMIOS Output Disable Input Signals.'

## 17.2.1.1 External Signals

When configured as an input, EMIOS n is synchronized and filtered by the programmable input filter (PIF). The output of the PIF is then used by the channel logic and is available to be read by the MCU through the UCIN bit of the EMIOS\_CSR .  When configured as an output, EMIOS n n is a registered output and is available for reading by the MCU through the UCOUT bit of the EMIOS\_CSR n .

Table 17-2. External Signals

| Signal             | Direction   | Function                       | Reset State   |
|--------------------|-------------|--------------------------------|---------------|
| EMIOS[0:11, 16:23] | Input       | eMIOS Unified Channel n input  | -             |
| EMIOS[12:15]       | Input       | From DSPI                      | -             |
| EMIOS[0:23]        | Output      | eMIOS Unified Channel n output | 0 / Hi-Z 1    |

1 A value of 0 refers to the reset value of the signal. Hi-Z refers to the state of the external pin if a tri-state output buffer is controlled by the corresponding eMIOS signal.

## 17.2.1.2 Output Disable Input-eMIOS Output Disable Input Signals

Output disable inputs to both the eMIOS and the eTPU modules are connected to EMIOS\_Flag\_Out n signals according to Table 17-3.

Table 17-3.  eMIOS Output Disable Input Signals

| eMIOS Channel 1   | eMIOS Output Disable Input Signal 2   | eTPU Output Disable Input Signal 3   |
|-------------------|---------------------------------------|--------------------------------------|
| EMIOS_Flag_Out8   | output disable input 3                | ETPUA_ODI3                           |
| EMIOS_Flag_Out9   | output disable input 2                | ETPUA_ODI2                           |
| EMIOS_Flag_Out10  | output disable input 1                | ETPUA_ODI1                           |
| EMIOS_Flag_Out11  | output disable input 0                | ETPUA_ODI0                           |
| EMIOS_Flag_Out20  | -                                     | ETPUB_ODI0                           |
| EMIOS_Flag_Out21  | -                                     | ETPUB_ODI1                           |
| EMIOS_Flag_Out22  | -                                     | ETPUB_ODI2                           |
| EMIOS_Flag_Out23  | -                                     | ETPUB_ODI3                           |

- 1 All other EMIOS\_Flag\_Out n output signals are not connected.
- 2 Each of the four internal eMIOS output disable input signals can be programmed to disable the output of any eMIOS channel if that channel has selected output disable capability by the setting of its EMIOS\_CCR n [ODIS] bit, and by specifying the output disable input in its EMIOS\_CCRn[ODISSL] field.
- 3 ETPU \_ODI  input signals disable outputs for eTPU engine x y x , channels ( y *8) through ( y *8+7). Refer to the ETPU chapter for more details.

## 17.3 Memory Map/Register Definition

Addresses of unified channel (UC) registers are specified  as  offsets  from  the  channel's  base  address, otherwise the eMIOS base address is used as reference.

The overall address map organization is shown in Table 17-4. Table 17-5 describes the unified channel registers. All registers are cleared on reset.

Table 17-4. eMIOS Memory Map

| Address                    | Register Name   | Register Description           | Size (bits)   |
|----------------------------|-----------------|--------------------------------|---------------|
| Base (0xC3FA_0000)         | EMIOS_MCR       | Module Configuration Register  | 32            |
| Base + 0x004               | EMIOS_GFR       | Global Flag Register           | 32            |
| Base + 0x008               | EMIOS_OUDR      | Output Update Disable Register | 32            |
| Base + 0x00C- Base + 0x01F | -               | Reserved                       | -             |
| Base + 0x020               | UC0             | Unified Channel 0 Registers    | 256           |
| Base + 0x040               | UC1             | Unified Channel 1 Registers    | 256           |
| Base + 0x060               | UC2             | Unified Channel 2 Registers    | 256           |
| Base + 0x080               | UC3             | Unified Channel 3 Registers    | 256           |
| Base + 0x0A0               | UC4             | Unified Channel 4 Registers    | 256           |
| Base + 0x0C0               | UC5             | Unified Channel 5 Registers    | 256           |
| Base + 0x0E0               | UC6             | Unified Channel 6 Registers    | 256           |
| Base + 0x100               | UC7             | Unified Channel 7 Registers    | 256           |
| Base + 0x120               | UC8             | Unified Channel 8 Registers    | 256           |
| Base + 0x140               | UC9             | Unified Channel 9 Registers    | 256           |
| Base + 0x160               | UC10            | Unified Channel 10 Registers   | 256           |
| Base + 0x180               | UC11            | Unified Channel 11 Registers   | 256           |
| Base + 0x1A0               | UC12            | Unified Channel 12 Registers   | 256           |
| Base + 0x1C0               | UC13            | Unified Channel 13 Registers   | 256           |
| Base + 0x1E0               | UC14            | Unified Channel 14 Registers   | 256           |
| Base + 0x200               | UC15            | Unified Channel 15 Registers   | 256           |
| Base + 0x220               | UC16            | Unified Channel 16 Registers   | 256           |
| Base + 0x240               | UC17            | Unified Channel 17 Registers   | 256           |
| Base + 0x260               | UC18            | Unified Channel 18 Registers   | 256           |
| Base + 0x280               | UC19            | Unified Channel 19 Registers   | 256           |
| Base + 0x2A0               | UC20            | Unified Channel 20 Registers   | 256           |
| Base + 0x2C0               | UC21            | Unified Channel 21 Registers   | 256           |

## Table 17-4. eMIOS Memory Map (continued)

| Address      | Register Name   | Register Description         |   Size (bits) |
|--------------|-----------------|------------------------------|---------------|
| Base + 0x2E0 | UC22            | Unified Channel 22 Registers |           256 |
| Base + 0x300 | UC23            | Unified Channel 23 Registers |           256 |

## Table 17-5. UC Memory Map

| Address                            | Register Name   | Register Description     | Size (bits)   |
|------------------------------------|-----------------|--------------------------|---------------|
| UC n Base + 0x00                   | EMIOS_CADR n    | Channel A Data Register  | 32            |
| UC n Base + 0x04                   | EMIOS_CBDR n    | Channel B Data Register  | 32            |
| UC n Base + 0x08                   | EMIOS_CCNTR n   | Channel Counter Register | 32            |
| UC n Base + 0x0C                   | EMIOS_CCR n     | Channel Control Register | 32            |
| UC n Base + 0x10                   | EMIOS_CSR n     | Channel Status Register  | 32            |
| UC n Base + 0x14- UC n Base + 0x1F | -               | Reserved                 | -             |

## 17.3.1 Register Description

All registers are 32-bit wide. This section illustrates the eMIOS with 24 unified channels supporting 24-bit wide data.

## 17.3.1.1 eMIOS Module Configuration Register (EMIOS\_MCR)

EMIOS\_MCR contains global control bits for the eMIOS module.

Figure 17-2. eMIOS Module Configuration Register (EMIOS\_MCR)

<!-- image -->

|          | 0           | 1           | 2           | 3           | 4           | 5           | 6           | 7           | 8           | 9           | 10          | 11          | 12          | 13          | 14          | 15          |
|----------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|
| R        | 0           | MDIS        | FRZ         | GTBE        | ETB         | GPREN       | 0           | 0           | 0           | 0           | 0           | 0           | SRV         | SRV         | SRV         | SRV         |
| W        |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |
| Reset    | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           |
| Reg Addr | Base + 0x00 | Base + 0x00 | Base + 0x00 | Base + 0x00 | Base + 0x00 | Base + 0x00 | Base + 0x00 | Base + 0x00 | Base + 0x00 | Base + 0x00 | Base + 0x00 | Base + 0x00 | Base + 0x00 | Base + 0x00 | Base + 0x00 | Base + 0x00 |
|          | 16          | 17          | 18          | 19          | 20          | 21          | 22          | 23          | 24          | 25          | 26          | 27          | 28          | 29          | 30          | 31          |
| R        |             |             |             |             | GPRE        |             |             |             | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           |
| W        |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |
| Reset    | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           |
| Reg Addr | Base + 0x00 | Base + 0x00 | Base + 0x00 | Base + 0x00 | Base + 0x00 | Base + 0x00 | Base + 0x00 | Base + 0x00 | Base + 0x00 | Base + 0x00 | Base + 0x00 | Base + 0x00 | Base + 0x00 | Base + 0x00 | Base + 0x00 | Base + 0x00 |

Table 17-6. EMIOS\_MCR Field Descriptions

| Bits   | Name       | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
|--------|------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0      | -          | Reserved. This bit is readable/writable, but has no effect.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| 1      | MDIS       | Module disable. Puts the eMIOS in low power mode. The MDIS bit is used to stop the clock of the module, except the access to registers EMIOS_MCR and EMIOS_OUDR. 0 Clock is running 1 Enter low power mode                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 2      | FRZ        | Freeze. Enables the eMIOS to freeze the registers of the unified channels when debug mode is requested at MCU level. Each unified channel should have FREN bit set in order to enter freeze mode. While in freeze mode, the eMIOS continues to operate to allow the MCU access to the unified channels registers. The unified channel will remain frozen until the FRZ bit is written to zero or the MCU exits debug mode or the unified channel FREN bit is cleared. 0 Allows unified channels to continue to operate when device enters debug mode and the EMIOS_CCR n [FREN] bit is set 1 Stops unified channels operation when in debug mode and the EMIOS_CCR n [FREN] bit is set |
| 3      | GTBE 1     | Global time base enable. Used to export a global time base enable from the module and provide a method to start time bases of several modules simultaneously. 0 Global time base enable out signal negated 1 Global time base enable out signal asserted Note: The global time base enable input signal controls the internal counters. When asserted, internal counters are enabled. When negated, internal counters disabled.                                                                                                                                                                                                                                                        |
| 4      | ETB        | External time base. Selects the time base source that drives counter bus[A]. 0 Unified channel 23 drives counter bus[A] 1 STAC drives counter bus[A] Note: If ETB is set to select STAC as the counter bus[A] source, the GTBE must be set to enable the STAC to counter bus[A]. See Section 17.4.2, 'STAC Client Submodule' and the shared time and angle clock (STAC) bus interface section and the STAC bus configuration register (ETPU_REDCR) section of the eTPU chapter for more information about the STAC.                                                                                                                                                                    |
| 5      | GPREN      | Global prescaler enable. Enables the prescaler counter. 0 Prescaler disabled (no clock) and prescaler counter is cleared 1 Prescaler enabled                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| 6-11   | -          | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| 12-15  | SRV [0:3]  | Server time slot. Selects the address of a specific STAC server to which the STAC client submodule is assigned (refer to Section 17.4.2, 'STAC Client Submodule,' for details) 0000 - eTPU engine A, TCR1 0001 - eTPU engine B, TCR1 0010 - eTPU engine A, TCR2 0011 - eTPU engine B, TCR2 0100-1111 reserved                                                                                                                                                                                                                                                                                                                                                                          |
| 16-23  | GPRE [0:7] | Global prescaler. Selects the clock divider value for the global prescaler, as shown in Table 17-7.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| 24-31  | -          | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |

1 The GTBE signal is an inter-module signal, not an external pin on the device.

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 17-7. Global Prescaler Clock Divider

| GPRE[0:7]   | Divide Ratio   |
|-------------|----------------|
| 00000000    | 1              |
| 00000001    | 2              |
| .           | .              |
| .           | .              |
| .           | .              |
| .           | .              |
| 11111111    | 256            |

## 17.3.1.2 eMIOS Global Flag Register (EMIOS\_GFR)

The EMIOS\_GFR is a read-only register that groups the FLAG bits from all channels. This organization improves interrupt handling on simpler devices. These bits are mirrors of the FLAG bits of each channel register (EMIOS\_CSR) and flag bits in those channel registers cannot be cleared by accessing this 'mirror' register.

Figure 17-3. eMIOS Global Flag Register (EMIOS\_GFR)

<!-- image -->

|          | 0           | 1           | 2           | 3           | 4           | 5           | 6           | 7           | 8           | 9           | 10          | 11          | 12          | 13          | 14          | 15          |
|----------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|
| R        | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | F23         | F22         | F21         | F20         | F19         | F18         | F17         | F16         |
| W        |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |
| Reset    | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           |
| Reg Addr | Base + 0x04 | Base + 0x04 | Base + 0x04 | Base + 0x04 | Base + 0x04 | Base + 0x04 | Base + 0x04 | Base + 0x04 | Base + 0x04 | Base + 0x04 | Base + 0x04 | Base + 0x04 | Base + 0x04 | Base + 0x04 | Base + 0x04 | Base + 0x04 |
|          | 16          | 17          | 18          | 19          | 20          | 21          | 22          | 23          | 24          | 25          | 26          | 27          | 28          | 29          | 30          | 31          |
| R        | F15         | F14         | F13         | F12         | F11         | F10         | F9          | F8          | F7          | F6          | F5          | F4          | F3          | F2          | F1          | F0          |
| W        |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |
| Reset    | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           |
| Reg Addr | Base + 0x04 | Base + 0x04 | Base + 0x04 | Base + 0x04 | Base + 0x04 | Base + 0x04 | Base + 0x04 | Base + 0x04 | Base + 0x04 | Base + 0x04 | Base + 0x04 | Base + 0x04 | Base + 0x04 | Base + 0x04 | Base + 0x04 | Base + 0x04 |

## 17.3.1.3 eMIOS Output Update Disable Register (EMIOS\_OUDR)

The EMIOS\_OUDR serves to disable transfers from the A2 to the A1 channel registers and from the B2 to  the  B1  channel  registers  when  values  are  written  to  these  registers,  and  the  channel  is  running  in modulus counter (MC) mode or an output mode.

Figure 17-4. eMIOS Output Update Disable Register (EMIOS\_OUDR)

<!-- image -->

Table 17-8. EMIOS\_OUDR Field Descriptions

| Bits   | Name   | Description                                                                                                                                                                                                                                                                                                                                                                                                               |
|--------|--------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-7    | -      | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                 |
| 8-31   | OU n   | Channel n output update disable. When running in MC mode or an output mode, values are written to registers A2 and B2. OU n bits are used to disable transfers from registers A2 to A1 and B2 to B1. Each bit controls one channel. 0 Transfer enabled. Depending on the operating mode, transfer may occur immediately or in the next period. Unless stated otherwise, transfer occurs immediately. 1 Transfers disabled |

## 17.3.1.4 eMIOS Channel A Data Register (EMIOS\_CADR n )

Depending on the mode of operation, internal registers A1 or A2, used for matches and captures, can be assigned to address EMIOS\_CADR n . Both A1 and A2 are cleared by reset. Table 17-9 summarizes the EMIOS\_CADR  writing and reading accesses for all operating modes. For more information see section n Section 17.4.4.4, 'Modes of Operation of the Unified Channels.'

Figure 17-5. eMIOS Channel A Data Register (EMIOS\_CADR n )

<!-- image -->

|          | 0                | 1                | 2                | 3                | 4                | 5                | 6                | 7                | 8                | 9                | 10               | 11               | 12               | 13               | 14               | 15               |
|----------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|
| R        | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                |                  |                  |                  | A                |                  |                  |                  |                  |
| W        |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |
| Reset    | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                |
| Reg Addr | UC n Base + 0x00 | UC n Base + 0x00 | UC n Base + 0x00 | UC n Base + 0x00 | UC n Base + 0x00 | UC n Base + 0x00 | UC n Base + 0x00 | UC n Base + 0x00 | UC n Base + 0x00 | UC n Base + 0x00 | UC n Base + 0x00 | UC n Base + 0x00 | UC n Base + 0x00 | UC n Base + 0x00 | UC n Base + 0x00 | UC n Base + 0x00 |
|          | 16               | 17               | 18               | 19               | 20               | 21               | 22               | 23               | 24               | 25               | 26               | 27               | 28               | 29               | 30               | 31               |
| R        | A                | A                | A                | A                | A                | A                | A                | A                | A                | A                | A                | A                | A                | A                | A                | A                |
| W        |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |
| Reset    | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                |
| Reg Addr | UC n Base + 0x00 | UC n Base + 0x00 | UC n Base + 0x00 | UC n Base + 0x00 | UC n Base + 0x00 | UC n Base + 0x00 | UC n Base + 0x00 | UC n Base + 0x00 | UC n Base + 0x00 | UC n Base + 0x00 | UC n Base + 0x00 | UC n Base + 0x00 | UC n Base + 0x00 | UC n Base + 0x00 | UC n Base + 0x00 | UC n Base + 0x00 |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## 17.3.1.5 eMIOS Channel B Data Register (EMIOS\_CBDR n )

Depending  on  the  mode  of  operation,  internal  registers  B1  or  B2  can  be  assigned  to  address EMIOS\_CBDR . Both B1 and B2 are cleared by reset. Table 17-9  summarizes  the  EMIOS\_CBDR n n writing and reading accesses for all operating modes. For more information see section Section 17.4.4.4, 'Modes of Operation of the Unified Channels.'

## NOTE

The EMIOS\_CBDR   must n not be read speculatively. For future compatibility,  the  TLB  entry  covering  the  EMIOS\_CBDR n must  be configured to be guarded.

Figure 17-6. eMIOS Channel B  Data Register (EMIOS\_CBDR n )

<!-- image -->

|          | 0                | 1                | 2                | 3                | 4                | 5                | 6                | 7                | 8                | 9                | 10               | 11               | 12               | 13               | 14               | 15               |
|----------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|
| R        | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                |                  |                  |                  | B                |                  |                  |                  |                  |
| W        |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |
| Reset    | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                |
| Reg Addr | UC n Base + 0x04 | UC n Base + 0x04 | UC n Base + 0x04 | UC n Base + 0x04 | UC n Base + 0x04 | UC n Base + 0x04 | UC n Base + 0x04 | UC n Base + 0x04 | UC n Base + 0x04 | UC n Base + 0x04 | UC n Base + 0x04 | UC n Base + 0x04 | UC n Base + 0x04 | UC n Base + 0x04 | UC n Base + 0x04 | UC n Base + 0x04 |
|          | 16               | 17               | 18               | 19               | 20               | 21               | 22               | 23               | 24               | 25               | 26               | 27               | 28               | 29               | 30               | 31               |
| R        | B                | B                | B                | B                | B                | B                | B                | B                | B                | B                | B                | B                | B                | B                | B                | B                |
| W        |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |
| Reset    | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                |
| Reg Addr | UC n Base + 0x04 | UC n Base + 0x04 | UC n Base + 0x04 | UC n Base + 0x04 | UC n Base + 0x04 | UC n Base + 0x04 | UC n Base + 0x04 | UC n Base + 0x04 | UC n Base + 0x04 | UC n Base + 0x04 | UC n Base + 0x04 | UC n Base + 0x04 | UC n Base + 0x04 | UC n Base + 0x04 | UC n Base + 0x04 | UC n Base + 0x04 |

Table 17-9. EMIOS\_CADR n and EMIOS\_CBDR n Value Assignments

| Operating Mode   | Register Access   | Register Access   | Register Access   | Register Access   |
|------------------|-------------------|-------------------|-------------------|-------------------|
| Operating Mode   | Write             | Read              | Write             | Read              |
| GPIO             | A1, A2            | A1                | B1,B2             | B1                |
| SAIC 1           | -                 | A2                | B2                | B2                |
| SAOC 1           | A2                | A1                | B2                | B2                |
| IPWM             | -                 | A2                | -                 | B1                |
| IPM              | -                 | A2                | -                 | B1                |
| DAOC             | A2                | A1                | B2                | B1                |
| PEA              | A1                | A2                | -                 | B1                |
| PEC 1            | A1                | A1                | B1                | B1                |
| QDEC 1           | A1                | A1                | B2                | B2                |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 17-9. EMIOS\_CADR n and EMIOS\_CBDR n Value Assignments (continued)

| WPTA             | A1   | A1   | B1   | B1   |
|------------------|------|------|------|------|
| MC - Normal 1    | A2   | A1   | B2   | B2   |
| MC - Buffered    | A2   | A1   | B2   | B2   |
| OPWFM - Normal   | A2   | A1   | B2   | B1   |
| OPWFM - Buffered | A2   | A1   | B2   | B1   |
| OPWMC - Normal   | A2   | A1   | B2   | B1   |
| OPWMC - Buffered | A2   | A1   | B2   | B1   |
| OPWM - Normal    | A2   | A1   | B2   | B1   |
| OPWM - Buffered  | A2   | A1   | B2   | B1   |

1 In these modes, the register EMIOS\_CBDR n is not used, but B2 can be accessed.

## 17.3.1.6 eMIOS Channel Counter Register (EMIOS\_CCNTR n )

The EMIOS\_CCNTR  contains the value of the internal counter. When GPIO mode is selected or the n channel is frozen, the EMIOS\_CCNTR   is  readable  and  writable.  For  all  others  modes,  the n EMIOS\_CCNTR   is  a  read-only  register.  When  entering  some  operating  modes,  this  register  is n automatically cleared (refer to section Section 17.4.4.4, 'Modes of Operation of the Unified Channels,' for details).

<!-- image -->

|          | 0                | 1                | 2                | 3                | 4                | 5                | 6                | 7                | 8                | 9                | 10               | 11               | 12               | 13               | 14               | 15               |
|----------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|
| R        | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                |                  |                  |                  | C                |                  |                  |                  |                  |
| W 1      |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |
| Reset    | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                |
| Reg Addr | UC n Base + 0x08 | UC n Base + 0x08 | UC n Base + 0x08 | UC n Base + 0x08 | UC n Base + 0x08 | UC n Base + 0x08 | UC n Base + 0x08 | UC n Base + 0x08 | UC n Base + 0x08 | UC n Base + 0x08 | UC n Base + 0x08 | UC n Base + 0x08 | UC n Base + 0x08 | UC n Base + 0x08 | UC n Base + 0x08 | UC n Base + 0x08 |
|          | 16               | 17               | 18               | 19               | 20               | 21               | 22               | 23               | 24               | 25               | 26               | 27               | 28               | 29               | 30               | 31               |
| R        | C                | C                | C                | C                | C                | C                | C                | C                | C                | C                | C                | C                | C                | C                | C                | C                |
| W 1      |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |
| Reset    | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                |
| Reg Addr | UC n Base + 0x08 | UC n Base + 0x08 | UC n Base + 0x08 | UC n Base + 0x08 | UC n Base + 0x08 | UC n Base + 0x08 | UC n Base + 0x08 | UC n Base + 0x08 | UC n Base + 0x08 | UC n Base + 0x08 | UC n Base + 0x08 | UC n Base + 0x08 | UC n Base + 0x08 | UC n Base + 0x08 | UC n Base + 0x08 | UC n Base + 0x08 |

1 In GPIO mode or freeze action, this register is writable.

Figure 17-7. eMIOS Channel Counter Register (EMIOS\_CCNTR n )

## 17.3.1.7 eMIOS Channel Control Register (EMIOS\_CCR n )

The eMIOS\_CCR n enables the setting of several control parameters for a unified channel.  Among these controls  are  the  setting  of  a  channel  prescaler,  channel  mode  selection,  input  trigger  sensitivity  and filtering, interrupt and DMA request enabling, and output mode control.

Figure 17-8. eMIOS Channel Control Register (EMIOS\_CCR n )

<!-- image -->

|          | 0                | 1                | 2                | 3                | 4                | 5                | 6                | 7                | 8                | 9                | 10               | 11               | 12               |                  | 13 14            | 15               |
|----------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|
| R        | FREN             | ODIS             | ODISSL           | ODISSL           | UCPRE            | UCPRE            | UCPREN           | DMA              | 0                |                  | IF               | IF               |                  | FCK              | FEN              | 0                |
| W        |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |
| Reset    | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                |
| Reg Addr | UC n Base + 0x0C | UC n Base + 0x0C | UC n Base + 0x0C | UC n Base + 0x0C | UC n Base + 0x0C | UC n Base + 0x0C | UC n Base + 0x0C | UC n Base + 0x0C | UC n Base + 0x0C | UC n Base + 0x0C | UC n Base + 0x0C | UC n Base + 0x0C | UC n Base + 0x0C | UC n Base + 0x0C | UC n Base + 0x0C | UC n Base + 0x0C |
|          | 16               | 17               | 18               | 19               | 20               | 21               | 22               | 23               | 24               | 25               | 26               | 27               | 28               | 29               | 30               | 31               |
| R        | 0                | 0                | 0                | 0                | 0                | BSL              | BSL              | EDSEL            | EDPOL            |                  |                  |                  |                  | MODE             |                  |                  |
| W        |                  |                  | FOR CMA          | FOR CMB          |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |
| Reset    | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                |
| Reg Addr | UC n Base + 0x0C | UC n Base + 0x0C | UC n Base + 0x0C | UC n Base + 0x0C | UC n Base + 0x0C | UC n Base + 0x0C | UC n Base + 0x0C | UC n Base + 0x0C | UC n Base + 0x0C | UC n Base + 0x0C | UC n Base + 0x0C | UC n Base + 0x0C | UC n Base + 0x0C | UC n Base + 0x0C | UC n Base + 0x0C | UC n Base + 0x0C |

## Table 17-10. EMIOS\_CCR n Field Description

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

| Bits   | Name         | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                  | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|--------|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0      | FREN         | Freeze enable. If set and validated by FRZ bit in EMIOS_MCR, freezes all registers values when in debug mode, allowing the MCU to perform debug functions. 0 Normal operation 1 Freeze UC registers values                                                                                                                                                                                                                                                   | Freeze enable. If set and validated by FRZ bit in EMIOS_MCR, freezes all registers values when in debug mode, allowing the MCU to perform debug functions. 0 Normal operation 1 Freeze UC registers values                                                                                                                                                                                                                                                   |
| 1      | ODIS         | Output disable. Allows output disable in any output mode except GPIO. 0 The output pin operates normally 1 If the selected output disable input signal is asserted, the output pin goes to the complement of EDPOL for OPWFM, OPWFMB, and OPWMB modes, but the unified channel continues to operate normally; that is, it continues to produce FLAG and matches. When the selected output disable input signal is negated, the output pin operates normally. | Output disable. Allows output disable in any output mode except GPIO. 0 The output pin operates normally 1 If the selected output disable input signal is asserted, the output pin goes to the complement of EDPOL for OPWFM, OPWFMB, and OPWMB modes, but the unified channel continues to operate normally; that is, it continues to produce FLAG and matches. When the selected output disable input signal is negated, the output pin operates normally. |
| 2-3    | ODISSL [0:1] | Output disable select. Selects one of the four output disable input signals. 00 output disable input 0 01 output disable input 1 10 output disable input 2 11 output disable input 3                                                                                                                                                                                                                                                                         | Output disable select. Selects one of the four output disable input signals. 00 output disable input 0 01 output disable input 1 10 output disable input 2 11 output disable input 3                                                                                                                                                                                                                                                                         |
| 4-5    | UCPRE [0:1]  | Prescaler. Selects the clock divider value for the unified channel internal prescaler, shown below.                                                                                                                                                                                                                                                                                                                                                          | Prescaler. Selects the clock divider value for the unified channel internal prescaler, shown below.                                                                                                                                                                                                                                                                                                                                                          |
|        |              |                                                                                                                                                                                                                                                                                                                                                                                                                                                              | UCPRE[0:1]                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|        |              |                                                                                                                                                                                                                                                                                                                                                                                                                                                              | 00                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
|        |              |                                                                                                                                                                                                                                                                                                                                                                                                                                                              | 01                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
|        |              |                                                                                                                                                                                                                                                                                                                                                                                                                                                              | 10                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
|        |              |                                                                                                                                                                                                                                                                                                                                                                                                                                                              | 11                                                                                                                                                                                                                                                                                                                                                                                                                                                           |

Table 17-10. EMIOS\_CCR n Field Description (continued)

| Bits   | Name   | Description                                                                                                                                                                                                                                                                                                                                                 | Description                                                                                                                                                                                                                                                                                                                                                 | Description                                                                                                                                                                                                                                                                                                                                                 |
|--------|--------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 6      | UCPREN | Prescaler enable. Enables the prescaler counter. 0 Prescaler disabled (no clock) and prescaler counter is loaded with UCPREvalue                                                                                                                                                                                                                            | Prescaler enable. Enables the prescaler counter. 0 Prescaler disabled (no clock) and prescaler counter is loaded with UCPREvalue                                                                                                                                                                                                                            | Prescaler enable. Enables the prescaler counter. 0 Prescaler disabled (no clock) and prescaler counter is loaded with UCPREvalue                                                                                                                                                                                                                            |
| 7      | DMA    | 1 Prescaler enabled Direct memory access. Selects if the FLAG generation will be used as an interrupt or as a DMA request. 0 FLAG assigned to Interrupt request 1 FLAG assigned to DMA request Not all eMIOS channels support DMA, as shown below. The DMA bit should not be changed from its default value of 0 for any channel that does not support DMA. | 1 Prescaler enabled Direct memory access. Selects if the FLAG generation will be used as an interrupt or as a DMA request. 0 FLAG assigned to Interrupt request 1 FLAG assigned to DMA request Not all eMIOS channels support DMA, as shown below. The DMA bit should not be changed from its default value of 0 for any channel that does not support DMA. | 1 Prescaler enabled Direct memory access. Selects if the FLAG generation will be used as an interrupt or as a DMA request. 0 FLAG assigned to Interrupt request 1 FLAG assigned to DMA request Not all eMIOS channels support DMA, as shown below. The DMA bit should not be changed from its default value of 0 for any channel that does not support DMA. |
|        |        |                                                                                                                                                                                                                                                                                                                                                             | eMIOS Channel                                                                                                                                                                                                                                                                                                                                               | DMA = 0                                                                                                                                                                                                                                                                                                                                                     |
|        |        |                                                                                                                                                                                                                                                                                                                                                             | 0                                                                                                                                                                                                                                                                                                                                                           | Interrupt                                                                                                                                                                                                                                                                                                                                                   |
|        |        |                                                                                                                                                                                                                                                                                                                                                             | 1                                                                                                                                                                                                                                                                                                                                                           | Interrupt                                                                                                                                                                                                                                                                                                                                                   |
|        |        |                                                                                                                                                                                                                                                                                                                                                             | 2                                                                                                                                                                                                                                                                                                                                                           | Interrupt                                                                                                                                                                                                                                                                                                                                                   |
|        |        |                                                                                                                                                                                                                                                                                                                                                             | 3                                                                                                                                                                                                                                                                                                                                                           | Interrupt                                                                                                                                                                                                                                                                                                                                                   |
|        |        |                                                                                                                                                                                                                                                                                                                                                             | 4                                                                                                                                                                                                                                                                                                                                                           | Interrupt                                                                                                                                                                                                                                                                                                                                                   |
|        |        |                                                                                                                                                                                                                                                                                                                                                             | 5                                                                                                                                                                                                                                                                                                                                                           | Interrupt                                                                                                                                                                                                                                                                                                                                                   |
|        |        |                                                                                                                                                                                                                                                                                                                                                             | 6                                                                                                                                                                                                                                                                                                                                                           | Interrupt                                                                                                                                                                                                                                                                                                                                                   |
|        |        |                                                                                                                                                                                                                                                                                                                                                             | 7                                                                                                                                                                                                                                                                                                                                                           | Interrupt                                                                                                                                                                                                                                                                                                                                                   |
|        |        |                                                                                                                                                                                                                                                                                                                                                             | 8                                                                                                                                                                                                                                                                                                                                                           | Interrupt                                                                                                                                                                                                                                                                                                                                                   |
|        |        |                                                                                                                                                                                                                                                                                                                                                             | 9                                                                                                                                                                                                                                                                                                                                                           | Interrupt                                                                                                                                                                                                                                                                                                                                                   |
|        |        |                                                                                                                                                                                                                                                                                                                                                             | 10                                                                                                                                                                                                                                                                                                                                                          | Interrupt                                                                                                                                                                                                                                                                                                                                                   |
|        |        |                                                                                                                                                                                                                                                                                                                                                             | 11                                                                                                                                                                                                                                                                                                                                                          | Interrupt                                                                                                                                                                                                                                                                                                                                                   |
|        |        |                                                                                                                                                                                                                                                                                                                                                             | 12                                                                                                                                                                                                                                                                                                                                                          | Interrupt                                                                                                                                                                                                                                                                                                                                                   |
|        |        |                                                                                                                                                                                                                                                                                                                                                             | 13                                                                                                                                                                                                                                                                                                                                                          | Interrupt                                                                                                                                                                                                                                                                                                                                                   |
|        |        |                                                                                                                                                                                                                                                                                                                                                             | 14                                                                                                                                                                                                                                                                                                                                                          | Interrupt                                                                                                                                                                                                                                                                                                                                                   |
|        |        |                                                                                                                                                                                                                                                                                                                                                             | 15                                                                                                                                                                                                                                                                                                                                                          | Interrupt                                                                                                                                                                                                                                                                                                                                                   |
|        |        |                                                                                                                                                                                                                                                                                                                                                             | 16                                                                                                                                                                                                                                                                                                                                                          | Interrupt                                                                                                                                                                                                                                                                                                                                                   |
|        |        |                                                                                                                                                                                                                                                                                                                                                             | 17                                                                                                                                                                                                                                                                                                                                                          | Interrupt                                                                                                                                                                                                                                                                                                                                                   |
|        |        |                                                                                                                                                                                                                                                                                                                                                             | 18                                                                                                                                                                                                                                                                                                                                                          | Interrupt                                                                                                                                                                                                                                                                                                                                                   |
|        |        |                                                                                                                                                                                                                                                                                                                                                             | 19                                                                                                                                                                                                                                                                                                                                                          | Interrupt                                                                                                                                                                                                                                                                                                                                                   |
|        |        |                                                                                                                                                                                                                                                                                                                                                             | 20                                                                                                                                                                                                                                                                                                                                                          | Interrupt                                                                                                                                                                                                                                                                                                                                                   |
|        |        |                                                                                                                                                                                                                                                                                                                                                             | 21                                                                                                                                                                                                                                                                                                                                                          | Interrupt                                                                                                                                                                                                                                                                                                                                                   |
|        |        |                                                                                                                                                                                                                                                                                                                                                             | 22                                                                                                                                                                                                                                                                                                                                                          | Interrupt                                                                                                                                                                                                                                                                                                                                                   |
|        |        |                                                                                                                                                                                                                                                                                                                                                             | 23                                                                                                                                                                                                                                                                                                                                                          | Interrupt                                                                                                                                                                                                                                                                                                                                                   |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 17-10. EMIOS\_CCR n Field Description (continued)

| Bits   | Name     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                  | Description                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|--------|----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 8      | -        | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                    | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| 9-12   | IF [0:3] | Input filter. Controls the programmable input filter, selecting the minimum input pulse width that can pass through the filter, as shown below. For output modes, these bits have no meaning.                                                                                                                                                                                                                                                | Input filter. Controls the programmable input filter, selecting the minimum input pulse width that can pass through the filter, as shown below. For output modes, these bits have no meaning.                                                                                                                                                                                                                                                |
|        |          |                                                                                                                                                                                                                                                                                                                                                                                                                                              | IF[0:3] 1                                                                                                                                                                                                                                                                                                                                                                                                                                    |
|        |          |                                                                                                                                                                                                                                                                                                                                                                                                                                              | 0000                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|        |          |                                                                                                                                                                                                                                                                                                                                                                                                                                              | 0001                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|        |          |                                                                                                                                                                                                                                                                                                                                                                                                                                              | 0010                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|        |          |                                                                                                                                                                                                                                                                                                                                                                                                                                              | 0100                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|        |          |                                                                                                                                                                                                                                                                                                                                                                                                                                              | 1000                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|        |          |                                                                                                                                                                                                                                                                                                                                                                                                                                              | all others                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|        |          |                                                                                                                                                                                                                                                                                                                                                                                                                                              | 1 Filter latency is 3 clock cycles. 2 Theinput signal is synchronized before arriving at the digital filter.                                                                                                                                                                                                                                                                                                                                 |
| 13     | FCK      | Filter clock select. Selects the clock source for the programmable input filter. 0 Prescaled clock                                                                                                                                                                                                                                                                                                                                           | Filter clock select. Selects the clock source for the programmable input filter. 0 Prescaled clock                                                                                                                                                                                                                                                                                                                                           |
| 14     | FEN      | FLAGenable. Allows the unified channel FLAG bit to generate an interrupt signal or a DMA request signal (The type of signal to be generated is defined by the DMA bit). 0 Disable (FLAG does not generate an interrupt or DMA request) 1 Enable (FLAG will generate an interrupt or DMA request)                                                                                                                                             | FLAGenable. Allows the unified channel FLAG bit to generate an interrupt signal or a DMA request signal (The type of signal to be generated is defined by the DMA bit). 0 Disable (FLAG does not generate an interrupt or DMA request) 1 Enable (FLAG will generate an interrupt or DMA request)                                                                                                                                             |
| 15-17  | -        | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                    | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| 18     | FORCMA   | Force match A. For output modes, the FORCMA bit is equivalent to a successful comparison on comparator A (except that the FLAG bit is not set). This bit is cleared by reset and is always read as zero. This bit is valid for every output operating mode which uses comparator A, otherwise it has no effect. 0 Has no effect 1 Force a match at comparator A For input modes, the FORCMA bit is not used and writing to it has no effect. | Force match A. For output modes, the FORCMA bit is equivalent to a successful comparison on comparator A (except that the FLAG bit is not set). This bit is cleared by reset and is always read as zero. This bit is valid for every output operating mode which uses comparator A, otherwise it has no effect. 0 Has no effect 1 Force a match at comparator A For input modes, the FORCMA bit is not used and writing to it has no effect. |
| 19     | FORCMB   | Force match B. For output modes, the FORCMB bit is equivalent to a successful comparison on comparator B (except that the FLAG bit is not set). This bit is cleared by reset and is always read as zero. This bit is valid for every output operating mode which uses comparator B, otherwise it has no effect. 0 Has no effect 1 Force a match at comparator B                                                                              | Force match B. For output modes, the FORCMB bit is equivalent to a successful comparison on comparator B (except that the FLAG bit is not set). This bit is cleared by reset and is always read as zero. This bit is valid for every output operating mode which uses comparator B, otherwise it has no effect. 0 Has no effect 1 Force a match at comparator B                                                                              |
| 20     | -        | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                    | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                    |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## Table 17-10. EMIOS\_CCR n Field Description (continued)

| Bits   | Name      | Description                                                                                                                                                                                                                                                                                                                                                                                                       | Description                                                                                                                                                                                                                                                                                                                                                                                                       |
|--------|-----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 21-22  | BSL [0:1] | Bus select. Used to select either one of the counter buses or the internal counter to be used by the unified channel.                                                                                                                                                                                                                                                                                             | Bus select. Used to select either one of the counter buses or the internal counter to be used by the unified channel.                                                                                                                                                                                                                                                                                             |
|        |           |                                                                                                                                                                                                                                                                                                                                                                                                                   | BSL[0:1]                                                                                                                                                                                                                                                                                                                                                                                                          |
|        |           |                                                                                                                                                                                                                                                                                                                                                                                                                   | 00                                                                                                                                                                                                                                                                                                                                                                                                                |
|        |           |                                                                                                                                                                                                                                                                                                                                                                                                                   | 01                                                                                                                                                                                                                                                                                                                                                                                                                |
|        |           |                                                                                                                                                                                                                                                                                                                                                                                                                   | 10                                                                                                                                                                                                                                                                                                                                                                                                                |
|        |           |                                                                                                                                                                                                                                                                                                                                                                                                                   | 11                                                                                                                                                                                                                                                                                                                                                                                                                |
|        |           | Note: In certain modes the internal counter is used internally and therefore cannot be used as the channel time base.                                                                                                                                                                                                                                                                                             | Note: In certain modes the internal counter is used internally and therefore cannot be used as the channel time base.                                                                                                                                                                                                                                                                                             |
| 23     | EDSEL     | Edge selection bit. For input modes, the EDSEL bit selects whether the internal counter is triggered by both edges of a pulse or just by a single edge as defined by the EDPOL bit. When not shown in the mode of operation description, this bit has no effect. 0 Single edge triggering defined by the EDPOL bit 1 Both edges triggering For GPIO input mode, the EDSEL bit selects if a FLAG can be generated. | Edge selection bit. For input modes, the EDSEL bit selects whether the internal counter is triggered by both edges of a pulse or just by a single edge as defined by the EDPOL bit. When not shown in the mode of operation description, this bit has no effect. 0 Single edge triggering defined by the EDPOL bit 1 Both edges triggering For GPIO input mode, the EDSEL bit selects if a FLAG can be generated. |

## Table 17-10. EMIOS\_CCR n Field Description (continued)

| Bits   | Name       | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
|--------|------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 24     | EDPOL      | Edge polarity. For input modes (except QDEC and WPTA mode), the EDPOL bit asserts which edge triggers either the internal counter or an input capture or a FLAG. When not shown in the mode of operation description, this bit has no affect. 0 Trigger on a falling edge 1 Trigger on a rising edge For WPTA mode, the internal counter is used as a time accumulator and counts up when the input gating signal has the same polarity of EDPOL bit. 0 Counting occurs when the input gating signal is low 1 Counting occurs when the input gating signal is high For QDEC (MODE[6] cleared), the EDPOL bit selects the count direction according to direction signal (UC n input). 0 Counts down when UC n is asserted 1 Counts up when UC n is asserted NOTE: UC[n-1] EDPOL bit selects which edge clocks the internal counter of UC n 0 Trigger on a falling edge 1 Trigger on a rising edge For QDEC (MODE[6] set), the EDPOL bit selects the count direction according to the phase difference. 0 Internal counter decrements if phase_A is ahead phase_B signal 1 Internal counter increments if phase_A is ahead phase_B signal NOTE: In order to operate properly, EDPOL bit must contain the same value in UC n and UC[n-1] For output modes, the EDPOL bit is used to select the logic level on the output pin. 0 Amatch on comparator Aclears the output flip-flop, while a match on comparator Bsets it 1 Amatch on comparator Asets the output flip-flop, while a match on comparator Bclears it |
| 25-31  | MODE [0:6] | Mode selection. Selects the mode of operation of the unified channel, as shown in Table 17-11.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |

Table 17-11. Unified Channel MODE Bits

|   MODE0:6] | Unified Channel Mode of Operation                                |
|------------|------------------------------------------------------------------|
|    0000000 | General purpose input/output mode (input)                        |
|    0000001 | General purpose input/output mode (output)                       |
|    0000010 | Single action input capture                                      |
|    0000011 | Single action output compare                                     |
|    0000100 | Input pulse width measurement                                    |
|    0000101 | Input period measurement                                         |
|    0000110 | Double action output compare (with FLAG set on the second match) |
|    0000111 | Double action output compare (with FLAG set on both match)       |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 17-11. Unified Channel MODE Bits (continued)

| MODE0:6]         | Unified Channel Mode of Operation                                                                                                                   |
|------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| 0001000          | Pulse/edge accumulation (continuous)                                                                                                                |
| 0001001          | Pulse/edge accumulation (single shot)                                                                                                               |
| 0001010          | Pulse/edge counting (continuous)                                                                                                                    |
| 0001011          | Pulse/edge counting (single shot)                                                                                                                   |
| 0001100          | Quadrature decode (for count and direction encoders type)                                                                                           |
| 0001101          | Quadrature decode (for phase_A and phase_B encoders type)                                                                                           |
| 0001110          | Windowed programmable time accumulation                                                                                                             |
| 0001111          | Reserved                                                                                                                                            |
| 0010000          | Modulus counter (up counter, internal clock source)                                                                                                 |
| 0010001          | Modulus counter (up counter, external clock source)                                                                                                 |
| 0010010- 0010011 | Reserved                                                                                                                                            |
| 0010100          | Modulus counter (up/down counter, no change in counter direction upon match of input counter and register B1, internal clock source)                |
| 0010101          | Modulus counter (up/down counter, no change in counter direction upon match of input counter and register B1, external clock source)                |
| 0010110          | Modulus counter (up/down counter, change in counter direction upon match of input counter and register B1 and sets the FLAG, internal clock source) |
| 0010111          | Modulus counter (up/down counter, change in counter direction upon match of input counter and register B1 and sets the FLAG, external clock source) |
| 0011000          | Output pulse width and frequency modulation (FLAG set at match of internal counter and comparator B, immediate update)                              |
| 0011001          | Output pulse width and frequency modulation (FLAG set at match of internal counter and comparator B, next period update)                            |
| 0011010          | Output pulse width and frequency modulation (FLAG set at match of internal counter and comparator A or comparator B, immediate update)              |
| 0011011          | Output pulse width and frequency modulation (FLAG set at match of internal counter and comparator A or comparator B, next period update)            |
| 0011100          | Center aligned output pulse width modulation (FLAG set in trailing edge, trailing edge dead-time)                                                   |
| 0011101          | Center aligned output pulse width modulation (FLAG set in trailing edge, leading edge dead-time)                                                    |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 17-11. Unified Channel MODE Bits (continued)

| MODE0:6]         | Unified Channel Mode of Operation                                                                                              |
|------------------|--------------------------------------------------------------------------------------------------------------------------------|
| 0011110          | Center aligned output pulse width modulation (FLAG set in both edges, trailing edge dead-time)                                 |
| 0011111          | Center aligned output pulse width modulation (FLAG set in both edges, leading edge dead-time)                                  |
| 0100000          | Output pulse width modulation (FLAG set at match of internal counter and comparator B, immediate update)                       |
| 0100001          | Output pulse width modulation (FLAG set at match of internal counter and comparator B, next period update)                     |
| 0100010          | Output pulse width modulation (FLAG set at match of internal counter and comparator A or comparator B, immediate update)       |
| 0100011          | Output pulse width modulation (FLAG set at match of internal counter and comparator A or comparator B, next period update)     |
| 1100100- 1111111 | Reserved                                                                                                                       |
| 1010000          | Modulus up counter, buffered, internal clock                                                                                   |
| 1010001          | Modulus up counter, buffered, external clock                                                                                   |
| 1010010- 1010001 | Reserved                                                                                                                       |
| 1010100          | Modulus up/down counter, buffered (FLAG set on one event, internal clock)                                                      |
| 1010101          | Modulus up/down counter, buffered (FLAG set on one event, external clock)                                                      |
| 1010110          | Modulus up/down counter, buffered (FLAG set on both events, internal clock)                                                    |
| 1010111          | Modulus up/down counter, buffered (FLAG set on both events, external clock)                                                    |
| 1011000          | Output pulse width and frequency modulation, buffered (FLAG set at match of internal counter and comparator B)                 |
| 1011001          | Reserved                                                                                                                       |
| 1011010          | Output pulse width and frequency modulation, buffered (FLAG set at match of internal counter and comparator A or comparator B) |
| 1011011          | Reserved                                                                                                                       |
| 1011100          | Center aligned output pulse width modulation, buffered (FLAG set on trailing edge, trailing edge dead-time)                    |
| 1011101          | Center aligned output pulse width modulation, buffered (FLAG set on trailing edge, leading edge dead-time)                     |
| 1011110          | Center aligned output pulse width modulation, buffered (FLAG set on both edges, trailing edge dead-time)                       |
| 1011111          | Center aligned output pulse width modulation, buffered (FLAG set on both edges, leading edge dead-time)                        |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 17-11. Unified Channel MODE Bits (continued)

|   MODE0:6] | Unified Channel Mode of Operation                                  |
|------------|--------------------------------------------------------------------|
|    1100000 | Output pulse width modulation, buffered (FLAG set on second match) |
|    1100001 | Reserved                                                           |
|    1100010 | Output pulse width modulation, buffered (FLAG set on both matches) |

## 17.3.1.8 eMIOS Channel Status Register (EMIOS\_CSR n )

EMIOS\_CSR  reflects the status of the UC input/output signals and the overflow condition of the internal n counter, as well as the occurrence of a trigger event.

Figure 17-9. eMIOS Channel Status Register (EMIOS\_CSR n )

<!-- image -->

|          | 0                | 1                | 2                | 3                | 4                | 5                | 6                | 7                | 8                | 9                | 10               | 11               | 12               | 13               | 14               | 15               |
|----------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|
| R        | OVR              | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                |
| W        | w1c              |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |
| Reset    | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                |
| Reg Addr | UC n Base + 0x10 | UC n Base + 0x10 | UC n Base + 0x10 | UC n Base + 0x10 | UC n Base + 0x10 | UC n Base + 0x10 | UC n Base + 0x10 | UC n Base + 0x10 | UC n Base + 0x10 | UC n Base + 0x10 | UC n Base + 0x10 | UC n Base + 0x10 | UC n Base + 0x10 | UC n Base + 0x10 | UC n Base + 0x10 | UC n Base + 0x10 |
|          | 16               | 17               | 18               | 19               | 20               | 21               | 22               | 23               | 24               | 25               | 26               | 27               | 28               | 29               | 30               | 31               |
| R        | OVFL             | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | UCIN             | UCOUT            | FLAG             |
| W        | w1c              |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  |                  | w1c              |
| Reset    | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                | 0                |
| Reg Addr | UC n Base + 0x10 | UC n Base + 0x10 | UC n Base + 0x10 | UC n Base + 0x10 | UC n Base + 0x10 | UC n Base + 0x10 | UC n Base + 0x10 | UC n Base + 0x10 | UC n Base + 0x10 | UC n Base + 0x10 | UC n Base + 0x10 | UC n Base + 0x10 | UC n Base + 0x10 | UC n Base + 0x10 | UC n Base + 0x10 | UC n Base + 0x10 |

Table 17-12. EMIOS\_CSR n Field Descriptions

| Bits   | Name   | Description                                                                                                                                                                                                     |
|--------|--------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0      | OVR    | Overrun. Indicates that FLAG generation occurred when the FLAG bit was already set. This bit can be cleared by writing a 1 to it or by clearing the FLAG bit. 0 Overrun has not occurred 1 Overrun has occurred |
| 1-15   | -      | Reserved.                                                                                                                                                                                                       |
| 16     | OVFL   | Overflow. Indicates that an overflow has occurred in the internal counter. OVFL is cleared by writing a 1 to it. 0 No overflow 1 An overflow had occurred                                                       |
| 17-28  | -      | Reserved.                                                                                                                                                                                                       |
| 29     | UCIN   | Unified channel input pin. Reflects the input pin state after being filtered and synchronized.                                                                                                                  |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## Table 17-12. EMIOS\_CSR n Field Descriptions (continued)

|   Bits | Name   | Description                                                                                                                                                                                                                                               |
|--------|--------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|     30 | UCOUT  | Unified channel output pin. The UCOUT bit reflects the output pin state.                                                                                                                                                                                  |
|     31 | FLAG   | FLAG. Set when an input capture or a match event in the comparators occurred. This bit is cleared by writing a 1 to it. 0 FLAG cleared 1 FLAG set event has occurred Note: When EMIOS_CCR[DMA] bit is set, the FLAG bit is cleared by the eDMAcontroller. |

## 17.4 Functional Description

The  eMIOS  provides  independent  channels  (UC)  that  can  be  configured  and  accessed  by  the MPC5553/MPC5554. Four time bases can be shared by the channels through four counter buses and each unified channel can generate its own time base. Optionally, the counter A bus can be driven by an external time base from the eTPU imported through the STAC interface.

## NOTE

Counter bus A can be driven by unified channel 23 or by the STAC bus. Counter  bus  B,  C,  and  D  are  driven  by  unified  channels  0,  8,  and  16, respectively. Counter bus A can be shared among all unified channels. UCs 0  to  7,  8  to  15,  and  16  to  23  can  share  counter  buses  B,  C,  and  D, respectively.

The following four components of the MPC5553/MPC5554 eMIOS are discussed below:

- · Bus interface unit
- · STAC client submodule
- · Global clock prescaler
- · Unified channels and their modes of operation

## 17.4.1 Bus Interface Unit (BIU)

The bus interface unit provides the interface between the internal bus and the slave interface, allowing communication among all submodules and the slave interface.

The BIU allows 8-, 16-, and 32-bit accesses. They are performed over a 32-bit data bus in a single cycle clock.

## 17.4.1.1 Effect of Freeze on the BIU

When the FRZ bit in the EMIOS\_MCR is set and the module is in debug mode, the operation of the BIU is not affected.

## 17.4.2 STAC Client Submodule

The shared time and angle count (STAC) bus provides access to one external time base, imported from the STAC bus to the eMIOS unified channels. The eTPU module's time bases and angle count can be exported and/or imported through the STAC client submodule interface. Time bases and/or angle information of either eTPU engine can be exported to the other eTPU engine and to the eMIOS module, which is only a

STAC client. There are restrictions on engine export/import targets: one engine cannot export from or import to itself, nor can it import time base and/or angle count if in angle mode.

The MPC5553/MPC5554 STAC server identification assignment is shown in Table 17-13. The time slot assignment is fixed, so only time bases running at system clock ÷ 4 or slower can be integrally exported. The STAC client submodule runs with the system clock, and its time slot timing is synchronized with the eTPU timing on reset. The time slot sequence is 0-1-2-3, such that they are alternated between engines 1 and 2.

Table 17-13. STAC Client Submodule Server Slot Assignment

|   Engine | Time Base   |   Server ID |
|----------|-------------|-------------|
|        1 | TCR1        |           0 |
|        1 | TCR2        |           2 |
|        2 | TCR1        |           1 |
|        2 | TCR2        |           3 |

Figure 17-10 provides a block diagram for the STAC client submodule.

Figure 17-10. STAC Client Submodule Block Diagram

<!-- image -->

Bits  SRV[0:3]  in  register  EMIOS\_MCR,  selects  the  desired  time  slot  of  the  STAC  bus  to  be  output. Figure 17-11 shows a timing diagram for the STAC client submodule.

<!-- image -->

Note: In this case, SRV bits were set to capture TS[01].

Figure 17-11. Timing Diagram for the STAC Bus and STAC Client Submodule Output

Every time the selected time slot changes, the STAC Client Submodule output is updated.

## 17.4.2.1 Effect of Freeze on the STAC Client Submodule

When the FRZ bit in the EMIOS\_MCR is set and the module is in debug mode, the operation of the STAC client submodule submodule is not affected; that is, there is no freeze function in this submodule.

## 17.4.3 Global Clock Prescaler Submodule (GCP)

The GCP divides the system clock to generate a clock for the clock prescalers of the unified channels. The system clock is  prescaled  by  the  value  defined  in  Table 17-7  according  to  the  GPRE[0:7]  bits  in  the EMIOS\_MCR. The output is clocked every time the counter overflows. Counting is enabled by setting EMIOS\_MCR[GPREN]. The counter can be stopped at any time by clearing this bit, thereby stopping the internal counter in all the unified channels.

## 17.4.3.1 Effect of Freeze on the GCP

When the FRZ bit in the EMIOS\_MCR is set and the module is in debug mode, the operation of GCP submodule is not affected; that is, there is no freeze function in this submodule.

## 17.4.4 Unified Channel (UC)

Figure 17-12 shows the unified channel block diagram. Each unified channel consists of the following:

- · Counter bus selector that selects the time base to be used by the channel for all timing functions
- · Programmable clock prescaler
- · Two double buffered data registers A and B that allow up to two input capture and/or output compare events to occur before software intervention is needed.
- · Two comparators (equal only) A and B that compare the selected counter bus with the value in the data registers
- · Internal counter that can be used as a local time base or to count input events
- · Programmable input filter that ensures that only valid pin transitions are received by a channel
- · Programmable input edge detector that detects rising, falling, or both edges
- · Output flip-flop that holds the logic level to be applied to the output pin
- · eMIOS status and control registers
- · Output disable input selector that selects the output disable input signal to be used as the unified channel output disable
- · Control state machine (FSM)

The  major  components  and  functions  of  the  MPC5553/MPC5554  unified  channels  are  discussed  in Section 17.4.4.1, 'Programmable Input Filter (PIF) through Section 17.4.4.4, 'Modes of Operation of the Unified Channels.'

Counter Bus A

Notes:

<!-- image -->

- 1. Counter bus A can be driven by either the STAC bus or channel 23. Refer to EMIOS\_MCR[ETB]. Channel 0 drives counter bus B, channel 8 drives counter bus C and channel 16 drives counter bus D. Counter bus B can be selected as the counter for channels 0-7, counter bus C for channels 8-15, and counter bus D for channels 16-23. Refer to Figure 16-1 and EMIOS\_CCR n [BS].
- 2. Goes to the finite state machine of the UC[n-1]. These signals are used for QDEC mode.

Figure 17-12. Unified Channel Block Diagram

## 17.4.4.1 Programmable Input Filter (PIF)

The PIF ensures that only valid input pin transitions are received by the unified channel edge detector. A block diagram of the PIF is shown in Figure 17-13.

The PIF is a 5-bit programmable up counter that is incremented by the selected clock source, according to bits IF[0:3] in EMIOS\_CCR n . The clock source is selected by the EMIOS\_CCR n [FCK] bit.

Figure 17-13. Programmable Input Filter Submodule Diagram

<!-- image -->

The input signal is synchronized by the system clock. When a state change occurs in this signal, the 5-bit counter starts counting up. As long as the new state is stable on the pin, the counter continues incrementing. If a counter overflows occurs, the new pin value is validated. In this case, it is transmitted as a pulse edge to the edge detector. If the opposite edge appears on the pin before validation (overflow), the counter is reset. At the next synchronized pin transition, the counter starts counting again. Any pulse that is shorter than a full range of the masked counter is regarded as a glitch, and it is not passed on to the edge detector. A timing diagram of the input filter is shown in Figure 17-14.

Figure 17-14. Programmable Input Filter Example

<!-- image -->

## 17.4.4.2 Clock Prescaler (CP)

A unified channel has a clock prescaler (CP) that divides the global clock prescaler (refer to Section 17.4.3, 'Global Clock Prescaler Submodule (GCP)') output signal to generate a clock enable for the internal counter  of  the  unified  channel.  It  is  a  programmable  2-bit  down  counter.  The  global  clock  prescaler submodule  (GCP)  output  signal  is  prescaled  by  the  value  defined  in  Table 17-10  according  to  the UCPRE[0:1]  bits  in  the  EMIOS\_CCR n .  The  output  is  clocked  every  time  the  counter  reaches  zero. Counting is enabled by setting the UCPREN bit in the EMIOS\_CCR n . The counter can be stopped at any time by clearing this bit, thereby stopping the internal counter in the unified channel.

## 17.4.4.3 Effect of Freeze on the Unified Channel

When in debug mode and the EMIOS\_MCR[FRZ] bit and the EMIOS\_CCR n [FREN] bit are both set, the internal counter and the unified channel's capture and compare functions are halted. The UC is frozen in its current state.

During freeze, all registers are accessible. When the unified channel is operating in an output mode, the force match functions remain available, allowing the software to force the output to the desired level.

Note that for input modes, any input events that may occur while the channel is frozen are ignored.

When exiting debug mode or freeze enable bit is cleared (FRZ in the EMIOS\_MCR or FREN in the EMIOS\_CCR ) the channel actions resume. n

## 17.4.4.4 Modes of Operation of the Unified Channels

The mode of operation of a unified channel is determined by the mode select bits MODE[0:6] in the EMIOS\_CCR . See Table 17-11 for details. n

When entering an output mode (except for GPIO mode), the output flip-flop is set to the complement of the EDPOL bit in the EMIOS\_CCR n .

Because the internal counter EMIOS\_CCNTR n continues to run in all modes (except for GPIO mode), it is possible to use this counter as the UC time base unless it (the internal counter) is a required resource in the operation of the selected mode.

To provide smooth waveform generation while allowing A and B registers to be changed on the fly, the double-buffered  modes  MCB,  OPWFMB,  OPWMB,  and  OPWMCB  are  provided  (beginning  at Section 17.4.4.4.15, 'Modulus Counter, Buffered Mode (MCB) (MPC5553 Only)'). In these modes the A and B registers are double buffered. Descriptions of the double-buffered modes are presented separately, because there are several basic differences from the single-buffered MC, OPWFM, OPWM, and OPWMC modes.

Section 17.4.4.4.2,  'Single  Action  Input  Capture  Mode  (SAIC)'  through  Section 17.4.4.4.18,  'Output Pulse Width Modulation, Buffered Mode (OPWMB) (MPC5553 Only)' below explain in detail the unified channels' modes of operation.

## 17.4.4.4.1 General Purpose Input/Output Mode (GPIO)

In GPIO mode, all input capture and output compare functions of the UC are disabled, the internal counter (EMIOS\_CCNTRn register) is cleared and disabled. All control bits remain accessible. In order to prepare the UC for a new operating mode, writing to registers EMIOS\_CADR n or EMIOS\_CBDR  stores the n same value in registers A1/A2 or B1/B2, respectively.

MODE[6] bit selects between input (MODE[6] = 0) and output (MODE[6] = 1) modes.

It is required that when changing MODE[0:6], the application software goes to GPIO mode first in order to reset the UC's internal functions properly. Failure to do this can lead to invalid and unexpected output compares and input capture results, or can cause the FLAGs to be set incorrectly.

In GPIO input mode, the FLAG generation is determined according to EDPOL and EDSEL bits and the input pin status can be determined by reading the UCIN bit.

In GPIO output mode, the unified channel is used as a single output port pin and the value of the EDPOL bit is permanently transferred to the output flip-flop.

## NOTE

The GPIO modes provided in the eMIOS are particularly useful as interim modes when certain other eMIOS modes are being dynamically configured and enabled or disabled during the execution of the application. For normal GPIO function on the eMIOS pins, it is recommended that the SIU be used to configure those pins as system GPIO. See Section 6.2.1.3, 'General-Purpose I/O Pins (GPIO[0:210]).

## 17.4.4.4.2 Single Action Input Capture Mode (SAIC)

In SAIC mode, when a triggering event occurs on the input pin, the value on the selected time base is captured into register A2. At the same time, the FLAG bit is set to indicate that an input capture has occurred. Register EMIOS\_CADR n returns the value of register A2.

The input capture is triggered by a rising, falling or either edges in the input pin, as configured by EDPOL and EDSEL bits in EMIOS\_CCR . n

Figure 17-15 shows how the unified channel can be used for input capture.

<!-- image -->

Reading EMIOS\_CADR

n

returns the value of

A2.

Figure 17-15. Single Action Input Capture Example

## 17.4.4.4.3 Single Action Output Compare Mode (SAOC)

In SAOC mode a match value is loaded in register A2 and then transferred to register A1 to be compared with the selected time base. When a match occurs, the EDSEL bit selects if the output flip-flop is toggled or if the value in EDPOL is transferred to it. At the same time, the FLAG bit is set to indicate that the output compare match has occurred. Writing to register EMIOS\_CADR n stores  the  value  in  register  A2  and reading to register EMIOS\_CADR n returns the value of register A1.

An output compare match can be simulated in software by setting the FORCMA bit in EMIOS\_CCR n . In this case, the FLAG bit is not set.

Figure 17-16 and Figure 17-17 show how the unified channel can be used to perform a single output compare with EDPOL value being transferred to the output flip-flop and toggling the output flip-flop at each match, respectively.

Figure 17-16. SAOC Example with EDPOL Value Transferred to the Output Flip-flop

<!-- image -->

Figure 17-17. SAOC Example Toggling the Output Flip-flop

<!-- image -->

## 17.4.4.4.4 Input Pulse Width Measurement Mode (IPWM)

The IPWM mode allows the measurement of the width of a positive or negative pulse by capturing the leading  edge  on  register  B1  and  the  trailing  edge  on  register  A2.  Successive  captures  are  done  on consecutive edges of opposite polarity. The leading edge sensitivity (that is, pulse polarity) is selected by EDPOL bit in the EMIOS\_CCR . Registers EMIOS\_CADR n n and EMIOS\_CBDR  return the values in n register A2 and B1, respectively.

The capture function of register A2 remains disabled until the first leading edge triggers the first input capture on register B2. When this leading edge is detected, the count value of the selected time base is latched into register B2; the FLAG bit is not set. When the trailing edge is detected, the count value of the selected time base is latched into register A2 and, at the same time, the FLAG bit is set and the content of register B2 is transferred to register B1.

If subsequent input capture events occur while the corresponding FLAG bit is set, registers A2 and B1 will be updated with the latest captured values and the FLAG will remain set. Registers EMIOS\_CADR n and EMIOS\_CBDR  return the value in registers A2 and B1, respectively. n

In order to guarantee coherent access, reading EMIOS\_CADR n disables transfers between B2 and B1 until reading EMIOS\_CBDR . After that, transfer is re-enabled. n

The input pulse width is calculated by subtracting the value in B1 from A2.

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## Enhanced Modular Input/Output Subsystem (eMIOS)

Figure 17-18 shows how the unified channel can be used for input pulse width measurement.

<!-- image -->

Notes:

After input filter.

1

- 2 Reading EMIOS\_CADR  returns the value of A2, writing EMIOS\_CADR n n writes to A2.
- 3 Reading EMIOS\_CBDR  returns the value of B1, writing EMIOS\_CBDR n n writes to B1.

Figure 17-18. Input Pulse Width Measurement Example

## 17.4.4.4.5 Input Period Measurement Mode (IPM)

The IPM mode allows the measurement of the period of an input signal by capturing two consecutive rising edges or two consecutive falling edges. Successive input captures are done on consecutive edges of the same polarity. The edge polarity is defined by the EDPOL bit in the EMIOS\_CCR n .

When the first edge of selected polarity is detected, the selected time base is latched into the registers A2 and B2, and the data previously held in register B2 is transferred to register B1. On this first capture the FLAG line is not set, and the values in registers B1 is meaningless. On the second and subsequent captures, the FLAG line is set and data in register B2 is transferred to register B1.

When the second edge of the same polarity is detected, the counter bus value is latched into registers A2 and B2, the data previously held in register B2 is transferred to data register B1, and the FLAG bit is set to indicate the start and end points of a complete period have been captured. This sequence of events is repeated for each subsequent capture. Registers EMIOS\_CADR n and EMIOS\_CBDR  return the values n in register A2 and B1, respectively.

In order to guarantee coherent access, reading EMIOS\_CADR n disables transfers between B2 and B1 until reading EMIOS\_CBDR  register, then any pending transfer is re-enabled. n

The input pulse period is calculated by subtracting the value in B1 from A2.

Figure 17-19 shows how the unified channel can be used for input period measurement.

<!-- image -->

Notes:

- 1 After input filter.
- 2 Reading EMIOS\_CADR n returns the value of A2, writing EMIOS\_CADR n writes to A2.
- 3 Reading EMIOS\_CBDR n returns the value of B1, writing EMIOS\_CBDR n writes to B1.

Figure 17-19. Input Period Measurement Example

## 17.4.4.4.6 Double Action Output Compare Mode (DAOC)

In the DAOC mode the leading and trailing edges of the variable pulse width output are generated by matches occurring on comparators A and B, respectively.

When  the  DAOC  mode  is  first  selected  (coming  from  GPIO  mode)  both  comparators  are  disabled. Comparators A and B are enabled by updating registers A1 and B1 respectively and remain enabled until a match occurs on that comparator, when it is disabled again. In order to update registers A1 and B1, a write to A2 and B2 must occur and the EMIOS\_CCR n [ODIS] bit must be cleared.

The output flip-flop is set to the value of EMIOS\_CCR n [EDPOL] when a match occurs on comparator A and to the complement of EDPOL when a match occurs on comparator B.

MODE[6] controls if the EMIOS\_CSR n [FLAG] is set on both matches or just on the second match (see Table 17-11 for details).

If subsequent enabled output compares occur on registers A1 and B1, pulses will continue to be generated, regardless of the state of the FLAG bit.

At any time, the EMIOS\_CCR n [FORCMA] and EMIOS\_CCR [FORCMB] bits allow the software to n force  the  output  flip-flop  to  the  level  corresponding  to  a  comparison  event  in  comparator  A  or  B, respectively. Note that the FLAG bit is not affected by these forced operations.

## NOTE

If both registers (A1 and B1) are loaded with the same value, the unified channel behaves as if a single match on comparator B had occurred; that is, the output flip-flop will be set to the complement of EDPOL bit and the FLAG bit is set.

Figure 17-20 and Figure 17-21 show how the unified channel can be used to generate a single output pulse with FLAG bit being set on the second match or on both matches, respectively.

Update to

<!-- image -->

2 Writing EMIOS\_CBDR n writes to B1.

A2 value transferred to A1 according to OU n bit.

B2 value transferred to B1 according to OU n bit.

Figure 17-20. Double Action Output Compare with FLAG Set on the Second Match

Update to

Figure 17-21. Double Action Output Compare with FLAG Set on Both Matches

<!-- image -->

## 17.4.4.4.7 Pulse/Edge Accumulation Mode (PEA)

The PEA mode returns the time taken to detect a desired number of input events. MODE[6] bit selects between continuous or single shot operation.

After writing to register A1, the internal counter is cleared on the first input event, ready to start counting input events and the selected timebase is latched into register B2. On the match between the internal counter and register A1, a counter bus capture is triggered to register A2 and B2. The data previously held in register B2 is transferred to register B1 and the FLAG bit is set to indicate that an event has occurred. The desired time interval can be determined subtracting register B1 from A2. Registers EMIOS\_CADR n and EMIOS\_CBDR  return the values in register A2 and B1, respectively. n

In order to guarantee coherent access, reading EMIOS\_CADR n disables transfers between B2 and B1 until reading EMIOS\_CBDR  register, then any pending transfer is re-enabled. n

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Triggering of the counter clock (input event) is done by a rising or falling edge or both edges on the input pin. The polarity of the triggering edge is selected by the EDSEL and EDPOL bits in EMIOS\_CCR n .

For continuous operating mode (MODE[6] cleared), the counter is cleared on the next input event after a FLAG generation and continues to operate as described above.

For  single  shot  operation  (MODE[6]  set),  the  counter  is  not  cleared  or  incremented  after  a  FLAG generation, until a new writing operation to register A is performed.

## NOTE

The FORCMA and FORCMB bits have no effect when the unified channel is configured for PEA mode.

Figure 17-22 and Figure 17-23 show how the unified channel can be used for continuous and single shot pulse/edge accumulation mode.

<!-- image -->

Notes:

1 Cleared on the first input event after writing to register A1.

- 2 After input filter.
- 3 Writing EMIOS\_CADR n writes to A1.
- 4 Reading EMIOS\_CADR n returns the value of A2 .
- 5 Reading EMIOS\_CBDR n returns the value of B1.

Figure 17-22. Pulse/Edge Accumulation Continuous Mode Example

<!-- image -->

Notes:

- 1 Cleared on the first input event after writing to register A1.
- 2 After input filter.
- 3 Writing EMIOS\_CADR n writes to A1.
- 4 Reading EMIOS\_CADR n returns the value of A2 .
- 5 Reading EMIOS\_CBDR n returns the value of B1.

Figure 17-23. Pulse/Edge Accumulation Single-shot Mode Example

## 17.4.4.4.8 Pulse/Edge Counting Mode (PEC)

The PEC mode returns the amount of pulses or edges detected on the input for a desired time window. MODE[6] bit selects between continuous or single shot operation.

Triggering of the internal counter is done by a rising or falling edge or both edges on the input signal. The polarity and the triggering edge is selected by EDSEL and EDPOL bits in EMIOS\_CCR n .

Register A1 holds the start time and register B1 holds the stop time for the time window. After writing to register A1, when a match occur between comparator A and the selected timebase, the internal counter is cleared and it is ready to start counting input events. When the time base matches comparator B1, the internal counter is disabled and the FLAG bit is set. Reading the EMIOS\_CCNTR n returns the amount of detected pulses.

For continuous operation (MODE[6] cleared), the next match between comparator A and the selected time base clears the internal counter and counting is enabled again. In order to guarantee the accuracy when reading EMIOS\_CCNTR  after the flag is set, the software must check if the time base value is out of the n time interval defined by registers A1 and B1.

For single shot operation (MODE[6] set), the next match between comparator A and the selected time base has no effect, until a new write to register A is performed.

## NOTE

The FORCMA and FORCMB bits have no effect when the unified channel is configured for PEC mode.

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Figure 17-24 and Figure 17-25 show how the unified channel can be used for continuous or single shot pulse/edge counting mode.

<!-- image -->

Notes:

Writing EMIOS\_CADR

n

writes to

A1.

1

2 Writing EMIOS\_CBDR n writes to B1.

Figure 17-24. Pulse/Edge Counting Continuous Mode Example

<!-- image -->

2 Reading EMIOS\_CBDR n returns the value of B1.

Notes:

1 Reading EMIOS\_CADR n returns the value of A1.

Figure 17-25. Pulse/Edge Counting Single-Shot Mode Example

## 17.4.4.4.9 Quadrature Decode Mode (QDEC)

Quadrature decode mode uses UC n operating in QDEC mode and the programmable input filter (PIF) from UC[n-1]. Note that UC[n-1] can be configured, at the same time, to an operation mode that does not use I/O pins, such as MC mode (modulus counter). The connection among the UCs is circular; that is, when UC0 is running in QDEC mode, the programmable input filter from UC23 is being used.

This mode generates a FLAG every time the internal counter matches A1 register. The internal counter is automatically selected and is not cleared when entering this mode.

MODE[6] bit selects which type of encoder will be used: count and direction encoder or phase\_A and phase\_B encoders.

When operating with count and direction encoder (MODE[6] cleared), UC n input pin must be connected to the direction signal and UC[n-1] input pin must be connected to the count signal of the quadrature encoder. UC n EDPOL bit selects count direction according to direction signal and UC[n-1] EDPOL bit selects if the internal counter is clocked by the rising or falling edge of the count signal.

When operating with phase\_A and phase\_B encoder (MODE[6] set), UC n input pin must be connected to the phase\_A signal and UC[n-1] input pin must be connected to the phase\_B signal of the quadrature encoder. EDPOL bit selects the count direction according to the phase difference between phase\_A and phase\_B signals.

Figure 17-26 and Figure 17-27 show two unified channels configured to quadrature decode mode for count and direction encoder and phase\_A and phase\_B encoders, respectively.

<!-- image -->

Note:  Writing EMIOS\_CADR

n

writes to

A1.

Figure 17-26. Quadrature Decode Mode Example with Count and Direction Encoder

<!-- image -->

Note:  Writing EMIOS\_CADR

n

writes to

A1.

Figure 17-27. Quadrature Decode Mode Example with Phase\_A and Phase\_B Encoder

## 17.4.4.4.10 Windowed Programmable Time Accumulation Mode (WPTA)

The  WPTA mode accumulates  the  sum  of  the  total  high  time  or  low  time  of  an  input  signal  over  a programmable interval (time window).

The prescaler bits UCPRE[0:1] in EMIOS\_CCR n define the increment rate of the internal counter.

Register A1 holds the start time and register B1 holds the stop time of the programmable time interval. When a match occurs between register A and the selected timebase, the internal counter is cleared and it is ready to start counting. The internal counter is used as a time accumulator; that is, it counts up when the input signal has the same polarity of EDPOL bit in EMIOS\_CCR n and does not count otherwise. When a match occurs in comparator B, the internal counter is disabled regardless of the input signal polarity and the FLAG bit is set. Reading EMIOS\_CCNTR n returns the high or low time of the input signal.

## NOTE

The FORCMA and FORCMB bits have no effect when the unified channel is configured for WPTA mode.

Figure 17-28 shows how the unified channel can be used to accumulate high time.

<!-- image -->

Notes:

After input filter.

1

- 2 Writing EMIOS\_CADR n writes to A1.
- 3
- Writing EMIOS\_CBDR n writes to B1.

Figure 17-28. Windowed Programmable Time Accumulation Example

## 17.4.4.4.11 Modulus Counter Mode (MC)

The MC mode can be used to provide a time base for a counter bus or as a general purpose timer.

MODE[6] bit selects internal or external clock source when cleared or set, respectively. When external clock is selected, the input signal pin is used as the source and the triggering polarity edge is selected by the EDPOL and EDSEL in the EMIOS\_CCR . n

The internal counter counts up from the current value until it matches the value in register A1. Register B1 is cleared and is not accessible to the MCU. MODE[4] bit selects up mode or up/down mode, when cleared or set, respectively.

When in up count mode, a match between the internal counter and register A1 sets the FLAG and clears the internal counter.

When in up/down count mode, a match between the internal counter and register A1 sets the FLAG and changes the counter direction from increment to decrement. A match between register B1 and the internal counter changes the counter direction from decrement to increment and sets the FLAG only if MODE[5] bit is set.

## NOTE

The FORCMA and FORCMB bits have no effect when the unified channel is configured for MC mode.

## NOTE

Any update to the A register will take place immediately, regardless of the current  state  of  the  counter  and  whether  the  counter  is  in  up  mode,  or up/down mode.

Figure 17-29 and Figure 17-30 shows how the unified channel can be used as modulus counter in up mode and up/down mode, respectively.

<!-- image -->

Notes:

1

Writing EMIOS\_A

n

writes to

A2.

A2 value transferred to A1 according to OU n bit.

Figure 17-29. Modulus Counter Up Mode Example

<!-- image -->

Notes:

1

Writing EMIOS\_A

n

writes to

A2.

A2 value transferred to A1 according to OU n bit.

Figure 17-30. Modulus Counter Up/Down Mode Example

## 17.4.4.4.12 Output Pulse Width and Frequency Modulation Mode (OPWFM)

In this mode, register A1 contains the duty cycle and register B1 contains the period of the output signal. MODE[6]  bit  controls  the  transfer  from  register  B2  to  B1,  which  can  be  done  either  immediately (MODE[6] cleared), providing the fastest change in the duty cycle, or at every match of  register  A1 (MODE[6] set).

The  internal  counter  is  automatically  selected  as  a  time  base,  therefore  the  BSL[0:1]  bits  in  register EMIOS\_CCR  have no meaning. The output flip-flop's active state is the complement of EDPOL bit. The n output  flip-flop  is  active  during  the  duty  cycle  (from  the  start  of  the  cycle  until  a  match  occurs  in comparator A). After the match in comparator A the output flip-flop is in the inactive state (the value of EDPOL) until the next cycle starts. When a match on comparator A occurs, the output flip-flop is set to the value of the EDPOL bit. When a match occurs on comparator B, the output flip-flop is set to the complement of the EDPOL bit and the internal counter is cleared.

FLAG can be generated at match B, when MODE[5] is cleared, or in both matches, when MODE[5] is set.

## Enhanced Modular Input/Output Subsystem (eMIOS)

At any time, the FORCMA and FORCMB bits allow the software to force the output flip-flop to the level corresponding to a match on A or B respectively. Also, FORCMB clears the internal counter. Note that the FLAG bit is not set by the FORCMA or FORCMB operations.

If  subsequent  comparisons  occur  on  comparators  A  and  B,  the  PWFM  pulses  continue  to  be  output, regardless of the state of the FLAG bit.

In  order  to  achieve  0%  duty  cycle,  both  registers  A1  and  B1  must  be  set  to  the  same  value.  When  a simultaneous match occurs on comparators A and B, the output flip-flop is set at every period to the value of EDPOL bit.

To temporarily change from the curent duty cycle to 0% and then return to the current duty cycle, the sequence is the following:

- 1. If not currently stored, store value of register A.
- 2. Set A=B.
- 3. If immediate 0% duty cycle is desired, set FORCA=1.
- 4. To return to the previous duty cycle, restore register A with its former value.

100% duty cycle is possible by writing 0x000000 to register A. When a match occurs, the output flip-flop is  set  at  every  period  to  the  complement  of  EDPOL  bit.  The  transfer  from  register  B2  to  B1  is  still controlled by MODE[6] bit.

To temporarily change from the current duty cycle to 100% and then return to the current duty cycle, the sequence is the following:

- 1. If not currently stored, store value of register A.
- 2. Set A=0.
- 3. If immediate 100% duty cycle is desired, set FORCB=1.
- 4. To return to the previous duty cycle, restore register A with its former value.

## NOTE

Updates to  the  A  register  will  always  occur  immediately.  If  next  period update is selected via the mode[6] bit, only the B register update is delayed until the next period.

Figure 17-31 shows the unified channel running in OPFWM mode with immediate register update and Figure 17-32 shows the unified channel running in OPFWM mode with next period update PFWM mode. In  both  figures  EDPOL  =  1,  so  the  output  is  low  during  the  duty  cyle.  Table 17-14  has  additional illustrative examples.

<!-- image -->

- 1
- 2 Writing EMIOS\_B n writes to B2.

Notes: Writing EMIOS\_A n writes to A2.

A2 value transferred to A1 according to OU n bit.

B2 value transferred to B1 according to OU n bit.

Figure 17-31. OPWFM with Immediate Update

<!-- image -->

Notes:

- 1 Writing EMIOS\_A n writes to A2.
- 2 Writing EMIOS\_B n writes to B2.

A2 value transferred to A1 according to OU n bit.

B2 value transferred to B1 according to OU n bit.

Figure 17-32. OPWFM with Next Period Update

Table 17-14. Examples of Output Waveforms

| EDPOL                 | Duty Cycle   |   A (decimal) |   B (decimal) | Waveform   |
|-----------------------|--------------|---------------|---------------|------------|
| 0 (active high ouput) | 0%           |          1000 |          1000 | L H        |
| 0 (active high ouput) | 25%          |           250 |          1000 | L H        |
| 0 (active high ouput) | 50%          |           500 |          1000 | L H        |
| 0 (active high ouput) | 75%          |           750 |          1000 | L H        |
| 0 (active high ouput) | 100%         |             0 |          1000 | L H        |
| 1 (active low ouput)  | 0%           |          1000 |          1000 | L H        |
| 1 (active low ouput)  | 25%          |           250 |          1000 | L H        |
| 1 (active low ouput)  | 50%          |           500 |          1000 | L H        |
| 1 (active low ouput)  | 75%          |           750 |          1000 | L H        |
| 1 (active low ouput)  | 100%         |             0 |          1000 | L H        |

## 17.4.4.4.13 Center Aligned Output Pulse Width Modulation with Dead-time Mode (OPWMC)

This operating mode generates a center aligned PWM with dead time insertion in the leading or trailing edge.

The selected counter bus must be running an up/down time base, as shown in Figure 17-30. BSL[0:1] bits select the time base. Register A1 contains the ideal duty cycle for the PWM signal and is compared with the selected time base. Register B1 contains the dead time value and is compared with the internal counter. For a leading edge dead time insertion, the output PWM duty cycle is equal to the difference between register A1 and register B1, and for a trailing edge dead time insertion, the output PWM duty cycle is equal

to the sum of register A1 and register B1. MODE[6] bit selects between trailing and leading dead time insertion, respectively.

## NOTE

It is recommended that the internal prescaler of the OPWMCB channel be set  to  the  same  value  as  the  MCB  channel  prescaler,  and  the  prescalers should  also  be  synchronized.  This  allows  the  A1  and  B1  registers  to represent the same time scale for duty cycle and dead time insertion.

When operating with leading edge dead time insertion, the first match between A1 and the selected time base clears the internal counter and switches the selected time base to the internal counter. When a match occurs between register B1 and the selected time base, the output flip-flop is set to the value of the EDPOL bit and the time base is switched to the selected counter bus. In the next match between register A1 and the selected time base, the output flip-flop is set to the complement of the EDPOL bit. This sequence repeats continuously.

When operating with trailing edge dead time insertion, the first match between A1 and the selected time base sets the output flip-flop to the value of the EDPOL bit. In the next match between register A1 and the selected time base, the internal counter is cleared and the selected time base is switched to the internal counter. When a match occurs between register B1 and the selected time base, the output flip-flop is set to the complement of the EDPOL bit and the time base is switched to the selected counter bus. This sequence repeats continuously.

FLAG can be generated in the trailing edge of the output PWM signal when MODE[5] is cleared, or in both edges, when MODE[5] is set.

At any time, the FORCMA or FORCMB bits are equivalent to a successful comparison on comparator A or B with the exception that the FLAG bit is not set.

## NOTE

When  in  freeze  mode,  the  FORCMA  or  FORCMB  bits  only  allow  the software to force the output flip-flop to the level corresponding of a match on A or B respectively.

If  subsequent  matches  occur  on  comparators  A  and  B,  the  PWM  pulses  continue  to  be  generated, regardless of the state of the FLAG bit.

In order to achieve a duty cycle of 100%, both registers A1 and B1 must be set to the same value. When a simultaneous match occurs between the selected time base and registers A1 and B1, the output flip-flop is set at every period to the value of EDPOL bit and the selected time base switches to the selected counter bus, allowing a new cycle to begin at any time, as previously described. 0% duty cycle is possible by writing 0x000000 to register A. When a match occurs, the output flip-flop is set at every period to the complement of EDPOL bit and the selected time base switches to the selected counter bus, allowing a new cycle  to  begin  at  any  time,  as  previously  described.  In  both  cases,  FLAG  is  generated  regardless  of MODE[5] bit.

## NOTE

If  A1  and  B1  are  set  to  the  0x000000,  a  0%  duty  cycle  waveform  is produced.

## NOTE

Any updates to the A or B register will take place immediately.

Figure 17-33 and Figure 17-34 show the unified channel running in OPWMC with leading and trailing dead time, respectively.

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

<!-- image -->

Notes:

- 1 Writing EMIOS\_A n writes to A2.
- 2 Writing EMIOS\_B n writes to B1.

A2 value transferred to A1 according to OU n bit.

B2 value transferred to B1 according to OU n bit.

Figure 17-33. Output PWMC with Leading Dead-time Insertion

<!-- image -->

Notes:

1 Writing EMIOS\_A n writes to A2.

2 Writing EMIOS\_B n writes to B1.

A2 value transferred to A1 according to OU n bit.

B2 value transferred to B1 according to OU n bit.

Figure 17-34. Output PWMC with Trailing Dead-time Insertion

## 17.4.4.4.14 Output Pulse Width Modulation Mode (OPWM)

Registers  A1  and  B1  define  the  leading  and  trailing  edges  of  the  PWM  output  pulse,  respectively. MODE[6]  bit  controls  the  transfer  from  register  B2  to  B1,  which  can  be  done  either  immediately (MODE[6] cleared), providing the fastest change in the duty cycle, or at every match of  register  A1 (MODE[6] set).

The value loaded in register A1 is compared with the value on the selected time base. When a match on comparator A occurs, the output flip-flop is set to the value of the EDPOL bit. When a match occurs on comparator B, the output flip-flop is set to the complement of the EDPOL bit.

FLAG can be generated at match B, when MODE[5] is cleared, or in both matches, when MODE[5] is set.

At any time, the FORCMA and FORCMB bits allow the software to force the output flip-flop to the level corresponding to a match on A or B respectively. Note that FLAG bit is not set by the FORCMA and FORCMB operations.

If  subsequent  matches  occur  on  comparators  A  and  B,  the  PWM  pulses  continue  to  be  generated, regardless of the state of the FLAG bit.

In  order  to  achieve  0%  duty  cycle,  both  registers  A1  and  B1  must  be  set  to  the  same  value.  When  a simultaneous match on comparators A and B occur, the output flip-flop is set at every period to the value of EDPOL bit. 0% duty cycle is possible by writing 0x000000 to register A. When a match occurs, the output flip-flop is set at every period to the complement of EDPOL bit. The transfer from register B2 to B1 is still controlled by MODE[6] bit.

## NOTE

If  A1  and  B1  are  set  to  the  0x000000,  a  100%  duty  cycle  waveform  is produced.

## NOTE

Updates to  the  A  register  will  always  occur  immediately.  If  next  period update is selected via the mode[6] bit, only the B register update is delayed until the next period.

Figure 17-35 and Figure 17-36 show the unified channel running in OPWM with immediate update and next period update, respectively.

<!-- image -->

Notes:

- 1 Writing EMIOS\_A n writes to A2.

2 Writing EMIOS\_B n writes to B2.

A2 value transferred to A1 according to OU n bit.

B2 value transferred to B1 according to OU n bit.

Figure 17-35. Output PWM with Immediate Update

<!-- image -->

Notes:

1 Writing EMIOS\_A n writes to A2.

2 Writing EMIOS\_B n writes to B2.

A2 value transferred to A1 according to OU n bit.

B2 value transferred to B1 according to OU n bit.

Figure 17-36. Output PWM with Next Period Update

## 17.4.4.4.15 Modulus Counter, Buffered Mode (MCB) (MPC5553 Only)

The MCB mode provides a time base which can be shared with other channels through the internal counter buses. Register A1 is double buffered, thus allowing smooth transitions between cycles when changing the A2 register value on the fly. The A1 register is updated at the cycle boundary, which is defined as when the internal counter reaches the value one. Note that the internal counter values are within a range from one up to register A1 value in MCB mode.

The MODE[6] bit selects the internal clock source if clear or external if set. When an external clock is selected, the channel input pin is used as the channel clock source. The active edge of this clock is defined by EDPOL and EDSEL bits in the EMIOS\_CCR channel register.

When  entering  the  MCB  mode,  if  up  counter  is  selected  (MODE[4] = 0),  the  internal  counter  starts counting up from its current value to until an A1 match occurs. On the next system clock cycle after an A1 match occurs, the internal counter is set to one and the counter continues counting up. If up/down mode is selected (MODE[4] = 1), the counter changes direction at the A1 match and counts down until it reaches one and is then set to count up again. In this mode B1 is set to one and cannot be changed, as it is used to generate a match to switch from down count to up count.

Note that versus the MC mode, the MCB mode counts between one and the A1 register value. The counter cycle period in up count mode is equal to the A1 value. In up/down counter mode the period is defined by the formula: (2 × A1) - 2.

Figure 17-37 illustrates the counter cycle for several A1 values. Register A1 is loaded with the A2 value at the cycle boundary. Thus any value written to A2 within cycle ( n ) will be updated to A1 at the next cycle boundary, and therefore will be used on cycle ( n +1). The cycle boundary between cycle ( n ) and cycle ( n +1) is defined as the first clock cycle of cycle ( n +1). Note that flags are set when A1 matches occur.

Figure 17-37. eMIOS MCB Mode Example - Up Operation

<!-- image -->

## NOTE

If a prescaler greater than 1 is used, there are several system clock cycles between when the flag is asserted and the counter is set to one. This should be considered when the A value is changed in every cycle, because A1 is updated on the cycle boundary, which is after the flag is set.

Figure 17-38 illustrates the MCB up/down counter mode. The A1 register is updated at the cycle boundary. If A2 is written in cycle ( n ), this new value will be used in cycle ( n +1) for the next A1 match.

Flags are generated only at an A1 match if MODE[5] is 0. If MODE[5] is 1, flags are also generated at the cycle boundary.

Figure 17-38. eMIOS MCB Mode Example - Up/Down Operation

<!-- image -->

Figure 17-39 provides a more detailed illustration of the A1 update process in up counter mode. The A1 load signal is generated based on the detection of the internal counter reaching one, and has the duration of one system clock cycle. Note that during the load pulse A1 still holds its previous value. It is actually updated at the second system clock cycle.

<!-- image -->

A2

value transferred to

A1 according to OU

n

bit.

Figure 17-39. eMIOS MCB Mode Example - Up Operation A1 Register Update

Figure 17-40 illustrates the A1 register update process in up/down counter mode. Note that A2 can be written at any time within cycle ( n ) in order to be used in cycle ( n +1). Thus A1 receives the new value at the next cycle boundary. The EMIOS\_OUDR[n] bits can be used to disable the update of A1 register.

<!-- image -->

A2 value transferred to A1 according to OU n bit (the transfer is triggered by the A1 load signal)

Figure 17-40. eMIOS MCB Mode Example - Up/Down Operation A1 Register Update

## 17.4.4.4.16 Output Pulse Width and Frequency Modulation, Buffered Mode (OPWFMB) (MPC5553 Only)

This mode generates waveforms with variable duty cycle and frequency. The internal channel counter is automatically selected as the time base, A1 sets the duty cycle and B1 determines the frequency. Both A1 and B1 are double buffered to allow smooth signal generation when changing the register values on the fly. 0% and 100% duty cycles are supported.

In  order  to  provide  smooth  and  consistent  channel  operation,  this  mode  differs  substantially  from  the OPWFM mode. The main differences are in how A1 and B1 are updated, the delay from the A1 match to the output flip-flop transition, and the range of the internal counter which ranges from 1 up to B1 value.

When a match on comparator A occurs, the output register is set to the value of EDPOL. When a match on comparator B occurs, the output register is set to the complement of EDPOL. A B1 match also causes the internal counter to transition to 1, thus re-starting the counter cycle.

Figure 17-41 shows an example of OPWFMB mode operation. Note that the output flip-flop transition occurs when the A1 or B1 match signal is negated, as detected by the negative edge of the A1 and B1 match signals. For example, if register A1 is set to 0x000004, the output flip-flop transitions 4 counter periods after the cycle starts, plus one system clock cycle. Note that in the example shown in Figure 17-41 the prescaler ratio is set to two (refer to Section 17.5.3, 'Time Base Generation).

Figure 17-41. eMIOS OPWFMB Mode Example - A1/B1 Match to Output Register Delay

<!-- image -->

Figure 17-42 shows the generated output signal if A1 is 0. Since the counter does not reach zero in this mode, the channel internal logic infers a match as if A1 = 1, with the difference that in this case the positive edge of the match signal is used to trigger the output flip-flop transition instead of the positive edge that is used when A1 = 1. Note that the A1 positive edge match signal from cycle ( n +1) occurs at the same time as the B1 match negative edge from cycle ( n ). This allows the use of the A1 match positive edge to mask the B1 match negative edge when they occur at the same time. The result is that no transition occurs on the output flip-flop, and a 0% duty cycle is generated.

<!-- image -->

EDPOL = 0

Figure 17-42. eMIOS OPWFMB Mode Example - A1 = 0 (0% Duty Cycle)

Figure 17-43 shows the timing for the A1 and B1 loading. A1 and B1 use the same signal to trigger a load, which is generated based on the selected counter reaching one. This event is defined as the cycle boundary. The load signal pulse has the duration of one system clock cycle and occurs at the first system clock period of every cycle of the counter. If A2 and B2 are written within cycle ( n ), their values are loaded into A1 and B1, respectively, at the first clock of cycle ( n +1). The update disable bits, EMIOS\_OUDR, can be used to control the update of these registers, thus allowing the delay of A1 and B1 update for synchronization purposes.

During the load pulse A1 still holds its old value, which is updated on the following system clock cycle. During the A1 load pulse, an internal by-pass allows the use of A2 instead of A1 for matches if A2 is either 0 or 1, thus allowing matches to be generated even when A1 is being loaded. This approach allows a uniform channel operation for any A2 value, including 1 and 0.

In Figure 17-43 it is assumed that the channel and global prescalers are set to one, meaning that the channel internal counter transition at every system clock cycle. FLAGs can be generated only on B1 matches when MODE[5] is cleared, or on both A1 and B1 matches when MODE[5] is set. Since B1 FLAG occurs at the cycle boundary, this flag can be used to indicate that A2 or B2 data written on cycle ( n ) were loaded to A1 or B1, respectively, thus generating matches in cycle ( n +1).

Figure 17-43. eMIOS OPWFMB Mode Example - A1/B1 Updates and Flags

<!-- image -->

Figure 17-44 shows the operation of the output disable feature in OPWFMB mode. Unlike OPWFM mode, the output disable forces the channel output flip-flop to the EDPOL bit value. This functionality targets applications that use active high signals and a high to low transition at A1 match. For such cases EDPOL should be 0.

Figure 17-44. eMIOS OPWFMB Mode Example - Active Output Disable

<!-- image -->

Note that the output disable has a synchronous operation, meaning that the assertion of the output disable input signal causes the channel output flip-flop to transition to EDPOL at the next system clock cycle. If the output disable input is negated, the output flip-flop transitions at the following A1 or B1 match.

In Figure 17-44 it is assumed that the output disable input is enabled and selected for the channel (refer to Section 17.3.1.7, 'eMIOS Channel Control Register (EMIOS\_CCRn),' for a detailed description of the ODIS and ODISSL bits and selection of the output disable inputs).

The  FORCMA  and  FORCMB  bits  allow  the  software  to  force  the  output  flip-flop  to  the  level corresponding to a match on comparators A or B respectively. Similar to a B1 match, FORCMB clears the internal counter. The FLAG bit is not set when the FORCMA or FORCMB bits are set.

Figure 17-45 illustrates the generation of 100% and 0% duty cycle signals. It is assumed that EDPOL = 0 and the prescaler ratio is 1. Initially A1 = 0x000008 and B1 = 0x000008. In this case, a B1 match has precedence over an A1 match, thus the output flip-flop is set to the complement of EDPOL. This cycle corresponds to a 100% duty cycle signal. The same output signal can be generated for any A1 value greater than or equal to B1.

Figure 17-45. eMIOS OPWFMB Mode Example - 100% to 0% Duty Cycle

<!-- image -->

A  0%  duty  cycle  signal  is  generated  if  A1 = 0  as  shown  in  Figure 17-45  cycle  9.  In  this  case  the B1 = 0x000008 match from cycle 8 occurs at the same time as the A1 = 0x000000 match from cycle 9. Refer to Figure 17-42 for a description of A1 and B1 match generation for a case where A1 match has precedence over B1 match and the output signal transitions to EDPOL.

## 17.4.4.4.17 Center Aligned Output Pulse Width Modulation, Buffered Mode (OPWMCB) (MPC5553 Only)

This mode generates a center aligned PWM with dead time insertion on the leading or trailing edge. A1 and B1 registers are double buffered to allow smooth output signal generation when changing A2 or B2 values on the fly.

The selected counter bus for a channel configured to OPWMCB mode must be another channel running in MCB up/down counter mode (refer to Section 17.4.4.4.15, 'Modulus Counter, Buffered Mode (MCB) (MPC5553 Only)'). Register A1 contains the ideal duty cycle for the PWM signal and is compared with the selected time base. Register B1 contains the dead time value and is compared against the internal counter. For a leading edge dead time insertion, the output PWM duty cycle is equal to the difference between register A1 and register B1, and for a trailing edge dead time insertion, the output PWM duty

cycle is equal to the sum of register A1 and register B1. The MODE[6] bit selects between trailing and leading dead time insertion, respectively.

## NOTE

It is recommended that the internal prescaler of the OPWMCB channel be set  to  the  same  value  as  the  MCB  channel  prescaler,  and  the  prescalers should  also  be  synchronized.  This  allows  the  A1  and  B1  registers  to represent the same time scale for duty cycle and dead time insertion.

Figure 17-46 illustrates loading of the A1 and B1 registers, which occurs when the selected counter bus reaches the value one. This counter value defines the cycle boundary. Values written to A2 or B2 within cycle ( n ) are loaded into A1 or B1 registers and are used to generate matches in cycle (n+1).

Figure 17-46. eMIOS OPWMCB Mode Example - A1/B1 Register Loading

<!-- image -->

The EMIOS\_OUDR[n] bit can be used to disable the A1 and B1 updates, thus allowing the loading of these registers to be synchronized with the load of A1 or B1 registers in others channels. Note that by using the update disable bit, the A1 and B1 registers can be updated in the same counter cycle.

In this mode A1 matches set the internal counter to one. When operating with leading edge dead time insertion,  the  first  A1  match  resets  the  internal  counter  to  0x000001.  When  a  match  occurs  between register B1 and the internal time base, the output flip-flop is set to the value of the EDPOL bit. In the following match between A1 and the selected time base, the output flip-flop is set to the complement of the EDPOL bit. This sequence repeats continuously. Figure 17-47 shows two cycles of a center aligned PWM signal. Note that both A1 and B1 register values are changing within the same cycle, which allows the duty cycle and dead time values to be changed at simultaneously.

Figure 17-47. eMIOS PWMCB Mode Example - Lead Dead Time Insertion

<!-- image -->

As shown in Figure 17-48, when operating with trailing edge dead time insertion the first match between A1 and the selected time base sets the output flip-flop to the value of the EDPOL bit and resets the internal counter to 0x000001. In the second match between register A1 and the selected time base, the internal counter is reset to 0x000001 and B1 matches are enabled. When the match between register B1 and the selected time base occurs the output flip-flop is set to the complement of the EDPOL bit. This sequence repeats continuously.

<!-- image -->

EDPOL = 1

Figure 17-48. eMIOS PWMCB Mode Example - Trailing Dead Time Insertion

FLAG can be generated in the trailing edge of the output PWM signal when MODE[5] is cleared, or on both edges when MODE[5] is set. If subsequent matches occur on A and B, the PWM pulses continue to be generated, regardless of the state of the FLAG bit.

## NOTE

In  OPWMCB  mode,  FORCMA  and  FORCMB  do  not  have  the  same behavior  as  a  regular  match.  Instead  they  force  the  output  flip-flop  to  a constant value which depends upon the selected dead time insertion mode, lead or trail and the value of the EDPOL bit.

FORCMA has different behaviors depending on the selected dead time insertion mode. In leading dead time insertion mode, writing one to FORCMA sets the output flip-flop to the compliment of EDPOL. In trailing dead time insertion mode, the output flip-flop is forced to the value of EDPOL.

If FORCMB is set, the output flip-flop value depends on the selected dead time insertion mode. In leading dead time insertion mode, FORCMB sets the output flip-flop to the value of EDPOL. In trailing dead time insertion mode, the output flip-flop is forced to the compliment of EDPOL.

## NOTE

Setting the FORCMA bit does not reset the internal time base to 0x000001 as  a  regular  A1  match  does.  FORCMA  and  FORCMB  have  the  same behavior  even  in  freeze  or  normal  mode  regarding  the  output  flip-flop transition.

The FLAG bit is not set in the case of the FORCMA, FORCMB or both bits being set at the same time.

When FORCMA and FORCMB are both set, the output flip-flop is set to the compliment of the EDPOL bit. This is equivalent to FORCMA having precedence over FORCMB when lead dead time insertion is selected and FORCMB having precedence over FORCMA when trailing dead time insertion is selected.

Duty cycles from 0% to 100% can be generated by setting appropriate A1 and B1 values relative to the period of the external time base. Setting A1 = 1  generates  a 100%  duty  cycle  waveform.  If A1 &gt; period ÷ 2, where period refers to the selected counter bus period, then a 0% duty cycle is produced. Assuming EDPOL is one and OPWMCB mode with trailing dead time insertion mode is selected, 100% duty cycle signals can be generated if B1 occurs at or after the cycle boundary (external counter = 1).

## NOTE

A special case occurs when A1 is set to the external counter bus period ÷ 2, which is the maximum value of the external counter. In this case the output flip-flop is constantly set to the EDPOL bit value.

Internal channel logic prevents matches from one cycle to propagate to the next cycle. In trailing dead time insertion mode, a B1 match from cycle ( n ) could eventually cross the cycle boundary and occur in cycle (n+1).  In  this  case  the  B1  match  is  masked  out  and  does  not  cause  the  output  flip-flop  to  transition. Therefore matches in cycle (n+1) are not affected by the late B1 matches from cycle ( n ).

Figure 17-49 shows a 100% duty cycle output signal generated by setting A1 = 4 and B1 = 3. In this case the trailing edge is positioned at the boundary of cycle (n+1), which is actually considered to belong to cycle (n+2) and therefore does not cause the output flip-flip to transition.

Figure 17-49. eMIOS PWMCB Mode Example - 100% Duty Cycle (A1 = 4, B1 = 3)

<!-- image -->

The output disable input, if enabled, causes the output flip-flop to transition to the compliment of EDPOL. This allows to the channel output flip-flop to be forced to a safety state. The internal channel matches continue to occur in this case, thus generating flags. When the output disable is negated, the channel output flip-flop is again controlled by A1 and B1 matches. This process is synchronous, meaning that the output channel pin transitions only occur on system clock edges.

It is important to note that, like in OPWMB and OPWFMB modes, the match signal used to set or clear the channel output flip-flop is generated on the negation of the channel comparator output signal which compares the selected time base with A1 or B1. Refer to Figure 17-41, which illustrates the delay from matches to output flip-flop transition in OPWFMB mode.

## 17.4.4.4.18 Output Pulse Width Modulation, Buffered Mode (OPWMB) (MPC5553 Only)

OPWMB mode is used to generate pulses with programmable leading and trailing edge placement. An external counter is selected from one of the counter buses. The A1 register value defines the first edge and B1 defines the second edge. The output signal polarity is defined by the EDPOL bit. If EDPOL is zero, a negative edge occurs when A1 matches the selected counter bus and a positive edge occurs when B1 matches the selected counter bus.

The A1 and B1 registers are double buffered and updated from A2 and B2, respectively, at the cycle boundary.  The  load  operation  is  similar  to  the  OPWFMB  mode.  Refer  to  Figure 17-43  for  more information on A1 and B1 register updates.

Flags  are  generated  at  B1  matches  when  MODE[5]  is  cleared,  or  on  both  A1  and  B1  matches  when MODE[5] is set. If subsequent matches occur on comparators A and B, the PWM pulses continue to be generated regardless of the state of the FLAG bit.

The FORCMA and FORCMB bits allow software to force the output flip-flop to the level corresponding to a match on A1 or B1 respectively. FLAG is not set by the FORCMA and FORCMB operations.

The following rules apply to the OPWMB mode:

- · B1 matches have precedence over A1 matches if they occur at the same time within the same counter cycle.
- · A1 = 0 match from cycle ( n ) has precedence over a B1 match from cycle (n-1).
- · A1 matches are masked if they occur after a B1 match within the same cycle.
- · Values written to A2 or B2 on cycle ( n ) are loaded to A1 or B1 at the following cycle boundary (assuming EMIOS\_OUDR[ ] is not asserted). Thus the new values will be used for A1 and B1 n matches in cycle ( n +1).

Figure 17-50 illustrates operation in OPWMB mode with A1/B1 matches and the transition of the channel output flip-flop. In this example EDPOL is zero.

Figure 17-50. eMIOS OPWMB Mode Example - Matches and Flags

<!-- image -->

Note that the output flip-flop transitions are based on the negative edges of the A1 and B1 match signals. Figure 17-50 shows the value of A1 being set to zero in cycle (n+1). In this case the match positive edge is used instead of the negative edge to transition the output flip-flop.

Figure 17-51 illustrates the channel operation for 0% duty cycle. Note that the A1 match signal positive edge occurs at the same time as the B1 = 8 signal negative edge. In this case the A1 match has precedence over the B1 match, causing the output flip-flop to remain at the EDPOL value, thus generating a 0% duty cycle.

Figure 17-51. eMIOS OPWMB Mode Example - 0% Duty Cycle

<!-- image -->

Figure 17-52 shows the operation of the OPWMB mode with the output disable signal asserted. The output disable  forces  a  transition  in  the  output  flip-flop  to  the  EDPOL  bit  value.  After  the  output  disable  is negated, the output flip-flop is allowed to transition at the next A1 or B1 match. The output disable does not modify the flag bit behavior. Note that there is one system clock delay between the assertion of the output disable signal and the transition of the output flip-flop.

Figure 17-52. eMIOS OPWMB Mode Example - Active Output Disable

<!-- image -->

Figure 17-53 shows a waveform changing from 100% to 0% duty cycle. In this case EDPOL is zero and B1 is set to the same value as the period of the selected external time base.

Figure 17-53. eMIOS OPWMB Mode Example - 100% to 0% Duty Cycle

<!-- image -->

In Figure 17-53 if B1 is set to a value lower than 0x000008 it is not possible to achieve 0% duty cycle by only changing A1 register value. Since B1 matches have precedence over A1 matches, the output flip-flop transitions to the compliment of EDPOL at B1 matches. In this example, if B1 = 0x000009, a B1 match does not occur, and thus a 0% duty cycle signal is generated.

## 17.5 Initialization / Application Information

Upon reset all of the unified channels of the eMIOS default to general purpose inputs (GPIO input mode).

## 17.5.1 Considerations on Changing a UC Mode

Before changing an operating mode, the UC must be programmed to GPIO mode, and EMIOS\_CADR n and EMIOS\_CBDR  must be updated with the correct values for the next operating mode. Then the n EMIOS\_CCR  can be written with the new operating mode. If a UC is changed from one mode to another n without performing this procedure, the first operating cycle of the selected time base is unpredictable.

## NOTE

When interrupts are enabled and an interrupt is generated, the FLAG bits should be cleared before exiting the interrupt service routine.

## 17.5.2 Generating Correlated Output Signals

Correlated output signals can be generated by all output operating modes. Bits ODIS n can be used to control the update of these output signals.

In order to guarantee that the internal counters of correlated channels are incremented in the same clock cycle, the internal prescalers must be set up before enabling the global prescaler. If the internal prescalers are set after enabling the global prescaler, the internal counters may increment in the same ratio, but at a different clock cycle.

When an output disable condition occurs, the software interrupt routine must service the output channels before servicing the channels running SAIC. This procedure avoid glitches in the output pins.

## 17.5.3 Time Base Generation

For all channel operation modes that generate a time base (MC, OPWFM, OPWM, MCB, OPWFMB and OPWMB), the clock prescaler can use several ratios calculated as:

```
Ratio GPRE + 1 ( ) × ( UCPRE + 1 ) =
```

The prescaled clocks in Figure 17-55, Figure 17-56, and Figure 17-57 illustrate this ratio. For example, if the ratio is 1, the prescaled clock is high and continuously enables the internal counter (EMIOS\_CCNTR n ) (Figure 17-55); if the ratio is 3, then it pulses every 3 clock cycles (Figure 17-56) and the internal counter increments every 3 clock  cycles; if the ratio is 9, it pulses every 9 clock cycles, etc. This high pulse enables the EMIOS\_CCNTR  to increment as long as no other conditions disable this counter. The match signal n is generated by pulsing every time the internal counter matches the programmed match value. Note that for the same programmed match value, the period is shorter when using a prescaler ratio greater than one.

Figure 17-54. eMIOS Time Base Generation Block Diagram

<!-- image -->

NOTE: The period of the time base includes the match value. When a match occurs, the first clock cycle is used to clear the internal counter, starting another period

<!-- image -->

Figure 17-55. eMIOS Time Base Example - Fastest Prescaler Ratio

<!-- image -->

NOTE: The period of the time base does not include the match value. When a match occurs, the first clock cycle is used to clear the internal counter, starting another period

Figure 17-56. eMIOS Time Base Example - Prescale Ratio = 3, Match Value = 3

## Enhanced Modular Input/Output Subsystem (eMIOS)

NOTE: The period of the time base does not include the match value. When a match occurs, the first clock cycle is used to clear the internal counter, starting another period

<!-- image -->

Figure 17-57. eMIOS Time Base Example - Prescale Ratio = 2, Match Value = 5

## 17.6 Revision History

## Substantive Changes since Rev 3.0

- GLYPH&lt;127&gt; Corrected footnote in MC, OPWM, OPWFM, and OPWMC mode figures.
- GLYPH&lt;127&gt; Added note regarding FORCMA and FORMCB bits having no effect in some modes.
- GLYPH&lt;127&gt; Added note regarding immediate update of A register in OPW and OPWFM modes.
- GLYPH&lt;127&gt; Added noteregarding immediate update of A register in MC mode.
- GLYPH&lt;127&gt; Added note regarding immediate update of A and B registers in OPWMC mode.

Added note to BSL bit definition 'In certain modes the internal counter is used internally and therefore cannot be used as the channel time base.'

Added Section 17.4.4.4.1, 'General Purpose Input/Output Mode (GPIO).'
