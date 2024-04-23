import subprocess
import tkinter as tk
from tkinter import ttk

def switch_git_account():
    def set_git_config():
        email = email_entry.get()
        name = name_entry.get()
        
        # Set up Git config
        subprocess.run(["git", "config", "--global", "user.email", email])
        subprocess.run(["git", "config", "--global", "user.name", name])
        
        # Store the current configuration
        with open("git_accounts.txt", "a") as f:
            f.write(f"{email}:{name}\n")
        
        print("Git account switched successfully.")
        root.destroy()

    def on_existing_select(event):
        selected_email = existing_dropdown.get()
        if selected_email:
            name_entry.delete(0, tk.END)
            name_entry.insert(0, existing_accounts[selected_email])
            email_entry.delete(0, tk.END)
            email_entry.insert(0, selected_email)

    root = tk.Tk()
    root.title("Git Account Switcher")

    existing_accounts = {}
    try:
        with open("git_accounts.txt", "r") as f:
            for line in f:
                if line.strip():
                    email, name = line.strip().split(":")
                    existing_accounts[email.strip()] = name.strip()
    except FileNotFoundError:
        pass
    
    label_email = ttk.Label(root, text="Enter your email:")
    label_email.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    email_entry = ttk.Entry(root)
    email_entry.grid(row=0, column=1, padx=5, pady=5)

    label_name = ttk.Label(root, text="Enter your name:")
    label_name.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    name_entry = ttk.Entry(root)
    name_entry.grid(row=1, column=1, padx=5, pady=5)

    label_existing = ttk.Label(root, text="Or select from existing:")
    label_existing.grid(row=2, column=0, padx=5, pady=5, sticky="w")

    existing_var = tk.StringVar(root)
    existing_dropdown = ttk.Combobox(root, textvariable=existing_var)
    existing_dropdown['values'] = list(existing_accounts.keys())
    existing_dropdown.grid(row=2, column=1, padx=5, pady=5)

    existing_dropdown.bind("<<ComboboxSelected>>", on_existing_select)

    button_set = ttk.Button(root, text="Set", command=set_git_config)
    button_set.grid(row=3, column=1, padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    switch_git_account()

