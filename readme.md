# Morphology Analysis Pipeline

Analysis code and example data for distal dendrite reconstructions from ExM, EM, and STED imaging.

The repository combines:

- Python analysis code for branch- and diameter-level measurements.
- Jupyter notebooks for modality-specific exploratory analysis.
- Example figures and example morphology files.

The associated dataset is hosted on [Zenodo](https://zenodo.org/records/14037025). This repository contains the analysis pipeline and example notebook workflows.

## Setup

Create the conda environment from the exported environment file:

```bash
conda env create -f environment.yml
conda activate BonnData
```

If you already have the environment, update it with:

```bash
conda env update -f environment.yml --prune
```

Open the notebooks in `notebooks/` and set the root directory expected by the notebook to your local data location when required.

## Repository Layout

- `data/`: input tables and morphology-related source data.
- `figs/`: example figures used in notebooks and documentation.
- `notebooks/`: modality-specific analysis notebooks and example outputs.
- `output/`: generated plots and analysis exports.
- `scripts/`: helper scripts for running parts of the workflow.
- `src/`: reusable Python analysis modules.
- `workflow/`: workflow-specific assets.

## Analysis Workflow

Each microscopy modality is analyzed through its corresponding notebook. The notebooks load branch or branch-segment reconstructions from CSV tables, compare reconstructions against raw and binary images, and support manual correction of false positives and false negatives before downstream quantification.

The default code shows the reconstruction and identified DSCs for the example dendrite in the figures. Diameters of other dendritic reconstructions can also be explored.

![example diameter plot](<figs/Diam_branch_C1_03_cell2_d3.png>)

### ExM

The ExM example dataset includes a full dendritic morphology reconstruction with raw images, binarized images, and local-thickness analysis outputs.

![Example dendrite](<figs/20210201_dg-t1_af488-03_decon-Resolution Level 1_8bit_100-20000_Zproj.png>)

Typical ExM folder contents include:

- `raw/` and `decon/` image data.
- `binary/` outputs generated from Fiji MaxEntropy binarization.
- `analysis/` outputs including local thickness (`_LD`) and skeletonization (`SK`) files used to generate measurement tables.

### STED

The STED example dataset contains raw image volumes together with derived binary images and analysis products.

Typical STED folder contents include:

- `raw/` image data.
- `binary/` outputs generated from Fiji MaxEntropy binarization.
- `analysis/` outputs including local thickness (`_LD`) and skeletonization (`SK`) files used to generate measurement tables.

### EM

The EM example dataset contains cropped EM images for example dendrites together with [IMOD](https://bio3d.colorado.edu/imod/) models of the dendrite and neighboring structures.

## Notes

- Generated outputs in `output/` are intentionally excluded from version control.

## Citation

If you use this analysis pipeline or dataset in your research, please cite our paper:

> Kelly, T., Ofer, N., Rodriguez-Gatica, J. E., Döngi, M., Cissewski, N., Barboni, M., ... & Beck, H. (2026). Dendritic shaft constrictions shape synaptic integration in neurons. *Science Advances*, 12(37), eaec4911. https://doi.org/10.1126/sciadv.aec4911

To reference or reproduce the exact computational environment and archived code snapshot:

> Kelly, T. (2026). DSC Morphology Pipeline.
> GitHub. https://github.com/tonykelly00/DSC_morphology_pipeline
> Zenodo. https://doi.org/10.5281/zenodo.14037025
