from adk_core import Agent
from fhir_models import Bundle

class ValidatorAgent(Agent):
    def __init__(self):
        system_instruction = """
        You are a FHIR Validator Agent.
        Your task is to validate the FHIR Bundle for structural correctness and clinical plausibility.
        
        Check for:
        1. Required fields are present (e.g., status, code).
        2. References are valid (e.g., MedicationRequest points to a valid Patient).
        3. Coding systems are standard (ICD-10, CPT, LOINC, RxNorm).
        4. Logical consistency (e.g., Discharge date after Admission date).
        
        If you find minor errors (e.g., missing status where it can be inferred), FIX THEM.
        If the bundle is valid, return it as is.
        
        Input: a FHIR Bundle (JSON).
        Output: The VALIDATED (and potentially fixed) FHIR Bundle (JSON).
        """
        super().__init__(system_instruction=system_instruction)

    def validate(self, bundle: Bundle) -> Bundle:
        input_text = f"""
        Please validate and fix this FHIR Bundle:
        {bundle.model_dump_json(indent=2)}
        """
        
        return self.process(input_text, response_model=Bundle)
