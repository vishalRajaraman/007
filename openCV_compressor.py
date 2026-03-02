# compressor.py
import numpy as np
import cv2
import base64

def encode_frame_to_base64(sct_img):
    """
    Takes an mss screen capture object, compresses it to PNG in RAM, 
    and returns a Base64 encoded string.
    """
    # Convert raw memory to a NumPy array (BGRA format)
    img_np = np.array(sct_img)
    
    # Compress the raw array into a PNG format entirely in RAM
    success, buffer = cv2.imencode('.png', img_np)
    
    if not success:
        raise ValueError("Failed to encode image in memory.")

    # Convert the RAM buffer directly to a Base64 string
    base64_image = base64.b64encode(buffer).decode('utf-8')
    
    return base64_image