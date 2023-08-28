#!/usr/bin/python
# Authorized by Kenan Soufan - Arista Network 2022

import os
import subprocess
import sys
import time
import json
import struct

def EOSUpgradecheck (  ):
  currentEOS = getValueFromFile( "/etc/swi-version", "SWI_VERSION" )
  minEOS = "4.25"
  url="http://192.168.20.65/EOS-4.25.4M.swi"
  dest_folder = "/mnt/flash/"
  filename = url.split('/')[-1].replace(" ", "_")
  file_path = os.path.join(dest_folder, filename) 
  if currentEOS < minEOS:
    r = requests.get(url, stream=True)
    if r.ok:
        with open(file_path, 'wb') as f:
             for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                   f.write(chunk)
                   f.flush()
                   os.fsync(f.fileno())
             output = subprocess.check_output ( 'FastCli -p 15 -c "enable \n configure  \n boot system flash:EOS-4.25.4M.swi"', shell =True)
    else: 
    # HTTP status code 4XX/5XX
        print("Download failed")
def Copyconfig ():
    url="http://192.168.20.65/config"
    cmd = "wget {} -O /mnt/flash/config; sudo ip netns exec default /usr/bin/FastCli \
         -p15 -G -A -c $'configure replace flash:config ignore-errors'".format(url)
    subprocess.check_output ( cmd, shell=True, stderr=subprocess.STDOUT )
    subprocess.call( [ "reboot" ] )
if __name__ == "__main__":
	EOSUpgradecheck (  )
	Copyconfig ()