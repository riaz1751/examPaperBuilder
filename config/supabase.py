from supabase import create_client
import os

SUPABASE_URL = os.getenv("https://fvvswvfoqgfeyzqxdpdd.supabase.co")
SUPABASE_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ2dnN3dmZvcWdmZXl6cXhkcGRkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDEzODk1MzAsImV4cCI6MjA1Njk2NTUzMH0.B27MlhEHPfXPXtkuJSiuFLMeGpOG5zhxSCDbhAJagag")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
