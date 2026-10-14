import os, shutil, datetime, sys, tkinter as tk
from tkinter import ttk, filedialog, messagebox


window = tk.Tk()
window.title("Smart File Organizer")
window.geometry("950x600")

box_frame = ttk.Frame(window)
output_box = tk.Text(box_frame, font=("Consolas", 10), bg="#1e1e1e", fg="#d4d4d4",
                     padx=10, pady=10, relief="flat", wrap="none")
class PrintToBox:
    def write(self,text):
        output_box.insert(tk.END,text)
        output_box.see(tk.END)
    def flush(self):
        pass
folder_map = {
    ".py": "Python Files",
    ".txt": "Text Files",
    ".csv": "CSV Files",
    ".json": "JSON Files",
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",

    ".pdf": "Documents",
    ".docx": "Documents",

    ".mp4": "Videos",
    ".mkv": "Videos",

    ".mp3": "Audio",
    ".wav": "Audio"
}

def organize_files(folder_path):
    current_time = datetime.datetime.now()
    real_time = f"Organization started at: {current_time.strftime('%Y-%m-%d %H:%M:%S')}"
    print("\n" + real_time + "\n")
    Add_file_logs(real_time)

    file_count = {
        ".py": 0,
        ".txt": 0,
        ".csv": 0,
        ".json": 0,
        ".jpg": 0,
        ".jpeg": 0,
        ".png": 0,

        ".pdf": 0,
        ".docx": 0,

        ".mp4": 0,
        ".mkv": 0,

        ".mp3": 0,
        ".wav": 0,
        "others": 0
    }

    files_scanned = {
        "scanned": 0
    }

    files_moved = {
        "moved": 0
    }

    Error_file = {}

    moves = []
    dupl_file = {}

    # Check each item in the selected folder
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        # Only work on real files
        if not os.path.isfile(item_path):
            continue
        if item in ("organization_log.txt", os.path.basename(__file__)):
            continue
        files_scanned["scanned"] += 1

        name, extension = os.path.splitext(item)
        extension = extension.lower()

        if extension in folder_map:
            target_folder = os.path.join(folder_path, folder_map[extension])
        else:
            target_folder = os.path.join(folder_path, "Others")

        os.makedirs(target_folder, exist_ok=True)
        destination = os.path.join(target_folder, item)


        try:
            if os.path.exists(destination):
                dupl_folder = os.path.join(folder_path, "Duplicate_Files")
                os.makedirs(dupl_folder, exist_ok=True)
                duplicate_destination = os.path.join(dupl_folder, item)

                n = 1
                while os.path.exists(duplicate_destination):
                    duplicate_destination = os.path.join(dupl_folder, f"{name} {n}{extension}")
                    n += 1
                shutil.move(item_path, duplicate_destination)
                dupl_file[item] = dupl_file.get(item, 0) + 1
                Add_file_logs(f"Duplicate file found: {item} -> Moved to Duplicate_Files")
            
            else:
                shutil.move(item_path, destination)
                Add_file_logs(f"{item} -> Moved to {target_folder}")

            files_moved["moved"] += 1
            if extension in folder_map:
                file_count[extension] += 1                       
            else:
                file_count["others"] += 1
        except  Exception as e:
            Error_file[item] = Error_file.get(item, 0) + 1
            Add_file_logs(f"ERROR: {item} -> {e}")

        
            

    print("\n...Organizing Files...\n")


    print("--------------------------------------------------------------------")
    print("                      ORGANIZATION COMPLETE!                        ")
    print("--------------------------------------------------------------------")

    present_time = datetime.datetime.now()
    orga_time = f"\nOrganization completed at: {present_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
    print("\n" + orga_time)
    Add_file_logs(orga_time)


    t_time = f"Total Time Taken: {(present_time - current_time).total_seconds():.2f} seconds"
    print(t_time+ "\n"+ "\n")
    Add_file_logs(t_time)

    print(f"Total Files Scanned: {files_scanned['scanned']}")
    print(f"Total Files Moved: {files_moved['moved']}\n")
    for item, count in Error_file.items():
        print(f"Error occurred while moving file: {item} -> {count} times")

    print(f"Python Files: {file_count['.py']}")
    print(f"CSV Files: {file_count['.csv']}")
    print(f"JSON Files: {file_count['.json']}")
    print(f"Text Files: {file_count['.txt']}")
    print(f"Image Files: {file_count['.jpg'] + file_count['.jpeg'] + file_count['.png']}")
    print(f"Document Files: {file_count['.pdf'] + file_count['.docx']}")
    print(f"Video Files: {file_count['.mp4'] + file_count['.mkv']}")
    print(f"Audio Files: {file_count['.mp3'] + file_count['.wav']}")
    if dupl_file:
        print("\nDuplicate files found:")
        for name, count in dupl_file.items():
            print(f"{name} -> {count} times")
    print(f"Other Files: {file_count['others']}")
    print("--------------------------------------------------------------------")


def preview_mode(folder_path):
    will_move = 0
    duplicate_files = 0
    other_files = 0
    per_category = {}
    lines = []


    for file in os.listdir(folder_path):
        if not os.path.isfile(os.path.join(folder_path, file)):
            continue

        _, extension = os.path.splitext(file)
        category = folder_map.get(extension.lower(), "Others")
        destination = os.path.join(folder_path, category, file)

        if os.path.exists(destination):
            lines.append(f"{file:<30} -> Duplicate_File")
            duplicate_files += 1
            will_move += 1
        else:
            lines.append(f"{file:<30} -> {category}")
            will_move += 1
        if category == "Others":
            other_files += 1
        per_category[category] = per_category.get(category, 0) + 1

    if not lines:
        print("No files found in the specified folder.")
        return

    print("===================================================================")
    print("                   ORGANIZATION PREVIEW                            ")
    print("===================================================================")

    print("\nFiles in each category:\n")
    for category, count in per_category.items():
        print(f"{category:<20}->  {count}")
    print("\n-----------------------------------------------------------------")
    print("Files will move in folder:\n")
    for line in lines:
            print(line)

    print("-------------------------------------------------------------------")
    print("\nFiles that will move: ", will_move)
    print("\nDuplicate files found: ", duplicate_files)
    print("\nFiles in Others category: ", other_files)
    print("===================================================================")
    print("\nNOTE: This is a preview mode. No files will be moved or modified.")
    #if messagebox.askyesno("Preview","Organize now?"):
    #    organize_files(folder_path)
    #else:
    #    print("Organization cancelled.")
def Add_file_logs(log_entry):
    with open("organization_log.txt", "a") as log_file:
        log_file.write(log_entry + "\n")
def show_organization_history():
    try:
        with open("organization_log.txt", "r") as log_file:
            print("\n")
            print("===================================================================")
            print("                        ORGANIZATION HISTORY                       ")
            print("===================================================================")
            print("\n")
            print(log_file.read())
    except FileNotFoundError:
        print("\nNo organization history found.")

def show_statistics(folder_path):
    print("--------------------------------------------------------------------")
    print("                   FILE STATISTICS                                  ")
    print("--------------------------------------------------------------------")

    
    file_count = {
        ".py": 0,
        ".txt": 0,
        ".csv": 0,
        ".json": 0,
        ".jpg": 0,
        ".jpeg": 0,
        ".png": 0,
        ".pdf": 0,
        ".docx": 0,
        ".mp4": 0,
        ".mkv": 0,
        ".mp3": 0,
        ".wav": 0,
        "others": 0
    }

    unorganized_files = 0
    other_folder_files = 0
    organized_files = 0

    total_files = 0
    duplicate_files = {}

    for current_folder, _, items in os.walk(folder_path):
        for item in items:
            item_path = os.path.join(current_folder, item)
            if not os.path.isfile(item_path):
                continue

            total_files += 1
            duplicate_files[item] = duplicate_files.get(item, 0) + 1

            _, extension = os.path.splitext(item)

            extension = extension.lower()
            if extension in file_count:
                file_count[extension] += 1
            else:
                file_count["others"] += 1


            relative_folder = os.path.relpath(current_folder, folder_path).lower()
            expected_folder = folder_map.get(extension, "Others").lower()

            if relative_folder == expected_folder or relative_folder == "duplicate_files":
               organized_files += 1
            elif relative_folder == ".":
               unorganized_files += 1
            else:
               other_folder_files += 1

    print(f"{'Total Files':<15} -> {total_files}\n")
    print(f"{'Python Files':<15} -> {file_count['.py']}")
    print(f"{'CSV Files':<15} -> {file_count['.csv']}")
    print(f"{'JSON Files':<15} -> {file_count['.json']}")
    print(f"{'Text Files':<15} -> {file_count['.txt']}")
    print(f"{'Image Files':<15} -> {file_count['.jpg'] + file_count['.jpeg'] + file_count['.png']}")
    print(f"{'Document Files':<15} -> {file_count['.pdf'] + file_count['.docx']}")
    print(f"{'Video Files':<15} -> {file_count['.mp4'] + file_count['.mkv']}")
    print(f"{'Audio Files':<15} -> {file_count['.mp3'] + file_count['.wav']}")
    print(f"{'Other Files':<15} -> {file_count['others']}")

    print(f"{'ALREADY ORGANIZED FILES':<15} -> {organized_files}")
    print(f"{'FILES TO ORGANIZE':<15} -> {unorganized_files}")
    print("--------------------------------------------------------------------")

    duplicates = {name: count for name, count in duplicate_files.items() if count > 1}
    if duplicates:
        print("\nDuplicate filenames found:")
        for name, count in duplicates.items():
            print(f"{name:<15} -> {count} times")
    else:
        print("\nNo duplicate files found.")

def clear():
    output_box.delete("1.0", tk.END)

def run_organize():
    folder = filedialog.askdirectory()
    if not folder:
        return
    if not messagebox.askyesno("Confirm", f"Organize {folder}?"):
        return
    clear()
    try:
        organize_files(folder)
        messagebox.showinfo("Done", "Files organized!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def run_preview():
    folder = filedialog.askdirectory()
    if folder:
        clear()
        preview_mode(folder)

def run_stats():
    folder = filedialog.askdirectory()
    if folder:
        clear()
        show_statistics(folder)

def run_history():
    clear()
    show_organization_history()

def show_organized_files(folder_path):
    print("ORGANIZED FILES\n")
    found = False
    for category in sorted(set(folder_map.values()) | {"Others", "Duplicate_Files"}):
        category_path = os.path.join(folder_path, category)
        if not os.path.isdir(category_path):
            continue
        files = [f for f in os.listdir(category_path)
                 if os.path.isfile(os.path.join(category_path, f))]
        if files:
            found = True
            print(f"{category} ({len(files)})")
            for f in files:
                print(f"   {f}")
            print()
    if not found:
        print("No organized files found.")

def run_organized():
    folder = filedialog.askdirectory()
    if folder:
        clear()
        show_organized_files(folder)

def main():
    style = ttk.Style()
    style.theme_use("clam")
    GREY = "#e6e6e6"
    window.configure(bg=GREY)
    style.configure("TFrame", background=GREY)
    style.configure("TLabel", background=GREY)
    style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=8)

    ttk.Label(window, text="Smart File Organizer",
              font=("Segoe UI", 20, "bold")).pack(pady=(15, 0))
    ttk.Label(window, text="Sort your messy folders in one click",
              font=("Segoe UI", 10)).pack(pady=(0, 10))

    button_frame = ttk.Frame(window)
    button_frame.pack(pady=5)
    ttk.Button(button_frame, text="Organize Files", command=run_organize).grid(row=0, column=0, padx=5)
    ttk.Button(button_frame, text="Preview Mode", command=run_preview).grid(row=0, column=1, padx=5)
    ttk.Button(button_frame, text="Show Statistics", command=run_stats).grid(row=0, column=2, padx=5)
    ttk.Button(button_frame, text="Organization History", command=run_history).grid(row=0, column=3, padx=5)
    ttk.Button(button_frame, text="Organized Files", command=run_organized).grid(row=0, column=4, padx=5)

    box_frame.pack(fill="both", expand=True, padx=15, pady=15)
    scrollbar = ttk.Scrollbar(box_frame, command=output_box.yview)
    output_box.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    output_box.pack(side="left", fill="both", expand=True)

    sys.stdout = PrintToBox()

main()
window.mainloop()
