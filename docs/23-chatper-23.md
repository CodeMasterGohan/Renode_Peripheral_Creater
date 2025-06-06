### Chatper 23

## Voltage Regulator Controller (VRC) and POR Module

## 23.1 Introduction

The voltage regulator controller (VRC) and POR module contains circuitry to control regulation of the external 1.5-V supply used by the device. It also contains power-on reset (POR) circuits for the 1.5-V supply, V DDSYN  and the VDDE supply that powers the RESET pad.

## 23.1.1 Block Diagram

The block diagram of the VRC and POR module is shown in Figure 23-1. The diagram represents the various submodules as implemented on the MPC5553/MPC5554.

Figure 23-1. Voltage Regulator Controller and POR Blocks

<!-- image -->

## 23.2 External Signal Description

Table 23-1 provides an overview of VRC signals.

Table 23-1. Voltage Regulator Controller and POR Block External Signals

| Signal   | Type           | Signal Level   | Description                                                                         |
|----------|----------------|----------------|-------------------------------------------------------------------------------------|
| V RC33   | Supply pin     | 3.3V           | Regulator supply input                                                              |
| V DDSYN  | Supply pin     | 3.3V           | FMPLL supply input                                                                  |
| V DDEH6  | Supply pin     | 3.3/5.0V       | RESET pin supply input                                                              |
| V RCVSS  | Supply pin     | 0V             | Regulator supply ground                                                             |
| VRCSNS   | 1.5-V Sense    | 1.5V           | 1.5-V Sense used by VRC. Pad connected to V DD plane in package-not a package ball. |
| V RCCTL  | Current output | -              | Regulator control output                                                            |

## 23.2.1 Detailed Signal Description

The following paragraphs provide descriptions of signals coming into and going out of the VRC.

## 23.2.1.1 VRC33

3.3V VRC supply input.

## 23.2.1.2 VDDSYN

3.3V supply input for FMPLL.

## 23.2.1.3 VDDEH6

Power supply input for padring segment that contains the RESET pad.

## 23.2.1.4 VRCVSS

3.3V VRC ground supply.

## 23.2.1.5 VRCSNS

1.5V sense from external 1.5-V supply output of NPN transistor. This input is monitored by the VRC to determine current value for V RCCTL . VRCSNS is a pad on the die that is connected to a V DD  plane inside the package. It is not a package ball.

## 23.2.1.6 VRCCTL

The V RCCTL  sources base current to the external bypass transistor. The V RCCTL  signal is used with internal and external transistors to provide V DD , which is the MCU's 1.5V power supply.

## 23.2.1.7 VDD

Internal 1.5V supply input.

## 23.3 Memory Map/Register Definition

The VRC and POR module has no memory-mapped registers.

## 23.4 Functional Description

The VRC portion of the module contains a voltage regulator controller, and the POR portion contains circuits to monitor the voltage levels of the 1.5V and V DDSYN  supplies as well as circuits to monitor the supply that powers the RESET pad. The PORs indicate whether each monitored supply is above a specified voltage  threshold.  These  PORs  are  used  to  ensure  that  the  device  is  correctly  powered  up  during  a power-on reset. The MPC5553/MPC5554 resets the device if any of the supplies are below the specified minimum.

## 23.4.1 Voltage Regulator Controller

The VRC circuit provides a control current that can be used with an external NPN transistor and an external resistor to provide the 1.5V V DD  supply. The control current is output on the V RCCTL  pin. The voltage regulator controller begins to turn the pass transistor on slowly while the 3.3V POR still is asserted. The pass transistor will be completely turned on when the 3.3V POR negates.

## NOTE

The voltage regulator controller will keep the 1.5V supply in regulation as long as V RC33  is in regulation. If more protection is desired, the customer may also supply an external 1.5V low voltage reset circuit.

If  the  on  chip  voltage  regulator  controller  is  not  used,  an  external  1.5V power supply must be used. To avoid a power sequencing requirement when an external power supply is used, external 3.3V must power V RC33  while the VRCCTL  pad is unconnected. In this case the internal 1.5V POR will remain enabled.  If  the  V RC33   is  not  powered,  the  device  is  subject  to  power sequencing requirements for the 1.5V and 3.3V or RESET power supplies (See Section 23.5.3, 'Power Sequencing'). This is necessary to ensure that the 1.5V power supply is high enough for internal logic to operate properly during power-up.

## 23.4.2 POR Circuits

The individual POR circuits will negate whenever the supply they are monitoring is below a specified threshold.  The  entire  device  will  be  in  power-on  reset  if  any  of  these  supplies  are  below  the  values specified in the MPC5553/MPC5554 Microcontroller Hardware Specifications .

Power-on reset will assert as soon as possible after the voltage level of the POR power supplies begins to rise. Each POR will negate before its power supply rises into its specified range. Each POR will assert after its power supply drops below its specified range. Power-on reset will remain asserted until all of the POR power supplies have dropped below the minimum POR threshold. The behavior for each POR during power sequencing is shown in Figure 23-2.

Before the 3.3V POR circuit asserts when ramping up or after it negates when ramping down, the device can exit POR but still be in system reset. In this case, MDO[0] will be driving high. Also in this case, though, no clocks will be toggling. If the 3.3V POR circuit is asserted, the device will behave as if in POR even if the 1.5V and RESET power POR circuits have not yet asserted when ramping up or have negated when ramping down.

## NOTE

The PORs for each power supply are not intended to indicate that the power supply has dropped below the specified voltage range for the device. The user  must  monitor  the  power  supplies  externally  and  assert  RESET  to provide this precision of monitoring.

<!-- image -->

POR Asserts

Figure 23-2. Regions POR is Asserted

## 23.4.2.1 1.5V POR Circuit

The 1.5V POR circuit monitors the voltage on the VRCSNS pad. The 1.5V POR will function if the V RC33 pad is powered. If the user does not power V RC33  to the specified voltage, the 1.5V POR will be disabled and the user must follow the specified power sequence.

## 23.4.2.2 3.3V POR Circuit

The 3.3V POR circuit is used to ensure that V DDSYN  is high enough that the FMPLL will begin to operate properly.

## 23.4.2.3 RESET Power POR Circuit

The RESET power POR circuit, which monitors the power supply that is powering the RESET pin, is used to  ensure  that  the  supply  that  powers  the  RESET  pin  is  high  enough  that  the  state  of  the  input  will propagate reliably. The power supply monitored by this POR can go as high as 5.5V.

## 23.5 Initialization/Application Information

## 23.5.1 Voltage Regulator Example

Figure 23-3. Voltage Regulator Controller Hookup

<!-- image -->

## NOTE

The  figure  above  should  not  be  used  as  an  application  board  design reference. See  Engineering  Bulletin  EB641:  Power  Supplies  on  the MPC5500.

## 23.5.2 Recommended Power Transistors

Freescale  recommends  the  use  of  the  following  NPN  transistors  with  the  on-chip  V oltage  Regulator Controller: ON Semiconductor™ BCP68T1 and Phillips Semiconductor™ BCP68.

Refer to the MPC5553/MPC5554  Microcontroller  Hardware  Specifications for information on recommended operating characteristics.

## 23.5.3 Power Sequencing

Power sequencing between the 1.5V power supply and V DDSYN  or the RESET power supplies is required if  the  user  provides  an  external  1.5V  power  supply  and  ties  V RC33   to  ground.  To  avoid  this  power sequencing requirement, the user should power up V RC33  within the specified operating range, even if not using the on chip voltage regulator controller. Refer to Section 23.5.3.1, 'Power-Up Sequence If V RC33 Grounded' and Section 23.5.3.2, 'Power-Down Sequence If V RC33  Grounded.'

Another power sequencing requirement is that V DD33  must be of sufficient voltage before POR negates so that the values on certain pins are treated as 1s when POR does negate. Refer to Section 23.5.3.3, 'Input Value of Pins During POR Dependent on V DD33 .'

Although there is no power sequencing required between V RC33  and V DDSYN , during power up, in order for the VRC staged turn-on to operate within specification, V RC33  must not lead V DDSYN  by more than 600 mV or lag by more than 100 mV. Higher spikes in the emitter current of the pass transistor will occur if V RC33  leads or lags V DDSYN  by more than those amounts. The value of that higher spike in current depends on the board power supply circuitry and the amount of board level capacitance.

When powering down, V RC33  and V DDSYN  do not have a delta requirement to each other because the bypass capacitors internal and external to the SoC already are charged.

When not powering up or down, V RC33  and V DDSYN  do not have a delta requirement to each other for the VRC to operate within specification.

## 23.5.3.1 Power-Up Sequence If V RC33  Grounded

In this case, the 1.5V V DD  supply must rise to 1.35V before the 3.3V V DDSYN  and the RESET power supplies rise above 2.0V. This is to insure that digital logic in the PLL on the 1.5V supply will not begin to  operate  below  the  specified  operation  range  lower  limit  of  1.35V .  Since  the  internal  1.5V  POR  is disabled, the internal 3.3V POR or the RESET power POR must be depended on to hold the device in reset. Since they may negate as low as 2.0V, it is necessary for V DD  to be within spec before the 3.3V POR and the RESET power POR negate.

NOTE: V DD  must reach 1.35V before V DDSYN  and RESET reach 2.0V.

<!-- image -->

Figure 23-4. Power-Up Sequence, V RC33  Grounded

## 23.5.3.2 Power-Down Sequence If V RC33  Grounded

In this case, the only requirement is that if V DD  falls below its operating range, V DDSYN  or the RESET power must fall below 2.0V before V DD  is allowed to rise back into its operating range. This is to insure that digital 1.5V logic that is only reset by ORed\_POR, which may have been affected by the 1.5V supply falling below spec, will be reset properly.

## 23.5.3.3 Input Value of Pins During POR Dependent on V DD33

In order to avoid accidentally selecting the bypass clock because PLLCFG[0:1] and RSTCFG were not treated as 1s when POR negates (refer to Section 23.5.3.4, 'Pin Values after Negation of POR'), V DD33 must not lag V DDSYN  and the RESET pin power when powering the device by more than the V DD33 \_LAG specification in Table 5 of the MPC5554 Microcontroller Hardware Specifications . V DD33  individually can  lag  either  V DDSYN   or  the  RESET  pin  power  by  more  than  the  V DD33 \_LAG  specification.  The VDD33 \_LAG  specification applies regardless of whether VRC33 is powered. The  V DD33 \_LAG specification only applies during power up. V DD33  has no lead or lag requirements when powering down.

## 23.5.3.4 Pin Values after Negation of POR

Depending on the final PLL mode required, the PLLCFG[0:1] and RSTCFG pins must have the values shown  in  Table 23-2  after  POR  negates.  See  application  note  AN2613,  'MPC5554  Minimum  Board Configuration' for one example of the external configuration circuit.

Table 23-2. Values after POR Negation

| Final PLL Mode                                                                  | RSTCFG   | PLLCFG0   | PLLCFG1   |
|---------------------------------------------------------------------------------|----------|-----------|-----------|
| Crystal Reference (Using RSTCFG to select Crystal Reference as the default)     | 1        | -         | -         |
| Crystal Reference (Using RSTCFG to not select Crystal Reference as the default) | -        | 1         | -         |
| External Reference                                                              | 0        | 1         | 1         |
| Dual-Controller                                                                 | -        | 1         | -         |

## NOTE

After POR negates,  RSTCFG and PLLCFG[0:1] can be changed to their final value, but must avoid switching through the 0, 0, 0 state on these pins.

## 23.6 Revision History

## Substantive Changes since Rev 3.0

Changed V RCVSS  from 3.3V to 0V in Table 23-1

added 'The V DD33 \_LAG specification applies regardless of whether or not V RC33  is powered.' to Section 23.5.3.3, 'Input Value of Pins During POR Dependent on V DD33 .'
