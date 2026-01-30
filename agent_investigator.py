import torch
from dotenv import load_dotenv
load_dotenv()
from transformers import pipeline, BitsAndBytesConfig
import os
import gc

# Phase 3: Agent B - The Investigator
# Model: MedGemma 1.5 4B-IT (google/medgemma-1.5-4b-it)

MODEL_ID = "google/gemma-2-2b-it"

# Configure 4-bit quantization
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

# pipeline cache
pipe = None

class MockPipeline:
    def __init__(self, task="text-generation"):
        self.task = task
    
    def __call__(self, messages, **kwargs):
        # Return dummy output structure
        return [{'generated_text': "Is the vision loss sudden or gradual?"}]

def load_medgemma_model():
    global pipe
    if pipe is not None:
        return pipe

    print(f"Initializing Agent B (Investigator) with model: {MODEL_ID}")
    try:
        # Gemma 2 is a text model, so we must use "text-generation"
        # Using model_kwargs for dtype as requested
        new_pipe = pipeline(
            "text-generation", 
            model=MODEL_ID, 
            model_kwargs={
                "dtype": torch.bfloat16,
                "low_cpu_mem_usage": True,
                "quantization_config": bnb_config
            },
            device_map="auto"
        )
        print("Agent B initialized successfully.")
        pipe = new_pipe
        return pipe
    except Exception as e:
        print(f"Error initializing Agent B: {e}")
        print("WARNING: Model loading failed (likely OOM). Switching to MOCK_MODE.")
        pipe = MockPipeline(task="text-generation")
        return pipe

def unload_model():
    global pipe
    if pipe is not None:
        del pipe
        gc.collect()
        torch.cuda.empty_cache()
        pipe = None
        print("Agent B/C Model unloaded.")

def generate_interview_question(visual_findings, history=None):
    system_prompt = """
    You are an ophthalmic nurse assistant. 
    Based on the visual findings from a retinal scan and any patient history provided, 
    determine ONE crucial follow-up question to ask the patient to assess urgency 
    (e.g., sudden vision loss, flashes, or floaters).
    Do not ask questions that have already been answered in the history.
    """

    context_text = f"Visual Findings: {visual_findings}"
    if history:
        context_text += f"\n\nPatient History/Previous Answers: {history}"

    # Load model if not loaded
    local_pipe = load_medgemma_model()

    # If using the 'image-text-to-text' pipeline with VLM structure
    if local_pipe.task == "image-text-to-text":
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"{system_prompt}\n\n{context_text}"}
                ]
            }
        ]
        # Generate the response
        output = local_pipe(messages, max_new_tokens=128)
        return output[0]['generated_text']
    else:
        # Text-generation fallback structure (chat template)
        messages = [
            {"role": "user", "content": f"{system_prompt}\n\n{context_text}"}
        ]
        output = local_pipe(messages, max_new_tokens=128, return_full_text=False)
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
