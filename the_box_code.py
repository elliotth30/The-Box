# --- Repositry Imports ---
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library.
import time # mporting Time for access to countdown and pause breaks.
import os # Allows direct terminal commands
import tm1637
import pygame

import datetime

# --- Variables ---
flicker_time=0.4
#activation_state=0

# --- Pin Numbers ---
#Button
button_pin=15
mag_pin=13
#LED
led_pin=11
#Display
display_clk=16 #CLK -> GPIO23 (Pin 16)
display_di0=18 #DI0 -> GPIO24 (Pin 18)

# --- Setting Startpoint ---
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    #Button
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 15 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(mag_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 13 to be an input pin and set initial value to be pulled low (off)
    #LED
GPIO.setup(led_pin, GPIO.OUT) # Sets the LED to an output
    #Display
Display = tm1637.TM1637(16,18,tm1637.BRIGHT_TYPICAL)
Display.Clear()
Display.SetBrightnes(1)

# - Red Button Pushed -
def button_push(channel):
    print("--- Red Button was pushed! --- \n")
    GPIO.output(led_pin, GPIO.LOW)
    Display.Clear()
    pygame.mixer.music.stop()
    

    #time.sleep(5)

# - Magnet Switch Activated -
def mag_switch(channel):
    #global activation_state
    #activation_state=1

    print("[Magnetic button activated!] \n")
    #time.sleep(5)

# - LED ON -
def led_on():
    GPIO.output(led_pin, GPIO.HIGH)
    print("[LED was set to ON!] \n")

# - LED OFF -
def led_off():
    GPIO.output(led_pin, GPIO.LOW)
    print("[LED was set to OFF!] \n")

# - Display -
def display_start(display_wait, flashes, flash_time, brightness):
    print("--- Starting Display --- \n")
    Display.Clear()
    print("[Display: Cleared!] \n")
    sleep(display_wait)
    #here
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    second = now.second
    currenttime = [ int(hour / 10), hour % 10, int(minute / 10), minute % 10 ] #intiger-devide - https://stackoverflow.com/questions/40514682/choose-a-certain-digit-of-a-number
    """print("---------------")
    print(now)
    print(hour)
    print(minute)
    print(second)
    print(currenttime)
    print("---------------")
    print(int(hour / 10))
    print(hour % 10)
    print(int(minute / 10))
    print(minute % 10)
    print("---------------")
    Display.Show(currenttime)
    sleep(4)"""
    sixty_second=[0 , 0 , 6, 0]
    while flashes!=0:
        Display.SetBrightnes(brightness)
        Display.Show(sixty_second)
        Display.ShowDoublepoint(1)
        Display.SetBrightnes(3)
        print("[Display: Set to 60 Seconds] \n")
        timer(flash_time)
        Display.Clear()
        print("[Display: Cleared!] \n")
        timer(flash_time/3)
        flashes=flashes-1
    Display.Show(sixty_second)
    Display.ShowDoublepoint(1)
    Display.SetBrightnes(brightness)
    print("[Display: Set to 60 Seconds] \n")


    #print("--------------- \n")
    #here - SET TO ONE VARIABLE
    
    #Display.Show(0, 0, 6, 0)
    #print("[Display: set to 60 seconds!] \n")
    #display.ShowDoublepoint(1)
    #print("[Display: Colon to ON!] \n")
    print("### Display Complete ### \n")


# - Timer -
def timer(timer_time):
    print(" Waiting for", timer_time, "Seconds!")
    time.sleep(timer_time)
    print(" Timer for", timer_time, "Complete! \n")

# - Sleep -
def sleep(sleep_time):
    #print("--- Starting Sleep --- \n")
    print("[", sleep_time, "seconds starting! ]\n")
    while sleep_time!=0:
        print(" "+str(sleep_time))
        time.sleep(1)
        sleep_time=sleep_time-1
    #print("--- Sleep Complete --- \n")
    print(" 0 \n")

# - Flicker -
def flicker(sleep_time, flicker_time, flicker_percent):
    print("--- Starting Flicker --- \n")
    sleep(sleep_time)
    led_on()
    timer(flicker_time)
    led_off()
    timer(flicker_time*flicker_percent) # Multiplyered for a more analogue flicker feel.
    led_on()
    print("### Flicker Complete ### \n")
    #time.sleep(5)

# - Credits -
def credits(c_status):
    os.system('clear') # Clears the screen - (for debugging and code display)
    if c_status==1: # are credits activated? "1" = TRUE
        print("The Box.")
        time.sleep(1)
        print("Designed & Programmed by Elliott Hall\n")
        print("Portfolio - www.elliotthall.co.uk")
        print("Email - hello@elliotthall.co.uk \n")
        print("######################################## \n")
    else:
        print("The Box. \n")

# - Activation - (awaiting Magnetic Release)
def mag_activation(start, mag_state):
    if start==1: # Is magnetic activation turned on? "1" = TRUE
        print("--- Magnetic Activation --- \n")
        if mag_state=="HIGH":
            print("[Mag_state set to HIGH!]")
            while GPIO.input(mag_pin) == GPIO.HIGH: #Set to work on magnetic press
                time.sleep(0.1)  # wait 10 ms to give CPU chance to do other things
            mag_switch(mag_pin)
        elif mag_state=="LOW":
            print("[Mag_state set to LOW!]")
            while GPIO.input(mag_pin) == GPIO.LOW: #Set to work on magnetic release
                time.sleep(0.1)  # wait 10 ms to give CPU chance to do other things
            mag_switch(mag_pin)
        else:
            print("Mag_state '"+mag_state+"' not recognised set to HIGH or LOW \n")
            print("[ Mag_state automatically set to LOW ] \n")
            #mag_state=("LOW")
            while GPIO.input(mag_pin) == GPIO.LOW: #Set to work on magnetic release
                time.sleep(0.1)  # wait 10 ms to give CPU chance to do other things
            mag_switch(mag_pin)
        print("### Magnetic Activation Complete ### \n")
    else:
        print("[Magnetic Activation set to OFF] \n")

# - Starting Countdown - [countdown ~ syncing audio during testing]
def start_clock(start,start_time):
    if start==1:
        print("--- Starting Countdown --- \n")
        sleep(start_time)
    else:
        print("[Countdown set to OFF] \n")

def play_audio():
    pygame.mixer.init()
    pygame.mixer.music.load('the_box_audio.mp3')
    pygame.mixer.music.play(loops=0)

# --- Debug Menu/Display ---
def debug_menu():
    led_off()
    credits(1) # ON or OFF [1 or 0]
    mag_activation(1, "LOW") # ON or OFF[1 or 0], HIGH OR LOW
    play_audio()
    start_clock(0, 4) # ON or OFF[1 or 0], Count down time
    flicker(12, 0.12, 1.3) # [time before flicker], [ON/OFF time], [Percentage Multiplyer]
    display_start(5, 1, 0.6, 3) # [how long to wait before starting display], [Number of flashed], [Flash time], [Brighrness]

# --- Program Start ---
debug_menu()

GPIO.add_event_detect(button_pin,GPIO.RISING,callback=button_push,bouncetime=150) # Setup event on pin 10 rising edge
GPIO.add_event_detect(mag_pin,GPIO.RISING,callback=mag_switch,bouncetime=100) # Setup event on pin 10 rising edge

message = input("\nPress enter to quit\n\n") # Run until someone presses enter

GPIO.cleanup() # Clean up