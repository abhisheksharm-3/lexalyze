from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
import hashlib
from typing import Dict
from .models import LegalAnalysis, LegalQuery, HealthCheck
from .processor import LegalDocumentProcessor
from .config import SUPPORTED_FILE_TYPES, logger, analysis_cache
from .utils import (
    _compare_clauses, _compare_entities, _compare_obligations,
    _compare_deadlines, _compare_monetary_values
)

router = APIRouter()
legal_processor = LegalDocumentProcessor()

@router.get("/health", response_model=HealthCheck)
async def health_check():
    """Check API health status"""
    return HealthCheck(
        status="healthy",
        version="2.0.0",
        models_loaded=True
    )

@router.post("/analyze", response_model=LegalAnalysis)
async def analyze_document(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None
):
    """Analyze a legal document"""
    try:
        file_type = file.filename.split(".")[-1].lower()
        if file_type not in SUPPORTED_FILE_TYPES:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        content = await file.read()
        analysis = await legal_processor.analyze_document(content, file_type)

        # Cache the analysis
        analysis_cache[analysis.doc_id] = analysis

        return analysis
    except Exception as e:
        logger.error(f"Error analyzing document: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing document")

@router.post("/compare", response_model=Dict)
async def compare_documents(
    doc1: UploadFile = File(...),
    doc2: UploadFile = File(...)
):
    """Compare two legal documents"""
    try:
        file_type1 = doc1.filename.split(".")[-1].lower()
        file_type2 = doc2.filename.split(".")[-1].lower()

        if file_type1 != file_type2:
            raise HTTPException(status_code=400, detail="Documents must be of the same file type")

        content1 = await doc1.read()
        content2 = await doc2.read()

        analysis1 = await legal_processor.analyze_document(content1, file_type1)
        analysis2 = await legal_processor.analyze_document(content2, file_type2)

        comparison = {
            "clauses": _compare_clauses(analysis1.key_clauses, analysis2.key_clauses),
            "entities": _compare_entities(analysis1.entities, analysis2.entities),
            "obligations": _compare_obligations(analysis1.obligations, analysis2.obligations),
            "deadlines": _compare_deadlines(analysis1.deadlines, analysis2.deadlines),
            "monetary_values": _compare_monetary_values(analysis1.monetary_values, analysis2.monetary_values)
        }

        return comparison
    except Exception as e:
        logger.error(f"Error comparing documents: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing documents")

@router.post("/query", response_model=Dict)
async def query_document(
    legal_query: LegalQuery
):
    """Query a legal document"""
    try:
        doc_id = legal_query.doc_id
        if doc_id and doc_id in analysis_cache:
            analysis = analysis_cache[doc_id]
        else:
            raise HTTPException(status_code=404, detail="Document not found")

        # Use the QA model to answer the query
        result = legal_processor.qa_model({
            "question": legal_query.question,
            "context": legal_query.context if legal_query.context else analysis.summary
        })

        return {
            "answer": result["answer"],
            "score": result["score"]
        }
    except Exception as e:
        logger.error(f"Error querying document: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing query")