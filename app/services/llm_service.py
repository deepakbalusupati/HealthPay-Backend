import google.generativeai as genai
from app.core.config import settings
from typing import Optional, Dict, Any
import json

class LLMService:
    def __init__(self):
        if not settings.google_api_key:
            raise ValueError("Google API key is not configured")
        genai.configure(api_key=settings.google_api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    async def classify_document(self, filename: str, text_content: str) -> str:
        prompt = f"""
        Classify this medical insurance document based on its filename and content.
        Possible types are: bill, discharge_summary, id_card, or unknown.
        
        Filename: {filename}
        Content: {text_content[:2000]}... [truncated]
        
        Return ONLY the document type (bill, discharge_summary, id_card, or unknown).
        """
        
        response = await self.model.generate_content_async(prompt)
        return response.text.strip().lower()
    
    async def extract_document_data(self, doc_type: str, text_content: str) -> Dict[str, Any]:
        prompt = f"""
        Extract structured data from this {doc_type} document. Return ONLY a JSON object with the following fields:
        
        {self._get_document_template(doc_type)}
        
        Document Content:
        {text_content[:4000]}... [truncated]
        """
        
        response = await self.model.generate_content_async(prompt)
        return self._parse_json_response(response.text)
    
    async def validate_claim(self, documents: list) -> Dict[str, Any]:
        prompt = """
        Validate these medical insurance claim documents for completeness and consistency.
        Check for:
        1. Required documents (bill, discharge summary, ID card)
        2. Consistent patient names across documents
        3. Date consistency (discharge date should be after admission, service date should match)
        4. Policy number presence in ID card
        
        Documents:
        {documents}
        
        Return a JSON object with:
        - missing_documents: list of missing document types
        - discrepancies: list of inconsistencies found
        - decision: approve/reject
        - reason: brief explanation
        """
        
        response = await self.model.generate_content_async(prompt.format(documents=documents))
        return self._parse_json_response(response.text)
    
    def _get_document_template(self, doc_type: str) -> str:
        templates = {
            "bill": "hospital_name: string, total_amount: number, date_of_service: date (YYYY-MM-DD)",
            "discharge_summary": "patient_name: string, diagnosis: string, admission_date: date (YYYY-MM-DD), discharge_date: date (YYYY-MM-DD)",
            "id_card": "patient_name: string, policy_number: string, expiry_date: date (YYYY-MM-DD) or null"
        }
        return templates.get(doc_type, "key_value_pairs: object")
    
    def _parse_json_response(self, text: str) -> Dict[str, Any]:
        try:
            # Clean the response text
            text = text.strip().strip('`').replace('json\n', '').replace('\n', '')
            return json.loads(text)
        except json.JSONDecodeError as e:
            return {"error": f"Failed to parse LLM response: {str(e)}"}