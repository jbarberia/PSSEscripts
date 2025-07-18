# coding: latin-1
"""
Archivo para ejecutar sobre la interfaz grafica del PSSE
"""

import Tkinter as tk
import tkFileDialog
import zipfile
import tempfile
import time
import shutil
import re
import os
import io

import psse34
import psspy

def extract_zip_file(zip_file_path):
    temp_dir = tempfile.mkdtemp()    
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    return temp_dir
    
    
def get_contingencies(working_folder):
    with io.open(os.path.join(working_folder, 'Names.phy'), encoding="latin-1") as f:
        file_content = f.read()
    strings = re.findall(r'[^\x00-\x1F\x7F-\xFF]+', file_content)[1:]
    contingency_identificator = [(label, isv.strip()) for label, isv in zip(strings[::2], strings[1::2])]
    return contingency_identificator


def print_pdf(tmp_output_file, output_file, new_title_2=""):
    title_1, title_2 = psspy.titldt()
    title_1 = title_1.strip()

    title_2 = os.path.basename(output_file)\
        .replace(".zip", "")\
        .replace(".sav", "")\
        .replace(".cnv", "")
    title_2 += new_title_2
    psspy.case_title_data(title_1, title_2)

    psspy.refreshdiagfile()
    
    time.sleep(1)
    psspy.printdiagfile(r"""Microsoft Print to PDF""",1,2)           
    time.sleep(1)
    
    title_1 = title_1.replace("/", "-").decode("latin-1")
    title_2 = title_2.replace("/", "-").decode("latin-1")
    
    tmp_output_file_folder = os.path.dirname(tmp_output_file)
    output_file = os.path.join(tmp_output_file_folder, title_2 + ".pdf")
       
    time.sleep(2)    
    shutil.move(tmp_output_file, output_file)
             

class FileLoaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ACCC/SAV SLD Printer")
        self.root.attributes("-topmost", True)  # Make window always on top
        
        # List to hold selected files
        self.file_list = []
        self.tmp_output_file = "C:/Users/User/Documents/ms_print.pdf"
        
        # Listbox to display the files
        self.file_listbox = tk.Listbox(root, width=50, height=15)
        self.file_listbox.pack(padx=10, pady=10)
        
        # Load file button
        self.load_button = tk.Button(root, text="Load Files", command=self.load_files)
        self.load_button.pack(padx=10, pady=5)
        
        # Textbox (Entry) to display and edit the output file path
        self.output_entry = tk.Entry(root, width=50)
        self.output_entry.pack(padx=10, pady=5)
        
        # Select output file button
        self.output_button = tk.Button(root, text="Select Output File", command=self.select_output_file)
        self.output_button.pack(padx=10, pady=5)
        self.output_entry.insert(0, self.tmp_output_file)
        
        # Label and textbox for prefix
        self.prefix_label = tk.Label(root, text="Prefix:")
        self.prefix_label.pack(padx=10, pady=5)
        self.prefix_entry = tk.Entry(root, width=50)
        self.prefix_entry.pack(padx=10, pady=5)
        
        # Label and textbox for suffix
        self.suffix_label = tk.Label(root, text="Suffix:")
        self.suffix_label.pack(padx=10, pady=5)
        self.suffix_entry = tk.Entry(root, width=50)
        self.suffix_entry.pack(padx=10, pady=5)
                
        # Process files button
        self.process_button = tk.Button(root, text="Process Files", command=self.process_files)
        self.process_button.pack(padx=10, pady=5)
        self.orig_color = self.process_button.cget("background")
        
        # Clear list button
        self.clear_button = tk.Button(root, text="Clear List", command=self.clear_list)
        self.clear_button.pack(padx=10, pady=5)
        
        
    def load_files(self):
        # Open file dialog to select files
        filenames = tkFileDialog.askopenfilenames(
            initialdir="../../estudios",
            title="Select ZIP files", 
            filetypes=[("ZIP files", "*.zip"), ("SAV files", "*.sav"), ("CNV files", "*.cnv")]  # Restrict to ZIP files
        )
        if filenames:
            for file in filenames:
                if file not in self.file_list:
                    self.file_list.append(file)
                    self.file_listbox.insert(tk.END, os.path.basename(file))
    

    def process_files(self):
        if not self.file_list:
            print("No files loaded!")
            return
        
        self.process_button.config(bg="orange")
        self.root.update()
        
        zip_files = [f for f in self.file_list if f.endswith(".zip")]
        single_files = [f for f in self.file_list if f.endswith(".sav") or f.endswith(".cnv")]


        for file in zip_files:
            working_folder = extract_zip_file(file)
            contingencies = get_contingencies(working_folder)
            
            # Caso base
            psspy.case(os.path.join(working_folder, "InitCase.sav"))
            print_pdf(self.tmp_output_file, file, " - CASO BASE" + self.suffix_entry.get())
            
            # Contingencias
            for colabel, coid in contingencies:
                psspy.case(os.path.join(working_folder, "InitCase.sav"))
                ierr = psspy.getcontingencysavedcase(file.encode("utf-8"), coid)
                print_pdf(self.tmp_output_file, file, " - " + self.prefix_entry.get() + colabel.strip() + self.suffix_entry.get())

            shutil.rmtree(working_folder)

        for file in single_files:
            psspy.case(file)
            print_pdf(self.tmp_output_file, file)

        self.process_button.config(bg=self.orig_color)
        self.root.update()
        print("Processing complete")
            
    def clear_list(self):
        # Clear the file list and the listbox
        self.file_list = []
        self.file_listbox.delete(0, tk.END)
        print("File list cleared")
        
    def select_output_file(self):
        # Open file dialog to select or create an output file
        self.tmp_output_file = tkFileDialog.asksaveasfilename(title="Select output file", defaultextension=".txt")
        if self.tmp_output_file:
            # Display the selected output file path in the textbox
            self.output_entry.delete(0, tk.END)  # Clear the entry first
            self.output_entry.insert(0, self.tmp_output_file)
            print("Selected output file:", self.tmp_output_file)
            
            
if __name__ == "__main__":
    root = tk.Tk()
    app = FileLoaderApp(root)
    root.mainloop()
