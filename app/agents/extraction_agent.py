from app.services.llm_service import LLMService
from app.schemas.models import DocumentType

class ExtractionAgent:
    def __init__(self):
        self.llm_service = LLMService()
    
    async def extract_document_data(self, classified_docs: list) -> list:
        extracted_docs = []
        for doc in classified_docs:
            try:
                extracted_data = await self.llm_service.extract_document_data(
                    doc["type"], doc["content"]
                )
                extracted_docs.append({
                    "type": doc["type"],
                    "content": extracted_data
                })
            except Exception as e:
                extracted_docs.append({
                    "type": doc["type"],
                    "content": {"error": str(e)}
                })
        return extracted_docs