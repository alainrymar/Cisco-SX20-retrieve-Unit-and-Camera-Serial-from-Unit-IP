"# Cisco-SX20-retrieve-Unit-and-Camera-Serial-from-Unit-IP" 

Retrieve Cisco SX20 Codec Unit Serial Number and Camera Serial Number from an IP @ list
written for python 3+.

Serial Codec IP is a list of IP addresses, one per line, from which we extract the Unit serial and camera serial.
Use Paramiko SSH library
file containing the IP addresses list must be in the same Directory than the SX20.py code file
Output is Codec_Camera_Serial.txt containing Codec IP + codec serial + camera serial per line

Usefull to retrieve Serials (Unit and Camera) in a large Cisco SX20 codec deployement.
