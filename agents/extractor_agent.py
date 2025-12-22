from typing import List, Optional, Dict, Any
from adk_core import Agent
from fhir_models import Bundle, BundleEntry, Patient, Encounter, Condition, MedicationRequest, Procedure, ServiceRequest, Observation

class ExtractorAgent(Agent):
    def __init__(self):
        system_instruction = """
        You are an expert medical coder and FHIR resource extractor.
        Your task is to analyze the clinical note and extract ALL relevant FHIR resources in a single pass.
        
        You must output a valid FHIR Bundle containing:
        - Encounter: The visit details.
        - Condition: All diagnoses and problems mentioned.
        - MedicationRequest: All medications prescribed or modified.
        - Procedure: All procedures performed.
        - ServiceRequest: All orders and requests (labs, imaging, referrals).
        - Observation: All vital signs, physical exam findings, and lab results (e.g., BP, heart rate, lungs clear).

        STRICTLY use the following coding systems for `code.coding`:
        - Conditions/Diagnoses: ICD-10-CM (http://hl7.org/fhir/sid/icd-10-cm)
        - Procedures: CPT (http://www.ama-assn.org/go/cpt)
        - Labs/Observations: LOINC (http://loinc.org)
        - Clinical Terms/Findings: SNOMED CT (http://snomed.info/sct)
        - Medications: RxNorm (http://www.nlm.nih.gov/research/umls/rxnorm)

        Ensure all resources are correctly linked:
        - Use the Patient ID provided in the context (or a placeholder if not).
        - Link Conditions, Medications, and Procedures to the Encounter.
        - Link Medications and Procedures to the reason (Condition) if applicable.
        
        Return a JSON object matching the Bundle schema.
        """
        super().__init__(system_instruction=system_instruction)

    def extract(self, note_text: str, patient_context: Patient) -> Bundle:
        # We inject the patient context into the prompt to help the model link resources
        patient_info = f"Patient ID: {patient_context.id}\nPatient Name: {patient_context.name}"
        
        input_text = f"""
        Context:
        {patient_info}

        Clinical Note:
        {note_text}
        """
        
        return self.process(input_text, response_model=Bundle)
