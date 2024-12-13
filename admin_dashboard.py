import tkinter as tk
from tkinter import messagebox, ttk
from database import (
    get_uploaded_materials,
    approve_material,
    reject_material,
    delete_material,
    approve_request,
    reject_request,
    delete_material_request,
    get_material_requests,
    get_all_users,
    delete_user,
)
from shared import main

def admin_dashboard():
    def go_back():
        from shared import main
        root.destroy() 
        main()
    # Function to refresh the materials table
    def refresh_materials():
        for row in table_materials.get_children():
            table_materials.delete(row)
        materials = get_uploaded_materials()
        if materials:
            for material in materials:
                table_materials.insert(
                    "",
                    "end",
                    values=(
                        material[0],
                        material[1],
                        material[2],
                        material[3],
                        material[4],
                    ),
                )

    # Functions for handling material actions
    def get_selected_material_id():
        selected_item = table_materials.focus()
        if selected_item:
            return table_materials.item(selected_item)["values"][0]
        return None

    def approve_material_selected():
        material_id = get_selected_material_id()
        if material_id:
            approve_material(material_id)
            messagebox.showinfo("Success", f"Material ID {material_id} approved!")
            refresh_materials()
        else:
            messagebox.showerror("Error", "Please select a material to approve.")

    def reject_material_selected():
        material_id = get_selected_material_id()
        if material_id:
            reject_material(material_id)
            messagebox.showinfo("Success", f"Material ID {material_id} rejected!")
            refresh_materials()
        else:
            messagebox.showerror("Error", "Please select a material to reject.")

    def delete_material_selected():
        material_id = get_selected_material_id()
        if material_id:
            delete_material(material_id)
            messagebox.showinfo("Success", f"Material ID {material_id} deleted!")
            refresh_materials()
        else:
            messagebox.showerror("Error", "Please select a material to delete.")

    # Function to refresh the requests table
    def load_requests():
        for row in table_requests.get_children():
            table_requests.delete(row)
        requests = get_material_requests()
        if requests:
            for request in requests:
                table_requests.insert(
                    "",
                    "end",
                    values=(
                        request[0],
                        request[1],
                        request[2],
                        request[3],
                    ),
                )

    # Functions for handling request actions
    def get_selected_request_id():
        selected_item = table_requests.focus()
        if selected_item:
            return table_requests.item(selected_item)["values"][0]
        return None

    def approve_request_material():
        request_id = get_selected_request_id()
        if request_id:
            approve_request(request_id)
            messagebox.showinfo("Success", f"Request ID {request_id} approved!")
            load_requests()
        else:
            messagebox.showerror("Error", "Please select a request to approve.")

    def reject_request_material():
        request_id = get_selected_request_id()
        if request_id:
            reject_request(request_id)
            messagebox.showinfo("Success", f"Request ID {request_id} rejected!")
            load_requests()
        else:
            messagebox.showerror("Error", "Please select a request to reject.")

    def delete_request_material():
        request_id = get_selected_request_id()
        if request_id:
            delete_material_request(request_id)
            messagebox.showinfo("Success", f"Request ID {request_id} deleted!")
            load_requests()
        else:
            messagebox.showerror("Error", "Please select a request to delete.")

    # Function to refresh the users table
    def refresh_users():
        for row in table_users.get_children():
            table_users.delete(row)
        users = get_all_users()
        if users:
            for user in users:
                password_masked = "*" * len(user[3]) if len(user) >= 4 else "N/A"
                table_users.insert(
                    "",
                    "end",
                    values=(
                        user[0],
                        user[1],
                        password_masked,
                        user[2],
                    ),
                )
    # Function for handling users action
    def delete_user_info():
        selected_item = table_users.focus()
        if selected_item:
            user_id = table_users.item(selected_item)["values"][0]
            delete_user(user_id)
            messagebox.showinfo("Success", f"User ID {user_id} deleted!")
            refresh_users()
        else:
            messagebox.showerror("Error", "Please select a user to delete.")

    # Setup GUI
    root = tk.Tk()
    root.title("Admin Dashboard")
    root.configure(bg="black")
    root.geometry("1530x500")  
    root.resizable(False, False)
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

    # Header
    tk.Label(
        root,
        text="Admin Dashboard",
        font=("Helvetica", 20, "bold"),
        bg="black",
        fg="white",
    ).pack(pady=10)
    
    # Material Requests Table
    frame_requests = tk.Frame(root, bg="black")
    frame_requests.pack(side="left", padx=5, pady=10)
    tk.Label(
        frame_requests, text="Material Requests", font=("Helvetica", 15, "bold"), bg="black", fg="white"
    ).pack(pady=5)
    columns_requests = ("ID", "Description", "Status", "Requester ID")
    table_requests = ttk.Treeview(
        frame_requests, columns=columns_requests, show="headings", height=10
    )
    for col in columns_requests:
        table_requests.heading(col, text=col)
        table_requests.column(col, width=100)
    table_requests.pack(pady=5)

    # Buttons for request actions
    action_buttons_requests = tk.Frame(frame_requests, bg="black")
    action_buttons_requests.pack(pady=10)
    tk.Button(action_buttons_requests, text="Approve",font=("Helvetica", 10, "bold"),width=10, height=1, command=approve_request_material).pack(
        side="left", padx=5
    )
    tk.Button(action_buttons_requests, text="Reject", font=("Helvetica", 10, "bold"),width=10, height=1, command=reject_request_material).pack(
        side="left", padx=5
    )
    tk.Button(action_buttons_requests, text="Delete", font=("Helvetica", 10, "bold"),width=10, height=1, command=delete_request_material).pack(
        side="left", padx=5
    )

    # Uploaded Materials Table
    frame_materials = tk.Frame(root, bg="black")
    frame_materials.pack(side="left", padx=5, pady=10)
    tk.Label(
        frame_materials, text="Uploaded Materials", font=("Helvetica", 15, "bold"), bg="black", fg="white"
    ).pack(pady=5)
    columns_materials = ("ID", "Material Name", "File", "Status", "Uploader ID")
    table_materials = ttk.Treeview(
        frame_materials, columns=columns_materials, show="headings", height=10
    )
    for col in columns_materials:
        table_materials.heading(col, text=col)
        if col == "File":
            table_materials.column(col, width=300) 
        else:
            table_materials.column(col, width=100)
            table_materials.pack(pady=5)

    # Buttons for material actions
    action_buttons_materials = tk.Frame(frame_materials, bg="black")
    action_buttons_materials.pack(pady=10)
    tk.Button(action_buttons_materials, text="Approve", font=("Helvetica", 10, "bold"),width=10, height=1, command=approve_material_selected).pack(
        side="left", padx=5
    )
    tk.Button(action_buttons_materials, text="Reject", font=("Helvetica", 10, "bold"),width=10, height=1, command=reject_material_selected).pack(
        side="left", padx=5
    )
    tk.Button(action_buttons_materials, text="Delete", font=("Helvetica", 10, "bold"),width=10, height=1, command=delete_material_selected).pack(
        side="left", padx=5
    )

    # Users Table
    frame_users = tk.Frame(root, bg="black")
    frame_users.pack(side="left", padx=5, pady=10)
    tk.Label(
        frame_users, text="Users", font=("Helvetica", 15, "bold"), bg="black", fg="white"
    ).pack(pady=5)
    columns_users = ("ID", "Username", "Password", "Role")
    table_users = ttk.Treeview(
        frame_users, columns=columns_users, show="headings", height=10
    )
    for col in columns_users:
        table_users.heading(col, text=col)
        table_users.column(col, width=100)
    table_users.pack(pady=5)

    # Buttons for user actions
    tk.Button(frame_users, text="Delete User", font=("Helvetica", 10, "bold"),width=10, height=1, command=delete_user_info).pack(pady=10)
    refresh_materials()
    load_requests()
    refresh_users()

    root.mainloop()