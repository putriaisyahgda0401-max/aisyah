import streamlit as st
import json
import os

FILE_DB = "database_chatbot.json"

with open(FILE_DB, "r") as f:
    json.load(f)

st.set_page_config(page_title="App Streamlit")

def home_page() -> None:
    st.title("Aplikasi Informasi Sekolah")
    st.write("Selamat datang di aplikasi pembelajaran sederhana dengan Streamlit.")
    st.write("Gunakan menu di sidebar untuk membuka halaman Akademik, Fasilitas, dan Chatbot.")

st.sidebar.title("Menu Utama")
st.sidebar.caption("Pilih halaman yang ingin dibuka")

pages = [
    st.Page(home_page, title="Beranda", default=True),
    st.Page("pages/akademik.py", title="Informasi Akademik"),
    st.Page("pages/fasilitas.py", title="Fasilitas Kampus"),
    st.Page("pages/chatbot.py", title="Layanan Chatbot")
]

pg = st.navigation(pages)
pg.run()