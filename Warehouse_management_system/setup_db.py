import mysql.connector

# Connect to MySQL server
conn = mysql.connector.connect(
    host="localhost",
    user="root",         # your MySQL username
    password="Letmein2272"  # your MySQL password
)
cursor = conn.cursor()

# Create Database
cursor.execute("CREATE DATABASE IF NOT EXISTS InventoryDB")
cursor.execute("USE InventoryDB")

# Create Tables
cursor.execute("""
CREATE TABLE Provider (
    ProviderID INT PRIMARY KEY,
    ProviderName VARCHAR(100) NOT NULL,
    ProviderAddress VARCHAR(200) NOT NULL
)
""")

cursor.execute("""
CREATE TABLE Customer (
    CustomerID INT PRIMARY KEY,
    CustomerName VARCHAR(100) NOT NULL,
    CustomerAddress VARCHAR(200) NOT NULL
)
""")

cursor.execute("""
CREATE TABLE Product (
    ProductID INT PRIMARY KEY,
    ProductCode VARCHAR(100) NOT NULL,
    BarCode VARCHAR(100) NOT NULL,
    ProductName VARCHAR(100) NOT NULL,
    ProductDescription VARCHAR(2000) NOT NULL,
    ProductCategory VARCHAR(100) NOT NULL,
    ReorderQuantity INT NOT NULL,
    PackedWeight DECIMAL(10,2) NOT NULL,
    PackedHeight DECIMAL(10,2) NOT NULL,
    PackedWidth DECIMAL(10,2) NOT NULL,
    PackedDepth DECIMAL(10,2) NOT NULL,
    Refrigerated BOOLEAN NOT NULL
)
""")

cursor.execute("""
CREATE TABLE Warehouse (
    WarehouseID INT PRIMARY KEY,
    WarehouseName VARCHAR(100) NOT NULL,
    IsRefrigerated BOOLEAN NOT NULL
)
""")

cursor.execute("""
CREATE TABLE Location (
    LocationID INT PRIMARY KEY,
    LocationName VARCHAR(100) NOT NULL,
    LocationAddress VARCHAR(200) NOT NULL
)
""")

cursor.execute("""
CREATE TABLE Inventory (
    InventoryID INT PRIMARY KEY,
    QuantityAvailable INT NOT NULL,
    MinimumStockLevel INT NOT NULL,
    MaximumStockLevel INT NOT NULL,
    ReorderPoint INT NOT NULL,
    ProductID INT NOT NULL,
    WarehouseID INT NOT NULL,
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID),
    FOREIGN KEY (WarehouseID) REFERENCES Warehouse(WarehouseID)
)
""")

cursor.execute("""
CREATE TABLE `Order` (
    OrderID INT PRIMARY KEY,
    OrderDate DATE NOT NULL,
    ProviderID INT NOT NULL,
    FOREIGN KEY (ProviderID) REFERENCES Provider(ProviderID)
)
""")

cursor.execute("""
CREATE TABLE OrderDetail (
    OrderDetailID INT PRIMARY KEY,
    OrderID INT NOT NULL,
    ProductID INT NOT NULL,
    OrderQuantity INT NOT NULL,
    ExpectedDate DATE NOT NULL,
    ActualDate DATE,
    FOREIGN KEY (OrderID) REFERENCES `Order`(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
)
""")

cursor.execute("""
CREATE TABLE Transfer (
    TransferID INT PRIMARY KEY,
    ProductID INT NOT NULL,
    FromWarehouseID INT NOT NULL,
    ToWarehouseID INT NOT NULL,
    TransferQuantity INT NOT NULL,
    SentDate DATE NOT NULL,
    ReceivedDate DATE,
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID),
    FOREIGN KEY (FromWarehouseID) REFERENCES Warehouse(WarehouseID),
    FOREIGN KEY (ToWarehouseID) REFERENCES Warehouse(WarehouseID)
)
""")

cursor.execute("""
CREATE TABLE Delivery (
    DeliveryID INT PRIMARY KEY,
    CustomerID INT NOT NULL,
    SalesDate DATE NOT NULL,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
)
""")

cursor.execute("""
CREATE TABLE DeliveryDetail (
    DeliveryDetailID INT PRIMARY KEY,
    DeliveryID INT NOT NULL,
    ProductID INT NOT NULL,
    DeliveryQuantity INT NOT NULL,
    ExpectedDate DATE NOT NULL,
    ActualDate DATE,
    FOREIGN KEY (DeliveryID) REFERENCES Delivery(DeliveryID),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
)
""")

print("✅ InventoryDB created and all tables successfully set up.")

cursor.close()
conn.close()
