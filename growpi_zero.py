import csv
import os
import time

from grovepi import *

# Connect the Grove Moisture Sensor to analog port A0, Light Sensor to A1
# Connect Waterpump to D3

# Sensors
moistureSensor = 0
lightSensor = 1
waterPump = 3

checkInterval = 10 * 60  # How long before loop starts again?
lightThreshold = 10  # Value above threshold is lightsOn

dryIntervals = 5  # How many consecutive dry intervals before waterPlants
mlSecond = 5  # How much ml water the waterpump produces per second
waterAmount = 50  # How much ml water should be given to the plants


# Write data to csv
def appendCSV():
    fields = ['Time', 'Moisture', 'MoistureClass',
              'LightValue', 'Lights', 'PiTemperature', 'WaterGiven']

    with open(r'moisture.csv', 'a') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writerow({'Time': currentTime,
                         'Moisture': moisture,
                         'MoistureClass': moistureClass,
                         'LightValue': lightValue,
                         'Lights': lightsOn,
                         'PiTemperature': (piTemperature()),
                         'WaterGiven': waterGiven
                         })


def piTemperature():
    temp = os.popen("vcgencmd measure_temp").readline()
    return temp[5:9]


def moistureClassifier():
    if moisture < 300:
        moistureResult = 'Dry'
    elif moisture < 600:
        moistureResult = 'Moist'
    else:
        moistureResult = 'Wet'
    return moistureResult


def printSensorData():
    print(currentTime)
    print('Moisture: {0} ({1})'.format(moisture, moistureClass))
    print("Lights: {} ({})".format(lightValue, "On" if lightsOn else "Off"))
    print("Raspberry pi: {}'C".format(piTemperature()))
    if waterGiven:
        print("Water given: {}ml\n".format(waterGiven))
    else:
        print("")


def waterPlants():
    digitalWrite(waterPump, 1)
    time.sleep(waterAmount / mlSecond)
    digitalWrite(waterPump, 0)


# Main Loop

waterCheck = []
while True:
    try:
        # Time loop
        t0 = time.time()

        # Get sensor readings
        lightValue = analogRead(lightSensor)
        moisture = analogRead(moistureSensor)

        currentTime = time.ctime()
        moistureClass = moistureClassifier()
        lightsOn = lightValue > lightThreshold

        # Lights on
        if lightsOn:
            # Check if ground is dry and append value to waterCheck
            if moistureClass == 'Dry':
                waterCheck.append(moisture)

                # Get x consecutive dryIntervals, before waterPlants
                if len(waterCheck) >= dryIntervals:
                    waterPlants()
                    waterGiven = waterAmount
                    waterCheck = []
                else:
                    waterGiven = 0

            else:
                waterCheck = []
                waterGiven = 0

        # Lights off
        else:
            # Not watering when dark
            waterCheck = []
            waterGiven = 0

        printSensorData()
        appendCSV()

        loopTime = time.time() - t0
        time.sleep(checkInterval - loopTime)

    except KeyboardInterrupt:
        digitalWrite(waterPump, 0)
        print(" Waterpump shutdown safely")
        break
    except IOError:
        print("Error")
