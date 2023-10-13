# Sensors that Use GPIO and GPIO Pin Actuator

This module contains:
* [gpio.dht_sensor.DhtSensor](#gpiodht_sensordhtsensor)
* [gpio.ds18x20_sensor.Ds18x20Sensor](#gpiods18x20_sensords18x20sensor)
* [gpio.rpi_gpio.RpiGpioSensor](#gpiorpi_gpiorpigpiosensor)
* [gpio.rpi_gpio.RpiGpioActuator](#gpiorpi_gpiorpigpioactuator)
* [gpio.gpio_led.GpioColorLED](#gpiogpio_ledgpiocolorled)

## `gpio.dht_sensor.DhtSensor`

A polling sensor that reads temperature and humidity from a DHT11, DHT22, or AM2302 sensor wired to the GPIO pins.

### Dependencies

This sensor uses the [adaFruit CircuitPython libraries](https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/python-setup).

```bash
sudo apt-get install libgpiod2
sudo pip3 install RPI.GPIO
sudo pip3 install adafruit-blinka
sudo pip3 install adafruit-circuitpython-dht
```

### Parameters

| Parameter     | Required | Restrictions                  | Purpose                                                                                                                                                                                    |
|---------------|----------|-------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `Class`       | X        | `gpio.dht_sensor.DhtSensor`   |                                                                                                                                                                                            |
| `Connections` | X        | dictionary of connectors      | Defines where to publish the sensor status for each connection. This sensor has 2 outputs, see below. Look at connection readme's for 'Actuator / sensor relevant parameters' for details. |
| `Level`       |          | DEBUG, INFO, WARNING, ERROR   | Override the global log level and use another one for this sensor.                                                                                                                         |
| `Poll`        | X        | Positive number               | Refresh interval for the sensor in seconds.                                                                                                                                                |
| `Sensor`      | X        | `DHT11`, `DHT22`, or `AM2302` | The type of the sensor.                                                                                                                                                                    |
| `Pin`         | X        |                               | GPIO data pin in BMC numbering.                                                                                                                                                            |
| `TempUnit`    |          | `F` or `C`                    | Temperature unit to use, defaults to `C`.                                                                                                                                                  |
| `Smoothing`   |          | Boolean                       | If `True`, publishes the average of the last five readings instead of each individual reading.                                                                                             |

### Outputs

The DhtSensor has 2 outputs which can be configured within the 'Connections' section (Look at connection readme's for 'Actuator / sensor relevant parameters' for details).

| Output        | Purpose                                                                                                  |
|---------------|----------------------------------------------------------------------------------------------------------|
| `Temperature` | Where to publish the temperature. When using with the openHAB connection configure a number/string Item. |
| `Humidity`    | Where to publish the humidity. When using with the openHAB connection configure a number/string Item.    |

### Configuration Example

```yaml
Logging:
    Syslog: yes
    Level: INFO

Connection1:
    Class: openhab_rest.rest_conn.OpenhabREST
    Name: openHAB
    URL: http://localhost:8080
    RefreshItem: Test_Refresh

SensorOutdoorClima:
    Class: gpio.dht_sensor.DhtSensor
    Connections:
        openHAB:
            Temperature:
                Item: temperature
            Humidity:
                Item: humidity
    Poll: 2
    Sensor: AM2302
    Pin: 7
    TempUnit: F
    Smoothing: False
    Level: DEBUG
```

## `gpio.ds18x20_sensor.Ds18x20Sensor`

A polling sensor that reads temperature from a DS18S20 or DS18B20 1-Wire bus sensor connected wired to the Raspberry Pi's GPIO pins.

### Dependencies

To enable the 1-Wire interface on your Raspberry Pi, add the following to the bottom of `/boot/config.txt`:

```bash
# Enable 1-Wire interface on default GPIO4
dtoverlay=w1-gpio
```

To load the `w1-gpio` and `w1-therm` kernel modules, add the following to `/etc/modules`:

```bash
# Load modules for DS18x20 1-Wire temperature sensors
w1-gpio
w1-therm
```

Reboot the Raspberry Pi.

### Parameters

| Parameter     | Required           | Restrictions                        | Purpose                                                                                                                                                     |
|---------------|--------------------|-------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `Class`       | X                  | `gpio.ds18x20_sensor.Ds18x20Sensor` |                                                                                                                                                             |
| `Connections` | X                  | dictionary of connectors            | Defines where to publish the sensor status for each connection.                                                                                             |
| `Level`       |                    | `DEBUG`, `INFO`, `WARNING`, `ERROR` | Override the global log level and use another one for this sensor.                                                                                          |
| `Poll`        | X                  | Positive number                     | Refresh interval for the sensor in seconds.                                                                                                                 |
| `Mac`         | X                  |                                     | Full 1-Wire device address. To list all 1-Wire devices, run `ls /sys/bus/w1/devices`. To read a specific one, run `cat /sys/bus/w1/devices/<Mac>/w1_slave`. |
| `TempUnit`    |                    | `F` or `C`                          | Temperature unit to use, defaults to `C`.                                                                                                                   |
| `Smoothing`   |                    | Boolean                             | If `True`, publishes the average of the last five readings instead of each individual reading.                                                              |

### Outputs

The DS18x20 sensor has only one output, the temperature.

### Configuration Example

Publishes to a MQTT connection with name `MQTT`:

```yaml
#Logging and connection configuration omitted

SensorTempOutside:
    Class: gpio.ds18x20_sensor.Ds18x20Sensor
    Connections:
        MQTT:
            StateDest: temp/outside
    Poll: 10
    Mac: 28-a66c801e64ff
```

## `gpio.rpi_gpio.RpiGpioSensor`

A sensor that can behave as either a polling sensor or a background sensor that reports the HIGH/LOW status of a GPIO pin.
Additionally, the sensor can detect toggle events and report the time of the event to different locations depending on the event duration.

### Dependencies

The user running sensor_reporter must have permission to access the GPIO pins.
To grant the `sensorReporter` user GPIO permissions add the user to the group `gpio`:

```bash
sudo adduser sensorReporter gpio
```

Depends on `RPi.GPIO`:

```bash
sudo pip3 install RPI.GPIO
```

### Basic parameters

| Parameter        | Required | Restrictions                        | Purpose                                                                                                                                                                                                                                   |
|------------------|----------|-------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `Class`          | X        | `gpio.rpi_gpio.RpiGpioSensor`       |                                                                                                                                                                                                                                           |
| `Connections`    | X        | dictionary of connectors            | Defines where to publish the sensor status for each connection. This sensor has 3 outputs, see below. Look at connection readme's for 'Actuator / sensor relevant parameters' for details.                                                |
| `Pin`            | X        | IO Pin                              | Pin to use as sensor input, using the pin numbering defined in `PinNumbering` (see below).                                                                                                                                                |
| `Level`          |          | `DEBUG`, `INFO`, `WARNING`, `ERROR` | Override the global log level and use another one for this sensor.                                                                                                                                                                        |
| `Poll`           |          | Positive decimal number             | The interval in seconds to check for a change of the pin state. If the new state is present for a shorter time then the specified time noting is reported. Can be used as debounce. When not defined `EventDetection` must be configured. |
| `EventDetection` |          | RISING, FALLING, or BOTH            | When defined, Poll is ignored. Indicates which GPIO event to listen for in the background.                                                                                                                                                |
| `PUD`            |          | The Pull UP/DOWN for the pin        | Defaults to "DOWN"                                                                                                                                                                                                                        |

### Advanced parameters

For a valid configuration the basic parameters marked as required are necessary, all advanced parameters are optional.

| Parameter               | Required | Restrictions                  | Purpose                                                                                                                                                                                                                                                                                              |
|-------------------------|----------|-------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `Values`                |          | list of strings or dictionary | Values to replace the default state message of the `Switch` output (default is OPEN, CLOSED). For details see below.                                                                                                                                                                                 |
| `Short_Press-Threshold` |          | decimal number                | Defines the lower bound of short button press event in seconds, if the duration of the button press was shorter no update will be send. Usful to ignor false detection of button press due to electrical interferences. (default is 0)                                                               |
| `Long_Press-Threshold`  |          | decimal number                | Defines the lower bound of long button press event in seconds, if the duration of the button press was shorter a short button event will be triggered. Can be determinded via the sensor-reporter log when set on info level. If not defined all button press events will be treated as short press. |
| `Btn_Pressed_State`     |          | LOW or HIGH                   | Sets the expected input level for short and long button press events. Set it to `LOW` if the input pin is connected to ground while the button is pressed (default is determined via PUD config value: `PUD = UP` will assume `Btn_Pressed_State: LOW`)                                              |

#### Values parameter

With this parameter the default state messages of the `Switch` output can be overwritten.
Two different layouts are possible.
To override the state message for all defined connections, configure a list of two string items:

```yaml
Values:
    - 'ON'
    - 'OFF'
```

The fist string will be send if the input is HIGH, the second on LOW.

If separate state messages for each connection are desired, configure a dictionary of connection names containing the string Item list:

```yaml
Values:
    <connection_name>:
        - 'ON'
        - 'OFF'
    <connection_name2>:
        - 'high'
        - 'low'
```

If a configured connection is not present in the Values parameter it will use the sensor default state messages (OPEN, CLOSED).

### Global parameters

Can only be set for all GPIO devices (RpiGpioSensor and RpiGpioActuator).
Global parameters are set in the `DEFAULT` section.
See example at the bottom of the page.

| Parameter      | Required | Restrictions | Purpose                                                                                                                                                                           |
|----------------|----------|--------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `PinNumbering` |          | BCM or BOARD | Select which numbering to use for the IO Pin's. Use BCM when GPIO numbering is desired. BOARD refers to the pin numbers on the P1 header of the Raspberry Pi board. (default BCM) |

### Outputs

The RpiGpioSensor has 3 outputs which can be configured within the `Connections` section (Look at connection readme's for 'Actuator / sensor relevant parameters' for details).

| Output             | Purpose                                                                                                                                                                                                                                                                                                                                                                                               |
|--------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `Switch`           | Where the OPEN/CLOSED messages are published. When using with the openHAB connection configure a contact/string Item.                                                                                                                                                                                                                                                                                 |
| `ShortButtonPress` | Location to publish an update after a short button press happened. Which are two changes of the logic level at the selected pin (eg. LOW, HIGH, LOW) and the duration of the button press is between Short_Press-Threshold and Long_Press-Threshold. For the recommended setup see example config at the bottom of the page. When using with the openHAB connection configure a datetime/string Item. |
| `LongButtonPress`  | Location to publish an update after a long button press happened, requires `Long_Press-Threshold`. When using with the openHAB connection configure a datetime/string Item.                                                                                                                                                                                                                           |

### Configuration Example

```yaml
Logging:
    Syslog: yes
    Level: INFO

Connection1:
    Class: openhab_rest.rest_conn.OpenhabREST
    Name: openHAB
    URL: http://localhost:8080
    RefreshItem: Test_Refresh

SensorBackDoor:
    Class: gpio.rpi_gpio.RpiGpioSensor
    Connections: 
        openHAB:
            Switch:
                Item: back_door
            ShortButtonPress:
                Item: back_door_short
            LongButtonPress:
                Item: back_door_long
    Pin: 17
    PUD: UP
    EventDetection: BOTH
    Long_Press-Threshold: 1.2

SensorFrontDoor:
    Class: gpio.rpi_gpio.RpiGpioSensor
    Connections:
        openHAB:
            Switch:
                Items: front_door
    Poll: 1
    Pin: 18
    PUD: UP
    Values:
        openHAB:
            - 'ON'
            - 'OFF'
    Level: DEBUG
```

## `gpio.rpi_gpio.RpiGpioActuator`

Commands a GPIO pin to go high, low, or if configured with SimulateButton it goes high for half a second and then goes to low.
A received command will be sent back on all configured connections to the configured return topic, to keep them up to date.

### Dependencies

The user running sensor_reporter must have permission to access the GPIO pins.
To grant the `sensorReporter` user GPIO permissions add the user to the group `gpio`:

```bash
sudo adduser sensorReporter gpio
```

Depends on `RPi.GPIO`:

```bash
sudo pip3 install RPI.GPIO
```

### Parameters

| Parameter        | Required | Restrictions                    | Purpose                                                                                                                                                                           |
|------------------|----------|---------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `Class`          | X        | `gpio.rpi_gpio.RpiGpioActuator` |                                                                                                                                                                                   |
| `Connections`    | X        | dictionary of connectors        | Defines where to subscribe for messages and where to publish the status for each connection. Look at connection readme's for 'Actuator / sensor relevant parameters' for details. |
| `Pin`            | X        | IO Pin                          | Pin to use as actuator output, using the pin numbering defined in `PinNumbering` (see below).                                                                                     |
| `Level`          |          | DEBUG, INFO, WARNING, ERROR     | Override the global log level and use another one for this sensor.                                                                                                                |
| `ToggleDebounce` |          | decimal number                  | The interval in seconds during which repeated toggle commands are ignored (default 0.15 seconds)                                                                                  |
| `InitialState`   |          | ON or OFF                       | Optional, when set to ON the pin's state is initialized to HIGH. Ignores InvertOut (default OFF)                                                                                  |
| `SimulateButton` |          | Boolean                         | When `True` simulates a button press by setting the pin to HIGH for half a second and then back to LOW. In case of `InitalState` ON it will toggle the other way around.          |
| `InvertOut`      |          | Boolean                         | Inverts the output when set to `True`. When inverted sending `ON` to the actuator will set the output to LOW, `OFF` will set the output to HIGH.                                  |

### Global parameters

Can only be set for all GPIO devices (RpiGpioSensor and RpiGpioActuator). Global parameters are set in the `DEFAULT` section.

| Parameter      | Required | Restrictions | Purpose                                                                                                                                                                           |
|----------------|----------|--------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `PinNumbering` |          | BCM or BOARD | Select which numbering to use for the IO Pin's. Use BCM when GPIO numbering is desired. BOARD refers to the pin numbers on the P1 header of the Raspberry Pi board. (default BCM) |

### Outputs / Inputs

The RpiGpioActuator has only one output and input.
The input expects ON, OFF, TOGGLE or a datetime string as command.
While ON, OFF set the GPIO pin accordingly, TOGGLE and a datetime string will toggle the pin.
Can be connected directly to a RpiGpioSensor ShortButtonPress / LongButtonPress output.
The output will send the pin state as ON / OFF after a change.
When using with the openHAB connection configure a switch/string Item.

### Configuration Examples

```yaml
DEFAULT:
    PinNumbering: BOARD

Logging:
    Syslog: yes
    Level: INFO

Connection1:
    Class: openhab_rest.rest_conn.OpenhabREST
    Name: openHAB
    URL: http://localhost:8080
    RefreshItem: Test_Refresh

ActuatorGarageDoor:
    Class: gpio.rpi_gpio.RpiGpioActuator
    Connections:
        openHAB:
            Item: GarageDoorCmd
    Pin: 35
    InitialState: ON
    SimulateButton: True
    Level: DEBUG
```

Using a local connection to toggle an actuator, which is also connected to openHAB.
The actuator shows always the correct status in openHAB, even if it is toggled locally.

```yaml
Logging:
    Syslog: yes
    Level: INFO

Connection_openHAB:
    Class: openhab_rest.rest_conn.OpenhabREST
    Name: openHAB
    URL: http://localhost:8080
    RefreshItem: Test_Refresh

Connection0:
    Class: local.local_conn.LocalConnection
    Name: local

SensorLightSwitch:
    Class: gpio.rpi_gpio.RpiGpioSensor
    Connections:
        local:
            ShortButtonPress:
                StateDest: toggle_garage_light
    Pin: 17
    PUD: UP
    EventDetection: BOTH
    Btn_Pressed_State: HIGH

ActuatorGarageLight:
    Class: gpio.rpi_gpio.RpiGpioActuator
    Connections:
        local:
            CommandSrc: toggle_garage_light
        openHAB:
            Item: garage_light
    Pin: 19
```

Circuit diagram

![example2](circuit_diagram/example2_circuit.png)

## `gpio.gpio_led.GpioColorLED`

Commands 3 to 4 GPIO pins to control a RGB or RGBW LED via software PWM.
A recieved command will be sent back on all configured connections to the configured return topic, to keep them up to date.

### Dependencies

The user running sensor_reporter must have permission to access the GPIO pins.
To grant the `sensorReporter` user GPIO permissions add the user to the group `gpio`:  `$ sudo adduser sensorReporter gpio`

Depends on RPi.GPIO.

```bash
sudo pip3 install RPI.GPIO
```

### Parameters

Parameter | Required | Restrictions | Purpose
-|-|-|-
`Class` | X | `gpio.gpio_led.GpioColorLED` |
`Connections` | X | dictionary of connectors | Defines where to subscribe for messages and where to publish the status for each connection. Look at connection readme's for 'Actuator / sensor relevant parameters' for details.
`Pin` | X | dictionary of pin's | Pin to use as PWM output use sub parameter `Red`, `Green`, `Blue`, `White`, using the pin numbering defined in `PinNumbering` (see below). It is not nessesary to define pin's for all colors.
`Level` | | DEBUG, INFO, WARNING, ERROR | When provided, sets the logging level for the sensor.
`InitialState` | | dictionary of values 0-100 | Optional, will set the PWM duty cycle for the color (0 = off, 100 = on, full brightness). Use the sub parameter `Red`, `Green`, `Blue`, `White` (default RGBW = 0)
`InvertOut` | | Boolean | Use `True` for common anode LED (default setting). Otherwhise use `False`

### Global parameters
Can only be set for all GPIO devices (RpiGpioSensor, RpiGpioActuator and GpioColorLED). Global parametes are set in the `DEFAULT` section
Parameter | Required | Restrictions | Purpose
-|-|-|-
`PinNumbering` | | BCM or BOARD | Select which numbering to use for the IO Pin's. Use BCM when GPIO numbering is desired. BOARD refers to the pin numbers on the P1 header of the Raspberry Pi board. (default BCM)

### Outputs / Inputs
The GpioColorLED has only one output and input.
The input expects 3 comma separated values as command. 
The values will set the LED color in HSV colorspace, e.g. `h,s,v`.
If the white pin is configured and the second value (saturation) = 0 then only the white LED will shine.
The output will replay the LED color state in the same format.
When using with the openHAB connection configure a color item.

### Example Config
```yaml
Logging:
    Syslog: yes
    Level: INFO

Connection_openHAB:
    Class: openhab_rest.rest_conn.OpenhabREST
    Name: openHAB
    URL: http://localhost:8080
    RefreshItem: Test_Refresh
    
ActuatorRgbLED:
    Class: gpio.gpio_led.GpioColorLED
    Pin:
        Red: 5
        Blue: 13
        Green: 6
        White: 7
    InitialState:
        White: 100
    Connections:
        openHAB:
            Item: eg_w_color_led
    Level: DEBUG
```
