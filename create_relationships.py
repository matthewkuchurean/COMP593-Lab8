"""
Description:
 Creates the people table in the Social Network database
 and populates it with 200 fake people.

Usage:
 python create_db.py
"""
import os
import inspect
import sqlite3
from faker import Faker
# from datetime import datetime
from random import randint, choice

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'social_network.db')
def main():
    global db_path
    db_path = os.path.join(get_script_dir(), 'social_network.db')
    create_people_table()
    populate_relationships_table()


def create_people_table():
    """Creates the people table in the database"""
    con = sqlite3.connect('social_network.db')
    cur = con.cursor()
    create_relationship_tbl_query  = """
        CREATE TABLE IF NOT EXISTS people
        (
            id INTEGER PRIMARY KEY,
            person1_id INTEGER NOT NULL,
            person2_id INTERGER NOT NULL,
            type TEXT NOT NULL,
            start_date DATE NOT NULL, 
            FOREIGN KEY (person1_id) REFERENCES people (id),
            FOREIGN KEY (person2_id) REFERENCES people (id) 
         );
    """
    cur.execute(create_relationship_tbl_query)
    con.commit()
    con.close()
    return

def  populate_relationships_table():

    """Populates the people table with 200 fake people"""
    con = sqlite3.connect('social_network.db')
    cur = con.cursor()
    
    add_relationship_query = """
        INSERT INTO relationship
        (
            person1_id,
            person2_id, 
            type, 
            start_date,
            
        )
        VALUES (?, ?, ?, ?);
    """
    fake = Faker()
    # Randomly select first person in relationship
    for new_relationship in range (100):
        person1_id = randint(1, 200)
        # Randomly select second person in relationship
    # Loop ensures person will not be in a relationship with themself
        person2_id = randint(1, 200)
        while person2_id == person1_id:
            person2_id = randint(1, 200)
    # Randomly select a relationship type
        rel_type = choice(('friend', 'spouse', 'partner', 'relative'))
    # Randomly select a relationship start date between now and 50 years ago
        start_date = fake.date_between(start_date='-50y', end_date='today')
    # Create tuple of data for the new relationship
        new_relationship = (person1_id, person2_id, rel_type, start_date)
    # Add the new relationship to the DB
        cur.execute(populate_relationships_table(), new_relationship)
        con.commit()
    con.close()

def get_script_dir():
    """Determines the path of the directory in which this script resides
    Returns:
        str: Full path of the directory in which this script resides
    """
    script_path = os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)
    return os.path.dirname(script_path)

if __name__ == '__main__':
   main()