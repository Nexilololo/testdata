# 📚 Databases 1 — Exam Cheat Sheet
*EFREI S4 | All Chapters*

---

## Chapter 0 — Introduction to Databases

### Key Definitions
| Term | Definition |
|------|-----------|
| **Data** | A raw value with a meaning and context (e.g., "1880" alone is data) |
| **Information** | Data with an interpretation (e.g., "EFREI was founded in 1880") |
| **Database (DB)** | Organized collection of data for a specific domain, designed for access & manipulation |
| **DBMS** | Software dedicated to managing a DB (MySQL, Oracle, PostgreSQL, SQLite) |
| **Schema** | Description/structure of the database (metadata) |

### Problems with Traditional File Storage (why DBMS?)
- **Data redundancy** → same data stored many times → inconsistency
- **No data integrity** → no rules to ensure correctness
- **No concurrency** → multiple users can't work simultaneously
- **No security** → no fine-grained access control
- **Difficult to query/search** across files

### ANSI/SPARC 3-Level Architecture
```
┌─────────────────────────────────┐
│       EXTERNAL LEVEL            │  ← Individual user views (subsets)
├─────────────────────────────────┤
│     CONCEPTUAL/LOGICAL LEVEL    │  ← Global view, all data & links (the "Schema")
├─────────────────────────────────┤
│       PHYSICAL LEVEL            │  ← How data is stored on disk (blocks, indices)
└─────────────────────────────────┘
```
- **Logical independence**: Change conceptual without affecting external
- **Physical independence**: Change physical without affecting conceptual

### Merise Design Phases
```
Requirements → CDM → LDM → PDM → Implementation
```

---

## Chapter 1 — Conceptual Data Model (CDM)

### Core Components

| Component | Description | Notation |
|-----------|------------|---------|
| **Entity** | Object/concept with independent existence (e.g., `Student`) | Rectangle |
| **Attribute** | Property of an entity (e.g., `name`, `birth_date`) | Oval/field |
| **Identifier** | Attribute that uniquely identifies instances | **Underlined** |
| **Relationship** | Named link between entities (e.g., `Enrolls In`) | Diamond/Ellipse |
| **Relationship Attribute** | Data belonging to a relationship (e.g., `grade` on `Enrolls`) | Attribute on relationship |
| **Weak Entity** | Entity that depends on another entity for existence | Double rectangle |

### Cardinalities (min, max)
| Notation | Meaning |
|----------|---------|
| `(0,1)` | Optional, at most one |
| `(1,1)` | Mandatory, exactly one |
| `(0,n)` | Optional, zero or many |
| `(1,n)` | Mandatory, one or many |
| `(1,1)R` | Weak entity (relative identification) |

### Reading Cardinalities
> Read from the **entity** outward toward the **relationship**
> 
> **Example**: `Student (1,n) ── Enrolls ── (0,n) Course`
> - A Student enrolls in **1 to n** courses
> - A Course has **0 to n** students enrolled

### Relationship Types
- **Binary**: Between 2 entities
- **Ternary (N-ary)**: Between 3+ entities (always becomes a join table in LDM)
- **Recursive**: An entity linked to itself (e.g., `Employee` manages `Employee`)
- **Weak (Relative)**: Weak entity linked to parent with `(1,1)R`

### Common CDM Mistakes to Avoid
- Never put a relationship identifier (identifiers belong only to entities)
- A weak entity's identifier is partial — it only makes sense combined with parent's key
- Cardinalities go **on the entity side** (not on the relationship side)

---

## Chapter 2 — Logical Data Model (LDM)

### Key Terms
| Term | Definition |
|------|-----------|
| **Relation (Table)** | A set of named columns and rows |
| **Tuple (Row)** | One record in a table |
| **Attribute (Column)** | A named field of a relation |
| **Domain** | Set of allowed values for an attribute |
| **Primary Key (PK)** | Minimal set of attributes that uniquely identify each tuple — **underlined** |
| **Foreign Key (FK)** | Attribute referencing another table's PK — prefixed with `#` |
| **Schema/Intention** | The structure definition: `R(A1:D1, A2:D2, ...)` |
| **Extension/Instance** | The actual data rows at a given moment |

### ⭐ CDM → LDM Mapping Rules (CRITICAL)

#### Rule 1 — Every Entity → Table
- Entity name = table name
- Identifier = **Primary Key**
- Other attributes = columns
```
Entity: Student(student_id, name, birth_date)
→ Table: Student(student_id, name, birth_date)
                ───────────
```

#### Rule 2 — Binary (X,1)—(X,n) Relationship (One-to-Many)
- **No new table created**
- PK of the "**1**" side goes as **FK into the "n" side**
```
Student (1,1) ── Lives In ── (0,n) City
→ Student(student_id, name, #city_id)   ← city_id is FK
  City(city_id, city_name)
```

#### Rule 3 — Binary (X,n)—(X,n) Relationship (Many-to-Many)
- **New join table created**
- PK = concatenation of both entities' PKs
- Any relationship attributes go into this new table
```
Student (0,n) ── Enrolls ── (0,n) Course    [grade is attr on Enrolls]
→ Student(student_id, name)
  Course(course_id, title)
  Enrolls(#student_id, #course_id, grade)
          ──────────────────────────────
```

#### Rule 4 — N-ary Relationship (3+ Entities)
- **Always creates a new join table**
- PK = concatenation of all entities' PKs
```
Teacher (0,n) ── Teaches ── (0,n) Course in (0,n) Room
→ Teaches(#teacher_id, #course_id, #room_id, schedule)
          ────────────────────────────────────
```

#### Rule 5 — Weak Entity
- Receives parent's PK as part of its own **composite PK** + as **FK**
```
Order (1,1)R ── Contains ── (1,n) Product
→ OrderLine(#order_id, line_num, quantity, #product_id)
             ───────────────────
```

#### Rule 6 — Recursive Relationship
- **(0,1)–(0,n)**: Add a self-referencing FK in the same table
  ```
  Employee(emp_id, name, #manager_id)  ← manager_id → emp_id
  ```
- **(0,n)–(0,n)**: New table with two FKs to the same table
  ```
  Friendship(#emp_id_1, #emp_id_2)
  ```

### Notation Summary
```
TableName(PK_col, normal_col, #FK_col)
          ──────                ───────
```
- PK → underlined
- FK → prefixed with `#`

---

## Chapter 3 — SQL DDL & DML

### SQL Language Categories
| Category | Purpose | Commands |
|----------|---------|---------|
| **DDL** | Define structure | `CREATE`, `ALTER`, `DROP` |
| **DML** | Manipulate data | `INSERT`, `UPDATE`, `DELETE` |
| **DQL** | Query data | `SELECT` |
| **DCL** | Control access | `GRANT`, `REVOKE` |
| **TCL** | Transactions | `COMMIT`, `ROLLBACK` |

### DDL — Database & Table Management

```sql
-- Database
CREATE DATABASE db_name;
USE db_name;
DROP DATABASE db_name;
SHOW TABLES;
DESCRIBE table_name;  -- or DESC

-- Create Table
CREATE TABLE table_name (
    col1  INT           PRIMARY KEY AUTO_INCREMENT,
    col2  VARCHAR(100)  NOT NULL,
    col3  DECIMAL(8,2)  DEFAULT 0.00,
    col4  DATE,
    col5  BOOLEAN,
    UNIQUE (col2),
    CHECK (col3 >= 0),
    FOREIGN KEY (col_fk) REFERENCES parent_table(parent_pk)
        ON DELETE CASCADE    -- or SET NULL / RESTRICT / NO ACTION
        ON UPDATE CASCADE
);

-- Alter Table
ALTER TABLE table ADD    column_name type;
ALTER TABLE table DROP   COLUMN column_name;
ALTER TABLE table MODIFY COLUMN column_name new_type;
ALTER TABLE table RENAME COLUMN old_name TO new_name;
ALTER TABLE table ADD    CONSTRAINT fk_name FOREIGN KEY (col) REFERENCES t(pk);

-- Drop / Truncate
DROP TABLE table_name;
TRUNCATE TABLE table_name;  -- empties table, resets AUTO_INCREMENT
```

### Data Types Reference
| Category | Types |
|----------|-------|
| **Integer** | `TINYINT`, `SMALLINT`, `INT`, `BIGINT` |
| **Decimal** | `FLOAT`, `DOUBLE`, `DECIMAL(precision, scale)` |
| **String** | `CHAR(n)` (fixed), `VARCHAR(n)` (variable), `TEXT` |
| **Date/Time** | `DATE` (YYYY-MM-DD), `TIME`, `DATETIME`, `YEAR` |
| **Other** | `BOOLEAN` (= TINYINT 1), `BLOB` (binary) |

### Column Constraints
| Constraint | Meaning |
|-----------|---------|
| `PRIMARY KEY` | Unique + NOT NULL identifier |
| `NOT NULL` | Cannot be empty |
| `UNIQUE` | All values must differ (NULLs allowed) |
| `DEFAULT value` | Fallback if no value given |
| `AUTO_INCREMENT` | Auto-increments integer on insert |
| `CHECK (expr)` | Custom validation rule |
| `FOREIGN KEY ... REFERENCES` | Referential integrity |

### Referential Integrity Actions
| Action | On Parent Delete/Update |
|--------|------------------------|
| `CASCADE` | Propagate change to children |
| `SET NULL` | Set FK to NULL |
| `RESTRICT` | **Block** deletion if children exist |
| `NO ACTION` | Similar to RESTRICT (default) |

### DML — Data Manipulation

```sql
-- INSERT
INSERT INTO table (col1, col2, col3) VALUES (val1, val2, val3);
INSERT INTO table VALUES (val1, val2, val3);  -- all columns in order

-- UPDATE (⚠️ always add WHERE unless intentional)
UPDATE table SET col1 = val1, col2 = val2 WHERE condition;

-- DELETE (⚠️ always add WHERE unless intentional)
DELETE FROM table WHERE condition;

-- TRUNCATE (drops all rows, faster than DELETE without WHERE)
TRUNCATE TABLE table;
```

> [!WARNING]
> Forgetting `WHERE` in `UPDATE` or `DELETE` modifies/deletes **ALL rows**!

### Insertion Order Rules
When inserting with FK constraints:
1. Insert **parent** tables first
2. Then insert **child** tables (the ones with FK)

---

## Chapter 4 — Query Algebra & SQL SELECT

### Relational Algebra Operators

| Symbol | Name | SQL Equivalent | Description |
|--------|------|---------------|-------------|
| **σ** (sigma) | Selection | `WHERE` | Filter rows by condition |
| **π** (pi) | Projection | `SELECT [DISTINCT]` | Select specific columns |
| **ρ** (rho) | Rename | `AS` | Rename table or column |
| **×** | Cartesian Product | `CROSS JOIN` | All combinations of tuples |
| **⋈** | Natural Join | `JOIN ... ON` | Join on common attributes |
| **⋈θ** | Theta Join | `JOIN ... ON condition` | Join with a condition |
| **∪** | Union | `UNION` | Rows in R1 OR R2 |
| **∩** | Intersection | `INTERSECT` | Rows in R1 AND R2 |
| **−** | Difference | `EXCEPT` / `MINUS` | Rows in R1 but NOT R2 |

### Full SELECT Syntax (in execution order)

```sql
SELECT   [DISTINCT] col1, col2, aggregate(col3) AS alias
FROM     table1
[JOIN    table2 ON table1.fk = table2.pk]
[WHERE   condition]           -- Filter rows BEFORE grouping
[GROUP BY col1, col2]         -- Group rows
[HAVING  aggregate_condition] -- Filter AFTER grouping
[ORDER BY col [ASC|DESC]]     -- Sort results
[LIMIT   n];                  -- Limit number of results
```

**Execution order**: `FROM → JOIN → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT`

### JOIN Types
```sql
-- INNER JOIN (only matching rows)
SELECT * FROM A INNER JOIN B ON A.id = B.a_id;

-- LEFT JOIN (all from A, NULLs if no match in B)
SELECT * FROM A LEFT JOIN B ON A.id = B.a_id;

-- RIGHT JOIN (all from B, NULLs if no match in A)
SELECT * FROM A RIGHT JOIN B ON A.id = B.a_id;

-- CROSS JOIN (cartesian product)
SELECT * FROM A CROSS JOIN B;

-- SELF JOIN (recursive)
SELECT e.name, m.name AS manager
FROM Employee e
JOIN Employee m ON e.manager_id = m.emp_id;
```

### Aggregate Functions
| Function | Description |
|----------|------------|
| `COUNT(*)` | Count all rows |
| `COUNT(col)` | Count non-NULL values |
| `COUNT(DISTINCT col)` | Count distinct values |
| `SUM(col)` | Sum of values |
| `AVG(col)` | Average of values |
| `MIN(col)` | Minimum value |
| `MAX(col)` | Maximum value |

> [!IMPORTANT]
> Aggregate functions **cannot** be used in `WHERE` — use `HAVING` instead.

### WHERE vs HAVING
```sql
-- WHERE: filter individual rows (before grouping)
SELECT department, COUNT(*) 
FROM Employee
WHERE salary > 2000               -- ✅ filters rows first
GROUP BY department
HAVING COUNT(*) > 5;              -- ✅ filters groups after aggregation
```

### GROUP BY Rules
- Every column in `SELECT` that is NOT inside an aggregate must be in `GROUP BY`
- `HAVING` filters **groups**, `WHERE` filters **rows**

### Set Operations
```sql
-- Same column count and compatible types required

SELECT col FROM T1
UNION          -- removes duplicates
SELECT col FROM T2;

SELECT col FROM T1
UNION ALL      -- keeps duplicates (faster)
SELECT col FROM T2;

SELECT col FROM T1
INTERSECT      -- rows common to both
SELECT col FROM T2;

SELECT col FROM T1
EXCEPT         -- rows in T1 not in T2 (MySQL uses MINUS)
SELECT col FROM T2;
```

### Subqueries

```sql
-- Scalar subquery (returns 1 value)
SELECT * FROM Product WHERE price = (SELECT MAX(price) FROM Product);

-- IN subquery (list of values)
SELECT * FROM Student WHERE student_id IN (
    SELECT student_id FROM Enrollment WHERE course_id = 5
);

-- NOT IN
SELECT * FROM Student WHERE student_id NOT IN (
    SELECT student_id FROM Enrollment
);

-- EXISTS (checks if subquery returns any rows)
SELECT * FROM Customer c WHERE EXISTS (
    SELECT 1 FROM Order o WHERE o.customer_id = c.customer_id
);

-- Correlated subquery (references outer query)
SELECT name, salary FROM Employee e
WHERE salary > (SELECT AVG(salary) FROM Employee WHERE dept = e.dept);
```

### Useful Clauses & Functions

```sql
-- Aliases
SELECT col AS new_name FROM table AS t_alias;

-- DISTINCT
SELECT DISTINCT city FROM Customer;

-- BETWEEN
WHERE age BETWEEN 18 AND 25;       -- inclusive

-- LIKE (pattern matching)
WHERE name LIKE 'A%';              -- starts with A
WHERE name LIKE '%son';            -- ends with son
WHERE name LIKE '_a%';             -- second letter is 'a'
WHERE name LIKE '%ar%';            -- contains 'ar'

-- IS NULL / IS NOT NULL
WHERE manager_id IS NULL;

-- ORDER BY
ORDER BY salary DESC, name ASC;

-- LIMIT
LIMIT 10;
LIMIT 5 OFFSET 10;   -- skip 10, return next 5
```

---

## Quick Reference: Full CDM → SQL Pipeline

```
1. TEXT ANALYSIS
   → Identify entities (nouns) and relationships (verbs)
   → Determine attributes and identifiers

2. CDM (Entity-Relationship Diagram)
   → Draw entities with identifiers and attributes
   → Connect with relationships and cardinalities (min, max)

3. LDM (Relational Schema)
   → Apply 5 mapping rules
   → Result: TableName(PK, col, #FK)

4. SQL DDL (Physical Implementation)
   → CREATE TABLE statements in correct order
   → Apply all constraints

5. SQL DML (Data Population)
   → INSERT parent tables first, then children

6. SQL SELECT (Queries)
   → Apply SELECT/FROM/JOIN/WHERE/GROUP BY/HAVING/ORDER BY
```

---

## Exam Tips ⭐

| Topic | Key Points |
|-------|-----------|
| **Cardinalities** | Read from entity → relationship; (min, max) tells you participation |
| **Weak entity** | Always `(1,1)R`, gets parent PK in its composite PK |
| **LDM Rule 2** | FK goes to the **n-side** (many side) |
| **LDM Rule 3** | Many-to-many → **always new table** |
| **INSERT order** | Parents before children (FK constraint) |
| **WHERE vs HAVING** | `WHERE` before GROUP BY, `HAVING` after |
| **GROUP BY** | Non-aggregated SELECT columns must be in GROUP BY |
| **Subquery in WHERE** | Use `IN`, `EXISTS`, `= (scalar)` |
| **JOIN** | INNER = only matches; LEFT = all from left + NULLs |
| **NULL** | Use `IS NULL` not `= NULL`; NULLs excluded from aggregates |
