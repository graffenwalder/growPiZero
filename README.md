# growPi-Zero

Raspberry Pi Zero WH, with GrovePi Zero. Checks ground moisture.
If moisture readings are "Dry" for x consecutive intervals, the waterpump will activate. Data is saved to `moisture.csv`.

![growPi](/images/plantsense.jpg)

## Hardware

- [Raspberry Pi Zero WH](https://www.kiwi-electronics.nl/raspberry-pi-zero-wh-header-voorgesoldeerd)
  - Adapter
  - 8GB SD Card
- [GrovePi Zero](https://www.dexterindustries.com/product/grovepizero/)
  - [Moisture Sensor](http://wiki.seeedstudio.com/Grove-Moisture_Sensor/)
  - [Light Sensor](http://wiki.seeedstudio.com/Grove-Light_Sensor/)
  - [Mini Fan](http://wiki.seeedstudio.com/Grove-Mini_Fan/)
- [3-6V Waterpump](https://www.bitsandparts.eu/Motoren-Servos-and-Drivers/Doseringspomp-Waterpomp-dompelpomp-3-6V-120l-h/p116339)
  - Aquarium tubing
  - Watercontainer (bottle, bucket.....)
  - 2 female to female jumper wires

## Setup

1. Download and burn [Raspbian](https://www.raspberrypi.org/downloads/raspbian/) to SD card.
2. Do initial Raspbian setup, make sure to setup an internet connection.
3. Update Raspbian:
```
$ sudo apt-get update
$ sudo apt-get upgrade
$ sudo apt-get dist-upgrade
```
4. Attach GrovePi Zero To Raspberry Pi Zero and run:
```
$ sudo curl -kL dexterindustries.com/update_grovepi | bash -s -- --bypass-gui-installation
$ sudo reboot
```
5. After reboot run:
```
$ sudo i2cdetect -y 1
```
- If the install was succesfull, you should see "04" in the output.
- See [GrovePi Setup](https://www.dexterindustries.com/GrovePi/get-started-with-the-grovepi/setting-software/) if unsuccesfull.
6. Connect waterpump to Mini Fan board:
- Carefully take off the plastic shell of both the jumperwires, on one end.
- Pull the waterpump wires through the small holes of the shells.
- Put the waterpump wires in the stripped opening of the jumperwires and attach them with some plyers
- Pull back the shells.
- Attach the other end of the jumperwires to the Mini Fan board, where the Mini Fan plug normaly goes.
- Attach aquarium tubing and put in watercontainer.
![waterpump](/images/waterpump.jpg)
7. Connect sensors to the GrovePi ports:

| Module/Sensor                  | Port  |
| -------------------------------|-------|
| Moisture Sensor                | A0    |
| Light Sensor                   | A1    |
| Mini Fan board (waterpump)	 | D3	 |


Feel free to use different ports, just be sure to change them in `growpi_zero.py`.

8. Launch growPi:
```
$ python growpi_zero.py
```

## Notes

- The waterpump in this setup produces about 5ml/second. Make sure to test how much your setup produces, results may vary.
