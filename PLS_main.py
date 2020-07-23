# PLS main source file
# EREN 0993650
import PLS_classes

publib = PLS_classes.PublicLibrary()

publib.startlibrary(open('booksset1.json', 'r',
                         encoding='UTF-8'),
                    open('FakeNameSet20.csv', 'r',
                         encoding='UTF-8'))
while True:

    option = input(
        "1: Search for books and loan books.\n2: search for custommers.\n3: add a book.\n4: Add a custommer  \n5: Make Back up\n6: Restore Back up\n7: exit\n")
    customerbook = []
    optionloan = 0

    if (option == "1"):
        # boek vinden en lenen
        customerId = 0
        idbooklist = publib.catalog.searchBookItem(input(
            "Give one of the following informations to find book(s): \n author, country, language, wikipedia link, title, year"))

        if idbooklist == []:
            print()
            print()
            print("Book(s) not found try again!!!!!")

        else:
            publa = publib.loanadministration

            optionInside = input(
                "1: Are you a custommer and Do you wan't to loan these book(s)?\n2: Do you wan't to loan these book(s)? But you are here for the first time?\n3: Do you wan't to search again?\n")

            if optionInside == "2":
                publa.AddCustomer(Gender=input("Put in your gender"),
                                  NameSet=input("Put in your Nameset"), GivenName=input("Put in your GivenName"),
                                  Surname=input("Put in your Surname"),
                                  StreetAddress=input("Put in your StreetAddress"),
                                  ZipCode=input("Putin your ZipCode"), City=input("Put in your City"),
                                  EmailAddress=input("Put in your EmailAdress"), Username=input("Put in your Username"),
                                  TelephoneNumber=input("Put in your TelephoneNumber"))
                optionInside = "1"

            if optionInside == "1":
                customerId = publa.FindCustomer(input(
                    "Give one of the following informations to find you'account: \n Number,Gender,NameSet,GivenName,Surname,StreetAddress,ZipCode,City,EmailAddress,Username,TelephoneNumber"))

                for b in idbooklist:
                    if publib.catalog.bookitemsamount(b) > 0:
                        publa.MakeBookItemLoan(b, customerId)
                    else:
                        print("Book: " + b + " out of stock")

    if (option == "2"):
        # customer vinden
        customerId = publib.loanadministration.FindCustomer(input(
            "Give one of the following informations to find the custommer: \n Number,Gender,NameSet,GivenName,Surname,StreetAddress,ZipCode,City,EmailAddress,Username,TelephoneNumber"))

    if (option == "3"):
        # boek toevoegen
        cat = publib.catalog
        cat.addbookitem(author=input("Who is the author of the book?"), title=input("What is the title of the book?"),
                        language=input("What is the language of the book?"),
                        link=input("What is the website of the book?") + "\n",
                        pages=int(input("How many pages does the boook have?(only numbers)")),
                        year=int(input("in which year is the book brought out?(only numbers")))

    if (option == "4"):
        # add customer
        publa = publib.loanadministration
        publa.AddCustomer(Gender=input("Put in your gender"),
                          NameSet=input("Put in your Nameset"), GivenName=input("Put in your GivenName"),
                          Surname=input("Put in your Surname"), StreetAddress=input("Put in your StreetAddress"),
                          ZipCode=input("Putin your ZipCode"), City=input("Put in your City"),
                          EmailAddress=input("Put in your EmailAdress"), Username=input("Put in your Username"),
                          TelephoneNumber=input("Put in your TelephoneNumber"))

    if (option == "5"):
        print()
        print()
        print()

        publib.makebackup()
        print("Backup is succesvol!")

    if (option == "6"):
        publib.restorebackup()
        print("restore is succesvol!")


    if (option == "7"):
        break

    print()
    print()
