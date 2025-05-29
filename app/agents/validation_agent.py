from app.services.llm_service import LLMService
from app.schemas.models import ValidationResult, ClaimDecision

class ValidationAgent:
    def __init__(self):
        self.llm_service = LLMService()
    
    async def validate_claim(self, documents: list) -> dict:
        try:
            validation_result = await self.llm_service.validate_claim(documents)
            
            return {
                "validation": ValidationResult(**{
                    "missing_documents": validation_result.get("missing_documents", []),
                    "discrepancies": validation_result.get("discrepancies", [])
                }),
                "claim_decision": ClaimDecision(**{
                    "status": validation_result.get("decision", "reject").lower(),
                    "reason": validation_result.get("reason", "Validation failed")
                })
            }
        except Exception as e:
            return {
                "validation": ValidationResult(**{
                    "missing_documents": ["unknown"],
                    "discrepancies": [str(e)]
                }),
                "claim_decision": ClaimDecision(**{
                    "status": "reject",
                    "reason": f"Validation error: {str(e)}"
                })
            }