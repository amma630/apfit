from supabase import create_client, Client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://tmkyofqcohexnhqnrshw.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRta3lvZnFjb2hleG5ocW5yc2h3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM5MTM0OTAsImV4cCI6MjA1OTQ4OTQ5MH0.70FHh3pgwogvRDFwegEK0848GlV49T2w4tUzeOFHox4")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
