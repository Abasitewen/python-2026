"""
Create the small "company" dataset used in notebooks 02, 03 and extra_scipy_sklearn.

Running this script (re)creates three files in the current directory:
  - employees.csv    (employee_id, name, department_id, salary, tenure_years)
  - departments.csv  (department_id, department_name, location)
  - company.db       (SQLite database with the same two tables)

The data are synthetic and generated with a fixed random seed, so every run
produces exactly the same files. Salary grows with tenure and depends on the
department, so there is something to find in the plots and tests.
"""
import sqlite3

import numpy as np
import pandas as pd

SEED = 2026

DEPARTMENTS = [
    # department_id, department_name, location, n_employees, base_salary
    (1, "Engineering", "Building A", 80, 70_000),
    (2, "Sales", "Building B", 60, 52_000),
    (3, "Human Resources", "Building A", 20, 45_000),
    (4, "Marketing", "Building B", 40, 50_000),
]

FIRST_NAMES = [
    "Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Hana", "Ivan",
    "Julia", "Karim", "Laura", "Marco", "Nadia", "Oscar", "Paola", "Quentin",
    "Rosa", "Sven", "Tanja", "Ugo", "Vera", "Walter", "Xenia", "Yusuf", "Zoe",
]


def make_tables(seed=SEED):
    rng = np.random.default_rng(seed)
    rows = []
    employee_id = 101
    for dep_id, _, _, n, base in DEPARTMENTS:
        tenure = np.round(np.clip(rng.gamma(shape=2.0, scale=3.0, size=n), 0, 35), 1)
        salary = base + 2_500 * tenure + rng.normal(0, 7_000, size=n)
        salary = np.round(salary, -2)  # round to the nearest 100
        for t, s in zip(tenure, salary):
            rows.append(
                {
                    "employee_id": employee_id,
                    "name": str(rng.choice(FIRST_NAMES)),
                    "department_id": dep_id,
                    "salary": float(s),
                    "tenure_years": float(t),
                }
            )
            employee_id += 1
    employees = pd.DataFrame(rows)
    departments = pd.DataFrame(
        [(d, name, loc) for d, name, loc, _, _ in DEPARTMENTS],
        columns=["department_id", "department_name", "location"],
    )
    return employees, departments


def write_database(employees, departments, path="company.db"):
    """Write both tables to an SQLite file using plain SQL statements."""
    conn = None
    try:
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS employees")
        cur.execute("DROP TABLE IF EXISTS departments")
        cur.execute(
            """
            CREATE TABLE departments (
                department_id   INTEGER PRIMARY KEY,
                department_name TEXT NOT NULL,
                location        TEXT
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE employees (
                employee_id   INTEGER PRIMARY KEY,
                name          TEXT NOT NULL,
                department_id INTEGER REFERENCES departments(department_id),
                salary        REAL,
                tenure_years  REAL
            )
            """
        )
        cur.executemany(
            "INSERT INTO departments VALUES (?, ?, ?)",
            departments.itertuples(index=False, name=None),
        )
        cur.executemany(
            "INSERT INTO employees VALUES (?, ?, ?, ?, ?)",
            employees.itertuples(index=False, name=None),
        )
        conn.commit()
        print(f"{path}: {len(departments)} departments, {len(employees)} employees.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    employees, departments = make_tables()
    employees.to_csv("employees.csv", index=False)
    departments.to_csv("departments.csv", index=False)
    print(f"employees.csv: {len(employees)} rows; departments.csv: {len(departments)} rows.")
    write_database(employees, departments)
