import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time
import threading
from crypto import Currency, getAllAssets

currencies = getAllAssets()


alerts = []
data = {
    'sign': '<',
    'currency': 'USD'
}


def changeSign():
    print(data['sign'])
    if data['sign'] == '<':
        data['sign'] = '>'
    else:
        data['sign'] = '<'
    sign_entry['text'] = data['sign']


def alertMethod(currency):
    if eval(f"{currency.currentValue} {currency.sign} {currency.alertValue}"):
        messagebox.showinfo(
            "Alert", f"{currency.name} is now worth {currency.currentValue} USD (alert value: {currency.sign}{currency.alertValue} USD)")


def add_alert():
    alert = selectValue.get()
    value = value_entry.get()
    if alert and value:
        for currency in currencies:
            if currency['name'] == alert:
                alerts.append(
                    Currency(currency['id'], currency['name'], value, data['sign']))
        update_listbox()
    else:
        messagebox.showinfo("Error", "Please enter both alert and value")


def remove_alert():
    selected_alert = listbox.curselection()
    print(selected_alert)
    if selected_alert:
        alerts.pop(selected_alert['name'])
        update_listbox()
    else:
        messagebox.showinfo("Error", "Please select an alert to remove")


def update_alert():
    selected_alert = listbox.curselection()
    if selected_alert:
        new_value = value_entry.get()
        if new_value:
            alerts[selected_alert[0]].alertValue = float(new_value)
            alerts[selected_alert[0]].sign = data['sign']
            update_listbox()
        else:
            messagebox.showinfo("Error", "Please enter a new value")
    else:
        messagebox.showinfo("Error", "Please select an alert to update")


def update_listbox():
    listbox.delete(0, tk.END)
    for alert in alerts:
        listbox.insert(tk.END, alert.toLine())


def updateLoop():
    while True:
        time.sleep(6)
        print('updating')
        for alert in alerts:
            time.sleep(1)
            alert.updateValues()
            alertMethod(alert)
        update_listbox()


# Create the main window
root = tk.Tk()
root.title("Crypto Alerts")
root.geometry("500x550")

# Create a Listbox widget
listbox = tk.Listbox(root)
listbox.configure(width=55, height=20)
listbox.pack()

currenciesNames = sorted([currency['name'] for currency in currencies])

selectValue = tk.StringVar(root)
selectValue.set("Bitcoin")

# Create entry fields for alert and value
alert_entry = ttk.Combobox(
    root, textvariable=selectValue, values=currenciesNames)
alert_entry.pack()

sign_entry = tk.Button(root, text='<', command=changeSign)
sign_entry.pack()

value_entry = tk.Entry(root)
value_entry.pack()

# Create buttons for adding, removing, and updating alerts
add_button = tk.Button(root, text="Add Alert", command=add_alert)
add_button.pack()

remove_button = tk.Button(root, text="Remove Alert", command=remove_alert)
remove_button.pack()

update_button = tk.Button(root, text="Update Value", command=update_alert)
update_button.pack()


threading.Thread(target=updateLoop, daemon=True).start()

root.mainloop()