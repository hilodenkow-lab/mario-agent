import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel

# Load .env
load_dotenv()

# Schema JSON (tetap di sini)
class keputusanagent(BaseModel):
    alasan: str
    url_tujuan: str

def get_client():
    """Fungsi pembantu buat bikin client dengan API Key yang bener."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY tidak ditemukan di .env!")
    return genai.Client(api_key=api_key)

def pikirkan_perintah(perintah_user, konteks_halaman=""):
    # Panggil client di DALAM fungsi ini, jangan di global scope
    client = get_client() 
    
    prompt_lengkap = f"Perintah User: {perintah_user}\n\nKonteks Halaman Saat Ini:\n{konteks_halaman}"

    response = client.models.generate_content(
        model='gemini-2.0-flash', # Pastikan nama modelnya bener (biasanya gemini-2.0-flash)
        contents=prompt_lengkap,
        config=types.GenerateContentConfig(
            system_instruction=(
                "Tugasmu adalah menganalisis perintah user..."
            ),
            response_mime_type="application/json",
            response_schema=keputusanagent,
        ),
    )
    return response.parsed