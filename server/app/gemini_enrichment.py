import json
from typing import Dict, Any
from datetime import datetime
import google.generativeai as genai

from .models import LegalAnalysis
from .config import logger, GEMINI_API_KEY

def initialize_gemini_model():
    """Initialize and return the Gemini model"""
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        logger.error(f"Failed to initialize Gemini model: {str(e)}")
        return None

def enrich_legal_analysis(analysis: LegalAnalysis) -> LegalAnalysis:
    """
    Enrich legal analysis using Gemini AI
    
    Args:
        analysis (LegalAnalysis): The initial legal analysis to be enriched
    
    Returns:
        LegalAnalysis: Enhanced legal analysis with additional insights
    """
    # Initialize Gemini model
    gemini_model = initialize_gemini_model()
    if not gemini_model:
        logger.warning("Gemini model not initialized. Returning original analysis.")
        return analysis

    try:
        # Prepare a comprehensive prompt for Gemini
        enrichment_prompt = f"""
        Analyze and enhance the following legal document insights:

        Document Type: {analysis.document_type}
        Summary: {analysis.summary}

        Key Details:
        - Entities: {', '.join(analysis.entities.parties + analysis.entities.organizations)}
        - Jurisdiction: {analysis.jurisdiction or 'Not specified'}
        - Governing Law: {analysis.governing_law or 'Not specified'}
        
        Key Clauses: {', '.join([clause.clause_type for clause in analysis.key_clauses])}
        
        Deadlines: {', '.join([d['text'] for d in analysis.deadlines])}
        
        Risk Factors: {', '.join(analysis.risk_factors)}

        Tasks:
        1. Provide a more nuanced and professional summary
        2. Identify potential legal risks or opportunities
        3. Suggest potential areas of further investigation
        4. Clean up and standardize the extracted information
        5. Add contextual insights based on the document type and content

        Respond in the following JSON format:
        {{
            "enhanced_summary": "string",
            "additional_risk_factors": ["string"],
            "suggested_investigations": ["string"],
            "key_insights": ["string"]
        }}

        Don't Add any language or markdown decorators, just pure json response is needed.
        """

        # Generate enrichment response
        response = gemini_model.generate_content(enrichment_prompt)
        
        # Parse and integrate Gemini's insights
        try:
            gemini_insights = json.loads(response.text)
            
            # Update analysis with Gemini's enrichments
            if 'enhanced_summary' in gemini_insights:
                analysis.summary = gemini_insights.get('enhanced_summary', analysis.summary)
            
            if 'additional_risk_factors' in gemini_insights:
                analysis.risk_factors.extend(gemini_insights.get('additional_risk_factors', []))
            
            # Add enrichment insights to metadata
            analysis.metadata['gemini_enrichments'] = {
                'suggested_investigations': gemini_insights.get('suggested_investigations', []),
                'key_insights': gemini_insights.get('key_insights', [])
            }
            
            # Add a flag to indicate Gemini enrichment
            analysis.metadata['enriched_by_gemini'] = True
            analysis.metadata['gemini_enrichment_timestamp'] = datetime.now().isoformat()
        
        except (json.JSONDecodeError, TypeError) as parse_error:
            logger.warning(f"Could not parse Gemini response: {str(parse_error)}")
            # Log the actual response for debugging
            logger.warning(f"Gemini response: {response.text}")
        
        return analysis
    
    except Exception as e:
        logger.error(f"Gemini enrichment failed: {str(e)}")
        # Return original analysis if enrichment fails
        return analysis
def enrich_qa_response(qa_response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Enrich and improve a QA model response using Gemini AI
    
    Args:
        qa_response (Dict[str, Any]): The original QA model response containing 'answer' and 'score'
    
    Returns:
        Dict[str, Any]: Enhanced QA response with additional insights
    """
    # Initialize Gemini model
    gemini_model = initialize_gemini_model()
    if not gemini_model:
        logger.warning("Gemini model not initialized. Returning original QA response.")
        return qa_response

    try:
        # Prepare a comprehensive prompt for Gemini to enhance the QA response
        enrichment_prompt = f"""
        Enhance the following question-answering response:

        Original Answer: {qa_response['answer']}
        Confidence Score: {qa_response['score']}

        Tasks:
        1. Refine and improve the answer's clarity, language, and professional tone
        2. Add contextual insights or additional relevant information
        3. Assess the completeness and accuracy of the original answer
        4. Suggest potential follow-up questions or areas of further investigation
        5. Provide a confidence assessment based on the original response

        Respond in the following JSON format:
        {{
            "enhanced_answer": "string",
            "additional_context": ["string"],
            "confidence_assessment": "string",
            "suggested_follow_up_questions": ["string"],
            "improved_score": float
        }}

        Don't Add any language or markdown decorators, just pure json response is needed.
        """

        # Generate enrichment response
        response = gemini_model.generate_content(enrichment_prompt)
        
        # Parse and integrate Gemini's insights
        try:
            gemini_insights = json.loads(response.text)
            
            # Update QA response with Gemini's enrichments
            enriched_response = {
                'answer': gemini_insights.get('enhanced_answer', qa_response['answer']),
                'score': gemini_insights.get('improved_score', qa_response['score']),
                'metadata': {
                    'additional_context': gemini_insights.get('additional_context', []),
                    'confidence_assessment': gemini_insights.get('confidence_assessment', ''),
                    'suggested_follow_up_questions': gemini_insights.get('suggested_follow_up_questions', []),
                    'original_score': qa_response['score']
                }
            }
            
            return enriched_response
        
        except (json.JSONDecodeError, TypeError) as parse_error:
            logger.warning(f"Could not parse Gemini QA response enrichment: {str(parse_error)}")
            # Log the actual response for debugging
            logger.warning(f"Gemini response: {response.text}")
            return qa_response
    
    except Exception as e:
        logger.error(f"Gemini QA response enrichment failed: {str(e)}")
        # Return original QA response if enrichment fails
        return qa_response