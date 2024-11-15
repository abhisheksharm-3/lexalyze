from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Set
import spacy
from transformers import pipeline, AutoTokenizer, AutoModelForQuestionAnswering
import PyPDF2
import io
import json
import hashlib
from datetime import datetime
import logging
import nltk
from nltk.tokenize import sent_tokenize
from collections import Counter, defaultdict
import re
import asyncio
from cachetools import TTLCache, LRUCache

# Download required NLTK data
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize caches
document_cache = TTLCache(maxsize=100, ttl=3600)  # 1-hour TTL
analysis_cache = LRUCache(maxsize=1000)

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

app = FastAPI(
    title="Legal Document Analysis API",
    description="Advanced legal document processing and analysis API",
    version="2.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LegalDocumentProcessor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.qa_model = pipeline("question-answering", model="deepset/roberta-base-squad2")
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        
        # Legal-specific patterns
        self.citation_pattern = r'\d+\s+[A-Za-z\.]+\s+\d+|[A-Z]+\s+v\.\s+[A-Z]+|\[\d+\]\s+[A-Za-z\s]+\s+\d+'
        self.monetary_pattern = r'\$\s*\d+(?:,\d{3})*(?:\.\d{2})?|\d+\s+dollars'
        self.date_pattern = r'\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}'
        
        # Common legal terms and definitions
        self.legal_terms = self._load_legal_terms()

    @staticmethod
    def _load_legal_terms() -> Dict[str, str]:
        """Load common legal terms and their definitions"""
        # This would typically load from a comprehensive legal terms database
        return {
            "force majeure": "Unforeseeable circumstances that prevent someone from fulfilling a contract",
            "consideration": "Something of value given by both parties to a contract",
            "jurisdiction": "The official power to make legal decisions and judgments",
            # Add more legal terms...
        }

    async def extract_text_from_pdf(self, content: bytes) -> str:
        """Extract text from PDF content"""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text.strip()
        except Exception as e:
            logger.error(f"PDF extraction error: {str(e)}")
            raise HTTPException(status_code=500, detail="Error processing PDF file")

    def extract_legal_entities(self, doc) -> LegalEntities:
        """Extract legal entities from the document"""
        entities = defaultdict(set)
        
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                # Attempt to classify person as judge, lawyer, or party
                context = doc[max(0, ent.start - 5):min(len(doc), ent.end + 5)].text.lower()
                if any(term in context for term in ["judge", "justice", "honor"]):
                    entities["judges"].add(ent.text)
                elif any(term in context for term in ["attorney", "counsel", "esq"]):
                    entities["lawyers"].add(ent.text)
                else:
                    entities["parties"].add(ent.text)
            elif ent.label_ == "ORG":
                if any(term in ent.text.lower() for term in ["court", "tribunal"]):
                    entities["courts"].add(ent.text)
                else:
                    entities["organizations"].add(ent.text)

        return LegalEntities(
            parties=list(entities["parties"]),
            judges=list(entities["judges"]),
            lawyers=list(entities["lawyers"]),
            courts=list(entities["courts"]),
            organizations=list(entities["organizations"])
        )

    def extract_citations(self, text: str) -> List[LegalCitation]:
        """Extract legal citations from text"""
        citations = []
        matches = re.finditer(self.citation_pattern, text)
        
        for match in matches:
            citation_text = match.group()
            # Parse citation components
            year_match = re.search(r'\d{4}', citation_text)
            year = int(year_match.group()) if year_match else None
            
            citations.append(LegalCitation(
                citation_text=citation_text,
                year=year,
                source=self._determine_citation_source(citation_text)
            ))
        
        return citations

    def _determine_citation_source(self, citation: str) -> Optional[str]:
        """Determine the source of a legal citation"""
        # Add logic to identify common citation sources
        if "U.S." in citation:
            return "United States Reports"
        elif "F.Supp." in citation:
            return "Federal Supplement"
        # Add more citation sources...
        return None

    def extract_clauses(self, doc) -> List[LegalClause]:
        """Extract and classify legal clauses"""
        clauses = []
        
        # Define clause patterns
        clause_patterns = {
            "indemnification": r"(?i)indemnif[iy]|hold\s+harmless",
            "termination": r"(?i)terminat(e|ion)|cancel(lation)?",
            "confidentiality": r"(?i)confidential|non-disclosure",
            "warranty": r"(?i)warrant(y|ies)|guarantee",
            "governing_law": r"(?i)govern(ing)?\s+law|jurisdiction",
        }
        
        for sent in doc.sents:
            for clause_type, pattern in clause_patterns.items():
                if re.search(pattern, sent.text):
                    clauses.append(LegalClause(
                        clause_type=clause_type,
                        text=sent.text,
                        importance=self._calculate_clause_importance(sent.text)
                    ))
        
        return clauses

    def _calculate_clause_importance(self, text: str) -> float:
        """Calculate importance score for a clause"""
        # Simple scoring based on key legal terms and phrase patterns
        importance_terms = {
            "shall": 0.3,
            "must": 0.3,
            "will": 0.2,
            "agree": 0.2,
            "terminate": 0.4,
            "indemnify": 0.4,
            "warrant": 0.3,
            "material": 0.4
        }
        
        score = sum(importance_terms.get(word.lower(), 0)
                   for word in text.split())
        return min(1.0, score)  # Normalize to 0-1

    def extract_deadlines(self, text: str) -> List[Dict[str, str]]:
        """Extract deadlines and time-sensitive information"""
        deadlines = []
        
        # Pattern for deadline-related phrases
        deadline_patterns = [
            r"(?i)within\s+(\d+)\s+(day|month|year)s?",
            r"(?i)no\s+later\s+than\s+([^\.]+)",
            r"(?i)deadline\s+[^\.]+",
            r"(?i)due\s+(?:date|by)\s+([^\.]+)"
        ]
        
        for pattern in deadline_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                deadline_text = match.group()
                date_match = re.search(self.date_pattern, deadline_text)
                deadlines.append({
                    "text": deadline_text,
                    "date": date_match.group() if date_match else None,
                    "context": text[max(0, match.start()-50):min(len(text), match.end()+50)]
                })
        
        return deadlines

    def extract_monetary_values(self, text: str) -> List[Dict[str, str]]:
        """Extract monetary values and related context"""
        monetary_values = []
        
        matches = re.finditer(self.monetary_pattern, text)
        for match in matches:
            monetary_values.append({
                "value": match.group(),
                "context": text[max(0, match.start()-50):min(len(text), match.end()+50)]
            })
        
        return monetary_values

    def extract_obligations(self, doc) -> List[Dict[str, str]]:
        """Extract legal obligations"""
        obligations = []
        
        obligation_patterns = [
            r"(?i)shall\s+[^\.]+",
            r"(?i)must\s+[^\.]+",
            r"(?i)agrees?\s+to\s+[^\.]+",
            r"(?i)required\s+to\s+[^\.]+",
        ]
        
        for sent in doc.sents:
            for pattern in obligation_patterns:
                if re.search(pattern, sent.text):
                    obligations.append({
                        "text": sent.text,
                        "type": "mandatory" if any(word in sent.text.lower() 
                                                 for word in ["shall", "must"]) 
                               else "contractual"
                    })
        
        return obligations

    async def analyze_document(self, content: bytes, file_type: str) -> LegalAnalysis:
        """Perform comprehensive legal document analysis"""
        start_time = datetime.now()
        
        # Extract text based on file type
        if file_type == 'pdf':
            text = await self.extract_text_from_pdf(content)
        else:
            text = content.decode().strip()
            
        # Generate document ID
        doc_id = hashlib.md5(text.encode()).hexdigest()
        
        # Process with spaCy
        doc = self.nlp(text)
        
        # Extract document type
        document_type = self._determine_document_type(text)
        
        # Generate summary
        summary = self.summarizer(text[:1024], 
                                max_length=150, 
                                min_length=50, 
                                do_sample=False)[0]['summary_text']
        
        # Perform comprehensive analysis
        analysis = LegalAnalysis(
            doc_id=doc_id,
            document_type=document_type,
            entities=self.extract_legal_entities(doc),
            key_clauses=self.extract_clauses(doc),
            citations=self.extract_citations(text),
            legal_definitions=self._extract_definitions(doc),
            obligations=self.extract_obligations(doc),
            deadlines=self.extract_deadlines(text),
            jurisdiction=self._extract_jurisdiction(text),
            governing_law=self._extract_governing_law(text),
            risk_factors=self._extract_risk_factors(doc),
            monetary_values=self.extract_monetary_values(text),
            summary=summary,
            metadata={
                "file_type": file_type,
                "language": doc.lang_,
                "processed_at": datetime.now().isoformat()
            },
            processing_time=(datetime.now() - start_time).total_seconds(),
            word_count=len(doc),
            created_at=datetime.now().isoformat()
        )
        
        # Cache the analysis
        analysis_cache[doc_id] = analysis
        
        return analysis

    def _determine_document_type(self, text: str) -> str:
        """Determine the type of legal document"""
        text_lower = text.lower()
        
        document_types = {
            "contract": ["agreement", "contract", "terms and conditions"],
            "court_filing": ["motion", "petition", "complaint", "brief"],
            "legislation": ["act", "statute", "bill", "regulation"],
            "opinion": ["opinion", "decision", "order", "judgment"],
        }
        
        for doc_type, keywords in document_types.items():
            if any(keyword in text_lower for keyword in keywords):
                return doc_type
                
        return "other"

    def _extract_definitions(self, doc) -> Dict[str, str]:
        """Extract defined terms and their definitions"""
        definitions = {}
        
        # Pattern for common definition structures
        definition_patterns = [
            r'(?i)"([^"]+)"\s+means\s+([^\.]+)',
            r'(?i)"([^"]+)"\s+shall\s+mean\s+([^\.]+)',
            r'(?i)term\s+"([^"]+)"\s+is\s+defined\s+as\s+([^\.]+)',
            r'(?i)"([^"]+)"\s+refers\s+to\s+([^\.]+)'
        ]
        
        text = doc.text
        for pattern in definition_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                term, definition = match.groups()
                definitions[term.strip()] = definition.strip()

        return definitions

    def _extract_jurisdiction(self, text: str) -> Optional[str]:
        """Extract jurisdiction information"""
        jurisdiction_patterns = [
            r'(?i)jurisdiction\s+of\s+([^\.]+)',
            r'(?i)under\s+the\s+laws\s+of\s+([^\.]+)',
            r'(?i)in\s+the\s+state\s+of\s+([^\.]+)',
            r'(?i)in\s+the\s+country\s+of\s+([^\.]+)'
        ]
        
        for pattern in jurisdiction_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        return None

    def _extract_governing_law(self, text: str) -> Optional[str]:
        """Extract governing law information"""
        governing_law_patterns = [
            r'(?i)governed\s+by\s+the\s+laws\s+of\s+([^\.]+)',
            r'(?i)governing\s+law[^\.]+?(?:shall\s+be|is)\s+([^\.]+)',
            r'(?i)interpreted\s+under\s+the\s+laws\s+of\s+([^\.]+)'
        ]
        
        for pattern in governing_law_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        return None

    def _extract_risk_factors(self, doc) -> List[str]:
        """Extract potential risk factors and warnings"""
        risk_factors = []
        
        risk_patterns = [
            r'(?i)risk\s+factor',
            r'(?i)warning',
            r'(?i)disclaimer',
            r'(?i)limitation\s+of\s+liability',
            r'(?i)indemnification',
            r'(?i)may\s+result\s+in',
            r'(?i)could\s+lead\s+to'
        ]
        
        for sent in doc.sents:
            if any(re.search(pattern, sent.text) for pattern in risk_patterns):
                risk_factors.append(sent.text.strip())
        
        return risk_factors

# Initialize processor
legal_processor = LegalDocumentProcessor()

@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Check API health status"""
    return HealthCheck(
        status="healthy",
        version="2.0.0",
        models_loaded=True
    )

@app.post("/api/analyze", response_model=LegalAnalysis)
async def analyze_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
):
    """
    Analyze a legal document and extract key information
    """
    try:
        content = await file.read()
        file_type = 'pdf' if file.filename.endswith('.pdf') else 'txt'
        
        # Check cache first
        doc_id = hashlib.md5(content).hexdigest()
        if doc_id in analysis_cache:
            return analysis_cache[doc_id]
        
        # Process document
        analysis = await legal_processor.analyze_document(
            content,
            file_type
        )
        
        # Schedule background task for additional processing
        background_tasks.add_task(
            perform_deep_analysis,
            doc_id,
            content
        )
        
        return analysis
        
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing document: {str(e)}"
        )

@app.post("/api/query", response_model=Dict[str, str])
async def answer_legal_query(query: LegalQuery):
    """
    Answer legal questions about the document
    """
    try:
        if query.doc_id and query.doc_id in analysis_cache:
            analysis = analysis_cache[query.doc_id]
            context_text = (
                f"{analysis.summary} "
                f"Key clauses: {' '.join([c.text for c in analysis.key_clauses])} "
                f"Obligations: {' '.join([o['text'] for o in analysis.obligations])}"
            )
        else:
            context_text = (query.context if isinstance(query.context, str) 
                          else json.dumps(query.context))

        # Get answer using QA model
        answer = legal_processor.qa_model(
            question=query.question.strip(),
            context=context_text.strip()
        )

        return {"answer": answer["answer"]}

    except Exception as e:
        logger.error(f"Query error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )

@app.post("/api/extract-clauses")
async def extract_clauses(file: UploadFile = File(...)):
    """
    Extract and analyze specific clauses from a legal document
    """
    try:
        content = await file.read()
        file_type = 'pdf' if file.filename.endswith('.pdf') else 'txt'
        
        if file_type == 'pdf':
            text = await legal_processor.extract_text_from_pdf(content)
        else:
            text = content.decode().strip()
            
        doc = legal_processor.nlp(text)
        clauses = legal_processor.extract_clauses(doc)
        
        return {
            "clauses": [clause.dict() for clause in clauses],
            "count": len(clauses)
        }
    
    except Exception as e:
        logger.error(f"Clause extraction error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error extracting clauses: {str(e)}"
        )

@app.post("/api/compare-documents")
async def compare_documents(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...)
):
    """
    Compare two legal documents and identify key differences
    """
    try:
        # Process both documents
        content1 = await file1.read()
        content2 = await file2.read()
        
        analysis1 = await legal_processor.analyze_document(
            content1,
            'pdf' if file1.filename.endswith('.pdf') else 'txt'
        )
        
        analysis2 = await legal_processor.analyze_document(
            content2,
            'pdf' if file2.filename.endswith('.pdf') else 'txt'
        )
        
        # Compare key aspects
        comparison = {
            "different_clauses": _compare_clauses(
                analysis1.key_clauses,
                analysis2.key_clauses
            ),
            "different_entities": _compare_entities(
                analysis1.entities,
                analysis2.entities
            ),
            "different_obligations": _compare_obligations(
                analysis1.obligations,
                analysis2.obligations
            ),
            "different_deadlines": _compare_deadlines(
                analysis1.deadlines,
                analysis2.deadlines
            ),
            "different_monetary_values": _compare_monetary_values(
                analysis1.monetary_values,
                analysis2.monetary_values
            )
        }
        
        return comparison
        
    except Exception as e:
        logger.error(f"Document comparison error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error comparing documents: {str(e)}"
        )

async def perform_deep_analysis(doc_id: str, content: bytes):
    """Perform additional deep analysis in background"""
    try:
        # Add any additional analysis tasks here
        # For example: risk assessment, compliance checking, etc.
        pass
    except Exception as e:
        logger.error(f"Deep analysis error: {str(e)}")

def _compare_clauses(clauses1: List[LegalClause], clauses2: List[LegalClause]) -> Dict:
    """Compare clauses between two documents"""
    return {
        "unique_to_first": [c.dict() for c in clauses1 if not any(
            c.text == c2.text for c2 in clauses2
        )],
        "unique_to_second": [c.dict() for c in clauses2 if not any(
            c.text == c1.text for c1 in clauses1
        )],
        "modified": [
            {"from": c1.dict(), "to": c2.dict()}
            for c1 in clauses1
            for c2 in clauses2
            if c1.clause_type == c2.clause_type and c1.text != c2.text
        ]
    }

def _compare_entities(entities1: LegalEntities, entities2: LegalEntities) -> Dict:
    """Compare legal entities between documents"""
    return {
        "parties_changed": set(entities1.parties) != set(entities2.parties),
        "new_parties": list(set(entities2.parties) - set(entities1.parties)),
        "removed_parties": list(set(entities1.parties) - set(entities2.parties)),
        "organizations_changed": set(entities1.organizations) != set(entities2.organizations),
        "new_organizations": list(set(entities2.organizations) - set(entities1.organizations))
    }

def _compare_obligations(obligations1: List[Dict], obligations2: List[Dict]) -> Dict:
    """Compare obligations between documents"""
    return {
        "added": [o for o in obligations2 if o not in obligations1],
        "removed": [o for o in obligations1 if o not in obligations2]
    }

def _compare_deadlines(deadlines1: List[Dict], deadlines2: List[Dict]) -> Dict:
    """Compare deadlines between documents"""
    return {
        "changed": [
            {"from": d1, "to": d2}
            for d1 in deadlines1
            for d2 in deadlines2
            if d1["text"] != d2["text"] and any(
                word in d1["text"] for word in d2["text"].split()
            )
        ],
        "added": [d for d in deadlines2 if d not in deadlines1],
        "removed": [d for d in deadlines1 if d not in deadlines2]
    }

def _compare_monetary_values(values1: List[Dict], values2: List[Dict]) -> Dict:
    """Compare monetary values between documents"""
    return {
        "changed": [
            {"from": v1, "to": v2}
            for v1 in values1
            for v2 in values2
            if v1["value"] != v2["value"] and v1["context"] == v2["context"]
        ],
        "added": [v for v in values2 if v not in values1],
        "removed": [v for v in values1 if v not in values2]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)