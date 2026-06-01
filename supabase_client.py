from supabase import create_client, Client
import os


SUPABASE_URL = "https://jfmvlxadqhgbvovnbcbq.supabase.co"
SUPABASE_KEY = ""

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)