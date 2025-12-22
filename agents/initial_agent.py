from typing import Optional
from fhir_models import Patient

class InitialAgent:
    def __init__(self, fhir_server_url: str = "http://mock-fhir-server.org"):
        self.fhir_server_url = fhir_server_url

    def get_patient_context(self, patient_id: str) -> Patient:
        """
        Fetches patient details from the configured FHIR server.
        For now, returns a hardcoded mock patient.
        """
        print(f"InitialAgent: Fetching patient {patient_id} from {self.fhir_server_url}...")
        
        # Mock Patient Data
        return Patient(
            id=patient_id,
            name=[{"family": "Argonaut", "given": ["Jason"]}],
            gender="male",
            birthDate="1985-08-01"
        )
