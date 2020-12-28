# Arbitration Fee Calculator

A Django web app which lets one calculate arbitration fee 
(including arbitrators fee, administrative fee, registration 
fee and emergency arbitrator's fee) based on such parameters of
a dispute as amount in dispute, number of arbitrators, number 
of parties and type of procedure.

Availiable at https://www.arbitrationfee.com

### Main features
#### 15 algorithms to calculate fees
* in 12 arbitral institutions (international arbitration)
* in 3 arbitral institutions (domestic arbitration in Russia)

#### Auto-Rendering PDF chart with the results data
A pretty bar chart is automatically rendered as a PDF file 
to visually present the results data using matplotlib Python 
library. 

The PDF file is created in buffer and is avaliable for
download as user clicks on "Download PDF Chart" button
on results page.

#### Auto-Creating XLSX workbook with the results data
The results can also be downloaded as an Excel Workbook. 
The results data is collected to workbook using xlsxwriter 
Python library.

The XLSX file is created in buffer and is avaliable for
download as user clicks on "Download XLS Table" button
on results page.

#### Currency rates auto-updates
While International Arbitral Institutions set their fees 
in different currencies, all results are provided in USD 
for convenience.
To make correct exchange happen exchange rates are aquired 
*via* [Foreign exchange rates API](https://exchangeratesapi.io) 
in background every hour using Celery beat (Redis as broker).

## Installation

To run app locally one should 
* Clone the repository
```bash
git clone
```
* Install the dependencies (which are listed in 
the 'requirements.txt' file) in the working environment
```bash
pip install -r requirements.txt
```
* Set the environment variables
    * SECRET_KEY="[CREATE YOUR OWN SECRET KEY]"
    * DEBUG_VALUE="True"
    * REDIS_URL="redis://0.0.0.0:6379/0"
    * REDIS_HOST="0.0.0.0"
    * REDIS_PORT="6379"
    
* Migrate database (Sqlite3 engine is used for development)
 ```bash
python manage.py migrate
```
* Run Django server locally
 ```bash
python manage.py runserver
```
* Set up currency rate updates
    * Create Rate objects in admin panel or from shell
     ```bash
     python manage.py shell
  
     from calc.models import Rate
     USD_EUR = Rate(name="USD_EUR", rate=0)
     USD_EUR.save()
     EUR_USD = Rate(name="EUR_USD", rate=0)
     EUR_USD.save()
     USD_RUB = Rate(name="USD_RUB", rate=0)
     USD_RUB.save()
     RUB_USD = Rate(name="RUB_USD", rate=0)
     RUB_USD.save()
     USD_CNY = Rate(name="USD_CNY", rate=0)
     USD_CNY.save()
     CNY_USD = Rate(name="CNY_USD", rate=0)
     CNY_USD.save()
     USD_HKD = Rate(name="USD_HKD", rate=0)
     USD_HKD.save()
     HKD_USD = Rate(name="HKD_USD", rate=0)
     HKD_USD.save()
     USD_SGD = Rate(name="USD_SGD", rate=0)
     USD_SGD.save()
     SGD_USD = Rate(name="SGD_USD", rate=0)
     SGD_USD.save()
     USD_KRW = Rate(name="USD_KRW", rate=0)
     USD_KRW.save()
     KRW_USD = Rate(name="KRW_USD", rate=0)
     KRW_USD.save()      
     ```
    * Run Redis on Docker
    ```bash
     docker run -d -p 6379:6379 redis
     ```
    * Run Celery worker
     ```bash
     celery -A arbcalc worker -l INFO
     ```
    * Run Celery beat (in a new terminal window)
     ```bash
     celery -A arbcalc beat -l INFO
     ```
 
 #### P.S.
 CSS code is a mess in this project (I just didn't care)
 but it works.
 
 Might you have any questions, please do not hesitate to contact 
 me *via* mrtnkrll@gmail.com.