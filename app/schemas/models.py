from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date

class DocumentType(str, Enum):
    BILL = "bill"
    DISCHARGE_SUMMARY = "discharge_summary"
    ID_CARD = "id_card"
    UNKNOWN = "unknown"

class BillDocument(BaseModel):
    hospital_name: str = Field(..., description="Name of the hospital")
    total_amount: float = Field(..., description="Total amount billed")
    date_of_service: date = Field(..., description="Date of service")

class DischargeSummaryDocument(BaseModel):
    patient_name: str = Field(..., description="Name of the patient")
    diagnosis: str = Field(..., description="Diagnosis of the patient")
    admission_date: date = Field(..., description="Date of admission")
    discharge_date: date = Field(..., description="Date of discharge")

class IDCardDocument(BaseModel):
    patient_name: str = Field(..., description="Name of the patient")
    policy_number: str = Field(..., description="Insurance policy number")
    expiry_date: Optional[date] = Field(None, description="Expiry date of the ID card")

class Document(BaseModel):
    type: DocumentType = Field(..., description="Type of document")
    content: dict = Field(..., description="Extracted content from document")

class ValidationResult(BaseModel):
    missing_documents: List[str] = Field(default_factory=list)
    discrepancies: List[str] = Field(default_factory=list)

class ClaimDecision(BaseModel):
    status: str = Field(..., description="approve or reject")
    reason: str = Field(..., description="Reason for decision")

class ProcessedClaimResponse(BaseModel):
    documents: List[Document]
    validation: ValidationResult
    claim_decision: ClaimDecision