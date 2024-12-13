import tkinter as tk
from tkinter import messagebox
from database import insert_user, validate_login
from uploader_dashboard import uploader_dashboard
from admin_dashboard import admin_dashboard
from viewer_dashboard import viewer_dashboard 

def erms_main():
    # Function for registration
    def register():
        username = entry_username_reg.get()
        password = entry_password_reg.get()
        role = selected_role.get()

        if username and password and role:
            insert_user(username, password, role)
            messagebox.showinfo("Success", "User registered successfully!")
            entry_username_reg.delete(0, tk.END)
            entry_password_reg.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Please fill all fields")

    # Function for login
    def login():
        username = entry_username_login.get()
        password = entry_password_login.get()
        role = selected_role.get()

        user = validate_login(username, password, role)
        if user:
            messagebox.showinfo("Success", f"Welcome {role}!")
            entry_username_login.delete(0, tk.END)
            entry_password_login.delete(0, tk.END)
            selected_role.set("")

            if role == "Admin":
                main_root.destroy()
                admin_dashboard()  # Admin dashboard
            elif role == "Uploader":
                main_root.destroy()
                uploader_dashboard(user[0])  # Uploader dashboard, pass uploader ID
            elif role == "Viewer":
                main_root.destroy()
                viewer_dashboard(user[0])  # Viewer dashboard, pass viewer ID
        else:
            messagebox.showerror("Error", "Invalid credentials or role")

    # Show login screen
    def show_login():
        role_frame.pack_forget()
        register_frame.pack_forget()
        login_frame.pack(pady=80)

    # Show registration screen
    def show_register():
        login_frame.pack_forget()
        register_frame.pack(pady=90)

    # Select a role (Admin/Uploader/Viewer)
    def select_role(role):
        selected_role.set(role)
        show_login()

    # Show the role selection screen
    def show_role_selection():
        login_frame.pack_forget()
        register_frame.pack_forget()
        role_frame.pack(pady=110)
    
    def exit():
        main_root.destroy()

    # Main GUI setup
    main_root = tk.Tk()
    main_root.title("User Role Selection")
    main_root.geometry("1000x500")
    main_root.configure(bg="black")
    main_root.resizable(False, False)
    selected_role = tk.StringVar()

    tk.Button(
        main_root,
        text="Exit",
        width = 15,
        height = 1,
        command=exit,
        font=("Helvetica", 12, "bold"),
        bg="white",
        fg="black",
    ).pack(side="bottom", anchor="se", padx=10, pady=10)

    # Role selection frame
    role_frame = tk.Frame(main_root, padx = 20, pady = 20, bg="black", relief=tk.RIDGE, bd=2)
    tk.Label(role_frame, text="Select Your Role", font=("Helvetica", 25, "bold"), bg="black", fg = "white").grid(row=0, columnspan=2, pady=30)
    tk.Button(role_frame, text="Admin", width = 15, height = 1, command=lambda: select_role("Admin"), font=("Helvetica", 12, "bold"), bg="white", fg="black").grid(row=1, column=0, padx=5, pady=10)
    tk.Button(role_frame, text="Uploader", width = 15, height = 1,  command=lambda: select_role("Uploader"), font=("Helvetica", 12, "bold"), bg="white", fg="black").grid(row=1, column=1, padx=5, pady=10)
    tk.Button(role_frame, text="Viewer", width = 15, height = 1, command=lambda: select_role("Viewer"), font=("Helvetica", 12, "bold"), bg="white", fg="black").grid(row=2, columnspan=2, pady=5)
    role_frame.pack(padx=20, pady=20)

    # Login frame
    login_frame = tk.Frame(main_root, padx=20, pady=20, bg="black", relief=tk.RIDGE, bd=2)
    tk.Label(login_frame, text="Login", font=("Helvetica", 18, "bold"), bg="black", fg = "white").grid(row=0, columnspan=2, pady=10)
    tk.Label(login_frame, text="Username:", font=("Helvetica", 12, "bold"), bg="black", fg = "white").grid(row=1, column=0, sticky="e", pady=5)
    tk.Label(login_frame, text="Password:", font=("Helvetica", 12, "bold"), bg="black", fg = "white").grid(row=2, column=0, sticky="e", pady=5)

    entry_username_login = tk.Entry(login_frame, font=("Helvetica", 12, "bold"), bg = "black", fg = "white")
    entry_password_login = tk.Entry(login_frame, show="*", font=("Helvetica", 12, "bold"), bg = "black", fg = "white")
    entry_username_login.grid(row=1, column=1, pady=5)
    entry_password_login.grid(row=2, column=1, pady=5)

    tk.Button(login_frame, text="Login", width = 10, height = 1, command=login, font=("Helvetica", 12, "bold"), bg="white", fg="black").grid(row=3, columnspan=2,padx= 10, pady=10)
    tk.Label(login_frame, text="Don't have an account?", font=("Helvetica", 12), bg="black", fg = "white").grid(row=4, columnspan=2, pady=5)
    tk.Button(login_frame, text="Sign Up", width = 10, height = 1, command=show_register, font=("Helvetica", 12, "bold"), bg="white", fg="black").grid(row=5, columnspan=2, pady=5)
    tk.Button(login_frame, text="Back", width = 10, height = 1, command=show_role_selection, font=("Helvetica", 12, "bold"), bg="white", fg="black").grid(row=6, columnspan=2, pady=10)

    # Register frame
    register_frame = tk.Frame(main_root, padx=20, pady=20, bg="black", relief=tk.RIDGE, bd=2)
    tk.Label(register_frame, text="Register", font=("Helvetica", 18, "bold"), bg="black", fg = "white").grid(row=0, columnspan=2, pady=10)
    tk.Label(register_frame, text="Username:", font=("Helvetica", 12, "bold"), bg="black", fg = "white").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    tk.Label(register_frame, text="Password:", font=("Helvetica", 12, "bold"), bg="black", fg = "white").grid(row=2, column=0, sticky="e", padx=5, pady=5)

    entry_username_reg = tk.Entry(register_frame, font=("Helvetica", 12, "bold"), bg = "black", fg = "white")
    entry_password_reg = tk.Entry(register_frame, show="*", font=("Helvetica", 12, "bold"), bg = "black", fg = "white")
    entry_username_reg.grid(row=1, column=1, pady=5)
    entry_password_reg.grid(row=2, column=1, pady=5)

    tk.Button(register_frame, text="Register", width = 10, height = 1, command=register, font=("Helvetica", 12, "bold"), bg="white", fg="black").grid(row=3, columnspan=2, pady=10)
    tk.Label(register_frame, text="Already have an account?", font=("Helvetica", 12), bg="black", fg="white").grid(row=4, columnspan=2, pady=10)
    tk.Button(register_frame, text="Login", width = 10, height = 1, command=show_login, font=("Helvetica", 12, "bold"), bg="white", fg="black").grid(row=5, columnspan=2, pady=5)

    show_role_selection()

    main_root.mainloop()
erms_main()