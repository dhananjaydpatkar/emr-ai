# EMR Note Agent Design & Architecture

This document outlines the architecture of the EMR Note Agent, a system designed to extract FHIR resources from clinical notes using a **5-Stage Multi-Agent Pipeline** powered by the **Model Context Protocol (MCP)**.

## Architecture Diagram

```mermaid
graph TD
    subgraph Inputs
        Note["Clinical Note (Text)"]
        PID["Patient ID"]
    end

    subgraph "External Systems"
        MCP_Server[("FHIR MCP Server")]
    end

    subgraph "Agent Workflow"
        Initial[**Initial Agent**<br>Fetch Patient Context]
        Extractor[**Extractor Agent**<br>Analyze Note]
        Reconciler[**Reconciler Agent**<br>Merge Context & Data]
        Validator[**Validator Agent**<br>Validate Compliance]
        Outbound[**Outbound Agent**<br>Persist Data]
    end

    subgraph Output
        Bundle[Final FHIR Bundle]
    end

    %% Flow
    PID --> Initial
    MCP_Server <-->|"MCP Tool Call"| Initial
    
    Initial -- "Patient Context" --> Reconciler
    Note --> Extractor
    Extractor -- "Extracted Resources" --> Reconciler
    
    Reconciler -- "Merged Bundle" --> Validator
    Validator -- "Validated Bundle" --> Outbound
    
    Outbound -->|"MCP Tool Call"| MCP_Server
    Outbound --> Bundle

    %% Styling
    style Initial fill:#e1f5fe,stroke:#01579b
    style Extractor fill:#f3e5f5,stroke:#4a148c
    style Reconciler fill:#fff3e0,stroke:#e65100
    style Validator fill:#e8f5e9,stroke:#1b5e20
    style Outbound fill:#ffebee,stroke:#b71c1c
    style MCP_Server fill:#eee,stroke:#333,stroke-dasharray: 5 5
```

## Components

### 1. Initial Agent (Context Fetcher)
*   **Role**: Retrieval of patient context.
*   **Input**: Patient ID.
*   **Action**: Calls `get_patient_context` tool via MCP session.
*   **Output**: `Patient` resource.

### 2. Extractor Agent (Clinical Logic)
*   **Role**: Core medical concept extraction.
*   **Input**: Clinical Note text.
*   **Action**: Uses LLM to identify Entities (Conditions, Meds, Vitals) and map to FHIR resources.
*   **Output**: Unlinked/Partial FHIR Bundle.

### 3. Reconciler Agent (Data Merger)
*   **Role**: Logic & consistency.
*   **Input**: Patient Context + Extracted Resources.
*   **Action**:
    *   Injects the correct Patient ID into all resources.
    *   Resolves relative dates.
    *   Ensures implicit links are made explicit (e.g., Encounter links).
*   **Output**: A cohesive, linked FHIR Bundle.

### 4. Validator Agent (Quality Assurance)
*   **Role**: Compliance checking.
*   **Input**: Reconciled Bundle.
*   **Action**:
    *   Checks for required FHIR fields.
    *   Verifies terminology standards (ICD-10, CPT, etc.).
    *   Fixes minor structural errors.
*   **Output**: Validated FHIR Bundle.

### 5. Outbound Agent (Persistence)
*   **Role**: System interface.
*   **Input**: Validated Bundle.
*   **Action**: Calls `save_bundle` tool via MCP session.
*   **Output**: Commit status / Final JSON output.

## MCP Integration & Future Flexibility

This system is built using the **Model Context Protocol (MCP)** to abstract the FHIR server interaction.
*   **Current State**: Includes a local `fhir_mcp_server.py` using FastMCP for testing and development.
*   **Future/Production**: The `fhir_mcp_server.py` can be swapped for a production-grade MCP server, such as **WSO2's FHIR MCP Server** or any other MCP-compliant interface, without changing the agent code. The agents simply call `get_patient_context` or `save_bundle` regardless of the underlying implementation.

## Key Features

*   **Sequential Chaining**: Each agent performs a specialized task.
*   **Context Isolation**: The Extractor focuses only on text, while the Reconciler handles business logic.
*   **Protocol Agnostic**: Interacts via standard MCP tools, enabling easy integration with enterprise FHIR gateways.
