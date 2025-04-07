from supabase import create_client, Client

# Replace these with your actual values from Supabase → Settings → API
url = "https://tmkyofqcohexnhqnrshw.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRta3lvZnFjb2hleG5ocW5yc2h3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM5MTM0OTAsImV4cCI6MjA1OTQ4OTQ5MH0.70FHh3pgwogvRDFwegEK0848GlV49T2w4tUzeOFHox4"

try:
    supabase: Client = create_client(url, key)
    response = supabase.table("users").select("*").limit(1).execute()
    print("✅ Supabase is connected!")
    print("Sample data:", response.data)
except Exception as e:
    print("❌ Supabase connection failed!")
    print("Error:", e)
