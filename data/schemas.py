from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import date

class ClaimRecord(BaseModel):
    claim_id: str
    service_date: date
    payer_name: str
    payer_category: str
    cpt_code: Optional[str] = None
    charges: float = Field(default=0.0, ge=0)
    allowed_amount: float = Field(default=0.0, ge=0)
    payments: float = Field(default=0.0, ge=0)
    adjustments: float = Field(default=0.0, ge=0)
    patient_responsibility: float = Field(default=0.0, ge=0)
    pos_collections: float = Field(default=0.0, ge=0)
    claim_status: str
    denial_reason: Optional[str] = None
    denial_category: Optional[str] = None
    charge_entry_date: Optional[date] = None
    claim_submission_date: Optional[date] = None
    payment_date: Optional[date] = None
    facility: str = "Main Campus"

    @field_validator('service_date', mode='before')
    @classmethod
    def parse_date(cls, v):
        if isinstance(v, str):
            return date.fromisoformat(v)
        return v

class DataQualityReport(BaseModel):
    total_rows: int
    valid_rows: int
    invalid_rows: int
    missing_payer_name: int
    future_service_dates: int
    validation_errors: List[str]
    status: str = "success"
