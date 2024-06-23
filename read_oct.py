import tkinter as tk
from tkinter import filedialog, messagebox

import numpy as np
from PIL import Image


def read_raster(file_name):
    no_images = 21
    window_height = 768
    scan_length1 = 1020

    I = []

    try:
        with open(file_name, 'rb') as fid:
            for i in range(no_images):
                data = np.fromfile(fid, dtype=np.float32, count=window_height * scan_length1)
                I.append(data.reshape((scan_length1, window_height)))

        minimum = 800
        for nr_skanu in range(no_images):
            b1 = I[nr_skanu]
            maximum = np.max(b1)

            b1 = 255 * ((b1 - minimum) / (maximum - minimum))
            b1[b1 < 0] = 0
            b1 = np.uint8(b1)
            I1 = np.flipud(b1.T)

            if nr_skanu > 99:
                przedrostek = str(nr_skanu)
            elif nr_skanu > 9:
                przedrostek = f"0{nr_skanu}"
            else:
                przedrostek = f"00{nr_skanu}"

            nazwapliku = f"Skan_nr_{przedrostek}.jpg"
            Image.fromarray(I1).save(nazwapliku)
        messagebox.showinfo("Info", "Process completed successfully!")
    except Exception as e:
        print(f"Error: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")


def run():
    file_path = entry.get()
    if file_path:
        read_raster(file_path)
    else:
        messagebox.showwarning("Warning", "Please provide a file path.")


def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("OCT files", "*.OCT"), ("All files", "*.*")])
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)


# Create the main window
root = tk.Tk()
root.title("OCT Reader")

label = tk.Label(root, text="OCT File Path:")
label.pack(pady=10)

entry = tk.Entry(root, width=50)
entry.pack(pady=5, padx=10)

browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.pack(pady=5)

run_button = tk.Button(root, text="Run", command=run)
run_button.pack(pady=10)

label = tk.Label(root, text="Licencjat: Dominika Wendland")
label.pack(pady=10)

# Run the application
root.mainloop()
