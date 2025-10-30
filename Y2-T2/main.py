###############################
# Import libraries            #
###############################
import RPi.GPIO as GPIO
import time
import random
import os
import vlc

# --- Pin Definitions (BCM numbering scheme) ---
# GPIO17 - The Stove LED (The start of the fire in Pudding Lane)
STOVE_LED = 17
# GPIO18 - The Lower Floor LED
LOWER_FLOOR_LED = 18
# GPIO24 - The Upper Floor LED
UPPER_FLOOR_LED = 24

# --- Setup GPIO ---
# Use BCM (Broadcom SOC Channel) pin numbering
GPIO.setmode(GPIO.BCM) 

# Set up the pins as outputs
GPIO.setup([STOVE_LED, LOWER_FLOOR_LED, UPPER_FLOOR_LED], GPIO.OUT)

# Set up PWM (Pulse Width Modulation) for smooth brightness control
# Frequency is set to 100Hz for smooth transitions
PWM_FREQ = 100

pwm_stove = GPIO.PWM(STOVE_LED, PWM_FREQ)
pwm_lower = GPIO.PWM(LOWER_FLOOR_LED, PWM_FREQ)
pwm_upper = GPIO.PWM(UPPER_FLOOR_LED, PWM_FREQ)

# Start all PWM channels at 0% brightness (off)
pwm_stove.start(0)
pwm_lower.start(0)
pwm_upper.start(0)

# List of PWM objects for easy iteration
led_pwms = [pwm_stove, pwm_lower, pwm_upper]


def flicker_leds():
    vlc_instance = None
    player = None

    print("Initializing VLC audio...")
    try:
        # 1. Initialize VLC instance
        vlc_instance = vlc.Instance()
        
        # 2. Create a media player object
        player = vlc_instance.media_player_new()
        
        # 3. Get the absolute path of the audio file for robustness
        audio_file_path = os.path.abspath('fire.mp3')
        
        # 4. Create a media object and set it on the player
        media = vlc_instance.media_new(audio_file_path)
        player.set_media(media)
        
        # 5. Start playback
        player.play()
        print("Fire sound started. Starting LED flicker simulation... Press Ctrl+C to stop.")
    
   
        while True:
            # Iterate through each LED to give it a unique, staggered flicker
            for led in led_pwms:
                # 1. Random Brightness (Duty Cycle)
                # Range from 50% (dim) to 100% (bright) for a strong, burning effect
                brightness = random.randint(50, 100) 
                
                # 2. Apply the new brightness
                led.ChangeDutyCycle(brightness)
                
                # 3. Random Delay
                # A short, random delay makes the flicker look irregular and natural
                delay = random.uniform(0.05, 0.15)
                time.sleep(delay)

    except KeyboardInterrupt:
        # Exit cleanly when Ctrl+C is pressed
        print("\nSimulation stopped by user.")
    
    finally:
        # --- Cleanup GPIO ---
        # Stop all PWM channels
        for led in led_pwms:
            led.stop()
        
        # Reset all GPIO pins to a safe state
        GPIO.cleanup()
        print("GPIO cleaned up. Simulation finished.")

# Run the simulation
if __name__ == '__main__':
    flicker_leds()
