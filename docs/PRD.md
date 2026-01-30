# VisionLink Product Requirements Document (PRD)

**Project Name:** VisionLink  
**Type:** Rural Triage Agent / Hackathon Submission  
**Goal:** Build an automated ophthalmic triage system using a multi-agent "Relay Race" architecture to detect diabetic retinopathy and other conditions, conduct patient interviews, and generate referral reports.

---

## 1. Architecture Overview (The Mental Model)

The system operates as a pipeline of three distinct AI agents, designed as a "Relay Race":

1.  **Agent A (The Observer):** Vision-Language Model (PaliGemma). "Sees" the image and extracts features.
2.  **Agent B (The Investigator):** LLM (MedGemma 9B). "Thinks" about the findings and asks a relevant history question.
3.  **Agent C (The Diagnostician):** LLM (MedGemma 9B). "Synthesizes" the visual data and patient history to generate a report.

**Data Flow:**
```mermaid
graph LR
    UserOp[User Upload] --> AgentA[Agent A: Observer]
    AgentA --> Findings[Visual Findings]
    Findings --> AgentB[Agent B: Investigator]
    AgentB --> Question[Dynamic Question]
    Question --> UserIn[User Input]
    UserIn --> AgentC[Agent C: Diagnostician]
    AgentC --> Report[Triage Report]
```

---

## 2. Technology Stack

*   **Vision Model:** `google/paligemma-3b-mix-224` (via `keras_nlp`)
    *   *Role:* Visual feature extraction.
*   **LLM:** `google/gemma-1.1-instruction-en` (MedGemma 9B, via `keras_nlp`)
    *   *Role:* Clinical reasoning and synthesis.
*   **Orchestration:** LangGraph
    *   *Role:* Managing the cyclic agent loop and state.
*   **Interface:** Gradio
    *   *Role:* Demonstration UI for judges.
*   **Dataset:** ODIR-5K (Ocular Disease Intelligent Recognition)
    *   *Role:* Validation and few-shot prompting examples.
*   **Optimization:** Float16 or Int8 quantization
    *   *Role:* Enabling "Rural/Low-resource" deployment on consumer hardware.

---

## 3. Implementation Phases

### Phase 1: Data Preparation (ODIR-5K)
*   **Source:** ODIR-5K dataset (Kaggle).
*   **Action:**
    *   Download dataset.
    *   Map "Left Eye" images to "Left Eye Keywords" (Excel).
*   **Goal:** Create pairs for "few-shot" prompting of Agent A to verify it can recognize features like "microaneurysms" or "cotton wool spots".
*   **Note:** Full training is NOT required; focus on verification and prompt-tuning.

### Phase 2: Agent A - The Observer (Vision-to-Text)
*   **Role:** Bridge the gap between Image and Text-only MedGemma.
*   **Model:** PaliGemma (`pali_gemma_3b_mix_224`).
*   **Input:** Retinal Scan Image.
*   **Output:** Descriptive text of findings (e.g., "Microaneurysms present, optic disc clear").
*   **Code Strategy:**
    ```python
    import keras_nlp
    import keras

    # Load PaliGemma
    pali_gemma = keras_nlp.models.PaliGemmaCausalLM.from_preset("pali_gemma_3b_mix_224")

    def get_visual_findings(image_path):
        # Few-shot prompting recommended here using ODIR examples
        prompt = "detect signs of diabetic retinopathy and glaucoma, and describe the optic disc and macula"
        
        output = pali_gemma.generate(
            inputs={
                "images": load_image(image_path),
                "prompts": [prompt]
            }
        )
        return output 
    ```

### Phase 3: Agent B - The Investigator (Dynamic Interview)
*   **Role:** Determine urgency by asking relevant medical history questions based on visual evidence.
*   **Model:** MedGemma 1.5 4B-IT (medgemma_1.5_4b_it).
*   **Input:** Visual Findings (Text from Agent A).
*   **Output:** ONE crucial follow-up question for the patient.
*   **Code Strategy:**
    
    ```python
    import torch
    from transformers import pipeline

    # Load the Jan 2026 MedGemma 1.5 weights via Hugging Face
    # Built on Gemma 3, optimized for medical reasoning and instruction following
    model_id = "google/medgemma-1.5-4b-it"

    pipe = pipeline(
        "image-text-to-text", 
        model=model_id, 
        torch_dtype=torch.bfloat16, 
        device_map="auto"
    )

    def generate_interview_question(visual_findings):
        system_prompt = """
        You are an ophthalmic nurse assistant. 
        Based on the visual findings from a retinal scan, determine ONE crucial follow-up question 
        to ask the patient to assess urgency (e.g., sudden vision loss, flashes, or floaters).
        """

        # Construct the conversation following the Gemma 3 chat template
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
    ```

### Phase 4: The Orchestration (LangGraph Loop)
*   **Logic:**
    1.  **Node 1 (Start):** Receive Image -> Run Agent A -> Get Findings.
    2.  **Node 2 (Investigate):** findings -> Run Agent B -> Get Question.
    3.  **Node 3 (Interaction):** Display Question -> Wait for User Answer.
    4.  **Node 4 (Synthesize/Check):** Run Agent C.
        *   *Condition:* Does Agent C have enough info for a diagnosis?
            *   *Yes:* Output Referral Report (End).
            *   *No:* Loop back to Node 2 (Ask another question).
*   **Agent C Prompt:** "You are a senior ophthalmologist. Review the visual findings: {findings} and the patient's history: {history}. Write a referral letter for a specialist. Include a Triage Level: Green (Routine), Yellow (Urgent), Red (Emergency)."

### Phase 5: User Interface (Gradio)
*   **Goal:** Simple, demonstrative UI for judges.
*   **Code Strategy (The "Winning" Upgrade):**
    *   *Recommendation:* Use Gradio's `ChatInterface` with multimodal support. This allows the judges to see Agent B ask a question, and Agent C only "Synthesizes" the report after the user answers.
    ```python
    import gradio as gr

    def vision_link_chat(message, history):
        # message is a dict: {"text": "...", "files": ["..."]}
        image_path = message["files"][0] if message["files"] else None
        user_text = message["text"]

        if not history:
            # Error Handling: Ensure user uploaded an image
            if not image_path:
                return "⚠️ Please upload a retinal scan to start the triage process."

            # First Turn: Agent A (Observer) -> Agent B (Investigator)
            findings = get_visual_findings(image_path) # Agent A
            question = generate_interview_question(findings) # Agent B
            return f"**Visual Findings:** {findings}\n\n**Interviewer:** {question}"
        else:
            # Second Turn: Agent C (Diagnostician)
            # Pull findings from history and combine with user's new answer
            past_findings = history[0][1] 
            report = generate_final_report(past_findings, user_text) # Agent C
            return f"**Final Triage Report:**\n\n{report}"

    demo = gr.ChatInterface(
        fn=vision_link_chat,
        multimodal=True,
        title="VisionLink: Rural Triage Agent",
        description="Upload a retinal scan to start the automated triage interview.",
        # Ensure UI follows the persona
        additional_inputs=[
             gr.Textbox(value="You are an Ophthalmic Nurse Assistant.", label="System Persona", visible=False)
        ]
    )
    demo.launch()
    ```

---

## 4. "Winning" Checklist & Narrative

### Checklist
1.  **Efficiency:** Ensure PaliGemma runs in `float16` or `int8` to demonstrate rural viability on low hardware.
2.  **Citation:** Explicitly state: "We used PaliGemma for the visual encoding to separate perception from reasoning, allowing MedGemma to focus on clinical logic."

### Scenario (The Story)
*   **Patient:** Maria.
*   **Context:** Lives 4 hours from a city.
*   **Flow:**
    1.  VisionLink sees optic disc cupping (early Glaucoma sign).
    2.  System asks: "Do you have a family history of glaucoma?"
    3.  Maria (or nurse) confirms "Yes".
    4.  System generates a **Yellow/Red** urgency referral for specialist evaluation.
