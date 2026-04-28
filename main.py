import tkinter as tk
from tkinter import messagebox, ttk
import random
import string
import json
import os
from datetime import datetime

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("500x600")
        
        self.history_file = "password_history.json"
        self.history = self.load_history()

        # Интерфейс
        tk.Label(root, text="Настройки пароля", font=('Arial', 12, 'bold')).pack(pady=10)

        tk.Label(root, text="Длина пароля:").pack()
        self.length_slider = tk.Scale(root, from_=4, to=32, orient=tk.HORIZONTAL, length=300)
        self.length_slider.set(12)
        self.length_slider.pack(pady=5)

        self.use_digits = tk.BooleanVar(value=True)
        self.use_letters = tk.BooleanVar(value=True)
        self.use_spec = tk.BooleanVar(value=False)

        tk.Checkbutton(root, text="Цифры (0-9)", variable=self.use_digits).pack(anchor="w", padx=150)
        tk.Checkbutton(root, text="Буквы (a-z, A-Z)", variable=self.use_letters).pack(anchor="w", padx=150)
        tk.Checkbutton(root, text="Спецсимволы (!@#$)", variable=self.use_spec).pack(anchor="w", padx=150)

        tk.Button(root, text="Сгенерировать", command=self.generate, bg="lightblue").pack(pady=15)

        self.result_entry = tk.Entry(root, font=('Arial', 12), width=30)
        self.result_entry.pack(pady=5)

        tk.Label(root, text="История:").pack(pady=5)
        self.tree = ttk.Treeview(root, columns=("Дата", "Пароль"), show='headings', height=10)
        self.tree.heading("Дата", text="Дата")
        self.tree.heading("Пароль", text="Пароль")
        self.tree.column("Дата", width=150)
        self.tree.column("Пароль", width=250)
        self.tree.pack(padx=10, fill=tk.BOTH)

        self.update_table()

    def generate(self):
        length = self.length_slider.get()
        chars = ""
        if self.use_letters.get(): chars += string.ascii_letters
        if self.use_digits.get(): chars += string.digits
        if self.use_spec.get(): chars += string.punctuation

        if not chars:
            messagebox.showwarning("Ошибка", "Выберите хотя бы один тип символов!")
            return

        password = "".join(random.choice(chars) for _ in range(length))
        self.result_entry.delete(0, tk.END)
        self.result_entry.insert(0, password)

        entry = {"timestamp": datetime.now().strftime("%H:%M:%S"), "password": password}
        self.history.append(entry)
        self.save_history()
        self.update_table()

    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r") as f: return json.load(f)
            except: return []
        return []

    def save_history(self):
        with open(self.history_file, "w") as f:
            json.dump(self.history, f, indent=4)

    def update_table(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        for item in reversed(self.history):
            self.tree.insert("", tk.END, values=(item["timestamp"], item["password"]))

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()
