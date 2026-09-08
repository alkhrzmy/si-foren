"""
SI-FOREN: Sistem Intelijen Finansial & Operasional Rekanan Pengadaan.
Gradio Production Web Application for Hugging Face Spaces (Zero-OSINT Edition).
Features:
1. Native Collapsible Sidebar with Presets, Open Data Links & Methodology References.
2. Clean Initial Landing State (Lower result containers hidden until search is executed).
3. 5-KPI Tender Conversion Funnel Hero Scorecard.
4. Symmetrical Radial Co-Bidding Network Graph in Dark Matte Container.
5. Agency Win Distribution & Market Incumbents DataFrames.
6. Full Interactive Dynamic Year & Real Bids Filtering.
"""
import base64
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import gradio as gr
import numpy as np
import pandas as pd

# Setup paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
sys.path.append(str(BASE_DIR))

from src.agents.supervisor import ForensicSupervisorOrchestrator

# ZeroGPU initialization requirement on Hugging Face Spaces
try:
    import spaces

    @spaces.GPU(duration=1)
    def dummy_gpu():
        return None
except Exception:
    pass

# Initialize supervisor orchestrator
orchestrator = ForensicSupervisorOrchestrator(data_dir=str(DATA_DIR))


def get_total_packages_count_str() -> str:
    count = orchestrator.sql_tool.get_total_tenders_count()
    return f"{count:,.0f}".replace(",", ".")


TOTAL_PKTS_STR = get_total_packages_count_str()


# ── CSS THEME STYLING (Dark Editorial Standard) ─────────────────────────────
CUSTOM_CSS = """
/* Background & Global Resets */
.gradio-container {
    background-color: #121214 !important;
    color: #F4F4F5 !important;
    font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    max-width: 1400px !important;
    margin: 0 auto !important;
}

/* Sidebar styling */
[data-testid="sidebar"] {
    background-color: #111113 !important;
    border-right: 1px solid #27272A !important;
}

/* Header Banner */
.siforen-header {
    background: #18181B;
    border: 1px solid #27272A;
    padding: 2.2rem 3rem 1.8rem;
    border-radius: 6px;
    margin-bottom: 1.5rem;
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

/* Scorecard Hero */
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

/* Section Cards */
.section-dossier-block {
    background: #18181B;
    border: 1px solid #27272A;
    border-radius: 6px;
    padding: 1.6rem 2rem;
    margin-bottom: 1.6rem;
}

.section-dossier-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.28rem;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 0.9rem;
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

/* Links in Amber */
a {
    color: #FDE68A !important;
    text-decoration: none !important;
}
a:hover {
    color: #D97706 !important;
    text-decoration: underline !important;
}
"""


def format_currency(val: float) -> str:
    if val >= 1e12:
        return f"Rp {val / 1e12:.2f} Triliun"
    elif val >= 1e9:
        return f"Rp {val / 1e9:.2f} Miliar"
    elif val > 0:
        return f"Rp {val:,.0f}".replace(",", ".")
    return "Rp 0"


def render_hero_scorecard_html(dossier) -> str:
    cf = dossier.conversion_funnel
    pb = dossier.pricing_behavior

    hps_won_str = format_currency(cf.get("total_hps_won", 0.0))
    wasted_val = cf.get("wasted_bidding_capital", 0.0)
    if wasted_val >= 1e9:
        wasted_str = f"Rp {wasted_val / 1e9:.2f} Miliar"
    elif wasted_val > 0:
        wasted_str = f"Rp {wasted_val / 1e6:.1f} Juta"
    else:
        wasted_str = "Rp 0"

    real_win_rate_str = f"{cf.get('real_bid_win_rate_percent', 0.0)}%"
    avg_discount_str = f"{pb.get('avg_discount_pct', 0.0)}% HPS"
    median_discount_str = f"{pb.get('median_discount_pct', 0.0)}% HPS"

    return f"""
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
                <div style="font-size: 0.70rem; color: #71717A; margin-top: 0.25rem;">Median: {median_discount_str}</div>
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
    """


def render_graph_iframe(graph_html: str) -> str:
    b64 = base64.b64encode(graph_html.encode('utf-8')).decode('ascii')
    return f"""
    <div style="background: #111113; border: 1px solid #27272A; border-radius: 4px; overflow: hidden; margin-bottom: 1.2rem;">
        <iframe src="data:text/html;base64,{b64}" width="100%" height="470" frameborder="0"></iframe>
    </div>
    """


def render_recommendations_html(recommendations: List[str]) -> str:
    cards = "".join([f'<div class="action-card">• {rec}</div>' for rec in recommendations])
    return f"""
    <div class="section-dossier-block">
        <div class="section-dossier-title">5. Rekomendasi Strategis Manajemen Tender &amp; Capture Advisory</div>
        {cards}
    </div>
    """


# ── MAIN INVESTIGATION DISPATCHER ───────────────────────────────────────────
def run_investigation(
    query_text: str,
    selected_years: List[str],
    real_bids_only: bool
) -> Tuple[Any, str, str, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, str]:
    if not query_text or len(query_text.strip()) < 3:
        return (
            gr.update(visible=False),
            "<div style='padding: 2rem; color: #FDA4AF; background: #18181B; border-radius: 6px;'>Input terlalu pendek. Masukkan nama entitas vendor pengadaan.</div>",
            "", pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), ""
        )

    # 1. Run Pipeline
    state = orchestrator.investigate(query_text.strip())

    if not state.is_valid_query:
        return (
            gr.update(visible=False),
            f"<div style='background: #18181B; border: 1px solid #27272A; border-left: 3px solid #E11D48; padding: 1.2rem; border-radius: 4px; color: #FDA4AF;'>{state.rejection_reason}</div>",
            "", pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), ""
        )

    dossier = state.final_dossier
    if not dossier:
        return (
            gr.update(visible=False),
            f"<div style='background: #18181B; border: 1px solid #27272A; border-left: 3px solid #D97706; padding: 1.2rem; border-radius: 4px; color: #FDE68A;'>Entitas <b>{state.target_vendor}</b> tidak memiliki rekam jejak transaksi pada {TOTAL_PKTS_STR} data lelang SPSE terbuka saat ini.</div>",
            "", pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), ""
        )

    # 2. Render Scorecard HTML
    hero_html = render_hero_scorecard_html(dossier)

    # 3. Dynamic Filter Recalculation
    effective_years = selected_years if selected_years else ["2024", "2025", "2026"]
    
    filtered_partners = orchestrator.sql_tool.get_dynamic_cobid_partners(
        vendor_name=dossier.target_entity,
        selected_years=effective_years,
        real_bids_only=real_bids_only,
        limit=12
    )

    partner_names = [p.get("partner_vendor") for p in filtered_partners if p.get("partner_vendor")]
    interconnected_edges = orchestrator.sql_tool.get_interconnected_partner_edges(
        partner_names=partner_names,
        selected_years=effective_years,
        real_bids_only=real_bids_only,
        min_weight=5
    )

    # Generate Radial Graph HTML
    graph_html = orchestrator.graph_tool.generate_dynamic_pyvis_html(
        target_node=dossier.target_entity,
        dynamic_partners=filtered_partners,
        interconnected_edges=interconnected_edges
    )
    graph_iframe_html = render_graph_iframe(graph_html) if graph_html else "<div style='color: #71717A; padding: 1rem;'>Subgraf tidak memiliki koneksi relasi pada filter yang dipilih.</div>"

    # Co-bidding Partners Dataframe
    partners_rows = []
    for p in filtered_partners:
        partners_rows.append({
            "Nama Rekanan": p.get("partner_vendor"),
            "Lelang Bersama": f"{p.get('cobid_frequency')}x Paket",
            "HPS Bersama": format_currency(p.get("shared_hps_total", 0.0)),
            "Tumpang Tindih (%)": f"{p.get('overlap_ratio_percent', 0.0)}%"
        })
    df_partners = pd.DataFrame(partners_rows)

    # Agency Win Distribution Dataframe
    filtered_agency_wins = orchestrator.sql_tool.get_agency_win_distribution(
        vendor_name=dossier.target_entity,
        selected_years=effective_years,
        limit=10
    )
    agency_rows = []
    for r in filtered_agency_wins:
        wr = r.get("Win Rate Penawaran (%)")
        agency_rows.append({
            "Kementerian / Lembaga": r.get("Kementerian / Lembaga"),
            "Kontrak Menang": f"{r.get('Kontrak Menang', 0)} Proyek",
            "Akumulasi Nilai": format_currency(r.get("Nilai Kontrak", 0.0)),
            "Penawaran Riil": f"{r.get('Penawaran Riil', 0)} Paket",
            "Total Dipantau": f"{r.get('Total Dipantau', 0)} Paket",
            "Konversi Menang": f"{wr}%" if pd.notnull(wr) else "—"
        })
    df_agencies = pd.DataFrame(agency_rows)

    # Primary Agency Incumbents Dataframe
    primary_agency, filtered_incumbents = orchestrator.sql_tool.get_primary_agency_incumbents(
        vendor_name=dossier.target_entity,
        selected_years=effective_years,
        limit=6
    )
    incumbent_rows = []
    for inc in filtered_incumbents:
        incumbent_rows.append({
            "Kompetitor Utama": inc.get("Entitas Kompetitor Utama"),
            "Proyek Dimenangkan": f"{inc.get('Proyek Dimenangkan')} Proyek",
            "Nilai Proyek": format_currency(inc.get("Akumulasi Nilai Proyek", 0.0)),
            "Penawaran Rata-rata": f"{inc.get('Rata-rata Penawaran (% HPS)')}% HPS"
        })
    df_incumbents = pd.DataFrame(incumbent_rows)

    # Pricing History Dataframe
    filtered_pricing = orchestrator.sql_tool.get_bidding_pricing_history(
        vendor_name=dossier.target_entity,
        selected_years=effective_years,
        limit=8
    )
    pricing_rows = []
    for pr in filtered_pricing:
        pricing_rows.append({
            "ID": pr.get("ID Paket"),
            "Nama Paket Tender": pr.get("Nama Paket Tender"),
            "Instansi": pr.get("Instansi"),
            "Nilai HPS": format_currency(pr.get("Nilai HPS", 0.0)),
            "Tawaran Target": format_currency(pr.get("Tawaran Target", 0.0)) if pr.get("Tawaran Target") else "Tidak Submit",
            "Diskon Target": f"{pr.get('Diskon Target (%)')}% HPS" if pd.notnull(pr.get('Diskon Target (%)')) else "—",
            "Pemenang Riil": pr.get("Pemenang Riil"),
            "Diskon Pemenang": f"{pr.get('Diskon Pemenang (%)')}% HPS" if pd.notnull(pr.get('Diskon Pemenang (%)')) else "—",
            "Status": pr.get("Status Hasil")
        })
    df_pricing = pd.DataFrame(pricing_rows)

    # Recommendations HTML
    rec_html = render_recommendations_html(dossier.strategic_recommendations)

    return (
        gr.update(visible=True),
        hero_html,
        graph_iframe_html,
        df_partners,
        df_agencies,
        df_incumbents,
        df_pricing,
        rec_html
    )


# ── GRADIO BLOCKS APPLICATION ───────────────────────────────────────────────
with gr.Blocks(title="SI-FOREN") as demo:
    # ── 1. Collapsible Sidebar ──
    with gr.Sidebar(label="Navigasi & Skenario"):
        gr.Markdown("### Skenario Kasus")
        gr.Markdown("Klik tombol preset untuk memuat profil instan:")
        btn_preset1 = gr.Button("PT DWI TUNGGAL JAYA", size="sm")
        btn_preset2 = gr.Button("PT TUAKARTA DAYA CIPTA", size="sm")
        btn_preset3 = gr.Button("CV RAFLINDO", size="sm")
        btn_preset4 = gr.Button("PT TELKOM SATELIT INDONESIA", size="sm")
        btn_preset5 = gr.Button("Perum Peruri", size="sm")

        gr.Markdown("---")
        gr.Markdown("### Publikasi & Data Terbuka")
        gr.Markdown("""
        - [Dashboard Interaktif SPSE (Tableau Public)](https://public.tableau.com/app/profile/gymnastiar.al.khoarizmy/viz/DashboardSPSETableau/Dashboard1)
        - [Open Dataset SPSE Pengadaan (Kaggle)](https://www.kaggle.com/datasets/jimnaas/indonesia-spse-procurement-raw-data)
        """)

        gr.Markdown("---")
        gr.Markdown("### Kerangka Metodologi")
        gr.Markdown("""
        - [Fazekas et al. (2016): Model komposit risiko lelang (CRI Model)](https://doi.org/10.1007/s10610-016-9308-z)
        - [Decarolis et al. (2022): Triangulasi multi-indikator eliminasi false positive](https://doi.org/10.1140/epjds/s13688-022-00325-x)
        - [OECD Guidelines (2025): Standar deteksi persekongkolan tender (Bid Rigging)](https://www.oecd.org/en/topics/sub-issues/competition-enforcement/fighting-bid-rigging-in-public-procurement.html)
        """)

        gr.Markdown("---")
        gr.Markdown("### Parameter Sistem")
        gr.Markdown(f"""
        - **Basis Data:** DuckDB ({TOTAL_PKTS_STR} Lelang SPSE)
        - **Graf Relasi:** NetworkX (Modularity $Q = 0.670$)
        - **Orkestrator:** Qwen2.5-72B-Instruct (Hugging Face)
        """)

    # ── 2. Main Page Header ──
    gr.HTML(f"""
    <div class="siforen-header">
        <h1>SI-FOREN</h1>
        <div class="tagline">Sistem Intelijen Finansial &amp; Operasional Rekanan Pengadaan · B2B Procurement Intelligence</div>
    </div>
    """)

    # ── 3. Query Row ──
    with gr.Row():
        query_input = gr.Textbox(
            label="Kueri Analisis Pengadaan",
            placeholder="Contoh: Audit vendor PT DWI TUNGGAL JAYA di Kemenkeu",
            value="Audit vendor PT DWI TUNGGAL JAYA di Kemenkeu",
            lines=2,
            scale=4
        )
        submit_btn = gr.Button("Mulai Analisis Pasar →", variant="primary", scale=1)

    gr.Markdown(f"**Basis Data Aktif:** `{TOTAL_PKTS_STR} Lelang SPSE (Rp 249,17T HPS)` · **Model:** `Qwen2.5-72B-Instruct` · **Engine:** `DuckDB & NetworkX`")

    # ── 4. Dynamic Filters ──
    with gr.Row():
        year_filter = gr.Dropdown(
            choices=["2024", "2025", "2026"],
            value=["2024", "2025", "2026"],
            multiselect=True,
            label="Filter Tahun Anggaran",
            scale=2
        )
        real_bids_toggle = gr.Checkbox(
            value=True,
            label="Penawar Riil (Harga > 0)",
            info="Centang untuk menyaring murni penawar aktif. Hapus centang untuk menyertakan seluruh pendaftar.",
            scale=2
        )

    # ── 5. Hero Scorecard Area ──
    hero_scorecard_output = gr.HTML("""
    <div style="text-align: center; padding: 4rem 2rem; background: #18181B; border: 1px solid #27272A; border-radius: 6px; margin-top: 1rem;">
        <div style="font-family: 'Playfair Display', Georgia, serif; font-size: 1.5rem; color: #FFFFFF; font-weight: 700; margin-bottom: 0.5rem;">
            Mulai Analisis Pasar &amp; Profil Rekanan Pengadaan
        </div>
        <div style="font-size: 0.92rem; color: #A1A1AA; max-width: 580px; margin: 0 auto; line-height: 1.6;">
            Pilih salah satu tombol preset di bilah samping atau masukkan nama entitas vendor pada kolom kueri lalu klik <strong>Mulai Analisis Pasar →</strong>.
        </div>
    </div>
    """)

    # ── 6. Results Container (HIDDEN INITIALLY, SHOWN ONLY UPON SEARCH) ──
    with gr.Column(visible=False) as results_container:
        # Section 1: Graph & Partners
        gr.HTML("<div class='section-dossier-title'>1. Peta Ekosistem Rekanan Kompetitor (Co-Bidding Ego-Network)</div>")
        graph_output = gr.HTML()
        gr.Markdown("**Daftar Rekanan yang Sering Hadir Bersama di Tender:**")
        table_partners_output = gr.Dataframe(interactive=False)

        # Section 2: Agency Win Distribution
        gr.HTML("<div class='section-dossier-title'>2. Sebaran Kemenangan &amp; Portofolio Rekanan per Instansi</div>")
        gr.Markdown("Rekam jejak konversi tender vendor di kementerian/lembaga negara, diurutkan dari kemenangan kontrak terbanyak:")
        table_agencies_output = gr.Dataframe(interactive=False)

        # Section 3: Market Incumbents
        gr.HTML("<div class='section-dossier-title'>3. Peta Penguasa Pasar di Instansi Utama</div>")
        gr.Markdown("Daftar kompetitor yang mendominasi kemenangan proyek pada kementerian/lembaga basis utama:")
        table_incumbents_output = gr.Dataframe(interactive=False)

        # Section 4: Pricing History
        gr.HTML("<div class='section-dossier-title'>4. Histori Penawaran Harga pada Paket-Paket Terbesar</div>")
        gr.Markdown("Komparasi harga penawaran target terhadap nilai pemenang kontrak pada paket bernilai besar:")
        table_pricing_output = gr.Dataframe(interactive=False)

        # Section 5: Strategic Recommendations
        recommendations_output = gr.HTML()

        # Disclaimer Footer
        gr.HTML("""
        <div class="disclaimer-card">
            <div style="font-weight: 600; color: #D97706; margin-bottom: 0.35rem; text-transform: uppercase; font-size: 0.78rem; letter-spacing: 0.06em;">Catatan Kepatuhan &amp; Disclaimer Intelijen Pasar</div>
            <div style="font-size: 0.86rem; color: #A1A1AA; line-height: 1.6;">
                Platform ini merupakan instrumen analitik intelijen pasar dan penapisan komersial berbasis data terbuka pengadaan publik (SPSE). Seluruh metrik, konversi tender, dan perbandingan harga penawaran dihitung secara empiris untuk mendukung analisis strategi bisnis dan uji kepatuhan internal. Keputusan keikutsertaan tender dan verifikasi kualifikasi teknis/hukum sepenuhnya merupakan tanggung jawab masing-masing entitas pelaku usaha.
            </div>
        </div>
        """)

    # ── Wire up preset buttons ──
    btn_preset1.click(lambda: "PT DWI TUNGGAL JAYA", outputs=query_input)
    btn_preset2.click(lambda: "PT TUAKARTA DAYA CIPTA", outputs=query_input)
    btn_preset3.click(lambda: "CV RAFLINDO", outputs=query_input)
    btn_preset4.click(lambda: "PT TELKOM SATELIT INDONESIA", outputs=query_input)
    btn_preset5.click(lambda: "PERUM PERURI", outputs=query_input)

    # ── Wire up execution and filter events ──
    event_inputs = [query_input, year_filter, real_bids_toggle]
    event_outputs = [
        results_container,
        hero_scorecard_output,
        graph_output,
        table_partners_output,
        table_agencies_output,
        table_incumbents_output,
        table_pricing_output,
        recommendations_output
    ]

    submit_btn.click(fn=run_investigation, inputs=event_inputs, outputs=event_outputs)
    year_filter.change(fn=run_investigation, inputs=event_inputs, outputs=event_outputs)
    real_bids_toggle.change(fn=run_investigation, inputs=event_inputs, outputs=event_outputs)


if __name__ == "__main__":
    demo.launch(css=CUSTOM_CSS)
