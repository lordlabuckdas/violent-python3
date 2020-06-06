# Chapter 3 - Forensic Investigations with Python

**note :** programs 1 and 2 are windows OS-specific

### [program #1](./1-discoverNetworks.py)

* 3rd and 4th arguments for openkey function for reading HKLM have been modified because i was using 32bit python in 64bit windows
* added headers to browser object to prevent error 403
* changed login page
* redirected to api response website with proper arguments instead of result page
* handled json response by api
* displays verbose physical location in addition to ssid, mac addr, latitude and longitude

### [program #2](./2-dumpRecycleBin.py)

* in recent windows operating systems, listing files of recycle bin of users only returns hex file
* handled hex files with binascii, replacing, slicing and decoding
* refer this [website](https://www.blackbagtech.com/blog/examining-the-windows-10-recycle-bin/) for theory behind hex files in recycle bin
* better error handling for unknown and inaccessible files