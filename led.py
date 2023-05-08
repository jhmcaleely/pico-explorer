# An asyncio LED flasher

from machine import Pin
import uasyncio as asyncio

# RPi Pico builtin LED on GPIO 25
led = Pin(25, mode=Pin.OUT, value=1)

async def flash(led, time):
    while True:
        await asyncio.sleep_ms(time)
        led.toggle()
        
asyncio.run(flash(led, 500))