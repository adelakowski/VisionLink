import os
import torch
import numpy as np
from PIL import Image
from transformers import PaliGemmaForConditionalGeneration, PaliGemmaProcessor, BitsAndBytesConfig
from dotenv import load_dotenv
import json

load_dotenv()

# Configuration
# Use the Google version from HF Hub
MODEL_ID = "google/paligemma-3b-mix-224"
# Configure 4-bit quantization
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

print(f"Loading {MODEL_ID} with Transformers...")

# Global model/processor cache
model = None
processor = None

def load_model():
    global model, processor
    if model is None:
        try:
            print("Initializing Processor...")
            processor = PaliGemmaProcessor.from_pretrained(MODEL_ID)
            
            print("Initializing Model (4-bit quantization)...")
            # Note: BitsAndBytes requires CUDA. If no CUDA, this will fail.
            if torch.cuda.is_available():
                model = PaliGemmaForConditionalGeneration.from_pretrained(
                    MODEL_ID,
                    quantization_config=bnb_config,
                    device_map="auto"
                )
            else:
                print("CUDA not found. Falling back to CPU/Float32 (Warning: High RAM usage).")
                model = PaliGemmaForConditionalGeneration.from_pretrained(
                    MODEL_ID,
                    torch_dtype=torch.float32,
                    device_map="cpu"
                )
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise e

def get_visual_findings(image_path):
    """
    Generates a descriptive text of visual findings from a retinal scan.
    """
    if model is None:
        load_model()
        
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found at {image_path}")

    # Load Image
    image = Image.open(image_path).convert("RGB")
    
    # Prompt
    prompt = "detect signs of diabetic retinopathy and glaucoma, and describe the optic disc and macula"
    
    # Preprocess
    inputs = processor(text=prompt, images=image, return_tensors="pt")
    
    # Move inputs to same device as model
    device = model.device
    input_ids = inputs.input_ids.to(device)
    pixel_values = inputs.pixel_values.to(device)
    attention_mask = inputs.attention_mask.to(device)

    # Generate
    with torch.no_grad():
        generated_ids = model.generate(
            input_ids=input_ids,
            pixel_values=pixel_values,
            attention_mask=attention_mask,
            max_new_tokens=128
        )
    
    # Decode
    result = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    
    # Simple clean up if prompt is repeated in output
    if result.startswith(prompt):
        # Often PaliGemma outputs "\n" after prompt
        result = result[len(prompt):].strip()
        
    return result

if __name__ == "__main__":
    # Test stub
    json_path = "few_shot_examples.json"
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            examples = json.load(f)
        
        # Test D (Diabetic Retinopathy)
        if "D" in examples and examples["D"]:
            test_img = examples["D"][0]["image_path"]
            print(f"Testing Agent A on: {test_img}")
            try:
                findings = get_visual_findings(test_img)
                print("--- Findings ---")
                print(findings)
                print("----------------")
            except Exception as e:
                print(f"Error testing: {e}")
                import traceback
                traceback.print_exc()
    else:
        print("No few_shot_examples.json found for testing.")
