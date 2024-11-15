from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Set
from datetime import datetime

class LegalDocument(BaseModel):
    doc_id: str
    title: Optional[str]
    document_type: Optional[str]
    jurisdiction: Optional[str]
    date: Optional[str]
    content: str

class LegalEntities(BaseModel):
    parties: List[str]
    judges: List[str]
    lawyers: List[str]
    courts: List[str]
    organizations: List[str]

class LegalCitation(BaseModel):
    citation_text: str
    source: Optional[str]
    year: Optional[int]
    page: Optional[str]

class LegalClause(BaseModel):
    clause_type: str
    text: str
    section: Optional[str]
    importance: Optional[float]

class LegalAnalysis(BaseModel):
    doc_id: str
    document_type: str
    entities: LegalEntities
    key_clauses: List[LegalClause]
    citations: List[LegalCitation]
    legal_definitions: Dict[str, str]
    obligations: List[Dict[str, str]]
    deadlines: List[Dict[str, str]]
    jurisdiction: Optional[str]
    governing_law: Optional[str]
    risk_factors: List[str]
    monetary_values: List[Dict[str, str]]
    summary: str
    metadata: Dict[str, str]
    processing_time: float
    word_count: int
    created_at: str

class LegalQuery(BaseModel):
    question: str = Field(..., min_length=3, max_length=500)
    context: Dict[str, str] | str = Field(...)
    doc_id: Optional[str] = None

class HealthCheck(BaseModel):
    status: str
    version: str
    models_loaded: bool