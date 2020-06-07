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

### [program #3](./3-pdfRead.py)

* download the required pdf for this program from [here](http://www.wired.com/images_blogs/threatlevel/2010/12/ANONOPS_The_Press_Release.pdf)
* pypdf module has been depreciated, so using PyPDF2 in it's place
* urlencode, urlparse and urlopen have been changed to different modules