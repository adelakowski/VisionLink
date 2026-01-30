import os
import sys
import operator
from dotenv import load_dotenv
load_dotenv()
from typing import Annotated, List, TypedDict, Union

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import Agents
# Lazy import or direct import? Direct import is fine as we need them for the graph.
# Note: Importing agents loads models. Expect startup time.
try:
    import agent_observer
    import agent_investigator
    import agent_diagnostician
except ImportError as e:
    print(f"Error importing agents: {e}")
    sys.exit(1)

# Try importing LangGraph
try:
    from langgraph.graph import StateGraph, END
except ImportError:
    print("LangGraph not found. Please install it via pip install langgraph langchain")
    sys.exit(1)

# --- State Definition ---
class AgentState(TypedDict):
    image_path: str
    visual_findings: str
    history_log: Annotated[List[str], operator.add]
    last_question: str
    referral_report: str
    status: str # "CONTINUE" or "FINISHED"

# --- Node Definitions ---

def observer_node(state: AgentState):
    print("\n--- Node 1: Observer (Agent A) ---")
    image_path = state["image_path"]
    print(f"Anaylzing image: {image_path}")
    findings = agent_observer.get_visual_findings(image_path)
    print(f"Visual Findings: {findings}")
    agent_observer.unload_model()
    return {"visual_findings": findings}

def investigator_node(state: AgentState):
    print("\n--- Node 2: Investigator (Agent B) ---")
    findings = state["visual_findings"]
    # Format history for Agent B
    # History log is a list of strings "Q: ... A: ..."
    history_str = "\n".join(state["history_log"]) if state["history_log"] else None
    
    question = agent_investigator.generate_interview_question(findings, history=history_str)
    print(f"Generated Question: {question}")
    return {"last_question": question}

def interaction_node(state: AgentState):
    print("\n--- Node 3: Interaction ---")
    question = state["last_question"]
    print(f"Doctor/Agent: {question}")
    
    # In a real app, this would be a UI callback. Here we use console input.
    user_answer = input("Patient Answer: ")
    
    # Record the Q&A pair
    new_history_entry = f"Q: {question}\nA: {user_answer}"
    return {"history_log": [new_history_entry]}

def diagnostician_node(state: AgentState):
    print("\n--- Node 4: Synthesize/Check (Agent C) ---")
    findings = state["visual_findings"]
    history_str = "\n".join(state["history_log"])
    
    referral = agent_diagnostician.generate_referral(findings, history_str)
    
    print(f"Agent C Thoughts: {referral}")
    
    # Check condition
    if "INSUFFICIENT_INFO" in referral or "insufficient info" in referral.lower():
        print("Decision: Not enough info. Looping back...")
        return {"status": "CONTINUE", "referral_report": referral}
    else:
        print("Decision: Diagnosis/Referral Ready.")
        agent_investigator.unload_model()
        return {"status": "FINISHED", "referral_report": referral}

# --- Graph Construction ---

def create_graph():
    workflow = StateGraph(AgentState)

    # Add Nodes
    workflow.add_node("observer", observer_node)
    workflow.add_node("investigator", investigator_node)
    workflow.add_node("interaction", interaction_node)
    workflow.add_node("diagnostician", diagnostician_node)

    # Set Entry Point
    workflow.set_entry_point("observer")

    # Add Edges
    workflow.add_edge("observer", "investigator")
    workflow.add_edge("investigator", "interaction")
    workflow.add_edge("interaction", "diagnostician")

    # Conditional Logic
    def check_diagnosis(state):
        if state["status"] == "FINISHED":
            return "end"
        else:
            return "loop"

    workflow.add_conditional_edges(
        "diagnostician",
        check_diagnosis,
        {
            "end": END,
            "loop": "investigator"
        }
    )

    return workflow.compile()

# --- Main Execution ---

if __name__ == "__main__":
    # Load example image if available
    target_image = ""
    json_path = "few_shot_examples.json"
    import json
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            data = json.load(f)
            # Pick a diabetic retinopathy example
            if "D" in data and data["D"]:
                target_image = data["D"][0]["image_path"]
    
    if not target_image:
        print("Please provide an image path:")
        target_image = input().strip()

    if not os.path.exists(target_image):
        print(f"Error: Image {target_image} not found.")
        sys.exit(1)

    print(f"Starting VisionLink Orchestration with Image: {target_image}")
    
    app = create_graph()
    
    # Initial State
    initial_state = {
        "image_path": target_image,
        "visual_findings": "",
        "history_log": [],
        "last_question": "",
        "referral_report": "",
        "status": "START"
    }

    # Run the graph
    # Depending on langgraph version, output might supply the final state
    try:
        final_state = app.invoke(initial_state)
        print("\n\n=== FINAL REFERRAL REPORT ===")
        print(final_state["referral_report"])
    except Exception as e:
        print(f"Error during execution: {e}")
