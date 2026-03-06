# stealth_led.py
import time
import ctypes
import keyboard
import re

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
    Parses the LLM response and flashes the Caps Lock LED for all correct options:
    A = 1 blink, B = 2 blinks, C = 3 blinks, D = 4 blinks.
    Adds a 2-second pause between different option letters.
    """
    # \b ensures we only match standalone letters (ignoring 'A' and 'D' inside the word "AND")
    matches = re.findall(r'\b[A-D]\b', ai_response.upper())
    
    # Remove duplicates and sort them alphabetically (e.g., ['A', 'C'])
    unique_answers = sorted(list(set(matches)))
    
    if not unique_answers:
        print("Could not find A, B, C, or D in the response.")
        return

    mapping = {'A': 1, 'B': 2, 'C': 3, 'D': 4}

    print(f"Hardware Notifier: Signaling sequence for {unique_answers}...")
    
    # Ensure the light is OFF before we start signaling

    # Loop through each answer letter found
    for index, letter in enumerate(unique_answers):
        blinks = mapping[letter]
        
        # Flash the LED the correct number of times for the current letter
        for _ in range(blinks):
            set_caps_lock(True)  # Light ON
            time.sleep(0.8)      # Hold for 400ms
            set_caps_lock(False) # Light OFF
            time.sleep(0.8)      # Pause between blinks
            
        # If this is not the last letter in the list, pause for 2 seconds before the next sequence
        if index < len(unique_answers) - 1:
            time.sleep(2.0)