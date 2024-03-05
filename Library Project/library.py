import datetime
import csv

class Book:
    instances = []
    ISBNs = []
    def __init__(self, title, author, ISBN, quantity):
        if int(ISBN) in self.ISBNs:
            print("Book already exists")
        else:
            self.title = title
            self.author = author
            self.ISBN = int(ISBN)
            self.quantity = int(quantity)
            self.__class__.instances.append(self)
            self.__class__.ISBNs.append(int(ISBN))
    def setTitle(self, title):
        self.title = title
    def setAuthor(self, author):
        self.author = author
    def setISBN(self, ISBN):
        if int(ISBN) not in self.ISBNs:
            self.ISBN = int(ISBN)
            self.__class__.ISBNs.append(int(ISBN))
    def setQuantity(self, quantity):
        self.quantity = int(quantity)
    def display(self):
        return [self.title, self.author, self.ISBN, self.quantity]
    
with open('books.csv', 'r') as books:
    reader = csv.reader(books)
    for row in reader:
        Book(row[0],row[1],row[2],row[3])

class Patron:
    instances = []
    IDList = []
    def __init__(self, name, ID, email, number, fine, checkedBook = [], returnDate = []):
        if int(ID) in self.IDList:
            print("ID already exists")
        else:
            self.name = name
            self.ID = int(ID)
            self.email = email
            self.number = number
            self.fine = int(fine)
            self.checkedBooks = {}
            for i in range(len(checkedBook)):
                self.checkedBooks[int(checkedBook[i])] = int(returnDate[i])
            self.__class__.instances.append(self)
            self.__class__.IDList.append(int(ID))
    def setName(self, name):
        self.name = name
    def setID(self, ID):
        if int(ID) not in self.IDList:
            self.ID = int(ID)
    def setEmail(self, email):
        self.email = email
    def setNumber(self, number):
        self.number = number
    def setFine(self, fine):
        self.fine = int(fine)
    def display(self):
        return [self.name, self.ID, self.email, self.number, self.fine]
    
with open('patrons.csv', 'r') as patrons:
    reader = csv.reader(patrons)
    for row in reader:
        Patron(row[0],row[1],row[2],row[3],row[4],row[5::2],row[6::2])

class Transaction:
    def checkBook(patron, book):
        if book.quantity >= 1:
            patron.checkedBooks[book.ISBN] = getDate() + 7
            book.setQuantity(book.quantity - 1)
        with open('books.csv', 'w') as file:
            writer = csv.writer(file, lineterminator='\n')
            for i in Book.instances:
                writer.writerow(i.display())
        with open('patrons.csv', 'w') as file:
            writer = csv.writer(file, lineterminator='\n')
            for i in Patron.instances:
                kvs = []
                for k,v in i.checkedBooks.items():kvs.append(k),kvs.append(v)
                writer.writerow(i.display() + kvs)
    def returnBook(patron, book):
        date = getDate()
        if book.ISBN in patron.checkedBooks:
            if date > patron.checkedBooks[book.ISBN]:
                if date - patron.checkedBooks[book.ISBN] < 50:
                    patron.fine += (date - patron.checkedBooks[book.ISBN])
                else:
                    patron.fine += 50
            book.setQuantity(book.quantity + 1)
            patron.checkedBooks.pop(book.ISBN)
        with open('books.csv', 'w') as file:
            writer = csv.writer(file, lineterminator='\n')
            for i in Book.instances:
                writer.writerow(i.display())
        with open('patrons.csv', 'w') as file:
            writer = csv.writer(file, lineterminator='\n')
            for i in Patron.instances:
                kvs = []
                for k,v in i.checkedBooks.items():kvs.append(k),kvs.append(v)
                writer.writerow(i.display() + kvs)
    def renewBook(patron, book):
        if book.ISBN in patron.checkedBooks:
            if getDate() > patron.checkedBooks[book.ISBN]:
                print("Cannot renew, book overdue")
            else:
                patron.checkedBooks[book.ISBN] += 7
        with open('patrons.csv', 'w') as file:
            writer = csv.writer(file, lineterminator='\n')
            for i in Patron.instances:
                kvs = []
                for k,v in i.checkedBooks.items():kvs.append(k),kvs.append(v)
                writer.writerow(i.display() + kvs)
    def payFine(patron, amount):
        if patron.fine > 0:
            if amount > patron.fine:
                patron.fine = 0
            else:
                patron.fine -= amount
        print("Fine remaining:", patron.fine)

class Library:
    def searchTitle(title):
        books = []
        for i in Book.instances:
            if title in i.display():
                books.append(i)
        if len(books) == 0:
            print("No books with title", title)
        else:
            print("Books called ", title, ":", sep='', end='\n')
            for i in books:
                print(i.display())
    def searchAuthor(author):
        books = []
        for i in Book.instances:
            if author in i.display():
                books.append(i)
        if len(books) == 0:
            print("No books by", author)
        else:
            print("Books by ", author, ":", sep='', end='\n')
            for i in books:
                print(i.display())
    def searchISBN(ISBN):
        for i in Book.instances:
            if int(ISBN) in i.display():
                print("Book with ISBN ", ISBN, ":", sep='', end='\n')
                print(i.display())
                return
        print("No book with ISBN", ISBN)
    def searchName(name):
        patrons = []
        for i in Patron.instances:
            if name in i.display():
                patrons.append(i)
        if len(patrons) == 0:
            print("No patrons with name", name)
        else:
            print("Patrons named ", name, ":", sep='', end='\n')
            for i in patrons:
                print(i.display())
    def searchEmail(email):
        patrons = []
        for i in Patron.instances:
            if email in i.display():
                patrons.append(i)
        if len(patrons) == 0:
            print("No patrons with email", email)
        else:
            print("Patrons with email ", email, ":", sep='', end='\n')
            for i in patrons:
                print(i.display())
    def searchNumber(number):
        patrons = []
        for i in Patron.instances:
            if number in i.display():
                patrons.append(i)
        if len(patrons) == 0:
            print("No patrons with phone number", number)
        else:
            print("Patrons with phone number ", number, ":", sep='', end='\n')
            for i in patrons:
                print(i.display())
    def searchID(ID):
        for i in Patron.instances:
            if int(ID) in i.display():
                print("Patron with ID ", ID, ":", sep='', end='\n')
                print(i.display())
                return
        print("No patron with ID", ID)
    def addBook():
        book = input("Enter book details (Title,Author,ISBN,Quantity): ").split(',')
        while len(book) != 4 or not book[2].isnumeric() or int(book[2]) in Book.ISBNs or not book[3].isnumeric():
            if int(book[2]) in Book.ISBNs: book = input("ISBN already exists, enter book details (Title,Author,ISBN,Quantity): ")
            else: book = input("Invalid format, enter book details (Title,Author,ISBN,Quantity): ").split(',')
        print(book)
        choice = str(input("Add this book? (Y/N): "))
        while choice not in ['Y','y','N','n']:
            choice = str(input("Invalid action, add this book? (Y/N): "))
        if choice.upper() == 'Y':
            Book(book[0],book[1],book[2],book[3])
            with open('books.csv', 'w') as file:
                writer = csv.writer(file, lineterminator='\n')
                for i in Book.instances:
                    writer.writerow(i.display())
            input("Book added, press Enter to continue")
            bookMenu()
        elif choice.upper() == 'N':
            bookMenu()
    def removeBook():
        isbn = input("Enter ISBN of book to remove: ")
        while not isbn.isnumeric() or int(isbn) not in Book.ISBNs:
            isbn = input("Invalid ISBN, enter ISBN of book to remove: ")
        for i in Book.instances:
            if i.display()[2] == int(isbn):
                book = i
                print(i.display())
        choice = str(input("Remove this book? (Y/N): "))
        while choice not in ['Y','y','N','n']:
            choice = str(input("Invalid action, remove this book? (Y/N): "))
        if choice.upper() == 'Y':
            del Book.instances[Book.instances.index(book)]
            with open('books.csv', 'w') as file:
                writer = csv.writer(file, lineterminator='\n')
                for i in Book.instances:
                    writer.writerow(i.display())
            input("Book removed, press Enter to continue")
            bookMenu()
        elif choice.upper() == 'N':
            bookMenu()
    def editBook():
        isbn = input("Enter ISBN of book to edit: ")
        while not isbn.isnumeric() or int(isbn) not in Book.ISBNs:
            isbn = input("Invalid ISBN, enter ISBN of book to edit: ")
        for i in Book.instances:
            if i.display()[2] == int(isbn):
                book = i
        attr = input("Enter attribute to be edited (Title/Author/ISBN/Quantity): ")
        while attr.lower() not in ['title','author','isbn','quantity']:
            attr = input("Invalid action, enter attribute to be edited (Title/Author/ISBN/Quantity): ")
        if attr.lower() == 'title':
            title = input("Enter new title: ")
            print(book.display(), " -> ['", title, "', '{1}', {2}, {3}]".format(*book.display()), sep='')
            choice = str(input("Confirm edit? (Y/N): "))
            while choice not in ['Y','y','N','n']:
                choice = str(input("Invalid action, confirm edit? (Y/N): "))
            if choice.upper() == 'Y':
                book.setTitle(title)
                with open('books.csv', 'w') as file:
                    writer = csv.writer(file, lineterminator='\n')
                    for i in Book.instances:
                        writer.writerow(i.display())
                input("Book edited, press Enter to continue")
                bookMenu()
            elif choice.upper() == 'N':
                bookMenu()
        elif attr.lower() == 'author':
            author = input("Enter new author: ")
            print(book.display(), " -> ['{0}', '".format(*book.display()), author, "', {2}, {3}]".format(*book.display()), sep='')
            choice = str(input("Confirm edit? (Y/N): "))
            while choice not in ['Y','y','N','n']:
                choice = str(input("Invalid action, confirm edit? (Y/N): "))
            if choice.upper() == 'Y':
                book.setAuthor(author)
                with open('books.csv', 'w') as file:
                    writer = csv.writer(file, lineterminator='\n')
                    for i in Book.instances:
                        writer.writerow(i.display())
                input("Book edited, press Enter to continue")
                bookMenu()
            elif choice.upper() == 'N':
                bookMenu()
        elif attr.lower() == 'isbn':
            isbn = input("Enter new ISBN: ")
            while not isbn.isnumeric() or int(isbn) in Book.ISBNs:
                isbn = input("Invalid ISBN, enter new ISBN: ")
            print(book.display(), " -> ['{0}', '{1}', ".format(*book.display()), isbn, ", {3}]".format(*book.display()), sep='')
            choice = str(input("Confirm edit? (Y/N): "))
            while choice not in ['Y','y','N','n']:
                choice = str(input("Invalid action, confirm edit? (Y/N): "))
            if choice.upper() == 'Y':
                Book.ISBNs.remove(int(book.ISBN))
                book.setISBN(isbn)
                with open('books.csv', 'w') as file:
                    writer = csv.writer(file, lineterminator='\n')
                    for i in Book.instances:
                        writer.writerow(i.display())
                input("Book edited, press Enter to continue")
                bookMenu()
            elif choice.upper() == 'N':
                bookMenu()
        elif attr.lower() == 'quantity':
            quantity = input("Enter new quantity: ")
            while not quantity.isnumeric():
                quantity = input("Invalid quantity, enter new quantity: ")
            print(book.display(), " -> ['{0}', '{1}', {2}, ".format(*book.display()), quantity, "]", sep='')
            choice = str(input("Confirm edit? (Y/N): "))
            while choice not in ['Y','y','N','n']:
                choice = str(input("Invalid action, confirm edit? (Y/N): "))
            if choice.upper() == 'Y':
                book.setQuantity(quantity)
                with open('books.csv', 'w') as file:
                    writer = csv.writer(file, lineterminator='\n')
                    for i in Book.instances:
                        writer.writerow(i.display())
                input("Book edited, press Enter to continue")
                bookMenu()
            elif choice.upper() == 'N':
                bookMenu()
    def addPatron():
        patron = input("Enter patron details (Name,Email,Phone): ").split(',')
        while len(patron) != 3 or not patron[2].isnumeric():
            patron = input("Invalid format, enter patron details (Name,Email,Phone): ").split(',')
        id=1
        while id in Patron.IDList:id+=1
        patron.insert(1,id)
        print(patron)
        choice = str(input("Add this patron? (Y/N): "))
        while choice not in ['Y','y','N','n']:
            choice = str(input("Invalid action, add this patron? (Y/N): "))
        if choice.upper() == 'Y':
            Patron(patron[0],patron[1],patron[2],patron[3],0)
            with open('patrons.csv', 'w') as file:
                writer = csv.writer(file, lineterminator='\n')
                for i in Patron.instances:
                    kvs = []
                    for k,v in i.checkedBooks.items():kvs.append(k),kvs.append(v)
                    writer.writerow(i.display() + kvs)
            input("Patron added, press Enter to continue")
            patronMenu()
        elif choice.upper() == 'N':
            patronMenu()
    def removePatron():
        id = input("Enter ID of patron to remove: ")
        while not id.isnumeric() or int(id) not in Patron.IDList:
            id = input("Invalid ID, enter ID of patron to remove: ")
        for i in Patron.instances:
            if i.display()[1] == int(id):
                patron = i
                print(i.display())
        choice = str(input("Remove this patron? (Y/N): "))
        while choice not in ['Y','y','N','n']:
            choice = str(input("Invalid action, remove this patron? (Y/N): "))
        if choice.upper() == 'Y':
            del Patron.instances[Patron.instances.index(patron)]
            with open('patrons.csv', 'w') as file:
                writer = csv.writer(file, lineterminator='\n')
                for i in Patron.instances:
                    kvs = []
                    for k,v in i.checkedBooks.items():kvs.append(k),kvs.append(v)
                    writer.writerow(i.display() + kvs)
            input("Patron removed, press Enter to continue")
            patronMenu()
        elif choice.upper() == 'N':
            patronMenu()
    def editPatron():
        id = input("Enter ID of patron to edit: ")
        while not id.isnumeric() or int(id) not in Patron.IDList:
            id = input("Invalid ID, enter ID of patron to edit: ")
        for i in Patron.instances:
            if i.display()[1] == int(id):
                patron = i
        attr = input("Enter attribute to be edited (Name/Email/Number/Fine): ")
        while attr.lower() not in ['name','email','number','fine']:
            attr = input("Invalid action, enter attribute to be edited (Name/Email/Number/Fine): ")
        if attr.lower() == 'name':
            name = input("Enter new name: ")
            print(patron.display(), " -> ['", name, "', {1}, '{2}', '{3}', {4}]".format(*patron.display()), sep='')
            choice = str(input("Confirm edit? (Y/N): "))
            while choice not in ['Y','y','N','n']:
                choice = str(input("Invalid action, confirm edit? (Y/N): "))
            if choice.upper() == 'Y':
                patron.setName(name)
                with open('patrons.csv', 'w') as file:
                    writer = csv.writer(file, lineterminator='\n')
                    for i in Patron.instances:
                        kvs = []
                        for k,v in i.checkedBooks.items():kvs.append(k),kvs.append(v)
                        writer.writerow(i.display() + kvs)
                input("Patron edited, press Enter to continue")
                patronMenu()
            elif choice.upper() == 'N':
                patronMenu()
        elif attr.lower() == 'email':
            email = input("Enter new email: ")
            print(patron.display(), " -> ['{0}', {1}, '".format(*patron.display()), email, "', '{3}', {4}]".format(*patron.display()), sep='')
            choice = str(input("Confirm edit? (Y/N): "))
            while choice not in ['Y','y','N','n']:
                choice = str(input("Invalid action, confirm edit? (Y/N): "))
            if choice.upper() == 'Y':
                patron.setEmail(email)
                with open('patrons.csv', 'w') as file:
                    writer = csv.writer(file, lineterminator='\n')
                    for i in Patron.instances:
                        kvs = []
                        for k,v in i.checkedBooks.items():kvs.append(k),kvs.append(v)
                        writer.writerow(i.display() + kvs)
                input("Patron edited, press Enter to continue")
                patronMenu()
            elif choice.upper() == 'N':
                patronMenu()
        elif attr.lower() == 'number':
            number = input("Enter new phone number: ")
            while not number.isnumeric():
                number = input("Invalid format, enter new phone number: ")
            print(patron.display(), " -> ['{0}', {1}, '{2}', '".format(*patron.display()), number, "', {4}]".format(*patron.display()), sep='')
            choice = str(input("Confirm edit? (Y/N): "))
            while choice not in ['Y','y','N','n']:
                choice = str(input("Invalid action, confirm edit? (Y/N): "))
            if choice.upper() == 'Y':
                patron.setNumber(number)
                with open('patrons.csv', 'w') as file:
                    writer = csv.writer(file, lineterminator='\n')
                    for i in Patron.instances:
                        kvs = []
                        for k,v in i.checkedBooks.items():kvs.append(k),kvs.append(v)
                        writer.writerow(i.display() + kvs)
                input("Patron edited, press Enter to continue")
                patronMenu()
            elif choice.upper() == 'N':
                patronMenu()
        elif attr.lower() == 'fine':
            fine = input("Enter new fine total: ")
            print(patron.display(), " -> ['{0}', {1}, '{2}', '{3}', ".format(*patron.display()), fine, "]", sep='')
            choice = str(input("Confirm edit? (Y/N): "))
            while choice not in ['Y','y','N','n']:
                choice = str(input("Invalid action, confirm edit? (Y/N): "))
            if choice.upper() == 'Y':
                patron.setFine(fine)
                with open('patrons.csv', 'w') as file:
                    writer = csv.writer(file, lineterminator='\n')
                    for i in Patron.instances:
                        kvs = []
                        for k,v in i.checkedBooks.items():kvs.append(k),kvs.append(v)
                        writer.writerow(i.display() + kvs)
                input("Patron edited, press Enter to continue")
                patronMenu()
            elif choice.upper() == 'N':
                patronMenu()
    def checkBook():
        ID = input("Enter the ID of a patron: ")
        while not ID.isnumeric() or int(ID) not in Patron.IDList:
            ID = input("Invalid ID, enter the ID of a patron: ")
        for i in Patron.instances:
            if int(ID) in i.display():
                patron = i
        ISBN = input("Enter the ISBN code of the book: ")
        while not ISBN.isnumeric() or int(ISBN) not in Book.ISBNs:
            ISBN = input("Invalid code, enter the ISBN code of the book: ")
        for i in Book.instances:
            if int(ISBN) in i.display():
                book = i
        if book.quantity == 0:
            print("Book not available")
            input("Press Enter to continue")
            transactionMenu()
        elif book.ISBN in patron.checkedBooks:
            print("Book already checked out by patron")
            input("Press Enter to continue")
            transactionMenu()
        else:
            print(patron.display(), "is checking out", book.display())
            choice = str(input("Confirm transaction? (Y/N): "))
            while choice not in ['Y','y','N','n']:
                choice = str(input("Invalid action, confirm transaction? (Y/N): "))
            if choice.upper() == 'Y':
                Transaction.checkBook(patron, book)
                input("Transaction completed, press Enter to continue")
                transactionMenu()
            if choice.upper() == 'N':
                transactionMenu()
    def returnBook():
        ID = input("Enter the ID of a patron: ")
        while not ID.isnumeric() or int(ID) not in Patron.IDList:
            ID = input("Invalid ID, enter the ID of a patron: ")
        for i in Patron.instances:
            if int(ID) in i.display():
                patron = i
        ISBN = input("Enter the ISBN code of the book: ")
        while not ISBN.isnumeric() or int(ISBN) not in Book.ISBNs:
            ISBN = input("Invalid code, enter the ISBN code of the book: ")
        for i in Book.instances:
            if int(ISBN) in i.display():
                book = i
        if book.ISBN not in patron.checkedBooks:
            print("Patron does not have that book checked out")
            input("Press Enter to continue")
            transactionMenu()
        else:
            print(patron.display(), "is returning", book.display())
            choice = str(input("Confirm transaction? (Y/N): "))
            while choice not in ['Y','y','N','n']:
                choice = str(input("Invalid action, confirm transaction? (Y/N): "))
            if choice.upper() == 'Y':
                Transaction.returnBook(patron, book)
                input("Transaction completed, press Enter to continue")
                transactionMenu()
            if choice.upper() == 'N':
                transactionMenu()
    def renewBook():
        ID = input("Enter the ID of a patron: ")
        while not ID.isnumeric() or int(ID) not in Patron.IDList:
            ID = input("Invalid ID, enter the ID of a patron: ")
        for i in Patron.instances:
            if int(ID) in i.display():
                patron = i
        ISBN = input("Enter the ISBN code of the book: ")
        while not ISBN.isnumeric() or int(ISBN) not in Book.ISBNs:
            ISBN = input("Invalid code, enter the ISBN code of the book: ")
        for i in Book.instances:
            if int(ISBN) in i.display():
                book = i
        if book.ISBN not in patron.checkedBooks:
            print("Patron does not have that book checked out")
            input("Press Enter to continue")
            transactionMenu()
        else:
            print(patron.display(), "is renewing", book.display())
            choice = str(input("Confirm transaction? (Y/N): "))
            while choice not in ['Y','y','N','n']:
                choice = str(input("Invalid action, confirm transaction? (Y/N): "))
            if choice.upper() == 'Y':
                Transaction.renewBook(patron, book)
                input("Transaction completed, press Enter to continue")
                transactionMenu()
            if choice.upper() == 'N':
                transactionMenu()
    def payFine():
        ID = input("Enter the ID of a patron: ")
        while not ID.isnumeric() or int(ID) not in Patron.IDList:
            ID = input("Invalid ID, enter the ID of a patron: ")
        for i in Patron.instances:
            if int(ID) in i.display():
                patron = i
        if patron.fine == 0:
            print("Patron has no fines")
            input("Press Enter to continue")
            transactionMenu()
        else:
            print("['{0}', {1}, '{2}', '{3}']".format(*patron.display()), " has ", patron.fine, "$ worth of fines", sep='', end='\n')
            payment = input("Enter payment amount in USD: ")
            while not payment.isnumeric():
                payment = input("Invalid amount, enter payment amount in USD: ")
            if patron.fine - payment > 0:
                print("['{0}', {1}, '{2}', '{3}']".format(*patron.display()), " will have ", patron.fine - payment, "$ worth of fines remaining", sep='', end='\n')
                choice = str(input("Confirm transaction? (Y/N): "))
                while choice not in ['Y','y','N','n']:
                    choice = str(input("Invalid action, confirm transaction? (Y/N): "))
                if choice.upper() == 'Y':
                    Transaction.payFine(patron, payment)
                    input("Transaction completed, press Enter to continue")
                    transactionMenu()
                if choice.upper() == 'N':
                    transactionMenu()
            elif patron.fine - payment <= 0:
                print("['{0}', {1}, '{2}', '{3}']".format(*patron.display()), "will have 0$ worth of fines remaining")
                choice = str(input("Confirm transaction? (Y/N): "))
                while choice not in ['Y','y','N','n']:
                    choice = str(input("Invalid action, confirm transaction? (Y/N): "))
                if choice.upper() == 'Y':
                    Transaction.payFine(patron, payment)
                    input("Transaction completed, press Enter to continue")
                    transactionMenu()
                if choice.upper() == 'N':
                    transactionMenu()
    def bookLog():
        with open('books.csv', 'r') as file:
            reader = csv.reader(file)
            for row in file:
                print(row)
    def patronLog():
        with open('patrons.csv', 'r') as file:
            reader = csv.reader(file)
            for row in file:
                print(row)

def getDate():
    return (datetime.date.today()-datetime.date(1970,1,1)).days

def searchBookMenu():
    choice = 0
    print("How would you like to search?")
    while choice not in ['1','2','3','4']:
        print("1) Search by title\n2) Search by author\n3) Search by ISBN\n4) Return to main menu")
        choice = str(input())
        if choice == '1':
            title = str(input("Enter the title of the book: "))
            Library.searchTitle(title)
            input("Press Enter to continue")
            searchBookMenu()
        elif choice == '2':
            author = str(input("Enter the name of the author of the book: "))
            Library.searchAuthor(author)
            input("Press Enter to continue")
            searchBookMenu()
        elif choice == '3':
            ISBN = str(input("Enter the ISBN code of the book: "))
            while not ISBN.isnumeric():
                ISBN = str(input("Invalid code, enter the ISBN code of the book: "))
            Library.searchISBN(ISBN)
            input("Press Enter to continue")
            searchBookMenu()
        elif choice == '4':
            mainMenu()
        else:
            print("Invalid action, how would you like to search?")

def searchPatronMenu():
    choice = 0
    print("How would you like to search?")
    while choice not in ['1','2','3','4','5']:
        print("1) Search by name\n2) Search by email\n3) Search by phone number\n4) Search by ID\n5) Return to main menu")
        choice = str(input())
        if choice == '1':
            name = str(input("Enter the name of the patron: "))
            Library.searchName(name)
            input("Press Enter to continue")
            searchPatronMenu()
        elif choice == '2':
            email = str(input("Enter the email address of the patron: "))
            Library.searchEmail(email)
            input("Press Enter to continue")
            searchPatronMenu()
        elif choice == '3':
            number = str(input("Enter the phone number of the patron: "))
            Library.searchNumber(number)
            input("Press Enter to continue")
            searchPatronMenu()
        elif choice == '4':
            ID = str(input("Enter the ID of the patron: "))
            while not ID.isnumeric():
                ID = str(input("Invalid code, enter the ID of a patron: "))
            Library.searchID(ID)
            input("Press Enter to continue")
            searchPatronMenu()
        elif choice == '5':
            mainMenu()
        else:
            print("Invalid action, how would you like to search?")

def bookMenu():
    choice = 0
    print("What would you like to do?")
    while choice not in ['1','2','3','4']:
        print("1) Add book\n2) Remove book\n3) Update book data\n4) Return to main menu")
        choice = str(input())
        if choice == '1':
            Library.addBook()
        elif choice == '2':
            Library.removeBook()
        elif choice == '3':
            Library.editBook()
        elif choice == '4':
            mainMenu()
        else:
            print("Invalid action, what would you like to do?")

def patronMenu():
    choice = 0
    print("What would you like to do?")
    while choice not in ['1','2','3','4']:
        print("1) Add patron\n2) Remove patron\n3) Update patron data\n4) Return to main menu")
        choice = str(input())
        if choice == '1':
            Library.addPatron()
        elif choice == '2':
            Library.removePatron()
        elif choice == '3':
            Library.editPatron()
        elif choice == '4':
            mainMenu()
        else:
            print("Invalid action, what would you like to do?")

def transactionMenu():
    choice = 0
    print("What transaction would you like to complete?")
    while choice not in ['1','2','3','4','5']:
        print("1) Check a book\n2) Return a book\n3) Renew a book\n4) Pay a fine\n5) Return to main menu")
        choice = str(input())
        if choice == '1':
            Library.checkBook()
        elif choice == '2':
            Library.returnBook()
        elif choice == '3':
            Library.renewBook()
        elif choice == '4':
            Library.payFine()
        elif choice == '5':
            mainMenu()
        else:
            print("Invalid action, what transaction would you like to complete?")

def logMenu():
    choice = 0
    print("What log would you like to view?")
    while choice not in ['1','2','3']:
        print("1) Book log\n2) Patron log\n3) Return to main menu")
        choice = str(input())
        if choice == '1':
            Library.bookLog()
            input("Press Enter to continue")
            logMenu()
        elif choice == '2':
            Library.patronLog()
            input("Press Enter to continue")
            logMenu()
        elif choice == '3':
            mainMenu()
        else:
            print("Invalid action, what log would you like to view?")

def mainMenu():
    choice = 0
    print("Welcome to the LMS, please select an option")
    while choice not in ['1','2','3','4','5','6','7']:
        print("1) Search inventory\n2) Find patrons\n3) Manage books\n4) Manage patrons\n5) Initiate transaction\n6) View logs\n7) Exit LMS")
        choice = str(input())
        if choice == '1':
            searchBookMenu()
        elif choice == '2':
            searchPatronMenu()
        elif choice == '3':
            bookMenu()
        elif choice == '4':
            patronMenu()
        elif choice == '5':
            transactionMenu()
        elif choice == '6':
            logMenu()
        elif choice == '7':
            break
        else:
            print("Invalid action, please select an option")

mainMenu()

with open('books.csv', 'w') as file:
    writer = csv.writer(file, lineterminator='\n')
    for i in Book.instances:
        writer.writerow(i.display())

with open('patrons.csv', 'w') as file:
    writer = csv.writer(file, lineterminator='\n')
    for i in Patron.instances:
        kvs = []
        for k,v in i.checkedBooks.items():kvs.append(k),kvs.append(v)
        writer.writerow(i.display() + kvs)
