#Classes of the PLS

import json, csv, pathlib
from random import randint


currentid = 100000
def generateid(t):
    global currentid
    currentid +=1
    return t+str(currentid)

class PublicLibrary:
    def __init__(self):
        self.catalog = Catalog()
        self.loanadministration = LoanAdministration()

    def startlibrary(self, bookfile, customerfile):
        booklist = json.load(bookfile)
        for d in booklist:
            book = Book(**d)
            self.catalog.bookdict[book.id] = book
            aantalbookitems = randint(1, 6)
            for n in range(aantalbookitems):
                bookitem = BookItem(book)
                bookattr = dict(book.__dict__)
                del bookattr['id']
                self.catalog.addbookitem(**bookattr)

        csvdictreader = csv.DictReader(customerfile)
        for csvline in csvdictreader:
            customer = Customer(**csvline)

            self.loanadministration.customerdict[customer.id] = customer


    def backupfunc(self, bd):
        if bd != {}:
            bdforjson0 = {itemid: dict(bd[itemid].__dict__) for itemid in bd}
            for key in bdforjson0:
                del bdforjson0[key]['id']
            return  bdforjson0

    def makebackup(self,):
        # bd = self.catalog.bookdict
        bdforjson0 = self.backupfunc(self.catalog.bookdict)
        bdforjson1 = self.backupfunc(self.loanadministration.customerdict)
        bdforjson2 = self.backupfunc(self.loanadministration.loanitemdict)
        bdforjson3 = self.catalog.bookitemdict
        bdforjson4 = self.loanadministration.loanitemsperbookitem
        bdforjson5 = self.loanadministration.loanitemspercustomer


        bdforjson3 = {bookitemid: bdforjson3[bookitemid].book.id for bookitemid in bdforjson3}
        json.dump([bdforjson0,bdforjson1, bdforjson2,bdforjson3, bdforjson4, bdforjson5, currentid], open("backup.json", 'w', encoding = 'UTF-8'), indent=1)

    def getJSON(filePathAndName):
        with open("backup.json", 'r', encoding = 'UTF-8') as fp:
            return json.load(fp)

    def restorebackup(self):
        global currentid
        currentid = 100000 * 10
        bookfile = open('backup.json', 'r',
                                 encoding='utf')

        data = json.load(bookfile)
        self.catalog.bookdict = {}
        self.loanadministration.customerdict = {}
        self.loanadministration.loanitemdict = {}
        self.catalog.bookitemdict = {}
        self.catalog.bookitemsperbookdict = {}
        self.loanadministration.loanitemspercustomer = data[4]
        self.loanadministration.loanitemsperbookitem = data[5]
        currentid = data[6]


        booklist = data[0]
        for i in booklist:

            custlist = dict(booklist.get(i))
            customerd = Customer(i, **custlist)
            self.catalog.bookdict[customerd.id] = customerd

        for d in booklist:
            aantalbookitems = randint(1, 6)
            for n in range(aantalbookitems):
                bookattr = dict(booklist.get(d))
                bookattributes = bookattr
                bookpresentlist = self.catalog.searchbookID(**bookattributes)
                bookid = bookpresentlist[0]
                book = self.catalog.bookdict[bookid]
                bookitem = BookItem(book)
                self.catalog.bookitemdict[bookitem.id] = bookitem
                bookitemid = bookitem.id
                bookid = book.id
                if bookid in self.catalog.bookitemsperbookdict:
                    self.catalog.bookitemsperbookdict[bookid].append(bookitemid)
                else:
                    self.catalog.bookitemsperbookdict[bookid] = [bookitemid]

            customerlist = data[1]
            for i in customerlist:
                custlist = dict(customerlist.get(i))
                customerd = Customer(i,**custlist)

                self.loanadministration.customerdict[customerd.id] = customerd

            loanlist = data[2]
            if loanlist:
                for i in loanlist:
                    custlist = dict(loanlist.get(i))
                    customerd = LoanItem(i, **custlist)

                    self.loanadministration.loanitemdict[customerd.id] = customerd

class Book:
    def __init__(self, idd=0, **attributedict):
        if idd == 0:
            self.id = generateid('B')
        else:
            self.id = idd
        for key in attributedict:
            setattr(self, key, attributedict[key])

class BookItem:
    def __init__(self, book):
        self.id = generateid('BI')
        self.book = book

class Customer:
    def __init__(self,idd = 0, **attributedict):
        if idd == 0:
            self.id = generateid('C')
        else:
            self.id = idd
        for key in attributedict:
                setattr(self, key, attributedict[key])


class LoanItem:
    def __init__(self,idd = 0, **attributedict):
        if idd == 0:
            self.id = generateid('LI')
        else:
            self.id = idd
        for key in attributedict:
                setattr(self, key, attributedict[key])


class Catalog:
    def __init__(self):
        self.bookdict = {}
        self.bookitemdict = {}
        self.bookitemsperbookdict = {}

    def searchbookID(self, **searchattributes):
        return [id for id in self.bookdict if
                all(searchattributes[k] == getattr(self.bookdict[id], k) for
                    k in searchattributes)]

    def bookitemsamount(self, bookid):
        countofbooks = 0
        for bookitemid in self.bookitemdict:
            if self.bookitemdict[bookitemid].book.id == bookid:
                countofbooks += 1
        return countofbooks

    def searchBookItem(self, findbook):
        booklist = []
        for bookid in self.bookdict:
            book = self.bookdict[bookid]
            tmpbookid = ''
            for key in book.__dict__:
                if book.__dict__[key] == findbook:
                    tmpbookid = bookid
                    booklist.append(bookid)
                    print()
                if bookid == tmpbookid:
                    print(bookid, key, book.__dict__[key])
            if bookid == tmpbookid:
                print("Amount of books left in stock: " + str(self.bookitemsamount(bookid)))
        return booklist

    def addbookitem(self, **bookattributes):
        bookpresentlist = self.searchbookID(**bookattributes)
        if bookpresentlist == []:
            book = Book(**bookattributes)
            self.bookdict[book.id] = book
        else:
            bookid = bookpresentlist[0]
            book = self.bookdict[bookid]
        bookitem = BookItem(book)
        self.bookitemdict[bookitem.id] = bookitem
        bookitemid = bookitem.id
        bookid = book.id
        if bookid in self.bookitemsperbookdict:
            self.bookitemsperbookdict[bookid].append(bookitemid)
        else:
            self.bookitemsperbookdict[bookid] = [bookitemid]

    def bookitemdict(self):

        return self.bookitemdict
        

class LoanAdministration():
    def __init__(self):
        self.loanitemdict = {}
        self.customerdict = {}
        self.loanitemsperbookitem = {}
        self.loanitemspercustomer = {}

    def FindCustomer(self,findcstmr ):
        lms = self
        for customerid in lms.customerdict:
            cstmr = lms.customerdict[customerid]
            tmpcstmrid = ''
            status = True
            for key in cstmr.__dict__:
                if cstmr.__dict__[key] == findcstmr:
                    tmpcstmrid = customerid
                    print()
                    status = True
                else:
                    status = False

            for key in cstmr.__dict__:
                if customerid == tmpcstmrid:
                    print(customerid, key, cstmr.__dict__[key])
                    return customerid

    def SearchCustomerID(self, **searchattributes):
        return [id for id in self.customerdict if
                all(searchattributes[k] == getattr(self.customerdict[id], k) for
                    k in searchattributes)]

    def AddCustomer(self, **customerattr, ):
        Customerpresentlist = self.SearchCustomerID(**customerattr)
        if Customerpresentlist == []:
            customer = Customer(**customerattr)
            self.customerdict[customer.id] = customer
        else:
            customerid = Customerpresentlist[0]
            customer = self.customerdict[customerid]


    def MakeBookItemLoan(self, bookitemid, customerid):
        loandict = {"a": bookitemid, "b": customerid}
        loan = LoanItem(**loandict)
        check = False
        self.loanitemdict[loan.id] = loan
        if customerid in self.loanitemsperbookitem:
            self.loanitemsperbookitem[bookitemid].append(customerid)
        else:
            self.loanitemsperbookitem[bookitemid] = [customerid]
        if customerid in self.loanitemspercustomer:
            self.loanitemspercustomer[customerid].append(bookitemid)
        else:
            self.loanitemspercustomer[customerid] = [bookitemid]

