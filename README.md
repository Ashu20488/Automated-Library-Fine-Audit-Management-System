# Automated Library & Fine Management System

A Python-based desktop application integrated with MySQL (PL/SQL) to automate library operations, book issuing/returning, fine calculations, and audit log tracking.

## 🚀 Features
* **Book & Member Management:** Keep track of available books and registered library members.
* **Automated Book Issue & Return:** Handled seamlessly via PL/SQL stored procedures (`IssueBook` and `ReturnBook`).
* **Dynamic Fine Calculation:** Automatically calculates late return fines based on rules.
* **Audit Trail & Verification:** Logs every major transaction into an `audit_log` table for system transparency and security.
* **Interactive GUI:** Built with Python to provide a user-friendly dashboard showing summary metrics and active records.

## 🛠️ Tech Stack
* **Frontend/Backend Logic:** Python (Tkinter GUI)
* **Database & Procedures:** MySQL, PL/SQL (Stored Procedures, Triggers, Functions)
* **Development Tools:** Visual Studio Code, MySQL Workbench

## 📊 Project Output Screenshots
1. **Schema & Tables:** Contains relational tables like `books`, `members`, `borrow_records`, `fines`, and `audit_log`.
2. **PL/SQL Procedures:** Compiled stored procedures (`IssueBook`, `ReturnBook`).
3. **Python GUI Dashboard:** Interactive interface displaying summary cards and records.
4. **Audit Log Verification:** Tracks live transactional audit messages.

## ⚙️ How to Run
1. Clone this repository or download the project files.
2. Set up your MySQL database and execute the required schema scripts.
3. Configure your database credentials in the Python script.
4. Run the application:
   ```bash
   python app.py
