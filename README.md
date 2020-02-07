# iot-applications
The project allows you to control a relay in different ways, connected to a light.

# Introduction
You can create an intelligent light managed through the internet, and maintaining the functionality of the original light button.
This light can be managed with the original light button, Alexa, an Android app or an Amazon IoT button.

# Installation
NOTE: Necessary to make an explanation (TODO)

## Config contab
```sh
sudo crontab -e
```
Don't forget to change the directory in the CD command
add this command:
```sh
@reboot screen -S server -dm bash -c "CD /home/pi/Desktop/you_folder/ && python3 main.py 2>&1 | tee output.log"
```

# Config files
 * File: "Python - Raspberry Pi/config.json", field examples:
    * iot_endpoint: `<YOUR IOT ID>.iot.us-east-1.amazonaws.com`
    * name: `my bedroom`
    * MAC: `FF-FF-FF-FF-FF-FF`

# Voice commands for alexa:
 * Ask (App name) {State}
 * Open (App name)
     1. Alexa responds: Indicates action
     2. You can respond: {State}

 {State} = ["on", "off", "switch", "sleep", "wake up"]


# Help commands (CMD)
If the PC is turned on alone:
```cmd
powercfg -lastwake
```
```cmd
powercfg -waketimers
```

Get the mac of the pc:
```cmd
getmac
```

# Using
 * [AWS IoT](https://aws.amazon.com/iot/)
 * [AWS Lambda](https://aws.amazon.com/lambda/)
 * [AWS API Gateway](https://aws.amazon.com/api-gateway/)
 * [Amazon Alexa](https://developer.amazon.com/es/alexa)
 * [Amazon Alexa Dev](https://developer.amazon.com/alexa/console/ask)
 * [Raspberry Pi 3 Model B](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/)

