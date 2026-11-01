import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            port=3307,
            user="root",
            password="2005",  
            database="library_db"
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Connection Failed: {err}")
        return None

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Automated Library Fine & Audit Management System")
        self.root.geometry("1000x680")
        self.root.configure(bg="#f8fafc")

        # Top Header Banner
        header = tk.Frame(root, bg="#1e40af", height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(
            header, text="📚 Automated Library & Fine Management System", 
            font=("Segoe UI", 16, "bold"), bg="#1e40af", fg="white"
        ).pack(side=tk.LEFT, padx=25)

        # Summary Metric Cards Frame (Dynamic Data)
        stats_frame = tk.Frame(root, bg="#f8fafc")
        stats_frame.pack(fill=tk.X, padx=20, pady=15)

        # Fetch live stats from database
        total_books, active_members, issued_books, total_fines = self.get_dashboard_stats()

        self.card_books = self.create_stat_card(stats_frame, "Total Books", str(total_books), "#3b82f6", 0)
        self.card_members = self.create_stat_card(stats_frame, "Active Members", str(active_members), "#10b981", 1)
        self.card_issued = self.create_stat_card(stats_frame, "Issued Books", str(issued_books), "#f59e0b", 2)
        self.card_fines = self.create_stat_card(stats_frame, "Total Fines (₹)", str(total_fines), "#ef4444", 3)

        # Notebook / Tabs Container
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#f8fafc', borderwidth=0)
        style.configure('TNotebook.Tab', font=('Segoe UI', 10, 'bold'), padding=[18, 8], background='#e2e8f0', foreground='#334155')
        style.map('TNotebook.Tab', background=[('selected', '#1e40af')], foreground=[('selected', 'white')])

        notebook = ttk.Notebook(root)
        notebook.pack(pady=10, padx=20, expand=True, fill="both")

        issue_frame = ttk.Frame(notebook)
        notebook.add(issue_frame, text="  📖 Issue Book  ")
        self.setup_issue_tab(issue_frame)

        return_frame = ttk.Frame(notebook)
        notebook.add(return_frame, text="  🔄 Return Book  ")
        self.setup_return_tab(return_frame)

        records_frame = ttk.Frame(notebook)
        notebook.add(records_frame, text="  📊 View Records & Audit  ")
        self.setup_records_tab(records_frame)

    def get_dashboard_stats(self):
        b_count, m_count, iss_count, fine_sum = 0, 0, 0, 0
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT COUNT(*) FROM books")
                b_count = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM members")
                m_count = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM borrow_records WHERE status='Issued'")
                iss_count = cursor.fetchone()[0]

                cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM fines")
                fine_sum = cursor.fetchone()[0]
            except mysql.connector.Error:
                pass
            finally:
                conn.close()
        return b_count, m_count, iss_count, fine_sum

    def create_stat_card(self, parent, title, value, color, col):
        card = tk.Frame(parent, bg="white", bd=1, relief="solid", highlightbackground="#cbd5e1")
        card.grid(row=0, column=col, padx=10, ipadx=25, ipady=10, sticky="nsew")
        parent.grid_columnconfigure(col, weight=1)

        val_label = tk.Label(card, text=value, font=("Segoe UI", 18, "bold"), bg="white", fg=color)
        val_label.pack()
        tk.Label(card, text=title, font=("Segoe UI", 9, "bold"), bg="white", fg="#64748b").pack()
        return val_label

    def setup_issue_tab(self, frame):
        container = tk.Frame(frame, bg="white", bd=1, relief="solid", highlightbackground="#cbd5e1")
        container.place(relx=0.5, rely=0.5, anchor="center", width=520, height=330)

        tk.Label(container, text="Issue Book Portal", font=("Segoe UI", 13, "bold"), bg="white", fg="#1e40af").pack(pady=15)

        form = tk.Frame(container, bg="white")
        form.pack(pady=5)

        tk.Label(form, text="Book ID:", font=("Segoe UI", 10, "bold"), bg="white", fg="#334155").grid(row=0, column=0, sticky="e", padx=15, pady=10)
        self.issue_book_id = tk.Entry(form, font=("Segoe UI", 10), bg="#f1f5f9", bd=1, relief="solid", width=24)
        self.issue_book_id.grid(row=0, column=1, padx=10, pady=10, ipady=5)

        tk.Label(form, text="Member ID:", font=("Segoe UI", 10, "bold"), bg="white", fg="#334155").grid(row=1, column=0, sticky="e", padx=15, pady=10)
        self.issue_member_id = tk.Entry(form, font=("Segoe UI", 10), bg="#f1f5f9", bd=1, relief="solid", width=24)
        self.issue_member_id.grid(row=1, column=1, padx=10, pady=10, ipady=5)

        tk.Label(form, text="Due Date (YYYY-MM-DD):", font=("Segoe UI", 10, "bold"), bg="white", fg="#334155").grid(row=2, column=0, sticky="e", padx=15, pady=10)
        self.issue_due_date = tk.Entry(form, font=("Segoe UI", 10), bg="#f1f5f9", bd=1, relief="solid", width=24)
        self.issue_due_date.insert(0, "2026-11-30")
        self.issue_due_date.grid(row=2, column=1, padx=10, pady=10, ipady=5)

        tk.Button(
            container, text="Issue Book Now", font=("Segoe UI", 10, "bold"), 
            bg="#2563eb", fg="white", activebackground="#1d4ed8", activeforeground="white",
            bd=0, cursor="hand2", command=self.issue_book
        ).pack(pady=15, ipadx=20, ipady=6)

    def issue_book(self):
        b_id = self.issue_book_id.get()
        m_id = self.issue_member_id.get()
        d_date = self.issue_due_date.get()

        if not b_id or not m_id or not d_date:
            messagebox.showwarning("Input Error", "Kripya saare fields fill karein!")
            return

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.callproc('IssueBook', [int(b_id), int(m_id), d_date])
                conn.commit()
                messagebox.showinfo("Success", "Book Issue Request Successfully Executed!")
                self.refresh_stats()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Failed to issue book: {err}")
            finally:
                conn.close()

    def setup_return_tab(self, frame):
        container = tk.Frame(frame, bg="white", bd=1, relief="solid", highlightbackground="#cbd5e1")
        container.place(relx=0.5, rely=0.5, anchor="center", width=520, height=270)

        tk.Label(container, text="Return Book & Fine Portal", font=("Segoe UI", 13, "bold"), bg="white", fg="#1e40af").pack(pady=15)

        form = tk.Frame(container, bg="white")
        form.pack(pady=5)

        tk.Label(form, text="Record ID:", font=("Segoe UI", 10, "bold"), bg="white", fg="#334155").grid(row=0, column=0, sticky="e", padx=15, pady=10)
        self.return_record_id = tk.Entry(form, font=("Segoe UI", 10), bg="#f1f5f9", bd=1, relief="solid", width=24)
        self.return_record_id.grid(row=0, column=1, padx=10, pady=10, ipady=5)

        tk.Label(form, text="Return Date:", font=("Segoe UI", 10, "bold"), bg="white", fg="#334155").grid(row=1, column=0, sticky="e", padx=15, pady=10)
        self.return_date = tk.Entry(form, font=("Segoe UI", 10), bg="#f1f5f9", bd=1, relief="solid", width=24)
        self.return_date.insert(0, "2026-11-10")
        self.return_date.grid(row=1, column=1, padx=10, pady=10, ipady=5)

        tk.Button(
            container, text="Process Return", font=("Segoe UI", 10, "bold"), 
            bg="#16a34a", fg="white", activebackground="#15803d", activeforeground="white",
            bd=0, cursor="hand2", command=self.return_book
        ).pack(pady=15, ipadx=20, ipady=6)

    def return_book(self):
        r_id = self.return_record_id.get()
        ret_date = self.return_date.get()

        if not r_id or not ret_date:
            messagebox.showwarning("Input Error", "Kripya saare fields fill karein!")
            return

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.callproc('ReturnBook', [int(r_id), ret_date])
                conn.commit()
                messagebox.showinfo("Success", "Book Return Status Successfully Updated!")
                self.refresh_stats()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Failed to return book: {err}")
            finally:
                conn.close()

    def setup_records_tab(self, frame):
        top_bar = tk.Frame(frame, bg="#f8fafc")
        top_bar.pack(fill=tk.X, pady=10)

        tk.Button(
            top_bar, text="🔄 Refresh Records", font=("Segoe UI", 9, "bold"), 
            bg="#9333ea", fg="white", activebackground="#7e22ce", activeforeground="white",
            bd=0, cursor="hand2", command=self.fetch_records
        ).pack(pady=5, ipadx=12, ipady=5)

        table_frame = tk.Frame(frame, bg="white")
        table_frame.pack(expand=True, fill="both", padx=20, pady=10)

        self.tree = ttk.Treeview(table_frame, columns=("Record ID", "Book ID", "Member ID", "Issue Date", "Due Date", "Return Date", "Status"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=110, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, expand=True, fill="both", padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def refresh_stats(self):
        b_count, m_count, iss_count, fine_sum = self.get_dashboard_stats()
        self.card_books.config(text=str(b_count))
        self.card_members.config(text=str(m_count))
        self.card_issued.config(text=str(iss_count))
        self.card_fines.config(text=str(fine_sum))
        self.fetch_records()

    def fetch_records(self, event=None):
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT record_id, book_id, member_id, issue_date, due_date, return_date, status FROM borrow_records")
            rows = cursor.fetchall()
            
            for row in self.tree.get_children():
                self.tree.delete(row)

            for row in rows:
                self.tree.insert("", tk.END, values=row)
            
            conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()