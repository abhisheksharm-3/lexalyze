# main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import spacy
from transformers import pipeline
import PyPDF2
import io

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize NLP models
nlp = spacy.load("en_core_web_sm")
qa_model = pipeline("question-answering")
summarizer = pipeline("summarization")

class Query(BaseModel):
    question: str
    context: dict | str

class DocumentAnalysis(BaseModel):
    entities: dict
    summary: str
    key_points: List[str]

@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    """Handle document upload and initial processing"""
    try:
        content = await file.read()
        
        # Handle PDF files
        if file.filename.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        else:
            text = content.decode()
        
        # Process document
        doc = nlp(text)
        
        # Extract entities
        entities = {
            "organizations": [ent.text for ent in doc.ents if ent.label_ == "ORG"],
            "dates": [ent.text for ent in doc.ents if ent.label_ == "DATE"],
            "people": [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
        }
        
        # Generate summary
        summary = summarizer(text[:1024], max_length=150, min_length=50)[0]['summary_text']
        
        # Extract key points
        sentences = [sent.text.strip() for sent in doc.sents]
        key_points = sentences[:5]  # Simplified; you might want to use importance scoring
        
        return DocumentAnalysis(
            entities=entities,
            summary=summary,
            key_points=key_points
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/query")
async def answer_query(query: Query):
    """Answer questions about the document"""
    try:
        if not query.question or not query.context:
            raise HTTPException(status_code=400, detail="Question and context must not be empty")
            
        context_text = query.context if isinstance(query.context, str) else str(query.context)
        answer = qa_model(
            question=query.question.strip(),
            context=context_text.strip()
        )
        return {"answer": answer["answer"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run with: uvicorn main:app --reload