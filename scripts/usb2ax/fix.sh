python usb2ax_fix.py 
dfu-programmer atmega32u2 erase
dfu-programmer atmega32u2 flash fix.hex
#/!\: with some versions of dfu-programmer, the .hex needed to have UNIX-style end of lines (\n, LF) instead of DOS end of lines (\r\n CRLF)!
dfu-programmer atmega32u2 start
