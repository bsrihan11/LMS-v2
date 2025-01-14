from lms import db
from werkzeug.security import generate_password_hash, check_password_hash
from lms import cache
from sqlalchemy import event,func
from datetime import date, datetime,timezone,timedelta, tzinfo


class Permission:
    USER = 1
    MANAGER = 2
    ADMIN = 4
    
class Role(db.Model):
    __tablename__ = 'roles'
    role_id = db.Column(db.Integer,primary_key=True)
    role_name = db.Column(db.String(64),unique=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User',backref='role',lazy='dynamic')

    def __init__(self,role_name,permissions=0,*args,**kwargs):
        self.role_name = role_name
        self.permissions = permissions

    def to_json(self):
        result = {
            "role_name":self.role_name,
            "user_count":len((self.users))
        }
        
        return result


class User(db.Model):
    __tablename__='users'
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50),nullable = False)
    last_name = db.Column(db.String(50),nullable = False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash= db.Column(db.String(264),nullable=False)
    active = db.Column(db.Integer,nullable=False,default = 1)
    last_visited = db.Column(db.DateTime,nullable = False)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.role_id'))
    collection = db.relationship('Book', secondary='transactions', 
                                 backref=db.backref('customers',lazy="dynamic"),lazy="dynamic") 
    
    

    def __init__(self,first_name,last_name,email, password,role_id,
                 last_visited=datetime.now(timezone.utc),*args,**kwargs):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.role_id = role_id
        self.last_visited = last_visited
        self.set_password(password)

    @property
    def username(self):
        return self.first_name + " " + self.last_name

    # User credentials
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_eligible(self,permission):
        return self.role.permissions>=permission
    
    def is_active(self):
        return self.active == 1
    
     
    # User Transactions

    # Add book to user collection
    def add_to_collection(self, book_id):
        current_utc_datetime = datetime.now(timezone.utc)
        book = Book.query.get(book_id)
        if not book or not book.is_available:
            raise Exception("invalid book.")

        future_datetime = current_utc_datetime + timedelta(days=book.days)
        trans = Transaction.query.filter_by(user_id=self.user_id, book_id=book_id).first()

        if trans:
            if trans.status == 'AVAILABLE':
                raise Exception('book already added to collection')
            
            trans.status = "AVAILABLE"
            trans.transaction_time = current_utc_datetime

            # for demo 

            # if self.email == '21f1004112@ds.study.iitm.ac.in' and book.book_id == 1:
            #     trans.deadline = current_utc_datetime + timedelta(minutes=1)
            # else:
            
            trans.deadline = future_datetime

            trans.downloaded = False
            db.session.commit()

            rating = Rating.query.filter_by(user_id=self.user_id, book_id=book.book_id).first()

            cache.set(f"user-{self.user_id}-collection", self.get_collection(), timeout=12 * 60 * 60)

            book.update_vol()

            return {"book_name": book.book_name,
                    "book_id":book.book_id,
                    "deadline": self.time_left(trans.deadline),
                    'rating': rating.rating if rating else 0
                    }
        
        new_trans = Transaction(user_id=self.user_id, book_id=book_id)

        #for demo 

        # if self.email == '21f1004112@ds.study.iitm.ac.in' and book.book_id == 1:
        #         new_trans.deadline = current_utc_datetime + timedelta(minutes=1)
        # else:
        
        new_trans.deadline = future_datetime

        db.session.add(new_trans)
        db.session.commit()

        cache.set(f"user-{self.user_id}-collection", self.get_collection(), timeout=12 * 60 * 60)


        book.update_vol()

        return {"book_name": book.book_name,
                "book_id":book.book_id,
                "deadline": self.time_left(new_trans.deadline),
                'rating': 0
                }

    # Return book
    # Same method will be used by celery task also to return if not already returned.
    def return_book(self,book_id):
        trans = Transaction.query.filter_by(user_id=self.user_id , book_id=book_id).first()
        if trans:
            if trans.status == 'RETURNED':
                raise Exception('Book already returned.')
            else:
                trans.status = 'RETURNED'
                db.session.commit()
                cache.set(f"user-{self.user_id}-collection",self.get_collection(),timeout = 12 * 60 * 60)


        else:
            raise Exception('Transaction not found.')
   
    #rate a book
    def rate_book(self,book_id,rating):
        trans = Transaction.query.filter_by(user_id=self.user_id , book_id=book_id).first()
        if trans:
            if trans.status == 'RETURNED':
                raise Exception('book already returned.')
            existing = Rating.query.filter_by(user_id=self.user_id,book_id=book_id).first()
            if existing:
                if existing.rating != rating:
                    existing.rating = rating
                    db.session.commit()
                
                cache.set(f"user-{self.user_id}-collection",self.get_collection(),timeout = 12 * 60 * 60)

            else:
                new_rating = Rating(user_id=self.user_id,book_id=book_id)
                new_rating.rating = rating
                db.session.add(new_rating)
                db.session.commit()
                cache.set(f"user-{self.user_id}-collection",self.get_collection(),timeout = 12 * 60 * 60)

            
        else:
            raise Exception('only those who availed book can rate it.')


    def time_left(self,deadline):
        end_date = deadline.replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)

        
        time_difference = end_date - now
        days = time_difference.days
        hours, remainder = divmod(time_difference.seconds, 3600)

        if days > 0:
            return f"{days} {'day' if days == 1 else 'days'} left"
        else:
            return "Ending Soon"



    def get_collection(self):
        available_books = [(Transaction.query.filter_by(user_id=self.user_id,
                                              book_id=book.book_id,status="AVAILABLE").first(),book) 
                                              for book in self.collection.all()]
        
        available_books = [(transaction, book) for transaction, book in available_books 
                           if transaction is not None]
        
        sorted_books = sorted(available_books,key=lambda x:x[0].deadline.replace(tzinfo=timezone.utc))
        result = {}
        for trans,book in sorted_books:
            rating = Rating.query.filter_by(user_id = self.user_id,book_id = book.book_id).first()
            result[book.book_id] = {"book_name":book.book_name,
                                    "book_id":book.book_id,
                                    "deadline":self.time_left(trans.deadline),
                                    'rating':rating.rating if rating else 0
                                    }

        return result
        


    def to_json(self):
        self.last_visited = datetime.now(timezone.utc)
        db.session.commit()

        result = {
            "user_id":self.user_id,
            "first_name":self.first_name,
            "last_name":self.last_name,
            "email":self.email,
            "active":self.active,
            "role":self.role.role_name
        }

        return result


class Section(db.Model):
    __tablename__="sections"
    section_id = db.Column(db.Integer, primary_key=True)
    section_name = db.Column(db.String(264), nullable=False)
    section_cover = db.Column(db.String(100),nullable=False)
    books = db.relationship('Book', backref='section',lazy="dynamic")


    def __init__(self,section_name,section_cover,*args,**kwargs):
        self.section_name = section_name
        self.section_cover = section_cover

    def vol_sold(self):
        total = 0
        for book in self.books.all():
            total+=book.vol_sold

        return total
    
    def to_json(self,type = 'FULL'):

        if type == 'BRIEF':
            result = {
                "section_id":self.section_id,
                "section_name":self.section_name,
                "section_cover":self.section_cover
                }
            
            return result

        result = {
                "section_id":self.section_id,
                "section_name":self.section_name,
                "section_cover":self.section_cover,
                "books":[book.book_id for book in self.books.all() if book.is_available]
                }
        
        return result

class Author(db.Model):
    __tablename__ = "authors"

    author_id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String(264), nullable=False)
    books = db.relationship('Book', secondary='book_authors',
                            backref=db.backref("authors",lazy="dynamic"),lazy="dynamic")

    def __init__(self,author_name,*args,**kwargs):
        self.author_name = author_name

    def vol_sold(self):
        total = 0
        for book in self.books.all():
            total+=book.vol_sold

        return total
    

    def to_json(self):
        result = {
            "author_id":self.author_id,
            "author_name":self.author_name
        }

        return result


class Book(db.Model):
    __tablename__ = "books"
    book_id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(264), nullable=False)
    book_cover = db.Column(db.String(100),nullable=False)
    book_price = db.Column(db.Integer, nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.section_id'), nullable=False)
    is_available = db.Column(db.Boolean,nullable = False)
    path = db.Column(db.String(200),nullable=False) 
    book_summary = db.Column(db.Text, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    days = db.Column(db.Integer,nullable=False)
    avg_rating = db.Column(db.Integer,nullable = False,default = 0)
    vol_sold = db.Column(db.BigInteger,nullable = False,default = 0)
    preprocessed_text = db.Column(db.Text)


    def __init__(self,book_name,book_cover,
                 book_price,section_id,path,
                 book_summary,year,days=7,is_available=True,vol_sold=0,avg_rating=0,*args,**kwargs):

        self.book_name = book_name 
        self.book_cover = book_cover
        self.book_price = book_price 
        self.book_summary = book_summary 
        self.year = year
        self.section_id = section_id
        self.is_available = is_available
        self.path = path
        self.days = days
        self.vol_sold = vol_sold
        self.avg_rating = avg_rating
        
        self.preprocess()


    # Manager Functions
        
    # Assign authors to book by their id
    def assign_authors(self, author_list):  
        author_list = [int(author_id) for author_id in author_list.split(",")]          
        # Remove existing authors not in the new list
        existing_authors = [author.author_id for author in self.authors.all()]

        authors_to_remove = set(existing_authors) - set(author_list)
        for author_id in authors_to_remove:
            BookAuthor.query.filter_by(book_id = self.book_id, author_id = author_id).delete()

        db.session.commit()

        # Add new authors not in the existing list
        new_authors = set(author_list) - set(existing_authors)
        for author_id in new_authors:
            book_authors = BookAuthor(book_id=self.book_id, author_id=author_id)
            db.session.add(book_authors)

        db.session.commit()


    # Helpers
    # Avg rating for a book(rounded to 0)
    def update_rating(self):
        avg_rating = db.session.query(func.avg(Rating.rating)).filter(Rating.book_id == self.book_id).scalar()
        

  
        self.avg_rating = round(avg_rating,0) if avg_rating else self.avg_rating

        db.session.commit()

    # Amount of vol sold for this book
    def update_vol(self):
        self.vol_sold += 1
        db.session.commit()




    # Preprocess text for search
    def preprocess(self):
        
        text = self.book_summary


        from lms.helpers import lemmatize_text

        self.preprocessed_text = lemmatize_text(text)
        db.session.commit()


    
    def to_json(self,type="FULL"):
        self.update_rating()
        from lms.api.utils import format_vol_sold
        if type == 'BRIEF':
            result = {
            "book_id":self.book_id,
            "book_name": self.book_name,
            "book_cover":self.book_cover,
            "book_price":self.book_price,
            "section_name":self.section.section_name,
            "is_available":self.is_available,
            "avg_rating":self.avg_rating
            }

            return result
        
        if type == 'ADMIN':
            result = {
            "book_id":self.book_id,
            "book_name": self.book_name,
            "book_cover":self.book_cover,
            "book_price":self.book_price,
            "is_available":self.is_available,
            "section_id":self.section.section_id,
            "path":self.path,
            "book_summary":self.book_summary,
            "year":self.year,
            'days':self.days,
            "author_list":",".join([str(author.author_id) for author in self.authors.all()])
            }

            return result

        result = {
            "book_id":self.book_id,
            "book_name": self.book_name,
            "book_cover":self.book_cover,
            "book_price":self.book_price,
            "is_available":self.is_available,
            "section_name":self.section.section_name,
            "book_summary":self.book_summary,
            "avg_rating":self.avg_rating,
            "vol_sold":format_vol_sold(self.vol_sold),
            "year":self.year,
            'days':self.days,
            "authors":[author.author_name for author in self.authors.all()]
        }

        return result





class Rating(db.Model):
    __tablename__ = 'ratings'
    rating = db.Column( db.Integer, nullable=False,default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), primary_key=True)

    def __init__(self, user_id, book_id, rating=0 ,*args,**kwargs):
        self.rating = rating
        self.user_id = user_id
        self.book_id = book_id

class BookAuthor(db.Model):
    __tablename__ = 'book_authors'
    author_id = db.Column(db.Integer, db.ForeignKey('authors.author_id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), primary_key=True)

    def __init__(self, author_id, book_id,*args,**kwargs):
        self.author_id = author_id
        self.book_id = book_id


class Transaction(db.Model):
    __tablename__ = 'transactions'
    transaction_id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))
    deadline = db.Column(db.DateTime,nullable=False)
    transaction_time = db.Column(db.DateTime,nullable=False)
    status = db.Column(db.String(50),nullable=False)
    downloaded = db.Column(db.Boolean,default = False)

    def __init__(self, 
                 user_id, 
                 book_id,
                 deadline=datetime.now(timezone.utc),
                 transaction_time=datetime.now(timezone.utc),downloaded=False,*args,**kwargs):
        
        self.user_id = user_id
        self.book_id = book_id
        self.deadline = deadline
        self.transaction_time = transaction_time
        self.status = "AVAILABLE"
        self.downloaded = downloaded




@event.listens_for(Role.__table__, 'after_create')
def create_roles(*args, **kwargs):
    roles = [
        {"role_name":'USER',"permissions":Permission.USER},
        { "role_name":'MANAGER', "permissions":Permission.MANAGER},
        { "role_name":'ADMIN' ,"permissions":Permission.ADMIN}
    ]

    db.session.bulk_insert_mappings(Role,roles)

    db.session.commit()

@event.listens_for(User.__table__, 'after_create')
def add_admin(*args,**kwargs):
    ad_id = Role.query.filter_by(role_name = 'ADMIN').first().role_id
    mg_id = Role.query.filter_by(role_name = 'MANAGER').first().role_id
    us_id = Role.query.filter_by(role_name = 'USER').first().role_id
    users_to_add = [
        {"first_name": "Admin","last_name":"One", "email": "admin@lms.com", "password": "admin","role_id":ad_id},
        {"first_name": "Manager","last_name":"One", "email": "manager1@lms.com", "password": "manager1","role_id":mg_id},
        {"first_name": "Manager","last_name":"Two", "email": "manager2@lms.com", "password": "manager2","role_id":mg_id},
        {"first_name": "User","last_name":"One", "email": "user1@lms.com", "password": "user1","role_id":us_id},
        {"first_name": "User","last_name":"Two", "email": "user2@lms.com", "password": "user2","role_id":us_id}
    ]

    for user in users_to_add:
        new_user = User(**user)
        db.session.add(new_user)

    db.session.commit()


@event.listens_for(Section.__table__, 'after_create')
def add_sections(*args, **kwargs):
    sections_to_add = [
        {'section_name':'DEFAULT',"section_cover":"section_cover.jpeg"},
        {"section_name": 'Fiction', "section_cover": "section_cover.jpeg"},         
        {"section_name": 'Dystopian', "section_cover": "section_cover.jpeg"},
        {"section_name": 'Romance', "section_cover": "section_cover.jpeg"},                    
        {"section_name": 'Fantasy', "section_cover": "section_cover.jpeg"},           
        {"section_name": 'Coming-of-age', "section_cover": "section_cover.jpeg"},            
        {"section_name": 'Romance', "section_cover": "section_cover.jpeg"},         
        {"section_name": 'Adventure', "section_cover": "section_cover.jpeg"}      
    ]
    db.session.bulk_insert_mappings(Section, sections_to_add)
    db.session.commit()

@event.listens_for(Author.__table__, 'after_create')
def add_authors(*args, **kwargs):
    authors_to_add = [
    {"author_name": 'Harper Lee', "author_cover": "author_cover.jpg"}, 
    {"author_name": 'George Orwell', "author_cover": "author_cover.jpg"},  
    {"author_name": 'Jane Austen', "author_cover": "author_cover.jpg"},   
    {"author_name": 'F. Scott Fitzgerald', "author_cover": "author_cover.jpg"},  
    {"author_name": 'J.K. Rowling', "author_cover": "author_cover.jpg"}, 
    {"author_name": 'J.D. Salinger', "author_cover": "author_cover.jpg"}, 
    {"author_name": 'J.R.R. Tolkien', "author_cover": "author_cover.jpg"},     
    {"author_name": 'Charlotte Brontë', "author_cover": "author_cover.jpg"}, 
    {"author_name": 'Herman Melville', "author_cover": "author_cover.jpg"}  
    ]

    db.session.bulk_insert_mappings(Author, authors_to_add)
    db.session.commit()

import random
@event.listens_for(BookAuthor.__table__, 'after_create')
def add_books(*args, **kwargs):
    books_to_add = [
        {
            'book_name': 'To Kill a Mockingbird',
            'book_cover': 'book_cover.jpg',
            'book_price': 1099,
            'section_id': Section.query.filter_by(section_name = "Fiction").first().section_id,
            'path': 'book.pdf',
            'book_summary': 'A novel set in the American South during the 1930s, addressing racial injustice.',
            'year': 1960,
            'days': 14,
            'is_available': True,
            'vol_sold':random.randint(2000,4000),
            'avg_rating':5,
            'author_list':",".join([str(Author.query.filter_by(author_name="Harper Lee").first().author_id)])
        },
        {
            'book_name': '1984',
            'book_cover': 'book_cover.jpg',
            'book_price': 1299,
            'section_id': Section.query.filter_by(section_name = "Dystopian").first().section_id,
            'path': 'book.pdf',
            'book_summary': 'A dystopian novel, portraying a totalitarian regime and surveillance.',
            'year': 1949,
            'days': 7,
            'is_available': True,
            'vol_sold':random.randint(2000,4000),
            'avg_rating':3,
            'author_list':",".join([str(Author.query.filter_by(author_name='George Orwell').first().author_id)])
        },
        {
            'book_name': 'Pride and Prejudice',
            'book_cover': 'book_cover.jpg',
            'book_price': 999,
            'section_id': Section.query.filter_by(section_name = "Romance").first().section_id,
            'path':'book.pdf',
            'book_summary': 'A classic novel, focusing on themes of love, marriage, and societal expectations.',
            'year': 1813,
            'days': 10,
            'is_available': True,
            'vol_sold':random.randint(2000,4000),
            'avg_rating':5,
            'author_list':",".join([str(Author.query.filter_by(author_name='Jane Austen').first().author_id)])
        },
        {
            'book_name': 'The Great Gatsby',
            'book_cover': 'book_cover.jpg',
            'book_price': 1199,
            'section_id': Section.query.filter_by(section_name = "Fiction").first().section_id,
            'path': 'book.pdf',
            'book_summary': 'A novel depicting the Jazz Age in America and the pursuit of the American Dream.',
            'year': 1925,
            'days': 7,
            'is_available': True,
            'vol_sold':random.randint(2000,4000),
            'avg_rating':2,
            'author_list':",".join([str(Author.query.filter_by(author_name='F. Scott Fitzgerald').first().author_id)])
        },
        {
            'book_name': 'Harry Potter and the Philosopher\'s Stone',
            'book_cover': 'book_cover.jpg',
            'book_price': 1499,
            'section_id': Section.query.filter_by(section_name = "Fantasy").first().section_id,
            'path': 'book.pdf',
            'book_summary': 'The first book in the Harry Potter series ,following the journey of a young wizard, Harry Potter.',
            'year': 1997,
            'days': 14,
            'is_available': True,
            'vol_sold':random.randint(2000,4000),
            'avg_rating':4,
            'author_list':",".join([str(Author.query.filter_by(author_name='J.K. Rowling').first().author_id)])
        },
        {
            'book_name': 'The Catcher in the Rye',
            'book_cover': 'book_cover.jpg',
            'book_price': 1049,
            'section_id': Section.query.filter_by(section_name = "Coming-of-age").first().section_id,
            'path': 'book.pdf',
            'book_summary': 'novel narrated by a teenager, Holden Caulfield, depicting his experiences in New York City.',
            'year': 1951,
            'days': 7,
            'is_available': True,
            'vol_sold':random.randint(2000,4000),
            'avg_rating':3,
            'author_list':",".join([str(Author.query.filter_by(author_name='J.D. Salinger').first().author_id)])
        },
        {
            'book_name': 'The Lord of the Rings',
            'book_cover': 'book_cover.jpg',
            'book_price': 1999,
            'section_id': Section.query.filter_by(section_name = "Fantasy").first().section_id,
            'path': 'book.pdf',
            'book_summary': 'set in the fictional world of Middle-earth, depicting the journey to destroy the One Ring.',
            'year': 1954,
            'days': 14,
            'is_available': True,
            'vol_sold':random.randint(2000,4000),
            'avg_rating':3,
            'author_list':",".join([str(Author.query.filter_by(author_name='J.R.R. Tolkien').first().author_id)])
        },
        {
            'book_name': 'The Hobbit',
            'book_cover': 'book_cover.jpg',
            'book_price': 1349,
            'section_id': Section.query.filter_by(section_name = "Fantasy").first().section_id,
            'path': 'book.pdf',
            'book_summary': 'preceding The Lord of the Rings, following the journey of Bilbo Baggins.',
            'year': 1937,
            'days': 10,
            'is_available': True,
            'vol_sold':random.randint(2000,4000),
            'avg_rating':2,
            'author_list':",".join([str(Author.query.filter_by(author_name='J.R.R. Tolkien').first().author_id)])
        },
        {
            'book_name': 'Jane Eyre',
            'book_cover': 'book_cover.jpg',
            'book_price': 949,
            'section_id': Section.query.filter_by(section_name = "Romance").first().section_id,
            'path': 'book.pdf',
            'book_summary': 'A novel following the life of the orphaned protagonist, Jane Eyre, as she faces various challenges and finds love.',
            'year': 1847,
            'days': 7,
            'is_available': True,
            'vol_sold':random.randint(2000,4000),
            'avg_rating':4,
            'author_list':",".join( [str(Author.query.filter_by(author_name='Charlotte Brontë').first().author_id)])
        },
        {
            'book_name': 'Moby-Dick',
            'book_cover': 'book_cover.jpg',
            'book_price': 1179,
            'section_id': Section.query.filter_by(section_name = "Adventure").first().section_id,
            'path': 'book.pdf',
            'book_summary': 'A novel following the voyage of the whaling ship Pequod and its captain, Ahab, in pursuit of the white whale, Moby Dick.',
            'year': 1851,
            'days': 14,
            'is_available': True,
            'vol_sold':random.randint(2000,4000),
            'avg_rating':5,
            'author_list':",".join( [str(Author.query.filter_by(author_name='Herman Melville').first().author_id)])
        }]   

    for book_info in books_to_add: 
        book = Book(**book_info)
        db.session.add(book)
        db.session.commit()

        book.assign_authors(author_list = book_info['author_list'])
