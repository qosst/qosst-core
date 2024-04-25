# Configuration

The configuration file and reader is one of the most important of `qosst-core`. In particular it provides the reader of the documentation to create a convenient object that can be used by Alice and Bob.

## A word on TOML

The configuration file is written in [TOML](https://toml.io/en/). The choice of this is mainly motivated from the [PEP 518](https://peps.python.org/pep-0518/#file-formats) file format choice, from which the following table has been extracted:

| Feature                 | TOML | YAML | JSON | CFG/INI |
| ----------------------- | ---- | ---- | ---- | ------- |
| Well-defined            | yes  | yes  | yes  |         |
| Real data types         | yes  | yes  | yes  |         |
| Reliable unicode        | yes  | yes  | yes  |         |
| Reliable comments       | yes  | yes  |      |         |
| Easy for humans to edit | yes  | ??   |      | ??      |
| Easy for tools to edit  | yes  | ??   | yes  | ??      |
| In standard library     |      |      | yes  | yes     |
| Easy for pip to vendor  | yes  |      | n/a  | n/a     |

(also see this [reference](https://gist.github.com/njsmith/78f68204c5d969f8c8bc645ef77d4a8f#summary)).

Although TOML is not in the python standard library for versions ranging from 3.7 to 3.10, it was included in version 3.11 (see [PEP 680](https://peps.python.org/pep-0680/)). The choice is also motivated as it know the language to provide the specifications to build python projects (`pyproject.toml`).

In `qosst` however, since the software officially supports versions 3.7.2 and above, the choice of the [toml](https://pypi.org/project/toml/) package was made.

## Reader

The main class of the reader is {py:class}`qosst_core.configuration.config.Configuration` and can be used in the following way

```{code-block} python

from qosst_core.configuration import Configuration

config = Configuration("config.example.toml")

print(config)

print(config.frame.quantum.modulation)
```

When initialized, this class reads the TOML file, and feed it the `from_dict` method. It will then called subclasses that will also be using the `from_dict` method to load the value on the class. More information can be found [here](../api/configuration.md).

```{note}
For most of the section and subsections, if the section or parameter is not present, default(s) value(s) is (are) used. However, in some cases, the entire section is also left to None (for instance, Alice doesn't need to have the config.bob filled with default values). The table below summarize if the values are auto-filled with the default values if the section is absent from the configuration file:

| Section                                           | Auto filled ? |
| ------------------------------------------------- | ------------- |
| logs                                              | yes           |
| notifications                                     | no            |
| authentication                                    | no            |
| clock                                             | no            |
| channel                                           | no            |
| channel.voa                                       | yes           |
| local_oscillator                                  | no            |
| alice                                             | no            |
| alice.signal_generation                           | yes           |
| alice.network                                     | yes           |
| alice.dac                                         | yes           |
| alice.powermeter                                  | yes           |
| alice.voa                                         | yes           |
| alice.modulator_bias_control                      | yes           |
| alice.laser                                       | yes           |
| alice.polarisation_recovery                       | yes           |
| bob                                               | no            |
| bob.network                                       | yes           |
| bob.adc                                           | yes           |
| bob.switch                                        | yes           |
| bob.laser                                         | yes           |
| bob.polarisation_recovery                         | yes           |
| bob.polarisation_recovery.polarisation_controller | yes           |
| bob.polarisation_recovery.powermeter              | yes           |
| bob.dsp                                           | yes           |
| bob.dsp.equalizer                                 | yes           |
| bob.parameters_estimation                         | yes           |
| bob.electronic_noise                              | yes           |
| bob.electronic_shot_noise                         | yes           |
| frame                                             | no            |
| frame.pilots                                      | yes           |
| frame.quantum                                     | yes           |
| frame.zadoff_chu                                  | yes           |
```

## Parameters in the configuration file

This section will describe each section of the configuration file alongside with the description of every parameter in the file.

```{warning}
This section reflects the purpose of each configuration variable as it was intended in the configuration file. More details can be found in the documentation of `qosst-alice` and `qosst-bob` for the specific implementation.
```

The default value is also given.

```{py:attribute} label
:type: str
:value: '"Example config"'

Name of the configuration. This is useful when several configuration file exists to quickly check which one is used.
```

```{py:attribute} serial_number
:type: str
:value: '""'

Identifier of the hardware.
```

### Logs

This section holds the configuration for file logging.

The configuration for console logging is done when calling the scripts (with the `-v` option).

The configuration for GUI logging is also done when calling them GUI script.

```{py:attribute} logging
:type: bool
:value: "True"

If True, logs will be saved to a file. If False, logs will not be saved to a file. This option does not concern the console or GUI logs.
```

```{py:attribute} path
:type: str
:value: '"qosst.log"'

Path of the file where the logs should be saved.
```

```{py:attribute} level
:type: str
:value: '"info"'

Log level. Possible choices are: debug, info, warning, error and critical. Any log level will save its level and the higher level.
```

### Notifications

This section holds the configuration for the notifications that can be sent to tue user to inform of the progress of the experiment.

```{py:attribute} notify
:type: bool
:value: "False"

If True, notifier will be initialized and used. If False, notifier will not be initialized.
```


```{py:attribute} notifier_class
:type: str
:value: '"qosst_core.notifications.FakeNotifier"'

Import path of the notifier to use. The notifier should be a valid class, inheriting from {py:class}`qosst_core.notifications.QOSSTNotifier`.
```

```{py:attribute} notifier_args
:type: dict
:value: "{}"

Dict of arguments that will be passed as kwargs to the `__init__` method of the notifier. For instance, the dict `{token="abc"}` would be equivalent to the python call `notifier = Notifier(token="abc")`.
```

### Authentication

This section holds the configuration for the authentication, in particular deciding which algorithm will be used to sign the digest and give the parameters to sign the digest and check the digests of the other party.

```{py:attribute} authentication_class
:type: str
:value: '"qosst_core.authentication.NoneAuthenticator"'

Import path of the authentication class to use for the control protocol for the classical channel. The authenticator should be a valid class, inheriting from {py:class}`qosst_core.authentication.base.BaseAuthenticator`.
```

````{py:attribute} authentication_params
:type: dict
:value: "{}"

Dict of arguments that will be passed as kwargs to the `__init__` method of the authenticator. For instance, the dict `{secret_key="abc"}` would be equivalent to the python call `authenticator = Authenticator(secret_key="abc")`.

```{note}
For this particular dict of parameters, the special directive `from_file` can be used. This is done to be able to load a private and public key from a file instead of putting in the configuration file. The syntax is the following: 
`{secret_key = "from_file(my_secret_file)"}`.
```

````

### Clock

This section holds the configuration for clock sharing.

````{py:attribute} sharing
:type: bool
:value: "False"

If True, it will be assumed that the clock is shared between Alice and Bob's DAC and ADC. In particular this can be used to simplify the digital signal processing. In some cases, the hardware will be also configured to actually enable the clock sharing. If False, not clock sharing is assumed and no steps are done to enable clock sharing.

```{warning}
The automatic configuration of the clock sharing should be checked and considered not working.
```
````

```{py:attribute} master
:type: str
:value: '"alice"'

Master of the clock sharing (i.e.) the party that emits the clock reference. Possible choice are "alice" and "bob". This parameter is ignored if the clock sharing is not enable.
```

### Local oscillator

This section holds the configuration for local oscillator sharing.

```{py:attribute} shared
:type: bool
:value: "False"

If True, it will be assumed that the local oscillator is shared between Alice and Bob, *i.e.* that the same laser is used for the signal generation and the local oscillator for Bob. In particular this can be used to simplify the digital signal processing.
```

### Channel

This section holds the configuration for the channel, in particular if a Variable Optical Attenuator (VOA) is used to emulate the channel.

#### VOA

This section holds the configuration of a VOA that is used to emulate the channel.

This particular section can be used when a Variable Optical Attenuator (VOA) is used to emulate the channel.

```{note}
In general, in QOSST, VOA are assumed to be controlled by a voltage, and this is usually what you configure in the configuration file as the VOA value. However, it is possible to code hardware classes taking the attenuation as an input.
```

```{py:attribute} use
:type: bool
:value: "False"

If True, the VOA will be initialized using the VOA device, and the attenuation/voltage will be applied to the VOA. If False, all this section is ignored.
```

```{py:attribute} applier
:type: str
:value: '"alice"'

The party that will apply the value to the VOA. Possible choices are "alice" and "bob". The party that is not the applier will ignore this section. 
```

```{py:attribute} device
:type: str
:value: '"qosst_hal.voa.FakeVOA"'

Import path of the VOA class to use to emulate the channel. The VOA should be a valid class, inheriting from {external:py:class}`qosst_hal.voa.GenericVOA`.
```

```{py:attribute} location
:type: str
:value: '""'

Location of the VOA device. The format depends on the specific VOA class that is used.
```

```{py:attribute} value
:type: float
:value: 0

Value to use for the VOA. Depending on the VOA class that is used, this value can represent an attenuation, a voltage, *etc*...
```

```{py:attribute} extra_args
:type: dict
:value: "{}"

Dict of arguments that will be passed as kwargs to the `__init__` method of the VOA. For instance, the dict `{min_value=0}` would be equivalent to the python call `voa = VOA(min_value=0)`.

```

### Alice

This section holds configuration relative to Alice.

`````{py:attribute} photodiode_to_output_conversion
:type: float
:value: 1

This represent the ratio between the power that is detected by Alice's monitoring photodiode and Alice's output. In practice this value will be used by Alice to compute the average number of photons per symbol at the output of Alice.

````{note}
This is explained in more details in `qosst-alice` documentation but the average number of photons per symbols can be computed as 
```{math}
\langle n \rangle = \frac{P_{out}}{E_{ph}\cdot R_s} 
```

where {math}`P_{out}` is the optical power at Alice's output, {math}`E_{ph} = \frac{hc}{\lambda}` the energy of a photon and {math}`R_s` is the symbol rate.

{math}`P_{out}` is computed as 

```{math}
P_{out} = r_{conv}\cdot P_{monitoring}
```
where {math}`r_{conv}` is th photodiode to output conversion ratio and {math}`P_{monitoring}` is the optical power at the monitoring photodiode, yielding the final formula

```{math}
\langle n \rangle = \frac{r_{conv}\cdot P_{monitoring}}{E_{ph}\cdot R_s} 
```
````
`````

````{py:attribute} artificial_excess_noise
:type: float
:value: 0

This parameter will be used as the variance of a white noise that will be added to the generated quantum symbols that will be applied to the IQ modulator but not saved in the actual symbols of Alice. This is useful to check that we indeed detect the artificial excess noise.

```{warning}
This should also be 0 for real tests.
```
````

```{py:attribute} schema
:type: str
:value: '"qosst_core.schema.emission.SINGLE_POLARISATION"'

Emission schema. The list of possible emission schemas is available [here](../api/schema.md). The schema should be a valid instance of {py:class}`qosst_core.schema.emission.EmissionSchema`.
```

#### Signal generation

This section holds configuration to load and/or save data during the signal generation algorithm.

```{py:attribute} symbols_path
:type: str
:value: '"symbols.npy"'

Path to load the symbols from if `load_symbols` is True. Path to save the symbols if `save_symbols` is True. This parameter is ignored if both parameters are False.
```

```{py:attribute} final_sequence_path
:type: str
:value: '"final_sequence.npy"'

Path to load the final sequence from if `load_final_sequence` is True. Path to save the final sequence if `save_final_sequence` is True. This parameter is ignored if both parameters are False.
```

```{py:attribute} quantum_sequence_path
:type: str
:value: '"quantum_sequence.npy"'

Path to save the symbols if `save_quantum_sequence` is True. This parameter is ignored if `save_quantum_sequence` is False.
```

```{py:attribute} load_symbols
:type: bool
:value: "False"

If True, the symbols are not generated but loaded from a file, using the path provided in `symbols_path`.
```

```{py:attribute} load_final_sequence
:type: bool
:value: "False"

If True, the finale sequence is not generated but loaded from a file, using the path provided in `final_sequence_path`.
```

```{py:attribute} save_symbols
:type: bool
:value: "True"

If True, the symbols are saved using the path provided in `symbols_path`.
```

```{py:attribute} save_final_sequence
:type: bool
:value: "True"

If True, the final sequence is saved using the path provided in `final_sequence_path`.
```

```{py:attribute} save_quantum_sequence
:type: bool
:value: "True"

If True, the quantum sequence are saved using the path provided in `quantum_sequence_path`.
```

```{note}

The symbols represent the actual complex symbols that encode the information. They are then inputted into the digital signal processing of Alice to be processed for emission, yielding the quantum sequence. Finally, the pilots and the Zadoff-Chu sequence (classical signals) are added to form the final sequence. This is explained in more detail in the `qosst-alice` documentation.

```

#### Network

This section holds the network configuration for Alice.

```{py:attribute} bind_address
:type: str
:value: '"127.0.0.1"'

Network address to bind to for the server.
```

```{py:attribute} port
:type: int
:value: 8181

Network port to bind to for the server.
```

#### DAC

This section holds the DAC configuration for Alice.

```{py:attribute} rate
:type: int
:value: '500e6'

Rate of the DAC of Alice in Samples/second. The scientific notation e (500e6 for instance) is available.
```

```{py:attribute} amplitude
:type: float
:value: '0'

Amplitude to use for the DAC. In particular this value will be passed to the DAC class. If this is set to {math}`A` V, it should mean that a +1 in the final sequence will generate a voltage of {math}`+A` V and a -1 will generate {math}`-A` V. It should be set to stay in the limit of the linearity range of the modulator and the specifications of the DAC.
```


```{py:attribute} device
:type: str
:value: '"qosst_hal.dac.FakeDAC"'
:noindex:

Import path of the DAC class to use. The DAC should be a valid class, inheriting from {external:py:class}`qosst_hal.dac.GenericDAC`.
```

```{py:attribute} channels
:type: List[int]
:value: '[0, 1]'

List of channels to use for the DAC.
```

```{py:attribute} extra_args
:type: dict
:value: "{}"
:noindex:

Dict of arguments that will be passed as kwargs to the `__init__` method of the DAC. For instance, the dict `{"erase":true}` would be equivalent to the python call `dac = DAC(erase=True)`.
```

#### Powermeter

This section holds the configuration for the monitoring photodiode for Alice that is used to compute the average num,ber of photons at the output of Alice.

```{py:attribute} device
:type: str
:value: '"qosst_hal.powermeter.FakePowerMeter"'
:noindex:

Import path of the powermeter class for the power monitoring. The powermeter should be a valid class, inheriting from {external:py:class}`qosst_hal.powermeter.GenericPowerMeter`.
```

```{py:attribute} location
:type: str
:value: '""'
:noindex:

Location of the powermeter device. The format depends on the specific powermeter class that is used.
```

```{py:attribute} extra_args
:type: dict
:value: "{}"
:noindex:

Dict of arguments that will be passed as kwargs to the `__init__` method of the powermeter.

```

#### VOA

This section holds the configuration of the VOA of Alice.

```{py:attribute} device
:type: str
:value: '"qosst_hal.voa.FakeVOA"'
:noindex:

Import path of the VOA class to tune Alice's variance. The VOA should be a valid class, inheriting from {external:py:class}`qosst_hal.voa.GenericVOA`.
```

```{py:attribute} location
:type: str
:value: '""'
:noindex:

Location of the VOA device. The format depends on the specific VOA class that is used.
```

```{py:attribute} value
:type: float
:value: 0
:noindex:

Value to use for the VOA. Depending on the VOA class that is used, this value can represent an attenuation, a voltage, *etc*...
```

```{py:attribute} extra_args
:type: dict
:value: "{}"
:noindex:

Dict of arguments that will be passed as kwargs to the `__init__` method of the VOA.
```

#### Modulator bias controller

This section holds the configuration for the modulation bias controller of Alice.

```{py:attribute} device
:type: str
:value: '"qosst_hal.modulator_bias_control.FakeModulatorBiasController"'
:noindex:

Import path of the bias controller class to use to lock the IQ modulator. The bias controller should be a valid class, inheriting from {external:py:class}`qosst_hal.modulator_bias_control.GenericModulatorBiasController`.
```

```{py:attribute} location
:type: str
:value: '""'
:noindex:

Location of the bias controller device. The format depends on the specific VOA class that is used.
```

```{py:attribute} extra_args
:type: dict
:value: "{}"
:noindex:

Dict of arguments that will be passed as kwargs to the `__init__` method of the bias controller.
```

#### Laser

This section holds the configuration for the laser of Alice.

```{py:attribute} device
:type: str
:value: '"qosst_hal.laser.FakeLaser"'
:noindex:

Import path of the laser class of Alice. The laser should be a valid class, inheriting from {external:py:class}`qosst_hal.laser.GenericLaser`.
```

```{py:attribute} location
:type: str
:value: '""'
:noindex:

Location of the laser device. The format depends on the specific laser class that is used.
```

```{py:attribute} parameters
:type: dict
:value: "{}"
:noindex:

Dict of arguments that will be passed to the `set_parameters` method of the laser. This could be the power, the frequency, *etc*... This depends on the specific laser class that is used.
```

#### Polarisation recovery

The polarisation recovery is done by Alice sending a strong classical signal for Bob to optimize the polarisation recovery. This section holds the parameters for the generation of this classical signal.

```{py:attribute} signal_frequency
:type: float
:value: 20e6

Frequency of the tone, in Hz, to send as the classical recovery signal.
```

```{py:attribute} signal_amplitude
:type: float
:value: 1

Amplitude of the tone to send (this will then be multiplied by the amplitude of the DAC to get the physical amplitude).
```

### Bob

This section holds the configuration relative to Bob.

```{py:attribute} export_directory
:type: str
:value: '"export"'

Path of the directory for the auto-export features of Bob.
```

```{py:attribute} eta
:type: float
:value: 0.8

Value of the receiver's globale efficiency (on the signal path). This will be used to compute the excess noise at Alice's side, the transmittance and the secret key rate.
```

````{py:attribute} automatic_shot_noise_calibration
:type: bool
:value: '"False"'

If True, an automatic shot noise calibration, Bob will automatically perform a shot noise calibration before the start of each Quantum Information Exchange (QIE). If False, the shot noise calibration should either done once prior to exchanges or using the automatic calibration with the switch (see later).

```{warning}
It is highly recommended to use one of the two automatic calibration method for the shot noise.
```
````

```{py:attribute} schema
:type: str
:value: '"qosst_core.schema.detection.SINGLE_POLARISATION_RF_HETERODYNE"'
:noindex:

Detection schema. The list of possible detection schemas is available [here](../api/schema.md). The schema should be a valid instance of {py:class}`qosst_core.schema.detection.DetectionSchema`.
```


#### Network

This section holds the network configuration of Bob.

```{py:attribute} server_address
:type: str
:value: '"127.0.0.1"'

Network address to connect to.
```

```{py:attribute} server_port
:type: int
:value: 8181

Network port to connect to.
```


#### ADC

This section holds the ADC configuration of Bob.

```{py:attribute} rate
:type: int
:value: '2500e6'
:noindex:

Rate of the ADC of Bob in Samples/second. The scientific notation e (2500e6 for instance) is available.
```

```{py:attribute} device
:type: str
:value: '"qosst_hal.dac.FakeADC"'
:noindex:

Import path of the DAC class to use. The DAC should be a valid class, inheriting from {external:py:class}`qosst_hal.dac.GenericDAC`.
```

```{py:attribute} channels
:type: List[int]
:value: '[0]'
:noindex:

List of channels to use for the ADC.
```

```{py:attribute} location
:type: Any
:value: '""'
:noindex:

Location of the ADC device.
```

````{py:attribute} acquisition_time
:type: float
:value: 0

Duration of the acquisition, in seconds. If 0 is given, the acquisition time will be computed as 

```{math}
t = \frac{N_{sym}}{R_s} + t_{overhead}
```

where {math}`N_{sym}` is the number of symbols, {math}`R_s` the rate of symbols and `t_{overhead}` the overhead time define as the next parameter.
````

````{py:attribute} overhead_time
:type: float
:value: 0

Overhead time, in seconds, that will be added to the symbols emission time. If the `acquisition_time` parameter is 0, this parameter is ignored.

If the `acquisition_time` parameter is 0, he acquisition time will be computed as

```{math}
t = \frac{N_{sym}}{R_s} + t_{overhead}
```

where {math}`N_{sym}` is the number of symbols, {math}`R_s` the rate of symbols and `t_{overhead}` the overhead time define as the next parameter.

```{warning}
For an experimental system, it's always better to use the `acquisition_time` parameter to have a better control on what is done.
```
````


```{py:attribute} extra_args
:type: dict
:value: "{}"
:noindex:

Dict of arguments that will be passed as kwargs to the `__init__` method of the ADC. For instance, the dict `{"erase":true}` would be equivalent to the python call `adc = ADC(erase=True)`.
```


```{py:attribute} extra_acquisition_parameters
:type: dict
:value: "{}"
:noindex:

Dict of arguments that will be passed as kwargs to the `set_acquisition_parameters` method of the ADC. For instance, the dict `{"paths":"test.npy"}` would be equivalent to the python call `adc.set_acquisition_parameters(..., paths="test.npy")`.
```

#### Switch

This section holds the configuration for the switch of Bob, that is used to "cut" the signal input for calibration.

```{py:attribute} device
:type: str
:value: '"qosst_hal.switch.FakeSwitch"'
:noindex:

Import path of the switch class to use. The switch should be a valid class, inheriting from {external:py:class}`qosst_hal.switch.GenericSwitch`.
```

```{py:attribute} location
:type: Any
:value: '""'
:noindex:

Location of the switch device.
```

```{py:attribute} timeout
:type: int
:value: 100

Timeout for communication with the switch, in seconds.
```

```{py:attribute} signal_state
:type: int
:value: 100

State that will be used for the signal (*i.e.* the switch is ON).
```

```{py:attribute} calibration_state
:type: int
:value: 100

State that will be used for the calibration (*i.e.* the switch is OFF).
```

```{py:attribute} switching_time
:type: int
:value: 0

Time to wait before switching back to the signal state and send the trigger to Alice.

If this value is not 0, the first part of the acquired signal will be used to calibrate the shot noise (the part that is ensured to be before the switch).

If 0 the calibration should be done manually (the switch won't automatically switch in the calibration state before).
```

#### Laser

This section holds the configuration for the laser of Bob.

```{py:attribute} device
:type: str
:value: '"qosst_hal.laser.FakeLaser"'
:noindex:

Import path of the laser class to use. The laser should be a valid class, inheriting from {external:py:class}`qosst_hal.laser.GenericLaser`.
```

```{py:attribute} location
:type: str
:value: '""'
:noindex:

Location of the laser device.
```

```{py:attribute} parameters
:type: dict
:value: "{}"
:noindex:

Dict of arguments that will be passed to the `set_parameters` method of the laser. This could be the power, the frequency, *etc*... This depends on the specific laser class that is used.
```

#### Polarisation recovery

The polarisation recovery is done by Alice sending a strong classical signal and Bob searching for the optimal position using a motorised polarisation controller, a polarisation beam splitter and a powermeter.

```{py:attribute} use
:type: bool
:value: false
:noindex:

Whether or not to use the polarisation recovery algorithm.
```

```{py:attribute} step
:type: float
:value: 1
:noindex:

Step to use for the search. The unit depends on the polarisation controller used.
```

```{py:attribute} start_course
:type: float
:value: 0

First value of the search. The unit depends on the polarisation controller used.
```

```{py:attribute} end_course
:type: float
:value: 0

Last value of the search. The unit depends on the polarisation controller used.
```

```{py:attribute} wait_time
:type: float
:value: 0

Wait time, in seconds, between two positions of the search.
```

##### Polarisation Controller

This section is for the polarisation controller to use for polarisation recovery.

```{py:attribute} device
:type: str
:value: '"qosst_hal.polarisation_controller.FakePolarisationController"'
:noindex:

Class of the device to use for the polarisation controller.
```

```{py:attribute} location
:type: str
:value: '""'
:noindex:

Location of the polarisation controller.
```

##### Powermeter

This section is for the powermeter to use for polarisation recovery.

```{py:attribute} device
:type: str
:value: '"qosst_hal.polarisation_controller.FakePowerMeter"'
:noindex:

Class of the device to use for the powermeter.
```

```{py:attribute} location
:type: str
:value: '""'
:noindex:

Location of the powermeter.
```

```{py:attribute} timeout
:type: int
:value: 10
:noindex:

Timeout for the powermeter.
```

#### DSP

This section holds the different parameters that will be used during the Digital Signal Processing of Bob.

This section holds the parameters for the Digital Signal Processing of Bob. A brief discussion of each parameter is present for each of them, but the reader should also refers to the documentation of the Digital Signal Processing of Bob in `qosst-bob`.

````{py:attribute} debug
:type: bool
:value: "True"

If True, a {external:py:class}`qosst_bob.dsp.dsp.DSPDebug` object is returned by the DSP with more information.

```{note}
The information contained in this object is:
* Begin and end of the Zadoff-Chu sequence;
* Begin and end of the data;
* Arrays containing the tones;
* Uncorrected data;
* Frequencies of pilots and beat;
* Difference of frequencies between the pilots and clock correction.
```
````

````{py:attribute} fir_size
:type: int
:value: 500

Number of taps for the Finite Impulse Response (FIR) filters.

```{note}
Those filters are mainly used to filter the tones.
```
````

`````{py:attribute} tone_filtering_cutoff
:type: float
:value: 10e6

Cut-off frequency for the filtering of the pilots in Hz.

````{note}
Once the pilot as been detected by a maximum peak searching in frequency, yielding the frequency {math}`f_{tone}`, the tone is filtered with a FIR filter on the frequency region

```{math}
\left[f_{tone} - f_{cutoff}, f_{tone}+f_{cutoff}\right]
```

````
`````

```{py:attribute} process_subframes
:type: bool
:value: "False"

In general, the Digital Signal Processing algorithm can operate in two ways:

1. In the first way, the whole process is done on the whole data
2. In the second way, the data is separated into smaller chunk to apply the carrier frequency estimation, the phase compensation, the downsampling for each chunk.

The second way is called subframes and is useful if some parameters are varying, as for instance the beat frequency between the two lasers.

This parameter controls if the data should be processed as subframes (`True`) or not (`False`).
```

```{py:attribute} subframes_size
:type: int
:value: 0

The size of the subframes can be adjusted by choosing how many **symbols** should be recovered in each subframes.

This parameter should not be 0 if `process_subframes` is `True`.
```

```{py:attribute} abort_clock_recovery
:type: float
:value: 0

The clock recovery algorithm uses the difference pilots frequencies to estimate the clock difference. However, in some cases this algorithm can fail, and it is better to leave the clock uncorrected than corrected with the wrong correction. This parameters determine the maximum ratio between the two clocks allowed for clock correction before it aborts.

Letting the value of 0 will ensure that the algorithm never aborts.
```

```{py:attribute} alice_dac_rate
:type: int
:value: 500e6

Rate of the DAC of Alice in Samples per second.

Bob's Digital Signal Processing requires the knowledge of Alice's rate.
```

`````{py:attribute} exclusion_zone_pilots
:type: "List[List[float, float]]"
:value: "[[0.0, 100e3]]"

Exclusion zone for the search of the pilots. This is represented as a list of lists. The insides tuple should be a of length 2, where the first element is the beginning of the exclusion zone (included) and the second element is the end of the exclusion zone (also included).

````{note}
If you consider this as being {math}`[[a_1, b_1], [a_2, b_2], ..., [a_n, b_n]]`, then the union of intervals

```{math}
U = \bigcup_{1\leq i \leq n} [a_i, b_i]
```
will be ignored for pilots searching.
````
`````

```{py:attribute} pilot_phase_filtering_size
:type: int
:value: 0

Before phase compensation, the phase is filtered using an uniform filter. This parameter represents the size of this filter.

If this parameter is 0, then the filter is not applied.
```

```{py:attribute} num_samples_fbeat_estimation
:type: int
:value: 100000

In the general case, the carrier frequency should be found before precise synchronisation. For this, the synchronisation sequence is found with low precision and a chunk of data is used to estimate the beat frequency. This parameter controls the size of this chunk.
```

##### Equalizer

This section holds the parameters for the equalizer, that is part of the Digital Signal Processing (experimental).

More information on the equalizer can be found in the documentation of `qosst-bob`.

```{warning}
Equalizer is marked as experimental for now.
```

```{py:attribute} equalize
:type: bool
:value: "False"

If True, the Constant Modulus Algorithm (CMA) equalizer will be used.
```

```{py:attribute} length
:type: int
:value: 100

Length of the equalizer filter.
```

```{py:attribute} step
:type: float
:value: 0.01

Step of the equalizer.
```

```{py:attribute} p
:type: int
:value: 2

Parameter p for the equalizer.
```

```{py:attribute} q
:type: int
:value: 2

Parameter q for the equalizer.
```

#### Parameters estimation

This section hodls the configuration to perform parameters estimation.

```{py:attribute} estimator
:type: str
:value: '"qosst_core.parameters_estimation.NoneEstimator"'

Import path of the estimator class to use. The estimator should be a valid class, inheriting from {py:class}`qosst_core.parameters_estimation.BaseEstimator`.
```

```{py:attribute} skr_calculator
:type: str
:value: '"qosst_core.skr_computations.NoneSKRCalculator"'

Import path of the Secret Key Rate (SKR) calculator class to use. The calculator should be a valid class, inheriting from {py:class}`qosst_core.skr_computations.BaseCVQKDSKRCalculator`.
```

````{py:attribute} ratio
:type: float
:value: 0.5

Ratio of data to use for the estimation of the parameters. For instance, if the value is 0.5, 50% of the data will be used for the estimations. If it's 0.10, 10% will be used for the estimations.

```{warning}
This value should be be between 0 and 1.
```
````

#### Electronic noise

This section holds the configuration to load and save the electronic noise calibration.

```{py:attribute} path
:type: str
:value: '"electronic_noise.qosst"'
:noindex:

Path used to load and save the electronic noise object ({external:py:class}`qosst_bob.data.ElectronicNoise`).
```

#### Electronic shot noise

This section holds the configuration to load and save the electronic and shot noise calibration.

```{py:attribute} path
:type: str
:value: '"electronic_shot_noise.qosst"'
:noindex:

Path used to load and save the electronic and shot noise object ({external:py:class}`qosst_bob.data.ElectronicShotNoise`).

This will not be used in case automatic shot noise calibration is used.
```

### Frame

This section holds the description of the CV-QKD frame, that is common to Alice and Bon.

```{py:attribute} num_zeros_start
:type: int
:value: 0

Number of zeros to prepend to the final sequence before emission.
```

```{py:attribute} num_zeros_end
:type: int
:value: 0

Number of zeros to append to the final sequence before emission.
```

#### Pilots

This section holds the configuration for the classical pilots that are used for clock correction, carrier frequency recovery and phase compensation.

````{py:attribute} num_pilots
:type: int
:value: 2

Number of pilots to multiplex to the quantum data.

```{note}
In the general case, two pilots are required.
```
````

````{py:attribute} frequencies
:type: List[float]
:value: '[200e6, 220e6]'

List of frequencies for the pilots, in Hz. The scientific notation e is available.

```{warning}
The length of the list should be the equal to the number of pilots.
```
````

````{py:attribute} amplitudes
:type: List[float]
:value: '[0.4, 0.4]'

List of amplitudes for the pilots.

```{warning}
The length of the list should be the equal to the number of pilots.
```

```{note}
The sequence at Bob side is always generated between +1 and -1, and those amplitudes are relative to those limits.
```
````


#### Quantum

This section holds the configuration for the quantum data ion the frame.

```{py:attribute} num_symbols
:type: int
:value: 1000000

Number of symbols to generate / to expect to receive.
```

```{py:attribute} frequency_shift
:type: float
:value: 100e6

Frequency shift of the quantum data in Hz.
```

````{py:attribute} pulsed
:type: bool
:value: 'False'

If True, the pulse shaping will be regular pulses in time. If False, Nyquist pulse shaping is used.

```{warning}
Not real exchange were made in the pulsed regime.
```
````

```{py:attribute} symbol_rate
:type: int
:value: 100e6

Symbol rate in Symbols/second (Baud).
```

````{py:attribute} roll_off
:type: float
:value: 0.5

Value of the Roll-Off factor for the Root Raised Cosine (RRC) filter.

```{warning}
This value should be between 0 and 1.
```
````

````{py:attribute} variance
:type: float
:value: 0.01

Variance for the generation of the quantum symbols, again relative to the +1 and -1 limits.

```{Warning}
This value is not directly {math}`V_a` but {math}`V_a` is proportional to this value.
```
````

```{py:attribute} modulation_type
:type: str
:value: "qosst_core.modulation.GaussianModulation"

Import path of the modulation class to use. The modulation should be a valid class, inheriting from {py:class}`qosst_core.modulation.modulation.Modulation `.
```

````{py:attribute} modulation_size
:type: int
:value: 0

Size of the modulation for discrete modulations. This value is ignored for continuous modulations such as the Gaussian modulation.

```{warning}
Depending of the modulation, there might be additional constraints on this number such as being a power of 2 (PSK and QAM), or being a perfect square (QAM).
```
````

#### Zadoff-Chu

This configuration holds the configuration for the Zadoff-Chu sequence that is used for synchronisation.

```{py:attribute} root
:type: int
:value: 5

Root of the Zadoff-Chu sequence. This value should be coprime with the length of the Zadoff-Chu sequence.
```

```{py:attribute} length
:type: int
:value: 3989
:noindex:

Length of the Zadoff-Chu sequence. This value should be coprime with the root of the Zadoff-Chu sequence.
```

```{py:attribute} rate
:type: int
:value: 0
:noindex:

Rate of the Zadoff-Chu sequence in Samples/second. The notation e is available.

If 0 is used, the Zadoff-Chu is emitted at the maximal rate (*i.e.* the rate of Alice's DAC).
```

## Example configuration file

Below is displayed the example configuration file as provided in the `qosst-core` package.

```{eval-rst} 
.. literalinclude:: ../../../qosst_core/configuration/config.example.toml
    :language: toml
```