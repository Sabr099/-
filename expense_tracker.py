import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import os

DATA_FILE = "expenses.json"

class ExpenseTracker:
    def init(self, root):
        self.root = root
        self.root.title("Expense Tracker - Трекер расходов")
        self.root.geometry("950x700")

        self.expenses = self.load_expenses()

        # Форма добавления расхода
        form = ttk.LabelFrame(root, text="Добавить новый расход", padding=15)
        form.pack(fill="x", padx=15, pady=10)

        ttk.Label(form, text="Сумма (руб):").grid(row=0, column=0, sticky="w", pady=5)
        self.amount_var = tk.DoubleVar()
        ttk.Entry(form, textvariable=self.amount_var, width=20).grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(form, text="Категория:").grid(row=0, column=2, sticky="w", pady=5)
        self.category_var = tk.StringVar(value="Еда")
        categories = ["Еда", "Транспорт", "Развлечения", "Коммуналка", "Здоровье", "Одежда", "Другое"]
        ttk.Combobox(form, textvariable=self.category_var, values=categories, state="readonly", width=18).grid(row=0, column=3, padx=10, pady=5)

        ttk.Label(form, text="Дата (ГГГГ-ММ-ДД):").grid(row=1, column=0, sticky="w", pady=5)
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(form, textvariable=self.date_var, width=20).grid(row=1, column=1, padx=10, pady=5)

        ttk.Button(form, text="Добавить расход", command=self.add_expense).grid(row=1, column=3, pady=10)

        # Таблица
        columns = ("Дата", "Сумма", "Категория")
        self.tree = ttk.Treeview(root, columns=columns, show="headings", height=18)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack(fill="both", expand=True, padx=15, pady=10)

        # Сумма
        self.total_label = ttk.Label(root, text="Сумма за период: 0.00 руб", font=("Arial", 12, "bold"))
        self.total_label.pack(pady=8)

        ttk.Button(root, text="Сохранить данные", command=self.save_expenses).pack(pady=5)

        self.refresh_table()

    def load_expenses(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_expenses(self):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.expenses, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Успех", "Данные сохранены в expenses.json")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def add_expense(self):
        try:
            amount = self.amount_var.get()
            if amount <= 0:
                raise ValueError("Сумма должна быть положительной!")
            category = self.category_var.get()
            date_str = self.date_var.get().strip()

            datetime.strptime(date_str, "%Y-%m-%d")  # проверка даты

            self.expenses.append({"date": date_str, "amount": amount, "category": category})
            self.save_expenses()
            self.refresh_table()
            self.amount_var.set(0.0)
            messagebox.showinfo("Готово", "Расход успешно добавлен!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Проверьте данные:\n{str(e)}")

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        total = 0
        for exp in self.expenses:
            self.tree.insert("", "end", values=(exp["date"], f"{exp['amount']:.2f}", exp["category"]))
            total += exp["amount"]
        self.total_label.config(text=f"Сумма за период: {total:.2f} руб")

if name == "main":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()