import gradio as gr
import os
from agent_observer import get_visual_findings
from agent_investigator import generate_interview_question
from agent_diagnostician import generate_referral

# Global state to track conversation
conversation_state = {
    "findings": None,
    "question": None,
    "history": []
}

def process_first_turn(image):
    """First turn: Agent A (Observer) -> Agent B (Investigator)"""
    global conversation_state
    
    if image is None:
        return "⚠️ Please upload a retinal scan to start the triage process.", "", ""
    
    print(f"[Agent A] Processing image...")
    findings = get_visual_findings(image)  # Agent A
    
    print(f"[Agent A] Findings: {findings}")
    print(f"[Agent B] Generating interview question...")
    
    question = generate_interview_question(findings)  # Agent B
    
    print(f"[Agent B] Question: {question}")
    
    # Store in state
    conversation_state["findings"] = findings
    conversation_state["question"] = question
    
    return findings, question, ""

def process_second_turn(patient_answer):
    """Second turn: Agent C (Diagnostician)"""
    global conversation_state
    
    if not conversation_state["findings"] or not conversation_state["question"]:
        return "⚠️ Please upload a retinal scan first."
    
    if not patient_answer or patient_answer.strip() == "":
        return "⚠️ Please provide an answer to the question."
    
    print(f"[Agent C] Generating final report...")
    
    # Combine findings and patient history
    findings = conversation_state["findings"]
    patient_history = f"Q: {conversation_state['question']}\nA: {patient_answer}"
    
    report = generate_referral(findings, patient_history)  # Agent C
    
    print(f"[Agent C] Report generated.")
    
    # Store in history
    conversation_state["history"].append({
        "findings": findings,
        "question": conversation_state["question"],
        "answer": patient_answer,
        "report": report
    })
    
    return report

def reset_conversation():
    """Reset the conversation state"""
    global conversation_state
    conversation_state = {
        "findings": None,
        "question": None,
        "history": []
    }
    return "", "", "", ""

# Create the Gradio Interface
with gr.Blocks(title="🏥 VisionLink: Rural Triage Agent", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🏥 VisionLink: Rural Triage Agent
    
    **Automated Ophthalmic Triage System**
    
    This system uses a multi-agent architecture:
    - **Agent A (Observer):** Analyzes visual features using PaliGemma
    - **Agent B (Investigator):** Asks relevant medical history questions using MedGemma
    - **Agent C (Diagnostician):** Synthesizes findings and generates referral reports
    
    ---
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Step 1: Upload Retinal Scan")
            image_input = gr.Image(type="filepath", label="Retinal Scan Image")
            analyze_btn = gr.Button("🔍 Analyze Scan", variant="primary", size="lg")
            
        with gr.Column(scale=1):
            gr.Markdown("### Step 2: Visual Findings & Question")
            findings_output = gr.Textbox(label="🔍 Visual Findings", lines=4, interactive=False)
            question_output = gr.Textbox(label="👨‍⚕️ Interview Question", lines=3, interactive=False)
    
    gr.Markdown("---")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Step 3: Patient Response")
            patient_answer = gr.Textbox(
                label="Your Answer",
                placeholder="Type your response to the question above...",
                lines=3
            )
            generate_btn = gr.Button("📋 Generate Triage Report", variant="primary", size="lg")
            
        with gr.Column(scale=1):
            gr.Markdown("### Step 4: Triage Report")
            report_output = gr.Textbox(label="📋 Final Triage Report", lines=10, interactive=False)
    
    gr.Markdown("---")
    
    with gr.Row():
        reset_btn = gr.Button("🔄 Start New Triage", variant="secondary")
    
    # Event handlers
    analyze_btn.click(
        fn=process_first_turn,
        inputs=[image_input],
        outputs=[findings_output, question_output, report_output]
    )
    
    generate_btn.click(
        fn=process_second_turn,
        inputs=[patient_answer],
        outputs=[report_output]
    )
    
    reset_btn.click(
        fn=reset_conversation,
        inputs=[],
        outputs=[findings_output, question_output, patient_answer, report_output]
    )
    
    gr.Markdown("""
    ---
    **How to use:**
    1. Upload a retinal scan image
    2. Click "Analyze Scan" to get visual findings and an interview question
    3. Answer the question in the text box
    4. Click "Generate Triage Report" to get the final diagnosis and referral
    """)

if __name__ == "__main__":
    print("=" * 60)
    print("🏥 VisionLink: Rural Triage Agent")
    print("=" * 60)
    print("\nStarting Gradio interface...")
    print("Upload a retinal scan to begin the triage process.\n")
    
    try:
        demo.launch(
            share=False,
            server_name="0.0.0.0", 
            server_port=int(os.environ.get("PORT", 7860)),
            show_error=True,
            inbrowser=True
        )
    except Exception as e:
        print(f"\n✗ Error launching Gradio: {e}")
        import traceback
        traceback.print_exc()
