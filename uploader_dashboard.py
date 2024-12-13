import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from database import get_materials_by_uploader, insert_uploaded_material, update_uploaded_material, get_material_requests

def uploader_dashboard(uploader_id):
    def go_back():
        from shared import main
        root.destroy()  # Close the admin dashboard
        main()
    # Function to view all uploaded material
    def view_uploaded_materials():
        table_materials.delete(*table_materials.get_children()) 
        materials = get_materials_by_uploader(uploader_id)
        if materials:
            for material in materials:
                table_materials.insert(
                    "", "end",
                    values=(material[0], material[1], material[2], material[3], material[4])
                )
        else:
            messagebox.showinfo("Info", "No materials uploaded yet.")
    
    # Function for uploading a material
    def upload_material():
        material_name = entry_material_name.get()
        file_path = lbl_file_path["text"]  # Get the selected file path
        if material_name and file_path != "No file selected":
            insert_uploaded_material(uploader_id, material_name, file_path)
            messagebox.showinfo("Success", "Material uploaded successfully!")
            entry_material_name.delete(0, tk.END)  # Clear the entry box
            lbl_file_path["text"] = "No file selected"  # Reset file path label
            view_uploaded_materials()  # Refresh the material list
        else:
            messagebox.showerror("Error", "Please provide a material name and select a file.")

    def select_file():
        file_path = filedialog.askopenfilename(title="Select a file")
        if file_path:
            lbl_file_path["text"] = file_path

    def update_material():
        selected_item = table_materials.selection()
        if selected_item:
            material_id = table_materials.item(selected_item[0])["values"][0]
            new_name = entry_material_name.get()
            new_file = lbl_file_path["text"]
            if new_name and new_file != "No file selected":
                update_uploaded_material(material_id, new_name, new_file)
                messagebox.showinfo("Success", "Material updated successfully!")
                entry_material_name.delete(0, tk.END)
                lbl_file_path["text"] = "No file selected"
                view_uploaded_materials()  # Refresh the material list
            else:
                messagebox.showerror("Error", "Please provide both new material name and file path.")
        else:
            messagebox.showerror("Error", "Please select a material to update.")

    def view_material_requests():
        table_requests.delete(*table_requests.get_children())  # Clear the table
        material_requests = get_material_requests()
        if material_requests:
            for request in material_requests:
                request_id = request[0]
                description = request[1]
                status = request[2] if len(request) > 2 and request[2] else "Unknown"  # Handle missing status
                table_requests.insert(
                    "", "end",
                    values=(request_id, description, status)
                )
        else:
            messagebox.showinfo("Info", "No pending requests.")

    # Setup GUI for uploader dashboard
    root = tk.Tk()
    root.title("Uploader Dashboard")
    root.geometry("1360x500")
    root.configure(bg="black")
    root.resizable(False,False)
    tk.Button(
        root,
        text="Back",
        width = 15,
        height = 1,
        command=go_back,
        font=("Helvetica", 12, "bold"),
        bg="white",
        fg="black",
    ).pack(side="bottom", anchor="se", padx=10, pady=10)
    

    tk.Label(root, text="Uploader Dashboard", font=("Helvetica", 20, "bold"), bg="black", fg="white").pack(pady=10)

    # Material Requests Table
    frame_requests = tk.Frame(root, bg="black")
    frame_requests.pack(side="left", padx=10, pady=10)
    tk.Label(frame_requests, text="Material Requests", font=("Helvetica", 15, "bold"), bg="black", fg="white").pack(pady=5)
    columns_requests = ("Request ID", "Description", "Status")
    table_requests = ttk.Treeview(frame_requests, columns=columns_requests, show="headings", height=10)
    for col in columns_requests:
        table_requests.heading(col, text=col)
        table_requests.column(col, width=70 if col != "Description" else 300)
    table_requests.pack(pady=5)
    tk.Button(frame_requests, text="View Requests", font=("Helvetica", 10, "bold"), width=15, height=1, command=view_material_requests).pack(pady=5)

    # Uploaded Materials Table
    frame_materials = tk.Frame(root, bg="black")
    frame_materials.pack(side="left", padx=10, pady=10)
    tk.Label(frame_materials, text="Uploaded Materials", font=("Helvetica", 15, "bold"), bg="black", fg="white").pack(pady=5)
    columns_materials = ("ID", "Material Name", "File", "Status", "Uploader ID")
    table_materials = ttk.Treeview(frame_materials, columns=columns_materials, show="headings", height=10)
    for col in columns_materials:
        table_materials.heading(col, text=col)
        table_materials.column(col, width=90 if col != "File" else 300)
    table_materials.pack(pady=5)
    tk.Button(frame_materials, text="Refresh Materials", font=("Helvetica", 10, "bold"), width=15, height=1, command=view_uploaded_materials).pack(pady=5)

    # Upload and Update Section
    frame_upload = tk.Frame(root, bg="black")
    frame_upload.pack(side="left", padx=10, pady=10)
    tk.Label(frame_upload, text="Upload New Material", font=("Helvetica", 15, "bold"), bg="black", fg="white").pack(pady=10)
    tk.Label(frame_upload, text="Material Name:",font=("Helvetica", 10, "bold"), bg="black", fg="white").pack()
    entry_material_name = tk.Entry(frame_upload, font=("Helvetica", 10))
    entry_material_name.pack(pady=5)
    tk.Label(frame_upload, text="File:",font=("Helvetica", 10, "bold"), bg="black", fg="white").pack()
    lbl_file_path = tk.Label(frame_upload, text="No file selected",font=("Helvetica", 10), fg="white", bg="black")
    lbl_file_path.pack()
    tk.Button(frame_upload, text="Select File", font=("Helvetica", 10, "bold"), width=10, height=1, command=select_file).pack(pady=5)
    tk.Button(frame_upload, text="Upload Material", font=("Helvetica", 10, "bold"), width=15, height=1, command=upload_material).pack(pady=10)
    tk.Label(frame_upload, text="Update Material", font=("Helvetica", 15), bg="black", fg="white").pack(pady=10)
    tk.Button(frame_upload, text="Update Selected Material",font=("Helvetica", 10, "bold"), width=22, height=1, command=update_material).pack(pady=5)

    # Load uploaded materials on startup
    view_uploaded_materials()

    root.mainloop()