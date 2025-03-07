# Import library yang diperlukan
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Set style seaborn
sns.set(style='dark')

# Judul dashboard
st.title("Dashboard Analisis Kualitas Udara - Stasiun Wanshouxigong")

# Deskripsi dashboard
st.write("""
Dashboard ini menampilkan hasil analisis data kualitas udara dari stasiun Wanshouxigong (2013-2017).
Visualisasi mencakup tren PM2.5, pola musiman, dan hubungan antara PM2.5 dengan polutan lain.
""")

# Load dataset langsung dari URL
@st.cache_data  # Cache data untuk meningkatkan performa
def load_data():
    url = "https://github.com/marceloreis/HTI/raw/refs/heads/master/PRSA_Data_20130301-20170228/PRSA_Data_Wanshouxigong_20130301-20170228.csv"
    air_quality_df = pd.read_csv(url)
    air_quality_df['timestamp'] = pd.to_datetime(air_quality_df[['year', 'month', 'day', 'hour']])
    air_quality_df['month'] = air_quality_df['timestamp'].dt.month
    return air_quality_df

air_quality_df = load_data()

# Sidebar untuk filter tanggal
min_date = air_quality_df['timestamp'].min()
max_date = air_quality_df['timestamp'].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://th.bing.com/th/id/OIP.S-rb0E1Wd6Z0shn9CLxlRQHaHa?rs=1&pid=ImgDetMain")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data berdasarkan tanggal yang dipilih
main_df = air_quality_df[(air_quality_df['timestamp'] >= pd.to_datetime(start_date)) & 
                         (air_quality_df['timestamp'] <= pd.to_datetime(end_date))]

# Tampilkan dataset
if st.checkbox("Tampilkan Dataset"):
    st.write(main_df)

# Visualisasi 1: Tren PM2.5 dari Waktu ke Waktu
st.header("1. Tren PM2.5 dari Waktu ke Waktu")
st.write("Grafik ini menunjukkan tren konsentrasi PM2.5 dari tahun 2013 hingga 2017.")

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='timestamp', y='PM2.5', data=main_df, ax=ax)
ax.set_title('Tren PM2.5 di Stasiun Wanshouxigong', fontsize=20)
ax.set_xlabel('Tanggal', fontsize=15)
ax.set_ylabel('PM2.5 (µg/m³)', fontsize=15)
st.pyplot(fig)

# Visualisasi 2: Pola Musiman PM2.5
st.header("2. Pola Musiman PM2.5")
st.write("Grafik ini menunjukkan pola musiman dalam konsentrasi PM2.5.")

fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(x='month', y='PM2.5', data=main_df, ax=ax)
ax.set_title('Pola Musiman PM2.5 di Stasiun Wanshouxigong', fontsize=20)
ax.set_xlabel('Bulan', fontsize=15)
ax.set_ylabel('PM2.5 (µg/m³)', fontsize=15)
st.pyplot(fig)

# Visualisasi 3: Hubungan antara PM2.5 dengan Polutan Lain
st.header("3. Hubungan antara PM2.5 dengan Polutan Lain")
st.write("Grafik ini menunjukkan hubungan antara PM2.5 dengan polutan lain seperti NO2 dan CO.")

# Heatmap Korelasi
st.subheader("Heatmap Korelasi Antar Polutan")
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(main_df[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].corr(), annot=True, cmap='coolwarm', ax=ax)
ax.set_title('Heatmap Korelasi Antar Polutan di Stasiun Wanshouxigong', fontsize=20)
st.pyplot(fig)

# Scatter Plot PM2.5 vs NO2
st.subheader("Scatter Plot PM2.5 vs NO2")
fig, ax = plt.subplots(figsize=(8, 6))
sns.scatterplot(x='NO2', y='PM2.5', data=main_df, ax=ax)
ax.set_title('Hubungan antara PM2.5 dan NO2', fontsize=20)
ax.set_xlabel('NO2 (µg/m³)', fontsize=15)
ax.set_ylabel('PM2.5 (µg/m³)', fontsize=15)
st.pyplot(fig)

# Scatter Plot PM2.5 vs CO
st.subheader("Scatter Plot PM2.5 vs CO")
fig, ax = plt.subplots(figsize=(8, 6))
sns.scatterplot(x='CO', y='PM2.5', data=main_df, ax=ax)
ax.set_title('Hubungan antara PM2.5 dan CO', fontsize=20)
ax.set_xlabel('CO (µg/m³)', fontsize=15)
ax.set_ylabel('PM2.5 (µg/m³)', fontsize=15)
st.pyplot(fig)

# Kesimpulan
st.header("Kesimpulan")
st.write("""
- **Tren PM2.5:** Konsentrasi PM2.5 menunjukkan fluktuasi musiman dengan puncak pada bulan-bulan tertentu.
- **Pola Musiman:** Tingkat PM2.5 cenderung lebih tinggi pada bulan-bulan musim dingin.
- **Hubungan Antar Polutan:** PM2.5 memiliki korelasi positif dengan NO2 dan CO, menunjukkan bahwa sumber polusi PM2.5 mungkin berasal dari emisi kendaraan atau pembakaran bahan bakar fosil.
""")

# Footer
st.caption('MC006D5Y2425 LESNAR TAMBUN')