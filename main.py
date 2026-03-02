# main.py
import keyboard
import mss
from openCV_compressor import encode_frame_to_base64
from api_client import analyze_image
from hardware_notifier import signal_answer,set_caps_lock  # <-- IMPORT THE NEW MODULE

SECRET_CODE = "sakthi"
key_buffer = []
def capture_and_process():
    print("\n[Sequence Detected] Intercepting Frame Buffer...")
    
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        sct_img = sct.grab(monitor)
        
        try:
            print("Compressing image in RAM...")
            base64_image = encode_frame_to_base64(sct_img)
            
            print("Sending to Gemini...")
            result = analyze_image(base64_image)
            
            print("\n" + "="*40)
            print("🤖 Agent Response:")
            print("="*40)
            print(result)
            print("="*40 + "\n")
            
            # ---> TRIGGER THE HARDWARE LED SIGNAL <---
            set_caps_lock(False)
            set_caps_lock(False);
            signal_answer(result)
            
        except Exception as e:
            print(f"Error during processing: {e}")

def on_key_event(event):
    global key_buffer
    
    if event.event_type == keyboard.KEY_DOWN:
        if len(event.name) == 1:
            key_buffer.append(event.name.lower())
            
            if len(key_buffer) > len(SECRET_CODE):
                key_buffer.pop(0)
            
            if "".join(key_buffer) == SECRET_CODE:
                capture_and_process()
                key_buffer.clear()

keyboard.hook(on_key_event)

print("Stealth Agent is online.")
print(f"Type '{SECRET_CODE}' anywhere to trigger.")
print("Watch your Scroll Lock LED for the answer!")
print("Press 'ESC' to exit.")

keyboard.wait('esc')