USE inst_db;

ALTER TABLE customer
    ADD CONSTRAINT chk_cust_email CHECK (Cust_Email REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$');

ALTER TABLE instrument
    ADD CONSTRAINT chk_inst_condition CHECK (Inst_Condition IN ('New', 'B-Stock', 'Used - Excellent', 'Used - Good', 'Used - Fair', 'Vintage')),
    ADD CONSTRAINT chk_inst_weight CHECK (Inst_Weight > 0),
    ADD CONSTRAINT chk_sale_price CHECK (Sale_Price > 0);

ALTER TABLE rent
    ADD CONSTRAINT chk_rent_monthly CHECK (Rent_Monthly > 0);

ALTER TABLE task
    ADD CONSTRAINT chk_task_duration CHECK (Task_Duration > 0);

ALTER TABLE part
    ADD CONSTRAINT chk_part_unitcost CHECK (Part_UnitCost >= 0),
    ADD CONSTRAINT chk_stock_qty CHECK (Stock_Qty >= 0);

ALTER TABLE consumption
    ADD CONSTRAINT chk_consumption_qty CHECK (quantity > 0);

ALTER TABLE supply
    ADD CONSTRAINT chk_warranty_date CHECK (Warranty_End >= Order_Date);

DROP TRIGGER IF EXISTS trg_check_rental_insert;
DELIMITER //
CREATE TRIGGER trg_check_rental_insert
BEFORE INSERT ON rent
FOR EACH ROW
BEGIN
    IF EXISTS (
        SELECT 1 FROM instrument 
        WHERE Inst_Serial = NEW.Inst_Serial 
        AND id_cust_owner IS NOT NULL 
        AND id_cust_owner != NEW.id_cust
    ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Instrument is already owned by someone else and cannot be rented to this customer.';
    END IF;
END;
//
DELIMITER ;

DROP TRIGGER IF EXISTS trg_check_rental_update;
DELIMITER //
CREATE TRIGGER trg_check_rental_update
BEFORE UPDATE ON rent
FOR EACH ROW
BEGIN
    IF EXISTS (
        SELECT 1 FROM instrument 
        WHERE Inst_Serial = NEW.Inst_Serial 
        AND id_cust_owner IS NOT NULL 
        AND id_cust_owner != NEW.id_cust
    ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Instrument is already owned by someone else and cannot be rented to this customer.';
    END IF;
END;
//
DELIMITER ;

DROP TRIGGER IF EXISTS trg_check_stock;
DELIMITER //
CREATE TRIGGER trg_check_stock
BEFORE INSERT ON consumption
FOR EACH ROW
BEGIN
    DECLARE current_stock INT;
    SELECT Stock_Qty INTO current_stock FROM part WHERE Part_Ref = NEW.Part_Ref;
    
    IF current_stock < NEW.quantity THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Not enough stock available for part';
    END IF;
END;
//
DELIMITER ;

DROP TRIGGER IF EXISTS trg_reduce_stock;
DELIMITER //
CREATE TRIGGER trg_reduce_stock
AFTER INSERT ON consumption
FOR EACH ROW
BEGIN
    UPDATE part SET Stock_Qty = Stock_Qty - NEW.quantity WHERE Part_Ref = NEW.Part_Ref;
END;
//
DELIMITER ;
