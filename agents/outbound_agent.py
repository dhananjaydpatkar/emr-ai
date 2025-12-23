import json
from fhir_models import Bundle
from mcp import ClientSession

class OutboundAgent:
    def __init__(self, mcp_session: ClientSession):
        self.mcp_session = mcp_session

    async def save_bundle(self, bundle: Bundle):
        """
        Persists the bundle to the FHIR server via MCP.
        """
        print(f"OutboundAgent: Sending Bundle via MCP...")
        
        # Call the MCP tool
        result = await self.mcp_session.call_tool("save_bundle", arguments={"bundle": bundle.model_dump()})
        
        print(f"OutboundAgent: Received response: {result.content[0].text}")
        
        # Also save to file for verification (local artifact)
        with open("final_output.json", "w") as f:
            f.write(bundle.model_dump_json(indent=2))
        print("OutboundAgent: Saved to final_output.json for verification.")
