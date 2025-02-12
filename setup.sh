#!/bin/bash
set -e

echo "Updating system packages..."
sudo apt-get update && sudo apt-get -qq -y install espeak-ng

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Setup complete!"
