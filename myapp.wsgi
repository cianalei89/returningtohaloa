import sys
import os

# Set the path to your app folder
sys.path.insert(0, os.path.dirname(__file__))

# Import the app object from your Flask app
from webpage import app as application  # 'application' is the required name