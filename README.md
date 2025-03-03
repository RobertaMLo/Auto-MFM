# Cerebellar Mean Field v25 rev00

**Built on SNN awake v.0.5.0 (BSB version updated at Jan. 30th, 2025)**

## Description

This repository contains the implementation of the **Cerebellar Mean Field v25 rev00**, a computational model based on mean-field formalism presented in **Zerlaut et al., 2018, J Comput Neurosci**. The model is developed based on the methods presented in **Lorenzi et al., 2023, Plos Comp Bio** and update to reporduce the cerebellar dynamics tuned on awake states.

## Model Parameters

The parameters are derived following the same rationale used in **Lorenzi et al., 2023, Plos Comp Bio**. 
Further modifications were needed due to the awake-state of the SNN, i.e. a tuning of the granular layer parameters:  
reduction of 75% of Kgrc_goc;  
reduction of 50% of Kgoc_grc  
The following table summarizes the parameters used to derive the Mean Field (MF) configuration (see syn_and_connec_library.py, configuration: 'CRBL_CONFIG_20PARALLEL_wN_PLOS23_Kgocgrc_red')

### Granule Cells (GrC)
| Connection | K    | Q    | Tsyn | Erev  |
|------------|------|------|------|------|
| MF → GrC   | 4.00 | 0.23 | 1.90 | 0.00 |
| GrC → GrC  | 0.00 | 0.00 | 0.00 | 0.00 |
| GoC → GrC  | 1.75 | 0.36 | 4.50 | -80.0 |
| MLI → GrC  | 0.00 | 0.00 | 0.00 | 0.00 |
| PC → GrC   | 0.00 | 0.00 | 0.00 | 0.00 |

### Golgi Cells (GoC)
| Connection | K     | Q    | Tsyn | Erev  |
|------------|------|------|------|------|
| MF → GoC   | 35.00 | 0.24 | 5.00 | 0.00 |
| GrC → GoC  | 132.50 | 0.437 | 1.25 | 0.00 |
| GoC → GoC  | 20.00 | 1.12 | 5.00 | -80.0 |
| MLI → GoC  | 0.00  | 0.00 | 0.00 | 0.00 |
| PC → GoC   | 0.00  | 0.00 | 0.00 | 0.00 |

### Molecular Layer Interneurons (MLI)
| Connection | K     | Q     | Tsyn | Erev  |
|------------|------|------|------|------|
| MF → MLI   | 0.00 | 0.00  | 0.00 | 0.00 |
| GrC → MLI  | 272.0 | 0.15  | 0.64 | 0.00 |
| GoC → MLI  | 0.00  | 0.00  | 0.00 | 0.00 |
| MLI → MLI  | 15.66 | 0.531 | 2.00 | -80.0 |
| PC → MLI   | 0.00  | 0.00  | 0.00 | 0.00 |

### Purkinje Cells (PC)
| Connection | K     | Q     | Tsyn | Erev  |
|------------|------|------|------|------|
| MF → PC    | 0.00 | 0.00  | 0.00 | 0.00 |
| GrC → PC   | 392.0 | 0.275 | 3.50 | 0.00 |
| GoC → PC   | 0.00  | 0.00  | 0.00 | 0.00 |
| MLI → PC   | 7.12  | 0.60  | 4.67 | -80.0 |
| PC → PC    | 0.00  | 0.00  | 0.00 | 0.00 |

**Note:** The standard Q value for MLI → PC in this configuration is 0.60, but previous tests indicate that a critical transition in system stability may occur between 0.68 and 0.97.

## License
By using this framework, you agree to collaborate with R.M Lorenzi, M. De Grazia, F. Palesi, C. Casellato and E. D'Angelo and acknowledge their contribution.
Anyone using this framework must cite the following paper:  

**Lorenzi et al., 2023, PLOS Computational Biology, doi:https://doi.org/10.1371/journal.pcbi.1011434** 

## Contact

For any inquiries, please contact Roberta M. Lorenzi at robertamaria.lorenzi01@universitadipavia.it.
