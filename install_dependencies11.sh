#!/bin/bash

# Update package list and install pip (if not installed)
echo "Updating package list and installing pip..."
sudo apt update && sudo apt install -y python3-pip

# Install required Python packages
echo "Installing required Python packages..."
pip install openai pytesseract pdf2image requests pandas streamlit

echo "All required modules are installed successfully!"
