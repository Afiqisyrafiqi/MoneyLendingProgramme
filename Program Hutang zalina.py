import tkinter as tk
from tkinter import messagebox, Toplevel, Scrollbar, Text, RIGHT, Y, END
from PIL import Image, ImageTk
import csv
from datetime import datetime

def open_admin_system():
    root = tk.Tk()
    root.title("Program Kiraan Hutang Puan Zalina (Admin)")

    # Image path
    image_path = r"C:\Users\mafiq\OneDrive\Desktop\zalina.jpeg"  # Make sure the path is correct
    try:
        image = Image.open(image_path)
        image = image.resize((200, 200))
        photo = ImageTk.PhotoImage(image)

        label_image = tk.Label(root, image=photo)
        label_image.image = photo
        label_image.grid(row=0, column=0, columnspan=2, pady=10)
    except Exception as e:
        messagebox.showerror("Error", f"Error loading image: {e}")
    
    label_result = tk.Label(root, text="Total Amount: RM 0.00")
    label_result.grid(row=5, column=0, columnspan=2, pady=10)

    def calculate_debt():
        try:
            name = entry_name.get()
            debt = float(entry_debt.get())
            years = int(entry_years.get())
            
            if not name:
                messagebox.showerror("Ralat Input", "Sila masukkan nama.")
                return
            
            base_interest_rate = 0.035
            additional_interest_rate = 0.005
            interest_rate = base_interest_rate + (additional_interest_rate * years)
            total = debt + (debt * interest_rate)
            
            label_result.config(text=f"Jumlah selepas {years} tahun: RM {total:.2f}")
            
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Simpan dalam fail CSV
            with open("hutang_zalina.csv", mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([name, f"{debt:.2f}", years, f"{total:.2f}", now])
            
            messagebox.showinfo("Berjaya", "Maklumat telah disimpan dalam sistem.")
        
        except ValueError:
            messagebox.showerror("Ralat Input", "Sila masukkan jumlah hutang dan tahun yang betul.")

    def lihat_semua_hutang():
        try:
            with open('hutang_zalina.csv', mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                rekod = list(reader)

                if len(rekod) <= 1:
                    messagebox.showinfo("Tiada Rekod", "Tiada rekod hutang ditemui.")
                    return

                # Tetingkap baru untuk paparan
                window = Toplevel(root)
                window.title("Semua Rekod Hutang")

                # Tambah Scrollbar
                scrollbar = Scrollbar(window)
                scrollbar.pack(side=RIGHT, fill=Y)

                # Paparan teks
                text_area = Text(window, wrap="none", yscrollcommand=scrollbar.set, width=80)
                text_area.pack()

                scrollbar.config(command=text_area.yview)

                # Tulis isi CSV
                for row in rekod:
                    line = "\t".join(row) + "\n"
                    text_area.insert(END, line)

        except FileNotFoundError:
            messagebox.showerror("Ralat", "Fail CSV belum wujud.")
    
    def delete_debt():
        password = entry_password_delete.get()

        # Verifikasi password untuk padam rekod
        if password == 'adminpass':
            try:
                with open('hutang_zalina.csv', mode='r', newline='', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    records = list(reader)

                # Hapus rekod hutang
                if len(records) > 1:
                    with open('hutang_zalina.csv', mode='w', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerows([records[0]])  # Only write header
                    messagebox.showinfo("Berjaya", "Semua hutang telah dipadam.")
                else:
                    messagebox.showinfo("Tiada Rekod", "Tiada hutang untuk dipadam.")
            except FileNotFoundError:
                messagebox.showerror("Ralat", "Fail CSV belum wujud.")
        else:
            messagebox.showerror("Ralat", "Password tidak betul!")

    # Fungsi untuk mengurangkan hutang dengan password
    def reduce_debt():
        password = entry_password_reduce.get()

        if password != 'adminpass':
            messagebox.showerror("Ralat", "Password tidak betul!")
            return
        
        try:
            name = entry_reduce_name.get()
            reduce_amount = float(entry_reduce_amount.get())

            if not name:
                messagebox.showerror("Ralat Input", "Sila masukkan nama peminjam.")
                return

            if reduce_amount <= 0:
                messagebox.showerror("Ralat Input", "Jumlah pengurangan harus lebih besar daripada 0.")
                return

            # Baca fail CSV dan cari rekod untuk nama peminjam
            with open('hutang_zalina.csv', mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                records = list(reader)

            # Carikan rekod peminjam
            for i, row in enumerate(records):
                if row[0] == name:
                    original_debt = float(row[1])
                    if original_debt < reduce_amount:
                        messagebox.showerror("Ralat Pengurangan", "Jumlah pengurangan lebih besar daripada hutang asal.")
                        return

                    # Kurangkan jumlah hutang
                    new_debt = original_debt - reduce_amount
                    records[i][1] = f"{new_debt:.2f}"

                    # Simpan semula rekod yang telah dikemas kini
                    with open('hutang_zalina.csv', mode='w', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerows(records)

                    messagebox.showinfo("Berjaya", f"Hutang {name} berjaya dikurangkan sebanyak RM {reduce_amount:.2f}.")
                    return

            # Jika nama peminjam tidak ditemui
            messagebox.showerror("Ralat", "Nama peminjam tidak dijumpai.")

        except ValueError:
            messagebox.showerror("Ralat Input", "Sila masukkan jumlah yang betul.")

    # GUI untuk admin (Zalina)
    label_name = tk.Label(root, text="Masukkan nama peminjam:")
    label_name.grid(row=1, column=0, sticky="w", padx=10, pady=5)
    entry_name = tk.Entry(root)
    entry_name.grid(row=1, column=1, padx=10, pady=5)

    label_debt = tk.Label(root, text="Masukkan jumlah hutang (RM):")
    label_debt.grid(row=2, column=0, sticky="w", padx=10, pady=5)
    entry_debt = tk.Entry(root)
    entry_debt.grid(row=2, column=1, padx=10, pady=5)

    label_years = tk.Label(root, text="Masukkan jumlah tahun anda telah berhutang:")
    label_years.grid(row=3, column=0, sticky="w", padx=10, pady=5)
    entry_years = tk.Entry(root)
    entry_years.grid(row=3, column=1, padx=10, pady=5)

    button_force = tk.Button(root, text="Kira Hutang", command=calculate_debt, bg='blue', fg='white')
    button_force.grid(row=4, column=0, columnspan=2, pady=10)

    # Button untuk lihat semua hutang
    button_view_debt = tk.Button(root, text="Lihat Semua Hutang", command=lihat_semua_hutang)
    button_view_debt.grid(row=5, column=0, columnspan=2, pady=10)

    # Button untuk padam hutang (memerlukan password)
    label_password_delete = tk.Label(root, text="Masukkan password untuk padam hutang:")
    label_password_delete.grid(row=6, column=0, sticky="w", padx=10, pady=5)
    entry_password_delete = tk.Entry(root, show="*")
    entry_password_delete.grid(row=6, column=1, padx=10, pady=5)

    button_delete_debt = tk.Button(root, text="Padam Hutang", command=delete_debt, bg='red', fg='white')
    button_delete_debt.grid(row=7, column=0, columnspan=2, pady=10)

    # Fungsi untuk mengurangkan hutang
    label_password_reduce = tk.Label(root, text="Masukkan password untuk kurangkan hutang:")
    label_password_reduce.grid(row=8, column=0, sticky="w", padx=10, pady=5)
    entry_password_reduce = tk.Entry(root, show="*")
    entry_password_reduce.grid(row=8, column=1, padx=10, pady=5)

    label_reduce_name = tk.Label(root, text="Masukkan nama peminjam untuk kurangkan hutang:")
    label_reduce_name.grid(row=9, column=0, sticky="w", padx=10, pady=5)
    entry_reduce_name = tk.Entry(root)
    entry_reduce_name.grid(row=9, column=1, padx=10, pady=5)

    label_reduce_amount = tk.Label(root, text="Masukkan jumlah pengurangan hutang (RM):")
    label_reduce_amount.grid(row=10, column=0, sticky="w", padx=10, pady=5)
    entry_reduce_amount = tk.Entry(root)
    entry_reduce_amount.grid(row=10, column=1, padx=10, pady=5)

    button_reduce_debt = tk.Button(root, text="Kurangkan Hutang", command=reduce_debt, bg='green', fg='white')
    button_reduce_debt.grid(row=11, column=0, columnspan=2, pady=10)

    root.mainloop()

open_admin_system()
