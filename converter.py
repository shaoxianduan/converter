import tkinter as tk
from tkinter import ttk, messagebox
import requests

# ===================== Currency Converter =====================
# Author: Shaoxian Duan, 2023.09.09


def currency_converter_window():
    """for money converter"""
    def convert():
        base = base_entry.get().upper()
        target = target_entry.get().upper()
        try:
            amount = float(amount_entry.get())
        except ValueError:
            messagebox.showerror("error", "Please enter a valid number:")
            return
        url = f"https://v6.exchangerate-api.com/v6/42e07609c352e07befd0aa1c/latest/{base}"
        try:
            response = requests.get(url)
            data = response.json()
            if data["result"] == "success":
                rate = data["conversion_rates"].get(target)
                if rate:
                    result_var.set(
                        f"{amount} {base} = {amount*rate:.2f} {target}")
                else:
                    messagebox.showerror(
                        "error", f"Unsupported target currency：{target}")
            else:
                messagebox.showerror(
                    "error", "Unable to retrieve exchange rate data")
        except Exception as e:
            messagebox.showerror("error", f"Failed to fetch exchange rate：{e}")

    win = tk.Toplevel(root)
    win.title("Currency Converter")

    tk.Label(win, text="Base Currency:").grid(row=0, column=0, padx=5, pady=5)
    base_entry = tk.Entry(win)
    base_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(win, text="Target Currency:").grid(
        row=1, column=0, padx=5, pady=5)
    target_entry = tk.Entry(win)
    target_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(win, text="Amount:").grid(row=2, column=0, padx=5, pady=5)
    amount_entry = tk.Entry(win)
    amount_entry.grid(row=2, column=1, padx=5, pady=5)

    result_var = tk.StringVar()
    tk.Label(win, textvariable=result_var, fg="blue").grid(
        row=4, column=0, columnspan=2, padx=5, pady=5)

    tk.Button(win, text="convert", command=convert).grid(
        row=3, column=0, columnspan=2, pady=10)

    # Critical Fix: Automatic Window Resizing
    win.update_idletasks()
    win.minsize(win.winfo_reqwidth(), win.winfo_reqheight())


# ===================== General Unit Conversion =====================
def unit_converter_window(title, units_dict):
    """for unit converter"""
    def convert():
        try:
            value = float(value_entry.get())
        except ValueError:
            messagebox.showerror("error", "Please enter a valid number:！")
            return
        from_u = from_unit.get()
        to_u = to_unit.get()
        try:
            converted = value * units_dict[from_u][to_u]
            result_var.set(f"{value} {from_u} = {converted:.4f} {to_u}")
        except KeyError:
            messagebox.showerror("error", "Unsupported Unit Conversion！")

    win = tk.Toplevel(root)
    win.title(title)

    tk.Label(win, text="Vaule:").grid(row=0, column=0, padx=5, pady=5)
    value_entry = tk.Entry(win)
    value_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(win, text="Original Unit:").grid(row=1, column=0, padx=5, pady=5)
    from_unit = ttk.Combobox(win, values=list(units_dict.keys()))
    from_unit.grid(row=1, column=1, padx=5, pady=5)
    from_unit.current(0)

    tk.Label(win, text="Target Unit:").grid(row=2, column=0, padx=5, pady=5)
    to_unit = ttk.Combobox(win, values=list(units_dict.keys()))
    to_unit.grid(row=2, column=1, padx=5, pady=5)
    to_unit.current(1)

    result_var = tk.StringVar()
    tk.Label(win, textvariable=result_var, fg="blue").grid(
        row=4, column=0, columnspan=2, pady=5)

    tk.Button(win, text="Convert", command=convert).grid(
        row=3, column=0, columnspan=2, pady=10)

    win.update_idletasks()
    win.minsize(win.winfo_reqwidth(), win.winfo_reqheight())


# ===================== temperature converter =====================
def temperature_converter_window():
    """for temp"""
    def convert():
        try:
            temp = float(temp_entry.get())
        except ValueError:
            messagebox.showerror("error", "Please enter a valid number:！")
            return
        f = from_unit.get().upper()
        t = to_unit.get().upper()
        if f == "C":
            res = temp*9/5 + 32 if t == "F" else temp + 273.15 if t == "K" else temp
        elif f == "F":
            res = (temp-32)*5/9 if t == "C" else (temp-32) * \
                5/9 + 273.15 if t == "K" else temp
        elif f == "K":
            res = temp - \
                273.15 if t == "C" else (
                    temp-273.15)*9/5 + 32 if t == "F" else temp
        else:
            messagebox.showerror("error", "Unsupported temperature unit!")
            return
        result_var.set(f"{temp} {f} = {res:.2f} {t}")

    win = tk.Toplevel(root)
    win.title("temperature converter")

    tk.Label(win, text="Temperature Value:").grid(
        row=0, column=0, padx=5, pady=5)
    temp_entry = tk.Entry(win)
    temp_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(win, text="Original Unit:").grid(row=1, column=0, padx=5, pady=5)
    from_unit = ttk.Combobox(win, values=["C", "F", "K"])
    from_unit.grid(row=1, column=1, padx=5, pady=5)
    from_unit.current(0)

    tk.Label(win, text="Target Unit:").grid(row=2, column=0, padx=5, pady=5)
    to_unit = ttk.Combobox(win, values=["C", "F", "K"])
    to_unit.grid(row=2, column=1, padx=5, pady=5)
    to_unit.current(1)

    result_var = tk.StringVar()
    tk.Label(win, textvariable=result_var, fg="blue").grid(
        row=4, column=0, columnspan=2, pady=5)

    tk.Button(win, text="Convert", command=convert).grid(
        row=3, column=0, columnspan=2, pady=10)

    win.update_idletasks()
    win.minsize(win.winfo_reqwidth(), win.winfo_reqheight())


# ===================== Main windows =====================
root = tk.Tk()
root.title("Travelers' Unit Converter")
root.geometry("250x350")

tk.Label(root, text="Pls select a conver-type:",
         font=("Arial", 14)).pack(pady=10)

tk.Button(root, text="Currency Converter", width=20,
          command=currency_converter_window).pack(pady=5)
tk.Button(root, text="Length Conversion", width=20, command=lambda: unit_converter_window(
    "Length Conversion", {"in": {"cm": 2.54, "m": 0.0254, "ft": 0.0833333},
                          "cm": {"in": 0.393701, "m": 0.01, "ft": 0.0328084},
                          "m": {"in": 39.3701, "cm": 100, "ft": 3.28084},
                          "ft": {"in": 12, "cm": 30.48, "m": 0.3048}})).pack(pady=5)
tk.Button(root, text="Speed Conversion", width=20, command=lambda: unit_converter_window(
    "Speed Conversion", {"km/h": {"mph": 0.621371}, "mph": {"km/h": 1.60934}})).pack(pady=5)
tk.Button(root, text="Volume Conversion", width=20, command=lambda: unit_converter_window(
    "Volume Conversion", {"gal": {"L": 3.78541}, "L": {"gal": 0.264172}})).pack(pady=5)
tk.Button(root, text="Mass Conversion", width=20, command=lambda: unit_converter_window(
    "Mass Conversion", {"lb": {"oz": 16, "kg": 0.453592}, "oz": {"lb": 0.0625, "kg": 0.0283495}, "kg": {"lb": 2.20462, "oz": 35.274}})).pack(pady=5)
tk.Button(root, text="temperature Conversion", width=20,
          command=temperature_converter_window).pack(pady=5)

root.mainloop()
