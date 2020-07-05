# NEM File Parser Python Framework

Nem provides a very convenient framework to read, process, ingest and browse energy consumption data provided in CSV format. The format of the data is defined by AEMO. 

## Installation

Download the package and install requirements

```sh
pip install -r requirements.txt
```


### Requirements

-   Python 3.6+
-   Django 3.0+
-   Sqlite3

## Usage

#### To read a NEM13 file 

```sh
python manage.py readnem -a path/to/nem13.csv
```

#### To run Django server

```sh
python manage.py runserver 8000
```

#### To browse ingested data 

1. Create a superuser
```sh
python manage.py createsuperuser
```
2. Navigate to 127.0.0.1:8000/admin to log in and start browsing

### Ingestion Policy

NemParser has a strict data ingestion policy: only non-corrupted NEM file shall be imported into the database. It means that if the parser finds any errors during the process, either from the row or the field, it will not save the data into the database. It will log the errors in two tables ReaderError and NemFileError. This will help avoid having to cleaning up the data when one or more rows have been incorrect or corrupted. 

### Error Handling

If there is an error occurs during the parsing process, the file's data shall not be ingested into the database, and the ReaderRun table shall record an Failed run of the file. This is to make sure that only proper data are imported and no file is ingested twice.