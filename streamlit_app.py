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
    padding-top: 10px;
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
    height: 60px;
    box-shadow: inset 0 2px 5px rgba(0,0,0,0.2);
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
.reagent-tag {
    text-align: center;
    font-weight: bold;
    background-color: #e2e8f0;
    color: #1e293b;
    padding: 6px 12px;
    border-radius: 8px;
    margin-bottom: 15px;
    border: 1px solid #cbd5e1;
}
@keyframes floatUp {
    0% { bottom: 0px; opacity: 1; }
    100% { bottom: 250px; opacity: 0; }
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. FUNGSI HELPER & DATABASE
# ==============================================================================
def force_rerun():
    if hasattr(st, 'rerun'):
        st.rerun()
    elif hasattr(st, 'experimental_rerun'):
        st.experimental_rerun()

def render_tube(tinggi, warna_larutan, efek, warna_endapan=None):
    e_html = ""
    if efek == "precipitate":
        bg_endapan = warna_endapan if warna_endapan else warna_larutan
        e_html = f"<div class='precipitate-layer' style='background: {bg_endapan}; border-top: 3.5px solid rgba(0, 0, 0, 0.25);'></div>"
    elif efek == "cloudy":
        e_html = "<div class='cloudy-layer'></div>"
    elif efek == "bubbles":
        e_html = "<div class='bubble-fx' style='left:20px;'></div><div class='bubble-fx' style='left:50px; animation-delay:0.5s;'></div>"
    return f"<div class='tube-wrap'><div class='tube-glass'><div class='tube-liquid' style='height:{tinggi}; background:{warna_larutan};'>{e_html}</div></div></div>"

# Warna awal pereaksi sebelum reaksi
reagen_colors = {
    "Ceric Nitrat":                  "#f97316",   # jingga
    "Pereaksi Jones":                "#f97316",   # jingga
    "Pereaksi Lucas":                "#f8fafc",   # bening
    "Pereaksi Lucas (Panas)":        "#f8fafc",   # bening
    "Na-Bisulfit":                   "#f8fafc",   # bening
    "Pereaksi Fehling":              "#3b82f6",   # biru
    "Pereaksi Schiff":               "#f8fafc",   # bening (tak berwarna)
    "Uji Iodoform":                  "#f8fafc",   # bening
    "Hidroksilamin (Uji Ester)":     "#f8fafc",   # bening
    "Uji Barit (NaHCO3)":           "#f8fafc",   # bening
}

# Urutan pereaksi tiap senyawa (Blind Sample)
flowchart_paths = {
    "1-Butanol":       ["Ceric Nitrat", "Pereaksi Jones", "Pereaksi Lucas (Panas)"],
    "2-Butanol":       ["Ceric Nitrat", "Pereaksi Jones", "Pereaksi Lucas (Panas)", "Uji Iodoform"],
    "t-Butil Alkohol": ["Ceric Nitrat", "Pereaksi Jones", "Pereaksi Lucas"],
    "Formaldehida":    ["Ceric Nitrat", "Na-Bisulfit", "Pereaksi Fehling", "Pereaksi Schiff"],
    "Aseton":          ["Ceric Nitrat", "Na-Bisulfit", "Pereaksi Fehling", "Uji Iodoform"],
    "Etil Asetat":     ["Ceric Nitrat", "Na-Bisulfit", "Hidroksilamin (Uji Ester)"],
    "Asam Asetat":     ["Ceric Nitrat", "Na-Bisulfit", "Hidroksilamin (Uji Ester)", "Uji Barit (NaHCO3)"],
    "Heksana":         ["Ceric Nitrat", "Na-Bisulfit", "Hidroksilamin (Uji Ester)", "Uji Barit (NaHCO3)"],
}

# Database lengkap: hasil, persamaan reaksi, pembahasan, warna akhir, efek visual
database_reaksi = {

    # ─────────────────────────────────────────────
    # 1-BUTANOL  (Alkohol Primer)
    # ─────────────────────────────────────────────
    "1-Butanol": {
        "Ceric Nitrat": {
            "hasil": "(+) Merah Ceri",
            "reaksi": r"n\text{-}C_4H_9OH + [Ce(NO_3)_6]^{2-} \rightarrow [Ce(OC_4H_9)(NO_3)_5]^{2-} + HNO_3",
            "alasan": "Gugus –OH bebas pada alkohol primer membentuk ikatan koordinasi dengan ion Ce(IV), menghasilkan kompleks berwarna merah ceri yang khas. Ini membuktikan keberadaan gugus hidroksil pada sampel.",
            "warna_akhir": "#ef4444", "efek": "none"
        },
        "Pereaksi Jones": {
            "hasil": "(+) Hijau — terbentuk Butanal/Asam Butanoat",
            "reaksi": r"3\ n\text{-}C_4H_9OH + 2\ CrO_3 + 3\ H_2SO_4 \rightarrow 3\ C_3H_7CHO + Cr_2(SO_4)_3 + 6\ H_2O",
            "alasan": "Alkohol primer memiliki atom hidrogen α sehingga dapat dioksidasi oleh CrO₃/H₂SO₄ (Pereaksi Jones). Ion Cr(VI) yang berwarna jingga tereduksi menjadi Cr(III) yang berwarna hijau, menandakan hasil positif. Produk awal adalah butanal yang dapat teroksidasi lebih lanjut menjadi asam butanoat.",
            "warna_akhir": "#10b981", "efek": "none"
        },
        "Pereaksi Lucas (Panas)": {
            "hasil": "(-) Bening — tidak bereaksi dalam waktu 5 menit",
            "reaksi": r"n\text{-}C_4H_9OH + HCl \xrightarrow{ZnCl_2,\ \Delta} \text{Tidak bereaksi pada suhu kamar}",
            "alasan": "Alkohol primer membentuk karbokation primer yang sangat tidak stabil sehingga substitusi oleh Cl⁻ tidak terjadi pada suhu kamar meski dipanaskan sebentar. Larutan tetap bening dan homogen, membuktikan sampel adalah alkohol primer (bukan sekunder atau tersier).",
            "warna_akhir": "#f8fafc", "efek": "none"
        },
    },

    # ─────────────────────────────────────────────
    # 2-BUTANOL  (Alkohol Sekunder)
    # ─────────────────────────────────────────────
    "2-Butanol": {
        "Ceric Nitrat": {
            "hasil": "(+) Merah Ceri",
            "reaksi": r"sec\text{-}C_4H_9OH + [Ce(NO_3)_6]^{2-} \rightarrow [Ce(OC_4H_9)(NO_3)_5]^{2-} + HNO_3",
            "alasan": "Gugus –OH pada alkohol sekunder masih mampu membentuk kompleks koordinasi dengan Ce(IV) menghasilkan warna merah ceri. Hasil ini positif, menunjukkan sampel mengandung gugus hidroksil.",
            "warna_akhir": "#ef4444", "efek": "none"
        },
        "Pereaksi Jones": {
            "hasil": "(+) Hijau — terbentuk Butanon (MEK)",
            "reaksi": r"3\ CH_3CH(OH)C_2H_5 + 2\ CrO_3 + 3\ H_2SO_4 \rightarrow 3\ CH_3COC_2H_5 + Cr_2(SO_4)_3 + 6\ H_2O",
            "alasan": "Alkohol sekunder dioksidasi menjadi keton (butanon / MEK) oleh Pereaksi Jones. Perubahan warna dari jingga ke hijau mengonfirmasi oksidasi berhasil. Keton tidak dapat dioksidasi lebih lanjut sehingga reaksi berhenti di tahap ini.",
            "warna_akhir": "#10b981", "efek": "none"
        },
        "Pereaksi Lucas (Panas)": {
            "hasil": "(+) Emulsi Putih — terbentuk 2-Klorobutana (5–10 menit)",
            "reaksi": r"CH_3CH(OH)C_2H_5 + HCl \xrightarrow{ZnCl_2,\ \Delta} CH_3CHClC_2H_5 \downarrow + H_2O",
            "alasan": "Karbokation sekunder memiliki stabilitas menengah, sehingga reaksi substitusi berlangsung dengan bantuan pemanasan dan ZnCl₂ dalam 5–10 menit. Terbentuknya lapisan putih keruh (emulsi alkil klorida) membedakan alkohol sekunder dari primer (tidak bereaksi) dan tersier (bereaksi seketika).",
            "warna_akhir": "#e2e8f0", "efek": "cloudy"
        },
        "Uji Iodoform": {
            "hasil": "(+) Endapan Kuning Iodoform (CHI₃)",
            "reaksi": r"CH_3CH(OH)C_2H_5 + 4\ I_2 + 6\ NaOH \rightarrow CHI_3 \downarrow + C_2H_5COONa + 5\ NaI + 5\ H_2O",
            "alasan": "2-Butanol memiliki struktur metil karbinol (CH₃–CHOH–) yang menjadi syarat positif uji iodoform. Iodin dalam suasana basa (NaOH) mengoksidasi gugus metil karbinol, lalu terjadi iodinasi bertahap menghasilkan kristal kuning iodoform (CHI₃) yang tidak larut dan berbau khas.",
            "warna_akhir": "#fef08a", "efek": "precipitate", "warna_endapan": "#facc15"
        },
    },

    # ─────────────────────────────────────────────
    # t-BUTIL ALKOHOL  (Alkohol Tersier)
    # ─────────────────────────────────────────────
    "t-Butil Alkohol": {
        "Ceric Nitrat": {
            "hasil": "(+) Merah Ceri",
            "reaksi": r"(CH_3)_3COH + [Ce(NO_3)_6]^{2-} \rightarrow [Ce(OC(CH_3)_3)(NO_3)_5]^{2-} + HNO_3",
            "alasan": "Meskipun tergolong alkohol tersier, gugus –OH tetap bebas dan mampu berkoordinasi dengan Ce(IV) membentuk kompleks merah ceri. Hasil positif ini hanya membuktikan adanya gugus hidroksil, bukan jenis alkohol.",
            "warna_akhir": "#ef4444", "efek": "none"
        },
        "Pereaksi Jones": {
            "hasil": "(-) Tetap Jingga — tidak teroksidasi",
            "reaksi": r"(CH_3)_3COH + CrO_3 \rightarrow \text{Tidak bereaksi}",
            "alasan": "Alkohol tersier tidak memiliki atom hidrogen α pada karbon karbinol, sehingga tidak dapat dioksidasi oleh Pereaksi Jones. Larutan tetap berwarna jingga. Hasil negatif ini adalah bukti kunci yang membedakan alkohol tersier dari primer dan sekunder.",
            "warna_akhir": "#f97316", "efek": "none"
        },
        "Pereaksi Lucas": {
            "hasil": "(+) Emulsi Putih Seketika — terbentuk t-Butil Klorida",
            "reaksi": r"(CH_3)_3COH + HCl \xrightarrow{ZnCl_2} (CH_3)_3CCl \downarrow + H_2O",
            "alasan": "Karbokation tersier yang terbentuk sangat stabil secara hiperkonjugasi dan induksi dari tiga gugus metil, sehingga reaksi substitusi SN1 berjalan instan pada suhu kamar tanpa pemanasan. Terbentuknya kabut putih seketika merupakan tanda definitif alkohol tersier.",
            "warna_akhir": "#94a3b8", "efek": "cloudy"
        },
    },

    # ─────────────────────────────────────────────
    # FORMALDEHIDA  (Aldehida / Alkanal)
    # ─────────────────────────────────────────────
    "Formaldehida": {
        "Ceric Nitrat": {
            "hasil": "(-) Tetap Jingga",
            "reaksi": r"HCHO + [Ce(NO_3)_6]^{2-} \rightarrow \text{Tidak bereaksi}",
            "alasan": "Formaldehida tidak memiliki gugus hidroksil (–OH) bebas sehingga tidak dapat membentuk kompleks koordinasi dengan Ce(IV). Warna pereaksi tetap jingga, menunjukkan sampel bukan alkohol atau fenol.",
            "warna_akhir": "#f97316", "efek": "none"
        },
        "Na-Bisulfit": {
            "hasil": "(+) Endapan Putih Kristal",
            "reaksi": r"HCHO + NaHSO_3 \rightarrow HOCH_2SO_3Na \downarrow",
            "alasan": "Gugus karbonil aldehida sangat reaktif terhadap nukleofil. Ion bisulfit (HSO₃⁻) menyerang karbon karbonil formaldehida secara adisi nukleofilik menghasilkan senyawa aduk α-hidroksi sulfonat berupa endapan kristal putih yang tidak larut. Hasil positif ini menunjukkan adanya gugus karbonil aktif (aldehida atau keton suku rendah).",
            "warna_akhir": "#cbd5e1", "efek": "precipitate", "warna_endapan": "#ffffff"
        },
        "Pereaksi Fehling": {
            "hasil": "(+) Endapan Merah Bata (Cu₂O)",
            "reaksi": r"HCHO + 2\ Cu^{2+} + 5\ OH^- \rightarrow HCOO^- + Cu_2O \downarrow + 3\ H_2O",
            "alasan": "Formaldehida adalah reduktor kuat. Gugus –CHO mereduksi ion Cu²⁺ kompleks tartrat dalam suasana basa menjadi Cu₂O (endapan merah bata). Formaldehida adalah satu-satunya aldehida yang bisa memberikan endapan tembaga metalik mengkilap pada kondisi tertentu karena sangat reaktif.",
            "warna_akhir": "#3b82f6", "efek": "precipitate", "warna_endapan": "#b91c1c"
        },
        "Pereaksi Schiff": {
            "hasil": "(+) Ungu / Magenta",
            "reaksi": r"HCHO + \text{p-Rosanilin (tak berwarna)} \rightarrow \text{Kompleks Magenta}",
            "alasan": "Pereaksi Schiff (fuchsin yang didekolorisasi oleh SO₂) secara spesifik bereaksi dengan aldehida melalui adisi aминоsulfonat. Aldehida memulihkan kromofor quinoidal dari p-rosanilin sehingga warna merah-ungu (magenta) muncul kembali. Keton tidak memberikan reaksi ini, menjadikan uji Schiff sebagai pembeda definitif aldehida dari keton.",
            "warna_akhir": "#d946ef", "efek": "none"
        },
    },

    # ─────────────────────────────────────────────
    # ASETON  (Keton / Alkanon)
    # ─────────────────────────────────────────────
    "Aseton": {
        "Ceric Nitrat": {
            "hasil": "(-) Tetap Jingga",
            "reaksi": r"(CH_3)_2CO + [Ce(NO_3)_6]^{2-} \rightarrow \text{Tidak bereaksi}",
            "alasan": "Aseton tidak memiliki gugus –OH bebas sehingga tidak bereaksi dengan pereaksi CAN. Warna tetap jingga, mengindikasikan sampel bukan golongan alkohol.",
            "warna_akhir": "#f97316", "efek": "none"
        },
        "Na-Bisulfit": {
            "hasil": "(+) Endapan Putih Kristal",
            "reaksi": r"(CH_3)_2CO + NaHSO_3 \rightarrow (CH_3)_2C(OH)SO_3Na \downarrow",
            "alasan": "Aseton (keton suku rendah) memiliki halangan sterik yang relatif kecil sehingga masih dapat diadisi oleh nukleofil bisulfit membentuk senyawa aduk α-hidroksi sulfonat. Endapan putih terbentuk. Keton suku tinggi dengan halangan sterik besar umumnya tidak bereaksi.",
            "warna_akhir": "#cbd5e1", "efek": "precipitate", "warna_endapan": "#ffffff"
        },
        "Pereaksi Fehling": {
            "hasil": "(-) Tetap Biru",
            "reaksi": r"(CH_3)_2CO + Cu^{2+} \rightarrow \text{Tidak bereaksi}",
            "alasan": "Keton tidak memiliki atom hidrogen terikat langsung pada gugus karbonil, sehingga tidak bersifat reduktor dan tidak dapat mereduksi Cu²⁺ menjadi Cu₂O. Larutan tetap biru. Hasil negatif ini secara definitif membedakan keton dari aldehida.",
            "warna_akhir": "#3b82f6", "efek": "none"
        },
        "Uji Iodoform": {
            "hasil": "(+) Endapan Kuning Iodoform (CHI₃)",
            "reaksi": r"CH_3COCH_3 + 3\ I_2 + 4\ NaOH \rightarrow CHI_3 \downarrow + CH_3COONa + 3\ NaI + 3\ H_2O",
            "alasan": "Aseton adalah metil keton (memiliki gugus –CO–CH₃) sehingga memberikan hasil positif uji iodoform. Iodin dalam NaOH mengiodinasi ketiga atom H pada gugus metil karbonil, diikuti pembelahan ikatan C–C oleh OH⁻ membentuk iodoform (CHI₃) berupa endapan kristal kuning berbau khas.",
            "warna_akhir": "#fef08a", "efek": "precipitate", "warna_endapan": "#facc15"
        },
    },

    # ─────────────────────────────────────────────
    # ETIL ASETAT  (Ester)
    # ─────────────────────────────────────────────
    "Etil Asetat": {
        "Ceric Nitrat": {
            "hasil": "(-) Tetap Jingga",
            "reaksi": r"CH_3COOC_2H_5 + [Ce(NO_3)_6]^{2-} \rightarrow \text{Tidak bereaksi}",
            "alasan": "Etil asetat tidak memiliki gugus –OH bebas. Oksigen ester terikat dalam ikatan kovalen dengan karbon asil dan etil sehingga tidak dapat berkoordinasi dengan Ce(IV). Warna tetap jingga.",
            "warna_akhir": "#f97316", "efek": "none"
        },
        "Na-Bisulfit": {
            "hasil": "(-) Bening — tidak bereaksi",
            "reaksi": r"CH_3COOC_2H_5 + NaHSO_3 \rightarrow \text{Tidak bereaksi}",
            "alasan": "Gugus karbonil ester distabilkan oleh resonansi dari pasangan elektron bebas oksigen (efek mesomeri), sehingga elektrofilisitas karbon karbonilnya jauh berkurang dibandingkan aldehida atau keton. Bisulfit sebagai nukleofil lemah tidak mampu mengadisi karbonil ester. Larutan tetap bening.",
            "warna_akhir": "#f8fafc", "efek": "none"
        },
        "Hidroksilamin (Uji Ester)": {
            "hasil": "(+) Merah Violet — Kompleks Fe(III) Hidroksamat",
            "reaksi": r"CH_3COOC_2H_5 + NH_2OH \rightarrow CH_3CONHOH + C_2H_5OH \quad\text{lalu}\quad 3\ CH_3CONHOH + FeCl_3 \rightarrow Fe(CH_3CONHO)_3 + 3\ HCl",
            "alasan": "Etil asetat bereaksi dengan hidroksilamin (NH₂OH) membentuk asam asetohidroksamat (CH₃CONHOH) melalui reaksi aminolisis. Senyawa hidroksamat kemudian mengkelat ion Fe³⁺ membentuk kompleks oktahedral berwarna merah-violet yang intens. Ini adalah uji spesifik untuk ester dan derivat asam karboksilat.",
            "warna_akhir": "#c026d3", "efek": "none"
        },
    },

    # ─────────────────────────────────────────────
    # ASAM ASETAT  (Asam Karboksilat)
    # ─────────────────────────────────────────────
    "Asam Asetat": {
        "Ceric Nitrat": {
            "hasil": "(-) Tetap Jingga",
            "reaksi": r"CH_3COOH + [Ce(NO_3)_6]^{2-} \rightarrow \text{Tidak bereaksi}",
            "alasan": "Gugus –OH pada asam karboksilat kehilangan karakter nukleofilik karena efek resonansi dengan karbonil (pasangan elektron terdelokalisasi). Oleh sebab itu, –OH pada –COOH tidak dapat membentuk kompleks koordinasi dengan Ce(IV). Warna tetap jingga.",
            "warna_akhir": "#f97316", "efek": "none"
        },
        "Na-Bisulfit": {
            "hasil": "(-) Bening — tidak bereaksi",
            "reaksi": r"CH_3COOH + NaHSO_3 \rightarrow \text{Tidak bereaksi}",
            "alasan": "Asam karboksilat tidak memiliki gugus karbonil yang reaktif terhadap adisi nukleofilik bisulfit. Resonansi gugus –COOH menstabilkan karbon karbonil sehingga tidak rentan terhadap serangan nukleofilik bisulfit. Larutan tetap bening.",
            "warna_akhir": "#f8fafc", "efek": "none"
        },
        "Hidroksilamin (Uji Ester)": {
            "hasil": "(-) Bening / Kuning Pucat — tidak membentuk hidroksamat",
            "reaksi": r"CH_3COOH + NH_2OH + FeCl_3 \rightarrow \text{Tidak terbentuk kompleks violet}",
            "alasan": "Asam karboksilat bebas tidak mengalami aminolisis dengan hidroksilamin pada kondisi uji standar (suhu kamar, tanpa aktivasi) untuk menghasilkan hidroksamat yang cukup untuk membentuk kompleks Fe(III) berwarna violet. Hasil negatif atau sangat lemah ini membedakannya dari ester.",
            "warna_akhir": "#f8fafc", "efek": "none"
        },
        "Uji Barit (NaHCO3)": {
            "hasil": "(+) Gelembung Gas CO₂ → Larutan Barit Keruh",
            "reaksi": r"CH_3COOH + NaHCO_3 \rightarrow CH_3COONa + H_2O + CO_2\uparrow \quad\text{lalu}\quad CO_2 + Ba(OH)_2 \rightarrow BaCO_3\downarrow + H_2O",
            "alasan": "Asam asetat (pKa ≈ 4,75) cukup asam untuk mendeprotonasi NaHCO₃ menghasilkan CO₂. Gelembung gas yang terbentuk dialirkan ke dalam larutan barit [Ba(OH)₂], menyebabkan terbentuknya endapan putih barium karbonat (BaCO₃) yang mengeruhkan larutan. Ini adalah bukti definitif sifat asam yang kuat pada gugus karboksilat.",
            "warna_akhir": "#f8fafc", "efek": "bubbles"
        },
    },

    # ─────────────────────────────────────────────
    # HEKSANA  (Alkana / Hidrokarbon Jenuh)
    # ─────────────────────────────────────────────
    "Heksana": {
        "Ceric Nitrat": {
            "hasil": "(-) Tetap Jingga",
            "reaksi": r"C_6H_{14} + [Ce(NO_3)_6]^{2-} \rightarrow \text{Tidak bereaksi}",
            "alasan": "Heksana adalah senyawa nonpolar inert yang tidak memiliki gugus fungsi apapun. Tidak ada gugus –OH untuk berkoordinasi dengan Ce(IV). Warna jingga tetap tidak berubah.",
            "warna_akhir": "#f97316", "efek": "none"
        },
        "Na-Bisulfit": {
            "hasil": "(-) Bening — tidak bereaksi",
            "reaksi": r"C_6H_{14} + NaHSO_3 \rightarrow \text{Tidak bereaksi}",
            "alasan": "Heksana tidak mengandung gugus karbonil (aldehida, keton, atau ester), sehingga tidak ada situs aktif untuk adisi nukleofilik bisulfit. Larutan tetap bening dan tidak terbentuk endapan.",
            "warna_akhir": "#f8fafc", "efek": "none"
        },
        "Hidroksilamin (Uji Ester)": {
            "hasil": "(-) Bening — tidak bereaksi",
            "reaksi": r"C_6H_{14} + NH_2OH \rightarrow \text{Tidak bereaksi}",
            "alasan": "Heksana tidak memiliki gugus ester atau derivat asam karboksilat yang dapat beraksi dengan hidroksilamin membentuk hidroksamat. Tidak ada perubahan warna saat FeCl₃ ditambahkan.",
            "warna_akhir": "#f8fafc", "efek": "none"
        },
        "Uji Barit (NaHCO3)": {
            "hasil": "(-) Bening — tidak ada gelembung",
            "reaksi": r"C_6H_{14} + NaHCO_3 \rightarrow \text{Tidak bereaksi}",
            "alasan": "Heksana bersifat inert secara kimia dan tidak bersifat asam, sehingga tidak dapat mendeprotonasi NaHCO₃ dan tidak menghasilkan gas CO₂. Larutan barit tetap jernih. Kegagalan di seluruh empat tahap uji gugus fungsi ini secara definitif membuktikan bahwa sampel adalah golongan alkana (hidrokarbon jenuh).",
            "warna_akhir": "#f8fafc", "efek": "none"
        },
    },
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

# Inisialisasi State Sub-Bab agar bisa diganti lewat tombol
if "sub_bab_i" not in st.session_state:
    st.session_state.sub_bab_i = "A. Sifat Fisika Hidrokarbon"
if "sub_bab_ii" not in st.session_state:
    st.session_state.sub_bab_ii = "A. Sifat Fisika & Klasifikasi"
if "sub_bab_iii" not in st.session_state:
    st.session_state.sub_bab_iii = "A. Sifat Fisika"
if "sub_bab_iv" not in st.session_state:
    st.session_state.sub_bab_iv = "A. Sifat Fisika"

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
# 5. LOGIKA KONTEN TIAP HALAMAN
# ==============================================================================

if pilihan_halaman == "🏠 HALAMAN UTAMA":
    st.markdown("""
        <div class="banner-utama">
            <h1 style='color: white; margin-bottom: 5px; font-weight: 700;'>Eksplorasi Dunia Kimia Organik Tanpa Batas! 👋</h1>
            <p style='font-size: 1.2em; opacity: 0.95;'>Solusi cerdas belajar mandiri dan simulasi identifikasi gugus fungsi dalam satu platform.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.subheader("💡 Tentang Platform Ini")
    st.write(
         "Kami hadir untuk menjembatani teori dan praktik. Platform ini dirancang khusus untuk "
        "membantu Anda memahami materi teoretis sekaligus memvisualisasikan reaksi uji kualitatif "
        "senyawa organik secara interaktif—kapan saja dan di mana saja, layaknya memiliki laboratorium pribadi."
    )
    st.markdown("---")
    
    st.markdown("### 📜 Petunjuk Penggunaan")
    st.write("Ikuti langkah-langkah berikut untuk memulai petualangan laboratorium virtualmu:")
    
    p1, p2, p3 = st.columns(3)
    
    with p1:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 12px; border-top: 5px solid #0f766e; box-shadow: 0 4px 6px rgba(0,0,0,0.05); min-height: 180px;">
            <h4 style="margin-top:0; color:#0f766e;">📖 Langkah 1: Pelajari</h4>
            <p style="font-size: 0.95em; color: #475569;">Buka <b>Menu Navigasi</b> di samping kiri. Pilih materi dari <b>BAB I hingga BAB IV</b> untuk membaca teori dasar, sifat fisik/kimia, dan persamaan reaksi kimia senyawa organik.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with p2:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 12px; border-top: 5px solid #14b8a6; box-shadow: 0 4px 6px rgba(0,0,0,0.05); min-height: 180px;">
            <h4 style="margin-top:0; color:#14b8a6;">🧪 Langkah 2: Simulasi</h4>
            <p style="font-size: 0.95em; color: #475569;">Masuk ke menu <b>🔬 POST TEST</b>. Di sana, kamu bisa memilih sampel misterius (<i>Blind Sample</i>) untuk menguji pemahaman analisismu secara langsung.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with p3:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 12px; border-top: 5px solid #0ea5e9; box-shadow: 0 4px 6px rgba(0,0,0,0.05); min-height: 180px;">
            <h4 style="margin-top:0; color:#0ea5e9;">📊 Langkah 3: Amati</h4>
            <p style="font-size: 0.95em; color: #475569;">Klik tombol reaksi, amati perubahan visual pada <b>Visual Lab</b> (warna/endapan/gas), serta baca hasil evaluasi otomatis pada tab <b>Logbook & Analisis</b>.</p>
        </div>
        """, unsafe_allow_html=True)

    st.info("💡 **Tips:** Pastikan koneksi internet stabil agar transisi animasi tabung reaksi berjalan dengan mulus!")

elif pilihan_halaman == "📘 BAB I. HIDROKARBON":
    st.title("📘 BAB I. HIDROKARBON")
    st.write("---")
    
    st.write("**Pilih Sub-Bab Materi:**")
    btn_col1, btn_col2, _ = st.columns([1, 1, 2])
    with btn_col1:
        if st.button("A. Sifat Fisika Hidrokarbon", use_container_width=True):
            st.session_state.sub_bab_i = "A. Sifat Fisika Hidrokarbon"
    with btn_col2:
        if st.button("B. Sifat Kimia & Identifikasi", use_container_width=True):
            st.session_state.sub_bab_i = "B. Sifat Kimia & Reaksi Identifikasi"
    st.write("---")
    
    if st.session_state.sub_bab_i == "A. Sifat Fisika Hidrokarbon":
        st.markdown("""
        #### **A. Sifat Fisika Hidrokarbon**
        Hidrokarbon adalah senyawa organik yang seluruh strukturnya hanya tersusun atas unsur karbon (C) dan hidrogen (H). Berdasarkan jenis ikatannya, hidrokarbon alifatik dibagi menjadi hidrokarbon jenuh (alkana) dan tidak jenuh (alkena dan alkuna). Sementara itu, hidrokarbon aromatik memiliki rantai siklik konjugasi yang sangat stabil.

        * **Wujud Zat (pada suhu kamar):**
          * Suhu rendah ($C_1 - C_4$) berwujud gas (contoh: metana, etana, etena, etuna).
          * Suhu sedang ($C_5 - C_{17}$) berwujud cair (contoh: pentana, heksana, benzena).
          * Suhu tinggi ($\ge C_{18}$) berwujud padat (contoh: parafin padat).
        * **Kelarutan:** Bersifat nonpolar, sehingga tidak larut dalam air (pelarut polar). Hidrokarbon larut dengan baik dalam sesama pelarut organik nonpolar seperti kloroform ($CHCl_3$), karbon tetraklorida ($CCl_4$), atau eter.
        * **Titik Didih dan Titik Leleh:** Meningkat seiring bertambahnya massa molekul (panjang rantai karbon). Untuk isomer dengan jumlah atom karbon sama, senyawa dengan rantai lurus memiliki titik didih lebih tinggi dibandingkan rantai bercabang karena luas permukaan kontak antarmolekul yang lebih besar.
        * **Densitas:** Memiliki massa jenis (densitas) yang lebih kecil daripada air. Jika dicampur dengan air, lapisan hidrokarbon akan selalu berada di bagian atas.
        """)
        
    elif st.session_state.sub_bab_i == "B. Sifat Kimia & Reaksi Identifikasi":
        st.markdown("""
        #### **B. Sifat Kimia & Reaksi Identifikasi Hidrokarbon**
        
        **1. Alkana (Hidrokarbon Jenuh)**
        * Disebut juga parafin (afinitas kecil) karena sangat tidak reaktif terhadap sebagian besar pereaksi seperti asam kuat, basa kuat, dan oksidator pada suhu kamar.
        * **Uji Iodo (Substitusi Halogen):** Alkana dapat bereaksi dengan halogen ($I_2$) melalui reaksi substitusi radikal bebas dengan bantuan paparan sinar ultraviolet (UV) atau pemanasan tinggi.
        """)
        st.latex(r"\text{CH}_4 + \text{I}_2 \xrightarrow{\text{Sinar UV} / \Delta} \text{CH}_3\text{I} + \text{HI}")
        
        st.markdown("""
        **2. Alkena dan Alkuna (Hidrokarbon Tidak Jenuh)**
        * **Uji Adisi Iodium:** Mengadisi halogen pada ikatan rangkap tanpa memerlukan bantuan sinar UV. Ditandai dengan warna ungu iodium yang memudar/hilang seketika.
        """)
        st.latex(r"\text{R-CH}=\text{CH-R} + \text{I}_2 \rightarrow \text{R-CH(I)-CH(I)-R}")
        
        st.markdown("""
        * **Uji Baeyer (Oksidasi dengan $KMnO_4$):** Ditandai dengan hilangnya warna ungu $KMnO_4$ dan terbentuknya endapan cokelat $MnO_2$.
        """)
        st.latex(r"3\text{CH}_2=\text{CH}_2 + 2\text{KMnO}_4 + 4\text{H}_2\text{O} \rightarrow 3\text{HO-CH}_2\text{-CH}_2\text{-OH} + 2\text{MnO}_2\downarrow + 2\text{KOH}")
        
        st.markdown("""
        **3. Benzena (Hidrokarbon Aromatik)**
        * **Uji Bakar:** Menghasilkan nyala api berminyak disertai jelaga hitam tebal.
        * **Reaksi Nitrasi:**
        """)
        st.latex(r"\text{C}_6\text{H}_6 + \text{HNO}_3 \xrightarrow{\text{H}_2\text{SO}_4\text{ pekat}} \text{C}_6\text{H}_5\text{NO}_2 + \text{H}_2\text{O}")

elif pilihan_halaman == "📙 BAB II. ALKOHOL, ETER, DAN FENOL":
    st.title("📙 BAB II. ALKOHOL, ETER, DAN FENOL")
    st.write("---")
    
    st.write("**Pilih Sub-Bab Materi:**")
    btn_col1, btn_col2, btn_col3, _ = st.columns([1.2, 1.2, 1.2, 1])
    with btn_col1:
        if st.button("A. Sifat Fisika & Klasifikasi", use_container_width=True):
            st.session_state.sub_bab_ii = "A. Sifat Fisika & Klasifikasi"
    with btn_col2:
        if st.button("B. Reaksi Alkohol & Eter", use_container_width=True):
            st.session_state.sub_bab_ii = "B. Reaksi Alkohol & Eter"
    with btn_col3:
        if st.button("C. Reaksi Kimia Fenol", use_container_width=True):
            st.session_state.sub_bab_ii = "C. Reaksi Kimia Fenol"
    st.write("---")
    
    if st.session_state.sub_bab_ii == "A. Sifat Fisika & Klasifikasi":
        st.markdown("""
        #### **A. Sifat Fisika & Klasifikasi**
        * **Alkohol ($R - OH$):** Turunan alkana di mana satu atau lebih atom H digantikan oleh gugus hidroksil ($-OH$). Alkohol diklasifikasikan menjadi alkohol primer ($1^\circ$), sekunder ($2^\circ$), dan tersier ($3^\circ$) berdasarkan jenis atom C yang mengikat gugus $-OH$. Alkohol suhu rendah mudah larut dalam air karena sanggup membentuk ikatan hidrogen dengan molekul air.
        * **Eter ($R^1 - O - R^2$):** Isomer fungsional dari alkohol. Titik didih eter jauh lebih rendah dibandingkan alkohol isomernya karena tidak memiliki ikatan hidrogen antar-sesama molekul eter.
        * **Fenol ($C_6H_5OH$):** Senyawa hidrokarbon aromatik yang mengikat gugus fungsi $-OH$ langsung pada cincin benzena. Berupa padatan/hablur pada suhu kamar, sedikit larut dalam air, dan larutannya bersifat asam lemah.
        """)
        
    elif st.session_state.sub_bab_ii == "B. Reaksi Alkohol & Eter":
        st.markdown("""
        #### **B. Persamaan Reaksi Kimia Alkohol & Eter**
        
        **1. Pereaksi Lucas (Substitusi Gugus $-OH$ oleh Cl)**
        """)
        st.latex(r"\text{R}_3\text{C-OH} + \text{HCl} \xrightarrow{\text{ZnCl}_2} \text{R}_3\text{C-Cl}\downarrow \text{ (Keruh)} + \text{H}_2\text{O}")
        
        st.markdown("""
        **2. Pereaksi Jones (Oksidasi Alkohol)**
        """)
        st.latex(r"\text{R-CH}_2\text{-OH} \xrightarrow{\text{CrO}_3/\text{H}_2\text{SO}_4} \text{R-COOH [Jingga } \rightarrow \text{ Hijau]}")
        
        st.markdown("""
        **3. Uji Iodoform**
        """)
        st.latex(r"\text{R-CH(OH)-CH}_3 + 4\text{I}_2 + 6\text{NaOH} \rightarrow \text{R-COONa} + \text{CHI}_3\downarrow + 5\text{NaI} + 5\text{H}_2\text{O}")
        
        st.markdown("""
        **4. Pereaksi Ceric Ammonium Nitrate (CAN)**
        """)
        st.latex(r"\text{ROH} + [\text{Ce(NO}_3)_6]^{2-} \rightarrow [\text{Ce(OR)(NO}_3)_5]^{2-} \text{ (Kompleks Merah)} + \text{HNO}_3")
        
    elif st.session_state.sub_bab_ii == "C. Reaksi Kimia Fenol":
        st.markdown("""
        #### **C. Persamaan Reaksi Kimia Fenol**
        
        **1. Reaksi dengan Basa Kuat ($NaOH$)**
        """)
        st.latex(r"\text{C}_6\text{H}_5\text{OH} + \text{NaOH} \rightarrow \text{C}_6\text{H}_5\text{ONa} + \text{H}_2\text{O}")
        
        st.markdown("""
        **2. Uji Besi(III) Klorida ($FeCl_3$)**
        """)
        st.latex(r"6\text{C}_6\text{H}_5\text{OH} + \text{FeCl}_3 \rightarrow [\text{Fe(OC}_6\text{H}_5)_6]^{3-} + 3\text{H}^+ + 3\text{Cl}^-")
        
        st.markdown("""
        **3. Reaksi Substitusi Aromatik (Trisubstitusi Air Brom)**
        """)
        st.latex(r"\text{C}_6\text{H}_5\text{OH} + 3\text{Br}_2 \rightarrow \text{C}_6\text{H}_2\text{Br}_3\text{OH}\downarrow \text{ (Endapan Putih)} + 3\text{HBr}")

elif pilihan_halaman == "📗 BAB III. ALDEHID DAN KETON":
    st.title("📗 BAB III. ALDEHID DAN KETON")
    st.write("---")
    
    st.write("**Pilih Sub-Bab Materi:**")
    btn_col1, btn_col2, btn_col3, _ = st.columns([1, 1.2, 1.5, 1])
    with btn_col1:
        if st.button("A. Sifat Fisika", use_container_width=True):
            st.session_state.sub_bab_iii = "A. Sifat Fisika"
    with btn_col2:
        if st.button("B. Reaksi Adisi Karbonil", use_container_width=True):
            st.session_state.sub_bab_iii = "B. Reaksi Adisi Karbonil"
    with btn_col3:
        if st.button("C. Reaksi Diferensiasi (Uji Reduksi)", use_container_width=True):
            st.session_state.sub_bab_iii = "C. Reaksi Diferensiasi (Uji Reduksi)"
    st.write("---")
    
    if st.session_state.sub_bab_iii == "A. Sifat Fisika":
        st.markdown("""
        #### **A. Sifat Fisika**
        Aldehida (${R-CHO}$) dan keton (${R-CO-R}'$) adalah senyawa organik isomer fungsional yang sama-sama memiliki gugus fungsi karbonil (${C}={O}$). Perbedaan utamanya terletak pada atom C karbonil aldehida yang mengikat minimal satu atom hidrogen, sedangkan pada keton terikat pada dua gugus alkil/aril.

        Metanal (formaldehida) merupakan suku paling rendah yang berwujud gas pada suhu kamar dengan bau menyengat. Keton suku rendah (seperti aseton atau propanon) berupa cairan encer, mudah larut dalam air, mudah menguap, dan memiliki aroma yang segar.
        """)
        
    elif st.session_state.sub_bab_iii == "B. Reaksi Adisi Karbonil":
        st.markdown("""
        #### **B. Reaksi Adisi Karbonil**
        
        **1. Adisi Natrium Bisulit (${NaHSO}_3$):**
        """)
        st.latex(r"\text{R-CHO} + \text{NaHSO}_3 \rightarrow \text{R-CH(OH)-SO}_3\text{Na}")
        
        st.markdown("""
        **2. Pembentukan Hemiasetal dan Asetal:**
        """)
        st.latex(r"\text{R-CHO} + \text{R'OH} \xrightarrow{\text{HCl}} \text{R-CH(OH)(OR')}")
        st.latex(r"\text{R-CH(OH)(OR')} + \text{R'OH} \xrightarrow{\text{HCl}} \text{R-CH(OR')}_2 + \text{H}_2\text{O}")
        
    elif st.session_state.sub_bab_iii == "C. Reaksi Diferensiasi (Uji Reduksi)":
        st.markdown("""
        #### **C. Reaksi Diferensiasi (Uji Daya Reduksi Aldehida)**
        
        **1. Uji Tollens (Cermin Perak):**
        """)
        st.latex(r"\text{R-CHO} + 2[\text{Ag(NH}_3)_2]^+ + 3\text{OH}^- \rightarrow \text{R-COO}^- + 2\text{Ag}\downarrow + 4\text{NH}_3 + 2\text{H}_2\text{O}")
        
        st.markdown("""
        **2. Uji Fehling:**
        """)
        st.latex(r"\text{R-CHO} + 2\text{Cu}^{2+} + 5\text{OH}^- \rightarrow \text{R-COO}^- + \text{Cu}_2\text{O}\downarrow + 3\text{H}_2\text{O}")
        
        st.markdown("""
        **3. Uji Benedict:**
        """)
        st.latex(r"\text{R-CHO} + 2\text{Cu}^{2+} + 5\text{OH}^- \rightarrow \text{R-COO}^- + \text{Cu}_2\text{O}\downarrow + 3\text{H}_2\text{O}")

elif pilihan_halaman == "📕 BAB IV. ASAM KARBOKSILAT DAN DERIVATNYA":
    st.title("📕 BAB IV. ASAM KARBOKSILAT DAN DERIVATNYA")
    st.write("---")
    
    st.write("**Pilih Sub-Bab Materi:**")
    btn_col1, btn_col2, btn_col3, _ = st.columns([1, 1.5, 1.5, 1])
    with btn_col1:
        if st.button("A. Sifat Fisika", use_container_width=True):
            st.session_state.sub_bab_iv = "A. Sifat Fisika"
    with btn_col2:
        if st.button("B. Reaksi Kimia Asam Karboksilat", use_container_width=True):
            st.session_state.sub_bab_iv = "B. Reaksi Kimia Asam Karboksilat"
    with btn_col3:
        if st.button("C. Identifikasi Derivat (Ester)", use_container_width=True):
            st.session_state.sub_bab_iv = "C. Identifikasi Derivat (Ester)"
    st.write("---")
    
    if st.session_state.sub_bab_iv == "A. Sifat Fisika":
        st.markdown("""
        #### **A. Sifat Fisika**
        Asam karboksilat memiliki gugus fungsi karboksil ($-{COOH}$). Asam karboksilat rantai pendek ($C_1 - C_4$) memiliki kelarutan yang sangat baik di dalam air. Titik didih asam karboksilat relatif tinggi dibandingkan senyawa organik lain dengan berat molekul setara.
        """)
        
    elif st.session_state.sub_bab_iv == "B. Reaksi Kimia Asam Karboksilat":
        st.markdown("""
        #### **B. Persamaan Reaksi Kimia Asam Karboksilat**
        
        **1. Reaksi dengan Basa Kuat (${NaOH}$):**
        """)
        st.latex(r"\text{R-COOH} + \text{NaOH} \rightarrow \text{R-COONa} + \text{H}_2\text{O}")
        
        st.markdown("""
        **2. Reaksi dengan Basa Lemah (${NaHCO}_3$):**
        """)
        st.latex(r"\text{R-COOH} + \text{NaHCO}_3 \rightarrow \text{R-COONa} + \text{H}_2\text{O} + \text{CO}_2\uparrow")
        st.latex(r"\text{CO}_2 + \text{Ba(OH)}_2 \rightarrow \text{BaCO}_3\downarrow + \text{H}_2\text{O}")
        
        st.markdown("""
        **3. Esterifikasi Fischer:**
        """)
        st.latex(r"\text{R-COOH} + \text{R'-OH} \xrightarrow{\text{H}_2\text{SO}_4, \Delta} \text{R-COOR'} + \text{H}_2\text{O}")
        
    elif st.session_state.sub_bab_iv == "C. Identifikasi Derivat (Ester)":
        st.markdown("""
        #### **C. Persamaan Reaksi Identifikasi Derivat Asam Karboksilat (Uji Asam Hidroksamat)**
        
        *Pembentukan Asam Hidroksamat dari Ester:*
        """)
        st.latex(r"\text{R-COOR'} + \text{NH}_2\text{OH} \rightarrow \text{R-CONH-OH} + \text{R'-OH}")
        
        st.markdown("""
        *Pembentukan Kompleks Khelat Ungu dengan ${FeCl}_3$:*
        """)
        st.latex(r"3\text{R-CONH-OH} + \text{FeCl}_3 \rightarrow \text{Fe(R-CONHO)}_3 + 3\text{HCl}")

# ==============================================================================
# 6. HALAMAN POST TEST (SIMULASI LANGKAH DEMI LANGKAH)
# ==============================================================================
elif pilihan_halaman == "🔬 POST TEST":
    st.title("🔀 Asisten Identifikasi Cerdas (Step-by-Step)")
    st.write("Sistem ini mensimulasikan penelusuran Identifikasi Kualitatif langkah demi langkah. Tekan tombol **Lanjut** untuk melanjutkan ke tahap reaksi berikutnya.")

    if not st.session_state.test_started:
        st.divider()
        senyawa = st.selectbox(
            "Pilih Senyawa yang Akan Diuji (Sebagai *Blind Sample*):",
            ["-- Pilih Senyawa --"] + list(flowchart_paths.keys())
        )
        if st.button("Mulai Identifikasi 🚀", type="primary"):
            if senyawa == "-- Pilih Senyawa --":
                st.warning("⚠️ Harap pilih komponen senyawa terlebih dahulu!")
            else:
                st.session_state.test_started = True
                st.session_state.senyawa_uji = senyawa
                st.session_state.current_step = 0
                st.session_state.log_history = []
                st.session_state.trigger_animation = True
                force_rerun()

    else:
        st.write("---")
        senyawa = st.session_state.senyawa_uji
        urutan = flowchart_paths[senyawa]

        col_visual, col_log = st.columns([1, 2.5])
        
        with col_visual:
            st.markdown("<h4 style='text-align: center;'>Visual Lab</h4>", unsafe_allow_html=True)
            
            reagent_tag_placeholder = st.empty()
            tube_placeholder = st.empty() 
            status_placeholder = st.empty()
            
            st.write("")
            if st.button("⏹️ Stop & Pilih Reagen/Sampel Ulang", use_container_width=True, type="secondary"):
                st.session_state.test_started = False
                st.session_state.current_step = 0
                st.session_state.log_history = []
                st.session_state.trigger_animation = False
                force_rerun()
            
        with col_log:
            st.markdown("#### 📑 Logbook & Analisis Teoritis")
            log_container = st.container()

        with log_container:
            for log in st.session_state.log_history:
                if "(+)" in log["hasil"]:
                    st.success(f"**Tahap {log['step']}: {log['pereaksi']}** ➔ **{log['hasil']}**")
                    st.latex(log['reaksi'])
                    st.write(f"**Pembahasan:** {log['alasan']}")
                else:
                    st.error(f"**Tahap {log['step']}: {log['pereaksi']}** ➔ **{log['hasil']}**")
                    st.latex(log['reaksi'])
                    st.write(f"**Pembahasan:** {log['alasan']}")

        if st.session_state.trigger_animation and st.session_state.current_step < len(urutan):
            pereaksi = urutan[st.session_state.current_step]
            
            reagent_tag_placeholder.markdown(f"<div class='reagent-tag'>🧪 Pereaksi: {pereaksi}</div>", unsafe_allow_html=True)
            tube_placeholder.markdown(render_tube("30%", "#f1f5f9", "none"), unsafe_allow_html=True)
            status_placeholder.markdown("<div style='text-align:center;'><em>Menyiapkan sampel untuk analisis...</em></div>", unsafe_allow_html=True)
            time.sleep(1.0)
            
            warna_reagen = reagen_colors.get(pereaksi, "#f8fafc")
            tube_placeholder.markdown(render_tube("65%", warna_reagen, "none"), unsafe_allow_html=True)
            status_placeholder.markdown("<div style='text-align:center;'><em>Mereaksikan komponen senyawa...</em></div>", unsafe_allow_html=True)
            time.sleep(1.5)
            
            res = database_reaksi[senyawa][pereaksi]
            w_endapan = res.get("warna_endapan", None)
            tube_placeholder.markdown(render_tube("65%", res["warna_akhir"], res["efek"], warna_endapan=w_endapan), unsafe_allow_html=True)
            status_placeholder.markdown("<div style='text-align:center; font-weight:bold;'>Mengamati pengendapan & perubahan warna...</div>", unsafe_allow_html=True)
            time.sleep(1.2)
            
            st.session_state.log_history.append({
                "step": st.session_state.current_step + 1,
                "pereaksi": pereaksi,
                "hasil": res["hasil"],
                "reaksi": res["reaksi"],
                "alasan": res["alasan"]
            })
            
            st.session_state.current_step += 1
            st.session_state.trigger_animation = False
            force_rerun()

        elif not st.session_state.trigger_animation:
            if st.session_state.current_step > 0:
                last_pereaksi = urutan[st.session_state.current_step - 1]
                reagent_tag_placeholder.markdown(f"<div class='reagent-tag'>🧪 Pereaksi: {last_pereaksi}</div>", unsafe_allow_html=True)
                res = database_reaksi[senyawa][last_pereaksi]
                w_endapan = res.get("warna_endapan", None)
                tube_placeholder.markdown(render_tube("65%", res["warna_akhir"], res["efek"], warna_endapan=w_endapan), unsafe_allow_html=True)
            
            if st.session_state.current_step < len(urutan):
                next_pereaksi = urutan[st.session_state.current_step]
                status_placeholder.markdown("<div style='text-align:center; color:#475569;'>Menunggu konfirmasi data...</div>", unsafe_allow_html=True)
                
                with col_visual:
                    if st.button(f"Lanjutkan ke {next_pereaksi} ⏭️", use_container_width=True, type="primary"):
                        st.session_state.trigger_animation = True
                        force_rerun()
                        
            else:
                reagent_tag_placeholder.markdown("<div class='reagent-tag' style='background-color:#d1fae5; color:#065f46;'>🏁 Identifikasi Selesai</div>", unsafe_allow_html=True)
                status_placeholder.markdown("<div style='text-align:center; font-weight:bold; color:#10b981;'>Rangkaian uji selesai!</div>", unsafe_allow_html=True)
                with log_container:
                    st.info(f"🎉 **KESIMPULAN AKHIR:** Sampel ini terbukti sah merupakan golongan **{senyawa.upper()}**.")
                
                with col_visual:
                    if st.button("🔄 Uji Golongan Senyawa Lain", use_container_width=True):
                        st.session_state.test_started = False
                        force_rerun()
