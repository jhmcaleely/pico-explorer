# An asyncio LED toggle in response to a button

from machine import Pin
import uasyncio as asyncio


async def poll_button():
    button = Pin(12, mode=Pin.IN, pull=Pin.PULL_UP)
    button_state = button.value()
    
    # RPi Pico builtin LED on GPIO 25
    led = Pin(25, mode=Pin.OUT, value=button_state)

    while True:
        await asyncio.sleep_ms(10)
        val = button.value()
        if val != button_state:
            led.toggle()
            button_state = val
        
asyncio.run(poll_button())