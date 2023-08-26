import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox
from tkinter.ttk import Progressbar, Style

def move_files_with_keywords(src_path, keywords, dest_folder_name, selected_file_endings, output_folder, progress_bar):
    moved_count = 0
    for gui, _, files in os.walk(src_path):
        for file in files:
            if any(keyword.lower() in file.lower() for keyword in keywords) and file.lower().endswith(tuple(selected_file_endings)):
                src_file_path = os.path.join(gui, file)
                if output_folder:
                    dest_folder = output_folder
                else:
                    dest_folder = os.path.join(src_path, dest_folder_name)
                
                dest_file_path = os.path.join(dest_folder, file)
                
                if not os.path.exists(dest_folder):
                    os.makedirs(dest_folder)
                
                shutil.move(src_file_path, dest_file_path)
                moved_count += 1
                progress_bar.step(1)
    
    return moved_count

def browse_source_path():
    global source_path
    source_path = filedialog.askdirectory()
    source_entry.delete(0, tk.END)
    source_entry.insert(0, source_path)

def browse_output_folder():
    global output_folder
    output_folder = filedialog.askdirectory()
    dest_folder_name_entry.delete(0, tk.END)
    dest_folder_name_entry.insert(0, output_folder)

def start_processing():
    keywords = keywords_entry.get().split()
    dest_folder_name = dest_folder_name_entry.get()
    selected_file_endings = file_endings_listbox.curselection()
    selected_file_endings = [file_endings[file_ending_index] for file_ending_index in selected_file_endings]
    
    custom_file_types = custom_file_types_entry.get().split(',')
    custom_file_types = [file_type.strip() for file_type in custom_file_types]
    
    selected_file_endings.extend(custom_file_types)
    
    progress_bar.start(len(os.listdir(source_path)))
    moved_count = move_files_with_keywords(source_path, keywords, dest_folder_name, selected_file_endings, output_folder, progress_bar)
    progress_bar.stop()
    
    messagebox.showinfo("File Moving Result", f"Moved {moved_count} files.")
    
    if output_folder:
        os.startfile(output_folder)
    else:
        new_folder_path = os.path.join(source_path, dest_folder_name)
        os.startfile(new_folder_path)

# Create the main GUI window
gui = tk.Tk()
gui.title("File Mover with Keywords")

style = Style()
style.configure("TButton", padding=10)
style.configure("TLabel", padding=10)

source_label = tk.Label(gui, text="Source Path:")
source_label.pack()

source_entry = tk.Entry(gui)
source_entry.pack()

browse_button = tk.Button(gui, text="Browse", command=browse_source_path)
browse_button.pack()

output_folder_var = tk.IntVar()
output_folder_checkbox = tk.Checkbutton(gui, text="Choose Output Folder", variable=output_folder_var, command=browse_output_folder)
output_folder_checkbox.pack()

dest_folder_name_label = tk.Label(gui, text="Destination Folder Name:")
dest_folder_name_label.pack()

dest_folder_name_entry = tk.Entry(gui)
dest_folder_name_entry.pack()

keywords_label = tk.Label(gui, text="Keywords (separated by spaces):")
keywords_label.pack()

keywords_entry = tk.Entry(gui)
keywords_entry.pack()

custom_file_types_label = tk.Label(gui, text="Custom File Types (comma separated):")
custom_file_types_label.pack()

custom_file_types_entry = tk.Entry(gui)
custom_file_types_entry.pack()

file_endings_label = tk.Label(gui, text="Select File Endings:")
file_endings_label.pack()

file_endings = [
    '.mp4', '.avi', '.mkv', '.mov', '.flv',
    '.mp3', '.wav', '.ogg', '.wma', '.aac',
    '.jpg', '.jpeg', '.png', '.gif', '.bmp',
    '.doc', '.docx', '.pdf', '.txt', '.csv',
    '.ppt', '.pptx', '.xls', '.xlsx', '.zip',
    '.rar', '.7z', '.tar', '.gz', '.exe',
    '.dll', '.py', '.html', '.css', '.js',
    '.json', '.xml', '.cpp', '.h', '.java',
    '.sql', '.php', '.rb', '.md', '.log',
    '.ico', '.svg', '.psd', '.ai', '.ttf'
]

file_endings_listbox = Listbox(gui, selectmode=tk.MULTIPLE)
for file_ending in file_endings:
    file_endings_listbox.insert(tk.END, file_ending)
file_endings_listbox.pack()

start_button = tk.Button(gui, text="Start Processing", command=start_processing)
start_button.pack()

progress_bar = Progressbar(gui, orient=tk.HORIZONTAL, length=300, mode='determinate')
progress_bar.pack()

source_path = ""
output_folder = ""

gui.mainloop()
