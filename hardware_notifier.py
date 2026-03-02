# hardware_notifier.py
import time
import ctypes
import keyboard

# Windows Virtual Key code for Caps Lock
VK_CAPITAL = 0x14

def set_caps_lock(target_state):
    """
    Reads the physical hardware state of the Caps Lock LED.
    Only presses the key if the LED needs to change to match target_state.
    target_state: True (Light ON) or False (Light OFF)
    """
    # Ask Windows API for the current hardware state of the key
    current_state = ctypes.windll.user32.GetKeyState(VK_CAPITAL) & 0x0001
    
    # If the light isn't in the state we want, press it
    if bool(current_state) != target_state:
        keyboard.send('caps lock')

def signal_answer(ai_response):
    """
    Parses the LLM response and flashes the Caps Lock LED:
    A = 1 blink, B = 2 blinks, C = 3 blinks, D = 4 blinks.
    """
    text = ai_response.upper()
    
    blinks = 0
    if "A" in text: blinks = 1
    elif "B" in text: blinks = 2
    elif "C" in text: blinks = 3
    elif "D" in text: blinks = 4
    
    if blinks == 0:
        print("Could not find A, B, C, or D in the response.")
        return

    print(f"Hardware Notifier: Signaling {blinks} blinks on Caps Lock...")
    
    # Ensure the light is OFF before we start signaling
    set_caps_lock(False)
    time.sleep(0.5) 
    
    # Flash the LED!
    for _ in range(blinks):
        set_caps_lock(True)  # Light ON
        time.sleep(0.8)      # Hold for 400ms
        set_caps_lock(False) # Light OFF
        time.sleep(0.8)      # Pause between blinks