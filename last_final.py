from flask import Flask, render_template,request,session,flash
import sqlite3 as sql
import os
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time
import sys
import pandas as pd
from tkinter import *
from bs4 import BeautifulSoup
import requests
from difflib import get_close_matches
import webbrowser
from collections import defaultdict
import random
options = webdriver.FirefoxOptions()
import telepot


token = '5783448314:AAH8GvDmkNXdrG2p4QMxhy-ZF2k2fVoqDTQ' # telegram token
receiver_id = 1724091177 # https://api.telegram.org/bot<TOKEN>/getUpdates


bot = telepot.Bot(token)
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/gohome')
def homepage():
    return render_template('index.html')

@app.route('/enternew')
def new_user():
   return render_template('signup.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            nm = request.form['Name']
            phonno = request.form['MobileNumber']
            email = request.form['email']
            unm = request.form['Username']
            passwd = request.form['password']
            with sql.connect("agricultureuser.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO agriuser(name,phono,email,username,password)VALUES(?, ?, ?, ?,?)",(nm,phonno,email,unm,passwd))
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("result.html", msg=msg)
            con.close()

@app.route('/userlogin')
def user_login():
   return render_template("login.html")

@app.route('/logindetails',methods = ['POST', 'GET'])
def logindetails():
    if request.method=='POST':
            usrname=request.form['username']
            passwd = request.form['password']

            with sql.connect("agricultureuser.db") as con:
                cur = con.cursor()
                cur.execute("SELECT username,password FROM agriuser where username=? ",(usrname,))
                account = cur.fetchall()

                for row in account:
                    database_user = row[0]
                    database_password = row[1]
                    if database_user == usrname and database_password==passwd:
                        session['logged_in'] = True
                        return render_template('home.html')
                    else:
                        flash("Invalid user credentials")
                        return render_template('login.html')

@app.route('/predictinfo')
def predictin():
   return render_template('info.html')



@app.route('/predict',methods = ['POST', 'GET'])
def predcrop():
    if request.method == 'POST':


        def flip_rate(key):
            home = 'https://www.flipkart.com'
            url12 = 'https://www.flipkart.com/search?q=' + str(
                key) + '&marketplace=FLIPKART&otracker=start&as-show=on&as=off'

            source_code = requests.get(url12)
            soup = BeautifulSoup(source_code.text, "html.parser")
            # print('soup',soup)
            for block in soup.find_all('div', {'class': '_2kHMtA'}):
                title, price, link = None, 'Currently Unavailable', None
                feature12 = None
                for heading in block.find_all('div', {'class': '_4rR01T'}):
                    title = heading.text
                for p in block.find_all('div', {'class': '_30jeq3 _1_WHN1'}):
                    price = p.text[1:]
                for pp in block.find_all('div', {'class': '_3k-BhJ-'}):
                    feature12 = pp.text[:]
                # specs = item.findAll('li', attrs={'class': 'tVe95H'})
                for l in block.find_all('a', {'class': '_1fQZEK'}):
                    link = home + l.get('href')
                    # map[title] = [price, link]
            #print(title)
            #print(price)
            #print(feature12)
            #print(link)
            item = soup
            model = item.find('div', {'class': "_4rR01T"}).text
            # Extracting Stars from 1st card
            star = item.find('div', {'class': "_3LWZlK"}).text
            # Extracting Number of Ratings from 1st card
            num_ratings = item.find('span', {'class': "_2_R_DZ"}).text.replace('\xa0&\xa0', " ; ")[
                          0:item.find('span', {'class': "_2_R_DZ"}).text.replace('\xa0&\xa0', " ; ").find(';')].strip()
            # Extracting Number of Reviews from 1st card
            reviews = item.find('span', {'class': "_2_R_DZ"}).text.replace('\xa0&\xa0', " ; ")[
                      item.find('span', {'class': "_2_R_DZ"}).text.replace('\xa0&\xa0', " ; ").find(';') + 1:].strip()
            # Extracting RAM from the 1st card
            ram = item.find('li', {'class': "rgWa7D"}).text[0:item.find('li', {'class': "rgWa7D"}).text.find('|')]
            # Extracting Storage/ROM from 1st card
            storage = item.find('li', {'class': "rgWa7D"}).text[
                      item.find('li', {'class': "rgWa7D"}).text.find('|') + 1:][0:10].strip()
            # Extracting whether there is an option of expanding the storage or not
            expandable = item.find('li', {'class': "rgWa7D"}).text[
                         item.find('li', {'class': "rgWa7D"}).text.find('|') + 1:][13:]
            # Extracting the display option from the 1st card
            display = item.find_all('li')[1].text.strip()
            # Extracting camera options from the 1st card
            camera = item.find_all('li')[2].text.strip()
            # Extracting the battery option from the 1st card
            battery = item.find_all('li')[3].text
            # Extracting the processir option from the 1st card
            processor = item.find_all('li')[4].text.strip()
            # Extracting Warranty from the 1st card
            warranty = item.find_all('li')[-1].text.strip()
            # Extracting price of the model from the 1st card
            price = item.find('div', {'class': '_30jeq3 _1_WHN1'}).text
            result = (
            ram, storage, expandable, display, camera, battery, processor)
            print('result', result)
            return title, price, link, result

        def amaz_rate(key):
            url_amzn = 'https://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=' + str(key)

            # Faking the visit from a browser
            headers = {
                'authority': 'www.amazon.com',
                'pragma': 'no-cache',
                'cache-control': 'no-cache',
                'dnt': '1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'sec-fetch-site': 'none',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-dest': 'document',
                'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            }

            map = defaultdict(list)
            home = 'https://www.amazon.in'
            # proxies_list = ["128.199.109.241:8080", "113.53.230.195:3128", "125.141.200.53:80", "125.141.200.14:80",
            # "128.199.200.112:138", "149.56.123.99:3128", "128.199.200.112:80", "125.141.200.39:80",
            # "134.213.29.202:4444"]
            # proxies = {'https': random.choice(proxies_list)}
            source_code = requests.get(url_amzn, headers=headers)
            plain_text = source_code.text
            count1 = 0
            count2 = 0
            count3 = 0
            # opt_title = StringVar()
            soup = BeautifulSoup(plain_text, "html.parser")
            # print(soup)
            # print(soup.find_all('div', {'class': 'sg-col-inner'}))
            for html in soup.find_all('div', {'class': 'sg-col-inner'}):
                count3 = count3 + 1
                #print('count3', count3)
                if count3 > 3:
                    break
                title, link, price = None, None, None
                for heading in html.find_all('span', {'class': 'a-size-medium a-color-base a-text-normal'}):
                    count2 = count2 + 1
                    if count2 > 1:
                        break
                    #print('count2', count2)
                    title = heading.text
                    print(title)
                    am_title = heading.text

                for p in html.find_all('span', {'class': 'a-price-whole'}):
                    price = p.text

                    count1 = count1 + 1
                    if count1 > 1:
                        break
                    #print('count1', count1)
                    print(price)
                    am_price = price

                for l in html.find_all('a', {
                    'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}):
                    link = home + l.get('href')
                if title and link:
                    map[title] = [price, link]
                    print('link', link)
                    am_link = link
            return am_title, am_price, am_link
            # user_input = var.get().title()
            # matches_amzn = get_close_matches(user_input, list(map.keys()), 20, 0.01)
            looktable = {}

        def croma(itemName):
            itemName = itemName
            croma_base_url = 'https://www.croma.com'
            croma_url = f'https://www.croma.com/search/?text={itemName}'
            driver = webdriver.Firefox(
                executable_path="C:\\Users\katty\\Desktop\\Amazon-Flipkart-Price-Comparison-Engine-master\\new_main\\agri_last\\geckodriver.exe",
                options=options)
            headers = {
                'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'
            }

            driver.get(croma_url)

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # list of all the products on the newUrl
            pro_list = []
            pro = soup.findAll('div', class_='content-wrap')
            for j in pro:
                for i in j.findAll('ul', class_='product-list'):
                    #         print(i)
                    for k in i.findAll('li', class_='product-item'):
                        pro_list.append(k)

            try:
                prod = pro_list[0]

                imageTag = prod.find('div', class_='product-img')
                prodImage = imageTag.find('img')
                prodImageLink = prodImage['src']
                print("Image Link:", prodImageLink)

                atag = prod.h3.a
                prodLink = croma_base_url + atag['href']
                print("\nProduct Link:", prodLink)

                name = prod.h3.text
                print("Name:", name)

                cromaPrice = prod.find('span', class_='amount').text

                # append the price scraped in float form
                temp_pro_price = cromaPrice.replace("₹", "")
                final_pro_price = float(temp_pro_price.replace(",", ""))
                final_price_list.append(final_pro_price)

                print("\nPrice:", cromaPrice)
                #print("\n\n\nNow Let's scrape Ajio.........\n")
                #ajio(itemName)
            except:
                print("Product not found!")
                #print("\n\n\nNow Let's scrape Ajio.........\n")
                #ajio(itemName)

            return name, cromaPrice, prodLink

        comment2 = request.form['comment2']
        key = comment2
        [title, price, link, result]=flip_rate(key)
        [am_title, am_price, am_link]=amaz_rate(key)
        [cr_title, cr_price, cr_link] = croma(key)

        ram, storage, expandable, display, camera, battery, processor = result
        '''
        if price < am_price and price < cr_price:
            bot.sendMessage(receiver_id, 'Lowest price for Selected Product click the link below')
            bot.sendMessage(receiver_id, link)
        elif am_price < cr_price:
            bot.sendMessage(receiver_id, 'Lowest price for Selected Product click the link below')
            bot.sendMessage(receiver_id, am_link)

        else:
            bot.sendMessage(receiver_id, 'Lowest price for Selected Product click the link below')
            bot.sendMessage(receiver_id, cr_link)
            '''





        return render_template('resultpred.html', prediction=title, price=price,
                               p1=ram, p2=storage, p3= expandable, p4=display,p5=camera,p6=battery,p7= processor,
                               prediction1=link, prediction2=am_title, price1=am_price,
                               prediction3=am_link, prediction4=cr_title, price2=cr_price, prediction5=cr_link)


        '''
        return render_template('resultpred.html', prediction=response, price=statistics.mean(Price_Crop88), prediction1=response2, price1=statistics.mean(Price_Crop99),
                               yeild88=statistics.mean(Yield_Crop88), yeild99 = statistics.mean(Yield_Crop99),
                               prediction2=pred[0], price2=statistics.mean(Price_Crop1), prediction3=pred[1],
                               price3=statistics.mean(Price_Crop2),yeild1 = statistics.mean(Yield_Crop1), yeild2 = statistics.mean(Yield_Crop2),
                               prediction4=pred1[0], price4=statistics.mean(Price_Crop4), yeild4 = statistics.mean(Yield_Crop4),
                               yeild5=statistics.mean(Yield_Crop5), prediction5=pred1[1],
                               price5=statistics.mean(Price_Crop5))
                               '''


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return render_template('login.html')

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)

