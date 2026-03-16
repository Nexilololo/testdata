USE inst_db;

SELECT DISTINCT Inst_Model 
FROM instrument 
WHERE Inst_Condition IN ('New', 'B-Stock') 
ORDER BY Inst_Model ASC;

SELECT Cust_FirstName, Cust_LastName, Cust_Phone 
FROM customer 
WHERE Cust_LastName LIKE 'M%' AND Cust_Phone IS NOT NULL;

SELECT Inst_Serial, Inst_Brand, Inst_Model, Sale_Price 
FROM instrument 
WHERE Sale_Price BETWEEN 1000.00 AND 3000.00 
ORDER BY Sale_Price DESC;

SELECT id_maint, Maint_Date, Inst_Serial 
FROM maintenance 
WHERE Maint_Date BETWEEN '2025-01-01' AND '2025-03-31' 
ORDER BY Maint_Date ASC;

SELECT Part_Ref, Part_Name, Material_Type 
FROM part 
WHERE Material_Type IN ('Nickel', 'Bone');

SELECT id_cust, COUNT(Inst_Serial) AS Total_Rentals, ROUND(AVG(Rent_Monthly), 2) AS Avg_Monthly_Rent 
FROM rent 
GROUP BY id_cust 
HAVING COUNT(Inst_Serial) > 1;

SELECT Material_Type, SUM(Stock_Qty * Part_UnitCost) AS Total_Stock_Value 
FROM part 
GROUP BY Material_Type 
HAVING SUM(Stock_Qty * Part_UnitCost) > 500.00;

SELECT id_luthier, COUNT(DISTINCT id_task) AS Distinct_Tasks_Performed 
FROM perform 
GROUP BY id_luthier 
HAVING COUNT(DISTINCT id_task) >= 3;

SELECT Task_Desc, MAX(Task_Duration) AS Max_Task_Duration_Min 
FROM task 
GROUP BY Task_Desc 
HAVING MAX(Task_Duration) > 60;

SELECT CASE WHEN id_cust_owner IS NULL THEN 'Shop Owned' ELSE 'Customer Owned' END AS Ownership, 
       SUM(Inst_Weight) AS Total_Weight 
FROM instrument 
GROUP BY CASE WHEN id_cust_owner IS NULL THEN 'Shop Owned' ELSE 'Customer Owned' END 
HAVING SUM(Inst_Weight) > 10.0;

SELECT c.Cust_FirstName, c.Cust_LastName, i.Inst_Brand, i.Inst_Model 
FROM customer c 
JOIN instrument i ON c.id_cust = i.id_cust_owner;

SELECT p.Part_Name, p.Part_Ref, s.Supp_Name, sup.Warranty_End 
FROM part p 
LEFT JOIN supply sup ON p.Part_Ref = sup.Part_Ref 
LEFT JOIN supplier s ON sup.id_supp = s.id_supp;

SELECT l.Luth_Name, t.Task_Desc, m.Inst_Serial, m.Maint_Date 
FROM luthier l 
JOIN perform p ON l.id_luthier = p.id_luthier 
JOIN task t ON p.id_task = t.id_task 
JOIN maintenance m ON p.id_maint = m.id_maint;

SELECT i.Inst_Serial, i.Inst_Brand, comp.Comp_Name, c.Assy_Name 
FROM instrument i 
JOIN composition c ON i.Inst_Serial = c.Inst_Serial 
JOIN component comp ON c.id_comp = comp.id_comp 
WHERE i.Inst_Type = 'Synthesizer';

SELECT t.Task_Desc, SUM(c.quantity) AS Total_Parts_Consumed 
FROM task t 
JOIN perform p ON t.id_task = p.id_task 
JOIN consumption c ON p.id_maint = c.id_maint AND p.id_task = c.id_task 
GROUP BY t.Task_Desc 
ORDER BY Total_Parts_Consumed DESC;

SELECT Cust_Email 
FROM customer 
WHERE id_cust IN (
    SELECT r.id_cust 
    FROM rent r 
    JOIN instrument i ON r.Inst_Serial = i.Inst_Serial 
    WHERE i.Sale_Price > 2500.00
);

SELECT i.Inst_Serial, i.Inst_Brand, i.Inst_Model 
FROM instrument i 
WHERE NOT EXISTS (
    SELECT 1 
    FROM rent r 
    WHERE r.Inst_Serial = i.Inst_Serial
);

SELECT Inst_Serial, Inst_Brand, Inst_Model, Inst_Weight 
FROM instrument 
WHERE Inst_Weight > ALL (
    SELECT Inst_Weight 
    FROM instrument 
    WHERE Inst_Type = 'Electric Guitar' AND Inst_Weight IS NOT NULL
);

SELECT Luth_Name, Luth_Specialty 
FROM luthier 
WHERE id_luthier = ANY (
    SELECT p.id_luthier 
    FROM perform p 
    JOIN task t ON p.id_task = t.id_task 
    WHERE t.Task_Duration > 180
);

SELECT Part_Name, Part_Ref, Stock_Qty 
FROM part 
WHERE Part_Ref NOT IN (
    SELECT Part_Ref 
    FROM consumption
);
