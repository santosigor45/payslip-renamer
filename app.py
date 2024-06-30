import os
import fitz
import re
import subprocess
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from ttkthemes import ThemedTk


def extract_text_from_pdf(pdf_path, region):
    # Extract text from specified region in PDF pages
    pdf_document = fitz.open(pdf_path)
    text = [page.get_text("text", clip=fitz.Rect(*region)) for page in pdf_document]
    name_by_page = [
        re.sub('[^A-Za-z ]+', '', t)
        .split(' PIS')[0]
        .strip()
        .split('\n')[0]
        .replace("  ", " ")
        for t in text
    ]
    pdf_document.close()
    return name_by_page


def save_pages_to_pdf(pdf_path, names_by_page, output_directory):
    # Save pages sorted by city to individual PDFs
    i = 0
    for name in names_by_page:
        output_pdf_path = os.path.join(output_directory, f'{name}.pdf')
        with fitz.open(pdf_path) as original_pdf, fitz.open() as pdf_document:
            pdf_document.insert_pdf(original_pdf, from_page=i, to_page=i)
            pdf_document.save(output_pdf_path)
        i += 1


def select_file():
    # File selection dialog
    global selected_pdf
    pdf_file_path = filedialog.askopenfilename(title="Selecionar Arquivo PDF")
    if pdf_file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, pdf_file_path)
        selected_pdf = True


def select_output_directory():
    # Output directory selection dialog
    global selected_output_directory
    output_directory_path = filedialog.askdirectory(title="Selecionar Diretório de Saída")
    if output_directory_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, output_directory_path)
        selected_output_directory = True


def process_pdf():
    # Main processing function for PDF file
    global selected_pdf, selected_output_directory
    root.config(cursor="watch")
    root.update()
    if not selected_pdf or not selected_output_directory:
        messagebox.showwarning("Aviso", "Por favor, selecione o arquivo PDF e o diretório de saída.")
        return
    pdf_path, output_directory = file_entry.get(), output_entry.get()
    pdfregion = (84, 175, 360, 200)
    names_by_page = extract_text_from_pdf(pdf_path, pdfregion)
    save_pages_to_pdf(pdf_path, names_by_page, output_directory)
    root.config(cursor="")
    messagebox.showinfo("Concluído", "Processo concluído com sucesso!")
    subprocess.Popen(f'explorer "{os.path.abspath(output_directory)}"', shell=True)


selected_pdf = False
selected_output_directory = False

# GUI setup
root = ThemedTk(theme="plastik")
root.title("Renomeador de Holerites")

file_label = ttk.Label(root, text="Arquivo PDF:")
file_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

file_entry = ttk.Entry(root, width=50)
file_entry.grid(row=0, column=1, padx=10, pady=10)

file_button = ttk.Button(root, text="Selecionar Arquivo", command=select_file)
file_button.grid(row=0, column=2, padx=10, pady=10)

output_label = ttk.Label(root, text="Diretório de Saída:")
output_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

output_entry = ttk.Entry(root, width=50)
output_entry.grid(row=1, column=1, padx=10, pady=10)

output_button = ttk.Button(root, text="Selecionar Diretório", command=select_output_directory)
output_button.grid(row=1, column=2, padx=10, pady=10)

process_button = ttk.Button(root, text="Processar PDF", command=process_pdf)
process_button.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()
