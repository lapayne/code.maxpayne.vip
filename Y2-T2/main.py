import time
from typing import List
# Import the actual RPi.GPIO library for hardware control
import RPi.GPIO as GPIO

# 1. Pin Definitions
PIN_STOVE = 17
PIN_DOWNSTAIRS = 18
PIN_UPSTAIRS = 27
ALL_PINS: List[int] = [PIN_STOVE, PIN_DOWNSTAIRS, PIN_UPSTAIRS]


if __name__ == "__main__":
    # Define the duration for ON and OFF states
    FLASH_DURATION = 4

    try:
        # 2. Setup the GPIO configuration ONCE (outside the loop)
        # Use BCM numbering (GPIO numbers, not physical pin numbers)
        GPIO.setmode(GPIO.BCM)
        print("GPIO setup complete (using BCM numbering).")

        # 3. Set all pins as output
        for pin in ALL_PINS:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW) # Ensure pins start off
        
        print(f"\nStarting infinite toggle loop (ON/OFF every {FLASH_DURATION}s). Press Ctrl+C to stop.")
        
        # 4. Start the continuous loop
        while True:
            # --- ON CYCLE ---
            print(f"\n--- ACTION: Turning all pins ON (HIGH) for {FLASH_DURATION} seconds ---")
            for pin in ALL_PINS:
                GPIO.output(pin, GPIO.HIGH)

            time.sleep(FLASH_DURATION)

            # --- OFF CYCLE ---
            print(f"--- ACTION: Turning all pins OFF (LOW) for {FLASH_DURATION} seconds ---")
            for pin in ALL_PINS:
                GPIO.output(pin, GPIO.LOW)
            
            time.sleep(FLASH_DURATION)

    except KeyboardInterrupt:
        # This block catches the user pressing Ctrl+C gracefully
        print("\n\nLoop manually stopped by user (KeyboardInterrupt).")
    except Exception as e:
        # Catch any other unexpected errors
        print(f"\nAn unexpected error occurred: {e}")
    finally:
        # 5. Always perform cleanup to reset GPIO state when the script ends
        GPIO.cleanup()
        print("GPIO cleanup performed. Script exiting.")
