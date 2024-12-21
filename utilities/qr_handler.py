import os
import pyqrcode
from pyqrcode import QRCode

def generate_qr(text, image_name):
    # Define the directory path
    directory = 'C:/images/static/qr_codes/'

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Generate QR code
    url = pyqrcode.create(text)

    # Create and save the PNG file
    url.png(f"{directory}{image_name}", scale=6)

# Test
if __name__ == "__main__":
    # String which represents the QR code 
    text = "www.geeksforgeeks.org"
    image_name = "{% static 'qr_codes/qr_1731275742404.png' %}"

    # Generate QR code and save it
    generate_qr(text, image_name)
