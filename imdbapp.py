import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import squarify  # Library untuk membuat treemap

# Load data
@st.cache
def load_data():
    data = pd.read_csv("imdb_top_250_cleaned.csv")
    return data

# Load data
data = load_data()

# Judul aplikasi
st.markdown(f"""
        <div style="display: flex; justify-content: center;">
            <img src="{"https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/IMDB_Logo_2016.svg/1150px-IMDB_Logo_2016.svg.png"}" width="200">
        </div>
    """, unsafe_allow_html=True)

# Menambahkan CSS untuk memusatkan judul
st.markdown("""
    <style>
    .centered-title {
        text-align: center;
        font-size: 36px;
    }
    </style>
""", unsafe_allow_html=True)

# Judul aplikasi yang dipusatkan
st.markdown('<h1 class="centered-title">IMDB TOP 250 Movies</h1>', unsafe_allow_html=True)

# Top 10 Film berdasarkan IMDb Rating
st.header('Top 10 Film dengan IMDb Rating Tertinggi')
top_10_movies = data.sort_values(by='IMDb Rating', ascending=False).head(10)
plt.figure(figsize=(12, 8))
plt.barh(top_10_movies['Title'], top_10_movies['IMDb Rating'], color='chocolate')
plt.xlabel('IMDb Rating')
plt.title('Top 10 Film dengan IMDb Rating Tertinggi')
plt.gca().invert_yaxis()
st.pyplot(plt)
st.write("Grafik ini menampilkan 10 film dengan rating IMDb tertinggi dalam data. Film-film ini memiliki rating yang sangat tinggi, menunjukkan bahwa mereka sangat dihargai oleh penonton dan kritikus.")

# Rata-rata IMDb Rating berdasarkan Sound Mix
st.header('Rata-rata IMDb Rating berdasarkan Sound Mix')
rating_by_sound_mix = data.groupby('Sound mix')['IMDb Rating'].mean().sort_values(ascending=False)
plt.figure(figsize=(12, 8))
rating_by_sound_mix.plot(kind='bar', color='darkgoldenrod')
plt.title('Rata-rata IMDb Rating berdasarkan Sound Mix')
plt.xlabel('Sound Mix')
plt.ylabel('Rata-rata IMDb Rating')
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(plt)
st.write("Grafik ini menunjukkan rata-rata rating IMDb untuk berbagai jenis sound mix yang digunakan dalam film. Ini bisa memberikan wawasan tentang bagaimana kualitas audio bisa mempengaruhi penilaian film.")

# Keuntungan Bersih 5 Film dengan Budget Tertinggi
st.header('Keuntungan Bersih 5 Film dengan Budget Tertinggi (dalam juta USD)')
data['Gross Profit'] = data['Gross Worldwide'] - data['Budget']
top_budget_films = data.nlargest(5, 'Budget')
plt.figure(figsize=(10, 6))
plt.bar(top_budget_films['Title'], top_budget_films['Gross Profit'] / 1e6, color='sandybrown')
plt.title('Keuntungan Bersih 5 Film dengan Budget Tertinggi (dalam juta USD)')
plt.xlabel('Judul Film')
plt.ylabel('Keuntungan Bersih (Juta USD)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
st.pyplot(plt)
st.write("Grafik ini menunjukkan keuntungan bersih (dalam juta USD) dari 5 film dengan anggaran tertinggi. Ini menunjukkan bagaimana film-film dengan anggaran besar dapat menghasilkan keuntungan yang signifikan.")

# Komposisi Warna Film
st.header('Komposisi Warna Film')
color_counts = data['Color'].value_counts()
colors = ['orange', 'lightslategrey']
plt.figure(figsize=(8, 8))
plt.pie(color_counts, labels=color_counts.index, autopct='%1.1f%%', startangle=140, colors=colors)
plt.axis('equal')
st.pyplot(plt)
st.write("Pie chart ini menunjukkan komposisi warna film dalam data. Sebagian besar film berwarna, dengan persentase kecil dari film yang berwarna hitam-putih.")

# Komposisi Klasifikasi Film
st.header('Komposisi Klasifikasi Film')
classification_counts = data['Classifications'].value_counts()
colors = ['gold', 'sandybrown', 'lightyellow', 'rosybrown', 'darkorange', 'tan', 'darkkhaki', 'goldenrod']
plt.figure(figsize=(8, 8))
plt.pie(classification_counts, labels=classification_counts.index, autopct='%1.1f%%', startangle=140, pctdistance=0.85, colors=colors)
plt.pie([1], radius=0.6, colors='white')
plt.title('Komposisi Klasifikasi Film')
plt.axis('equal')
st.pyplot(plt)
st.write("Pie chart ini menunjukkan distribusi klasifikasi film dalam data. Klasifikasi film dapat memberikan wawasan tentang audiens target dari film-film tersebut.")

# Treemap Komposisi Jenis Sound Mix dalam Film
st.header('Treemap Komposisi Jenis Sound Mix dalam Film')
sound_mix_counts = data['Sound mix'].value_counts()
colors = ['darkorange', 'tan', 'darkkhaki', 'sienna', 'wheat', 'goldenrod', 'gold', 'sandybrown', 'lightyellow', 'rosybrown']
plt.figure(figsize=(10, 8))
squarify.plot(sizes=sound_mix_counts.values, label=sound_mix_counts.index, alpha=0.8, text_kwargs={'fontsize': 7, 'fontweight': 'bold'}, color=colors)
plt.title('Treemap Komposisi Jenis Sound Mix dalam Film')
plt.axis('off')
st.pyplot(plt)
st.write("Treemap ini menunjukkan distribusi jenis sound mix yang digunakan dalam film. Ukuran setiap kotak sebanding dengan jumlah film yang menggunakan jenis sound mix tersebut.")

# Distribusi Runtime Film
st.header('Distribusi Runtime Film (dalam Menit)')
def convert_runtime_to_minutes(runtime_str):
    if pd.isna(runtime_str):
        return None
    total_minutes = 0
    parts = runtime_str.split()
    i = 0
    while i < len(parts):
        if parts[i].isdigit():
            if i + 1 < len(parts) and parts[i + 1].startswith('hour'):
                total_minutes += int(parts[i]) * 60
                i += 1
            elif i + 1 < len(parts) and parts[i + 1].startswith('minute'):
                total_minutes += int(parts[i])
                i += 1
            else:
                total_minutes += int(parts[i])
        i += 1
    return total_minutes

df = pd.DataFrame(data)
df['Runtime (minutes)'] = df['Runtime'].apply(convert_runtime_to_minutes)
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
sns.histplot(df['Runtime (minutes)'], kde=True, color='brown')
plt.title('Distribusi Runtime Film (dalam Menit)')
plt.xlabel('Runtime (menit)')
plt.ylabel('Frekuensi')
plt.grid(False)
plt.xticks(ticks=plt.xticks()[0], labels=[f'{int(tick)}' for tick in plt.xticks()[0]])
st.pyplot(plt)
st.write("Histogram ini menunjukkan distribusi durasi film dalam menit. Kebanyakan film memiliki durasi antara 100 hingga 150 menit.")

# Distribusi IMDb Ratings
st.header('Distribusi IMDb Ratings')
plt.figure(figsize=(10, 6))
sns.histplot(data['IMDb Rating'], bins=20, kde=True, color='darkkhaki')
plt.title('Distribusi IMDb Ratings')
plt.xlabel('IMDb Rating')
plt.ylabel('Frekuensi')
plt.grid(False)
st.pyplot(plt)
st.write("Histogram ini menunjukkan distribusi rating IMDb dari film-film dalam data. Rating IMDb berkisar dari 8 hingga hampir 10, menunjukkan bahwa semua film dalam data ini sangat dihargai.")

# Hubungan Budget dan Pendapatan Kotor Global
st.header('Hubungan Budget dan Pendapatan Kotor Global')
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Budget', y='Gross Worldwide', data=data, color='gold')
plt.title('Hubungan antara Budget dan Pendapatan Kotor Global')
plt.xlabel('Budget')
plt.ylabel('Pendapatan Kotor Global')
plt.grid(True)
st.pyplot(plt)
st.write("Scatter plot ini menunjukkan hubungan antara budget film dan pendapatan kotor global. Secara umum, film dengan budget lebih tinggi cenderung menghasilkan pendapatan kotor yang lebih besar.")

# Scatter Plot Tahun Rilis dan IMDb Rating
st.header('Scatter Plot Tahun Rilis dan IMDb Rating Film')
data = data[['IMDb Rating', 'Opening Weekend Date']].dropna()
data['Opening Weekend Date'] = pd.to_datetime(data['Opening Weekend Date'], errors='coerce')
data['Year'] = data['Opening Weekend Date'].dt.year
data = data.dropna(subset=['Year'])
plt.figure(figsize=(12, 8))
plt.scatter(data['Year'], data['IMDb Rating'], alpha=0.5, color='orange')
plt.title('Scatter Plot Tahun Rilis dan IMDb Rating Film')
plt.xlabel('Tahun Rilis')
plt.ylabel('IMDb Rating')
plt.grid(True)
st.pyplot(plt)
st.write("Scatter plot ini menunjukkan hubungan antara tahun rilis film dan rating IMDb. Ini bisa memberikan wawasan tentang bagaimana persepsi penonton terhadap film mungkin telah berubah selama bertahun-tahun.")

st.caption('© 21082010090 - Annisa
