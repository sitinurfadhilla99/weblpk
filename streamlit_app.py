import streamlit as st
import pandas as pd
import time

# =========================================
# SESSION STATE
# =========================================

if "rumus" not in st.session_state:
    st.session_state.rumus = ""

if "golongan" not in st.session_state:
    st.session_state.golongan = ""

# =========================================
# KONFIGURASI HALAMAN
# =========================================

st.set_page_config(
    page_title="Laboratorium Virtual Kimia Organik",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 Laboratorium Virtual Kimia Organik")

# =========================================
# INPUT STRUKTUR
# =========================================

st.header("🔬 Penyusun Struktur Senyawa")

jumlah_c = st.number_input(
    "Jumlah karbon utama",
    min_value=1,
    max_value=20,
    value=3
)

opsi_gugus = [

    # Alkana
    "CH3",
    "CH2",
    "CH",
    "C",

    # Alkohol
    "CH2(OH)",
    "CH(OH)",
    "C(OH)",

    # Aldehid
    "CHO",

    # Keton
    "CO",

    # Asam karboksilat
    "COOH",

    # Amina
    "CH2(NH2)",
    "CH(NH2)",
    "C(NH2)",
    "NH",
    "N",

    # Alkena
    "CH=CH2",
    "CH=CH",
    "C=C",

    # Fenol
    "C6H5OH"
]

opsi_cabang = [
    "Tidak ada",
    "Metil",
    "Dimetil",
    "Trimetil",
    "Tetrametil",
    "Etil",
    "Dietil",
    "Trietil",
    "Isopropil"
]

cabang_map = {
    "Tidak ada": "",
    "Metil": "(CH3)",
    "Dimetil": "(CH3)2",
    "Trimetil": "(CH3)3",
    "Tetrametil": "(CH3)4",
    "Etil": "(C2H5)",
    "Dietil": "(C2H5)2",
    "Trietil": "(C2H5)3",
    "Isopropil": "(CH(CH3)2)"
}

rantai = []

for i in range(jumlah_c):

    st.subheader(f"Karbon {i+1}")

    col1, col2 = st.columns(2)

    with col1:

        gugus = st.selectbox(
            f"Gugus C-{i+1}",
            opsi_gugus,
            key=f"g{i}"
        )

    with col2:

        cabang = st.selectbox(
            f"Cabang C-{i+1}",
            opsi_cabang,
            key=f"c{i}"
        )

    struktur = gugus + cabang_map[cabang]

    rantai.append(struktur)

# =========================================
# MEMBUAT SENYAWA
# =========================================

if st.button("🧪 Buat Senyawa"):

    rumus = "-".join(rantai)

    st.session_state.rumus = rumus

    # =====================================
    # IDENTIFIKASI GOLONGAN
    # =====================================

    if "COOH" in rumus:

        golongan = "Asam Karboksilat"

    elif "CHO" in rumus:

        golongan = "Aldehid"

    elif "CO" in rumus:

        golongan = "Keton"

    elif "NH2" in rumus or "NH" in rumus:

        golongan = "Amina"

    elif "=" in rumus:

        golongan = "Alkena"

    elif "OH" in rumus:

        if "CH2(OH)" in rumus:

            golongan = "Alkohol Primer"

        elif "CH(OH)" in rumus:

            golongan = "Alkohol Sekunder"

        elif "C(OH)" in rumus:

            golongan = "Alkohol Tersier"

        else:

            golongan = "Alkohol"

    elif "C6H5OH" in rumus:

        golongan = "Fenol"

    else:

        golongan = "Hidrokarbon"

    st.session_state.golongan = golongan

# =========================================
# TAMPILKAN SENYAWA
# =========================================

if st.session_state.rumus != "":

    rumus = st.session_state.rumus
    golongan = st.session_state.golongan

    st.header("📌 Struktur Senyawa")

    st.code(rumus)

    st.header("📊 Informasi Senyawa")

    data = pd.DataFrame({
        "Parameter": [
            "Rumus Struktur",
            "Golongan"
        ],
        "Hasil": [
            rumus,
            golongan
        ]
    })

    st.table(data)

    st.success(
        f"Senyawa termasuk {golongan}"
    )

    # =====================================
    # PILIH UJI
    # =====================================

    st.header("⚗️ Simulasi Praktikum")

    opsi_uji = [

        "Lucas",
        "CrO3",
        "Asam Kromat",
        "Natrium",
        "Esterifikasi",
        "Tollens",
        "Fehling",
        "Benedict",
        "Schiff",
        "Iodoform",
        "2,4-DNP",
        "NaHCO3",
        "Lakmus",
        "Bromin",
        "KMnO4",
        "FeCl3",
        "Hinsberg",
        "Karbilamina"
    ]

    uji = st.selectbox(
        "Pilih uji",
        opsi_uji
    )

    perlakuan = st.radio(
        "Perlakuan",
        [
            "Dikocok",
            "Dipanaskan"
        ]
    )

    # =====================================
    # JALANKAN UJI
    # =====================================

    if st.button("▶️ Jalankan Uji"):

        st.subheader("🧪 Tahapan Praktikum")

        st.write("1️⃣ Memasukkan sampel...")
        time.sleep(1)

        st.info(rumus)

        st.write("2️⃣ Menambahkan pereaksi...")
        time.sleep(1)

        st.warning(uji)

        st.write(f"3️⃣ {perlakuan}...")

        progress = st.progress(0)

        for i in range(100):

            time.sleep(0.02)

            progress.progress(i + 1)

        # =================================
        # HASIL UJI
        # =================================

        hasil = "Tidak ada perubahan"

        if uji == "Lucas":

            if "Primer" in golongan:

                hasil = "Larutan tetap bening"

            elif "Sekunder" in golongan:

                hasil = "Larutan agak keruh"

            elif "Tersier" in golongan:

                hasil = "Larutan cepat keruh"

        elif uji == "Tollens":

            if golongan == "Aldehid":

                hasil = "Terbentuk cermin perak"

        elif uji == "Bromin":

            if "=" in rumus:

                hasil = "Warna bromin hilang"

        elif uji == "NaHCO3":

            if golongan == "Asam Karboksilat":

                hasil = "Muncul gelembung CO2"

        elif uji == "FeCl3":

            if "C6H5OH" in rumus:

                hasil = "Larutan ungu"

        elif uji == "Karbilamina":

            if "NH2" in rumus:

                hasil = "Bau menyengat"

        st.header("🔬 Hasil Pengamatan")

        st.info(hasil)

        # =================================
        # PERSAMAAN REAKSI
        # =================================

        st.header("🧾 Persamaan Reaksi")

        reaksi = "Tidak ada reaksi"

        if uji == "Lucas":

            if "OH" in rumus:

                produk = rumus.replace(
                    "OH",
                    "Cl"
                )

                reaksi = (
                    f"{rumus} + HCl "
                    f"→ {produk} + H2O"
                )

        elif uji == "Tollens":

            if golongan == "Aldehid":

                reaksi = (
                    "RCHO + Ag2O "
                    "→ RCOOH + Ag"
                )

        elif uji == "Bromin":

            if "=" in rumus:

                reaksi = (
                    "RCH=CHR + Br2 "
                    "→ RCHBr-CHBrR"
                )

        elif uji == "NaHCO3":

            if golongan == "Asam Karboksilat":

                reaksi = (
                    "RCOOH + NaHCO3 "
                    "→ RCOONa + CO2 + H2O"
                )

        elif uji == "FeCl3":

            if "C6H5OH" in rumus:

                reaksi = (
                    "Fenol + FeCl3 "
                    "→ kompleks ungu"
                )

        elif uji == "Karbilamina":

            if "NH2" in rumus:

                reaksi = (
                    "RNH2 + CHCl3 + KOH "
                    "→ RNC"
                )

        st.code(reaksi)

        # =================================
        # KESIMPULAN
        # =================================

        st.header("📖 Kesimpulan")

        st.write(
            f"Sampel {rumus} "
            f"teridentifikasi sebagai "
            f"{golongan}."
        )

        st.write(
            f"Hasil uji {uji}: {hasil}"
        )

# =========================================
# FOOTER
# =========================================

st.markdown("---")

st.caption(
    "🧪 Laboratorium Virtual Kimia Organik"
)
