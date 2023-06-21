gp27_techchallenge
==============================

Development of the phase 1 Tech Challenge @ Fiap

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io

Data Acquired
------------
- [Dados da Vitivinicultura](http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01) was indicated as main source of data;
- [WBPY](https://pypi.org/project/wbpy/) maybe can give us economics data
    - Was made from https://documents.worldbank.org/en/publication/documents-reports/api
    - Indicators in http://api.worldbank.org/v2/indicator
    - We've acquired 'inflation consumer prices', 'gini index','number of procedures to register business','logistics performance index','domestic credit to private sector' and 'population growth'
- [NOAA global historical climatology network (daily)](https://www.kaggle.com/datasets/noaa/noaa-global-historical-climatology-network-daily), climate data from stations worldwide, where we use lat/long to normalize data to countries, and get the climatological data to compare with RS/Brazil data

Decisions around the process
------------
- We are using Country Code (in english) as a key to manipulate all the data;
- After recover and explored, the NOAA data, specifically Temperature (TMIN, TMAX, TAVG), was in Farenheidt; So, we apply an formula to generate Celsius Degrees;
- After that, we have temperatures like -5000ºC, or more than 100ºC; when the temperature was > 57ªC (highest temperature, found in Death Valley, CA, USA) and < -90 (lowest temperature, in Antarctica), we put a nan in it, and imput the mean of the value in this place, after;
- We've filtered this database with the lowest year as 1970, because it is the lowest year in wine data;

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
