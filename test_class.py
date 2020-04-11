class Account:
    def __init__(self):
        pass

    def display(self):
        print(self.name, self.balance)

    def withdraw(self, amount):
        self.balance -= amount
        
    def deposit(self, amount):
        self.balance += amount

class Book:
    def __init__(self, isbn, title, author, publisher, pages, price, copies):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.publisher = publisher
        self.pages = pages
        self.price = price
        self.copies = copies

    def preview_book(self):
        print(self.isbn, self.title, self.price, self.copies)

    def in_stock(self):
        if self.copies > 0:
            return True
        else:
            return False

    def sell(self):
        if self.in_stock() == True:
            self.copies -= 1
        else:
            print("Book is out of stock!")

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, new_price):
        if new_price >= 50 and new_price <= 1000:
            self._price = new_price
        else:
            raise ValueError ("Price must be at least 50 and max 1000!")

class Fraction:
    def __init__(self, nr, dr=1):
        self.nr = abs(nr)
        self.dr = abs(dr)

    def print_fraction(self):
        print(self.nr, "/" , self.dr)

    def multiply(self)
            


book1 = Book('957-4-36-547417-1', 'Learn Physics','Stephen', 'CBC', 350, 200,10)
book2 = Book('652-6-86-748413-3', 'Learn Chemistry','Jack', 'CBC', 400, 220,20)
book3 = Book('957-7-39-347216-2', 'Learn Maths','John', 'XYZ', 500, 300,5)
book4 = Book('957-7-39-347216-2', 'Learn Biology','Jack', 'XYZ', 400, 200,6)

books = [book1, book2, book3, book4]
jacks_books = [book.title for book in books if book.author == 'Jack']

for book in books:
    book.preview_book()
