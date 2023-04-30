"""
1) get mode (add, search)
2) if add,
    - get contact details
    - store into file/database
3) if search,
    - ask for details to be search
    - search by detail
        - if found ,show details
        - else, show not found.
4) delete
5) update
"""
import sqlite3
import click

# @click is decorator 
@click.command()
@click.argument('entity')
@click.argument('operation')
def phonebook(entity,operation):
    if operation == 'add':
        add_contact()   

    if operation == 'search':
        search_contact_by_details()
    
    if operation == 'delete':
        delete_contact()

    if update == 'update':
        update_contact()
       
    # click.echo(entity,operation)
def Create_table_If_not_exist():
    # check if table exist return from function
    # if not exist create
    
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    res = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='contacts'")
    result = cursor.fetchone()
        # Check if the table exists
    if result:
        # cursor.execute("ALTER TABLE contacts RENAME COLUMN contact TO phone")
        print("Table exists.")
    else:
        res = cursor.execute("CREATE TABLE contacts(name, phone, EmailId)")

    cursor.close()
    con.close()
    

def add_contact():
    name = input("name")
    phone = int(input("phone"))
    EmailId = input("EmailId")

    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    cursor.execute('INSERT INTO contacts (name, phone,EmailId) VALUES (?, ?, ?)', (name, phone,EmailId))
    con.commit()
    con.close()
    click.echo(f'contact successfully added')


def search_contact_by_details():
    search_term = input("Write anything you remember name or phone number: ").strip()

    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    # cursor.execute('SELECT name,phone FROM contacts WHERE name=?', (user_input,))
      
    # Construct the SQL query with the LIKE operator
    # The LIKE operator is used in SQL to perform a pattern matching of a string value against a search pattern.
    sql_query = "SELECT * FROM contacts WHERE name LIKE? OR phone LIKE ?"

# SELECT * FROM contacts WHERE name LIKE '%7260%'  OR phone LIKE '%7260%'

    search_term = f"%{search_term}%"

    # Execute the query with the search term
    cursor.execute(sql_query, (search_term, search_term))

    contacts = cursor.fetchall()
    # if user input is incomplete string or incomplete num, show all possible matches
    # match to phonenum and name both column

    # Display the matching contacts 
    if len(contacts) > 0:
        for row in contacts:
            print(row)
    else:
        print("No contacts found.")


    cursor.close()
    con.close()

def delete_contact():
    pass


def update_contact():
    pass

if __name__ == '__main__':
    Create_table_If_not_exist()
    phonebook()
    