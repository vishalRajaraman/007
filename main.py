# main.py
import keyboard
import mss
from openCV_compressor import encode_frame_to_base64
from api_client import analyze_image

# 1. Define your sequential trigger 
SECRET_CODE = "sakthi"
key_buffer = []

def capture_and_process():
    print("\n[Sequence Detected] Intercepting Frame Buffer...")
    
    with mss.mss() as sct:
        # Grab the primary monitor
        monitor = sct.monitors[1]
        sct_img = sct.grab(monitor)
        
        try:
            # Step 1: Compress the frame buffer in RAM (calls compressor.py)
            print("Compressing image in RAM...")
            base64_image = encode_frame_to_base64(sct_img)
            
            # Step 2: Send to OpenAI (calls api_client.py)
            print("Sending to OpenAI...")
            result = analyze_image(base64_image)
            
            # Step 3: Print the result
            print("\n" + "="*40)
            print("🤖 Agent Response:")
            print("="*40)
            print(result)
            print("="*40 + "\n")
            
        except Exception as e:
            print(f"Error during processing: {e}")

def on_key_event(event):
    global key_buffer
    
    # We only care when a key is pressed down, not released
    if event.event_type == keyboard.KEY_DOWN:
        # We only want to track single character keys
        if len(event.name) == 1:
            key_buffer.append(event.name.lower())
            
            # Keep the buffer strictly the same length as our secret code
            if len(key_buffer) > len(SECRET_CODE):
                key_buffer.pop(0)
            
            # Match detected
            if "".join(key_buffer) == SECRET_CODE:
                capture_and_process()
                key_buffer.clear()

# Hook the custom function to listen to ALL keyboard events
keyboard.hook(on_key_event)

print("Stealth Agent is online.")
print(f"Type '{SECRET_CODE}' anywhere to trigger.")
print("Press 'ESC' to exit.")

keyboard.wait('esc')