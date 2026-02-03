import tkinter as tk
from tkinter import ttk, messagebox
import requests

BASE_URL = "http://127.0.0.1:5000"

# ================= CLIENTES ================= #

def load_clients():
    list_clients.delete(0, tk.END)
    response = requests.get(f"{BASE_URL}/clients")

    if response.status_code == 200:
        for client in response.json()["clients"]:
            list_clients.insert(
                tk.END,
                f'{client["id"]} - {client["name"]} ({client["email"]})'
            )

def create_client():
    payload = {
        "name": entry_client_name.get(),
        "age": entry_client_age.get(),
        "weight": entry_client_weight.get(),
        "email": entry_client_email.get()
    }

    if not all(payload.values()):
        messagebox.showerror("Erro", "Preencha todos os campos")
        return

    response = requests.post(f"{BASE_URL}/client", json=payload)

    if response.status_code in (200, 201):
        messagebox.showinfo("Sucesso", "Cliente cadastrado")
        clear_client_fields()
        load_clients()
    else:
        messagebox.showerror("Erro", response.json().get("message"))

def delete_client():
    selection = list_clients.curselection()
    if not selection:
        return

    client_id = list_clients.get(selection).split(" - ")[0]

    response = requests.delete(f"{BASE_URL}/client/{client_id}")

    if response.status_code == 200:
        load_clients()
    else:
        messagebox.showerror("Erro", "Erro ao deletar cliente")

def clear_client_fields():
    for e in (entry_client_name, entry_client_age, entry_client_weight, entry_client_email):
        e.delete(0, tk.END)

# ================= REFEIÇÕES ================= #

def load_meals():
    list_meals.delete(0, tk.END)
    response = requests.get(f"{BASE_URL}/meals")

    if response.status_code == 200:
        for meal in response.json()["meals"]:
            list_meals.insert(
                tk.END,
                f'{meal["meal_id"]} - {meal["name"]} ({meal["total_calories"]} kcal)'
            )

def create_meal():
    payload = {
        "name": entry_meal_name.get(),
        "description": entry_meal_desc.get(),
        "total_calories": entry_meal_cal.get()
    }

    if not payload["name"] or not payload["total_calories"]:
        messagebox.showerror("Erro", "Nome e calorias são obrigatórios")
        return

    response = requests.post(f"{BASE_URL}/meal", json=payload)

    if response.status_code in (200, 201):
        messagebox.showinfo("Sucesso", "Refeição cadastrada")
        clear_meal_fields()
        load_meals()
    else:
        messagebox.showerror("Erro", response.json().get("message"))

def delete_meal():
    selection = list_meals.curselection()
    if not selection:
        return

    meal_id = list_meals.get(selection).split(" - ")[0]

    response = requests.delete(f"{BASE_URL}/meal/{meal_id}")

    if response.status_code == 200:
        load_meals()
    else:
        messagebox.showerror("Erro", "Erro ao deletar refeição")

def clear_meal_fields():
    for e in (entry_meal_name, entry_meal_desc, entry_meal_cal):
        e.delete(0, tk.END)

# ================= UI ================= #

root = tk.Tk()
root.title("Daily Diet System")
root.geometry("820x520")
root.configure(bg="#f3f4f6")

FONT_LABEL = ("Segoe UI", 10)
FONT_ENTRY = ("Segoe UI", 10)
FONT_TITLE = ("Segoe UI", 13, "bold")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

# ================= TAB CLIENTES ================= #

tab_clients = tk.Frame(notebook, bg="#f3f4f6")
notebook.add(tab_clients, text="Clientes")

# ----- Formulário Clientes ----- #
client_form = tk.LabelFrame(
    tab_clients,
    text=" Cadastro de Cliente ",
    font=FONT_TITLE,
    bg="#f3f4f6",
    padx=15,
    pady=15
)
client_form.grid(row=0, column=0, padx=10, pady=10, sticky="n")

tk.Label(client_form, text="Nome", font=FONT_LABEL, bg="#f3f4f6").grid(row=0, column=0, sticky="w", pady=4)
entry_client_name = tk.Entry(client_form, font=FONT_ENTRY, width=30)
entry_client_name.grid(row=0, column=1, pady=4)

tk.Label(client_form, text="Idade", font=FONT_LABEL, bg="#f3f4f6").grid(row=1, column=0, sticky="w", pady=4)
entry_client_age = tk.Entry(client_form, font=FONT_ENTRY)
entry_client_age.grid(row=1, column=1, pady=4)

tk.Label(client_form, text="Peso", font=FONT_LABEL, bg="#f3f4f6").grid(row=2, column=0, sticky="w", pady=4)
entry_client_weight = tk.Entry(client_form, font=FONT_ENTRY)
entry_client_weight.grid(row=2, column=1, pady=4)

tk.Label(client_form, text="Email", font=FONT_LABEL, bg="#f3f4f6").grid(row=3, column=0, sticky="w", pady=4)
entry_client_email = tk.Entry(client_form, font=FONT_ENTRY)
entry_client_email.grid(row=3, column=1, pady=4)

tk.Button(
    client_form,
    text="Cadastrar Cliente",
    command=create_client,
    bg="#2563eb",
    fg="white",
    font=FONT_LABEL,
    padx=10
).grid(row=4, column=1, pady=12, sticky="e")

# ----- Lista Clientes ----- #
client_list_frame = tk.LabelFrame(
    tab_clients,
    text=" Clientes Cadastrados ",
    font=FONT_TITLE,
    bg="#f3f4f6",
    padx=10,
    pady=10
)
client_list_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

list_clients = tk.Listbox(client_list_frame, width=45, height=15, font=FONT_ENTRY)
list_clients.pack(pady=5)

btn_frame_client = tk.Frame(client_list_frame, bg="#f3f4f6")
btn_frame_client.pack(pady=5)

tk.Button(btn_frame_client, text="Atualizar", command=load_clients).grid(row=0, column=0, padx=5)
tk.Button(btn_frame_client, text="Deletar", command=delete_client).grid(row=0, column=1, padx=5)

# ================= TAB REFEIÇÕES ================= #

tab_meals = tk.Frame(notebook, bg="#f3f4f6")
notebook.add(tab_meals, text="Refeições")

# ----- Formulário Refeições ----- #
meal_form = tk.LabelFrame(
    tab_meals,
    text=" Cadastro de Refeição ",
    font=FONT_TITLE,
    bg="#f3f4f6",
    padx=15,
    pady=15
)
meal_form.grid(row=0, column=0, padx=10, pady=10, sticky="n")

tk.Label(meal_form, text="Nome", font=FONT_LABEL, bg="#f3f4f6").grid(row=0, column=0, sticky="w", pady=4)
entry_meal_name = tk.Entry(meal_form, font=FONT_ENTRY, width=30)
entry_meal_name.grid(row=0, column=1, pady=4)

tk.Label(meal_form, text="Descrição", font=FONT_LABEL, bg="#f3f4f6").grid(row=1, column=0, sticky="w", pady=4)
entry_meal_desc = tk.Entry(meal_form, font=FONT_ENTRY)
entry_meal_desc.grid(row=1, column=1, pady=4)

tk.Label(meal_form, text="Calorias", font=FONT_LABEL, bg="#f3f4f6").grid(row=2, column=0, sticky="w", pady=4)
entry_meal_cal = tk.Entry(meal_form, font=FONT_ENTRY)
entry_meal_cal.grid(row=2, column=1, pady=4)

tk.Button(
    meal_form,
    text="Cadastrar Refeição",
    command=create_meal,
    bg="#16a34a",
    fg="white",
    font=FONT_LABEL,
    padx=10
).grid(row=3, column=1, pady=12, sticky="e")

# ----- Lista Refeições ----- #
meal_list_frame = tk.LabelFrame(
    tab_meals,
    text=" Refeições Cadastradas ",
    font=FONT_TITLE,
    bg="#f3f4f6",
    padx=10,
    pady=10
)
meal_list_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

list_meals = tk.Listbox(meal_list_frame, width=45, height=15, font=FONT_ENTRY)
list_meals.pack(pady=5)

btn_frame_meal = tk.Frame(meal_list_frame, bg="#f3f4f6")
btn_frame_meal.pack(pady=5)

tk.Button(btn_frame_meal, text="Atualizar", command=load_meals).grid(row=0, column=0, padx=5)
tk.Button(btn_frame_meal, text="Deletar", command=delete_meal).grid(row=0, column=1, padx=5)

root.mainloop()
