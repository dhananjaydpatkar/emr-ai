# EMR Note Agent

A multi-agent system powered by **Google Gemini** that processes unstructured clinical notes and Patient FHIR resources to generate a structured FHIR Bundle.

## Architecture

This project uses a **5-Agent Pipeline** connected via **Model Context Protocol (MCP)**:

1.  **Initial Agent**: Fetches Patient Context via MCP tool (`get_patient_context`).
2.  **Extractor Agent**: Extracts unstructured data from the note.
3.  **Reconciler Agent**: Merges patient context with extracted data.
4.  **Validator Agent**: Validates the bundle against FHIR standards.
5.  **Outbound Agent**: Persists the final bundle via MCP tool (`save_bundle`).

See [design.md](design.md) for details on MCP integration and flexible architecture (e.g., swapping for WSO2).

## Prerequisites

-   Python 3.10+
-   Google Cloud API Key (`GOOGLE_API_KEY`)

## Installation

1.  **Clone & Setup**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

2.  **Configuration**:
    Create a `.env` file:
    ```bash
    GOOGLE_API_KEY="your_api_key_here"
    ```

## Usage

### 1. The FHIR MCP Server
The system runs a local MCP server (`fhir_mcp_server.py`) automatically as a subprocess when you run the pipeline. No separate start command is needed, though you can run it standalone to inspect tools:
```bash
mcp dev fhir_mcp_server.py
```

### 2. Run the Agent Pipeline
Run the main script to process a clinical note:

```bash
python main.py --note sample_data/note.txt --patient_id patient-123
```

### Output
The system will:
1.  Fetch patient `patient-123`.
2.  Extract data from `note.txt`.
3.  Validate and Save the result to `final_output.json`.

### Sample Run

```bash
.venv) dhananjaypatkar@Dhananjays-MacBook-Air emr-ai % python main.py --note sample_data/note.txt --patient_id patient-123

--- Connecting to FHIR MCP Server ---
--- Initializing Agents ---

[Step 1] Initial Agent: Fetching Patient Context...
InitialAgent: Fetching patient patient-123 via MCP...
Processing request of type CallToolRequest
Processing request of type ListToolsRequest
Context retrieved for: Jason Argonaut

[Step 2] Extractor Agent: Extracting FHIR Resources from Note...
Extraction complete. Found 9 resources.

[Step 3] Reconciler Agent: Reconciling Context and Extraction...
Reconciliation complete.

[Step 4] Validator Agent: Validating Bundle...
Validation complete.

[Step 5] Outbound Agent: Persisting Data...
OutboundAgent: Sending Bundle via MCP...
Processing request of type CallToolRequest
OutboundAgent: Received response: Successfully saved Bundle with 10 entries.
OutboundAgent: Saved to final_output.json for verification.
Pipeline successfully completed.

```

## Project Structure

```
.
├── agents/                  # The 5 Agents
│   ├── initial_agent.py
│   ├── extractor_agent.py
│   ├── reconciler_agent.py
│   ├── validator_agent.py
│   └── outbound_agent.py
├── main.py                  # Pipeline Orchestrator
├── fhir_mcp_server.py       # FHIR MCP Server (FastMCP)
├── fhir_models.py           # Pydantic Models
├── final_output.json        # Pipeline Output
├── design.md                # System Architecture
└── mcp_ecosystem_design.md  # Future MCP Integrations
```
