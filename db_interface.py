# db_interface.py

import os
from dotenv import load_dotenv
from supabase import create_client, Client
from typing import Dict, Any

# Load environment variables (Supabase URL and Key)
# NOTE: This load is crucial for this file to work outside of the Streamlit script's flow
load_dotenv() 
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY") 

# Global Supabase client instance
supabase: Client = None

if SUPABASE_URL and SUPABASE_SERVICE_KEY:
    try:
        # Initialize the Supabase client
        supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        # print("Supabase client initialized successfully.") 
    except Exception as e:
        print(f"Error initializing Supabase client: {e}")
else:
    print("Warning: Supabase credentials not found. Database functions will be disabled.")


# --- Database Functions for V2 ---
# (These are placeholders that app.py will call)

def save_user_profile(user_id: str, profile_json: Dict[str, Any]) -> bool:
    """Placeholder for saving the structured ResumeProfile JSON to Supabase."""
    if not supabase: return False
    print(f"Database simulation: Profile for {user_id} saved.")
    # In V2, the real Supabase insert/update logic goes here.
    return True

def save_user_alert_preferences(user_id: str, keywords: str, frequency: str) -> bool:
    """Placeholder for saving job alert preferences to Supabase."""
    if not supabase: return False
    print(f"Database simulation: Alerts for {user_id} saved.")
    # In V2, the real Supabase upsert logic goes here.
    return True