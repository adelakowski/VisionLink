# VisionLink - Quick Start Guide

## 🎯 Running the Gradio UI

### Prerequisites
- Python 3.9+
- CUDA-capable GPU (optional, will use MOCK_MODE if unavailable)

### Launch the UI

```powershell
# Navigate to project directory
cd d:\Users\axeld\MCIT\VisionLink\VisionLink

# Activate the virtual environment and run
.\venv_gradio\Scripts\Activate.ps1; python src/ui_gradio.py
```

The UI will be available at: **http://127.0.0.1:7860**

### How to Use

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

The system uses a three-agent relay architecture:

- **Agent A (Observer)**: PaliGemma 3B - Extracts visual features from retinal scans
- **Agent B (Investigator)**: Gemma 2 2B - Generates interview questions based on findings
- **Agent C (Diagnostician)**: Gemma 2 2B - Synthesizes findings + history into triage report

## 📦 Virtual Environment Details

The UI runs in a clean virtual environment (`venv_gradio`) with the following stable versions:
- `gradio==4.44.1`
- `pydantic==2.7.0`
- `fastapi==0.110.0`
- `transformers` (latest)
- `torch` (latest)
- `bitsandbytes` (for 4-bit quantization)

## 🔧 Troubleshooting

### If the UI doesn't start:
1. Ensure the virtual environment is activated
2. Check that port 7860 is not in use
3. Verify all dependencies are installed: `pip list`

### If models fail to load:
- The system will automatically fall back to MOCK_MODE
- Check CUDA availability with: `python scripts/check_cuda.py`

### To recreate the virtual environment:
```powershell
Remove-Item -Recurse -Force venv_gradio
python -m venv venv_gradio
.\venv_gradio\Scripts\Activate.ps1
pip install -r requirements_gradio.txt
pip install pydantic==2.7.0 fastapi==0.110.0 gradio==4.44.1
```

## 📊 Sample Test Images

Test images are available in:
- `archive/ODIR-5K/Training Images/` (Left-Fundus images)
- Use images from `data/few_shot_examples.json` for pre-validated cases

## 🎓 For Judges/Demo

This implementation demonstrates:
1. ✅ Multi-agent orchestration (3 specialized agents)
2. ✅ Vision-Language Model integration (PaliGemma)
3. ✅ Medical LLM reasoning (MedGemma/Gemma 2)
4. ✅ Interactive patient interview workflow
5. ✅ Real-time triage report generation
6. ✅ Production-ready UI with error handling
7. ✅ Efficient model loading with 4-bit quantization

## 📝 Notes

- Currently using MOCK_MODE for Agent A to prevent OOM on limited hardware
- Can be switched to full PaliGemma inference by setting `MOCK_MODE=False` in `agent_observer.py`
- Agent B and C use real Gemma 2 2B inference with 4-bit quantization
