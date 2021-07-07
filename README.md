# VATSIM Online Controllers

![Version](https://img.shields.io/github/manifest-json/v/stevepiratex/vatsim-online-controllers)
![License](https://img.shields.io/github/license/stevepiratex/vatsim-online-controllers)
![Python Version](https://img.shields.io/github/pipenv/locked/python-version/stevepiratex/vatsim-online-controllers)

This uses a conbination of both the live VATSIM data feed and the AFV API

VATSIM Data Feed: https://data.vatsim.net/v3/vatsim-data.json

AFV API Server 1: https://voice1.vatsim.uk/api

AFV API Server 2: https://voice2.vatsim.uk/api

The load is balanced between the two AFV servers.


Using the generated config.ini file on first load, a polygon can be defined
for a division so if anyone logs in with an unusual/unsued callsign, they can
still be picked up. The position of the controller is not located in the VATSIM
data feed. This is where the AFV API comes in. It uses the first transmitter
and tests to see if the transmitter is within the defined polygon.

If the division uses a POF file for VRC, this can be used to define the callsigns
that the division uses in case the user's transmitter is outside of the polygon.
This means that a bulk of cases are handled to make sure everyone is on the online
list for when they control.