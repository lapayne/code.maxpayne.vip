###############################
# Import libraries            #
###############################
import RPi.GPIO as GPIO
import time
import random
import os
import vlc

# --- Pin Definitions (BCM numbering scheme) ---
LED1 = 14 #blue
LED2 = 15 #green
LED3 = 18
LED4 = 23
LED5 = 24

# --- Setup GPIO (Remainder of setup unchanged) ---
GPIO.setmode(GPIO.BCM)
GPIO.setup([LED1, LED2, LED3, LED4, LED5], GPIO.OUT)
PWM_FREQ = 100

pwm_stove = GPIO.PWM(LED1, PWM_FREQ)
pwm_lower1 = GPIO.PWM(LED2, PWM_FREQ)
pwm_upper1 = GPIO.PWM(LED3, PWM_FREQ)
pwm_lower2 = GPIO.PWM(LED4, PWM_FREQ)
pwm_upper2 = GPIO.PWM(LED5, PWM_FREQ)

pwm_stove.start(0)
pwm_lower1.start(0)
pwm_upper1.start(0)
pwm_lower2.start(0)
pwm_upper2.start(0)

led_pwms = [pwm_stove, pwm_lower1, pwm_upper1, pwm_lower2, pwm_upper2]

# --- Global Player Reference ---
# These must be global so the callback can access them
GLOBAL_PLAYER = None 
GLOBAL_MEDIA = None

# --- Event Handler Function (THE FIX) ---
def audio_end_callback(event):
    global GLOBAL_PLAYER
    
    # 1. Add a brief pause to allow VLC state transition
    time.sleep(0.1) 
    
    # 2. Re-play the media from the beginning.
    # The combination of end-reached event + stop/play is the most reliable way.
    GLOBAL_PLAYER.stop()
    GLOBAL_PLAYER.play()
    print("VLC Loop Triggered.")

# -----------------------------------------------

def flicker_leds():
    global GLOBAL_PLAYER, GLOBAL_MEDIA
    
    vlc_instance = None
    
    print("Initializing VLC audio...")
    try:
        vlc_instance = vlc.Instance("--aout=alsa --no-xlib")
        GLOBAL_PLAYER = vlc_instance.media_player_new()

        audio_file_path = os.path.abspath('fire.mp3')
        GLOBAL_MEDIA = vlc_instance.media_new(audio_file_path)

        GLOBAL_PLAYER.set_media(GLOBAL_MEDIA)
        
        # 💥 EVENT LISTENER SETUP 💥
        event_manager = GLOBAL_PLAYER.event_manager()
        
        # Attach the callback function to the 'Media Player End Reached' event
        event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, audio_end_callback)

        GLOBAL_PLAYER.play()
        print("Fire sound started (Event-looping). Starting LED flicker simulation... Press Ctrl+C to stop.")

        # --- Main Flicker Loop ---
        while True:
            # Use a slightly longer main loop sleep to reduce CPU load 
            # while the event loop is running asynchronously.
            time.sleep(0.01) 
            
            for led in led_pwms:
                brightness = random.randint(50, 100)
                led.ChangeDutyCycle(brightness)
                delay = random.uniform(0.05, 0.15)
                time.sleep(delay)

    except KeyboardInterrupt:
        print("\nSimulation stopped by user.")

    finally:
        # --- Cleanup GPIO ---
        for led in led_pwms:
            led.stop()

        # Clean up VLC resources
        if GLOBAL_PLAYER:
            # Detach the event handler 
            event_manager.event_detach(vlc.EventType.MediaPlayerEndReached)
            GLOBAL_PLAYER.stop()
            
        GPIO.cleanup()
        print("GPIO cleaned up. Simulation finished.")

# Run the simulation
if __name__ == '__main__':
    flicker_leds()
