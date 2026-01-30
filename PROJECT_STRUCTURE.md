# VisionLink Project Structure

```
VisionLink/
├── README.md                      # Main project documentation
├── LICENSE                        # MIT License
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Core Python dependencies
├── requirements_gradio.txt       # Gradio UI dependencies
├── progress.txt                  # Development progress log
│
├── src/                          # Source code
│   ├── agent_observer.py         # Agent A: Visual feature extraction
│   ├── agent_investigator.py     # Agent B: Interview question generation
│   ├── agent_diagnostician.py    # Agent C: Triage report synthesis
│   ├── orchestrator.py           # LangGraph workflow orchestration
│   ├── ui_gradio.py             # Gradio web interface
│   └── prepare_few_shot.py       # ODIR-5K dataset preparation
│
├── docs/                         # Documentation
│   ├── PRD.md                    # Product Requirements Document
│   └── QUICKSTART.md             # Quick start guide
│
├── presentation/                 # Presentation materials
│   ├── EXECUTIVE_SUMMARY.md      # One-page business overview
│   ├── PITCH_DECK.md            # 5-minute pitch deck outline
│   ├── TECHNICAL_POSTER.md       # Technical deep dive poster
│   └── SHOWCASE_MATERIALS.md     # Index of all materials
│
├── assets/                       # Visual assets
│   ├── architecture_diagram.png  # Three-agent workflow diagram
│   └── impact_comparison.png     # Traditional vs VisionLink comparison
│
├── data/                         # Data files
│   └── few_shot_examples.json    # Few-shot prompting examples
│
├── scripts/                      # Utility scripts
│   ├── check_cuda.py            # CUDA availability checker
│   ├── check_handles.py         # Process handle checker
│   ├── check_user.py            # User verification
│   ├── download_model.py        # Model download utility
│   ├── extract_model.py         # Model extraction utility
│   ├── find_handle.py           # Handle finder
│   ├── hack_config.py           # Configuration utility
│   ├── test_backbone.py         # Backbone testing
│   ├── test_gradio.py           # Gradio testing
│   ├── verify_auth.py           # Authentication verification
│   └── who_am_i.py              # User identity checker
│
├── venv_gradio/                 # Virtual environment (gitignored)
│   └── ...                       # Python packages
│
├── hf_cache/                    # Hugging Face cache (gitignored)
│   └── ...                       # Downloaded models
│
└── archive/                     # ODIR-5K dataset (gitignored)
    └── ODIR-5K/
        ├── Training Images/
        └── ...
```

## Directory Descriptions

### `/src` - Source Code
Contains all Python source files for the VisionLink application:
- **Agents**: Three specialized AI agents (Observer, Investigator, Diagnostician)
- **Orchestration**: LangGraph workflow management
- **UI**: Gradio web interface
- **Data Prep**: Dataset preparation utilities

### `/docs` - Documentation
Technical and user documentation:
- **PRD.md**: Detailed product requirements and architecture
- **QUICKSTART.md**: Installation and usage guide

### `/presentation` - Presentation Materials
Materials for showcasing VisionLink:
- **EXECUTIVE_SUMMARY.md**: One-page business overview
- **PITCH_DECK.md**: Complete pitch deck with speaker notes
- **TECHNICAL_POSTER.md**: Technical deep dive for conferences
- **SHOWCASE_MATERIALS.md**: Index and usage guide for all materials

### `/assets` - Visual Assets
Images and diagrams for presentations and documentation:
- **architecture_diagram.png**: Three-agent workflow visualization
- **impact_comparison.png**: Traditional vs VisionLink comparison

### `/data` - Data Files
Application data and examples:
- **few_shot_examples.json**: Curated examples from ODIR-5K for few-shot prompting

### `/scripts` - Utility Scripts
Helper scripts for development and testing:
- CUDA and hardware checks
- Model download and extraction
- Testing utilities
- Configuration helpers

## Quick Navigation

### For Users
- **Getting Started**: [QUICKSTART.md](docs/QUICKSTART.md)
- **Run the UI**: `python src/ui_gradio.py`
- **View Examples**: [data/few_shot_examples.json](data/few_shot_examples.json)

### For Developers
- **Architecture**: [PRD.md](docs/PRD.md)
- **Source Code**: [src/](src/)
- **Agent A**: [src/agent_observer.py](src/agent_observer.py)
- **Agent B**: [src/agent_investigator.py](src/agent_investigator.py)
- **Agent C**: [src/agent_diagnostician.py](src/agent_diagnostician.py)
- **Orchestrator**: [src/orchestrator.py](src/orchestrator.py)

### For Recruiters/Judges
- **Executive Summary**: [presentation/EXECUTIVE_SUMMARY.md](presentation/EXECUTIVE_SUMMARY.md)
- **Pitch Deck**: [presentation/PITCH_DECK.md](presentation/PITCH_DECK.md)
- **Technical Poster**: [presentation/TECHNICAL_POSTER.md](presentation/TECHNICAL_POSTER.md)
- **Diagrams**: [assets/](assets/)

## Running the Application

### From Project Root
```bash
# Activate virtual environment
.\venv_gradio\Scripts\Activate.ps1  # Windows
# source venv_gradio/bin/activate    # Linux/Mac

# Run the Gradio UI
python src/ui_gradio.py
```

### From src/ Directory
```bash
cd src
python ui_gradio.py
```

## File Sizes (Approximate)

- **Source Code**: ~30 KB
- **Documentation**: ~25 KB
- **Presentation Materials**: ~40 KB
- **Visual Assets**: ~1.5 MB
- **Data**: ~5 KB
- **Scripts**: ~5 KB

**Total (excluding venv, cache, dataset)**: ~1.6 MB

## Gitignored Items

The following directories are excluded from version control:
- `venv_gradio/` - Virtual environment (~500 MB)
- `hf_cache/` - Model cache (~10 GB)
- `archive/` - ODIR-5K dataset (~1.7 GB)
- `__pycache__/` - Python bytecode
- Various log and error files

See [.gitignore](.gitignore) for complete list.

---

*Last Updated: January 29, 2026*
