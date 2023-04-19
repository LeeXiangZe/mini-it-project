import sqlite3
from datetime import datetime, timedelta
from tabulate import tabulate
conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS CREDENTIALS
            (NAME     TEXT PRIMARY KEY NOT NULL, 
             PASSWORD TEXT NOT NULL, 
             PHONE    INT  NOT NULL, 
             EMAIL    TEXT NOT NULL,
             PENALTY  INT )''')
fetch = c.execute('SELECT NAME from CREDENTIALS WHERE NAME=?',('ADMIN',))
if fetch.fetchone() == None:
    c.execute("INSERT INTO CREDENTIALS (NAME, PASSWORD, PHONE, EMAIL)\
        VALUES('ADMIN', 'ADMINPWD', 0199999999, 'admin@email.com') ")
    conn.commit()

c.execute('''CREATE TABLE IF NOT EXISTS BOOKS 
                (ID INT PRIMARY KEY NOT NULL,
                TITLE TEXT NOT NULL,
                AUTHOR TEXT,
                CATEGORY TEXT NOT NULL,
                LANGUAGE TEXT NOT NULL,
                FICTION TEXT NOT NULL, 
                AMOUNT INT NOT NULL,
                PRICE REAL NOT NULL, 
                PUBLISHER TEXT NOT NULL,
                YEAR INT );''')

c.execute('''CREATE TABLE IF NOT EXISTS LIST
         (ID           INT       NOT NULL, 
          TITLE        TEXT      NOT NULL,
          BORROWEDBY   TEXT      NOT NULL,  
          BORROWEDDATE TIMESTAMP NOT NULL,
          EXPIREDDATE  TIMESTAMP NOT NULL, 
          COLLECT      INT       NOT NULL)''')

def signUp():   
    name = str(input("Enter name: "))
    fetch  = c.execute('SELECT NAME from CREDENTIALS WHERE NAME=?', (name,))
    while name == '':
        print("Username cannot be empty. ")
        name = str(input("Enter name: "))
    while name == '' or fetch.fetchone() != None:
        print("Username has been taken")
        name = str(input("Enter name: "))
        fetch  = c.execute('SELECT NAME from CREDENTIALS WHERE NAME=?', (name,))
    
    pwd = str(input("Enter password (at least 10 characters): "))
    while pwd == '' or len(pwd) < 10:
        print("Password invalid. ")
        pwd = str(input("Enter password (at least 10 characters): "))

    phone = input("Enter phone: ")
    while  phone == '' or len(phone) < 10 or len(phone) > 11 or phone.isdigit() == False:
        print("Phone number invalid. ")
        phone = input("Enter phone: ")

    email = str(input("Enter email: "))
    while email == '' or '@' not in email:
        print("Email invalid. ")
        email = str(input("Enter email: "))

    c.execute("INSERT INTO CREDENTIALS (NAME, PASSWORD, PHONE, EMAIL) VALUES(?, ?, ?, ?)",(name, pwd, phone, email))
    print("Signed up successfully. ")
    conn.commit()
    main()
    quit()

def checklogin(name,pwd):
    check = c.execute('SELECT * from CREDENTIALS WHERE NAME=? AND PASSWORD=?', (name, pwd))
    for row in check:
        if row != None:
            return True
        else:
            return False

def titlef():
    global title
    title = str(input("Title: "))
    while title == '':
        print("Invalid")
        title = str(input("Title: "))

def categoryf():
    global category, catChoice, ficChoice, langChoice
    categoryList =['Literature', 'Encyclopedia', 'Guidlines', 'Motivations', 'Dictionary', 'History', 'News', 'Others']
    catChoice = int(input("[1]Literature\n[2]Encyclopedia\n[3]Guidlines\n[4]Motivations\n[5]Dictionary\n[6]History\n[7]News\n[8]Others\nEnter choice: "))
    while catChoice < 1 or catChoice >9:
        print("Input invalid. ")
        catChoice = int(input("[1]Literature\n[2]Encyclopedia\n[3]Guidlines\n[4]Motivations\n[5]Dictionary\n[6]History\n[7]News\n[8]Others\nEnter choice: "))
    category = categoryList[catChoice-1]
    fictionf()
    languagef()

def amountf():
    global amount
    amount = input("Enter amount: ")
    while amount == '' or int(amount) <= 0 or amount.isdigit() == False:
        print("Invalid")
        amount = input("Enter amount: ")

def pricef():
    global price
    price = input("Enter price: RM")
    while price == '':
        print("Invalid")
        price = input("Enter price: RM")
    price = format(float(price), ".2f")

def authorf():
    global author
    author = str(input("Enter author: "))
    while author == '':
        print("Invalid")
        author = str(input("Enter author: "))

def languagef():
    global langChoice, language
    languageList = ["English", "Malay", "Chinese", "Tamil", "Others"]
    langChoice = int(input("[1]English\n[2]Malay\n[3]Chinese\n[4]Tamil\n[5]Others\nEnter choice: "))
    while langChoice == '':
        print("Invalid")
        langChoice = input("[1]English\n[2]Malay\n[3]Chinese\n[4]Tamil\n[5]Others\nEnter choice: ")
    language = str(languageList[langChoice-1])
    

def fictionf():
    global ficChoice, fiction
    ficChoice = input("[1]Fiction\n[2]Non-fiction\nEnter choice: ")
    while ficChoice not in ('1', '2'):
        print("Invalid")
        ficChoice = input("[1]Fiction\n[2]Non-fiction\nEnter choice: ")
    if ficChoice == 1:
        fiction = str("Fiction")
    else:
        fiction = str("Non-fiction")

def commitf(index, title, author, category, language, fiction, amount, price, publisher, year,):
    amountl = int(1)
    if int(amount) > 1:
        for i in range (1, int(amount) + 1):
            c.execute("INSERT INTO BOOKS (ID, TITLE, AUTHOR, CATEGORY, LANGUAGE, FICTION, AMOUNT, PRICE, PUBLISHER, YEAR) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (index, title, author, category, language, fiction, amountl, price, publisher, year,))
            index = int(index) + 1
    else:
        c.execute("INSERT INTO BOOKS (ID, TITLE, AUTHOR, CATEGORY, LANGUAGE, FICTION, AMOUNT, PRICE, PUBLISHER, YEAR) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (index, title, author, category, language, fiction, amountl, price, publisher, year,))
    conn.commit()
    print("Book has been added. ")
    
def idf(catChoice, langChoice, ficChoice):
    #id = category, language, fiction, index
    global index
    catChoice = str(catChoice)
    langChoice = str(langChoice)
    ficChoice = str(ficChoice)
    x = (catChoice + langChoice + ficChoice + "0001")
    row = c.execute("SELECT * FROM BOOKS")
    existance = row.fetchone()
    rows = c.execute("SELECT * FROM BOOKS")
    quantity = len(rows.fetchall())
    if existance == None:
        index = str(x)
    elif quantity >= 1:
        h = (catChoice + langChoice + ficChoice + "0001")
        h = int(h)
        result = c.execute("SELECT * FROM BOOKS")
        for y in result:
            if y[0] == h:
                h += 1
        h = str(h)
        index = str(h.zfill(4))

def publisherf():
    global publisher
    publisher = str(input("Enter publisher: "))
    while publisher == "":
        print("Invalid")
        publisher = str(input("Enter publisher: "))

def yearf():
    global year
    year = input("Enter year: ")
    while year == '' or year.isdigit() == False:
        print("Invalid")
        year = input("Enter year: ")
    year = int(year)
   
def addBooks():
    titlef()
    categoryf()
    amountf()
    pricef()
    authorf()
    idf(catChoice, langChoice, ficChoice)
    publisherf()
    yearf()
    print(f"\nTitle: {title} \nCategory: {category} \nFiction: {fiction} \nLanguage: {language} \nAmount: {amount} \nPrice: {price} \nAuthor: {author} \nIndex: {index} \nPublisher: {publisher}")
    commitf(index, title, author, category, language, fiction, amount, price, publisher, year)
    print("Back to menu to make any changes. ")
    

#def menu():
def searchBook():
    choice = int(input("[1]Search Book \n[2]View All Books \n[3]Back to menu \nEnter your choice: "))
    while choice == '' or choice < 1 or choice > 3: 
        print("Input Invalid")
        choice = int(input("[1]Search Book \n[2]View All Books \n[3]Back to menu \nEnter your choice: "))
    if choice == 1:
        search_menu()
    elif choice == 2:
        view_all_books()
    else:
        studentFeature()

def search_menu():
    choices = ["title", "author", "year", "category", "language", "amount", "publisher"]
    choice_input = int(input("Search with: \n[1]Title \n[2]Author \n[3]Year \n[4]Category \n[5]Language \n[6]Availability \n[7]Publisher \n[8]Back to menu \nEnter your choice: "))
    while choice_input < 1 or choice_input > 8:
        choice_input = int(input("Search with: \n[1]Title \n[2]Author \n[3]Year \n[4]Category \n[5]Language \n[6]Availability \n[7]Publisher \n[8]Back to menu \nEnter your choice: "))
    if choice_input == 8:
        if user == "ADMIN":
            adminFeature()
        else:
            studentFeature()
    else:
        choice = choices[choice_input-1]
        if choice_input == 6:
            user_input = str(input(f"Enter {choice} (0 or 1): "))
        else:
            user_input = str(input(f"Enter {choice}: "))
    library = str(f"SELECT ID, TITLE, AUTHOR, CATEGORY, LANGUAGE, FICTION, AMOUNT, PUBLISHER, YEAR FROM books WHERE {choice} LIKE '%{user_input}%'")
    #print(library)
    data = []
    c.execute(library)
    books = c.fetchall()
    #print(books)
    if len(books) == 0:
        print("No books found.")
    else:
        print("Search results:")
        for book in books:
            data.append(book)
        listing(data)

    while True:
        if user != "ADMIN":
            choice = int(input("[1]Another search \n[2]Borrow Book \n[3]Back to menu \nEnter your choice: "))
            while choice < 1 or choice >4:
                choice = input("Invalid input. \n[1]Another search \n[2]Borrow Book \n[3]Back to menu \nEnter your choice: ")
            if choice == 1:
                search_menu()
            elif choice == 2:
                BorrowBook(0)
            elif choice == 3:
                print("we will proceed back to menu")
                studentFeature()

        elif user == "ADMIN":
            choice = int(input("[1]Another search \n[2]Back to menu \nEnter your choice: "))
            while choice < 1 or choice >3:
                choice = input("Invalid input. \n[1]Another search \n[2]Back to menu \nEnter your choice: ")
            if choice == 1:
                search_menu()
            elif choice == 2:
                print("we will proceed back to menu")
                adminFeature()

def view_all_books():
    c.execute("SELECT * FROM books")
    books = c.fetchall()
    data = []
    if len(books) == 0:
       print("No books found.")
    else:
        print("Books:")
        for book in books:
            data.append(book)
        listing(data)
    
    while True:
        if user != "ADMIN":
            choice = int(input("[1]Another search \n[2]Borrow Book \n[3]Back to menu \nEnter your choice: "))
            while choice < 1 or choice >4:
                choice = input("Invalid input. \n[1]Another search \n[2]Borrow Book \n[3]Back to menu \nEnter your choice: ")
            if choice == 1:
                search_menu()
            elif choice == 2:
                BorrowBook(0)
            elif choice == 3:
                print("we will proceed back to menu")
                studentFeature()

        elif user == "ADMIN":
            choice = int(input("[1]Another search \n[2]Back to menu \nEnter your choice: "))
            while choice < 1 or choice >3:
                choice = input("Invalid input. \n[1]Another search \n[2]Back to menu \nEnter your choice: ")
            if choice == 1:
                search_menu()
            elif choice == 2:
                print("we will proceed back to menu")
                adminFeature()

def listing(data):
    headers = ["ID", "TITLE", "AUTHOR", "CATEGORY", "LANGUAGE", "FICTION", "AVAILABILITY", "PRICE", "PUBLISHER", "YEAR"]
    print(tabulate(data, headers=headers, tablefmt="outline"))

def BorrowBook(x):
    if x == 1:
        username = input("Enter username:")
        c.execute('SELECT NAME FROM CREDENTIALS WHERE NAME=?',(username,))
        result = c.fetchone()
        #print(username)
        while result == None:
            print("Username not found in database.")
            username = input("Enter username:")
            c.execute('SELECT NAME FROM CREDENTIALS WHERE NAME=?',(username,))
            result = c.fetchone()

        c.execute('SELECT PENALTY from CREDENTIALS WHERE NAME=?',(result[0],))
        penalty = c.fetchone()[0]

    elif x == 0:
        c.execute('SELECT PENALTY from CREDENTIALS WHERE NAME=?',(user,))
        penalty = c.fetchone()[0]

    if penalty != None :
        print(f"Currrently your status is not available, pay your penalty first to borrow books. \nThe amount you need to pay is: RM{penalty}")
        #payment system
        if user == "ADMIN":
            adminFeature()
        else:
            studentFeature()
    else:
        qty = 0
        count = 0
        amt = 0
        data = []
        while qty <= 0 or qty >= 4:
            qty = int(input("Input amount of book u want to borrow maximum 3: "))

        while count < qty:
            #select the book u want
            bookMau = input("Input book ID that u want to borrow: ")
            c.execute('SELECT ID FROM BOOKS where ID=?',(bookMau,))
            id = c.fetchone()
            num = c.execute('SELECT AMOUNT FROM BOOKS WHERE ID=?',(bookMau,))
            for row in num:
                amt = int(row[0])
            while id==None or amt<=0:
                print("Book is not available. Please enter a valid book ID ")
                bookMau = input("Input book ID that u want to borrow or press 'n' back to menu: ")
                if bookMau == 'n':
                    if user == "ADMIN":
                        adminFeature()
                    else:
                        studentFeature()
                else:
                    bookMau = int(bookMau)
                    c.execute('SELECT TITLE FROM BOOKS where ID=?',(bookMau,))
                    id = c.fetchone()
                    num = c.execute('SELECT AMOUNT FROM BOOKS WHERE ID=?',(bookMau,))
                    for row in num:
                        amt = int(row[0])

            #get book title
            book = c.execute('SELECT * from BOOKS WHERE ID=?', (bookMau,))
            for row in book:
                title = row[1]
                data.append(row)
            listing(data)

            decn=input("press any key to continue, press 'n' back to menu: ")
            if decn=='n' :
                if user == "ADMIN":
                    adminFeature()
                else:
                    studentFeature()
            else:
                #create borrow datetime
                now = datetime.now().strftime("%Y-%m-%d")
            
                #create expried datetime
                expDate = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

                #update amount left into BOOKS.db & insert data into LIST.db
                c.execute('UPDATE BOOKS SET AMOUNT=AMOUNT-? WHERE ID=?',(1,bookMau,))
                c.execute('INSERT INTO LIST (ID, TITLE, BORROWEDBY, BORROWEDDATE, EXPIREDDATE, COLLECT) VALUES(?, ?, ?, ?, ?, ?)', (bookMau, title, user, now, expDate, x,))

                conn.commit()
                count += 1
        print('borrow successful')
        if user == "ADMIN":
            adminFeature()
        else:
            studentFeature()

def CollectBook():
    # Read table where collect = 0
    list = []
    c.execute("SELECT * from LIST WHERE COLLECT = ?",(0,))
    record = c.fetchall()
    for row in record:
        print('ID: ',row[0])
        print('Title: ',row[1])
        print('Borrowed by: ',row[2])
        print('Borrowed date: ',row[3])
        print('Return date: ',row[4])
        print('Collect: ',row[5])
        print('-----------')

    user_input = int(input('Press [1] to proceed; Press [2] to cancel: '))
    while user_input not in [1,2]:
        print('Invalid input, please try again.')
        user_input = int(input('Press [1] to proceed; Press [2] to cancel: '))
    if user_input == 2:
        #Back to admin menu (X)
        adminFeature()
    elif user_input == 1:
        # Change collect into 1
        book_id = input('Enter book ID: ')
        c.execute('UPDATE LIST SET COLLECT = ? WHERE ID = ?',(1,book_id,))
        conn.commit()
        print('Update completed.')

def ReturnBook(): 
    penalty = 0
    count = 0
    data = c.execute('SELECT * FROM LIST')
    for x in data:
        count = count + 1
    rtnAmt = int(input('Enter how many books u want to return: '))
    while rtnAmt > count:
        print("the amount u input is not valid")
        rtnAmt = int(input('Enter how many books u want to return: '))
    for count in range (1, rtnAmt+1, 1):
        rtnBookID = int(input('Enter book ID that u want to return: '))
        c.execute('SELECT ID FROM LIST WHERE ID=?',(rtnBookID,))
        id = c.fetchone()
        while id == None:
            print("input invalid, input again")
            rtnBookID = int(input('Enter book ID that u want to return: '))
            c.execute('SELECT ID FROM LIST WHERE ID=?',(rtnBookID,))
            id = c.fetchone()

        c.execute("SELECT EXPIREDDATE from LIST WHERE ID=?",(rtnBookID,))
        ExpriredDate = c.fetchone()[0]
    
        now = datetime.now()
        #convert to object
        Exprired_date = datetime.strptime(ExpriredDate, "%Y-%m-%d")
        print("now ",now)
        print("ExpriredDate ",ExpriredDate)
        #date diff
        dateDiff = (now - Exprired_date).days
        print("dateDiff ",dateDiff)
        if dateDiff > 0:
            penalty = penalty + (dateDiff*1)

        #AMOUNT + 1
        #c.execute('UPDATE BOOKS SET AMOUNT=AMOUNT+? WHERE ID=?',(1,rtnBookID,))
        #conn.commit()

        #delete data in LIST after the people return the book
        #c.execute('DELETE from LIST WHERE ID=?;',(rtnBookID,))
        #conn.commit()

        print("return successful")
        print("penalty ",penalty)
    #update credentials penalty database
    print(user)
    c.execute('UPDATE CREDENTIALS SET PENALTY=PENALTY+? WHERE NAME=?',(penalty, user))
    conn.commit()

def edit_credential(): 
    choices = int(input("Edit: \n[1]Name \n[2]Password \n[3]Phone \n[4]Email \nEnter choice: "))
    if choices == 1:
        choice = "NAME"  
        value = str(input("Enter name: "))
        fetch  = c.execute('SELECT NAME from CREDENTIALS WHERE NAME=?', (value,))
        while value == '':
            print("Username cannot be empty. ")
            value = str(input("Enter name: "))
        while value == '' or fetch.fetchone() != None:
            print("Username has been taken")
            value = str(input("Enter name: "))
            
    elif choices == 2:
        choice = "password"
        value = str(input("Enter password (at least 10 characters): "))
        while value == '' or len(value) < 10:
            print("Password invalid. ")
            value = str(input("Enter password (at least 10 characters): "))

    elif choices == 3:
        choice = "phone"
        value = input("Enter phone: ")
        while  value == '' or len(value) < 10 or len(value) > 11 or value.isdigit() == False:
            print("Phone number invalid. ")
            value = input("Enter phone: ")

    elif choices == 4:
        choice = "email"
        value = str(input("Enter email: "))
        while value == '' or '@' not in value:
            print("Email invalid. ")
            value = str(input("Enter email: "))

    c.execute(f"UPDATE CREDENTIALS set {choice}=? WHERE NAME=?", (value, user))
    print("Edit successfully. ")
    conn.commit()
    studentFeature()

def main():
    global user
    login = False
    choice = input("[1]Login \n[2]Sign Up \n[3]End \nEnter your choice: ")
    if choice == '1':
        name = str(input("Enter username: "))
        pwd = str(input("Enter password: "))
        login  = checklogin(name, pwd)
        if login == True:
            print("Login successful. ")
            print("Welcome", name)
            user = name
        else:
            print("Username or password incorrect. ")
            main()
            quit()
    elif choice == '2':
        signUp()
    elif choice == '3':
        quit()
    else:
        main()
        quit()

    if user == 'ADMIN':
        adminFeature()
    else:
        studentFeature()

def studentFeature():
    print("[1]Search Book \n[2]View status \n[3]Edit user Details \n[4]Log Out")
    choice = int(input("Enter your choice:"))
    if choice == 1:
        searchBook()
    elif choice == 2:
        status = c.execute("SELECT * from CREDENTIALS WHERE NAME=?",(user,))
        for row in status:
            print('Name: ',row[0])
            print('Phone: ',row[2])
            print('Email: ',row[3])
            print('Penalty: ',row[4])
            print('-----------')
        studentFeature()
    elif choice == 3:
        edit_credential()
    else:
        main()
        quit()

def adminFeature():
    print("[1]Add book \n[2]Search book \n[3]Borrow Books \n[4]View Books To collect \n[5]Return Books \n[6]Log Out")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        addBooks()
    elif choice == 2:
        searchBook()
    elif choice == 3:
        BorrowBook(1)
    elif choice == 4:
        CollectBook()
    elif choice == 5:
        ReturnBook()
    else:
        main()
        quit()
    adminFeature()

#main
main()
conn.close()
