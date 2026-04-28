import tkinter as tk
from tkinter import messagebox
import requests
import json
import os

class GitHubFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub User Finder")
        self.root.geometry("450x550")
        
        self.fav_file = "favorites.json"
        self.favorites = self.load_favorites()

        # Интерфейс
        tk.Label(root, text="Введите логин GitHub:", font=('Arial', 10, 'bold')).pack(pady=5)
        
        self.search_entry = tk.Entry(root, width=35)
        self.search_entry.pack(pady=5)
        
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Найти", command=self.search_user, width=10, bg="lightblue").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="В избранное", command=self.add_to_fav, width=12, bg="lightgreen").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Показать избранное", command=self.show_favorites).pack(side=tk.LEFT, padx=5)

        # Область вывода данных
        self.info_text = tk.Text(root, height=15, width=50, state=tk.DISABLED)
        self.info_text.pack(pady=10, padx=10)
        
        self.current_user_data = None

    def search_user(self):
        username = self.search_entry.get().strip()
        if not username:
            messagebox.showwarning("Ошибка", "Поле поиска не должно быть пустым!")
            return

        try:
            response = requests.get(f"https://github.com{username}")
            if response.status_code == 200:
                data = response.json()
                self.current_user_data = {
                    "login": data.get("login"),
                    "name": data.get("name"),
                    "bio": data.get("bio"),
                    "url": data.get("html_url")
                }
                self.display_user(self.current_user_data)
            else:
                messagebox.showerror("Ошибка", "Пользователь не найден")
        except Exception as e:
            messagebox.showerror("Ошибка сети", f"Не удалось подключиться: {e}")

    def display_user(self, user):
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        info = f"Логин: {user['login']}\nИмя: {user['name']}\nО себе: {user['bio']}\nСсылка: {user['url']}"
        self.info_text.insert(tk.END, info)
        self.info_text.config(state=tk.DISABLED)

    def add_to_fav(self):
        if self.current_user_data:
            login = self.current_user_data['login']
            self.favorites[login] = self.current_user_data
            self.save_favorites()
            messagebox.showinfo("Успех", f"{login} добавлен в избранное!")
        else:
            messagebox.showwarning("Внимание", "Сначала найдите пользователя")

    def load_favorites(self):
        if os.path.exists(self.fav_file):
            with open(self.fav_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_favorites(self):
        with open(self.fav_file, "w", encoding="utf-8") as f:
            json.dump(self.favorites, f, ensure_ascii=False, indent=4)

    def show_favorites(self):
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        if not self.favorites:
            self.info_text.insert(tk.END, "Список избранного пуст.")
        for login in self.favorites:
            self.info_text.insert(tk.END, f"- {login}\n")
        self.info_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = GitHubFinder(root)
    root.mainloop()
