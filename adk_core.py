import os
import google.generativeai as genai
from typing import Type, TypeVar, Optional, Any
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# Configure GenAI
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    # Fallback or warning. For now, assuming it will be present or user will set it.
    print("Warning: GOOGLE_API_KEY not found in environment variables.")
else:
    genai.configure(api_key=api_key)

T = TypeVar("T", bound=BaseModel)

class Agent:
    def __init__(self, model_name: str = "gemini-2.0-flash", system_instruction: str = ""):
        self.model_name = model_name
        self.system_instruction = system_instruction
        self.model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=system_instruction
        )

    def process(self, input_text: str, response_model: Optional[Type[T]] = None) -> T | str:
        """
        Process the input text.
        If response_model is provided, returns an instance of that Pydantic model.
        Otherwise, returns the raw text response.
        """
        generation_config = {}
        if response_model:
            generation_config["response_mime_type"] = "application/json"
            # Inject schema into prompt instead of using response_schema to avoid API limitations
            import json
            schema = response_model.model_json_schema()
            input_text += f"\n\nOutput must strictly follow this JSON schema:\n{json.dumps(schema, indent=2)}"
            # generation_config["response_schema"] = response_model

        response = self.model.generate_content(
            input_text,
            generation_config=genai.types.GenerationConfig(**generation_config)
        )

        if response_model:
            try:
                # The response.text should be JSON matching the schema
                return response_model.model_validate_json(response.text)
            except Exception as e:
                print(f"Error parsing JSON response: {e}")
                print(f"Raw response: {response.text}")
                raise e
        else:
            return response.text
