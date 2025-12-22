from typing import List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime

# --- Base FHIR Types ---

class CodeableConcept(BaseModel):
    text: Optional[str] = None

class Reference(BaseModel):
    reference: str
    display: Optional[str] = None
    type: Optional[str] = None

class Period(BaseModel):
    start: Optional[datetime] = None
    end: Optional[datetime] = None

# --- Resources ---

class Resource(BaseModel):
    resourceType: str
    id: Optional[str] = None

class Patient(Resource):
    resourceType: str = "Patient"
    name: Optional[List[Any]] = None
    gender: Optional[str] = None
    birthDate: Optional[str] = None

class Encounter(Resource):
    resourceType: str = "Encounter"
    status: str
    class_attr: Optional[Any] = Field(alias="class", default=None)
    type: Optional[List[CodeableConcept]] = None
    subject: Optional[Reference] = None
    period: Optional[Period] = None
    reasonCode: Optional[List[CodeableConcept]] = None

class Condition(Resource):
    resourceType: str = "Condition"
    clinicalStatus: Optional[CodeableConcept] = None
    verificationStatus: Optional[CodeableConcept] = None
    category: Optional[List[CodeableConcept]] = None
    code: Optional[CodeableConcept] = None
    subject: Optional[Reference] = None
    encounter: Optional[Reference] = None
    onsetDateTime: Optional[datetime] = None
    recordedDate: Optional[datetime] = None

class MedicationRequest(Resource):
    resourceType: str = "MedicationRequest"
    status: str
    intent: str
    medicationCodeableConcept: Optional[CodeableConcept] = None
    subject: Optional[Reference] = None
    encounter: Optional[Reference] = None
    authoredOn: Optional[datetime] = None
    reasonReference: Optional[List[Reference]] = None
    dosageInstruction: Optional[List[Any]] = None

class Procedure(Resource):
    resourceType: str = "Procedure"
    status: str
    code: Optional[CodeableConcept] = None
    subject: Optional[Reference] = None
    encounter: Optional[Reference] = None
    performedDateTime: Optional[datetime] = None
    reasonReference: Optional[List[Reference]] = None

class ServiceRequest(Resource):
    resourceType: str = "ServiceRequest"
    status: str
    intent: str
    code: Optional[CodeableConcept] = None
    subject: Optional[Reference] = None
    reasonReference: Optional[List[Reference]] = None

class Observation(Resource):
    resourceType: str = "Observation"
    status: str
    category: Optional[List[CodeableConcept]] = None
    code: CodeableConcept
    subject: Optional[Reference] = None
    encounter: Optional[Reference] = None
    effectiveDateTime: Optional[datetime] = None
    valueQuantity: Optional[Any] = None
    valueString: Optional[str] = None
    component: Optional[List[Any]] = None

# --- Bundle ---

class BundleEntry(BaseModel):
    resource: Any
    request: Optional[Any] = None

class Bundle(Resource):
    resourceType: str = "Bundle"
    type: str = "transaction"
    entry: List[BundleEntry] = []
