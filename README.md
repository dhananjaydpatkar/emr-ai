# EMR Note Agent

A multi-agent system powered by **Google Gemini** that processes unstructured clinical notes and Patient FHIR resources to generate a structured FHIR Bundle.

## Architecture

This project uses a **5-Agent Pipeline** to ensure accuracy and FHIR compliance:

1.  **Initial Agent**: Fetches Patient Context (Mock/Real FHIR Server).
2.  **Extractor Agent**: Extracts unstructured data from the note.
3.  **Reconciler Agent**: Merges patient context with extracted data.
4.  **Validator Agent**: Validates the bundle against FHIR standards.
5.  **Outbound Agent**: Persists the final bundle to the FHIR Server.

See [design.md](design.md) for details.

## Prerequisites

-   Python 3.9+
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

### 1. Start the Mock FHIR Server (Optional)
To verify endpoint connectivity, you can start the included mock server:

```bash
python mock_fhir_server.py
# Running on http://localhost:8080
```

*Note: The current agent implementation mocks the network calls internally for simplicity, but designed to work with this endpoint structure.*

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
(.venv) dhananjaypatkar@Dhananjays-MacBook-Air emr-note-agent % python main.py --note sample_data/note.txt --patient_id patient-123 
--- Initializing Agents ---

[Step 1] Initial Agent: Fetching Patient Context...
InitialAgent: Fetching patient patient-123 from http://mock-fhir-server.org...
Context retrieved for: Jason Argonaut

[Step 2] Extractor Agent: Extracting FHIR Resources from Note...
Extraction complete. Found 9 resources.

[Step 3] Reconciler Agent: Reconciling Context and Extraction...
Reconciliation complete.

[Step 4] Validator Agent: Validating Bundle...
Validation complete.

[Step 5] Outbound Agent: Persisting Data...
OutboundAgent: Sending Bundle to http://mock-fhir-server.org...
OutboundAgent: Successfully transmitted Bundle.
OutboundAgent: Saved to final_output.json for verification.
Pipeline successfully completed.
(.venv) dhananjaypatkar@Dhananjays-MacBook-Air emr-note-agent % 

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
├── mock_fhir_server.py      # Simple Mock Server
├── fhir_models.py           # Pydantic Models
└── final_output.json        # Pipeline Output
```
