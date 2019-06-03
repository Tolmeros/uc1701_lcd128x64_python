## LCD ## 

JLX12864G-086
Monochrome 128x64 pixels.
SPI oneway interface (scl, mosi, cs) + 2 control pins(reset, rs/cd/a0).

## Required software ##

### python-spidev ###

### onion-gpio-sysfs ###
pyOnionGpio
gpio-sysfs


## Tested on ... ##

Tested on hlk-7688a (mt7688an). 
OS based on OpenWRT 18.06.2
Python 2.7.x
Now it is working only with software spi. 

## Software spi ##

On ephy leds (led pins for ethernet builtin switch)

Install `kmod-spi-gpio-custom`

Run `insmod spi-gpio-custom bus0=1,42,41,40,0,10000000`
