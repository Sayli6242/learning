"""
Library_management
    - Display options to user (add_books, registering_members, borrow_books, return_books, generate_report)

# check if tabel exist or not
    - if not then create BOOKS table 
    - if yes then continue programm
    - check members tabel exist or not
    - if not then create, if yes then continue to next step.
    - check table for Recods is exist or not.
    - if not then , create table using CREate Table query.
    - if yes then continue to next step.

1) adding books
    - take user input(book_title, author, publication year, ISBN number)
    - then add this detail in sqlite BOOKS_Table using INSERT queary 
    - then display massage(book successfully added)

2) register member
    - ask user to enter member(name, address, contacts_Information)
    - store user details to members table using INSERT query./         
    - display massage(member successfully registered.)

3) borrow book
    - ask user for MemberID and BookId
    - check provided memberID and BookId is existed in Recods table or not using Select query.
    - then insert provided details(memberID and BookId, status = 'borrowed') into Records table using Insert query.

4) return book
    - ask user for memberID and bookId
    - then check if user has borrowed the book by running select query where book status is 'borrowed'
    - if yes then update status to 'return' by runing update query.

5) generate report
    - display borrowed books and their member names
    - find unique bookId and their memberId.
    - and find book_title from books table and find member_name from members table.
    - then print all members name and all books name.
"""
import re
import click
import sqlite3
from validationHelper import check_name_validation
from validationHelper import check_validation_of_memberID
from validationHelper import check_year_validation
from validationHelper import check_ISBN_validation
from validationHelper import check_phone_validation
from sqliteHelper import execute_query
from sqliteHelper import create_table_if_not_exist
from sqliteHelper import fetch_one
@click.command()
def library_management():

    while True :
            click.echo('choose options: as given below \n 1) add_book \n 2) register_members \n 3) borrowing_books  \n 4) returning_books  \n 5) generationg_reports')
            option_as_input = int(input('Enter operation you wants to perform: ').strip())
            if not check_validation_for_option_as_input(option_as_input):
                print('choice must be an number from given options')
                return

            # user_input = input("Enter your options: ")
            if option_as_input == 1: 
                adding_books()

            elif option_as_input == 2:
                registering_members()

            elif option_as_input == 3:
                borrowing_books()

            elif option_as_input == 4:
                returning_books()

            elif option_as_input == 5:
                generating_reports() 
            
          
def check_validation_for_option_as_input(option_as_input):
    if option_as_input >= 1 and option_as_input <= 5:
        return True
        
    else:
        return False

def execute_table_queries():

        create_books_table_query = "CREATE TABLE IF NOT EXISTS Books (book_ID INTEGER PRIMARY KEY AUTOINCREMENT, Book_title TEXT, Publication_year INTEGER, ISBN_number TEXT)"
        create_table_if_not_exist("Books", create_books_table_query)

        create_members_table_query = "CREATE TABLE IF NOT EXISTS Members (memberID INTEGER PRIMARY KEY AUTOINCREMENT, member_name TEXT, member_address TEXT, member_contact INTEGER)"
        create_table_if_not_exist("Members", create_members_table_query)

        create_records_table_query = "CREATE TABLE IF NOT EXISTS Records(RecordID INTEGER PRIMARY KEY AUTOINCREMENT,memberId INTEGER, book_ID INTEGER, status TEXT DEFAULT 'borrowed')"
        create_table_if_not_exist("Records", create_records_table_query)

    

def adding_books():
        Book_title = input("Book_Title: ").strip()
        if not check_name_validation(Book_title):
            print('Invalid name format') 
            return
              
        Publication_year = int(input("Publication_year: ").strip())
        while not check_year_validation(Publication_year):
            print('the integer must be in range 1-10')
            return    
        
        ISBN_number = input("ISBN_number: ").strip()
        if not check_ISBN_validation(ISBN_number):
            print('invalid ISBN number')
            return

        query = "INSERT INTO Books(Book_title, Publication_year, ISBN_number) VALUES (?, ?, ?)"
        parameters = (Book_title, Publication_year, ISBN_number)
        result, book_ID = execute_query(query, parameters)
        # Book_id = cursor.lastrowid
        click.echo(f'Book successfully added with ID: {book_ID}')
    # when user enters their name then display his BookID
      # use sql query using ID to generate Id using auto increment.
        

def registering_members():
    member_name = (input('member name')).strip()
    if not check_name_validation(member_name):
        print('Invalid name format') 
        return

    member_address = input('member_address').strip()
    if not check_name_validation(member_address):
        print('Invalid name format') 
        return

    member_contact = int(input('member_contact').strip())
    if not check_phone_validation(member_contact):
            print('the integer must be in range 1-10')
            return

    # when user enters their name then display his memberID
        # use sql query using ID to generate Id using auto increment.

    query = "INSERT INTO Members(member_name, member_address, member_contact) VALUES (?, ?, ?)"
    parameters = (member_name, member_address, member_contact)
    result, memberID = execute_query(query, parameters)
    click.echo(f'Member successfully added with ID: {memberID}')
   

def borrowing_books():
    memberID = input('memberID: ')
    if not check_validation_of_memberID(memberID):
        print('Invalid memberID')
        return

    book_ID = input('bookId: ')  
    if not check_validation_of_memberID(book_ID):
        print('Invalid bookID')
        return

    # query = "SELECT * FROM Records WHERE memberID = ? AND book_ID = ?"
    # parameters = (memberID, book_ID)
    # result = execute_query(query, parameters)
    
    # if result:
    #     print(" book already borrowed")
        
    #     return
    
    query = "INSERT INTO Records(memberID, book_ID, status) VALUES (?, ?, ?)"
    parameters = (memberID, book_ID, 'borrowed')
    result , RecordId = execute_query(query, parameters)

    print(f'Book successfully borrowed:{RecordId}')

def returning_books():
    memberID = input('memberID: ')
    if not check_validation_of_memberID(memberID):
        print('Invalid memberID')
        return

    book_ID = input('bookId: ')  
    if not check_validation_of_memberID(book_ID):
        print('Invalid bookID')
        return

    # Check if the user has borrowed the book (status = 'borrowed')
    query = "SELECT * FROM Records WHERE memberID = ? AND book_ID = ? AND status = 'borrowed'"
    parameters = (memberID, book_ID)
    result = execute_query(query, parameters)

    if not result:
        print("The member has not borrowed the book.")
        cursor.close()
        con.close()
        return

    # Update the status to 'return'
    query = "UPDATE Records SET status = 'return' WHERE memberID = ? AND book_ID = ?"
    parameters = (memberID, book_ID)
    result = execute_query(query,parameters)
    
    print('Book successfully returned')


def generating_reports(): 
    # query = "SELECT book_Id, memberId FROM Records WHERE status = ?"
    # parameters = ("borrowed",)
    # result = execute_query(query, parameters)
    

    # for record in result:
    #     book_Id = record[0]
    #     member_Id = record[1]
    #     print("Book ID:", book_Id)
    #     print("Member ID:", member_Id)
    # Step 1: Display borrowed books and their member names
    query = '''
    SELECT Books.book_title, Members.member_name
    FROM Records
    INNER JOIN Books ON Records.book_ID = Books.book_ID
    INNER JOIN Members ON Records.memberID = Members.memberID
    '''
    borrowed_books = execute_query(query)

    print("Borrowed Books and Member Names:")
    
    for book, member in borrowed_books:
        print(f"Book Title: {book} | Member Name: {member}")

    # Step 2: Find unique bookId and memberId
    query = "SELECT DISTINCT book_ID, memberID FROM Records"
    unique_ids = execute_query(query)

     # Step 3: Find book_title from books table and member_name from members table
    book_titles = []
    member_names = []

    for book_ID, memberID in unique_ids:
    # Query books table for book_title
        query = "SELECT book_title FROM Books WHERE book_ID = ?"
        parameters = book_ID
        book = fetch_one(query,parameters)
        book_titles.append(book[0])


     # Query members table for member_name
        query = "SELECT member_name FROM Members WHERE memberID = ?"
        parameters = memberID
        member = fetch_one(query,memberID)
        member_names.append(member[0])

    # Step 4: Print all member names and all book titles
    print("\nAll Member Names:")
    for member in member_names:
        print(member)

    print("\nAll Book Titles:")
    for book in book_titles:
        print(book)
    
if __name__ == '__main__':
    execute_table_queries()
    library_management()
    