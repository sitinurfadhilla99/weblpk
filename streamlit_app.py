import streamlit as st
import time

# ==============================================================================
# 1. KONFIGURASI HALAMAN
# ==============================================================================
st.set_page_config(
    page_title="OrganicChem | Platform Edu-Lab",
    page_icon="🧪",
    layout="wide"
)

# ==============================================================================
# 2. CUSTOM CSS INTERAKTIF — TEMA TEAL/EMERALD SENADA
# ==============================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

    /* ── WARNA UTAMA (CSS Variables) ── */
    :root {
        --teal-50:  #f0fdfa;
        --teal-100: #ccfbf1;
        --teal-200: #99f6e4;
        --teal-400: #2dd4bf;
        --teal-500: #14b8a6;
        --teal-600: #0d9488;
        --teal-700: #0f766e;
        --teal-800: #115e59;
        --teal-900: #134e4a;
        --amber-400: #fbbf24;
        --amber-500: #f59e0b;
        --slate-50:  #f8fafc;
        --slate-100: #f1f5f9;
        --slate-200: #e2e8f0;
        --slate-600: #475569;
        --slate-700: #334155;
        --slate-800: #1e293b;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    /* ── SIDEBAR ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--teal-900) 0%, var(--teal-800) 60%, var(--teal-700) 100%) !important;
    }
    [data-testid="stSidebar"] * {
        color: #e0f2fe !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        color: var(--teal-100) !important;
        font-weight: 500;
    }
    [data-testid="stSidebar"] [data-baseweb="radio"] div[aria-checked="true"] ~ span {
        color: var(--amber-400) !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: var(--teal-600) !important;
    }

    /* ── MAIN BACKGROUND ── */
    .stApp {
        background: linear-gradient(135deg, #f0fdfa 0%, #f8fafc 50%, #ecfdf5 100%);
    }

    /* ── BANNER UTAMA ── */
    .banner-utama {
        background: linear-gradient(135deg, var(--teal-800) 0%, var(--teal-600) 60%, #0891b2 100%);
        padding: 40px 45px;
        border-radius: 16px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 8px 32px rgba(13, 148, 136, 0.25);
        position: relative;
        overflow: hidden;
    }
    .banner-utama::before {
        content: '⬡';
        position: absolute;
        right: 40px; top: 10px;
        font-size: 120px;
        opacity: 0.08;
        color: white;
    }

    /* ── KOTAK ANALISIS ── */
    .kotak-analisis {
        border-left: 5px solid var(--teal-500);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 18px;
        background: white;
        box-shadow: 0 2px 12px rgba(13, 148, 136, 0.08);
    }
    .label-analisis {
        font-weight: 700;
        color: var(--teal-700);
        font-size: 1.1em;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        margin-bottom: 6px;
        font-family: 'Space Mono', monospace;
    }

    /* ── JUDUL HALAMAN ── */
    h1 { color: var(--teal-800) !important; font-family: 'DM Sans', sans-serif !important; font-weight: 700 !important; }
    h2 { color: var(--teal-700) !important; font-family: 'DM Sans', sans-serif !important; }
    h3 { color: var(--teal-700) !important; }
    h4 { color: var(--teal-800) !important; }

    /* ── TOMBOL ── */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--teal-600), var(--teal-500)) !important;
        border: none !important;
        color: white !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 14px rgba(13, 148, 136, 0.3) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, var(--teal-700), var(--teal-600)) !important;
        box-shadow: 0 6px 20px rgba(13, 148, 136, 0.4) !important;
        transform: translateY(-1px) !important;
    }
    .stButton > button[kind="secondary"] {
        background: white !important;
        border: 2px solid var(--teal-400) !important;
        color: var(--teal-700) !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background: var(--teal-50) !important;
        border-color: var(--teal-600) !important;
    }

    /* ── TOMBOL BAHAYA (ganti sampel) ── */
    .ganti-sampel-btn > button {
        background: linear-gradient(135deg, #dc2626, #b91c1c) !important;
        border: none !important;
        color: white !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 14px rgba(220, 38, 38, 0.25) !important;
    }

    /* ── SELECT BOX ── */
    [data-baseweb="select"] {
        border-radius: 10px !important;
    }

    /* ── SUCCESS / ERROR BOX ── */
    .stSuccess { background: var(--teal-50) !important; border-color: var(--teal-400) !important; }
    .stAlert { border-radius: 10px !important; }

    /* ── DIVIDER ── */
    hr { border-color: var(--teal-200) !important; }

    /* ── TABUNG REAKSI 2D ── */
    .tube-wrap {
        display: flex;
        justify-content: center;
        height: 380px;
        padding-top: 20px;
        flex-direction: column;
        align-items: center;
        gap: 8px;
    }
    .tube-label {
        font-family: 'Space Mono', monospace;
        font-size: 0.75em;
        color: var(--teal-700);
        font-weight: 700;
        text-align: center;
        letter-spacing: 0.5px;
    }
    .tube-outer {
        position: relative;
        width: 88px;
    }
    .tube-cap {
        width: 100px;
        height: 14px;
        background: linear-gradient(180deg, #cbd5e1, #94a3b8);
        border-radius: 6px 6px 0 0;
        margin: 0 auto 0;
        border: 2px solid #94a3b8;
        border-bottom: none;
    }
    .tube-glass {
        width: 80px;
        height: 280px;
        border: 3px solid #94a3b8;
        border-top: 2px solid #cbd5e1;
        border-radius: 0 0 40px 40px;
        position: relative;
        overflow: hidden;
        background: linear-gradient(100deg, rgba(255,255,255,0.4) 0%, rgba(255,255,255,0.05) 50%, rgba(255,255,255,0.15) 100%);
        box-shadow: inset -6px 0 12px rgba(255,255,255,0.3), 0 4px 20px rgba(0,0,0,0.08);
    }
    /* Kilap kaca */
    .tube-glass::after {
        content: '';
        position: absolute;
        top: 0; left: 6px;
        width: 12px;
        height: 100%;
        background: linear-gradient(180deg, rgba(255,255,255,0.55) 0%, rgba(255,255,255,0.05) 100%);
        border-radius: 6px;
        pointer-events: none;
        z-index: 10;
    }
    .tube-liquid {
        position: absolute;
        bottom: 0; left: 0; right: 0;
        transition: height 1.2s cubic-bezier(.4,0,.2,1), background 1.2s ease;
    }

    /* ── ENDAPAN REALISTIS ── */
    .precipitate-layer {
        position: absolute;
        bottom: 0; left: 0; right: 0;
        height: 0;
        animation: settleDown 2.5s ease-out forwards;
        overflow: hidden;
    }
    @keyframes settleDown {
        0%   { height: 0; opacity: 0; }
        30%  { height: 30px; opacity: 0.6; }
        60%  { height: 22px; opacity: 0.85; }
        100% { height: 28px; opacity: 1; }
    }
    .precipitate-body {
        position: absolute;
        bottom: 0; left: 0; right: 0;
        height: 28px;
        background: linear-gradient(180deg,
            rgba(255,255,255,0) 0%,
            rgba(220,220,220,0.5) 25%,
            rgba(245,245,245,0.85) 55%,
            rgba(255,255,255,0.98) 100%
        );
    }
    .precipitate-particles {
        position: absolute;
        bottom: 0; left: 0; right: 0;
        height: 60px;
        overflow: hidden;
    }
    .particle {
        position: absolute;
        background: rgba(255,255,255,0.9);
        border-radius: 50%;
        animation: fallParticle linear forwards;
    }
    @keyframes fallParticle {
        0%   { transform: translateY(-80px) translateX(0px); opacity: 0.9; }
        80%  { opacity: 0.8; }
        100% { transform: translateY(0px) translateX(var(--dx, 0px)); opacity: 0.6; }
    }
    .cloud-particle {
        position: absolute;
        background: rgba(255,255,255,0.6);
        border-radius: 50%;
        animation: floatCloud 3s ease-in-out infinite alternate;
    }
    @keyframes floatCloud {
        0%   { transform: translateY(0px) scale(1); opacity: 0.5; }
        100% { transform: translateY(-10px) scale(1.1); opacity: 0.3; }
    }

    /* ── EFEK KERUH ── */
    .cloudy-layer {
        position: absolute;
        top: 0; bottom: 0; left: 0; right: 0;
        background: radial-gradient(ellipse at 50% 40%, rgba(255,255,255,0.7) 0%, rgba(255,255,255,0.3) 60%, transparent 100%);
        animation: cloudyPulse 2s ease-in-out infinite alternate;
    }
    @keyframes cloudyPulse {
        0%   { opacity: 0.6; }
        100% { opacity: 0.9; }
    }

    /* ── EFEK GELEMBUNG ── */
    .bubble-fx {
        position: absolute;
        background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.9), rgba(255,255,255,0.2));
        border-radius: 50%;
        border: 1px solid rgba(255,255,255,0.5);
        width: 8px; height: 8px;
        animation: floatUp 1.8s infinite ease-in;
    }
    .bubble-fx.b2 { width: 5px; height: 5px; animation-delay: 0.4s; }
    .bubble-fx.b3 { width: 10px; height: 10px; animation-delay: 0.9s; }
    @keyframes floatUp {
        0%   { bottom: 0px; opacity: 1; transform: translateX(0); }
        50%  { transform: translateX(4px); }
        100% { bottom: 240px; opacity: 0; transform: translateX(-4px); }
    }

    /* ── BADGE GOLONGAN ── */
    .golongan-badge {
        display: inline-block;
        background: linear-gradient(135deg, var(--teal-600), var(--teal-500));
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8em;
        font-weight: 600;
        letter-spacing: 0.4px;
        margin-bottom: 6px;
    }

    /* ── STEP INDICATOR ── */
    .step-indicator {
        display: flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 12px;
        flex-wrap: wrap;
    }
    .step-dot {
        width: 28px; height: 28px;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 0.72em; font-weight: 700;
        font-family: 'Space Mono', monospace;
        transition: all 0.3s ease;
    }
    .step-dot.done    { background: var(--teal-500); color: white; }
    .step-dot.active  { background: var(--amber-500); color: white; box-shadow: 0 0 0 3px rgba(245,158,11,0.3); }
    .step-dot.pending { background: var(--slate-200); color: var(--slate-600); }
    .step-line { width: 18px; height: 3px; border-radius: 2px; background: var(--teal-200); }
    .step-line.done { background: var(--teal-400); }

    /* ── INFO BOX ── */
    .info-box {
        background: linear-gradient(135deg, var(--teal-50), white);
        border: 1px solid var(--teal-200);
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 12px;
    }

    /* ── KESIMPULAN ── */
    .kesimpulan-box {
        background: linear-gradient(135deg, var(--teal-700), var(--teal-600));
        color: white;
        padding: 24px 28px;
        border-radius: 14px;
        box-shadow: 0 8px 24px rgba(13, 148, 136, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. FUNGSI HELPER & SIMULASI TABUNG
# ==============================================================================
def force_rerun():
    if hasattr(st, 'rerun'):
        st.rerun()
    elif hasattr(st, 'experimental_rerun'):
        st.experimental_rerun()
    else:
        st.warning("⚠️ Versi Streamlit usang. Silakan refresh halaman secara manual (F5).")

def render_tube(tinggi, warna, efek, label=""):
    e_html = ""
    if efek == "endapan":
        # Partikel yang berjatuhan lalu mengendap — lebih realistis
        particles_html = ""
        particle_configs = [
            {"left": 10, "size": 4, "delay": 0.1, "dur": 1.4, "dx": 3},
            {"left": 20, "size": 6, "delay": 0.3, "dur": 1.7, "dx": -4},
            {"left": 32, "size": 3, "delay": 0.5, "dur": 1.3, "dx": 2},
            {"left": 42, "size": 7, "delay": 0.2, "dur": 1.9, "dx": -2},
            {"left": 52, "size": 5, "delay": 0.6, "dur": 1.5, "dx": 5},
            {"left": 60, "size": 4, "delay": 0.4, "dur": 1.6, "dx": -3},
            {"left": 68, "size": 6, "delay": 0.15, "dur": 1.8, "dx": 1},
            {"left": 15, "size": 3, "delay": 0.7, "dur": 1.2, "dx": 4},
            {"left": 50, "size": 4, "delay": 0.8, "dur": 2.0, "dx": -5},
            {"left": 38, "size": 5, "delay": 0.9, "dur": 1.4, "dx": 3},
        ]
        for p in particle_configs:
            particles_html += f"""
                <div class='particle' style='
                    left:{p["left"]}%; width:{p["size"]}px; height:{p["size"]}px;
                    animation-duration:{p["dur"]}s; animation-delay:{p["delay"]}s;
                    --dx:{p["dx"]}px; bottom:0;
                '></div>"""
        # Layer awan kecil di dalam cairan (partikel melayang)
        cloud_html = ""
        cloud_positions = [
            {"left": 15, "size": 18, "top": "55%", "delay": 0},
            {"left": 55, "size": 14, "top": "40%", "delay": 0.8},
            {"left": 35, "size": 20, "top": "70%", "delay": 0.4},
            {"left": 70, "size": 12, "top": "60%", "delay": 1.1},
        ]
        for c in cloud_positions:
            cloud_html += f"""
                <div class='cloud-particle' style='
                    left:{c["left"]}%; width:{c["size"]}px; height:{c["size"]}px;
                    top:{c["top"]}; animation-delay:{c["delay"]}s;
                '></div>"""
        e_html = f"""
            <div class='precipitate-particles'>{particles_html}</div>
            {cloud_html}
            <div class='precipitate-layer'>
                <div class='precipitate-body'></div>
            </div>
        """
    elif efek == "keruh":
        e_html = "<div class='cloudy-layer'></div>"
    elif efek == "gelembung":
        e_html = """
            <div class='bubble-fx' style='left:15px;'></div>
            <div class='bubble-fx b2' style='left:38px;'></div>
            <div class='bubble-fx b3' style='left:56px; animation-delay:0.7s;'></div>
        """
    label_html = f"<div class='tube-label'>{label}</div>" if label else ""
    return f"""
    <div class='tube-wrap'>
        {label_html}
        <div class='tube-outer'>
            <div class='tube-cap'></div>
            <div class='tube-glass'>
                <div class='tube-liquid' style='height:{tinggi}; background:{warna};'>{e_html}</div>
            </div>
        </div>
    </div>"""

reagen_colors = {
    "Ceric Nitrat": "#facc15",
    "Pereaksi Jones": "#f97316",
    "Pereaksi Lucas": "#e2e8f0",
    "Pereaksi Lucas (Panas)": "#e2e8f0",
    "Na-Bisulfit": "#f1f5f9",
    "Pereaksi Fehling": "#3b82f6",
    "Pereaksi Schiff": "#fdf4ff",
    "Uji Iodoform": "#fef9c3",
    "Hidroksilamin (Uji Ester)": "#f0fdf4",
    "Uji Barit (NaHCO3)": "#f8fafc"
}

# ── Nama Golongan untuk Post Test ──
nama_golongan = {
    "1-Butanol":       "Alkohol Primer (1°)",
    "2-Butanol":       "Alkohol Sekunder (2°)",
    "t-Butil Alkohol": "Alkohol Tersier (3°)",
    "Formaldehida":    "Aldehid (Aldehida Alifatik)",
    "Aseton":          "Keton (Metil Keton)",
    "Etil Asetat":     "Ester (Etil Ester)",
    "Asam Asetat":     "Asam Karboksilat (Asam Alifatik)",
    "Heksana":         "Alkana (Hidrokarbon Jenuh)"
}

# Deskripsi golongan
deskripsi_golongan = {
    "1-Butanol":       "Sampel mengandung gugus –OH pada karbon primer (–CH₂OH)",
    "2-Butanol":       "Sampel mengandung gugus –OH pada karbon sekunder (–CHOH–)",
    "t-Butil Alkohol": "Sampel mengandung gugus –OH pada karbon tersier (–COH–)",
    "Formaldehida":    "Sampel mengandung gugus karbonil –CHO pada karbon terkecil (H–CHO)",
    "Aseton":          "Sampel mengandung gugus karbonil –C(=O)– dengan dua gugus metil",
    "Etil Asetat":     "Sampel mengandung gugus –COO– (ester) dengan gugus etil",
    "Asam Asetat":     "Sampel mengandung gugus –COOH (karboksil) alifatik rantai pendek",
    "Heksana":         "Sampel adalah rantai karbon lurus tanpa gugus fungsi aktif"
}

flowchart_paths = {
    "1-Butanol": ["Ceric Nitrat", "Pereaksi Jones", "Pereaksi Lucas (Panas)"],
    "2-Butanol": ["Ceric Nitrat", "Pereaksi Jones", "Pereaksi Lucas (Panas)", "Uji Iodoform"],
    "t-Butil Alkohol": ["Ceric Nitrat", "Pereaksi Jones", "Pereaksi Lucas"],
    "Formaldehida": ["Ceric Nitrat", "Na-Bisulfit", "Pereaksi Fehling", "Pereaksi Schiff"],
    "Aseton": ["Ceric Nitrat", "Na-Bisulfit", "Pereaksi Fehling", "Uji Iodoform"],
    "Etil Asetat": ["Ceric Nitrat", "Na-Bisulfit", "Hidroksilamin (Uji Ester)"],
    "Asam Asetat": ["Ceric Nitrat", "Na-Bisulfit", "Hidroksilamin (Uji Ester)", "Uji Barit (NaHCO3)"],
    "Heksana": ["Ceric Nitrat", "Na-Bisulfit", "Hidroksilamin (Uji Ester)", "Uji Barit (NaHCO3)"]
}

database_reaksi = {
    "1-Butanol": {
        "Ceric Nitrat": {
            "hasil": "(+) Merah Ceri",
            "reaksi": r"\text{R-OH} + [\text{Ce(NO}_3)_6]^{2-} \rightarrow [\text{Ce(OR)(NO}_3)_5]^{2-} + \text{HNO}_3",
            "alasan": "Gugus -OH bebas dari 1-butanol bereaksi menggantikan ligan nitrat pada ion Cerium(IV) membentuk senyawa kompleks koordinasi yang berwarna merah ceri.",
            "warna_akhir": "#ef4444", "efek": "tidak_ada"
        },
        "Pereaksi Jones": {
            "hasil": "(+) Hijau",
            "reaksi": r"3\text{R-CH}_2\text{-OH} + 2\text{CrO}_3 + 3\text{H}_2\text{SO}_4 \rightarrow 3\text{R-COOH} + \text{Cr}_2(\text{SO}_4)_3 + 6\text{H}_2\text{O}",
            "alasan": "1-butanol adalah alkohol primer yang dioksidasi kuat menjadi asam karboksilat. Kromium(VI) jingga tereduksi menjadi Kromium(III) hijau.",
            "warna_akhir": "#10b981", "efek": "tidak_ada"
        },
        "Pereaksi Lucas (Panas)": {
            "hasil": "(-) Bening",
            "reaksi": r"\text{R-CH}_2\text{-OH} + \text{HCl} \xrightarrow{\text{ZnCl}_2, \Delta} \text{Tidak terjadi reaksi}",
            "alasan": "Karbokation primer sangat tidak stabil. Reaksi SN1 tidak berjalan bahkan setelah dibantu pemanasan.",
            "warna_akhir": "#e8f4f8", "efek": "tidak_ada"
        }
    },
    "2-Butanol": {
        "Ceric Nitrat": {
            "hasil": "(+) Merah Ceri",
            "reaksi": r"\text{R-OH} + [\text{Ce(NO}_3)_6]^{2-} \rightarrow [\text{Ce(OR)(NO}_3)_5]^{2-} + \text{HNO}_3",
            "alasan": "Ikatan koordinasi terbentuk antara atom oksigen gugus hidroksil sekunder dengan logam Cerium pusat menghasilkan warna merah.",
            "warna_akhir": "#ef4444", "efek": "tidak_ada"
        },
        "Pereaksi Jones": {
            "hasil": "(+) Hijau",
            "reaksi": r"3\text{R}_2\text{CH-OH} + 2\text{CrO}_3 + 3\text{H}_2\text{SO}_4 \rightarrow 3\text{R}_2\text{C}=\text{O} + \text{Cr}_2(\text{SO}_4)_3 + 6\text{H}_2\text{O}",
            "alasan": "2-butanol dioksidasi menjadi keton. Cr(VI) jingga tereduksi ke Cr(III) hijau.",
            "warna_akhir": "#10b981", "efek": "tidak_ada"
        },
        "Pereaksi Lucas (Panas)": {
            "hasil": "(+) Emulsi Putih",
            "reaksi": r"\text{R}_2\text{CH-OH} + \text{HCl} \xrightarrow{\text{ZnCl}_2} \text{R}_2\text{CH-Cl}\downarrow + \text{H}_2\text{O}",
            "alasan": "Karbokation sekunder memiliki stabilitas menengah. Reaksi butuh pemanasan menghasilkan alkil klorida yang mengeruhkan larutan.",
            "warna_akhir": "#c8e6f0", "efek": "keruh"
        },
        "Uji Iodoform": {
            "hasil": "(+) Endapan Kuning",
            "reaksi": r"\text{R-CH(OH)-CH}_3 + 4\text{I}_2 + 6\text{NaOH} \rightarrow \text{CHI}_3\downarrow + \text{R-COONa} + 5\text{NaI} + 5\text{H}_2\text{O}",
            "alasan": "2-Butanol adalah metil karbinol yang dioksidasi iodin menjadi metil keton. Gugus metil tersubstitusi membentuk kristal iodoform kuning.",
            "warna_akhir": "#fde047", "efek": "endapan"
        }
    },
    "t-Butil Alkohol": {
        "Ceric Nitrat": {
            "hasil": "(+) Merah Ceri",
            "reaksi": r"\text{R-OH} + [\text{Ce(NO}_3)_6]^{2-} \rightarrow [\text{Ce(OR)(NO}_3)_5]^{2-} + \text{HNO}_3",
            "alasan": "Terdapat gugus -OH bebas yang berikatan koordinasi membentuk kompleks merah.",
            "warna_akhir": "#ef4444", "efek": "tidak_ada"
        },
        "Pereaksi Jones": {
            "hasil": "(-) Tetap Jingga",
            "reaksi": r"\text{R}_3\text{C-OH} + \text{CrO}_3 + \text{H}^+ \rightarrow \text{Tidak bereaksi}",
            "alasan": "Alkohol tersier tidak memiliki atom hidrogen alfa — tidak bisa dioksidasi oleh reagen Jones.",
            "warna_akhir": "#f97316", "efek": "tidak_ada"
        },
        "Pereaksi Lucas": {
            "hasil": "(+) Emulsi Putih (Seketika)",
            "reaksi": r"\text{R}_3\text{C-OH} + \text{HCl} \xrightarrow{\text{ZnCl}_2} \text{R}_3\text{C-Cl}\downarrow + \text{H}_2\text{O}",
            "alasan": "Karbokation tersier sangat stabil. Reaksi SN1 terjadi seketika menghasilkan endapan alkil klorida.",
            "warna_akhir": "#c8dde8", "efek": "keruh"
        }
    },
    "Formaldehida": {
        "Ceric Nitrat": {
            "hasil": "(-) Kuning",
            "reaksi": r"\text{HCHO} + [\text{Ce(NO}_3)_6]^{2-} \rightarrow \text{Tidak bereaksi}",
            "alasan": "Formaldehida adalah aldehid dan tidak memiliki gugus hidroksil bebas.",
            "warna_akhir": "#facc15", "efek": "tidak_ada"
        },
        "Na-Bisulfit": {
            "hasil": "(+) Endapan Putih",
            "reaksi": r"\text{H-CHO} + \text{NaHSO}_3 \rightarrow \text{H}_2\text{C(OH)SO}_3\text{Na}\downarrow",
            "alasan": "Nukleofil bisulfit menyerang karbonil yang miskin elektron membentuk garam padatan kristal putih.",
            "warna_akhir": "#dde8f0", "efek": "endapan"
        },
        "Pereaksi Fehling": {
            "hasil": "(+) Merah Bata",
            "reaksi": r"\text{H-CHO} + 2\text{Cu}^{2+} + 5\text{OH}^- \rightarrow \text{H-COO}^- + \text{Cu}_2\text{O}\downarrow + 3\text{H}_2\text{O}",
            "alasan": "Aldehid mereduksi Tembaga(II) biru menjadi endapan Tembaga(I) oksida merah bata.",
            "warna_akhir": "#b91c1c", "efek": "endapan"
        },
        "Pereaksi Schiff": {
            "hasil": "(+) Ungu / Magenta",
            "reaksi": r"\text{Aldehida} + \text{Reagen Schiff} \rightarrow \text{Kompleks warna magenta}",
            "alasan": "Reaksi adisi spesifik memulihkan pewarna p-rosanilin hidroklorida.",
            "warna_akhir": "#d946ef", "efek": "tidak_ada"
        }
    },
    "Aseton": {
        "Ceric Nitrat": {
            "hasil": "(-) Kuning",
            "reaksi": r"\text{CH}_3\text{COCH}_3 + [\text{Ce(NO}_3)_6]^{2-} \rightarrow \text{Tidak bereaksi}",
            "alasan": "Keton tidak memiliki gugus hidroksil alkoholik.",
            "warna_akhir": "#facc15", "efek": "tidak_ada"
        },
        "Na-Bisulfit": {
            "hasil": "(+) Endapan Putih",
            "reaksi": r"\text{CH}_3\text{-CO-CH}_3 + \text{NaHSO}_3 \rightarrow (\text{CH}_3)_2\text{C(OH)SO}_3\text{Na}\downarrow",
            "alasan": "Aseton dengan halangan sterik rendah mengalami adisi membentuk garam bisulfit berupa padatan.",
            "warna_akhir": "#dde8f0", "efek": "endapan"
        },
        "Pereaksi Fehling": {
            "hasil": "(-) Tetap Biru",
            "reaksi": r"\text{CH}_3\text{-CO-CH}_3 + \text{Cu}^{2+} \rightarrow \text{Tidak direduksi}",
            "alasan": "Keton tidak memiliki sifat reduktor karena tidak ada H pada karbon karbonil.",
            "warna_akhir": "#3b82f6", "efek": "tidak_ada"
        },
        "Uji Iodoform": {
            "hasil": "(+) Endapan Kuning",
            "reaksi": r"\text{CH}_3\text{-CO-CH}_3 + 3\text{I}_2 + 4\text{NaOH} \rightarrow \text{CHI}_3\downarrow + \text{CH}_3\text{COONa} + 3\text{NaI} + 3\text{H}_2\text{O}",
            "alasan": "Atom H alfa pada metil keton sangat asam, tersubstitusi oleh Iodin membentuk Iodoform kuning.",
            "warna_akhir": "#fde047", "efek": "endapan"
        }
    },
    "Etil Asetat": {
        "Ceric Nitrat": {
            "hasil": "(-) Kuning",
            "reaksi": r"\text{Ester} + \text{Ceric Nitrat} \rightarrow \text{Tidak bereaksi}",
            "alasan": "Gugus ester tidak memiliki gugus hidroksil reaktif.",
            "warna_akhir": "#facc15", "efek": "tidak_ada"
        },
        "Na-Bisulfit": {
            "hasil": "(-) Bening",
            "reaksi": r"\text{Ester} + \text{NaHSO}_3 \rightarrow \text{Tidak bereaksi}",
            "alasan": "Resonansi pasangan elektron bebas gugus etoksi menstabilkan karbon karbonil, tidak reaktif terhadap nukleofil lemah.",
            "warna_akhir": "#e8f4f8", "efek": "tidak_ada"
        },
        "Hidroksilamin (Uji Ester)": {
            "hasil": "(+) Merah Violet",
            "reaksi": r"1.\ \text{R-COOR'} + \text{NH}_2\text{OH} \rightarrow \text{R-CONHOH} + \text{R'-OH} \quad 2.\ 3\text{R-CONHOH} + \text{FeCl}_3 \rightarrow \text{Fe(R-CONHO)}_3 + 3\text{HCl}",
            "alasan": "Ester diubah oleh hidroksilamin menjadi asam hidroksamat yang mengkelat Fe³⁺ menghasilkan kompleks violet.",
            "warna_akhir": "#c026d3", "efek": "tidak_ada"
        }
    },
    "Asam Asetat": {
        "Ceric Nitrat": {
            "hasil": "(-) Kuning",
            "reaksi": r"\text{CH}_3\text{COOH} + \text{Ceric Nitrat} \rightarrow \text{Tidak bereaksi}",
            "alasan": "Oksigen karboksil ditarik resonansi ikatan rangkap karbonil, kurang nukleofilik untuk Cerium.",
            "warna_akhir": "#facc15", "efek": "tidak_ada"
        },
        "Na-Bisulfit": {
            "hasil": "(-) Bening",
            "reaksi": r"\text{CH}_3\text{COOH} + \text{NaHSO}_3 \rightarrow \text{Tidak bereaksi}",
            "alasan": "Bukan senyawa golongan aldehid atau keton.",
            "warna_akhir": "#e8f4f8", "efek": "tidak_ada"
        },
        "Hidroksilamin (Uji Ester)": {
            "hasil": "(-) Bening",
            "reaksi": r"\text{CH}_3\text{COOH} + \text{NH}_2\text{OH} + \text{FeCl}_3 \rightarrow \text{Tidak bereaksi}",
            "alasan": "Bukan ester. Asam karboksilat tidak memicu pembentukan asam hidroksamat reaktif.",
            "warna_akhir": "#e8f4f8", "efek": "tidak_ada"
        },
        "Uji Barit (NaHCO3)": {
            "hasil": "(+) Gelembung & Keruh",
            "reaksi": r"1.\ \text{CH}_3\text{COOH} + \text{NaHCO}_3 \rightarrow \text{CH}_3\text{COONa} + \text{H}_2\text{O} + \text{CO}_2\uparrow \quad 2.\ \text{CO}_2 + \text{Ba(OH)}_2 \rightarrow \text{BaCO}_3\downarrow + \text{H}_2\text{O}",
            "alasan": "Asam mendonasikan proton mengurai bikarbonat. Gas CO₂ bereaksi dengan air barit membentuk BaCO₃ keruh.",
            "warna_akhir": "#e8f4f8", "efek": "gelembung"
        }
    },
    "Heksana": {
        "Ceric Nitrat": {
            "hasil": "(-) Kuning",
            "reaksi": r"\text{Heksana} + \text{Ceric Nitrat} \rightarrow \text{Tidak bereaksi}",
            "alasan": "Tidak ada gugus fungsi -OH alkoholik.",
            "warna_akhir": "#facc15", "efek": "tidak_ada"
        },
        "Na-Bisulfit": {
            "hasil": "(-) Bening",
            "reaksi": r"\text{Heksana} + \text{NaHSO}_3 \rightarrow \text{Tidak bereaksi}",
            "alasan": "Tidak memiliki gugus aktif karbonil.",
            "warna_akhir": "#e8f4f8", "efek": "tidak_ada"
        },
        "Hidroksilamin (Uji Ester)": {
            "hasil": "(-) Bening",
            "reaksi": r"\text{Heksana} + \text{NH}_2\text{OH} \rightarrow \text{Tidak bereaksi}",
            "alasan": "Bukan senyawa turunan ester.",
            "warna_akhir": "#e8f4f8", "efek": "tidak_ada"
        },
        "Uji Barit (NaHCO3)": {
            "hasil": "(-) Bening",
            "reaksi": r"\text{Heksana} + \text{NaHCO}_3 \rightarrow \text{Tidak bereaksi}",
            "alasan": "Senyawa hidrokarbon alifatik jenuh, bersifat non-polar dan inert. Gagal bereaksi di seluruh uji fungsional — terbukti sebagai alkana.",
            "warna_akhir": "#e8f4f8", "efek": "tidak_ada"
        }
    }
}

# Inisialisasi State
for key, default in {
    'test_started': False,
    'senyawa_uji': "",
    'current_step': 0,
    'log_history': [],
    'trigger_animation': False,
    'confirm_ganti': False
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ==============================================================================
# 4. SIDEBAR NAVIGASI
# ==============================================================================
with st.sidebar:
    st.markdown("""
        <div style='text-align:center; padding: 10px 0 5px;'>
            <span style='font-size: 3em;'>⬡</span>
        </div>
        <div style='text-align:center;'>
            <span style='font-family: Space Mono, monospace; font-size:1.3em; font-weight:700; color:#99f6e4;'>OrganicChem</span>
        </div>
        <div style='text-align:center; font-size:0.85em; color:#5eead4; margin-top:4px;'>🔬 Identifikasi Senyawa Organik</div>
    """, unsafe_allow_html=True)
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

# --- HALAMAN UTAMA ---
if pilihan_halaman == "🏠 HALAMAN UTAMA":
    st.markdown("""
        <div class="banner-utama">
            <h1 style='color:white; margin-bottom:8px; font-weight:700;'>Eksplorasi Dunia Kimia Organik Tanpa Batas! 👋</h1>
            <p style='font-size:1.15em; opacity:0.92; margin:0;'>Solusi cerdas belajar mandiri dan simulasi identifikasi gugus fungsi dalam satu platform.</p>
        </div>
    """, unsafe_allow_html=True)

    st.subheader("💡 Tentang OrganicChem")
    st.write(
        "Kami hadir untuk menjembatani teori dan praktik. Platform ini dirancang khusus untuk "
        "membantu Anda memahami materi teoretis sekaligus memvisualisasikan reaksi uji kualitatif "
        "senyawa organik secara interaktif—kapan saja dan di mana saja, layaknya memiliki laboratorium pribadi."
    )

    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""<div class='info-box'><h4>📘 Bab I</h4><p>Sifat fisika & kimia Hidrokarbon: alkana, alkena, alkuna, benzena.</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class='info-box'><h4>📙 Bab II</h4><p>Alkohol, Eter, dan Fenol beserta uji klasifikasinya.</p></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class='info-box'><h4>📗 Bab III</h4><p>Aldehid dan Keton: reaksi adisi karbonil dan uji daya reduksi.</p></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""<div class='info-box'><h4>📕 Bab IV</h4><p>Asam Karboksilat dan Derivatnya, termasuk uji hidroksamat.</p></div>""", unsafe_allow_html=True)

# --- BAB I ---
elif pilihan_halaman == "📘 BAB I. HIDROKARBON":
    st.title("📘 BAB I. HIDROKARBON")
    st.write("---")
    st.markdown("""
    Hidrokarbon adalah senyawa organik yang seluruh strukturnya hanya tersusun atas unsur karbon (C) dan hidrogen (H). Berdasarkan jenis ikatannya, hidrokarbon alifatik dibagi menjadi hidrokarbon jenuh (alkana) dan tidak jenuh (alkena dan alkuna). Sementara itu, hidrokarbon aromatik memiliki rantai siklik konjugasi yang sangat stabil.

    #### **A. Sifat Fisika Hidrokarbon**
    * **Wujud Zat (pada suhu kamar):**
      * Suhu rendah ($C_1 - C_4$) berwujud gas (contoh: metana, etana, etena, etuna).
      * Suhu sedang ($C_5 - C_{17}$) berwujud cair (contoh: pentana, heksana, benzena).
      * Suhu tinggi ($\ge C_{18}$) berwujud padat (contoh: parafin padat).
    * **Kelarutan:** Bersifat nonpolar, sehingga tidak larut dalam air (pelarut polar). Hidrokarbon larut baik dalam pelarut organik nonpolar seperti kloroform ($CHCl_3$), karbon tetraklorida ($CCl_4$), atau eter.
    * **Titik Didih dan Titik Leleh:** Meningkat seiring bertambahnya massa molekul. Rantai lurus memiliki titik didih lebih tinggi dari rantai bercabang.
    * **Densitas:** Lebih kecil daripada air. Lapisan hidrokarbon selalu berada di atas air.

    #### **B. Sifat Kimia & Reaksi Identifikasi Hidrokarbon**

    **1. Alkana (Hidrokarbon Jenuh)**
    * Disebut parafin karena tidak reaktif terhadap asam, basa, dan oksidator pada suhu kamar.
    * **Uji Iodo (Substitusi Halogen):** Bereaksi lambat dengan halogen melalui substitusi radikal bebas dengan bantuan UV atau panas.
    """)
    st.latex(r"\text{CH}_4 + \text{I}_2 \xrightarrow{\text{Sinar UV} / \Delta} \text{CH}_3\text{I} + \text{HI}")
    st.markdown("""
    **2. Alkena dan Alkuna (Hidrokarbon Tidak Jenuh)**
    * Sangat reaktif karena ikatan rangkap kaya elektron, mudah mengalami adisi.
    * **Uji Adisi Iodium:** Warna ungu iodium memudar seketika.
    """)
    st.latex(r"\text{R-CH}=\text{CH-R} + \text{I}_2 \rightarrow \text{R-CH(I)-CH(I)-R}")
    st.markdown("""
    * **Uji Baeyer ($KMnO_4$):** Warna ungu hilang, terbentuk endapan cokelat $MnO_2$.
    """)
    st.latex(r"3\text{CH}_2=\text{CH}_2 + 2\text{KMnO}_4 + 4\text{H}_2\text{O} \rightarrow 3\text{HO-CH}_2\text{-CH}_2\text{-OH} + 2\text{MnO}_2\downarrow + 2\text{KOH}")
    st.markdown("""
    **3. Benzena (Hidrokarbon Aromatik)**
    * Sangat stabil karena resonansi elektron pi (aturan Hückel $4n+2$).
    * **Uji Bakar:** Nyala berminyak dengan jelaga hitam tebal karena kadar karbon tinggi.
    * **Reaksi Nitrasi (Substitusi Elektrofilik):**
    """)
    st.latex(r"\text{C}_6\text{H}_6 + \text{HNO}_3 \xrightarrow{\text{H}_2\text{SO}_4\text{ pekat}} \text{C}_6\text{H}_5\text{NO}_2 + \text{H}_2\text{O}")

# --- BAB II ---
elif pilihan_halaman == "📙 BAB II. ALKOHOL, ETER, DAN FENOL":
    st.title("📙 BAB II. ALKOHOL, ETER, DAN FENOL")
    st.write("---")
    st.markdown("""
    #### **A. Sifat Fisika & Klasifikasi**
    * **Alkohol ($R - OH$):** Diklasifikasikan menjadi alkohol primer ($1^\circ$), sekunder ($2^\circ$), dan tersier ($3^\circ$). Alkohol rantai pendek mudah larut dalam air karena membentuk ikatan hidrogen.
    * **Eter ($R^1 - O - R^2$):** Titik didih lebih rendah dari alkohol isomernya karena tidak ada ikatan hidrogen antar-sesama.
    * **Fenol ($C_6H_5OH$):** Padatan pada suhu kamar, larutan bersifat asam lemah karena ion fenoksida distabilkan resonansi.

    #### **B. Reaksi Kimia Alkohol & Eter**

    **1. Pereaksi Lucas**
    * Alkohol $3^\circ$: bereaksi seketika (keruh). Alkohol $2^\circ$: 5–10 menit. Alkohol $1^\circ$: tidak bereaksi.
    """)
    st.latex(r"\text{R}_3\text{C-OH} + \text{HCl} \xrightarrow{\text{ZnCl}_2} \text{R}_3\text{C-Cl}\downarrow + \text{H}_2\text{O}")
    st.markdown("""
    **2. Pereaksi Jones (Oksidasi)**
    * Alkohol $1^\circ$ → Asam Karboksilat. Alkohol $2^\circ$ → Keton. Alkohol $3^\circ$ tidak bereaksi.
    """)
    st.latex(r"\text{R-CH}_2\text{-OH} \xrightarrow{\text{CrO}_3/\text{H}_2\text{SO}_4} \text{R-COOH}\text{ [Jingga} \rightarrow \text{Hijau]}")
    st.latex(r"\text{R}_2\text{CH-OH} \xrightarrow{\text{CrO}_3/\text{H}_2\text{SO}_4} \text{R}_2\text{C}=\text{O}\text{ [Jingga} \rightarrow \text{Hijau]}")
    st.markdown("""
    **3. Uji Iodoform**
    * Khusus alkohol metil karbinol $(CH_3CH(OH))$ membentuk endapan kuning $CHI_3$.
    """)
    st.latex(r"\text{R-CH(OH)-CH}_3 + 4\text{I}_2 + 6\text{NaOH} \rightarrow \text{R-COONa} + \text{CHI}_3\downarrow + 5\text{NaI} + 5\text{H}_2\text{O}")
    st.markdown("""
    **4. Pereaksi Ceric Ammonium Nitrate (CAN)**
    """)
    st.latex(r"\text{ROH} + [\text{Ce(NO}_3)_6]^{2-} \rightarrow [\text{Ce(OR)(NO}_3)_5]^{2-}\text{ (Kompleks Merah)} + \text{HNO}_3")
    st.markdown("""
    #### **C. Reaksi Kimia Fenol**

    **1. Basa Kuat ($NaOH$)**
    """)
    st.latex(r"\text{C}_6\text{H}_5\text{OH} + \text{NaOH} \rightarrow \text{C}_6\text{H}_5\text{ONa} + \text{H}_2\text{O}")
    st.markdown("**2. Uji $FeCl_3$ → Kompleks ungu tua**")
    st.latex(r"6\text{C}_6\text{H}_5\text{OH} + \text{FeCl}_3 \rightarrow [\text{Fe(OC}_6\text{H}_5)_6]^{3-}\text{ (Ungu)} + 3\text{H}^+ + 3\text{Cl}^-")
    st.markdown("**3. Air Brom → Trisubstitusi**")
    st.latex(r"\text{C}_6\text{H}_5\text{OH} + 3\text{Br}_2 \rightarrow \text{C}_6\text{H}_2\text{Br}_3\text{OH}\downarrow\text{ (Endapan Putih)} + 3\text{HBr}")

# --- BAB III ---
elif pilihan_halaman == "📗 BAB III. ALDEHID DAN KETON":
    st.title("📗 BAB III. ALDEHID DAN KETON")
    st.write("---")
    st.markdown("""
    Aldehida (${R-CHO}$) dan keton (${R-CO-R}'$) sama-sama memiliki gugus karbonil (${C}={O}$). Perbedaan: karbon karbonil aldehida mengikat minimal satu H, keton mengikat dua gugus alkil/aril.

    #### **A. Sifat Fisika**
    Formaldehida berwujud gas dengan bau menyengat. Aldehida suku rendah beraroma buah. Keton suku rendah (aseton) berupa cairan mudah menguap beraroma segar.

    #### **B. Reaksi Adisi Karbonil**

    **1. Adisi Natrium Bisulfit (${NaHSO}_3$)**
    """)
    st.latex(r"\text{R-CHO} + \text{NaHSO}_3 \rightarrow \text{R-CH(OH)-SO}_3\text{Na (Kristal Putih)}")
    st.markdown("""
    **2. Pembentukan Hemiasetal dan Asetal**
    """)
    st.latex(r"\text{R-CHO} + \text{R'OH} \xrightarrow{\text{HCl}} \text{R-CH(OH)(OR') (Hemiasetal)}")
    st.markdown("""
    #### **C. Uji Daya Reduksi Aldehida**

    **1. Uji Tollens (Cermin Perak)**
    """)
    st.latex(r"\text{R-CHO} + 2[\text{Ag(NH}_3)_2]^+ + 3\text{OH}^- \rightarrow \text{R-COO}^- + 2\text{Ag}\downarrow + 4\text{NH}_3 + 2\text{H}_2\text{O}")
    st.markdown("**2. Uji Fehling**")
    st.latex(r"\text{R-CHO} + 2\text{Cu}^{2+} + 5\text{OH}^- \rightarrow \text{R-COO}^- + \text{Cu}_2\text{O}\downarrow\text{ (Merah Bata)} + 3\text{H}_2\text{O}")
    st.markdown("**3. Uji Benedict**")
    st.latex(r"\text{R-CHO} + 2\text{Cu}^{2+}\text{(sitrat)} + 5\text{OH}^- \rightarrow \text{R-COO}^- + \text{Cu}_2\text{O}\downarrow + 3\text{H}_2\text{O}")

# --- BAB IV ---
elif pilihan_halaman == "📕 BAB IV. ASAM KARBOKSILAT DAN DERIVATNYA":
    st.title("📕 BAB IV. ASAM KARBOKSILAT DAN DERIVATNYA")
    st.write("---")
    st.markdown("""
    Asam karboksilat memiliki gugus karboksil ($-{COOH}$). Derivatnya terbentuk saat gugus $-{OH}$ digantikan nukleofil lain.

    #### **A. Sifat Fisika**
    Asam karboksilat rantai pendek ($C_1 - C_4$) sangat larut dalam air karena ikatan hidrogen kuat. Titik didih relatif tinggi karena pembentukan dimer.

    #### **B. Reaksi Kimia**

    **1. Reaksi dengan $NaOH$**
    """)
    st.latex(r"\text{R-COOH} + \text{NaOH} \rightarrow \text{R-COONa} + \text{H}_2\text{O}")
    st.markdown("**2. Reaksi dengan $NaHCO_3$ (Uji Barit)**")
    st.latex(r"\text{R-COOH} + \text{NaHCO}_3 \rightarrow \text{R-COONa} + \text{H}_2\text{O} + \text{CO}_2\uparrow")
    st.latex(r"\text{CO}_2 + \text{Ba(OH)}_2 \rightarrow \text{BaCO}_3\downarrow\text{ (Endapan Putih)} + \text{H}_2\text{O}")
    st.markdown("**3. Esterifikasi Fischer**")
    st.latex(r"\text{R-COOH} + \text{R'-OH} \xrightarrow{\text{H}_2\text{SO}_4, \Delta} \text{R-COOR' (Ester)} + \text{H}_2\text{O}")
    st.markdown("""
    #### **C. Uji Asam Hidroksamat (Identifikasi Ester)**
    """)
    st.latex(r"\text{R-COOR'} + \text{NH}_2\text{OH} \rightarrow \text{R-CONH-OH} + \text{R'-OH}")
    st.latex(r"3\text{R-CONH-OH} + \text{FeCl}_3 \rightarrow \text{Fe(R-CONHO)}_3\text{ (Kompleks Ungu)} + 3\text{HCl}")

# --- POST TEST ---
elif pilihan_halaman == "🔬 POST TEST":
    st.title("🔀 Asisten Identifikasi Cerdas (Step-by-Step)")
    st.write("Simulasi penelusuran identifikasi kualitatif langkah demi langkah. Tekan **Lanjut** untuk melanjutkan ke reaksi berikutnya.")

    # ── HALAMAN PEMILIHAN SAMPEL ──
    if not st.session_state.test_started:
        st.divider()
        st.markdown("#### 🧫 Pilih Golongan Senyawa Uji (Blind Sample)")
        st.write("Pilih golongan senyawa yang ingin diidentifikasi. Nama senyawa spesifiknya akan terungkap di akhir pengujian.")

        # Kelompokkan senyawa per golongan
        opsi_golongan = {nama_golongan[k]: k for k in nama_golongan}
        opsi_list = ["-- Pilih Golongan Senyawa --"] + list(opsi_golongan.keys())

        golongan_dipilih = st.selectbox("Golongan Senyawa:", opsi_list)

        if golongan_dipilih != "-- Pilih Golongan Senyawa --":
            senyawa_asli = opsi_golongan[golongan_dipilih]
            st.markdown(f"""
            <div class='info-box'>
                <div class='golongan-badge'>{golongan_dipilih}</div>
                <div style='color:#334155; margin-top:6px;'>{deskripsi_golongan[senyawa_asli]}</div>
            </div>
            """, unsafe_allow_html=True)

        if st.button("Mulai Identifikasi 🚀", type="primary"):
            if golongan_dipilih == "-- Pilih Golongan Senyawa --":
                st.warning("⚠️ Harap pilih golongan senyawa terlebih dahulu!")
            else:
                senyawa = opsi_golongan[golongan_dipilih]
                st.session_state.test_started = True
                st.session_state.senyawa_uji = senyawa
                st.session_state.current_step = 0
                st.session_state.log_history = []
                st.session_state.trigger_animation = True
                st.session_state.confirm_ganti = False
                force_rerun()

    # ── HALAMAN PENGUJIAN AKTIF ──
    else:
        senyawa = st.session_state.senyawa_uji
        urutan = flowchart_paths[senyawa]
        total_steps = len(urutan)

        # ── Header dengan info senyawa & tombol ganti ──
        col_h1, col_h2 = st.columns([3, 1])
        with col_h1:
            st.markdown(f"""
            <div class='info-box' style='margin-bottom:12px;'>
                <div class='golongan-badge'>🧪 Sedang Diuji</div>
                <span style='font-size:1.05em; font-weight:600; color:#0f766e;'>{nama_golongan[senyawa]}</span>
                <span style='color:#94a3b8; font-size:0.85em; margin-left:12px;'>Nama spesifik tersembunyi — terungkap saat selesai</span>
            </div>
            """, unsafe_allow_html=True)
        with col_h2:
            st.markdown("")
            if not st.session_state.trigger_animation:
                if st.button("🔁 Ganti Sampel", use_container_width=True, key="btn_ganti_top"):
                    st.session_state.confirm_ganti = True
                    force_rerun()

        # ── Dialog Konfirmasi Ganti Sampel ──
        if st.session_state.confirm_ganti:
            st.warning("⚠️ **Yakin ingin mengganti sampel?** Semua progres pengujian saat ini akan hilang.")
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                if st.button("✅ Ya, Ganti Sampel", type="primary", use_container_width=True):
                    st.session_state.test_started = False
                    st.session_state.senyawa_uji = ""
                    st.session_state.current_step = 0
                    st.session_state.log_history = []
                    st.session_state.trigger_animation = False
                    st.session_state.confirm_ganti = False
                    force_rerun()
            with col_c2:
                if st.button("❌ Batal, Lanjutkan", use_container_width=True):
                    st.session_state.confirm_ganti = False
                    force_rerun()
            st.divider()

        # ── Step Indicator ──
        step_html = "<div class='step-indicator'>"
        for i, pereaksi in enumerate(urutan):
            if i > 0:
                done_line = i < st.session_state.current_step
                step_html += f"<div class='step-line {'done' if done_line else ''}'></div>"
            if i < st.session_state.current_step:
                cls = "done"
            elif i == st.session_state.current_step:
                cls = "active"
            else:
                cls = "pending"
            step_html += f"<div class='step-dot {cls}'>{i+1}</div>"
        step_html += "</div>"
        st.markdown(step_html, unsafe_allow_html=True)

        st.write("---")
        col_visual, col_log = st.columns([1, 2.5])

        with col_visual:
            st.markdown("<h4 style='text-align:center;'>🧪 Visualisasi Lab</h4>", unsafe_allow_html=True)
            tube_placeholder = st.empty()
            status_placeholder = st.empty()

        with col_log:
            st.markdown("#### 📑 Buku Catatan Laboratorium")
            log_container = st.container()

        # ── Tampilkan log history ──
        with log_container:
            for log in st.session_state.log_history:
                is_positive = "(+)" in log["hasil"]
                if is_positive:
                    st.success(f"**Tahap {log['step']}: {log['pereaksi']}** ➔ **{log['hasil']}**")
                else:
                    st.error(f"**Tahap {log['step']}: {log['pereaksi']}** ➔ **{log['hasil']}**")
                with st.expander(f"Lihat Persamaan Reaksi & Pembahasan — Tahap {log['step']}"):
                    st.latex(log['reaksi'])
                    st.write(f"**Pembahasan:** {log['alasan']}")

        # ── ANIMASI & TOMBOL LANJUT ──
        if st.session_state.trigger_animation and st.session_state.current_step < total_steps:
            pereaksi = urutan[st.session_state.current_step]

            tube_placeholder.markdown(render_tube("25%", "#e8f4f8", "tidak_ada", "Sampel awal"), unsafe_allow_html=True)
            status_placeholder.info(f"⏳ Menyiapkan sampel untuk **{pereaksi}**...")
            time.sleep(0.9)

            warna_reagen = reagen_colors[pereaksi]
            tube_placeholder.markdown(render_tube("62%", warna_reagen, "tidak_ada", f"+ {pereaksi}"), unsafe_allow_html=True)
            status_placeholder.info(f"🔬 Meneteskan **{pereaksi}**...")
            time.sleep(1.4)

            res = database_reaksi[senyawa][pereaksi]
            tube_placeholder.markdown(render_tube("62%", res["warna_akhir"], res["efek"], res["hasil"]), unsafe_allow_html=True)
            status_placeholder.success("✅ Hasil reaksi diamati!")
            time.sleep(1.1)

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
            # Tampilkan tabung hasil terakhir
            if st.session_state.current_step > 0:
                last_pereaksi = urutan[st.session_state.current_step - 1]
                res = database_reaksi[senyawa][last_pereaksi]
                tube_placeholder.markdown(render_tube("62%", res["warna_akhir"], res["efek"], res["hasil"]), unsafe_allow_html=True)

            # ── Belum selesai: tampilkan tombol Lanjut ──
            if st.session_state.current_step < total_steps:
                next_pereaksi = urutan[st.session_state.current_step]
                status_placeholder.markdown(
                    f"<div style='text-align:center; color:#0f766e; font-weight:600; padding:8px;'>⏸ Menunggu konfirmasi praktikan...</div>",
                    unsafe_allow_html=True
                )
                with col_visual:
                    st.write("")
                    if st.button(f"▶ Lanjut: Uji {next_pereaksi}", use_container_width=True, type="primary"):
                        st.session_state.trigger_animation = True
                        force_rerun()

            # ── Selesai: tampilkan kesimpulan ──
            else:
                status_placeholder.markdown(
                    "<div style='text-align:center; font-weight:700; color:#0d9488; padding:8px;'>🎉 Identifikasi selesai!</div>",
                    unsafe_allow_html=True
                )
                with log_container:
                    st.markdown(f"""
                    <div class='kesimpulan-box'>
                        <div style='font-size:1.05em; opacity:0.85; margin-bottom:4px;'>✅ KESIMPULAN IDENTIFIKASI</div>
                        <div style='font-size:1.4em; font-weight:700;'>{nama_golongan[senyawa]}</div>
                        <div style='font-size:1em; opacity:0.85; margin-top:6px;'>Nama spesifik: <strong>{senyawa}</strong></div>
                        <div style='font-size:0.9em; opacity:0.75; margin-top:4px;'>{deskripsi_golongan[senyawa]}</div>
                    </div>
                    """, unsafe_allow_html=True)

                with col_visual:
                    st.write("")
                    if st.button("🔄 Uji Sampel Baru", use_container_width=True, type="primary"):
                        st.session_state.test_started = False
                        st.session_state.confirm_ganti = False
                        force_rerun()
