import pickle
import numpy as np
import streamlit as st
import os
from PIL import Image
import base64

# Function to load background image
def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://img.freepik.com/free-vector/abstract-medical-wallpaper-template-design_53876-61802.jpg");
             background-attachment: fixed;
             background-size: cover;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

# Function to create custom CSS
def load_css():
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
            border-radius: 10px;
            background-color: rgba(255, 255, 255, 0.95);
        }
        .big-font {
            font-size: 24px !important;
            font-weight: bold;
        }
        .card {
            padding: 20px;
            border-radius: 10px;
            background-color: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .metric-card {
            background-color: #f0f2f6;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            margin: 10px 0;
        }
        .header-style {
            color: #2c3e50;
            font-weight: bold;
            text-align: center;
            margin-bottom: 30px;
        }
        .nav-button {
            width: 100%;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            background-color: #2c3e50;
            color: white;
            text-align: center;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .nav-button:hover {
            background-color: #34495e;
        }
        .stButton>button {
            width: 100%;
            background-color: #2c3e50;
            color: white;
            font-weight: bold;
            padding: 0.5rem 1rem;
            border-radius: 5px;
        }
        .stButton>button:hover {
            background-color: #34495e;
        }
        </style>
    """, unsafe_allow_html=True)

# Muat model yang telah disimpan
def load_model():
    try:
        return pickle.load(open('obesity_classifier.pkl', 'rb'))
    except Exception as e:
        return None

def main():
    add_bg_from_url()
    load_css()

    # Create session state for navigation
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 'Beranda'

    st.sidebar.image("https://img.freepik.com/free-vector/hospital-logo-design-vector-medical-cross_53876-136743.jpg", width=200)
    st.sidebar.title('Menu')
    page = st.sidebar.radio('Pilih Halaman:', ['Beranda', 'Prediksi Obesitas', 'Pencegahan Obesitas'])
    
    # Update session state
    st.session_state['current_page'] = page
    
    if st.session_state['current_page'] == 'Beranda':
        halaman_beranda()
    elif st.session_state['current_page'] == 'Prediksi Obesitas':
        halaman_prediksi()
    else:
        halaman_pencegahan()

def navigate_to(page):
    st.session_state['current_page'] = page
    st.experimental_rerun()

def halaman_beranda():
    st.markdown("<h1 class='header-style'>Selamat Datang di Sistem Prediksi Obesitas</h1>", unsafe_allow_html=True)
    
    # Content columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h2>🎯 Tentang Kami</h2>
            <p>Kami menyediakan platform modern untuk membantu Anda memahami dan mengelola risiko obesitas. 
            Dengan menggunakan machine learning, kami dapat memberikan prediksi akurat tentang tingkat obesitas berdasarkan berbagai faktor.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
            <h2>🌟 Fitur Utama</h2>
            <ul>
                <li>Prediksi tingkat obesitas berbasis AI</li>
                <li>Rekomendasi pencegahan personal</li>
                <li>Informasi kesehatan terkini</li>
                <li>Interface yang mudah digunakan</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <h2>📊 Statistik Obesitas</h2>
            <div class="metric-card">
                <h3>13%</h3>
                <p>Populasi Dewasa dengan Obesitas</p>
            </div>
            <div class="metric-card">
                <h3>5.4 Juta</h3>
                <p>Kasus Obesitas di Indonesia</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

def halaman_prediksi():
    st.markdown("<h1 class='header-style'>Prediksi Tingkat Obesitas</h1>", unsafe_allow_html=True)
    
    # Cek keberadaan model
    model = load_model()
    if model is None:
        st.error("Error: File model 'obesity_classifier.pkl' tidak ditemukan. Pastikan file model berada di folder yang sama dengan script ini.")
        st.info(f"Current working directory: {os.getcwd()}")
        return
    
    st.markdown("""
    <div class="card">
        <h3>📝 Silakan isi data berikut dengan lengkap</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        usia = st.number_input('Masukkan Usia', min_value=0, max_value=150, step=1)
        jenis_kelamin = st.selectbox('Pilih Jenis Kelamin', ('Laki-laki', 'Perempuan'))
        tinggi_badan = st.number_input('Masukkan Tinggi Badan (meter)', min_value=0.5, max_value=3.0, step=0.01)
        berat_badan = st.number_input('Masukkan Berat Badan (kg)', min_value=10.0, max_value=300.0, step=0.1)
    
    with col2:
        konsumsi_kalori = st.selectbox('Konsumsi Makanan Tinggi Kalori?', ('Tidak', 'Ya'))
        riwayat_keluarga = st.selectbox('Riwayat Keluarga Obesitas?', ('Tidak', 'Ya'))
        konsumsi_air_harian = st.selectbox('Konsumsi Air Harian', ['<2 liter', '<3 liter', '<4 liter'])
        konsumsi_makanan = st.selectbox(
            'Frekuensi Makanan Selingan',
            ['no', 'Sometimes', 'Frequently', 'Always']
        )

    # Konversi input
    konsumsi_air_harian_mapping = {'<2 liter': 0, '<3 liter': 1, '<4 liter': 2}
    konsumsi_makanan_mapping = {'no': 3, 'Sometimes': 2, 'Frequently': 1, 'Always': 0}

    jenis_kelamin = 1 if jenis_kelamin == 'Laki-laki' else 0
    riwayat_keluarga = 1 if riwayat_keluarga == 'Ya' else 0
    konsumsi_kalori = 1 if konsumsi_kalori == 'Ya' else 0
    konsumsi_air_harian = konsumsi_air_harian_mapping[konsumsi_air_harian]
    konsumsi_makanan_selingan = konsumsi_makanan_mapping[konsumsi_makanan]

    if st.button('Prediksi Tingkat Obesitas', key='predict_button'):
        try:
            input_data = np.array([[
                usia, jenis_kelamin, tinggi_badan, berat_badan,
                konsumsi_kalori, riwayat_keluarga, konsumsi_air_harian,
                konsumsi_makanan_selingan
            ]])

            prediction = model.predict(input_data)
            st.markdown(f"""
            <div class="card" style="background-color: #e3f2fd;">
                <h2 style="color: #1976d2; text-align: center;">Hasil Prediksi</h2>
                <p style="font-size: 20px; text-align: center;">{prediction[0]}</p>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error saat memprediksi: {str(e)}")

def halaman_pencegahan():
    st.markdown("<h1 class='header-style'>Cegah Obesitas, Hidup Sehat Lebih Baik!</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <h2>🎯 Kenapa Pencegahan Obesitas Penting?</h2>
        <p>Obesitas bukan sekadar masalah berat badan, tapi risiko serius bagi kesehatan. 
        Mari kita bersama-sama membangun gaya hidup sehat!</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h2 class='header-style'>6 Strategi Utama Mencegah Obesitas</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>🥗 Pola Makan Seimbang</h3>
            <p>Konsumsi makanan bergizi, kaya serat, dan protein. Batasi gula dan lemak berlebih.</p>
        </div>
        <div class="card">
            <h3>💧 Hidrasi Tepat</h3>
            <p>Minum air putih 8 gelas sehari. Hindari minuman manis dan berkarbonasi.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3>🏃‍♀️ Aktivitas Fisik</h3>
            <p>Olahraga minimal 150 menit per minggu. Pilih aktivitas yang menyenangkan!</p>
        </div>
        <div class="card">
            <h3>😴 Tidur Berkualitas</h3>
            <p>Tidur 7-9 jam per malam. Pola tidur yang baik membantu metabolisme.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card">
            <h3>🧘‍♀️ Manajemen Stres</h3>
            <p>Praktikkan meditasi, yoga, atau teknik relaksasi untuk mengkontrol emosi lebih baik.</p>
        </div>
        <div class="card">
            <h3>🍽️ Kontrol Porsi</h3>
            <p>Gunakan piring kecil, makan perlahan, dan batasi kekenyangan.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card" style="text-align: center; margin-top: 30px;">
        <h2>🌟 Perubahan Dimulai Hari Ini!</h2>
        <p>Setiap langkah kecil menuju gaya hidup sehat adalah kemenangan besar. 
        Mulailah sekarang, konsisten, dan lihat perubahan positif!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<p style='text-align: center; margin-top: 30px;'>Fadhilla dan Zikra Machine Learning | Cegah Obesitas</p>", unsafe_allow_html=True)

if __name__ == '__main__':
    main()