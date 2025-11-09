
import os
from supabase import create_client

# SUPABASE_URL = os.environ['SUPABASE_URL']
# SUPABASE_KEY = os.environ['SUPABASE_KEY']  # use anon/public key for front-end tasks, service_role only server-side

NEXT_PUBLIC_SUPABASE_URL='https://fbruzjoimpxapglrontg.supabase.co'
NEXT_PUBLIC_SUPABASE_ANON_KEY='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZicnV6am9pbXB4YXBnbHJvbnRnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI2MDE5MzEsImV4cCI6MjA3ODE3NzkzMX0.1f36TBZCzKSBdZRrKUsovcDEsJb0J0A4kGUOn9l6MNA'

supabase = create_client(NEXT_PUBLIC_SUPABASE_URL, NEXT_PUBLIC_SUPABASE_ANON_KEY)