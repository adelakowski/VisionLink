from agent_investigator import load_medgemma_model
from transformers import pipeline

# ...

def generate_referral(findings, history):
    # ... (prompt def)
    base_prompt = f"""You are a senior ophthalmologist. Review the visual findings: {findings} and the patient's history: {history}. 
    
    Determine the Triage Level based on these STRICT criteria:
    - **RED (EMERGENCY)**: Sudden vision loss (hours/days), eye pain, trauma, retinal detachment, or signs of severe proliferative retinopathy with active bleeding. Immediate referral required.
    - **YELLOW (URGENT)**: Distorted vision, macular edema, severe non-proliferative retinopathy, or gradual but significant vision decline. Specialist needed within 1-2 weeks.
    - **GREEN (ROUTINE)**: Mild/Moderate retinopathy, stable vision, routine screening, or normal findings. Routine follow-up.

    Write a professional referral letter. 
    explicitly state the TRIAGE LEVEL at the top.
    Explain your reasoning for the chosen level.
    """

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
