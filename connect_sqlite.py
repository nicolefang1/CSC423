import sqlite3
import pandas as pd

# Connects to an existing database file in the current directory
# If the file does not exist, it creates it in the current directory
db_connect = sqlite3.connect('test.db')

# Instantiate cursor object for executing queries
cursor = db_connect.cursor()

# String variable for passing queries to cursor

# Create tables ----------------------------------------
query = """
    -- Create Clinic
    CREATE TABLE IF NOT EXISTS Clinic (
        clinicNo integer NOT NULL primary key,
        clinicName text,
        address text NOT NULL,
        telephone int NOT NULL);
    """
cursor.execute(query)
query = """
    -- Create Staff
    CREATE TABLE IF NOT EXISTS Staff (
        staffNo integer NOT NULL primary key,
        staffName text,
        address text,
        telephone int,
        DOB date,
        staffPos text,
        salary integer,
        clinicNo integer,
        FOREIGN KEY (clinicNo) REFERENCES Clinic(clinicNo));
    """
cursor.execute(query)
query = """
    -- Create Owner
    CREATE TABLE IF NOT EXISTS Owner (
        ownerNo integer NOT NULL primary key,
        ownerName text,
        address text,
        telephone int);
    """
cursor.execute(query)
query = """
    -- Create Pet
    CREATE TABLE IF NOT EXISTS Pet (
        petNo integer NOT NULL primary key,
        petName text,
        DOB date,
        species text,
        breed text,
        color text,
        ownerNo integer,
        FOREIGN KEY (ownerNo) REFERENCES Owner(ownerNo));
    """
cursor.execute(query)
query = """
    -- Create Examination
    CREATE TABLE IF NOT EXISTS Examination (
        examNo integer NOT NULL primary key,
        chiefComplaint text,
        description text,
        dateSeen date,
        actions text,
        clinicNo integer,
        petNo integer,
        FOREIGN KEY (clinicNo) REFERENCES Clinic(clinicNo),
        FOREIGN KEY (petNo) REFERENCES Pet(petNo));
    """
# Execute query, the result is stored in cursor
cursor.execute(query)

# Insert row into table ------------------------------------------
clinics = [(1000, 'Rural Vets', '123rd St', '8002343456'),
           (2000, 'Paws Clinic', '45th St', '8004567890'),
           (3000, 'ABCDogs', '786th Ave', '8001231234'),
           (4000, 'ABCats', '135th Blvd', '8001237890'),
           (5000, 'PetCare Clinic', '10th st', '8008909753')]
cursor.executemany('INSERT INTO Clinic VALUES(?,?,?,?);', clinics)

staff = [(1001, 'Alice Baker', 'address1', '1232343456', '1990-11-16', 'Manager', 10000, 1000),
         (1002, 'Bob Carp', 'address2', '1234567890', '1998-12-06', 'Groomer', 5000, 1000),
         (1003, 'Charlie Davis', 'address3', '1231231234', '1980-07-24', 'Vet', 11000, 1000),
         (1004, 'Danielle Espina', 'address4', '1230987654', '1983-01-30', 'Vet', 11000, 1000),
         (1005, 'Eve Fisher', 'address5', '1239876543', '2000-04-01', 'Groomer', 5000, 1000)]
cursor.executemany('INSERT INTO Staff VALUES(?,?,?,?,?,?,?,?)', staff)

owners = [(1101, 'Alice', 'address1', '1232343456'),
          (1102, 'Barbara', 'address6', '1231234567'),
          (1103, 'Clara', 'address7', '1230987654'),
          (1104, 'Damian', 'address8', '1234567456'),
          (1105, 'Edna', 'address9', '8901234567')]
cursor.executemany('INSERT INTO Owner VALUES(?,?,?,?);', owners)

pets = [(1011, 'Spots', '2010-01-01', 'Dog', 'Dalmatian', 'White', 1101),
        (1012, 'Boots', '2012-02-02', 'Cat', 'Tabby', 'Orange', 1102),
        (1013, 'Oreo', '2018-03-03', 'Cat', 'Shorthair', 'Gray', 1103),
        (1014, 'Sparky', '2012-02-29', 'Dog', 'Bicheom', 'White', 1104),
        (1015, 'Nemo', '2010-05-05', 'Fish', 'Goldfish', 'Gold', 1105)]
cursor.executemany('INSERT INTO Pet VALUES(?,?,?,?,?,?,?);', pets)

exams = [(1111, 'XYZ', 'ABC', '2022-12-01', 'ZZZ', 1000, 1011),
         (1112, 'WXY', 'ABC', '2022-12-02', 'YYY', 1000, 1012),
         (1113, 'VWX', 'ABC', '2022-12-03', 'XXX', 1000, 1013),
         (1114, 'UVW', 'ABC', '2022-12-04', 'VVV', 1000, 1014),
         (1115, 'TUV', 'ABC', '2022-12-05', 'UUU', 1000, 1015)]
cursor.executemany('INSERT INTO Examination VALUES(?,?,?,?,?,?,?);', exams)

# Select data --------------------------------------------------
query = """
    Select s.staffNo, s.staffName
    From clinic c, staff s
    Where c.clinicNo = s.clinicNo and c.address like '123rd St';
    """
cursor.execute(query)
# Extract column names from cursor
column_names = [row[0] for row in cursor.description]
# Fetch data and load into a pandas dataframe
table_data = cursor.fetchall()
df = pd.DataFrame(table_data, columns=column_names)
# Examine dataframe
print(df)
print(df.columns)
print('----------------------------')
query = """
    Select o.ownerName
    From examination e, pet p, owner o
    Where e.petNo = p.petNo and p.ownerNo = o.ownerNo and dateSeen = '2022-12-01';
    """
cursor.execute(query)
# Extract column names from cursor
column_names = [row[0] for row in cursor.description]
# Fetch data and load into a pandas dataframe
table_data = cursor.fetchall()
df = pd.DataFrame(table_data, columns=column_names)
# Examine dataframe
print(df)
print(df.columns)
print('----------------------------')
query = """
    Select p.*
    From Pet p, Owner o
    Where p.ownerNo = o.ownerNo AND ownerName like 'Alice%';
    """
cursor.execute(query)
# Extract column names from cursor
column_names = [row[0] for row in cursor.description]
# Fetch data and load into a pandas dataframe
table_data = cursor.fetchall()
df = pd.DataFrame(table_data, columns=column_names)
# Examine dataframe
print(df)
print(df.columns)
print('----------------------------')
query = """
    Select count(*)
    From Pet p, Examination e
    Where p.petNo = e.petNo and species like 'Dog' and chiefComplaint like 'XYZ';
    """
cursor.execute(query)
# Extract column names from cursor
column_names = [row[0] for row in cursor.description]
# Fetch data and load into a pandas dataframe
table_data = cursor.fetchall()
df = pd.DataFrame(table_data, columns=column_names)
# Examine dataframe
print(df)
print(df.columns)
print('----------------------------')
query = """
    Select o.*
    From Examination e, Pet p, Owner o
    Where p.ownerNo = o.ownerNo and e.petNo = p.petNo and e.actions like 'ZZZ';
    """
cursor.execute(query)
# Extract column names from cursor
column_names = [row[0] for row in cursor.description]
# Fetch data and load into a pandas dataframe
table_data = cursor.fetchall()
df = pd.DataFrame(table_data, columns=column_names)
# Examine dataframe
print(df)
print(df.columns)
print('----------------------------')
# Example to extract a specific column
# print(df['name'])

# Commit any changes to the database
db_connect.commit()

# Close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
db_connect.close()
