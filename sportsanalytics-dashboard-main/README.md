# sportsanalytics-dashboard

## (1) Create .env file in root directory
Create this `.env` file or rename the file `example.env.txt` to `.env` and change the values.
```bash
DATABASE_FILE=fit_database.db
DEBUG=False
WEIGHT=75
```
## (2) Install the requirements `requirements.txt`
### Linux/Mac
```bash
./venv/bin/pip install -r requirements.txt
```
### Windows
```shell
venv/Scripts/pip.exe install -r requirements.txt
```
## (3) Create and import database
### Linux/Mac
```bash
./venv/bin/python import.py
```
### Windows
```shell
venv/Scripts/python.exe import.py
```

## (4) Start Dashboard
### Linux/Mac
```bash
./venv/bin/python app.py
```
### Windows
```shell
venv/Scripts/python.exe app.py
```

------------------
## Build SASS (Linux/Mac only)
```bash
npm install -g sass
```

## Rebuild CSS (Linux/Mac only)
```bash
sass scss/dashboard.scss assets/dashboard.css
```
------------------
## Port is already in use: How to kill port
```bash
lsof -nti:8050 | xargs kill -9
```
## Kill port Windows
```shell
netstat -ano | findstr :8050
taskkill /PID <typeyourPIDhere> /F
```
