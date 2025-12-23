from mcp.server.fastmcp import FastMCP
from fhir_models import Patient, Bundle
import json

# Initialize FastMCP Server
mcp = FastMCP("FHIR MCP Server")

@mcp.tool()
def get_patient_context(patient_id: str) -> str:
    """
    Fetches patient details from the FHIR server.
    Returns the Patient resource as a JSON string.
    """
    # Mock Data Logic (Migrated from InitialAgent)
    patient = Patient(
        id=patient_id,
        name=[{"family": "Argonaut", "given": ["Jason"]}],
        gender="male",
        birthDate="1985-08-01"
    )
    return patient.model_dump_json()

@mcp.tool()
def save_bundle(bundle: dict) -> str:
    """
    Persists the bundle to the FHIR server.
    Input should be a FHIR Bundle dict.
    Returns a success message.
    """
    # Validation / "Saving" Logic (Migrated from OutboundAgent)
    try:
        # verify it parses as a bundle
        valid_bundle = Bundle(**bundle)
        
        # Simulate saving
        # In a real scenario, this would POST to a real FHIR API
        
        # For our mock implementation, we just return success
        return f"Successfully saved Bundle with {len(valid_bundle.entry)} entries."
    except Exception as e:
        return f"Error saving bundle: {str(e)}"

if __name__ == "__main__":
    mcp.run()
