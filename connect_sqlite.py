import sqlite3
import pandas as pd

# Connects to an existing database file in the current directory
# If the file does not exist, it creates it in the current directory
db_connect = sqlite3.connect('test.db')

# Instantiate cursor object for executing queries
cursor = db_connect.cursor()

# String variable for passing queries to cursor
query = """
    -- Create Clinic
    CREATE TABLE Clinic (
    clinicNo int NOT NULL primary key,
    name varchar(255),
    address varchar(255) NOT NULL,
    telephone char(10) NOT NULL);

    -- Create Staff
    CREATE TABLE Staff (
    staffNo int NOT NULL primary key,
    name varchar(255),
    address varchar(255),
    telephone char(10),
    DOB date,
    position varchar(255),
    salary int,
    clinicNo int foreign key references Clinic(clinicNo));

    -- Create Owner
    CREATE TABLE Owner (
    ownerNo int NOT NULL primary key,
    name varchar(255),
    address varchar(255),
    telephone char(10));

    -- Create Pet
    CREATE TABLE Pet (
    petNo int NOT NULL primary key,
    name varchar(255),
    DOB date,
    species varchar(255),
    breed varchar(255),
    color varchar(255),
    ownerNo int foreign key references Owner(ownerNo);

    -- Create Examination
    CREATE TABLE Examination (
    examNo int NOT NULL primary key,
    chiefComplaint varchar(255),
    description varchar(255),
    dateSeen date,
    actions varchar(255),
    clinicNo int foreign key references Clinic(clinicNo),
    petNo int foreign key references Pet(petNo));

    """

# Execute query, the result is stored in cursor
cursor.execute(query)

# Insert row into table
query = """
    INSERT INTO Person
    VALUES (1, "person1");
    """
cursor.execute(query)

# Select data
query = """
    SELECT *
    FROM Person
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

# Example to extract a specific column
# print(df['name'])


# Commit any changes to the database
db_connect.commit()

# Close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
db_connect.close()
