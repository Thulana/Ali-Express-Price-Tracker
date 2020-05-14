# Ali-Express-Price-Tracker

## How to run

* Add gmail address, password, csv file and the recurrent time delay in the config.json file

sample :

`{
  "csv_file": "products.csv",
  "recurrent_time": 300,
  "gmail": {
    "password": "password",
    "email": "email address"
  }
}`

* Execute the watcher like `python3 product_watcher.py`

