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

### Handling exceptions
