import os
import argparse
from typing import Optional

from agents.initial_agent import InitialAgent
from agents.extractor_agent import ExtractorAgent
from agents.reconciler_agent import ReconcilerAgent
from agents.validator_agent import ValidatorAgent
from agents.outbound_agent import OutboundAgent

def read_note(file_path: str) -> str:
    with open(file_path, "r") as f:
        return f.read()

import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

def main():
    parser = argparse.ArgumentParser(description="EMR Note Agent - Multi-Agent Pipeline")
    parser.add_argument("--note", type=str, default="sample_data/note.txt", help="Path to clinical note")
    parser.add_argument("--patient_id", type=str, default="patient-123", help="Patient ID to fetch context")
    args = parser.parse_args()

    asyncio.run(run_pipeline(args))

async def run_pipeline(args):
    # 1. Initialize MCP Connection
    print("--- Connecting to FHIR MCP Server ---")
    
    # We run the local server as a subprocess
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["fhir_mcp_server.py"],
        env=None # Inherit env
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # 2. Initialize Agents
            print("--- Initializing Agents ---")
            initial_agent = InitialAgent(mcp_session=session)
            extractor_agent = ExtractorAgent()
            reconciler_agent = ReconcilerAgent()
            validator_agent = ValidatorAgent()
            outbound_agent = OutboundAgent(mcp_session=session)

            # 3. Pipeline Execution
            try:
                # Step 1: Initial Agent (Context)
                print("\n[Step 1] Initial Agent: Fetching Patient Context...")
                # Async call
                patient_context = await initial_agent.get_patient_context(args.patient_id)
                print(f"Context retrieved for: {patient_context.name[0]['given'][0]} {patient_context.name[0]['family']}")

                # Step 2: Extractor Agent (Extraction)
                print("\n[Step 2] Extractor Agent: Extracting FHIR Resources from Note...")
                note_text = read_note(args.note)
                extracted_bundle = extractor_agent.extract(note_text, patient_context)
                print(f"Extraction complete. Found {len(extracted_bundle.entry)} resources.")

                # Step 3: Reconciler Agent (Merging)
                print("\n[Step 3] Reconciler Agent: Reconciling Context and Extraction...")
                reconciled_bundle = reconciler_agent.reconcile(patient_context, extracted_bundle)
                print("Reconciliation complete.")

                # Step 4: Validator Agent (Validation)
                print("\n[Step 4] Validator Agent: Validating Bundle...")
                min_validated_bundle = validator_agent.validate(reconciled_bundle)
                print("Validation complete.")

                # Step 5: Outbound Agent (Persistence)
                print("\n[Step 5] Outbound Agent: Persisting Data...")
                # Async call
                await outbound_agent.save_bundle(min_validated_bundle)
                print("Pipeline successfully completed.")

            except Exception as e:
                print(f"\n[ERROR] Pipeline failed: {e}")
                import traceback
                traceback.print_exc()

if __name__ == "__main__":
    main()
