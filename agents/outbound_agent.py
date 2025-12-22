import json
from fhir_models import Bundle

class OutboundAgent:
    def __init__(self, fhir_server_url: str = "http://mock-fhir-server.org"):
        self.fhir_server_url = fhir_server_url

    def save_bundle(self, bundle: Bundle):
        """
        Persists the bundle to the FHIR server.
        """
        print(f"OutboundAgent: Sending Bundle to {self.fhir_server_url}...")
        
        # Simulate FHIR Transaction POST
        bundle_json = bundle.model_dump_json(indent=2)
        
        # Logging "transmission"
        print("OutboundAgent: Successfully transmitted Bundle.")
        
        # Also save to file for verification
        with open("final_output.json", "w") as f:
            f.write(bundle_json)
        print("OutboundAgent: Saved to final_output.json for verification.")
