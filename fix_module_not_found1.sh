#!/bin/bash

echo "Starting OpenAI module installation fix..."

# Update package list and install pip if needed
echo "Checking and updating system packages..."
sudo apt update && sudo apt install -y python3-pip

# Verify pip installation
echo "Checking pip version..."
pip --version || { echo "pip is not installed. Please install pip first."; exit 1; }

# Install required Python packages
echo "Installing required Python packages..."
pip install openai pytesseract pdf2image requests pandas streamlit

# Verify OpenAI installation
echo "Verifying OpenAI installation..."
python3 -c "import openai; print('OpenAI module is installed successfully!')" || { echo "OpenAI installation failed."; exit 1; }

# Provide instructions for virtual environment usage
echo "To use a virtual environment, follow these steps:"
echo "1. Create a virtual environment: python -m venv myenv"
echo "2. Activate it: source myenv/bin/activate (Mac/Linux) or .\myenv\Scripts\activate (Windows)"
echo "3. Install packages inside the environment: pip install -r requirements.txt"

# Provide guidance for Streamlit Cloud deployment
echo "If deploying on Streamlit Cloud:"
echo "1. Create a requirements.txt file with the following contents:"
echo "   openai"
echo "   pytesseract"
echo "   pdf2image"
echo "   requests"
echo "   pandas"
echo "   streamlit"
echo "2. Upload your project with this file, and Streamlit Cloud will install dependencies automatically."

echo "All required modules are installed successfully!"
