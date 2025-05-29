from app.services.llm_service import LLMService
from app.schemas.models import DocumentType
import logging

logger = logging.getLogger(__name__)

class ClassificationAgent:
    def __init__(self):
        self.llm_service = LLMService()
    
    async def classify_documents(self, files: list) -> list:
        classified_docs = []
        for file in files:
            try:
                doc_type = await self.llm_service.classify_document(
                    file["filename"], file["content"]
                )
                classified_docs.append({
                    "filename": file["filename"],
                    "content": file["content"],
                    "type": doc_type
                })
            except Exception as e:
                logger.error(f"Classification failed for {file['filename']}: {str(e)}")
                classified_docs.append({
                    "filename": file["filename"],
                    "content": file["content"],
                    "type": "unknown",
                    "error": str(e)
                })
        return classified_docs