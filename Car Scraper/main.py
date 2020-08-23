from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
from tkinter import *
from bs4 import BeautifulSoup
import requests
import mysql.connector
import xlwt
from xlwt import Workbook
import os, errno
from requests_html import HTMLSession
import threading

background_color = '#424242'
PATH = "chromedriver.exe"
MIN_PRICE = 1500

class Frames:
    def __init__(self, master, website_name, mydb, my_cursor):
        global background_color
        self.mydb = mydb
        self.mycursor = my_cursor
        x = 0
        self.master = master
        self.website_name = website_name
        self.label_box = Label(self.master, text = self.website_name, bg = background_color, fg = 'white', font = ('Calibri', 12))
        self.label_box.config(borderwidth = 2, relief="ridge", padx = 10)
        self.label_box.place(relx=0.5, y = 10, anchor=N)
        self.name_label = Label(self.master, text = 'Marca:', bg = background_color, fg = 'white')
        self.name_label.place(x = 0+x, y = 70)
        self.entry1 = Entry(self.master, width = 15)
        self.entry1.place(x = 50+x, y = 70)
        self.model_label = Label(self.master, text = 'Model:', bg = background_color, fg = 'white')
        self.model_label.place(x = 175+x, y = 70)
        self.entry2 = Entry(self.master, width = 15)
        self.entry2.place(x = 225+x, y = 70)
        self.FabYear_Label = Label(self.master, text = 'Anul Fabricatiei:', bg = background_color, fg = 'white')
        self.FabYear_Label.place(x = 350+x, y = 70)
        self.entry3 = Entry(self.master, width = 15)
        self.entry3.place(x = 450+x, y = 70)
        self.Km_Label = Label(self.master, text = 'Rulaj pana la:', bg = background_color, fg = 'white')
        self.Km_Label.place(x = 575+x, y = 70)
        self.entry4 = Entry(self.master, width = 15)
        self.entry4.place(x = 665+x, y = 70)
        self.Fuel_Label = Label(self.master, text = 'Combustibil:', bg = background_color, fg = 'white')
        self.Fuel_Label.place(x = 445, y = 100)
        self.checkbutton1 = IntVar()
        self.Petrol = Checkbutton(self.master, variable = self.checkbutton1, onvalue=1, offvalue=0, bg=background_color,
                                  activebackground=background_color, fg='black', activeforeground='black')
        self.Petrol.place(x=445, y=130)
        self.Petrol_Label = Label(self.master, text='Benzina', bg=background_color, fg='white')
        self.Petrol_Label.place(x=465, y=132)
        self.checkbutton2 = IntVar()
        self.Diesel = Checkbutton(self.master, variable = self.checkbutton2, onvalue=1, offvalue=0, bg=background_color,
                                  activebackground=background_color, fg='black', activeforeground='black')
        self.Diesel.place(x=445, y=160)
        self.Diesel_Label = Label(self.master, text='Diesel', bg=background_color, fg='white')
        self.Diesel_Label.place(x=465, y=162)

        self.MaxPrice_Label = Label(self.master, text = 'Pret maxim:', bg = background_color, fg = 'white')
        self.MaxPrice_Label.place(x = 790+x, y = 70)
        self.entry5 = Entry(self.master, width = 15)
        self.entry5.place(x = 875+x, y = 70)

        self.mysql_insert_query = """INSERT INTO car_list (Titlu, Pret, An, Kilometraj, Combustibil, Culoare, Link, p) 
                                           VALUES 
                                           (%s, %s, %s, %s, %s, %s, %s, %s)"""


    def List_in_DB(self, All_Cars, title, price, car_link, color, fuel_type, fab_year, mileage, p):
        for car in All_Cars:
            if car[7] == car_link:
                if car[2] != price:
                    sql = "UPDATE car_list SET Pret = %s WHERE id = %s"
                    sql2 = "UPDATE car_list SET p = %s WHERE id = %s"
                    self.mycursor.execute(sql, (car[2], car[0]))
                    self.mycursor.execute(sql2, (p, car[0]))
                return

        tuple = (title.strip(), price.strip(), fab_year.strip(), mileage.strip(), fuel_type.strip(), color.strip(), car_link.strip(), p)
        self.mycursor.execute(self.mysql_insert_query, tuple)
        self.mydb.commit()


    def search_on_MD(self, All_Cars):
        entrybox = ''
        entrybox = self.entry1.get()
        if entrybox:
            entrybox = entrybox.lower()
            if entrybox == 'bmw':
                entrybox = entrybox.upper()
            else:
                entrybox = entrybox[0].upper() + entrybox[1:]
            global PATH
            driver = webdriver.Chrome(PATH)
            driver.get('https://suchen.mobile.de/fahrzeuge/search.html?lang=en')
            try:
                time.sleep(3)
                driver.find_element_by_id('gdpr-consent-accept-button').click()
            except:
                pass
            carmaker_slider = Select(driver.find_element_by_id('selectMake1-ds'))
            carmaker_slider.select_by_visible_text(entrybox)
            entrybox = self.entry2.get()
            if entrybox:
                ok = 1
                for c in entrybox:
                    if c.isdigit() == True:
                        entrybox = '    ' + entrybox
                        ok = 0
                        break
                if ok:
                    entrybox = entrybox.strip()
                model = Select(driver.find_element_by_id('selectModel1-ds'))
                model.select_by_visible_text(entrybox)
            entrybox = self.entry3.get()
            if entrybox:
                driver.find_element_by_id('minFirstRegistrationDate').send_keys(entrybox)
            entrybox = self.entry4.get()
            if entrybox:
                driver.find_element_by_id('maxMileage').send_keys(entrybox)
            entrybox = self.entry5.get()
            if entrybox:
                driver.find_element_by_id('maxPrice').send_keys(entrybox)
            #self.checkbutton1 = self.checkbutton1.get()
            #print(str(self.checkbutton2.get()))
            if self.checkbutton1.get():
                driver.find_element_by_id('fuels-PETROL-ds').click()
            #self.checkbutton2 = self.checkbutton2.get()
            #print(str(self.checkbutton2.get()))
            if self.checkbutton2.get():
                driver.find_element_by_id('fuels-DIESEL-ds').click()
            driver.find_element_by_id('dsp-upper-search-btn').click()
            time.sleep(5)
            sort_slider = Select(driver.find_element_by_id('so-sb'))
            sort_slider.select_by_visible_text('Price ascending')
            time.sleep(5)
            try:
                driver.find_element_by_id('rbt-p-2').click()
            except:
                driver.find_element_by_id('sticky-billboard__close btn--close btn--icon-grey-80').click()
                driver.find_element_by_id('rbt-p-2').click()
            url = driver.current_url
            seq = 'pageNumber=2'
            n = len(url)
            for i in range(0, n, 1):
                ok = 1
                for j in range(i, n, 1):
                    if j - i > 11:
                        break
                    # print(str(j) + ' ' + str(i))
                    if seq[j - i] != url[j]:
                        ok = 0
                        break
                if ok:
                    part2 = url[(i + 12):]
                    part1 = url[:i]
                    break
            seq = 'pageNumber='
            page = 1
            title = ''
            price = ''
            car_link = ''
            color = ''
            fuel_type = ''
            fab_year = ''
            mileage = ''
            while True:
                link = part1 + seq + str(page) + part2
                driver.get(link)
                HTML = driver.execute_script('return document.documentElement.outerHTML')
                Soup = BeautifulSoup(HTML, 'html.parser')
                cars = Soup.find_all(class_='link--muted no--text--decoration result-item', href = True)
                if len(cars) == 0:
                    break
                for car in cars:
                    car_link = car['href']
                    driver.get(car_link)
                    html = driver.execute_script('return document.documentElement.outerHTML')
                    soup = BeautifulSoup(html, 'html.parser')
                    price = soup.find(class_='h3 rbt-prime-price').text
                    title = soup.find(class_='g-col-7').text
                    mileage = soup.find(id = 'rbt-mileage-v').text
                    fuel_type = soup.find(id = 'rbt-fuel-v').text
                    fab_year = soup.find(id = 'rbt-firstRegistration-v').text
                    try:
                        color = soup.find(id = 'rbt-color-v').text
                    except:
                        pass
                    if price is not None:
                        p = 0
                        for c in price:
                            if c.isdigit() == True:
                                p = p * 10 + int(c)
                        if p > MIN_PRICE:
                            self.List_in_DB(All_Cars, title, price, car_link, color, fuel_type, fab_year, mileage, p)
                        print(p)
                page += 1
            print('done')





    def search_on_OLX(self, All_Cars):
        try:
            Max_Price = int(self.entry5.get())
        except ValueError:
            Max_Price = 1000000000
        entrybox = ''
        ok = 0
        entrybox = self.entry1.get()
        if entrybox:
            link = 'https://www.olx.ro/auto-masini-moto-ambarcatiuni/autoturisme/'
            entrybox = entrybox.lower()
            link = link + entrybox + '/'
            entrybox = ''
            entrybox = self.entry2.get().lower()
            if entrybox:
                link = link + entrybox + '/'
            entrybox = ''
            entrybox = str(self.entry3.get())
            if entrybox:
                link = link + '?search[filter_float_year%3Afrom]=' + str(entrybox)
                ok = 1
            entrybox = ''
            entrybox = self.entry4.get()
            if entrybox:
                if not ok:
                    link = link + '?search[filter_float_rulaj_pana%3Ato]=' + str(entrybox)
                    ok = 1
                else:
                    link = link + '&search[filter_float_rulaj_pana%3Ato]=' + str(entrybox)
            if self.checkbutton1 and self.checkbutton2:
                if not ok:
                    link = link + '?search[filter_enum_petrol][0]=petrol&search[filter_enum_petrol][1]=diesel'
                    ok = 1
                else:
                    link = link + '&search[filter_enum_petrol][0]=petrol&search[filter_enum_petrol][1]=diesel'
            elif self.checkbutton1:
                if not ok:
                    link = link + '?search[filter_enum_petrol][0]=petrol'
                    ok = 1
                else:
                    link = link + '&search[filter_enum_petrol][0]=petrol'
            else:
                if not ok:
                    link = link + '?search[filter_enum_petrol][0]=diesel'
                    ok = 1
                else:
                    link = link + '&search[filter_enum_petrol][0]=diesel'
            if not ok:
                link = link + '?search%5Border%5D=filter_float_price%3Aasc'
            else:
                link = link + '&search%5Border%5D=filter_float_price%3Aasc'
            link = link + '&page='
            repeat = 1
            page = 1
            title = ''
            price = ''
            car_link = ''
            color = ''
            fuel_type = ''
            fab_year = ''
            mileage = ''
            global MIN_PRICE
            while repeat:
                r = requests.get(link + str(page)).content
                soup = BeautifulSoup(r, 'html.parser')
                cars = soup.find_all('a', class_='marginright5 link linkWithHash detailsLink', href = True)


                for car in cars:
                    title = car.text
                    car_link = car['href']
                    req = requests.get(car_link).content
                    Soup = BeautifulSoup(req, 'html.parser')
                    boxes = Soup.find_all(class_='offer-details__item')
                    for box in boxes:
                        if box.find(class_='offer-details__name').text == 'An de fabricatie':
                            fab_year = box.find(class_='offer-details__value').text
                        if box.find(class_='offer-details__name').text == 'Rulaj':
                            mileage = box.find(class_='offer-details__value').text
                        if box.find(class_='offer-details__name').text == 'Combustibil':
                            fuel_type = box.find(class_='offer-details__value').text
                        if box.find(class_='offer-details__name').text == 'Culoare':
                            color = box.find(class_='offer-details__value').text
                    price = Soup.find(class_='offer-titlebox__price')
                    if price is not None:
                        price = price.text
                        p = 0
                        for c in price:
                            if c == '€':
                                break
                            if c.isdigit() == True:
                                p = p * 10 + int(c)
                        if p > Max_Price:
                            repeat = 0
                            break
                        if p > MIN_PRICE:
                            self.List_in_DB(All_Cars, title, price, car_link, color, fuel_type, fab_year, mileage, p)
                page += 1





class GUI:
    def __init__(self, root, mydb, my_cursor):
        global background_color
        self.mydb = mydb
        self.mycursor = my_cursor
        self.root = root
        self.root.geometry('1000x550')
        self.root.config(bg = background_color)
        self.MD_Frame = Frame(self.root, bg = background_color, borderwidth = 2, relief="ridge", padx = 10)
        self.MD_Frame.place(x = -1, y = 0, width = 1003, height = 230)
        self.OLX_Frame = Frame(self.root, bg = background_color, borderwidth = 2, relief="ridge", padx = 10)
        self.OLX_Frame.place(x = -1, y = 228, width = 1003, height = 230)
        self.MD_Label = Frames(self.MD_Frame, 'MOBILE.DE', self.mydb, self.mycursor)
        self.OLX_Label = Frames(self.OLX_Frame, 'OLX.RO', self.mydb, self.mycursor)
        self.clear_DataBase = Button(self.root, text = 'Goleste', bg = background_color, activebackground = background_color,
                                     relief = 'ridge', fg = 'white', activeforeground = 'white', width = 10, command = self.ClearDataBase)
        self.clear_DataBase.place(x = 350, y = 490)
        self.update_DataBase = Button(self.root, text = 'Actualizeaza', bg = background_color, activebackground = background_color,
                                     relief = 'ridge', fg = 'white', activeforeground = 'white', width = 10, command = self.UpdateDataBase)
        self.update_DataBase.place(x = 455, y = 490)
        self.export_DataBase = Button(self.root, text = 'Export', bg = background_color, activebackground = background_color,
                                     relief = 'ridge', fg = 'white', activeforeground = 'white', width = 10, command = self.ExportDataBase)
        self.export_DataBase.place(x = 560, y = 490)
    def ExportDataBase(self):
        filename = 'Masini.xls'
        try:
            os.remove(filename)
        except OSError:
            pass
        wb = Workbook()
        sheet = wb.add_sheet('Masini')
        sql_select_Query = "select * from car_list"
        self.mycursor.execute('SELECT * FROM car_list ORDER BY p ASC')
        All_Cars = self.mycursor.fetchall()
        query = ['Titlu', 'Pret', 'An', 'Kilometraj', 'Combustibil', 'Culoare', 'Link']
        for i in range(0, 7, 1):
            sheet.write(0, i, query[i])
        i = 1
        for car in All_Cars:
            for j in range(0, 7, 1):
                sheet.write(i, j, car[j+1])
            i += 1
        wb.save(filename)


    def ClearDataBase(self):
        self.mycursor.execute("TRUNCATE TABLE car_list")
    def Disable_Enable_Button(self, Thread1, Thread2):
        while Thread1.is_alive() or Thread2.is_alive():
            time.sleep(3)
        self.update_DataBase['state'] = NORMAL
    def UpdateDataBase(self):
        self.update_DataBase['state'] = DISABLED
        sql_select_Query = "select * from car_list"
        try:
            self.mycursor.execute(sql_select_Query)
        except:
            pass
        All_Cars = self.mycursor.fetchall()
        Thread1 = threading.Thread(target = self.MD_Label.search_on_MD, args = (All_Cars,))
        Thread2 = threading.Thread(target = self.OLX_Label.search_on_OLX, args = (All_Cars,))
        Thread1.start()
        Thread2.start()
        Thread3 = threading.Thread(target = self.Disable_Enable_Button, args=(Thread1, Thread2))
        Thread3.start()

if __name__ == '__main__':
    # here you have to enter your mysql user and password
    username = ''
    passwd = ''
    mydb = mysql.connector.connect(
        host="localhost",
        user=username,
        password=passwd,
        database="car_list"
    )
    my_cursor = mydb.cursor()
    root = Tk()
    root.title('Car Scraper')
    Icon = PhotoImage(file = 'icon.png')
    root.iconphoto(False, Icon)
    Interface = GUI(root, mydb, my_cursor)
    #my_cursor.execute('CREATE TABLE car_list (id INT AUTO_INCREMENT PRIMARY KEY, Titlu VARCHAR(255), Pret VARCHAR(255), An VARCHAR(255), Kilometraj VARCHAR(255), Combustibil VARCHAR(255), Culoare VARCHAR(255), Link VARCHAR(511), p INT)')
    root.mainloop()
    my_cursor.close()
    mydb.close()
