from agent_investigator import load_medgemma_model
from transformers import pipeline

# ...

def generate_referral(findings, history):
    # ... (prompt def)
    base_prompt = f"""You are a senior ophthalmologist. Review the visual findings: {findings} and the patient's history: {history}. 
Write a referral letter for a specialist. Include a Triage Level: Green (Routine), Yellow (Urgent), Red (Emergency).
If the history and findings are too vague to form even a preliminary referral, simply output 'INSUFFICIENT_INFO'."""

    # Load shared pipe
    pipe = load_medgemma_model()
    
    # Check if Mock
    if type(pipe).__name__ == "MockPipeline":
        # Return a conditional mock result based on history length to simulate loop
        if history and len(history.split('\n')) > 1:
             return "REFERRAL DIAGNOSIS: Proliferative Diabetic Retinopathy. TRIAGE: Red (Emergency)."
        else:
             return "INSUFFICIENT_INFO. Please ask about blood sugar levels."

    # Check pipeline type to format input correctly
    if hasattr(pipe, 'task') and pipe.task == "image-text-to-text":
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": base_prompt}
                ]
            }
        ]
        # Generate the response
        output = pipe(messages, max_new_tokens=512)
        return output[0]['generated_text']
    else:
        # Text-generation fallback structure (chat template)
        messages = [
            {"role": "user", "content": base_prompt}
        ]
        output = pipe(messages, max_new_tokens=512, return_full_text=False)
        return output[0]['generated_text']

if __name__ == "__main__":
    findings = "Optic disc blurring observed."
    history = "Patient reports sudden vision loss in left eye starting 2 hours ago."
    print("--- Test Agent C ---")
    print(generate_referral(findings, history))
