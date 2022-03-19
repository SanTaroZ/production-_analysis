# Production Analysis 

By: Edwin Carlos Cárdenas Sotomayor


Version: 2

## Automatization of reports to analyze and take decisions based on production reports of industrial equipment.

Background:

In our factory we have more than 50 industrial machines and more than 60 operators working 24 hours a day and seven days a week. All the information about production, scrap, who is the operator or even if the machine worked or not is registered in physical production reports that are delivered every day to a typist. The typist job is to register all in a excel sheet with table format.
Every day around 150 to 200 new reports are inserted getting around 5000 reports at the end of each month.


## General Objective:

    * 	Analyze the data in order to found information enough to allow us detect which machines have the lowest performance so, when repaired, have a high influence level in the global production, granting more benefits to the factory.
    
## Particular Objectives:

    *	To know the amount of day that each machine works every month
    *	To calculate the scrap generated for each machine related with its production and graph its tendency of the last 7 days.
    *	To calculate the scrap generated for each machine related with the total scrap produced in the factory and graph its tendency of the last 7 days.
    *	To cross information of the last two objectives in order to identify the most important machines to be repaired.
    *	To deliver the result of their work to the operators, which is the amount of scrap generated related to the production of their machines.



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
        │   ├── processed      <- The final, canonical data sets for modeling and results
        │   └── raw            <- The original, immutable data dump.
        │
        ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering) + `_` + description, e.g.
        │                         `1.0-data-exploration`.
        │
        ├── .gitignore         <- Files to ignore by `git`.
        │
        ├── environment.yml    <- The requirements file for reproducing the analysis environment.
        │
        └── README.md          <- The top-level README for developers using this project.



