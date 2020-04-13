import sqlite3
from Car import Car
import os
from prettytable import PrettyTable
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

# making a clear function to clear the console. Only works on windows
clear = lambda: os.system('cls')  # on Windows System
clear()

db = sqlite3.connect("carDB.sqlite3")
cursor = db.cursor()

carList = []

# Automatically creates a new table in the database if there are none existing already.
cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='cars' ''')
if cursor.fetchone()[0] != 1:
    cursor.execute(
        '''CREATE TABLE cars(id INTEGER PRIMARY KEY, brand TEXT, price INTEGER, year INTEGER, licensePlate TEXT, 
        isLeasingCar BOOLEAN)''')
    carList.append(Car("Mercedes", 950000, 2018, "AB07354", 1))
    carList.append(Car("Citroën", 60000, 2013, "B012345", 0))
    carList.append(Car("BMW", 567000, 2020, "SC60856", 0))

    for c in carList:
        cursor.execute(''' INSERT INTO cars(brand, price, year, licensePlate, isLeasingCar) VALUES (?,?,?,?,?) ''',
                       (c.brand, c.price, c.year, c.licensePlate, c.isLeasingCar))
        db.commit()


def intro():
    clear()
    cursor.execute("SELECT COUNT (*) FROM cars")
    rowcount = cursor.fetchone()[0]
    print("There is ", rowcount, " cars in the database.")
    print("1. Show all cars")
    print("2. Add a car")
    print("3. Remove a car")
    print("4. Update a car")
    print("5. Show a certain car")
    print("6. Exit")
    userInput = input("What do you choose? Enter number\n")
    switch = 0
    while switch == 0:
        try:
            int(userInput)
        except ValueError:
            clear()
            print("This is not a number")
            input("Press enter to continue")
            intro()
        else:
            switch = 1
    choice = int(userInput)
    if choice == 1:
        showAll()
    elif choice == 2:
        add()
    elif choice == 3:
        remove()
    elif choice == 4:
        update()
    elif choice == 5:
        showOne()
    elif choice == 6:
        clear()
        print("Saving cars and exiting program")
    else:
        print("This is not an option")
        input("Press enter to continue")
        intro()


def showAll():
    clear()
    cur = cursor.execute("SELECT * from cars")
    t = PrettyTable(["ID", "Brand", "Price [kr.]", "Year", "License plate", "Is car leased?"])
    for row in cur:
        if row[5]:
            leasing = "Yes"
        else:
            leasing = "No"
        t.add_row([row[0], row[1], row[2], row[3], row[4], leasing])
    print(t)
    input("Press enter to continue")
    intro()


def add():
    clear()
    print('What is the brand of the car? Write "a" to cancel\n')
    brandInput = input('Or write "i" to import a car from bilhandel.dk\n')
    if brandInput.lower() == "a":
        intro()
    elif brandInput.lower() == "i":
        clear()
        url = input("Enter URL for the car you want to import\n")
        try:
            page = urlopen(url)
        except:
            print("Error opening the URL")
        else:
            clear()
            soup = BeautifulSoup(page, 'html.parser')

            contentTitle = soup.find('div', {"class": "col-xs-8"})
            title = ''

            for x in contentTitle.findAll('h1'):
                title = title + ' ' + x.text
                if len(title) > 0:
                    titleSplit = title.split()
                    title = titleSplit[0]

                contentPrice = soup.find('div', {"class": "col-xs-4"})
                price = ''
                for x in contentPrice.findAll('div'):
                    price = price + ' ' + x.text

                contentYear = soup.find('div', {"style": "font-size: 16px;padding-left:15px;"})
                year = ''
                for x in contentYear.findAll('span'):
                    year = year + ' ' + x.text

                priceOutput = re.sub('\D', '', price)
                yearSplit = year.split()
                if len(yearSplit) > 0:
                    yearOutput = re.sub('\D', '', yearSplit[4])

                licensePlateInput = input("What is the license plate if the car?\n")
                isLeasingCarInput = input("Is the car leased?\n").lower()
                if isLeasingCarInput.startswith("j" or "y"):
                    cursor.execute(
                        ''' INSERT INTO cars(brand, price, year, licensePlate, isLeasingCar) VALUES (?,?,?,?,?) ''',
                        (title, priceOutput, yearOutput, licensePlateInput, 1))
                else:
                    cursor.execute(
                        ''' INSERT INTO cars(brand, price, year, licensePlate, isLeasingCar) VALUES (?,?,?,?,?) ''',
                        (title, priceOutput, yearOutput, licensePlateInput, 0))
                db.commit()
                intro()
    else:
        switch = 0
        while switch == 0:
            try:
                priceInput = float(input('What is the price of the car?\n'))
            except ValueError:
                clear()
                print("This is not a number")
                input("Press enter to continue")
            else:
                switch = 1
        switch = 0
        while switch == 0:
            try:
                yearInput = int(input("What year is the car from?\n"))
            except ValueError:
                clear()
                print("This is not a number")
                input("Press enter to continue")
            else:
                switch = 1
        licensePlateInput = input("What is the license plate if the car?\n")
        isLeasingCarInput = input("Is the car leased?\n").lower()
        if isLeasingCarInput.startswith("j" or "y"):
            cursor.execute(''' INSERT INTO cars(brand, price, year, licensePlate, isLeasingCar) VALUES (?,?,?,?,?) ''',
                           (brandInput.capitalize(), priceInput, yearInput, licensePlateInput, 1))
        else:
            cursor.execute(''' INSERT INTO cars(brand, price, year, licensePlate, isLeasingCar) VALUES (?,?,?,?,?) ''',
                           (brandInput.capitalize(), priceInput, yearInput, licensePlateInput, 0))
        db.commit()
        intro()


def remove():
    clear()
    cur = cursor.execute("SELECT id, brand, price, year, licensePlate, isLeasingCar from cars")
    t = PrettyTable(["ID", "Brand", "Price [kr.]", "Year", "License plate", "Is car leased?"])
    for row in cur:
        if row[5]:
            leasing = "Ja"
        else:
            leasing = "Nej"
        t.add_row([row[0], row[1], row[2], row[3], row[4], leasing])
        '''print(str(row[0]) + ".", row[1], "fra år ", row[2], "med nummepladen:", row[3])'''
    print(t)
    print('What car do you want to remove? Enter ID')
    carID = input('Write "a" to cancel\n')
    if carID.lower() == "a":
        intro()
    else:
        switch = 0
        while switch == 0:
            try:
                float(carID)
            except ValueError:
                clear()
                print("This is not a number")
                input("Press enter to continue")
                remove()
            else:
                switch = 1
        sqlDelete = '''DELETE from cars where id=?'''
        sqlData = (int(carID))
        cursor.execute(sqlDelete, (int(sqlData),))
        db.commit()
        intro()


def update():
    clear()
    cur = cursor.execute("SELECT id, brand, price, year, licensePlate, isLeasingCar from cars")
    t = PrettyTable(["ID", "Brand", "Price [kr.]", "Year", "License plate", "Is car leased?"])
    for row in cur:
        if row[5]:
            leasing = "Yes"
        else:
            leasing = "No"
        t.add_row([row[0], row[1], row[2], row[3], row[4], leasing])
    print(t)
    print('What car do you want to update? Enter ID')
    carID = input('Write "a" to cancel\n')
    if carID.lower() == "a":
        intro()
    else:
        switch = 0
        while switch == 0:
            try:
                float(carID)
            except ValueError:
                clear()
                print("This is not a number")
                input("Press enter to continue")
                update()
            else:
                switch = 1
        switch1 = 0
        while switch1 == 0:
            sqlUpdate = ''' SELECT * from cars WHERE id =?'''
            sqlData = (int(carID))
            cur = cursor.execute(sqlUpdate, (int(sqlData),))
            clear()
            for row in cur:
                print("1. Brand:", row[1])
                print("2. Price:", row[2])
                print("3. Year:", row[3])
                print("4. License plate:", row[4])
                if row[5] == 0:
                    print("5. Leasing status: The car is not leased")
                else:
                    print("5. Leasing status: The car is leased")
                print("6. Exit")
            userInput = input("What do you want to update? Enter number\n")
            switch1 = 1
            switch2 = 0
            while switch2 == 0:
                try:
                    float(userInput)
                except ValueError:
                    clear()
                    print("This is not a number")
                    input("Press enter to continue")
                else:
                    switch2 = 1
            if int(userInput) == 1:
                clear()
                sqlUpdate = ''' UPDATE cars SET brand =? WHERE id =? '''
                sqlData = input("What is the new brand for the car?\n")
                cursor.execute(sqlUpdate, (sqlData, int(carID),))
                db.commit()
            if int(userInput) == 2:
                clear()
                sqlUpdate = ''' UPDATE cars SET price =? WHERE id =? '''
                switch3 = 0
                while switch3 == 0:
                    sqlData = input("What is the new price for the car?\n")
                    try:
                        float(sqlData)
                    except ValueError:
                        clear()
                        print("This is not a number")
                        input("Press enter to continue")
                    else:
                        switch3 = 1
                cursor.execute(sqlUpdate, (int(sqlData), int(carID),))
                db.commit()
            if int(userInput) == 3:
                clear()
                sqlUpdate = ''' UPDATE cars SET year =? WHERE id =? '''
                switch4 = 0
                while switch4 == 0:
                    sqlData = input("What is the new year for the car?\n")
                    try:
                        float(sqlData)
                    except ValueError:
                        clear()
                        print("This is not a number")
                        input("Press enter to continue")
                    else:
                        switch4 = 1
                cursor.execute(sqlUpdate, (int(sqlData), int(carID),))
                db.commit()
            if int(userInput) == 4:
                clear()
                sqlUpdate = ''' UPDATE cars SET licensePlate =? WHERE id =? '''
                sqlData = input("What is the new license plate for the car?\n")
                cursor.execute(sqlUpdate, (sqlData, int(carID),))
                db.commit()
            if int(userInput) == 5:
                clear()
                sqlUpdate = ''' UPDATE cars SET isLeasingCar =? WHERE id =? '''
                sqlData = input("Is the car leased?\n").lower()
                if sqlData.startswith("j" or "y"):
                    sqlData = 1
                else:
                    sqlData = 0
                cursor.execute(sqlUpdate, (int(sqlData), int(carID),))
                db.commit()
            if int(userInput) == 6:
                clear()
                switch = 1
        update()


def showOne():
    clear()
    sqlSearch = ''' SELECT * from cars WHERE brand =?'''
    sqlData = (input("Search for car brand: "))
    cur = cursor.execute(sqlSearch, (sqlData.capitalize(),))
    if cur.fetchone():
        clear()
        cur = cursor.execute(sqlSearch, (sqlData.capitalize(),))
        t = PrettyTable(["ID", "Brand", "Price [kr.]", "Year", "License plate", "Is car leased?"])
        print("Showing results for", sqlData)
        for row in cur:
            if row[5]:
                leasing = "Yes"
            else:
                leasing = "No"
            t.add_row([row[0], row[1], row[2], row[3], row[4], leasing])
        print(t)
        input("Press enter to continue")
    else:
        clear()
        print("There was no results for the brand", sqlData + ".")
        userInput = input("Do you want to add a new car?\n").lower()
        print(userInput)
        if userInput.startswith("j" or "y"):
            add()
        else:
            intro()
    intro()


intro()

db.commit()
db.close()
