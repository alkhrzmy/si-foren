"""
State Management & Pydantic Schema Definitions for SI-FOREN.
Sistem Intelijen Finansial & Operasional Rekanan Pengadaan.
Focus: Commercial Performance Funnel, Pricing Aggressiveness, Ecosystem Competitor Graph, and Strategic Capture Advisory.
"""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class CommercialIntelligenceDossier(BaseModel):
    target_entity: str
    status_badge: str = Field(description="Profil status komersial vendor (e.g., KONTRAKTOR AKTIF KOMPETITIF)")
    
    # ── 1. Tender Conversion Funnel & Capital ──
    conversion_funnel: Dict[str, Any] = Field(default_factory=dict)
    
    # ── 2. Pricing Behavior & Agency Footprint ──
    pricing_behavior: Dict[str, Any] = Field(default_factory=dict)
    
    # ── 3. Dual Strategic Advisory ──
    commercial_efficiency_memo: str = Field(description="Analisis efisiensi konversi tender, disiplin modal bidding, dan agresivitas harga")
    competitive_landscape_memo: str = Field(description="Analisis lanskap persaingan, dominasi incumbent, dan tekanan ekosistem rivalitas")
    
    # ── 4. Per-Section Analytical Callouts ──
    graph_callout: str = Field(default="", description="Catatan analis untuk peta jejaring rivalitas co-bidding")
    incumbent_callout: str = Field(default="", description="Catatan analis untuk peta dominasi incumbent penguasa pasar")
    pricing_callout: str = Field(default="", description="Catatan analis untuk histori harga penawaran terbesar")
    
    # ── 5. Actionable Strategic Recommendations ──
    strategic_recommendations: List[str] = Field(default_factory=list)
    
    # ── 6. Raw Data Collections ──
    cobid_partners: List[Dict[str, Any]] = Field(default_factory=list)
    primary_agency_incumbents: List[Dict[str, Any]] = Field(default_factory=list)
    agency_win_distribution: List[Dict[str, Any]] = Field(default_factory=list)
    bidding_pricing_history: List[Dict[str, Any]] = Field(default_factory=list)


class InvestigationState(BaseModel):
    user_query: str
    target_vendor: str
    query_type: str = "SINGLE_ENTITY"
    
    # Gatekeeper Validation
    is_valid_query: bool = True
    rejection_reason: Optional[str] = None
    
    # Raw Data Stores
    sql_findings: Optional[Dict[str, Any]] = None
    graph_findings: Optional[Dict[str, Any]] = None
    incumbent_findings: Optional[List[Dict[str, Any]]] = None
    pricing_history_findings: Optional[List[Dict[str, Any]]] = None
    
    # Final Commercial Intelligence Dossier
    final_dossier: Optional[CommercialIntelligenceDossier] = None
