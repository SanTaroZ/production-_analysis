# Production Analysis 

By: Your name (or your organization/company/team).

Version: 0.1

A short description of the project.


## Create environment

```bash
conda env create -f environment.yml
activate production_analysis
```

or 

```bash
mamba env create -f environment.yml
activate production_analysis
```

## Project organization

    production_analysis
        ├── data
        │   ├── processed      <- The final, canonical data sets for modeling.
        │   └── raw            <- The original, immutable data dump.
        │
        ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
        │                         the creator's initials, and a short `-` delimited description, e.g.
        │                         `1.0-ecardenas-data-exploration`.
        │
        ├── .gitignore         <- Files to ignore by `git`.
        │
        ├── environment.yml    <- The requirements file for reproducing the analysis environment.
        │
        └── README.md          <- The top-level README for developers using this project.

---

This template serves as initial point for my data projects so i do not have to create a scenario from scratch every time i want to begin a project.