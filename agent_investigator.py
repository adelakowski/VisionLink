import torch
from transformers import pipeline
import os
from dotenv import load_dotenv

load_dotenv()

# Phase 3: Agent B - The Investigator
# Model: MedGemma 1.5 4B-IT (google/medgemma-1.5-4b-it)
# This model represents the state-of-the-art medical instruction tuned model as of Jan 2026.
# It is built on Gemma 3 architecture.

# NOTE: If "google/medgemma-1.5-4b-it" is not available/public, we will need to fallback.
# For now, we attempt to load it as specified in the PRD.
MODEL_ID = "google/medgemma-1.5-4b-it"

print(f"Initializing Agent B (The Investigator) with model: {MODEL_ID}")

try:
    # Using 'image-text-to-text' as per PRD strategy, assuming MedGemma 1.5 is mutimodal or compatible
    # with the multimodal pipeline structure defined in the PRD.
    # Note: If this fails because the model is text-only, we might need 'text-generation'.
    pipe = pipeline(
        "image-text-to-text", 
        model=MODEL_ID, 
        torch_dtype=torch.bfloat16, 
        device_map="auto"
    )
    print("Agent B initialized successfully.")

except Exception as e:
    print(f"Error initializing Agent B with model {MODEL_ID}: {e}")
    print("Attempting fallback to a standard Gemma pipeline for testing purposes if this is a simulation context,")
    print("or asking user for clarification if this is a real deployment failure.")
    # Fallback to text-generation with a known model if the specific 2026 model ID isn't found in this environment
    # Use Gemma 2 2b IT as a close proxy for "instruction tuned gemma" if the "MedGemma 1.5" is hypothetical.
    MODEL_ID = "google/gemma-2-2b-it" 
    print(f"FALLBACK: Initializing with {MODEL_ID} using 'text-generation' pipeline.")
    try:
        pipe = pipeline(
            "text-generation", 
            model=MODEL_ID, 
            torch_dtype=torch.bfloat16, 
            device_map="auto"
        )
        print("Fallback Agent B initialized successfully.")
    except Exception as e2:
        print(f"Critical Error: Could not load fallback model either. {e2}")
        raise e2

def generate_interview_question(visual_findings):
    system_prompt = """
    You are an ophthalmic nurse assistant. 
    Based on the visual findings from a retinal scan, determine ONE crucial follow-up question 
    to ask the patient to assess urgency (e.g., sudden vision loss, flashes, or floaters).
    """

    # If using the 'image-text-to-text' pipeline with VLM structure
    if pipe.task == "image-text-to-text":
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"{system_prompt}\n\nVisual Findings: {visual_findings}"}
                ]
            }
        ]
        # Generate the response
        output = pipe(messages, max_new_tokens=128)
        return output[0]['generated_text']
    else:
        # Text-generation fallback structure (chat template)
        messages = [
            {"role": "user", "content": f"{system_prompt}\n\nVisual Findings: {visual_findings}"}
        ]
        output = pipe(messages, max_new_tokens=128, return_full_text=False)
        return output[0]['generated_text']

if __name__ == "__main__":
    # Test stub
    dummy_findings = "The optic disc shows signs of blurring margins, consistent with papilledema. Macula appears normal. No extensive hemorrhages."
    print("--- Test Input (Visual Findings) ---")
    print(dummy_findings)
    print("\n--- Agent B Output (Interview Question) ---")
    try:
        question = generate_interview_question(dummy_findings)
        print(question)
    except Exception as e:
        print(f"Error generating question: {e}")
