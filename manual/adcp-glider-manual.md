# Quick Start Guide Seaglider AD2CP

Last updated October 2020. For the most recent version, telemetry scripts, and links to supporting software and documentation visit:

https://github.com/callumrollo/adcp-glider-guide

This informal guide was compiled using information from the Nortek Signature manuals, in particular the Integrator's Guide, correspondence with Nortek and Seaglider (now Hydroid, previously Kongsberg) support teams, published data from previous integrations on the Seaglider and Spray platforms, and personal experience working with the system 2018-2020. This guide comes with no warranty, guarantees of competence, or support. In following this guide you may irreparably damage your glider, sensor, computer, lab, person etc. The author assumes no responsibility. See licence file for full details. Please don't sue me, I'm poor.

For qualified and competent tech support contact:

support@nortekgroup.com

seaglidersupport@hydroid.com

## To the bench

To connect to the AD2CP for bench testing you will require:

- **AD2CP  Signature Deployment and MIDAS software** 

https://www.nortekgroup.com/software (software is Windows only as of October 2020)

- **A Windows computer with an ethernet port**

- **AD2CP manuals "Signature Operations" and "AD2CP Integrator's Guide"**

  https://www.nortekgroup.com/manuals-quick-guides

- **Powered ethernet to standard subsea 8 pin cable** 
this is included in the glider case

The Nortek website is the authoritative source for all information regarding the AD2CP and should be checked for the latest software and manuals.

### Connect to the AD2CP

1. Ensure that both glider and AD2CP ethernet cable are powered **off**. It is not necessary to disconnect the AD2CP to glider serial cable at the port marked "R"
2. Remove the dummy plug and connect the 8 pin subsea connector to the starboard port of the AD2CP, the port is marked "E" for ethernet. **Note** the serial and ethernet ports on the glider AD2CP are the opposite way round to that shown in the Signature 1000 guide.
3. Connect the ethernet cable to your windows computer.
4. Connect the power supply and power the cable. The ethernet port on your computer should light up. The blue light between the transducers on the AD2CP should turn on.
5. Open the Signature Deployment software and wait 1-2 minutes for the AD2CP to assign an IP address.
6. In Signature Deployment select menu option "Discover," you should see a line of data appear with the sensor highlighted in red. Right click this and select "view in browser" to see instrument information and download data files. Select "open in command mode" to control the instrument and conduct bench tests.

The Signature Deployment software expects sensors from the Nortek Signature range but has the capability to interact with the glider mounted AD2CP. Using this software it is possible to communicate with the AD2CP via a terminal emulator, download files from the AD2CP and start recording data. Data visualization/interpretation is not supported as of September 2020.

### Bench test the AD2CP

For ease of reading I have printed all commands in **BOLD UPPERCASE** the AD2CP itself is not case sensitive.

1. Open the command window as detailed above and send the following commands:
2. **INQ** to check the glider is in state 002 ready to receive commands. Otherwise see instrument states below.
3. **LISTFILES** to see what's already on the memory card.
4. **SETDEFAULT,ALL** a good place to start. This sets all AD2CP recording settings to their default values. No AD2CP data files will be affected.
5. **SETPLAN,FN="sensible_filename.ad2cp"** so you don't overwrite pre-existing files. The previous command sets default filename Data.ad2cp. You must specify the .ad2cp file extension.
6. Change other variables as you see fit, there are some suggestions later in this guide.
7. **SAVE,ALL** to test if your configuration is possible with the instrument. If this returns **OK** you can deploy, otherwise **GETERROR** will tell you which settings are incompatible. It's a good idea to **SAVE,ALL** after each variable you change to ensure you entered a compatible value.
8. **START** this will put the instrument in record mode. Leave it to collect data.
9. To finish recording, use the GUI buttons "send break" and "switch to command mode" or send keyboard commands **CTRL-C**  then **MC** 

### Instrument modes

![AD2CP_modes](images/AD2CP_modes.png)

A schematic of the core states of the instrument and the commands to switch between them. Adapted from the Nortek AD2CP Integrator's Guide.

|Mode number  | Instrument Mode|
| :------------- | :---------- | 
|0000|  Bootloader/firmware upgrade|
|0001|  Measurement|
|0002|  Command|
|0004|  Data retrieval|
|0005|  Confirmation|
|0006|  FTP-mode|

Numerical codes for the AD2CP states. This is the number returned after sending the **INQ** command. Adapted from the Nortek AD2CP Integrator's Guide 

### A sample plan for a glider deployment, as used in tank testing


**SETDEFAULT,ALL **

**SETPLAN,FN="todays_date_and_start_time_TANKTEST.AD2CP"** 

**SETPLAN,MIAVG=30** 

**SETAVG,AI=2**

**SETAVG,NC=15**

**SETAVG,CS=2.0**

**SETAVG,NPING=8**

**START**

This will record a profile every 30 s. Each profile will average 8 pings over a two second period. The ADCP will record 15 cells of 2 m size.

## More detail on the AD2CP

### Handy commands 

Commands for parameters typically have three key options **GET** for the present setting **GETLIM** for the acceptable range of values and **SET** to assign a new value to a parameter. To confuse things, parameters are grouped into a number of categories which must be stated when interrogating that parameter. e.g. to interrogate the cell size **CS** parameter for the average profile use: **GETAVG,CS** to find its present value, **GETAVGLIM,CS** to find the accepted range of cell size values, and **SETAVG,CS=x** to set a new cell size of x meters. Values such as file name are controlled through the group **PLAN** rather than"**AVG**

General commands:

- **BBPWAKEUP** when connected to instrument so it will receive commands.
- **INQ** get glider state. Glider must be in mode 002 to receive other commands.
- **GETSTATE** for more detailed info than **INQ** regarding deployment time etc.
- **GETPLAN** for details on the deployment plan, including the filename for data.
- **GETPLAN1** for the alternate plan parameters (these parameters set to 0 by default).
- **GETALL** and **GETALLLIM** for most parameters and their ranges of accepted values.
- **GETPRECISION**/**GETPRECISION1** for precision in burst and avg mode (cm/s) for plan 0/plan 1.
- **RECSTAT** for recorder (memory card) information, free blocks etc.
- **LISTFILES** list all files on the memory card.
- **GETCLOCKSTR** to get the clock. This syncs from the glider clock on each dive.
- **SETTMAVG** for averaging of profiles. used for returning snippet files.
- **ERASE,9999** Wipe the recorder before deployment. This will also reset any plans loaded. Make sure you copied all the data you need before using this.

n.b. **GETALL** will return some errors as the custom glider AD2CP lacks some of the functionality of the Signature 1000 such as a vertical beam. Don't panic, your sensor is fine. 

### On data limit formats (values returned by GETLIM commands)

The limits for the various arguments are returned as a list of valid values, and/or ranges, enclosed in parenthesis (). An empty list, (), is used for arguments that are unused/not yet implemented. Square brackets [] signify a range of valid values that includes the listed values. String arguments are encapsulated with “”, like for normal parameter handling. A semicolon ; is used as separator between limits and values. The argument format can also be inferred from the limits, integer values are shown without a decimal point, floating point values are shown with a decimal point and strings are either shown with the string specifier, “”, or as a range of characters using ‘’ for specifying a character.

Examples:
-  [1;128] – Integer value, valid from 1 to 128.
- ([1300.00;1700.00];0.0) – Floating point value, valid values are 0.0 and the range from 1300.00 to 1700.00.
- (['0';'9'];['a';'z'];['A';'Z'];'.') – String argument with valid characters being . and the character ranges a-z, A-Z, 0-9.
- ("BEAM") – String argument with BEAM being the only valid string.
- (0;1) – Integer value with two valid values, 0 and 1.

### Potentially confusing terms

- **SETPLAN,MIAVG** is the time period between successive average measurements. **SETAVG,AI** is the time interval over which the measurements are averaged. So setting **SETPLAN,MIAVG=20** and **SETAVG,AI=5** will instruct the sensor to take measurements every 20 seconds. The recorded data will be an over a 5 second measurement interval.
- The .ad2cp files store all the variables that the AD2CP was set to during recording, so there is no need to record what commands you sent to the instrument.
- The AD2CP will only use 3 beams at once, you must set the vertical direction to avoid disappointment! The glider will do this automatically when performing dives (including sim dives), but for bench tests you must change it manually with **SETPLAN,VD**
- If a co-ordinate system other than **BEAM** is set (e.g. **XYZ**), the AD2CP will convert to this system at time of recording. This conversion is difficult to reverse later and an error in the compass/tilt sensor could really mess with your data. Nortek recommend recording in BEAM mode and carrying out any coordinate transformations in post processing.
- The AD2CP can run two average and burst plans concurrently so many parameters have four settings, **SETBURST** for burst mode in plan 0, **SETAVG** for average mode in plan 0 and **SETBURST1**, **SETAVG1** for the same parameters in plan 1. See the Integrator's Guide for more detail.

### What to do if the AD2CP demands a password

The AD2CP occasionally requires a login, usually after being left powered on with no input. The details should be

Signature Username: nortek
Password:
(blank) 
or 
Signature Username: nortek
Password: nortek

If neither of these work, temporarily interrupting the power supply and restarting Signature Deployment will get you back in. This does stop the AD2CP from recording data. The password can be reset when connected via ethernet.

### Miscellaneous handy information

When connected to power, a steady blue light on the AD2CP indicates that it is drawing power and not actively recording.  When deployed, the light blinks when it sends out an acoustic ping, there is a quiet but audible click.

Tests shows the clock drifts at approx 1 sec/week. However the AD2CP clock syncs with the Seaglider clock at the start of every profile, so this should not be an issue.

The AD2CP has a 16GB memory card

The AD2CP does not have:

- a vertical beam
- bottom tracking
- pulse coherence
- onboard power
- active beam remapping

The ethernet comm port connetcs to a dedicated Linux processor. This can handle connections over telnet, raw connection and FTP. It should be possible to connect to the instrument this way, without using Nortek's dedicated software if needed.

Using **SETEALTERNATE** you can run two completely independent AD2CP setups in tandem. The primary configuration runs for **PLAN** seconds, the unit then powers down for **IDLE** seconds. The secondary configuration runs for **PLAN1** seconds followed by an idle period of **IDLE1** seconds. The process the repeats. All data are recorded to the same file to the filename **FN** in **SETPLAN** and **SETPLAN1** must be the same The valid range for the various arguments should be verified using the GETALTERNATELIM command. **SETALTERNATE** is potentially useful but quite confusing. One can run two completely different recording plans in alternating time segments. Caution is recommended if using this functionality, consult the Integrator's Guide for more detail.

## Controlling the AD2CP through the Seaglider

This requires three things:

1. Seaglider must be using a main.run variant that works with the Nortek AD2CP. I recommend EAGLCP, this is a version of firmware 66.12 Eagleray. This firmware version solves some timing issues that Clownfish has with the AD2CP as well as an issue in Dorado where the AD2CP was turning the wrong beams on and off during ascent and descent. For further details contact Hydroid support.
2. The file ncp.cnf must be loaded to the glider memory card and stripped. This contains low level commands for the glider-AD2CP interface
3. The file NCP_GO must be present on the basestation and the settings stipulated in it must be valid for the AD2CP, i.e. the AD2CP does not return an error when you try to do a bench test with these settings. This file can be updated during a deployment to change the AD2CP settings.

Note: the NCP_GO file supplied by Elizabeth Creed in September 2018 is rejected by the glider with settmavg,cy="ENU". The coordinates must be set to "BEAM". This only affects the coordinate system of velocity data in the telemetry snippet files.

To toggle the return of snippet files (approx 8Kb  per dive), use the command $CP\_XMITPROFILE in the cmdfile on the glider base staion. $CP\_XMITPROFILE,1 to turn on snippet files or $CP\_XMITPROFILE,0 to turn off.

### Telemetry/snippet files

If telemetry is enabled, the glider will send back snippet files over Iridium. Once all the parts are uploaded to the basestation, two files will be generated for each dive cpNNNNau.r for the dive and cpNNNNbu.r for the climb, where NNNN is the four digit dive number. These data are then combined in pcp637NNNNa.dat

The telemetry files are made up of repeating blocks of National Marine Electronics Association (NMEA) 0183 messages. The first row of each block specifies the instrument type (4=Signature), instrument serial number, number of beams in use, number of cells, blanking distance, cell size and coordinate system of snippet file data.

`$PNORI1,4,100476,3,15,0.30,2.00,ENU*0F`

These NMEA strings consist of three parts:
1.  `$PNORI1` is the "talker". In this case `P` identifies a proprietary system `NOR` is the identifier for Nortek and `I1` is the Nortek code for this message string. 
2.  `4,100476,3,15,0.30,2.00,ENU` The comma separated values are the values of parameters specified by the manufacturer for this message type, identified by their position. Where data are not available, an empty space is left e.g.`4,100476,,,0.30,,ENU` such that position is not lost. In this case the values are number of transducers on instrument, instrument serial number, number of beams recording, number of cells, blanking distance (m), cell size (m) and coordinate reference frame.
3. `*0F`is an optional checksum in hexadecimal, calculated by bitwise exclusive OR of the ASCII characters between the `$` and `*`

For more information on NMEA, see the pdf guide from the pynmea2 library https://github.com/Knio/pynmea2/blob/master/NMEA0183.pdf this package performs a number of useful functions, including checksum calculation and NMEA string parsing.

The second row:

`$PNORS1,112318,113108,0,2A4C0002,13.8,1497.3,0.00,226.4,18.0,0.00,-1.5,0.00,63.305,0.00,11.83*7F`

Specifies more constants: date (mmddyy), time (hhmmss), error code, status code, battery voltage (V), sound speed (m/s), heading standard deviation (deg) heading (deg), pitch (deg), pitch standard deviation (deg), roll (deg), roll standard deviation (deg), pressure (dBar), pressure standard deviation (dBar), temperature (C).

After this there are multiple rows beginning $PNORC1, one for each sample taken.

`$PNORC1,112318,113108,1,2.3,0.083,0.113,-0.039,64.0,63.3,63.4,86,82,75*5D`

The columns of this data following the talker string are as follows: date (mmddyy), time (hhmmss), cell number, cell distance from transducer, velocity head 1, velocity head 2, velocity head 3, return amp head 1, return amp head 2, return amp head 3, correlation head 1, correlation head 2, correlation head 3. Distance in m, velocity in m/s, amplitude in dB, correlation in %.
 
The python script `tele_checker.py` reads these text files and plots the beam amplitude and correlation for each dive in groups of 10 ensembles. Each plot typically covers 40 - 60 minutes of data. These plots are saved as in png format with file names `tele_amp_NNNN_X.png` and `tele_cor_NNNN_X.png` where NNNN is the dive number and X the chunk number. Plots below show examples from a deployment in oligotrophic waters with good quality data.

![adcp_snippet_correlation](images/tele_cor_0004_1.png)

**Snippet files correlations**: Good correlations are in blue, we expect good correlation out to 10 m at least. Range may be less in low scattering however. The first cell often has a lower correlation, possibly due to ringing.

![adcp_snippet_return_amp](images/tele_amp_0004_1.png)

**Snippet files amplitudes**: Amplitude drops off rapidly with distance, this is raw return amp not gain adjusted so this is expected. Check to make sure all three heads report similar return amps. Return amp is dependant on amount of suitable size scatterers in the water column. As a result, it will decrease in clear oligotrophic water. 

The script also produces average plots using all the snippet file data in the folder.

Call `tele_checker.py` from the terminal using **python telechecker.py -p 'path-to-your-adcp-snippet-files'**. Make sure that the Python libraries required by the script are in your shell path. Snippet files can be processed automatically by adding this command to a glider's `.logout` file. The script checks for existing figures, so only new snippet files and average data are processed. If you wish to force reprocessing, remove the figures from the directory before calling the script.


### Further snippet files details

The settings for snippet files can be changed in NCP_GO with **SETTMAVG**. The following arguments can be specified:

- **EN** Enable Averaging Mode Telemetry 1 to enable, 0 to disable
- **CD** Cells Divisor
- **PD** Packets Divisor
- **AVG** Average Telemetry Data
- **TV** Store Velocity
- **TA** Store Amplitude
- **TC** Store Correlation
- **CY** Coordinate System
- **FO** Enable File Output
- **SO** Enable Serial Output
- **DF** Data format **Do not change!**


----------------------

## Recommendations for operators


### Deployment guidance

Average mode is best for shear velocity information. Low power consumption and good data quality can be achieved by averaging every 15 or 30 seconds using 4 or 8 ensembles. Burst mode is geared toward measurements of turbulence. This is more power hungry and will fill up the memory card faster. Burst mode allows more pings per second. 

During deployment, the glider should be kept within an attitude envelope that orients the three operating transducers at similar angles from the vertical. If the glider pitches or rolls outside of the envelope, the beams will sample water parcels at different depths. The AD2CP does not actively resample by changing time gating of data recording as some other ADCPs do.

This vertical beam miss can be calculated using functions in the adcp-glider repo. Here is an example of the attitude effects on vertical beam miss at 15 m from the glider, assuming 2 m bin size.

![beam miss](images/beam_miss.png)


I recommend using a large bin size or 2 m to ensure sufficient scatterers in each bin for reliable measurements. If a smaller bin is used, the glider attitude must be more tightly controlled.

I recommend recording in glider coordinates (BEAM). The conversions to XYZ and ENU rely on the AD2CP's attitude sensors. If there is an error with these, it is difficult to recover the original AD2CP data. Conversely, the conversion from glider coordinates to XYZ or ENU is trivial. Functions in the linked repository perform this conversion.


### Data analysis options

The free Nortek software **SignatureViewer** will display data and show you that the sensor is recording at the intervals you set. However, it does not process the three beams correctly as it expects four beam input. You can use SignatureViewer to export data files as ntk and then view them with another program.

**Nortek MIDAS** will read .adcp files and convert them to netCDF4, matlab or csv format. It will also convert to and replay ntk files.

Nortek's proprietary **OceanContour** apparently can read the AD2CP data, but costs over £1000. The author has not tried it.

### How to convert the .ad2cp files for analysis

1. Open Nortek MIDAS
2. In the Data menu use the option "AD2CP to ntk" to convert your binary ad2cp file to a re-playable ntk.
3. In the same Data menu there are tools for exporting these ntk files to netCDF4, Matlab and ASCII format.
4. The netCDF4 files are open source standards that can be read into a number of programes with the netCDF4 library.

The repository https://github.com/callumrollo/adcp-glider/ contains Python scripts that as input the netcdf files created in step 3 and the output of the UEA Seaglider Toolbox.

### Bench tests before and after all deployments
 
A number of bench tests are recommended before deploying the ADCP glider. Particularly after making any changes to the AD2CP or glider firmware. The process for setting up the glider for bench tests is described in the first section of this manual. As part of bench testing, sim dives should be performed.

It is recommended to carry out bench tests in a tank prior to deploying the glider. Testing is a tank will test that the four transducers record a similar signal return in water. If the signal return of the transducers differs by more than a few decibels, this could be a sign of a damaged transducer. Due to the amount of acoustic ringing in a tank, the measurements of water velocity reported will not be reliable.

### Physically test transducers

Rationale: At least one Seaglider firmware version (66.12 Dorado) had an error that supplied the opposite orientation parameter to the AD2CP during dive and climb phases. This caused the incorrect beam to be switched off, though the AD2CP sent out pings and recorded data as normal. To test that the AD2CP is behaving as expected, I recommend you physically test the transducers during a sim dive.

This can be accomplished by the simple expedient of a water filled nitrile glove and a timing source. 

![Glove test photo](images/glove_test.jpeg)

Be sure that your timing source matches the AD2CP. The simplest way to achieve this is to conduct a sim dive after the glider has synced its clock to GPS and use a similarly synced source. +/- a second is good enough.

1. Set the AD2CP up to record every 15 seconds (see example in bench test section) using the NCP_GO file on the base station.
1. Start the glider on a sim dive to at lest 30 m, to ensure a long enough time series for recording.
1. Fill a nitrile glove with water and place it over each transducer head in turn, recording the timing of each placement.
1. Once the sim dive is finished, turn off the glider and recover the data.
1. Plot the amplitude return of the transducers and compare to the timing of when each transducer was covered. Covering the transducer with a water filled glove significantly increases the return amplitude of the signal, in comparison to the other transducers that are firing in air. See the example at https://github.com/callumrollo/adcp-glider/blob/master/notebooks/bench_tests.ipynb.
1. One transducer will not fire, check this is the correct one. For ideal data collection, the aft facing transducer should be switched off during the dive, the fore facing transducer should be switched off during the climb.

![Results of transducer tests](images/transducer_tests.png)
Example result of the above procedure when used to test a firmware fix. Under the old Dorado firmware (top row) the fore facing beam was switched off during the dive and the aft facing beam was switched off during ascent, the opposite behaviour to what was desired. The issue was fixed with the Eaglecp firmware (bottom row).

-----------------------------------
This guide is a work in progress. Please direct any questions/recommendations to Callum Rollo

 *firstnameinitial.lastname*@uea.ac.uk 
 
 *firstnameinitial.lastname*@outlook.com 
 
 Or submit an issue/pull request on Github

