### Chatper 2 Signal Description

This chapter describes the signals of the MPC5553 and the MPC5554 that connect off chip. It includes a table of signal properties, detailed descriptions of signals, and the I/O pin power/ground segmentation.

## 2.1 Block Diagram

Figure 2-1 shows the signals of the MPC5553, and Figure 2-2 shows the signals of the MPC5554.

Figure 2-1. MPC5553 Signal Diagram

<!-- image -->

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Figure 2-2. MPC5554 Signal Diagram

<!-- image -->

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## 2.2 External Signal Description

Table 2-1 gives a summary of the MPC5553 external signals and properties, and Table 2-2 provides a summary of the MPC5554 external signals and properties. The Signal and Range column lists the signal name and range of each signal. The Function column lists all the functions multiplexed on a pin, beginning with the primary function.  For example, for the pin CNTXB\_PCSC3\_GPIO85, CNTXB is the primary function, PCSC3 is the alternate function, and GPIO85 is the GPIO.

## 2.2.1 MPC5553 Signals Summary

Table 2-1 gives a summary of the MPC5553 external signals and properties.

Table 2-1. MPC5553 Signal Properties

| Signal and Range                    | P/ A/ G                             | Function 1                          | Description                                                             | I/O Type                            | Voltage 2                           | Pad Type 3                          | Status During Reset 4               | Status After Reset 5                | Package                             |
|-------------------------------------|-------------------------------------|-------------------------------------|-------------------------------------------------------------------------|-------------------------------------|-------------------------------------|-------------------------------------|-------------------------------------|-------------------------------------|-------------------------------------|
| Reset / Configuration (8)           | Reset / Configuration (8)           | Reset / Configuration (8)           | Reset / Configuration (8)                                               | Reset / Configuration (8)           | Reset / Configuration (8)           | Reset / Configuration (8)           | Reset / Configuration (8)           | Reset / Configuration (8)           | Reset / Configuration (8)           |
| RESET                               | P                                   | RESET                               | External reset input                                                    | I                                   | V DDEH6                             | S                                   | RESET / Up                          | RESET / Up                          | 416 324 208                         |
| RSTOUT                              | P                                   | RSTOUT                              | External Reset Output                                                   | O                                   | V DDEH6                             | S                                   | RSTOUT / Low                        | RSTOUT / High                       | 416 324 208                         |
| PLLCFG0                             | P A G                               | PLLCFG0 IRQ4 GPIO208                | FMPLL Mode Selection External Interrupt Request GPIO                    | I I I/O                             | V DDEH6                             | M                                   | PLLCFG/ Up                          | - / Up                              | 416 324 208                         |
| PLLCFG1                             | P A A2 G                            | PLLCFG1 IRQ5 SOUTD GPIO209          | FMPLL mode selection External Interrupt Request DSPI D Data Output GPIO | I I O I/O                           | V DDEH6                             | M                                   | PLLCFG/ Up                          | - / Up                              | 416 324 208                         |
| RSTCFG                              | P G                                 | RSTCFG GPIO210                      | Reset configuration input GPIO                                          | I I/O                               | V DDEH6                             | S                                   | RSTCFG / Up                         | - / Up                              | 416 324                             |
| BOOTCFG0 6                          | P A G                               | BOOTCFG0 6 IRQ2 GPIO211             | Boot configuration input 6 External interrupt request GPIO              | I I I/O                             | V DDEH6                             | S                                   | BOOTCF G / Down                     | - / Down                            | 416 324                             |
| BOOTCFG1                            | P A G                               | BOOTCFG1 IRQ3 GPIO212               | Boot configuration input External interrupt request GPIO                | I I I/O                             | V DDEH6                             | S                                   | BOOTCF G / Down                     | - / Down                            | 416 324 208                         |
| WKPCFG                              | P G                                 | WKPCFG GPIO213                      | Weak pull configuration input GPIO                                      | I I/O                               | V DDEH6                             | S                                   | WKPCFG / Up                         | - / Up                              | 416 324 208                         |
| External Bus Interface (EBI) 7 (72) | External Bus Interface (EBI) 7 (72) | External Bus Interface (EBI) 7 (72) | External Bus Interface (EBI) 7 (72)                                     | External Bus Interface (EBI) 7 (72) | External Bus Interface (EBI) 7 (72) | External Bus Interface (EBI) 7 (72) | External Bus Interface (EBI) 7 (72) | External Bus Interface (EBI) 7 (72) | External Bus Interface (EBI) 7 (72) |
| CS[0]                               | P A G                               | CS[0] ADDR[8] 8 GPIO[0]             | External chip selects External address bus 8 GPIO                       | O I/O I/O                           | V DDE2                              | F                                   | - / Up                              | - / Up 9                            | 416 324 208                         |

Table 2-1. MPC5553 Signal Properties  (continued)

| Signal and Range   | P/ A/ G   | Function 1                              | Description                                                       | I/O Type      | Voltage 2   | Pad Type 3   | Status During Reset 4   | Status After Reset 5   | Package   |
|--------------------|-----------|-----------------------------------------|-------------------------------------------------------------------|---------------|-------------|--------------|-------------------------|------------------------|-----------|
| CS[1:3]            | P A G     | CS[1:3] ADDR[9:11] 8 GPIO[1:3]          | External chip selects External address bus 8 GPIO                 | O I/O I/O     | V DDE2      | F            | - / Up                  | - / Up 9               | 416 324   |
| ADDR [8:11]        | P A G     | ADDR[8:11] 8 CAL_ADDR [27:30] GPIO[4:7] | External Address Bus 8, 10 Calibration Address Bus GPIO           | I/O O I/O     | V DDE2      | F            | - / Up                  | - / Up 9               | 416       |
| ADDR [12:31]       | P G       | ADDR[12:31] GPIO[8:27]                  | External Address Bus 10 GPIO                                      | I/O I/O       | V DDE2      | F            | - / Up                  | - / Up 9               | 416 324   |
| DATA [0:15]        | P G       | DATA[0:15] GPIO[28:43]                  | External Data Bus 10 GPIO                                         | I/O I/O       | V DDE3      | F            | - / Up                  | - / Up 9               | 416 324   |
| DATA16             | P A A2 G  | DATA16 TX_CLK CAL_DATA0 GPIO44          | External Data Bus 10 FEC Transmit Clock Calibration Data Bus GPIO | I/O I I/O I/O | V DDE3      | F            | - / Up                  | - / Up 9               | 416       |
| DATA17             | P A A2 G  | DATA17 CRS CAL_DATA1 GPIO45             | External Data Bus 10 FEC Carrier Sense Calibration Data Bus GPIO  | I/O I I/O I/O | V DDE3      | F            | - / Up                  | - / Up 9               | 416       |
| DATA18             | P A A2 G  | DATA18 TX_ER CAL_DATA2 GPIO46           | External Data Bus 10 FEC Transmit Error Calibration Data Bus GPIO | I/O O I/O I/O | V DDE3      | F            | - / Up                  | - / Up 9               | 416       |
| DATA19             | P A A2 G  | DATA19 RX_CLK CAL_DATA3 GPIO47          | External Data Bus 10 FEC Receive Clock Calibration Data Bus GPIO  | I/O I I/O I/O | V DDE3      | F            | - / Up                  | - / Up 9               | 416       |
| DATA20             | P A A2 G  | DATA20 TXD0 CAL_DATA4 GPIO48            | External Data Bus 10 FEC Transmit Data Calibration Data Bus GPIO  | I/O O I/O I/O | V DDE3      | F            | - / Up                  | - / Up 9               | 416       |
| DATA21             | P A A2 G  | DATA21 RX_ER CAL_DATA5 GPIO49           | External Data Bus 10 FEC Receive Error Calibration Data Bus GPIO  | I/O I I/O I/O | V DDE3      | F            | - / Up                  | - / Up 9               | 416       |
| DATA22             | P A A2 G  | DATA22 RXD0 CAL_DATA6 GPIO50            | External Data Bus 10 FEC Receive Data Calibration Data Bus GPIO   | I/O I I/O I/O | V DDE3      | F            | - / Up                  | - / Up 9               | 416       |
| DATA23             | P A A2 G  | DATA23 TXD3 CAL_DATA7 GPIO51            | External Data Bus 10 FEC Transmit Data Calibration Data Bus GPIO  | I/O O I/O I/O | V DDE3      | F            | - / Up                  | - / Up 9               | 416       |

Table 2-1. MPC5553 Signal Properties  (continued)

| Signal and Range   | P/ A/ G   | Function 1                     | Description                                                           | I/O Type      | Voltage 2   | Pad Type 3   | Status During Reset 4   | Status After Reset 5   | Package   |
|--------------------|-----------|--------------------------------|-----------------------------------------------------------------------|---------------|-------------|--------------|-------------------------|------------------------|-----------|
| DATA24             | P A A2 G  | DATA24 COL CAL_DATA8 GPIO52    | External Data Bus 10 FEC Collision Detect Calibration Data Bus GPIO   | I/O I I/O I/O | V DDE3      | F            | - / Up                  | - / Up 9               | 416       |
| DATA25             | P A A2 G  | DATA25 RX_DV CAL_DATA9 GPIO53  | External Data Bus 10 FEC Receive Data Valid Calibration Data Bus GPIO | I/O I I/O I/O | V DDE3      | F            | - / Up                  | - / Up 9               | 416       |
| DATA26             | P A A2 G  | DATA26 TX_EN CAL_DATA10 GPIO54 | External Data Bus 10 FEC Transmit Enable Calibration Data Bus GPIO    | I/O O I/O I/O | V DDE3      | F            | - / Up                  | - / Up 9               | 416       |
| DATA27             | P A A2 G  | DATA27 TXD2 CAL_DATA11 GPIO55  | External Data Bus 10 FEC Transmit Data Calibration Data Bus GPIO      | I/O O I/O I/O | V DDE3      | F            | - / Up                  | - / Up 9               | 416       |
| DATA28             | P A A2 G  | DATA28 TXD1 CAL_DATA12 GPIO56  | External Data Bus 10 FEC Transmit Data Calibration Data Bus GPIO      | I/O O I/O I/O | V DDE3      | F            | - / Up                  | - / Up 9               | 416       |
| DATA29             | P A A2 G  | DATA29 RXD1 CAL_DATA13 GPIO57  | External Data Bus 10 FEC Receive Data Calibration Data Bus GPIO       | I/O I I/O I/O | V DDE3      | F            | - / Up                  | - / Up 9               | 416       |
| DATA30             | P A A2 G  | DATA30 RXD2 CAL_DATA14 GPIO58  | External Data Bus 10 FEC Receive Data Calibration Data Bus GPIO       | I/O I I/O I/O | V DDE3      | F            | - / Up                  | - / Up 9               | 416       |
| DATA31             | P A A2 G  | DATA31 RXD3 CAL_DATA15 GPIO59  | External Data Bus 10 FEC Receive Data Calibration Data Bus GPIO       | I/O I I/O I/O | V DDE3      | F            | - / Up                  | - / Up 9               | 416       |
| RD_WR              | P G       | RD_WR GPIO62                   | External Read/Write GPIO                                              | I/O I/O       | V DDE2      | F            | - / Up                  | - / Up 9               | 416 324   |
| BDIP               | P G       | BDIP GPIO63                    | External Burst Data In Progress GPIO                                  | O I/O         | V DDE2      | F            | - / Up                  | - / Up 9               | 416 324   |
| WE[0:1]            | P A G     | WE[0:1] BE[0:1] GPIO[64:65]    | External Write Enable External Byte Enable 11 GPIO                    | O O I/O       | V DDE2      | F            | - / Up                  | - / Up 9               | 416 324   |

Table 2-1. MPC5553 Signal Properties  (continued)

| Signal and Range   | P/ A/ G     | Function 1                                         | Description                                                                                         | I/O Type      | Voltage 2   | Pad Type 3   | Status During Reset 4   | Status After Reset 5   | Package     |
|--------------------|-------------|----------------------------------------------------|-----------------------------------------------------------------------------------------------------|---------------|-------------|--------------|-------------------------|------------------------|-------------|
| WE[2:3]            | P A A2 A3 G | WE[2:3] BE[2:3] CAL_WE[0:1] CAL_BE[0:1 GPIO[66:67] | External Write Enable External Byte Enable 11 Calibration Write Enable Calibration Byte Enable GPIO | O O O O I/O   | V DDE2      | F            | - / Up                  | - / Up 9               | 416         |
| OE                 | P G         | OE GPIO68                                          | External Output Enable GPIO                                                                         | O I/O         | V DDE3      | F            | - / Up                  | - / Up 9               | 416 324 208 |
| TS                 | P G         | TS GPIO69                                          | External Transfer Start GPIO                                                                        | I/O I/O       | V DDE2      | F            | - / Up                  | - / Up 9               | 416 324     |
| TA                 | P G         | TA GPIO70                                          | External Transfer Acknowledge GPIO                                                                  | I/O I/O       | V DDE2      | F            | - / Up                  | - / Up 9               | 416 324     |
| TEA                | P A G       | TEA CAL_CS0 GPIO71                                 | External Transfer Error Acknowledge Calibration Chip Select GPIO                                    | I/O O I/O     | V DDE2      | F            | - / Up                  | - / Up 9               | 416         |
| BR 12 (CAL_ADDR10) | - P A A2 G  | CAL_ADDR10 MDC CAL_CS2 GPIO72                      | Calibration Address Bus FEC Management Clock Calibration Chip Select GPIO                           | O O O I/O     | V DDE3      | F            | - / Up                  | - / Up 9               | 416         |
| BG 12 (CAL_ADDR11) | - P A A2 G  | CAL_ADDR11 MDIO CAL_CS3 GPIO73                     | Calibration Address Bus FEC Management Data I/O Calibration Chip Select GPIO                        | O I/O I/O I/O | V DDE3      | F            | - / Up                  | - / Up 9               | 416         |
| NEXUS (18)         | NEXUS (18)  | NEXUS (18)                                         | NEXUS (18)                                                                                          | NEXUS (18)    | NEXUS (18)  | NEXUS (18)   | NEXUS (18)              | NEXUS (18)             | NEXUS (18)  |
| EVTI               | P           | EVTI                                               | Nexus Event In                                                                                      | I             | V DDE7      | F            | I / Up                  | EVTI / Up              | 416 324 208 |
| EVTO               | P           | EVTO                                               | Nexus Event Out                                                                                     | O             | V DDE7      | F            | O / Low                 | EVTO / High            | 416 324 208 |
| MCKO               | P           | MCKO                                               | Nexus Message Clock Out                                                                             | O             | V DDE7      | F            | O / Low                 | MCKO / Enabled 13      | 416 324 208 |
| MDO[0]             | P           | MDO[0] 14                                          | Nexus Message Data Out                                                                              | O             | V DDE7      | F            | O / High                | MDO / Low              | 416 324 208 |
| MDO[3:1]           | P           | MDO[3:1]                                           | Nexus Message Data Out                                                                              | O             | V DDE7      | F            | O / Low                 | MDO / Low              | 416 324 208 |

Table 2-1. MPC5553 Signal Properties  (continued)

| Signal and Range   | P/ A/ G        | Function 1               | Description                                         | I/O Type       | Voltage 2      | Pad Type 3     | Status During Reset 4   | Status After Reset 5   | Package        |
|--------------------|----------------|--------------------------|-----------------------------------------------------|----------------|----------------|----------------|-------------------------|------------------------|----------------|
| MDO[11:4]          | P G            | MDO[11:4] 15 GPIO[75:82] | Nexus Message Data Out GPIO                         | O I/O          | V DDE7         | F              | O / Low                 | - / Down               | 416 324        |
| MSEO[1:0]          | P              | MSEO[1:0]                | Nexus Message Start/End Out                         | O              | V DDE7         | F              | O / High                | MSEO / High            | 416 324 208    |
| RDY                | P              | RDY                      | Nexus Ready Output                                  | O              | V DDE7         | F              | O / High                | RDY/ High              | 416 324        |
| JTAG / TEST(6)     | JTAG / TEST(6) | JTAG / TEST(6)           | JTAG / TEST(6)                                      | JTAG / TEST(6) | JTAG / TEST(6) | JTAG / TEST(6) | JTAG / TEST(6)          | JTAG / TEST(6)         | JTAG / TEST(6) |
| TCK                | P              | TCK                      | JTAG Test Clock Input                               | I              | V DDE7         | F              | TCK / Down              | TCK / Down             | 416 324 208    |
| TDI                | P              | TDI                      | JTAG Test Data Input                                | I              | V DDE7         | F              | TDI / Up                | TDI / Up               | 416 324 208    |
| TDO                | P              | TDO                      | JTAG Test Data Output                               | O              | V DDE7         | F              | TDO / Up                | TDO / Up               | 416 324 208    |
| TMS                | P              | TMS                      | JTAG Test Mode Select Input                         | I              | V DDE7         | F              | TMS / Up                | TMS / Up               | 416 324 208    |
| JCOMP              | P              | JCOMP                    | JTAG TAP Controller Enable                          | I              | V DDE7         | F              | JCOMP / Down            | JCOMP / Down           | 416 324 208    |
| TEST               | P              | TEST                     | Test Mode Select                                    | I              | V DDE7         | F              | TEST / Up               | TEST / Up              | 416 324 208    |
| FlexCAN (4)        | FlexCAN (4)    | FlexCAN (4)              | FlexCAN (4)                                         | FlexCAN (4)    | FlexCAN (4)    | FlexCAN (4)    | FlexCAN (4)             | FlexCAN (4)            | FlexCAN (4)    |
| CNTXA              | P G            | CNTXA GPIO83             | CAN_A Transmit GPIO                                 | O I/O          | V DDEH4        | S              | - / Up                  | - / Up 16              | 416 324 208    |
| CNRXA              | P G            | CNRXA GPIO84             | CAN_A Receive GPIO                                  | I I/O          | V DDEH4        | S              | - / Up                  | - / Up                 | 416 324 208    |
| CNTXC              | P A G          | CNTXC PCSD3 GPIO87       | CAN_C Transmit DSPI D Peripheral Chip Select 3 GPIO | O O I/O        | V DDEH6        | M              | - / Up                  | - / Up                 | 416 324 208    |
| CNRXC              | P A G          | CNRXC PCSD4 GPIO88       | CAN_C Receive DSPI D Peripheral Chip Select 4 GPIO  | I O I/O        | V DDEH6        | M              | - / Up                  | - / Up                 | 416 324 208    |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 2-1. MPC5553 Signal Properties  (continued)

| Signal and Range   | P/ A/ G   | Function 1         | Description                                                          | I/O Type   | Voltage 2   | Pad Type 3   | Status During Reset 4   | Status After Reset 5   | Package     |
|--------------------|-----------|--------------------|----------------------------------------------------------------------|------------|-------------|--------------|-------------------------|------------------------|-------------|
| SCI (4)            | SCI (4)   | SCI (4)            | SCI (4)                                                              | SCI (4)    | SCI (4)     | SCI (4)      | SCI (4)                 | SCI (4)                | SCI (4)     |
| TXDA               | P G       | TXDA GPIO89        | SCI_A Transmit GPIO                                                  | O I/O      | V DDEH6     | S            | - / Up                  | - / Up                 | 416 324 208 |
| RXDA               | P G       | RXDA GPIO90        | SCI_A Receive GPIO                                                   | I I/O      | V DDEH6     | S            | - / -                   | - / Up                 | 416 324 208 |
| TXDB               | P A G     | TXDB PCSD1 GPIO91  | SCI_B Transmit DSPI D Peripheral Chip Select 1 GPIO                  | O O I/O    | V DDEH6     | M            | - / Up                  | - / Up                 | 416 324 208 |
| RXDB               | P A G     | RXDB PCSD5 GPIO92  | SCI_B Receive DSPI D Peripheral Chip Select 5 GPIO                   | I O I/O    | V DDEH6     | M            | - / Up                  | - / Up                 | 416 324 208 |
| DSPI(20)           | DSPI(20)  | DSPI(20)           | DSPI(20)                                                             | DSPI(20)   | DSPI(20)    | DSPI(20)     | DSPI(20)                | DSPI(20)               | DSPI(20)    |
| CNTXB              | P A G     | CNTXB PCSC3 GPIO85 | CAN_B Transmit (not functional) DSPI C Peripheral Chip Select 3 GPIO | O O I/O    | V DDEH4     | M            | - / Up                  | - / Up                 | 416 324 208 |
| CNRXB              | P A G     | CNRXB PCSC4 GPIO86 | CAN_B Receive (not functional) DSPI C Peripheral Chip Select 4 GPIO  | I O I/O    | V DDEH4     | M            | - / Up                  | - / Up                 | 416 324 208 |
| SCKA               | P A G     | SCKA PCSC1 GPIO93  | - DSPI C Peripheral Chip Select 1 GPIO                               | - O I/O    | V DDEH6     | M            | - / Up                  | - / Up                 | 416 324     |
| SINA               | P A G     | SINA PCSC2 GPIO94  | - DSPI C Peripheral Chip Select 2 GPIO                               | - O I/O    | V DDEH6     | M            | - / Up                  | - / Up                 | 416 324     |
| SOUTA              | P A G     | SOUTA PCSC5 GPIO95 | - DSPI C Peripheral Chip Select 5 GPIO                               | - O I/O    | V DDEH6     | M            | - / Up                  | - / Up                 | 416 324     |
| PCSA0              | P A G     | PCSA0 PCSD2 GPIO96 | - DSPI D Peripheral Chip Select 2 GPIO                               | - O I/O    | V DDEH6     | M            | - / Up                  | - / Up                 | 416 324     |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 2-1. MPC5553 Signal Properties  (continued)

| Signal and Range   | P/ A/ G   | Function 1          | Description                                                          | I/O Type   | Voltage 2   | Pad Type 3   | Status During Reset 4   | Status After Reset 5   | Package     |
|--------------------|-----------|---------------------|----------------------------------------------------------------------|------------|-------------|--------------|-------------------------|------------------------|-------------|
| PCSA1              | P A G     | PCSA1 PCSB2 GPIO97  | - DSPI B Peripheral Chip Select 2 GPIO                               | - O I/O    | V DDEH6     | M            | - / Up                  | - / Up                 | 416 324     |
| PCSA2              | P A G     | PCSA2 SCKD GPIO98   | - DSPI D Clock GPIO                                                  | - I/O I/O  | V DDEH6     | M            | - / Up                  | - / Up                 | 416 324 208 |
| PCSA3              | P A G     | PCSA3 SIND GPIO99   | - DSPI D Data Input GPIO                                             | - I I/O    | V DDEH6     | M            | - / Up                  | - / Up                 | 416 324 208 |
| PCSA4              | P A G     | PCSA4 SOUTD GPIO100 | - DSPI D Data Output GPIO                                            | - O I/O    | V DDEH6     | M            | - / Up                  | - / Up                 | 416 324     |
| PCSA5              | P A G     | PCSA5 PCSB3 GPIO101 | - DSPI B Peripheral Chip Select 3 GPIO                               | - O I/O    | V DDEH6     | M            | - / Up                  | - / Up                 | 416 324     |
| SCKB               | P A G     | SCKB PCSC1 GPIO102  | DSPI B Clock DSPI C Peripheral Chip Select 1 GPIO                    | I/O O I/O  | V DDEH10    | M            | - / Up                  | - / Up                 | 416 324 208 |
| SINB               | P A G     | SINB PCSC2 GPIO103  | DSPI B Data Input DSPI C Peripheral Chip Select 2 GPIO               | I O I/O    | V DDEH10    | M            | - / Up                  | - / Up                 | 416 324 208 |
| SOUTB              | P A G     | SOUTB PCSC5 GPIO104 | DSPI B Data Output DSPI C Peripheral Chip Select 5 GPIO              | O O I/O    | V DDEH10    | M            | - / Up                  | - / Up                 | 416 324 208 |
| PCSB0              | P A G     | PCSB0 PCSD2 GPIO105 | DSPI B Peripheral Chip Select 0 DSPI D Peripheral Chip Select 2 GPIO | I/O O I/O  | V DDEH10    | M            | - / Up                  | - / Up                 | 416 324 208 |
| PCSB1              | P A G     | PCSB1 PCSD0 GPIO106 | DSPI B Peripheral Chip Select 1 DSPI D Peripheral Chip Select 0 GPIO | O I/O I/O  | V DDEH10    | M            | - / Up                  | - / Up                 | 416 324 208 |
| PCSB2              | P A G     | PCSB2 SOUTC GPIO107 | DSPI B Peripheral Chip Select 2 DSPI C Data Output GPIO              | O O I/O    | V DDEH10    | M            | - / Up                  | - / Up                 | 416 324 208 |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 2-1. MPC5553 Signal Properties  (continued)

| Signal and Range   | P/ A/ G   | Function 1          | Description                                                          | I/O Type   | Voltage 2   | Pad Type 3   | Status During Reset 4   | Status After Reset 5   | Package     |
|--------------------|-----------|---------------------|----------------------------------------------------------------------|------------|-------------|--------------|-------------------------|------------------------|-------------|
| PCSB3              | P A G     | PCSB3 SINC GPIO108  | DSPI B Peripheral Chip Select 3 DSPI C Data Input GPIO               | O I I/O    | V DDEH6     | M            | - / Up                  | - / Up                 | 416 324 208 |
| PCSB4              | P A G     | PCSB4 SCKC GPIO109  | DSPI B Peripheral Chip Select 4 DSPI C Clock GPIO                    | O I/O I/O  | V DDEH6     | M            | - / Up                  | - / Up                 | 416 324 208 |
| PCSB5              | P A G     | PCSB5 PCSC0 GPIO110 | DSPI B Peripheral Chip Select 5 DSPI C Peripheral Chip Select 0 GPIO | O I/O I/O  | V DDEH6     | M            | - / Up                  | - / Up                 | 416 324 208 |
| eQADC(45)          | eQADC(45) | eQADC(45)           | eQADC(45)                                                            | eQADC(45)  | eQADC(45)   | eQADC(45)    | eQADC(45)               | eQADC(45)              | eQADC(45)   |
| AN0                | P A       | AN0 DAN0+           | Single Ended Analog Input 0 Positive Terminal Differential Input     | I I        | V DDA1 17   | AE           | I / -                   | AN0/ -                 | 416 324 208 |
| AN1                | P A       | AN1 DAN0-           | Single Ended Analog Input 1 Negative Terminal Differential Input     | I I        | V DDA1 17   | AE           | I / -                   | AN1/ -                 | 416 324 208 |
| AN2                | P A       | AN2 DAN1+           | Single Ended Analog Input 2 Positive Terminal Differential Input     | I I        | V DDA1 17   | AE           | I / -                   | AN2 / -                | 416 324 208 |
| AN3                | P A       | AN3 DAN1-           | Single Ended Analog Input 3 Negative Terminal Differential Input     | I I        | V DDA1 17   | AE           | I / -                   | AN3 / -                | 416 324 208 |
| AN4                | P A       | AN4 DAN2+           | Single Ended Analog Input 4 Positive Terminal Differential Input     | I I        | V DDA1 17   | AE           | I / -                   | AN4/ -                 | 416 324 208 |
| AN5                | P A       | AN5 DAN2-           | Single Ended Analog Input 5 Negative Terminal Differential Input     | I I        | V DDA1 17   | AE           | I / -                   | AN5 / -                | 416 324 208 |
| AN6                | P A       | AN6 DAN3+           | Single Ended Analog Input 6 Positive Terminal Differential Input     | I I        | V DDA1 17   | AE           | I / -                   | AN6 / -                | 416 324 208 |

Table 2-1. MPC5553 Signal Properties  (continued)

| Signal and Range   | P/ A/ G   | Function 1   | Description                                                         | I/O Type   | Voltage 2   | Pad Type 3   | Status During Reset 4   | Status After Reset 5   | Package     |
|--------------------|-----------|--------------|---------------------------------------------------------------------|------------|-------------|--------------|-------------------------|------------------------|-------------|
| AN7                | P A       | AN7 DAN3-    | Single Ended Analog Input 7 Negative Terminal Differential Input    | I I        | V DDA1 17   | AE           | I / -                   | AN7 / -                | 416 324 208 |
| AN8                | P A       | AN8 ANW      | Single Ended Analog Input 8 External Multiplexed Analog Input W     | I I        | V DDA1 17   | AE           | I / -                   | AN8/ -                 | 416 324     |
| AN9                | P A A     | AN9 ANX      | Single Ended Analog Input 9 External Multiplexed Analog Input X     | I I        | V DDA1 17   | AE           | I / -                   | AN9 / -                | 416 324 208 |
| AN10               | P A       | AN10 ANY     | Single Ended Analog Input 10 External Multiplexed Analog Input Y    | I I        | V DDA1 17   | AE           | I / -                   | AN10/ -                | 416 324     |
| AN11               | P A       | AN11 ANZ     | Single Ended Analog Input 11 External Multiplexed Analog Input Z    | I I        | V DDA1 17   | AE           | I / -                   | AN11 / -               | 416 324 208 |
| AN12               | P A A     | AN12 MA0 SDS | Single Ended Analog Input 12 Mux Address 0 eQADC Serial Data Select | I O O      | V DDEH9     | A, M         | I / -                   | AN12/ -                | 416 324 208 |
| AN13               | P A A     | AN13 MA1 SDO | Single Ended Analog Input 13 Mux Address 1 eQADC Serial Data Out    | I O O      | V DDEH9     | A, M         | I / -                   | AN13/ -                | 416 324 208 |
| AN14               | P A A     | AN14 MA2 SDI | Single Ended Analog Input 14 Mux Address 2 eQADC Serial Data In     | I O I      | V DDEH9     | A, M         | I / -                   | AN14/ -                | 416 324 208 |
| AN15               | P A       | AN15 FCK     | Single Ended Analog Input 15 eQADC Free Running Clock               | I O        | V DDEH9     | A, M         | I / -                   | AN15/ -                | 416 324 208 |
| AN[16:18]          | P         | AN[16:18]    | Single Ended Analog Input 16-18                                     | I          | V DDA1 17   | AE           | I / -                   | AN[16:18]/ -           | 416 324 208 |
| AN[19:20]          | P         | AN[19:20]    | Single Ended Analog Input 19-20                                     | I          | V DDA1 17   | AE           | I / -                   | AN[19:20]/ -           | 416 324     |
| AN21               | P         | AN21         | Single Ended Analog Input 21                                        | I          | V DDA1 17   | AE           | I / -                   | AN21/ -                | 416 324 208 |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 2-1. MPC5553 Signal Properties  (continued)

| Signal and Range   | P/ A/ G   | Function 1                            | Description                                      | I/O Type   | Voltage 2   | Pad Type 3   | Status During Reset 4   | Status After Reset 5   | Package     |
|--------------------|-----------|---------------------------------------|--------------------------------------------------|------------|-------------|--------------|-------------------------|------------------------|-------------|
| AN[22:25]          | P         | AN[22:25]                             | Single Ended Analog Input 22-25                  | I          | V DDA0 17   | AE           | I / -                   | AN[22:25]/ -           | 416 324 208 |
| AN26               | P         | AN26                                  | Single Ended Analog Input 26                     | I          | V DDA0 17   | AE           | I / -                   | AN26/ -                | 416 324     |
| AN[27:28]          | P         | AN[27:28]                             | Single Ended Analog Input 27-28                  | I          | V DDA0 17   | AE           | I / -                   | AN[27:28]/ -           | 416 324 208 |
| AN29               | P         | AN29                                  | Single Ended Analog Input 29                     | I          | V DDA0 17   | AE           | I / -                   | AN29/ -                | 416 324     |
| AN[30:35]          | P         | AN[30:35]                             | Single Ended Analog Input 30-35                  | I          | V DDA0 17   | AE           | I / -                   | AN[30:35]/ -           | 416 324 208 |
| AN[36:39]          | P         | AN[36:39]                             | Single Ended Analog Input 36-39                  | I          | V DDA1 17   | AE           | I / -                   | AN[36:39] / -          | 416 324 208 |
| ETRIG[0:1]         | P G       | ETRIG[0:1] GPIO[111:112]              | eQADC Trigger Input 0, 1 GPIO                    | I I/O      | V DDEH8     | S            | - / Up                  | - / Up                 | 416         |
| VRH                | P         | VRH                                   | Voltage Reference High                           | I          | V DDA0 17   | VDDI NT      | - / -                   | VRH                    | 416 324 208 |
| VRL                | P         | VRL                                   | Voltage Reference Low                            | I          | V DDA0 17   | VSSI NT      | - / -                   | VRL                    | 416 324 208 |
| REFBYPC            | P         | REFBYPC                               | Reference Bypass Capacitor Input                 | I          | V DDA0 17   | AE           | - / -                   | REFBYPC                | 416 324 208 |
| eTPU(33)           | eTPU(33)  | eTPU(33)                              | eTPU(33)                                         | eTPU(33)   | eTPU(33)    | eTPU(33)     | eTPU(33)                | eTPU(33)               | eTPU(33)    |
| TCRCLKA            | P A G     | TCRCLKA IRQ7 GPIO113                  | eTPU A TCR clock External interrupt request GPIO | I I I/O    | V DDEH1     | S            | - / Up                  | - / Up                 | 416 324 208 |
| ETPUA [0:3]        | P A G     | ETPUA[0:3] ETPUA[12:15] GPIO[114:117] | eTPU A channel eTPU A channel (output only) GPIO | I/O O I/O  | V DDEH1     | S            | -/ WKPCFG               | -/ WKPCFG              | 416 324 208 |
| ETPUA [4:7]        | P A G     | ETPUA[4:7] ETPUA[16:19] GPIO[118:121] | eTPU A channel eTPU A channel (output only) GPIO | I/O O I/O  | V DDEH1     | S            | -/ WKPCFG               | -/ WKPCFG              | 416 324 208 |

Table 2-1. MPC5553 Signal Properties  (continued)

| Signal and Range   | P/ A/ G   | Function 1                             | Description                                                  | I/O Type   | Voltage 2   | Pad Type 3   | Status During Reset 4   | Status After Reset 5   | Package     |
|--------------------|-----------|----------------------------------------|--------------------------------------------------------------|------------|-------------|--------------|-------------------------|------------------------|-------------|
| ETPUA [8:11]       | P A G     | ETPUA[8:11] ETPUA[20:23] GPIO[122:125] | eTPU A channel eTPU A channel (output only) GPIO             | I/O O I/O  | V DDEH1     | S            | -/ WKPCFG               | -/ WKPCFG              | 416 324 208 |
| ETPUA12            | P A G     | ETPUA12 PCSB1 GPIO126                  | eTPU A channel DSPI B peripheral chip select 1 GPIO          | I/O O I/O  | V DDEH1     | M            | -/ WKPCFG               | -/ WKPCFG              | 416 324 208 |
| ETPUA13            | P A G     | ETPUA13 PCSB3 GPIO127                  | eTPU A channel DSPI B peripheral chip select 3 GPIO          | I/O O I/O  | V DDEH1     | M            | -/ WKPCFG               | -/ WKPCFG              | 416 324 208 |
| ETPUA14            | P A G     | ETPUA14 PCSB4 GPIO128                  | eTPU A channel DSPI B peripheral chip select 4 GPIO          | I/O O I/O  | V DDEH1     | M            | -/ WKPCFG               | -/ WKPCFG              | 416 324 208 |
| ETPUA15            | P A G     | ETPUA15 PCSB5 GPIO129                  | eTPU A channel DSPI B peripheral chip select 5 GPIO          | I/O O I/O  | V DDEH1     | M            | -/ WKPCFG               | -/ WKPCFG              | 416 324 208 |
| ETPUA16            | P A G     | ETPUA16 PCSD1 GPIO130                  | eTPU A channel DSPI D peripheral chip select 1 GPIO          | I/O O I/O  | V DDEH1     | M            | -/ WKPCFG               | -/ WKPCFG              | 416 324 208 |
| ETPUA17            | P A G     | ETPUA17 PCSD2 GPIO131                  | eTPU A channel DSPI D peripheral chip select 2 GPIO          | I/O O I/O  | V DDEH1     | M            | -/ WKPCFG               | -/ WKPCFG              | 416 324 208 |
| ETPUA18            | P A G     | ETPUA18 PCSD3 GPIO132                  | eTPU A channel DSPI D peripheral chip select 3 GPIO          | I/O O I/O  | V DDEH1     | M            | -/ WKPCFG               | -/ WKPCFG              | 416 324 208 |
| ETPUA19            | P A G     | ETPUA19 PCSD4 GPIO133                  | eTPU A channel DSPI D peripheral chip select 4 GPIO          | I/O O I/O  | V DDEH1     | M            | -/ WKPCFG               | -/ WKPCFG              | 416 324 208 |
| ETPUA [20:23]      | P A G     | ETPUA[20:23] IRQ[8:11] GPIO[134:137]   | eTPU A channel External interrupt request GPIO               | I/O I I/O  | V DDEH1     | M            | -/ WKPCFG               | -/ WKPCFG              | 416 324 208 |
| ETPUA [24:26]      | P A G     | ETPUA[24:26] IRQ[12:14] GPIO[138:140]  | eTPU A channel (output only) External interrupt request GPIO | O I I/O    | V DDEH1     | S            | -/ WKPCFG               | -/ WKPCFG              | 416 324 208 |

Table 2-1. MPC5553 Signal Properties  (continued)

| Signal and Range   | P/ A/ G   | Function 1                          | Description                                                       | I/O Type   | Voltage 2   | Pad Type 3   | Status During Reset 4   | Status After Reset 5   | Package     |
|--------------------|-----------|-------------------------------------|-------------------------------------------------------------------|------------|-------------|--------------|-------------------------|------------------------|-------------|
| ETPUA27            | P A G     | ETPUA27 IRQ15 GPIO141               | eTPU A channel (output only) External interrupt request GPIO      | O I I/O    | V DDEH1     | S            | -/ WKPCFG               | -/ WKPCFG              | 416 324 208 |
| ETPUA28            | P A G     | ETPUA28 PCSC1 GPIO142               | eTPU A Channel (Output Only) DSPI C peripheral chip select 1 GPIO | O O I/O    | V DDEH1     | M            | -/ WKPCFG               | -/ WKPCFG              | 416 324 208 |
| ETPUA29            | P A G     | ETPUA29 PCSC2 GPIO143               | eTPU A Channel (Output Only) DSPI C peripheral chip select 2 GPIO | O O I/O    | V DDEH1     | M            | -/ WKPCFG               | -/ WKPCFG              | 416 324 208 |
| ETPUA30            | P A G     | ETPUA30 PCSC3 GPIO144               | eTPU A Channel DSPI C peripheral chip select 3 GPIO               | I/O O I/O  | V DDEH1     | M            | -/ WKPCFG               | -/ WKPCFG              | 416 324 208 |
| ETPUA31            | P A G     | ETPUA31 PCSC4 GPIO145               | eTPU A Channel DSPI C peripheral chip select 4 GPIO               | I/O O I/O  | V DDEH1     | M            | -/ WKPCFG               | -/ WKPCFG              | 416 324 208 |
| EMIOS(24)          | EMIOS(24) | EMIOS(24)                           | EMIOS(24)                                                         | EMIOS(24)  | EMIOS(24)   | EMIOS(24)    | EMIOS(24)               | EMIOS(24)              | EMIOS(24)   |
| EMIOS [0:9]        | P A G     | EMIOS[0:9] ETPUA[0:9] GPIO[179:188] | eMIOS channel eTPU A channel (output only) GPIO                   | I/O O I/O  | V DDEH4     | S            | -/ WKPCFG               | -/ WKPCFG              | 416 324 208 |
| EMIOS[10:11]       | P G       | EMIOS[10:11] GPIO[189:190]          | eMIOS channel GPIO                                                | I/O I/O    | V DDEH4     | S            | -/ WKPCFG               | -/ WKPCFG              | 416 324 208 |
| EMIOS12            | P A G     | EMIOS12 SOUTC GPIO191               | EMIOS Channel (Output Only) DSPI C Data Output GPIO               | O O I/O    | V DDEH4     | M            | -/ WKPCFG               | -/ WKPCFG              | 416 324 208 |
| EMIOS13            | P A G     | EMIOS13 SOUTD GPIO192               | EMIOS Channel (Output Only) DSPI D Data Output GPIO               | O O I/O    | V DDEH4     | M            | -/ WKPCFG               | -/ WKPCFG              | 416 324 208 |
| EMIOS [14:15]      | P A G     | EMIOS[14:15] IRQ[0:1] GPIO[193:194] | eMIOS channel (output only) External interrupt request GPIO       | O I I/O    | V DDEH4     | S            | -/ WKPCFG               | -/ WKPCFG              | 416 324 208 |

Table 2-1. MPC5553 Signal Properties  (continued)

| Signal and Range      | P/ A/ G               | Function 1                                                                      | Description                                     | I/O Type              | Voltage 2             | Pad Type 3            | Status During Reset 4   | Status After Reset 5   | Package               |
|-----------------------|-----------------------|---------------------------------------------------------------------------------|-------------------------------------------------|-----------------------|-----------------------|-----------------------|-------------------------|------------------------|-----------------------|
| EMIOS [16:23]         | P A G                 | EMIOS[16:23] ETPUB[0:7] GPIO[195:202]                                           | eMIOS channel eTPU B channel (output only) GPIO | I/O O I/O             | V DDEH4               | S                     | -/ WKPCFG               | -/ WKPCFG              | 416 324 208           |
| GPIO(5)               | GPIO(5)               | GPIO(5)                                                                         | GPIO(5)                                         | GPIO(5)               | GPIO(5)               | GPIO(5)               | GPIO(5)                 | GPIO(5)                | GPIO(5)               |
| GPIO 18 [203:204]     | P A                   | EMIOS[14:15] GPIO[203:204] Note: EMIOS is primary function                      | EMIOS Channel (Output Only) GPIO                | O I/O                 | V DDEH6               | S                     | - / Up                  | - / Up                 | 416 324               |
| GPIO205               | P                     | GPIO205 19                                                                      | GPIO                                            | I/O                   | V DDEH8               | M                     | - / Up                  | - / Up                 | 416                   |
| GPIO [206:207]        | P                     | GPIO[206:207] 20 (can be selected assourcesforthe ADC trigger in the SIU_ETISR) | GPIO eQADC Trigger Input                        | I/O                   | V DDE3                | F                     | - / Up                  | - / Up                 | 416 324 208           |
| Clock Synthesizer (4) | Clock Synthesizer (4) | Clock Synthesizer (4)                                                           | Clock Synthesizer (4)                           | Clock Synthesizer (4) | Clock Synthesizer (4) | Clock Synthesizer (4) | Clock Synthesizer (4)   | Clock Synthesizer (4)  | Clock Synthesizer (4) |
| XTAL                  | P                     | XTAL                                                                            | Crystal Oscillator Output                       | O                     | V DDSYN               | AE                    | O / -                   | XTAL 21 / -            | 416 324 208           |
| EXTAL                 | P A                   | EXTAL 22 EXTCLK                                                                 | Crystal Oscillator Input External Clock Input   | I                     | V DDSYN               | AE                    | I / -                   | EXTAL 23 / -           | 416 324 208           |
| CLKOUT                | P                     | CLKOUT                                                                          | System Clock Output                             | O                     | V DDE5                | F                     | CLKOUT / Enabled        | CLKOUT/ Enabled        | 416 324               |
| ENGCLK                | P                     | ENGCLK                                                                          | Engineering Clock Output                        | O                     | V DDE5                | F                     | ENGCLK/ Enabled         | ENGCLK/ Enabled        | 416 324 208           |
| Power / Ground (77)   | Power / Ground (77)   | Power / Ground (77)                                                             | Power / Ground (77)                             | Power / Ground (77)   | Power / Ground (77)   | Power / Ground (77)   | Power / Ground (77)     | Power / Ground (77)    | Power / Ground (77)   |
| V RC33                | P                     | V RC33 24                                                                       | Voltage Regulator Control Supply                | I                     | 3.3V                  | -                     | I / -                   | V RC33                 | 416 324 208           |
| V RCVSS               | P                     | V RCVSS                                                                         | Voltage Regulator Control Ground                | I                     | -                     | -                     | I / -                   | V RCVSS                | 416 324 208           |
| V RCCTL               | P                     | V RCCTL                                                                         | Voltage Regulator Control Output                | O                     | 3.3V                  | -                     | O / -                   | V RCCTL                | 416 324 208           |
| V DDA0                | P                     | V DDA0 25                                                                       | Analog Power Input ADC0                         | I                     | 5.0V                  | -                     | I / -                   | V DDA0                 | 416 324 208           |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 2-1. MPC5553 Signal Properties  (continued)

| Signal and Range   | P/ A/ G   | Function 1   | Description                       | I/O Type   | Voltage 2   | Pad Type 3   | Status During Reset 4   | Status After Reset 5   | Package     |
|--------------------|-----------|--------------|-----------------------------------|------------|-------------|--------------|-------------------------|------------------------|-------------|
| V SSA0             | P         | V SSA0 25    | Analog Ground Input ADC0          | I          | -           | -            | I / -                   | V SSA0                 | 416 324 208 |
| V DDA1             | P         | V DDA1 25    | Analog Power Input                | I          | 5.0V        | -            | I / -                   | V DDA1                 | 416 324 208 |
| V SSA1             | P         | V SSA1 25    | Analog Ground Input               | I          | -           | -            | I / -                   | V SSA1                 | 416 324 208 |
| V DDSYN            | P         | V DDSYN      | Clock Synthesizer Power Input     | I          | 3.3V        | -            | I / -                   | V DDSYN                | 416 324 208 |
| V SSSYN            | P         | V SSSYN      | Clock Synthesizer Ground Input    | I          | -           | -            | I / -                   | V SSSYN                | 416 324 208 |
| V FLASH            | P         | V FLASH      | Flash Read Supply Input           | I          | 3.3V        | -            | I / -                   | V FLASH                | 416 324 208 |
| V PP               | P         | V PP 26      | Flash Program/Erase Supply Input  | I          | 5.0V        | -            | I / -                   | V PP                   | 416 324 208 |
| V STBY             | P         | V STBY 27    | Internal SRAM Standby Power Input | I          | TBD         | -            | I / -                   | V STBY                 | 416 324 208 |
| V DD               | P         | V DD         | Internal Logic Supply Input       | I          | 1.5V        | -            | I / -                   | V DD                   | 416 324 208 |
| V DDE              | P         | V DDE        | External I/O Supply Input         | I          | 1.8V - 3.3V | -            | I / -                   | V DDE                  | 416 324 208 |
| V DDEH             | P         | V DDEH 28    | External I/O Supply Input         | I          | 3.3V - 5.0V | -            | I / -                   | V DDEH                 | 416 324 208 |
| V DD33             | P         | V DD33 29    | 3.3V I/O Supply Input             | I          | 3.3V        | -            | I / -                   | 3.3V                   | 416 324 208 |
| V SS               | P         | V SS         | Ground                            | -          | -           | -            | I / -                   | V SS                   | 416 324 208 |

## Table 2-1. MPC5553 Signal Properties  (continued)

| Signal and Range   | P/ A/ G        | Function 1     | Description    | I/O Type       | Voltage 2      | Pad Type 3     | Status During Reset 4   | Status After Reset 5   | Package        |
|--------------------|----------------|----------------|----------------|----------------|----------------|----------------|-------------------------|------------------------|----------------|
| No Connect (2)     | No Connect (2) | No Connect (2) | No Connect (2) | No Connect (2) | No Connect (2) | No Connect (2) | No Connect (2)          | No Connect (2)         | No Connect (2) |
| NC 30              |                | NC             | No Connect     | -              | -              | -              | -                       | -                      | 416 324 208    |

- 1 For each pin in the table, each line in the Function column is a separate function of the pin. For all MPC5553 I/O pins the selection of primary pin function or secondary function or GPIO is done in the MPC5553 SIU except where explicitly noted.
- 2 The V DD E and VDDEH supply inputs are broken into segments. Each segment of slow I/O pins (VDDEH) may have a separate supply in the 3.3V to 5.0V range (+/- 5%). Each segment of fast I/O (VDDE) may have a separate supply in the 1.8V to 3.3V range (+/- 5%). Currently in the MPC5553 package, the V DDE2  and VDDE3 segments are shorted together into one segment. This segment is labelled V DDE2  in the ball map. See Table 2-4., 'MPC5554 Power/Ground Segmentation' for a definition of the I/O pins that are powered by each segment.
- 3 The pad type is indicated by one of the abbreviations; F for fast, M for medium, S for slow, A for analog, AE for analog with ESD protection circuitry. Some pads may have two types, depending on which pad function is selected.
- 4 Terminology is O - output, I - input, up - weak pull up enabled, down - weak pull down enabled, low - output driven low, high - output driven high. A dash on the left side of the slash denotes that both the input and output buffers for the pin are off. A dash on the right side of the slash denotes that there is no weak pull up/down enabled on the pin. The signal name to the left or right of the slash indicates the pin is enabled.
- 5 Function after reset of GPI is general-purpose input. A dash on the left side of the slash denotes that both the input and output buffers for the pin are off. A dash on the right side of the slash denotes that there is no weak pull up/down enabled on the pin.
- 6 BOOTCFG0 does not function in the 208 package of the MPC5553.
- 7 The EBI is specified and tested at 1.8V and 3.3V.
- 8 ADDR[8:11] and CS[0:3] pins must not be simultaneously configured to select ADDR[8:11].  Only one pin must be configured to provide the address input.
- 9 The function and state of these pins after execution of the BAM program is determined by the BOOTCFG[1:0] pins. See Table 16-6 for detail on the external bus interface (EBI) configuration after execution of the BAM program.
- 10 Although GPIO versus EBI function is specified in the SIU, when EBI function is chosen, the function must also be enabled in the EBI for these pins. The SIU and EBI configurations must match for proper operation.
- 11 GPIO versus EBI function for the WE[0:3]\_BE[0:3]\_GPIO[64:67] pins is specified in the SIU. When configured for EBI operation, the pin function of WE[0:3] or BE[0:3] is specified in the EBI\_BR0 -  EBI\_BR3 registers for each chip select region.
- 12 The BR and BG functionality is not implemented on the MPC5553, it is replaced by calibration functionality. The pin name on the ball map, however, does remain BR and BG. The primary functions are CAL\_ADDR10 and CAL\_ADDR11, respectively.
- 13 MCKO is only enabled if debug mode is enabled. Debug mode can be enabled before or after exiting System Reset (RSTOUT negated).
- 14 MDO[0] is driven high following a power-on reset until the system clock achieves lock, at which time it is then negated. There is an internal pull up on MDO[0].
- 15 The function of the MDO[11:4]\_GPIO[75:82] pins is selected during a debug port reset by the EVTI pin. When functioning as MDO[11:4] the pad configuration specified by the SIU does not apply. See Section 2.3.3.5, 'Nexus Message Data Out / GPIO (MDO[11:4]\_GPIO[82:75])' for more detail on MDO[11:4] pin operation.
- 16 The function and state of the CAN\_A and SCI\_A pins after execution of the BAM program is determined by the BOOTCFG[0:1] pins. See Table 16-8 for detail on the CAN and SCI pin configuration after execution of the BAM program.
- 17 All analog input channels are connected to both ADC blocks. The supply designation for this pin(s) specifies only the ESD rail used.
- 18 Because other balls already are named EMIOS[14:15], the balls for these signals are named GPIO[203:204].
- 19 The GPIO[205] pin is a protect for pin for configuring an external boot for a double data rate memory.
- 20 The GPIO[206:207] pins are protect for pins for double data rate memory data strobes.
- 21 The function after reset of the XTAL pin is determined by the value of the signal on the PLLCFG[1] pin. When bypass mode is chosen XTAL has no function and should be grounded.

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

- 22 When the FMPLL is configured for external reference mode, the V DDE5  supply affects the acceptable signal levels for the external reference. See Section 11.1.4.2, 'External Reference Mode.'
- 23 The function after reset of the EXTAL\_EXTCLK pin is determined by the value of the signal on the PLLCFG[0:1] pins. If the EXTCLK function is chosen, the valid operating voltage for the pin is 1.6V to 3.6V. If the EXTAL function is chosen, the valid operating voltage is 3.3V. Refer to Table 11-1.
- 24 VRC33  is the 3.3V input for the voltage regulator control.
- 25 The V DDA n and V SSA n supply inputs are split into separate traces in the package substrate. Each trace is bonded to a separate pad location, which provides isolation between the analog and digital sections within each ADC. The digital power/ground use pad\_vddint/pad\_vssint pads respectively. The analog power/ground use spcr\_filr\_32\_vdde/spcr\_filr\_32\_vsse pads respectively.
- 26 May be tied to 5.0V for both read operation and program/erase.
- 27 The V STBY  pin should be tied to V SSA 0 if the battery backed internal SRAM is not used.
- 28 The V DDEH9  segment may be powered from 3.0V to 5.0V for mux address or SSI functions, but must meet the V DDA 1 specifications of 4.5V to 5.25V for analog input function.
- 29 All pins with pad type pad\_fc will be driven to the high state if their VDDE segment is powered before V DD33 .
- 30 The pins are reserved for the clock and inverted clock outputs for DDR memory interface. In the MPC5553/MPC5554  416-pin package, the two NC pins are isolated (not shorted together in the package substrate)

## 2.2.2 MPC5554 Signals Summary

Table 2-2 gives a summary of the MPC5554 external signals and properties.

Table 2-2. MPC5554 Signal Properties

| Signal and Range 1                  | Pin                                                                                                         | P/A/G 2                             | Function 3                          | Description                                                          | I/O Type                            | Pad Type 4                          | Status During Reset 5               | Status After Reset 6                |
|-------------------------------------|-------------------------------------------------------------------------------------------------------------|-------------------------------------|-------------------------------------|----------------------------------------------------------------------|-------------------------------------|-------------------------------------|-------------------------------------|-------------------------------------|
| Reset / Configuration (8)           | Reset / Configuration (8)                                                                                   | Reset / Configuration (8)           | Reset / Configuration (8)           | Reset / Configuration (8)                                            | Reset / Configuration (8)           | Reset / Configuration (8)           | Reset / Configuration (8)           | Reset / Configuration (8)           |
| RESET                               | W26                                                                                                         | P                                   | RESET                               | External reset input                                                 | I                                   | S                                   | RESET / Up                          | RESET / Up                          |
| RSTOUT                              | V25                                                                                                         | P                                   | RSTOUT                              | External reset output                                                | O                                   | S                                   | RSTOUT/ Low                         | RSTOUT / High                       |
| PLLCFG0                             | AB25                                                                                                        | P A G                               | PLLCFG0 IRQ4 GPIO208                | FMPLL mode selection External interrupt request GPIO                 | I I I/O                             | M                                   | PLLCFG / Up                         | -/ Up                               |
| PLLCFG1                             | AA24                                                                                                        | P A A2 G                            | PLLCFG1 IRQ5 SOUTD GPIO209          | FMPLL mode selection External interrupt request DSPI D data out GPIO | I I O I/O                           | M                                   | PLLCFG / Up                         | -/ Up                               |
| RSTCFG                              | V26                                                                                                         | P A                                 | RSTCFG GPIO210                      | Reset configuration input GPIO                                       | I I/O                               | S                                   | RSTCFG/ Up                          | -/ Up                               |
| BOOTCFG[0:1]                        | AA25, Y24                                                                                                   | P A G                               | BOOTCFG[0:1] IRQ[2:3] GPIO[211:212] | Boot configuration input External interrupt request GPIO             | I I I/O                             | S                                   | BOOTCFG / Down                      | -/ Down                             |
| WKPCFG                              | Y23                                                                                                         | P G                                 | WKPCFG GPIO213                      | Weak pull configuration input GPIO                                   | I I/O                               | S                                   | WKPCFG/ Up                          | -/ Up                               |
| External Bus Interface (EBI) 7 (75) | External Bus Interface (EBI) 7 (75)                                                                         | External Bus Interface (EBI) 7 (75) | External Bus Interface (EBI) 7 (75) | External Bus Interface (EBI) 7 (75)                                  | External Bus Interface (EBI) 7 (75) | External Bus Interface (EBI) 7 (75) | External Bus Interface (EBI) 7 (75) | External Bus Interface (EBI) 7 (75) |
| CS[0:3]                             | P4, P3, P2, P1                                                                                              | P A G                               | CS[0:3] ADDR[8:11] GPIO[0:3]        | External chip selects External address bus GPIO                      | O I/O I/O                           | F                                   | -/ Up                               | -/ Up 8                             |
| ADDR[8:31]                          | V4, W3, W4, Y3, AA4, AA3, AB4, AB3, U1, V2, V1, W2, W1, Y2, Y1, AA2, AA1, AB2, AC1, AC2, AD1, AE1, AD2, AC3 | P G                                 | ADDR[8:31] GPIO[4:27]               | External address bus 9 GPIO                                          | I/O I/O                             | F                                   | -/ Up                               | -/ Up 8                             |

## Table 2-2. MPC5554 Signal Properties (continued)

| Signal and Range 1   | Pin                                                                                                                                                                | P/A/G 2   | Function 3                  | Description                                        | I/O Type       | Pad Type 4   | Status During Reset 5   | Status After Reset 6   |
|----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|-----------------------------|----------------------------------------------------|----------------|--------------|-------------------------|------------------------|
| DATA[0:31]           | AE8, AF9, AE9, AF10, AE10, AF12, AE11, AF13, AC11, AD11, AC12, AD12, AC14, AD13, AC15, AD14, AF3, AE4, AF4, AE5, AF6, AE6, AF7, AE7, AD5, AD6, AC6, AD7, AC7, AD8, | P G       | DATA[0:31] GPIO[28:59]      | External data bus 9 GPIO                           | I/O I/O        | F            | -/ Up                   | -/ Up 8                |
| TSIZ[0:1]            | T2, U2                                                                                                                                                             | P G       | TSIZ[0:1] GPIO[60:61]       | External transfer size 9 GPIO                      | I/O I/O        | F            | -/ Up                   | -/ Up 8                |
| RD_WR                | T3                                                                                                                                                                 | P G       | RD_WR GPIO62                | External read/write GPIO                           | I/O I/O        | F            | -/ Up                   | -/ Up 8                |
| BDIP                 | N1                                                                                                                                                                 | P G       | BDIP GPIO63                 | External burst data in progress GPIO               | O I/O          | F            | -/ Up                   | -/ Up 8                |
| WE[0:3]              | R4, R3, R2, R1                                                                                                                                                     | P A G     | WE[0:3] BE[0:3] GPIO[64:67] | External write enable External byte enable 10 GPIO | O O I/O        | F            | -/ Up                   | -/ Up 8                |
| OE                   | AE12                                                                                                                                                               | P G       | OE GPIO68                   | External output enable GPIO                        | O I/O          | F            | -/ Up                   | -/ Up 8                |
| TS                   | V3                                                                                                                                                                 | P G       | TS GPIO69                   | External transfer start GPIO                       | I/O I/O        | F            | -/ Up                   | -/ Up 8                |
| TA                   | U3                                                                                                                                                                 | P G       | TA GPIO70                   | External transfer acknowledge GPIO                 | I/O I/O        | F            | -/ Up                   | -/ Up 8                |
| TEA                  | N2                                                                                                                                                                 | P G       | TEA GPIO71                  | External transfer error acknowledge GPIO           | I/O I/O        | F            | -/ Up                   | -/ Up 8                |
| BR                   | AE13                                                                                                                                                               | P G       | BR GPIO72                   | External bus request 9 GPIO                        | I/O I/O        | F            | -/ Up                   | -/ Up 8                |
| BG                   | AE14                                                                                                                                                               | P G       | BG GPIO73                   | External bus grant 9 GPIO                          | I/O I/O        | F            | -/ Up                   | -/ Up 8                |
| BB                   | AF14                                                                                                                                                               | P G       | BB GPIO74                   | External bus busy 9 GPIO                           | I/O I/O        | F            | -/ Up                   | -/ Up 8                |
| NEXUS (18)           | EVTI                                                                                                                                                               | F25       | P                           | EVTI                                               | Nexus event in | I            | F                       | I / Up EVTI / Up       |

Table 2-2. MPC5554 Signal Properties (continued)

| Signal and Range 1   | Pin                                    | P/A/G 2        | Function 3               | Description                                             | I/O Type       | Pad Type 4     | Status During Reset 5   | Status After Reset 6   |
|----------------------|----------------------------------------|----------------|--------------------------|---------------------------------------------------------|----------------|----------------|-------------------------|------------------------|
| EVTO                 | F26                                    | P              | EVTO                     | Nexus event out                                         | O              | F              | O / Low                 | EVTO / High            |
| MCKO                 | G24                                    | P              | MCKO                     | Nexus message clock out                                 | O              | F              | O / Low                 | MCKO / Enabled 11      |
| MDO[3:0] 12          | C22, D21, C23, B24                     | P              | MDO[3:0]                 | Nexus message data out                                  | O              | F              | O / Low                 | MDO / Low              |
| MDO[11:4]            | A22, B21, C20, A23, B22, C21, D20, B23 | P G            | MDO[11:4] GPIO[75:82] 13 | Nexus message data out GPIO                             | O I/O          | F              | O / Low                 | -/ Down                |
| MSEO[1:0]            | G23, F23                               | P              | MSEO[1:0]                | Nexus message start/end out                             | O              | F              | O / High                | MSEO / High            |
| RDY                  | H23                                    | P              | RDY                      | Nexus ready output                                      | O              | F              | O / High                | RDY / High             |
| JTAG / TEST(6)       | JTAG / TEST(6)                         | JTAG / TEST(6) | JTAG / TEST(6)           | JTAG / TEST(6)                                          | JTAG / TEST(6) | JTAG / TEST(6) | JTAG / TEST(6)          | JTAG / TEST(6)         |
| TCK                  | D25                                    | P              | TCK                      | JTAG test clock input                                   | I              | F              | TCK / Down              | TCK / Down             |
| TDI                  | D26                                    | P              | TDI                      | JTAG test data input                                    | I              | F              | TDI / Up                | TDI / Up               |
| TDO                  | E25                                    | P              | TDO                      | JTAG test data output                                   | O              | F              | TDO / Up 14             | TDO / Up               |
| TMS                  | E24                                    | P              | TMS                      | JTAG test mode select input                             | I              | F              | TMS / Up                | TMS / Up               |
| JCOMP                | F24                                    | P              | JCOMP                    | JTAG TAP controller enable                              | I              | F              | JCOMP / Down            | JCOMP / Down           |
| TEST                 | E26                                    | P              | TEST                     | Test mode select                                        | I              | F              | TEST / Up               | TEST / Up              |
| FlexCAN (6)          | FlexCAN (6)                            | FlexCAN (6)    | FlexCAN (6)              | FlexCAN (6)                                             | FlexCAN (6)    | FlexCAN (6)    | FlexCAN (6)             | FlexCAN (6)            |
| CNTXA                | AD21                                   | P G            | CNTXA GPIO83             | FlexCAN A transmit GPIO                                 | O I/O          | S              | -/ Up                   | -/ Up 15               |
| CNRXA                | AE22                                   | P G            | CNRXA GPIO84             | FlexCAN A receive GPIO                                  | I I/O          | S              | -/ Up                   | -/ Up 15               |
| CNTXB                | AF22                                   | P A G          | CNTXB PCSC3 GPIO85       | FlexCAN B transmit DSPI C peripheral chip select 3 GPIO | O O I/O        | M              | -/ Up                   | -/ Up                  |
| CNRXB                | AF23                                   | P A G          | CNRXB PCSC4 GPIO86       | FlexCAN B receive DSPI C peripheral chip select 4 GPIO  | I O I/O        | M              | -/ Up                   | -/ Up                  |
| CNTXC                | V23                                    | P A G          | CNTXC PCSD3 GPIO87       | FlexCAN C transmit DSPI D peripheral chip select 3 GPIO | O O I/O        | M              | -/ Up                   | -/ Up                  |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## Table 2-2. MPC5554 Signal Properties (continued)

| Signal and Range 1   | Pin      | P/A/G 2   | Function 3          | Description                                                          | I/O Type   | Pad Type 4   | Status During Reset 5   | Status After Reset 6   |
|----------------------|----------|-----------|---------------------|----------------------------------------------------------------------|------------|--------------|-------------------------|------------------------|
| CNRXC                | W24      | P A G     | CNRXC PCSD4 GPIO88  | FlexCAN C receive DSPI D peripheral chip select 4 GPIO               | I O I/O    | M            | -/ Up                   | -/ Up                  |
| eSCI (4)             | eSCI (4) | eSCI (4)  | eSCI (4)            | eSCI (4)                                                             | eSCI (4)   | eSCI (4)     | eSCI (4)                | eSCI (4)               |
| TXDA                 | U24      | P G       | TXDA GPIO89         | eSCI A transmit GPIO                                                 | O I/O      | S            | -/ Up                   | -/ Up 15               |
| RXDA                 | V24      | P G       | RXDA GPIO90         | eSCI A receive GPIO                                                  | I I/O      | S            | -/ -                    | -/ - 15                |
| TXDB                 | W25      | P A G     | TXDB PCSD1 GPIO91   | eSCI B transmit DSPI D peripheral chip select 1 GPIO                 | O O I/O    | M            | -/ Up                   | -/ Up                  |
| RXDB                 | W23      | P A G     | RXDB PCSD5 GPIO92   | eSCI B receive DSPI D peripheral chip select 5 GPIO                  | I O I/O    | M            | -/ Up                   | -/ Up                  |
| DSPI(18)             | DSPI(18) | DSPI(18)  | DSPI(18)            | DSPI(18)                                                             | DSPI(18)   | DSPI(18)     | DSPI(18)                | DSPI(18)               |
| SCKA                 | R26      | P A G     | SCKA PCSC1 GPIO93   | DSPI A clock DSPI C peripheral chip select 1 GPIO                    | I/O O I/O  | M            | -/ Up                   | -/ Up                  |
| SINA                 | R25      | P A G     | SINA PCSC2 GPIO94   | DSPI A data input DSPI C peripheral chip select 2 GPIO               | I O I/O    | M            | -/ Up                   | -/ Up                  |
| SOUTA                | R24      | P A G     | SOUTA PCSC5 GPIO95  | DSPI A data output DSPI C peripheral chip select 5 GPIO              | O O I/O    | M            | -/ Up                   | -/ Up                  |
| PCSA0                | T24      | P A G     | PCSA0 PCSD2 GPIO96  | DSPI A peripheral chip select 0 DSPI D peripheral chip select 2 GPIO | I/O O I/O  | M            | -/ Up                   | -/ Up                  |
| PCSA1                | T23      | P A G     | PCSA1 PCSB2 GPIO97  | DSPI A peripheral chip select 1 DSPI B peripheral chip select 2 GPIO | O O I/O    | M            | -/ Up                   | -/ Up                  |
| PCSA2                | T25      | P A G     | PCSA2 SCKD GPIO98   | DSPI A peripheral chip select 2 DSPI D clock GPIO                    | O I/O I/O  | M            | -/ Up                   | -/ Up                  |
| PCSA3                | P23      | P A G     | PCSA3 SIND GPIO99   | DSPI A peripheral chip select DSPI D data input GPIO                 | O I I/O    | M            | -/ Up                   | -/ Up                  |
| PCSA4                | U23      | P A G     | PCSA4 SOUTD GPIO100 | DSPI A peripheral chip select DSPI D data output GPIO                | O O I/O    | M            | -/ Up                   | -/ Up                  |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 2-2. MPC5554 Signal Properties (continued)

| Signal and Range 1   | Pin       | P/A/G 2   | Function 3          | Description                                                          | I/O Type   | Pad Type 4   | Status During Reset 5   | Status After Reset 6   |
|----------------------|-----------|-----------|---------------------|----------------------------------------------------------------------|------------|--------------|-------------------------|------------------------|
| PCSA5                | U25       | P A G     | PCSA5 PCSB3 GPIO101 | DSPI A peripheral chip select 5 DSPI B peripheral chip select 3 GPIO | O O I/O    | M            | -/ Up                   | -/ Up                  |
| SCKB                 | P25       | P A G     | SCKB PCSC1 GPIO102  | DSPI B clock DSPI C peripheral chip select GPIO                      | I/O O I/O  | M            | -/ Up                   | -/ Up                  |
| SINB                 | M26       | P A G     | SINB PCSC2 GPIO103  | DSPI B data input DSPI C peripheral chip select GPIO                 | I O I/O    | M            | -/ Up                   | -/ Up                  |
| SOUTB                | N23       | P A G     | SOUTB PCSC5 GPIO104 | DSPI B data output DSPI C peripheral chip select GPIO                | O O I/O    | M            | -/ Up                   | -/ Up                  |
| PCSB0                | N25       | P A G     | PCSB0 PCSD2 GPIO105 | DSPI B peripheral chip select DSPI D peripheral chip select GPIO     | I/O O I/O  | M            | -/ Up                   | -/ Up                  |
| PCSB1                | N26       | P A G     | PCSB1 PCSD0 GPIO106 | DSPI B peripheral chip select DSPI D peripheral chip select GPIO     | O I/O I/O  | M            | -/ Up                   | -/ Up                  |
| PCSB2                | P26       | P A G     | PCSB2 SOUTC GPIO107 | DSPI B peripheral chip select DSPI C data output GPIO                | O O I/O    | M            | -/ Up                   | -/ Up                  |
| PCSB3                | N24       | P A G     | PCSB3 SINC GPIO108  | DSPI B peripheral chip select DSPI C data input GPIO                 | O I I/O    | M            | -/ Up                   | -/ Up                  |
| PCSB4                | P24       | P A G     | PCSB4 SCKC GPIO109  | DSPI B peripheral chip select DSPI C clock GPIO                      | O I/O I/O  | M            | -/ Up                   | -/ Up                  |
| PCSB5                | R23       | P A G     | PCSB5 PCSC0 GPIO110 | DSPI B peripheral chip select DSPI C peripheral chip select GPIO     | O I/O I/O  | M            | -/ Up                   | -/ Up                  |
| eQADC(45)            | eQADC(45) | eQADC(45) | eQADC(45)           | eQADC(45)                                                            | eQADC(45)  | eQADC(45)    | eQADC(45)               | eQADC(45)              |
| AN0                  | B7        | P A       | AN0 DAN0+           | Analog input Differential analog input                               | I          | AE           | I / -                   | AN0 / -                |
| AN1                  | A7        | P A       | AN1 DAN0-           | Analog input Differential analog input                               | I          | AE           | I / -                   | AN1 / -                |
| AN2                  | D9        | P A       | AN2 DAN1+           | Analog input Differential analog input                               | I          | AE           | I / -                   | AN2 / -                |
| AN3                  | C8        | P A       | AN3 DAN1-           | Analog input Differential analog input                               | I          | AE           | I / -                   | AN3 / -                |
| AN4                  | B8        | P A       | AN4 DAN2+           | Analog input Differential analog input                               | I          | AE           | I / -                   | AN4 / -                |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## Table 2-2. MPC5554 Signal Properties (continued)

| Signal and Range 1   | Pin                                                                                           | P/A/G 2   | Function 3               | Description                                       | I/O Type   | Pad Type 4   | Status During Reset 5   | Status After Reset 6   |
|----------------------|-----------------------------------------------------------------------------------------------|-----------|--------------------------|---------------------------------------------------|------------|--------------|-------------------------|------------------------|
| AN5                  | A8                                                                                            | P A       | AN5 DAN2-                | Analog input Differential analog input            | I          | AE           | I / -                   | AN5 / -                |
| AN6                  | D10                                                                                           | P A       | AN6 DAN3+                | Analog input Differential analog input            | I          | AE           | I / -                   | AN6 / -                |
| AN7                  | C9                                                                                            | P A       | AN7 DAN3-                | Analog input Differential analog input            | I          | AE           | I / -                   | AN7 / -                |
| AN8                  | C4                                                                                            | P A       | AN8 ANW                  | Analog input Mux input                            | I I        | AE           | I / -                   | AN8 / -                |
| AN9                  | D6                                                                                            | P A       | AN9 ANX                  | Analog input Mux input                            | I I        | AE           | I / -                   | AN9 / -                |
| AN10                 | D7                                                                                            | P A       | AN10 ANY                 | Analog input Mux input                            | I I        | AE           | I / -                   | AN10 / -               |
| AN11                 | A4                                                                                            | P A       | AN11 ANZ                 | Analog input Mux input                            | I I        | AE           | I / -                   | AN11 / -               |
| AN12                 | D15                                                                                           | P A A     | AN12 MA0 SDS             | Analog input Mux address eQADC serial data select | I O O      | A, M         | I / -                   | AN12 / -               |
| AN13                 | C15                                                                                           | P A A     | AN13 MA1 SDO             | Analog input Mux address eQADC serial data out    | I O O      | A, M         | I / -                   | AN13 / -               |
| AN14                 | B15                                                                                           | P A A     | AN14 MA2 SDI             | Analog input Mux address eQADC serial data in     | I O I      | A, M         | I / -                   | AN14 / -               |
| AN15                 | A15                                                                                           | P A       | AN15 FCK                 | Analog input eQADC free running clock             | I O        | A, M         | I / -                   | AN15 / -               |
| AN[16:39]            | A6, C5, D8, B5, B6, C7, B10, A10, D11, C11, B11, A11, A12, D12, C12, B12, B13, C13, D13, A13, | P         | AN[16:39]                | Analog input                                      | I          | AE           | I / -                   | AN[x] / -              |
| ETRIG[0:1]           | B16, A16                                                                                      | P G       | ETRIG[0:1] GPIO[111:112] | eQADC trigger input GPIO                          | I I/O      | S            | -/ Up                   | -/ Up                  |
| VRH                  | A9                                                                                            | P         | VRH                      | Voltage reference high                            | I          | -            | -/ -                    | VRH                    |
| VRL                  | C10                                                                                           | P         | VRL                      | Voltage reference low                             | I          | -            | -/ -                    | VRL                    |
| REFBYPC              | B9                                                                                            | P         | REFBYPC                  | Reference Bypass Capacitor Input                  | I          | AE           | -/ -                    | REFBYPC                |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 2-2. MPC5554 Signal Properties (continued)

| Signal and Range 1   | Pin                                            | P/A/G 2   | Function 3                             | Description                                                  | I/O Type   | Pad Type 4   | Status During Reset 5   | Status After Reset 6   |
|----------------------|------------------------------------------------|-----------|----------------------------------------|--------------------------------------------------------------|------------|--------------|-------------------------|------------------------|
| eTPU(66)             | eTPU(66)                                       | eTPU(66)  | eTPU(66)                               | eTPU(66)                                                     | eTPU(66)   | eTPU(66)     | eTPU(66)                | eTPU(66)               |
| TCRCLKA              | N4                                             | P A G     | TCRCLKA IRQ7 GPIO113                   | eTPU A TCR clock External interrupt request GPIO             | I I I/O    | S            | -/ Up                   | - / Up                 |
| ETPUA[0:11]          | N3, M4, M3, M2, M1, L4, L3, L2, L1, K4, K3, K2 | P A G     | ETPUA[0:11] ETPUA[12:23] GPIO[114:125] | eTPU A channel eTPU A channel (output only) GPIO             | I/O O I/O  | S            | -/ WKPCFG               | -/ WKPCFG              |
| ETPUA12              | K1                                             | P A G     | ETPUA12 PCSB1 GPIO126                  | eTPU A channel DSPI B peripheral chip select 1 GPIO          | I/O O I/O  | M            | -/ WKPCFG               | -/ WKPCFG              |
| ETPUA13              | J4                                             | P A G     | ETPUA13 PCSB3 GPIO127                  | eTPU A channel DSPI B peripheral chip select 3 GPIO          | I/O O I/O  | M            | -/ WKPCFG               | -/ WKPCFG              |
| ETPUA14              | J3                                             | P A G     | ETPUA14 PCSB4 GPIO128                  | eTPU A channel DSPI B peripheral chip select 4 GPIO          | I/O O I/O  | M            | -/ WKPCFG               | -/ WKPCFG              |
| ETPUA15              | J2                                             | P A G     | ETPUA15 PCSB5 GPIO129                  | eTPU A channel DSPI B peripheral chip select 5 GPIO          | I/O O I/O  | M            | -/ WKPCFG               | -/ WKPCFG              |
| ETPUA16              | J1                                             | P A G     | ETPUA16 PCSD1 GPIO130                  | eTPU A channel DSPI D peripheral chip select 1 GPIO          | I/O O I/O  | M            | -/ WKPCFG               | -/ WKPCFG              |
| ETPUA17              | H4                                             | P A G     | ETPUA17 PCSD2 GPIO131                  | eTPU A channel DSPI D peripheral chip select 2 GPIO          | I/O O I/O  | M            | -/ WKPCFG               | -/ WKPCFG              |
| ETPUA18              | H3                                             | P A G     | ETPUA18 PCSD3 GPIO132                  | eTPU A channel DSPI D peripheral chip select 3 GPIO          | I/O O I/O  | M            | -/ WKPCFG               | -/ WKPCFG              |
| ETPUA19              | H2                                             | P A G     | ETPUA19 PCSD4 GPIO133                  | eTPU A channel DSPI D peripheral chip select 4 GPIO          | I/O O I/O  | M            | -/ WKPCFG               | -/ WKPCFG              |
| ETPUA[20:23]         | H1, G4, G2, G1                                 | P A G     | ETPUA[20:23] IRQ[8:11] GPIO[134:137]   | eTPU A channel External interrupt request GPIO               | I/O I I/O  | M            | -/ WKPCFG               | -/ WKPCFG              |
| ETPUA[24:26]         | F1, G3, F3                                     | P A G     | ETPUA[24:26] IRQ[12:14] GPIO[138:140]  | eTPU A channel (output only) External interrupt request GPIO | O I I/O    | S            | -/ WKPCFG               | -/ WKPCFG              |
| ETPUA27              | F2                                             | P A G     | ETPUA27 IRQ15 GPIO141                  | eTPU A channel (output only) External interrupt request GPIO | O I I/O    | S            | -/ WKPCFG               | -/ WKPCFG              |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 2-2. MPC5554 Signal Properties (continued)

| Signal and Range 1   | Pin                                                                            | P/A/G 2   | Function 3                             | Description                                                       | I/O Type   | Pad Type 4   | Status During Reset 5   | Status After Reset 6   |
|----------------------|--------------------------------------------------------------------------------|-----------|----------------------------------------|-------------------------------------------------------------------|------------|--------------|-------------------------|------------------------|
| ETPUA28              | E1                                                                             | P A G     | ETPUA28 PCSC1 GPIO142                  | eTPU A Channel (Output Only) DSPI C peripheral chip select 1 GPIO | O O I/O    | M            | -/ WKPCFG               | -/ WKPCFG              |
| ETPUA29              | E2                                                                             | P A G     | ETPUA29 PCSC2 GPIO143                  | eTPU A Channel (Output Only) DSPI C peripheral chip select 2 GPIO | O O I/O    | M            | -/ WKPCFG               | -/ WKPCFG              |
| ETPUA30              | D1                                                                             | P A G     | ETPUA30 PCSC3 GPIO144                  | eTPU A Channel DSPI C peripheral chip select 3 GPIO               | I/O O I/O  | M            | -/ WKPCFG               | -/ WKPCFG              |
| ETPUA31              | D2                                                                             | P A G     | ETPUA31 PCSC4 GPIO145                  | eTPU A Channel DSPI C peripheral chip select 4 GPIO               | I/O O I/O  | M            | -/ WKPCFG               | -/ WKPCFG              |
| TCRCLKB              | M23                                                                            | P A G     | TCRCLKB IRQ6 GPIO146                   | eTPU B TCR clock External Interrupt Request GPIO                  | I I I/O    | S            | -/ Up                   | - / Up                 |
| ETPUB[0:15]          | M25, M24, L26, L25, L24, K26, L23, K25, K24, J26, K23, J25, J24, H26, H25, G26 | P A G     | ETPUB[0:15] ETPUB[16:31] GPIO[147:162] | eTPU B channel eTPU B channel (output only) GPIO                  | I/O O I/O  | S            | -/ WKPCFG               | -/ WKPCFG              |
| ETPUB16              | D16                                                                            | P A G     | ETPUB16 PCSA1 GPIO163                  | eTPU B channel DSPI A peripheral chip select 1 GPIO               | I/O O I/O  | S            | -/ WKPCFG               | -/ WKPCFG              |
| ETPUB17              | D17                                                                            | P A G     | ETUB17 PCSA2 GPIO164                   | eTPU B channel DSPI A peripheral chip select 2 GPIO               | I/O O I/O  | S            | -/ WKPCFG               | -/ WKPCFG              |
| ETPUB18              | A17                                                                            | P A G     | ETUB18 PCSA3 GPIO165                   | eTPU B channel DSPI Aperipheral chip select 3 GPIO                | I/O O I/O  | S            | -/ WKPCFG               | -/ WKPCFG              |
| ETPUB19              | C16                                                                            | P A G     | ETUB19 PCSA4 GPIO166                   | eTPU B channel DSPI A peripheral chip select 4 GPIO               | I/O O I/O  | S            | -/ WKPCFG               | -/ WKPCFG              |
| ETPUB[20:31]         | A18, B17, C17, D18, A19, B18, C18, A20, B19, D19, C19, B20                     | P G       | ETPUB[20:31] GPIO[167:178]             | eTPU B channel GPIO                                               | I/O I/O    | S            | -/ WKPCFG               | -/ WKPCFG              |

## Table 2-2. MPC5554 Signal Properties (continued)

| Signal and Range 1    | Pin                                                        | P/A/G 2               | Function 3                                                                     | Description                                                 | I/O Type              | Pad Type 4            | Status During Reset 5   | Status After Reset 6   |
|-----------------------|------------------------------------------------------------|-----------------------|--------------------------------------------------------------------------------|-------------------------------------------------------------|-----------------------|-----------------------|-------------------------|------------------------|
| eMIOS(24)             | eMIOS(24)                                                  | eMIOS(24)             | eMIOS(24)                                                                      | eMIOS(24)                                                   | eMIOS(24)             | eMIOS(24)             | eMIOS(24)               | eMIOS(24)              |
| EMIOS[0:9]            | AF15, AE15, AC16, AD15, AF16, AE16, AD16, AF17, AC17, AE17 | P A G                 | EMIOS[0:9] ETPUA[0:9] GPIO[179:188]                                            | eMIOS channel eTPU A channel (output only) GPIO             | I/O O I/O             | S                     | -/ WKPCFG               | -/ WKPCFG              |
| EMIOS10               | AD17                                                       | P G                   | EMIOS10 GPIO189                                                                | eMIOS channel GPIO                                          | I/O I/O               | S                     | -/ WKPCFG               | -/ WKPCFG              |
| EMIOS11               | AF18                                                       | P G                   | EMIOS11 GPIO190                                                                | eMIOS channel GPIO                                          | I/O I/O               | S                     | -/ WKPCFG               | -/ WKPCFG              |
| EMIOS12               | AC18                                                       | P A G                 | EMIOS12 SOUTC GPIO191                                                          | eMIOS channel (output only) DSPI C data output GPIO         | O O I/O               | M                     | -/ WKPCFG               | -/ WKPCFG              |
| EMIOS13               | AE18                                                       | P A G                 | EMIOS13 SOUTD GPIO192                                                          | eMIOS channel (output only) DSPI D data output GPIO         | O O I/O               | M                     | -/ WKPCFG               | -/ WKPCFG              |
| EMIOS[14:15]          | AF19, AD18                                                 | P A G                 | EMIOS[14:15] IRQ[0:1] GPIO[193:194]                                            | eMIOS channel (output only) External interrupt request GPIO | O I I/O               | S                     | -/ WKPCFG               | -/ WKPCFG              |
| EMIOS[16:23]          | AE19, AD19, AF20, AE20, AF21, AC19, AD20, AE21             | P A G                 | EMIOS[16:23] ETPUB[0:7] GPIO[195:202]                                          | eMIOS channel eTPU B channel (output only) GPIO             | I/O O I/O             | S                     | -/ WKPCFG               | -/ WKPCFG              |
| GPIO(5)               | GPIO(5)                                                    | GPIO(5)               | GPIO(5)                                                                        | GPIO(5)                                                     | GPIO(5)               | GPIO(5)               | GPIO(5)                 | GPIO(5)                |
| GPIO[203:204] 16      | H24, G25                                                   | P A                   | EMIOS[14:15] GPIO[203:204] Note: EMIOS is primary function                     | eMIOS channel (output only) GPIO                            | O I/O                 | S                     | - / Up                  | - / Up                 |
| GPIO205               | A21                                                        | P                     | GPIO205 17                                                                     | GPIO                                                        | I/O                   | M                     | -/ Up                   | -/ Up                  |
| GPIO[206:207]         | AF8, AD10                                                  | P                     | GPIO[206:207] 18 (can be selected assources for the ADCtriggerinthe SIU_ETISR) | GPIO                                                        | I/O                   | F                     | -/ Up                   | -/ Up                  |
| Clock Synthesizer (6) | Clock Synthesizer (6)                                      | Clock Synthesizer (6) | Clock Synthesizer (6)                                                          | Clock Synthesizer (6)                                       | Clock Synthesizer (6) | Clock Synthesizer (6) | Clock Synthesizer (6)   | Clock Synthesizer (6)  |
| XTAL                  | AB26                                                       | P                     | XTAL                                                                           | Crystal oscillator output                                   | O                     | AE                    | O / -                   | XTAL 19 / -            |
| EXTAL                 | AA26                                                       | P A                   | EXTAL EXTCLK 20                                                                | Crystal oscillator input External clock input               | I                     | AE                    | I / -                   | EXTAL 21 / -           |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## Table 2-2. MPC5554 Signal Properties (continued)

| Signal and Range 1   | Pin                                                                                                                             | P/A/G 2             | Function 3          | Description                      | I/O Type            | Pad Type 4          | Status During Reset 5   | Status After Reset 6   |
|----------------------|---------------------------------------------------------------------------------------------------------------------------------|---------------------|---------------------|----------------------------------|---------------------|---------------------|-------------------------|------------------------|
| CLKOUT               | AE24                                                                                                                            | P                   | CLKOUT              | System clock output              | O                   | F                   | CLKOUT / Enabled        | CLKOUT / Enabled       |
| ENGCLK               | AF25                                                                                                                            | P                   | ENGCLK              | Engineering clock output         | O                   | F                   | O / Low                 | ENGCLK / Low           |
| Power / Ground (76)  | Power / Ground (76)                                                                                                             | Power / Ground (76) | Power / Ground (76) | Power / Ground (76)              | Power / Ground (76) | Power / Ground (76) | Power / Ground (76)     | Power / Ground (76)    |
| V RC33               | AC25                                                                                                                            | P                   | V RC33 22           | Voltage regulator control supply | I                   | -                   | I / -                   | V RC33                 |
| V RCVSS              | Y25                                                                                                                             | P                   | V RCVSS             | Voltage regulator control ground | I                   | -                   | I / -                   | V RCVSS                |
| V RCCTL              | AB24                                                                                                                            | P                   | V RCCTL             | Voltage regulator control output | O                   | -                   | O / -                   | V RCCTL                |
| V DDA0               | C14                                                                                                                             | P                   | V DDA0 23           | Analog power input               | I                   | -                   | I / -                   | V DDA0                 |
| V SSA0               | A14, B14                                                                                                                        | P                   | V SSA0 23           | Analog ground input              |                     | -                   | I / -                   | V SSA0                 |
| V DDA1               | A5                                                                                                                              | P                   | V DDA1 23           | Analog power input               | I                   | -                   | I / -                   | V DDA1                 |
| V SSA1               | C6                                                                                                                              | P                   | V SSA1 23           | Analog ground input              | I                   | -                   | I / -                   | V SSA1                 |
| V DDSYN              | AC26                                                                                                                            | P                   | V DDSYN             | Clock synthesizer power input    | I                   | -                   | I / -                   | V DDSYN                |
| V SSSYN              | Y26                                                                                                                             | P                   | V SSSYN             | Clock synthesizer ground input   | I                   | -                   | I / -                   | V SSSYN                |
| V FLASH              | U26                                                                                                                             | P                   | V FLASH             | Flash read supply input          | I                   | -                   | I / -                   | V FLASH                |
| V PP                 | T26                                                                                                                             | P                   | V PP 24             | Flash program/erase supply input | I                   | -                   | I / -                   | V PP                   |
| V STBY               | A2                                                                                                                              | P                   | V STBY 25           | SRAM standby power input         | I                   | -                   | I / -                   | V STBY                 |
| V DD                 | A24, B1, C2, C26, D3, E4, AB23, AC5, AC24, AD4, AD25, AE3, AE26, AF2                                                            | P                   | V DD                | Internal logic supply input      | I                   | -                   | I / -                   | V DD                   |
| V DDE2               | T1, T4, Y4, AB1, AF5, AC8, AF11, AC13, M10, N10, P10, R10, T10, M11, N11, P11, R11, U11, T12, U12, T13, U13, T14, U14, T15, U15 | P                   | v DDE               | External I/O supply input        | I                   | -                   | I / -                   | v DDE                  |
| V DDE5               | AC21, AD22, AE23, AF24                                                                                                          | P                   | v DDE               | External I/O supply input        | I                   | -                   | I / -                   | v DDE                  |

## Table 2-2. MPC5554 Signal Properties (continued)

| Signal and Range 1   | Pin                                                                                                                                                                                                                                                                 | P/A/G 2        | Function 3     | Description                    | I/O Type       | Pad Type 4     | Status During Reset 5   | Status After Reset 6   |
|----------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------|----------------|--------------------------------|----------------|----------------|-------------------------|------------------------|
| V DDE7               | B26, C25, D24, E23, K14, K15, K16, K17, L17, M17, N17                                                                                                                                                                                                               | P              | v DDE          | External I/O supply input      | I              | -              | I / -                   | v DDE                  |
| V DDEH1              | E3, F4                                                                                                                                                                                                                                                              | P              | v DDEH         | External I/O high supply input | I              | -              | I / -                   | v DDEH                 |
| V DDEH4              | AC20                                                                                                                                                                                                                                                                | P              | v DDEH         | External I/O high supply input | I              | -              | I / -                   | v DDEH                 |
| V DDEH6              | AA23, J23                                                                                                                                                                                                                                                           | P              | v DDEH         | External I/O high supply input | I              | -              | I / -                   | v DDEH                 |
| V DDEH8              | D22                                                                                                                                                                                                                                                                 | P              | v DDEH         | External I/O high supply input | I              | -              | I / -                   | v DDEH                 |
| V DDEH9              | D14                                                                                                                                                                                                                                                                 | P              | V DDEH 26      | External I/O high supply input | I              | -              | I / -                   | V DDEH                 |
| V DD33               | C1, U4, AD9,                                                                                                                                                                                                                                                        | P              | V DD33 27      | 3.3V I/O supply input          | I              | -              | I / -                   | V DD33                 |
| V SS                 | A25, AD26 A1, AF1, B2, AE2, C3, AD3, D4, AC4, D23, C24, B25, A26, AD24, AE 25, AF26, K10, K11, K12, K13, L10, L11, L12, L13, L14, L15, L16, M12, M13, M14, M15, M16, N12, N13, N14, N15, N16, P12, P13, P14, P15, P16, P17, R12, R13, R14, R15, R16, R17, T11, T16, | P              | V SS           | Ground                         |                | -              | I / -                   | V SS                   |
| No Connect (2)       | No Connect (2)                                                                                                                                                                                                                                                      | No Connect (2) | No Connect (2) | No Connect (2)                 | No Connect (2) | No Connect (2) | No Connect (2)          | No Connect (2)         |
| NC                   | AC22,AD23                                                                                                                                                                                                                                                           |                | NC 28          | No Connect                     | -              | -              | -                       | -                      |

1 This is the pin name that appears on the PBGA pinout.

- 2 Primary, alternate, or GPIO function. Note that some pins may have a third function rather than, or in addtion to GPIO.
- 3 For each pin in the table, each line in the function column is a separate function of the pin. For all MPC5554 I/O pins the selection of primary, secondary or tertiary function is done in the MPC5554 SIU except where explicitly noted.
- 4 The pad type is indicated by one of the abbreviations; F for fast, M for medium, S for slow, A for analog, AE for analog with ESD protection circuitry. Some pads may have two types, depending on which pad function is selected.
- 5 Terminology is O - output, I - input, up - weak pull up enabled, down - weak pull down enabled, low - output driven low, High - output driven high. A dash on the left side of the slash denotes that both the input and output buffers for the pin are off. A dash on the right side of the slash denotes that there is no weak pull up/down enabled on the pin. The signal name to the left or right of the slash indicates the pin is enabled.
- 6 Function after reset of GPI is general-purpose input. A dash on the left side of the slash denotes that both the input and output buffers for the pin are off. A dash on the right side of the slash denotes that there is no weak pull up/down enabled on the pin.
- 7 The EBI is specified and tested at 1.8V and 3.3V.
- 8 The function and state of this pin  after execution of the BAM  program is determined by the BOOTCFG[0:1] pins. See Table 16-6 for detail on the external bus interface (EBI) configuration after execution of the BAM program.
- 9 Although GPIO versus EBI function is specified in the SIU, when EBI function is chosen, the function must also be enabled in the EBI for these pins. The SIU and EBI configurations must match for proper operation.
- 10 GPIO versus EBI function for the WE[0:3]\_BE[0:3]\_GPIO[64:67] pins is specified in the SIU. When configured for EBI operation, the pin function of WE[0:3] or BE[0:3] is specified in the EBI\_BR0-EBI\_BR3 registers for each chip select region.
- 11 MCKO is only enabled if debug mode is enabled. Debug mode can be enabled before or after exiting System Reset (RSTOUT negated).
- 12 MDO[0] is driven high following a power-on reset until the system clock achieves lock, at which time it is then negated. There is an internal pull up on MDO[0].
- 13 The function of the MDO[11:4]\_GPIO[75:82] pins is selected during a debug port reset by the EVTI pin. When functioning as MDO[11:4] the pad configuration specified by the SIU does not apply.
- 14 The pull-up on TDO is only functional when not in JTAG mode, that is with JCOMP negated.
- 15 The function and state of the FlexCAN\_A and eSCI\_A pins after execution of the BAM program is determined by the BOOTCFG[0:1] pins.
- 16 Because other balls already are named EMIOS[14:15], the balls for these signals are named GPIO[203:204].
- 17 The GPIO205 pin is a protect for pin for configuring an external boot for a double data rate memory.
- 18 The GPIO[207:206] pins are protect for pins for double data rate memory data strobes.
- 19 The function after reset of the XTAL pin is determined by the value of the signal on the PLLCFG[1] pin. When bypass mode is chosen XTAL has no function and should be grounded.
- 20 When the FMPLL is configured for external reference mode, the V DDE5  supply affects the acceptable signal levels for the external reference. See Section 11.1.4.2, 'External Reference Mode.'
- 21 The function after reset of the EXTAL\_EXTCLK pin is determined by the value of the signal on the PLLCFG[0:1] pins. If the EXTCLK function is chosen, the valid operating voltage for the pin is 1.6V to 3.6V. If the EXTAL function is chosen, the valid operating voltage is 3.3V. Refer to Table 11-1.
- 22 V RC33  is the 3.3V input for the voltage regulator control.
- 23 The V DDA n and V SSA n supply inputs are split into separate traces in the package substrate. Each trace is bonded to a separate pad location, which provides isolation between the analog and digital sections within each ADC. The digital power/ground use pad\_vddint/pad\_vssint pads respectively. The analog power/ground use spcr\_filr\_32\_vdde/spcr\_filr\_32\_vsse pads respectively.
- 24 May be tied to 5.0V for both read operation and program/erase.
- 25 The V STBY  pin should be tied to V SS  if the battery backed SRAM is not used.
- 26 The V DDEH9  segment may be powered from 3.0V to 5.0V for mux address or SSI functions, but must meet the V DDA 1 specifications of 4.5V to 5.25V for analog input function.
- 27 All pins will be driven to the high state if their V DDE  segment is powered before the V DD33  supply.
- 28 The pins are reserved for the clock and inverted clock outputs for DDR memory interface. In the MPC5553/MPC5554  416-pin package, the two NC pins are isolated (not shorted together in the package substrate)

## 2.3 Detailed Signal Description

Below are detailed descriptions of the signals that occur on both the MPC5553 and the MPC5554.  Some signals are implemented only on one device or the other; these signals are marked MPC5553 Only or MPC5554 Only. Signals not so marked function on both devices.

## 2.3.1 Reset / Configuration

## 2.3.1.1 External Reset Input (RESET)

The RESET input is asserted by an external device to reset the all modules of the MPC5553/MPC5554 MCU. The RESET pin should be asserted during a power-on reset. Refer to Section 4.2.1, 'Reset Input (RESET).'

## 2.3.1.2 External Reset Output (RSTOUT)

The RSTOUT output is a push/pull output that is asserted during an internal MPC5553/MPC5554 reset. The pin may also be asserted by software without causing an internal reset of the MPC5553/MPC5554 MCU. Refer to Section 4.2.2, 'Reset Output (RSTOUT).'

## NOTE

During a power on reset, RSTOUT is tri-stated.

## 2.3.1.3 FMPLL Mode Selection / External Interrupt Request / GPIO (PLLCFG0\_IRQ4\_GPIO208)

PLLCFG0\_IRQ4\_GPIO208 are sampled on the negation of the RESET input pin, if the RSTCFG pin is asserted  at  that  time.  The  values  are  used  to  configure  the  FMPLL  mode  of  operation.  The  alternate function is external interrupt request input.

## 2.3.1.4 FMPLL Mode Selection / External Interrupt Request / DSPI / GPIO (PLLCFG1\_IRQ5\_SOUTD\_GPIO209)

PLLCFG1\_IRQ5\_SOUTD\_GPIO209  are  sampled  on  the  negation  of  the  RESET  input  pin,  if  the RSTCFG pin is asserted at that time. The values are used to configure the FMPLL mode of operation. The alternate functions are external interrupt request input, and data output for the DSPI module D.

## 2.3.1.5 Reset Configuration Input / GPIO (RSTCFG\_GPIO210)

The RSTCFG input is used to enable the BOOTCFG[0:1] and PLLCFG[0:1] pins during reset. If RSTCFG is negated during reset, the BOOTCFG and PLLCFG pins are not sampled at the negation of RSTOUT. In that case, the default values for BOOTCFG and PLLCFG are used. If RSTCFG is asserted during reset, the values on the BOOTCFG and PLLCFG pins are sampled and configure the boot and FMPLL modes.

## 2.3.1.6 Reset Configuration / External Interrupt Request / GPIO (BOOTCFG[0:1]\_IRQ[2:3]\_GPIO[211:212])

BOOTCFG[0:1]\_IRQ[2:3]\_GPIO[211:212]  are  sampled  on  the  negation  of  the  RSTOUT  pin,  if  the RSTCFG pin is asserted at that time. The values are used by the BAM program to determine the boot configuration of the MPC5553/MPC5554. The alternate function is external interrupt request inputs. Note that in the 208 package of the MPC5553, BOOTCFG0 does not function.

## 2.3.1.7 Weak Pull Configuration / GPIO (WKPCFG\_GPIO213)

WKPCFG\_GPIO213 determines whether specified eTPU and EMIOS pins are connected to a weak pull up or weak pull down during and immediately after reset.

## 2.3.2 External Bus Interface (EBI)

## 2.3.2.1 External Chip Selects / External Address / GPIO (CS[0:3]\_ADDR[8:11]\_GPIO[0:3])

CS[0:3]\_ADDR[8:11]\_GPIO[0:3] are the external bus interface (EBI) chip select output signals. They can be individually configured as chip selects or GPIO. CS[1:3]\_ADDR[9:11]\_GPIO[1:3] are not pinned out in the 208 PBGA of the MPC5553.

## 2.3.2.2 External Address / Calibration Address / GPIO (ADDR[8:11]\_CAL\_ADDR[27:30]\_GPIO[4:7]) - MPC5553 Only

ADDR[8:11]\_ADDR[27:30]\_GPIO[4:7] are the EBI address and calibration signals.

## 2.3.2.3 External Address /  GPIO (ADDR[12:31]\_GPIO[8:27])

ADDR[12:31]\_GPIO[8:27] are the EBI address signals.

## 2.3.2.4 External Data - MPC5554 Only

Both the MPC5553 and the MPC5554 can be configured for 16-bit or 32-bit data bus operation.

## 2.3.2.4.1 External Data / GPIO (DATA[0:31]\_GPIO[28:59]) - MPC5554 Only

DATA[0:31]\_GPIO[28:59] are the EBI data signals. The multiplexing of DATA[0:31]\_GPIO[28:59] occur in the MPC5554 only.

## 2.3.2.5 External Data - MPC5553 Only

## 2.3.2.5.1 External Data / GPIO (DATA[0:15]\_GPIO[28:43]) - MPC5553 Only

## 2.3.2.5.2 DATA[0:15]\_GPIO[28:43] are the EBI data signals. The data signals can be split as half data and half GPIO for 16-bit data bus operation. External Data / FEC / Calibration Data / GPIO (DATA16\_TX\_CLK\_CAL\_DATA0\_GPIO44) - MPC5553 Only

DATA16\_TX\_CLK\_CAL\_DATA0\_GPIO44 are the EBI, FEC transmit clock, and calibration data signals.

## 2.3.2.5.3 External Data / FEC / Calibration Data / GPIO (DATA17\_CRS\_CAL\_DATA1\_GPIO45) - MPC5553 Only

DATA17\_CRS\_CAL\_DATA1\_GPIO45 are the EBI, FEC carrier sense, and calibration signals.

## 2.3.2.5.4 External Data / FEC / Calibration Data / GPIO (DATA18\_TX\_ER\_CAL\_DATA2\_GPIO46) - MPC5553 Only

DATA18\_TX\_ER\_CAL\_DATA2\_GPIO46 are the EBI, FEC transmit error, and calibration signals.

## 2.3.2.5.5 External Data / FEC / Calibration Data / GPIO (DATA19\_RX\_CLK\_CAL\_DATA3\_GPIO47) - MPC5553 Only

DATA19\_RX\_CLK\_CAL\_DATA3\_GPIO47 are the EBI, FEC receive clock, and calibration signals.

## 2.3.2.5.6 External Data / FEC / Calibration Data / GPIO (DATA20\_TXD0\_CAL\_DATA4\_GPIO48) - MPC5553 Only

DATA20\_TXD0\_CAL\_DATA4\_GPIO48 are the EBI, FEC transmit data, and calibration signals.

## 2.3.2.5.7 External Data / FEC / Calibration Data / GPIO (DATA21\_RX\_ER\_CAL\_DATA5\_GPIO49) - MPC5553 Only

DATA21\_RX\_ER\_CAL\_DATA5\_GPIO49 are the EBI, FEC receive error, and calibration signals.

## 2.3.2.5.8 External Data / FEC / Calibration Data / GPIO (DATA22\_RXD0\_CAL\_DATA6\_GPIO50) - MPC5553 Only

DATA22\_RXD0\_CAL\_DATA6\_GPIO50 are the EBI, FEC receive data, and calibration signals.

## 2.3.2.5.9 External Data / FEC / Calibration Data / GPIO (DATA23\_TXD3\_CAL\_DATA7\_GPIO51) - MPC5553 Only

DATA23\_TXD3\_CAL\_DATA7\_GPIO51 are the EBI, FEC transmit data, and calibration signals.

## 2.3.2.5.10 External Data / FEC / Calibration Data / GPIO (DATA24\_COL\_CAL\_DATA8\_GPIO52) - MPC5553 Only

DATA24\_COL\_CAL\_DATA8\_GPIO52 are the EBI, FEC collision detect, and calibration signals.

## 2.3.2.5.11 External Data / FEC / Calibration Data / GPIO (DATA25\_RX\_DV\_CAL\_DATA9\_GPIO53) - MPC5553 Only

DATA25\_RX\_DV\_CAL\_DATA9\_GPIO53 are the EBI, FEC receive data valid, and calibration signals.

## 2.3.2.5.12 External Data / FEC / Calibration Data / GPIO (DATA26\_TX\_EN\_CAL\_DATA10\_GPIO54) - MPC5553 Only

DATA26\_TX\_EN\_CAL\_DATA10\_GPIO54 are the EBI, FEC transmit enable, and calibration signals.

## 2.3.2.5.13 External Data / FEC / Calibration Data / GPIO (DATA27\_TXD2\_CAL\_DATA11\_GPIO55) - MPC5553 Only

DATA27\_TXD2\_CAL\_DATA11\_GPIO55 are the EBI, FEC transmit data, and calibration signals.

## 2.3.2.5.14 External Data / FEC / Calibration Data / GPIO (DATA28\_TXD1\_CAL\_DATA12\_GPIO56) - MPC5553 Only

DATA28\_TXD1\_CAL\_DATA12\_GPIO56 are the EBI, FEC transmit data, and calibration signals.

## 2.3.2.5.15 External Data / FEC / Calibration Data / GPIO (DATA29\_RXD1\_CAL\_DATA13\_GPIO57) - MPC5553 Only

DATA29\_RXD1\_CAL\_DATA13\_GPIO57 are the EBI, FEC receive data, and calibration signals.

## 2.3.2.5.16 External Data / FEC / Calibration Data / GPIO (DATA30\_RXD2\_CAL\_DATA14\_GPIO58) - MPC5553 Only

DATA30\_RXD2\_CAL\_DATA14\_GPIO58 are the EBI, FEC receive data, and calibration signals.

## 2.3.2.5.17 External Data / FEC / Calibration Data / GPIO (DATA31\_RXD3\_CAL\_DATA15\_GPIO59) - MPC5553 Only

DATA31\_RXD3\_CAL\_DATA15\_GPIO59 are the EBI, FEC receive data, and calibration signals.

## 2.3.2.6 External Transfer Size / GPIO (TSIZ[0:1]\_GPIO[60:61]) - MPC5554 Only

TSIZ[0:1]\_GPIO[60:61] indicate the size of an external bus transfer when in external master operation or in slave mode. The TSIZ[0:1] signals are not driven by the EBI in single master operation.  The MPC5553 has no TSIZ[0:1].

## 2.3.2.7 External Read/Write / GPIO (RD\_WR\_GPIO62)

RD\_WR\_GPIO62 indicates whether an external bus transfer is a read or write operation.

## 2.3.2.8 External Burst Data In Progress / GPIO (BDIP\_GPIO63)

BDIP\_GPIO63 indicates that an EBI burst transfer is in progress.

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## 2.3.2.9 Write Enables

## 2.3.2.9.1 External Write/Byte Enable / GPIO

(WE[0:3]\_BE[64:67]\_GPIO[64:67]) - MPC5554 Only

WE[0:3]\_BE[0:3]\_GPIO[64:67] specify which data pins contain valid data for an external bus transfer.

## 2.3.2.9.2 External Write/Byte Enable / GPIO

(WE[0:1]\_BE[0:1]\_GPIO[64:65]) - MPC5553 Only

WE[0:1]\_BE[0:1]\_GPIO[64:65] specify which data pins contain valid data for an external bus transfer.

## 2.3.2.9.3 External Write/Byte Enable / Calibration Write Enable / GPIO (WE[2:3]\_BE[2:3]\_CAL\_WE[0:1]\_GPIO[66:67]) - MPC5553 Only

WE[2:3]\_BE[2:3]\_CAL\_WE[0:1]\_GPIO[66:67] specify which data pins contain valid data for an external bus transfer and provide write enables for calibration in the MPC5553.

## 2.3.2.10 External Output Enable / GPIO (OE\_GPIO68)

OE\_GPIO68 indicates that the EBI is ready to accept read data.

## 2.3.2.11 External Transfer Start / GPIO (TS\_GPIO69)

TS\_GPIO69 is asserted by the EBI owner to indicate the start of a transfer.

## 2.3.2.12 External Transfer Acknowledge (TA\_GPIO70)

TA\_GPIO70 is asserted by the EBI owner to acknowledge that the slave has completed the current transfer.

## 2.3.2.12.1 External Transfer Error Acknowledge / GPIO (TEA\_GPIO71) - MPC5554 Only

TEA\_GPIO71 indicates that an error occurred in the current external bus transfer.

## 2.3.2.12.2 External Transfer Error Acknowledge / Calibration Chip Select / GPIO (TEA\_CAL\_CS0\_GPIO71) - MPC5553 Only

TEA\_CA;\_CS0\_GPIO71 indicates that an error occurred in the current external bus transfer, and provides a calibration chip select function in the MPC5553.

## 2.3.2.13 Calibration Address 1  / FEC / Calibration Chip Select / GPIO (CAL\_ADDR10\_MDC\_CAL\_CS2\_GPIO72) - MPC5553 Only

CAL\_ADDR10\_MDC\_CAL\_CS2\_GPIO72  are  the  calibration  and  FEC  management  clock  output signals.  Note that BR is not implemented on the MPC5553.

## 2.3.2.14 External Bus Request / GPIO (BR\_GPIO72) - MPC5554 Only

BR\_GPIO72 is used by an external bus master to request ownership of the EBI from the arbiter. BR is only functional on the MPC5554.

## 2.3.2.15 Calibration Address 1  / FEC / Calibration Chip Select / GPIO (CAL\_ADDR11\_MDIO\_CAL\_CS3\_GPIO73) - MPC5553 Only

CAL\_ADDR11\_MDIO\_CAL\_CS3\_GPIO73 are the calibration and FEC management data in/out signals. Note that BG is not implemented on the MPC5553.

## 2.3.2.16 External Bus Grant / GPIO (BG\_GPIO73) - MPC5554 Only

BG\_GPIO73 is used by the external bus arbiter to give ownership of the EBI to the requesting master. BG is only functional on the MPC5554.

## 2.3.2.17 External Bus Busy / GPIO (BB\_GPIO74) - MPC5554 Only

BB\_GPIO74 is asserted by the current external bus master during a transfer to indicate that the EBI is busy. BB is only functional on the MPC5554.

## 2.3.3 Nexus

## 2.3.3.1 Nexus Event In (EVTI )

EVTI is an input that is read on the negation of TRST to enable or disable the Nexus debug port. After reset, the EVTI pin is used to initiate program and data trace synchronization messages or generate a breakpoint.

## 2.3.3.2 Nexus Event Out (EVTO )

EVTO is an output that provides timing to a development tool for a single watchpoint or breakpoint occurrence.

1. The BR and BG functionality is not implemented on the MPC5553, it is replaced by calibration functionality. The pin name on the ball map, however, does remain BR and BG.

## 2.3.3.3 Nexus Message Clock Out (MCKO)

MCKO is a free running clock output to the development tools which is used for timing of the MDO and MSEO signals.

## 2.3.3.4 Nexus Message Data Out (MDO[3:0])

MDO[3:0] are the trace message outputs to the development tools.

In addition to being a trace output, MDO[0] indicates the lock status of the system clock following a power-on reset. MDO[0] is driven high following a power-on reset until the system clock achieves lock, at which time it is then negated. There is an internal pull up on MDO[0].

## 2.3.3.5 Nexus Message Data Out / GPIO (MDO[11:4]\_GPIO[82:75])

MDO[11:4]\_GPIO[82:75] are the trace message outputs to the development tools for full port mode. These pins function as GPIO when the Nexus port controller (NPC) operates in reduced port mode.

## 2.3.3.6 Nexus Message Start/End Out (MSEO[1:0])

MSEO[1:0] are outputs that indicate when messages start and end on the MDO pins.

## 2.3.3.7 Nexus Ready Output (RDY )

RDY is an output that indicates to the development tools the data is ready to be read from or written to the Nexus read/write access registers.

## 2.3.4 JTAG

## 2.3.4.1 JTAG Test Clock Input (TCK)

TCK provides the clock input for the on-chip test logic.

## 2.3.4.2 JTAG Test Data Input (TDI)

TDI provides the serial test instruction and data input for the on-chip test logic.

## 2.3.4.3 JTAG Test Data Output (TDO)

TDO provides the serial test data output for the on-chip test logic.

## 2.3.4.4 JTAG Test Mode Select Input (TMS)

TMS controls test mode operations for the on-chip test logic.

## 2.3.4.5 JTAG Compliance Input (JCOMP)

The JCOMP pin is used to enable the JTAG TAP controller.

## 2.3.4.6 Test Mode Enable Input (TEST )

The TEST pin is used to place the chip in test mode. It should be negated for normal operation.

## 2.3.5 FlexCAN

## 2.3.5.1 FlexCAN A Transmit / GPIO (CNTXA\_GPIO83)

CNTXA\_GPIO83 is the transmit pin for the FlexCAN A module.

## 2.3.5.2 FlexCAN A Receive / GPIO (CNRXA\_GPIO84)

CNRXA\_GPIO84 is the receive pin for the FlexCAN A module.

## 2.3.5.3 FlexCAN B Transmit / DSPI C Chip Select / GPIO (CNTXB\_PCSC3\_GPIO85)

CNTXB\_PCSC3\_GPIO85 is the transmit pin for the FlexCAN B module. The alternate function is a peripheral chip select output for the DSPI C module.

## 2.3.5.4 FlexCAN B Receive / DSPI C Chip Select / GPIO (CNRXB\_PCSC4\_GPIO86)

CNRXB\_PCSC4\_GPIO86 is the receive pin for the  FlexCAN B module. The alternate function is a peripheral chip select output for the DSPI C module.

## 2.3.5.5 FlexCAN C Transmit / DSPI D Chip Select / GPIO (CNTXC\_PCSD3\_GPIO87)

CNTXC\_PCSD3\_GPIO87 is the transmit pin for the FlexCAN C module. The alternate function is a peripheral chip select for the DSPI D module.

## 2.3.5.6 FlexCAN C Receive / DSPI D Chip Select / GPIO (CNRXC\_PCSD4\_GPIO88)

CNRXC\_PCSD4\_GPIO88 is the receive pin for the FlexCAN C module. The alternate function is a peripheral chip select for the DSPI D module.

## 2.3.6 eSCI

## 2.3.6.1 eSCI\_A Transmit / GPIO (TXDA\_GPIO89)

TXDA\_GPIO89 is the transmit pin for the eSCI A module.

## 2.3.6.2 eSCI\_A Receive / GPIO (RXDA\_GPIO90)

RXDA\_GPIO90 is the receive pin for the eSCI A module. The pin is an input only for the RXD function and does not have a weak pull device, but as GPIO the pin is input or output based on the SIU PCR configuration.

## 2.3.6.3 eSCI B Transmit / DSPI D Chip Select / GPIO (TXDB\_PCSD1\_GPIO91)

TXDB\_PCSD1\_GPIO91 is the transmit pin for the eSCI B module. The alternate function is a peripheral chip select output for the DSPI D module.

## 2.3.6.4 eSCI B Receive / DSPI D Chip Select / GPIO (RXDB\_PCSD5\_GPIO92)

RXDB\_PCSD5\_GPIO92 is the transmit pin for the eSCI B module. The secondary function is a peripheral chip select for the DSPI D module.

## 2.3.7 DSPI

## 2.3.7.1 DSPI A Clock 1  / PCSC1 / GPIO (SCKA\_PCSC1\_GPIO93)

SCKA\_PCSC1\_GPIO93 is the SPI clock pin for the DSPI A module; PCSC1 is a peripheral chip select output pin for the DSPI C module. SCKA is not implemented on the MPC5553.

## 2.3.7.2 DSPI A Data Input 1  / PCSC2 / GPIO (SINA\_PCSC2\_GPIO94)

SINA\_PCSC2\_GPIO94 is the data input pin for the DSPI A module; PCSC2 is a peripheral chip select output pin for the DSPI C module. SINA is not implemented on the MPC5553.

1. In the MPC5553, the DSPI A module is not implemented. The MPC5554 does implement the DSPI A module, and both the MPC5553 and MPC5554 implement the secondary and tertiary functions of the pin.

## 2.3.7.3 DSPI A Data Output 1  / PCSC5 / GPIO (SOUTA\_PCSC5\_GPIO95)

SOUTA\_PCSC5\_GPIO95 is the data output pin for the DSPI A module; PCSC5 is a peripheral chip select output pin for the DSPI C module. SOUTA is not implemented on the MPC5553.

## 2.3.7.4 DSPI A Chip Selec 1 t / PCSD2 / GPIO (PCSA0\_PCSD2\_GPIO96)

PCSA0\_PCSD2\_GPIO96 are peripheral chip select output pins for the DSPI A module. PCSA0 also serves as the slave select input (SS) of the DSPI A module. PCSD2 is a peripheral chip select output pin for the DSPI D module. PCSA0 is not implemented on the MPC5553.

## 2.3.7.5 DSPI A Chip Select 1  / PCSB2 / GPIO (PCSA1\_PCSB2\_GPIO97)

PCSA1\_PCSB2\_GPIO97 are peripheral chip select  output  pins  for  the  DSPI  A  module.  PCSB2  is  a peripheral chip select output pin for the DSPI B module. PCSA1 is not implemented on the MPC5553.

## 2.3.7.6 DSPI A Chip Select 1  / DSPI D Clock / GPIO (PCSA2\_SCKD\_GPIO98)

PCSA2\_SCKD\_GPIO98 is a peripheral chip select output pin for the DSPI A module. The alternate function is the SPI clock for the DSPI D module. PCSA2 is not implemented on the MPC5553.

## 2.3.7.7 DSPI A Chip Select 1  / DSPI D Data Input / GPIO (PCSA3\_SIND\_GPIO99)

PCSA3\_SIND\_GPIO99 is a peripheral  chip  select  output  pin  for  the  DSPI  A  module.  The  alternate function is the data input for the DSPI D module. PCSA3 is not implemented on the MPC5553.

## 2.3.7.8 DSPI A Chip Select 1  / DSPI D Data Output / GPIO (PCSA4\_SOUTD\_GPIO100)

PCSA4\_SOUTD\_GPIO100 is a peripheral chip select output pin for the DSPI A module. The alternate function is the data output for the DSPI D module. PCSA4 is not implemented on the MPC5553.

## 2.3.7.9 DSPI A Chip Select 1  /PCSB3 / GPIO (PCSA5\_PCSB3\_GPIO101)

PCSA5\_PCSB3\_GPIO101 is a peripheral chip select output pin for the DSPI A module. PCSB3 is a peripheral chip select output pin for the DSPI B module. PCSA 5 is not implemented on the MPC5553.

1. In the MPC5553, the DSPI A module is not implemented. The MPC5554 does implement the DSPI A module, and both the MPC5553 and MPC5554 implement the secondary and tertiary functions of the pin.

## 2.3.7.10 DSPI B Clock / DSPI C Chip Select / GPIO (SCKB\_PCSC1\_GPIO102)

SCKB\_PCSC1\_GPIO102 is the SPI clock pin for the DSPI B module. The alternate function is a chip select output for the DSPI C module.

## 2.3.7.11 DSPI B Data Input / DSPI C Chip Select / GPIO (SINB\_PCSC2\_GPIO103)

SINB\_PCSC2\_GPIO103 is the data input pin for the DSPI B module. The alternate function is a chip select output for the DSPI C module.

## 2.3.7.12 DSPI B Data Output / DSPI C Chip Select / GPIO (SOUTB\_PCSC5\_GPIO104)

SOUTB\_PCSC5\_GPIO104 is the data output pin for the DSPI B module. The alternate function is a chip select output for the DSPI C module.

## 2.3.7.13 DSPI B Chip Select / DSPI D Chip Select / GPIO (PCSB0\_PCSD2\_GPIO105)

PCSB0\_PCSD2\_GPIO105 is a peripheral chip select output pin (slave select input pin for slave operation) for the DSPI B module. The alternate function is a chip select output for the DSPI D module.

## 2.3.7.14 DSPI B Chip Select / DSPI D Chip Select / GPIO (PCSB1\_PCSD0\_GPIO106)

PCSB1\_PCSD0\_GPIO106 is a peripheral chip select output pin for the DSPI B module. The alternate function is a chip select output (slave select input pin for slave operation) for the DSPI D module.

## 2.3.7.15 DSPI B Chip Select / DSPI C Data Output / GPIO (PCSB2\_SOUTC\_GPIO107)

PCSB2\_SOUTC\_GPIO107 is a peripheral chip select output pin for the DSPI B module. The alternate function is the data output for the DSPI C module.

## 2.3.7.16 DSPI B Chip Select / DSPI C Data Input / GPIO (PCSB3\_SINC\_GPIO108)

PCSB3\_SINC\_GPIO108 is a peripheral chip select output pin for the DSPI B module. The alternate function is the data input for the DSPI C module.

## 2.3.7.17 DSPI B Chip Select / DSPI C Clock / GPIO (PCSB4\_SCKC\_GPIO109)

PCSB4\_SCKC\_GPIO109 is a peripheral chip select output pin for the DSPI B module. The alternate function is the SPI clock for the DSPI C module.

## 2.3.7.18 DSPI B Chip Select / DSPI C Chip Select / GPIO (PCSB5\_PCSC0\_GPIO110)

PCSB5\_PCSC0\_GPIO110 is a peripheral chip select output pin for the DSPI B module. The alternate function is a chip select output (slave select input in slave mode) for the DSPI C module.

## 2.3.8 eQADC

## 2.3.8.1 Analog Input / Differential Analog Input (AN0\_DAN0+)

AN0 is a single-ended analog input to the two on-chip ADCs. DAN0+ is the positive terminal of the differential analog input DAN0 (DAN0+ to DAN0-).

## 2.3.8.2 Analog Input / Differential Analog Input (AN1\_DAN0-)

AN1 is a single-ended analog input to the two on-chip ADCs. DAN0- is the negative terminal of the differential analog input DAN0 (DAN0+ to DAN0-).

## 2.3.8.3 Analog Input / Differential Analog Input (AN2\_DAN1+)

AN2 is a single-ended analog input to the two on-chip ADCs. DAN1+ is the positive terminal of the differential analog input DAN1 (DAN1+ to DAN1-).

## 2.3.8.4 Analog Input / Differential Analog Input (AN3\_DAN1-)

AN3 is a single-ended analog input to the two on-chip ADCs. DAN1- is the negative terminal of the differential analog input DAN1 (DAN1+ to DAN1-).

## 2.3.8.5 Analog Input / Differential Analog Input (AN4\_DAN2+)

AN4 is a single-ended analog input to the two on-chip ADCs. DAN2+ is the positive terminal of the differential analog input DAN2 (DAN2+ to DAN2-).

## 2.3.8.6 Analog Input / Differential Analog Input (AN5\_DAN2-)

AN5 is a single-ended analog input to the two on-chip ADCs. DAN2- is the negative terminal of the differential analog input DAN2 (DAN2+ to DAN2-).

## 2.3.8.7 Analog Input / Differential Analog Input (AN6\_DAN3+)

AN6 is a single-ended analog input to the two on-chip ADCs. DAN3+ is the positive terminal of the differential analog input DAN3 (DAN3+ to DAN3-).

## 2.3.8.8 Analog Input / Differential Analog Input (AN7\_DAN3-)

AN7 is a single-ended analog input to the two on-chip ADCs. DAN3- is the negative terminal of the differential analog input DAN3 (DAN3+ to DAN3-).

## 2.3.8.9 Analog Input / Multiplexed Analog Input (AN8\_ANW)

AN8 is an analog input pin. The alternate function, ANW, is an analog input in external multiplexed mode. This pin has reduced analog to digital conversion accuracy as compared to the AN[0:7] and AN[16:39] analog input pins.

## 2.3.8.10 Analog Input / Multiplexed Analog Input / Test BIAS (AN9\_ANX\_BIAS 1 )

AN9 is an analog input pin. The alternate function, ANX, is an analog input in external multiplexed mode. This pin has reduced analog to digital conversion accuracy as compared to the AN[0:7] and AN[16:39] analog input pins. BIAS is only implemented on the MPC5553; AN9 and ANX are implemented on both the MPC5553 and the MPC5554.

## 2.3.8.11 Analog Input / Multiplexed Analog Input (AN10\_ANY)

AN10 is an analog input pin. The alternate function, ANY, is an analog input in external multiplexed mode. This pin has reduced analog to digital conversion accuracy as compared to the AN[0:7] and AN[16:39] analog input pins.

## 2.3.8.12 Analog Input / Multiplexed Analog Input (AN11\_ANZ)

AN11 is an analog input pin. The alternate function, ANZ, is an analog input in external multiplexed mode. This pin has reduced analog to digital conversion accuracy as compared to the AN[0:7] and AN[16:39] analog input pins.

## 2.3.8.13 Analog Input / Mux Address 0 / eQADC Serial Data Strobe (AN12\_MA0\_SDS )

AN12\_MA0\_SDS is an analog input pin. The alternate function, MA0, is a MUX address pin. The second alternate function is the serial data strobe for the eQADC SSI. This pin has reduced analog to digital conversion accuracy as compared to the AN[0:7] and AN[16:39] analog input pins.

## 2.3.8.14 Analog Input / Mux Address 1 / eQADC Serial Data Out (AN13\_MA1\_SDO)

AN13\_MA1\_SDO is an analog input pin. The alternate function, MA1, is a MUX address pin. The second alternate function is the serial data output for the eQADC SSI. This pin has reduced analog to digital conversion accuracy as compared to the AN[0:7] and AN[16:39] analog input pins.

1. BIAS is only implemented on the MPC5553.

## 2.3.8.15 Analog Input / Mux Address 2  / eQADC Serial Data In (AN14\_MA2\_SDI)

AN14\_MA2\_SDI is an analog input pin. The alternate function, MA2, is a MUX address pin. The second alternate  function  is  the  serial  data  input  for  the  eQADC  SSI.  This  pin  has  reduced  analog  to  digital conversion accuracy as compared to the AN[0:7] and AN[16:39] analog input pins.

## 2.3.8.16 Analog Input / eQADC Free Running Clock (AN15\_FCK)

AN15\_FCK is an analog input pin. The alternate function is the free running clock for the eQADC SSI. This pin has reduced analog to digital conversion accuracy as compared to the AN[0:7] and AN[16:39] analog input pins.

## 2.3.8.17 Analog Input (AN[16:39])

AN[16:39] are analog input pins.

## 2.3.8.18 External Trigger / GPIO (ETRIG[0:1]\_GPIO[111:112])

ETRIG[0:1]\_GPIO[111:112] are external trigger input pins for the eQADC.

## 2.3.8.19 Voltage Reference High (VRH)

VRH is the voltage reference high input pin for the eQADC.

## 2.3.8.20 Voltage Reference Low (VRL)

VRL is the voltage reference low input pin for the eQADC.

## 2.3.8.21 Reference Bypass Capacitor (REFBYPC)

REFBYPC is a bypass capacitor input for the eQADC. The REFBYPC pin is used to connect an external bias capacitor between the REFBYPC pin and VRL. The value of this capacitor should be 100nF.

## 2.3.9 eTPU

## 2.3.9.1 eTPU A TCR Clock / External Interrupt Request / GPIO (TCRCLKA\_IRQ7\_GPIO113)

TCRCLKA\_IRQ7\_GPIO113 is the TCR A clock input for the eTPU module. The alternate function is an external interrupt request input for the SIU module.

## 2.3.9.2 eTPU A Channel / eTPU A Channel (Output Only) / GPIO (ETPUA[0:11]\_ETPUA[12:23]\_GPIO[114:125])

ETPUA[0:11]\_ETPUA[12:23]\_GPIO[114:125] are input/output channel pins for the eTPU A module. The  alternate  function  is  for  output  channels  of  the  eTPU  A  module;  that  is,  when  configured  as ETPUA[12:23], the pins function as outputs only.

## 2.3.9.3 eTPU A Channel / DSPI / GPIO (ETPUA[12:19]\_PCS Xn \_GPIO[126:133])

ETPUA[12:19]\_PCS Xn \_GPIO[126:133] are input/output channel pins for the eTPU A module muxed with DSPI B and D pins.

## 2.3.9.4 eTPU A Channel / External Interrupt Request / GPIO (ETPUA[20:27]\_IRQ[8:15]\_GPIO[134:141])

ETPUA[20:27]\_IRQ[8:15]\_GPIO[134:141] are input/output channel pins for the eTPU A module muxed with interrupt request pins.

## 2.3.9.5 eTPU A Channel / DSPI / GPIO (ETPUA[28:31]\_PCSC[1:4]\_GPIO[142:145])

ETPUA[28:31]\_PCSC[1:4]\_GPIO[142:145]  are  input/output  channel  pins  for  the  eTPU  A  module multiplexed with DSPI C pins.

## 2.3.9.6 eTPU B TCR Clock / External Interrupt Request / GPIO (TCRCLKB\_IRQ6\_GPIO146) - MPC5554 Only

TCRCLKB\_IRQ6\_GPIO146 is the TCR B clock input for the eTPU module. The alternate function is an external interrupt request input for the SIU module. This pin functions only on the MPC5554.

## 2.3.9.7 eTPU B Channel / eTPU B Channel (Output Only) / GPIO (ETPUB[0:15]\_ETPUB[16:31]\_GPIO[147:162]) - MPC5554 Only

ETPUB[0:15]\_ETPUB[16:31]\_GPIO[147:162] are 16 input/output channel pins for the eTPU B module. The  alternate  function  is  for  output  channels  for  the  eTPU  B  module;  that  is,  when  configured  as ETPUB[16:31], the pins function as outputs only. This pin functions only on the MPC5554.

## 2.3.9.8 eTPU B Channel / DSPI / GPIO (ETPUB[16:19]\_PCSA[1:4]\_GPIO[163:166]) - MPC5554 Only

ETPUB[16:19]\_PCSA[1:4]\_GPIO[163:166] are input/output channel pins for the eTPU B module and DSPI A functionality is the alternate. This pin functions only on the MPC5554.

## 2.3.9.9 eTPU B Channel / GPIO (ETPUB[20:31]\_GPIO[167:178]) - MPC5554 Only

ETPUB[20:31]\_GPIO[167:178] are input/output channel pins for the eTPU B module. This pin functions only on the MPC5554.

## 2.3.10 eMIOS

## 2.3.10.1 EMIOS Channel / eTPU A Channel (Output Only) / GPIO (EMIOS[0:9]\_ETPUA[0:9]\_GPIO[179:188])

EMIOS[0:9]\_ETPUA[0:9]\_GPIO[179:188] are input/output channel pins for the eMIOS module. The alternate function is output channels for the eTPU A module; that is, when configured as ETPUA[0:9], the pins function as outputs only.

## 2.3.10.2 EMIOS Channel / GPIO (EMIOS[10:11]\_GPIO[189:190])

EMIOS[10:11]\_GPIO[189:190] are input/output channel pins for the eMIOS module.

## 2.3.10.3 eMIOS Channel (Output Only) / DSPI C Data Output / GPIO (EMIOS12\_SOUTC\_GPIO191)

EMIOS12\_SOUTC\_GPIO191 is an output channel pin for the eMIOS module. The alternate function is the data output for the DSPI C module.

## 2.3.10.4 eMIOS Channel (Output Only) / DSPI D Data Output / GPIO (EMIOS13\_SOUTD\_GPIO192)

EMIOS[13]\_SOUTD\_GPIO[192] is an output channel pin for the eMIOS module. The alternate function is the data output for the DSPI D module.

## 2.3.10.5 eMIOS Channel (Output Only) / External Interrupt Request / GPIO (EMIOS[14:15]\_IRQ[0:1]\_GPIO[193:194])

EMIOS[14:15]\_IRQ[0:1]\_GPIO[193:194] are output channel pins for the eMIOS module. The alternate function is for external interrupt request inputs.

## 2.3.10.6 eMIOS Channel / eTPU Channel (Output Only) / GPIO (EMIOS[16:23]\_ETPUB[0:7]\_GPIO[195:202])

EMIOS[16:23]\_ETPUB[0:7]\_GPIO[195:202] are input/output channel pins for the eMIOS module. The alternate function is for output channels for the eTPU B module; that is, when configured as ETPUB[0:7], the pins function as outputs only.

## 2.3.11 GPIO

## 2.3.11.1 GPIO

## (GPIO[203:204]\_EMIOS[14:15])

The  GPIO[203:204]\_EMIOS[14:15]  pins'  primary  function  is  EMIOS[14:15].  When  configured  as EMIOS[14:15], the pins function as output channels for the eMIOS module. Because other balls already are named EMIOS[14:15], the balls for these signals are named GPIO[203:204]. The alternate function for these pins is GPIO.

## 2.3.11.2 GPIO (GPIO[205:207])

The GPIO[205:207] pins only have GPIO functionality. These pins are reserved for double data rate memory interface support. Note that the pad type for GPIO205 is medium driver and CMOS input buffer, 5V capability. The pad type for GPIO[206:207] is fast driver and CMOS input buffer (1.62V-1.98V). The GPIO[206:207]  pins  can  be  selected  as  sources  for  the  ADC  trigger  in  the  SIU\_ETISR.  See Section 6.3.1.12.97, 'Pad Configuration Registers 206 - 207 (SIU\_PCR206 - SIU\_PCR207).'

## 2.3.12 Clock Synthesizer

## 2.3.12.1 Crystal Oscillator Output (XTAL)

XTAL is the output pin for an external crystal oscillator.

## 2.3.12.2 Crystal Oscillator Input / External Clock Input (EXTAL\_EXTCLK)

EXTAL is the input pin for an external crystal oscillator or an external clock source. The alternate function is the external clock input. The function of this pin is determined by the PLLCFG configuration pins.

## 2.3.12.3 System Clock Output (CLKOUT)

CLKOUT is an MPC5553/MPC5554 system clock output.

## 2.3.12.4 Engineering Clock Output (ENGCLK)

ENGCLK is a 50% duty cycle output clock with a maximum frequency of the MPC5553/MPC5554 system clock divided by two. ENGCLK is not synchronous to CLKOUT.

## 2.3.13 Power/Ground

## 2.3.13.1 Voltage Regulator Control Supply Input (V RC33 )

VRC33  is the 3.3V supply input pin for the on-chip 1.5-V regulator control circuit.

## 2.3.13.2 Voltage Regulator Control Ground Input (V RCVSS )

VRCVSS  is the ground reference for the on-chip 1.5-V regulator control circuit.

## 2.3.13.3 Voltage Regulator Control Output (V RCCTL )

VRCCTL  is the output pin for the on-chip 1.5-V regulator control circuit.

## 2.3.13.4 eQADC Analog Supply (V DDA n )

VDDA  is the analog supply input pin for the eQADC. n

## 2.3.13.5 eQADC Analog Ground Reference (V SSA n )

VSSA n is the analog ground reference input pin for the eQADC.

## 2.3.13.6 Clock Synthesizer Power Input (V DDSYN )

VDDSYN  is the power supply input for the FMPLL.

## 2.3.13.7 Clock Synthesizer Ground Input (V SSSYN )

VSSSYN  is the ground reference input for the FMPLL.

## 2.3.13.8 Flash Read Supply Input (V FLASH )

VFLASH  is the on-chip Flash read supply input.

## 2.3.13.9 Flash Program/Erase Supply Input (V PP )

VPP  is the on-chip Flash program/erase supply input.

## 2.3.13.10 SRAM Standby Power Input (V STBY )

VSTBY  is the power supply input that is used to maintain a portion of the contents of internal SRAM during power down. If not used,   V STBY  is tied toV SS .

## 2.3.13.11 Internal Logic Supply Input (V DD )

VDD  is the 1.5V logic supply input.

## 2.3.13.12 External I/O Supply Input (V DDE )

VDDE  is the 1.8V to 3.3V +/- 10% external I/O supply input.

## 2.3.13.13 External I/O Supply Input (V DDEH n )

VDDEH  is the 3.3V to 5.0V -10%/+5% external I/O supply input. n

## 2.3.13.14 Fixed 3.3V Internal Supply Input (V DD33 )

VDD33  is the 3.3V internal supply input.

## 2.3.13.15 Ground (V SS )

VSS  is the ground reference input.

## 2.3.14 I/O Power/Ground Segmentation

Table 2-3 gives the preliminary power/ground segmentation of the MPC5553 MCU and Table 2-4 gives the preliminary power/ground segmentation of the MPC5554 MCU.  Each segment provides the power and ground for the given set of I/O pins. Each segment can be powered by any voltage within the allowed voltage range regardless of the power on the other segments. The power/ground segmentation applies regardless of whether a particular pin is configured for its primary function or GPIO.

Table 2-3. MPC5553 Power/Ground Segmentation 1

| Power Segment (V DDE )   | V DDE Package Ball Numbers                                                                                                   | Voltage Range 2      | I/O Pins Powered by Segment                                                                                                                                                                                                                                                                                 |
|--------------------------|------------------------------------------------------------------------------------------------------------------------------|----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| V DDEH1                  | E3, F4                                                                                                                       | 3.3V - 5.0V          | ETPUA[0:31], TCRCLKA                                                                                                                                                                                                                                                                                        |
| V DDEH4                  | AC20                                                                                                                         | 3.3V - 5.0V          | EMIOS[0:23], CNTXA, CNRXA, CNTXB, CNRXB                                                                                                                                                                                                                                                                     |
| V DDEH6                  | AA23                                                                                                                         | 3.3V - 5.0V          | RESET, RSTOUT, RSTCFG, WKPCFG, BOOTCFG[0:1], PLLCFG[0:1], CNTXC, CNRXC, TXDA, RXDA, TXDB, RXDB, SCKA, SINA, SOUTA, PCSA[0:5], PCSB[3:5], GPIO[203:204]                                                                                                                                                      |
| V DDEH8                  | D22                                                                                                                          | 3.3V - 5.0V          | ETRIG[0:1], GPIO[205]                                                                                                                                                                                                                                                                                       |
| V DDEH9                  | D14                                                                                                                          | 3.3V - 5.0V          | AN12, AN13, AN14, AN15                                                                                                                                                                                                                                                                                      |
| V DDEH10                 | J23                                                                                                                          | 3.3V - 5.0V          | SCKB, PCSB[0:2], SINB, SOUTB                                                                                                                                                                                                                                                                                |
| V DDE2 3                 | T1, T4, Y4, AB1, AF5, AC8,AF11,AC13,M10, N10, P10, R10, T10, M11, N11, P11, R11, U11, T12, U12, T13, U13, T14, U14, T15, U15 | 1.8V - 3.3V          | ADDR[8:31], WE[0:3], CS[0:3], BDIP, RD_WR, TS, TA, TEA, DATA[0:31], OE, BR, BG, GPIO[206:207] Note: V DDE2 and VDDE3 are separate segments in the MPC5553 pad ring. These segments are shorted together in the package substrate. The following pins are part of the VDDE3 segment: DATA[0:31], OE, BR, BG. |
| V DDE5                   | AC21, AD22, AE23, AF24                                                                                                       | 1.8V - 3.3V          | CLKOUT, ENGCLK                                                                                                                                                                                                                                                                                              |
| V DDE7                   | B26, C25, D24, E23, K14, K15, K16, K17, L17, M17, N17                                                                        | 1.8V- 3.3V           | MDO[11:0], EVTI, EVTO, MCKO, RDY, MSEO[1:0], TDO, TDI, TMS, TCK, JCOMP, TEST                                                                                                                                                                                                                                |
| V DDSYN                  | AC26                                                                                                                         | 3.3V                 | XTAL, EXTAL                                                                                                                                                                                                                                                                                                 |
| V RC33                   | AC25                                                                                                                         | 3.3V                 | V RCCTL                                                                                                                                                                                                                                                                                                     |
| V DDA0                   | C14                                                                                                                          | 5.0V                 | AN[22:35], VRH, VRL, REFBYPC                                                                                                                                                                                                                                                                                |
| V DDA1                   | A5                                                                                                                           | 5.0V                 | AN[0:11, 16:21, 36:39]                                                                                                                                                                                                                                                                                      |
| V SSA0                   | A14, B14                                                                                                                     | GND                  | -                                                                                                                                                                                                                                                                                                           |
| V SSA1                   | C6                                                                                                                           | GND                  | -                                                                                                                                                                                                                                                                                                           |
| Other Power Segments     | Other Power Segments                                                                                                         | Other Power Segments | Other Power Segments                                                                                                                                                                                                                                                                                        |
| V PP                     | T26                                                                                                                          | 4.5V-5.25V 4         | -                                                                                                                                                                                                                                                                                                           |
| V FLASH                  | U26                                                                                                                          | 3.0V-3.6V            | -                                                                                                                                                                                                                                                                                                           |
| V DD33                   | C1, U4, AD9, A25, AD26                                                                                                       | 3.0V-3.6V            | -                                                                                                                                                                                                                                                                                                           |
| V STBY                   | A2                                                                                                                           | 0.9V-1.1V            | -                                                                                                                                                                                                                                                                                                           |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

## Signal Description

- 1 This table applies only to the 416 package of the MPC5553.
- 2 These are nominal voltages. All V DDE  and V DDEH  voltages are +/- 10% (V DDE  1.62V to 3.6V, V DDEH  3.0V to 5.5V). V RC33 is +/- 10%. V DDSYN  is +/- 10%. V DDA1  is + 5%, -10%.
- 3 VDDE2  and VDDE3 are separate segments in the MPC5553 pad ring. These segments are shorted together in the package substrate. The following pins are part of the VDDE3 segment: DATA[0:31], OE, BR, BG.
- 4 During read operations, VPP can be as high as 5.3V and as low as 3.0V.

Table 2-4. MPC5554 Power/Ground Segmentation

| Power Segment (V DDE )   | V DDE Package Ball Numbers                                                                                                      | Voltage Range 1      | I/O Pins Powered by Segment                                                                                                                                                                                                                                                                           |
|--------------------------|---------------------------------------------------------------------------------------------------------------------------------|----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| V DDEH1                  | E3, F4                                                                                                                          | 3.3V- 5.0V           | ETPUA[0:31], TCRCLKA                                                                                                                                                                                                                                                                                  |
| V DDEH4                  | AC20                                                                                                                            | 3.3V- 5.0V           | EMIOS[0:23], CNTXA, CNRXA, CNTXB, CNRXB                                                                                                                                                                                                                                                               |
| V DDEH6 2                | AA23, J23                                                                                                                       | 3.3V- 5.0V           | RESET, RSTOUT, RSTCFG, WKPCFG, BOOTCFG[0:1], PLLCFG[0:1], CNTXC, CNRXC, TXDA, RXDA, TXDB, RXDB, SCKA, SINA, SOUTA, PCSA[0:5], SCKB, SINB, SOUTB, PCSB[0:5], GPIO[203:204], ETPUB[0:15], TCRCLKB                                                                                                       |
| V DDEH8                  | D22                                                                                                                             | 3.3V- 5.0V           | ETPUB[16:31], ETRIG[0:1], GPIO205                                                                                                                                                                                                                                                                     |
| V DDEH9                  | D14                                                                                                                             | 3.3V- 5.0V           | AN12, AN13, AN14, AN15                                                                                                                                                                                                                                                                                |
| V DDE2 3                 | T1, T4, Y4, AB1, AF5, AC8, AF11, AC13, M10, N10, P10, R10, T10, M11, N11, P11, R11, U11, T12, U12, T13, U13, T14, U14, T15, U15 | 1.8V- 3.3V           | ADDR[8:31], WE[0:3], CS[0:3], BDIP, RD_WR, TS, TA, TEA, TSIZ[0:1], Note: V DDE2 and VDDE3 are separate segments in the MPC5553 pad ring. These segments are shorted together in the package substrate. The following pins are part of the VDDE3segment:DATA[0:31], GPIO[206:207], and BR, BB, BG, OE. |
| V DDE5                   | AC21, AD22, AE23, AF24                                                                                                          | 1.8V- 3.3V           | CLKOUT, ENGCLK                                                                                                                                                                                                                                                                                        |
| V DDE7                   | B26, C25, D24, E23, K14, K15, K16, K17, L17, M17, N17                                                                           | 1.8V- 3.3V           | MDO[11:0], EVTI, EVTO, MCKO, RDY, MSEO[1:0], TDO, TDI, TMS, TCK, JCOMP, TEST                                                                                                                                                                                                                          |
| V DDA0                   | C14                                                                                                                             | 5.0V                 | AN[22:35], VRH, VRL, REFBYPC                                                                                                                                                                                                                                                                          |
| V DDA1                   | A5                                                                                                                              | 5.0V                 | AN[0:11, 16:21, 36:39]                                                                                                                                                                                                                                                                                |
| V SSA0                   | A14, B14                                                                                                                        | GND                  | -                                                                                                                                                                                                                                                                                                     |
| V SSA1                   | C6                                                                                                                              | GND                  | -                                                                                                                                                                                                                                                                                                     |
| V DDSYN                  | AC26                                                                                                                            | 3.3V                 | XTAL, EXTAL                                                                                                                                                                                                                                                                                           |
| V RC33                   | AC25                                                                                                                            | 3.3V                 | V RCCTL                                                                                                                                                                                                                                                                                               |
| Other Power Segments     | Other Power Segments                                                                                                            | Other Power Segments | Other Power Segments                                                                                                                                                                                                                                                                                  |
| V PP                     | T26                                                                                                                             | 4.5V-5.25V 4         | -                                                                                                                                                                                                                                                                                                     |
| V FLASH                  | U26                                                                                                                             | 3.0V-3.6V            | -                                                                                                                                                                                                                                                                                                     |
| V DD33                   | C1, U4, AD9, A25, AD26                                                                                                          | 3.0V-3.6V            | -                                                                                                                                                                                                                                                                                                     |
| V STBY                   | A2                                                                                                                              | 0.9V-1.1V            | -                                                                                                                                                                                                                                                                                                     |

## MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

- 1 These are nominal voltages. All V DDE  and V DDEH  voltages are +/- 10% (V DDE  1.62V to 3.6V, V DDEH  3.0V to 5.5V). VRC33  is +/- 10%. V DDSYN  is +/- 10%. V DDA1  is + 5%, -10%.
- 2 When the FMPLL is configured for external reference mode, the V DDE5  supply affects the acceptable signal levels for the external reference. See Section 11.1.4.2, 'External Reference Mode.'
- 3 VDDE2  and V DDE3  are separate segments in the MPC5554 pad ring. These segments are shorted together in the package substrate. The following pins are part of the V DDE3  segment: DATA[0:31], GPIO[206:207], BR, BB, BG, and OE.
- 4 During read operations, V PP  can be as high as 5.3V and as low as 3.0V.

## 2.4 eTPU Pin Connections and Serialization

## 2.4.1 ETPUA[0:15]

The ETPUA[0:15] module channels connect to external pins or may be serialized out through the DSPIC module. A diagram for the ETPUA[0:15] / SOUTC connection is given in Figure 2-3. The full list of connections  is given  in Table 2-5. Although  not  shown  in  Figure 2-3,  the  output  channels  of ETPUA[12:15] are connected to the ETPUA[0:3]\_ETPUA[12:15]\_GPIO[114:117] pins.

The eTPU  TCRA clock input is connected to an external pin only.

Figure 2-3. ETPUA[0:15]-DSPI C I/O Connections

<!-- image -->

Table 2-5. ETPUA[0:15]-DSPI C I/O Mapping

|   DSPI C Serialized Input |   eTPU A Channel Output |
|---------------------------|-------------------------|
|                        15 |                      11 |
|                        14 |                      10 |
|                        13 |                       9 |
|                        12 |                       8 |
|                        11 |                       7 |
|                        10 |                       6 |
|                         9 |                       5 |
|                         8 |                       4 |
|                         7 |                       3 |
|                         6 |                       2 |
|                         5 |                       1 |
|                         4 |                       0 |
|                         3 |                      15 |
|                         2 |                      14 |
|                         1 |                      13 |
|                         0 |                      12 |

## 2.4.2 ETPUA[16:31]

ETPUA[16:23,30:31] connect to external pins for both the input and output function. ETPUA[16:21,24:29] are serialized out on the DSPI B and DSPI D modules and ETPUA[22:23,30:31] are not serialized out. ETPUA[24:29] connect to external pins for only the output function. Figure 2-4 shows the  connections  for  ETPUA16  and  applies  to  ETPUA[16:21].  Figure 2-5  shows  the  connections  for ETPUA24 and applies to TPUA[24:29]. The full ETPUA to DSPI B connections are given in Table 2-6, and  ETPU  A  to  DSPI  D  in  Table 2-7.  Although  not  shown  in  Figure 2-4,  the  output  channels  of ETPUA[16:23] are also connected to the ETPUA[4:11]\_ETPUA[16:23]\_GPIO[118:125] pins.

Figure 2-4. ETPUA[16:21]-DSPI B-DSPI D I/O Connections

<!-- image -->

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Figure 2-5. ETPUA[24:29]-DSPI B-DSPI D I/O Connections

<!-- image -->

Table 2-6. ETPUA[16:31]-DSPI B I/O Mapping

|   DSPI B Serialized Inputs / Outputs 1 |   eTPU A Channel Output | eTPU A Channel Input   |
|----------------------------------------|-------------------------|------------------------|
|                                     13 |                      24 | 24                     |
|                                     12 |                      25 | 25                     |
|                                     11 |                      26 | 26                     |
|                                     10 |                      27 | 27                     |
|                                      9 |                      28 | 28                     |
|                                      8 |                      29 | 29                     |
|                                      7 |                      16 | -                      |
|                                      6 |                      17 | -                      |
|                                      5 |                      18 | -                      |
|                                      4 |                      19 | -                      |
|                                      3 |                      20 | -                      |
|                                      2 |                      21 | -                      |

- 1 DSPI B serialized input channels 0, 1, 14, and 15 are connected to EMIOS channels. DSPI B serialized output channels 14, 15 are connected to EMIOS channels. DSPI  B serialized output channels 0-7 are not connected.

Table 2-7. ETPUA[16:31]-DSPI D I/O Mapping

|   DSPI D Serialized Inputs 1 |   eTPU A Channel Output |
|------------------------------|-------------------------|
|                           15 |                      24 |
|                           14 |                      25 |
|                           13 |                      26 |
|                           12 |                      27 |
|                           11 |                      28 |
|                           10 |                      29 |
|                            5 |                      16 |

MPC5553/MPC5554 Microcontroller Reference Manual, Rev. 3.1

Table 2-7. ETPUA[16:31]-DSPI D I/O Mapping

|   DSPI D Serialized Inputs 1 |   eTPU A Channel Output |
|------------------------------|-------------------------|
|                            4 |                      17 |
|                            3 |                      18 |
|                            2 |                      19 |
|                            1 |                      20 |
|                            0 |                      21 |

- 1 DSPI D serialized input channels 6-9 are connected to EMIOS channels.

## 2.4.3 ETPUB[0:31] - MPC5554 Only

The I/O connections for ETPUB[0:31] channels are given in Figure 2-6. The outputs of ETPUB[16:31] are connected to two pins. This allows the input and output of those channels to be connected to different pins.  The  outputs  of  ETPUB[16:31]  are  multiplexed  on  the  ETPUB[0:15]  pins.  The  outputs  of ETPUB[0:7] are multiplexed on the EMIOS[16:23] pins so that the output channels of ETPUB[0:7] can be used when the normal pins for these channels are used by ETPUB[16:23] channels. The output channels of ETPUB[0:15] are serialized on DSPI A. The full ETPUB to DSPI A connections are given in Table 2-8.

Figure 2-6. ETPUB[31:0]-DSPI A I/O Connections

<!-- image -->

Table 2-8. ETPUB[0:15]-DSPI A I/O Mapping

|   DSPI A Serialized Inputs |   eTPU B Channel Output |
|----------------------------|-------------------------|
|                         15 |                       0 |
|                         14 |                       1 |
|                         13 |                       2 |
|                         12 |                       3 |
|                         11 |                       4 |
|                         10 |                       5 |

Table 2-8. ETPUB[0:15]-DSPI A I/O Mapping

|   DSPI A Serialized Inputs |   eTPU B Channel Output |
|----------------------------|-------------------------|
|                          9 |                       6 |
|                          8 |                       7 |
|                          7 |                       8 |
|                          6 |                       9 |
|                          5 |                      10 |
|                          4 |                      11 |
|                          3 |                      12 |
|                          2 |                      13 |
|                          1 |                      14 |
|                          0 |                      15 |

## 2.5 eMIOS Pin Connections and Serialization

The eMIOS channels connect to external pins or may be serialized in and out of the MPC5553/MPC5554. The  input  and  output  channels  of  EMIOS[0:11,  16:23]  connect  to  pins.  Only  the  output  channels  of EMIOS[12:15] connect to pins. The output channels of EMIOS[10:13] may be serialized out, and the inputs of EMIOS[12:15] may be serialized in. The DSPI connections for EMIOS[10:11] are given in Figure 2-7, Figure 2-8 for EMIOS[12:13], and Figure 2-9 for EMIOS[14:15].

Figure 2-7. EMIOS[10:11]-DSPI B-DSPI D I/O Connections

<!-- image -->

Figure 2-8. EMIOS[12:13]-DSPI B-DSPI D I/O Connections

<!-- image -->

Figure 2-9. EMIOS[14:15]-DSPI D I/O Connections

<!-- image -->

## 2.6 Revision History

## Substantive Changes since Rev 3.0

Table 2-2, Changed ADDR[12:31] to ADDR[8:31], changed GPIO[8:27] to GPIO[4:27]; Left pin listing as is - it correctly shows 24 pins.

Replaced existing Note on status after reset of MCKO in Table 2-1 and Table 2-2 with this note: 'MCKO is only enabled if debug mode is enabled. Debug mode can be enabled before or after exiting System Reset (RSTOUT negated).'

Fixed typo (6 occurences of V ddeh1 0 changed to V ddeh10 .

Updated Section 2.3.13.12, 'External I/O Supply Input (VDDE)' and Section 2.3.13.13, 'External I/O Supply Input (VDDEHn) with: VDDE +/- 10% of 1.8 to 3.3 nominal and VDDEH -10%/+5% of the nominal 3.3 to 5.0 volts.

The ethernet signal TX\_ER was changed from an input to an output.

Table 2-2 changed REFBYPC to say 'Reference Bypass Capacitor Input' instead of 'Reference Bypass Resistor Input'

Fixed voltage signal name subscripts. Removed V SUP  from MPC5553 signals diagram

Moved GPIO85\_PCSC3\_CNTXB and GPIO86\_PCSC4\_CNRXB from the FlexCAN group of signals to the DSPI group of signals in MPC5553 signals diagram (Figure 2-1) and in Table 2-1.

Updated GPIO[206:207] in table and in description to reflect a change in SIU PCR section (added Note to Section 6.3.1.12.97, 'Pad Configuration Registers 206 - 207 (SIU\_PCR206 - SIU\_PCR207)' describing ETRIG functionality. NOTE: The GPIO[206:7] pins have the capability to trigger the ADCs. For the ETRIG functionality, these GPIO pins need to be set as GPIO and then select the GPIO ADC trigger in the eQADC Trigger Input Select Register (SIU\_ETISR).')

In Section 2.3.6.2, 'eSCI\_A Receive / GPIO (RXDA\_GPIO90),' changed an ambiguous input-only sentence to read 'The pin is an input only for the RXD function and does not have a weak pull device, but as GPIO the pin is input or output based on the SIU PCR configuration.'

## Signal Description
