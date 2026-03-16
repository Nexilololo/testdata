CREATE DATABASE IF NOT EXISTS inst_db;
USE inst_db;

DROP TABLE IF EXISTS supply;
DROP TABLE IF EXISTS consumption;
DROP TABLE IF EXISTS perform;
DROP TABLE IF EXISTS composition;
DROP TABLE IF EXISTS rent;
DROP TABLE IF EXISTS maintenance;
DROP TABLE IF EXISTS instrument;
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS component;
DROP TABLE IF EXISTS task;
DROP TABLE IF EXISTS luthier;
DROP TABLE IF EXISTS part;
DROP TABLE IF EXISTS supplier;

CREATE TABLE customer (
    id_cust INT AUTO_INCREMENT PRIMARY KEY,
    Cust_FirstName VARCHAR(255) NOT NULL,
    Cust_LastName VARCHAR(255) NOT NULL,
    Cust_Email VARCHAR(255) UNIQUE NOT NULL,
    Cust_Phone VARCHAR(50)
);

CREATE TABLE instrument (
    Inst_Serial VARCHAR(100) PRIMARY KEY,
    Inst_Brand VARCHAR(255) NOT NULL,
    Inst_Model VARCHAR(255) NOT NULL,
    Inst_Type VARCHAR(100) NOT NULL,
    Inst_Condition VARCHAR(50),
    Inst_Weight DECIMAL(8, 2),
    Sale_Price DECIMAL(10, 2),
    id_cust_owner INT,
    FOREIGN KEY (id_cust_owner) REFERENCES customer(id_cust) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE rent (
    id_cust INT,
    Inst_Serial VARCHAR(100),
    Rent_Start DATE,
    Rent_Monthly DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (id_cust, Inst_Serial, Rent_Start),
    FOREIGN KEY (id_cust) REFERENCES customer(id_cust) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Inst_Serial) REFERENCES instrument(Inst_Serial) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE component (
    id_comp INT AUTO_INCREMENT PRIMARY KEY,
    Comp_Name VARCHAR(255) NOT NULL,
    Comp_TechSpec TEXT
);

CREATE TABLE composition (
    Inst_Serial VARCHAR(100),
    id_comp INT,
    Assy_Name VARCHAR(255),
    PRIMARY KEY (Inst_Serial, id_comp),
    FOREIGN KEY (Inst_Serial) REFERENCES instrument(Inst_Serial) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_comp) REFERENCES component(id_comp) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE maintenance (
    id_maint INT AUTO_INCREMENT PRIMARY KEY,
    Maint_Date DATE NOT NULL,
    Inst_Serial VARCHAR(100) NOT NULL,
    FOREIGN KEY (Inst_Serial) REFERENCES instrument(Inst_Serial) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE task (
    id_task INT AUTO_INCREMENT PRIMARY KEY,
    Task_Desc TEXT NOT NULL,
    Task_Duration INT NOT NULL
);

CREATE TABLE luthier (
    id_luthier INT AUTO_INCREMENT PRIMARY KEY,
    Luth_Name VARCHAR(255) NOT NULL,
    Luth_Specialty VARCHAR(255)
);

CREATE TABLE perform (
    id_maint INT,
    id_task INT,
    id_luthier INT NOT NULL,
    PRIMARY KEY (id_maint, id_task),
    FOREIGN KEY (id_maint) REFERENCES maintenance(id_maint) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_task) REFERENCES task(id_task) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_luthier) REFERENCES luthier(id_luthier) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE part (
    Part_Ref VARCHAR(100) PRIMARY KEY,
    Part_Name VARCHAR(255) NOT NULL,
    Part_UnitCost DECIMAL(10, 2) NOT NULL,
    Stock_Qty INT NOT NULL,
    Wood_Species VARCHAR(255),
    Material_Type VARCHAR(255)
);

CREATE TABLE consumption (
    id_maint INT,
    id_task INT,
    Part_Ref VARCHAR(100),
    quantity INT NOT NULL,
    PRIMARY KEY (id_maint, id_task, Part_Ref),
    FOREIGN KEY (id_maint, id_task) REFERENCES perform(id_maint, id_task) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Part_Ref) REFERENCES part(Part_Ref) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE supplier (
    id_supp INT AUTO_INCREMENT PRIMARY KEY,
    Supp_Name VARCHAR(255) NOT NULL
);

CREATE TABLE supply (
    id_supp INT,
    Part_Ref VARCHAR(100),
    Order_Date DATE,
    Warranty_End DATE,
    PRIMARY KEY (id_supp, Part_Ref),
    FOREIGN KEY (id_supp) REFERENCES supplier(id_supp) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Part_Ref) REFERENCES part(Part_Ref) ON DELETE CASCADE ON UPDATE CASCADE
);
