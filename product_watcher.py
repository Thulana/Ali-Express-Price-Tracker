import requests
import time
import smtplib, ssl
import json

csv_file = ''
smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = ''
password = ''
email_msg = "Subject: {subject}\n\n{body}"
recurrent_time = 300  # in seconds


# Create a secure SSL context
# context = ssl.create_default_context()


# Try to log in to server and send email
def login_to_gmail():
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()
        server.starttls()
        server.login(sender_email, password)
        return server
    except Exception as e:
        # Print any error messages to stdout
        print(e)


# read csv for products to watch on and return list of data
def read_csv(file_name):
    data = []
    with open(file_name) as input_file:
        index = 1
        for line in input_file:
            if index is not 1:
                data.append(line.strip().split(','))
            index += 1
    return data


# For the given product fetch current price
def get_current_price(url):
    response = requests.get(url)
    json_str = response.text.split('var GaData = ')[1].split('var PAGE_TIMING =')[0].strip()[:-1]
    str_price = json_str.split('totalValue: ')[1].split('}')[0].strip()
    price = float(str_price.split('$')[1][:-1].replace(',', ''))
    return price


# watch products for price reductions and notify
def watch_products(data_list):
    for data in data_list:
        # fetch current price for the product
        price = get_current_price(data[0])
        # check if current price is lower than expected price
        if price < float(data[1]):
            print('Price reduced product found')
            subject = 'product price reduced below threshold'
            msg = 'Product in url ' + data[0] + ' has gone down than your expected price to value $' + str(price)
            email_content = email_msg.format(subject=subject, body=msg)
            email_server.sendmail(sender_email, data[2], email_content)
        time.sleep(2)
    time.sleep(recurrent_time)


if __name__ == '__main__':

    with open('config.json') as config_file:
        config = json.load(config_file)
    recurrent_time = config['recurrent_time']
    sender_email = config['gmail']['email']
    password = config['gmail']['password']
    csv_file = config['csv_file']
    # get products in csv
    data_list = read_csv(csv_file)
    # login to email
    email_server = login_to_gmail()

    while True:
        watch_products(data_list)
