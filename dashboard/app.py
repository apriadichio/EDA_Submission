import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
@st.cache_data
def load_data():
    # Membaca dataset
    df = pd.read_csv('day_cleaned.csv')  
    
    # Konversi tipe data
    dtype_mapping = {
        "season": "category",
        "yr": "category",
        "mnth": "category",
        "holiday": "category",
        "weekday": "category",
        "workingday": "category",
        "weathersit": "category",
    }
    df = df.astype(dtype_mapping)
    df['dteday'] = pd.to_datetime(df['dteday'])
    
    return df

df = load_data()

with st.sidebar:
    st.title("Marchio Apriadi")
    st.image("https://streamlit.io/images/brand/streamlit-mark-color.png")

st.title('Analisa Penyewaan Sepeda')

# 1. Visualisasi Tren Peminjaman Sepeda (Casual vs Registered)
st.write("### Trend Peminjaman Sepeda: Casual vs Registered")

total_registered = df['registered'].sum()
total_casual = df['casual'].sum()

df['casual_smooth'] = df['casual'].rolling(window=7).mean()
df['registered_smooth'] = df['registered'].rolling(window=7).mean()

chart_type = st.selectbox("Pilih hasil yang ingin ditampilkan", ("Trend", "Proporsi"))

def display_chart(chart_type):
    if chart_type == 'Trend':
        # Line chart untuk tren peminjaman
        plt.figure(figsize=(12, 6))
        plt.plot(df['dteday'], df['casual_smooth'], label="Casual Users", color='lightblue', linewidth=2)
        plt.plot(df['dteday'], df['registered_smooth'], label="Registered Users", color='blue', linewidth=2)
        plt.title("Tren Peminjaman Sepeda: Casual vs Registered", fontsize=14)
        plt.xlabel("Tanggal", fontsize=12)
        plt.ylabel("Jumlah Peminjaman", fontsize=12)
        plt.legend()
        plt.grid(True, linestyle="--", alpha=0.5)
        st.pyplot(plt.gcf())
    elif chart_type == 'Proporsi':
        # Pie chart untuk proporsi total peminjaman
        st.write("### Proporsi Total Peminjaman Sepeda")
        plt.figure(figsize=(6, 6))
        plt.pie([df['casual'].sum(), df['registered'].sum()], labels=['Casual', 'Registered'], autopct='%1.1f%%', colors=['lightblue', 'royalblue'])
        plt.title('Proporsi Total Peminjaman Sepeda')
        st.pyplot(plt.gcf())

display_chart(chart_type)

col1, col2 = st.columns(2)
with col1:
    st.write(f"**Total Pengguna Registered:** {total_registered}")
with col2:
    st.write(f"**Total Pengguna Casual:** {total_casual}") 

st.write("""
    Pengguna registered sangatlah mendominasi total peminjaman sepeda selama 2 tahun (2011-2013) 
    dimana pengguna registered memilik proporsi sekitar 81.2% dibanding dengan casual yang hanya 18.2%. 
    Namun dapat dilihat bahwa keduanya memili trend yang serupa dimana terdapat penurunan jumlah penyewaan 
    pada bulan ke 10 sampai ke bulan 1 (tahun selanjutnya) dan setelahnya jumlah penyewaan berlangsung meningkat 
    dengan pola yang nampaknya terulang kembali.
""")
st.markdown("---")

# 2. Visualisasi Rata-rata Penyewaan Sepeda Berdasarkan Musim
st.write("### Rata-rata Penyewaan Sepeda Berdasarkan Musim")

season_avg = df.groupby('season', observed=False)['cnt'].mean().reset_index()
season_labels = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
season_avg['season_label'] = season_avg['season'].map(season_labels)
base_color = 'royalblue'
fade_color = 'lightblue'
max_value = season_avg['cnt'].max()

plt.figure(figsize=(8, 5))
ax = sns.barplot(x='season_label', y='cnt', data=season_avg, color=fade_color)

for p, value in zip(ax.patches, season_avg['cnt']):
    if value == max_value:
        p.set_color(base_color)

    ax.annotate(f"{value:.0f}",
                (p.get_x() + p.get_width() / 2, p.get_height()),
                ha='center', va='bottom', fontsize=12, fontweight='bold', color='black')

plt.title("Rata-rata Penyewaan Sepeda Berdasarkan Musim", fontsize=14)
plt.xlabel("Musim", fontsize=12)
plt.ylabel("Jumlah Peminjaman", fontsize=12)
st.pyplot(plt.gcf())

st.write("""
    Musim-musim tertentu memiliki pengaruh yang berbeda-beda terhadap total penyewaan. 
    Dimana summer dan fall menjadi penyumbang terbesar untuk jumlah penyewaan dan disusul oleh winter. 
    Sementara Spring menjadi penyumbang terkecil terhadap jumlah penyewaan sepeda.
""")
st.markdown("---")

# 3. Visualisasi Rata-rata Penyewaan Sepeda Berdasarkan Cuaca
st.write("### Rata-rata Penyewaan Sepeda Berdasarkan Cuaca")

all_weather = pd.DataFrame({
    'weathersit': [1, 2, 3, 4],
    'weather_description': ['Clear', 'Misty', 'Light Snow/Rain', 'Heavy Rain/Snow']
})

weather_avg = df.groupby('weathersit', observed=False)['cnt'].mean().reset_index()
weather_avg = pd.merge(all_weather, weather_avg, on='weathersit', how='left')
weather_avg['cnt'] = weather_avg['cnt'].astype(float).fillna(0)

weather_labels = {1: 'Clear', 2: 'Misty', 3: 'Light Snow/Rain', 4: 'Heavy Rain/Snow'}
weather_avg['weathersit_label'] = weather_avg['weathersit'].map(weather_labels)

base_color = 'royalblue'
fade_color = 'lightblue'

max_value = weather_avg['cnt'].max()

plt.figure(figsize=(8, 5))
ax = sns.barplot(x='weathersit_label', y='cnt', data=weather_avg, color=fade_color)

for p, value in zip(ax.patches, weather_avg['cnt']):
    if value == max_value:
        p.set_color(base_color)

    ax.annotate(f"{value:.0f}",
                (p.get_x() + p.get_width() / 2, p.get_height()),
                ha='center', va='bottom', fontsize=12, fontweight='bold', color='black')

plt.title("Rata-rata Peminjaman Sepeda Berdasarkan Cuaca", fontsize=14)
plt.xlabel("Kondisi Cuaca", fontsize=12)
plt.ylabel("Rata-rata Jumlah Peminjaman", fontsize=12)

st.pyplot(plt.gcf())

st.write("""
    Cuaca sangat berpengaruh terhadap penyewaan sepeda, 
    dimana cuaca cerah tampak sangatlah diminati oleh pengguna untuk melakukan penyewaan sepeda. 
    Sementara itu, cuaca yang tidak mendukung seperti hujan dan salju sangatlah tidak diminati dan bahkan pada cucaca extreme 
    (hujan lebat/badai salju) tidak ada pengguna yang melakukan penyewaan.
""")
st.markdown("---")

# 4. Visualisasi Hubungan Suhu dengan Penyewaan Sepeda
st.write("### Hubungan Suhu dengan Penyewaan Sepeda")

plt.figure(figsize=(8, 5))
sns.scatterplot(x="temp", y="cnt", data=df, alpha=0.5)
plt.title("Hubungan Suhu dengan Penyewaan Sepeda", fontsize=14)
plt.xlabel("Suhu Normalisasi", fontsize=12)
plt.ylabel("Jumlah Peminjaman", fontsize=12)
st.pyplot(plt.gcf())

max_rentals = df.loc[df['cnt'].idxmax()]  
max_rentals_temp = max_rentals['temp']  
max_rentals_count = max_rentals['cnt']  


st.write(f"**Penyewaan Sepeda Terbanyak terjadi pada suhu:** {max_rentals_temp:.2f} (normalisasi)")
st.write(f"**Jumlah Peminjaman pada Suhu Tersebut:** {max_rentals_count} penyewaan")

st.write("""
    suhu sangat berpengaruh pada penyewaan, suhu yang lebih tinggi memiliki jumlah penyewaan seped yang relatif lebih tinggi pula, 
    selain itu ditemukan ada sekitar 8000 jumlah peminjaman pada suhu dengan normalisasi sekitar 0.6 (24.6°C)
""")

# Footer
st.markdown("---")
st.write("Dibuat oleh Marchio Apriadi")
