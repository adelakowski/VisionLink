# VisionLink - Quick Start Guide

VisionLink is available in two distributions: an **Online Serverless Edition** and an **Offline GPU air-gapped Edition**.

## ☁️ Option 1: VisionLink Online (Cloud/Serverless)
This version uses Google's Gemini 1.5 Flash API for near-instant responses. It requires an active internet connection.

### Prerequisites
- Python 3.9+
- A Google AI Studio API Key

### Launch the UI

```powershell
# Navigate to project directory
cd d:\Users\axeld\MCIT\VisionLink\VisionLink

# Install dependencies
pip install -r requirements.txt

# Set your API Key in the `.env` file
# GEMINI_API_KEY=your_api_key_here

# Run the app
python src/ui_gradio.py
```
The UI will be available at: **http://127.0.0.1:7860**

---

## 🛑 Option 2: VisionLink Offline (Air-Gapped GPU)
This version runs entirely locally using Hugging Face transformers. It requires no internet after the initial setup.

### Prerequisites
- Python 3.10+
- A CUDA-capable NVIDIA GPU (8GB+ VRAM)

### Launch the UI

```powershell
# Navigate to the Offline directory
cd d:\Users\axeld\MCIT\VisionLink\VisionLinkOffline

# Run the auto-installer/launcher
# (Requires internet the very first time to download the ~6GB of models)
.\run_offline.ps1
```
The UI will automatically open at: **http://127.0.0.1:7860**

---

## 💡 How to Use the UI

1. **Upload a Retinal Scan**
   - Click on the image upload area
   - Select a retinal scan image from the ODIR-5K dataset or any retinal image

2. **Click "Analyze Scan"**
   - Agent A (Observer) will analyze the visual features
   - Agent B (Investigator) will generate a relevant medical history question

3. **Answer the Question**
   - Type your response in the "Your Answer" text box
   - This simulates the patient interview

4. **Click "Generate Triage Report"**
   - Agent C (Diagnostician) will synthesize the findings and patient history
   - A complete triage report with urgency level will be generated

5. **Start New Triage** (optional)
   - Click "Start New Triage" to reset and analyze another case

## 🏗️ Architecture

The system uses a three-agent relay architecture.
- **Online:** Gemini 1.5 Flash (API)
- **Offline:** PaliGemma 3B + Gemma 2 2B (Local via transformers with 4-bit quantization)

## 📊 Sample Test Images

Test images are available in:
- `archive/ODIR-5K/Training Images/` (Left-Fundus images)
- Use images from `data/few_shot_examples.json` for pre-validated cases
