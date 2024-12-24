import streamlit as st
from PIL import Image
import folium
from streamlit_folium import st_folium
import time
import requests
import pandas as pd


# Menambahkan CSS untuk mengubah background dan button
def add_custom_bg():
    st.markdown(
        """
        <style>
        body {
            background-color: #DCECE9; /* Warna hijau pastel */
        }
        .stApp {
            background-color: #DCECE9; /* Warna hijau pastel */
        }
        .stButton > button {
            background-color: #1F4529; /* Warna hijau gelap */
            color: white;
        }
        .stButton > button:hover {
            background-color: #ABBA7C; /* Warna hover hijau terang */
            color: white;
        }
        .stButton > button:active {
            color: #3C552D; /* Warna font ketika button diklik */
        }
        .stTextInput > div > input[type='password'] {
            background-color: white !important; /* Warna putih untuk input password */
            color: black;
        }
        .center-button {
            display: flex;
            justify-content: center;
        }
        .center-button > button {
            margin: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Memanggil fungsi untuk menambahkan background
add_custom_bg()


# Fungsi untuk mendapatkan koordinat lokasi menggunakan Google Maps API
def get_coordinates(location_name, api_key):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": location_name, "key": api_key}
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        results = response.json().get("results")
        if results:
            location = results[0]["geometry"]["location"]
            return location["lat"], location["lng"]
    return None, None

# Fungsi untuk menghitung jarak (Haversine formula)
def calculate_distance(lat1, lon1, lat2, lon2):
    from math import radians, cos, sin, sqrt, atan2
    R = 6371  # Radius bumi dalam kilometer
    
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    return R * c

# Fungsi untuk menghitung harga perjalanan
def calculate_fare(distance):
    if distance <= 1:
        return 3000
    elif distance <= 2:
        return 5000
    elif distance <= 3:
        return 7000
    elif distance <= 4:
        return 9000
    elif distance <= 5:
        return 10000
    elif distance <= 6:
        return 12000
    elif distance <= 7:
        return 14000
    elif distance <= 8:
        return 16000
    elif distance <= 9:
        return 18000
    elif distance <= 10:
        return 20000
    else:
        return 20000 + (distance - 5) * 5000

# Fungsi untuk mencari driver terdekat menggunakan linear search
def find_nearest_driver(user_lat, user_lon, drivers):
    nearest_driver = None
    min_distance = float('inf')
    for _, driver in drivers.iterrows():
        distance = calculate_distance(user_lat, user_lon, driver['Latitude'], driver['Longitude'])
        if distance < min_distance:
            min_distance = distance
            nearest_driver = driver
    return nearest_driver, min_distance

# Masukkan API Key Google Maps Anda di sini
GOOGLE_MAPS_API_KEY = "AIzaSyALLSRepqj68uMkUqxrGWU1X8hKzTo3afw"

# Load driver data with error handling
def load_driver_data():
    try:
        drivers_liwet = pd.read_csv('driver unesa lidah wetan.csv')
        drivers_ktt = pd.read_csv('driver unesa ketintang.csv')
        return pd.concat([drivers_liwet, drivers_ktt])
    except FileNotFoundError:
        st.error("File driver data tidak ditemukan. Harap unggah file yang diperlukan.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Terjadi kesalahan saat memuat data driver: {e}")
        return pd.DataFrame()

# Load drivers
all_drivers = load_driver_data()


# Fungsi untuk halaman login
def login():
    logo = Image.open('Logo NesaRide.png')

    col1, col2 = st.columns([2, 3])
    with col1:
        st.image(logo, use_container_width=True)

    with col2:
        st.markdown("# NESARIDE")
        st.markdown("Selamat datang! Silahkan Login terlebih dahulu.")

        username = st.text_input("Username", placeholder="Masukkan username anda")
        password = st.text_input("Password", placeholder="Masukkan password anda", type="password")

        if st.button("Masuk"):
            st.session_state.page = "home"  # Menyimpan status halaman

        if st.button("Buat Akun"):
            st.session_state.page = "sign_up"  # Menyimpan status halaman

# Fungsi untuk halaman sign up
def sign_up():
    logo = Image.open('Logo NesaRide.png')

    col1, col2 = st.columns([2, 3])
    with col1:
        st.image(logo, use_container_width=True)

    with col2:
        st.markdown("# NESARIDE")
        st.markdown("Mulai dengan gratis! Silahkan buat akun anda.")

        username = st.text_input("Username", placeholder="Masukkan username anda")
        nim = st.text_input("NIM", placeholder="Masukkan NIM anda")
        password = st.text_input("Password", placeholder="Masukkan password anda", type="password")

        terms = st.checkbox("Saya telah menyetujui Syarat dan ketentuan yang berlaku")

        if st.button("Buat Akun"):
            st.session_state.page = "login"  # Menyimpan status halaman

        if st.button("Sudah punya akun? Login"):
            st.session_state.page = "login"

# Fungsi halaman Home
def home():
    # Reset status konfirmasi selesai saat halaman home diakses
    st.session_state.konfirmasi_selesai = False

    image_path = 'gedung rektorat.png'  
    st.image(image_path, use_container_width=True)  

    st.markdown("<h1 style='text-align: center; color: black;'>Selamat datang Di <span style='color: #1F4529;'>NesaRide</span> website</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>NesaRide menyediakan layanan ojek online untuk mahasiswa Unesa dengan harga terjangkau, memudahkan pengguna dalam mengakses NesaRide untuk bepergian secara praktis.</p>", unsafe_allow_html=True)

    # Menempatkan tombol "Pesan" di tengah
    st.markdown("<div class='center-button'>", unsafe_allow_html=True)
    if st.button("Pesan", key="home_pesan_button"):
        st.session_state.page = "pesan"
        st.query_params = {"page": "pesan"}
    st.markdown("</div>", unsafe_allow_html=True)

# Fungsi halaman Pesan
def pesan():
    st.markdown("<h1 style='text-align: center; color: black;'>Set Lokasi</h1>", unsafe_allow_html=True)

    # Reset status konfirmasi selesai saat halaman pesan diakses
    st.session_state.konfirmasi_selesai = False

    # Form Input Lokasi
    titik_jemput = st.text_input("Titik Jemput", placeholder="Masukkan lokasi jemput")
    tujuan_pengantaran = st.text_input("Tujuan Pengantaran", placeholder="Masukkan lokasi tujuan")

    # Peta dengan Folium
    m = folium.Map(location=[-7.250445, 112.768845], zoom_start=12)

    user_lat, user_lon, tujuan_lat, tujuan_lon = None, None, None, None

    # Marker untuk titik jemput
    if titik_jemput:
        user_lat, user_lon = get_coordinates(titik_jemput, GOOGLE_MAPS_API_KEY)
        if user_lat and user_lon:
            folium.Marker(
                [user_lat, user_lon],
                popup="Titik Jemput",
                tooltip="Titik Jemput",
                icon=folium.Icon(color='blue', icon='circle', prefix='fa')
            ).add_to(m)

    # Marker untuk tujuan pengantaran
    if tujuan_pengantaran:
        tujuan_lat, tujuan_lon = get_coordinates(tujuan_pengantaran, GOOGLE_MAPS_API_KEY)
        if tujuan_lat and tujuan_lon:
            folium.Marker(
                [tujuan_lat, tujuan_lon],
                popup="Tujuan Pengantaran",
                tooltip="Tujuan Pengantaran",
                icon=folium.Icon(color='blue', icon='circle', prefix='fa')
            ).add_to(m)

    # Menampilkan driver di sekitar
    if user_lat and user_lon:
        for _, driver in all_drivers.iterrows():
            distance = calculate_distance(user_lat, user_lon, driver['Latitude'], driver['Longitude'])
            if distance <= 5:  # Menampilkan driver dalam radius 5 km dari titik jemput
                # Cek apakah driver ini sudah terhubung
                if st.session_state.get("connected_driver") == driver['Nama']:
                    # Marker khusus untuk driver yang sudah terhubung
                    folium.Marker(
                        [driver['Latitude'], driver['Longitude']],
                        popup=f"Driver Terhubung: {driver['Nama']} ({driver['Plat']})",
                        icon=folium.Icon(color='red', icon='motorcycle', prefix='fa')
                    ).add_to(m)
                else:
                    # Marker untuk driver lain
                    folium.Marker(
                        [driver['Latitude'], driver['Longitude']],
                        popup=f"Driver: {driver['Nama']} ({driver['Plat']})",
                        icon=folium.Icon(color='pink', icon='motorcycle', prefix='fa')
                    ).add_to(m)

    # Menampilkan peta
    st_folium(m, width=725)

    # Perhitungan biaya jika semua input valid
    if titik_jemput and tujuan_pengantaran and user_lat and user_lon and tujuan_lat and tujuan_lon:
        total_distance = calculate_distance(user_lat, user_lon, tujuan_lat, tujuan_lon)
        fare = calculate_fare(total_distance)

        # Simpan biaya perjalanan di session_state
        st.session_state.harga = fare  # Menyimpan biaya perjalanan

        st.markdown(f"<p style='font-size: 16px;'><b>Jarak perjalanan:</b> {total_distance:.2f} km</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 16px;'><b>Estimasi biaya perjalanan:</b> Rp {fare:,.0f}</p>", unsafe_allow_html=True)

        if st.button("Cari Driver"):
            with st.spinner("Mencari driver..."):
                time.sleep(3)  # Simulasi pencarian
                nearest_driver, distance_to_driver = find_nearest_driver(user_lat, user_lon, all_drivers)
                if nearest_driver is not None:
                    st.success(f"Driver ditemukan! {nearest_driver['Nama']} ({nearest_driver['Plat']}) akan segera menuju titik jemput.")
                    st.session_state.connected_driver = nearest_driver['Nama']  # Simpan driver yang terhubung
                else:
                    st.error("Tidak ada driver tersedia.")


    # Tombol untuk navigasi
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("Kembali ke Home"):
            st.session_state.page = "home"
    with col2:
        if st.button("Konfirmasi Pesanan"):
            st.session_state.page = "konfirmasi"  # Pindah ke halaman konfirmasi

# Fungsi halaman Konfirmasi
def konfirmasi():
    st.markdown("<h1 style='text-align: center; color: black;'>Konfirmasi Pesanan</h1>", unsafe_allow_html=True)

    # Menampilkan gambar uang dengan posisi tengah
    col1, col2, col3 = st.columns([1.5, 1, 1.5])  # Membuat kolom untuk posisi tengah
    with col2:
        uang_image = Image.open('tunai.png')
        st.image(uang_image, use_container_width=False, width=200)

    # Menampilkan informasi pembayaran
    st.markdown(
    "<h3 style='text-align: center; color: black; font-size: 18px;'>Pembayaran Tunai</h3>", 
    unsafe_allow_html=True)

    # Menampilkan harga yang telah dihitung dari session state
    harga = st.session_state.get("harga", 0)  # Harga diambil dari session_state
    st.markdown(
        f"<p style='text-align: center; font-size: 16px;'>Harga yang perlu dibayar: Rp {harga:,.0f}</p>",
        unsafe_allow_html=True
    )


    # Tombol untuk konfirmasi pembayaran
    if "konfirmasi_selesai" not in st.session_state:
        st.session_state.konfirmasi_selesai = False

    if not st.session_state.konfirmasi_selesai:
        if st.button("Konfirmasi Pembayaran"):
            st.session_state.konfirmasi_selesai = True

    if st.session_state.konfirmasi_selesai:
        st.success("Pesanan telah selesai.")
        # Menambahkan tombol OK
        if st.button("OK"):
            # Reset semua data pesanan
            st.session_state.pop("harga", None)  # Hapus data harga
            st.session_state.konfirmasi_selesai = False  # Reset status konfirmasi
            st.session_state.page = "home"  # Kembali ke halaman home


# Fungsi utama
def main():
    add_custom_bg() 
    if "page" not in st.session_state:
        st.session_state.page = "login"
    # Kontrol navigasi halaman
    if st.session_state.page == "pesan":
        pesan()  # Halaman pemesanan
    elif st.session_state.page == "home":
        home()  # Halaman utama
    elif st.session_state.page == "sign_up":
        sign_up()  # Halaman daftar akun
    elif st.session_state.page == "konfirmasi":
        konfirmasi()  # Halaman konfirmasi pesanan
    else:
        login()  # Halaman login


if __name__ == "__main__":
    main()
