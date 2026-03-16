# Final prompt used
You work in the field of [music retail, specialized rentals, and professional instrument maintenance]. Your [company] is involved in the domain of [high-end instrument sales, recurring rental subscriptions, and expert luthiery/repair services]. It is a [company] such as [Thomann or Guitar Center]. [We have collected data regarding our complex instrument assemblies (like modular synthesizers or drum kits), technical specifications of individual components, specialized cleaning and repair tasks, and the various raw materials or spare parts required for different types of maintenance]. Take inspiration from the following [websites]: [https://www.thomann.de/ and https://www.stewmac.com/].

Your [company] wants to apply MERISE to design an information system. You are responsible for the analysis part, i.e., gathering the company's requirements.
It has called on a computer engineering student to carry out this project, and you must provide him with the necessary information so that he can then apply the following steps of database design and development himself.

First, establish the data business rules for your [company] in the form of a bulleted list. It must correspond to the information provided by someone who knows how the company works, but not how an information system is built.

Next, based on these rules, provide a raw data dictionary with the following columns, grouped in a table: meaning of the data, type, size in number of characters or digits. 
There should be between 25 and 35 data items. It is used to provide additional information about each data item (size and type) but without any assumptions about how the data will be modeled later.

Provide the business rules and the data dictionary.


# Business Rules
Customers & Transactions: Every customer is identified by unique contact details to manage high-end sales and recurring monthly rental subscriptions.

Instrument Complexity: An instrument can be a single unit (e.g., a vintage guitar) or a complex assembly (e.g., modular synthesizers) comprised of multiple individual components.

Component Specifications: Each component within an assembly has its own technical specifications, such as voltage for synth modules or material for drum shells.

Maintenance & Repairs: When an instrument is brought in for maintenance, the specific cleaning or repair tasks performed by luthiers must be recorded.

Parts & Materials: Every repair task consumes a specific quantity of raw materials or spare parts (e.g., fret wire, solder, or specific potentiometers).

Rentals: A rental subscription is linked to a specific instrument and includes a defined start date and a recurring monthly fee.

Inventory Management: The system tracks stock levels for both finished instruments and individual spare parts used in the workshop.

Workforce: Every maintenance task is assigned to a specific expert luthier or technician responsible for the repair.


# Data Dictionary

<img width="762" height="699" alt="image" src="https://github.com/user-attachments/assets/e8c5f324-c891-4918-b864-babf944d854e" />


# CDM
<img width="911" height="546" alt="image" src="https://github.com/user-attachments/assets/92b2e93b-070f-4cde-92a6-422702b07fb7" />


# LDM (Logical Data Model)
- **customer** (<ins>id_cust</ins>, Cust_FirstName, Cust_LastName, Cust_Email, Cust_Phone)
- **instrument** (<ins>Inst_Serial</ins>, Inst_Brand, Inst_Model, Inst_Type, Inst_Condition, Inst_Weight, Sale_Price, *id_cust_owner#*)
- **rent** (*<ins>id_cust#</ins>*, *<ins>Inst_Serial#</ins>*, <ins>Rent_Start</ins>, Rent_Monthly)
- **component** (<ins>id_comp</ins>, Comp_Name, Comp_TechSpec)
- **composition** (*<ins>Inst_Serial#</ins>*, *<ins>id_comp#</ins>*, Assy_Name)
- **maintenance** (<ins>id_maint</ins>, Maint_Date, *Inst_Serial#*)
- **task** (<ins>id_task</ins>, Task_Desc, Task_Duration)
- **perform** (*<ins>id_maint#</ins>*, *<ins>id_task#</ins>*, *id_luthier#*)
- **luthier** (<ins>id_luthier</ins>, Luth_Name, Luth_Specialty)
- **part** (<ins>Part_Ref</ins>, Part_Name, Part_UnitCost, Stock_Qty, Wood_Species, Material_Type)
- **consumption** (*<ins>id_maint#</ins>*, *<ins>id_task#</ins>*, *<ins>Part_Ref#</ins>*, quantity)
- **supplier** (<ins>id_supp</ins>, Supp_Name)
- **supply** (*<ins>id_supp#</ins>*, *<ins>Part_Ref#</ins>*, Order_Date, Warranty_End)


# Data Generation Prompt
I am a computer engineering student working on a database project using PostgreSQL. 
Here is my Logical Data Model (LDM) for a high-end music instrument retail, rental, and repair company:

- **customer** (id_cust, Cust_FirstName, Cust_LastName, Cust_Email, Cust_Phone)
- **instrument** (Inst_Serial, Inst_Brand, Inst_Model, Inst_Type, Inst_Condition, Inst_Weight, Sale_Price, id_cust_owner#)
- **rent** (id_cust#, Inst_Serial#, Rent_Start, Rent_Monthly)
- **component** (id_comp, Comp_Name, Comp_TechSpec)
- **composition** (Inst_Serial#, id_comp#, Assy_Name)
- **maintenance** (id_maint, Maint_Date, Inst_Serial#)
- **task** (id_task, Task_Desc, Task_Duration)
- **perform** (id_maint#, id_task#, id_luthier#)
- **luthier** (id_luthier, Luth_Name, Luth_Specialty)
- **part** (Part_Ref, Part_Name, Part_UnitCost, Stock_Qty, Wood_Species, Material_Type)
- **consumption** (id_maint#, id_task#, Part_Ref#, quantity)
- **supplier** (id_supp, Supp_Name)
- **supply** (id_supp#, Part_Ref#, Order_Date, Warranty_End)

Please generate 40 rows of realistic test data for customer, instrument, 
ent and component.
Then generate 20 rows of realistic test data for 	ask, luthier, part, supplier.
Then create meaningful associations for composition, maintenance, perform, consumption, and supply.

Ensure that:
1. Contact info and names are realistic (e.g. valid emails, varied phone numbers).
2. Instruments are high-end brands like Fender, Gibson, Korg, Roland, with varied types (Guitars, Synths, Drumkits). Condition must be one of: 'New', 'B-Stock', 'Used - Excellent', 'Used - Good', 'Used - Fair', 'Vintage'.
3. Rentals reference valid instruments and customers.
4. Maintenance and tasks represent typical luthier operations (e.g., Fret dressing, Synth recap, String replacement).
5. All IDs match up exactly so I don't get foreign key constraint violations during INSERT. 
6. Provide only valid PostgreSQL INSERT INTO statements. Output them in the correct dependency order.
`


# Usage Scenario (Querying the DB)
You are the **Operations and Marketing Manager** for this high-end music instrument retail, rental, and workshop company. You are preparing for the busy summer season when both touring musicians and local students require gear and repairs. You need to analyze the database to answer critical business questions:
1. **Sales & Inventory Oversight**: Which of our high-end instruments are currently in pristine condition, and what is our stock levels for critical fretwire repair materials?
2. **Financial Performance**: What are our highest valued rentals right now, and what is the average cost of materials we are keeping in stock?
3. **Workshop Efficiency**: Which luthiers are performing the longest tasks, and which repair tasks consume the highest quantities of spare parts? 
4. **Targeted Marketing & Operations**: Who are the customers that have submitted an instrument for maintenance but haven't rented anything recently, and which suppliers do we rely on for critical electronic components?

To answer these questions, the .sql queries are designed to explore basic listing (selections), aggregate statistics (grouping), cross-referencing between departments (joins), and finding exceptional cases (nested queries).
