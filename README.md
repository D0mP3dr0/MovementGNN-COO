# MovementGNN-COO

**Reproducibility package** for:

> Seelig, L. F. C.; Migon, E. X. F. G. *MovementGNN: A Physics-Informed Graph Attention Network for Military Terrain Traversability Classification.* Defence Technology, 2026.

---

## Overview

MovementGNN is a GATv2-based graph neural network that automates the production of Combined Obstacle Overlays (COO) within the NATO Intelligence Preparation of the Battlefield (IPB) framework. The model performs multi-task node classification on a 12-million-node terrain graph derived from Copernicus DEM and Sentinel-2 imagery, simultaneously classifying traversability (Go / Slow Go / No Go) for four military fractions: dismounted, motorized, mechanized, and armored.

Key contributions:

1. **MovementGNN architecture** — GATv2 with shared backbone and per-fraction classification heads
2. **COO-Informed Loss (CIL)** — physics-informed loss encoding NATO FM 5-33 traversability thresholds as differentiable penalties
3. **Remote sensing proxies** — NDVI and NDWI as substitutes for in-situ vegetation and hydrological measurements
4. **Spatial anti-leakage protocol** — grid-based splitting ensuring generalization metrics
5. **Georeferenced GeoTIFF output** — directly ingestible by C2 systems
6. **Documented model evolution (V1 → V2)** — evidence-based optimization workflow

## Repository Structure

```
MovementGNN-COO/
├── src/                          # Core library (modular)
│   ├── models/
│   │   ├── movement_gnn.py       # GATv2 architecture
│   │   ├── dameplan_loss.py      # COO-Informed Loss (CIL)
│   │   └── focal_loss.py         # Focal loss variant
│   ├── training/
│   │   ├── trainer.py            # Training loop with NeighborLoader
│   │   └── early_stopping.py     # Early stopping by val_loss
│   ├── baselines/
│   │   ├── random_forest_baseline.py
│   │   ├── mlp_baseline.py
│   │   ├── rule_based_baseline.py
│   │   ├── baseline_runner.py    # Orchestrates all baselines
│   │   └── export_baseline_to_geotiff.py
│   ├── data_processing/
│   │   ├── feature_extractor.py  # Topographic feature extraction
│   │   ├── dataset_loader.py     # Graph dataset loading
│   │   └── data_validator.py     # Data integrity checks
│   ├── graph_construction/
│   │   ├── graph_integrator.py   # Integrates DAMEPLAN labels into graph
│   │   └── spatial_splitter.py   # Spatial train/val/test splitting
│   └── label_generation/
│       ├── dameplan_rules.py     # NATO FM 5-33 traversability rules
│       ├── label_generator.py    # Label generation from features
│       └── label_validator.py    # Label distribution validation
│
├── scripts/
│   ├── training/
│   │   ├── 07_train_gnn.py       # V1 training (Colab, baseline)
│   │   ├── 07_train_gnn_v2.py    # V2 training (local, optimized)
│   │   ├── 08_resume_train.py    # Resume from checkpoint
│   │   └── 07b_retrain_blindada_fix.py  # V2 fine-tuning
│   ├── analysis/
│   │   ├── 09_diagnostico_transicao.py  # Transition zone analysis
│   │   ├── 10_analise_incerteza.py      # Uncertainty & spatial coherence
│   │   ├── 13_label_audit.py            # Label quality audit
│   │   ├── 14_embeddings_analysis.py    # PCA of learned embeddings
│   │   ├── 15_analise_geoespacial.py    # GEOINT cartographic maps
│   │   └── analyze_dataset.py           # EDA of HeteroData
│   ├── inference/
│   │   ├── 11_gerar_probs.py     # Full-graph inference → probabilities
│   │   ├── 12_gerar_zrn.py       # Post-processing (entropy-based 4th class)
│   │   └── re_export_geotiff.py  # GeoTIFF re-export utility
│   └── data/
│       ├── download_pacaraima_full_package.py  # Orchestrator
│       ├── download_dem_pacaraima_q1q4.py      # Copernicus GLO-30 DEM
│       ├── download_sentinel2_pacaraima_q1q4.py # Sentinel-2 L2A
│       ├── download_lidar_pacaraima_q1q4.py     # ICESat-2 + GEDI
│       ├── 06b_extract_topo_embeddings.py       # Embedding extraction (Colab)
│       └── 06b_extract_topo_embeddings_local.py # Embedding extraction (local)
│
├── figures/                      # Article figure generation scripts
│   ├── fig01_study_area.py
│   ├── fig02_pipeline.py
│   ├── fig03_architecture.py
│   ├── fig04_comparative.py
│   ├── fig05_intelligence_gap.py
│   ├── fig06_performance.py
│   ├── fig07_asymmetric_error.py
│   ├── fig_feature_analysis.py
│   ├── fig_erdc_composite.py
│   └── utils_nato.py            # Shared NATO styling utilities
│
├── train.py                     # Modular training entry point
├── requirements.txt
├── LICENSE                      # MIT
└── README.md
```

## Input Data

All input data are publicly available:

| Source | Product | Resolution | Access |
|--------|---------|------------|--------|
| ESA Copernicus | GLO-30 DEM | 30 m | [Copernicus Data Space](https://dataspace.copernicus.eu/) |
| ESA Copernicus | Sentinel-2 L2A (B02-B04, B08) | 10 m | [Copernicus Data Space](https://dataspace.copernicus.eu/) |

Download scripts are provided in `scripts/data/`.

## Data Layout

By default, scripts read and write under the repository root:

```
data/
├── graph/          # HeteroData graphs, embeddings, terrain checkpoints
├── raw/
│   ├── dem/
│   ├── sentinel2/pacaraima/
│   └── lidar/
├── analysis/       # Extracted features, labels, pos, raster_meta
└── geo/            # Optional boundary / reference layers for figures

results/
├── v1/             # Baseline (V1) training outputs
├── v2/             # V2 Colab outputs
├── v2_local/       # V2 local training outputs
├── v2_armored_finetune/
├── baselines/      # RF, MLP, rule-based predictions
└── analysis/       # Post-training analysis outputs
```

### Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `MOVEMENTGNN_DATA_ROOT` | Root for graphs, raw downloads, analysis extracts | `./data` |
| `MOVEMENTGNN_RESULTS_ROOT` | Root for training outputs and analysis results | `./results` |
| `MOVEMENTGNN_WORK_ROOT` | Colab Drive root (only when running in Colab without overrides) | `/content/drive/MyDrive/GEOINT` |

Example (pointing to an external data directory):

```bash
export MOVEMENTGNN_DATA_ROOT=/path/to/my/data
export MOVEMENTGNN_RESULTS_ROOT=/path/to/my/results
python scripts/training/07_train_gnn_v2.py
```

## Reproduction Pipeline

```
1. Download raw data          → scripts/data/download_*.py
2. Extract embeddings         → scripts/data/06b_extract_topo_embeddings*.py
3. Train V1 (baseline)        → scripts/training/07_train_gnn.py
4. Train V2 (optimized)       → scripts/training/07_train_gnn_v2.py
5. Full-graph inference       → scripts/inference/11_gerar_probs.py
6. Post-training analysis     → scripts/analysis/09_*.py, 10_*.py, 13_*.py, 14_*.py
7. Generate article figures   → figures/fig*.py
```

## Model Variants

| Variant | Features | Batch Size | Class Weights | Accuracy | F1-macro |
|---------|----------|------------|---------------|----------|----------|
| V1 (baseline) | d=273 (17 raw + 256 emb) | 1,050,000 | Uniform | 0.974 | 0.954 |
| V2 (optimized) | d=271 (15 raw + 256 emb) | 750,000 | Asymmetric | 0.952 | 0.928 |

V2 removes two LiDAR features (zero information content) and introduces asymmetric class weights, trading 2.1 pp accuracy for improved spatial coherence and conservative error profile (6.7:1 to 17.1:1 conservative-to-dangerous ratio).

## Pre-trained Checkpoints and Graph Data

Pre-trained model checkpoints and preprocessed graph data (HeteroData, ~2 GB) are available upon request. Contact: seelig.felipe@eb.mil.br

## Requirements

```bash
pip install -r requirements.txt
```

**Note:** PyTorch Geometric requires platform-specific installation. See [PyG Installation Guide](https://pytorch-geometric.readthedocs.io/en/latest/install/installation.html).

## Citation

```bibtex
@article{seelig2026movementgnn,
  title={MovementGNN: A Physics-Informed Graph Attention Network for Military Terrain Traversability Classification},
  author={Seelig, Luis Felipe Comodo and Migon, Eduardo Xavier Ferreira Glaser},
  journal={Defence Technology},
  year={2026}
}
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgments

Military Science Laboratory (LCM), Brazilian Army Command and General Staff College (ECEME), and the Military Institute of Engineering (IME).
