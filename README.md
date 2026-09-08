---
title: SI-FOREN
emoji: ⚖️
colorFrom: yellow
colorTo: red
sdk: streamlit
sdk_version: 1.35.0
app_file: app.py
pinned: false
---

# SI-FOREN: Sistem Intelijen Finansial & Operasional Rekanan Pengadaan
### B2B Procurement Market Intelligence & Competitive Bidding Analytics Platform

SI-FOREN adalah platform analitik intelijen pasar pengadaan barang dan jasa publik (SPSE Indonesia). Sistem ini dirancang untuk membantu konsultan tender, kontraktor, dan analis kepatuhan korporasi dalam mengevaluasi efisiensi penawaran, memetakan penguasa pasar, dan menganalisis ekosistem rivalitas rekanan berbasis 36.135 transaksi lelang riil bernilai Rp 249,17 Triliun HPS.

---

## Fitur Utama

1. **Tender Conversion Funnel**  
   Memisahkan secara tegas antara peserta yang hanya mengunduh dokumen dengan kontraktor yang benar-benar mengajukan penawaran harga riil. Menghitung *Real Bid Win Rate* dan estimasi efisiensi modal penawaran.

2. **Analisis Agresivitas Penawaran Harga (% HPS)**  
   Menganalisis sebaran harga penawaran terhadap HPS, mengidentifikasi batas penawaran agresif di zona Evaluasi Kewajaran Harga (EKH), serta memetakan rentang harga pemenang lelang.

3. **Peta Ekosistem Rekanan Kompetitor (Co-Bidding Network)**  
   Visualisasi graf radial simetris (NetworkX Modularity Q = 0.670) yang memetakan jejaring rekanan yang sering hadir bersama di lelang, dilengkapi filter pemisah penawar riil vs pendaftar pasif.

4. **Peta Penguasa Pasar Instansi (Market Incumbents)**  
   Mengidentifikasi entitas kontraktor yang mendominasi kemenangan proyek pada kementerian atau lembaga target.

5. **Dual Strategic Advisory (Qwen2.5-72B-Instruct)**  
   Sintesis penalaran AI terstruktur yang memberikan evaluasi komersial berimbang mengenai disiplin harga dan dinamika persaingan pasar.

---

## Arsitektur Sistem (On-Premises Pattern)

Sistem mengadopsi pola IBM Enterprise Architecture:
- **Client Location (On-Premises):** Penyimpanan data 100% lokal menggunakan DuckDB Columnar Store dan NetworkX Graph Engine demi kedaulatan data privat.
- **Cloud (SaaS) / External AI:** Inferensi penalaran kognitif menggunakan model Qwen2.5-72B-Instruct melalui Hugging Face Serverless API.

---

## Parameter Sistem

- **Basis Data:** DuckDB (36.135 Lelang SPSE, 461.125 Rekam Peserta, 29.857 Pemenang)
- **Graf Relasi:** NetworkX (1.909 Nodes, 17.965 Edges, Q = 0.670)
- **Mesin Penalaran:** Qwen2.5-72B-Instruct via Hugging Face Inference API
- **Antarmuka:** Streamlit Editorial UI (Matte Charcoal & Amber Bronze Palette)

---

## Sumber Terbuka & Publikasi

- [Dashboard Interaktif SPSE (Tableau Public)](https://public.tableau.com/app/profile/gymnastiar.al.khoarizmy/viz/DashboardSPSETableau/Dashboard1)
- [Open Dataset SPSE Pengadaan (Kaggle)](https://www.kaggle.com/datasets/jimnaas/indonesia-spse-procurement-raw-data)
- [Kerangka Metodologi Fazekas (2016) Springer](https://doi.org/10.1007/s10610-016-9308-z)
- [Kerangka Metodologi Decarolis (2022) EPJ Data Science](https://doi.org/10.1140/epjds/s13688-022-00325-x)

---

## Lisensi & Catatan Kepatuhan

Platform ini dikembangkan untuk tujuan riset akademik, edukasi, dan analisis pasar pengadaan publik terbuka. Seluruh keputusan komersial dan keikutsertaan tender merupakan tanggung jawab masing-masing entitas pelaku usaha.
