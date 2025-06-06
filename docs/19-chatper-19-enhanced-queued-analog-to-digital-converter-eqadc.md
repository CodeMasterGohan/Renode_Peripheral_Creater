### Chatper 19 Enhanced Queued Analog-to-Digital Converter (eQADC)

## 19.1 Introduction

The enhanced queued analog-to-digital converter (eQADC) of the MPC5553/MPC5554 provides accurate and fast conversions for a wide range of applications. The eQADC provides a parallel interface to two on-chip analog-to-digital converters (ADCs), and a single master to single slave serial interface to an off-chip external device. The two on-chip ADCs are architected to allow access to all the analog channels.

## 19.1.1 Block Diagram

Figure 19-1 shows the primary components inside the eQADC.

Figure 19-1. Simplified eQADC Block Diagram

<!-- image -->

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## 19.1.2 Overview

The eQADC transfers commands from multiple command FIFOs (CFIFOs) to the on-chip ADCs or to the external device. The module can also in parallel (independently of the CFIFOs) receive data from the on-chip ADCs or from an off-chip external device into multiple result FIFOs (RFIFOs). The eQADC supports software and external hardware triggers from other modules to initiate transfers of commands from the  CFIFOs to the  on-chip  ADCs  or  to  the  external  device.  (Refer  to  Section 6.4.5.1,  'eQADC External Trigger Input Multiplexing.') It also monitors the fullness of CFIFOs and RFIFOs, which may result in either underflow or overflow conditions. A CFIFO underflow occurs when the CFIFO is in the TRIGGERED state and it becomes empty. An RFIFO overflow occurs when an RFIFO is full and more data is ready to be moved to the RFIFO by the host CPU or by eDMA. Accordingly, the eQADC generates eDMA or interrupt requests to control data movement between the FIFOs and the system memory, which is external to the eQADC.

The eQADC consists of the FIFO control unit which controls the CFIFOs and the RFIFOs, two ADCs with associated  control  logic,  and  the  eQADC  synchronous  serial  interface (eQADC  SSI)  which  allows communication with an external device. There are 6 CFIFOs and 6 RFIFOs, each with 4 entries.

The FIFO control unit performs the following functions:

- · Prioritizes the CFIFOs to determine what CFIFOs will have their commands transferred
- · Supports software and hardware triggers to start command transfers from a particular CFIFO
- · Decodes command data from the CFIFOs, and accordingly, sends these commands to one of the two on-chip ADCs or to the external device
- · Decodes result data from on-chip ADCs or from the external device, and transfers data to the appropriate RFIFO

The ADC control logic manages the execution of commands bound for on-chip ADCs from the CFIFOs and with the RFIFOs via the result format and calibration submodule. The ADC control logic performs the following functions:

- · Buffers command data for execution
- · Decodes command data and accordingly generates control signals for the two on-chip ADCs
- · Formats and calibrates conversion result data coming from the on-chip ADCs
- · Generates the internal multiplexer control signals and the select signals used by the external multiplexers

The eQADC SSI allows for a full duplex, synchronous, serial communication between the eQADC and an external device.

Figure 19-1 also depicts data flow through the eQADC. Commands are contained in system memory in a user-defined queue data structure. Command data is moved from the user-defined command queue to the CFIFOs by either the host CPU or by the eDMA. Once a CFIFO is triggered and becomes the highest priority, CFIFO command data is transferred from the CFIFO to the on chip ADCs, or to the external device. The ADC executes the command, and the result is moved through the result format and calibration submodule and to the RFIFO. The RFIFO target is specified by a field in the command that initiated the conversion. Data from the external device bypasses the result format and calibration submodule and is moved directly to its specified RFIFO. When data is stored in an RFIFO, data is moved from the RFIFO by the host CPU or by the eDMA to a data structure in system memory depicted in Figure 19-1 as a user-defined result queue.

For  users  familiar  with  the  QADC,  the  eQADC  system  upgrades  the  functionality  provided  by  that module. Refer to Section 19.5.7, 'eQADC versus QADC,' for a comparison between the eQADC and QADC.

## 19.1.3 Features

The eQADC includes these distinctive features:

- · Two independent on-chip RSD cyclic ADCs
- - 12 Bit AD Resolution.
- - Targets up to 10 bit accuracy at 400 kilosamples per second (ADC\_CLK=6MHz) and 8 bit accuracy at 800 kilosamples per second (ADC\_CLK=12MHz) for differential conversions.
- - Differential conversions (range -2.5V to +2.5V).
- - Single-ended signal range from 0 to 5V.
- - Sample times of 2 (default), 8, 64, or 128 ADC clock cycles.
- - Provides sample time stamp information when requested.
- - Parallel interface to eQADC CFIFOs and RFIFOs.
- - Supports both right-justified unsigned and signed formats for conversion results.
- - The REFBYPC pin allows process-independent low variation biasing current.
- · Optional automatic application of ADC calibration constants
- - Provision of reference voltages (25%VREF 1  and 75%VREF) for ADC calibration purposes
- · 40 input channels available to the two on-chip ADCs
- · Four pairs of differential analog input channels
- · Full duplex synchronous serial interface to an external device
- - A free-running clock is provided for use by the external device.
- - Supports a 26-bit message length.
- - Transmits a null message when there are no triggered CFIFOs with commands bound for external command buffers, or when there are triggered CFIFOs with commands bound for external command buffers but the external command buffers are full.
- · Priority-based CFIFOs
- - Supports six CFIFOs with fixed priority. The lower the CFIFO number, the higher its priority. When commands of distinct CFIFOs are bound for the same ADC, the higher priority CFIFO is always served first.
- - Supports software and several hardware trigger modes to arm a particular CFIFO.
- - Generates interrupt when command coherency is not achieved.
- · External hardware triggers
- - Supports rising edge, falling edge, high level and low level triggers
- - Supports configurable digital filter
- · Supports four external 8-to-1 muxes that can expand the input channel number from 40 to 68
- · Upgrades the functionality provided by the QADC

## 19.1.4 Modes of Operation

This section describes the operation modes of the eQADC.

## 19.1.4.1 Normal Mode

This is the default operational mode when the eQADC is not in background debug or stop mode.

1. VREF=VRH-VRL.

## 19.1.4.2 Debug Mode

Upon a debug mode entry request, eQADC behavior will vary according to the status of the DBG field in Section 19.3.2.1, 'eQADC Module Configuration Register (EQADC\_MCR).' If DBG is programmed to 0b00, the debug mode entry request is ignored. If DBG is programmed to 0b10 or to 0b11, the eQADC will enter debug mode. In case the eQADC SSI is enabled, the free running clock (FCK) output to external device will not stop when DBG is programmed to 0b11, but FCK will stop in low phase, when DBG is programmed to 0b10.

During debug mode, the eQADC will not transfer commands from any CFIFOs, no null messages will be transmitted to the external device, no data will be returned to any RFIFO, no hardware trigger event will be captured, and all eQADC registers can be accessed as in normal mode. Access to eQADC registers implies that CFIFOs can still be triggered using software triggers, because no scheme is implemented to write-protect registers during debug mode. eDMA and interrupt requests continue to be generated as in normal mode.

If at the time the debug mode entry request is detected, there are commands in the ADC that were already under execution, these commands will be completed but the generated results, if any, will not be sent to the RFIFOs until debug mode is exited. Commands whose execution has not started will not be executed until debug mode is exited. The clock associated with an on-chip ADC stops, during its low phase, after the ADC ceases executing commands. The time base counter will only stop after all on-chip ADCs cease executing commands.

When exiting  debug  mode,  the  eQADC  relies  on  the  FIFO  control  unit  and  on  the  CFIFO  status  to determine the next command entry to transfer.

The eQADC internal behavior after the debug mode entry request is detected differs depending on the status of command transfers.

- · No command transfer is in progress.
- The eQADC immediately halts future command transfers from any CFIFO.
- If a null message is being transmitted, eQADC will complete the serial transmission before halting future command transfers. If valid data (conversion result or data read from an ADC register) is received by the result format and calibration submodule at the end of transmission, this data will not be sent to an RFIFO until debug mode is exited.
- If the null message transmission is aborted, the eQADC will complete the abort procedure before halting future command transfers from any CFIFO. The message of the CFIFO that caused the abort of the previous serial transmission will only be transmitted after debug mode is exited.
- · Command transfer is in progress.
- eQADC will complete the transfer and update CFIFO status before halting future command
- transfers from any CFIFO.
- Command transfers to the external device are considered completed when the serial transmission of the command is completed. If valid data (conversion result or data read from an ADC register) is received at the end of a serial transmission, it will not be sent to an RFIFO until debug mode is exited. The CFIFO status bits will still be updated after the completion of the serial transmission, therefore, after debug mode entry request is detected, the eQADC status bits will only stop changing several system clock cycles after the on-going serial transmission completes.
- If the command message transmission is aborted, the eQADC will complete the abort procedure before halting future command transfers from any CFIFO. The message of the CFIFO that caused the abort of the previous serial transmission will only be transmitted after debug mode is exited.
- · Command/null message transfer through serial interface was aborted but next serial transmission did not start.

If the debug mode entry request is detected between the time a previous serial transmission was aborted and the start of the next transmission, the eQADC will complete the abort procedure before halting future command transfers from any CFIFO. The message of the CFIFO that caused the abort of the previous serial transmission will only be transmitted after debug mode is exited.

## 19.1.4.3 Stop Mode

Upon a stop mode entry request detection, the eQADC progressively halts its operations until it reaches a static, stable state from which it can recover when returning to normal mode. The eQADC then asserts an acknowledge signal, indicating that it is static and that the clock input can be stopped. In stop mode, the free running clock (FCK) output to external device will stop during its low phase if the eQADC SSI is enabled, and no hardware trigger events will be captured. No capturing of hardware trigger events means that - as long as the system clock is running - CFIFOs can still be triggered using software triggers because no scheme is implemented to write-protect registers during stop mode.

If at the time the stop mode entry request is detected, there are commands in the ADC that were already under execution, these commands will be completed but the generated results, if any, will not be sent to the RFIFOs until stop mode is exited. Commands whose execution has not started will not be executed until stop mode is exited.

After these remaining commands are executed, the clock input to the ADCs is stopped. The time base counter will stop after all on-chip ADCs cease executing commands and then the stop acknowledge signal is asserted. When exiting stop mode, the eQADC relies on the CFIFO operation modes and on the CFIFO status to determine the next command entry to transfer.

The eQADC internal behavior after the stop mode entry request is detected differs depending on the status of the command transfer.

- · No command transfer is in progres.s
- The eQADC immediately halts future command transfers from any CFIFO.
- If a null message is being transmitted, eQADC will complete the transmission before halting future command transfers. If valid data (conversion result or data read from an ADC register) is received at the end of the transmission, it will not be sent to an RFIFO until stop mode is exited.
- If the null message transmission is aborted, the eQADC will complete the abort procedure before halting future command transfers from any CFIFO. The message of the CFIFO that caused the abort of the previous serial transmission will only be transmitted after stop mode is exited.
- · Command transfer is in progress.
- The eQADC will complete the transfer and update CFIFO status before halting future command transfers from any CFIFO.
- Command transfers to the external device are considered completed when the serial transmission of the command is completed. If valid data (conversion result or data read from an ADC register) is received at the end of a serial transmission, it will not be sent to an RFIFO until stop mode is exited. The CFIFO status bits will still be updated after the completion of the serial transmission, therefore, after stop mode entry request is detected, the eQADC status bits will only stop changing several system clock cycles after the on-going serial transmission completes.
- If the command message transmission is aborted, the eQADC will complete the abort procedure before halting future command transfers from any CFIFO. The message of the CFIFO that caused the abort of the previous serial transmission will only be transmitted after stop mode is exited.
- · Command/null message transfer through serial interface was aborted but next serial transmission did not start.

If the stop mode entry request is detected between the time a previous serial transmission was aborted and the start of the next transmission, the eQADC will complete the abort procedure before halting future command transfers from any CFIFO. The message of the CFIFO that caused the abort of the previous serial transmission will only be transferred after stop mode is exited.

## 19.2 External Signals

The following is a list of external signals. These signals are external to the eQADC module, but may or may not be physical pins. See Chapter 2, 'Signal Description' for a complete list of all physical pins and signals.

Table 19-1. eQADC External Signals

| Function   | Description                                                      | I/O Type   | Status During Reset 1   | Status After Reset 2   | Type   | Package     |
|------------|------------------------------------------------------------------|------------|-------------------------|------------------------|--------|-------------|
| AN0 DAN0+  | Single Ended Analog Input 0 Positive Terminal Differential Input | I I        | I / -                   | AN0/ -                 | Analog | 416 324 208 |
| AN1 DAN0-  | Single Ended Analog Input 1 Negative Terminal Differential Input | I I        | I / -                   | AN1/ -                 | Analog | 416 324 208 |
| AN2 DAN1+  | Single Ended Analog Input 2 Positive Terminal Differential Input | I I        | I / -                   | AN2 / -                | Analog | 416 324 208 |
| AN3 DAN1-  | Single Ended Analog Input 3 Negative Terminal Differential Input | I I        | I / -                   | AN3 / -                | Analog | 416 324 208 |
| AN4 DAN2+  | Single Ended Analog Input 4 Positive Terminal Differential Input | I I        | I / -                   | AN4/ -                 | Analog | 416 324 208 |
| AN5 DAN2-  | Single Ended Analog Input 5 Negative Terminal Differential Input | I I        | I / -                   | AN5 / -                | Analog | 416 324 208 |
| AN6 DAN3+  | Single Ended Analog Input 6 Positive Terminal Differential Input | I I        | I / -                   | AN6 / -                | Analog | 416 324 208 |
| AN7 DAN3-  | Single Ended Analog Input 7 Negative Terminal Differential Input | I I        | I / -                   | AN7 / -                | Analog | 416 324 208 |
| AN8 ANW    | Single Ended Analog Input 8 External Multiplexed Analog Input W  | I I        | I / -                   | AN8/ -                 | Analog | 416 324 208 |
| AN9 ANX    | Single Ended Analog Input 9 External Multiplexed Analog Input X  | I I        | I / -                   | AN9 / -                | Analog | 416 324 208 |

Table 19-1. eQADC External Signals (continued)

| Function     | Description                                                             | I/O Type   | Status During Reset 1   | Status After Reset 2   | Type                     | Package     |
|--------------|-------------------------------------------------------------------------|------------|-------------------------|------------------------|--------------------------|-------------|
| AN10 ANY     | Single Ended Analog Input 10 External Multiplexed Analog Input Y        | I I        | I / -                   | AN10/ -                | Analog                   | 416 324 208 |
| AN11 ANZ     | Single Ended Analog Input 11 External Multiplexed Analog Input Z        | I I        | I / -                   | AN11 / -               | Analog                   | 416 324 208 |
| AN12 MA0 SDS | Single Ended Analog Input 12 Mux Address 0 eQADC SSI Serial Data Select | I O O      | I / -                   | AN12/ -                | Analog/ Digital/ Digital | 416 324 208 |
| AN13 MA1 SDO | Single Ended Analog Input 13 Mux Address 1 eQADC SSI Serial Data Out    | I O O      | I / -                   | AN13/ -                | Analog/ Digital/ Digital | 416 324 208 |
| AN14 MA2 SDI | Single Ended Analog Input 14 Mux Address 2 eQADC SSI Serial Data In     | I O I      | I / -                   | AN14/ -                | Analog/ Digital/ Digital | 416 324 208 |
| AN15 FCK     | Single Ended Analog Input 15 eQADC Free Running Clock                   | I O        | I / -                   | AN15/ -                | Analog/ Digital          | 416 324 208 |
| AN16         | Single Ended Analog Input 16                                            | I          | I / -                   | AN16 / -               | Analog                   | 416 324     |
| AN[17:19]    | Single Ended Analog Input 17-19                                         | I          | I / -                   | AN[17:19]/ -           | Analog                   | 416 324 208 |
| AN20         | Single Ended Analog Input                                               | I          | I / -                   | AN20/ -                | Analog                   | 416 324     |
| AN21         | Single Ended Analog Input                                               | I          | I / -                   | AN21/ -                | Analog                   | 416 324 208 |
| AN[22:25]    | Single Ended Analog Input                                               | I          | I / -                   | AN[22:25]/ -           | Analog                   | 416 324 208 |
| AN26         | Single Ended Analog Input                                               | I          | I / -                   | AN26/ -                | Analog                   | 416 324     |
| AN[27:28]    | Single Ended Analog Input                                               | I          | I / -                   | AN[27:28]/ -           | Analog                   | 416 324 208 |
| AN29         | Single Ended Analog Input                                               | I          | I / -                   | AN29/ -                | Analog                   | 416 324     |

Table 19-1. eQADC External Signals (continued)

| Function        | Description                                           | I/O Type       | Status During Reset 1   | Status After Reset 2   | Type           | Package        |
|-----------------|-------------------------------------------------------|----------------|-------------------------|------------------------|----------------|----------------|
| AN[30:32]       | Single Ended Analog Input                             | I              | I / -                   | AN[30:32]/ -           | Analog         | 416 324 208    |
| AN33            | Single Ended Analog Input                             | I              | I / -                   | AN33 / -               | Analog         | 416 324        |
| AN[34:35]       | Single Ended Analog Input                             | I              | I / -                   | AN[34:35]/ -           | Analog         | 416 324 208    |
| AN36            | Single Ended Analog Input                             | I              | I / -                   | AN36 / -               | Analog         | 416 324        |
| AN[37:39]       | Single Ended Analog Input 37-39                       | I              | I / -                   | AN[37:39] / -          | Analog         | 416 324 208    |
| ETRIG0/ GPIO111 | External trigger for CFIFO0, CFIFO2, and CFIFO4/ GPIO | I I/O          | - / Up                  | - / Up                 | Digital        | 416            |
| ETRIG1/ GPIO112 | External trigger for CFIFO1, CFIFO3, and CFIFO5/ GPIO | I I/O          | - / Up                  | - / Up                 | Digital        | 416            |
| Power Supplies  | Power Supplies                                        | Power Supplies | Power Supplies          | Power Supplies         | Power Supplies | Power Supplies |
| VRH             | Voltage Reference High                                | I              | - / -                   | VRH                    | Power          | 416 324 208    |
| VRL             | Voltage Reference Low                                 | I              | - / -                   | VRL                    | Power          | 416 324 208    |
| REFBYPC         | Reference Bypass Capacitor Input                      | I              | - / -                   | REFBYPC                | Power          | 416 324 208    |
| V DDA           | Analog Positive Power Supply                          | I              | -                       | -                      | Power          | 416 324 208    |
| V SSA           | Analog Negative Power Supply                          | I              | -                       | -                      | Power          | 416 324 208    |

1 Terminology is O - output, I - input, Up - weak pull up enabled, Down - weak pull down enabled, Low - output driven low, High - output driven high. A dash on the left side of the slash denotes that both the input and output buffers for the pin are off. A dash on the right side of the slash denotes that there is no weak pull up/down enabled on the pin. The signal name to the left or right of the slash indicates the pin is enabled.

- 2 Function after reset of GPI is general-purpose input. A dash on the left side of the slash denotes that both the input and output buffers for the pin are off. A dash on the right side of the slash denotes that there is no weak pull up/down enabled on the pin.

## 19.2.1 Detailed Signal Descriptions

## 19.2.1.1 Single-ended Analog Input/Differential Analog Input Positive Terminal (AN0/DAN0+)

AN0 is a single-ended analog inputs to the two on-chip ADCs. DAN0+ is the positive terminal of the differential analog input DAN0 (DAN0+-DAN0-).

## 19.2.1.2 Single-ended Analog Input/Differential Analog Input Negative Terminal (AN1/DAN0-)

AN1 is a single-ended analog inputs to the two on-chip ADCs. DAN0- is the negative terminal of the differential analog input DAN0 (DAN0+-DAN0-).

## 19.2.1.3 Single-ended Analog Input/Differential Analog Input Positive Terminal (AN2/DAN1+)

AN2 is a single-ended analog inputs to the two on-chip ADCs. DAN1+ is the positive terminal of the differential analog input DAN1 (DAN1+-DAN1-).

## 19.2.1.4 Single-ended Analog Input/Differential Analog Input Negative Terminal (AN3/DAN1-)

AN3 is a single-ended analog inputs to the two on-chip ADCs. DAN1- is the negative terminal of the differential analog input DAN1 (DAN1+-DAN1-).

## 19.2.1.5 Single-ended Analog Input/Differential Analog Input Positive Terminal (AN4/DAN2+)

AN4 is a single-ended analog inputs to the two on-chip ADCs. DAN2+ is the positive terminal of the differential analog input DAN2 (DAN2+-DAN2-).

## 19.2.1.6 Single-ended Analog Input/Differential Analog Input Negative Terminal (AN5/DAN2-)

AN5 is a single-ended analog inputs to the two on-chip ADCs. DAN2- is the negative terminal of the differential analog input DAN2 (DAN2+-DAN2-).

## 19.2.1.7 Single-ended Analog Input/Differential Analog Input Positive Terminal (AN6/DAN3+)

AN6 is a single-ended analog inputs to the two on-chip ADCs. DAN3+ is the positive terminal of the differential analog input DAN3 (DAN3+-DAN3-).

## 19.2.1.8 Single-ended Analog Input/Differential Analog Input Negative Terminal (AN7/DAN3-)

AN7 is a single-ended analog inputs to the two on-chip ADCs. DAN3- is the negative terminal of the differential analog input DAN3 (DAN3+-DAN3-).

## 19.2.1.9 Single-ended Analog Input/ Single-ended Analog Input from External Multiplexers (AN8/ANW)

AN8 is a single-ended analog inputs to the two on-chip ADCs. ANW is a single-ended analog input to one of the on-chip ADCs in external multiplexed mode.

## 19.2.1.10 Single-ended Analog Input/ Single-ended Analog Input from External Multiplexers (AN9/ANX)

AN9 is a single-ended analog inputs to the two on-chip ADCs. ANX is a single-ended analog input to one of the on-chip ADCs in external multiplexed mode.

## 19.2.1.11 Single-ended Analog Input/ Single-ended Analog Input from External Multiplexers (AN10/ANY)

AN10 is a single-ended analog inputs to the two on-chip ADCs. ANY is a single-ended analog input to one of the on-chip ADCs in external multiplexed mode.

## 19.2.1.12 Single-ended Analog Input/ Single-ended Analog Input from External Multiplexers (AN11/ANZ)

AN11 is a single-ended analog inputs to the two on-chip ADCs. ANZ is a single-ended analog input to one of the on-chip ADCs in external multiplexed mode.

## 19.2.1.13 Single-ended Analog Input (AN[12:14]/MA[0:2]/SD x )

AN12 through AN14 are single-ended analog inputs to the two on-chip ADCs. MA0, MA1, and MA2 combined form a select signal associated with external multiplexers. Serial data strobe, input, and output for the eQADC serial synchronous interface are also multiplexed here.

## NOTE

Performance of the analog channels AN12, AN13, AN14, and AN15 may have slightly reduced analog to digital conversion accuracy when compared to AN[0:11] and AN[16:3] because they are powered by V DDEH9  and can be used as digital pins for the synchronous serial interface (SSI) to external ADCs or used as the multiplexor digital outputs (MA[0:2]).

Attempts to convert the input voltage applied to AN12, AN13, AN14, and AN15 while a non-eQADC function is selected will result in an undefined conversion result.

## 19.2.1.13.1 eQADC SSI Serial Data Select (SDS)

SDS is the serial data select output that is muxed with AN12 and MA0. It indicates to the external (slave) device when it can latch incoming serial data, when it can output its own serial data, and when it must abort a data transmission. SDS corresponds to the chip select signal in a conventional SPI interface.

These pins are configured by setting the pad configuration register, SIU\_PCR215 (See Chapter 6, 'System Integration Unit (SIU)').

## 19.2.1.13.2 eQADC SSI Serial Data Out (SDO)

SDO is the serial data output signal to the external (slave) device. It is muxed with AN13 and MA1. These pins  are  configured  by  setting  the  pad  configuration  register,  SIU\_PCR216  (See  Chapter 6,  'System Integration Unit (SIU)').

## 19.2.1.13.3 eQADC SSI Serial Data In (SDI)

SDI is the serial data input signal from the external (slave) device. It is muxed with AN14 and MA2. These pins  are  configured  by  setting  the  pad  configuration  register,  SIU\_PCR217  (See  Chapter 6,  'System Integration Unit (SIU)').

## 19.2.1.14 Single-ended Analog Input (AN15) / eQADC SSI Free-running Clock (FCK)

FCK is a free-running clock signal for synchronizing transmissions between the eQADC (master) and the external (slave) device. AN15 is a single-ended analog input to the two on-chip ADCs. These pins are configured by setting the pad configuration register, SIU\_PCR218 (See Chapter 6, 'System Integration Unit (SIU)').

## 19.2.1.15 Single-ended Analog Input (AN[16:39])

AN16 through AN39 are single-ended analog inputs to the two on-chip ADCs.

## 19.2.1.16 External Triggers (ETRIG[0:1])

The external trigger signals are for hardware triggering. The eQADC can detect rising edge, falling edge, high level, and low level on each of the external trigger signals. The eQADC also supports configurable digital filters for these external trigger signals.

The eQADC external triggers input pins can be connected to the eTPU, the eMIOS, or an external signal. The  source  is  selected  by  configuring  the  eQADC  trigger  source  in  the  SIU\_ETISR  register.  See Section 6.3.1.15, 'eQADC Trigger Input Select Register (SIU\_ETISR).'

ETRIG0 is the external trigger for CFIFO0, CFIFO2, and CFIFO4, and ETRIG1 serves as the external trigger for CFIFO1, CFIFO3, and CFIFO5.

## 19.2.1.17 Voltage Reference High and Voltage Reference Low (VRH, VRL)

VRH and VRL are voltage references for the ADCs. VRH is the highest voltage reference, while VRL is the lowest voltage reference.

## 19.2.1.18 Power Supplies for Analog Components (V DDA,  V SSA )

VDDA  is the positive power supply pin for the ADCs and V SSA  is the negative power supply pin for the ADCs. Refer to electrical specifications.

## 19.2.1.19 Reference Bypass Capacitor (REFBYPC)

The REFBYPC pin is used to connect an external bias capacitor between the REFBYPC pin and VRL. The value of this capacitor should be 100nF. This bypass capacitor is used to provide a stable reference voltage for the ADC.

## 19.3 Memory Map/Register Definition

This section provides memory maps and detailed descriptions of all registers. Data written to or read from reserved areas of the memory map is undefined.

## 19.3.1 eQADC Memory Map

This section provides memory maps for the eQADC.

## Table 19-2. eQADC Memory Map

| Address            | Register Name   | Register Description                           | Size (bits)   |
|--------------------|-----------------|------------------------------------------------|---------------|
| Base (0xFFF8_0000) | EQADC_MCR       | EQADC module configuration register            | 32            |
| Base + 0x004       | -               | Reserved                                       | -             |
| Base + 0x008       | EQADC_NMSFR     | eQADC null message send format register        | 32            |
| Base + 0x00C       | EQADC_ETDFR     | eQADC external trigger digital filter register | 32            |
| Base + 0x010       | EQADC_CFPR0     | eQADC command FIFO push register 0             | 32            |
| Base + 0x014       | EQADC_CFPR1     | eQADC command FIFO push register 1             | 32            |
| Base + 0x018       | EQADC_CFPR2     | eQADC command FIFO push register 2             | 32            |
| Base + 0x01C       | EQADC_CFPR3     | eQADC command FIFO push register 3             | 32            |
| Base + 0x020       | EQADC_CFPR4     | eQADC command FIFO push register 4             | 32            |
| Base + 0x024       | EQADC_CFPR5     | eQADC command FIFO push register 5             | 32            |
| Base + 0x028       | -               | Reserved                                       | -             |
| Base + 0x02C       | -               | Reserved                                       | -             |
| Base + 0x030       | EQADC_RFPR0     | eQADC result FIFO pop register 0               | 32            |
| Base + 0x034       | EQADC_RFPR1     | eQADC result FIFO pop register 1               | 32            |
| Base + 0x038       | EQADC_RFPR2     | eQADC result FIFO pop register 2               | 32            |
| Base + 0x03C       | EQADC_RFPR3     | eQADC result FIFO pop register 3               | 32            |
| Base + 0x040       | EQADC_RFPR4     | eQADC result FIFO pop register 4               | 32            |
| Base + 0x044       | EQADC_RFPR5     | eQADC result FIFO pop register 5               | 32            |
| Base + 0x048       | -               | Reserved                                       | -             |
| Base + 0x04C       | -               | Reserved                                       | -             |
| Base + 0x050       | EQADC_CFCR0     | eQADC command FIFO control register 0          | 16            |
| Base + 0x052       | EQADC_CFCR1     | eQADC command FIFO control register 1          | 16            |
| Base + 0x054       | EQADC_CFCR2     | eQADC command FIFO control register 2          | 16            |
| Base + 0x056       | EQADC_CFCR3     | eQADC command FIFO control register 3          | 16            |
| Base + 0x058       | EQADC_CFCR4     | eQADC command FIFO control register 4          | 16            |
| Base + 0x05A       | EQADC_CFCR5     | eQADC command FIFO control register 5          | 16            |
| Base + 0x05C       | -               | Reserved                                       | -             |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 19-2. eQADC Memory Map (continued)

| Address                    | Register Name   | Register Description                                | Size (bits)   |
|----------------------------|-----------------|-----------------------------------------------------|---------------|
| Base + 0x060               | EQADC_IDCR0     | eQADC interrupt and eDMA control register 0         | 16            |
| Base + 0x062               | EQADC_IDCR1     | eQADC interrupt and eDMA control register 1         | 16            |
| Base + 0x064               | EQADC_IDCR2     | eQADC interrupt and eDMA control register 2         | 16            |
| Base + 0x066               | EQADC_IDCR3     | eQADC interrupt and eDMA control register 3         | 16            |
| Base + 0x068               | EQADC_IDCR4     | eQADC interrupt and eDMA control register 4         | 16            |
| Base + 0x06A               | EQADC_IDCR5     | eQADC interrupt and eDMA control register 5         | 16            |
| Base + 0x06C               | -               | Reserved                                            | -             |
| Base + 0x070               | EQADC_FISR0     | eQADC FIFO and interrupt status register 0          | 32            |
| Base + 0x074               | EQADC_FISR1     | eQADC FIFO and interrupt status register 1          | 32            |
| Base + 0x078               | EQADC_FISR2     | eQADC FIFO and interrupt status register 2          | 32            |
| Base + 0x07C               | EQADC_FISR3     | eQADC FIFO and interrupt status register 3          | 32            |
| Base + 0x080               | EQADC_FISR4     | eQADC FIFO and interrupt status register 4          | 32            |
| Base + 0x084               | EQADC_FISR5     | eQADC FIFO and interrupt status register 5          | 32            |
| Base + 0x088               | -               | Reserved                                            | -             |
| Base + 0x08C               | -               | Reserved                                            | -             |
| Base + 0x090               | EQADC_CFTCR0    | eQADC command FIFO transfer counter register 0      | 16            |
| Base + 0x092               | EQADC_CFTCR1    | eQADC command FIFO transfer counter register 1      | 16            |
| Base + 0x094               | EQADC_CFTCR2    | eQADC command FIFO transfer counter register 2      | 16            |
| Base + 0x096               | EQADC_CFTCR3    | eQADC command FIFO transfer counter register 3      | 16            |
| Base + 0x098               | EQADC_CFTCR4    | eQADC command FIFO transfer counter register 4      | 16            |
| Base + 0x09A               | EQADC_CFTCR5    | eQADC command FIFO transfer counter register 5      | 16            |
| Base + 0x09C               | -               | Reserved                                            | -             |
| Base + 0x0A0               | EQADC_CFSSR0    | eQADC command FIFO status snapshot register 0       | 32            |
| Base + 0x0A4               | EQADC_CFSSR1    | eQADC command FIFO status snapshot register 1       | 32            |
| Base + 0x0A8               | EQADC_CFSSR2    | eQADC command FIFO status snapshot register 2       | 32            |
| Base + 0x0AC               | EQADC_CFSR      | eQADC command FIFO status register                  | 32            |
| Base + 0x0B0               | -               | Reserved                                            | -             |
| Base + 0x0B4               | EQADC_SSICR     | eQADC synchronous serial interface control register | 32            |
| Base + 0x0B8               | EQADC_SSIRDR    | eQADC synchronous serial interface receive data     | 32            |
| Base + 0x0BC- Base + 0x0FC | -               | Reserved                                            | -             |
| Base + 0x100- Base + 0x10C | EQADC_CF0R n    | eQADC CFIFO0 registers 0-3                          | 32            |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## Table 19-2. eQADC Memory Map (continued)

| Address                    | Register Name   | Register Description       | Size (bits)   |
|----------------------------|-----------------|----------------------------|---------------|
| Base + 0x110- Base + 0x13C | -               | Reserved                   | -             |
| Base + 0x140- Base + 0x14C | EQADC_CF1R n    | eQADC CFIFO1 registers 0-3 | 32            |
| Base + 0x150- Base + 0x17C | -               | Reserved                   | -             |
| Base + 0x180- Base + 0x18C | EQADC_CF2R n    | eQADC CFIFO2 registers 0-3 | 32            |
| Base + 0x190- Base + 0x1BC | -               | Reserved                   | -             |
| Base + 0x1C0- Base + 0x1CC | EQADC_CF3R n    | eQADC CFIFO3 registers 0-3 | 32            |
| Base + 0x1D0- Base + 0x1FC | -               | Reserved                   | -             |
| Base + 0x200- Base + 0x20C | EQADC_CF4R n    | eQADC CFIFO4 registers 0-3 | 32            |
| Base + 0x210- Base + 0x23C | -               | Reserved                   | -             |
| Base + 0x240- Base + 0x24C | EQADC_CF5R n    | eQADC CFIFO5 registers 0-3 | 32            |
| Base + 0x250- Base + 0x2FC | -               | Reserved                   | -             |
| Base + 0x300- Base + 0x30C | EQADC_RF0R n    | eQADC RFIFO0 registers 0-3 | 32            |
| Base + 0x310- Base + 0x33C | -               | Reserved                   | -             |
| Base + 0x340- Base + 0x34C | EQADC_RF1R n    | eQADC RFIFO1 registers 0-3 | 32            |
| Base + 0x350- Base + 0x37C | -               | Reserved                   | -             |
| Base + 0x380- Base + 0x38C | EQADC_RF2R n    | eQADC RFIFO2 registers 0-3 | 32            |
| Base + 0x390- Base + 0x3BC | -               | Reserved                   | -             |
| Base + 0x3C0- Base + 0x3CC | EQADC_RF3R n    | eQADC RFIFO3 registers 0-3 | 32            |
| Base + 0x3D0- Base + 0x3FC | -               | Reserved                   | -             |
| Base + 0x400- Base + 0x40C | EQADC_RF4R n    | eQADC RFIFO4 registers 0-3 | 32            |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 19-2. eQADC Memory Map (continued)

| Address                    | Register Name   | Register Description       | Size (bits)   |
|----------------------------|-----------------|----------------------------|---------------|
| Base + 0x410- Base + 0x43C | -               | Reserved                   | -             |
| Base + 0x440- Base + 0x44C | EQADC_RF5R n    | eQADC RFIFO5 registers 0-3 | 32            |
| Base + 0x450- Base + 0x7FC | -               | Reserved                   | -             |

## 19.3.2 eQADC Register Descriptions

## 19.3.2.1 eQADC Module Configuration Register (EQADC\_MCR)

The EQADC\_MCR contains bits used to control how the eQADC responds to a debug mode entry request, and to enable the eQADC SSI interface.

Figure 19-2. eQADC Module Configuration Register (EQADC\_MCR)

<!-- image -->

|          | 0           | 1           | 2           | 3           | 4           | 5           | 6           | 7           | 8           | 9           | 10          | 11          | 12          | 13          | 14          | 15          |
|----------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|
| R        | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           |
| W        |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |
| Reset    | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           |
| Reg Addr | Base+ 0x000 | Base+ 0x000 | Base+ 0x000 | Base+ 0x000 | Base+ 0x000 | Base+ 0x000 | Base+ 0x000 | Base+ 0x000 | Base+ 0x000 | Base+ 0x000 | Base+ 0x000 | Base+ 0x000 | Base+ 0x000 | Base+ 0x000 | Base+ 0x000 | Base+ 0x000 |
|          | 16          | 17          | 18          | 19          | 20          | 21          | 22          | 23          | 24          | 25          | 26          | 27          | 28          | 29          | 30          | 31          |
| R        | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | ESSIE       | ESSIE       | 0           | DBG         | DBG         |
| W        |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |             |
| Reset    | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           | 0           |
| Reg Addr | Base+ 0x000 | Base+ 0x000 | Base+ 0x000 | Base+ 0x000 | Base+ 0x000 | Base+ 0x000 | Base+ 0x000 | Base+ 0x000 | Base+ 0x000 | Base+ 0x000 | Base+ 0x000 | Base+ 0x000 | Base+ 0x000 | Base+ 0x000 | Base+ 0x000 | Base+ 0x000 |

Table 19-3. EQADC\_MCR Field Descriptions

| Bits   | Name        | Description                                                                                                                                                                                                                                                                                                      |
|--------|-------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-26   | -           | Reserved.                                                                                                                                                                                                                                                                                                        |
| 27-28  | ESSIE [0:1] | eQADC synchronous serial interface enable. Defines the eQADC synchronous serial interface operation. 00 eQADC SSI is disabled 01 Reserved 10 eQADC SSI is enabled, FCK is free running, and serial transmissions are disabled 11 eQADC SSI is enabled, FCK is free running, and serial transmissions are enabled |

Table 19-3. EQADC\_MCR Field Descriptions

| Bits   | Name      | Description                                                                                                                                                                                                                                                                                                      |
|--------|-----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 29     | -         | Reserved.                                                                                                                                                                                                                                                                                                        |
| 30-31  | DBG [0:1] | Debug enable. Defines the eQADC response to a debug mode entry request. 00 Do not enter debug mode 01 Reserved 10 Enter debug mode. If the eQADC SSI is enabled, FCK stops while the eQADC is in debug mode. 11 Enter debug mode. If the eQADCSSIis enabled, FCKis free running while the eQADC is in debug mode |

## NOTE

Disabling the eQADC SSI (0b00 write to ESSIE) or serial transmissions from the eQADC SSI (0b10 write to ESSIE) while a serial transmission is in progress results in the abort of that transmission.

## NOTE

When disabling the eQADC SSI, the FCK will not stop until it reaches its low phase.

## 19.3.2.2 eQADC Null Message Send Format Register (EQADC\_NMSFR)

The EQADC\_NMSFR defines the format of the null message sent to the external device.

Figure 19-3. eQADC Null Message Send Format Register (EQADC\_NMSFR)

<!-- image -->

|          | 0            | 1            | 2            | 3            | 4            | 5            | 6            | 7            | 8            | 9            | 10           | 11           | 12           | 13           | 14           | 15           |
|----------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|
| R        | 0            | 0            | 0            | 0            | 0            | 0            | NMF          | NMF          | NMF          | NMF          | NMF          | NMF          | NMF          | NMF          | NMF          | NMF          |
| W        |              |              |              |              |              |              |              |              |              |              |              |              |              |              |              |              |
| Reset    | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            |
| Reg Addr | Base + 0x008 | Base + 0x008 | Base + 0x008 | Base + 0x008 | Base + 0x008 | Base + 0x008 | Base + 0x008 | Base + 0x008 | Base + 0x008 | Base + 0x008 | Base + 0x008 | Base + 0x008 | Base + 0x008 | Base + 0x008 | Base + 0x008 | Base + 0x008 |
|          | 16           | 17           | 18           | 19           | 20           | 21           | 22           | 23           | 24           | 25           | 26           | 27           | 28           | 29           | 30           | 31           |
| R        | NMF          | NMF          | NMF          | NMF          | NMF          | NMF          | NMF          | NMF          | NMF          | NMF          | NMF          | NMF          | NMF          | NMF          | NMF          | NMF          |
| W        |              |              |              |              |              |              |              |              |              |              |              |              |              |              |              |              |
| Reset    | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            |
| Reg Addr | Base + 0x008 | Base + 0x008 | Base + 0x008 | Base + 0x008 | Base + 0x008 | Base + 0x008 | Base + 0x008 | Base + 0x008 | Base + 0x008 | Base + 0x008 | Base + 0x008 | Base + 0x008 | Base + 0x008 | Base + 0x008 | Base + 0x008 | Base + 0x008 |

## Table 19-4. EQADC\_NMSFR Field Descriptions

| Bits   | Name       | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
|--------|------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-5    | -          | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| 6-31   | NMF [0:25] | Null message format. Contains the programmable null message send value for the eQADC. The value written to this register will be sent as a null message when serial transmissions from the eQADC SSI are enabled (ESSIE field is configured to 0b11 in EQADC_MCR (Section 19.3.2.1)) and either GLYPH<127> there are no triggered CFIFOs with commands bound for external command buffers, or; GLYPH<127> there are triggered CFIFOs with commands bound for external command buffers but the external command buffers are full. Refer to Section for more information on the format of a null message. |

## NOTE

The eQADC null message send format register only affects how the eQADC sends a null message, but it has no control on how the eQADC detects a null message on receiving data. The eQADC detects a null message by decoding the MESSAGE\_TAG field on the receive data. Refer to  Table 19-34 for more information on the MESSAGE\_TAG field.

## NOTE

Writing  to  the  eQADC  null  message  send  format  register  while  serial transmissions are enabled is not recommended (See EQADC\_MCR[ESSIE] field in Section 19.3.2.1).

## 19.3.2.3 eQADC External Trigger Digital Filter Register (EQADC\_ETDFR)

The EQADC\_ETDFR is used to set the minimum time a signal must be held in a logic state on the CFIFO triggers inputs to be recognized as an edge or level gated trigger. The digital filter length field specifies the minimum number of system clocks that must be counted by the digital filter counter to recognize a logic state change.

Figure 19-4. eQADC External Trigger Digital Filter Register (EQADC\_ETDFR)

<!-- image -->

## Table 19-5. EQADC\_ETDFR Field Description Table

| Bits   | Name      | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
|--------|-----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-27   | -         | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| 28-31  | DFL [0:3] | Digital filter length. Specifies the minimum number of system clocks that must be counted by the digital filter counter to recognize a logic state change. The count specifies the sample period of the digital filter which is calculated according to the following equation: Minimum clock counts for which an ETRIG signal needs to be stable to be passed through the filter are shown in Table 19-6. Refer to Section 19.4.3.4, 'External Trigger Event Detection,' for more information on the digital filter. Note: The DFL field must only be written when the MODE n of all CFIFOs are configured to disabled. FilterPeriod SystemClockPeriod ( 2 DFL ) × 1 SystemClockPeriod ( ) + = |

## Table 19-6. Minimum Required Time to Valid ETRIG

| DFL[0:3]   |   Minimum Clock Count |   Minimum Time (ns) (System Clock = 120MHz) |
|------------|-----------------------|---------------------------------------------|
| 0b0000     |                     2 |                                       16.67 |
| 0b0001     |                     3 |                                       25    |
| 0b0010     |                     5 |                                       41.67 |
| 0b0011     |                     9 |                                       75    |
| 0b0100     |                    17 |                                      141.67 |
| 0b0101     |                    33 |                                      275    |
| 0b0110     |                    65 |                                      541.67 |
| 0b0111     |                   129 |                                     1075    |
| 0b1000     |                   257 |                                     2141.67 |
| 0b1001     |                   513 |                                     4275    |
| 0b1010     |                  1025 |                                     8541.67 |
| 0b1011     |                  2049 |                                    17075    |
| 0b1100     |                  4097 |                                    34141.7  |
| 0b1101     |                  8193 |                                    68275    |
| 0b1110     |                 16385 |                                   136542    |
| 0b1111     |                 32769 |                                   273075    |

## 19.3.2.4 eQADC CFIFO Push Registers 0-5 (EQADC\_CFPR n )

The EQADC\_CFPRs provide a mechanism to fill the CFIFOs with command messages from the command queues. Refer to Section 19.4.3, 'eQADC Command FIFOs,' for more information on the CFIFOs and to Section 19.4.1.2, 'Message Format in eQADC,' for a description on command message formats.

Figure 19-5. eQADC CFIFO Push Registers (EQADC\_CFPR n )

<!-- image -->

|          | 0                                                                                                                                                                      | 1                                                                                                                                                                      | 2                                                                                                                                                                      | 3                                                                                                                                                                      | 4                                                                                                                                                                      | 5                                                                                                                                                                      | 6                                                                                                                                                                      | 7                                                                                                                                                                      | 8                                                                                                                                                                      | 9                                                                                                                                                                      | 10                                                                                                                                                                     | 11                                                                                                                                                                     | 12                                                                                                                                                                     | 13                                                                                                                                                                     | 14                                                                                                                                                                     | 15                                                                                                                                                                     |
|----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| R        | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      |
| W        | CF_PUSH n                                                                                                                                                              | CF_PUSH n                                                                                                                                                              | CF_PUSH n                                                                                                                                                              | CF_PUSH n                                                                                                                                                              | CF_PUSH n                                                                                                                                                              | CF_PUSH n                                                                                                                                                              | CF_PUSH n                                                                                                                                                              | CF_PUSH n                                                                                                                                                              | CF_PUSH n                                                                                                                                                              | CF_PUSH n                                                                                                                                                              | CF_PUSH n                                                                                                                                                              | CF_PUSH n                                                                                                                                                              | CF_PUSH n                                                                                                                                                              | CF_PUSH n                                                                                                                                                              | CF_PUSH n                                                                                                                                                              | CF_PUSH n                                                                                                                                                              |
| Reset    | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      |
| Reg Addr | Base + 0x010 (EQADC_CFPR0); Base + 0x014 (EQADC_CFPR1); Base + 0x018 (EQADC_CFPR2); Base + 0x01C (EQADC_CFPR3); Base + 0x020 (EQADC_CFPR4); Base + 0x024 (EQADC_CFPR5) | Base + 0x010 (EQADC_CFPR0); Base + 0x014 (EQADC_CFPR1); Base + 0x018 (EQADC_CFPR2); Base + 0x01C (EQADC_CFPR3); Base + 0x020 (EQADC_CFPR4); Base + 0x024 (EQADC_CFPR5) | Base + 0x010 (EQADC_CFPR0); Base + 0x014 (EQADC_CFPR1); Base + 0x018 (EQADC_CFPR2); Base + 0x01C (EQADC_CFPR3); Base + 0x020 (EQADC_CFPR4); Base + 0x024 (EQADC_CFPR5) | Base + 0x010 (EQADC_CFPR0); Base + 0x014 (EQADC_CFPR1); Base + 0x018 (EQADC_CFPR2); Base + 0x01C (EQADC_CFPR3); Base + 0x020 (EQADC_CFPR4); Base + 0x024 (EQADC_CFPR5) | Base + 0x010 (EQADC_CFPR0); Base + 0x014 (EQADC_CFPR1); Base + 0x018 (EQADC_CFPR2); Base + 0x01C (EQADC_CFPR3); Base + 0x020 (EQADC_CFPR4); Base + 0x024 (EQADC_CFPR5) | Base + 0x010 (EQADC_CFPR0); Base + 0x014 (EQADC_CFPR1); Base + 0x018 (EQADC_CFPR2); Base + 0x01C (EQADC_CFPR3); Base + 0x020 (EQADC_CFPR4); Base + 0x024 (EQADC_CFPR5) | Base + 0x010 (EQADC_CFPR0); Base + 0x014 (EQADC_CFPR1); Base + 0x018 (EQADC_CFPR2); Base + 0x01C (EQADC_CFPR3); Base + 0x020 (EQADC_CFPR4); Base + 0x024 (EQADC_CFPR5) | Base + 0x010 (EQADC_CFPR0); Base + 0x014 (EQADC_CFPR1); Base + 0x018 (EQADC_CFPR2); Base + 0x01C (EQADC_CFPR3); Base + 0x020 (EQADC_CFPR4); Base + 0x024 (EQADC_CFPR5) | Base + 0x010 (EQADC_CFPR0); Base + 0x014 (EQADC_CFPR1); Base + 0x018 (EQADC_CFPR2); Base + 0x01C (EQADC_CFPR3); Base + 0x020 (EQADC_CFPR4); Base + 0x024 (EQADC_CFPR5) | Base + 0x010 (EQADC_CFPR0); Base + 0x014 (EQADC_CFPR1); Base + 0x018 (EQADC_CFPR2); Base + 0x01C (EQADC_CFPR3); Base + 0x020 (EQADC_CFPR4); Base + 0x024 (EQADC_CFPR5) | Base + 0x010 (EQADC_CFPR0); Base + 0x014 (EQADC_CFPR1); Base + 0x018 (EQADC_CFPR2); Base + 0x01C (EQADC_CFPR3); Base + 0x020 (EQADC_CFPR4); Base + 0x024 (EQADC_CFPR5) | Base + 0x010 (EQADC_CFPR0); Base + 0x014 (EQADC_CFPR1); Base + 0x018 (EQADC_CFPR2); Base + 0x01C (EQADC_CFPR3); Base + 0x020 (EQADC_CFPR4); Base + 0x024 (EQADC_CFPR5) | Base + 0x010 (EQADC_CFPR0); Base + 0x014 (EQADC_CFPR1); Base + 0x018 (EQADC_CFPR2); Base + 0x01C (EQADC_CFPR3); Base + 0x020 (EQADC_CFPR4); Base + 0x024 (EQADC_CFPR5) | Base + 0x010 (EQADC_CFPR0); Base + 0x014 (EQADC_CFPR1); Base + 0x018 (EQADC_CFPR2); Base + 0x01C (EQADC_CFPR3); Base + 0x020 (EQADC_CFPR4); Base + 0x024 (EQADC_CFPR5) | Base + 0x010 (EQADC_CFPR0); Base + 0x014 (EQADC_CFPR1); Base + 0x018 (EQADC_CFPR2); Base + 0x01C (EQADC_CFPR3); Base + 0x020 (EQADC_CFPR4); Base + 0x024 (EQADC_CFPR5) | Base + 0x010 (EQADC_CFPR0); Base + 0x014 (EQADC_CFPR1); Base + 0x018 (EQADC_CFPR2); Base + 0x01C (EQADC_CFPR3); Base + 0x020 (EQADC_CFPR4); Base + 0x024 (EQADC_CFPR5) |
|          | 16                                                                                                                                                                     | 17                                                                                                                                                                     | 18                                                                                                                                                                     | 19                                                                                                                                                                     | 20                                                                                                                                                                     | 21                                                                                                                                                                     | 22                                                                                                                                                                     | 23                                                                                                                                                                     | 24                                                                                                                                                                     | 25                                                                                                                                                                     | 26                                                                                                                                                                     | 27                                                                                                                                                                     | 28                                                                                                                                                                     | 29                                                                                                                                                                     | 30                                                                                                                                                                     | 31                                                                                                                                                                     |
| R        | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      |
| W        | CF_PUSH n                                                                                                                                                              | CF_PUSH n                                                                                                                                                              | CF_PUSH n                                                                                                                                                              | CF_PUSH n                                                                                                                                                              | CF_PUSH n                                                                                                                                                              | CF_PUSH n                                                                                                                                                              | CF_PUSH n                                                                                                                                                              | CF_PUSH n                                                                                                                                                              | CF_PUSH n                                                                                                                                                              | CF_PUSH n                                                                                                                                                              | CF_PUSH n                                                                                                                                                              | CF_PUSH n                                                                                                                                                              | CF_PUSH n                                                                                                                                                              | CF_PUSH n                                                                                                                                                              | CF_PUSH n                                                                                                                                                              | CF_PUSH n                                                                                                                                                              |
| Reset    | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      |
| Reg Addr | Base + 0x010 (EQADC_CFPR0); Base + 0x014 (EQADC_CFPR1); Base + 0x018 (EQADC_CFPR2); Base + 0x01C (EQADC_CFPR3); Base + 0x020 (EQADC_CFPR4); Base + 0x024 (EQADC_CFPR5) | Base + 0x010 (EQADC_CFPR0); Base + 0x014 (EQADC_CFPR1); Base + 0x018 (EQADC_CFPR2); Base + 0x01C (EQADC_CFPR3); Base + 0x020 (EQADC_CFPR4); Base + 0x024 (EQADC_CFPR5) | Base + 0x010 (EQADC_CFPR0); Base + 0x014 (EQADC_CFPR1); Base + 0x018 (EQADC_CFPR2); Base + 0x01C (EQADC_CFPR3); Base + 0x020 (EQADC_CFPR4); Base + 0x024 (EQADC_CFPR5) | Base + 0x010 (EQADC_CFPR0); Base + 0x014 (EQADC_CFPR1); Base + 0x018 (EQADC_CFPR2); Base + 0x01C (EQADC_CFPR3); Base + 0x020 (EQADC_CFPR4); Base + 0x024 (EQADC_CFPR5) | Base + 0x010 (EQADC_CFPR0); Base + 0x014 (EQADC_CFPR1); Base + 0x018 (EQADC_CFPR2); Base + 0x01C (EQADC_CFPR3); Base + 0x020 (EQADC_CFPR4); Base + 0x024 (EQADC_CFPR5) | Base + 0x010 (EQADC_CFPR0); Base + 0x014 (EQADC_CFPR1); Base + 0x018 (EQADC_CFPR2); Base + 0x01C (EQADC_CFPR3); Base + 0x020 (EQADC_CFPR4); Base + 0x024 (EQADC_CFPR5) | Base + 0x010 (EQADC_CFPR0); Base + 0x014 (EQADC_CFPR1); Base + 0x018 (EQADC_CFPR2); Base + 0x01C (EQADC_CFPR3); Base + 0x020 (EQADC_CFPR4); Base + 0x024 (EQADC_CFPR5) | Base + 0x010 (EQADC_CFPR0); Base + 0x014 (EQADC_CFPR1); Base + 0x018 (EQADC_CFPR2); Base + 0x01C (EQADC_CFPR3); Base + 0x020 (EQADC_CFPR4); Base + 0x024 (EQADC_CFPR5) | Base + 0x010 (EQADC_CFPR0); Base + 0x014 (EQADC_CFPR1); Base + 0x018 (EQADC_CFPR2); Base + 0x01C (EQADC_CFPR3); Base + 0x020 (EQADC_CFPR4); Base + 0x024 (EQADC_CFPR5) | Base + 0x010 (EQADC_CFPR0); Base + 0x014 (EQADC_CFPR1); Base + 0x018 (EQADC_CFPR2); Base + 0x01C (EQADC_CFPR3); Base + 0x020 (EQADC_CFPR4); Base + 0x024 (EQADC_CFPR5) | Base + 0x010 (EQADC_CFPR0); Base + 0x014 (EQADC_CFPR1); Base + 0x018 (EQADC_CFPR2); Base + 0x01C (EQADC_CFPR3); Base + 0x020 (EQADC_CFPR4); Base + 0x024 (EQADC_CFPR5) | Base + 0x010 (EQADC_CFPR0); Base + 0x014 (EQADC_CFPR1); Base + 0x018 (EQADC_CFPR2); Base + 0x01C (EQADC_CFPR3); Base + 0x020 (EQADC_CFPR4); Base + 0x024 (EQADC_CFPR5) | Base + 0x010 (EQADC_CFPR0); Base + 0x014 (EQADC_CFPR1); Base + 0x018 (EQADC_CFPR2); Base + 0x01C (EQADC_CFPR3); Base + 0x020 (EQADC_CFPR4); Base + 0x024 (EQADC_CFPR5) | Base + 0x010 (EQADC_CFPR0); Base + 0x014 (EQADC_CFPR1); Base + 0x018 (EQADC_CFPR2); Base + 0x01C (EQADC_CFPR3); Base + 0x020 (EQADC_CFPR4); Base + 0x024 (EQADC_CFPR5) | Base + 0x010 (EQADC_CFPR0); Base + 0x014 (EQADC_CFPR1); Base + 0x018 (EQADC_CFPR2); Base + 0x01C (EQADC_CFPR3); Base + 0x020 (EQADC_CFPR4); Base + 0x024 (EQADC_CFPR5) | Base + 0x010 (EQADC_CFPR0); Base + 0x014 (EQADC_CFPR1); Base + 0x018 (EQADC_CFPR2); Base + 0x01C (EQADC_CFPR3); Base + 0x020 (EQADC_CFPR4); Base + 0x024 (EQADC_CFPR5) |

Table 19-7. EQADC\_CFPR n Field Description

| Bits   | Name      | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
|--------|-----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-31   | CF_PUSH n | CFIFO push data n . When CFIFO n is not full, writing to the whole word or any bytes of EQADC_CFPR n will push the 32-bit CF_PUSH n value into CFIFO n . Writing to the CF_PUSH n field also increments the corresponding CFCTR n value by one in Section 19.3.2.8, 'eQADC FIFO and Interrupt Status Registers 0-5 (EQADC_FISRn).' When the CFIFO n is full, the eQADC ignores any write to the CF_PUSH n . Reading the EQADC_CFPR n always returns 0. Note: Only whole words must be written to EQADC_CFPR. Writing half-words or bytes to EQADC_CFPR will still push the whole 32-bit CF_PUSH field into the corresponding CFIFO, but undefined data will fill the areas of CF_PUSH that were not specifically designated as target locations for the write. |

## 19.3.2.5 eQADC Result FIFO Pop Registers 0-5 (EQADC\_RFPR n )

The eQADC\_RFPRs provide a mechanism to retrieve data from RFIFOs.

## NOTE

The EQADC\_RFPR   must n not be read speculatively. For future compatibility,  the  TLB  entry  covering  the  EQADC\_RFPR n must  be configured to be guarded.

Figure 19-6. eQADC RFIFO Pop Registers (EQADC\_RFPR n )

<!-- image -->

Table 19-8. EQADC\_RFPR n Field Description

| Bits   | Name            | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|--------|-----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-15   | -               | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| 16-31  | RF_POP n [0:15] | Result FIFO pop data n . When RFIFO n is not empty, the RF_POP n contains the next unread entry value of RFIFO n. Reading the whole word, a half-word, or any bytes of EQADC_RFPR n will pop one entry from RFIFO n , and the corresponding RFCTR n value will be decremented by 1 (See Section 19.3.2.8 ). When the RFIFO n is empty, any read on EQADC_RFPR n returns undefined data value and does not decrement the RFCTR n value. Writing to EQADC_RFPR n has no effect. |

## 19.3.2.6 eQADC CFIFO Control Registers 0-5 (EQADC\_CFCR n )

The eQADC\_CFCRs contain bits that affect CFIFOs. These bits specify the CFIFO operation mode and can invalidate all of the CFIFO contents.

Figure 19-7. eQADC CFIFO Control Registers (EQADC\_CFCR n )

<!-- image -->

Table 19-9. EQADC\_CFCR n Field Descriptions

| Bits   | Name         | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
|--------|--------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-4    | -            | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| 5      | SSE n        | CFIFO single-scan enable bit n . Used to set the SSS n bit, as described in Section 19.3.2.8. Writing a 1 to SSE n will set the SSS n if the CFIFO is in single-scan mode. When SSS n is already asserted, writing a 1 to SSE n has no effect. If the CFIFO is in continuous-scan mode or is disabled, writing a 1 to SSE n will not set SSS n . Writing a 0 to SSE n has no effect. SSE n always is read as 0. 0 No effect. 1 Set the SSS n bit.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| 6      | CFINV n      | CFIFO invalidate bit n . Causes the eQADC to invalidate all entries of CFIFO n . Writing a 1 to CFINV n will reset the value of CFCTR n in the EQADC_FISR register (refer to Section 19.3.2.8, 'eQADC FIFO and Interrupt Status Registers 0-5 (EQADC_FISRn).' Writing a 1 to CFINV n also resets the push next data pointer, transfer next data pointer to the first entry of CFIFO n in Figure 19-35. CFINV n always is read as 0. Writing a 0 has no effect. 0 No effect. 1 Invalidate all of the entries in the corresponding CFIFO. Note: Writing CFINV n only invalidates commands stored in CFIFO n ; previously transferred commands that are waiting for execution, that is commands stored in the ADC command buffers, will still be executed, and results generated by them will be stored in the appropriate RFIFO. Note: CFINV n must not be written unless the MODE n is configured to disabled, and CFIFO status is IDLE. |
| 7      | -            | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| 8-11   | MODE n [0:3] | CFIFO operation mode n . Selects the CFIFO operation mode for CFIFO n . Refer to Section 19.4.3.5, 'CFIFO Scan Trigger Modes ,' for more information on CFIFO trigger mode. Note: If MODE n is not disabled, it must not be changed to any other mode besides disabled. If MODE n is disabled and the CFIFO status is IDLE, MODE n can be changed to any other mode.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| 12-15  | -            | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |

Table 19-10. CFIFO Operation Mode Table

| MODE n [0:3]   | CFIFO Operation Mode                                 |
|----------------|------------------------------------------------------|
| 0b0000         | Disabled                                             |
| 0b0001         | Software trigger, single scan                        |
| 0b0010         | Low level gated external trigger, single scan        |
| 0b0011         | High level gated external trigger, single scan       |
| 0b0100         | Falling edge external trigger, single scan           |
| 0b0101         | Rising edge external trigger, single scan            |
| 0b0110         | Falling or rising edge external trigger, single scan |
| 0b0111-0b1000  | Reserved                                             |
| 0b1001         | Software trigger, continuous scan                    |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 19-10. CFIFO Operation Mode Table (continued)

| MODE n [0:3]   | CFIFO Operation Mode                                     |
|----------------|----------------------------------------------------------|
| 0b1010         | Low level gated external trigger, continuous scan        |
| 0b1011         | High level gated external trigger, continuous scan       |
| 0b1100         | Falling edge external trigger, continuous scan           |
| 0b1101         | Rising edge external trigger, continuous scan            |
| 0b1110         | Falling or rising edge external trigger, continuous scan |
| 0b1111         | Reserved                                                 |

## 19.3.2.7 eQADC Interrupt and eDMA Control Registers 0-5 (EQADC\_IDCR n )

The  eQADC\_IDCRs  contain  bits  to  enable  the  generation  of  interrupt  or  eDMA  requests  when  the corresponding flag bits are set in EQADC\_FISRn (Section 19.3.2.8).

Figure 19-8. eQADC Interrupt and eDMA Control Registers (EQADC\_IDCR n )

<!-- image -->

Table 19-11. EQADC\_IDCR n Field Descriptions

|   Bits | Name    | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|--------|---------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|      0 | NCIE n  | Non-coherency interrupt enable n . Enables the eQADC to generate an interrupt request when the corresponding NCF n , described in Section 19.3.2.8, is asserted. 0 Disable non-coherency interrupt request 1 Enable non-coherency interrupt request                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
|      1 | TORIE n | Trigger overrun interrupt enable n . Enables the eQADC to generate an interrupt request when the corresponding TORF n (described in Section 19.3.2.8) is asserted. Apart from generating an independent interrupt request for a CFIFO n trigger overrun event, the eQADC also provides a combined interrupt at which the result FIFO overflow interrupt, the command FIFO underflow interrupt, and the command FIFO trigger overrun interrupt requests of all CFIFOs are ORed. When RFOIE n , CFUIE n , and TORIE n are all asserted, this combined interrupt request is asserted whenever one of the following 18 flags becomes asserted: RFOF n , CFUF n , and TORF n (assuming that all interrupts are enabled). See Section 19.4.7, 'eQADC eDMA/Interrupt Request ,' for details. 0 Disable trigger overrun interrupt request 1 Enable trigger overrun interrupt request |
|      2 | PIE n   | Pause interrupt enable n . Enables the eQADC to generate an interrupt request when the corresponding PFx in EQADC_FISRn (See Section 19.3.2.8 ) is asserted. 0 Disable pause interrupt request 1 Enable pause interrupt request                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## Table 19-11. EQADC\_IDCR n Field Descriptions (continued)

| Bits   | Name    | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
|--------|---------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 3      | EOQIE n | End-of-queue interrupt enable n . Enables the eQADC to generate an interrupt request when the corresponding EOQF n in EQADC_FISRn (See Section 19.3.2.8 ) is asserted. 0 Disable end of queue interrupt request. 1 Enable end of queue interrupt request.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| 4      | CFUIE n | CFIFO underflow interrupt enable n . Enables the eQADC to generate an interrupt request when the corresponding CFUF n in EQADC_FISRn (See Section 19.3.2.8 ) is asserted. Apart from generating an independent interrupt request for a CFIFO n underflow event, the eQADC also provides a combined interrupt at which the result FIFO overflow interrupt, the command FIFO underflow interrupt, and the command FIFO trigger overrun interrupt requests of all CFIFOs are ORed. When RFOIE n , CFUIE n , and TORIE n are all asserted, this combined interrupt request is asserted whenever one of the following 18 flags becomes asserted: RFOF n , CFUF n , and TORF n (assuming that all interrupts are enabled). See Section 19.4.7, 'eQADC eDMA/Interrupt Request,' for details. 0 Disable underflow interrupt request 1 Enable underflow interrupt request |
| 5      | -       | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| 6      | CFFE n  | CFIFO fill enable n . Enables the eQADC to generate an interrupt request (CFFS n is asserted) or eDMA request (CFFS n is negated) when CFFF n in EQADC_FISRn (Section 19.3.2.8 ) is asserted. 0 Disable CFIFO fill eDMA or interrupt request 1 Enable CFIFO fill eDMA or interrupt request Note: CFFE n must not be negated while an eDMA transaction is in progress.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| 7      | CFFS n  | CFIFO fill select n . Selects if an eDMA or interrupt request is generated when CFFF n in EQADC_FISRn (See Section 19.3.2.8 ) is asserted. If CFFE n is asserted, the eQADC generates an interrupt request when CFFS n is negated, or it generates an eDMA request if CFFS n is asserted. 0 Generate interrupt request to move data from the system memory to CFIFO n . 1 Generate eDMA request to move data from the system memory to CFIFO n . Note: CFFS n must not be negated while an eDMA transaction is in progress.                                                                                                                                                                                                                                                                                                                                      |
| 8-11   | -       | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| 12     | RFOIE n | RFIFO overflow interrupt enable n . Enables the eQADC to generate an interrupt request when the corresponding RFOF n in EQADC_FISRn (See Section 19.3.2.8 ) is asserted. Apart from generating an independent interrupt request for an RFIFO n overflow event, the eQADCalso provides a combined interrupt at which the result FIFO overflow Interrupt, the command FIFO underflow interrupt, and the command FIFO trigger overrun interrupt requests of all CFIFOs are ORed. When RFOIE n , CFUIE n, and TORIE n are all asserted, this combined interrupt request is asserted whenever one of the following 18 flags becomes asserted: RFOF n, CFUF n , and TORF n (assuming that all interrupts are enabled). See Section 19.4.7, 'eQADC eDMA/Interrupt Request,' for details. 0 Disable overflow interrupt request 1 Enable overflow Interrupt request       |
| 13     | -       | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |

## Table 19-11. EQADC\_IDCR n Field Descriptions (continued)

|   Bits | Name   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|--------|--------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|     14 | RFDE n | RFIFO drain enable n . Enables the eQADC to generate an interrupt request (RFDS n is asserted) or eDMA request (RFDS n is negated) when RFDF n in EQADC_FISRn (See Section 19.3.2.8 ) is asserted. 0 Disable RFIFO drain eDMA or interrupt request 1 Enable RFIFO drain eDMA or interrupt request Note: RFDE n must not be negated while an eDMA transaction is in progress.                                                                                                                                              |
|     15 | RFDS n | RFIFO drain select n . Selects if an eDMA or interrupt request is generated when RFDF n in EQADC_FISRn (See Section 19.3.2.8 ) is asserted. If RFDE n is asserted, the eQADC generates an interrupt request when RFDS n is negated, or it generates an eDMA request when RFDS n is asserted. 0 Generate interrupt request to move data from RFIF n to the system memory 1 Generate eDMA request to move data from RFIFO n to the system memory Note: RFDS n must not be negated while an eDMA transaction is in progress. |

## 19.3.2.8 eQADC FIFO and Interrupt Status Registers 0-5 (EQADC\_FISR n )

The EQADC\_FISRs contain flag and status bits for each CFIFO and RFIFO pair. Writing 1 to a flag bit clears it. Writing 0 has no effect. Status bits are read only. These bits indicate the status of the FIFO itself.

Figure 19-9. eQADC FIFO and Interrupt Status Registers (EQADC\_FISR n )

<!-- image -->

|          | 0     | 1                                                                                                                                                                      | 2                                                                                                                                                                      | 3                                                                                                                                                                      | 4                                                                                                                                                                      | 5                                                                                                                                                                      | 6                                                                                                                                                                      | 7                                                                                                                                                                      | 8                                                                                                                                                                      | 9                                                                                                                                                                      | 10                                                                                                                                                                     | 11                                                                                                                                                                     | 12                                                                                                                                                                     | 13                                                                                                                                                                     | 14                                                                                                                                                                     | 15                                                                                                                                                                     |
|----------|-------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| R        | NCF n | TORF n                                                                                                                                                                 | PF n                                                                                                                                                                   | EOQF n                                                                                                                                                                 | CFUF n                                                                                                                                                                 | SSS n                                                                                                                                                                  | CFFF n                                                                                                                                                                 | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | RFOF n                                                                                                                                                                 | 0                                                                                                                                                                      | RFDF n                                                                                                                                                                 | 0                                                                                                                                                                      |
| W        | w1c   | w1c                                                                                                                                                                    | w1c                                                                                                                                                                    | w1c                                                                                                                                                                    | w1c                                                                                                                                                                    |                                                                                                                                                                        | w1c                                                                                                                                                                    |                                                                                                                                                                        |                                                                                                                                                                        |                                                                                                                                                                        |                                                                                                                                                                        |                                                                                                                                                                        | w1c                                                                                                                                                                    |                                                                                                                                                                        | w1c                                                                                                                                                                    |                                                                                                                                                                        |
| Reset    | 0     | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 1                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      |
| Reg Addr |       | Base + 0x070 (EQADC_FISR0); Base + 0x074 (EQADC_FISR1); Base + 0x078 (EQADC_FISR2); Base + 0x07C (EQADC_FISR3); Base + 0x080 (EQADC_FISR4); Base + 0x084 (EQADC_FISR5) | Base + 0x070 (EQADC_FISR0); Base + 0x074 (EQADC_FISR1); Base + 0x078 (EQADC_FISR2); Base + 0x07C (EQADC_FISR3); Base + 0x080 (EQADC_FISR4); Base + 0x084 (EQADC_FISR5) | Base + 0x070 (EQADC_FISR0); Base + 0x074 (EQADC_FISR1); Base + 0x078 (EQADC_FISR2); Base + 0x07C (EQADC_FISR3); Base + 0x080 (EQADC_FISR4); Base + 0x084 (EQADC_FISR5) | Base + 0x070 (EQADC_FISR0); Base + 0x074 (EQADC_FISR1); Base + 0x078 (EQADC_FISR2); Base + 0x07C (EQADC_FISR3); Base + 0x080 (EQADC_FISR4); Base + 0x084 (EQADC_FISR5) | Base + 0x070 (EQADC_FISR0); Base + 0x074 (EQADC_FISR1); Base + 0x078 (EQADC_FISR2); Base + 0x07C (EQADC_FISR3); Base + 0x080 (EQADC_FISR4); Base + 0x084 (EQADC_FISR5) | Base + 0x070 (EQADC_FISR0); Base + 0x074 (EQADC_FISR1); Base + 0x078 (EQADC_FISR2); Base + 0x07C (EQADC_FISR3); Base + 0x080 (EQADC_FISR4); Base + 0x084 (EQADC_FISR5) | Base + 0x070 (EQADC_FISR0); Base + 0x074 (EQADC_FISR1); Base + 0x078 (EQADC_FISR2); Base + 0x07C (EQADC_FISR3); Base + 0x080 (EQADC_FISR4); Base + 0x084 (EQADC_FISR5) | Base + 0x070 (EQADC_FISR0); Base + 0x074 (EQADC_FISR1); Base + 0x078 (EQADC_FISR2); Base + 0x07C (EQADC_FISR3); Base + 0x080 (EQADC_FISR4); Base + 0x084 (EQADC_FISR5) | Base + 0x070 (EQADC_FISR0); Base + 0x074 (EQADC_FISR1); Base + 0x078 (EQADC_FISR2); Base + 0x07C (EQADC_FISR3); Base + 0x080 (EQADC_FISR4); Base + 0x084 (EQADC_FISR5) | Base + 0x070 (EQADC_FISR0); Base + 0x074 (EQADC_FISR1); Base + 0x078 (EQADC_FISR2); Base + 0x07C (EQADC_FISR3); Base + 0x080 (EQADC_FISR4); Base + 0x084 (EQADC_FISR5) | Base + 0x070 (EQADC_FISR0); Base + 0x074 (EQADC_FISR1); Base + 0x078 (EQADC_FISR2); Base + 0x07C (EQADC_FISR3); Base + 0x080 (EQADC_FISR4); Base + 0x084 (EQADC_FISR5) | Base + 0x070 (EQADC_FISR0); Base + 0x074 (EQADC_FISR1); Base + 0x078 (EQADC_FISR2); Base + 0x07C (EQADC_FISR3); Base + 0x080 (EQADC_FISR4); Base + 0x084 (EQADC_FISR5) | Base + 0x070 (EQADC_FISR0); Base + 0x074 (EQADC_FISR1); Base + 0x078 (EQADC_FISR2); Base + 0x07C (EQADC_FISR3); Base + 0x080 (EQADC_FISR4); Base + 0x084 (EQADC_FISR5) | Base + 0x070 (EQADC_FISR0); Base + 0x074 (EQADC_FISR1); Base + 0x078 (EQADC_FISR2); Base + 0x07C (EQADC_FISR3); Base + 0x080 (EQADC_FISR4); Base + 0x084 (EQADC_FISR5) | Base + 0x070 (EQADC_FISR0); Base + 0x074 (EQADC_FISR1); Base + 0x078 (EQADC_FISR2); Base + 0x07C (EQADC_FISR3); Base + 0x080 (EQADC_FISR4); Base + 0x084 (EQADC_FISR5) |
|          | 16    | 17                                                                                                                                                                     | 18                                                                                                                                                                     | 19                                                                                                                                                                     | 20                                                                                                                                                                     | 21                                                                                                                                                                     | 22                                                                                                                                                                     | 23                                                                                                                                                                     | 24                                                                                                                                                                     | 25                                                                                                                                                                     | 26                                                                                                                                                                     | 27                                                                                                                                                                     | 28                                                                                                                                                                     | 29                                                                                                                                                                     | 30                                                                                                                                                                     | 31                                                                                                                                                                     |
| R        | CFCTR | CFCTR                                                                                                                                                                  | n                                                                                                                                                                      | CFCTR                                                                                                                                                                  |                                                                                                                                                                        | TNXTPTR n                                                                                                                                                              | TNXTPTR n                                                                                                                                                              | TNXTPTR n                                                                                                                                                              |                                                                                                                                                                        | RFCTR n                                                                                                                                                                | RFCTR n                                                                                                                                                                | RFCTR n                                                                                                                                                                |                                                                                                                                                                        | POPNXTPTR n                                                                                                                                                            | POPNXTPTR n                                                                                                                                                            | POPNXTPTR n                                                                                                                                                            |
| W        |       |                                                                                                                                                                        |                                                                                                                                                                        |                                                                                                                                                                        |                                                                                                                                                                        |                                                                                                                                                                        |                                                                                                                                                                        |                                                                                                                                                                        |                                                                                                                                                                        |                                                                                                                                                                        |                                                                                                                                                                        |                                                                                                                                                                        |                                                                                                                                                                        |                                                                                                                                                                        |                                                                                                                                                                        |                                                                                                                                                                        |
| Reset    | 0     | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      | 0                                                                                                                                                                      |
| Reg Addr |       | Base + 0x070 (EQADC_FISR0); Base + 0x074 (EQADC_FISR1); Base + 0x078 (EQADC_FISR2); Base + 0x07C (EQADC_FISR3); Base + 0x080 (EQADC_FISR4); Base + 0x084 (EQADC_FISR5) | Base + 0x070 (EQADC_FISR0); Base + 0x074 (EQADC_FISR1); Base + 0x078 (EQADC_FISR2); Base + 0x07C (EQADC_FISR3); Base + 0x080 (EQADC_FISR4); Base + 0x084 (EQADC_FISR5) | Base + 0x070 (EQADC_FISR0); Base + 0x074 (EQADC_FISR1); Base + 0x078 (EQADC_FISR2); Base + 0x07C (EQADC_FISR3); Base + 0x080 (EQADC_FISR4); Base + 0x084 (EQADC_FISR5) | Base + 0x070 (EQADC_FISR0); Base + 0x074 (EQADC_FISR1); Base + 0x078 (EQADC_FISR2); Base + 0x07C (EQADC_FISR3); Base + 0x080 (EQADC_FISR4); Base + 0x084 (EQADC_FISR5) | Base + 0x070 (EQADC_FISR0); Base + 0x074 (EQADC_FISR1); Base + 0x078 (EQADC_FISR2); Base + 0x07C (EQADC_FISR3); Base + 0x080 (EQADC_FISR4); Base + 0x084 (EQADC_FISR5) | Base + 0x070 (EQADC_FISR0); Base + 0x074 (EQADC_FISR1); Base + 0x078 (EQADC_FISR2); Base + 0x07C (EQADC_FISR3); Base + 0x080 (EQADC_FISR4); Base + 0x084 (EQADC_FISR5) | Base + 0x070 (EQADC_FISR0); Base + 0x074 (EQADC_FISR1); Base + 0x078 (EQADC_FISR2); Base + 0x07C (EQADC_FISR3); Base + 0x080 (EQADC_FISR4); Base + 0x084 (EQADC_FISR5) | Base + 0x070 (EQADC_FISR0); Base + 0x074 (EQADC_FISR1); Base + 0x078 (EQADC_FISR2); Base + 0x07C (EQADC_FISR3); Base + 0x080 (EQADC_FISR4); Base + 0x084 (EQADC_FISR5) | Base + 0x070 (EQADC_FISR0); Base + 0x074 (EQADC_FISR1); Base + 0x078 (EQADC_FISR2); Base + 0x07C (EQADC_FISR3); Base + 0x080 (EQADC_FISR4); Base + 0x084 (EQADC_FISR5) | Base + 0x070 (EQADC_FISR0); Base + 0x074 (EQADC_FISR1); Base + 0x078 (EQADC_FISR2); Base + 0x07C (EQADC_FISR3); Base + 0x080 (EQADC_FISR4); Base + 0x084 (EQADC_FISR5) | Base + 0x070 (EQADC_FISR0); Base + 0x074 (EQADC_FISR1); Base + 0x078 (EQADC_FISR2); Base + 0x07C (EQADC_FISR3); Base + 0x080 (EQADC_FISR4); Base + 0x084 (EQADC_FISR5) | Base + 0x070 (EQADC_FISR0); Base + 0x074 (EQADC_FISR1); Base + 0x078 (EQADC_FISR2); Base + 0x07C (EQADC_FISR3); Base + 0x080 (EQADC_FISR4); Base + 0x084 (EQADC_FISR5) | Base + 0x070 (EQADC_FISR0); Base + 0x074 (EQADC_FISR1); Base + 0x078 (EQADC_FISR2); Base + 0x07C (EQADC_FISR3); Base + 0x080 (EQADC_FISR4); Base + 0x084 (EQADC_FISR5) | Base + 0x070 (EQADC_FISR0); Base + 0x074 (EQADC_FISR1); Base + 0x078 (EQADC_FISR2); Base + 0x07C (EQADC_FISR3); Base + 0x080 (EQADC_FISR4); Base + 0x084 (EQADC_FISR5) | Base + 0x070 (EQADC_FISR0); Base + 0x074 (EQADC_FISR1); Base + 0x078 (EQADC_FISR2); Base + 0x07C (EQADC_FISR3); Base + 0x080 (EQADC_FISR4); Base + 0x084 (EQADC_FISR5) |

## Table 19-12. EQADC\_FISR n Field Descriptions

|   Bits | Name   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
|--------|--------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|      0 | NCF n  | Non-coherency flag n . NCF n is set whenever a command sequence being transferred through CFIFO n becomes non-coherent. If NCIE n in EQADC_IDCRn (See Section 19.3.2.7) and NCF n are asserted, an interrupt request will be generated. Writing a 1 clears NCF n . Writing a 0 has no effect. More for information on non-coherency refer to Section 19.4.3.6.5, 'Command Sequence Non-Coherency Detection.' 0 Command sequence being transferred by CFIFO n is coherent 1 Command sequence being transferred by CFIFO n became non-coherent Note: Non-coherency means that a command in the command FIFO was not immediately executed, but delayed. This may occur if the command is pre-empted, where a higher priority queue is triggered and has a competing conversion command for the same converter.                                                                                                                                                                                                                                                                                                                                                                          |
|      1 | TORF n | Trigger overrun flag for CFIFO n . TORF n is set when trigger overrun occurs for the specified CFIFO in edge or level trigger mode. Trigger overrun occurs when an already triggered CFIFO receives an additional trigger. WhenEQADC_IDCRn[TORIE n] is set (See Section 19.3.2.7) and TORF n are asserted, an interrupt request will be generated. Apart from generating an independent interrupt request for a CFIFO n trigger overrun event, the eQADC also provides a combined interrupt at which the result FIFO overflow interrupt, the command FIFO underflow interrupt, and the command FIFO trigger overrun Interrupt requests of all CFIFOs are ORed. When RFOIE n , CFUIE n , and TORIE n are all asserted, this combined interrupt request is asserted whenever one of the following 18 flags becomes asserted: RFOF n , CFUF n , and TORF n (assuming that all interrupts are enabled). See Section 19.4.7, 'eQADC eDMA/Interrupt Request,' for details. Write 1 to clear the TORF n bit. Writing 0 has no effect. 0 No trigger overrun occurred 1 Trigger overrun occurred Note: The trigger overrun flag will not set for CFIFOs configured for software trigger mode. |

## Table 19-12. EQADC\_FISR n Field Descriptions (continued)

|   Bits | Name   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|--------|--------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|      2 | PF n   | Pause flag n . PF behavior changes according to the CFIFO trigger mode. GLYPH<127> In edge trigger mode, PF n is set when the eQADC completes the transfer of an entry with an asserted pause bit from CFIFO n . GLYPH<127> In level trigger mode, when CFIFO n is in the TRIGGEREDstate, PF n is set when CFIFO status changes from TRIGGERED due to the detection of a closed gate. An interrupt routine, generated due to the asserted PF, can be used to verify if a complete scan of the user-defined commandqueuewasperformed. If a closed gate is detected while no command transfers are taking place, it will have immediate effect on the CFIFO status. If a closed gate is detected while a command transfer to an on-chip ADC is taking place, it will only affect the CFIFO status when the transfer completes. If a closed gate is detected during the serial transmission of a command to the external device, it will have no effect on the CFIFO status until the transmission completes. The transfer of entries bound for the on-chip ADCs is considered completed when they are stored in the appropriate ADC command buffer. The transfer of entries bound for the external device is considered completed when the serial transmission of the entry is completed. In software trigger mode, PF n will never become asserted. If PIE n (See Section 19.3.2.7) and PF n are asserted, an interrupt will be generated. Writing a 1 clears the PF n . Writing a 0 has no effect. Refer to Section 19.4.3.6.3, 'Pause Status,' for more information on pause flag. 0 Entry with asserted pause bit was not transferred from CFIFO n (CFIFO in edge trigger mode), or CFIFO status did not change from the TRIGGERED state due to detection of a closed gate (CFIFO in level trigger mode). 1 Entry with asserted pause bit was transferred from CFIFO n (CFIFO in edge trigger mode), or CFIFO status changes from the TRIGGERED state due to detection of a closed gate (CFIFO in level trigger mode). Note: In edge trigger mode, an asserted PF n only implies that the eQADC has finished transferring a command with an asserted pause bit from CFIFO n . It does not imply that result data for the current command and for all previously transferred commands has been returned to the appropriate RFIFO. Note: In software or level trigger mode, when the eQADC completes the transfer of an entry from CFIFO n with an asserted pause bit, PF n will not be set and transfer of |
|      3 | EOQF n | End-of-queue flag n . Indicates that an entry with an asserted EOQbit was transferred from CFIFO n to the on-chip ADCs or to the external device. See Section 19.4.1.2, 'Message Format in eQADC,' for details about command message formats. When the eQADC completes the transfer of an entry with an asserted EOQ bit from CFIFO n , EOQF n will be set. The transfer of entries bound for the on-chip ADCsis considered completed when they are stored in the appropriate commandbuffer. The transfer of entries bound for the external device is considered completed when the serial transmission of the entry is completed. If the EOQIE n bit (See 19.3.2.7) and EOQF n are asserted, an interrupt will be generated. Writing a 1 clears the EOQF n bit. Writing a 0 has no effect. Refer to Section 19.4.3.6.2, 'Command Queue Completion Status,' for more information on end-of-queue flag. 0 Entry with asserted EOQ bit was not transferred from CFIFO n 1 Entry with asserted EOQ bit was transferred from CFIFO n Note: An asserted EOQF n only implies that the eQADC has finished transferring a command with an asserted EOQbit from CFIFO n . It does not imply that result data for the current command and for all previously transferred commands has been returned to the appropriate RFIFO.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |

## Table 19-12. EQADC\_FISR n Field Descriptions (continued)

| Bits   | Name   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|--------|--------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 4      | CFUF n | CFIFO underflow flag n . Indicates an underflow event on CFIFO n . CFUF n is set when CFIFO n is in the TRIGGERED state and it becomes empty. No commands will be transferred from an underflowing CFIFO, nor will command transfers from lower priority CFIFOs be blocked. When CFUIE n (see Section 19.3.2.7) and CFUF n are both asserted, the eQADC generates an interrupt request. Apart from generating an independent interrupt request for a CFIFO n underflow event, the eQADC also provides a combined interrupt at which the result FIFO overflow interrupt, the command FIFO underflow interrupt, and the command FIFO trigger overrun interrupt requests of all CFIFOs are ORed. When RFOIE n , CFUIE n , and TORIE n are all asserted, this combined interrupt request is asserted whenever one of the following 18 flags becomes asserted: RFOF n , CFUF n , and TORF n (assuming that all interrupts are enabled). See Section 19.4.7, 'eQADC eDMA/Interrupt Request,' for details. Writing a 1 clears CFUF n . Writing a 0 has no effect. 0 No CFIFO underflow event occurred 1 A CFIFO underflow event occurred                           |
| 5      | SSS n  | CFIFO single-scan status bit n . When asserted, enables the detection of trigger events for CFIFOs programmed into single-scan level- or edge-trigger mode, and works as trigger for CFIFOs programmed into single-scan software-trigger mode. Refer to Section 19.4.3.5.2, 'Single-Scan Mode,' for further details. The SSS n bit is set by writing a 1 to the SSE n bit (see Section 19.3.2.6). The eQADCclears the SSS n bit when a commandwith an asserted EOQ bit is transferred from a CFIFO in single-scan mode, when a CFIFO is in single-scan level-trigger mode and its status changes from the TRIGGERED state due to the detection of a closed gate, or when the value of the CFIFO operation mode MODE n (see Section 19.3.2.6) is changed to disabled. Writing to SSS n has no effect. SSS n has no effect in continuous-scan or in disabled mode. 0 CFIFO in single-scan level- or edge-trigger mode will ignore trigger events, or CFIFO in single-scan software-trigger mode is not triggered. 1 CFIFO in single-scan level- or edge-trigger mode will detect a trigger event, or CFIFO in single-scan software-trigger mode is triggered. |
| 6      | CFFF n | CFIFO fill flag n . CFFF n is set when the CFIFO n is not full. When CFFE n (see Section 19.3.2.7) and CFFF n are both asserted, an interrupt or an eDMArequest will be generated depending on the status of the CFFS n bit. When CFFS n is negated (interrupt requests selected), software clears CFFF n by writing a 1 to it. Writing a 0 has no effect. When CFFS n is asserted (eDMA requests selected), CFFF n is automatically cleared by the eQADC when the CFIFO becomes full. 0 CFIFO n is full. 1 CFIFO n is not full. Note: When generation of interrupt requests is selected (CFFS n =0), CFFF n must only be cleared in the ISR after the CFIFO n push register is accessed. Note: CFFF n should not be cleared when CFFSn is asserted (eDMA requests selected).                                                                                                                                                                                                                                                                                                                                                                               |
| 7-11   | -      | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |

## Table 19-12. EQADC\_FISR n Field Descriptions (continued)

| Bits   | Name            | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|--------|-----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 12     | RFOF n          | RFIFO overflow flag n . Indicates an overflow event on RFIFO n . RFOF n is set when RFIFO n is already full, and a new data is received from the on-chip ADCs or from the external device. The RFIFO n will not overwrite older data in the RFIFO, and the new data will be ignored. When RFOIE n (see Section 19.3.2.7) and RFOF n are both asserted, the eQADC generates an interrupt request. Apart from generating an independent interrupt request for an RFIFO n overflow event, the eQADC also provides a combined interrupt at which the result FIFO overflow interrupt, the command FIFO underflow interrupt, and the command FIFO trigger overrun interrupt requests of all CFIFOs are ORed. When RFOIE n , CFUIE n , and TORIE n are all asserted, this combined interrupt request is asserted whenever one of the following 18 flags becomes asserted: RFOF n , CFUF n , and TORF n (assuming that all interrupts are enabled). See Section 19.4.7, 'eQADC eDMA/Interrupt Request,' for details. Write 1 to clear RFOF n . Writing a 0 has no effect. 0 No RFIFO overflow event occurred. 1 An RFIFO overflow event occurred. |
| 13     | -               | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| 14     | RFDF n          | RFIFO drain flag n . Indicates if RFIFO n has valid entries that can be drained or not. RFDF n is set when the RFIFO n has at least one valid entry in it. When RFDE n (see Section 19.3.2.7) and RFDF n are both asserted, an interrupt or an eDMArequest will be generated depending on the status of the RFDS n bit. When RFDS n is negated (interrupt requests selected), software clears RFDF n by writing a 1 to it. Writing a 0 has no effect. When RFDS n is asserted (eDMA requests selected), RFDF n is automatically cleared by the eQADC when the RFIFO becomes empty. 0 RFIFO n is empty. 1 RFIFO n has at least one valid entry. Note: In the interrupt service routine, RFDF must be cleared only after the RFIFO n pop register is read. Note: RFDF n should not be cleared when RFDS n is asserted (eDMA requests selected).                                                                                                                                                                                                                                                                                             |
| 15     | -               | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| 16-19  | CFCTR n [0:3]   | CFIFO n entry counter. Indicates the number of commands stored in the CFIFO n . When the eQADC completes transferring a piece of new data from the CFIFO n , it decrements CFCTR n by 1. Writing a word or any bytes to the corresponding CFIFO Push Register (see Section 19.3.2.4) increments CFCTR n by 1. Writing any value to CFCTR n has no effect.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| 20-23  | TNXTPTR n [0:3] | CFIFO n transfer next pointer. Indicates the index of the next entry to be removed from CFIFO n when it completes a transfer. When TNXTPTR n is 0, it points to the entry with the smallest memory-mapped address inside CFIFO n . TNXTPTR n is only updated when a command transfer is completed. If the maximum index number (CFIFO depth minus 1) is reached, TNXTPTR n is wrapped to 0, else, it is incremented by 1. For details refer to Section 19.4.3.1, 'CFIFO Basic Functionality.' Writing any value to TNXTPTR n has no effect.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |

Table 19-12. EQADC\_FISR n Field Descriptions (continued)

| Bits   | Name              | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|--------|-------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 24-27  | RFCTR n [0:3]     | RFIFO n entry counter. Indicates the number of data items stored in the RFIFO n . When the eQADC stores a piece of new data into RFIFO n, it increments RFCTR n by 1. Reading the whole word, half-word or any bytes of the corresponding Result FIFO pop register (see Section 19.3.2.5) decrements RFCTR n by 1. Writing any value to RFCTR n itself has no effect.                                                                                                                                             |
| 28-31  | POPNXTPTR n [0:3] | RFIFO n pop next pointer. Indicates the index of the entry that will be returned when EQADC_RFPR n is read. When POPNXTPTR n is 0, it points to the entry with the smallest memory-mapped address inside RFIFO n . POPNXTPTR n is updated when EQADC_RFPR n is read. If the maximum index number (RFIFO depth minus 1) is reached, POPNXTPTR n is wrapped to 0, else, it is incremented by 1. For details refer to Section 19.4.4.1, 'RFIFO Basic Functionality.' Writing any value to POPNXTPTR n has no effect. |

## 19.3.2.9 eQADC CFIFO Transfer Counter Registers 0-5 (EQADC\_CFTCR n )

The EQADC\_CFTCRs record the number of commands transferred from a CFIFO. The EQADC\_CFTCR supports the monitoring of command transfers from a CFIFO.

Figure 19-10. eQADC CFIFO Transfer Counter Registers (EQADC\_CFTCR n )

<!-- image -->

Table 19-13. EQADC\_CFTCR n Field Descriptions

| Bits   | Name           | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
|--------|----------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-4    | -              | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| 5-15   | TC_CF n [0:10] | Transfer counter for CFIFO n . TC_CF n counts the number of commands that have been completely transferred from CFIFO n . TC_CF n =2, for example, signifies that two commands have been transferred. The transfer of entries bound for the on-chip ADCs is considered completed when they are stored in the appropriate command buffer. The transfer of entries bound for an external device is considered completed when the serial transmission of the entry is completed. The eQADC increments the TC_CF n value by 1 after a command is transferred. TC_CF n resets to 0 after eQADC completes transferring a command with an asserted EOQ bit. Writing any value to TC_CF n sets the counter to that written value. Note: If CFIFO n is in the TRIGGERED state when its MODE n field is programmed to disabled, the exact number of entries transferred from the CFIFO until that point (TC_CF n ) is only known after the CFIFO status changes to IDLE, as indicated by CFS n . For details refer to Section 19.4.3.5.1, 'Disabled Mode.' |

## 19.3.2.10 eQADC CFIFO Status Snapshot Registers 0-2 (EQADC\_CFSSR n )

The eQADC\_CFSSRs contain status fields to track the operation status of each CFIFO and the transfer counter of the last CFIFO to initiate a command transfer to the internal ADCs and the external command buffers. EQADC\_CFSSR0-1 are related to the on-chip ADC command buffers (buffers 0 and 1) while EQADC\_CFSSR2 is related to the external command buffers (buffers 2 and 3). All fields of a particular EQADC\_CFSSR are captured at the beginning of a command transfer to the buffer associated with that register.

Note that captured status register values are associated with a previous command transfer. This means that the eQADC\_CFSSR registers capture the status registers before the status registers change, because of the transfer of the current command that is about to be popped from the CFIFO. The EQADC\_CFSSRs are read only. Writing to the EQADC\_CFSSRs has no effect.

Figure 19-11. eQADC CFIFO Status Snapshot Register 0 (EQADC\_CFSSR0)

<!-- image -->

Table 19-14. EQADC\_CFSSR0 Field Descriptions

| Bits   | Name            | Description                                                                                                                                                                                                                                                                                                 |
|--------|-----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-11   | CFS n _T0 [0:1] | CFIFO status at transfer to ADC n command buffer . Indicates the CFIFO n status at the time a command transfer to ADC n command buffer is initiated. CFS n _T0 is a copy of the corresponding CFS n in EQADC_CFSR (see Section 19.3.2.11) captured at the time a command transfer to buffer n is initiated. |
| 12-16  | -               | Reserved.                                                                                                                                                                                                                                                                                                   |

## Table 19-14. EQADC\_CFSSR0 Field Descriptions (continued)

Figure 19-12. eQADC CFIFO Status Snapshot Register 1 (EQADC\_CFSSR1)

| Bits   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                              | Description                                                                                                                                                                                                                                                                                                                                                                                                                                              |
|--------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 17-20  | LCFT0 [0:3] Last CFIFO to transfer to ADC n command buffer . Holds the CFIFO number of last CFIFO to have initiated a command transfer to ADC n command buffer. LCFT0 has the following values: Name                                                                                                                                                                                                                                                     | LCFT0 [0:3] Last CFIFO to transfer to ADC n command buffer . Holds the CFIFO number of last CFIFO to have initiated a command transfer to ADC n command buffer. LCFT0 has the following values: Name                                                                                                                                                                                                                                                     |
| 17-20  |                                                                                                                                                                                                                                                                                                                                                                                                                                                          | LCFT 0 [0:3]                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 17-20  |                                                                                                                                                                                                                                                                                                                                                                                                                                                          | 0b0000                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| 17-20  |                                                                                                                                                                                                                                                                                                                                                                                                                                                          | 0b0001                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| 17-20  |                                                                                                                                                                                                                                                                                                                                                                                                                                                          | 0b0010                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| 17-20  |                                                                                                                                                                                                                                                                                                                                                                                                                                                          | 0b0011                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| 17-20  |                                                                                                                                                                                                                                                                                                                                                                                                                                                          | 0b0100                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| 17-20  |                                                                                                                                                                                                                                                                                                                                                                                                                                                          | 0b0101                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| 17-20  |                                                                                                                                                                                                                                                                                                                                                                                                                                                          | 0b0110-0b1110                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| 17-20  |                                                                                                                                                                                                                                                                                                                                                                                                                                                          | 0b1111                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| 21-31  | TC_LCFT0 Transfer counter for last CFIFO to transfer commands to ADC n command buffer. Indicates the number of commands which have been completely transferred from CFIFO n when a command transfer from CFIFO n to ADC n command buffer is initiated. TC_LCFT0 is a copy of the corresponding TC_CF n in EQADC_CFTCR n (see Section 19.3.2.9) captured at the time a command transfer from CFIFO n to ADC n command buffer is initiated. This field has | TC_LCFT0 Transfer counter for last CFIFO to transfer commands to ADC n command buffer. Indicates the number of commands which have been completely transferred from CFIFO n when a command transfer from CFIFO n to ADC n command buffer is initiated. TC_LCFT0 is a copy of the corresponding TC_CF n in EQADC_CFTCR n (see Section 19.3.2.9) captured at the time a command transfer from CFIFO n to ADC n command buffer is initiated. This field has |

<!-- image -->

| R        | 0 1                         | 0 1                         | 2 3                         | 2 3                         | 4 5                         | 4 5                         | 6 7                         | 6 7                         | 8 9                         | 8 9                         | 10                          | 11                          | 11                          | 12                          | 13 14                       | 15                          |                             |
|----------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|
| W        | CFS0_T1                     | CFS0_T1                     | CFS1_T1                     | CFS1_T1                     | CFS2_T1                     | CFS2_T1                     | CFS3_T1                     | CFS3_T1                     | CFS4_T1                     | CFS4_T1                     | CFS5_T1                     | 0                           | 0                           | 0                           | 0                           | 0                           |                             |
| Reset    | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           |                             |
| Reg Addr | Base + 0x0A4 (EQADC_CFSSR1) | Base + 0x0A4 (EQADC_CFSSR1) | Base + 0x0A4 (EQADC_CFSSR1) | Base + 0x0A4 (EQADC_CFSSR1) | Base + 0x0A4 (EQADC_CFSSR1) | Base + 0x0A4 (EQADC_CFSSR1) | Base + 0x0A4 (EQADC_CFSSR1) | Base + 0x0A4 (EQADC_CFSSR1) | Base + 0x0A4 (EQADC_CFSSR1) | Base + 0x0A4 (EQADC_CFSSR1) | Base + 0x0A4 (EQADC_CFSSR1) | Base + 0x0A4 (EQADC_CFSSR1) | Base + 0x0A4 (EQADC_CFSSR1) | Base + 0x0A4 (EQADC_CFSSR1) | Base + 0x0A4 (EQADC_CFSSR1) | Base + 0x0A4 (EQADC_CFSSR1) | Base + 0x0A4 (EQADC_CFSSR1) |
|          | 16                          | 17                          | 18                          | 19                          | 20                          | 21                          | 22                          | 23                          | 24                          | 25                          | 26                          | 27                          | 28                          | 29                          | 30                          | 31                          |                             |
| R        | 0 LCFT1                     | 0 LCFT1                     | 0 LCFT1                     | 0 LCFT1                     | 0 LCFT1                     | TC_LCFT1                    | TC_LCFT1                    | TC_LCFT1                    | TC_LCFT1                    | TC_LCFT1                    | TC_LCFT1                    | TC_LCFT1                    | TC_LCFT1                    | TC_LCFT1                    | TC_LCFT1                    | TC_LCFT1                    | TC_LCFT1                    |
| W        |                             |                             |                             |                             |                             |                             |                             |                             |                             |                             |                             |                             |                             |                             |                             |                             |                             |
| Reset    | 0                           | 1                           | 1                           | 1                           | 1                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           |                             |
| Reg      | Base + 0x0A4 (EQADC_CFSSR1) | Base + 0x0A4 (EQADC_CFSSR1) | Base + 0x0A4 (EQADC_CFSSR1) | Base + 0x0A4 (EQADC_CFSSR1) | Base + 0x0A4 (EQADC_CFSSR1) | Base + 0x0A4 (EQADC_CFSSR1) | Base + 0x0A4 (EQADC_CFSSR1) | Base + 0x0A4 (EQADC_CFSSR1) | Base + 0x0A4 (EQADC_CFSSR1) | Base + 0x0A4 (EQADC_CFSSR1) | Base + 0x0A4 (EQADC_CFSSR1) | Base + 0x0A4 (EQADC_CFSSR1) | Base + 0x0A4 (EQADC_CFSSR1) | Base + 0x0A4 (EQADC_CFSSR1) | Base + 0x0A4 (EQADC_CFSSR1) | Base + 0x0A4 (EQADC_CFSSR1) | Base + 0x0A4 (EQADC_CFSSR1) |

## Table 19-15. EQADC\_CFSSR1 Field Descriptions

| Bits   | Name            | Description                                                                                                                                                                                                                                                                                                                                                                                                                                    |
|--------|-----------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-11   | CFS n _T1 [0:1] | CFIFO status at transfer to ADC n command buffer . Indicates the CFIFO n status at the time a command transfer to ADC n command buffer is initiated. CFS n _T1 is a copy of the corresponding CFS n in EQADC_CFSR (see Section 19.3.2.11) captured at the time a command transfer to buffer n is initiated.                                                                                                                                    |
| 12-16  | -               | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| 17-20  | LCFT1 [0:3]     | Last CFIFO to transfer to ADC n command buffer . Holds the CFIFO number of last CFIFO to have initiated a command transfer to ADC n command buffer. LCFT1 has the following values:                                                                                                                                                                                                                                                            |
| 17-20  | LCFT1 [0:3]     |                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| 17-20  | LCFT1 [0:3]     |                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| 17-20  | LCFT1 [0:3]     |                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| 17-20  | LCFT1 [0:3]     |                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| 17-20  | LCFT1 [0:3]     |                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| 17-20  | LCFT1 [0:3]     |                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| 17-20  | LCFT1 [0:3]     |                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| 17-20  | LCFT1 [0:3]     |                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| 17-20  | LCFT1 [0:3]     |                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| 21-31  | TC_LCFT1 [0:10] | Transfer counter for last CFIFO to transfer commands to ADC n command buffer. Indicates the number of commands which have been completely transferred from CFIFO n when a command transfer from CFIFO n to ADC n command buffer is initiated. TC_LCFT1 is a copy of the corresponding TC_CF n in EQADC_CFTCRn (see Section 19.3.2.9) captured at the time a command transfer from CFIFO n to ADC n command buffer is initiated. This field has |

The third eQADC CFIFO status snapshot register is displayed in Figure 19-13.

Figure 19-13. eQADC CFIFO Status Snapshot Register 2 (EQADC\_CFSSR2)

<!-- image -->

|          | 0                           | 1                           | 2                           | 2                           | 3 4                         | 5                           | 6                           | 7                           | 8                           | 9                           | 10                          | 11                          | 12                          | 13                          | 14                          | 15                          |
|----------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|
| R        | CFS0_TSSI                   | CFS0_TSSI                   | CFS1_TSSI                   | CFS1_TSSI                   | CFS2_TSSI                   | CFS2_TSSI                   | CFS3_TSSI                   | CFS3_TSSI                   | CFS4_TSSI                   | CFS4_TSSI                   | CFS5_TSSI                   | CFS5_TSSI                   | 0                           | 0                           | 0                           | 0                           |
| W        |                             |                             |                             |                             |                             |                             |                             |                             |                             |                             |                             |                             |                             |                             |                             |                             |
| Reset    | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           |
| Reg Addr | Base + 0x0A8 (EQADC_CFSSR2) | Base + 0x0A8 (EQADC_CFSSR2) | Base + 0x0A8 (EQADC_CFSSR2) | Base + 0x0A8 (EQADC_CFSSR2) | Base + 0x0A8 (EQADC_CFSSR2) | Base + 0x0A8 (EQADC_CFSSR2) | Base + 0x0A8 (EQADC_CFSSR2) | Base + 0x0A8 (EQADC_CFSSR2) | Base + 0x0A8 (EQADC_CFSSR2) | Base + 0x0A8 (EQADC_CFSSR2) | Base + 0x0A8 (EQADC_CFSSR2) | Base + 0x0A8 (EQADC_CFSSR2) | Base + 0x0A8 (EQADC_CFSSR2) | Base + 0x0A8 (EQADC_CFSSR2) | Base + 0x0A8 (EQADC_CFSSR2) | Base + 0x0A8 (EQADC_CFSSR2) |
|          | 16                          | 17                          | 18                          | 19                          | 20                          | 21                          | 22                          | 23                          | 24                          | 25                          | 26                          | 27                          | 28                          | 29                          | 30                          | 31                          |
| R        | ENI LCFTSSI                 | ENI LCFTSSI                 | ENI LCFTSSI                 | ENI LCFTSSI                 | TC_LCFTSSI                  | TC_LCFTSSI                  | TC_LCFTSSI                  | TC_LCFTSSI                  | TC_LCFTSSI                  | TC_LCFTSSI                  | TC_LCFTSSI                  | TC_LCFTSSI                  | TC_LCFTSSI                  | TC_LCFTSSI                  | TC_LCFTSSI                  | TC_LCFTSSI                  |
| W        |                             |                             |                             |                             |                             |                             |                             |                             |                             |                             |                             |                             |                             |                             |                             |                             |
| Reset    | 0                           | 1                           | 1                           | 1                           | 1                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           | 0                           |
| Reg      | Base + 0x0A8 (EQADC_CFSSR2) | Base + 0x0A8 (EQADC_CFSSR2) | Base + 0x0A8 (EQADC_CFSSR2) | Base + 0x0A8 (EQADC_CFSSR2) | Base + 0x0A8 (EQADC_CFSSR2) | Base + 0x0A8 (EQADC_CFSSR2) | Base + 0x0A8 (EQADC_CFSSR2) | Base + 0x0A8 (EQADC_CFSSR2) | Base + 0x0A8 (EQADC_CFSSR2) | Base + 0x0A8 (EQADC_CFSSR2) | Base + 0x0A8 (EQADC_CFSSR2) | Base + 0x0A8 (EQADC_CFSSR2) | Base + 0x0A8 (EQADC_CFSSR2) | Base + 0x0A8 (EQADC_CFSSR2) | Base + 0x0A8 (EQADC_CFSSR2) | Base + 0x0A8 (EQADC_CFSSR2) |

## Table 19-16. EQADC\_CFSSR2 Field Descriptions

| Bits   | Name              | Description                                                                                                                                                                                                                                                                                                             |
|--------|-------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-11   | CFS n _TSSI [0:1] | CFIFO Status at Transfer through the eQADCSSI. Indicates the CFIFO n status at the time a serial transmission through the eQADC SSI is initiated. CFS n _TSSI is a copy of the corresponding CFS n in EQADC_CFSR (see Section 19.3.2.11) captured at the time a serial transmission through the eQADC SSI is initiated. |
| 12-15  | -                 | Reserved.                                                                                                                                                                                                                                                                                                               |
| 16     | ENI               | External command buffer number Indicator. Indicates to which external command buffer the last command was transmitted. 0 Last command was transferred to command buffer 2. 1 Last command was transferred to command buffer 3.                                                                                          |

## Table 19-16. EQADC\_CFSSR2 Field Descriptions (continued)

| Bits   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                    | Description                                                                                                                                                                                                                                                                                                                                                                                                                                    |
|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 17-20  | LCFTSSI [0:3] Last CFIFO to transfer commands through the eQADC SSI. Holds the CFIFO number of last CFIFO to have initiated a command transfer to an external command buffer through the eQADC SSI. LCFTSSI does not indicate the transmission of null messages. LCFTSSI has the following values: Name                                                                                                                                        | LCFTSSI [0:3] Last CFIFO to transfer commands through the eQADC SSI. Holds the CFIFO number of last CFIFO to have initiated a command transfer to an external command buffer through the eQADC SSI. LCFTSSI does not indicate the transmission of null messages. LCFTSSI has the following values: Name                                                                                                                                        |
|        |                                                                                                                                                                                                                                                                                                                                                                                                                                                | LCFTSSI[0:3]                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|        |                                                                                                                                                                                                                                                                                                                                                                                                                                                | 0b0000                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|        |                                                                                                                                                                                                                                                                                                                                                                                                                                                | 0b0001                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|        |                                                                                                                                                                                                                                                                                                                                                                                                                                                | 0b0010                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|        |                                                                                                                                                                                                                                                                                                                                                                                                                                                | 0b0011                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|        |                                                                                                                                                                                                                                                                                                                                                                                                                                                | 0b0100                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|        |                                                                                                                                                                                                                                                                                                                                                                                                                                                | 0b0101                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|        |                                                                                                                                                                                                                                                                                                                                                                                                                                                | 0b0110 - 0b1110                                                                                                                                                                                                                                                                                                                                                                                                                                |
|        |                                                                                                                                                                                                                                                                                                                                                                                                                                                | 0b1111                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| 21-31  | TC_LCFTSS Transfer counter for last CFIFO to transfer commands through eQADC SSI. Indicates the number of commands which have been completely transferred from a particular CFIFO at the time a command transfer from that CFIFO to an external command buffer is initiated. TC_LCFTSSI is a copy of the corresponding TC_CF n in EQADC_CFTCRn (see Section 19.3.2.9) captured at the time a command transfer to an external command buffer is | TC_LCFTSS Transfer counter for last CFIFO to transfer commands through eQADC SSI. Indicates the number of commands which have been completely transferred from a particular CFIFO at the time a command transfer from that CFIFO to an external command buffer is initiated. TC_LCFTSSI is a copy of the corresponding TC_CF n in EQADC_CFTCRn (see Section 19.3.2.9) captured at the time a command transfer to an external command buffer is |

## 19.3.2.11 eQADC CFIFO Status Register (EQADC\_CFSR)

The EQADC\_CFSR contains the current CFIFO status. The EQADC\_CFSRs are read only. Writing to the EQADC\_CFSR has no effect.

Figure 19-14. eQADC CFIFO Status Register (EQADC\_CFSR)

|          | 0            | 1            | 2            | 3            | 4            | 5            | 6            | 7            | 8            | 9            | 10           | 11           | 12           | 13           | 14           | 15           |
|----------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|
| R        | CFS0         | CFS0         | CFS1         | CFS1         | CFS2         | CFS2         | CFS3         | CFS3         | CFS4         | CFS4         | CFS5         | CFS5         | 0            | 0            | 0            | 0            |
| W        |              |              |              |              |              |              |              |              |              |              |              |              |              |              |              |              |
| Reset    | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            |
| Reg Addr | Base + 0x0AC | Base + 0x0AC | Base + 0x0AC | Base + 0x0AC | Base + 0x0AC | Base + 0x0AC | Base + 0x0AC | Base + 0x0AC | Base + 0x0AC | Base + 0x0AC | Base + 0x0AC | Base + 0x0AC | Base + 0x0AC | Base + 0x0AC | Base + 0x0AC | Base + 0x0AC |
|          | 16           | 17           | 18           | 19           | 20           | 21           | 22           | 23           | 24           | 25           | 26           | 27           | 28           | 29           | 30           | 31           |
| R        | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            |
| W        |              |              |              |              |              |              |              |              |              |              |              |              |              |              |              |              |
| Reset    | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            |
| Reg Addr | Base + 0x0AC | Base + 0x0AC | Base + 0x0AC | Base + 0x0AC | Base + 0x0AC | Base + 0x0AC | Base + 0x0AC | Base + 0x0AC | Base + 0x0AC | Base + 0x0AC | Base + 0x0AC | Base + 0x0AC | Base + 0x0AC | Base + 0x0AC | Base + 0x0AC | Base + 0x0AC |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## Table 19-17. EQADC\_CFSR Field Descriptions

| Bits   | Name        | Description                                                                                                        |
|--------|-------------|--------------------------------------------------------------------------------------------------------------------|
| 0-11   | CFS n [0:1] | CFIFO status. Indicates the current status of CFIFO n . Refer to Table 19-18 for more information on CFIFO status. |
| 12-31  | -           | Reserved.                                                                                                          |

Table 19-18. Current CFIFO Status

| CFIFO Status        | Field Value   | Explanation                                                                                                                                                                                                                                                                                                                                                                                                                   |
|---------------------|---------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| IDLE                | 0b00          | GLYPH<127> CFIFO is disabled. GLYPH<127> CFIFO is in single-scan edge or level trigger mode and does not have EQADC_FISRn[SSS] asserted. GLYPH<127> eQADC completed the transfer of the last entry of the user defined command queue in single-scan mode.                                                                                                                                                                     |
| Reserved            | 0b01          | Not applicable.                                                                                                                                                                                                                                                                                                                                                                                                               |
| WAITING FOR TRIGGER | 0b10          | GLYPH<127> CFIFO mode is modified to continuous-scan edge or level trigger mode. GLYPH<127> CFIFO mode is modified to single-scan edge or level trigger mode and EQADC_FISRn[SSS] is asserted. GLYPH<127> CFIFOmodeis modified to single-scan software trigger modeandEQADC_FISRn[SSS] is negated. GLYPH<127> CFIFO is paused. GLYPH<127> eQADC transferred the last entry of the queue in continuous-scan edge trigger mode. |
| TRIGGERED           | 0b11          | CFIFO is triggered                                                                                                                                                                                                                                                                                                                                                                                                            |

## 19.3.2.12 eQADC SSI Control Register (EQADC\_SSICR)

The EQADC\_SSICR configures the SSI submodule.

Figure 19-15. eQADC SSI Control Register (EQADC\_SSICR)

<!-- image -->

|          | 0            | 1            | 2            | 3            | 4            | 5            | 6            | 7            | 8            | 9            | 10           | 11           | 12           | 13           | 14           | 15           |
|----------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|
| R        | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            |
| W        |              |              |              |              |              |              |              |              |              |              |              |              |              |              |              |              |
| Reset    | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            |
| Reg Addr | Base + 0x0B4 | Base + 0x0B4 | Base + 0x0B4 | Base + 0x0B4 | Base + 0x0B4 | Base + 0x0B4 | Base + 0x0B4 | Base + 0x0B4 | Base + 0x0B4 | Base + 0x0B4 | Base + 0x0B4 | Base + 0x0B4 | Base + 0x0B4 | Base + 0x0B4 | Base + 0x0B4 | Base + 0x0B4 |
|          | 16           | 17           | 18           | 19           | 20           | 21           | 22           | 23           | 24           | 25           | 26           | 27           | 28           | 29           | 30           | 31           |
| R        | 0            | 0            | 0            | 0            | 0            |              | MDT          |              | 0            | 0            | 0            | 0            |              | BR           |              |              |
| W        |              |              |              |              |              |              |              |              |              |              |              |              |              |              |              |              |
| Reset    | 0            | 0            | 0            | 0            | 0            | 1            | 1            | 1            | 0            | 0            | 0            | 0            | 1            | 1            | 1            | 1            |
| Reg Addr | Base + 0x0B4 | Base + 0x0B4 | Base + 0x0B4 | Base + 0x0B4 | Base + 0x0B4 | Base + 0x0B4 | Base + 0x0B4 | Base + 0x0B4 | Base + 0x0B4 | Base + 0x0B4 | Base + 0x0B4 | Base + 0x0B4 | Base + 0x0B4 | Base + 0x0B4 | Base + 0x0B4 | Base + 0x0B4 |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## Table 19-19. EQADC\_SSICR Field Descriptions

| Bits   | Name      | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|--------|-----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-20   | -         | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| 21-23  | MDT [0:2] | Minimum delay after transmission. Defines the minimum delay after transmission time (t MDT ) expressed in serial clock (FCK) periods. t MDT is the minimum time SDS should be kept negated between two consecutive serial transmissions. Table 19-20 lists the minimum delay after transfer time according to how MDT is set. The MDTfield must only be written when the serial transmissions from the eQADCSSIare disabled - See EQADC_MCR[ESSIE] field in Section 19.3.2.1. |
| 24-27  | -         | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| 28-31  | BR [0:3]  | Baud rate. Selects system clock divide factor as shown in Table 19-21. The baud clock is calculated by dividing the system clock by the clock divide factor specified with the BRfield. Note: The BR field must only be written when the eQADC SSI is disabled - See EQADC_MCR[ESSIE] field in Section 19.3.2.1.                                                                                                                                                              |

## Table 19-20. Minimum Delay After Transmission (t MDT ) Time

| MDT   |   t MDT (FCK period) |
|-------|----------------------|
| 0b000 |                    1 |
| 0b001 |                    2 |
| 0b010 |                    3 |
| 0b011 |                    4 |
| 0b100 |                    5 |
| 0b101 |                    6 |
| 0b110 |                    7 |
| 0b111 |                    8 |

## Table 19-21. System Clock Divide Factor for Baud Clock

| BR[0:3]   |   System Clock Divide Factor 1 |
|-----------|--------------------------------|
| 0b0000    |                              2 |
| 0b0001    |                              3 |
| 0b0010    |                              4 |
| 0b0011    |                              5 |
| 0b0100    |                              6 |
| 0b0101    |                              7 |
| 0b0110    |                              8 |
| 0b0111    |                              9 |
| 0b1000    |                             10 |

Table 19-21. System Clock Divide Factor for Baud Clock (continued)

| BR[0:3]   |   System Clock Divide Factor 1 |
|-----------|--------------------------------|
| 0b1001    |                             11 |
| 0b1010    |                             12 |
| 0b1011    |                             13 |
| 0b1100    |                             14 |
| 0b1101    |                             15 |
| 0b1110    |                             16 |
| 0b1111    |                             17 |

- 1 If the system clock is divided by a odd number then the serial clock will have a duty cycle different from 50%.

## 19.3.2.13 eQADC SSI Receive Data Register (EQADC\_SSIRDR)

The eQADC SSI receive data register (EQADC\_SSIRDR) records the last message received from the external device.

Figure 19-16. eQADC SSI Receive Data Register (EQADC\_SSIRDR)

|          | 0            | 1            | 2            | 3            | 4            | 5            | 6            | 7            | 8            | 9            | 10           | 11           | 12           | 13           | 14           | 15           |
|----------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|
| R        | RDV          | 0            | 0            | 0            | 0            | 0            | R_DATA       | R_DATA       | R_DATA       | R_DATA       | R_DATA       | R_DATA       | R_DATA       | R_DATA       | R_DATA       | R_DATA       |
| W        |              |              |              |              |              |              |              |              |              |              |              |              |              |              |              |              |
| Reset    | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 1            | 1            | 1            | 1            |
| Reg Addr | Base + 0x0B8 | Base + 0x0B8 | Base + 0x0B8 | Base + 0x0B8 | Base + 0x0B8 | Base + 0x0B8 | Base + 0x0B8 | Base + 0x0B8 | Base + 0x0B8 | Base + 0x0B8 | Base + 0x0B8 | Base + 0x0B8 | Base + 0x0B8 | Base + 0x0B8 | Base + 0x0B8 | Base + 0x0B8 |
|          | 16           | 17           | 18           | 19           | 20           | 21           | 22           | 23           | 24           | 25           | 26           | 27           | 28           | 29           | 30           | 31           |
| R        | R_DATA       | R_DATA       | R_DATA       | R_DATA       | R_DATA       | R_DATA       | R_DATA       | R_DATA       | R_DATA       | R_DATA       | R_DATA       | R_DATA       | R_DATA       | R_DATA       | R_DATA       | R_DATA       |
| W        |              |              |              |              |              |              |              |              |              |              |              |              |              |              |              |              |
| Reset    | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            | 0            |
| Reg Addr | Base + 0x0B8 | Base + 0x0B8 | Base + 0x0B8 | Base + 0x0B8 | Base + 0x0B8 | Base + 0x0B8 | Base + 0x0B8 | Base + 0x0B8 | Base + 0x0B8 | Base + 0x0B8 | Base + 0x0B8 | Base + 0x0B8 | Base + 0x0B8 | Base + 0x0B8 | Base + 0x0B8 | Base + 0x0B8 |

Table 19-22. EQADC\_SSIRDR Field Descriptions

| Bits   | Name          | Description                                                                                                                                                                                                               |
|--------|---------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0      | RDV           | Receive data valid. Indicates if the last received data is valid. This bit is cleared automatically whenever the EQADC_SSIRDR is read. Writes have no effect. 0 Receive data is not valid. 1 Receive data is valid.       |
| 1-5    | -             | Reserved.                                                                                                                                                                                                                 |
| 6-31   | R_DATA [0:25] | eQADC receive DATA. Contains the last result message that was shifted in. Writes to the R_DATAhaveno effect. Messages that were not completely received due to a transmission abort will not be copied into EQADC_SSIRDR. |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## 19.3.2.14 eQADC CFIFO Registers (EQADC\_CF[0-5]R n )

EQADC\_CF[0-5]R  provide visibility of the contents of a CFIFO for debugging purposes. Each CFIFO n has four registers that are uniquely mapped to its four 32-bit entries. Refer to Section 19.4.3, 'eQADC Command FIFOs,' for more information on CFIFOs. These registers are read only. Data written to these registers is ignored.

Figure 19-17. eQADC CFIF0[0-5] Registers (EQADC\_CF[0-5]R n )

<!-- image -->

## Table 19-23. EQADC\_CF[0-5]R n Field Descriptions

| Bits   | Name                     | Description                                                                                                                                                                                                    |
|--------|--------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-31   | CFIFO[0-5]_DATA n [0:31] | CFIFO[0-5]_data n . Returns the value stored within the entry of CFIFO[0-5]. Each CFIFO is composed of four 32-bit entries, with register 0 being mapped to the entry with the smallest memory mapped address. |

## 19.3.2.15 eQADC RFIFO Registers (EQADC\_RF[0-5]R n )

EQADC\_RF[0-5]R  provide visibility of the contents of a RFIFO for debugging purposes. Each RFIFO n has four registers which are uniquely mapped to its four 16-bit entries. Refer to Section 19.4.4, 'Result FIFOs,' for more information on RFIFOs. These registers are read only. Data written to these registers is ignored.

Figure 19-18. eQADC RFIFO n Registers (EQADC\_RF[0-5]R n )

<!-- image -->

Table 19-24. EQADC\_RF[0-5]R n Field Descriptions

| Bits   | Name                     | Description                                                                                                                                                                                                    |
|--------|--------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-31   | RFIFO[0-5]_DATA n [0:15] | RFIFO[0-5] data n . Returns the value stored within the entry of RFIFO[0-5]. Each RFIFO is composed of four 16-bit entries, with register 0 being mapped to the entry with the smallest memory mapped address. |

## 19.3.3 On-Chip ADC Registers

This section describes a list of registers that control on-chip ADC operation. The ADC registers are not part  of  the  CPU  accessible  memory  map.  These  registers  can  only  be  accessed  indirectly  through configuration commands. There are five non memory mapped registers per ADC, five for ADC0 and five for  ADC1.  The  address,  usage,  and  access  privilege  of  each  register  is  shown  in  Table 19-25  and Table 19-26. Data written to or read from reserved areas of the memory map is undefined.

Their assigned addresses are the values used to set the ADC\_REG\_ADDRESS field of the read/write configuration  commands  bound  for  the  on-chip  ADCs.  These  are  half-word  addresses.  Further,  the following restrictions apply when accessing these registers:

- · Registers ADC0\_CR, ADC0\_GCCR, and ADC0\_OCCR can only be accessed by configuration commands sent to the ADC0 command buffer.
- · Registers ADC1\_CR, ADC1\_GCCR, and ADC1\_OCCR can only be accessed by configuration commands sent to the ADC1 command buffer.
- · Registers ADC\_TSCR and ADC\_TBCR can be accessed by configuration commands sent to the ADC0 command buffer or to the ADC1 command buffer. A data write to ADC\_TSCR through a configuration command sent to the ADC0 command buffer will write the same memory location

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

as when writing to it through a configuration command sent to the ADC1 command buffer. The same is valid for ADC\_TBCR.

## NOTE

Simultaneous write accesses from the ADC0 and ADC1 command buffers to ADC\_TSCR or to ADC\_TBCR are not allowed.

Table 19-25. ADC0 Registers

| ADC0 Register Address   | Use                                                        | Access     |
|-------------------------|------------------------------------------------------------|------------|
| 0x00                    | ADC0 Address 0x00 is used for conversion command messages. |            |
| 0x01                    | ADC0 Control Register (ADC0_CR)                            | Write/Read |
| 0x02                    | ADC Time Stamp Control Register (ADC_TSCR) 1               | Write/Read |
| 0x03                    | ADC Time Base Counter Register (ADC_TBCR) 1                | Write/Read |
| 0x04                    | ADC0 Gain Calibration Constant Register (ADC0_GCCR)        | Write/Read |
| 0x05                    | ADC0 Offset Calibration Constant Register (ADC0_OCCR)      | Write/Read |
| 0x06-0xFF               | Reserved                                                   | -          |

1 This register is also accessible by configuration commands sent to the ADC1 command buffer.

## Table 19-26. ADC1 Registers

| ADC1 Register Address   | Use                                                        | Access     |
|-------------------------|------------------------------------------------------------|------------|
| 0x00                    | ADC1 Address 0x00 is used for conversion command messages. |            |
| 0x01                    | ADC1 Control Register (ADC1_CR)                            | Write/Read |
| 0x02                    | ADC Time Stamp Control Register (ADC_TSCR) 1               | Write/Read |
| 0x03                    | ADC Time Base Counter Register (ADC_TBCR) 1                | Write/Read |
| 0x04                    | ADC1 Gain Calibration Constant Register (ADC1_GCCR)        | Write/Read |
| 0x05                    | ADC1 Offset Calibration Constant Register (ADC1_OCCR)      | Write/Read |
| 0x06-0xFF               | Reserved                                                   | -          |

1 This register is also accessible by configuration commands sent to the ADC0 command buffer.

## 19.3.3.1 ADC  Control Registers (ADC0\_CR and ADC1\_CR) n

The ADC  control registers (ADC n n \_CR) are used to configure the on-chip ADCs.

## Memory Map/Register Definition

Figure 19-19. ADC n Control Registers (ADC0\_CR and ADC1\_CR)

|          | 0       | 1    | 2    | 3    | 4         | 5    | 6    | 7    | 8    | 9    | 10   | 11   | 12          | 13          | 14          | 15          |
|----------|---------|------|------|------|-----------|------|------|------|------|------|------|------|-------------|-------------|-------------|-------------|
| R        | ADC0_EN | 0    | 0    | 0    | ADC0_EMUX | 0    | 0    | 0    | 0    | 0    | 0    |      | ADC0_CLK_PS | ADC0_CLK_PS | ADC0_CLK_PS | ADC0_CLK_PS |
| W        |         |      |      |      |           |      |      |      |      |      |      |      |             |             |             |             |
| Reset    | 0       | 0    | 0    | 0    | 0         | 0    | 0    | 0    | 0    | 0    | 0    | 1    | 1           | 1           | 1           | 1           |
| Reg Addr | 0x01    | 0x01 | 0x01 | 0x01 | 0x01      | 0x01 | 0x01 | 0x01 | 0x01 | 0x01 | 0x01 | 0x01 | 0x01        | 0x01        | 0x01        | 0x01        |

|          | 0       | 1    | 2    | 3    | 4         | 5    | 6    | 7    | 8    | 9    | 10   | 11   | 12          | 13          | 14          | 15          |
|----------|---------|------|------|------|-----------|------|------|------|------|------|------|------|-------------|-------------|-------------|-------------|
| R        | ADC1_EN | 0    | 0    | 0    | ADC1_EMUX | 0    | 0    | 0    | 0    | 0    | 0    |      | ADC1_CLK_PS | ADC1_CLK_PS | ADC1_CLK_PS | ADC1_CLK_PS |
| W        |         |      |      |      |           |      |      |      |      |      |      |      |             |             |             |             |
| Reset    | 0       | 0    | 0    | 0    | 0         | 0    | 0    | 0    | 0    | 0    | 0    | 1    | 1           | 1           | 1           | 1           |
| Reg Addr | 0x01    | 0x01 | 0x01 | 0x01 | 0x01      | 0x01 | 0x01 | 0x01 | 0x01 | 0x01 | 0x01 | 0x01 | 0x01        | 0x01        | 0x01        | 0x01        |

## Table 19-27. ADC n \_CR Field Descriptions

| Bits   | Name                | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|--------|---------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0      | ADC n _EN           | ADC n enable. Enables ADC n to perform A/D conversions. Refer to Section 19.4.5.1, 'Enabling and Disabling the on-chip ADCs,' for details. 0 ADC is disabled. Clock supply to ADC0/1 is stopped. 1 ADC is enabled and ready to perform A/D conversions. Note: The bias generator circuit inside the ADC ceases functioning when both ADC0_EN and ADC1_EN bits are negated. Note: Conversion commands sent to a disabled ADC are ignored by the ADC control hardware. Note: When the ADC n _EN status is changed from asserted to negated, the ADC clock will not stop until it reaches its low phase.                                                                                                                                                        |
| 1-3    | -                   | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| 4      | ADC n _EMUX         | ADC n external multiplexer enable. WhenADC n _EMUXisasserted, the MApins will output digital values according to the number of the external channel being converted for selecting external multiplexer inputs. Refer to Section 19.4.6, 'Internal/External Multiplexing,' for a detailed description about how ADC n _EMUX affects channel number decoding. 0 External multiplexer disabled; no external multiplexer channels can be selected. 1 External multiplexer enabled; external multiplexer channels can be selected. Note: Both ADC n _EMUX bits must not be asserted at the same time. Note: The ADC n _EMUX bit must only be written when the ADC n _EN bit is negated. ADC n _EMUX can be set during the same write cycle used to set ADC n _EN. |
| 5-10   | -                   | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| 11-15  | ADC n _CLK_PS [0:4] | ADC n clock prescaler. The ADC n _CLK_PS field controls the system clock divide factor for the ADC n clock as in Table 19-28. See Section 19.4.5.2, 'ADC Clock and Conversion Speed,' for details about how to set ADC0/1_CLK_PS. The ADC n _CLK_PSfield must only be written when the ADC n _ENbit is negated. This field can be configured during the same write cycle used to set ADC n _EN.                                                                                                                                                                                                                                                                                                                                                              |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 19-28. System Clock Divide Factor for ADC Clock

| ADC n _CLK_PS[0:4]   |   System Clock Divide Factor |
|----------------------|------------------------------|
| 0b00000              |                            2 |
| 0b00001              |                            4 |
| 0b00010              |                            6 |
| 0b00011              |                            8 |
| 0b00100              |                           10 |
| 0b00101              |                           12 |
| 0b00110              |                           14 |
| 0b00111              |                           16 |
| 0b01000              |                           18 |
| 0b01001              |                           20 |
| 0b01010              |                           22 |
| 0b01011              |                           24 |
| 0b01100              |                           26 |
| 0b01101              |                           28 |
| 0b01110              |                           30 |
| 0b01111              |                           32 |
| 0b10000              |                           34 |
| 0b10001              |                           36 |
| 0b10010              |                           38 |
| 0b10011              |                           40 |
| 0b10100              |                           42 |
| 0b10101              |                           44 |
| 0b10110              |                           46 |
| 0b10111              |                           48 |
| 0b11000              |                           50 |
| 0b11001              |                           52 |
| 0b11010              |                           54 |
| 0b11011              |                           56 |
| 0b11100              |                           58 |
| 0b11101              |                           60 |
| 0b11110              |                           62 |
| 0b11111              |                           64 |

## 19.3.3.2 ADC Time Stamp Control Register (ADC\_TSCR)

The ADC\_TSCR contains a system clock divide factor used in the making of the time base counter clock. It  determines  at  what  frequency  the  time  base  counter  will  run.  ADC\_TSCR  can  be  accessed  by configuration commands sent to ADC0 or to ADC1. A data write to ADC\_TSCR through a configuration command sent to ADC0 will write the same memory location as when writing to it through a configuration command sent to ADC1.

## NOTE

Simultaneous write accesses from ADC0 and ADC1 to ADC\_TSCR are not allowed.

Figure 19-20. ADC Time Stamp Control Register (ADC\_TSCR)

<!-- image -->

|          | 0    | 1    | 2    | 3    | 4    | 5    | 6    | 7    | 8    | 9    | 10   | 11   | 12         | 13         | 14         | 15         |
|----------|------|------|------|------|------|------|------|------|------|------|------|------|------------|------------|------------|------------|
| R        | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | TBC_CLK_PS | TBC_CLK_PS | TBC_CLK_PS | TBC_CLK_PS |
| W        |      |      |      |      |      |      |      |      |      |      |      |      |            |            |            |            |
| Reset    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0          | 0          | 0          | 0          |
| Reg Addr | 0x02 | 0x02 | 0x02 | 0x02 | 0x02 | 0x02 | 0x02 | 0x02 | 0x02 | 0x02 | 0x02 | 0x02 | 0x02       | 0x02       | 0x02       | 0x02       |

## Table 19-29. ADC\_TSCR Field Descriptions

| Bits   | Name             | Description                                                                                                                                                                                                   |
|--------|------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-11   | -                | Reserved.                                                                                                                                                                                                     |
| 12-15  | TBC_CLK_PS [0:3] | Time base counter clock prescaler. Contains the system clock divide factor for the time base counter. It controls the accuracy of the time stamp. The prescaler is disabled when TBC_CLK_PS is set to 0b0000. |

Table 19-30. Clock Divide Factor for Time Stamp

| TBC_CLK_PS[0:3]   | System Clock Divide Factor   | Clock to Time Stamp Counter for a 120 MHz System Clock (MHz)   |
|-------------------|------------------------------|----------------------------------------------------------------|
| 0b0000            | Disabled                     | Disabled                                                       |
| 0b0001            | 1                            | 120                                                            |
| 0b0010            | 2                            | 60                                                             |
| 0b0011            | 4                            | 30                                                             |
| 0b0100            | 6                            | 20                                                             |
| 0b0101            | 8                            | 15                                                             |
| 0b0110            | 10                           | 12                                                             |
| 0b0111            | 12                           | 10                                                             |
| 0b1000            | 16                           | 7.5                                                            |
| 0b1001            | 32                           | 3.75                                                           |
| 0b1010            | 64                           | 1.88                                                           |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 19-30. Clock Divide Factor for Time Stamp  (continued)

| TBC_CLK_PS[0:3]   | System Clock Divide Factor   | Clock to Time Stamp Counter for a 120 MHz System Clock (MHz)   |
|-------------------|------------------------------|----------------------------------------------------------------|
| 0b1011            | 128                          | 0.94                                                           |
| 0b1100            | 256                          | 0.47                                                           |
| 0b1101            | 512                          | 0.23                                                           |
| 0b1110 - 0b1111   | Reserved                     | -                                                              |

## NOTE

If TBC\_CLK\_PS is not set to disabled, it must not be changed to any other value besides disabled. If TBC\_CLK\_PS is set to disabled it can be changed to any other value.

## 19.3.3.3 ADC Time Base Counter Registers (ADC\_TBCR)

The ADC\_TBCR contains the current value of the time base counter. ADC\_TBCR can be accessed by configuration commands sent to ADC0 or to ADC1. A data write to ADC\_TBCR through a configuration command sent to ADC0 will write the same memory location as when writing to it through a configuration command sent to ADC1.

## NOTE

Simultaneous write accesses from ADC0 and ADC1 to ADC\_TBCR are not allowed.

Figure 19-21. ADC Time Base Counter Register (ADC\_TBCR)

<!-- image -->

|          | 0         | 1         | 2         | 3         | 4         | 5         | 6         | 7         | 8         | 9         | 10        | 11        | 12        | 13        | 14        | 15        |
|----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|
| R        | TBC_VALUE | TBC_VALUE | TBC_VALUE | TBC_VALUE | TBC_VALUE | TBC_VALUE | TBC_VALUE | TBC_VALUE | TBC_VALUE | TBC_VALUE | TBC_VALUE | TBC_VALUE | TBC_VALUE | TBC_VALUE | TBC_VALUE | TBC_VALUE |
| W        |           |           |           |           |           |           |           |           |           |           |           |           |           |           |           |           |
| Reset    | 0         | 0         | 0         | 0         | 0         | 0         | 0         | 0         | 0         | 0         | 0         | 0         | 0         | 0         | 0         | 0         |
| Reg Addr | 0x03      | 0x03      | 0x03      | 0x03      | 0x03      | 0x03      | 0x03      | 0x03      | 0x03      | 0x03      | 0x03      | 0x03      | 0x03      | 0x03      | 0x03      | 0x03      |

Table 19-31. ADC\_TBCR Field Descriptions

| Bits   | Name             | Description                                                                                                                                                                                                                                                                                           |
|--------|------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-15   | TBC_VALUE [0:15] | Time base counter VALUE. Contains the current value of the time base counter. Reading TBC_VALUE returns the current value of time base counter. Writes to TBC_VALUE register load the written data to the counter. The time base counter counts from 0x0000 to 0xFFFF and wraps when reaching 0xFFFF. |

## 19.3.3.4 ADC  Gain Calibration Constant Registers (ADC0\_GCCR and n ADC1\_GCCR)

The ADC \_GCCR contains the gain calibration constant used to fine-tune the ADC n n conversion results. Refer to Section 19.4.5.4, 'ADC Calibration Feature,' for details about the calibration scheme used in the eQADC.

Figure 19-22. ADC n Gain Calibration Constant Registers (ADC n \_GCCR)

<!-- image -->

|          | 0    | 1    | 2    | 3    | 4    | 5    | 6    | 7    | 8    | 9    | 10   | 11   | 12   | 13   | 14   | 15   |
|----------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| R        | 0    |      |      |      |      |      |      | GCC0 | GCC0 | GCC0 |      |      |      |      |      |      |
| W        |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |
| Reset    | 0    | 1    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |
| Reg Addr | 0x04 | 0x04 | 0x04 | 0x04 | 0x04 | 0x04 | 0x04 | 0x04 | 0x04 | 0x04 | 0x04 | 0x04 | 0x04 | 0x04 | 0x04 | 0x04 |
|          | 0    | 1    | 2    | 3    | 4    | 5    | 6    | 7    | 8    | 9    | 10   | 11   | 12   | 13   | 14   | 15   |
| R        | 0    |      |      |      |      |      |      | GCC1 | GCC1 | GCC1 |      |      |      |      |      |      |
| W        |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |
| Reset    | 0    | 1    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |
| Reg Addr | 0x04 | 0x04 | 0x04 | 0x04 | 0x04 | 0x04 | 0x04 | 0x04 | 0x04 | 0x04 | 0x04 | 0x04 | 0x04 | 0x04 | 0x04 | 0x04 |

Table 19-32. ADC n \_GCCR Field Descriptions

| Bits   | Name         | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
|--------|--------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0      | -            | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| 1-15   | GCC n [0:14] | ADC n gain calibration constant. Contains the gain calibration constant used to fine-tune ADC n conversion results. It is a unsigned 15-bit fixed pointed value. The gain calibration constant is an unsigned fixed point number expressed in the GCC_INT.GCC_FRAC binary format. The integer part of the gain constant (GCC_INT) contains a single binary digit while its fractional part (GCC_FRAC) contains 14 digits. For details about the GCC data format refer to Section 19.4.5.4.2, 'MAC Unit and Operand Data Format.' |

## 19.3.3.5 ADC  Offset Calibration Constant Registers (ADC0\_OCCR and n ADC1\_OCCR)

The ADC \_OCCR contains the offset calibration constant used to fine-tune of ADC0/1 conversion results. n The offset constant is a signed 14-bit integer value. Refer to Section 19.4.5.4, 'ADC Calibration Feature,' for details about the calibration scheme used in the eQADC.

Figure 19-23. ADC n Offset Calibration Constant Registers (ADC n \_OCCR)

<!-- image -->

|          | 0    | 1    | 2    | 3    | 4    | 5    | 6    | 7    | 8    | 9    | 10   | 11   | 12   | 13   | 14   | 15   |
|----------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| R        | 0    | 0    |      |      |      |      |      |      | OCC0 |      |      |      |      |      |      |      |
| W        |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |
| Reset    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |
| Reg Addr | 0x05 | 0x05 | 0x05 | 0x05 | 0x05 | 0x05 | 0x05 | 0x05 | 0x05 | 0x05 | 0x05 | 0x05 | 0x05 | 0x05 | 0x05 | 0x05 |
|          | 0    | 1    | 2    | 3    | 4    | 5    | 6    | 7    | 8    | 9    | 10   | 11   | 12   | 13   | 14   | 15   |
| R        | 0    | 0    |      |      |      |      |      |      | OCC1 |      |      |      |      |      |      |      |
| W        |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |
| Reset    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |
| Reg Addr | 0x05 | 0x05 | 0x05 | 0x05 | 0x05 | 0x05 | 0x05 | 0x05 | 0x05 | 0x05 | 0x05 | 0x05 | 0x05 | 0x05 | 0x05 | 0x05 |

Table 19-33. ADC n \_OCCR Field Descriptions

| Bits   | Name         | Description                                                                                                                                                                                            |
|--------|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-1    | -            | Reserved.                                                                                                                                                                                              |
| 2-15   | OCC n [0:13] | ADC n offset calibration constant. Contains the offset calibration constant used to fine-tune ADC n conversion results. Negative values should be expressed using the two's complement representation. |

## 19.4 Functional Description

The eQADC provides a parallel interface to two on-chip ADCs, and a single master to single slave serial interface to an off-chip external device. The two on-chip ADCs are architected to allow access to all the analog channels.

Initially, command data is contained in system memory in a user defined data queue structure. Command data is moved between the user-defined queues and CFIFOs by the host CPU or by the eDMA which responds to interrupt and eDMA requests generated by the eQADC. The eQADC supports software and hardware triggers from other modules or external pins to initiate transfers of commands from the multiple CFIFOs to the on-chip ADCs or to the external device.

CFIFOs can be configured to be in single-scan or continuous-scan mode. When a CFIFO is configured to be in single-scan mode, the eQADC scans the user-defined command queue one time. The eQADC stops transferring commands from the triggered CFIFO after detecting the EOQ bit set in the last transfer. After an EOQ bit is detected, software involvement is required to rearm the CFIFO so that it can detect new trigger events.

When a CFIFO is configured  for  continuous-scan  mode,  the  whole  user  command  queue  is  scanned multiple times. After the detection of an asserted EOQ bit in the last command transfer, command transfers can continue or not depending on the mode of operation of the CFIFO.

The eQADC can also in parallel and independently of the CFIFOs receive data from the on-chip ADCs or from  off-chip  external  device  into  multiple  RFIFOs.  Result  data  is  moved  from  the  RFIFOs  to  the user-defined result queues in system memory by the host CPU or by the eDMA.

## 19.4.1 Data Flow in the eQADC

Figure 19-24 shows how command data flows inside the eQADC system. A command message is the predefined format in which command data is stored in the user-defined command queues. A command message has 32 bits and is composed of two parts: a CFIFO header and an ADC command. Command messages are moved from the user command queues to the CFIFOs by the host CPU or by the eDMA as they respond to interrupt and eDMA requests generated by the eQADC. The eQADC generates these requests whenever a CFIFO is not full. The FIFO control unit will only transfer the command part of the command message to the selected ADC. Information in the CFIFO header together with the upper bit of the ADC command is used by the FIFO control unit to arbitrate which triggered CFIFO will be transferring the next command. Because command transfer through the serial interface can take significantly more time than a parallel transfer to the on-chip ADCs, command transfers for on-chip ADCs occur concurrently with the transfers through the serial interface. Commands sent to the ADCs are executed in a first-in-first-out (FIFO) basis and three types of results can be expected: data read from an ADC register, a conversion result, or a time stamp. The order at which ADC commands sent to the external device are executed, and the type of results that can be expected depends on the architecture of that device with the exception of unsolicited data like null messages for example.

## NOTE

While the eQADC pops commands out from a CFIFO, it also is checking the number of entries in the CFIFO and generating requests to fill it. The process of pushing and popping commands to and from a CFIFO can occur simultaneously.

The FIFO control unit expects all incoming results to be shaped in a pre-defined result message format. Figure 19-25 shows how result data flows inside the eQADC system. Results generated on the on-chip ADCs are formatted into result messages inside the result format and calibration submodule. Results returning from the external device are already formatted into result messages and therefore bypass the result format and calibration submodule located inside the eQADC. A result message is composed of an RFIFO header and an ADC Result. The FIFO control unit decodes the information contained in the RFIFO header to determine the RFIFO to which the ADC result should be sent. Once in an RFIFO, the ADC result is moved to the corresponding user result queue by the host CPU or by the eDMA as they respond to interrupt and eDMA requests generated by the eQADC. The eQADC generates these requests whenever an RFIFO has at least one entry.

## NOTE

While conversion results are returned, the eQADC is checking the number of entries in the RFIFO and generating requests to empty it. The process of pushing  and  popping  ADC  results  to  and  from  an  RFIFO  can  occur simultaneously.

Figure 19-24. Command Flow During eQADC Operation

<!-- image -->

Figure 19-25. Result Flow During eQADC Operation

<!-- image -->

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## 19.4.1.1 Assumptions/Requirements Regarding the External Device

The  external  device  exchanges  command  and  result  data  with  the  eQADC  through  the  eQADC  SSI interface. This section explains the minimum requirements an external device has to meet to properly interface  with  the  eQADC.  Some  assumptions  about  the  architecture  of  the  external  device  are  also described.

## 19.4.1.1.1 eQADC SSI Protocol Support

The external device must fully support the eQADC SSI protocol as specified in Section 19.4.8, 'eQADC Synchronous Serial Interface (SSI) Submodule,' section of this document. Support for the abort feature is optional. When aborts are not supported, all command messages bound for an external command buffer must have the ABORT\_ST bit negated - see Section , ' Command Message Format for External Device Operation.'

## 19.4.1.1.2 Number of Command Buffers and Result Buffers

The external device should have a minimum of one and a maximum of two command buffers to store command data sent from the eQADC. If more than two command buffers are implemented in the external device, they are not recognized by the eQADC as valid destinations for commands. In this document, the two valid external command buffers are referred to as command buffer 2 and command buffer 3 (the two on-chip ADCs being command buffer 0 and 1). The external device decides to which external command buffer a command should go by decoding the upper bit (BN bit) of the ADC command - see Section , ' Command Message Format for External Device Operation.' An external device that only implements one command buffer can ignore the BN bit.

The limit of two command buffers does not limit the number of result buffers in the slave device.

## 19.4.1.1.3 Command Execution and Result Return

Commands sent to a specific external command buffer should be executed in the order they were received.

Results generated by the execution of commands in an external command buffer should be returned in the order that the command buffer received these commands.

## 19.4.1.1.4 Null and Result Messages

The  external  device  must  be  capable  of  correctly  processing  null  messages  as  specified  in  the Section 19.3.2.2, 'eQADC Null Message Send Format Register (EQADC\_NMSFR).'

In case no valid result data is available to be sent to the eQADC, the external device must send data in the format specified in Section , ' Null Message Format for External Device Operation.'

In case valid result data is available to sent to the eQADC, the external device must send data in the format specified in Section , ' Result Message Format for External Device Operation.'

The BUSY0/1 fields of all  messages  sent  from  the  external  device  to  the  eQADC  must  be  correctly encoded according to the latest information on the fullness state of the command buffers. For example, if external command buffer 2 is empty before the end of the current serial transmission and if at the end of this transmission the external device receives a command to command buffer 2, then the BUSY0 field, that is to be sent to the eQADC on the next serial transmission, should be encoded assuming that the external command buffer has one entry.

## 19.4.1.2 Message Format in eQADC

This section explains the command and result message formats used for on-chip ADC operation and for external device operation.

A command message is the pre-defined format at which command data is stored in the user command queues. A command message has 32 bits and is composed of two parts: a CFIFO header and an ADC command. The size of the CFIFO header is fixed to 6 bits, and it works as inputs to the FIFO control unit. The header controls when a command queue ends, when it pauses, if commands are sent to internal or external buffers, and if it can abort a serial data transmission. Information contained in the CFIFO header, together with the upper bit of the ADC command, is used by the FIFO control unit to arbitrate which triggered CFIFO will transfer the next command. ADC commands are encoded inside the least significant 26 bits of the command message.

A result message is composed of an RFIFO header and an ADC result. The FIFO control unit decodes the information contained in the RFIFO header to determine the RFIFO to which the ADC result should be sent. An ADC result is always 16 bits long.

## 19.4.1.2.1 Message Formats for On-Chip ADC Operation

This section describes the command/result message formats used for on-chip ADC operation.

## NOTE

Although this subsection describes how the command and result messages are formatted to communicate with the on-chip ADCs, nothing prevents the programmer from using a different format when communicating with an external  device  through  the  serial  interface.  Refer  to  Section 19.4.1.2.2, 'Message Formats for External Device Operation.' Apart from the BN bit, the ADC  command  of  a  command  message  can  be  formatted  to communicate to an arbitrary external device provided that the device returns an RFIFO header in the format expected by the eQADC. When the FIFO control unit receives return data message, it decodes the message tag field and stores the 16-bit data into the corresponding RFIFO.

## Conversion Command Message Format for On-Chip ADC Operation

Figure 19-26 describes the command message format for conversion commands when interfacing with the on-chip  ADCs.  A  conversion  result  is  always  returned  for  conversion  commands  and  time  stamp information can be optionally requested. The lower byte of conversion commands is always set to 0 to distinguish it from configuration commands.

<!-- image -->

ADC Command

Figure 19-26. Conversion Command Message Format for On-Chip ADC Operation

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## Table 19-34. On-Chip ADC Field Descriptions: Conversion Command Message Format

| Bits   | Name   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
|--------|--------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0      | EOQ    | End-of-queue. Asserted in the last command of a command queue to indicate to the eQADC that a scan of the queue is completed. EOQ instructs the eQADC to reset its current CFIFO transfer counter value (TC_CF) to 0. Depending on the CFIFO mode of operation, the CFIFO status will also change upon the detection of an asserted EOQbit on the last transferred command. See Section 19.4.3.5, 'CFIFO Scan Trigger Modes,' for details. 0 Not the last entry of the command queue. 1 Last entry of the command queue. Note: If both the pause and EOQ bits are asserted in the same command message the respective flags are set, but the CFIFO status changes as if only the EOQ bit were asserted.                                                                         |
| 1      | PAUSE  | Pause. Allows software to create sub-queues within a command queue. When the eQADC completes the transfer of a command with an asserted pause bit, the CFIFO enters the WAITING FORTRIGGERstate. Refer to Section 19.4.3.6.1, 'CFIFO Operation Status,' for a description of the state transitions. The pause bit is only valid when CFIFO operation mode is configured to single or continuous-scan edge trigger mode. 0 Do not enter WAITING FOR TRIGGER state after transfer of the current command message. 1 Enter WAITING FOR TRIGGER state after transfer of the current command message. Note: If both the pause and EOQ bits are asserted in the same command message the respective flags are set, but the CFIFO status changes as if only the EOQ bit were asserted. |
| 2-4    | -      | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| 5      | EB     | External buffer bit. Anegated EBbit indicates that the command is sent to an on chip ADC. 0 Command is sent to an internal buffer. 1 Command is sent to an external buffer.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| 6      | BN     | Buffer number. Indicates which ADC the message will be sent to. ADCs 1 and 0 can either be internal or external depending on the EB bit setting. 0 Message sent to ADC 0. 1 Message sent to ADC 1.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| 7      | CAL    | Calibration. Indicates if the returning conversion result must be calibrated. 0 Do not calibrate conversion result. 1 Calibrate conversion result.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |

## Table 19-34. On-Chip ADC Field Descriptions:

## Conversion Command Message Format  (continued)

| Bits   | Name              | Description                                                                                                                                                                                                                                                                                                                                                                             | Description                                                                                                                                                                                                                                                                                                                                                                             |
|--------|-------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 8-11   | MESSAGE_TAG [0:3] | MESSAGE_TAG field. Allows the eQADC to separate returning results into different RFIFOs. When the eQADC transfers a command, the MESSAGE_TAG is included as part of the command. Eventually the external device/on-chip ADC returns the result with the same MESSAGE_TAG. The eQADC separates incoming messages into different RFIFOs by decoding the MESSAGE_TAG of the incoming data. | MESSAGE_TAG field. Allows the eQADC to separate returning results into different RFIFOs. When the eQADC transfers a command, the MESSAGE_TAG is included as part of the command. Eventually the external device/on-chip ADC returns the result with the same MESSAGE_TAG. The eQADC separates incoming messages into different RFIFOs by decoding the MESSAGE_TAG of the incoming data. |
|        |                   | MESSAGE_TAG[0:3]                                                                                                                                                                                                                                                                                                                                                                        | MESSAGE_TAG Meaning                                                                                                                                                                                                                                                                                                                                                                     |
|        |                   | 0b0000                                                                                                                                                                                                                                                                                                                                                                                  | Result is sent to RFIFO 0                                                                                                                                                                                                                                                                                                                                                               |
|        |                   | 0b0001                                                                                                                                                                                                                                                                                                                                                                                  | Result is sent to RFIFO 1                                                                                                                                                                                                                                                                                                                                                               |
|        |                   | 0b0010                                                                                                                                                                                                                                                                                                                                                                                  | Result is sent to RFIFO 2                                                                                                                                                                                                                                                                                                                                                               |
|        |                   | 0b0011                                                                                                                                                                                                                                                                                                                                                                                  | Result is sent to RFIFO 3                                                                                                                                                                                                                                                                                                                                                               |
|        |                   | 0b0100                                                                                                                                                                                                                                                                                                                                                                                  | Result is sent to RFIFO 4                                                                                                                                                                                                                                                                                                                                                               |
|        |                   | 0b0101                                                                                                                                                                                                                                                                                                                                                                                  | Result is sent to RFIFO 5                                                                                                                                                                                                                                                                                                                                                               |
|        |                   | 0b0110-0b0111                                                                                                                                                                                                                                                                                                                                                                           | Reserved                                                                                                                                                                                                                                                                                                                                                                                |
|        |                   | 0b1000                                                                                                                                                                                                                                                                                                                                                                                  | Null message received                                                                                                                                                                                                                                                                                                                                                                   |
|        |                   | 0b1001                                                                                                                                                                                                                                                                                                                                                                                  | Reserved for customer use. 1                                                                                                                                                                                                                                                                                                                                                            |
|        |                   | 0b1010                                                                                                                                                                                                                                                                                                                                                                                  | Reserved for customer use. 1                                                                                                                                                                                                                                                                                                                                                            |
|        |                   | 0b1011-0b1111                                                                                                                                                                                                                                                                                                                                                                           | Reserved                                                                                                                                                                                                                                                                                                                                                                                |
|        |                   | 1 These messages are treated as null messages. Therefore, they must obey the format for incoming null messages and return valid BUSY0/1 fields. Refer to Section , ' Null Message Format for External Device Operation.'                                                                                                                                                                | 1 These messages are treated as null messages. Therefore, they must obey the format for incoming null messages and return valid BUSY0/1 fields. Refer to Section , ' Null Message Format for External Device Operation.'                                                                                                                                                                |
| 12-13  | LST [0:1]         | Long sampling time. These two bits determine the duration of the sampling time in ADC clock cycles. Note: For external mux mode, 64 or 128 sampling cycles is recommended.                                                                                                                                                                                                              | Long sampling time. These two bits determine the duration of the sampling time in ADC clock cycles. Note: For external mux mode, 64 or 128 sampling cycles is recommended.                                                                                                                                                                                                              |
|        |                   |                                                                                                                                                                                                                                                                                                                                                                                         | Sampling cycles (ADC Clock Cycles)                                                                                                                                                                                                                                                                                                                                                      |
|        |                   |                                                                                                                                                                                                                                                                                                                                                                                         | 2                                                                                                                                                                                                                                                                                                                                                                                       |
|        |                   |                                                                                                                                                                                                                                                                                                                                                                                         | 8                                                                                                                                                                                                                                                                                                                                                                                       |
|        |                   |                                                                                                                                                                                                                                                                                                                                                                                         | 64                                                                                                                                                                                                                                                                                                                                                                                      |
|        |                   |                                                                                                                                                                                                                                                                                                                                                                                         | 128                                                                                                                                                                                                                                                                                                                                                                                     |
| 14     | TSR               | Time stamp request. TSR indicates the request for a time stamp. When TSR is asserted, the on-chip ADC control logic returns a time stamp for the current conversion command after the conversion result is sent to the RFIFOs. See Section 19.4.5.3, 'Time Stamp Feature,' for details. 0 Return conversion result only.                                                                | Time stamp request. TSR indicates the request for a time stamp. When TSR is asserted, the on-chip ADC control logic returns a time stamp for the current conversion command after the conversion result is sent to the RFIFOs. See Section 19.4.5.3, 'Time Stamp Feature,' for details. 0 Return conversion result only.                                                                |

## Table 19-34. On-Chip ADC Field Descriptions: Conversion Command Message Format  (continued)

| Bits   | Name                  | Description                                                                                                                                                                                                                                                                                          |
|--------|-----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 15     | FMT                   | Conversion data format. FMT specifies to the eQADC how to format the 12-bit conversion data returned by the ADCsinto the 16-bit format which is sent to the RFIFOs. See Section , ' ADC Result Format for On-Chip ADC Operation,' for details. 0 Right justified unsigned. 1 Right justified signed. |
| 16-23  | CHANNEL_ NUMBER [0:7] | Channel number. Selects the analog input channel. The software programs this field with the channel number corresponding to the analog input pin to be sampled and converted. See Section 19.4.6.1, 'Channel Assignment,' for details.                                                               |
| 24-31  | -                     | Reserved.                                                                                                                                                                                                                                                                                            |

## Write Configuration Command Message Format for On-Chip ADC Operation

Figure 19-27 describes the command message format for a write configuration command when interfacing with the on-chip ADCs. A write configuration command is used to set the control registers of the on-chip ADCs. No conversion  data  will  be  returned  for  a  write  configuration  command.  Write  configuration commands are differentiated from read configuration commands by a negated R/W bit.

<!-- image -->

ADC Command

Figure 19-27. Write Configuration Command Message Format for On-chip ADC Operation

Table 19-35. On-Chip ADC Field Descriptions: Write Configuration

| Bits   | Name                           | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
|--------|--------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0      | EOQ                            | End-of-queue. Asserted in the last command of a command queue to indicate to the eQADC that a scan of the queue is completed. EOQ instructs the eQADC to reset its current CFIFO transfer counter value (TC_CF) to 0. Depending on the CFIFO mode of operation, the CFIFO status will also change upon the detection of an asserted EOQbit on the last transferred command. See Section 19.4.3.5, 'CFIFO Scan Trigger Modes,' for details. 0 Not the last entry of the command queue. 1 Last entry of the command queue. Note: If both the pause and EOQ bits are asserted in the same command message the respective flags are set, but the CFIFO status changes as if only the EOQ bit were asserted.                                                                                |
| 1      | PAUSE                          | Pause bit. Allows software to create sub-queues within a command queue. When the eQADC completes the transfer of a command with an asserted pause bit, the CFIFO enters the WAITING FOR TRIGGER state. Refer to Section 19.4.3.6.1, 'CFIFO Operation Status,' for a description of the state transitions. The pause bit is only valid when CFIFO operation mode is configured to single or continuous-scan edge trigger mode. 0 Do not enter WAITING FOR TRIGGER state after transfer of the current command message. 1 Enter WAITING FOR TRIGGER state after transfer of the current command message. Note: If both the pause and EOQ bits are asserted in the same command message, the respective flags are set, but the CFIFO status changes as if only the EOQ bit were asserted. |
| 2-4    | -                              | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| 5      | EB                             | External buffer bit. This bit should always be cleared for messages sent to an on-chip ADC. 0 Command is sent to an internal command buffer. 1 Command is sent to an external command buffer.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 6      | BN                             | Buffer number. Indicates which buffer the message will be stored in. Buffers 1 and 0 can either be internal or external depending on the EB bit setting. 0 Message stored in buffer 0. 1 Message stored in buffer 1.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| 7      | R/W                            | Read/write. A negated R/W indicates a write configuration command. 0 Write 1 Read                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| 8-15   | ADC_ REGISTER_ HIGH_BYTE [0:7] | ADC register high byte. The value to be written into the most significant 8 bits of control/configuration register when the R/W bit is negated.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| 16-23  | ADC_ REGISTER_ LOW_BYTE [0:7]  | ADC register low byte. The value to be written into the least significant 8 bits of a control/configuration register when the R/W bit is negated.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| 24-31  | ADC_REG_ ADDRESS [0:7]         | ADCregister address. Selects a register on the ADCregister set to be written or read. Only half-word addresses can be used. See Table 19-25.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |

## Read Configuration Command Message Format for On-Chip ADC Operation

Figure 19-28 describes the command message format for a read configuration command when interfacing with the on-chip ADCs. A read configuration command is used to read the contents of the on-chip ADC registers which  are  only  accessible  via  command  messages.  Read  configuration  commands  are differentiated from write configuration commands by an asserted R/W bit.

<!-- image -->

| 0                        | 1                        | 2                        | 3                        | 4                        | 5                        | 6                        |                          | 7                        | 8                        | 9                        | 10                       | 11                       | 12                       | 13                       | 14                       | 15                       |
|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|
| EOQ                      | PAUSE                    | Reserved                 | Reserved                 | Reserved                 | EB (0b0)                 | BN                       | R/W (0b1)                |                          | MESSAGE_TAG              | MESSAGE_TAG              | MESSAGE_TAG              | MESSAGE_TAG              | Reserved                 | Reserved                 | Reserved                 | Reserved                 |
| CFIFO Header ADC Command | CFIFO Header ADC Command | CFIFO Header ADC Command | CFIFO Header ADC Command | CFIFO Header ADC Command | CFIFO Header ADC Command | CFIFO Header ADC Command | CFIFO Header ADC Command | CFIFO Header ADC Command | CFIFO Header ADC Command | CFIFO Header ADC Command | CFIFO Header ADC Command | CFIFO Header ADC Command | CFIFO Header ADC Command | CFIFO Header ADC Command | CFIFO Header ADC Command | CFIFO Header ADC Command |
| 16                       | 17                       | 18                       | 19                       | 20                       | 21                       | 22                       | 23                       | 24                       | 25                       | 26                       | 27                       |                          | 28                       | 29                       | 30                       | 31                       |
| Reserved                 | Reserved                 | Reserved                 | Reserved                 | Reserved                 | Reserved                 | Reserved                 | Reserved                 | Reserved                 | ADC_REG_ADDRESS          | ADC_REG_ADDRESS          | ADC_REG_ADDRESS          | ADC_REG_ADDRESS          | ADC_REG_ADDRESS          | ADC_REG_ADDRESS          | ADC_REG_ADDRESS          | ADC_REG_ADDRESS          |

ADC Command

Figure 19-28. Read Configuration Command Message Format for On-Chip ADC Operation

Table 19-36. On-Chip ADC Field Descriptions: Read Configuration

| Bits   | Name   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
|--------|--------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0      | EOQ    | End-of-queue. Asserted in the last command of a command queue to indicate to the eQADC that a scan of the queue is completed. EOQ instructs the eQADC to reset its current CFIFO transfer counter value (TC_CF) to 0. Depending on the CFIFO mode of operation, the CFIFO status will also change upon the detection of an asserted EOQbit on the last transferred command. See Section 19.4.3.5, 'CFIFO Scan Trigger Modes,' for details. 0 Not the last entry of the command queue. 1 Last entry of the command queue. Note: If both the pause and EOQ bits are asserted in the same command message the respective flags are set, but the CFIFO status changes as if only the EOQbit were asserted.                                                                               |
| 1      | PAUSE  | Pause bit. Allows software to create sub-queues within a command queue. When the eQADC completes the transfer of a command with an asserted pause bit, the CFIFO enters the WAITING FOR TRIGGER state. Refer to Section 19.4.3.6.1, 'CFIFO Operation Status,' for a description of the state transitions. The pause bit is only valid when CFIFO operation mode is configured to single or continuous-scan edge trigger mode. 0 Do not enter WAITING FOR TRIGGER state after transfer of the current command message. 1 Enter WAITING FOR TRIGGER state after transfer of the current command message. Note: If both the pause and EOQ bits are asserted in the same command message the respective flags are set, but the CFIFO status changes as if only the EOQbit were asserted. |
| 2-4    | -      | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| 5      | EB     | External buffer bit. This bit should always be cleared for messages sent to an on-chip ADC. 0 Command is sent to an internal command buffer. 1 Command is sent to an external command buffer.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |

Table 19-36. On-Chip ADC Field Descriptions: Read Configuration  (continued)

| Bits   | Name                   | Description                                                                                                                                                                                                                                                                                                                                                                                    |
|--------|------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 6      | BN                     | Buffer number. Indicates which buffer the message will be stored in. Buffers 1 and 0 can either be internal or external depending on the EB bit setting. 0 Message stored in buffer 0. 1 Message stored in buffer 1.                                                                                                                                                                           |
| 7      | R/W                    | Read/write. An asserted R/W bit indicates a read configuration command. 0 Write                                                                                                                                                                                                                                                                                                                |
| 8-11   | MESSAGE_TAG [0:3]      | 1 Read MESSAGE_TAG field. Allows the eQADC to separate returning results into different RFIFOs. When the eQADC transfers a command, the MESSAGE_TAG is included as part of the command. Eventually the external device/on-chip ADC returns the result with the same MESSAGE_TAG. The eQADC separates incoming messages into different RFIFOs by decoding the MESSAGE_TAG of the incoming data. |
| 8-11   | MESSAGE_TAG [0:3]      |                                                                                                                                                                                                                                                                                                                                                                                                |
| 8-11   | MESSAGE_TAG [0:3]      |                                                                                                                                                                                                                                                                                                                                                                                                |
| 8-11   | MESSAGE_TAG [0:3]      |                                                                                                                                                                                                                                                                                                                                                                                                |
| 8-11   | MESSAGE_TAG [0:3]      |                                                                                                                                                                                                                                                                                                                                                                                                |
| 8-11   | MESSAGE_TAG [0:3]      |                                                                                                                                                                                                                                                                                                                                                                                                |
| 8-11   | MESSAGE_TAG [0:3]      |                                                                                                                                                                                                                                                                                                                                                                                                |
| 8-11   | MESSAGE_TAG [0:3]      |                                                                                                                                                                                                                                                                                                                                                                                                |
| 8-11   | MESSAGE_TAG [0:3]      |                                                                                                                                                                                                                                                                                                                                                                                                |
| 8-11   | MESSAGE_TAG [0:3]      |                                                                                                                                                                                                                                                                                                                                                                                                |
| 8-11   | MESSAGE_TAG [0:3]      |                                                                                                                                                                                                                                                                                                                                                                                                |
| 8-11   | MESSAGE_TAG [0:3]      |                                                                                                                                                                                                                                                                                                                                                                                                |
| 8-11   | MESSAGE_TAG [0:3]      |                                                                                                                                                                                                                                                                                                                                                                                                |
| 8-11   | MESSAGE_TAG [0:3]      | 1 These messages are treated as null messages. Therefore, they must obey the format for incoming null messages and return valid BUSY0/1 fields. Refer to Section , ' Null Message Format for External Device Operation.'                                                                                                                                                                       |
| 12-23  | -                      | Reserved.                                                                                                                                                                                                                                                                                                                                                                                      |
| 24-31  | ADC_REG_ ADDRESS [0:7] | ADCregister address. Selects a register on the ADCregister set to be written or read. Only half-word addresses can be used. See Table 19-25.                                                                                                                                                                                                                                                   |

## ADC Result Format for On-Chip ADC Operation

When the FIFO control unit receives a return data message, it decodes the MESSAGE\_TAG field and stores the 16-bit data into the appropriate RFIFO. This section describes the ADC result portion of the result message returned by the on-chip ADCs.

The 16-bit data stored in the RFIFOs can be the following:

- · Data read from an ADC register with a read configuration command. In this case, the stored 16-bit data corresponds to the contents of the ADC register that was read.
- · A time stamp. In this case, the stored 16-bit data is the value of the time base counter latched when the eQADC detects the end of the analog input voltage sampling. For details see Section 19.4.5.3, 'Time Stamp Feature.'

- · A conversion result. In this case, the stored 16-bit data contains a right justified 14-bit result data. The conversion result can be calibrated or not depending on the status of CAL bit in the command that requested the conversion. When the CAL bit is negated, this 14-bit data is obtained by executing a 2-bit left-shift on the 12-bit data received from the ADC. When the CAL bit is asserted, this 14-bit data is the result of the calculations performed in the EQADC MAC unit using the12-bit data received from the ADC and the calibration constants GCC and OCC (See Section 19.4.5.4, 'ADC Calibration Feature'). Then, this 14-bit data is further formatted into a 16-bit format according to the status of the FMT bit in the conversion command. When FMT is asserted, the 14-bit result data is reformatted to look as if it was measured against an imaginary ground at VREF/2 (the msb (most significant bit) bit of the 14-bit result is inverted), and is sign-extended to a 16-bit format as in Figure 19-29. When FMT is negated, the eQADC zero-extends the 14-bit result data to a 16-bit format as in Figure 19-30. Correspondence between the analog voltage in a channel and the calculated digital values is shown in Table 19-39.

| 0 1      | 2 3 4 5 6 7 8 9 10                        |   11 | 12   | 13   | 14   |   15 |
|----------|-------------------------------------------|------|------|------|------|------|
| SIGN_EXT | CONVERSION_RESULT (With inverted msb bit) |    0 |      |      |      |    0 |

ADC Result

Figure 19-29. ADC Result Format when FMT = 1 (Right Justified Signed)On-Chip ADC Operation

Table 19-37. ADC Result Format when FMT = 1 Field Descriptions

| Bits   | Name                      | Description                                                                                                                                                                                                  |
|--------|---------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-1    | SIGN_EXT [0:1]            | Sign extension. Only has meaning when FMT is asserted. SIGN_EXT is 0b00 when CONVERSION_RESULT is positive, and 0b11 when CONVERSION_RESULT is negative.                                                     |
| 2-15   | CONVERSION _RESULT [0:13] | Conversion result. A digital value corresponding to the analog input voltage in a channel when the conversion command was initiated. The two's complement representation is used to express negative values. |

|   0 |   1 | 2 3 4 5 6 7 8 9 10 11 12 13 14 15   |
|-----|-----|-------------------------------------|
|   0 |   0 | CONVERSION_RESULT 0 0               |

ADC Result

Figure 19-30. ADC Result Format when FMT = 0 (Right Justified Unsigned)On-Chip ADC Operation

Table 19-38. ADC Result Format when FMT = 0 Field Descriptions

| Bits   | Name                      | Description                                                                                                                                              |
|--------|---------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0-1    | SIGN_EXT [0:1]            | Sign extension. Only has meaning when FMT is asserted. SIGN_EXT is 0b00 when CONVERSION_RESULT is positive, and 0b11 when CONVERSION_RESULT is negative. |
| 2-15   | CONVERSION _RESULT [0:13] | Conversion result. A digital value corresponding to the analog input voltage in a channel when the conversion command was initiated.                     |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 19-39. Correspondence between Analog Voltages and Digital Values 1, 2

|                          | Voltage Level on Channel (V)   | Corresponding 12-bit Conversion Result Returned by the ADC   | 16-bit Result Sent to RFIFOs (FMT=0) 3   | 16-bit Result Sent to RFIFOs (FMT=1) 3   |
|--------------------------|--------------------------------|--------------------------------------------------------------|------------------------------------------|------------------------------------------|
| Single-Ended Conversions | 5.12                           | 0xFFF                                                        | 0x3FFC                                   | 0x1FFC                                   |
| Single-Ended Conversions | 5.12 - lsb                     | 0xFFF                                                        | 0x3FFC                                   | 0x1FFC                                   |
| Single-Ended Conversions | ...                            | ...                                                          | ...                                      | ...                                      |
| Single-Ended Conversions | 2.56                           | 0x800                                                        | 0x2000                                   | 0x0000                                   |
| Single-Ended Conversions | ...                            | ...                                                          | ...                                      | ...                                      |
| Single-Ended Conversions | 1 lsb                          | 0x001                                                        | 0x0004                                   | 0xE004                                   |
| Single-Ended Conversions | 0                              | 0x000                                                        | 0x0000                                   | 0xE000                                   |
| Differential Conversions | 2.56                           | 0xFFF                                                        | 0x3FFC                                   | 0x1FFC                                   |
| Differential Conversions | 2.56 - lsb                     | 0xFFF                                                        | 0x3FFC                                   | 0x1FFC                                   |
| Differential Conversions | ...                            | ...                                                          | ...                                      | ...                                      |
| Differential Conversions | 0                              | 0x800                                                        | 0x2000                                   | 0x0000                                   |
| Differential Conversions | ...                            | ...                                                          | ...                                      | ...                                      |
| Differential Conversions | -2.56 + lsb                    | 0x001                                                        | 0x0004                                   | 0xE004                                   |
| Differential Conversions | -2.56                          | 0x000                                                        | 0x0000                                   | 0xE000                                   |

- 1 VREF =V RH  -V RL =5.12V. Resulting in one 12-bit count (lsb) =1.25mV.
- 2 The two's complement representation is used to express negative values.
- 3 Assuming uncalibrated conversion results.

## 19.4.1.2.2 Message Formats for External Device Operation

This section describes the command messages, data messages, and null messages formats used for external device operation.

## Command Message Format for External Device Operation

Figure 19-31 describes the command message format for external device operation. Command message formats for on-chip operation and for external device operation share the same CFIFO header format. However, there are no limitations regarding the format an ADC Command used to communicate to an arbitrary external device. Only the upper bit of an ADC Command has a fixed format (BN field) to indicate to the FIFO control unit/external device to which external command buffer the corresponding command should be sent. The remaining 25 bits can be anything decodable by the external device. Only the ADC command portion of a command message is transferred to the external device.

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

EOQ

PAUSE

Reserved

ABORT\_ST

EB

(0b1)

BN

OFF\_CHIP\_COMMAND

CFIFO Header

ADC Command

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

OFF\_CHIP\_COMMAND

<!-- image -->

ADC Command

Figure 19-31. Command Message Format for External Device Operation

Table 19-40. On-Chip ADC Field Descriptions: External Device Operation

| Bits   | Name     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
|--------|----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0      | EOQ      | End-of-queue. Asserted in the last command of a command queue to indicate to the eQADC that a scan of the queue is completed. EOQ instructs the eQADC to reset its current CFIFO transfer counter value (TC_CF) to 0. Depending on the CFIFO mode of operation, the CFIFO status will also change upon the detection of an asserted EOQ bit on the last transferred command. See Section 19.4.3.5, 'CFIFO Scan Trigger Modes,' for details. 0 Not the last entry of the command queue. 1 Last entry of the command queue. Note: If both the pause and EOQbits are asserted in the same command message the respective flags are set, but the CFIFO status changes as if only the EOQ bit were asserted.                                                                          |
| 1      | PAUSE    | Pause bit. Allows software to create sub-queues within a commandqueue.Whenthe eQADCcompletes the transfer of a command with an asserted pause bit, the CFIFO enters the WAITING FOR TRIGGER state. Refer to Section 19.4.3.6.1, 'CFIFO Operation Status,' for a description of the state transitions. The pause bit is only valid when CFIFO operation mode is configured to single or continuous-scan edge trigger mode. 0 Do not enter WAITING FOR TRIGGER state after transfer of the current command message. 1 Enter WAITING FOR TRIGGER state after transfer of the current command message. Note: If both the pause and EOQbits are asserted in the same command message the respective flags are set, but the CFIFO status changes as if only the EOQ bit were asserted. |
| 2-3    | -        | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| 4      | ABORT_ST | ABORT serial transmission. Indicates whether an on-going serial transmission should be aborted or not. All CFIFOs can abort null message transmissions when triggered but only CFIFO0 can abort command transmissions of lower priority CFIFOs. For more on serial transmission aborts see Section 19.4.3.2, 'CFIFO Prioritization and Command Transfer.' 0 Do not abort current serial transmission. 1 Abort current serial transmission.                                                                                                                                                                                                                                                                                                                                       |
| 5      | EB       | External buffer. This bit should always be set for messages sent to an external ADC. 0 Command is sent to an internal command buffer. 1 Command is sent to an external command buffer.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## Table 19-40. On-Chip ADC Field Descriptions: External Device Operation (continued)

| Bits   | Name                     | Description                                                                                                                                                                                                                                                                                                                                                                                         |
|--------|--------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 6      | BN                       | Refer to Section , ' Conversion Command Message Format for On-Chip ADC Operation.'                                                                                                                                                                                                                                                                                                                  |
| 7-31   | OFF_CHIP_ COMMAND [0:24] | OFF-CHIP COMMAND Field. The OFF_CHIP_COMMAND field can be anything decodable by the external device. It is 25 bits long and it is transferred together with the BN bit to the external device when the CFIFO is triggered. Refer to Section , ' Conversion Command Message Format for On-Chip ADC Operation,' for a description of the command message used when interfacing with the on-chip ADCs. |

## Result Message Format for External Device Operation

Data is returned from the ADCs in the form of result messages. A result message is composed of an RFIFO header and an ADC result. The FIFO control unit decodes the information contained in the RFIFO header and  sends  the  contents  of  the  ADC  result  to  the  appropriate  RFIFO.  Only  data  stored  on  the ADC\_RESULT field is stored in the RFIFOs/result queues. The ADC result of any received message with a null data message tag will be ignored. The format of a result message returned from the external device is shown in Figure 19-32. It is 26 bits long, and is composed of a MESSAGE\_TAG field, information about the status of the buffers (BUSY fields), and result data. The BUSY fields are needed to inform the eQADC about when it is appropriate to transfer commands to the external command buffers.

<!-- image -->

ADC Result

Figure 19-32. Result Message Format for External Device Operation

Table 19-41. Result Message Format for External Device Operation

| Bits   | Name              | Description                                                                                           |
|--------|-------------------|-------------------------------------------------------------------------------------------------------|
| 6-7    | -                 | Reserved.                                                                                             |
| 8-11   | MESSAGE_TAG [0:3] | MESSAGE_TAG Field. Refer to Section , ' Conversion Command Message Format for On-Chip ADC Operation.' |

Table 19-41. Result Message Format for External Device Operation (continued)

| Bits   | Name              | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|--------|-------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 12-15  | BUSY n [0:1]      | BUSY status. The BUSY fields indicate if the external device can receive more commands. Table 19-42 shows how these two bits are encoded. When an external device cannot accept any more new commands, it must set BUSY n to a value indicating 'Do not send commands' in the returning message. The BUSYfields of values 0b10 and 0b10 can be freely encoded by the external device to allow visibility of the status of the external command buffers for debug. As an example, they could indicate the number of entries in an external command buffer. |
| 16-31  | ADC_RESULT [0:15] | ADC RESULT Field. The result data received from the external device or on-chip ADC. This can be the result of a conversion command,data requested via a read configuration command, or time stamp value. The ADC_RESULTofany incoming message with a null message tag will be ignored. When the MESSAGE_TAG is for an RFIFO, the eQADC extracts the 16-bit ADC_RESULT from the raw message and stores it into the appropriate RFIFO.                                                                                                                      |

## Table 19-42. Command BUFFER n BUSY Status 1

| BUSY n [0:1]   | Meaning                                         |
|----------------|-------------------------------------------------|
| 0b00           | Send available commands-command buffer is empty |
| 0b01           | Send available commands                         |
| 0b10           | Send available commands                         |
| 0b11           | Do not send commands                            |

1 After reset, the eQADC always assumes that the external command buffers are full and cannot receive commands.

## Null Message Format for External Device Operation

Null messages are only transferred through the serial interface to allow results and unsolicited control data, like the status of the external command buffers, to return when there are no more commands pending to transfer. Null messages are only transmitted when serial transmissions from the eQADC SSI are enabled (see ESSIE field in Section 19.3.2.1, 'eQADC Module Configuration Register (EQADC\_MCR),'), and when one of the following conditions apply:

- 1. There are no triggered CFIFOs with commands bound for external command buffers.
- 2. There are triggered CFIFOs with commands bound for external command buffers but the external buffers are full. The eQADC detected returning BUSY n fields indicating 'Do not send commands.'

Figure 19-33  illustrates  the  null  message  send  format.  When  the  eQADC  transfers  a  null  message,  it directly shifts out the 26-bit data content inside the Section 19.3.2.2, 'eQADC Null Message Send Format Register (EQADC\_NMSFR).' The register must be programmed with the null message send format of the external device.

Figure 19-34 illustrates the null message receive format. It has the same fields found in a result message with the exception that the ADC result is not used. Refer to Section , ' Result Message Format for External Device Operation,' for more information. The MESSAGE\_TAG field must be set to the null message tag (0b1000). The eQADC does not store into an RFIFO any incoming message with a null message tag.

<!-- image -->

ADC Result

Figure 19-34. Null Message Receive Format for External Device Operation

Table 19-43. Null Message Receive Format for External Device Operation

| Bits   | Name              | Description                                                                                           |
|--------|-------------------|-------------------------------------------------------------------------------------------------------|
| 6-7    | -                 | Reserved.                                                                                             |
| 8-11   | MESSAGE_TAG[ 0:3] | MESSAGE_TAG field. Refer to Section , ' Conversion Command Message Format for On-Chip ADC Operation.' |
| 12-15  | BUSY n [0:1]      | BUSY status. Refer to Section , ' Result Message Format for External Device Operation.'               |
| 16-31  | -                 | Determined by the external device.                                                                    |

## 19.4.2 Command/Result Queues

The command and result queues are actually part of the eQADC system although they are not hardware implemented inside the eQADC. Instead command and result queues are user-defined queues located in system memory. Each command queue entry is a 32-bit command message.The last entry of a command queue has the EOQ bit asserted to indicate that it is the last entry of the queue. The result queue entry is a 16-bit data item.

See Section 19.1.4, 'Modes of Operation,' for a description of the message formats and their flow in eQADC.

Refer to Section 19.5.5, 'Command Queue and Result Queue Usage,' for examples of how command queues and result queues can be used.

## 19.4.3 eQADC Command FIFOs

## 19.4.3.1 CFIFO Basic Functionality

There are six prioritized CFIFOs located in the eQADC. Each CFIFO is four entries deep, and each CFIFO entry is 32 bits long. A CFIFO serves as a temporary storage location for the command messages stored in the command queues in system memory. When a CFIFO is not full, the eQADC sets the corresponding CFFF bit in Section 19.3.2.8, 'eQADC FIFO and Interrupt Status Registers 0-5 (EQADC\_FISRn).' If CFFE  is  asserted  as  in  Section 19.3.2.7,  'eQADC  Interrupt  and  eDMA  Control  Registers  0-5 (EQADC\_IDCRn),' the eQADC generates requests for more commands from a command queue. An interrupt request, served by the host CPU, is generated when CFFS is negated, and a eDMA request, served by the eDMA, is generated when CFFS is asserted. The host CPU or the eDMA respond to these requests by writing to the Section 19.3.2.4, 'eQADC CFIFO Push Registers 0-5 (EQADC\_CFPRn),' to fill the CFIFO.

## NOTE

Only whole words must be written to EQADC\_CFPR. Writing half-words or bytes to EQADC\_CFPR will still push the whole 32-bit CF\_PUSH field into  the  corresponding  CFIFO,  but  undefined  data  will  fill  the  areas  of CF\_PUSH  that  were  not  specifically  designated  as  target  locations  for writing.

Figure 19-35 describes the important components in the CFIFO. Each CFIFO is implemented as a circular set of registers to avoid the need to move all entries at each push/pop operation. The push next data pointer points to the next available CFIFO location for storing data written into the eQADC command FIFO push register.  The  transfer  next  data  pointer  points  to  the  next  entry  to  be  removed  from  CFIFO n when  it completes a transfer. The CFIFO transfer counter control logic counts the number of entries in the CFIFO and generates eDMA or interrupt requests to fill the CFIFO. TNXTPTR in Section 19.3.2.8, 'eQADC FIFO  and  Interrupt  Status  Registers  0-5  (EQADC\_FISRn),'  indicates  the  index  of  the  entry  that  is currently being addressed by the transfer next data pointer, and CFCTR, in the same register, provides the number of entries stored in the CFIFO.

Using TNXTPTR and CFCTR, the absolute addresses for the entries indicated by the transfer next data pointer and by the push next data pointer can be calculated using the following formulas:

```
Transfer Next Data Pointer Address = CFIFO n _BASE_ADDRESS + TNXTPTR n *4 Push Next Data Pointer Address = CFIFO n _BASE_ADDRESS + [(TNXTPTR n +CFCTR n ) mod CFIFO_DEPTH] * 4
```

## where

- · a mod b returns the remainder of the division of a by b .
- · CFIFO \_BASE\_ADDRESS is the smallest memory mapped address allocated to a CFIFO n n entry.
- · CFIFO\_DEPTH is the number of entries contained in a CFIFO - four in this implementation.

When  CFS n in Section 19.3.2.11,  'eQADC  CFIFO  Status  Register  (EQADC\_CFSR),'  is  in  the TRIGGERED state, the eQADC generates the proper control signals for the transfer of the entry pointed by transfer next data pointer. CFUF n in Section 19.3.2.8, 'eQADC FIFO and Interrupt Status Registers 0-5 (EQADC\_FISRn),' is set when a CFIFO n underflow event occurs. A CFIFO underflow occurs when the CFIFO is in the TRIGGERED state and it becomes empty. No commands will be transferred from an underflowing CFIFO, nor will command transfers from lower priority CFIFOs be blocked. CFIFO n is empty when the transfer next data pointer n equals the push next data pointer n and CFCTR  is 0. CFIFO n n is full when the transfer next data pointer n equals the push next data pointer n and CFCTR  is not 0. n

When the eQADC completes the transfer of an entry from CFIFO n : the transferred entry is popped from CFIFO , the CFIFO counter CFCTR in the Section 19.3.2.8, 'eQADC FIFO and Interrupt Status Registers n 0-5 (EQADC\_FISRn),' is decremented by 1, and transfer next data pointer n is  incremented by 1 (or wrapped around) to point to the next entry in the CFIFO. The transfer of entries bound for the on-chip ADCs is considered completed when they are stored in the appropriate ADC command buffer. The transfer of entries bound for the external device is considered completed when the serial transmission of the entry is completed.

When the EQADC\_CFPR  is written and CFIFO n n is not full, the CFIFO counter CFCTR n is incremented by 1, and the push next data pointer n then is incremented by 1 (or wrapped around) to point to the next entry in the CFIFO.

When the EQADC\_CFPR  is written but CFIFO n n is full, the eQADC will not increment the counter value and will not overwrite any entry in CFIFO n .

<!-- image -->

All CFIFO entries are memory mapped and the entries addressed by these pointers can have their absolute addresses calculated using TNXTPTR and CFCTR. *

Figure 19-35. CFIFO Diagram

The detailed behavior of the push next data pointer and transfer next data pointer is described in the example shown in Figure 19-36 where a CFIFO with 16 entries is shown for clarity of explanation, the actual hardware implementation has only four entries. In this example, CFIFO n with 16 entries is shown in sequence after pushing and transferring entries.

## Functional Description

Figure 19-36. CFIFO Entry Pointer Example

<!-- image -->

## 19.4.3.2 CFIFO Prioritization and Command Transfer

The CFIFO priority is fixed according to the CFIFO number. A CFIFO with a smaller number has a higher priority. When commands of distinct CFIFOs are bound for the same destination (the same on-chip ADC), the  higher  priority  CFIFO  is  always  served  first.  A  triggered,  not-underflowing  CFIFO  will  start  the transfer of its commands when the following occur:

- · Its commands are bound for an internal command buffer that is not full, and it is the highest priority triggered CFIFO sending commands to that buffer.

## Enhanced Queued Analog-to-Digital Converter (eQADC)

- · Its commands are bound for an external command buffer that is not full, and it is the highest priority triggered CFIFO sending commands to an external buffer that is not full.

A  triggered  CFIFO  with  commands  bound  for  a  certain  command  buffer  consecutively  transfers  its commands to the buffer until one of the following occurs:

- · An asserted end of queue bit is reached.
- · An asserted pause bit is encountered and the CFIFO is configured for edge trigger mode.
- · CFIFO is configured for level trigger mode and a closed gate is detected.
- · In case its commands are bound for an internal command buffer, a higher priority CFIFO that uses the same internal buffer is triggered.
- · In case its commands are bound for an external command buffer, a higher priority CFIFO that uses an external buffer is triggered.

The  prioritization  logic  of  the  eQADC,  depicted  in  Figure 19-37,  is  composed  of  three  independent submodules:  one  that  prioritizes  CFIFOs  with  commands  bound  for  ADC0,  another  that  prioritizes CFIFOs with commands for ADC1, and a last one that prioritizes CFIFOs with commands for external command buffer 2 and buffer 3. As these three submodules are independent, simultaneous commands to ADC0, to ADC1, and to eQADC SSI transmit buffer are allowed. The hardware identifies the destination of a command by decoding the EB and BN bits in the command message (see Section 19.4.1.2, 'Message Format in eQADC,' for details).

## NOTE

Triggered but empty CFIFOs, underflowing CFIFOs, are not considered for prioritization.  No  data  from  these  CFIFOs  will  be  sent  to  either  of  the on-chip ADCs or to either of the external command buffers, nor will they stop lower priority CFIFOs from transferring commands.

Whenever  ADC0  is  able  to receive new  commands,  the  prioritization submodule  selects the highest-priority triggered CFIFO with a command bound for ADC0, and sends it to the ADC. In case ADC0 is able to receive new entries but there are no triggered CFIFOs with commands bound for it, nothing is sent. The submodule prioritizing ADC1 usage behaves in the same way.

When the  eQADC SSI is  enabled  and  ready  to  start  serial  transmissions,  the  submodule  prioritizing eQADC SSI usage writes command or null messages into the eQADC SSI transmit buffer, data written to the eQADC SSI transmit buffer is subsequently transmitted to the external device through the eQADC SSI link. The submodule writes commands to the eQADC SSI transmit buffer when there are triggered CFIFOs with commands bound for not-full external command buffers. The command written to the transmit buffer belongs to the highest priority CFIFO sending commands to an external buffer that is not full. This implies that  a  lower  priority  CFIFO  can  have  its  commands  sent  if  a  higher  priority  CFIFO  cannot  send  its commands due to a full command buffer. The submodule writes null messages to the eQADC SSI transmit buffer when there are no triggered CFIFOs with commands bound for external command buffers, or when there are triggered CFIFOs with commands bound for external buffers but the external buffers are full. The eQADC monitors the status of the external buffers by decoding the BUSY fields of the incoming result messages  from  the  external  device  (see  Section ,  ' Result  Message  Format  for  External  Device Operation,' for details).

## NOTE

When  a  lower  priority  CFIFO  is  served  first  because  a  higher  priority CFIFO cannot send its commands due to a full external command buffer, there is a possibility that command transfers from the lower priority CFIFO will  be  interrupted  and  the  CFIFO  will  become  non-coherent,  when  the higher priority CFIFO again becomes ready to send commands. Whether the lower priority CFIFO becomes non-coherent or not depends on the rate at which commands on the external ADCs are executed, on the rate at which commands are transmitted  to  the  external  command  buffers,  and  on  the depth of those buffers.

Once a serial transmission is started, the submodule monitors triggered CFIFOs and manages the abort of serial transmissions. In case a null message is being transmitted, the serial transmission is aborted when all of the following conditions are met:

- · A not-underflowing CFIFO in the TRIGGERED state has commands bound for an external command buffer that is not full, and it is the highest priority CFIFO sending commands to an external buffer that is not full.
- · The ABORT\_ST bit of the command to be transmitted is asserted.
- · The 26th bit of the currently transmitting null message has not being shifted out.

The command from the CFIFO is then written into eQADC SSI transmit buffer, allowing for a new serial transmission to initiate.

In case a command is being transmitted, the serial transmission is aborted when all following conditions are met:

- · CFIFO0 is in the TRIGGERED state, is not underflowing, and its current command is bound for an external command buffer that is not full.
- · The ABORT\_ST bit of the command to be transmitted is asserted.
- · The 26th bit of the currently transmitting command has not being shifted out.

The command from CFIFO0 is then written into eQADC SSI transmit buffer, allowing for a new serial transmission to initiate.

## NOTE

The aborted command is not popped from the preempted CFIFO and will be retransmitted  as  soon  as  its  CFIFO  becomes  the  highest  priority  CFIFO sending commands to an unfilled external command buffer.

After a serial transmission is completed, the eQADC prioritizes the CFIFOs and schedules a command or a null message to be sent in the next serial transmission. After the data for the next transmission has been defined and scheduled, the eQADC can, under certain conditions, stretch the SDS negation time in order to allow the schedule of new data for that transmission. This occurs when the eQADC acknowledges that the status of a higher-priority CFIFO has changed to the TRIGGERED state and attempts to schedule that CFIFO command before SDS is asserted.  Only  commands  of  CFIFOs  that  have  the  ABORT\_ST  bit asserted can be scheduled in this manner. Under such conditions:

- 1. A CFIFO0 command is scheduled for the next transmission independently of the type of data that was previously scheduled. The time during which SDS is negated is stretched in order to allow the eQADC to load the CFIFO0 command and start its transmission.

- 2. CFIFO1-5 commands are only scheduled for the next transmission if the previously scheduled data was a null message.  The time during which SDS is negated is stretched in order to allow the eQADC to load that command and start its transmission. However, if the previously scheduled data was a command, no rescheduling occurs and the next transmission starts without delays.

If a CFIFO becomes triggered while SDS is negated, but the eQADC only attempts to reschedule that CFIFO command after SDS is asserted, then the current transmission  is  aborted  depending  on  if  the conditions for that are met or not.

Figure 19-37. CFIFO Prioritization Logic

<!-- image -->

## 19.4.3.3 External Trigger from eTPU or eMIOS Channels

The six eQADC external trigger inputs can be connected to either an external pin, an eTPU channel, or an eMIOS channel. The input source for each eQADC external trigger is individually specified in the eQADC trigger input select register (SIU\_ETISR) in the SIU block.

The eQADC trigger numbers specified by SIU\_ETISR[TSEL(0-5)] correspond to CFIFO numbers 0-5. To calculate the CFIFO number that each trigger is connected to, divide the eDMA channel number by 2.

A  complete  description  of  the  eTPU  and  eMIOS  trigger  function  and  configuration  is  found  in Section 6.4.5.1, 'eQADC External Trigger Input Multiplexing.'

## 19.4.3.4 External Trigger Event Detection

The  digital  filter  length  field  in  Section 19.3.2.3,  'eQADC  External  Trigger  Digital  Filter  Register (EQADC\_ETDFR),' specifies the minimum number of system clocks that the external trigger signals 0 and 1 must be held at a logic level to be recognized as valid. All ETRIG signals are filtered. A counter for each queue trigger is implemented to detect a transition between logic levels. The counter counts at the system clock rate. The corresponding counter is cleared and restarted each time the signal transitions between logic levels. When the corresponding counter matches the value specified by the digital filter length field in Section 19.3.2.3, 'eQADC External Trigger Digital Filter Register (EQADC\_ETDFR),' the eQADC considers the ETRIG logic level to be valid and passes that new logic level to the rest of the eQADC.

The filter is only for filtering the ETRIG signal. Logic after the filter checks for transitions between filtered values, such as for detecting the transition from a filtered logic level zero to a filtered logic level one in rising edge external trigger mode. The eQADC can detect rising edge, falling edge, or level gated external triggers.  The  digital  filter  will  always  be  active  independently  of  the  status  of  the  MODE n field  in Section 19.3.2.6,  'eQADC  CFIFO  Control  Registers  0-5  (EQADC\_CFCRn),'  but  the  edge,  level detection logic is only active when MODE n is set to a value different from disabled, and in case MODE n is set to single scan mode, when the SSS bit is asserted. Note that the time necessary for a external trigger event to result into a CFIFO status change is not solely determined by the DFL field in the Section 19.3.2.3, 'eQADC External Trigger Digital Filter Register (EQADC\_ETDFR).' After being synchronized to the system clock and filtered, a trigger event is checked against the CFIFO trigger mode. Only then, after a valid trigger event is detected, the eQADC accordingly changes the CFIFO status. Refer to Figure 19-38 for an example.

Figure 19-38. ETRIG Event Propagation Example

<!-- image -->

## 19.4.3.5 CFIFO Scan Trigger Modes

The eQADC supports two different scan modes, single-scan and continuous-scan. Refer to Table 19-44 for a summary of these two scan modes. When a CFIFO is triggered, the eQADC scan mode determines whether the eQADC will stop command transfers from a CFIFO, and wait for software intervention to rearm the CFIFO to detect new trigger events, upon detection of an asserted EOQ bit in the last transfer. Refer to Section 19.4.1.2, 'Message Format in eQADC,' for details about command formats.

CFIFOs can be configured  in  single-scan  or  continuous-scan  mode.  When  a  CFIFO  is  configured  in single-scan mode, the eQADC scans the command queue one time. The eQADC stops future command transfers from the triggered CFIFO after detecting the EOQ bit set in the last transfer. After a EOQ bit is detected, software involvement is required to rearm the CFIFO so that it can detect new trigger events.

## Enhanced Queued Analog-to-Digital Converter (eQADC)

When a CFIFO is configured for continuous-scan mode, no software involvement is necessary to rearm the CFIFO to detect new trigger events after an asserted EOQ is detected. In continuous-scan mode the whole command queue is scanned multiple times.

The eQADC also supports different triggering mechanisms for each scan mode. The eQADC will not transfer  commands from a CFIFO until the CFIFO is triggered. The combination of scan modes and triggering mechanisms allows the support of different requirements for scanning input channels. The scan mode  and  trigger  mechanism  are  configured  by  programming  the  MODE n field  in  Section 19.3.2.6, 'eQADC CFIFO Control Registers 0-5 (EQADC\_CFCRn).'

Enabled CFIFOs can be triggered by software or external trigger events. The elapsed time from detecting a  trigger  to  transferring  a  command  is  a  function  of  clock  frequency,  trigger  synchronization,  trigger filtering, programmable trigger events, command transfer, CFIFO prioritization, ADC availability, etc. Fast and predictable transfers can be achieved by ensuring that the CFIFO is not underflowing and that the target ADC can accept commands when the CFIFO is triggered.

## 19.4.3.5.1 Disabled Mode

The MODE  field in Section 19.3.2.6, 'eQADC CFIFO Control Registers 0-5 (EQADC\_CFCRn),' for n all of the CFIFOs can be changed from any other mode to disabled at any time. No trigger event can initiate command transfers from a CFIFO which has its MODE field programmed to disabled.

## NOTE

If MODE  is not disabled, it must not be changed to any other mode besides n disabled. If MODE n is disabled and the CFIFO status is IDLE, MODE n can be changed to any other mode.

## If MODE  is changed to disabled: n

- · The CFIFO execution status will change to IDLE. The timing of this change depends on whether a command is being transferred or not:
- - When no command transfer is in progress, the eQADC switches the CFIFO to IDLE status immediately.
- - When a command transfer to an on-chip ADC is in progress, the eQADC will complete the transfer, update TC\_CF, and switch CFIFO status to IDLE. Command transfers to the internal ADCs are considered completed when a command is written to the relevant buffer.
- - When a command transfer to an external command buffer is in progress, the eQADC will abort the transfer and switch CFIFO status to IDLE. If the eQADC cannot abort the transfer, that is when the 26th bit of the serial message has being already shifted out, the eQADC will complete the transfer, update TC\_CF and then switch CFIFO status to IDLE.
- · The CFIFOs are not invalidated automatically. The CFIFO still can be invalidated by writing a 1 to the CFINV n bit (see Section 19.3.2.6). Certify that CFS has changed to IDLE before setting CFINV . n
- · The TC\_CF  value also is not reset automatically, but it can be reset by writing 0 to it. n
- · The EQADC\_FISRn[SSS] bit (see Section 19.3.2.8) is negated. The SSS bit can be set even if a 1 is written to the EQADC\_CFCR[SSE] bit (see Section 19.3.2.6) in the same write that the MODE n field is changed to a value other than disabled.
- · The trigger detection hardware is reset. If MODE n is changed from disabled to an edge trigger mode, a new edge, matching that edge trigger mode, is needed to trigger the command transfers from the CFIFO.

## NOTE

CFIFO  fill  requests,  which  generated  when  CFFF  is  asserted,  are  not automatically  halted  when  MODE n is  changed  to  disabled.  CFIFO  fill requests will still be generated until EQADC\_IDCRn[CFFE] bit is cleared (see Section 19.3.2.7).

## 19.4.3.5.2 Single-Scan Mode

In single-scan mode, a single pass through a sequence of command messages in the user-defined command queue is performed.

In  single-scan  software  trigger  mode,  the  CFIFO  is  triggered  by  an  asserted  single-scan  status  bit, EQADC\_FISRn[SSS] (see Section 19.3.2.8). The SSS bit is set by writing 1 to the single-scan enable bit, EQADC\_CFCRn[SSE] (see Section 19.3.2.6).

In single-scan edge- or level-trigger mode, the respective triggers are only detected when the SSS bit is asserted. When the SSS bit is negated, all trigger events for that CFIFO are ignored. Writing a 1 to the SSE bit can be done during the same write cycle that the CFIFO operation mode is configured.

Only  the  eQADC  can  clear  the  SSS  bit.  Once  SSS  is  asserted,  it  remains  asserted  until  the  eQADC completes  the  command  queue  scan,  or  the  CFIFO  operation  mode,  EQADC\_CFCRn[MODE n ]  (see Section 19.3.2.6) is changed to disabled. The SSS n bit will be negated while MODE n is disabled.

## Single-Scan Software Trigger

When single-scan software trigger mode is selected, the CFIFO is triggered by an asserted SSS bit. The SSS bit is asserted by writing 1 to the SSE bit. Writing to SSE while SSS is already asserted will not have any effect on the state of the SSS bit, nor will it cause a trigger overrun event.

The CFIFO commands start to be transferred when the CFIFO becomes the highest priority CFIFO using an available on-chip ADC or an external command buffer that is not full. When an asserted EOQ bit is encountered, the eQADC will clear the SSS bit. Setting the SSS bit is required for the eQADC to start the next scan of the queue.

The pause bit has no effect in single-scan software trigger mode.

## Single-Scan Edge Trigger

When SSS is asserted and an edge triggered mode is selected for a CFIFO, an appropriate edge on the associated trigger signal causes the CFIFO to become triggered. For example, if rising-edge trigger mode is selected, the CFIFO becomes triggered when a rising edge is sensed on the trigger signal. The CFIFO commands start to be transferred when the CFIFO becomes the highest priority CFIFO using an available on-chip ADC, or an external command buffer that is not full.

When an asserted EOQ bit is encountered, the eQADC clears SSS and stops command transfers from the CFIFO. An asserted SSS bit and a subsequent edge trigger event are required to start the next scan for the CFIFO. When an asserted pause bit is encountered, the eQADC stops command transfers from the CFIFO, but SSS remains set. Another edge trigger event is required for command transfers to continue. A trigger overrun happens when the CFIFO is in a TRIGGERED state and an edge trigger event is detected.

## Single-Scan Level Trigger

When SSS is asserted and a level gated trigger mode is selected, the input level on the associated trigger signal puts the CFIFO in a TRIGGERED state. When the CFIFO is set to high-level gated trigger mode, a high level signal opens the gate, and a low level closes the gate. When the CFIFO is set to low-level gated trigger mode, a low level signal opens the gate, and a high level closes the gate. If the corresponding level is already present, setting the SSS bit triggers the CFIFO. The CFIFO commands start to be transferred

when the CFIFO becomes the highest priority CFIFO using an available on-chip ADC or an external command buffer that is not full.

The eQADC clears the SSS bit and stops transferring commands from a triggered CFIFO when an asserted EOQ bit is encountered or when CFIFO status changes from triggered due to the detection of a closed gate. If a closed gate is detected while no command transfers are taking place and the CFIFO status is triggered, the CFIFO status is immediately changed to IDLE, the SSS bit is negated, and the PF flag is asserted. If a closed gate is detected during the serial transmission of a command to the external device, it will have no effect  on  the  CFIFO  status  until  the  transmission  completes.  Once  the  transmission  is  completed,  the TC\_CF counter is updated, the SSS bit is negated, the PF flag is asserted, and the CFIFO status is changed to IDLE. An asserted SSS bit and a level trigger are required to restart the CFIFO. Command transfers will restart from the point they have stopped.

If the gate closes and opens during the same serial transmission of a command to the external device, it will have no effect on the CFIFO status or on the PF flag, but the TORF flag will become asserted as was exemplified in Figure 19-40. Therefore, closing the gate for a period less than a serial transmission time interval does not guarantee that the closure will affect command transfers from a CFIFO.

The pause bit has no effect in single-scan level-trigger mode.

## 19.4.3.5.3 Continuous-Scan Mode

In  continuous-scan  mode,  multiple  passes  looping  through  a  sequence  of  command  messages  in  a command  queue  are  executed.  When  a  CFIFO  is  programmed  for  a  continuous-scan  mode,  the EQADC\_CFCRn[SSE] (see Section 19.3.2.6) does not have any effect.

## Continuous-Scan Software Trigger

When  a  CFIFO  is  programmed  to  continuous-scan  software  trigger  mode,  the  CFIFO  is  triggered immediately. The CFIFO commands start to be transferred when the CFIFO becomes the highest priority CFIFO using an available on-chip ADC or an external command buffer that is not full. When a CFIFO is programmed to run in continuous-scan software trigger mode, the eQADC will not halt transfers from the CFIFO until the CFIFO operation mode is modified to disabled or a higher priority CFIFO preempts it. Although command transfers will not stop upon detection of an asserted EOQ bit, the EOQF is set and, if enabled, an EOQ interrupt request is generated.

The pause bit has no effect in continuous-scan software trigger mode.

## Continuous-Scan Edge Trigger

When rising, falling, or either edge trigger mode is selected for a CFIFO, a corresponding edge on the associated ETRIG signal places the CFIFO in a TRIGGERED state. The CFIFO commands start to be transferred when the CFIFO becomes the highest priority CFIFO using an available on-chip ADC or an external command buffer that is not full.

When an EOQ or a pause is encountered, the eQADC halts command transfers from the CFIFO and, if enabled, the appropriate interrupt requests are generated. Another edge trigger event is required to resume command transfers but no software involvement is required to rearm the CFIFO in order to detect such event.

A trigger overrun happens when the CFIFO is already in a TRIGGERED state and a new edge trigger event is detected.

## Continuous-Scan Level Trigger

When high or low level gated trigger mode is selected, the input level on the associated trigger signal places the CFIFO in a TRIGGERED state. When high-level gated trigger is selected, a high-level signal opens the gate, and a low level closes the gate. The CFIFO commands start to be transferred when the

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Freescale Semiconductor

CFIFO becomes the highest priority CFIFO using an available on-chip ADC or an external buffer that is not full. Although command transfers will not stop upon detection of an asserted EOQ bit at the end of a command transfer, the EOQF is asserted and, if enabled, an EOQ interrupt request is generated.

The eQADC stops transferring commands from a triggered CFIFO when CFIFO status changes from triggered due to the detection of a closed gate. If a closed gate is detected while no command transfers are taking place and the CFIFO status is TRIGGERED, the CFIFO status is immediately changed to waiting for  trigger  and  the  PF  flag  is  asserted.  If  a  closed  gate  is  detected  during  the  serial  transmission  of  a command  to  the  external  device,  it  will  have  no  effect  on  the  CFIFO  status  until  the  transmission completes. Once the transmission is completed, the TC\_CF counter is updated, the PF flag is asserted, and the CFIFO status is changed to waiting for trigger. Command transfers will restart as the gate opens.

If the gate closes and opens during the same serial transmission of a command to the external device, it will have no effect on the CFIFO status or on the PF flag, but the TORF flag will become asserted as was exemplified in Figure 19-40. Therefore, closing the gate for a period less than a serial transmission time interval does not guarantee that the closure will affect command transfers from a CFIFO.

The pause bit has no effect in continuous-scan level-trigger mode.

## 19.4.3.5.4 CFIFO Scan Trigger Mode Start/Stop Summary

Table 19-44 summarizes the start and stop conditions of command transfers from CFIFOs for all of the single-scan and continuous-scan trigger modes.

Table 19-44. CFIFO Scan Trigger Mode-Command Transfer Start/Stop Summary

| Trigger Mode             | Requires Asserted SSS to Recognize Trigger Events?   | Command Transfer Start/Restart Condition                          | Stop on asserted EOQ bit 1 ?   | Stop on asserted Pause bit 2 ?   | Other CommandTransfer Stop Condition 3 4                                                                                        |
|--------------------------|------------------------------------------------------|-------------------------------------------------------------------|--------------------------------|----------------------------------|---------------------------------------------------------------------------------------------------------------------------------|
| Single Scan Software     | Not Applicable                                       | Asserted SSS bit.                                                 | Yes                            | No                               | None.                                                                                                                           |
| Single Scan Edge         | Yes                                                  | A corresponding edge occurs when the SSS bit is asserted.         | Yes                            | Yes                              | None.                                                                                                                           |
| Single Scan Level        | Yes                                                  | Gate is opened when the SSS bit is asserted.                      | Yes                            | No                               | The eQADC also stops transfers from the CFIFO when CFIFO status changes from triggered due to the detection of a closed gate. 5 |
| Continuous Scan Software | No                                                   | CFIFO starts automatically after being configured into this mode. | No                             | No                               | None.                                                                                                                           |
| Continuous Scan Edge     | No                                                   | A corresponding edge occurs.                                      | Yes                            | Yes                              | None.                                                                                                                           |
| Continuous Scan Level    | No                                                   | Gate is opened.                                                   | No                             | No                               | The eQADC also stops transfers from the CFIFO when CFIFO status changes from triggered due to the detection of a closed gate. 5 |

- 1 Refer to Section 19.4.3.6.2, 'Command Queue Completion Status ,' for more information on EOQ.
- 2 Refer to Section 19.4.3.6.3, 'Pause Status,' for more information on pause.
- 3 The eQADC always stops command transfers from a CFIFO when the CFIFO operation mode is disabled.
- 4 The eQADC always stops command transfers from a CFIFO when a higher priority CFIFO is triggered. Refer to Section 19.4.3.2, 'CFIFO Prioritization and Command Transfer,' for information on CFIFO priority.
- 5 If a closed gate is detected while no command transfers are taking place, it will have immediate effect on the CFIFO status. If a closed gate is detected during the serial transmission of a command to the external device, it will have no effect on the CFIFO status until the transmission completes.

## 19.4.3.6 CFIFO and Trigger Status

## 19.4.3.6.1 CFIFO Operation Status

Each CFIFO has its own CFIFO status field. CFIFO status (CFS) can be read from EQADC\_CFSSR (see Section 19.3.2.11,  'eQADC  CFIFO  Status  Register  (EQADC\_CFSR).'  Figure 19-39  and  Table 19-45 indicate  the  CFIFO  status  switching  condition.  Refer  to  Table 19-18  for  the  meaning  of  each  CFIFO operation status. The last CFIFO to transfer a command to an on-chip ADC can be read from the LCFT n ( n =0,1) fields (see Section 19.3.2.10, 'eQADC CFIFO Status Snapshot Registers 0-2 (EQADC\_CFSSRn).' The last CFIFO to transfer a command to a specific external command buffer can be  identified  by  reading  the  EQADC\_CFSSR n [LCFTSSI]  and  EQADC\_CFSSR [ENI]  fields  (see n Section 19.3.2.10, 'eQADC CFIFO Status Snapshot Registers 0-2 (EQADC\_CFSSRn).'

Figure 19-39. State Machine of CFIFO Status

<!-- image -->

Table 19-45. Command FIFO Status Switching Condition

|   No. | From Current CFIFO Status (CFS)   | To New CFIFO Status (CFS)   | Status Switching Condition                                                                                                                                                                                                                                            |
|-------|-----------------------------------|-----------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|     1 | IDLE (00)                         | IDLE (0b00)                 | GLYPH<127> CFIFO mode is programmed to disabled, OR GLYPH<127> CFIFO mode is programmed to single-scan edge or level trigger mode and SSS is negated.                                                                                                                 |
|     2 | IDLE (00)                         | WAITING FOR TRIGGER (0b10)  | GLYPH<127> CFIFO mode is programmed to continuous-scan edge or level trigger mode, OR GLYPH<127> CFIFO mode is programmed to single-scan edge or level trigger mode and SSS is asserted, OR GLYPH<127> CFIFO mode is programmed to single-scan software trigger mode. |
|     3 | IDLE (00)                         | TRIGGERED (0b11)            | GLYPH<127> CFIFO mode is programmed to continuous-scan software trigger mode                                                                                                                                                                                          |
|     4 | WAITING FOR TRIGGER (10)          | IDLE (0b00)                 | GLYPH<127> CFIFO mode is modified to disabled mode.                                                                                                                                                                                                                   |
|     5 | WAITING FOR TRIGGER (10)          | WAITING FOR TRIGGER (0b10)  | GLYPH<127> No trigger occurred.                                                                                                                                                                                                                                       |
|     6 | WAITING FOR TRIGGER (10)          | TRIGGERED (0b11)            | GLYPH<127> Appropriate edge or level trigger occurred, OR GLYPH<127> CFIFO mode is programmed to single-scan software trigger mode and SSS bit is asserted.                                                                                                           |

Table 19-45. Command FIFO Status Switching Condition (continued)

|   No. | From Current CFIFO Status (CFS)   | To New CFIFO Status (CFS)   | Status Switching Condition                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
|-------|-----------------------------------|-----------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|     7 | TRIGGERED (11)                    | IDLE (0b00)                 | GLYPH<127> CFIFO in single-scan mode, eQADC detects the EOQ bit asserted at end of command transfer, and CFIFO mode is not modified to disabled, OR GLYPH<127> CFIFO, in single-scan level trigger mode, and the gate closes while no commands are being transferred from the CFIFO, and CFIFO mode is not modified to disabled, OR GLYPH<127> CFIFO, in single-scan level trigger mode, and eQADC detects a closed gated at end of command transfer, and CFIFO mode is not modified to disabled, OR GLYPH<127> CFIFO mode is modified to disabled mode and CFIFO was not transferring commands. GLYPH<127> CFIFO mode is modified to disabled mode while CFIFO was transferring commands, and CFIFO completes or aborts the transfer.                          |
|     8 | TRIGGERED (11)                    | WAITING FOR TRIGGER (0b10)  | GLYPH<127> CFIFO in single or continuous-scan edge trigger mode, eQADC detects the pause bit asserted at the end of command transfer, the EOQ bit in the same command is negated, and CFIFO mode is not modified to disabled, OR GLYPH<127> CFIFO in continuous-scan edge trigger mode, eQADC detects the EOQ bit asserted at the end of command transfer, and CFIFO mode is not modified to disabled, OR GLYPH<127> CFIFO, in continuous-scan level trigger mode, and the gate closes while no commands are being transferred from the CFIFO, and CFIFO mode is not modified to disabled, OR GLYPH<127> CFIFO, in continuous-scan level trigger mode, and eQADC detects a closed gated at end of command transfer, and CFIFO mode is not modified to disabled. |
|     9 | TRIGGERED (11)                    | TRIGGERED (0b11)            | GLYPH<127> No event to switch to IDLE or WAITING FOR TRIGGER status has happened.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |

## 19.4.3.6.2 Command Queue Completion Status

The  end  of  queue  flag,  EQADC\_FISRn[EOQF]  (see  Section  19.3.2.8)  is  asserted  when  the  eQADC completes the transfer of a CFIFO entry with an asserted EOQ bit. Software sets the EOQ bit in the last command message of a user-defined command queue to indicate that this entry is the end of the queue. See Section 19.4.1.2,  'Message  Format  in  eQADC,'  for  information  on  command  message  formats.  The transfer  of  entries  bound  for  the  on-chip  ADCs  is  considered  completed  when  they  are  stored  in  the appropriate command buffer. The transfer of entries bound for the external device is considered completed when the serial transmission of the entry is completed.

The command with a EOQ bit asserted is valid and will be transferred. When EQADC\_CFCRn[EOQIE] (see Section 19.3.2.6) and EQADC\_FISRn[EOQF] are asserted, the eQADC will generate an end of queue interrupt request.

In single-scan modes, command transfers from the corresponding CFIFO will cease when the eQADC completes the transfer of a entry with an asserted EOQ. Software involvement is required to rearm the CFIFO so that it can detect new trigger events.

## NOTE

An asserted EOQF n only implies that the eQADC has finished transferring a command with an asserted EOQ bit from CFIFO n . It does not imply that result  data  for  the  current  command  and  for  all  previously  transferred commands has been returned to the appropriate RFIFO.

## 19.4.3.6.3 Pause Status

In edge trigger mode, when the eQADC completes the transfer of a CFIFO entry with an asserted pause bit, the eQADC will stop future command transfers from the CFIFO and set EQADC\_FISRn[PF] (see Section 19.3.2.8). Refer to Section 19.4.1.2, 'Message Format in eQADC,' for information on command message formats. The eQADC ignores the pause bit in command messages in any software level trigger mode.  The  eQADC  sets  the  PF  flag  upon  detection  of  an  asserted  pause  bit  only  in  single  or continuous-scan edge trigger mode. When the PF flag is set for a CFIFO in single-scan edge trigger mode, the EQADC\_FISRn[SSS] bit will not be cleared (see Section 19.3.2.8).

In level trigger mode, the definition of the PF flag has been redefined. In level trigger mode, when CFIFO n is in TRIGGERED status, PF n is set when the CFIFO status changes from TRIGGERED due to detection of  a  closed  gate.  The  pause  flag  interrupt  routine  can be  used  to  verify  if  the  a  complete  scan  of  the command queue was performed. If a closed gate is detected while no command transfers are taking place, it will have immediate effect on the CFIFO status. If a closed gate is detected during the serial transmission of a command to the external device, it will have no effect on the CFIFO status until the transmission completes.

When EQADC\_CFCR[PIE] (see Section 19.3.2.6) and EQADC\_FISRn[PF] are asserted, the eQADC will generate a pause interrupt request.

## NOTE

In edge trigger mode, an asserted PF n only implies that the eQADC finished transferring a command with an asserted pause bit from CFIFO n . It does not imply  that  result  data  for  the  current  command  and  for  all  previously transferred commands has been returned to the appropriate RFIFO.

## NOTE

In software or level trigger mode, when the eQADC completes the transfer of an entry from CFIFO n with an asserted pause bit, PF n will not be set and command transfers will continues without pausing.

## 19.4.3.6.4 Trigger Overrun Status

When a CFIFO is configured for edge- or level-trigger mode and is in a TRIGGERED state, an additional trigger  occurring  for  the  same  CFIFO  results  in  a  trigger  overrun.  The  trigger  overrun  bit  for  the corresponding CFIFO  will  be  set (EQADC\_FISRn[TORF ]  =  1,  see  Section  19.3.2.8).  When n EQADC\_CFCRn[TORIE] (see Section 19.3.2.6) and EQADC\_FISRn[TORF] are asserted, the eQADC generates a trigger overrun interrupt request.

For CFIFOs configured for level-trigger mode, a trigger overrun event is only detected when the gate closes and reopens during a single serial command transmission as shown in Figure 19-40.

## Enhanced Queued Analog-to-Digital Converter (eQADC)

Command Transmission through eQADC SSI

CFIFO Status

TORF

Command 1

Null Message

Command 2

Triggered

WFT

Triggered

Triggered

WFT

Low Active Level Trigger

If gate closes during a command transmission, it is only recognized when the transmission ends.

1) CFIFO programmed to 'continuous-scan low level gated external trigger mode'.

2) Command 2 has its ABORT\_ST bit negated.

Assumptions:

3) There are no other CFIFOs using the serial interface.

WFT = Waiting for Trigger

Figure 19-40. Trigger Overrun on Level-Trigger Mode CFIFOs

<!-- image -->

## NOTE

The trigger overrun flag will not set for CFIFOs configured for software trigger mode.

## 19.4.3.6.5 Command Sequence Non-Coherency Detection

The eQADC provides a mechanism to indicate if a command sequence has been completely executed without interruptions. A command sequence is defined as a group of consecutive commands bound for the same ADC and it is expected to be executed without interruptions. A command sequence is coherent if its commands  are  executed  in  order  without  interruptions.  Because  commands  are  stored  in  the  ADC's command buffers before being executed in the eQADC, a command sequence is coherent if, while it is transferring commands to an on-chip ADC command buffer, the buffer is only fed with commands from that sequence without ever becoming empty.

A command sequence starts when:

- · A CFIFO in TRIGGERED state transfers its first command to an on-chip ADC.
- · The CFIFO is constantly transferring commands and the previous command sequence ended.
- · The CFIFO resumes command transfers after being interrupted.

And a command sequence ended when:

- · An asserted EOQ bit is detected on the last transferred command.
- · CFIFO is in edge-trigger mode and asserted pause bit is detected on the last transferred command.
- · The ADC to which the next command is bound is different from the ADC to which the last command was transferred.

Figure 19-41 shows examples of how the eQADC would detect command sequences when transferring commands from a CFIFO. The smallest possible command sequence can have a single command as shown in example 3 of Figure 19-41.

| User Command Queue with Two Command Sequences   |
|-------------------------------------------------|
| CF5_ADC1_CM0                                    |
| CF5_ADC1_CM1                                    |
| CF5_ADC1_CM2                                    |
| CF5_ADC1_CM3(Pause=1)                           |
| CF5_ADC1_CM4                                    |
| CF5_ADC1_CM5                                    |
| CF5_ADC1_CM6(EOQ=1)                             |

## Example 1

<!-- image -->

| User Command Queue with Three Command Sequences   |
|---------------------------------------------------|
| CF5_ADC1_CM0                                      |
| CF5_ADC1_CM1                                      |
| CF5_ADC1_CM2                                      |
| CF5_ADC0_CM3                                      |
| CF5_ADC0_CM4                                      |
| CF5_ADC1_CM5                                      |
| CF5_ADC1_CM6(EOQ=1)                               |

## Example 2

User Command Queue with a Seven Command Sequence

| CF5_ADC1_CM0        |
|---------------------|
| CF5_ADC2_CM1        |
| CF5_ADC3_CM2        |
| CF5_ADC1_CM3        |
| CF5_ADC0_CM4        |
| CF5_ADC2_CM5        |
| CF5_ADC1_CM6(EOQ=1) |

Assuming that these commands are transferred by a CFIFO configured for edge trigger mode and the command transfers are never interrupted, the eQADC would check for non-coherency of two command sequences: one formed by commands 0, 1, 2, 3, and the other by commands 4, 5, 6.

Assuming that command transfers from the CFIFO are never interrupted, the eQADC would check for non-coherency of three command sequences. The first being formed by commands 0, 1, 2, the second by commands 3, 4 and the third by commands 5, 6. Note that even when the commands of this queue are transferred through a CFIFO in continuous-scan mode, the first three commands and the last two commands of this command queue would still constitute two distinct command sequences, although they are all bound for the same ADC, because an asserted EOQ ends a command sequence.

The eQADC would check for non-coherency of seven command sequences, all containing a single command, but NCF would never get set.

CF \_ADCa\_CMD  - Command   in CFIFO  bound for ADCa (ADC3 n n n n and ADC4 are external devices associated with external command buffers 2 and 3).

Example 3

## Figure 19-41. Command Sequence Examples

The NCF flag is used to indicate command sequence non-coherency. When the NCF n flag is asserted, it indicates that the command sequence being transferred through CFIFO n became non-coherent. The NCF flag only becomes asserted for CFIFOs in a TRIGGERED state.

A command sequence is non-coherent when, after transferring the first command of a sequence from a CFIFO to a buffer, it cannot successively send all the other commands of the sequence before any of the following conditions are true:

- · The CFIFO through which commands are being transferred is pre-empted by a higher priority CFIFO which sends commands to the same ADC. The NCF flag becomes asserted immediately after the first command transfer from the pre-empting CFIFO, that is the higher priority CFIFO, to the ADC in use is completed. See Figure 19-43.
- · The external command buffer in use becomes empty. (Only the fullness of external buffers is monitored because the fill rate for internal ADC buffers is many times faster than the drain rate, and each has a dedicated priority engine.) This case happens when different CFIFOs attempt to use different external command buffers and the higher priority CFIFO bars the lower priority one from

sending new commands to its buffer-see Figure 19-44. An external command buffer is considered empty when the corresponding BUSY field in the last result message received from external device is encoded as 'Send available commands - buffer is empty'. Refer to Section , ' Result Message Format for External Device Operation.' The NCF flag becomes asserted immediately after the eQADC detects that the external buffer in use becomes empty.

## NOTE

After the transfer of a command sequence to an external command buffer starts,  the  eQADC  ignores,  for  non-coherency  detection  purposes,  the BUSY fields captured at the end of the first serial transmission. Thereafter, all BUSY fields captured at the end of consecutive serial transmissions are used to check the fullness of that external command buffer. This is done because the eQADC only updates its external ADC command buffer status record when it receives a serial message, resulting that the record kept by the  eQADC  is  always  outdated  by,  at  least,  the  length  of  one  serial transmission. This prevents a CFIFO from immediately becoming non-coherent when it starts transferring  commands to an empty external command buffer. Refer to Figure 19-42 for an example.

<!-- image -->

Assumptions:

1) The CFIFO starts sending commands to an external command buffer when triggered.

- 2) Execution of a command on the external device takes longer than the time to complete three serial transmissions.

Figure 19-42. External Command Buffer Status Detection at Command Sequence Transfer Start

Table 19-46. External Buffer Status

| Capture Point at eQADC   | Buffer Status at External Device   | Buffer Status as Captured by the eQADC   | Used for NCF detectionon the eQADC?   |
|--------------------------|------------------------------------|------------------------------------------|---------------------------------------|
| (a)                      | EMPTY                              | EMPTY                                    | Don't care                            |
| (b)                      | 1 ENTRY                            | EMPTY                                    | No                                    |
| (c)                      | 2 ENTRY                            | 1 ENTRY                                  | Yes                                   |

Once a command sequence starts to be transferred, the eQADC will check for the command sequence coherency until the command sequence ends or until one of the conditions below becomes true:

- · The command sequence became non-coherent.
- · The CFIFO status changed from the TRIGGERED state.
- · The CFIFO had underflow.

## NOTE

The NCF flag still becomes asserted if an external command buffer empty event  is  detected  at  the  same  time  the  eQADC  stops  checking  for  the coherency of a command sequence.

Once command transfers restart/continue, the non-coherency hardware will behave as if the command sequence started from that point. Figure 19-45 depicts how the non-coherency hardware will behave when a non-coherency event is detected.

## NOTE

If MODE  is changed to disabled while a CFIFO is transferring commands, n the NCF flag for that CFIFO will not become asserted.

## NOTE

When the eQADC enters debug or stop mode while a command sequence is being  executed,  the  NCF  will  become  asserted  if  an  empty  external command buffer is detected after debug/stop mode is exited.

<!-- image -->

TNXTPTR - Transfer Next Data Pointer.

*

CF \_ADCa\_CM  - Command   in CFIFO  bound for ADCa.

x

n

n

x

Figure 19-43. Non-Coherency Event When Different CFIFOs Use the Same Buffer

<!-- image -->

- TNXTPTR - Transfer Next Data Pointer. CF \_ADCa\_CM  - Command   in CFIFO  bound for external command buffer a. x n n x *

Figure 19-44. Non-Coherency Event When Different CFIFOs Are Using Different External Command Buffers

Figure 19-45. Non-coherency Detection When Transfers From A Command Sequence Are Interrupted

<!-- image -->

## 19.4.4 Result FIFOs

## 19.4.4.1 RFIFO Basic Functionality

There are six RFIFOs located in the eQADC. Each RFIFO is four entries deep, and each RFIFO entry is 16 bits long. Each RFIFO serves as a temporary storage location for the one of the result queues allocated in  system memory. All result data is saved in the RFIFOs before being moved into the system result queues. When an RFIFO is not empty, the eQADC sets the corresponding EQADC\_FISRn[RFDF] (see Section 19.3.2.8). If EQADC\_IDCR n [RFDE] is asserted (see Section 19.3.2.7), the eQADC generates a request so that the RFIFO entry is moved to a result queue. An interrupt request, served by the host CPU, is generated when EQADC\_IDCR n [RFDS] is negated, and an eDMA request, served by the eDMA, is generated when RFDS is asserted. The host CPU or the eDMA responds to these requests by reading EQADC\_RFPRn (see Section 19.3.2.5) to retrieve data from the RFIFO.

## NOTE

Reading a word, half-word, or any bytes from EQADC\_RFPR n will pop an entry from RFIFO n ,and the RFCTR n field will be decremented by 1.

The eDMA controller should be configured to read a single result (16-bit data)  from  the  RFIFO  pop  registers  for  every  asserted  eDMA  request  it acknowledges. Refer to Section 19.5.2, 'EQADC/eDMA  Controller Interface' for eDMA controller configuration guidelines.

Figure 19-46 describes the important components in the RFIFO. Each RFIFO is implemented as a circular set of registers to avoid the need to move all entries at each push/pop operation. The pop next data pointer always points to the next RFIFO message to be retrieved from the RFIFO when reading eQADC\_RFPR. The receive next data pointer points to the next available RFIFO location for storing the next incoming message from the on-chip ADCs or from the external device. The RFIFO counter logic counts the number of entries in RFIFO and generates interrupt or eDMA requests to drain the RFIFO.

EQADC\_FISRn[POPNXTPTR] (see Section 19.3.2.8) indicates which entry is currently being addressed by the pop next data pointer, and EQADC\_FISRn[RFCTR] provides the number of entries stored in the

RFIFO. Using POPNXTPTR and RFCTR, the absolute addresses for pop next data pointer and receive next data pointer can be calculated using the following formulas:

Pop Next Data Pointer Address= RFIFO \_BASE\_ADDRESS + POPNXTPTR n n *4

```
_BASE_ADDRESS +
```

Receive Next Data Pointer Address = RFIFO n [(POPNXTPTR n + RFCTR n ) mod RFIFO\_DEPTH] * 4

## where

- · a mod b returns the remainder of the division of a by b .
- · RFIFO \_BASE\_ADDRESS is the smallest memory mapped address allocated to an RFIFO n n entry.
- · RFIFO\_DEPTH is the number of entries contained in a RFIFO - four in this implementation.

When a new message arrives and RFIFO n is not full, the eQADC copies its contents into the entry pointed by receive next data pointer. The RFIFO counter EQADC\_FISR n [RFCTR ] (see Section 19.3.2.8) is n incremented by 1, and the receive next data pointer n is also incremented by 1 (or wrapped around) to point to the next empty  entry in RFIFO .  However,  if  the  RFIFO n n is full, the eQADC  sets  the EQADC\_FISR [RFOF] (see Section 19.3.2.8).  The  RFIFO n n will  not  overwrite  the  older  data  in  the RFIFO, the new data will be ignored, and the receive next data pointer n is not incremented or wrapped around.  RFIFO n is  full  when  the  receive  next  data  pointer n equals  the  pop  next  data  pointer n and RFCTR  is not 0. RFIFO n n is empty when the receive next data pointer n equals the pop next data pointer n and RFCTR  is 0. n

When the eQADC RFIFO pop register   is read and the RFIFO n n is not empty, the RFIFO counter RFCTR n is decremented by 1, and the pop next data pointer is incremented by 1 (or wrapped around) to point to the next RFIFO entry.

When the eQADC RFIFO pop register n is read and RFIFO n is empty, eQADC will not decrement the counter value and the pop next data pointer n will not be updated. The read value will be undefined.

<!-- image -->

- All RFIFO entries are memory mapped and the entries addressed by these pointers can have their absolute addresses calculated using POPNXTPTR and RFCTR. *

Figure 19-46. RFIFO Diagram

The detailed behavior of the pop next data pointer and receive next data pointer is described in the example shown in Figure 19-47 where an RFIFO with 16 entries is shown for clarity of explanation, the actual

## Enhanced Queued Analog-to-Digital Converter (eQADC)

hardware implementation has only four entries. In this example, RFIFO n with  16  entries  is  shown  in sequence after popping or receiving entries.

Figure 19-47. RFIFO Entry Pointer Example

<!-- image -->

## 19.4.4.2 Distributing Result Data into RFIFOs

Data to be moved into the RFIFOs can come from three sources: from ADC0, from ADC1, or from the external device. All result data comes with a MESSAGE\_TAG field defining what should be done with the received data. The FIFO control unit decodes the MESSAGE\_TAG field and:

- · Stores the 16-bit data into the appropriate RFIFO if the MESSAGE\_TAG indicates a valid RFIFO number or

- · Ignores the data in case of a null or 'reserved for customer use' MESSAGE\_TAG

In general, received data is moved into RFIFOs as they become available, while an exception happens when multiple results from different sources become available at the same time. In that case, result data from ADC0 is processed first, result data from ADC1 is only processed after all ADC0 data is processed, and result data from the external device is only processed after all data from ADC0/1 is processed.

When time-stamped results return from the on-chip ADCs, the conversion result and the time stamp are always moved to the RFIFOs in consecutive clock cycles in order to guarantee they are always stored in consecutive RFIFO entries.

## 19.4.5 On-Chip ADC Configuration and Control

## 19.4.5.1 Enabling and Disabling the on-chip ADCs

The on-chip ADCs have an enable bit (ADC0\_CR[ADC0\_EN] and ADC1\_CR[ADC1\_EN], see Section 19.3.3.1) which allows the enabling of the ADCs only when necessary. When the enable bit for an ADC is negated, the clock input to that ADC is stopped. The ADCs are disabled out of reset - ADC0/1\_EN bits are negated - to allow for their safe configuration. The ADC must only be configured when its enable bit is negated. Once the enable bit of an ADC is asserted, clock input is started, and the bias generator circuit is turned on. When the enable bits of both ADCs are negated, the bias circuit generator is stopped.

## NOTE

Conversion commands sent to a disabled ADC are ignored by the ADC control hardware.

## NOTE

NOTE An 8ms wait time from V DDA  power up to enabling ADC is required to pre-charge the external 100nf capacitor on REFBYPC. This time must be guaranteed by crystal startup time plus reset duration or the user. The ADC internal bias generator circuit will start up after 10us upon VRH/VRL power up and produces a stable/required bias current to the pre-charge circuit, but the current to the other analog circuits are disabled until ADCs are enabled. As soon as the ADCs are enabled, the bias currents to other analog circuits will be ready.

Because  of  previous  design  versions,  the  EQADC  will  always  wait  120 ADC clocks  before  issuing  the  first  conversion  command  following  the enabling of one of on-chip ADCs, or the exiting of stop mode. There are two independent counters checking for this delay: one clocked by ADC0\_CLK and another by ADC1\_CLK. Conversion commands can start to be executed whenever one of these counters completes counting 120 ADC clocks.

## 19.4.5.2 ADC Clock and Conversion Speed

The clock input to the ADCs is defined by setting the ADC0\_CR[ADC0\_CLK\_PS]  and ADC1\_CR[ADC1\_CLK\_PS] fields (see Section 19.3.3.1) The ADC0/1\_CLK\_PS field selects the clock divide  factor  by  which  the  system  clock  will  be  divided  as  showed  in  Table 19-28.  The  ADC  clock frequency is calculated as below and it must not exceed 12 MHz.

ADCClockFrequency = - - -- -- --- -- -- - -- -- --- -- -- - -- -- -- --- -- - -- --- - -- --- - -- --- - - SystemClockFrequency MHz -- -; ADCClockFrequency ( ) SystemClockDivideFactor - - -- - -- - -- - -- - - -- -- --- --- --12MHz ≤ ( )

Figure 19-48 depicts how the ADC clocks for ADC0 and ADC1 are generated.

Figure 19-48. ADC0/1 Clock Generation

<!-- image -->

The ADC conversion speed (in kilosamples per second - ksamp/s)is calculated by the following formula. The number of sampling cycles is determined by the LST bits in the command message - see Section , ' Conversion Command Message Format for On-Chip ADC Operation,' - and it can take one of the following values: 2, 8, 64, or 128 ADC clock cycles. The number of AD conversion cycles is 13 for differential conversions and 14 for single-ended conversions. The maximum conversion speed is achieved when the ADC Clock frequency is set to its maximum (12Mhz) and the number of sampling cycles set to its minimum (2 cycles). The maximum conversion speed for differential and single-ended conversions are 800ksamp/s and 750ksamp/s, respectively.

<!-- image -->

Table 19-47 shows an example of how the ADC0/1\_CLK\_PS can be set when using a 120 MHz system clock and the corresponding conversion speeds for all possible ADC clock frequencies. The table also shows that according to the system clock frequency, certain clock divide factors are invalid (2, 4, 6, 8 clock divide factors in the example) since their use would result in a ADC clock frequency higher than the maximum one supported by the ADC. ADC clock frequency must not exceed 12 Mhz.

Table 19-47. ADC Clock Configuration Example (System Clock Frequency = 120 MHz)

| ADC0/1_CLK_PS[0:4]   |   System Clock Divide Factor | ADC Clock in MHz (System Clock = 120MHz)   | Differential Conversion Speed with Default Sampling Time (13 + 2 cycles) in ksamp/s   | Single-Ended Conversion Speed with Default Sampling Time (14 + 2 cycles) in ksamp/s   |
|----------------------|------------------------------|--------------------------------------------|---------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------|
| 0b00000              |                            2 | N/A                                        | N/A                                                                                   | N/A                                                                                   |
| 0b00001              |                            4 | N/A                                        | N/A                                                                                   | N/A                                                                                   |
| 0b00010              |                            6 | N/A                                        | N/A                                                                                   | N/A                                                                                   |
| 0b00011              |                            8 | N/A                                        | N/A                                                                                   | N/A                                                                                   |
| 0b00100              |                           10 | 12.0                                       | 800                                                                                   | 750                                                                                   |
| 0b00101              |                           12 | 10.0                                       | 667                                                                                   | 625                                                                                   |
| 0b00110              |                           14 | 8.57                                       | 571                                                                                   | 536                                                                                   |
| 0b00111              |                           16 | 7.5                                        | 500                                                                                   | 469                                                                                   |
| 0b01000              |                           18 | 6.67                                       | 444                                                                                   | 417                                                                                   |
| 0b01001              |                           20 | 6.0                                        | 400                                                                                   | 375                                                                                   |
| 0b01010              |                           22 | 5.45                                       | 364                                                                                   | 341                                                                                   |
| 0b01011              |                           24 | 5.0                                        | 333                                                                                   | 313                                                                                   |
| 0b01100              |                           26 | 4.62                                       | 308                                                                                   | 288                                                                                   |
| 0b01101              |                           28 | 4.29                                       | 286                                                                                   | 268                                                                                   |
| 0b01110              |                           30 | 4.0                                        | 267                                                                                   | 250                                                                                   |
| 0b01111              |                           32 | 3.75                                       | 250                                                                                   | 234                                                                                   |
| 0b10000              |                           34 | 3.53                                       | 235                                                                                   | 221                                                                                   |
| 0b10001              |                           36 | 3.33                                       | 222                                                                                   | 208                                                                                   |
| 0b10010              |                           38 | 3.16                                       | 211                                                                                   | 197                                                                                   |
| 0b10011              |                           40 | 3.0                                        | 200                                                                                   | 188                                                                                   |
| 0b10100              |                           42 | 2.86                                       | 190                                                                                   | 179                                                                                   |
| 0b10101              |                           44 | 2.73                                       | 182                                                                                   | 170                                                                                   |
| 0b10110              |                           46 | 2.61                                       | 174                                                                                   | 163                                                                                   |
| 0b10111              |                           48 | 2.5                                        | 167                                                                                   | 156                                                                                   |
| 0b11000              |                           50 | 2.4                                        | 160                                                                                   | 150                                                                                   |
| 0b11001              |                           52 | 2.31                                       | 154                                                                                   | 144                                                                                   |
| 0b11010              |                           54 | 2.22                                       | 148                                                                                   | 139                                                                                   |
| 0b11011              |                           56 | 2.14                                       | 143                                                                                   | 134                                                                                   |
| 0b11100              |                           58 | 2.07                                       | 138                                                                                   | 129                                                                                   |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 19-47. ADC Clock Configuration Example  (continued) (System Clock Frequency = 120 MHz)

| ADC0/1_CLK_PS[0:4]   |   System Clock Divide Factor |   ADC Clock in MHz (System Clock = 120MHz) |   Differential Conversion Speed with Default Sampling Time (13 + 2 cycles) in ksamp/s |   Single-Ended Conversion Speed with Default Sampling Time (14 + 2 cycles) in ksamp/s |
|----------------------|------------------------------|--------------------------------------------|---------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------|
| 0b11101              |                           60 |                                       2    |                                                                                   133 |                                                                                   125 |
| 0b11110              |                           62 |                                       1.94 |                                                                                   129 |                                                                                   121 |
| 0b11111              |                           64 |                                       1.88 |                                                                                   125 |                                                                                   117 |

## 19.4.5.3 Time Stamp Feature

The on-chip ADCs can provide a time stamp for the conversions they execute. A time stamp is the value of the time base counter latched when the eQADC detects the end of the analog input voltage sampling. A time stamp for a conversion command is requested by setting the TSR bit in the corresponding command. When TSR is negated, that is a time stamp is not requested, the ADC returns a single result message containing the conversion result. When TSR is asserted, that is a time stamp is requested, the ADC returns two result messages; one containing the conversion result, and another containing the time stamp for that conversion. The result messages are sent in this order to the RFIFOs and both messages are sent to the same RFIFO as specified in the MESSAGE\_TAG field of the executed conversion command.

The time base counter is a 16-bit up counter and wraps after reaching 0xFFFF. It is disabled after reset and it  is  enabled  according  to  the  setting  of  ADC\_TSCR[TBC\_CLK\_PS]  field  (see  Section  19.3.3.2). TBC\_CLK\_PS defines if the  counter  is  enabled  or  disabled,  and,  if  enabled,  at  what  frequency  it  is incremented. The time stamps are returned regardless of whether the time base counter is enabled or disabled. The time base counter can be reset by writing 0x0000 to the ADC\_TBCR (Section 19.3.3.3) with a write configuration command.

## 19.4.5.4 ADC Calibration Feature

## 19.4.5.4.1 Calibration Overview

The eQADC provides a calibration scheme to remove the effects of gain and offset errors from the results generated by the on-chip ADCs. Only results generated by the on-chip ADCs are calibrated. The results generated by ADCs on the external device are directly sent to RFIFOs unchanged. The main component of calibration hardware is a multiply-and-accumulate (MAC) unit, one per on-chip ADC, that is used to calculate the following transfer function which relates a calibrated result to a raw, uncalibrated one.

<!-- formula-not-decoded -->

## where:

- · CAL\_RES is the calibrated result corresponding the input voltage V i .
- · GCC is the gain calibration constant.
- · RAW\_RES is the raw, uncalibrated result corresponding to an specific input voltage V i .
- · OCC is the offset calibration constant.
- · The addition of two reduces the maximum quantization error of the ADC. See Section 19.5.6.3, 'Quantization Error Reduction During Calibration .'

Calibration constants GCC and OCC are determined by taking two samples of known reference voltages and using these samples to calculate their values. For details and an example about how to calculate the calibration constants and use them in result calibration refer to Section 19.5.6, 'ADC Result Calibration.' Once calculated, GCC is stored in ADC0\_GCCR and ADC1\_GCCR (see Section 19.3.3.4) and OCC in ADC0\_OCCR and ADC1\_OCCR (see Section 19.3.3.5) from where their values are fed to the MAC unit. Since  the  analog  characteristics  of  each  on-chip  ADC  differs,  each  ADC  has  an  independent  pair  of calibration constants.

A conversion result is calibrated according to the status of CAL bit in the command that initiated the conversion. If the CAL bit is asserted, the eQADC will automatically calculate the calibrated result before sending the result to the appropriate RFIFO. If the CAL bit is negated, the result is not calibrated, it bypasses the calibration hardware, and is directly sent to the appropriate RFIFO.

## 19.4.5.4.2 MAC Unit and Operand Data Format

The MAC unit diagram is shown in Figure 19-49. Each on-chip ADC has a separate MAC unit to calibrate its conversion results.

Figure 19-49. MAC Unit Diagram

<!-- image -->

The OCC  operand is a 14-bit signed value and it is the upper 14 bits of the value stored in ADC0\_OCCR n and ADC1\_OCCR. The RAW\_RES operand is the raw uncalibrated result, and it is a direct output from the on-chip ADCs.

The GCC  operand is a 15-bit fixed point unsigned value, and it is the upper 15 bits of the value stored in n ADC0\_GCCR and ADC1\_GCCR. The GCC is expressed in the GCC\_INT.GCC\_FRAC binary format. The integer part of the GCC (GCC\_INT = GCC[1]) contains a single binary digit while its fractional part (GCC\_FRAC = GCC[2:15]) contains 14 bits. See Figure 19-50 for more information. The gain constant equivalent decimal value ranges from 0 to 1.999938..., as shown in Table 19-49. Two is always added to the  MAC output: see Section 19.5.6.3,  'Quantization  Error  Reduction  During  Calibration.  CAL\_RES output is the calibrated result, and it is a 14-bit unsigned value. CAL\_RES is truncated to 0x3FFF, in case of a overflow, and to 0x0000, in case of an underflow.

<!-- image -->

## Gain Calibration Constant (GCC)

Figure 19-50. Gain Calibration Constant Format

Table 19-48. Gain Calibration Constant Format Field Descriptions

| Bits   | Name            | Description                                                                                                                                                                                                         |
|--------|-----------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0      | -               | Reserved                                                                                                                                                                                                            |
| 1      | GCC_INT [0]     | Integer part of the gain calibration constant for ADC n . GCC_INT is the integer part of the gain calibration constant (GCC) for ADC0/1.                                                                            |
| 2-15   | GCC_FRAC [1:14] | Fractional part of the gain calibration constant for ADC n . GCC_FRAC is the fractional part of the gain calibration constant (GCC) for ADC n . GCC_FRAC can expresses decimal values ranging from 0 to 0.999938... |

Table 19-49. Correspondence between Binary and Decimal Representations of the Gain Constant

| Gain Constant (GCC_INT.GCC_FRAC binary format)   | Corresponding Decimal Value   |
|--------------------------------------------------|-------------------------------|
| 0.0000_0000_0000_00                              | 0                             |
| ...                                              | ...                           |
| 0.1000_0000_0000_00                              | 0.5                           |
| ...                                              | ...                           |
| 0.1111_1111_1111_11                              | 0.999938...                   |
| 1.0000_0000_0000_00                              | 1                             |
| ...                                              | ...                           |
| 1.1100_0000_0000_00                              | 1.75                          |
| ...                                              | ...                           |
| 1.1111_1111_1111_11                              | 1.999938...                   |

## 19.4.5.5 ADC Control Logic Overview and Command Execution

Figure 19-51  shows  the  basic  logic  blocks  involved  in  the  ADC  control  and  how  they  interact. CFIFOs/RFIFOs interact with ADC command/result message return logic through the FIFO control unit. The EB and BN bits in the command message uniquely identify the ADC to which a command should be sent. The FIFO control unit decodes these bits and sends the ADC command to the proper ADC. Other blocks of logic are the result format and calibration submodule, the time stamp logic , and the MUX control logic.

The result format and calibration submodule formats the returning data into result messages and sends them to the RFIFOs. The returning data can be data read from an ADC register, a conversion result, or a time stamp. The formatting and calibration of conversion results also take place inside this submodule.

The time stamp logic latches the value of the time base counter when detecting the end of the analog input voltage sampling, and sends it to the result format and calibration submodule as time stamp information.

The MUX control logic generates the proper MUX control signals and, when the ADC0/1\_EMUX bits are asserted, the MA signals based on the channel numbers extracted from the ADC Command.

ADC commands are stored in the ADC command buffers (2 entries) as they come in and they are executed on a first-in-first-out basis. After the execution of a command in ENTRY1 finishes, all commands are shifted  one  entry.  After  the  shift,  ENTRY0  is  always  empty  and  ready  to  receive  a  new  command. Execution of configuration commands only starts when they reach ENTRY1. Consecutive conversion commands are pipelined, and their execution can start while in ENTRY0. This is explained below.

A/D conversion accuracy can be affected by the settling time of the input channel multiplexers. Some time is  required  for  the  channel  multiplexer's  internal  capacitances  to  settle  after  the  channel  number  is changed. If the time prior to and during sampling is not long enough to permit this settling, then the voltage on the sample capacitors will not accurately represent the voltage to be read. This is a problem in particular when external muxes are used.

To maximize settling time, when a conversion command is in buffer ENTRY1 and another conversion command is identified in ENTRY0, then the channel number of ENTRY0 is sent to the MUX control logic half an ADC clock before the start of the sampling phase of the command in ENTRY0. This pipelining of sample and settling phase is shown in Figure 19-52(b).

This provides more accurate sampling, which is specially important for applications that require high conversion speeds, i.e., with the ADC running at maximum clock frequency and with the analog input voltage sampling time set to a minimum (2 ADC clock cycles). In this case the short sampling time may not allow the multiplexers to completely settle. The second advantage of pipelining conversion commands is to provide equal conversion intervals even though the sample time increases on second and subsequent conversions. See Figure 19-52. This is important for any digital signal process application.

## Enhanced Queued Analog-to-Digital Converter (eQADC)

Figure 19-51. On-Chip ADC Control Scheme

<!-- image -->

<!-- image -->

(b) Command Execution Sequence for Two Overlapped Commands

Figure 19-52. Overlapping Consecutive Conversion Commands

## 19.4.6 Internal/External Multiplexing

## 19.4.6.1 Channel Assignment

The internal  analog  multiplexers  select  one  of  the  40  analog  input  pins  for  conversion,  based  on  the CHANNEL\_NUMBER field of a Command Message. The analog input pin channel number assignments and the pin definitions vary depending on how the ADC0/1\_EMUX are configured. Allowed combinations of  ADC0/1\_EMUX bits  are  shown  in  Table 19-50  together  with  references  to  tables  indicating  how CHANNEL\_NUMBER  field  of  each  conversion  command  must  be  set  to  avoid  channel  selection conflicts.

During differential conversions the analog multiplexer passes differential signals to both the positive and negative terminals of the ADC. The differential conversions can only be initiated on four channels: DAN0, DAN1, DAN2, and DAN3. Refer to Table 19-51 and Figure 19-52 for the channel numbers used to select differential conversions.

Table 19-50. ADC n \_EMUX Bits Combinations

| ADC0_EMUX   | ADC1_EMUX   | CHANNEL_NUMBER should be set as in   | CHANNEL_NUMBER should be set as in   |
|-------------|-------------|--------------------------------------|--------------------------------------|
| ADC0_EMUX   | ADC1_EMUX   | ADC0                                 | ADC1                                 |
| 0           | 0           | Refer to Table 19-51                 | Refer to Table 19-51                 |
| 0           | 1           | Refer to Table 19-51                 | Refer to Figure 19-52                |
| 1           | 0           | Refer to Figure 19-52                | Refer to Table 19-51                 |
| 1           | 1           | Reserved 1                           | Reserved 1                           |

1 ADC0\_EMUX and ADC1\_EMUX must not be asserted at the same time.

Table 19-51 shows the channel number assignments for the non-multiplexed mode. The 40 single-ended channels and 4 differential pairs are shared between the two ADCs.

Table 19-51. Non-multiplexed Channel Assignments 1

| Input Pins                                                      | Input Pins                   | Input Pins                                          | Channel Number in CHANNEL_NUMBER Field   | Channel Number in CHANNEL_NUMBER Field   |
|-----------------------------------------------------------------|------------------------------|-----------------------------------------------------|------------------------------------------|------------------------------------------|
| Analog Pin Name                                                 | Other Functions              | Conversion Type                                     | Binary                                   | Decimal                                  |
| AN0 to AN39                                                     |                              | Single-ended                                        | 0000_0000 to 0010_0111                   | 0 to 39                                  |
| VRH                                                             |                              | Single-ended                                        | 0010_1000                                | 40                                       |
| VRL                                                             |                              | Single-ended                                        | 0010_1001                                | 41                                       |
|                                                                 | (VRH - VRL)/2 see footnote 2 | Single-ended                                        | 0010_1010                                | 42                                       |
|                                                                 | 75% x (VRH - VRL)            | Single-ended                                        | 0010_1011                                | 43                                       |
|                                                                 | 25% x (VRH - VRL)            | Single-ended                                        | 0010_1100                                | 44                                       |
| Reserved                                                        | Reserved                     | Reserved                                            | 0010_1101 to 0101_1111                   | 45 to 95                                 |
| DAN0+ and DAN0- DAN1+ and DAN1- DAN2+ and DAN2- DAN3+ and DAN3- |                              | Differential Differential Differential Differential | 0110_0000 0110_0001 0110_0010 0110_0011  | 96 97 98 99                              |
| Reserved                                                        | Reserved                     | Reserved                                            | 0110_0100 to 1111_1111                   | 100 to 255                               |

1 The two on-chip ADCs can access the same analog input pins but simultaneous conversions are not allowed. Also, when one ADC is performing a differential conversion on a pair of pins, the other ADC must not access either of these two pins as single-ended channels.

2 This equation only applies before calibration. After calibration, the 50% reference point will actually return approximately 20mV lower than the expected 50% of the difference between the High Reference Voltage (VRH) and the Low Reference Voltage (VRL). For calibration of the ADC only the 25% and 75% points should be used as described in Section 19.5.6.1, 'MAC Configuration Procedure'

Figure 19-52  shows  the  channel  number  assignments  for  multiplexed  mode.  The  ADC  with  the ADC \_EMUX bit asserted can access 4 differential pairs, 39 single-ended, and, at most, 32 externally n multiplexed channels. Refer to Section 19.4.6.2, 'External Multiplexing,' for a detailed explanation about how external multiplexing can be achieved.

Table 19-52. Multiplexed Channel Assignments 1

| Input Pins                                                      | Input Pins      | Input Pins                                          | Channel Number in CHANNEL_NUMBER Field   | Channel Number in CHANNEL_NUMBER Field   |
|-----------------------------------------------------------------|-----------------|-----------------------------------------------------|------------------------------------------|------------------------------------------|
| Analog Pin Name                                                 | Other Functions | Conversion Type                                     | Binary                                   | Decimal                                  |
| AN0 to AN7                                                      |                 | Single-ended                                        | 0000_0000 to 0000_0111                   | 0 to 7                                   |
| Reserved                                                        | Reserved        | Reserved                                            | 0000_1000 to 0000_1011                   | 8 to 11                                  |
| AN12 to AN39                                                    |                 | Single-ended                                        | 0000_1100 to 0010_0111                   | 12 to 39                                 |
| VRH                                                             |                 | Single-ended                                        | 0010_1000                                | 40                                       |
| VRL                                                             |                 | Single-ended                                        | 0010_1001                                | 41                                       |
|                                                                 | (VRH-VRL)/2     | Single-ended                                        | 0010_1010                                | 42                                       |
|                                                                 | 75% x (VRH-VRL) | Single-ended                                        | 0010_1011                                | 43                                       |
|                                                                 | 25% x (VRH-VRL) | Single-ended                                        | 0010_1100                                | 44                                       |
| Reserved                                                        | Reserved        | Reserved                                            | 0010_1101 to 0011_1111                   | 45 to 63                                 |
| ANW ANX ANY ANZ                                                 | - - - -         | Single-ended Single-ended Single-ended Single-ended | 0100_0xxx 0100_1xxx 0101_0xxx 0101_1xxx  | 64 to 71 72 to 79 80 to 87 88 to 95      |
| DAN0+ and DAN0- DAN1+ and DAN1- DAN2+ and DAN2- DAN3+ and DAN3- |                 | Differential Differential Differential Differential | 0110_0000 0110_0001 0110_0010 0110_0011  | 96 97 98 99                              |
| Reserved                                                        | Reserved        | Reserved                                            | 0011_0100 to 1111_1111                   | 100 to 255                               |

1 The two on-chip ADCs can access the same analog input pins but simultaneous conversions are not allowed. Also, when one ADC is performing a differential conversion on a pair of pins, the other ADC must not access either of these two pins as single-ended channels.

## 19.4.6.2 External Multiplexing

The eQADC can use from one to four external multiplexers to expand the number of analog signals that may be converted. Up to 32 analog channels can be converted through external multiplexer selection. The externally  multiplexed  channels  are  automatically  selected  by  the  CHANNEL\_NUMBER  field  of  a command message, in the same way done with internally multiplexed channels. The software selects the external  multiplexed  mode  by  setting  the  ADC0/1\_EMUX  bit  in  either  ADC0\_CR  or  ADC1\_CR depending  on  which  ADC  will  perform  the  conversion.  Figure 19-52  shows  the  channel  number assignments for the multiplexed mode. There are 4 differential pairs, 40 single-ended, and, at most, 32 externally multiplexed channels that can be selected. Only one ADC can have its ADC0/1\_EMUX bit asserted at a time.

Figure 19-53  shows  the  maximum  configuration  of  four  external  multiplexer  chips  connected  to  the eQADC. The external multiplexer chip selects one of eight analog inputs and connects it to a single analog output, which is fed to a specific input of the eQADC. The eQADC provides three multiplexed address signals, MA0, MA1, and MA2, to select one of eight inputs. These three multiplexed address signals are connected to all four external multiplexer chips. The analog output of the four multiplex chips are each connected to four separate eQADC inputs, ANW, ANX, ANY, and ANZ. The MA pins correspond to the

three least significant bits of the channel number that selects ANW, ANX, ANY, and ANZ with MA0 being the most significant bit - See Table 19-53.

Table 19-53. Encoding of MA Pins 1

| Channel Number selecting ANW, ANX, ANY, ANZ (decimal)   | Channel Number selecting ANW, ANX, ANY, ANZ (decimal)   | Channel Number selecting ANW, ANX, ANY, ANZ (decimal)   | Channel Number selecting ANW, ANX, ANY, ANZ (decimal)   | MA0   | MA1   | MA2   |
|---------------------------------------------------------|---------------------------------------------------------|---------------------------------------------------------|---------------------------------------------------------|-------|-------|-------|
| ANW                                                     | ANX                                                     | ANY                                                     | ANZ                                                     |       |       |       |
| 64                                                      | 72                                                      | 80                                                      | 88                                                      | 0     | 0     | 0     |
| 65                                                      | 73                                                      | 81                                                      | 89                                                      | 0     | 0     | 1     |
| 66                                                      | 74                                                      | 82                                                      | 90                                                      | 0     | 1     | 0     |
| 67                                                      | 75                                                      | 83                                                      | 91                                                      | 0     | 1     | 1     |
| 68                                                      | 76                                                      | 84                                                      | 92                                                      | 1     | 0     | 0     |
| 69                                                      | 77                                                      | 85                                                      | 93                                                      | 1     | 0     | 1     |
| 70                                                      | 78                                                      | 86                                                      | 94                                                      | 1     | 1     | 0     |
| 71                                                      | 79                                                      | 87                                                      | 95                                                      | 1     | 1     | 1     |

1 0 means pin is driven LOW and 1 that pin is driven HIGH.

When the external multiplexed mode is selected for either ADC, the eQADC automatically creates the MA output signals from CHANNEL\_NUMBER field of a command message. The eQADC also converts the proper input channel (ANW, ANX, ANY, and ANZ) by interpreting the CHANNEL\_NUMBER field. As a result, up to 32 externally multiplexed channels appear to the conversion queues as directly connected signals.

Figure 19-53. Example of External Multiplexing

<!-- image -->

## 19.4.7 eQADC eDMA/Interrupt Request

Table 19-54 lists methods to generate interrupt requests in the eQADC queuing control and triggering control.  The  eDMA/interrupt  request  select  bits  and  the  eDMA/interrupt  enable  bits  are  described  in Section 19.3.2.7,  'eQADC  Interrupt  and  eDMA  Control  Registers  0-5  (EQADC\_IDCRn),'  and  the interrupt flag bits are described in Section 19.3.2.8, 'eQADC FIFO and Interrupt Status Registers 0-5 (EQADC\_FISRn).' Table 19-54 depicts all interrupts and eDMA requests generated by the eQADC.

## Enhanced Queued Analog-to-Digital Converter (eQADC)

## Table 19-54. eQADC FIFO Interrupt Summary 1

| Interrupt                          | Condition                        | Clearing Mechanism                          |
|------------------------------------|----------------------------------|---------------------------------------------|
| Non Coherency Interrupt            | NCIE n = 1 NCF n = 1             | Clear NCF n bit by writing a 1 to the bit.  |
| Trigger Overrun Interrupt 2        | TORIE n = 1 TORF n =1            | Clear TORF n bit by writing a 1 to the bit. |
| Pause Interrupt                    | PIE n = 1 PF n =1                | Clear PF n bit by writing a 1 to the bit.   |
| End of Queue Interrupt             | EOQIE n = 1 EOQF n = 1           | Clear EOQF n bit by writing a 1 to the bit. |
| Command FIFO Underflow Interrupt 2 | CFUIE n = 1 CFUF n = 1           | Clear CFUF n bit by writing a 1 to the bit. |
| Command FIFO Fill Interrupt        | CFFE n = 1 CFFS n = 0 CFFF n = 1 | Clear CFFF n bit by writing a 1 to the bit. |
| Result FIFO Overflow Interrupt 2   | RFOIE n = 1 RFOF n = 1           | Clear RFOF n bit by writing a 1 to the bit. |
| Result FIFO Drain Interrupt        | RFDE n = 1 RFDS n = 0 RFDF n = 1 | Clear RFDF n bit by writing a 1 to the bit. |

- 1 For details refer to Section 19.3.2.8, 'eQADC FIFO and Interrupt Status Registers 0-5 (EQADC\_FISRn),' and Section 19.3.2.7, 'eQADC Interrupt and eDMA Control Registers 0-5 (EQADC\_IDCRn).'
- 2 Apart from generating an independent interrupt request for when a RFIFO overflow interrupt, a CFIFO underflow interrupt, and a CFIFO trigger overrun interrupt occurs, the eQADC also provides a combined interrupt request at which these requests from ALL CFIFOs are ORed. Refer to Figure 19-54 for details.

## Table 19-55 describes a list of methods to generate eDMA requests by the eQADC.

Table 19-55. eQADC FIFO eDMA Summary 1

| eDMA Request                   | Condition                        | Clearing Mechanism                                                                                                               |
|--------------------------------|----------------------------------|----------------------------------------------------------------------------------------------------------------------------------|
| Result FIFO Drain eDMA Request | RFDE n = 1 RFDS n = 1 RFDF n = 1 | The eQADC automatically clears the RFDF n when RFIFO n becomes empty. Writing 1 to the RFDF n bit is not allowed while RDFS = 1. |
| Command FIFO Fill eDMA Request | CFFE n = 1 CFFS n = 1 CFFF n = 1 | The eQADC automatically clears the CFFF n when CFIFO n becomes full. Writing 1 to the CFFF n bit is not allowed while CFDS = 1.  |

1 For details refer to Section 19.3.2.8, 'eQADC FIFO and Interrupt Status Registers 0-5 (EQADC\_FISRn),' and Section 19.3.2.7, 'eQADC Interrupt and eDMA Control Registers 0-5 (EQADC\_IDCRn).'

Figure 19-54. eQADC eDMA and Interrupt Requests

<!-- image -->

## 19.4.8 eQADC Synchronous Serial Interface (SSI) Submodule

Figure 19-55. eQADC Synchronous Serial Interface Block Diagram

<!-- image -->

The  eQADC  SSI  protocol  allows  for  a  full  duplex,  synchronous,  serial  communication  between  the eQADC and a single external device. Figure 19-55 shows the different components inside the eQADC SSI. The eQADC SSI submodule on the eQADC is always configured as a master. The eQADC SSI has four associated port pins:

- · Free running clock (FCK)
- · Serial data select (SDS)
- · Serial data in (SDI)
- · Serial data out (SDO)

The FCK clock signal times the shifting and sampling of the two serial data signals and it is free running between transmissions, allowing it to be used as the clock for the external device. The SDS signal will be asserted  to  indicate  the  start  of  a  transmission,  and  negated  to  indicate  the  end  or  the  abort  of  a transmission. SDI is the master serial data input and SDO the master serial data output.

The eQADC SSI submodule is enabled by setting the EQADC\_MCR[ESSIE] (see Section 19.3.2.1). When enabled, the eQADC SSI can be optionally capable of starting serial transmissions. When serial transmissions are disabled (ESSIE set to 0b10), no data will be transmitted to the external device but FCK will be free-running. This operation mode permits the control of the timing of the first serial transmission, and can be used to avoid the transmission of data to an unstable external device, for example, a device that is not fully reset. This mode of operation is specially important for the reset procedure of an external device that uses the FCK as its main clock.

The main elements of the eQADC SSI are the shift registers. The 26-bit transmit shift register in the master and 26-bit receive shift register in the slave are linked by the SDO pin. In a similar way, the 26-bit transmit shift register in the slave and 26-bit receive shift register in the master are linked by the SDI pin. See Figure 19-56. When a data transmission operation is performed, data in the transmit registers is serially shifted  twenty-six  bit  positions  into  the  receive  registers  by  the  FCK  clock  from  the  master;  data  is exchanged between the master and the slave. Data in the master transmit shift register in the beginning of

a transmission operation becomes the output data for the slave, and data in the master receive shift register after a transmission operation is the input data from the slave.

Figure 19-56. Full Duplex Pin Connection

<!-- image -->

## 19.4.8.1 eQADC SSI Data Transmission Protocol

Figure 19-57 shows the timing of an eQADC SSI transmission operation. The main characteristics of this protocol are the following:

- · FCK is free running, it does not stop between data transmissions. FCK will be driven low:
- - When the serial interface is disabled
- - In stop/debug mode
- - Immediately after reset
- · Frame size is fixed to 26 bits.
- · Msb bit is always transmitted first.
- · Master drives data on the positive edge of FCK and latches incoming data on the next positive edge of FCK.
- · Slave drives data on the positive edge of FCK and latches incoming data on the negative edge of FCK.

Master initiates a data transmission by driving SDS low, and its msb bit on SDO on the positive edge of FCK. Once an asserted SDS is detected, the slave shifts its data out, one bit at a time, on every FCK positive edge. Both the master and the slave drive new data on the serial lines on every FCK positive edge. This process continues until all the initial 26-bits in the master shift register are moved into the slave shift register. t DT  is the delay between two consecutive serial transmissions, time during which SDS is negated. When ready to start of the next transmission, the slave must drive the msb bit of the message on every positive edge of FCK regardless of the state of the SDS signal. On the next positive edge, the second bit of the message is conditionally driven according to if an asserted SDS was detected by the slave on the preceding  FCK  negative  edge.  This  is  an  important  requisite  since  the  SDS  and  the  FCK  are  not synchronous. The SDS signal is not generated by FCK, rather both are generated by the system clock, so that  it  is  not  guaranteed  that  FCK  edges  will  precede  SDS  edges.  While  SDS  is  negated,  the  slave continuously drives its msb bit on every positive edge of FCK until it detects an asserted SDS on the immediately next FCK negative edge. See Figure 19-58 for three situations showing how the slave should behave according to when SDS is asserted.

## NOTE

On the master, the FCK is not used as a clock. Although, the eQADC SSI behavior is described in terms of the FCK positive and negative edges, all eQADC SSI related signals (SDI, SDS, SDO, and FCK) are synchronized by the system clock on the master side. There are no restrictions regarding the use of the FCK as a clock on the slave device.

## 19.4.8.1.1 Abort Feature

The master indicates it is aborting the current transfer by negating SDS before the whole data frame has being shifted out, that is the 26th bit of data being transferred has not being shifted out. The eQADC ignores  the  incompletely  received  message.  The  eQADC  re-sends  the  aborted  message  whenever  the corresponding CFIFO becomes again the highest priority CFIFO with commands bound for an external command buffer that is not full. Refer to Section 19.4.3.2, 'CFIFO Prioritization and Command Transfer,' for more information on aborts and CFIFO priority.

## 19.4.8.2 Baud Clock Generation

As shown in Figure 19-55, the baud clock generator divides the system clock to produce the baud clock. The  EQADC\_SSICR[BR]  field  (see  Section  19.3.2.12)  selects  the  system  clock  divide  factor  as  in Table 19-21. 1

<!-- formula-not-decoded -->

<!-- image -->

t MDT  = Minimum t DT  is programmable and defined in Section 18.3.2.12, 'eQADC SSI Control Register (EQADC\_SSICR).'

Figure 19-57. Synchronous Serial Interface Protocol Timing

1.Maximum FCK frequency is highly dependable on track delays, master pad delays, and slave pad delays.

Figure 19-58. Slave Driving the msb and Consecutive Bits in a Data Transmission

<!-- image -->

## 19.4.9 Analog Submodule

## 19.4.9.1 Reference Bypass

The reference bypass capacitor (REFBYPC) signal requires a 100 nF capacitor connected to VRL to filter noise on the internal reference used by the ADC.

Figure 19-59. Reference Bypass Circuit

<!-- image -->

## 19.4.9.2 Analog-to-Digital Converter (ADC)

## 19.4.9.2.1 ADC Architecture

Figure 19-60. RSD ADC Block Diagram

<!-- image -->

The redundant signed digit (RSD) cyclic ADC consists of two main portions, the analog RSD stage, and the  digital  control  and  calculation  module,  as  shown  in  Figure 19-60.  To  begin  an  analog-to-digital conversion, a differential input is passed into the analog RSD stage. The signal is passed through the RSD stage, and then from the RSD stage output, back to its input to be passed again. To complete a 12-bit conversion, the signal must pass through the RSD stage 12 times. Each time an input signal is read into the RSD  stage, a digital sample is taken by the digital control/calculation module. The digital control/calculation module uses this sample to tell the analog module how to condition the signal. The digital module also saves each successive sample and adds them according to the RSD algorithm at the end of the entire conversion cycle.

## 19.4.9.2.2 RSD Overview

Figure 19-61. RSD Stage Block Diagram

<!-- image -->

On each pass through the RSD stage, the input signal will be multiplied by exactly two, and summed with either -vref, 0, or vref, depending on the logic control. The logic control will determine -vref, 0, or vref depending on the two comparator inputs. As the logic control sets the summing operation, it also sends a digital value to the RSD adder. Each time an analog signal passes through the RSD single-stage, a digital value is collected by the RSD adder. At the end of an entire AD conversion cycle, the RSD adder uses these collected values to calculate the 12-bit digital output.

Figure 19-62 shows the transfer function for the RSD stage. Note how the digital value (AB) is dependent on the two comparator inputs.

Figure 19-62. RSD Stage Transfer Function

<!-- image -->

In each pass through the RSD stage, the residue will be sent back to be the new input, and the digital signals, a and b, will be stored. For the 12-bit ADC, the input signal is sampled during the input phase, and after each of the 12 passes through the RSD stage. Thus, 13 total a and b values are collected. Upon

collecting all these values, they will be added according to the RSD algorithm to create the 12-bit digital representation of the original analog input. The bits are added in the following manner:

## 19.4.9.2.3 RSD Adder

The array, s1 to s12,will be the digital output of the RSD ADC with s1 being the msb and s12 being the lsb (least significant bit).

Figure 19-63. RSD Adder

<!-- image -->

## 19.5 Initialization/Application Information

## 19.5.1 Multiple Queues Control Setup Example

This  section  provides  an  example  of  how  to  configure  multiple  user  command  queues.  Table 19-56 describes how each queue can be used for a different application. Also documented in this section are general guidelines on how to initialize the on-chip ADCs and the external device, and how to configure the command queues and the eQADC.

Table 19-56. Example Applications of Each Command Queue

|   Command Queue Number | Queue Type                       | Running Speed                                              |   Number of Contiguous Conversions | Example                                     |
|------------------------|----------------------------------|------------------------------------------------------------|------------------------------------|---------------------------------------------|
|                      0 | Very fast burst time-based queue | every 2 µ s for 200 µ s; pause for 300 µ s and then repeat |                                  2 | Injector current profiling                  |
|                      1 | Fast hardware-triggered queue    | every 900 µ s                                              |                                  3 | Current sensing of PWM controlled actuators |
|                      2 | Fast repetitive time-based queue | every 2 ms                                                 |                                  8 | Throttle position                           |
|                      3 | Software-triggered queue         | every 3.9 ms                                               |                                  3 | Command triggered by software strategy      |
|                      4 | Repetitive angle-based queue     | every 625 us                                               |                                  7 | Airflow read every 30 degrees at 8000 RPM   |
|                      5 | Slow repetitive time-based queue | every 100 ms                                               |                                 10 | Temperature sensors                         |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## 19.5.1.1 Initialization of On-Chip ADCs/External Device

The following steps provide an example of configuring the eQADC to initialize the on-chip ADCs and the external device. In this example, commands will be sent through CFIFO0.

- 1. Load all required configuration commands in the RAM in such way that they form a queue; this data structure will be referred below as Queue0. Figure 19-64 shows an example of a command queue able to configure the on-chip ADCs and external device at the same time.
- 2. Configure Section 19.3.2.2, 'eQADC Null Message Send Format Register (EQADC\_NMSFR).'
- 3. Configure Section 19.3.2.12, 'eQADC SSI Control Register (EQADC\_SSICR),' to communicate with the external device.
- 4. Enable the eQADC SSI by programming the ESSIE field the Section 19.3.2.1, 'eQADC Module Configuration Register (EQADC\_MCR).'
- a) Write 0b10 to ESSIE field to enable the eQADC SSI. FCK is free running but serial transmissions are not started.
- b) Wait until the external device becomes stable after reset.
- c) Write 0b11 to ESSIE field to enable the eQADC SSI to start serial transmissions.
- 5. Configure the eDMA to transfer data from Queue0 to CFIFO0 in the eQADC.
- 6. Configure Section 19.3.2.7, 'eQADC Interrupt and eDMA Control Registers 0-5 (EQADC\_IDCRn).'
- a) Set CFFS0 to configure the eQADC to generate an eDMA request to load commands from Queue0 to the CFIFO0.
- b) Set CFFE0 to enable the eQADC to generate an eDMA request to transfer commands from Queue0 to CFIFO0; Command transfers from the RAM to the CFIFO0 will start immediately.
- c) Set EOQIE0 to enable the eQADC to generate an interrupt after transferring all of the commands of Queue0 through CFIFO0.
- 7. Configure Section 19.3.2.6, 'eQADC CFIFO Control Registers 0-5 (EQADC\_CFCRn).'
- a) Write 0b0001 to the MODE0 field in eQADC\_CFCR0 to program CFIFO0 for software single-scan mode.
- b) Write 1 to SSE0 to assert SSS0 and trigger CFIFO0.
- 8. Because CFIFO0 is in single-scan software mode and it is also the highest priority CFIFO, the eQADC starts to transfer configuration commands to the on-chip ADCs and to the external device.
- 9. When all of the configuration commands have been transferred, EQADC\_FISRn[CF0] )(see Section 19.3.2.8) will be set. The eQADC generates a end of queue interrupt. The initialization procedure is complete.

## Command Queue in System Memory

Configuration Command to ADC0-Ex: Write ADC0\_CR

0x0

0x1

0x2

0x3

Configuration Command to ADC2-Ex: Write to external device configuration register

Configuration Command to ADC0-Ex: Write ADC\_TSCR

Configuration Command to ADC1-Ex: Write ADC1\_CR

Command Address

Figure 19-64. Example of a Command Queue Configuring the On-Chip ADCs/External Device

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## 19.5.1.2 Configuring eQADC for Applications

This section provides an example based on the applications in Table 19-56. The example describes how to configure  multiple  command  queues  to  be  used  for  those  applications  and  provides  a  step-by-step procedure to configure the eQADC and the associated command queue structures. In the example, the 'Fast hardware-triggered command queue,' described on the second row of Table 19-56, will have its commands transferred to ADC1; the conversion commands will be executed by ADC1. The generated results will be returned to RFIFO3 before being transferred to the result queues in the RAM by the eDMA.

## NOTE

There is no fixed relationship between CFIFOs and RFIFOs with the same number. The results of commands being transferred through CFIFO1 can be returned to any RFIFO, regardless of its number. The destination of a result is determined by the MESSAGE\_TAG field of the command that requested the result. See Section 19.4.1.2, 'Message Format in eQADC,' for details.

Step One: Set up the command queues and result queues.

- 1. Load the RAM with configuration and conversion commands. Table 19-57 is an example of how command queue 1 commands should be set.
- a) Each trigger event will cause four commands to be executed. When the eQADC detects the pause bit asserted, it will wait for another trigger to restart transferring commands from the CFIFO.
- b) At the end of the command queue, the 'EOQ' bit is asserted as shown in Table 19-57.
- c) Results will be returned to RFIFO3 as specified in the MESSAGE\_TAG field of commands.
- 2. Reserve memory space for storing results.

Table 19-57. Example of Command Queue Commands 1

0 1 2 3 4 5 6 7 8 9 1 0 1 1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 2 0 2 1 2 2 2 3 2 4 2 5 2 6 2 7 2 8 2 9 3 0 3 1

|      | EOQ   | PAUSE   | RESERVED   | ABORT_ST   | EB (0b1)   | BN   | CAL   | MESSAGE TAG     | ADC COMMAND                                              |
|------|-------|---------|------------|------------|------------|------|-------|-----------------|----------------------------------------------------------|
| CMD1 | 0     | 0       | 0          | 0          | 0          | 1    | 0     | 0b0011          | Conversion Command                                       |
| CMD2 | 0     | 0       | 0          | 0          | 0          | 1    | 0     | 0b0011          | Conversion Command                                       |
| CMD3 | 0     | 0       | 0          | 0          | 0          | 1    | 0     | 0b0011          | Conversion Command                                       |
| CMD4 | 0     | 1       | 0          | 0          | 0          | 1    | 0     | 0b0011 2        | Configure peripheral device for next conversion sequence |
| CMD5 | 0     | 0       | 0          | 0 0        |            | 1    | 0     | 0b0011          | Conversion Command                                       |
| CMD6 | 0     | 0       | 0          | 0 0        |            | 1    | 0     | 0b0011          | Conversion Command                                       |
| CMD7 | 0     | 0       | 0          | 0 0        |            | 1    | 0     | 0b0011          | Conversion Command                                       |
| CMD8 | 0     | 1       | 0          | 0 0        |            | 1    | 0     | 0b0011 2        | Configure peripheral device for next conversion sequence |
|      |       |         |            |            |            |      |       | etc............ | etc............                                          |

CFIFO Header

ADC Command

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## Table 19-57. Example of Command Queue Commands 1

CMDEOQ

1

0

0

0

0

1

0

0b0011

EOQ Message

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

1

0

1

1

1

2

1

3

1

4

1

5

1

6

1

7

1

8

1

9

2

0

2

1

2

2

2

3

2

4

2

5

2

6

2

7

2

8

2

9

3

0

3

1

EOQ

PAUSE

RESERVED

ABORT\_ST

EB (0b1)

BN

CAL

MESSAGE TAG

ADC COMMAND

<!-- image -->

CFIFO Header

ADC Command

- 1 Fields LST, TSR, FMT, and CHANNEL\_NUMBER are not shown for clarity. See Section , ' Conversion Command Message Format for On-Chip ADC Operation,' for details.
- 2 MESSAGE\_TAG field is only defined for read configuration commands.

Step Two: Configure the eDMA to handle data transfers between the command/result queues in RAM and the CFIFOs/RFIFOs in the eQADC.

- 1. For transferring, set the source address of the eDMA TCD n to point to the start address of command queue 1. Set the destination address of the eDMA to point to EQADC\_CFPR1. Refer to Section 19.3.2.4, 'eQADC CFIFO Push Registers 0-5 (EQADC\_CFPRn).'
- 2. For receiving, set the source address of the eDMA TCD n to point to EQADC\_RFPR3. Refer to Section 19.3.2.5, 'eQADC Result FIFO Pop Registers 0-5 (EQADC\_RFPRn).' Set the destination address of the eDMA to point to the starting address of result queue 1.

Step Three: Configure the eQADC control registers.

- 3. Configure Section 19.3.2.7, 'eQADC Interrupt and eDMA Control Registers 0-5 (EQADC\_IDCRn).'
- a) Set EOQIE1 to enable the End of Queue Interrupt request.
- b) Set CFFS1 and RFDS3 to configure the eQADC to generate eDMA requests to push commands into CFIFO1 and to pop result data from RFIF03.
- c) Set CFINV1 to invalidate the contents of CFIFO1.
- d) Set RFDE3 and CFFE1 to enable the eQADC to generate eDMA requests. Command transfers from the RAM to the CFIFO1 will start immediately.
- e) Set RFOIE3 to indicate if RFIFO3 overflows.
- f) Set CFUIE1 to indicate if CFIFO1 underflows.
- 4. Configure MODE1 to continuous-scan rising edge external trigger mode in Section 19.3.2.6, 'eQADC CFIFO Control Registers 0-5 (EQADC\_CFCRn).'

Step Four: Command transfer to ADCs and result data reception.

When an external rising edge event occurs for CFIFO1, the eQADC automatically will begin transferring commands from CFIFO1 when it becomes the highest priority CFIFO trying to send commands to ADC1. The received results will be placed in RFIFO3 and then moved to result queue 1 by the eDMA.

## 19.5.2 EQADC/eDMA Controller Interface

This section provides an overview of the EQADC/eDMA interface and general guidelines about how the eDMA should be configured in order for it to correctly transfer data between the queues in system memory and the EQADC FIFOs.

## 19.5.2.1 Command Queue/CFIFO Transfers

In transfers involving command queues and CFIFOs, the eDMA moves data from a queued source to a single destination as shown in Figure 19-65. The location of the data to be moved is indicated by the source address, and the final destination for that data, by the destination address. The eDMA has transfer control descriptors (TCDs) containing these addresses and other parameters used in the control of data transfers (See  Section 9.3.1.16,  'Transfer  Control  Descriptor  (TCD)'  for  more  information).  For  every  eDMA request issued by the EQADC, the eDMA must be configured to transfer a single command (32-bit data) from the command queue, pointed to by the source address, to the CFIFO push register, pointed to by the destination address. After the service of an eDMA request is completed, the source address has to be updated to point to the next valid command. The destination address remains unchanged. When the last command of a queue is transferred one of the following actions is recommended. Refer to Chapter 9, 'Enhanced Direct Memory Access (eDMA)' for details about how this functionality is supported.

- · The corresponding eDMA channel should be disabled. This might be desirable for CFIFOs in single scan mode.
- · The source address should be updated to pointed to a valid command which can be the first command in the queue that has just been transferred (cyclic queue), or the first command of any other command queue. This is desirable for CFIFOs in continuous scan mode, or in some cases, for CFIFOs in single scan mode.

Figure 19-65. Command Queue/CFIFO Interface

<!-- image -->

## 19.5.2.2 Receive Queue/RFIFO Transfers

In transfers involving receive queues and RFIFOs, the eDMA controller moves data from a single source to a queue destination as shown in Figure 19-66. The location of the data to be moved is indicated by the source address, and the final destination for that data, by the destination address. For every eDMA request issued by the EQADC, the eDMA controller has to be configured to transfer a single result (16-bit data), pointed to by the source address, from the RFIFO pop register to the receive queue, pointed to by the destination address. After the service of an eDMA request is completed, the destination address has to be updated to point to the location where the next 16-bit result will be stored. The source address remains unchanged. When the last expected result is written to the receive queue, one of the following actions is recommended. Refer to Chapter 9, 'Enhanced Direct Memory Access (eDMA)' for details about how this functionality is supported.

- · The corresponding eDMA channel should be disabled.
- · The destination address should be updated pointed to the next location where new coming results are stored, which can be the first entry of the current receive queue (cyclic queue), or the beginning of a new receive queue.

Figure 19-66. Receive Queue/RFIFO Interface

<!-- image -->

## 19.5.3 Sending Immediate Command Setup Example

In the eQADC, there is no immediate command register for sending a command immediately after writing to  that  register.  However,  a  CFIFO  can  be  configured  to  perform  the  same  function  as  an  immediate command register. The following steps illustrate how to configure CFIFO5 as an immediate command CFIFO. This eliminates the use of the eDMA. The results will be returned to RFIFO5.

- 1. Configure the Section 19.3.2.7, 'eQADC Interrupt and eDMA Control Registers 0-5 (EQADC\_IDCRn).'
- a) Clear CFIFO fill enable5 (CFFE5 = 0) in EQADC\_IDCR5.
- b) Clear CFIFO underflow interrupt enable5 (CFUIE5 = 0) in EQADC\_IDCR2.
- c) Clear RFDS5 to configure the eQADC to generate interrupt requests to pop result data from RFIF05.
- d) Set RFIFO drain enable5 (RFDE5 = 1) in EQADC\_IDCR5.
- 2. Configure the Section 19.3.2.6, 'eQADC CFIFO Control Registers 0-5 (EQADC\_CFCRn).'
- a) Write 1 to CFINV5 in EQADC\_CFCR5. This will invalidate the contents of CFIFO5.
- b) Set MODE5 to continuous-scan software trigger mode in EQADC\_CFCR5.
- 3. To transfer a command, write it to the eQADC CFIFO push register 5 (EQADC\_CFPR5) with message tag = 0b0101. Refer to Section 19.3.2.4, 'eQADC CFIFO Push Registers 0-5 (EQADC\_CFPRn).'
- 4. Up to 4 commands can be queued in CFIFO5. Check the CFCTR5 status in EQADC\_FISR5 before pushing another command to avoid overflowing the CFIFO. Refer to Section 19.3.2.8, 'eQADC FIFO and Interrupt Status Registers 0-5 (EQADC\_FISRn).'
- 5. When the eQADC receives a conversion result for RFIFO5, it generates an interrupt request. RFIFO pop register 5 (EQADC\_RFPR5) can be popped to read the result. Refer to Section 19.3.2.5, 'eQADC Result FIFO Pop Registers 0-5 (EQADC\_RFPRn).'

## 19.5.4 Modifying Queues

More command queues may be needed than the six supported by the eQADC. These additional command queues  can  be  supported  by  interrupting  command  transfers  from  a  configured  CFIFO,  even  if  it  is triggered  and  transferring,  modifying  the  corresponding  command  queue  in  the  RAM  or  associating another command queue to it, and restarting the CFIFO. More details on disabling a CFIFO are described in Section 19.4.3.5.1, 'Disabled Mode.'

- 1. Determine the resumption conditions when later resuming the scan of the command queue at the point before it was modified.
- a) Change EQADC\_CFCRn[MODE ] (see Section 19.3.2.6) to disabled. Refer to n Section 19.4.3.5.1, 'Disabled Mode,' for a description of what happens when MODE n is changed to disabled.
- b) Poll EQADC\_CFSR[CFS ] until it becomes IDLE (see Section 19.3.2.11). n
- c) Read and save EQADC\_CFTCRn[TC\_CF ] (see Section 19.3.2.9) for later resuming the scan n of the queue. The TC\_CF n provides the point of resumption.
- d) Since all result data may not have being stored in the appropriate RFIFO at the time MODE n is changed to disable, wait for all expected results to be stored in the RFIFO/result queue before reconfiguring the eDMA to work with the modified result queue. The number of results that must return can be estimated from the TC\_CF n value obtained above.
- 2. Disable the eDMA from responding to the eDMA request generated by EQADC\_FISRn[CFFF n ] and EQADC\_FISRn[RFDF ] (see Section 19.3.2.8). n
- 3. Write '0x0000' to the TC\_CF n field.
- 4. Load the new configuration and conversion commands into RAM. Configure the eDMA to support the new command/result queue, but do not configure it yet to respond to eDMA requests from CFIFO /RFIFO . n n
- 5. If necessary, modify the EQADC\_IDCRn registers (see Section 19.3.2.7) to suit the modified command queue.
- 6. Write 1 to EQADC\_CFCRn[CFINV ] (see Section 19.3.2.6) to invalidate the entries of CFIFO n n .
- 7. Configure the eDMA to respond to eDMA requests generated by CFFF n and RFDF n .
- 8. Change MODE  to the modified CFIFO operation mode. Write 1 to SSE n n to trigger CFIFO n if MODE  is software trigger. n

## 19.5.5 Command Queue and Result Queue Usage

Figure 19-67 is an example of command queue and result queue usage. It shows the command queue 0 commands requesting results that will be stored in result queue 0 and result queue 1, and command queue 1 commands requesting results that will be stored only in result queue 1. Some command messages request data to be returned from the on-chip ADC/external device, but some only configure them and do not request returning data. When a command queue contains both write and read commands like command queue 0, the command queue and result queue entries will not be aligned, in Figure 19-67, the result for the second command of command queue 0 is the first entry of result queue 0. The figure also shows that command queue and result queue entries can also become unaligned even if all commands in a command queue request data as command queue 1. Command queue 1 entries became unaligned to result queue 1 entries because a result requested by the forth command queue 0 command was sent to result queue 1. This happens because the system can be configured so that several command queues can have results sent to a single result queue.

## Command Queue 0 (CQueue0)

<!-- image -->

## Result Queue 0 (RQueue0)

Figure 19-67. eQADC Command and Result Queues

## 19.5.6 ADC Result Calibration

The ADC result calibration process consists of two steps: determining the gain and offset calibration constants, and calibrating the raw results generated by the on-chip ADCs by solving the following equation discussed in Section 19.4.5.4.1, 'Calibration Overview.'

<!-- formula-not-decoded -->

The calibration constants GCC and OCC can be calculated from equation (5.5.a) provided that two pairs of expected (CAL\_RES) and measured (RAW\_RES) result values are available for two different input voltages. Most likely calibration points to be used are 25% VREF  and 75% VREF since they are far apart 1 but not too close to the end points of the full input voltage range. This allows for calculations of more representative calibration constants. The eQADC provides these voltages via channel numbers 43 and 44. The raw, uncalibrated results for these input voltages are obtained by converting these channels with conversion commands that have the CAL bit negated.

1.VREF=V RH -V RL

## Enhanced Queued Analog-to-Digital Converter (eQADC)

The transfer equations for when sampling these reference voltages are:

```
CAL_RES 75%VREF  = GCC * RAW_RES 75%VREF  + OCC +2;
```

(5.5.b)

<!-- formula-not-decoded -->

GCC = (CAL\_RES 75%VREF  - CAL\_RES 25%VREF  ) / (RAW\_RES 75%VREF  - RAW\_RES 25%VREF  );

(5.5.d)

OCC = CAL\_RES 75%VREF  - GCC*RAW\_RES 75%VREF  - 2   ;

(5.5.e)

Thus;

or

<!-- formula-not-decoded -->

After being calculated, the GCC and OCC values must be written to ADC0\_GCCR and ADC1\_GCCR registers (see Section 19.3.3.4) and the ADC0\_OCCR and ADC1\_OCCR registers (see Section 19.3.3.5) using write configuration commands.

The eQADC will automatically calibrate the results, according to equation (5.5.a), of every conversion command that has its CAL bit asserted using the GCC and OCC values stored in the ADC calibration registers.

## 19.5.6.1 MAC Configuration Procedure

The following steps illustrate how to configure the calibration hardware, that is, determining the values of the gain and offset calibration constants, and the writing these constants to the calibration registers. This procedure should be performed for both ADC0 and ADC1.

- 1. Convert channel 44 with a command that has its CAL bit negated and obtain the raw, uncalibrated result for 25%VREF (RAW\_RES 25%VREF ).
- 2. Convert channel 43 with a command that has its CAL bit negated and obtain the raw, uncalibrated result for 75%VREF (RAW\_RES 75%VREF ).
- 3. Because the expected values for the conversion of these voltages are known (CAL\_RES 25%VREF and CAL\_RES 75%VREF ), GCC and OCC values can be calculated from equations (5.5.d) and (5.5.e) using these values, and the results determined in steps 1 and 2.
- 4. Reformat GCC and OCC to the proper data formats as specified in Section 19.4.5.4.2, 'MAC Unit and Operand Data Format.' GCC is an unsigned 15-bit fixed point value and OCC is a signed 14-bit value.
- 5. Write the GCC value to ADCn gain calibration registers (see Section 19.3.3.4) and the OCC value to ADCn offset calibration constant registers (see Section 19.3.3.5) using write configuration commands.

## 19.5.6.2 Example Calculation of Calibration Constants

The raw results obtained when sampling reference voltages 25%VREF and 75%VREF were, respectively, 3798  and  11592.  The  results  that  should  have  been  obtained  from  the  conversion  of  these  reference voltages are, respectively, 4096 and 12288. Therefore, using equations (5.5.d) and (5.5.e), the gain and offset calibration constants are:

```
GCC=(12288-4096)/(11592-3798) = 1.05106492-> 1.05102539 1  = 0x4344 OCC=12288-1.05106492*11592 -2 = 102.06-> 102 = 0x0066
```

1. This calculation is rounded down due to binary approximation.

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 19-58 shows, for this particular case, examples of how the result values change according to GCC and OCC when result calibration is executed (CAL=1) and when it is not (CAL=0).

Table 19-58. Calibration Example

|               | Raw result (CAL=0)   | Raw result (CAL=0)   | Calibrated result (CAL=1)   | Calibrated result (CAL=1)   |
|---------------|----------------------|----------------------|-----------------------------|-----------------------------|
| Input Voltage | Hexadecimal          | Decimal              | Hexadecimal                 | Decimal                     |
| 25% VREF      | 0x0ED6               | 3798                 | 0x1000                      | 4095.794                    |
| 75% VREF      | 0x2D48               | 11592                | 0x3000                      | 12287.486                   |

## 19.5.6.3 Quantization Error Reduction During Calibration

Figure 19-68 shows how the ADC transfer curve changes due to the addition of two to the MAC output during the calibration - see MAC output equation in Section 19.4.5.4, 'ADC Calibration Feature ' . The maximum absolute quantization error is reduced by half leading to an increase in accuracy.

<!-- image -->

-4

Figure 19-68. Quantization Error Reduction During Calibration

## 19.5.7 eQADC versus QADC

This section describes how the eQADC upgrades the QADC functionality. The section also provides a comparison between the eQADC and QADC in terms of their functionality. This section targets users familiar with terminology in QADC. Figure 19-69 is an overview of a QADC. Figure 19-70 is an overview of the eQADC system.

<!-- image -->

Figure 19-69. QADC Overview

<!-- image -->

Hardware in eQADC that was not present in QADC

Figure 19-70. eQADC System Overview

The eQADC system consists of four parts: queues in system memory, the eQADC, on-chip ADCs, and an external device. As compared with the QADC, the eQADC system requires two pieces of extra hardware.

- 1. An eDMA or an MCU is required to move data between the eQADC's FIFOs and queues in the system memory.
- 2. A serial interface [eQADC synchronous serial interface (SSI)]is implemented to transmit and receive data between the eQADC and the external device.

Because there are only FIFOs inside the eQADC, much of the terminology or use of the register names, register contents, and signals of the eQADC involve FIFO instead of queue. These register names, register contents, and signals are functionally equivalent to the queue counterparts in the QADC. Table 19-59 lists how the eQADC register, register contents, and signals are related to QADC.

.

Table 19-59. Terminology Comparison between QADC and eQADC

| QADC Terminology                     | eQADC Terminology                                                    | Function                                                                                                                                                                                                                                                                                                                                           |
|--------------------------------------|----------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| CCW                                  | Command Message                                                      | In the QADC, the hardware only executes conversion command words. In the eQADC, not all commands are conversion commands; some are configuration commands.                                                                                                                                                                                         |
| Queue Trigger                        | CFIFO Trigger                                                        | In the QADC, a trigger event is required to start the execution of a queue. In the eQADC, a trigger event is required to start command transfers from a CFIFO. When a CFIFO is triggered and transferring, commands are continuously moved from command queues to CFIFOs. Thus, the trigger event initiates the 'execution of a queue' indirectly. |
| CommandWordPointer Queue n (CWPQ n ) | Counter Value of Commands Transferred from Command FIFO n (TC_CF n ) | In the QADC, CWPQ n allows the last executed command on queue n to be determined. In the eQADC, the TC_CF n value allows the last transferred command on command queue n to be determined.                                                                                                                                                         |
| Queue Pause Bit (P)                  | CFIFO Pause Bit                                                      | In the QADC, detecting a pause bit in the CCW will pause the queue execution. In the eQADC, detecting a pause bit in the command will pause command transfers from a CFIFO.                                                                                                                                                                        |
| Queue Operation Mode (MQ n )         | CFIFO Operation Mode (MODE n )                                       | The eQADC supports all queue operation modes in the QADC except operation modes related to a periodic timer. A timer elsewhere in the system can provide the same functionality if it is connected to ETRIG n .                                                                                                                                    |
| Queue Status (QS)                    | CFIFO Status (CFS n )                                                | In the QADC, the queue status is read to check whether a queue is idle, active, paused, suspended, or trigger pending. In the eQADC,the CFIFO status is read to check whether a queue is IDLE, WAITING FOR TRIGGER (idle or paused in QADC), or triggered (suspended or trigger pending in QADC).                                                  |

The eQADC and QADC also have similar procedures for the configuration or execution of applications. Table 19-60 shows the steps required for the QADC versus the steps required for the eQADC system.

Table 19-60. Usage Comparison between QADC and eQADC System

| Procedure                                   | QADC                                                                  | eQADC System                                                                        |
|---------------------------------------------|-----------------------------------------------------------------------|-------------------------------------------------------------------------------------|
| Analog Control Configuration                | Configure analog device by writing to the QADCs.                      | Program configuration commands into command queues.                                 |
| Prepare Scan Sequence                       | Program scan commands into command queues.                            | Program scan commands into command queues.                                          |
| Queue Control Configuration                 | Write to the QADC control registers.                                  | Write to the eQADC control registers.                                               |
| Data Transferred between Queues and Buffers | Not Required.                                                         | Program the eDMA or the CPU to handle the data transfer.                            |
| Serial Interface Configuration              | Not Required.                                                         | Write to the eQADC SSI registers.                                                   |
| Queue Execution                             | Require software or external trigger events to start queue execution. | Require software or external trigger events to start commandtransfers from a CFIFO. |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## 19.6 Revision History

## Substantive Changes since Rev 3.0

Changed Section 19.4.9.1, 'Reference Bypass,' to say only 'The reference bypass capacitor (REFBYPC) signal requires a 100 nF capacitor connected to VRL to filter noise on the internal reference used by the ADC.' Also changed Figure 19-59 to just show the bypass cap. Changed section title and figure title from 'Bias Generator' to 'Reference Bypasst'.

Added footnote to Table 19-51: 'This equation only applies before calibration. After calibration, the 50% reference point will actually return approximately 20mV lower than the expected 50% of the difference between the High Reference Voltage (VRH) and the Low Reference Voltage (VRL). For calibration of the ADC only the 25% and 75% points should be used as described in Section 19.5.6.1, 'MAC Configuration Procedure'
