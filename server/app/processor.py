import spacy
from transformers import pipeline
import PyPDF2
import io
import re
import nltk
import hashlib
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Optional, Tuple
from fastapi import HTTPException

from .models import (
    LegalEntities, LegalCitation, LegalClause, LegalAnalysis
)
from .config import logger, MODEL_CONFIGS, PATTERNS

# Download required NLTK data
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

class LegalDocumentProcessor:
    def __init__(self):
        self.nlp = spacy.load(MODEL_CONFIGS['spacy_model'])
        self.qa_model = pipeline("question-answering", model=MODEL_CONFIGS['qa_model'])
        self.summarizer = pipeline("summarization", model=MODEL_CONFIGS['summarizer'])
        
        # Legal-specific patterns
        self.citation_pattern = PATTERNS['citation']
        self.monetary_pattern = PATTERNS['monetary']
        self.date_pattern = PATTERNS['date']
        
        # Common legal terms and definitions
        self.legal_terms = self._load_legal_terms()

    @staticmethod
    def _load_legal_terms() -> Dict[str, str]:
        """Load common legal terms and their definitions"""
        return {
            "force majeure": "Unforeseeable circumstances that prevent someone from fulfilling a contract",
            "consideration": "Something of value given by both parties to a contract",
            "jurisdiction": "The official power to make legal decisions and judgments",
            "waiver": "Voluntary relinquishment of a known right",
            "indemnification": "Security or protection against a loss or other financial burden",
            "severability": "Contract provision that allows the contract to remain valid even if some parts are unenforceable",
            "precedent": "A previous court decision that guides future decisions on similar issues",
            "res judicata": "A matter that has been adjudicated by a competent court and may not be pursued further",
            "locus standi": "The right or capacity to bring an action or to appear in a court"
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
    def extract_legal_entities(self, doc) -> LegalEntities:
        """Extract legal entities from the document"""
        entities = defaultdict(set)
        
        for ent in doc.ents:
            if ent.label_ == "PERSON":
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
            year_match = re.search(r'\d{4}', citation_text)
            year = int(year_match.group()) if year_match else None
            
            citations.append(LegalCitation(
                citation_text=citation_text,
                year=year,
                source=self._determine_citation_source(citation_text),
                page=None
            ))
        
        return citations
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
    def _determine_citation_source(self, citation: str) -> Optional[str]:
        """Determine the source of a legal citation"""
        if "AIR" in citation:
            return "All India Reporter"
        elif "SCC" in citation:
            return "Supreme Court Cases"
        elif "SC" in citation:
            return "Supreme Court"
        elif "HC" in citation:
            return "High Court"
        elif "ILR" in citation:
            return "Indian Law Reports"
        return None

    def extract_clauses(self, doc) -> List[LegalClause]:
        """Extract and classify legal clauses"""
        clauses = []
        
        clause_patterns = {
            "indemnification": r"(?i)indemnif[iy]|hold\s+harmless",
            "termination": r"(?i)terminat(e|ion)|cancel(lation)?",
            "confidentiality": r"(?i)confidential|non-disclosure",
            "warranty": r"(?i)warrant(y|ies)|guarantee",
            "governing_law": r"(?i)govern(ing)?\s+law|jurisdiction",
            "force_majeure": r"(?i)force\s+majeure|acts?\s+of\s+god",
            "assignment": r"(?i)assign(ment)?|transfer\s+of\s+rights",
            "severability": r"(?i)sever(ability)?|invalid|unenforceable"
        }
        
        for sent in doc.sents:
            for clause_type, pattern in clause_patterns.items():
                if re.search(pattern, sent.text):
                    clauses.append(LegalClause(
                        clause_type=clause_type,
                        text=sent.text,
                        importance=self._calculate_clause_importance(sent.text),
                        section="Unknown"
                    ))
        
        return clauses

    def _calculate_clause_importance(self, text: str) -> float:
        """Calculate importance score for a clause"""
        importance_terms = {
            "shall": 0.3,
            "must": 0.3,
            "will": 0.2,
            "agree": 0.2,
            "terminate": 0.4,
            "indemnify": 0.4,
            "warrant": 0.3,
            "material": 0.4,
            "breach": 0.4,
            "liable": 0.3
        }
        
        score = sum(importance_terms.get(word.lower(), 0)
                   for word in text.split())
        return min(1.0, score)

    def extract_deadlines(self, text: str) -> List[Dict[str, str]]:
        """Extract deadlines and time-sensitive information"""
        deadlines = []
        
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
            r"(?i)obligations?\s+[^\.]+",
            r"(?i)duties?\s+[^\.]+",
            r"(?i)responsible\s+for\s+[^\.]+",
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
    def _extract_governing_law(self, text: str) -> Optional[str]:
        """Extract the governing law from the text"""
        governing_law_patterns = [
            r"(?i)governed\s+by\s+the\s+laws\s+of\s+([^\.]+)",
            r"(?i)subject\s+to\s+the\s+jurisdiction\s+of\s+([^\.]+)",
            r"(?i)Indian\s+law",
            r"(?i)laws\s+of\s+India"
        ]
        
        for pattern in governing_law_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        return None

    def _extract_jurisdiction(self, text: str) -> Optional[str]:    
        """Extract the jurisdiction from the text"""
        jurisdiction_patterns = [
            r"(?i)courts\s+of\s+([^\.]+)",
            r"(?i)jurisdiction\s+of\s+([^\.]+)",
            r"(?i)subject\s+to\s+the\s+exclusive\s+jurisdiction\s+of\s+([^\.]+)"
        ]
        
        for pattern in jurisdiction_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        return None
    def _extract_risk_factors(self, doc) -> List[str]:
        """Extract potential risk factors from the document"""
        risk_factors = []
        
        for ent in doc.ents:
            if ent.label_ == "PERSON" and any(term in ent.text.lower() for term in ["judge", "justice", "honor"]):
                risk_factors.append(f"Potential bias from {ent.text}")
            elif ent.label_ == "ORG" and any(term in ent.text.lower() for term in ["court", "tribunal"]):
                risk_factors.append(f"Jurisdiction of {ent.text}")
            elif ent.label_ == "GPE" and ent.text.lower() in ["india", "delhi", "mumbai", "chennai", "kolkata"]:
                risk_factors.append(f"Compliance with {ent.text} laws and regulations")
            elif ent.label_ == "MONEY":
                risk_factors.append(f"Financial obligation of {ent.text}")
        
        return risk_factors
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
            
        # Generate summary
        summary = self.summarizer(text[:1024], 
                                max_length=150, 
                                min_length=50, 
                                do_sample=False)[0]['summary_text']
            
        # Extract deadlines
        deadlines = self.extract_deadlines(text)
        
        # Convert deadline dates to the correct format
        for deadline in deadlines:
            if deadline['date']:
                try:
                    deadline_dt = datetime.strptime(deadline['date'], '%Y-%m-%d')
                    deadline['date'] = deadline_dt.strftime('%Y-%m-%d')
                except (ValueError, TypeError):
                    deadline['date'] = None
        
        word_count = len(text.split())

        analysis = LegalAnalysis(
            doc_id=doc_id,
            document_type=self._determine_document_type(text),
            entities=self.extract_legal_entities(doc),
            key_clauses=self.extract_clauses(doc),
            citations=self.extract_citations(text),
            legal_definitions=self._extract_definitions(doc),
            obligations=self.extract_obligations(doc),
            deadlines=[
                {"text": d["text"], "date": d["date"], "context": d["context"]}
                for d in deadlines if d["date"] is not None
            ],
            jurisdiction=self._extract_jurisdiction(text),
            governing_law=self._extract_governing_law(text),
            risk_factors=self._extract_risk_factors(doc),
            monetary_values=self.extract_monetary_values(text),
            summary=summary,
            metadata={
                "file_type": file_type,
                "language": doc.lang_,
                "word_count": str(word_count),
                "created_at": datetime.now().isoformat()
            },
            word_count=word_count,
            created_at=datetime.now().isoformat(),
            processing_time=(datetime.now() - start_time).total_seconds()
        )

        return analysis