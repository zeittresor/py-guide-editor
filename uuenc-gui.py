import tkinter as tk
from tkinter import filedialog, messagebox
import uu

def encode_file():
    input_file = filedialog.askopenfilename(title="Select file to encode")
    if input_file:
        output_file = filedialog.asksaveasfilename(title="Specify the name of the output file")
        if output_file:
            try:
                uu.encode(input_file, output_file)
                messagebox.showinfo("Success", "File encoded successfully")
            except Exception as e:
                messagebox.showerror("Error", str(e))

def decode_file():
    input_file = filedialog.askopenfilename(title="Select file to decode")
    if input_file:
        output_file = filedialog.asksaveasfilename(title="Specify the name of the output file")
        if output_file:
            try:
                uu.decode(input_file, output_file)
                messagebox.showinfo("Success", "File decoded successfully")
            except Exception as e:
                messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("UUEncode/Decode Tool")

encode_button = tk.Button(root, text="Encode", command=encode_file)
encode_button.pack(pady=10)

decode_button = tk.Button(root, text="Decode", command=decode_file)
decode_button.pack(pady=10)

root.mainloop()
