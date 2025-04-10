import tkinter as tk
import tkinter.messagebox as messagebox
from PIL import Image, ImageTk

# Create the main application window
root = tk.Tk()
root.title("Program Kiraan Hutang Puan Zalina")

# Image path
image_path = r"C:\Users\mafiq\OneDrive\Desktop\zalina.jpeg"  # Update path to OneDrive Desktop

# Row 0: Masuk gambar Zalina
image = Image.open(image_path)  # Ganti dengan nama fail sebenar
image = image.resize((200, 200))  # Saiz gambar (ikut suka)
photo = ImageTk.PhotoImage(image)

label_image = tk.Label(root, image=photo)
label_image.image = photo  # Wajib simpan reference supaya gambar tak hilang
label_image.grid(row=0, column=0, columnspan=2, pady=10)

# Create a label to display the result
label_result = tk.Label(root, text="Total Amount: RM 0.00")
label_result.grid(row=4, column=0, columnspan=2, pady=10)

# Functions for the calculations
def calculate_debt():
    try:
        debt = float(entry_debt.get())
        years = int(entry_years.get())
        
        # Set the interest rate to increase based on years
        base_interest_rate = 0.035  # 3.5% base rate
        additional_interest_rate = 0.005  # Add 0.5% per year
        
        # Increase interest rate based on years of debt
        interest_rate = base_interest_rate + (additional_interest_rate * years)
        
        # Calculate the total debt after interest
        total = debt + (debt * interest_rate)
        
        label_result.config(text=f"Jumlah selepas {years} tahun: RM {total:.2f}")
    except ValueError:
        messagebox.showerror("Ralat Input", "Sila masukkan jumlah hutang dan tahun yang betul.")

# Row 1: Label & Entry for debt
label_debt = tk.Label(root, text="Masukkan jumlah hutang (RM):")
label_debt.grid(row=1, column=0, sticky="w", padx=10, pady=5)
entry_debt = tk.Entry(root)
entry_debt.grid(row=1, column=1, padx=10, pady=5)

# Row 2: Label & Entry for years
label_years = tk.Label(root, text="Masukkan jumlah tahun anda telah berhutang :")
label_years.grid(row=2, column=0, sticky="w", padx=10, pady=5)
entry_years = tk.Entry(root)
entry_years.grid(row=2, column=1, padx=10, pady=5)

# Row 3: Button
button_force = tk.Button(root, text="Kira Hutang (Kadar Faedah Berdasarkan Tahun 3.5% + 0.05 percent setiap tahun)", command=calculate_debt)
button_force.grid(row=3, column=0, columnspan=2, pady=10)

# Run the GUI app
root.mainloop()
