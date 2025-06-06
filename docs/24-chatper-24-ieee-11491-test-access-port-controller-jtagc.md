### Chatper 24 IEEE 1149.1 Test Access Port Controller (JTAGC)

## 24.1 Introduction

The JTAG port of the MPC5553/MPC5554 consists of four inputs and one output. These pins include JTAG compliance select (JCOMP), test data input (TDI), test data output (TDO), test mode select (TMS), and test clock input (TCK). TDI, TDO, TMS, and TCK are compliant with the IEEE 1149.1-2001 standard and are shared with the NDI through the test access port (TAP) interface.

## 24.1.1 Block Diagram

Figure 24-1 is a block diagram of the JTAG Controller (JTAGC).

Figure 24-1. JTAG Controller Block Diagram

<!-- image -->

## 24.1.2 Overview

The JTAGC provides the means to test chip functionality and connectivity while remaining transparent to system logic when not in test mode. Testing is performed via a boundary scan technique, as defined in the IEEE 1149.1-2001 standard. In addition, instructions can be executed that allow the Test Access Port (TAP) to be shared with other modules on the MCU. All data input to and output from the JTAGC is communicated in serial format.

## 24.1.3 Features

The JTAGC is compliant with the IEEE 1149.1-2001 standard, and supports the following features:

- · IEEE 1149.1-2001 Test Access Port (TAP) interface. - 4 pins (TDI, TMS, TCK, and TDO),  See Section 24.2, 'External Signal Description.'
- · A JCOMP input that provides the ability to share the TAP.
- · A 5-bit instruction register that supports several IEEE 1149.1-2001 defined instructions, as well as several public and private MPC5553/MPC5554 specific instructions.
- · Four test data registers: a bypass register, a boundary scan register, and a device identification register. The size of the boundary scan register is 464 bits.
- · A TAP controller state machine that controls the operation of the data registers, instruction register and associated circuitry.

## 24.1.4 Modes of Operation

The JTAGC uses JCOMP and a power-on reset indication as its primary reset signals. Several IEEE 1149.1-2001 defined test modes are supported, as well as a bypass mode.

## 24.1.4.1 Reset

The JTAGC is placed in reset when the TAP controller state machine is in the TEST-LOGIC-RESET state. The TEST-LOGIC-RESET state is entered upon the assertion of the power-on reset signal, negation of JCOMP, or through TAP controller state machine transitions controlled by TMS. Asserting power-on reset or negating JCOMP results in asynchronous entry into the reset state. While in reset, the following actions occur:

- · The TAP controller is forced into the test-logic-reset state, thereby disabling the test logic and allowing normal operation of the on-chip system logic to continue unhindered.
- · The instruction register is loaded with the IDCODE instruction.

In addition, execution of certain instructions can result in assertion of the internal system reset. These instructions include EXTEST, CLAMP, and HIGHZ.

## 24.1.4.2 IEEE 1149.1-2001 Defined Test Modes

The JTAGC supports several IEEE 1149.1-2001 defined test modes. The test mode is selected by loading the  appropriate  instruction  into  the  instruction  register  while  the  JTAGC  is  enabled.  Supported  test instructions include EXTEST, HIGHZ, CLAMP, SAMPLE and SAMPLE/PRELOAD. Each instruction defines the set of data registers that may operate and interact with the on-chip system logic while the instruction is current. Only one test data register path is enabled to shift data between TDI and TDO for each instruction.

The  boundary  scan  register  is  enabled  for  serial  access  between  TDI  and  TDO  when  the  EXTEST, SAMPLE or SAMPLE/PRELOAD instructions are active. The single-bit bypass register shift stage is enabled for serial access between TDI and TDO when the HIGHZ, CLAMP or reserved instructions are active.  The  functionality  of  each  test  mode  is  explained  in  more  detail  in  Section 24.4.4,  'JTAGC Instructions.'

## 24.1.4.3 Bypass Mode

When no test operation is required, the BYPASS instruction can be loaded to place the JTAGC into bypass mode. While in bypass mode, the single-bit bypass shift register is used to provide a minimum-length serial path to shift data between TDI and TDO.

## 24.1.4.4 TAP Sharing Mode

On the MPC5553/MPC5554, there are four selectable auxiliary TAP controllers that share the TAP with the  JTAGC.  Selectable  TAP  controllers  include  the  Nexus  port  controller  (NPC),  e200  OnCE,  eTPU Nexus, and eDMA Nexus. The instructions required to grant ownership of the TAP to the auxiliary TAP controllers are ACCESS\_AUX\_TAP\_NPC, ACCESS\_AUX\_TAP\_ONCE, ACCESS\_AUX\_TAP\_eTPUN3,  and  ACCESS\_AUX\_TAP\_DMAN3.  Instruction  opcodes  for  each instruction are shown in Table 24-3.

When the access instruction for an auxiliary TAP is loaded, control of the JTAG pins is transferred to the selected TAP controller. Any data input via TDI and TMS is passed to the selected TAP controller, and any TDO output from the selected TAP controller is sent back to the JTAGC to be output on the pins. The

JTAGC regains control  of  the  JTAG  port  during  the  UPDATE-DR  state  if  the  PAUSE-DR  state  was entered. Auxiliary TAP controllers are held in RUN-TEST/IDLE while they are inactive.

For more information on the TAP controllers see Chapter 25, 'Nexus Development Interface.'

## 24.2 External Signal Description

## 24.2.1 Overview

The JTAGC consists of five signals that connect to off-chip development tools and allow access to test support functions. The JTAGC signals are outlined in Table 24-1.

Table 24-1. JTAG Signal Properties

| Name   | I/O   | Function         | Reset State   | Pull 1   |
|--------|-------|------------------|---------------|----------|
| TCK    | I     | Test Clock       | -             | Down     |
| TDI    | I     | Test Data In     | -             | Up       |
| TDO    | O     | Test Data Out    | High Z 2      | Down 2   |
| TMS    | I     | Test Mode Select | -             | Up       |
| JCOMP  | I     | JTAG Compliancy  | -             | Down     |

1 The pull is not implemented in this module. Pull-up/pull-down devices are implemented in the pads.

2 TDO output buffer enable is negated when JTAGC is not in the Shift-IR or Shift-DR states. A weak pull-down may be implemented on TDO.

## 24.3 Register Definition

This section provides a detailed description of the JTAGC registers accessible through the TAP interface, including data registers and the instruction register. Individual bit-level descriptions and reset states of each register are included. These registers are not memory-mapped and can only be accessed through the TAP.

## 24.3.1 Register Descriptions

The JTAGC  registers are described in this section.

## 24.3.1.1 Instruction Register

The JTAGC uses a 5-bit instruction register  as  shown  in  Figure 24-2.  The  instruction  register  allows instructions to be loaded into the module to select the test to be performed or the test data register to be accessed or both. Instructions are shifted in through TDI while the TAP controller is in the Shift-IR state, and latched on the falling edge of TCK in the Update-IR state. The latched instruction value can only be changed  in  the  Update-IR  and  Test-Logic-Reset  TAP  controller  states.  Synchronous  entry  into  the test-logic-reset  state  results  in  the  IDCODE  instruction  being  loaded  on  the  falling  edge  of  TCK. Asynchronous  entry  into  the  test-logic-reset  state  results  in  asynchronous  loading  of  the  IDCODE instruction. During the capture-IR TAP controller state, the instruction shift register is loaded with the value 0b10101, making this value the register's read value when the TAP controller is sequenced into the Shift-IR state.

Figure 24-2. 5-Bit Instruction Register

<!-- image -->

## 24.3.1.2 Bypass Register

The bypass register is a single-bit shift register path selected for serial data transfer between TDI and TDO when the BYPASS, CLAMP, HIGHZ or reserve instructions are active. After entry into the capture-DR state, the single-bit shift register is set to a logic 0. Therefore, the first bit shifted out after selecting the bypass register is always a logic 0.

## 24.3.1.3 Device Identification Register

The device identification register, shown in Figure 24-3, allows the part revision number, design center, part identification number, and manufacturer identity code to be determined through the TAP. The device identification  register  is  selected  for  serial  data  transfer  between  TDI  and  TDO  when  the  IDCODE instruction is active. Entry into the capture-DR state while the device identification register is selected loads the IDCODE into the shift register to be shifted out on TDO in the Shift-DR state. No action occurs in the update-DR state.

Figure 24-3. Device Identification Register

<!-- image -->

Table 24-2. Device Identification Register Field Descriptions

| Bits   | Name   | Description                                                                                                                                 |
|--------|--------|---------------------------------------------------------------------------------------------------------------------------------------------|
| 0-3    | PRN    | Part revision number. Contains the revision number of the device. This field changes with each revision of the device or module.            |
| 4-9    | DC     | Design center. Indicates the Freescale design center. For both the MPC5554 and MPC5553, this value is 0x20.                                 |
| 10-19  | PIN    | Part identification number. Contains the part number of the device. For the MPC5554, this value is 0x0, for the MPC5553 this value is 0x53. |
| 20-30  | MIC    | Manufacturer identity code. Contains the reduced Joint Electron Device Engineering Council (JEDEC) ID for Freescale, 0xE.                   |
| 31     | -      | IDCODE register ID. Identifies this register as the device identification register and not the bypass register. Always set to 1.            |

## 24.3.1.4 Boundary Scan Register

The  boundary  scan  register  is  connected  between  TDI  and  TDO  when  the  EXTEST,  SAMPLE  or SAMPLE/PRELOAD instructions are active. It is used to capture input pin data, force fixed values on output pins, and select a logic value and direction for bidirectional pins. Each bit of the boundary scan register represents a separate boundary scan register cell, as described in the IEEE 1149.1-2001 standard and discussed in Section 24.4.5, 'Boundary Scan.' The size of the boundary scan register is 464 bits for the MPC5554, and 392 bits for the MPC5553.

## 24.4 Functional Description

## 24.4.1 JTAGC Reset Configuration

While in reset, the TAP controller is forced into the test-logic-reset state, thus disabling the test logic and allowing normal operation of the on-chip system logic. In addition, the instruction register is loaded with the IDCODE instruction.

## 24.4.2 IEEE 1149.1-2001 (JTAG) Test Access Port

The JTAGC uses the IEEE 1149.1-2001 TAP for accessing registers. This port can be shared with other TAP controllers on the MCU. Ownership of the port is determined by the value of the JCOMP signal and the  currently  loaded  instruction.  For  more  detail  on  TAP  sharing  via  JTAGC  instructions  refer  to Section 24.4.4.2, 'ACCESS\_AUX\_TAP\_x Instructions.'

Data is shifted between TDI and TDO though the selected register starting with the least significant bit, as illustrated  in  Figure 24-4.  This  applies  for  the  instruction  register,  test  data  registers,  and  the  bypass register.

Figure 24-4. Shifting Data Through a Register

<!-- image -->

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## 24.4.3 TAP Controller State Machine

The TAP controller is a synchronous state machine that interprets the sequence of logical values on the TMS pin. Figure 24-5 shows the machine's states. The value shown next to each state is the value of the TMS signal sampled on the rising edge of the TCK signal. As Figure 24-5 shows, holding TMS at logic 1 while clocking TCK through a sufficient number of rising edges also causes the state machine to enter the test-logic-reset state.

NOTE: The value shown adjacent to each state transition in this figure represents the value of TMS at the time of a rising edge of TCK.

<!-- image -->

Figure 24-5. IEEE 1149.1-2001 TAP Controller Finite State Machine

## 24.4.3.1 Enabling the TAP Controller

The JTAGC TAP controller is enabled by setting JCOMP to a logic 1 value.

## 24.4.3.2 Selecting an IEEE 1149.1-2001 Register

Access to the JTAGC data registers is achieved by loading the instruction register with any of the JTAGC instructions while the JTAGC is enabled. Instructions are shifted in via the select-ir-scan path and loaded in the update-IR state. At this point, all data register access is performed via the select-dr-scan path.

The select-dr-scan path is used to read or write the register data by shifting in the data (lsb first) during the shift-DR state. When reading a register, the register value is loaded into the IEEE 1149.1-2001 shifter during the capture-DR state. When writing a register, the value is loaded from the IEEE 1149.1-2001 shifter to the register during the update-DR state. When reading a register, there is no requirement to shift out the entire register contents. Shifting may be terminated once the required number of bits have been acquired.

## 24.4.4 JTAGC Instructions

The JTAGC implements the IEEE 1149.1-2001 defined instructions listed in Table 24-3. This section gives an overview of each instruction, refer to the IEEE 1149.1-2001 standard for more details.

Table 24-3. JTAG Instructions

| Instruction              | Code[4:0]           | Instruction Summary                                                                                           |
|--------------------------|---------------------|---------------------------------------------------------------------------------------------------------------|
| IDCODE                   | 00001               | Selects device identification register for shift                                                              |
| SAMPLE/PRELOAD           | 00010               | Selects boundary scan register for shifting, sampling, and preloading without disturbing functional operation |
| SAMPLE                   | 00011               | Selects boundary scan register for shifting and sampling without disturbing functional operation              |
| EXTEST                   | 00100               | Selects boundary scan register while applying preloaded values to output pins and asserting functional reset  |
| HIGHZ                    | 01001               | Selects bypass register while three-stating all output pins and asserting functional reset                    |
| CLAMP                    | 01100               | Selects bypass register while applying preloaded values to output pins and asserting functional reset         |
| ACCESS_AUX_TAP_NPC       | 10000               | Grants the Nexus port controller (NPC) ownership of the TAP                                                   |
| ACCESS_AUX_TAP_ONCE      | 10001               | Grants the Nexus e200z6 core interface (NZ6C3) ownership of the TAP                                           |
| ACCESS_AUX_TAP_eTPUN3    | 10010               | Grants the Nexus dual-eTPU development interface (NDEDI) ownership of the TAP                                 |
| ACCESS_AUX_TAP_DMAN3     | 10011               | Grants the Nexus crossbar DMA interface (NXDM) ownership of the TAP                                           |
| BYPASS                   | 11111               | Selects bypass register for data operations                                                                   |
| Factory Debug Reserved 1 | 00101, 00110, 01010 | Intended for factory debug only                                                                               |
| Reserved 2               | All Other Codes     | Decoded to select bypass register                                                                             |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

- 1 Intended for factory debug, and not customer use
- 2 Freescale reserves the right to change the decoding of reserved instruction codes in the future

## 24.4.4.1 BYPASS Instruction

BYPASS selects  the  bypass  register,  creating  a  single-bit  shift  register  path  between  TDI  and  TDO. BYPASS enhances test efficiency by reducing the overall shift path when no test operation of the MCU is required. This allows more rapid movement of test data to and from other components on a board that are required to perform test functions. While the BYPASS instruction is active the system logic operates normally.

## 24.4.4.2 ACCESS\_AUX\_TAP\_x Instructions

The ACCESS\_AUX\_TAP\_x instructions allow the Nexus modules on the MCU to take control of the TAP. When this instruction  is  loaded,  control  of  the  TAP  pins  is  transferred  to  the  selected  auxiliary  TAP controller. Any data input via TDI and TMS is passed to the selected TAP controller, and any TDO output from the selected TAP controller is sent back to the JTAGC to be output on the pins. The JTAGC regains control of the JTAG port during the UPDATE-DR state if the PAUSE-DR state was entered. Auxiliary TAP controllers are held in RUN-TEST/IDLE while they are inactive.

## 24.4.4.3 CLAMP Instruction

CLAMP allows the state of signals driven from MCU pins to be determined from the boundary scan register while the bypass register is selected as the serial path between TDI and TDO. CLAMP enhances test efficiency by reducing the overall shift path to a single bit (the bypass register) while conducting an EXTEST type of instruction through the boundary scan register. CLAMP also asserts the internal system reset for the MCU to force a predictable internal state.

## 24.4.4.4 EXTEST - External Test Instruction

EXTEST selects the boundary scan register as the shift path between TDI and TDO. It allows testing of off-chip circuitry and board-level interconnections by driving preloaded data contained in the boundary scan register onto the system output pins. Typically, the preloaded data is loaded into the boundary scan register using the SAMPLE/PRELOAD instruction before the selection of EXTEST. EXTEST asserts the internal system reset for the MCU to force a predictable internal state while performing external boundary scan operations.

## 24.4.4.5 HIGHZ Instruction

HIGHZ selects the bypass register as the shift path between TDI and TDO. While HIGHZ is active, all output drivers are placed in an inactive drive state (for example, high impedance). HIGHZ also asserts the internal system reset for the MCU to force a predictable internal state.

## 24.4.4.6 IDCODE Instruction

IDCODE selects the 32-bit device identification register as the shift path between TDI and TDO. This instruction allows interrogation of the MCU to determine its version number and other part identification data. IDCODE is the instruction placed into the instruction register when the JTAGC is reset.

## 24.4.4.7 SAMPLE Instruction

The SAMPLE instruction obtains a sample of the system data and control signals present at the MCU input pins and just before the boundary scan register cells at the output pins. This sampling occurs on the rising edge of TCK in the capture-DR state when the SAMPLE instruction is active. The sampled data is viewed by shifting it through the boundary scan register to the TDO output during the Shift-DR state. There is no defined action in the update-DR state. Both the data capture and the shift operation are transparent to system operation.

## 24.4.4.8 SAMPLE/PRELOAD Instruction

The SAMPLE/PRELOAD instruction has two functions:

- · First, the SAMPLE portion of the instruction obtains a sample of the system data and control signals present at the MCU input pins and just before the boundary scan register cells at the output pins. This sampling occurs on the rising edge of TCK in the capture-DR state when the SAMPLE/PRELOAD instruction is active. The sampled data is viewed by shifting it through the boundary scan register to the TDO output during the shift-DR state. Both the data capture and the shift operation are transparent to system operation.
- · Secondly, the PRELOAD portion of the instruction initializes the boundary scan register cells before selecting the EXTEST or CLAMP instructions to perform boundary scan tests. This is achieved by shifting in initialization data to the boundary scan register during the shift-DR state. The initialization data is transferred to the parallel outputs of the boundary scan register cells on the falling edge of TCK in the update-DR state. The data is applied to the external output pins by the EXTEST or CLAMP instruction. System operation is not affected.

## 24.4.5 Boundary Scan

The  boundary  scan  technique  allows  signals  at  component  boundaries  to  be  controlled  and  observed through the shift-register stage associated with each pad. Each stage is part of a larger boundary scan register cell, and cells for each pad are interconnected serially to form a shift-register chain around the border of the design. The boundary scan register consists of this shift-register chain, and is connected between TDI and TDO when the EXTEST, SAMPLE, or SAMPLE/PRELOAD instructions are loaded. The shift-register chain contains a serial input and serial output, as well as clock and control signals.

## 24.5 Initialization/Application Information

The test logic is a static logic design, and TCK can be stopped in either a high or low state without loss of data. However, the system clock is not synchronized to TCK internally. Any mixed operation using both the test logic and the system functional logic requires external synchronization.

To initialize the JTAGC module and enable access to registers, the following sequence is required:

- 1. Set the JCOMP signal to logic 1, thereby enabling the JTAGC TAP controller.
- 2. Load the appropriate instruction for the test or action to be performed.

## 24.6 Revision History

Substantive Changes since Rev 3.0

No changes.

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

IEEE 1149.1 Test Access Port Controller (JTAGC)
