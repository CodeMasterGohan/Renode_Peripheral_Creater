### Chatper 4 Reset

## 4.1 Introduction

The following reset sources are supported in the MPC5553/MPC5554 MCU:

- · Power-on reset
- · External reset
- · Loss-of-lock reset
- · Loss-of-clock reset
- · Watchdog timer/debug reset
- · JTAG reset
- · Checkstop reset
- · Software system reset
- · Software external reset

All reset sources are processed by the reset controller, which is located in the SIU module. The reset controller monitors the reset input sources, and upon detection of a reset event, resets internal logic and controls the assertion of the RSTOUT pin. The RSTOUT signal may be automatically asserted by writing the SER bit in the SIU\_SRCR to 1. The RSTOUT signal will stay asserted for a number of system clocks 1 determined by the configuration of the PLL (See Section 4.2.2, 'Reset Output (RSTOUT)'). This does not reset the MPC5553/MPC5554 MCU. All other reset sources initiate an internal reset of the MCU.

For all reset sources, the BOOTCFG[0:1] and PLLCFG[0:1] signals can be used to determine the boot mode and the configuration of the FMPLL, respectively. If the RSTCFG pin is asserted during reset, the values on the BOOTCFG[0:1] pins are latched in the SIU\_RSR 4 clock cycles prior to the negation of the RSTOUT pin, determining the boot mode. The values on the PLLCFG[0:1] pins are latched at the negation of the RSTOUT pin, determining the configuration of the FMPLL. If the RSTCFG pin is negated during reset, the FMPLL defaults to normal operation (PLL enabled) with a crystal reference and the boot mode (latched in the SIU\_RSR) is defaulted to internal boot from Flash.

The reset status register (SIU\_RSR) gives the source of the last reset and indicates whether a glitch has occurred on the RESET pin. The SIU\_RSR is updated for all reset sources.

All reset sources initiate execution of the MPC5553/MPC5554 boot assist module (BAM) program with the exception of the software external reset.

The reset configuration half word (RCHW) provides several basic functions at reset. It provides a means to locate the boot code, determines if Flash memory is programmed or erased, enables or disables the watchdog timer, and if booting externally, sets the bus size. The location of the RCHW is specified by the state of the BOOTCFG[0:1] pins. These pins determine whether the RCHW is located in internal Flash, located in external memory, or whether a serial or CAN boot is configured. A complete description of the BOOTCFG[0:1] pins may be found in Chapter 2, 'Signal Description.' The BAM program reads the values of the BOOTCFG[0:1] pins from the BOOTCFG field of the SIU\_RSR, then reads the RCHW from the specified location and uses the RCHW value to determine and execute the specified boot procedure. See Section 4.4.3, 'Reset Configuration and Configuration Pins,' for a complete description.

1.  Unless noted otherwise, the use of 'clock' or 'clocks' in this section is a reference to the system clock.

## 4.2 External Signal Description

## 4.2.1 Reset Input (RESET)

The RESET pin is an active low input that is asserted by an external device during a power-on or external reset. The internal reset signal asserts only if the RESET pin is asserted for 10 clock cycles. Assertion of the RESET pin while the device is in reset causes the reset cycle to start over. The RESET pin also has an associated glitch detector which detects spikes greater than 2 clocks in duration that fall below the switch point of the input buffer logic.

## 4.2.2 Reset Output (RSTOUT)

The RSTOUT pin is an active low output that uses a push/pull configuration. The RSTOUT pin is driven to the low state by the MCU for all internal and external reset sources.

After the negation of the RESET input, if the PLL is configured for 1:1 (dual controller) mode or bypass mode, the RSTOUT signal is asserted for 16000 clocks, plus 4 clocks for sampling of the configuration pins. If the PLL is configured for any other operating mode, the RSTOUT signal is asserted for 2400 clocks,  plus  4  clocks  for  sampling  of  the  configuration  pins.  See  Section 11.1.4,  'FMPLL  Modes  of Operation' for details of PLL configuration.

The RSTOUT pin can also be asserted by a write to the SER bit of the system reset control register (SIU\_SRCR).

## NOTE

During a power on reset, RSTOUT is three-stated.

## 4.2.3 Reset Configuration (RSTCFG)

The RSTCFG input is used to enable the BOOTCFG[0:1] and PLLCFG[0:1] pins during reset. If RSTCFG is negated during reset, the BOOTCFG and PLLCFG pins are not sampled at the negation of RSTOUT. In that case, the default values for BOOTCFG and PLLCFG are used. If RSTCFG is asserted during reset, the values on the BOOTCFG and PLLCFG pins are sampled and configure the boot and FMPLL modes.

## 4.2.4 Weak Pull Configuration (WKPCFG)

WKPCFG determines whether specified eTPU and EMIOS pins are connected to a weak pull up or weak pull down during and immediately after reset.

## 4.2.5 Boot Configuration (BOOTCFG[0:1])

In the MPC5554, BOOTCFG determines the function and state of the following pins after execution of the BAM reset: CS[0:3], ADDR[12:31], DATA[0:31], TSIZ[0:1], RD\_WR, BDIP, WE[0:3], OE, TS, TA, TEA, BR, BG, BB.

In the MPC5553, BOOTCFG determines the function and state of the following pins after a BAM reset: CS[0:3], ADDR[8:31], DATA[0:31], RD\_WR, BDIP, WE[0:3], OE, TS, TA, TEA, BR, BG, TSIZ[0:1].

Note that BOOTCFG0 does not function in the 208 pin package of the MPC5553.

## 4.3 Memory Map/Register Definition

Table 4-1 summarizes the reset controller registers. The base address of the system integration unit is 0xC3F9\_0000.

Table 4-1. Reset Controller Memory Map

| Address                   | Register Name   | Register Description          |   Size (bits) |
|---------------------------|-----------------|-------------------------------|---------------|
| Base (0xC3F9_000C) + 0xC  | SIU_RSR         | Reset status register         |            32 |
| Base (0xC3F9_000C) + 0x10 | SIU_SRCR        | System reset control register |            32 |

## 4.3.1 Register Descriptions

This section describes all the reset controller registers. It includes details about the fields in each register, the number of bits per field, the reset value of the register, and the function of the register.

## 4.3.1.1 Reset Status Register (SIU\_RSR)

The reset status register (SIU\_RSR) reflects the most recent source, or sources, of reset. This register contains  one  bit  for  each  reset  source.  A  bit  set  to  logic  1  indicates  the  type  of  reset  that  occurred. Simultaneous reset requests cause more than one bit to be set at the same time. Once set, the reset source bits in the SIU\_RSR remain set until another reset occurs. A software external reset causes the SERF bit to be set, but no previously set bits in the SIU\_RSR will be cleared. Additional information about the SIU\_RSR may be found in Section 6.3.1.2, 'Reset Status Register (SIU\_RSR).'

The SIU\_RSR also contains the values latched at the last reset on the WKPCFG and BOOTCFG[0:1] pins and a RESET input pin glitch flag. The reset glitch flag bit (RGF) is cleared by writing a 1 to the bit. A write of 0 has no effect on the bit state. The SIU\_RSR can be read at all times.

<!-- image -->

|          | 0          | 1          | 2          | 3          | 4          | 5          | 6          | 7          | 8          | 9          | 10         | 11         | 12         | 13         | 14         | 15         |
|----------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|
| R        | PORS       | ERS        | LLRS       | LCRS       | WDRS       | CRS        | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | SSRS       | SERF       |
| W        |            |            |            |            |            |            |            |            |            |            |            |            |            |            |            |            |
| Reset 1  | 1          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          |
| Reg Addr | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC |
|          | 16         | 17         | 18         | 19         | 20         | 21         | 22         | 23         | 24         | 25         | 26         | 27         | 28         | 29         | 30         | 31         |
| R        | WKP CFG    | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | BOOTCFG    | BOOTCFG    | RGF        |
| W        |            |            |            |            |            |            |            |            |            |            |            |            |            |            |            |            |
| Reset    | - 2        | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | - 3        |            | 0          |
| Reg Addr | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC | Base + 0xC |

1 The RESET values for this register are defined for power-on reset only.

2 The RESET value of this bit or field is determined by the value latched on the associated pin or pins at the negation of the last reset.

3 The RESET value of this bit or field is determined by the value latched on the associated pin or pins at the negation of the last reset. BOOTCFG can also be loaded with a default instead of what is on the associated pin or pins.

Figure 4-1. Reset Status Register (SIU\_RSR)

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 4-2. SIU\_RSR Field Descriptions

| Bits   | Name    | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
|--------|---------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0      | PORS    | Power-on reset status 0 No power-on reset has occurred. 1 A power-on reset has occurred.                                                                                                                                                                                                                                                                                                                                                                                                                           |
| 1      | ERS     | External reset status 0 No external reset has occurred. 1 An external reset has occurred. The ERS bit is also set during a POR event.                                                                                                                                                                                                                                                                                                                                                                              |
| 2      | LLRS    | Loss-of-lock reset status 0 No loss-of-lock reset has occurred. 1 A loss-of-lock reset has occurred.                                                                                                                                                                                                                                                                                                                                                                                                               |
| 3      | LCRS    | Loss-of-clock reset status 0 No loss-of-clock reset has occurred. 1 A loss-of-clock reset has occurred due to a loss of the reference or failure of the FMPLL.                                                                                                                                                                                                                                                                                                                                                     |
| 4      | WDRS    | Watchdog timer/debug reset status 0 No watchdog timer or debug reset has occurred. 1 A watchdog timer or debug reset has occurred.                                                                                                                                                                                                                                                                                                                                                                                 |
| 5      | CRS     | Checkstop reset status 0 No enabled checkstop reset has occurred. 1 An enabled checkstop reset has occurred.                                                                                                                                                                                                                                                                                                                                                                                                       |
| 6-13   | -       | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 14     | SSRS    | Software system reset status 0 No software system reset has occurred. 1 A software system reset has occurred.                                                                                                                                                                                                                                                                                                                                                                                                      |
| 15     | SERF    | Software external reset flag 0 No software external reset has occurred. 1 A software external reset has occurred.                                                                                                                                                                                                                                                                                                                                                                                                  |
| 16     | WKPCFG  | Weak pull configuration pin status 0 WKPCFGpin latched during the last reset was logic 0 and weak pull down is the default setting. 1 WKPCFG pin latched during the last reset was logic 1 and weak pull up is the default setting.                                                                                                                                                                                                                                                                                |
| 17-28  | -       | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 29-30  | BOOTCFG | Reset configuration pin status. Holds the value of the BOOTCFG[0:1] pins that was latched 4 clocks before the last negation of the RSTOUT pin, if the RSTCFG pin was asserted. If the RSTCFG pin was negated at the last negation of RSTOUT, the BOOTCFG field is set to the value 0b00. The BOOTCFG field is used by the BAM program to determine the location of the reset configuration half word. See Table 4-10 for a translation of the reset configuration half word location from the BOOTCFG field value. |
| 31     | RGF     | RESETglitch flag. Set by the MCUwhentheRESETpinis asserted for more than 2 clocks clock cycles, but less than the minimum RESET assertion time of 10 consecutive clocks to cause a reset. This bit is cleared by the reset controller for a valid assertion of the RESET pin or a power-on reset or a write of 1 to the bit. 0 No glitch was detected on the RESET pin. 1 A glitch was detected on the RESET pin.                                                                                                  |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## 4.3.1.2 System Reset Control Register (SIU\_SRCR)

The system reset control register (SIU\_SRCR) allows software to generate either a software system reset or software external reset. The software system reset causes an internal reset sequence, while the software external  reset  only  causes  the  external  RSTOUT  pin  to  be  asserted.  When  written  to  1,  the  SER  bit automatically  clears  after  a  predetermined  number  of  clock  cycles  (See  Section 4.2.2,  'Reset  Output (RSTOUT)'). If the value of the SER bit is 1 and a 0 is written to the bit, the bit is cleared and the RSTOUT pin is negated regardless of whether the relevant number of clocks has expired.

The CRE bit in the SIU\_SRCR allows software to enable a checkstop reset. If enabled, a checkstop reset will occur if the checkstop reset input to the reset controller is asserted. The checkstop reset is enabled by default.

<!-- image -->

|          | 0           | 1           | 2           | 3           | 4           | 5           | 6           | 7           | 8           | 9           | 10          | 11          | 12          | 13          | 14          | 15          |
|----------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|
| R        | SSR         | SER         | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           |
| W        |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |
| Reset 1  | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           |
| Reg Addr | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 |
|          | 16          | 17          | 18          | 19          | 20          | 21          | 22          | 23          | 24          | 25          | 26          | 27          | 28          | 29          | 30          | 31          |
| R        | CRE         | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           |
| W        |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |
| Reset    | 1 1         | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           |
| Reg Addr | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 | Base + 0x10 |

1 The CRE bit is reset to 1 by POR. Other resets sources do not reset the bit value.

Figure 4-2. System Reset Control Register (SIU\_SRCR)

Table 4-3. SIU\_SRCR Field Descriptions

| Bits   | Name   | Description                                                                                                                                                                                                                                                                                                                                                                                       |
|--------|--------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0      | SSR    | Software system reset. Writing a 1 to this bit causes an internal reset and assertion of the RSTOUT pin. The bit is automatically cleared by all reset sources except the software external reset. 0 Do not generate a software system reset. 1 Generate a software system reset.                                                                                                                 |
| 1      | SER    | Software external reset. Writing a 1 to this bit causes an software external reset. The RSTOUT pin is asserted for a predetermined number of clock cycles (See Section 4.2.2, 'Reset Output (RSTOUT)'), but the MCUisnot reset. The bit is automatically cleared when the software external reset completes. 0 Do not generate an software external reset. 1 Generate an software external reset. |
| 2-15   | -      | Reserved.                                                                                                                                                                                                                                                                                                                                                                                         |

## Reset

Table 4-3. SIU\_SRCR Field Descriptions (continued)

| Bits   | Name   | Description                                                                                                                                                                                                                                                                                                                         |
|--------|--------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 16     | CRE    | Checkstop reset enable Writing a 1 to this bit enables a checkstop reset when the e200z6 core enters a checkstop state. The CRE bit defaults to checkstop reset enabled. This bit is reset at POR. 0 No reset occurs when the e200z6 core enters a checkstop state. 1 A reset occurs when the e200z6 core enters a checkstop state. |
| 17-31  | -      | Reserved.                                                                                                                                                                                                                                                                                                                           |

## 4.4 Functional Description

## 4.4.1 Reset Vector Locations

The reset vector contains a pointer to the instruction where code execution begins after BAM execution. The location of the reset vector is determined by boot mode, as illustrated in Table 4-4.

Table 4-4. Reset Vector Locations

| Boot Mode     | Reset Vector Location                                                                                                                                                                                                                                                             |
|---------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| External Boot | 0x0000_0004 (assuming 0x0000_0000 has a valid RCHW)                                                                                                                                                                                                                               |
| Internal Boot | Next word address after the first valid RCHW found. The BAM searches the lowest address of each of the six low address space blocks in Flash memory for a valid RCHW. Hence, the possible reset vector locations are: 0x0000_0004 0x0000_4004 0x0001_0004 0x0001_C004 0x0002_0004 |
| Serial Boot   | Specified over serial download                                                                                                                                                                                                                                                    |

## 4.4.2 Reset Sources

## 4.4.2.1 FMPLL Lock

A loss of lock of the FMPLL  can cause a reset (provided the SIU is enabled by the FMPLL\_SYNCR[LOLRE] bit). Furthermore, reset will remain asserted, regardless of the source of reset, until after the FMPLL has locked.

## 4.4.2.2 Flash High Voltage

There is no Flash access gating signal implemented in the MPC5553/MPC5554. However, the device is held in reset for a long enough period of time to guarantee that high voltage circuits are reset and stabilized and that Flash memory is accessible.

## 4.4.2.3 Reset Source Descriptions

For the following reset source descriptions refer to the reset flow diagrams in Figure 4-5 and Figure 4-6. Figure 4-5 shows the reset flow for assertion of the RESET pin. Figure 4-6 shows the internal processing of reset for all reset sources.

## 4.4.2.3.1 Power-on Reset

The power-on reset (POR) circuit is designed to detect a POR event and ensure that the RESET signal is correctly sensed. The POR is not intended to be used to detect falling power supply voltages. External supply monitoring should be provided. The output signals from the power-on reset circuits are active low signals. All power-on reset output signals are combined into one POR signal at the V DD  level and input to the reset controller. Although assertion of the power-on reset signal causes reset, the RESET pin must be asserted during a power-on reset to guarantee proper operation of the MCU.

The PLLCFG[0:1] and RSTCFG pins determine the configuration of the FMPLL. If the RSTCFG pin is asserted at the negation of RSTOUT, the PLLCFG[0:1] pins set the operating mode of the FMPLL. If RSTCFG is asserted  anytime  during  the  assertion  of  RSTOUT,  the  FMPLL  will  switch  to  the  mode specified by the PLLCFG[0:1] pins. The values on the RSTCFG and the PLLCFG[0:1] pins must be kept constant once RSTCFG is asserted to avoid transient mode changes in the FMPLL. If RSTCFG is in the negated state at the negation of RSTOUT, the FMPLL defaults to enabled with a crystal reference. See Chapter 11, 'Frequency Modulated Phase Locked Loop (FMPLL) and System Clocks,' for more details on the operation of the FMPLL and the PLLCFG[0:1] pins.

The signal on the WKPCFG pin determines whether weak pull up or pull down devices are enabled after reset on the eTPU and eMIOS pins. The WKPCFG pin is applied starting at the assertion of the internal reset signal, as indicated by the assertion of RSTOUT. Refer to Figure 4-4 and see Chapter 2, 'Signal Description,' for information on WKPCFG and RSTOUT.

Once the RESET input pin is negated, the reset controller checks if the FMPLL is locked. The internal reset signal and RSTOUT are kept asserted until the FMPLL is locked. After the FMPLL is locked, the reset  controller  waits  an  additional  predetermined  number  of  clock  cycles  (See  Section 4.2.2,  'Reset Output (RSTOUT)') before negating the RSTOUT pin. The WKPCFG and BOOTCFG[0:1] pins are sampled 4 clock cycles before the negation of RSTOUT, and the associated bits/fields are updated in the SIU\_RSR (note that the BOOTCFG[0:1] pins are only sampled if RSTCFG is asserted). In addition, the PORS and ERS bits are set, and all other reset status bits are cleared in the reset status register.

## 4.4.2.3.2 External Reset

When the reset controller detects assertion of the RESET pin, the internal reset signal and RSTOUT are asserted. Starting at the assertion of the internal reset signal (as indicated by assertion of RSTOUT), the value on the WKPCFG pin is applied; at the same time the PLLCFG[0:1] values are applied if RSTCFG is asserted. Once the RESET pin is negated and the FMPLL loss of lock request signal is negated, the reset controller waits the predetermined number of clock cycles (see Section 4.2.2, 'Reset Output (RSTOUT)').

Once  the  clock  count  finishes,  the  WKPCFG  and  BOOTCFG[0:1]  pins  are  sampled  (note  that  the BOOTCFG[0:1] pins are only sampled if RSTCFG is asserted). The reset controller then waits 4 clock cycles  before  the  negating  RSTOUT,  and  the  associated  bits/fields  are  updated  in  the  SIU\_RSR.  In addition, the ERS bit is set, and all other reset status bits in the SIU\_RSR are cleared.

## 4.4.2.3.3 Loss-of-Lock Reset

A loss-of-lock reset occurs when the FMPLL loses lock and the loss-of-lock reset enable (LOLRE) bit in the FMPLL synthesizer control register (FMPLL\_SYNCR) is set. The internal reset signal is asserted (as indicated by assertion of RSTOUT). Starting at the assertion of the internal reset signal (as indicated by

## Reset

assertion of RSTOUT), the value on the WKPCFG pin is applied; at the same time the PLLCFG[0:1] values are applied if RSTCFG is asserted. Once the FMPLL locks, the reset controller waits until the predetermined  clock  count  finishes  (See  Section 4.2.2,  'Reset  Output  (RSTOUT)')  and  then  the WKPCFG and BOOTCFG[0:1] pins are sampled (note that the BOOTCFG[0:1] pins are only sampled if RSTCFG is asserted). The reset controller then waits 4 clock cycles before negating RSTOUT, and the associated bits/fields are updated in the SIU\_RSR. In addition, the LLRS bit is set, and all other reset status bits  in  the  SIU\_RSR  are  cleared.  Refer  to  Chapter 11,  'Frequency  Modulated  Phase  Locked  Loop (FMPLL) and System Clocks,' for more information on loss-of-lock.

## 4.4.2.3.4 Loss-of-Clock Reset

A loss-of-clock reset occurs when the FMPLL detects a failure in either the reference signal or FMPLL output, and the loss-of-clock reset enable (LOCRE) bit in the FMPLL\_SYNCR is set. The internal reset signal is asserted (as indicated by assertion of RSTOUT). Starting at the assertion of the internal reset signal (as indicated by assertion of RSTOUT), the value on the WKPCFG pin is applied; at the same time the PLLCFG[0:1] values are applied if RSTCFG is asserted. Once the FMPLL has a clock and is locked, the  reset  controller  waits  the  the  predetermined  clock  cycles  (See  Section 4.2.2,  'Reset  Output (RSTOUT)') before negating RSTOUT. When the clock count finishes the WKPCFG  and BOOTCFG[0:1] pins are sampled (note that the BOOTCFG[0:1] pins are only sampled if RSTCFG is asserted). The reset controller then waits 4 clock cycles before the negating RSTOUT, and the associated bits/fields are updated in the SIU\_RSR. In addition, the LCRS bit is set, and all other reset status bits in the SIU\_RSR are cleared. Refer to Section 11.4.2.6, 'Loss-of-Clock Detection,' for more information on loss-of-clock.

## 4.4.2.3.5 Watchdog Timer/Debug Reset

A watchdog timer reset occurs when the e200z6 core watchdog timer is enabled, and a time-out occurs with the enable next watchdog timer (EWT) and watchdog timer interrupt status (WIS) bits set in the timer status register (TSR), and with the watchdog reset control (WRC) field in the timer control register (TCR) configured for a reset. The WDRS bit in the SIU\_RSR is also set when a debug reset command is issued from a debug tool. To determine whether the WDRS bit was set due to a watchdog timer or debug reset, check the WRS field in the e200z6 core TSR. The effect of a watchdog timer or debug reset request is the same for the reset controller. Starting at the assertion of the internal reset signal (as indicated by assertion of RSTOUT), the value on the WKPCFG pin is applied; at the same time the PLLCFG[0:1] values are applied if RSTCFG is asserted. Once the FMPLL is locked, the reset controller waits the predetermined number of clock cycles (See Section 4.2.2, 'Reset Output (RSTOUT)') before negating RSTOUT.. When the clock count finishes the WKPCFG  and  BOOTCFG[0:1]  pins  are  sampled  (note  that  the BOOTCFG[0:1] pins are only sampled if RSTCFG is asserted). The reset controller then waits 4 clock cycles  before  the  negating  RSTOUT,  and  the  associated  bits/fields  are  updated  in  the  SIU\_RSR.  In addition, the WTRS bit is set, and all other reset status bits in the SIU\_RSR are cleared. Refer to the e200z6 Core Guide for more information on the watchdog timer and debug operation.

## 4.4.2.3.6 Checkstop Reset

When the e200z6 core enters a checkstop state, and the checkstop reset is enabled (the CRE bit in the system reset control register (SIU\_SRCR) is set), a checkstop reset occurs. Starting at the assertion of the internal reset signal (as indicated by assertion of RSTOUT), the value on the WKPCFG pin is applied; at the same time the PLLCFG[0:1] values are applied if RSTCFG is asserted. Once the FMPLL is locked, the  reset  controller  waits  a  predetermined  number  of  clock  cycles  (See  Section 4.2.2,  'Reset  Output (RSTOUT)') before negating RSTOUT. When the clock count finishes the WKPCFG  and BOOTCFG[0:1] pins are sampled (note that the BOOTCFG[0:1] pins are only sampled if RSTCFG is asserted). The reset controller then waits 4 clock cycles before the negating RSTOUT, and the associated

bits/fields are updated in the SIU\_RSR. In addition, the CRS bit is set, and all other reset status bits in the SIU\_RSR are cleared. Refer to e200z6 Core Guide for more information.

## 4.4.2.3.7 JTAG Reset

A system reset occurs when JTAG is enabled and either the EXTEST, CLAMP, or HIGHZ instructions are executed by the JTAG controller. Starting at the assertion of the internal reset signal (as indicated by assertion of RSTOUT), the value on the WKPCFG pin is applied; at the same time the PLLCFG[0:1] values are applied if RSTCFG is asserted.

Once  the  JTAG  reset  request  has  negated  and  the  FMPLL  is  locked,  the  reset  controller  waits  a predetermined number of clock cycles (See Section 4.2.2, 'Reset Output (RSTOUT)') before negating RSTOUT.. When the clock count finishes the WKPCFG and BOOTCFG[0:1] pins are sampled (note that the BOOTCFG[0:1] pins are only sampled if RSTCFG is asserted), and their associated bits/fields are updated in the SIU\_RSR. The reset source status bits in the SIU\_RSR are unaffected. Refer to Chapter 24, 'IEEE 1149.1 Test Access Port Controller (JTAGC),' for more information.

## 4.4.2.3.8 Software System Reset

A  software  system  reset  is  caused  by  a  write  to  the  SSR  bit  in  the  system  reset  control  register (SIU\_SRCR). A write of 1 to the SSR bit causes an internal reset of the MCU. The internal reset signal is asserted (as indicated by assertion of RSTOUT). The value on the WKPCFG pin is applied starting at the assertion  of  the  internal  reset  signal  (as  indicated  by  assertion  of  RSTOUT);  at  the  same  time  the PLLCFG[0:1] values are applied if RSTCFG is asserted. Once the FMPLL locks, the reset controller waits a predetermined number of clock cycles (See Section 4.2.2, 'Reset Output (RSTOUT)') before negating RSTOUT.. When the clock count finishes the WKPCFG and BOOTCFG[0:1] pins are sampled (note that the BOOTCFG[0:1] pins are only sampled if RSTCFG is asserted). The reset controller then waits 4 clock cycles before negating RSTOUT, and the associated bits/fields are updated in the SIU\_RSR. In addition, the SSRS bit is set, and all other reset status bits in the SIU\_RSR are cleared.

## 4.4.2.3.9 Software External Reset

A write of 1 to the SER bit in the SIU\_SRCR causes the external RSTOUT pin to be asserted for a predetermined  number  of  clocks  (See  Section 4.2.2,  'Reset  Output  (RSTOUT)').  The  SER  bit automatically clears after the clock cycle expires. A software external reset does not cause a reset of the MCU, the BAM program is not executed, the PLLCFG[0:1], BOOTCFG[0:1], and WKPCFG pins are not sampled. The SERF bit in the SIU\_RSR is set, but no other status bits are affected. The SERF bit in the SIU\_RSR is not automatically cleared after the clock count expires, and remains set until cleared by software or another reset besides the software external reset occurs.

For a software external reset, the e200z6 core will continue to execute instructions, timers that are enabled will continue to operate, and interrupt requests will continue to be processed. It is the responsibility of the application to ensure devices connected to RSTOUT are not accessed during a software external reset, and to determine how to manage MCU resources.

## 4.4.3 Reset Configuration and Configuration Pins

The microcontroller and the BAM perform a reset configuration that allows certain functions of the MCU to be controlled and configured at reset. This reset configuration is defined by:

- · Configuration pins
- · A reset configuration half word (RCHW), if present
- · Serial port, if a serial boot is used

Reset

The following sections describe these configuration pins and the RCHW.

## 4.4.3.1 RSTCFG Pin

Table 4-5  shows  the  RSTCFG  pin  settings  for  configuring  the  MCU  to  use  a  default  or  a  custom configuration. Refer to Chapter 2, 'Signal Description' for more information about the RSTCFG pin.

Table 4-5. RSTCFG Settings

|   RSTCFG | Description                                                                                      |
|----------|--------------------------------------------------------------------------------------------------|
|        1 | Use default configuration of: - booting from internal flash - clock source is a crystal on FMPLL |
|        0 | Get configuration information from: - BOOTCFG[0:1] - PLLCFG[0:1]                                 |

## 4.4.3.2 WKPCFG Pin (Reset Weak Pull Up/Pull Down Configuration)

As shown in Table 4-6, the signal on the WKPCFG pin determines whether specific eTPU and eMIOS pins are connected to weak pull up or weak pull down devices during and after reset (see Chapter 2, 'Signal Description,' for the eTPU and eMIOS pins that are affected by WKPCFG). For all reset sources except the software external reset, the WKPCFG pin is applied starting at the assertion of the internal reset signal (as indicated by the assertion of RSTOUT). If the WKPCFG signal is logic high at this time, pull up devices will be enabled on the eTPU and eMIOS pins. If the WKPCFG signal is logic low at the assertion of the internal reset signal, pull down devices will be enabled on those pins. The value on WKPCFG must be held constant during reset to avoid oscillations on the eTPU and eMIOS pins caused by switching pull up/down states. The final value of WKPCFG is latched 4 clock cycles before the negation of RSTOUT. After reset, software may modify the weak pull up/down selection for all I/O pins through the PCRs in the SIU.

Table 4-6.  WKPCFG Settings

|   WKPCFG | Description                                            |
|----------|--------------------------------------------------------|
|        0 | Weak pull down applied to eTPU and eMIOS pins at reset |
|        1 | Weak pull up applied to eTPU and eMIOS pins at reset   |

Also refer to Chapter 2, 'Signal Description' for information about the WKPCFG pin.

## 4.4.3.3 BOOTCFG[0:1] Pins (MCU Configuration)

In addition to specifying the RCHW location, the values latched on the BOOTCFG[0:1] pins at reset are used to initialize the internal Flash memory enabled/disabled state, and whether no arbitration or external arbitration of the external bus interface is selected. Additionally, the RCHW can determine either directly or indirectly how the MMU is configured, how the external bus is configured, CAN or eSCI module and pin configuration, Nexus enabling, and password selection.

Also refer to Chapter 2, 'Signal Description' for information about the BOOTCFG pins.

## 4.4.3.4 PLLCFG[0:1] Pins

The  role  of  PLLCFG  pins  in  PLL  configuration  is  explained  in  Section 11.1.4,  'FMPLL  Modes  of Operation.' Also refer to Chapter 2, 'Signal Description' for information about the PLLCFG pins.

Table 4-7. PLLCFG[0:1] and RSTCFG in Configuration

|   RSTCFG | PLLCFG0             | PLLCFG1             | Clock Mode                  |   MODE |   PLLSEL |   PLLREF |
|----------|---------------------|---------------------|-----------------------------|--------|----------|----------|
|        1 | PLLCFG pins ignored | PLLCFG pins ignored | Crystal reference (default) |      1 |        1 |        1 |
|        0 | 0                   | 0                   | Bypass Mode                 |      0 |        0 |        0 |
|        0 | 0                   | 1                   | External reference          |      1 |        1 |        0 |
|        0 | 1                   | 0                   | Crystal reference           |      1 |        1 |        1 |
|        0 | 1                   | 1                   | 1:1 Mode                    |      1 |        0 |        0 |

## 4.4.3.5 Reset Configuration Half Word

## 4.4.3.5.1 Reset Configuration Half Word Definition

The RCHW is read from either external memory or internal Flash memory. If a valid RCHW is not found, a CAN/SCI boot is initiated. The RCHW is a collection of control bits that specify a minimum MCU configuration after reset and define the desired mode of operation of the BAM program. At reset the RCHW provides a means to locate the boot code, determines if Flash memory is programmed or erased, enables or disables the watchdog timer, and if booting externally, sets the bus size. The user should refer to the appropriate register given by the RCHW bit descriptions for a detailed description of each control bit.

## NOTE

Do not configure the RCHW to a 32-bit bus size for devices with only a 16-bit data bus.

If booting from internal Flash or external memory, the user must insure that the RCHW is the correct value for the desired configuration, and that it is located at the proper location in memory. The boot ID of the RCHW must be read as 0x5A. BOOT\_BLOCK\_ADDRESS is explained in Section 16.3.2.2.5, 'Reset Configuration Half Word Read.'

## Reset

The fields of the RCHW are shown in Figure 4-3.

<!-- image -->

| 0   | 1   | 2   | 3   | 4   | 5   | 6   | 7   | 8   | 9   | 10                     | 11                     | 12                     | 13                     | 14                     | 15                     |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|------------------------|------------------------|------------------------|------------------------|------------------------|------------------------|
|     |     |     |     |     | WTE | PS0 |     | 0   | 1   | 0                      | 1                      | 1                      | 0                      | 1                      | 0                      |
|     |     |     |     |     |     |     |     |     |     | Boot Identifier = 0x5A | Boot Identifier = 0x5A | Boot Identifier = 0x5A | Boot Identifier = 0x5A | Boot Identifier = 0x5A | Boot Identifier = 0x5A |

BOOT\_BLOCK\_ADDRESS + 0x0000\_0000

Figure 4-3. RCHW Fields

Table 4-8. Internal Boot RCHW Field Descriptions

| Bits   | Name         | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
|--------|--------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-4    | -            | Reserved: These bit values are ignored when the halfword is read. Write to 0 for future compatibility.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| 5      | WTE          | Watchdog timer enable. This is used to enable or disable the e200z6 watchdog timer through the BAMprogram. The configuration of the watchdog timer function is managed through the timer control register (TCR). 0 BAM does not write the e200z6 timebase registers (TBU and TBL) nor enable the e200z6 core watchdog timer. 1 BAM writes the e200z6 timebase registers (TBU and TBL) to 0x0000_0000_0000_0000 and enables the e200z6 core watchdog timer with a time-out period of 3 x 2 17 system clock cycles. (Example: For 8 MHz crystal -> 12MHz system clock -> 32.7mS time-out. For 20 MHz crystal -> 30 MHz system clock -> 13.1mS time-out)                                                                                   |
| 6      | PS0          | Port size. Defines the width of the data bus connected to the memory on CS0. After system reset, CS0is changed to a 16-bit port by the BAMwhich fetches the RCHWfrom either 16- or 32-bit external memories. Then the BAM reconfigures the EBI either as a 16-bit bus or a 32-bit bus, according to the settings of this bit. 0 32-bit CS0 port size 1 16-bit CS0 port size Note: Used only in external boot mode. Do not set the port to 32-bits if the device only has a 16-bit data bus.                                                                                                                                                                                                                                             |
| 7      | -            | Reserved: This bit value is ignored when the halfword is read. Write to 0 for future compatibility.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| 8-15   | BOOTID [0:7] | Boot identifier. This field serves two functions. First, it is used to indicate which block in Flash memory contains the boot program. Second, it identifies whether the Flash memory is programmed or invalid. The value of a valid boot identifier is 0x5A (0b01011010). The BAMprogram checks the first half word of each Flash memory block starting at block 0 until a valid boot identifier is found. If all blocks in the low address space of the internal Flash are checked and no valid boot identifier is found, then the internal Flash is assumed to be invalid and a CAN/SCI boot is initiated. For an external boot, only block 0 is checked for a valid boot identifier, and if not found, a CAN/SCI boot is initiated. |

## 4.4.3.5.2 Invalid RCHW

If the device is configured for a boot from internal Flash, a valid boot ID must be read at the lowest address of one of the six LAS blocks in internal Flash memory. If the device is configured for a boot from external memory, a valid boot ID must be read at 0x00\_0000 of CS0. Refer to Chapter 16, 'Boot Assist Module (BAM)' for more information.

If a valid RCHW is not found, a serial boot is initiated. A serial boot does not use a RCHW. The watchdog timer is enabled. For serial boot entered from a failed external boot, the port size remains configured as 16 bits wide. For serial boot entered from a failed internal boot, the external bus is never configured and remains in the reset state of GPIO inputs.

## 4.4.3.5.3 Reset Configuration Half Word Source

The  reset  configuration  half  word  (RCHW)  specifies  a  minimal  MCU  configuration  after  reset.  The RCHW also contains bits that control the BAM program flow. See Section 16.3.2.1.1, 'Finding Reset Configuration Half Word' for information on the BAM using the RCHW. The RCHW is read and applied each time the BAM program executes, which is for every power-on, external, or internal reset event. The only exception to this is the software external reset. See Section 4.4.3.5, 'Reset Configuration Half Word,' for detailed descriptions of the bits in the RCHW. The RCHW is read from one of the following locations:

- · The lowest address (0x00\_0000) of an external memory device, enabled by chip select CS0 using either a 16- or 32-bit data bus
- · The lowest address of one of the six low address space (LAS) blocks in the internal Flash memory. (2 x 16K; 2 x 48K; 2 x 64K)

At the negation of the RSTOUT pin, the BOOTCFG field in the RSR has been updated. If BOOTCFG0 is asserted, then the BAM program reads the RCHW from address 0x0000\_0000 in the external memory connected  to  CS0  (the  BAM  first  configures  the  MMU  and  CS0  such  that  address  0x0000\_0000  is translated  to  0x2000\_0000  and  then  directed  to  CS0).  When  BOOTCFG0  is  asserted,  BOOTCFG1 determines whether external arbitration must be enabled to fetch the RCHW.

If BOOTCFG0 and BOOTCFG1 are negated at the negation of the RSTOUT pin, then the BAM program attempts to read the RCHW from the first address of each of the 6 blocks in the low address space (LAS) of internal Flash. Table 4-9 shows the LAS addresses.

Table 4-9. LAS Block Memory Addresses

|   Block | Address     |
|---------|-------------|
|       0 | 0x0000_0000 |
|       1 | 0x0000_4000 |
|       2 | 0x0001_0000 |
|       3 | 0x0001_C000 |
|       4 | 0x0002_0000 |
|       5 | 0x0003_0000 |

If the RCHW stored in either internal or external Flash is invalid (boot identifier field of RCHW is not 0x5A), or if BOOTCFG0 is negated and BOOTCFG1 is asserted at the negation of the RSTOUT pin, then RCHW is not applicable, and serial boot mode is performed. Table 4-10 summarizes the RCHW location options.

## Reset

Note  that  the  BOOTCFG[0:1]  =  11  is  a  meaningless  configuration  for  the  MPC5553,  because  the arbitration pins and TSIZ have been removed.

Table 4-10. MPC5553/MPC5554 Reset Configuration Half Word Sources

|   RSTCFG | BOOTCFG0   | BOOTCFG1   | BootIdentifier Field (RCHW)   | Boot Mode                             | Configuration Word Source                                                                                                   |
|----------|------------|------------|-------------------------------|---------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|
|        1 | -          | -          | Valid                         | Internal                              | The lowest address of one of the six low address spaces (LAS) in internal Flash memory.                                     |
|        1 | -          | -          | Invalid                       | Serial                                | Not applicable                                                                                                              |
|        0 | 0          | 0          | Valid                         | Internal                              | The lowest address of one of the six low address spaces (LAS) in internal Flash memory.                                     |
|        0 | 0          | 0          | Invalid                       | Serial                                | Not applicable                                                                                                              |
|        0 | 0          | 1          | -                             | Serial                                | Not applicable                                                                                                              |
|        0 | 1          | 0          | Valid                         | External Boot, No Arbitration         | The lowest address (0x00_0000) of an external memorydevice, enabled by chip select CS0using either 16- or 32-bit data bus   |
|        0 | 1          | 0          | Invalid                       | Serial                                | Not applicable                                                                                                              |
|        0 | 1          | 1          | Valid 1                       | External 1 Boot, External Arbitration | Thelowest address (0x0000_0000) of an external memorydevice, enabled by chip select CS0using either 16- or 32-bit data bus. |
|        0 | 1          | 1          | Invalid                       | Serial                                | Not applicable                                                                                                              |

1 External boot mode with external arbitration is not supported in the MPC5553.

## 4.4.4 Reset Configuration Timing

The  timing  diagram  in  Figure 4-4  shows  the  sampling  of  the  BOOTCFG[0:1],  WKPCFG,  and PLLCFG[0:1] pins for a power-on reset. The timing diagram is also valid for internal/external resets assuming  that  V DD,   V DDSYN,   and  V DDEH6   are  within  valid  operating  ranges.  The  values  of  the PLLCFG[0:1] pins are latched at the negation of the RSTOUT pin, if the RSTCFG pin is asserted at the negation of RSTOUT. The value of the WKPCFG signal is applied at the assertion of the internal reset signal (as indicated by the assertion of RSTOUT). The values of the WKPCFG and BOOTCFG[0:1] pins are  latched  4  clock  cycles  before  the  negation  of  RSTOUT  and  stored  in  the  reset  status  register (SIU\_RSR). BOOTCFG[0:1] are latched only if RSTCFG is asserted. WKPCFG is not dependent on RSTCFG.

<!-- image -->

- 1  This clock count is dependent on the configuration of the FMPLL (See Section 4.2.2, 'RSTOUT'). If the FMPLL is configured for 1:1 (dual controller) operation or for bypass mode, this clock count is 16000.

Figure 4-4. MPC5553/MPC5554 Reset Configuration Timing

## 4.4.5 Reset Flow

Figure 4-5. External Reset Flow Diagram

<!-- image -->

## Functional Description

<!-- image -->

## NOTES:

The clock count is dependent on the configuration of the FMPLL (refer to Section 5.3.1.2, 'RSTOUT'). If the FMPLL is configured in 1:1 (dual controller) or bypass mode, this clock count is 16000. 1

Figure 4-6. Internal Reset Flow Diagram

## 4.5 Revision History

## Substantive Changes since Rev 3.0

Updated Table 4-5 by swapping the 0 and 1.

Changed 'Once the debug reset request has negated and the FMPLL is locked, the reset controller waits ...." to "Once the FMPLL is locked, the reset controller waits ...." in the Watchdog Timer/Debug Reset section.
