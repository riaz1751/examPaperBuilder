from dotenv import load_dotenv
import os
from supabase import create_client

# Load environment variables
load_dotenv()

# Log to verify loading
print("Loading environment variables...")

# Get Supabase URL and Key
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Log the values (for debugging only, remove once fixed)
print("SUPABASE_URL:", SUPABASE_URL)
print("SUPABASE_KEY:", SUPABASE_KEY)

# Ensure that the environment variables are loaded correctly
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in the .env file")

# Initialize the Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

