from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import List
import os
from app.services.file_processor import FileProcessor
from app.agents.classification_agent import ClassificationAgent
from app.agents.extraction_agent import ExtractionAgent
from app.agents.validation_agent import ValidationAgent
from app.schemas.models import ProcessedClaimResponse
import logging

app = FastAPI(title="HealthPay Claim Processor",
              description="AI-powered medical claim processing system")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/process-claim", response_model=ProcessedClaimResponse)
async def process_claim(files: List[UploadFile] = File(...)):
    try:
        # 1. Save and process uploaded files
        file_data = [(file.filename, await file.read()) for file in files]
        processed_files = await FileProcessor.process_uploaded_files(file_data)
        
        # 2. Classify documents
        classifier = ClassificationAgent()
        classified_docs = await classifier.classify_documents(processed_files)
        
        # 3. Extract data from documents
        extractor = ExtractionAgent()
        extracted_docs = await extractor.extract_document_data(classified_docs)
        
        # 4. Validate claim
        validator = ValidationAgent()
        validation_result = await validator.validate_claim(extracted_docs)
        
        # 5. Prepare response
        response = {
            "documents": extracted_docs,
            "validation": validation_result["validation"].dict(),
            "claim_decision": validation_result["claim_decision"].dict()
        }
        
        return JSONResponse(content=response)
    
    except Exception as e:
        logger.error(f"Error processing claim: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}