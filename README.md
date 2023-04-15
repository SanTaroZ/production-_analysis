# Production Analysis 

By: Edwin Carlos Cárdenas Sotomayor


<<<<<<< HEAD
Version: 2.0
=======
Version: 2
>>>>>>> 3373b86a3ee74a35d5547ef2e5e2e69e29dafd5b

## Automatization process for analyze and take decisions based on production reports of industrial equipment.

Background:

In our factory we have more than 50 industrial machines and more than 60 operators working 24 hours a day and seven days a week. All the information about production, scrap, who is the operator or even if the machine worked or not is registered in physical production reports that are delivered every day to a typist. The typist job is to register all in a excel sheet with table format.
Every day around 150 to 200 new reports are inserted getting around 5000 reports at the end of each month.


## General Objective:

    * 	Analyze the data in order to detect which machines have the lowest performance, act according it and improve the performance of the factory in general.
    
## Particular Objectives:

    *	Know the amount of day that each machine works every month
    *	Calculate the scrap generated for each machine related with its production and graph its tendency.
    *	Cross information in order to identify the most important machines to be repaired.
    *	Deliver the result of their work to the operators, which is the amount of scrap generated related to the production of their machines.
    *   Create historical data to compare the past with the present and stalibsh future goals.



## Project organization

    production_analysis
        ├── data
        │   ├── processed      <- The final, canonical data sets for modeling and results
        │   └── raw            <- The original, immutable data dump.
        │
        ├── __main.py__        <- Python file with the program.
        │
        ├── .gitignore         <- Files to ignore by `git`.
        │
        ├── environment.yml    <- The requirements file for reproducing the program.
        │
        └── README.md          <- Information about this project.



