"""qr_reader.py

QR code reader utility for app.py.

Main function:
  - scan_qr(image_path) -> (status: bool, data: str)
    Returns (True, decoded_string) on success or (False, error_message) on failure.

Dependencies:
  - pyzbar (for actual QR scanning)
  - Pillow (for image handling)
  - libzbar-64.dll (native library on Windows - can be installed via vcpkg or other methods)
"""

import os


def scan_qr(image_path):
    """
    Extract URL or text from a QR code image.
    Returns (success_flag, data) tuple.
    
    Args:
        image_path (str): Path to the QR code image.
    
    Returns:
        tuple: (bool, str) - (success, decoded_data_or_error_message)
    """
    
    if not os.path.exists(image_path):
        return False, f"File not found: {image_path}"
    
    try:
        from PIL import Image
        from pyzbar.pyzbar import decode
    except ImportError as e:
        return False, f"Missing dependency: {e}. Install with: pip install pyzbar pillow"
    
    try:
        img = Image.open(image_path)
        result = decode(img)

        if not result:
            return False, "No QR code detected in image"

        qr_data = result[0].data.decode("utf-8")
        return True, qr_data

    except FileNotFoundError:
        return False, f"libzbar-64.dll not found. See: https://github.com/NaturalHistoryMuseum/pyzbar#windows"
    except Exception as e:
        return False, f"Error scanning QR code: {str(e)}"
