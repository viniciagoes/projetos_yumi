# Projetos Yumi

I'm using this repo to help my girlfriend with whatever scripts she needs for better executing her job at her company, feel free to use the scripts any way you want

### city_names_fixer.py

Usage:
```
python city_names_fixer.py my_file.xlsx
```

(For Brazil 🇧🇷)
(Don't forget to install the libraries 😉)

For this script, it uses the IBGE API to get the correct names for all the cities documented in Brazil. It opens an excel file with two columns:

| CIDADE | ESTADO |
|--------|--------|

Then, gets all unique values from the column ESTADO (en: states), for each one, request the official list of cities. For each city in the sheet, remove any special characters known to happen and get the closest match.

The new sheet has a new column, in the format:

| CIDADE | ESTADO | CIDADE_FIX|
|--------|--------|--------|

Finally, the new dataframe is exported in the same file.