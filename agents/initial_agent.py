from typing import Optional
from fhir_models import Patient
from mcp import ClientSession

class InitialAgent:
    def __init__(self, mcp_session: ClientSession):
        self.mcp_session = mcp_session

    async def get_patient_context(self, patient_id: str) -> Patient:
        """
        Fetches patient details from the configured FHIR MCP server.
        """
        print(f"InitialAgent: Fetching patient {patient_id} via MCP...")
        
        # Call the MCP tool
        result = await self.mcp_session.call_tool("get_patient_context", arguments={"patient_id": patient_id})
        
        # Parse result (result.content is a list of Content objects, usually TextContent)
        # We assume the first text content is our JSON string
        patient_json = result.content[0].text
        
        return Patient.model_validate_json(patient_json)
