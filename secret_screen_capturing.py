import keyboard
import mss
import mss.tools
import time
import os

def capture_and_open():
    print("\n[Hotkey Pressed] Intercepting Frame Buffer...")
    
    with mss.mss() as sct:
        # Grab the primary monitor
        monitor = sct.monitors[1]
        sct_img = sct.grab(monitor)
        
        # Generate the filename and path
        filename = f"screenshot_{int(time.time())}.png"
        filepath = os.path.join(os.getcwd(), filename)
        
        # Save it to your hard drive
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=filepath)
        print(f"Success! Image saved to: {filepath}")
        
        # ---> NEW: Open the image automatically <---
        print("Opening image in your default viewer...")
        os.startfile(filepath)

# Register the hotkey
hotkey = 'ctrl+shift+space'
keyboard.add_hotkey(hotkey, capture_and_open, suppress=True)

print("Background Agent is running.")
print(f"Press '{hotkey}' to capture and open the screen.")
print("Press 'ESC' to exit.")

keyboard.wait('esc')