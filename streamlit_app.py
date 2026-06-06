import streamlit as st
import time

# ==============================================================================
# 1. KONFIGURASI HALAMAN
# ==============================================================================
st.set_page_config(
    page_title="OrganicChem | Edu-Lab Platform",
    page_icon="🧪",
    layout="wide"
)

# ==============================================================================
# 2. CUSTOM CSS INTERAKTIF (VERSI MODERN)
# ==============================================================================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f0f9ff, #f8fafc);
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f766e, #14b8a6);
}
[data-testid="stSidebar"] * {
    color: white !important;
}
.banner-utama {
    background: linear-gradient(135deg, #06b6d4, #3b82f6);
    padding: 35px;
    border-radius: 15px;
    color: white;
    margin-bottom: 30px;
    box-shadow: 0 6px 20px rgba(59,130,246,0.25);
}
.kotak-analisis {
    border-left: 6px solid #14b8a6;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
    background: linear-gradient(135deg, #f0fdfa, #ecfeff);
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}
.stButton > button {
    border-radius: 12px;
    border: none;
    background: linear-gradient(135deg, #14b8a6, #0ea5e9);
    color: white;
    font-weight: 600;
    transition: all 0.3s ease;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(14,165,233,0.3);
}
.tube-wrap {
    display: flex;
    justify-content: center;
    height: 350px;
    padding-top: 20px;
}
.tube-glass {
    width: 80px;
    height: 300px;
    border: 4px solid #64748b;
    border-top: none;
    border-radius: 0 0 40px 40px;
    position: relative;
    overflow: hidden;
    background: rgba(15, 23, 42, 0.16);
    box-shadow: inset 0 0 15px rgba(0,0,0,0.25);
    backdrop-filter: blur(3px);
}
.tube-liquid {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    transition: height 1.2s ease, background 1.2s ease;
}
.precipitate-layer {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 50px;
    background: linear-gradient(to top, #ffffff 0%, #f1f5f9 80%, #cbd5e1 100%) !important;
    box-shadow: 0 -4px 10px rgba(0,0,0,0.3);
    border-top: 2.5px solid #94a3b8;
}
.cloudy-layer {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(to bottom, rgba(255,255,255,0.85), rgba(241,245,249,0.95));
}
.bubble-fx {
    position: absolute;
    background: rgba(0,0,0,0.15);
    border-radius: 50%;
    width: 8px;
    height: 8px;
    animation: floatUp 1.8s infinite ease-in;
}
@keyframes floatUp {
    0% { bottom: 0px; opacity: 1; }
    100% { bottom: 250px; opacity: 0; }
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. FUNGSI HELPER & DATABASE (FORMAT LATEX PRESISI)
# ==============================================================================
def force_rerun():
    if hasattr(st, 'rerun'):
        st.rerun()
    elif hasattr(st, 'experimental_rerun'):
        st.experimental_rerun()

def render_tube(tinggi, warna, efek):
    e_html = ""
    if efek == "precipitate":
        e_html = "<div class='precipitate-layer'></div>"
    elif efek == "cloudy":
        e_html = "<div class='cloudy-layer'></div>"
    elif efek == "bubbles":
        e_html = "<div class='bubble-fx' style='left:20px;'></div><div class='bubble-fx' style='left:50px; animation-delay:0.5s;'></div>"
    return f"<div class='tube-wrap'><div class='tube-glass'><div class='tube-liquid' style='height:{tinggi}; background:{warna};'>{e_html}</div></div></div>"

reagen_colors = {
    "Uji Golongan Alkohol": "#facc15", 
    "Uji Oksidasi Alkohol": "#f97316", 
    "Uji Golongan Alkohol Tersier": "#f8fafc", 
    "Uji Golongan Alkohol Sekunder": "#f8fafc", 
    "Uji Golongan Alkanal/Aldehida (Bisulfit)": "#f8fafc", 
    "Uji Reduksi Golongan Alkanal (Fehling)": "#3b82f6", 
    "Uji Spesifik Golongan Alkanal (Schiff)": "#f8fafc",
    "Uji Golongan Metil Keton / Metil Karbinol": "#f8fafc",
    "Uji Golongan Ester": "#f8fafc",
    "Uji Golongan Asam Karboksilat": "#f8fafc"
}

flowchart_paths = {
    "Alkohol Primer": ["Uji Golongan Alkohol", "Uji Oksidasi Alkohol", "Uji Golongan Alkohol Sekunder"],
    "Alkohol Sekunder": ["Uji Golongan Alkohol", "Uji Oksidasi Alkohol", "Uji Golongan Alkohol Sekunder", "Uji Golongan Metil Keton / Metil Karbinol"],
    "Alkohol Tersier": ["Uji Golongan Alkohol", "Uji Oksidasi Alkohol", "Uji Golongan Alkohol Tersier"],
    "Aldehida (Alkanal)": ["Uji Golongan Alkohol", "Uji Golongan Alkanal/Aldehida (Bisulfit)", "Uji Reduksi Golongan Alkanal (Fehling)", "Uji Spesifik Golongan Alkanal (Schiff)"],
    "Keton (Alkanon)": ["Uji Golongan Alkohol", "Uji Golongan Alkanal/Aldehida (Bisulfit)", "Uji Reduksi Golongan Alkanal (Fehling)", "Uji Golongan Metil Keton / Metil Karbinol"],
    "Ester (Alkil Alkanoat)": ["Uji Golongan Alkohol", "Uji Golongan Alkanal/Aldehida (Bisulfit)", "Uji Golongan Ester"],
    "Asam Karboksilat": ["Uji Golongan Alkohol", "Uji Golongan Alkanal/Aldehida (Bisulfit)", "Uji Golongan Ester", "Uji Golongan Asam Karboksilat"],
    "Alkana / Hidrokarbon Jenuh": ["Uji Golongan Alkohol", "Uji Golongan Alkanal/Aldehida (Bisulfit)", "Uji Golongan Ester", "Uji Golongan Asam Karboksilat"]
}

database_reaksi = {
    "Alkohol Primer": {
        "Uji Golongan Alkohol": {
            "hasil": "(+) Merah Ceri", 
            "reaksi": r"R-OH + [Ce(NO_3)_6]^{2-} \rightarrow [Ce(OR)(NO_3)_5]^{2-} + HNO_3", 
            "alasan": "Gugus -OH bebas bereaksi menggantikan ligan nitrat pada ion Cerium(IV) membentuk senyawa kompleks koordinasi berwarna merah ceri.", 
            "warna_akhir": "#ef4444", "efek": "none"
        },
        "Uji Oksidasi Alkohol": {
            "hasil": "(+) Hijau", 
            "reaksi": r"3\ R-CH_2OH + 2\ CrO_3 + 3\ H_2SO_4 \rightarrow 3\ R-CHO + Cr_2(SO_4)_3 + 6\ H_2O", 
            "alasan": "Memiliki atom hidrogen alfa. Gugus -OH dioksidasi menjadi aldehida, sedangkan Kromium(VI) jingga tereduksi menjadi Kromium(III) hijau.", 
            "warna_akhir": "#10b981", "efek": "none"
        },
        "Uji Golongan Alkohol Sekunder": {
            "hasil": "(-) Bening", 
            "reaksi": r"R-CH_2OH + HCl \xrightarrow{ZnCl_2} \text{Tidak ada reaksi}", 
            "alasan": "Karbokation primer sangat tidak stabil sehingga tidak mampu bereaksi dengan pereaksi Lucas pada suhu kamar.", 
            "warna_akhir": "#f8fafc", "efek": "none"
        }
    },
    "Alkohol Sekunder": {
        "Uji Golongan Alkohol": {
            "hasil": "(+) Merah Ceri", 
            "reaksi": r"R-OH + [Ce(NO_3)_6]^{2-} \rightarrow [Ce(OR)(NO_3)_5]^{2-} + HNO_3", 
            "alasan": "Ikatan koordinasi terbentuk antara atom oksigen pada gugus hidroksil sekunder dengan logam Cerium pusat.", 
            "warna_akhir": "#ef4444", "efek": "none"
        },
        "Uji Oksidasi Alkohol": {
            "hasil": "(+) Hijau", 
            "reaksi": r"3\ R_2CH-OH + 2\ CrO_3 + 3\ H_2SO_4 \rightarrow 3\ R_2C=O + Cr_2(SO_4)_3 + 6\ H_2O", 
            "alasan": "Alkohol sekunder dioksidasi menjadi keton, ditandai dengan perubahan warna larutan dari jingga ke hijau.", 
            "warna_akhir": "#10b981", "efek": "none"
        },
        "Uji Golongan Alkohol Sekunder": {
            "hasil": "(+) Emulsi Putih", 
            "reaksi": r"R_2CH-OH + HCl \xrightarrow{ZnCl_2} R_2CH-Cl \downarrow + H_2O", 
            "alasan": "Karbokation sekunder memiliki stabilitas menengah. Bereaksi menghasilkan alkil klorida setelah 5-10 menit dengan bantuan pemanasan.", 
            "warna_akhir": "#e2e8f0", "efek": "cloudy"
        },
        "Uji Golongan Metil Keton / Metil Karbinol": {
            "hasil": "(+) Endapan Kuning", 
            "reaksi": r"R-CH(OH)-CH_3 + 4\ I_2 + 6\ NaOH \rightarrow CHI_3 \downarrow + R-COONa + 5\ NaI + 5\ H_2O", 
            "alasan": "Struktur metil karbinol dioksidasi oleh iodin menjadi metil keton, lalu membentuk kristal iodoform berwarna kuning.", 
            "warna_akhir": "#fef08a", "efek": "precipitate"
        }
    },
    "Alkohol Tersier": {
        "Uji Golongan Alkohol": {
            "hasil": "(+) Merah Ceri", 
            "reaksi": r"R-OH + [Ce(NO_3)_6]^{2-} \rightarrow [Ce(OR)(NO_3)_5]^{2-} + HNO_3", 
            "alasan": "Memiliki gugus -OH bebas yang dapat membentuk kompleks koordinasi berwarna merah dengan ceric ammonium nitrate.", 
            "warna_akhir": "#ef4444", "efek": "none"
        },
        "Uji Oksidasi Alkohol": {
            "hasil": "(-) Tetap Jingga", 
            "reaksi": r"R_3C-OH + CrO_3 \rightarrow \text{Tidak bereaksi}", 
            "alasan": "Alkohol tersier tidak memiliki atom hidrogen alfa sehingga tidak dapat dioksidasi oleh pereaksi Jones.", 
            "warna_akhir": "#f97316", "efek": "none"
        },
        "Uji Golongan Alkohol Tersier": {
            "hasil": "(+) Emulsi Putih (Seketika)", 
            "reaksi": r"R_3C-OH + HCl \xrightarrow{ZnCl_2} R_3C-Cl \downarrow + H_2O", 
            "alasan": "Membentuk karbokation tersier yang sangat stabil, sehingga reaksi substitusi berjalan instan membentuk kabut keruh alkil klorida.", 
            "warna_akhir": "#94a3b8", "efek": "cloudy"
        }
    },
    "Aldehida (Alkanal)": {
        "Uji Golongan Alkohol": {
            "hasil": "(-) Kuning", 
            "reaksi": r"R-CHO + [Ce(NO_3)_6]^{2-} \rightarrow \text{Tidak bereaksi}", 
            "alasan": "Aldehida tidak memiliki gugus hidroksil (-OH) bebas sehingga warna pereaksi tetap kuning.", 
            "warna_akhir": "#facc15", "efek": "none"
        },
        "Uji Golongan Alkanal/Aldehida (Bisulfit)": {
            "hasil": "(+) Endapan Putih", 
            "reaksi": r"R-CHO + NaHSO_3 \rightarrow R-CH(OH)SO_3Na \downarrow", 
            "alasan": "Nukleofil bisulfit menyerang gugus karbonil aldehida yang reaktif, menghasilkan produk adisi berupa kristal putih.", 
            "warna_akhir": "#ffffff", "efek": "precipitate"
        },
        "Uji Reduksi Golongan Alkanal (Fehling)": {
            "hasil": "(+) Merah Bata", 
            "reaksi": r"R-CHO + 2\ Cu^{2+} + 5\ OH^- \rightarrow R-COO^- + Cu_2O \downarrow + 3\ H_2O", 
            "alasan": "Aldehida adalah reduktor kuat yang mereduksi kupri oksida menjadi endapan tembaga(I) oksida berwarna merah bata.", 
            "warna_akhir": "#b91c1c", "efek": "precipitate"
        },
        "Uji Spesifik Golongan Alkanal (Schiff)": {
            "hasil": "(+) Ungu / Magenta", 
            "reaksi": r"\text{Aldehida} + \text{Pereaksi Schiff} \rightarrow \text{Kompleks Magenta}", 
            "alasan": "Reaksi adisi spesifik yang mengembalikan struktur warna p-rosanilin menjadi ungu murni.", 
            "warna_akhir": "#d946ef", "efek": "none"
        }
    },
    "Keton (Alkanon)": {
        "Uji Golongan Alkohol": {
            "hasil": "(-) Kuning", 
            "reaksi": r"\text{Keton} + [Ce(NO_3)_6]^{2-} \rightarrow \text{Tidak bereaksi}", 
            "alasan": "Keton tidak memiliki gugus fungsi hidroksil.", 
            "warna_akhir": "#facc15", "efek": "none"
        },
        "Uji Golongan Alkanal/Aldehida (Bisulfit)": {
            "hasil": "(+) Endapan Putih", 
            "reaksi": r"CH_3-CO-CH_3 + NaHSO_3 \rightarrow (CH_3)_2C(OH)SO_3Na \downarrow", 
            "alasan": "Keton suku rendah (seperti aseton) memiliki halangan sterik kecil sehingga masih bisa diadisi oleh bisulfit membentuk endapan putih.", 
            "warna_akhir": "#ffffff", "efek": "precipitate"
        },
        "Uji Reduksi Golongan Alkanal (Fehling)": {
            "hasil": "(-) Tetap Biru", 
            "reaksi": r"\text{Keton} + Cu^{2+} \rightarrow \text{Tidak bereaksi}", 
            "alasan": "Keton tidak memiliki atom hidrogen pada gugus karbonil sehingga tidak bersifat reduktor.", 
            "warna_akhir": "#3b82f6", "efek": "none"
        },
        "Uji Golongan Metil Keton / Metil Karbinol": {
            "hasil": "(+) Endapan Kuning", 
            "reaksi": r"R-CO-CH_3 + 3\ I_2 + 4\ NaOH \rightarrow CHI_3 \downarrow + R-COONa + 3\ NaI + 3\ H_2O", 
            "alasan": "Memiliki gugus metil yang terikat langsung pada karbonil, sehingga bereaksi positif membentuk endapan kuning iodoform.", 
            "warna_akhir": "#fef08a", "efek": "precipitate"
        }
    },
    "Ester (Alkil Alkanoat)": {
        "Uji Golongan Alkohol": {
            "hasil": "(-) Kuning", "reaksi": r"\text{Ester} + [Ce(NO_3)_6]^{2-} \rightarrow \text{Tidak bereaksi}", "alasan": "Tidak memiliki gugus hidroksil bebas.", "warna_akhir": "#facc15", "efek": "none"
        },
        "Uji Golongan Alkanal/Aldehida (Bisulfit)": {
            "hasil": "(-) Bening", "reaksi": r"\text{Ester} + NaHSO_3 \rightarrow \text{Tidak bereaksi}", "alasan": "Gugus ester stabil akibat efek resonansi elektron sehingga tidak reaktif terhadap nukleofil lemah.", "warna_akhir": "#f8fafc", "efek": "none"
        },
        "Uji Golongan Ester": {
            "hasil": "(+) Merah Violet", 
            "reaksi": r"3\ R-COOR' + 3\ NH_2OH + FeCl_3 \rightarrow Fe(R-CONHO)_3 \downarrow + 3\ R'-OH + 3\ HCl", 
            "alasan": "Ester bereaksi dengan hidroksilamin membentuk asam hidroksamat yang mengikat besi(III) menjadi kompleks berwarna violet.", 
            "warna_akhir": "#c026d3", "efek": "none"
        }
    },
    "Asam Karboksilat": {
        "Uji Golongan Alkohol": {
            "hasil": "(-) Kuning", "reaksi": r"R-COOH + [Ce(NO_3)_6]^{2-} \rightarrow \text{Tidak bereaksi}", "alasan": "Oksigen hidroksil ditarik oleh efek resonansi karbonil sehingga sifat nukleofilnya hilang.", "warna_akhir": "#facc15", "efek": "none"
        },
        "Uji Golongan Alkanal/Aldehida (Bisulfit)": {
            "hasil": "(-) Bening", "reaksi": r"R-COOH + NaHSO_3 \rightarrow \text{Tidak bereaksi}", "alasan": "Senyawa ini tidak mengandung gugus fungsi aldehida atau keton.", "warna_akhir": "#f8fafc", "efek": "none"
        },
        "Uji Golongan Ester": {
            "hasil": "(-) Bening", "reaksi": r"R-COOH + NH_2OH + FeCl_3 \rightarrow \text{Tidak bereaksi}", "alasan": "Asam karboksilat bebas tidak membentuk hidroksamat pada kondisi uji ini.", "warna_akhir": "#f8fafc", "efek": "none"
        },
        "Uji Golongan Asam Karboksilat": {
            "hasil": "(+) Gelembung & Keruh", 
            "reaksi": r"R-COOH + NaHCO_3 \rightarrow R-COONa + H_2O + CO_2 \uparrow", 
            "alasan": "Sifat asamnya mendonasikan proton untuk mengurai bikarbonat menjadi gas CO2. Gas tersebut jika diuji lanjut dengan air barit akan mengeruh karena membentuk BaCO3.", 
            "warna_akhir": "#f8fafc", "efek": "bubbles"
        }
    },
    "Alkana / Hidrokarbon Jenuh": {
        "Uji Golongan Alkohol": {
            "hasil": "(-) Kuning", "reaksi": r"\text{Alkana} + [Ce(NO_3)_6]^{2-} \rightarrow \text{Tidak bereaksi}", "alasan": "Senyawa nonpolar inert, tidak memiliki gugus hidroksil.", "warna_akhir": "#facc15", "efek": "none"
        },
        "Uji Golongan Alkanal/Aldehida (Bisulfit)": {
            "hasil": "(-) Bening", "reaksi": r"\text{Alkana} + NaHSO_3 \rightarrow \text{Tidak bereaksi}", "alasan": "Tidak memiliki gugus fungsi karbonil.", "warna_akhir": "#f8fafc", "efek": "none"
        },
        "Uji Golongan Ester": {
            "hasil": "(-) Bening", "reaksi": r"\text{Alkana} + NH_2OH \rightarrow \text{Tidak bereaksi}", "alasan": "Tidak memiliki gugus fungsi ester.", "warna_akhir": "#f8fafc", "efek": "none"
        },
        "Uji Golongan Asam Karboksilat": {
            "hasil": "(-) Bening", "reaksi": r"\text{Alkana} + NaHCO_3 \rightarrow \text{Tidak bereaksi}", 
            "alasan": "Hidrokarbon jenuh bersifat inert. Kegagalan di seluruh uji gugus fungsi membuktikan sampel ini adalah golongan alkana.", 
            "warna_akhir": "#f8fafc", "efek": "none"
        }
    }
}

# Inisialisasi session state jika belum ada
if "test_started" not in st.session_state:
    st.session_state.test_started = False
if "current_step" not in st.session_state:
    st.session_state.current_step = 0
if "log_history" not in st.session_state:
    st.session_state.log_history = []
if "trigger_animation" not in st.session_state:
    st.session_state.trigger_animation = False

# ==============================================================================
# 4. SIDEBAR NAVIGASI
# ==============================================================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3022/3022607.png", width=75)
    st.title("OrganicChem v1.0")
    st.write("🔬 *E-Learning & Lab Simulator*")
    st.markdown("---")
    
    pilihan_halaman = st.sidebar.radio(
        "Navigasi Menu:",
        [
            "🏠 HALAMAN UTAMA", 
            "📘 BAB I. HIDROKARBON", 
            "📙 BAB II. ALKOHOL, ETER, DAN FENOL", 
            "📗 BAB III. ALDEHID DAN KETON", 
            "📕 BAB IV. ASAM KARBOKSILAT DAN DERIVATNYA", 
            "🔬 POST TEST"
        ]
    )
    st.markdown("---")
    st.caption("E-Learning Kimia Organik | © 2026")

# ==============================================================================
# 5. LOGIKA KONTEN TIAP HALAMAN (DENGAN UPDATE MATERI LENGKAP)
# ==============================================================================

if pilihan_halaman == "🏠 HALAMAN UTAMA":
    st.markdown("""
        <div class="banner-utama">
            <h1 style='color: white; margin-bottom: 5px; font-weight: 700;'>Selamat Datang di OrganicChem! 👋</h1>
            <p style='font-size: 1.2em; opacity: 0.95;'>Platform Eksplorasi Dunia Kimia Organik Tanpa Batas Melalui Media Pembelajaran Mandiri & Simulasi Identifikasi Gugus Fungsi</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.subheader("💡 Tentang Platform Ini")
    st.write(
        "Platform ini dirancang khusus untuk membantu memahami materi teoritis "
        "sekaligus visualisasi reaksi uji kualitatif senyawa organik di laboratorium secara interaktif—kapan saja dan dimana saja, layaknya memiliki laboratorium pribadi."
    )
    st.markdown("---")
    st.markdown("""
    ### 📌 **Petunjuk Penggunaan**
    Untuk memaksimalkan pengalaman belajar Anda di platform **OrganicChem**, ikuti langkah-langkah sistematis berikut:
    
    1. **Pelajari Teori Dasar:** Pilih menu **BAB I hingga BAB IV** pada sidebar di sebelah kiri untuk membaca rangkuman materi lengkap, sifat fisika-kimia, serta mekanisme reaksi spesifik dari masing-masing golongan senyawa organik.
    2. **Pahami Persamaan Reaksi:** Perhatikan baik-baik visualisasi formula dan persamaan reaksi kimia berbasis LaTeX yang disediakan pada setiap bab guna memperkuat pemahaman struktural Anda.
    3. **Akses Lab Virtual:** Setelah menguasai teori, klik menu **🔬 POST TEST** untuk membuka fitur *Smart Flowchart Auto-Analyzer*.
    4. **Pilih Sampel Misterius:** Pilih salah satu golongan senyawa pada menu *drop-down* yang bertindak sebagai *Blind Sample* (sampel tidak diketahui).
    5. **Jalankan Simulasi Uji:** Klik tombol **Mulai Identifikasi 🚀** dan ikuti rangkaian pengujian langkah demi langkah.
    6. **Amati Perubahan Fisik:** Perhatikan perubahan warna, pembentukan emulsi kabut, atau endapan pada komponen **Visual Lab** (Tabung Reaksi).
    7. **Evaluasi Logbook:** Tinjau analisis teoritis, mekanisme persamaan reaksi, dan pembahasan otomatis yang muncul pada sisi **Logbook & Analisis Teoritis** hingga diperoleh kesimpulan akhir golongan fungsi senyawa.
    """)

elif pilihan_halaman == "📘 BAB I. HIDROKARBON":
    st.title("📘 BAB I. HIDROKARBON")
    st.write("---")
    
    st.markdown("""
    Hidrokarbon adalah senyawa organik yang seluruh strukturnya hanya tersusun atas unsur karbon dan hidrogen. Berdasarkan jenis ikatannya, hidrokarbon alifatik dibagi menjadi hidrokarbon jenuh (alkana) dan tidak jenuh (alkena dan alkuna). Sementara itu, hidrokarbon aromatik memiliki rantai siklik konjugasi yang sangat stabil.

    #### **A. Sifat Fisika Hidrokarbon**
    
    * **Wujud Zat:** Suku rendah ($C_1 - C_4$) berwujud gas, suku sedang ($C_5 - C_{17}$) berwujud cair, dan suku tinggi ($\ge C_{18}$) berwujud padat pada suhu kamar.
    * **Kelarutan:** Bersifat nonpolar, sehingga tidak larut dalam air melainkan larut dengan baik dalam pelarut organik nonpolar seperti kloroform ($CHCl_3$) atau eter.
    * **Titik Didih:** Meningkat seiring bertambahnya panjang rantai karbon. Senyawa berantai lurus memiliki titik didih lebih tinggi daripada isomer rantai bercabangnya.
    * **Densitas:** Memiliki massa jenis yang lebih kecil daripada air, sehingga lapisan hidrokarbon selalu berada di bagian atas jika dicampur air.

    #### **B. Sifat Kimia & Reaksi Identifikasi Hidrokarbon**

    ##### **1. Alkana (Hidrokarbon Jenuh)**
    Alkana kurang reaktif terhadap sebagian besar pereaksi pada suhu kamar karena ikatannya yang jenuh.
    
    * **Uji Iodo (Substitusi Halogen):** Dapat bereaksi melalui mekanisme radikal bebas dengan bantuan sinar UV atau pemanasan tinggi.
    """)
    st.latex(r"CH_4 + I_2 \xrightarrow{\text{Sinar UV}} CH_3I + HI")
    
    st.markdown("""
    ##### **2. Alkena dan Alkuna (Hidrokarbon Tidak Jenuh)**
    Sangat reaktif karena memiliki ikatan rangkap dua atau tiga yang kaya akan elektron, sehingga mudah mengalami reaksi adisi.
    
    * **Uji Adisi Iodium:** Mengadisi halogen pada ikatan rangkap tanpa bantuan sinar UV, ditandai dengan memudarnya warna ungu iodium seketika.
    """)
    st.latex(r"R-CH=CH-R + I_2 \rightarrow R-CH(I)-CH(I)-R")
    
    st.markdown("""
    * **Uji Baeyer (Oksidasi dengan $KMnO_4$):** Dioksidasi oleh kalium permanganat menghasilkan senyawa glikol dan menghasilkan endapan cokelat dari mangan dioksida.
    """)
    st.latex(r"3\ CH_2=CH_2 + 2\ KMnO_4 + 4\ H_2O \rightarrow 3\ HO-CH_2-CH_2-OH + 2\ MnO_2 \downarrow + 2\ KOH")
    
    st.markdown("""
    ##### **3. Benzena (Hidrokarbon Aromatik)**
    Memiliki cincin konjugasi stabil yang memenuhi aturan Hückel.
    
    * **Uji Bakar:** Memiliki persentase kadar karbon yang sangat tinggi sehingga jika dibakar menghasilkan jelaga hitam yang tebal.
    """)
    st.latex(r"\text{Benzena} + O_2 \rightarrow C_{(s)\ \text{[Jelaga]}} + CO + H_2O")

elif pilihan_halaman == "... [BAGIAN SCRIPT SEBELUMNYA TETAP SAMA] ...":
    pass

elif pilihan_halaman == "🔬 POST TEST":
    pass
