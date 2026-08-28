import streamlit as st
import json
import urllib.request
import os

st.set_page_config(page_title="AI Business Fortune Teller", page_icon="🔮", layout="centered")

GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY", ""))

st.title("🔮 AI BUSINESS FORTUNE TELLER")
st.caption("Program Studi Kewirausahaan")

with st.form("fortune_form"):
    nama = st.text_input("Nama & Asal Sekolah")
    target = st.text_input("Cita-Cita / Target Impian")
    who = st.text_area("Kartu 1: Who I Am (Hobi/Kepribadian)")
    what = st.text_area("Kartu 2: What I Know (Keahlian/Jurusan)")
    whom = st.text_area("Kartu 3: Whom I Know (Relasi/Akses)")
    submitted = st.form_submit_button("✨ RAMAL BISNIS MASA DEPANKU")

if submitted:
    if not who and not what and not whom:
        st.warning("Mohon isi minimal salah satu kartu modal.")
    elif not GROQ_API_KEY:
        st.error("API Key belum terpasang di Streamlit Secrets.")
    else:
        with st.spinner("🔮 AI sedang meramal..."):
            prompt = f"Ramal bisnis berdasarkan Effectuation. Nama: {nama}, Target: {target}, Who: {who}, What: {what}, Whom: {whom}."
            try:
                groq_req = urllib.request.Request(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
                    data=json.dumps({"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]}).encode('utf-8')
                )
                with urllib.request.urlopen(groq_req) as response:
                    res_data = json.loads(response.read().decode('utf-8'))
                    st.markdown(res_data['choices'][0]['message']['content'])
            except Exception as e:
                st.error(f"Terjadi kesalahan: {str(e)}")
