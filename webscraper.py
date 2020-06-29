from bs4 import BeautifulSoup as bs
import requests
import datetime
import mysql as mysql
import  mysql.connector
import os

mydb = mysql.connector.connect(
    host = "localhost", 
    user = "root",
    passwd = os.environ.get('MYSQL_PASSWORD'),
    database = "pcprices"
)

my_cursor = mydb.cursor()

now = datetime.datetime.now()

# requests links
source_cpu = requests.get('https://www.pccomponentes.com/amd-ryzen-7-3700x-36ghz-box').text
source_gpu = requests.get('https://www.pccomponentes.com/gigabyte-geforce-gtx-1660-super-oc-6gb-gddr6').text
#sour_cpu = requests.get('https://amzn.to/3eKMviR').text
#sour_gpu = requests.get('').text

soup_cpu = bs(source_cpu, 'lxml')
soup_gpu = bs(source_gpu, 'lxml')
#so_cpu = bs(sour_cpu, 'lxml')

# cpu pccomponentes.com
price = soup_cpu.find('div', class_='precioMain h1')
eur = price.find('span', class_='baseprice').text
cent = price.find('span', class_='cents').text

# gpu pccomponentes.com
priceg = soup_gpu.find('div', class_='precioMain h1')
eurg = priceg.find('span', class_='baseprice').text
centg = priceg.find('span', class_='cents').text

# cpu amazon.es
# gpu amazon.es

print(f'{now.year}-{now.month}-{now.day}') #day
print(f'{eur}{cent}')   #cpu
print(f'{eurg}{centg}')     #gpu

date1 = f'{now.year}-{now.month}-{now.day}'
cpu = f'{eur}{cent}'
gpu = f'{eurg}{centg}'

sql = "INSERT INTO price(day, cpu, gpu) VALUES (%s, %s, %s)"
data = (date1, cpu,  gpu)

my_cursor.execute(sql, data)
mydb.commit()