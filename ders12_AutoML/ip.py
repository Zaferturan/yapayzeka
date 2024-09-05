import psutil
import socket
import tkinter as tk
from tkinter import messagebox

def get_devices():
devices = []
# Ağ arayüzlerini al
for interface, addrs in psutil.net_if_addrs().items():
for addr in addrs:
if addr.family == socket.AF_INET:
devices.append((interface, addr.address))
return devices

def show_devices():
username = username_entry.get()
password = password_entry.get()

if username and password:
devices = get_devices()
device_list.delete(0, tk.END) # Önceki listeyi temizle
for device in devices:
device_list.insert(tk.END, f"Interface: {device[0]}, IP Address: {device[1]}")
else:
messagebox.showwarning("Giriş Hatası", "Kullanıcı adı ve şifre girin.")

# GUI oluşturma
root = tk.Tk()
root.title("Ağ Cihazları Listesi")

tk.Label(root, text="Kullanıcı Adı:").pack()
username_entry = tk.Entry(root)
username_entry.pack()

tk.Label(root, text="Şifre:").pack()
password_entry = tk.Entry(root, show='*')
password_entry.pack()

tk.Button(root, text="Cihazları Göster", command=show_devices).pack()

device_list = tk.Listbox(root, width=50)
device_list.pack()

root.mainloop()