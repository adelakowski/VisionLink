# 🏥 VisionLink: AI-Powered Rural Triage Agent

> **Democratizing specialist-level eye care for rural populations through intelligent multi-agent orchestration**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Gradio](https://img.shields.io/badge/Gradio-4.44.1-orange.svg)](https://gradio.app/)

---

## 🎯 Mission

VisionLink bridges the gap between advanced AI perception and clinical dialogue to provide **automated ophthalmic triage** in resource-limited settings. By combining vision-language models with medical reasoning, we enable early detection and appropriate referral for sight-threatening conditions like diabetic retinopathy and glaucoma.

## 🌟 Key Features

- **🔍 Intelligent Visual Analysis**: PaliGemma-powered retinal scan interpretation
- **💬 Dynamic Patient Interviews**: MedGemma-driven clinical questioning
- **🎯 Automated Triage**: Smart urgency classification (Green/Yellow/Red)
- **💰 Rural-Ready**: 60%+ cost reduction via 4-bit quantization
- **🔄 Adaptive Workflow**: LangGraph orchestration for cyclic reasoning

## 📚 Documentation

| For... | See... |
|--------|--------|
| **Quick Start** | [QUICKSTART.md](docs/QUICKSTART.md) |
| **Technical Details** | [PRD.md](docs/PRD.md) |
| **Project Structure** | [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) |
| **Pitch Deck** | [PITCH_DECK.md](presentation/PITCH_DECK.md) |
| **Executive Summary** | [EXECUTIVE_SUMMARY.md](presentation/EXECUTIVE_SUMMARY.md) |
| **Visual Diagrams** | [assets/](assets/) |

---

## 🏗️ Architecture

VisionLink employs a **three-agent relay architecture** that mimics the clinical workflow of specialist consultation:

```mermaid
graph LR
    A[Retinal Scan] --> B[Agent A: Observer]
    B --> C[Visual Findings]
    C --> D[Agent B: Investigator]
    D --> E[Interview Question]
    E --> F[Patient Response]
    F --> G[Agent C: Diagnostician]
    G --> H{Sufficient Info?}
    H -->|No| D
    H -->|Yes| I[Triage Report]
```

### Architecture Versions

VisionLink is provided in two distinct distributions to handle both modern connected clinics and completely remote, unconnected areas.

**1. VisionLink Online (Cloud/Serverless)**
- Uses Google's **Gemini 1.5 Flash API**.
- Zero cold-start times; responses in milliseconds.
- Severless deployment to Google Cloud Run and Firebase Hosting.
- Extremely low cost and requires zero local hardware.

**2. VisionLink Offline (Air-Gapped GPU Edition)**
- Runs locally via Hugging Face `transformers`.
- **Agent A**: PaliGemma 3B (4-bit quantization).
- **Agent B & C**: Gemma-2-2b-IT (4-bit quantization).
- Fully air-gapped; requires a CUDA-enabled GPU (8GB+ VRAM).

---

## 🚀 Quick Start

### Option 1: VisionLink Online (Cloud/Serverless)
Requires an active internet connection and a Google AI Studio API key.

1. Clone the repository and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file in the root directory and add your key:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```
3. Run the Gradio UI:
   ```bash
   python src/ui_gradio.py
   ```

### Option 2: VisionLink Offline (Air-Gapped GPU)
Requires a CUDA-capable NVIDIA GPU.

1. Navigate to the `VisionLinkOffline` directory.
2. Read the `OFFLINE_RUNNING_GUIDE.md` for setup instructions.
3. Run the auto-installer/launcher (requires internet for first run *only*):
   ```powershell
   cd VisionLinkOffline
   .\run_offline.ps1
   ```

📖 **For detailed instructions**, see [QUICKSTART.md](docs/QUICKSTART.md) or the Offline Guide.

---

## 💡 How It Works

### 1️⃣ Visual Perception Layer
**PaliGemma** interprets retinal scans to identify:
- Microaneurysms
- Hemorrhages
- Cotton wool spots
- Optic disc anomalies (cupping, blurring)
- Macular edema

### 2️⃣ Clinical Reasoning Layer
**MedGemma 1.5** simulates an Ophthalmic Nurse Assistant:
- Asks targeted questions based on visual findings
- Identifies "Red Flag" symptoms (sudden vision loss, flashes, floaters)
- Determines urgency through structured interview

### 3️⃣ Orchestration Layer
**LangGraph** manages the cyclic workflow:
- State management across agent interactions
- Conditional looping until sufficient information is gathered
- Final synthesis into actionable triage report

---

## 📊 Technical Highlights

### Performance Optimization
- **4-bit Quantization**: Reduces model size by 75% while maintaining accuracy
- **Shared Pipeline**: Agent B & C reuse the same MedGemma instance
- **Lazy Loading**: Models load on-demand to minimize memory footprint

### Rural Viability Metrics
| Metric | Traditional | VisionLink | Improvement |
|--------|------------|------------|-------------|
| Hardware Cost | $5,000+ | $1,500 | **70% reduction** |
| Inference Time | N/A | <30s | Real-time |
| Specialist Availability | Limited | 24/7 | Always-on |
| Cost per Screening | $50-100 | $15-20 | **60-80% reduction** |

---

## 🎨 User Interface

The Gradio-based UI provides a **step-by-step workflow**:

1. **Upload Retinal Scan** → Drag & drop or select image
2. **Analyze Scan** → Agent A extracts visual findings
3. **Answer Question** → Respond to Agent B's interview
4. **Generate Report** → Agent C produces triage recommendation

### Sample Output

```
🔍 Visual Findings:
Severe diabetic retinopathy with microaneurysms and hard exudates detected. 
Optic disc cup-to-disc ratio is 0.6. Macula shows signs of edema.

👨‍⚕️ Interview Question:
Have you experienced sudden vision loss or new floaters in the past 48 hours?

📋 Triage Report:
DIAGNOSIS: Proliferative Diabetic Retinopathy with Macular Edema
URGENCY: RED (Emergency)
RECOMMENDATION: Immediate referral to retinal specialist within 24 hours.
```

---

## 📁 Project Structure

```
VisionLink/
├── src/                          # Source code
│   ├── agent_observer.py         # Agent A: Visual feature extraction
│   ├── agent_investigator.py     # Agent B: Interview question generation
│   ├── agent_diagnostician.py    # Agent C: Triage report synthesis
│   ├── orchestrator.py           # LangGraph workflow orchestration
│   ├── ui_gradio.py             # Gradio web interface
│   └── prepare_few_shot.py       # ODIR-5K dataset preparation
│
├── docs/                         # Documentation
│   ├── PRD.md                    # Product requirements document
│   └── QUICKSTART.md             # Quick start guide
│
├── presentation/                 # Presentation materials
│   ├── EXECUTIVE_SUMMARY.md      # One-page business overview
│   ├── PITCH_DECK.md            # 5-minute pitch deck
│   ├── TECHNICAL_POSTER.md       # Technical deep dive
│   └── SHOWCASE_MATERIALS.md     # Materials index
│
├── assets/                       # Visual assets
│   ├── architecture_diagram.png  # Three-agent workflow
│   └── impact_comparison.png     # Traditional vs VisionLink
│
├── data/                         # Data files
│   └── few_shot_examples.json    # Few-shot prompting examples
│
├── scripts/                      # Utility scripts
│   ├── check_cuda.py            # CUDA availability checker
│   └── ...                       # Other utilities
│
├── requirements.txt              # Core dependencies
├── requirements_gradio.txt       # Gradio UI dependencies
└── README.md                     # This file
```

📋 **For complete structure**, see [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

---

## 🔬 Dataset

VisionLink uses the **ODIR-5K** (Ocular Disease Intelligent Recognition) dataset:
- 5,000 retinal fundus images
- 8 disease categories including diabetic retinopathy and glaucoma
- Left/Right eye pairs with clinical annotations

**Source**: [Kaggle ODIR-5K](https://www.kaggle.com/datasets/andrewmvd/ocular-disease-recognition-odir5k)

---

## 🛠️ Technology Stack

| Component | Online Version | Offline Version |
|-----------|-----------|---------|
| Vision Model | Gemini 1.5 Flash (API) | PaliGemma 3B (Local) |
| Medical LLM | Gemini 1.5 Flash (API) | Gemma-2-2B-IT (Local) |
| Orchestration | LangGraph | LangGraph |
| UI Framework | Gradio 4.44.1 | Gradio 4.44.1 |
| Infrastructure | Cloud Run + Firebase | Windows/Linux CUDA GPU |

---

## 🎯 Use Cases

### Primary
- **Rural Clinics**: First-line screening in areas without ophthalmologists
- **Telemedicine**: Remote triage for diabetic patients
- **Mobile Health Units**: Portable screening in underserved communities

### Secondary
- **Medical Education**: Training tool for ophthalmic nursing students
- **Research**: Dataset generation for clinical AI studies
- **Quality Assurance**: Second opinion system for general practitioners

---

## 🏆 Competitive Advantages

1. **Multi-Agent Architecture**: Separates perception from reasoning, improving interpretability
2. **Dynamic Interviews**: Adapts questions based on visual findings, not static forms
3. **Cyclic Reasoning**: Continues gathering information until confident diagnosis
4. **Rural-Optimized**: Designed for low-resource settings from the ground up
5. **Open Source**: Fully transparent and auditable for medical compliance

---

## 📈 Future Roadmap

- [ ] **Multi-Disease Support**: Expand beyond diabetic retinopathy to age-related macular degeneration, cataracts
- [ ] **Mobile App**: iOS/Android deployment for field use
- [ ] **Clinical Validation**: Prospective study with ophthalmology partners
- [ ] **Multi-Language**: Support for Spanish, Hindi, Mandarin
- [ ] **EHR Integration**: FHIR-compliant API for health record systems
- [ ] **Federated Learning**: Privacy-preserving model updates from rural deployments

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Format code
black . && isort .
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **ODIR-5K Dataset**: Peking University & Shanggong Medical Technology
- **Google Research**: PaliGemma and MedGemma models
- **LangChain Team**: LangGraph orchestration framework
- **Gradio**: Rapid UI prototyping platform

---

## 📞 Contact

**Project Lead**: Axel Delakowski  
**Email**: axeldelakowski@gmail.com  
**LinkedIn**: linkedin.com/in/adelakowski  
**Demo**: https://visionlinktriage.web.app/

---

## 📊 Citation

If you use VisionLink in your research, please cite:

```bibtex
@software{visionlink2026,
  author = {Delakowski, Axel},
  title = {VisionLink: AI-Powered Rural Triage Agent for Ophthalmic Care},
  year = {2026},
  url = {https://github.com/adelakowski/VisionLink}
}
```

---

<div align="center">

**Built with ❤️ for rural healthcare equity**

[⭐ Star this repo](https://github.com/adelakowski/VisionLink) | [🐛 Report Bug](https://github.com/adelakowski/VisionLink/issues) | [💡 Request Feature](https://github.com/adelakowski/VisionLink/issues)

</div>
