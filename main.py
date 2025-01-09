import pickle
import numpy as np
import streamlit as st
import os

# Muat model yang telah disimpan
def load_model():
    try:
        return pickle.load(open('obesity_classifier.pkl', 'rb'))
    except Exception as e:
        return None

def main():
    st.sidebar.title('Menu')
    page = st.sidebar.radio('Pilih Halaman:', ['Prediksi Obesitas', 'Pencegahan Obesitas'])
    
    if page == 'Prediksi Obesitas':
        halaman_prediksi()
    else:
        halaman_pencegahan()

def halaman_prediksi():
    st.title('Prediksi Tingkat Obesitas')
    
    # Cek keberadaan model
    model = load_model()
    if model is None:
        st.error("Error: File model 'obesity_classifier.pkl' tidak ditemukan. Pastikan file model berada di folder yang sama dengan script ini.")
        st.info(f"Current working directory: {os.getcwd()}")
        return
    
    # Form input pengguna
    usia = st.number_input('Masukkan Usia', min_value=0, max_value=150, step=1)
    jenis_kelamin = st.selectbox('Pilih Jenis Kelamin', ('Laki-laki', 'Perempuan'))
    tinggi_badan = st.number_input('Masukkan Tinggi Badan (contoh: 1.50 meter)', min_value=0.5, max_value=3.0, step=0.01)
    berat_badan = st.number_input('Masukkan Berat Badan (contoh: 45.0 kg)', min_value=10.0, max_value=300.0, step=0.1)
    konsumsi_kalori = st.selectbox('Apakah Anda Sering Mengonsumsi Makanan Tinggi Kalori?', ('Tidak', 'Ya'))
    riwayat_keluarga = st.selectbox('Apakah Ada Riwayat Keluarga dengan Kegemukan?', ('Tidak', 'Ya'))
    konsumsi_air_harian = st.selectbox('Konsumsi Air Harian', ['<2 liter', '<3 liter', '<4 liter'])
    konsumsi_makanan = st.selectbox(
        'Frekuensi Konsumsi Makanan di Antara Waktu Makan',
        ['no', 'Sometimes', 'Frequently', 'Always']
    )

    # Konversi input ke numerik
    konsumsi_air_harian_mapping = {'<2 liter': 0, '<3 liter': 1, '<4 liter': 2}
    konsumsi_makanan_mapping = {'no': 3, 'Sometimes': 2, 'Frequently': 1, 'Always': 0}

    jenis_kelamin = 1 if jenis_kelamin == 'Laki-laki' else 0
    riwayat_keluarga = 1 if riwayat_keluarga == 'Ya' else 0
    konsumsi_kalori = 1 if konsumsi_kalori == 'Ya' else 0
    konsumsi_air_harian = konsumsi_air_harian_mapping[konsumsi_air_harian]
    konsumsi_makanan_selingan = konsumsi_makanan_mapping[konsumsi_makanan]

    if st.button('Prediksi Tingkat Obesitas'):
        # Buat array input berdasarkan data pengguna
        try:
            input_data = np.array([[
                usia, jenis_kelamin, tinggi_badan, berat_badan,
                konsumsi_kalori, riwayat_keluarga, konsumsi_air_harian,
                konsumsi_makanan_selingan
            ]])

            prediction = model.predict(input_data)
            st.write('Prediksi Tingkat Obesitas: ', prediction[0])
        except Exception as e:
            st.error(f"Error saat memprediksi: {str(e)}")

def halaman_pencegahan():
    st.title('Cegah Obesitas, Hidup Sehat Lebih Baik!')
    st.header("Kenapa Pencegahan Obesitas Penting?")
    st.write("Obesitas bukan sekadar masalah berat badan, tapi risiko serius bagi kesehatan. Mari kita bersama-sama membangun gaya hidup sehat!")
    st.header("6 Strategi Utama Mencegah Obesitas")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 🥗 Pola Makan Seimbang")
        st.write("Konsumsi makanan bergizi, kaya serat, dan protein. Batasi gula dan lemak berlebih.")
        st.markdown("### 💧 Hidrasi Tepat")
        st.write("Minum air putih 8 gelas sehari. Hindari minuman manis dan berkarbonasi.")
    with col2:
        st.markdown("### 🏃‍♀️ Aktivitas Fisik")
        st.write("Olahraga minimal 150 menit per minggu. Pilih aktivitas yang menyenangkan!")
        st.markdown("### 😴 Tidur Berkualitas")
        st.write("Tidur 7-9 jam per malam. Pola tidur yang baik membantu metabolisme.")
    with col3:
        st.markdown("### 🧘‍♀️ Manajemen Stres")
        st.write("Praktikkan meditasi, yoga, atau teknik relaksasi untuk kontrol emosi.")
        st.markdown("### 🍽️ Kontrol Porsi")
        st.write("Gunakan piring kecil, makan perlahan, dan dengarkan sinyal kenyang tubuh.")
    st.header("Perubahan Dimulai Hari Ini!")
    st.write("Setiap langkah kecil menuju gaya hidup sehat adalah kemenangan besar. Mulailah sekarang, konsisten, dan lihat perubahan positif!")
    st.markdown("---")
    st.markdown("<p style='text-align: center;'>Fadhilla dan Zikra Machine Learning | Cegah Obesitas</p>", unsafe_allow_html=True)

if __name__ == '__main__':
    main()
