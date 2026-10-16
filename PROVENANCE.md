# Provenance

This file lists the SHA-256 of every file in the repository next to the SHA-256 of the file as it was run,
and states what differs between the two. `SHA256SUMS` carries the published digests in the format read by
`sha256sum -c`.

## What differs from the files as run

- **File names.** Six scripts were renamed from their Portuguese working names to English names. No other
  file imports them by name. The table below gives the name each file was run under.
- **Python sources.** Comments are as run. A few docstrings were edited (the file name in the first line of
  each renamed script, and three mentions of where the code came from), and one log message of the Sentinel-2
  download script was reworded. The absolute Google Drive default of `MOVEMENTGNN_WORK_ROOT` in `src/paths.py`
  was replaced by the variable `INTERNAL_WORK_ROOT_DEFAULT`, read from the same environment variable (default:
  the current directory) in one statement added after the `__future__` import. The executable code is otherwise
  unchanged: `verify_code.py` recomputes, for each script, the digest of its syntax tree with those parts
  normalized and compares it with the digest of the script as run, listed in `CODE_AST_SHA256` and in the last
  column below.
- **README.md, LICENSE.** Rewritten for this package (title, authors as in the manuscript, no result numbers,
  since no result files are included). `CITATION.cff`, `verify_code.py`, `CODE_AST_SHA256`, `PROVENANCE.md`,
  `SHA256SUMS` and `.gitattributes` are new.

Because the bytes of some scripts changed, a digest of a script recorded elsewhere refers to the file as run;
the third column below gives those.

## Renamed files

| published name | name as run |
| --- | --- |
| `scripts/analysis/09_transition_diagnosis.py` | `scripts/analysis/09_diagnostico_transicao.py` |
| `scripts/analysis/10_uncertainty_analysis.py` | `scripts/analysis/10_analise_incerteza.py` |
| `scripts/analysis/15_geospatial_maps.py` | `scripts/analysis/15_analise_geoespacial.py` |
| `scripts/inference/11_generate_probs.py` | `scripts/inference/11_gerar_probs.py` |
| `scripts/inference/12_generate_zrn.py` | `scripts/inference/12_gerar_zrn.py` |
| `scripts/training/07b_retrain_armored_fix.py` | `scripts/training/07b_retrain_blindada_fix.py` |

## Every file

| file | name as run | sha256 as run | sha256 published here | check |
| --- | --- | --- | --- | --- |
| `.gitignore` | `.gitignore` | `7968e276d94ef1bca6f25436e909b86208920fbdd5a8621cde9e81a5d7cda94f` | `7968e276d94ef1bca6f25436e909b86208920fbdd5a8621cde9e81a5d7cda94f` | byte-identical |
| `CITATION.cff` | n/a | n/a | `497a481e756820b74fa3dfa70e3607f8d837c2c9513d75a61f719149518ad284` | new file |
| `LICENSE` | `LICENSE` | `89c3189f3a789adaaa6f67dcc536c92b632a5131ef62bff0b8cc09801ff73b30` | `01c48ede86b2049553698a5d8d945654451833ded27587f79d6b849e9b304b3b` | rewritten for this package |
| `README.md` | `README.md` | `4d3e1e24c1adaa72453165b3210dbcc63877955c1ead7ef36141b6b1f4a988f4` | `54c823f376ea951d627f55485cf9483b81892be760d0268133f3d1b38a48b4ea` | rewritten for this package |
| `figures/fig01_study_area.py` | `figures/fig01_study_area.py` | `15fe04a74d77f5057d11957efc848df3697468af77544318b85695f6f49b90f7` | `15fe04a74d77f5057d11957efc848df3697468af77544318b85695f6f49b90f7` | byte-identical |
| `figures/fig02_pipeline.py` | `figures/fig02_pipeline.py` | `16d0618c5704951693aa6d80afbf0854f03f40bb73fd6e77d08b2922184f9e61` | `16d0618c5704951693aa6d80afbf0854f03f40bb73fd6e77d08b2922184f9e61` | byte-identical |
| `figures/fig03_architecture.py` | `figures/fig03_architecture.py` | `3ffd7eebb62740fde1b8d2a3cbc994c0bfa52bf3a35e6b56d3bd669adb892f1f` | `3ffd7eebb62740fde1b8d2a3cbc994c0bfa52bf3a35e6b56d3bd669adb892f1f` | byte-identical |
| `figures/fig04_comparative.py` | `figures/fig04_comparative.py` | `17fc7a56d08b45d61ab7d08ed6b206112badc4915ed09fe02ca8fb350f1640f3` | `17fc7a56d08b45d61ab7d08ed6b206112badc4915ed09fe02ca8fb350f1640f3` | byte-identical |
| `figures/fig05_intelligence_gap.py` | `figures/fig05_intelligence_gap.py` | `af319a7e9d6e628c192f7227ffafe3e29be81cf94208516f18bb2e7e8eef7649` | `af319a7e9d6e628c192f7227ffafe3e29be81cf94208516f18bb2e7e8eef7649` | byte-identical |
| `figures/fig06_performance.py` | `figures/fig06_performance.py` | `08161a3e895f0418eae1095271d22f217d9bbaabfc3829f75e83d0e1dea1882f` | `08161a3e895f0418eae1095271d22f217d9bbaabfc3829f75e83d0e1dea1882f` | byte-identical |
| `figures/fig07_asymmetric_error.py` | `figures/fig07_asymmetric_error.py` | `3cf3a796ec3fecb642dd1b07c7ba9612261237875fbfa2161ebd4fb6840591ed` | `3cf3a796ec3fecb642dd1b07c7ba9612261237875fbfa2161ebd4fb6840591ed` | byte-identical |
| `figures/fig_erdc_composite.py` | `figures/fig_erdc_composite.py` | `dfa981938aac6d1d0a3490e0636f4cdc45e536913202ce052bd088852ad54a79` | `64f7bd1012aa949a9964f2fd641adb3cf343265a53b8223a03e865af331e91ff` | code digest `9a0d9286a97fa6c87eb09bf508aa61f13b99a5cac8913833696d957356a1b667` |
| `figures/fig_feature_analysis.py` | `figures/fig_feature_analysis.py` | `f8326ad63e2b5a9e9d139b62391272eefd1347b5b2aa6033c3d8f674a52fa6bf` | `f8326ad63e2b5a9e9d139b62391272eefd1347b5b2aa6033c3d8f674a52fa6bf` | byte-identical |
| `figures/utils_nato.py` | `figures/utils_nato.py` | `f5af099d168dac4911c99efe47a793281d891ca01c63372394278350895d1020` | `8c5bac0e0a550b6d36fec1e4199de8c7a8078a5504645ce5fcfdc879a06707f6` | code digest `ffc010a58aff3f294faadb0cab65ffe9c8841c5311580bb8371a9b25c61d3466` |
| `requirements.txt` | `requirements.txt` | `7ab272e4ff382a5bb60c0e9b4510eca9c313fd3bb3b6293e171fffedd0e92998` | `7ab272e4ff382a5bb60c0e9b4510eca9c313fd3bb3b6293e171fffedd0e92998` | byte-identical |
| `scripts/analysis/09_transition_diagnosis.py` | `scripts/analysis/09_diagnostico_transicao.py` | `c37a9d6394f359e6a1ce29c3230c0e1b63f6e19a9f17cf844c3ca21e61941e24` | `4b22c06567fec781ead7b7c595a5a2596b1b93af54fca288dbc300f24f0da64a` | code digest `e54c09353c50847eb382d62beb18cf427a84a07d45fbf576bd5560c7be1fe805` |
| `scripts/analysis/10_uncertainty_analysis.py` | `scripts/analysis/10_analise_incerteza.py` | `5784db7f0e20a0d67e544ec50f06d2805715691e1c34a69f2f3296ab50543753` | `3e5957f0d95f051100437176b9406d8d766a8996abd2e66514a3b0d97ef2096c` | code digest `bd16689342a62f416db0fee9f25b3a0d07d1a781facaea9b6752abc3186cc039` |
| `scripts/analysis/13_label_audit.py` | `scripts/analysis/13_label_audit.py` | `6a273fa6180b1bb37f168ab6519f4690f5552a9a3c4ceb244883c9f08d4aa3ac` | `6a273fa6180b1bb37f168ab6519f4690f5552a9a3c4ceb244883c9f08d4aa3ac` | byte-identical |
| `scripts/analysis/14_embeddings_analysis.py` | `scripts/analysis/14_embeddings_analysis.py` | `2d81f9882cc203a0e02caf340615fda7bd9a06575b1bdd3036210cb6eb0df37c` | `2d81f9882cc203a0e02caf340615fda7bd9a06575b1bdd3036210cb6eb0df37c` | byte-identical |
| `scripts/analysis/15_geospatial_maps.py` | `scripts/analysis/15_analise_geoespacial.py` | `fdd7a5608a141a59131ac3a96cd8b4208fa331ae0376d306e36943a9c02ab6bd` | `0d7c206e7238d1464030e09a5fb37ad8a57c6d1214aaf3d2f0452da011f4eade` | code digest `11cc12ba61c970c811790ab7ef9cf7e7dabdc21425aa80dbca69c9fe159be766` |
| `scripts/analysis/analyze_dataset.py` | `scripts/analysis/analyze_dataset.py` | `682afd0b18f7d39c6538eabf5186a42d944ab23503a02871ab27a53c37d1af64` | `682afd0b18f7d39c6538eabf5186a42d944ab23503a02871ab27a53c37d1af64` | byte-identical |
| `scripts/data/06b_extract_topo_embeddings.py` | `scripts/data/06b_extract_topo_embeddings.py` | `8629c87bf09cbc1375a89f0f653de6836345de1eae110f53501f09ef66a645a3` | `8629c87bf09cbc1375a89f0f653de6836345de1eae110f53501f09ef66a645a3` | byte-identical |
| `scripts/data/06b_extract_topo_embeddings_local.py` | `scripts/data/06b_extract_topo_embeddings_local.py` | `58b1660610518fcab364380f8e3ee951ed8fa1d37d26ab1380f2647c43d7e604` | `58b1660610518fcab364380f8e3ee951ed8fa1d37d26ab1380f2647c43d7e604` | byte-identical |
| `scripts/data/download_dem_pacaraima_q1q4.py` | `scripts/data/download_dem_pacaraima_q1q4.py` | `93294d75cb3850d771938ddd34749ea1a5b572e60cc3804b34cb1dcc6aae06d2` | `93294d75cb3850d771938ddd34749ea1a5b572e60cc3804b34cb1dcc6aae06d2` | byte-identical |
| `scripts/data/download_lidar_pacaraima_q1q4.py` | `scripts/data/download_lidar_pacaraima_q1q4.py` | `7b4b97e1f63d3fedfbe8fc65e5513977945ec3d1501f48096e8d188864556a4b` | `7b4b97e1f63d3fedfbe8fc65e5513977945ec3d1501f48096e8d188864556a4b` | byte-identical |
| `scripts/data/download_pacaraima_full_package.py` | `scripts/data/download_pacaraima_full_package.py` | `ee1c7b4a1773c5ae5f8a9629c5d022c16567e0ea25c625cb1a793682232b594f` | `ee1c7b4a1773c5ae5f8a9629c5d022c16567e0ea25c625cb1a793682232b594f` | byte-identical |
| `scripts/data/download_sentinel2_pacaraima_q1q4.py` | `scripts/data/download_sentinel2_pacaraima_q1q4.py` | `9b64be64e790e36fd95feb1bc7a50bdb44e3f22df5c0b7d3169ec2bd859bf776` | `c3536b565da4787951c36cb9d96b92f865e3bb7760dc3708edb8dfb33170eed8` | code digest `5f95f0152f198e24c9526d556ec30fd81a0cbb6aff774aa666ce4c7f5f006e8b` |
| `scripts/inference/11_generate_probs.py` | `scripts/inference/11_gerar_probs.py` | `44f7c0004f24c43f2d2a960701bb2a3b3af5b79f7921a7566e5e0d6ec33f5e45` | `9b245bd0bc749c1eb87bc8f890d67b5071811823c5d0688825730ac59e981606` | code digest `0a71a73f0f27dc7dfddd09612e6adc26e14c95a71c775c87a26da86bccf7d931` |
| `scripts/inference/12_generate_zrn.py` | `scripts/inference/12_gerar_zrn.py` | `ae2c7a416e94b840bae425ec74bd885964ba850127f12dfbc134da68c33dc072` | `58f1df4cecf4312099168aadde854fb6b9c96a7d549291ff0af1e637389b190a` | code digest `d8a9e0b92bac59c68a7ea23ae28f1a79ed0cf696ff9690262ba1d3ceff5fb487` |
| `scripts/inference/re_export_geotiff.py` | `scripts/inference/re_export_geotiff.py` | `f5edf7b282ea6d8cb599844037556f3a6ea0309f42ad401d5096d297fd17891a` | `f5edf7b282ea6d8cb599844037556f3a6ea0309f42ad401d5096d297fd17891a` | byte-identical |
| `scripts/training/07_train_gnn.py` | `scripts/training/07_train_gnn.py` | `dbe171dd642038a28d1c267c62b6b5c746eddf90231b97b7381c14ba3f5fde5c` | `8186fdaca88a18cdb6e090425a3c8d38ed6db8f2fcc796a26224a3208c071ca7` | code digest `99445e94cc891172bfd07affc7704975235b6ac910c5f65c04d336819d74e105` |
| `scripts/training/07_train_gnn_v2.py` | `scripts/training/07_train_gnn_v2.py` | `aec33d5d7d087beac2aa59251d2b2f4df2488f5b8c049d10948de3518e668bd7` | `aec33d5d7d087beac2aa59251d2b2f4df2488f5b8c049d10948de3518e668bd7` | byte-identical |
| `scripts/training/07b_retrain_armored_fix.py` | `scripts/training/07b_retrain_blindada_fix.py` | `cbc760610edb5ee24f54204e5eacc0374c14af2f037de0bde259a1c98aad6cf7` | `dddf92fe3ba8a940b9009096aa83b281cdbe6282a95bd1547a8e8651922e6af9` | code digest `0381e2869cd92c561f3754077a09a2a5360e7cd270bb717e7c2243be2b36a0c5` |
| `scripts/training/08_resume_train.py` | `scripts/training/08_resume_train.py` | `03cf79182da8aceb08283bcd2e72071f9e75806157bbf795241e0a9b20605dd1` | `03cf79182da8aceb08283bcd2e72071f9e75806157bbf795241e0a9b20605dd1` | byte-identical |
| `src/__init__.py` | `src/__init__.py` | `695b5a6c3804a6be29db56462fa1ca824a0cf65bd52c6c93cd80d653444ab8a0` | `695b5a6c3804a6be29db56462fa1ca824a0cf65bd52c6c93cd80d653444ab8a0` | byte-identical |
| `src/baselines/__init__.py` | `src/baselines/__init__.py` | `6d9ffab321552bd2c0c21148d55ad1a8be46df3bf5e8058d13096cd299f03e0a` | `6d9ffab321552bd2c0c21148d55ad1a8be46df3bf5e8058d13096cd299f03e0a` | byte-identical |
| `src/baselines/baseline_runner.py` | `src/baselines/baseline_runner.py` | `ca1d3a27d1a63b43a9306b204c034c47679b1acaa3aa9e4b6a60c465712ad7b2` | `ca1d3a27d1a63b43a9306b204c034c47679b1acaa3aa9e4b6a60c465712ad7b2` | byte-identical |
| `src/baselines/export_baseline_to_geotiff.py` | `src/baselines/export_baseline_to_geotiff.py` | `941b6f142a51582669d2e004e4991884beae15f39b66fdb3588d5cfd3f80c764` | `941b6f142a51582669d2e004e4991884beae15f39b66fdb3588d5cfd3f80c764` | byte-identical |
| `src/baselines/mlp_baseline.py` | `src/baselines/mlp_baseline.py` | `7a8759b54d3325684b1307c745334effe8872598ddd05e50d057adf688e8883b` | `7a8759b54d3325684b1307c745334effe8872598ddd05e50d057adf688e8883b` | byte-identical |
| `src/baselines/random_forest_baseline.py` | `src/baselines/random_forest_baseline.py` | `f6a00977b4877f902c2c07016f7f1b554594f67c90ba8022d5443cdbcab49f66` | `f6a00977b4877f902c2c07016f7f1b554594f67c90ba8022d5443cdbcab49f66` | byte-identical |
| `src/baselines/rule_based_baseline.py` | `src/baselines/rule_based_baseline.py` | `0d8d6d3f79140e7ee7c0f1c161386316a019ed583a336321b6ae4e00db023535` | `0d8d6d3f79140e7ee7c0f1c161386316a019ed583a336321b6ae4e00db023535` | byte-identical |
| `src/data_processing/__init__.py` | `src/data_processing/__init__.py` | `e816d8d3f639d3b1890e897116f036926acfbf9bdba920153aa2093527a12d55` | `e816d8d3f639d3b1890e897116f036926acfbf9bdba920153aa2093527a12d55` | byte-identical |
| `src/data_processing/data_validator.py` | `src/data_processing/data_validator.py` | `7ff93027244aee0cd893f69a1d099bb1326d9c7b6f7abebb03326bfca047738f` | `7ff93027244aee0cd893f69a1d099bb1326d9c7b6f7abebb03326bfca047738f` | byte-identical |
| `src/data_processing/dataset_loader.py` | `src/data_processing/dataset_loader.py` | `171a43f797a1e8e70ac1a4e11900877f879edf81ceacbe6189ef2afd52084a9f` | `171a43f797a1e8e70ac1a4e11900877f879edf81ceacbe6189ef2afd52084a9f` | byte-identical |
| `src/data_processing/feature_extractor.py` | `src/data_processing/feature_extractor.py` | `2004989042f45bcf0f9df72c08566cbff0a1f22399ee68b1c5368e950632f30b` | `2004989042f45bcf0f9df72c08566cbff0a1f22399ee68b1c5368e950632f30b` | byte-identical |
| `src/graph_construction/__init__.py` | `src/graph_construction/__init__.py` | `2e36aaf80a507472a495b3dc9b1a1d251421936e9a0ad64de52e219bbfc5a409` | `2e36aaf80a507472a495b3dc9b1a1d251421936e9a0ad64de52e219bbfc5a409` | byte-identical |
| `src/graph_construction/graph_integrator.py` | `src/graph_construction/graph_integrator.py` | `f64bdb254488fd58c760ed91d3c4004cbb5ebbb01bd4f17a0868536b4f8abdc2` | `f64bdb254488fd58c760ed91d3c4004cbb5ebbb01bd4f17a0868536b4f8abdc2` | byte-identical |
| `src/graph_construction/spatial_splitter.py` | `src/graph_construction/spatial_splitter.py` | `bfef6c0a0947b3ee666170e46be539c9ff9e929fb36e5823c5a8d53f11497f49` | `bfef6c0a0947b3ee666170e46be539c9ff9e929fb36e5823c5a8d53f11497f49` | byte-identical |
| `src/label_generation/__init__.py` | `src/label_generation/__init__.py` | `6a1f4296852aef46b16ae861ee3af8cad4a805c67c11c2029d5c80625f359908` | `6a1f4296852aef46b16ae861ee3af8cad4a805c67c11c2029d5c80625f359908` | byte-identical |
| `src/label_generation/dameplan_rules.py` | `src/label_generation/dameplan_rules.py` | `d3b0fe0f4f70530ee1aa06709d384015385a8f958c3b77178f3f5a3be486cf6f` | `d3b0fe0f4f70530ee1aa06709d384015385a8f958c3b77178f3f5a3be486cf6f` | byte-identical |
| `src/label_generation/label_generator.py` | `src/label_generation/label_generator.py` | `c11e69ecde84f3c294f10c038477b39f86602edce9ae0237c1a08358c2802ed6` | `c11e69ecde84f3c294f10c038477b39f86602edce9ae0237c1a08358c2802ed6` | byte-identical |
| `src/label_generation/label_validator.py` | `src/label_generation/label_validator.py` | `12447124925da3134ad02829f190157a7818aa4bf92b3822ed2f4fdfefa41cf4` | `12447124925da3134ad02829f190157a7818aa4bf92b3822ed2f4fdfefa41cf4` | byte-identical |
| `src/models/__init__.py` | `src/models/__init__.py` | `666d7caae63322c9281f5a0f7114459ae6f37adf3e2d348947ec17b91a973012` | `666d7caae63322c9281f5a0f7114459ae6f37adf3e2d348947ec17b91a973012` | byte-identical |
| `src/models/dameplan_loss.py` | `src/models/dameplan_loss.py` | `224caefcec8ee0d67755481bd6d69bd0edd6f7b5961c26a5e7f3c9646eb2da2c` | `224caefcec8ee0d67755481bd6d69bd0edd6f7b5961c26a5e7f3c9646eb2da2c` | byte-identical |
| `src/models/focal_loss.py` | `src/models/focal_loss.py` | `5e65f4bfc2ae5a19a3497fdd23a199f4a7bfe9f820352049e5cec9743de09b32` | `5e65f4bfc2ae5a19a3497fdd23a199f4a7bfe9f820352049e5cec9743de09b32` | byte-identical |
| `src/models/movement_gnn.py` | `src/models/movement_gnn.py` | `26e8bca925c8367f5b0490271124f65254f67155773e9230aa105ccaa3e5ac39` | `26e8bca925c8367f5b0490271124f65254f67155773e9230aa105ccaa3e5ac39` | byte-identical |
| `src/paths.py` | `src/paths.py` | `f27d09614ffe5820c0a5f4fa43005ffdfb2d2e1f665a6fb060a11647986db211` | `2ae98cd43b8a87d87d30571582ded6c40ebffae2e2e31abdeaca0ba8848d7105` | code digest `25bb08e5e95ae6efd5f4b383f155b492ee7d3eadefbd7ae6276334e7b73af65c` |
| `src/training/__init__.py` | `src/training/__init__.py` | `f0a39d473aa0958244cf555a12b8a2823aab363f55a2d1347fd46f36c7e40359` | `f0a39d473aa0958244cf555a12b8a2823aab363f55a2d1347fd46f36c7e40359` | byte-identical |
| `src/training/early_stopping.py` | `src/training/early_stopping.py` | `19d9530c41048fc2cbf8e6ab9b5be258c844edac0e876bb02d3b93219de60452` | `19d9530c41048fc2cbf8e6ab9b5be258c844edac0e876bb02d3b93219de60452` | byte-identical |
| `src/training/trainer.py` | `src/training/trainer.py` | `2e5a739688cde45fd835a6d5f8eb259aecd3ef9dd6b143527765aab8ebd42193` | `2e5a739688cde45fd835a6d5f8eb259aecd3ef9dd6b143527765aab8ebd42193` | byte-identical |
| `train.py` | `train.py` | `a4f225894cd197386be6dca46b8a47f967441a54938f91fb93b6e9d30421bb62` | `a4f225894cd197386be6dca46b8a47f967441a54938f91fb93b6e9d30421bb62` | byte-identical |
| `verify_code.py` | n/a | n/a | `425eea5c1f7b3946661de340f686c0f92b2eacd9f8f3ffa6f9f90159a45b7fe5` | new file |
