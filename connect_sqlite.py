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
        clinicName varchar(255),
        address varchar(255) NOT NULL,
        telephone char(10) NOT NULL);

    -- Create Staff
    CREATE TABLE Staff (
        staffNo int NOT NULL primary key,
        staffName varchar(255),
        address varchar(255),
        telephone char(10),
        DOB date,
        staffPos varchar(255) CHECK (staffPos in ('Manager', 'Groomer', 'Vet')),
        salary int CHECK (salary >= 0),
        clinicNo references Clinic(clinicNo));

    -- Create Owner
    CREATE TABLE Owner (
        ownerNo int NOT NULL primary key,
        ownerName varchar(255),
        address varchar(255),
        telephone char(10));

    -- Create Pet
    CREATE TABLE Pet (
        petNo int NOT NULL primary key,
        petName varchar(255),
        DOB date,
        species varchar(255),
        breed varchar(255),
        color varchar(255),
        ownerNo int references Owner(ownerNo));

    -- Create Examination
    CREATE TABLE Examination (
        examNo int NOT NULL primary key,
        chiefComplaint varchar(255),
        description varchar(255),
        dateSeen date,
        actions varchar(255),
        clinicNo int references Clinic(clinicNo),
        petNo int references Pet(petNo));


    """

# Execute query, the result is stored in cursor
cursor.execute(query)

# Insert row into table
query = """
    -- Insert Clinic
    INSERT INTO Clinic VALUES (1000, 'Rural Vets', '123rd St', '8002343456');
    INSERT INTO Clinic VALUES (2000, 'Paws Clinic', '45th St', '8004567890');
    INSERT INTO Clinic VALUES (3000, 'ABCDogs', '786th Ave', '8001231234');
    INSERT INTO Clinic VALUES (4000, 'ABCats', '135th Blvd', '8001237890');
    INSERT INTO Clinic VALUES (5000, 'PetCare Clinic', '10th st', '8008909753');

    -- Insert Staff
    INSERT INTO Staff VALUES (1001, 'Alice Baker', 'address1', '1232343456',  to_date('11/16/1990', 'mm/dd/yyyy'), 'Manager', 10000, 1000);
    INSERT INTO Staff VALUES (1002, 'Bob Carp', 'address2', '1234567890',  to_date('12/06/1998', 'mm/dd/yyyy'), 'Groomer', 5000, 1000);
    INSERT INTO Staff VALUES (1003, 'Charlie Davis', 'address3', '1231231234',  to_date('07/24/1980', 'mm/dd/yyyy'), 'Vet', 11000, 1000);
    INSERT INTO Staff VALUES (1004, 'Danielle Espina', 'address4', '1230987654',  to_date('01/30/1983', 'mm/dd/yyyy'), 'Vet', 11000, 1000);
    INSERT INTO Staff VALUES (1005, 'Eve Fisher', 'address5', '1239876543',  to_date('04/01/2000', 'mm/dd/yyyy'), 'Groomer', 5000, 1000);

    -- Insert Owner
    INSERT INTO Owner VALUES (1101, 'Alice', 'address1', '1232343456');
    INSERT INTO Owner VALUES (1102, 'Barbara', 'address6', '1231234567');
    INSERT INTO Owner VALUES (1103, 'Clara', 'address7', '1230987654');
    INSERT INTO Owner VALUES (1104, 'Damian', 'address8', '1234567456');
    INSERT INTO Owner VALUES (1105, 'Edna', 'address9', '8901234567');

    -- Insert Pet
    INSERT INTO Pet VALUES (1011, 'Spots', to_date('01/01/2010', 'mm/dd/yyyy'), 'Dog', 'Dalmatian', 'White', 1101);
    INSERT INTO Pet VALUES (1012, 'Boots', to_date('02/02/2012', 'mm/dd/yyyy'), 'Cat', 'Tabby', 'Orange', 1102);
    INSERT INTO Pet VALUES (1013, 'Oreo', to_date('03/03/2018', 'mm/dd/yyyy'), 'Cat', 'Shorthair', 'Gray', 1103);
    INSERT INTO Pet VALUES (1014, 'Sparky', to_date('02/29/2012', 'mm/dd/yyyy'), 'Dog', 'Bicheom', 'White', 1104);
    INSERT INTO Pet VALUES (1015, 'Nemo', to_date('05/05/2010', 'mm/dd/yyyy'), 'Fish', 'Goldfish', 'Gold', 1105);

    -- Insert Examination
    INSERT INTO Examination VALUES (1111, 'XYZ', 'ABC', to_date('12/01/2022', 'mm/dd/yyyy'), 'ZZZ', 1000, 1011);
    INSERT INTO Examination VALUES (1112, 'WXY', 'ABC', to_date('12/02/2022', 'mm/dd/yyyy'), 'YYY', 1000, 1012);
    INSERT INTO Examination VALUES (1113, 'VWX', 'ABC', to_date('12/03/2022', 'mm/dd/yyyy'), 'XXX', 1000, 1013);
    INSERT INTO Examination VALUES (1114, 'UVW', 'ABC', to_date('12/04/2022', 'mm/dd/yyyy'), 'VVV', 1000, 1014);
    INSERT INTO Examination VALUES (1115, 'TUV', 'ABC', to_date('12/05/2022', 'mm/dd/yyyy'), 'UUU', 1000, 1015);

    """
cursor.execute(query)

# Select data
query = """
    Select s.staffNo, s.staffName
    From clinic c, staff s
    Where c.clinicNo = s.clinicNo and c.address like '123rd St';

    Select o.ownerName
    From examination e, pet p, owner o
    Where e.petNo = p.petNo and p.ownerNo = o.ownerNo and dateSeen = to_date('12/01/2022', 'mm/dd/yyyy');

    Select p.*
    From Pet p, Owner o
    Where p.ownerNo = o.ownerNo AND ownerName like 'Alice%';

    Select count(*)
    From Pet p, Examination e
    Where p.petNo = e.petNo and species like 'Dog' and chiefComplaint like 'XYZ';

    Insert into examination values (1116, 'STU', 'ABC', to_date('12/06/2022', 'mm/dd/yyyy'), 'TTT', 1000, 1011);
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
