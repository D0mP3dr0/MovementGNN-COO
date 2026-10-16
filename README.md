# Code of MovementGNN: a physics-informed graph attention network for military terrain traversability classification

Luis Felipe Comodo Seelig and Ronaldo Moreira Salles

This repository holds the code of MovementGNN, a GATv2-based graph neural network that produces Combined Obstacle Overlays (COO) within the NATO Intelligence Preparation of the Battlefield (IPB) framework. The model performs multi-task node classification on a terrain graph with one node per pixel of the Copernicus DEM, enriched with Sentinel-2 imagery, and classifies traversability (Go / Slow Go / No Go) for four military fractions: dismounted, motorized, mechanized and armored. The code covers the data download, the label rules, the graph construction and spatial split, the model and its COO-informed physics loss, training, the baselines, inference, the post-training analyses and the article figures.

This line of work continues in [github.com/D0mP3dr0/movementgnn-terrain-mobility](https://github.com/D0mP3dr0/movementgnn-terrain-mobility).

No data, trained weights or result files are included, so this repository does not reproduce numbers by itself; it documents the code that produced them.

## Repository structure

```
MovementGNN-COO/
├── src/                          # Core library
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
│   │   ├── baseline_runner.py    # Runs all baselines
│   │   └── export_baseline_to_geotiff.py
│   ├── data_processing/
│   │   ├── feature_extractor.py  # Topographic feature extraction
│   │   ├── dataset_loader.py     # Graph dataset loading
│   │   └── data_validator.py     # Data integrity checks
│   ├── graph_construction/
│   │   ├── graph_integrator.py   # Integrates DAMEPLAN labels into the graph
│   │   └── spatial_splitter.py   # Spatial train/val/test split
│   ├── label_generation/
│   │   ├── dameplan_rules.py     # Doctrinal traversability rules
│   │   ├── label_generator.py    # Label generation from features
│   │   └── label_validator.py    # Label distribution validation
│   └── paths.py                  # Central path configuration
│
├── scripts/
│   ├── training/
│   │   ├── 07_train_gnn.py               # V1 training (Colab)
│   │   ├── 07_train_gnn_v2.py            # V2 training (local GPU)
│   │   ├── 08_resume_train.py            # Resume from checkpoint
│   │   └── 07b_retrain_armored_fix.py    # V2 fine-tuning of the armored head
│   ├── analysis/
│   │   ├── 09_transition_diagnosis.py    # Transition zone analysis
│   │   ├── 10_uncertainty_analysis.py    # Uncertainty and spatial coherence
│   │   ├── 13_label_audit.py             # Label quality audit
│   │   ├── 14_embeddings_analysis.py     # PCA of learned embeddings
│   │   ├── 15_geospatial_maps.py         # Cartographic maps
│   │   └── analyze_dataset.py            # EDA of the HeteroData graph
│   ├── inference/
│   │   ├── 11_generate_probs.py  # Full-graph inference to probabilities
│   │   ├── 12_generate_zrn.py    # Post-processing (entropy-based fourth class)
│   │   └── re_export_geotiff.py  # GeoTIFF re-export utility
│   └── data/
│       ├── download_pacaraima_full_package.py   # Runs the downloads below
│       ├── download_dem_pacaraima_q1q4.py       # Copernicus GLO-30 DEM
│       ├── download_sentinel2_pacaraima_q1q4.py # Sentinel-2 L2A
│       ├── download_lidar_pacaraima_q1q4.py     # ICESat-2 and GEDI
│       ├── 06b_extract_topo_embeddings.py       # Embedding extraction (Colab)
│       └── 06b_extract_topo_embeddings_local.py # Embedding extraction (local)
│
├── figures/                      # Article figure scripts (fig01 to fig07, ERDC composite, feature analysis)
│   └── utils_nato.py             # Shared NATO styling utilities
│
├── train.py                      # Modular training entry point
├── requirements.txt
├── verify_code.py, CODE_AST_SHA256   # Code identity check (see below)
├── PROVENANCE.md, SHA256SUMS         # File provenance and digests
├── CITATION.cff
└── LICENSE                       # MIT
```

Six scripts were renamed from their Portuguese working names to the English names above; no other file imports them by name, and `PROVENANCE.md` maps each new name to the name it was run under. Inside the code, the four fractions keep their Portuguese keys (`a_pe` dismounted, `motorizada` motorized, `mecanizada` mechanized, `blindada` armored), and DAMEPLAN is the Brazilian Army planning-data manual the label rules come from. Those keys name columns and files, so changing them would change the code.

## Input data

All input data are public: the Copernicus GLO-30 DEM and Sentinel-2 L2A imagery (bands B02 to B04 and B08) from the [Copernicus Data Space](https://dataspace.copernicus.eu/). The download scripts are in `scripts/data/`.

## Data layout

By default, scripts read and write under the repository root:

```
data/
├── graph/          # HeteroData graphs, embeddings, terrain checkpoints
├── raw/
│   ├── dem/
│   ├── sentinel2/pacaraima/
│   └── lidar/
├── analysis/       # Extracted features, labels, positions, raster metadata
└── geo/            # Optional boundary and reference layers for figures

results/
├── v1/             # V1 training outputs
├── v2/             # V2 Colab outputs
├── v2_local/       # V2 local training outputs
├── v2_armored_finetune/
├── baselines/      # RF, MLP and rule-based predictions
└── analysis/       # Post-training analysis outputs
```

### Environment variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `MOVEMENTGNN_DATA_ROOT` | Root for graphs, raw downloads and analysis extracts | `./data` |
| `MOVEMENTGNN_RESULTS_ROOT` | Root for training outputs and analysis results | `./results` |
| `MOVEMENTGNN_WORK_ROOT` | Google Drive root, used only when running in Colab without the two overrides above | current directory |

Example:

```bash
export MOVEMENTGNN_DATA_ROOT=/path/to/my/data
export MOVEMENTGNN_RESULTS_ROOT=/path/to/my/results
python scripts/training/07_train_gnn_v2.py
```

## Pipeline

```
1. Download raw data          → scripts/data/download_*.py
2. Extract embeddings         → scripts/data/06b_extract_topo_embeddings*.py
3. Train V1                   → scripts/training/07_train_gnn.py
4. Train V2                   → scripts/training/07_train_gnn_v2.py
5. Full-graph inference       → scripts/inference/11_generate_probs.py
6. Post-training analysis     → scripts/analysis/09_*.py, 10_*.py, 13_*.py, 14_*.py
7. Article figures            → figures/fig*.py
```

V2 differs from V1 in two ways, both visible in the training scripts: it drops the two LiDAR features and it uses asymmetric, per-fraction class weights that penalize the transitional Slow Go class more heavily.

## Code identity and provenance

The scripts are the ones that were run, with the changes listed in `PROVENANCE.md`: a few docstrings edited, one log message reworded, six files renamed, and the absolute Google Drive default in `src/paths.py` replaced by a value read from `MOVEMENTGNN_WORK_ROOT`. `verify_code.py` recomputes the digest of each script's syntax tree with exactly those parts normalized and compares it with `CODE_AST_SHA256`, which lists the digests of the scripts as run:

```bash
python3.11 verify_code.py     # expects "56/56 files: code identical to the original"
sha256sum -c SHA256SUMS       # byte integrity of every published file
```

## Trained weights and graph data

Trained checkpoints and the preprocessed graph are available from the first author on request: seelig.felipe@eb.mil.br.

## Requirements

```bash
pip install -r requirements.txt
```

PyTorch Geometric needs a platform-specific installation; see the [PyG installation guide](https://pytorch-geometric.readthedocs.io/en/latest/install/installation.html).

## Citation

See `CITATION.cff`.

## License

MIT; see [LICENSE](LICENSE).

## Acknowledgments

Military Science Laboratory (LCM), Brazilian Army Command and General Staff College (ECEME), and the Military Institute of Engineering (IME).
