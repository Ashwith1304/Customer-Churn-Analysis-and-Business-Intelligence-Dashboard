"""
Customer Churn Analysis and Business Intelligence Dashboard
Main Application Entrypoint
"""

import sys
import os
from pathlib import Path

# Add project root to Python search path
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Import and execute the Streamlit dashboard
import app.streamlit_app
