import tkinter as tk
from tkinter import messagebox, ttk
from database import insert_material_request, get_uploaded_materials, get_all_requests

def viewer_dashboard(viewer_id):
    def go_back():
        from shared import main
        root.destroy()  # Close the admin dashboard
        main()
    # Function for submitting a request
    def submit_request():
        request_description = text_request_description.get("1.0", tk.END).strip() 
        if request_description:
            insert_material_request(viewer_id, request_description)
            messagebox.showinfo("Success", "Material request submitted successfully!")
            text_request_description.delete("1.0", tk.END)
            load_requests() 
        else:
            messagebox.showerror("Error", "Please provide a description.")

    # Function for viewing all materials from uploader
    def view_all_materials():
        for row in table_materials.get_children():
            table_materials.delete(row)
        materials = get_uploaded_materials()
        if materials:
            for material in materials:
                table_materials.insert(
                    "",
                    "end",
                    values=(material[0], material[1], material[2], material[3], material[4]),
                )
        else:
            messagebox.showinfo("Info", "No matching materials found.")

    # Function to refresh request table
    def load_requests():
        for row in table_requests.get_children():
            table_requests.delete(row)
        requests = get_all_requests(viewer_id)
        if requests:
            for request in requests:
                table_requests.insert(
                    "",
                    "end",
                    values=(request[0], request[1], request[2])
                )
        else:
            messagebox.showinfo("Info", "No material requests found.")

    # Setup GUI
    root = tk.Tk()
    root.title("Viewer Dashboard")
    root.geometry("1380x670")
    root.configure(bg="black")
    root.resizable(False,False)

    root.grid_columnconfigure(0, weight=1, minsize=500)
    root.grid_columnconfigure(1, weight=1, minsize=500)
    
    tk.Label(root, text="Viewer Dashboard", font=("Helvetica", 18, "bold"), bg="black", fg="white").grid(row=0, columnspan=2, pady=10)

    # Request Submission Section
    frame_request = tk.Frame(root, bg="black")
    frame_request.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
    frame_request.grid_columnconfigure(0, weight=1)

    tk.Label(frame_request, text="Submit a Material Request", font=("Helvetica", 15, "bold"), bg="black", fg="white").grid(row=0, column=0, pady=10, sticky="W")
    tk.Label(frame_request, text="Description of Material:", font=("Helvetica", 12, "bold"), bg="black", fg="white").grid(row=1, column=0, sticky="W")
    text_request_description = tk.Text(frame_request, font=("Helvetica", 10), bg="white", fg="black", width=50, height=10)
    text_request_description.grid(row=2, column=0, padx=5, pady=5)

    tk.Button(frame_request, text="Submit Request", width=15, height=1, font=("Helvetica", 12, "bold"), command=submit_request).grid(row=3, column=0, pady=10)

    # Request Table
    tk.Label(frame_request, text="List of Material Requests", font=("Helvetica", 15, "bold"), bg="black", fg="white").grid(row=4, column=0, pady=5, sticky="W")
    columns_requests = ("Request ID", "Description", "Status")
    table_requests = ttk.Treeview(frame_request, columns=columns_requests, show="headings", height=10)
    for col in columns_requests:
        if col == "Description":
            table_requests.heading(col, text=col)
            table_requests.column(col, anchor="w", width=300)
        else:
            table_requests.heading(col, text=col)
            table_requests.column(col, anchor="w", width=90)

    table_requests.grid(row=5, column=0, pady=5)

    # Material Viewing Section 
    frame_materials = tk.Frame(root, bg="black")
    frame_materials.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
    frame_materials.grid_columnconfigure(0, weight=1)

    tk.Label(frame_materials, text="View All Uploaded Materials", font=("Helvetica", 15, "bold"), bg="black", fg="white").grid(row=0, column=0, pady=10, sticky="W")

    tk.Button(frame_materials, text="View Materials", width=15, height=1, font=("Helvetica", 12, "bold"), command=view_all_materials).grid(row=1, column=0, pady=10)

    # Materials Table
    columns_materials = ("ID", "Material Name", "File", "Uploader ID", "Status")
    table_materials = ttk.Treeview(frame_materials, columns=columns_materials, show="headings", height=20)

    # Set column widths
    for col in columns_materials:
        if col == "File":
            table_materials.heading(col, text=col)
            table_materials.column(col, anchor="w", width=380)  
        else:
            table_materials.heading(col, text=col)
            table_materials.column(col, anchor="w", width=100)

    table_materials.grid(row=2, column=0, pady=5)

    tk.Button(frame_materials, text="Back", width=15, height=1, font=("Helvetica", 12, "bold"), command=go_back).grid(row=3, column=0, pady=10,padx=15, sticky = 'e')

    load_requests()

    root.mainloop()