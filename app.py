"""
SPSE Multi-Agent Forensic & Procurement Market Intelligence Platform.
SI-FOREN: Sistem Intelijen Finansial & Operasional Rekanan Pengadaan.
Human-Grade Editorial UI / High-End Legal & Commercial Intelligence Design System.
Zero-OSINT, Zero-Emoji-Spam, Pristine Material Icons Typography.
Production Ready for Hugging Face Spaces & On-Premises Deployment.
"""
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# Ensure local imports work reliably
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
sys.path.append(str(BASE_DIR))

from src.agents.supervisor import ForensicSupervisorOrchestrator


# ── 1. Page Configuration ───────────────────────────────────────────────────
st.set_page_config(
    page_title="SI-FOREN",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ── 2. Editorial Theme Styling (Charcoal, Amber Gold, Zero Blue/Purple) ──────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=Playfair+Display:wght@600;700&family=JetBrains+Mono:wght@400;500&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

@font-face {
    font-family: 'Material Symbols Rounded Local';
    font-style: normal;
    font-weight: 400;
    font-display: block;
    src: url('/static/media/MaterialSymbols-Rounded.Bc71WqoX.woff2') format('woff2');
}

:root {
    --bg-main: #121214;
    --bg-card: #18181B;
    --bg-card-inner: #111113;
    --border-main: #27272A;
    --border-subtle: #3F3F46;
    --text-pure: #FFFFFF;
    --text-primary: #F4F4F5;
    --text-muted: #A1A1AA;
    --accent-amber: #D97706;
    --accent-gold: #FDE68A;
    --accent-crimson: #E11D48;
    --accent-emerald: #10B981;
}

/* Background & main resets */
.stApp {
    background-color: var(--bg-main);
    color: var(--text-primary);
}

/* Base typography */
.stApp p, .stApp label, .stMarkdown, .stSelectbox, .stTextArea textarea {
    font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
}

.stButton button {
    font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    border-radius: 4px !important;
}

/* ── CRITICAL FIX: Ensure Material Symbols Icons Render as Glyphs, Never Raw Text ── */
[data-testid="stIconMaterial"],
.material-symbols-rounded,
.material-symbols-outlined,
[data-testid="stSidebarCollapseButton"] span[data-testid="stIconMaterial"],
.stExpander summary [data-testid="stIconMaterial"] {
    font-family: 'Material Symbols Rounded', 'Material Symbols Rounded Local' !important;
    font-weight: normal !important;
    font-style: normal !important;
    font-size: 1.25rem !important;
    line-height: 1 !important;
    letter-spacing: normal !important;
    text-transform: none !important;
    display: inline-block !important;
    white-space: nowrap !important;
    word-wrap: normal !important;
    direction: ltr !important;
    -webkit-font-smoothing: antialiased !important;
}

/* Ensure sidebar collapse button is always visible cleanly */
[data-testid="stBaseButton-headerNoPadding"],
[data-testid="stSidebarCollapseButton"] {
    visibility: visible !important;
    opacity: 1 !important;
}

/* Override all default blue/purple hyperlinks to warm amber/gold */
.stApp a {
    color: #FDE68A !important;
    text-decoration: none !important;
    font-weight: 500 !important;
}
.stApp a:hover {
    color: #D97706 !important;
    text-decoration: underline !important;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: #111113 !important;
    border-right: 1px solid var(--border-main) !important;
}

/* Header banner (Hypxr7 Legal Editorial Standard) */
.siforen-header {
    background: #18181B;
    border: 1px solid #27272A;
    padding: 2.2rem 3rem 1.8rem;
    border-radius: 6px;
    margin-bottom: 1.6rem;
    position: relative;
    overflow: hidden;
}

.siforen-header::before {
    content: "";
    position: absolute;
    inset: 0;
    background: repeating-linear-gradient(
        45deg,
        rgba(217, 119, 6, 0.03),
        rgba(217, 119, 6, 0.03) 1px,
        transparent 1px,
        transparent 12px
    );
    pointer-events: none;
}

.siforen-header h1 {
    font-family: 'Playfair Display', Georgia, serif !important;
    font-size: 2.6rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
    color: #FFFFFF !important;
    margin: 0 0 0.4rem 0 !important;
    line-height: 1.15 !important;
}

.siforen-header .tagline {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    color: #D97706 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}

/* Executive Scorecard Card */
.scorecard-hero {
    background: #18181B;
    border: 1px solid #27272A;
    border-radius: 6px;
    padding: 1.8rem 2.2rem;
    margin-bottom: 1.6rem;
}

.scorecard-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    border-bottom: 1px solid #27272A;
    padding-bottom: 1.2rem;
    margin-bottom: 1.4rem;
}

.entity-headline {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.85rem;
    font-weight: 700;
    color: #FFFFFF;
    letter-spacing: -0.01em;
}

.commercial-badge {
    padding: 0.4rem 0.9rem;
    border-radius: 3px;
    font-size: 0.74rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    background: rgba(217, 119, 6, 0.15);
    color: #FDE68A;
    border: 1px solid #D97706;
}

/* 5-Metric Funnel Grid */
.funnel-metric-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 0.85rem;
    margin-bottom: 1.2rem;
}

.funnel-metric-cell {
    background: #111113;
    border: 1px solid #27272A;
    border-radius: 4px;
    padding: 1rem 1.1rem;
}

.funnel-metric-label {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #A1A1AA;
    margin-bottom: 0.35rem;
    font-weight: 600;
}

.funnel-metric-value {
    font-size: 1.45rem;
    font-weight: 700;
    color: #FFFFFF;
    font-family: 'JetBrains Mono', monospace;
    line-height: 1.1;
}

.funnel-sub-bar {
    background: #111113;
    border: 1px solid #27272A;
    border-radius: 4px;
    padding: 0.85rem 1.2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.86rem;
    color: #D4D4D8;
    margin-bottom: 1.4rem;
}

/* Dual Strategic Advisory */
.advisory-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.2rem;
}

.advisory-card-commercial {
    background: #111113;
    border: 1px solid #27272A;
    border-left: 3px solid #D97706;
    border-radius: 4px;
    padding: 1.2rem 1.5rem;
}

.advisory-card-market {
    background: #111113;
    border: 1px solid #27272A;
    border-left: 3px solid #52525B;
    border-radius: 4px;
    padding: 1.2rem 1.5rem;
}

.advisory-title {
    font-size: 0.76rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 700;
    margin-bottom: 0.6rem;
}

.advisory-body {
    font-size: 0.90rem;
    line-height: 1.65;
    color: #D4D4D8;
}

/* Section Container Card */
.section-dossier-block {
    background: #18181B;
    border: 1px solid #27272A;
    border-radius: 6px;
    padding: 1.6rem 2rem;
    margin-bottom: 1.8rem;
}

.section-dossier-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.28rem;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 0.9rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.section-reasoning-card {
    background: #111113;
    border: 1px solid #27272A;
    border-radius: 4px;
    padding: 0.85rem 1.1rem;
    margin-bottom: 1.2rem;
    font-size: 0.88rem;
    color: #D4D4D8;
    line-height: 1.55;
}

/* Visual Legend Bar */
.graph-legend-bar {
    display: flex;
    gap: 1.5rem;
    background: #111113;
    border: 1px solid #27272A;
    border-radius: 4px;
    padding: 0.6rem 1.1rem;
    margin-bottom: 1rem;
    font-size: 0.80rem;
    color: #D4D4D8;
}

.legend-item {
    display: flex;
    align-items: center;
    gap: 0.45rem;
}

.legend-item .dot {
    width: 9px;
    height: 9px;
    border-radius: 50%;
    display: inline-block;
}

/* Action Recommendation Cards */
.action-card {
    background: #111113;
    border: 1px solid #27272A;
    border-left: 3px solid #D97706;
    border-radius: 4px;
    padding: 0.95rem 1.3rem;
    margin-bottom: 0.75rem;
    color: #F4F4F5;
    font-size: 0.91rem;
    line-height: 1.55;
}

/* Disclaimer Box */
.disclaimer-card {
    background: #18181B;
    border: 1px solid #27272A;
    border-left: 3px solid #52525B;
    border-radius: 4px;
    padding: 1.2rem 1.6rem;
    margin-top: 1.5rem;
}

/* Table styling */
[data-testid="stDataFrame"] {
    border: 1px solid #27272A !important;
    border-radius: 4px !important;
}

#MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── 3. Lazy Orchestrator & Stats Cache ───────────────────────────────────────
@st.cache_resource
def load_orchestrator():
    return ForensicSupervisorOrchestrator(data_dir=str(DATA_DIR))

@st.cache_data
def get_dynamic_package_count_str():
    import duckdb
    try:
        con = duckdb.connect()
        c = con.execute(f"SELECT COUNT(*) FROM read_parquet('{DATA_DIR}/paket.parquet')").fetchone()[0]
        return f"{c:,.0f}".replace(",", ".")
    except Exception:
        return "36.135"


# ── 4. Header Banner (Clean Editorial Standard) ──────────────────────────────
st.markdown("""
<div class="siforen-header">
    <h1>SI-FOREN</h1>
    <div class="tagline">Sistem Intelijen Finansial &amp; Operasional Rekanan Pengadaan · B2B Procurement Intelligence</div>
</div>
""", unsafe_allow_html=True)


# ── 5. Sidebar: Presets, Methodology Links & Platform Parameters ────────────
total_pkts_str = get_dynamic_package_count_str()

with st.sidebar:
    st.markdown("### Skenario Kasus")
    st.caption("Klik tombol kasus untuk memuat profil intelijen secara instan:")

    examples = [
        "Audit vendor PT DWI TUNGGAL JAYA di Kemenkeu",
        "PT TUAKARTA DAYA CIPTA",
        "Audit CV RAFLINDO",
        "Periksa afiliasi PT FRONTIER SENTRATAMA INDONESIA",
        "Audit kepatuhan PT TELKOM SATELIT INDONESIA",
        "Audit perum peruri"
    ]

    for ex in examples:
        if st.button(ex, key=f"btn_side_{ex}", use_container_width=True):
            st.session_state["query_input"] = ex

    st.markdown("---")
    st.markdown("### Publikasi & Data Terbuka")
    st.markdown("""
    - [Dashboard Interaktif SPSE (Tableau Public)](https://public.tableau.com/app/profile/gymnastiar.al.khoarizmy/viz/DashboardSPSETableau/Dashboard1)
    - [Open Dataset SPSE Pengadaan (Kaggle)](https://www.kaggle.com/datasets/jimnaas/indonesia-spse-procurement-raw-data)
    """)

    st.markdown("---")
    st.markdown("### Kerangka Metodologi")
    st.markdown(f"""
    - [Fazekas et al. (2016): Model komposit risiko lelang (*CRI Model*)](https://doi.org/10.1007/s10610-016-9308-z)
    - [Decarolis et al. (2022): Triangulasi multi-indikator eliminasi *false positive*](https://doi.org/10.1140/epjds/s13688-022-00325-x)
    - [OECD Guidelines (2025): Standar deteksi persekongkolan tender (*Bid Rigging*)](https://www.oecd.org/en/topics/sub-issues/competition-enforcement/fighting-bid-rigging-in-public-procurement.html)
    """)

    st.markdown("---")
    st.markdown("### Parameter Sistem")
    st.markdown(f"""
    - **Basis Data:** DuckDB ({total_pkts_str} Lelang SPSE)
    - **Graf Relasi:** NetworkX (Modularity $Q = 0.670$)
    - **Orkestrator:** Qwen2.5-72B-Instruct (Hugging Face)
    """)
    
    with st.expander("Metrik Modularity (Q = 0.670)"):
        st.caption(
            "Modularity (Q) mengukur derajat pemisahan jaringan menjadi kelompok-kelompok relasi lelang. "
            "Skala Q berkisar dari -0.5 hingga 1.0. Nilai Q > 0.4 membuktikan adanya struktur klaster "
            "lelang bersama yang sangat padat dan terisolasi dari persaingan pasar terbuka umum."
        )


# ── 6. Query Input Area ─────────────────────────────────────────────────────
if "query_input" not in st.session_state:
    st.session_state["query_input"] = "Audit vendor PT DWI TUNGGAL JAYA di Kemenkeu"

query = st.text_area(
    "Kueri Analisis Pengadaan",
    key="query_input",
    placeholder="Contoh: Audit vendor PT DWI TUNGGAL JAYA di Kemenkeu",
    height=80,
    label_visibility="collapsed"
)

col_btn, col_info = st.columns([2, 5])
with col_btn:
    run_btn = st.button("Mulai Analisis Pasar →", type="primary", use_container_width=True)
with col_info:
    st.markdown(
        f"<div style='padding-top: 0.45rem; font-size: 0.82rem; color: #A1A1AA; font-family: \"JetBrains Mono\", monospace;'>"
        f"Model: Qwen2.5-72B-Instruct · {total_pkts_str} Lelang (Rp 249,17T HPS) · Local Analytics Engine"
        f"</div>",
        unsafe_allow_html=True
    )


# ── 7. Pipeline Execution & Session State Cache ───────────────────────────────
if run_btn and query.strip():
    with st.spinner("Mengekstraksi conversion funnel, graf rivalitas & sintesis penawaran pasar..."):
        orchestrator = load_orchestrator()
        st.session_state["last_investigation_state"] = orchestrator.investigate(query.strip())

# Retrieve persistent state from session state
state = st.session_state.get("last_investigation_state", None)

if state:
    orchestrator = load_orchestrator()
    
    # Case A: Gatekeeper Rejection
    if not state.is_valid_query:
        st.markdown(f"""
        <div style="background: #18181B; border: 1px solid #27272A; border-left: 3px solid #E11D48; padding: 1.1rem 1.5rem; border-radius: 4px; margin-top: 1rem;">
            <div style="font-weight: 600; color: #FDA4AF; margin-bottom: 0.35rem; text-transform: uppercase; font-size: 0.78rem; letter-spacing: 0.06em;">Pemberitahuan Kebijakan Keamanan</div>
            <div style="color: #F4F4F5; font-size: 0.94rem; line-height: 1.5;">{state.rejection_reason}</div>
        </div>
        """, unsafe_allow_html=True)

    # Case B: Entity Found & Commercial Dossier Render
    else:
        exists = state.sql_findings.get("exists_in_database", False) if state.sql_findings else False

        if not exists:
            st.markdown(f"""
            <div style="background: #18181B; border: 1px solid #27272A; border-left: 3px solid #D97706; padding: 1.1rem 1.5rem; border-radius: 4px; margin-top: 1rem;">
                <div style="font-weight: 600; color: #FDE68A; margin-bottom: 0.35rem; text-transform: uppercase; font-size: 0.78rem; letter-spacing: 0.06em;">Data Transaksi Tidak Ditemukan</div>
                <div style="color: #F4F4F5; font-size: 0.94rem; line-height: 1.5;">
                    Entitas <b>{state.target_vendor}</b> tidak memiliki rekam jejak transaksi pada {total_pkts_str} data lelang SPSE terbuka saat ini.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            dossier = state.final_dossier
            if dossier:
                cf = dossier.conversion_funnel
                pb = dossier.pricing_behavior

                # Currency Formats
                hps_won_val = cf.get("total_hps_won", 0.0)
                if hps_won_val >= 1e12:
                    hps_won_str = f"Rp {hps_won_val / 1e12:.2f} Triliun"
                elif hps_won_val >= 1e9:
                    hps_won_str = f"Rp {hps_won_val / 1e9:.2f} Miliar"
                elif hps_won_val > 0:
                    hps_won_str = f"Rp {hps_won_val:,.0f}".replace(",", ".")
                else:
                    hps_won_str = "Rp 0"

                wasted_val = cf.get("wasted_bidding_capital", 0.0)
                if wasted_val >= 1e9:
                    wasted_str = f"Rp {wasted_val / 1e9:.2f} Miliar"
                elif wasted_val > 0:
                    wasted_str = f"Rp {wasted_val / 1e6:.1f} Juta"
                else:
                    wasted_str = "Rp 0"

                real_win_rate_str = f"{cf.get('real_bid_win_rate_percent', 0.0)}%"
                avg_discount_str = f"{pb.get('avg_discount_pct', 0.0)}% HPS"

                # ── 1. SCORECARD HERO: THE TENDER CONVERSION FUNNEL ──────────
                st.markdown(f"""
                <div class="scorecard-hero">
                    <div class="scorecard-header">
                        <div>
                            <div style="font-size: 0.74rem; text-transform: uppercase; letter-spacing: 0.08em; color: #A1A1AA; margin-bottom: 0.35rem;">Profil Intelijen Komersial</div>
                            <div class="entity-headline">{dossier.target_entity}</div>
                        </div>
                        <div>
                            <span class="commercial-badge">{dossier.status_badge}</span>
                        </div>
                    </div>
                    <div class="funnel-metric-grid">
                        <div class="funnel-metric-cell">
                            <div class="funnel-metric-label">1. Total Dipantau</div>
                            <div class="funnel-metric-value">{cf.get('total_registered', 0)} <span style="font-size: 0.85rem; color: #71717A; font-weight: 400;">Paket</span></div>
                            <div style="font-size: 0.70rem; color: #71717A; margin-top: 0.25rem;">Tahap Unduh Dokumen</div>
                        </div>
                        <div class="funnel-metric-cell">
                            <div class="funnel-metric-label">2. Penawaran Riil</div>
                            <div class="funnel-metric-value" style="color: #FDE68A;">{cf.get('total_bids_submitted', 0)} <span style="font-size: 0.85rem; color: #71717A; font-weight: 400;">Paket</span></div>
                            <div style="font-size: 0.70rem; color: #71717A; margin-top: 0.25rem;">Rasio Submit: {cf.get('submission_rate_percent', 0.0)}%</div>
                        </div>
                        <div class="funnel-metric-cell">
                            <div class="funnel-metric-label">3. Kontrak Menang</div>
                            <div class="funnel-metric-value" style="color: #10B981;">{cf.get('total_won', 0)} <span style="font-size: 0.85rem; color: #71717A; font-weight: 400;">Proyek</span></div>
                            <div style="font-size: 0.70rem; color: #71717A; margin-top: 0.25rem;">Pemenang Definitif</div>
                        </div>
                        <div class="funnel-metric-cell">
                            <div class="funnel-metric-label">4. Real Win Rate</div>
                            <div class="funnel-metric-value">{real_win_rate_str}</div>
                            <div style="font-size: 0.70rem; color: #71717A; margin-top: 0.25rem;">Dari Penawaran Riil</div>
                        </div>
                        <div class="funnel-metric-cell">
                            <div class="funnel-metric-label">5. Rata-rata Penawaran</div>
                            <div class="funnel-metric-value" style="color: #D97706;">{avg_discount_str}</div>
                            <div style="font-size: 0.70rem; color: #71717A; margin-top: 0.25rem;">Median: {pb.get('median_discount_pct', 0.0)}% HPS</div>
                        </div>
                    </div>
                    <div class="funnel-sub-bar">
                        <span><strong>Akumulasi Kontrak Dimenangkan:</strong> <span style="color: #10B981; font-weight: 600;">{hps_won_str}</span></span>
                        <span><strong>Estimasi Modal Bidding Terpakai:</strong> <span style="color: #FDA4AF; font-weight: 600;">{wasted_str}</span></span>
                        <span><strong>Basis Instansi Utama:</strong> <span style="color: #FFFFFF; font-weight: 600;">{pb.get('primary_agency', 'Kementerian Keuangan')}</span></span>
                    </div>
                    <div class="advisory-grid">
                        <div class="advisory-card-commercial">
                            <div class="advisory-title" style="color: #FDE68A;">Karakteristik Penawaran &amp; Efisiensi Komersial</div>
                            <div class="advisory-body">{dossier.commercial_efficiency_memo}</div>
                        </div>
                        <div class="advisory-card-market">
                            <div class="advisory-title" style="color: #D4D4D8;">Lanskap Persaingan &amp; Tekanan Pasar</div>
                            <div class="advisory-body">{dossier.competitive_landscape_memo}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # ── 2. DYNAMIC YEAR & BID FILTER BAR ─────────────────────────
                col_filter_label, col_filter_select, col_filter_toggle = st.columns([1.1, 2.4, 2.5])
                with col_filter_label:
                    st.markdown("<div style='padding-top: 0.4rem; font-weight: 600; font-size: 0.95rem; color: #F4F4F5;'>Filter:</div>", unsafe_allow_html=True)
                with col_filter_select:
                    selected_years = st.multiselect(
                        "Tahun Anggaran",
                        options=["2024", "2025", "2026"],
                        default=["2024", "2025", "2026"],
                        key="selected_years_filter",
                        label_visibility="collapsed"
                    )
                with col_filter_toggle:
                    real_bids_only = st.checkbox(
                        "Penawar Riil (Harga > 0)",
                        value=True,
                        help="Centang: Menyaring hanya peserta yang memasukkan harga penawaran riil. Hapus centang: Menyertakan seluruh pendaftar/pengunduh dokumen."
                    )

                effective_years = selected_years if selected_years else ["2024", "2025", "2026"]

                # Dynamic Recalculation based on filtered years & real bid toggle
                filtered_partners = orchestrator.sql_tool.get_dynamic_cobid_partners(
                    vendor_name=dossier.target_entity,
                    selected_years=effective_years,
                    real_bids_only=real_bids_only,
                    limit=12
                )
                
                primary_agency, filtered_incumbents = orchestrator.sql_tool.get_primary_agency_incumbents(
                    vendor_name=dossier.target_entity,
                    selected_years=effective_years,
                    limit=6
                )

                filtered_pricing = orchestrator.sql_tool.get_bidding_pricing_history(
                    vendor_name=dossier.target_entity,
                    selected_years=effective_years,
                    limit=8
                )

                filtered_agency_wins = orchestrator.sql_tool.get_agency_win_distribution(
                    vendor_name=dossier.target_entity,
                    selected_years=effective_years,
                    limit=10
                )

                partner_names = [p.get("partner_vendor") for p in filtered_partners if p.get("partner_vendor")]
                interconnected_edges = orchestrator.sql_tool.get_interconnected_partner_edges(
                    partner_names=partner_names,
                    selected_years=effective_years,
                    real_bids_only=real_bids_only,
                    min_weight=5
                )

                partner_freqs = [p.get("cobid_frequency", 1) for p in filtered_partners]
                q3_val = float(np.percentile(partner_freqs, 75)) if len(partner_freqs) >= 2 else (partner_freqs[0] if partner_freqs else 1)

                # ── SECTION 1: CO-BIDDING ECOSYSTEM GRAPH ────────────────────
                st.markdown("""
                <div class="section-dossier-block">
                    <div class="section-dossier-title">
                        <span>1. Peta Ekosistem Rekanan Kompetitor (Co-Bidding Ego-Network)</span>
                    </div>
                """, unsafe_allow_html=True)

                if dossier.graph_callout:
                    st.markdown(f"""
                    <div class="section-reasoning-card">
                        <strong>Catatan Analis Graf:</strong> {dossier.graph_callout}
                    </div>
                    """, unsafe_allow_html=True)

                # Visual Legend Bar
                st.markdown(f"""
                <div class="graph-legend-bar">
                    <span class="legend-item"><span class="dot" style="background: #E11D48;"></span> <strong>Target Entitas</strong></span>
                    <span class="legend-item"><span class="dot" style="background: #D97706;"></span> <strong>Rival Intensitas Tinggi (Q3 ≥ {q3_val:.0f}x)</strong></span>
                    <span class="legend-item"><span class="dot" style="background: #3F3F46;"></span> <strong>Peserta Terkait (&lt; {q3_val:.0f}x)</strong></span>
                </div>
                """, unsafe_allow_html=True)

                # Symmetrical Radial Vis.js Graph
                graph_html = orchestrator.graph_tool.generate_dynamic_pyvis_html(
                    target_node=dossier.target_entity,
                    dynamic_partners=filtered_partners,
                    interconnected_edges=interconnected_edges
                )
                if graph_html:
                    components.html(graph_html, height=470)
                else:
                    st.info("Subgraf tidak memiliki koneksi relasi pada tahun anggaran yang dipilih.")

                # Co-bidding Partners Data Table
                if filtered_partners:
                    mode_label = "Daftar Rekanan Penawar Riil (Kompetitor Aktif)" if real_bids_only else "Daftar Seluruh Rekanan Pendaftar (Termasuk Pemantau)"
                    st.markdown(f"<div style='margin-top: 1rem; font-weight: 600; font-size: 0.95rem; color: #FFFFFF;'>{mode_label}</div>", unsafe_allow_html=True)
                    table_partners_rows = []
                    for p in filtered_partners:
                        hps_shared = p.get("shared_hps_total", 0.0)
                        if hps_shared >= 1e12:
                            hps_shared_str = f"Rp {hps_shared / 1e12:.2f} Triliun"
                        elif hps_shared >= 1e9:
                            hps_shared_str = f"Rp {hps_shared / 1e9:.2f} Miliar"
                        elif hps_shared > 0:
                            hps_shared_str = f"Rp {hps_shared:,.0f}".replace(",", ".")
                        else:
                            hps_shared_str = "—"

                        table_partners_rows.append({
                            "Nama Rekanan Kompetitor": p.get("partner_vendor"),
                            "Frekuensi Lelang Bersama": f"{p.get('cobid_frequency')}x Paket",
                            "Akumulasi HPS Bersama": hps_shared_str,
                            "Rasio Tumpang Tindih (%)": f"{p.get('overlap_ratio_percent', 0.0)}%"
                        })
                    st.dataframe(pd.DataFrame(table_partners_rows), use_container_width=True, hide_index=True)

                st.markdown("</div>", unsafe_allow_html=True)

                # ── SECTION 2: AGENCY PORTFOLIO & WIN DISTRIBUTION ───────────
                st.markdown("""
                <div class="section-dossier-block">
                    <div class="section-dossier-title">2. Sebaran Kemenangan &amp; Portofolio Rekanan per Instansi</div>
                """, unsafe_allow_html=True)

                if filtered_agency_wins:
                    st.markdown("<div style='margin-bottom: 0.6rem; font-size: 0.88rem; color: #D4D4D8;'>Rekam jejak konversi tender vendor di kementerian/lembaga negara, diurutkan dari kemenangan kontrak terbanyak:</div>", unsafe_allow_html=True)
                    formatted_agency_rows = []
                    for r in filtered_agency_wins:
                        val = r.get("Nilai Kontrak", 0.0)
                        if val >= 1e12:
                            val_str = f"Rp {val / 1e12:.2f} Triliun"
                        elif val >= 1e9:
                            val_str = f"Rp {val / 1e9:.2f} Miliar"
                        elif val > 0:
                            val_str = f"Rp {val:,.0f}".replace(",", ".")
                        else:
                            val_str = "Rp 0"
                        
                        wr = r.get("Win Rate Penawaran (%)")
                        wr_str = f"{wr}%" if pd.notnull(wr) else "—"

                        formatted_agency_rows.append({
                            "Kementerian / Lembaga": r.get("Kementerian / Lembaga"),
                            "Kontrak Menang": f"{r.get('Kontrak Menang', 0)} Proyek",
                            "Akumulasi Nilai Kontrak": val_str,
                            "Penawaran Riil": f"{r.get('Penawaran Riil', 0)} Paket",
                            "Total Dipantau": f"{r.get('Total Dipantau', 0)} Paket",
                            "Rasio Konversi Menang": wr_str
                        })
                    st.dataframe(pd.DataFrame(formatted_agency_rows), use_container_width=True, hide_index=True)
                else:
                    st.info("Tidak ada rekam jejak kemenangan pada tahun anggaran yang dipilih.")

                st.markdown("</div>", unsafe_allow_html=True)

                # ── SECTION 3: MARKET INCUMBENTS IN PRIMARY AGENCY ───────────
                st.markdown(f"""
                <div class="section-dossier-block">
                    <div class="section-dossier-title">3. Peta Penguasa Pasar di Instansi Utama ({primary_agency})</div>
                """, unsafe_allow_html=True)

                if dossier.incumbent_callout:
                    st.markdown(f"""
                    <div class="section-reasoning-card">
                        <strong>Catatan Analis Pasar:</strong> {dossier.incumbent_callout}
                    </div>
                    """, unsafe_allow_html=True)

                if filtered_incumbents:
                    formatted_incumbents = []
                    for inc in filtered_incumbents:
                        hps_val = inc.get("Akumulasi Nilai Proyek", 0.0)
                        if hps_val >= 1e12:
                            hps_str = f"Rp {hps_val / 1e12:.2f} Triliun"
                        elif hps_val >= 1e9:
                            hps_str = f"Rp {hps_val / 1e9:.2f} Miliar"
                        elif hps_val > 0:
                            hps_str = f"Rp {hps_val:,.0f}".replace(",", ".")
                        else:
                            hps_str = "—"

                        formatted_incumbents.append({
                            "Entitas Kompetitor Utama": inc.get("Entitas Kompetitor Utama"),
                            "Proyek Dimenangkan": f"{inc.get('Proyek Dimenangkan')} Proyek",
                            "Akumulasi Nilai Proyek": hps_str,
                            "Rata-rata Penawaran (% HPS)": f"{inc.get('Rata-rata Penawaran (% HPS)')}% HPS"
                        })
                    st.dataframe(pd.DataFrame(formatted_incumbents), use_container_width=True, hide_index=True)
                else:
                    st.info(f"Tidak ditemukan kompetitor pemenang pada lelang di {primary_agency}.")

                st.markdown("</div>", unsafe_allow_html=True)

                # ── SECTION 4: BIDDING PRICING HISTORY ────────────────────────
                st.markdown("""
                <div class="section-dossier-block">
                    <div class="section-dossier-title">4. Histori Penawaran Harga pada Paket-Paket Terbesar</div>
                """, unsafe_allow_html=True)

                if dossier.pricing_callout:
                    st.markdown(f"""
                    <div class="section-reasoning-card">
                        <strong>Catatan Analis Penawaran:</strong> {dossier.pricing_callout}
                    </div>
                    """, unsafe_allow_html=True)

                if filtered_pricing:
                    df_pricing = pd.DataFrame(filtered_pricing)
                    if "Nilai HPS" in df_pricing.columns:
                        df_pricing["Nilai HPS"] = df_pricing["Nilai HPS"].apply(lambda x: f"Rp {x:,.0f}".replace(",", ".") if pd.notnull(x) and x > 0 else "—")
                    if "Penawaran Target" in df_pricing.columns:
                        df_pricing["Penawaran Target"] = df_pricing["Penawaran Target"].apply(lambda x: f"Rp {x:,.0f}".replace(",", ".") if pd.notnull(x) and x > 0 else "Tidak Submit")
                    if "Diskon Target (%)" in df_pricing.columns:
                        df_pricing["Diskon Target (%)"] = df_pricing["Diskon Target (%)"].apply(lambda x: f"{x}% HPS" if pd.notnull(x) else "—")
                    if "Diskon Pemenang (%)" in df_pricing.columns:
                        df_pricing["Diskon Pemenang (%)"] = df_pricing["Diskon Pemenang (%)"].apply(lambda x: f"{x}% HPS" if pd.notnull(x) else "—")
                    
                    st.dataframe(df_pricing, use_container_width=True, hide_index=True)
                else:
                    st.info("Tidak ada histori harga penawaran pada tahun anggaran yang dipilih.")

                st.markdown("</div>", unsafe_allow_html=True)

                # ── SECTION 5: STRATEGIC ACTIONABLE RECOMMENDATIONS ───────────
                st.markdown("""
                <div class="section-dossier-block">
                    <div class="section-dossier-title">5. Rekomendasi Strategis Manajemen Tender &amp; Capture Advisory</div>
                """, unsafe_allow_html=True)

                for rec in dossier.strategic_recommendations:
                    st.markdown(f"""
                    <div class="action-card">
                        • {rec}
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

                # ── 6. OFFICIAL COMMERCIAL & REGULATORY DISCLAIMER ────────────
                st.markdown("""
                <div class="disclaimer-card">
                    <div style="font-weight: 600; color: #D97706; margin-bottom: 0.35rem; text-transform: uppercase; font-size: 0.78rem; letter-spacing: 0.06em;">Catatan Kepatuhan &amp; Disclaimer Intelijen Pasar</div>
                    <div style="font-size: 0.86rem; color: #A1A1AA; line-height: 1.6;">
                        Platform ini merupakan instrumen analitik intelijen pasar dan penapisan komersial berbasis data terbuka pengadaan publik (SPSE). Seluruh metrik, konversi tender, dan perbandingan harga penawaran dihitung secara empiris untuk mendukung analisis strategi bisnis dan uji kepatuhan internal. Keputusan keikutsertaan tender dan verifikasi kualifikasi teknis/hukum sepenuhnya merupakan tanggung jawab masing-masing entitas pelaku usaha.
                    </div>
                </div>
                """, unsafe_allow_html=True)
else:
    # ── Initial Empty Landing State (Pure Minimalist, Zero Emoji) ───────────
    st.markdown("""
    <div style="text-align: center; padding: 4rem 2rem; background: #18181B; border: 1px solid #27272A; border-radius: 6px; margin-top: 1.5rem;">
        <div style="font-family: 'Playfair Display', Georgia, serif; font-size: 1.5rem; color: #FFFFFF; font-weight: 700; margin-bottom: 0.5rem;">
            Mulai Analisis Pasar &amp; Profil Rekanan Pengadaan
        </div>
        <div style="font-size: 0.92rem; color: #A1A1AA; max-width: 580px; margin: 0 auto; line-height: 1.6;">
            Pilih salah satu skenario kasus di bilah samping (sidebar) untuk pengujian instan, atau masukkan nama entitas vendor pada kolom kueri di atas lalu klik <strong>Mulai Analisis Pasar →</strong>.
        </div>
    </div>
    """, unsafe_allow_html=True)
