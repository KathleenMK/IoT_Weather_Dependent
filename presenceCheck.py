#!/usr/bin/env python3
#coding=utf-8
#from presence-detector.pyfile from week7
# MAC addresses required on line 12

import subprocess
import logging

logging.basicConfig(filename='log.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

#dictionary of known devices 
devices = [{"name":"My Phone", "mac":""}    #MAC addresses are required
            #, {"name":"Someone Else", "mac":""}
        ]

# Returns the list of known devices found on the network
def find_devices():
    output = subprocess.check_output("sudo nmap -sn 192.168.1.0/24 | grep MAC", shell=True) #phone showing on .0 and not .13, opposite in VM
    print(output)
    devices_found=[]
    for dev in devices:   
        if dev["mac"].lower() in str(output).lower():
            logging.info(dev["name"] + " device is present")
            devices_found.append(dev)
        else:
            logging.info(dev["name"] + " device is NOT present")
    return(devices_found)

# Main program (prints the return of arp_scan )
def main():
    #return len(find_devices()) #added so that value can have type and be used in blynkScript
    print(find_devices())

if __name__ == "__main__":
    main()
