from typing import Any
from adk_core import Agent
from fhir_models import Bundle, Patient

class ReconcilerAgent(Agent):
    def __init__(self):
        system_instruction = """
        You are a FHIR Reconciler Agent.
        Your task is to merge the Patient Context with the Extracted FHIR Resources.
        
        Rules:
        1. Ensure the Patient Resource in the Bundle matches the Patient Context (ID, Name, etc.).
        2. Ensure ALL other resources (Encounters, Conditions, etc.) are linked to this Patient ID.
        3. If the extracted bundle contains a placeholder Patient, REPLACE it with the Patient Context.
        4. Validate consistency between resources (e.g. Encounter dates vs Observation dates).
        
        Input:
        - Patient Context (JSON)
        - Extracted Bundle (JSON)
        
        Output:
        - A single, valid FHIR Bundle containing the merged data.
        """
        super().__init__(system_instruction=system_instruction)

    def reconcile(self, patient_context: Patient, extracted_bundle: Bundle) -> Bundle:
        input_text = f"""
        Patient Context:
        {patient_context.model_dump_json(indent=2)}
        
        Extracted Bundle:
        {extracted_bundle.model_dump_json(indent=2)}
        """
        
        return self.process(input_text, response_model=Bundle)
