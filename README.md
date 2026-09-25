![NORA logo](https://i.ibb.co/0VJCC9Gf/IMG-20260114-WA0008.jpg)
 
# Standing Timber Volume Calculator
 
*For foresters and land managers: enter tree DBH, height, and species to instantly compute individual tree volume and stand-level volume per hectare.*
 
[![GitHub](https://img.shields.io/badge/GitHub-Nora--Research--Lab-181717?logo=github)](https://github.com/Nora-Research-Lab) [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NoraResearchLab-yellow)](https://huggingface.co/NoraResearchLab) [![LinkedIn](https://img.shields.io/badge/LinkedIn-NORA%20Research%20Lab-0A66C2?logo=linkedin)](https://www.linkedin.com/company/nora-research-lab) [![X](https://img.shields.io/badge/X-@noraresearchlab-000000?logo=x)](https://x.com/noraresearchlab) [![NORA Research Lab](https://img.shields.io/badge/Website-noraresearchlab.site-2ea44f)](https://noraresearchlab.site) [![NORA Earth Intelligence](https://img.shields.io/badge/Platform-noraearth.xyz-2ea44f)](https://noraearth.xyz)
 

## Overview
 
**Industry:** Natural Resources & Land Management
 
This tool estimates the merchantable timber volume of a single tree or a uniform stand. It is designed for foresters, land managers, and natural resource professionals who need quick volume estimates for inventory or harvest planning.

Inputs:
- Tree species (dropdown: Douglas-fir, Loblolly Pine, Sugar Maple, Red Oak, generic hardwood, generic softwood; each species has a default form factor stored internally)
- Diameter at breast height (DBH) in centimeters (numeric slider or text input, range 5-200 cm)
- Tree height in meters (numeric input, range 1-60 m)
- Number of trees per hectare (stems/ha) – optional, default 1 for single tree calculation (numeric input, positive integer)
- Form factor (optional manual override, 0.3-0.7, default is species-specific: Douglas-fir 0.45, Loblolly Pine 0.42, Sugar Maple 0.48, Red Oak 0.43, generic hardwood 0.47, generic softwood 0.44). The user can toggle between using the default or entering a custom form factor.

Calculation logic:
1. If user does not manually enter form factor, use the species default.
2. Compute individual tree volume (m³) = (π/4) × (DBH/100)² × height × form_factor. (DBH converted to meters)
3. Stand volume per hectare (m³/ha) = individual tree volume × number_of_trees_per_hectare.
4. Also compute board foot equivalent: 1 m³ ≈ 424 board feet (Doyle or Scribner simplified; use a fixed conversion factor 424). Output board feet per tree and per hectare.
5. Classify the volume: < 0.1 m³ = 'sapling', 0.1-0.5 m³ = 'small', 0.5-1.0 m³ = 'medium', >1.0 m³ = 'large'. Display classification.

Gradio UI components:
- Dropdown for species
- Number inputs for DBH, height, trees/ha
- Checkbox: 'Use custom form factor' – if checked, a number input for form factor appears
- Button: 'Calculate Volume'
- Output area showing: individual tree volume (m³ and board feet), stand volume per hectare (m³/ha and board feet/acre optionally), size classification, and a simple horizontal bar chart comparing the tree volume to the typical range for the selected species (using stored average volumes for that species).
- Optional export button to download results as CSV.

No AI/ML component; all logic is deterministic forestry formulas.
 
## Run it
 
```bash
docker build -t standing-timber-volume-calculator .
docker run -p 7860:7860 standing-timber-volume-calculator
```
 
Then open http://localhost:7860 in your browser.
 
## About
 
This tool was generated and published automatically by the **NORA Earth Intelligence**
tool factory, an autonomous pipeline maintained by **NORA Research Lab** that turns
one idea per run into a small, working geoscience tool — end to end, with an
LLM writing and Docker-testing the code, and another model generating the
banner above.
 
- Platform: [https://noraearth.xyz](https://noraearth.xyz)
- Parent lab: [https://noraresearchlab.site](https://noraresearchlab.site)
 
Built 2026-09-25.
 
---
 
### Maintainer
 
**NORA Research Lab**
[![GitHub](https://img.shields.io/badge/GitHub-Nora--Research--Lab-181717?logo=github)](https://github.com/Nora-Research-Lab) [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NoraResearchLab-yellow)](https://huggingface.co/NoraResearchLab) [![LinkedIn](https://img.shields.io/badge/LinkedIn-NORA%20Research%20Lab-0A66C2?logo=linkedin)](https://www.linkedin.com/company/nora-research-lab) [![X](https://img.shields.io/badge/X-@noraresearchlab-000000?logo=x)](https://x.com/noraresearchlab) [![NORA Research Lab](https://img.shields.io/badge/Website-noraresearchlab.site-2ea44f)](https://noraresearchlab.site) [![NORA Earth Intelligence](https://img.shields.io/badge/Platform-noraearth.xyz-2ea44f)](https://noraearth.xyz)
