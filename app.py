import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Memuat variabel lingkungan dari file .env
load_dotenv()

# Mengambil API key dari variabel lingkungan
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Inisialisasi model Generative AI
model = genai.GenerativeModel('gemini-2.5-flash')

# Fungsi untuk mendapatkan respons dari Gemini
def get_gemini_response(question):
    try:
        # Menambahkan konteks untuk memastikan respons yang aman dan sesuai
        # Ini adalah prompt engineering yang penting untuk chatbot kesehatan mental
        prompt_with_context = (
            "Anda adalah asisten virtual yang ramah dan suportif untuk kesehatan mental. "
            "Anda dapat mendengarkan, memberikan kata-kata semangat, dan memberikan "
            "informasi umum seputar kesehatan mental. "
            "PENTING: Jangan pernah memberikan diagnosis, saran medis, atau "
            "menggantikan profesional. Selalu dorong pengguna untuk mencari bantuan profesional "
            "jika mereka merasa sangat tertekan atau dalam bahaya. "
            "Berikan respons yang empati dan menenangkan. "
            f"Pertanyaan pengguna: {question}"
        )
        response = model.generate_content(prompt_with_context)
        return response.text
    except Exception as e:
        return f"Maaf, terjadi kesalahan: {e}. Mohon coba lagi."

# --- Konfigurasi Antarmuka Streamlit ---
st.set_page_config(page_title="Chatbot Dukungan Mental 🤖❤️", layout="centered")

st.title("🤖 Teman Curhat AI")
st.markdown("---")
st.subheader("Selamat datang! 👋")
st.write(
    "Ini adalah chatbot sederhana yang dirancang untuk memberikan dukungan awal dan informasi "
    "umum seputar kesehatan mental. Saya di sini untuk mendengarkan. "
    "---"
    "**Penting:** Saya adalah AI dan **bukan** pengganti profesional kesehatan mental. "
    "Jika Anda dalam keadaan darurat atau sangat tertekan, **segera cari bantuan profesional**."
)
st.markdown("---")

# Menggunakan state session Streamlit untuk menyimpan riwayat percakapan
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan riwayat percakapan
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kolom input untuk pengguna
if prompt := st.chat_input("Apa yang sedang Anda pikirkan?"):
    # Tambahkan pesan pengguna ke riwayat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Dapatkan respons dari Gemini dan tambahkan ke riwayat
    with st.chat_message("assistant"):
        with st.spinner("Sedang memproses..."):
            response = get_gemini_response(prompt)
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})