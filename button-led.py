# flashes LED until button depressed. Then terminates, leaving the led in the last state

from machine import Pin
import uasyncio

cancel_me = False

async def flash(time):
    global cancel_me
    
    # RPi Pico builtin LED on GPIO 25
    led = Pin(25, mode=Pin.OUT, value=1)

    while True:
        await uasyncio.sleep_ms(time)
        if cancel_me:
            return
        led.toggle()

def end_it():
    global cancel_me
    cancel_me = True

async def poll_button(onpressed):
    global cancel_me
    
    button = Pin(12, mode=Pin.IN, pull=Pin.PULL_UP)
    button_state = button.value()
    print("button state {}".format(button_state))
    
    while True:
        val = button.value()
        prev_state = button_state
        if val != button_state:
            button_state = val
        
        if prev_state == 1 and button_state == 0:
            # falling button
            print("uhm")
        
        if prev_state == 0 and button_state == 1:
            # rising button.
            onpressed()
        
        if cancel_me:
            return

        await uasyncio.sleep_ms(50)


async def main():
    tasks = []

    tasks.append(uasyncio.create_task(flash(500)))
    tasks.append(uasyncio.create_task(poll_button(end_it)))
    
    await uasyncio.gather(*tasks)

uasyncio.run(main())
