import pickle;
import streamlit as st;

model = pickle.load(open('prediksi_obesitas.sav', 'rb')) 


st.title('Prediksi Tingkat Obesitas')
usia = st.number_input('Masukkan Usia', min_value=0, max_value=150, step=1)
jenis_kelamin = st.selectbox('Pilih Jenis Kelamin', ('Laki-laki', 'Perempuan'))
tinggi_badan = st.number_input('Masukkan Tinggi Badan (1.50)', min_value=0.5, max_value=3.0, step=0.1)
berat_badan = st.number_input('Masukkan Berat Badan (45.0)', min_value=10.0, max_value=300.0, step=0.1)
konsumsi_kalori = st.selectbox('Masukkan Jumlah Konsumsi Kalori ', ('Tidak', 'Ya'))
riwayat_keluarga = st.selectbox('Riwayat Keluarga dengan Kegemukan?', ('Tidak', 'Ya'))
aktivitas_fisik = st.selectbox('Frekuensi Aktivitas Fisik ', ('Tidak Sering', 'Sering','Sangat Sering'))
waktu_teknologi = st.number_input('Waktu Penggunaan Teknologi (jam per hari)', min_value=0, max_value=24, step=1)
makanan_selingan = st.number_input('Frekuensi Konsumsi Makanan Selingan (per hari)', min_value=0, max_value=10, step=1)

predict = ''
jenis_kelamin = 1 if jenis_kelamin == 'Laki-laki' else 0
riwayat_keluarga = 1 if riwayat_keluarga == 'Ya' else 0
konsumsi_kalori = 1 if konsumsi_kalori == 'Ya' else 0
if aktivitas_fisik == 'Tidak Sering':
    aktivitas_fisik = 0
elif aktivitas_fisik == 'Sering':
    aktivitas_fisik = 1
else:  # Jika pilihan adalah 'Sangat Sering'
    aktivitas_fisik = 2
    
if st.button('Prediksi Tingkat Obesitas'):
    predict = model.predict(
        [[usia,
                jenis_kelamin,
                tinggi_badan,
                berat_badan,
                konsumsi_kalori,
                riwayat_keluarga,
                aktivitas_fisik,
                waktu_teknologi,
                makanan_selingan]]
    )
    st.write('Prediksi Tingkat Obesitas = ',predict)