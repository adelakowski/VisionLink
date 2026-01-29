import os
import json
import keras_nlp
import keras

# Configuration
# Optimization: Float16 for "Rural/Low-resource" deployment
try:
    keras.config.set_floatx("float16")
except Exception as e:
    print(f"Warning: Could not set float16: {e}")

class VisionAgent:
    def __init__(self, model_id="pali_gemma_3b_mix_224"):
        print(f"Loading Vision Model: {model_id}...")
        # Load PaliGemma
        self.model = keras_nlp.models.PaliGemmaCausalLM.from_preset(model_id)
        print("Model loaded.")

    def analyze_image(self, image_path, prompt="detect signs of diabetic retinopathy and glaucoma, and describe the optic disc and macula"):
        """
        Analyzes the image and returns a text description of findings.
        """
        if not os.path.exists(image_path):
            return f"Error: Image not found at {image_path}"

        # Generate description
        output = self.model.generate(
            inputs={
                "images": [image_path], 
                "prompts": [prompt]
            }
        )
        
        # Result might be a list or single string depending on batch size
        result = output[0] if isinstance(output, list) else output
        return result

def load_few_shot_examples(json_path="few_shot_examples.json"):
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            return json.load(f)
    return {}

if __name__ == "__main__":
    # Test stub
    print("Initializing Agent A (Observer)...")
    agent = VisionAgent()
    
    examples = load_few_shot_examples()
    
    # Test for Diabetic Retinopathy (D) and Glaucoma (G)
    test_conditions = {'D': 'Diabetic Retinopathy', 'G': 'Glaucoma'}
    
    for label, conditions_name in test_conditions.items():
        if label in examples and examples[label]:
            test_case = examples[label][0]
            test_img = test_case['image_path']
            print(f"\nTesting with ODIR-5K image ({conditions_name}): {test_img}")
            
            description = agent.analyze_image(test_img)
            print(f"--- Visual Findings for {conditions_name} ---")
            print(description)
            print("---------------------------------------------")
        else:
            print(f"No few-shot examples found for {conditions_name} ({label}).")
