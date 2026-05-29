import streamlit as st
import pandas as pd
import time

# =========================================
# KONFIGURASI HALAMAN
# =========================================

st.set_page_config(
    page_title="Laboratorium Virtual Kimia Organik",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 Laboratorium Virtual Kimia Organik")

st.write(
    "Simulasi identifikasi senyawa organik "
    "dan praktikum virtual interaktif."
)

# =========================================
# INPUT STRUKTUR SENYAWA
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

    st.header("📌 Struktur Senyawa")

    st.code(rumus)

    # =========================================
    # IDENTIFIKASI GOLONGAN
    # =========================================

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

    # =========================================
    # TABEL INFORMASI
    # =========================================

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

    st.success(f"Senyawa termasuk {golongan}")

    # =========================================
    # PILIH UJI
    # =========================================

    st.header("⚗️ Simulasi Praktikum")

    opsi_uji = [

        # Alkohol
        "Lucas",
        "CrO3",
        "Asam Kromat",
        "Natrium",
        "Esterifikasi",

        # Aldehid
        "Tollens",
        "Fehling",
        "Benedict",
        "Schiff",

        # Keton
        "Iodoform",
        "2,4-DNP",

        # Asam karboksilat
        "NaHCO3",
        "Lakmus",

        # Alkena
        "Bromin",
        "KMnO4",

        # Fenol
        "FeCl3",

        # Amina
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

        # =========================================
        # HASIL UJI
        # =========================================

        st.header("🔬 Hasil Pengamatan")

        hasil = "Tidak ada perubahan"

        # =====================================
        # UJI ALKOHOL
        # =====================================

        if uji == "Lucas":

            if "Primer" in golongan:

                hasil = "Larutan tetap bening"

            elif "Sekunder" in golongan:

                hasil = "Larutan agak keruh"

            elif "Tersier" in golongan:

                hasil = "Larutan cepat keruh"

        elif uji == "CrO3":

            if "Primer" in golongan:

                hasil = (
                    "Warna oranye berubah hijau "
                    "dan terbentuk asam karboksilat"
                )

            elif "Sekunder" in golongan:

                hasil = (
                    "Warna berubah hijau "
                    "dan terbentuk keton"
                )

            elif "Tersier" in golongan:

                hasil = "Tidak bereaksi"

        elif uji == "Asam Kromat":

            if "OH" in rumus:

                hasil = (
                    "Warna oranye berubah hijau"
                )

        elif uji == "Natrium":

            if "OH" in rumus:

                hasil = (
                    "Terbentuk gelembung H2"
                )

        elif uji == "Esterifikasi":

            if (
                "OH" in rumus or
                "COOH" in rumus
            ):

                hasil = "Tercium bau ester"

        # =====================================
        # UJI ALDEHID
        # =====================================

        elif uji == "Tollens":

            if golongan == "Aldehid":

                hasil = (
                    "Terbentuk cermin perak"
                )

        elif uji == "Fehling":

            if golongan == "Aldehid":

                hasil = (
                    "Endapan merah bata"
                )

        elif uji == "Benedict":

            if golongan == "Aldehid":

                hasil = (
                    "Endapan merah"
                )

        elif uji == "Schiff":

            if golongan == "Aldehid":

                hasil = (
                    "Larutan merah muda"
                )

        # =====================================
        # UJI KETON
        # =====================================

        elif uji == "Iodoform":

            if golongan == "Keton":

                hasil = (
                    "Endapan kuning"
                )

        elif uji == "2,4-DNP":

            if golongan in [
                "Keton",
                "Aldehid"
            ]:

                hasil = (
                    "Endapan oranye"
                )

        # =====================================
        # UJI ASAM KARBOKSILAT
        # =====================================

        elif uji == "NaHCO3":

            if golongan == "Asam Karboksilat":

                hasil = (
                    "Muncul gelembung CO2"
                )

        elif uji == "Lakmus":

            if golongan == "Asam Karboksilat":

                hasil = (
                    "Lakmus biru "
                    "menjadi merah"
                )

            elif golongan == "Amina":

                hasil = (
                    "Lakmus merah "
                    "menjadi biru"
                )

        # =====================================
        # UJI ALKENA
        # =====================================

        elif uji == "Bromin":

            if "=" in rumus:

                hasil = (
                    "Warna bromin hilang"
                )

        elif uji == "KMnO4":

            if "=" in rumus:

                hasil = (
                    "Ungu menjadi coklat"
                )

        # =====================================
        # UJI FENOL
        # =====================================

        elif uji == "FeCl3":

            if "C6H5OH" in rumus:

                hasil = (
                    "Larutan ungu"
                )

        # =====================================
        # UJI AMINA
        # =====================================

        elif uji == "Hinsberg":

            if "NH2" in rumus:

                hasil = (
                    "Amina primer "
                    "teridentifikasi"
                )

            elif "NH" in rumus:

                hasil = (
                    "Amina sekunder "
                    "teridentifikasi"
                )

            elif "N" in rumus:

                hasil = (
                    "Amina tersier "
                    "teridentifikasi"
                )

        elif uji == "Karbilamina":

            if "NH2" in rumus:

                hasil = (
                    "Tercium bau menyengat"
                )

        # =========================================
        # VISUAL HASIL
        # =========================================

        if (
            "keruh" in hasil or
            "Endapan" in hasil
        ):

            st.warning(hasil)

        elif (
            "hijau" in hasil or
            "ungu" in hasil or
            "merah" in hasil
        ):

            st.success(hasil)

        elif (
            "Tidak" in hasil
        ):

            st.error(hasil)

        else:

            st.info(hasil)

        # =========================================
        # PERSAMAAN REAKSI
        # =========================================

        st.header("🧾 Persamaan Reaksi")

        reaksi = "Tidak ada reaksi"

        # =====================================
        # ALKOHOL
        # =====================================

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

        elif uji == "CrO3":

            if "CH2(OH)" in rumus:

                produk = rumus.replace(
                    "CH2(OH)",
                    "COOH"
                )

                reaksi = (
                    f"{rumus} + CrO3 "
                    f"→ {produk}"
                )

            elif "CH(OH)" in rumus:

                produk = rumus.replace(
                    "CH(OH)",
                    "CO"
                )

                reaksi = (
                    f"{rumus} + CrO3 "
                    f"→ {produk}"
                )

            elif "C(OH)" in rumus:

                reaksi = (
                    "Alkohol tersier "
                    "tidak teroksidasi"
                )

        elif uji == "Asam Kromat":

            if "OH" in rumus:

                reaksi = (
                    f"{rumus} + H2CrO4 "
                    f"→ produk oksidasi"
                )

        elif uji == "Natrium":

            if "OH" in rumus:

                reaksi = (
                    f"{rumus} + Na "
                    f"→ RONa + H2"
                )

        elif uji == "Esterifikasi":

            if "OH" in rumus:

                reaksi = (
                    f"{rumus} + RCOOH "
                    f"→ RCOOR + H2O"
                )

        # =====================================
        # ALDEHID
        # =====================================

        elif uji == "Tollens":

            if golongan == "Aldehid":

                reaksi = (
                    "RCHO + Ag2O "
                    "→ RCOOH + Ag"
                )

        elif uji == "Fehling":

            if golongan == "Aldehid":

                reaksi = (
                    "RCHO + Cu2+ + OH− "
                    "→ RCOO− + Cu2O"
                )

        elif uji == "Benedict":

            if golongan == "Aldehid":

                reaksi = (
                    "RCHO + Cu2+ "
                    "→ Cu2O"
                )

        elif uji == "Schiff":

            if golongan == "Aldehid":

                reaksi = (
                    "RCHO + Pereaksi Schiff "
                    "→ kompleks merah muda"
                )

        # =====================================
        # KETON
        # =====================================

        elif uji == "Iodoform":

            if golongan == "Keton":

                reaksi = (
                    "RCOCH3 + I2 + NaOH "
                    "→ CHI3 + RCOONa"
                )

        elif uji == "2,4-DNP":

            if golongan in [
                "Keton",
                "Aldehid"
            ]:

                reaksi = (
                    "RCOR + 2,4-DNP "
                    "→ hidrazon"
                )

        # =====================================
        # ASAM KARBOKSILAT
        # =====================================

        elif uji == "NaHCO3":

            if golongan == "Asam Karboksilat":

                reaksi = (
                    "RCOOH + NaHCO3 "
                    "→ RCOONa + CO2 + H2O"
                )

        elif uji == "Lakmus":

            if golongan == "Asam Karboksilat":

                reaksi = (
                    "Asam menghasilkan "
                    "ion H+"
                )

            elif golongan == "Amina":

                reaksi = (
                    "Amina menghasilkan "
                    "ion OH−"
                )

        # =====================================
        # ALKENA
        # =====================================

        elif uji == "Bromin":

            if "=" in rumus:

                reaksi = (
                    "RCH=CHR + Br2 "
                    "→ RCHBr-CHBrR"
                )

        elif uji == "KMnO4":

            if "=" in rumus:

                reaksi = (
                    "RCH=CHR + KMnO4 "
                    "→ diol"
                )

        # =====================================
        # FENOL
        # =====================================

        elif uji == "FeCl3":

            if "C6H5OH" in rumus:

                reaksi = (
                    "Fenol + FeCl3 "
                    "→ kompleks ungu"
                )

        # =====================================
        # AMINA
        # =====================================

        elif uji == "Hinsberg":

            if "NH2" in rumus:

                reaksi = (
                    "RNH2 + C6H5SO2Cl "
                    "→ sulfonamida"
                )

            elif "NH" in rumus:

                reaksi = (
                    "R2NH + C6H5SO2Cl "
                    "→ sulfonamida"
                )

        elif uji == "Karbilamina":

            if "NH2" in rumus:

                reaksi = (
                    "RNH2 + CHCl3 + KOH "
                    "→ RNC"
                )

        st.code(reaksi)

        # =========================================
        # KESIMPULAN
        # =========================================

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
