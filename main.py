import pickle
import numpy as np
import streamlit as st

# Muat model yang telah disimpan dengan Pickle
try:
    model = pickle.load(open('obesity_classifier.pkl', 'rb'))
except Exception as e:
    st.error(f"Error saat memuat model: {str(e)}")
    st.stop()

# Judul aplikasi
st.title('Prediksi Tingkat Obesitas')

# Input dari pengguna
usia = st.number_input('Masukkan Usia', min_value=0, max_value=150, step=1)
jenis_kelamin = st.selectbox('Pilih Jenis Kelamin', ('Laki-laki', 'Perempuan'))
tinggi_badan = st.number_input('Masukkan Tinggi Badan (contoh: 1.50 meter)', min_value=0.5, max_value=3.0, step=0.01)
berat_badan = st.number_input('Masukkan Berat Badan (contoh: 45.0 kg)', min_value=10.0, max_value=300.0, step=0.1)
konsumsi_kalori = st.selectbox('Apakah Anda Sering Mengonsumsi Makanan Tinggi Kalori?', ('Tidak', 'Ya'))
riwayat_keluarga = st.selectbox('Apakah Ada Riwayat Keluarga dengan Kegemukan?', ('Tidak', 'Ya'))

# Mapping untuk Konsumsi Air Harian
konsumsi_air_harian = st.selectbox('Konsumsi Air Harian', ['<2 liter', '<3 liter', '<4 liter'])
konsumsi_air_harian_mapping = {'<2 liter': 0, '<3 liter': 1, '<4 liter': 2}
konsumsi_air_harian = konsumsi_air_harian_mapping[konsumsi_air_harian]

# Mapping untuk Konsumsi Makanan di Antara Waktu Makan
konsumsi_makanan = st.selectbox(
    'Frekuensi Konsumsi Makanan di Antara Waktu Makan',
    ['no', 'Sometimes', 'Frequently', 'Always']
)
konsumsi_makanan_mapping = {'no': 3, 'Sometimes': 2, 'Frequently': 1, 'Always': 0}
konsumsi_makanan_selingan = konsumsi_makanan_mapping[konsumsi_makanan]

# Konversi jenis kelamin dan riwayat keluarga ke nilai numerik
jenis_kelamin = 1 if jenis_kelamin == 'Laki-laki' else 0
riwayat_keluarga = 1 if riwayat_keluarga == 'Ya' else 0
konsumsi_kalori = 1 if konsumsi_kalori == 'Ya' else 0

# Prediksi
if st.button('Prediksi Tingkat Obesitas'):
    # Buat array input berdasarkan data pengguna
    try:
        input_data = np.array([[
            usia, jenis_kelamin, tinggi_badan, berat_badan,
            konsumsi_kalori, riwayat_keluarga, konsumsi_air_harian,
            konsumsi_makanan_selingan
        ]])
    except Exception as e:
        st.error(f"Error pada input data: {str(e)}")
        st.stop()

    # Validasi jumlah fitur input
    required_features = 8
    if input_data.shape[1] != required_features:
        st.error(f'Jumlah fitur input tidak sesuai. Model membutuhkan {required_features} fitur.')
        st.stop()

    # Gunakan model untuk membuat prediksi
    try:
        prediction = model.predict(input_data)
        st.write('Prediksi Tingkat Obesitas: ', prediction[0])
    except Exception as e:
        st.error(f'Error saat memprediksi: {str(e)}')
