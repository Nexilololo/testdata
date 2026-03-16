# Database Project - Video Presentation Script

**Target Duration:** ~10-12 minutes
**Database Theme:** High-End Music Instrument Retail, Rental, and Workshop (inst_db)

---

## Part 1: Introduction & Design (3-4 minutes)

**[Screen: Show the CDM and LDM diagrams from README.md]**

**Speaker:**
"Hello, and welcome to our database project presentation. Our database is built for a high-end music instrument company that handles sales, monthly rentals, and a specialized repair workshop. 

### Justifying Modeling Choices
Instead of detailing every single entity, I want to highlight the core architectural decisions we made:
1. **Handling Complex Assemblies:** We designed an `instrument` entity that can either be a standalone item or a complex assembly. To manage this, we used a many-to-many relationship with `component`, resolved into the `composition` table. This is perfect for modular synthesizers or custom drum kits where we need to track individual parts.
2. **Maintenance Workflow:** Rather than a simple repair log, we split the workflow into `maintenance` (the event), `task` (the specific job done, like 'fret dressing'), and `perform` (linking the luthier to the task). This allows multiple luthiers to collaborate on a single maintenance ticket.
3. **Inventory Consumption:** We linked the specific repair tasks to stock inventory via the `consumption` table, ensuring that whenever a repair happens, parts like strings or potentiometers are accurately deducted from our `part` stock.

### 3NF Normalization
Our model strictly adheres to the Third Normal Form (3NF). 
- **1NF & 2NF:** All attributes are atomic, and every table has a clear primary key (like `Inst_Serial` or `id_cust`). There are no partial dependencies because all attributes depend entirely on the primary key.
- **3NF:** We ensured there are no transitive dependencies. For example, instead of storing a 'Supplier Phone Number' directly inside the `part` table, we separated it into a `supplier` table and created a `supply` relationship. Every non-key attribute depends *only* on the primary key of its respective table."

---

## Part 2: Physical Model & Integrity (2-3 minutes)

**[Screen: Open MySQL Workbench, showing the creation of the tables]**

**Speaker:**
"Now let's move to the physical implementation in MySQL."

**[Screen: Run `SELECT * FROM instrument LIMIT 5;` and `SELECT * FROM customer LIMIT 5;`]**
"Here you can see the data populated in our `instrument` and `customer` tables, generated to simulate a real-world shop."

**[Screen: Open `2_contraintes.sql` and demonstrate a constraint violation]**
"Data integrity is critical. Let's demonstrate what happens if we try to violate an integrity constraint. In our rules, an instrument cannot have a negative weight. 
*If I try to run:*
`UPDATE instrument SET Inst_Weight = -5 WHERE Inst_Serial = 'SN-DW-36796';`
*[Run query to trigger Error]*
MySQL blocks this update because we implemented a `CHECK (Inst_Weight > 0)` constraint, preserving our data integrity.

**[Screen: Demonstrate the Trigger for Rental Ownership]**
"We also have complex business rules. For example, a customer cannot rent an instrument that is already owned by someone else. 
*[Run query to attempt to rent an owned instrument]*
As you can see, our custom Trigger `trg_check_rental_insert` intercepts the INSERT and throws a custom error, preventing impossible business states."

**[Screen: Demonstrate Foreign Key cascading]**
"Finally, we handle referential integrity using `ON DELETE CASCADE`. If a customer wants their account completely wiped from our system:
*[Run query]* `DELETE FROM customer WHERE id_cust = 1;` 
Because of our foreign keys, any rentals associated with Customer 1 are also automatically cleaned up, preventing orphan records."

---

## Part 3: Use Case Demonstration (4-5 minutes)

**[Screen: Open `4_interrogation.sql`]**

**Speaker:**
"Our usage scenario puts us in the shoes of the Operations Manager, preparing for the busy summer season. We need to analyze inventory, financials, and workshop efficiency."

**[Screen: Run Query 15 - Total parts consumed by task]**
"First, let's look at an aggregate query utilizing multiple joins. We want to know which repair tasks consume the most parts."
*[Highlight the code]*
"This query joins `task`, `perform`, and `consumption`. We group by the `Task_Desc` and use the `SUM()` aggregate function on the part quantity. This tells the manager exactly what tasks are draining our hardware stock the fastest."

**[Screen: Run Query 10 - Grouping with CASE]**
"Next, an aggregation showing total instrument weight in our system, broken down by whether the shop owns it or a customer owns it."
*[Highlight the code]*
"We used a `CASE WHEN` statement inside our `GROUP BY` to dynamically categorize `id_cust_owner IS NULL` as 'Shop Owned'. We also added a `HAVING` clause to filter out any grouping that totals less than 10 lbs, which is a great example of advanced filtering on an aggregate."

**[Screen: Run Query 16 or 17 - Nested Queries]**
"Finally, let's look at a nested query. We need to find instruments that have *never* been rented out so they can be put on sale."
*[Highlight the code for Query 17 (NOT EXISTS)]*
"Here, we select from the `instrument` table where `NOT EXISTS` in a subquery checking the `rent` table. It's a highly efficient way to find anti-joins or missing relationships in our operational data."

---

## Part 4: Critical Assessment & Conclusion (1 minute)

**[Screen: Show the final slide or back to the CDM diagram]**

**Speaker:**
"To conclude, while our database successfully models the complex workflows of a high-end music shop, there is always room for improvement.

**Future Improvements:**
1. **Historical Tracking:** Currently, if a customer returns a rental, we delete or overwrite the record. Adding a `rent_history` or archiving system would allow for better long-term financial analytics.
2. **Maintenance Statuses:** Our maintenance table logs the event, but we don't have a concept of 'Status' (e.g., Pending, In Progress, Completed). Adding a workflow state machine would make this a true operational tool for the luthiers.
3. **Price Histories:** Sale prices and part costs change over time. Moving the `Sale_Price` into a temporal table would allow us to track inflation and seasonal pricing shifts.

Thank you for watching our presentation!"
