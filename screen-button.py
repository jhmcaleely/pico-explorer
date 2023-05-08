# flashes LED until button depressed. Then terminates, leaving the led in the last state

from machine import Pin
import uasyncio
from picographics import PicoGraphics, DISPLAY_PICO_EXPLORER, PEN_P4

# We're only using a few colours so we can use a 4 bit/16 colour palette and save RAM!
display = PicoGraphics(display=DISPLAY_PICO_EXPLORER, pen_type=PEN_P4, rotate=0)

display.set_backlight(0.5)
display.set_font("bitmap8")

WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)
CYAN = display.create_pen(0, 255, 255)
MAGENTA = display.create_pen(255, 0, 255)
YELLOW = display.create_pen(255, 255, 0)
GREEN = display.create_pen(0, 255, 0)

# sets up a handy function we can call to clear the screen
def clear():
    display.set_pen(BLACK)
    display.clear()
    display.update()


def display_text(text, color):
    display.set_pen(color)
    display.text(text, 10, 10, 240, 4)
    
# set up
clear()

display_text("Press any button!", GREEN)
display.update()

cancel_me = False


def button_a_pressed():
    button_pressed("Button A pressed", WHITE)

def button_b_pressed():
    button_pressed("Button B pressed", CYAN)

def button_x_pressed():
    button_pressed("Button X pressed", MAGENTA)

def button_y_pressed():
    button_pressed("Button Y pressed", YELLOW)

def button_pressed(text, colour):
    clear()
    display_text(text, colour)
    display.update()

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

async def poll_button(gpio, onpressed):
    global cancel_me
    
    button = Pin(gpio, mode=Pin.IN, pull=Pin.PULL_UP)
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
    tasks.append(uasyncio.create_task(poll_button(12, button_a_pressed)))
    tasks.append(uasyncio.create_task(poll_button(13, button_b_pressed)))
    tasks.append(uasyncio.create_task(poll_button(14, button_x_pressed)))
    tasks.append(uasyncio.create_task(poll_button(15, button_y_pressed)))
    
    await uasyncio.gather(*tasks)

uasyncio.run(main())

