import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
import mysql.connector
from tkinter import PhotoImage
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Database connection
db = mysql.connector.connect(
    host="",#Your Database Hostname
    user="",#Your Database Username
    password="",#Your Database Password
    database=""#Database name where tables are created
)
cursor = db.cursor()

# Main App Window
root = tk.Tk()
root.title("Explore Duniya")
root.geometry("1000x800")
root.config(bg="#f7f7f7")

# Adding Background Image to Main Window
canvas = tk.Canvas(root, width=800, height=800)
canvas.pack(fill="both", expand=True)

# Load and display the background image
bg_image = PhotoImage(file="background.png")  # can use any image here just replace it with your image's path name
canvas.create_image(0, 0, image=bg_image, anchor="nw")

# Title Label (Centered, Black Color)
canvas.create_text(400, 100, text="Welcome to Explore Duniya", font=("Brush Script MT", 40 ), fill="black")

# Signup Window
def signup():
    def register_user():
        name = name_entry.get()
        age = age_entry.get()
        email = email_entry.get()
        password = password_entry.get()

        if not name or not age or not email or not password:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            cursor.execute("INSERT INTO users (name, age, email, password) VALUES (%s, %s, %s, %s)",
                           (name, age, email, password))
            db.commit()
            messagebox.showinfo("Success", "Signup successful! Please login.")
            signup_window.destroy()
        except mysql.connector.IntegrityError:
            messagebox.showerror("Error", "Email already registered!")

    signup_window = tk.Toplevel(root)
    signup_window.title("Explore Duniya")
    signup_window.geometry("400x400")
    signup_window.config(bg="#e1f5fe")
    # Adding Background Image to Main Window
    canvas = tk.Canvas(root, width=800, height=800)
    canvas.pack(fill="both", expand=True)

    

    tk.Label(signup_window, text="Sign Up", font=("Algerian", 24,), bg="#e1f5fe").pack(pady=20, anchor="w", padx=20)
    tk.Label(signup_window, text="Name:", font=("Times New Roman", 12), bg="#e1f5fe").pack(anchor="w", padx=20)
    name_entry = tk.Entry(signup_window, font=("Times New Roman", 12))
    name_entry.pack(padx=20, pady=5, anchor="w")

    tk.Label(signup_window, text="Age:", font=("Times New Roman", 12), bg="#e1f5fe").pack(anchor="w", padx=20)
    age_entry = tk.Entry(signup_window, font=("Times New Roman", 12))
    age_entry.pack(padx=20, pady=5, anchor="w")

    tk.Label(signup_window, text="Email:", font=("Times New Roman", 12), bg="#e1f5fe").pack(anchor="w", padx=20)
    email_entry = tk.Entry(signup_window, font=("Times New Roman", 12))
    email_entry.pack(padx=20, pady=5, anchor="w")

    tk.Label(signup_window, text="Password:", font=("Times New Roman", 12), bg="#e1f5fe").pack(anchor="w", padx=20)
    password_entry = tk.Entry(signup_window, show="*", font=("Times New Roman", 12))
    password_entry.pack(padx=20, pady=5, anchor="w")

    tk.Button(signup_window, text="Sign Up", font=("Times New Roman", 12, "bold"), bg="#0288d1", fg="white", 
              command=register_user).pack(pady=20, anchor="w", padx=20)

# Login Window
def login():
    def authenticate():
        email = email_entry.get()
        password = password_entry.get()

        cursor.execute("SELECT id FROM users WHERE email = %s AND password = %s", (email, password))
        result = cursor.fetchone()

        if result:
            messagebox.showinfo("Success", "Login successful!")
            login_window.destroy()
            user_panel()
        else:
            messagebox.showerror("Error", "Invalid email or password!")
        return result
    login_window = tk.Toplevel(root)
    login_window.title("Explore Duniya")
    login_window.geometry("400x300")
    login_window.config(bg="#e8f5e9")

    tk.Label(login_window, text="Login", font=("Algerian", 24), bg="#e8f5e9").pack(pady=20, anchor="w", padx=20)
    tk.Label(login_window, text="Email:", font=("Times New Roman", 12), bg="#e8f5e9").pack(anchor="w", padx=20)
    email_entry = tk.Entry(login_window, font=("Times New Roman", 12))
    email_entry.pack(padx=20, pady=5, anchor="w")

    tk.Label(login_window, text="Password:", font=("Times New Roman", 12), bg="#e8f5e9").pack(anchor="w", padx=20)
    password_entry = tk.Entry(login_window, show="*", font=("Times New Roman", 12))
    password_entry.pack(padx=20, pady=5, anchor="w")

    tk.Button(login_window, text="Login", font=("Times New Roman", 12, "bold"), bg="#388e3c", fg="white",
              command=authenticate).pack(pady=20, anchor="w", padx=20)
# Booking Window
# Booking Window with Enhanced Design


def user_panel():
    def show_booking_window():
        user_panel_window.destroy()  # Close the selection window
        book_package()

    def show_cancel_booking_window():
        user_panel_window.destroy()  # Close the selection window
        cancel_booking()

    # Main User Panel Window
    user_panel_window = tk.Tk()
    user_panel_window.title("Explore Duniya")
    user_panel_window.geometry("400x400")
    user_panel_window.config(bg="#f0f8ff")

    # Header Section
    header_frame = tk.Frame(user_panel_window, bg="#0288d1", pady=20)
    header_frame.pack(fill="x")
    tk.Label(header_frame, text="User Panel", font=("Times New Roman", 20, "bold"), fg="white", bg="#0288d1").pack()

    # Selection Section
    selection_frame = tk.Frame(user_panel_window, bg="#ffffff", pady=40)
    selection_frame.pack(fill="both", expand=True)

    tk.Label(selection_frame, text="What would you like to do?", font=("Times New Roman", 16), bg="#ffffff").pack(pady=10)

    tk.Button(selection_frame, text="Book Package", font=("Times New Roman", 14, "bold"), bg="#4caf50", fg="white", 
              command=show_booking_window, width=15).pack(pady=10)

    tk.Button(selection_frame, text="Cancel Booking", font=("Times New Roman", 14, "bold"), bg="#f44336", fg="white", 
              command=show_cancel_booking_window, width=15).pack(pady=10)

    # Footer Section
    footer_frame = tk.Frame(user_panel_window, bg="#f0f8ff", pady=10)
    footer_frame.pack(fill="x")
    tk.Label(footer_frame, text="Powered by Explore Duniya", font=("Times New Roman", 10), bg="#f0f8ff", fg="#0288d1").pack()

    user_panel_window.mainloop()


def book_package():
    

    def send_booking_email(email, package_name, travel_date, total_cost):
        """
        Sends a booking confirmation email.

        Args:
            email (str): The recipient's email address.
            package_name (str): Name of the package booked.
            travel_date (str): Date of travel.
            total_cost (float): Total cost of the booking.
        """
        # Sender and recipient details
        sender_email = ""  # Replace with your email
        sender_password = ""  # Replace with your email's app password 
        recipient_email = email

        # Compose the email
        subject = "Booking Confirmation - Explore Duniya"
        body = f"""
        Dear Customer,

        Thank you for booking with Explore Duniya!

        Here are your booking details:
        - Package Name: {package_name}
        - Date of Travel: {travel_date}
        - Total Cost: ₹{total_cost}
        

        We hope you have a great journey!

        Regards,
        The Explore Duniya Team
        """

        try:
            # Set up the MIME structure
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = recipient_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))

            # Connect to the SMTP server and send the email
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()  # Upgrade to secure connection
                server.login(sender_email, sender_password)  # Login to the server
                server.send_message(message)  # Send the email

            print("Email sent successfully!")

        except Exception as e:
            print(f"Failed to send email: {e}")

    def update_details(event):
        """Update the description, price, and image based on the selected package."""
        selected_package = package_dropdown.get()
        if selected_package:
            # Update description
            cursor.execute("SELECT description FROM packages WHERE package_name = %s", (selected_package,))
            description_result = cursor.fetchone()
            description_box.delete("1.0", tk.END)  # Clear previous description
            description_box.insert(tk.END, description_result[0] if description_result else "Description not available.")
            
            # Update price
            cursor.execute("SELECT price_per_person FROM packages WHERE package_name = %s", (selected_package,))
            price_result = cursor.fetchone()
            price_box.delete("1.0", tk.END)  # Clear previous price
            price_box.insert(tk.END, str(price_result[0]) if price_result else "Price not available.")

           

    def calculate_total_travellers(*args):
        """Calculate the total number of travellers."""
        try:
            males = int(males_entry.get() or 0)
            females = int(females_entry.get() or 0)
            children = int(children_entry.get() or 0)
            total_travellers.set(males + females + children)
        except ValueError:
            total_travellers.set(0)

    def confirm_booking():
        """Confirm booking and store the data in the database."""
        # Get the required inputs
        selected_package = package_dropdown.get()
        travel_date = travel_date_entry.get()
        EMail = EMail_entry.get().strip()

        try:
            males = int(males_entry.get() or 0)  # Fetch number of males
            females = int(females_entry.get() or 0)  # Fetch number of females
            children = int(children_entry.get() or 0)  # Fetch number of children
            total_travellers = males + females + children  # Calculate total travelers
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for travelers!")
            return

        # Validate inputs
        if not selected_package:
            messagebox.showerror("Error", "Please select a package!")
            return
        if not travel_date:
            messagebox.showerror("Error", "Please enter the date of travel!")
            return
        if total_travellers <= 0:
            messagebox.showerror("Error", "Please enter valid traveler details!")
            return

        try:
            # Fetch user ID based on email
            cursor.execute('SELECT id FROM users WHERE email=%s', (EMail,))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Error", "Email not registered!")
                return
            user_id = result[0]

            # Insert booking details
            cursor.execute(
                "INSERT INTO bookings (package_name, user_id, travel_date, total_travellers) VALUES (%s, %s, %s, %s)",
                (selected_package, user_id, travel_date, total_travellers),
            )
            db.commit()

            # Fetch package price
            cursor.execute("SELECT price_per_person FROM packages WHERE package_name = %s", (selected_package,))
            price_per_person = cursor.fetchone()[0]
            total_cost = price_per_person * total_travellers

            # Send confirmation email
            send_booking_email(EMail, selected_package, travel_date, total_cost)

            messagebox.showinfo("Success", f"Package '{selected_package}' has been booked successfully!")
            booking_window.destroy()
            user_panel()  # Return to user panel
        except Exception as e:
            messagebox.showerror("Error", f"Error booking package: {e}")



    # Booking Window
    booking_window = tk.Tk()
    booking_window.title("Explore Duniya")
    booking_window.geometry("1600x1600")
    booking_window.config(bg="#f0f8ff")

    tk.Label(
        booking_window, text="Book Package", font=("Times New Roman", 20, "bold"), bg="#4caf50", fg="white"
    ).pack(fill="x", pady=10)

    frame = tk.Frame(booking_window, bg="#ffffff", padx=20, pady=20)
    frame.pack(fill="both", expand=True)

    # Package Dropdown
    tk.Label(frame, text="Select Package:", font=("Times New Roman", 14), bg="#ffffff").grid(row=0, column=0, sticky="w", pady=5)
    cursor.execute("SELECT package_name FROM packages")
    packages = [row[0] for row in cursor.fetchall()]
    package_dropdown = ttk.Combobox(frame, values=packages, state="readonly", font=("Times New Roman", 12), width=30)
    package_dropdown.grid(row=0, column=1, pady=5)
    package_dropdown.bind("<<ComboboxSelected>>", update_details)

    
    # Description Box
    tk.Label(frame, text="Package Description:", font=("Times New Roman", 14), bg="#ffffff").grid(row=2, column=0, sticky="nw", pady=5)
    description_box = tk.Text(frame, wrap="word", font=("Times New Roman", 12), height=6, width=40, bg="#f7f7f7", relief="solid")
    description_box.grid(row=2, column=1, sticky="w", pady=5)

    # Price Box
    tk.Label(frame, text="Package Price:", font=("Times New Roman", 14), bg="#ffffff").grid(row=3, column=0, sticky="nw", pady=5)
    price_box = tk.Text(frame, wrap="word", font=("Times New Roman", 12), height=1, width=40, bg="#f7f7f7", relief="solid")
    price_box.grid(row=3, column=1, sticky="w", pady=5)

    # Male, Female, and Children Count
    tk.Label(frame, text="Number of Males:", font=("Times New Roman", 14), bg="#ffffff").grid(row=4, column=0, sticky="w", pady=5)
    males_entry = tk.Entry(frame, font=("Times New Roman", 12), width=10)
    males_entry.grid(row=4, column=1, pady=5, sticky="w")
    males_entry.bind("<KeyRelease>", calculate_total_travellers)

    tk.Label(frame, text="Number of Females:", font=("Times New Roman", 14), bg="#ffffff").grid(row=4, column=2, sticky="w", pady=5)
    females_entry = tk.Entry(frame, font=("Times New Roman", 12), width=10)
    females_entry.grid(row=4, column=3, pady=5, sticky="w")
    females_entry.bind("<KeyRelease>", calculate_total_travellers)

    tk.Label(frame, text="Number of Children:", font=("Times New Roman", 14), bg="#ffffff").grid(row=4, column=5, sticky="w", pady=5)
    children_entry = tk.Entry(frame, font=("Times New Roman", 12), width=10)
    children_entry.grid(row=4, column=6, pady=5, sticky="w")
    children_entry.bind("<KeyRelease>", calculate_total_travellers)

    # Total Travellers
    total_travellers = tk.IntVar(value=0)
    
    
    

    # Date of Travel
    tk.Label(frame, text="Date of Travel (YYYY-MM-DD):", font=("Times New Roman", 14), bg="#ffffff").grid(row=5, column=0, sticky="w", pady=5)
    travel_date_entry = tk.Entry(frame, font=("Times New Roman", 12), width=20)
    travel_date_entry.grid(row=5, column=1, pady=5, sticky="w")

    tk.Label(frame, text="Registered E-Mail:", font=("Times New Roman", 14), bg="#ffffff").grid(row=5, column=2, sticky="w", pady=5)
    EMail_entry = tk.Entry(frame, font=("Times New Roman", 12), width=20)
    EMail_entry.grid(row=5, column=3, pady=5, sticky="w")

    # Confirm Booking Button
    tk.Button(frame, text="Confirm Booking", font=("Times New Roman", 14, "bold"), bg="#4caf50", fg="white", command=confirm_booking).grid(
        row=6, column=0, columnspan=2, pady=20
    )

    booking_window.mainloop()






def cancel_booking():
    def confirm_cancellation():
        email = email_entry.get()
        if not email:
            messagebox.showerror("Error", "Please enter your registered email!")
            return

        try:
            # Fetch user_id from the users table using the entered email
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            user_id = cursor.fetchone()

            if not user_id:
                messagebox.showerror("Error", "No user found with this email!")
                return

            user_id = user_id[0]

            # Fetch bookings for the user based on the user_id
            cursor.execute("SELECT package_name FROM bookings WHERE user_id = %s", (user_id,))
            bookings = [row[0] for row in cursor.fetchall()]

            if not bookings:
                messagebox.showerror("Error", "No bookings found for this user!")
                return

            # Update the dropdown with bookings for the user
            booking_dropdown['values'] = bookings
            booking_dropdown.set('')  # Clear any previously selected booking

        except Exception as e:
            messagebox.showerror("Error", f"Error fetching bookings: {e}")

    def confirm_cancel_booking():
        selected_booking = booking_dropdown.get()
        if not selected_booking:
            messagebox.showerror("Error", "Please select a booking to cancel!")
            return

        email = email_entry.get()
        if not email:
            messagebox.showerror("Error", "Please enter your registered email!")
            return

        try:
            # Fetch user_id from the users table using the entered email
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            user_id = cursor.fetchone()

            if not user_id:
                messagebox.showerror("Error", "No user found with this email!")
                return

            user_id = user_id[0]

            # Delete the booking from the bookings table
            cursor.execute("DELETE FROM bookings WHERE package_name = %s AND user_id = %s", (selected_booking, user_id))
            db.commit()
            messagebox.showinfo("Success", f"Booking for '{selected_booking}' has been cancelled!")
            cancel_booking_window.destroy()
            user_panel()  # Return to user panel

        except Exception as e:
            messagebox.showerror("Error", f"Error cancelling booking: {e}")

    # Cancel Booking Window
    cancel_booking_window = tk.Tk()
    cancel_booking_window.title("Explore Duniya")
    cancel_booking_window.geometry("500x500")
    cancel_booking_window.config(bg="#f0f8ff")

    tk.Label(cancel_booking_window, text="Cancel Booking", font=("Times New Roman", 20, "bold"), bg="#f44336", fg="white").pack(fill="x", pady=10)

    frame = tk.Frame(cancel_booking_window, bg="#ffffff", padx=20, pady=20)
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Enter Registered Email:", font=("Times New Roman", 14), bg="#ffffff").pack(anchor="w")

    # Email Entry Field
    email_entry = tk.Entry(frame, font=("Times New Roman", 12), width=30)
    email_entry.pack(pady=10)

    tk.Label(frame, text="Select Booking:", font=("Times New Roman", 14), bg="#ffffff").pack(anchor="w")

    # Empty booking dropdown initially
    booking_dropdown = ttk.Combobox(frame, state="readonly", font=("Times New Roman", 12), width=30)
    booking_dropdown.pack(pady=10)

    tk.Button(frame, text="Fetch Bookings", font=("Times New Roman", 14, "bold"), bg="#4caf50", fg="white", command=confirm_cancellation).pack(pady=10)
    tk.Button(frame, text="Cancel Booking", font=("Times New Roman", 14, "bold"), bg="#f44336", fg="white", command=confirm_cancel_booking).pack(pady=20)

    cancel_booking_window.mainloop()






# Admin Login Window
def admin_login():
    def authenticate_admin():
        username = admin_user_entry.get()
        password = admin_pass_entry.get()

        cursor.execute("SELECT id FROM admins WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()

        if result:
            messagebox.showinfo("Success", "Admin login successful!")
            admin_login_window.destroy()
            admin_panel()
        else:
            messagebox.showerror("Error", "Invalid admin credentials!")

    admin_login_window = tk.Toplevel(root)
    admin_login_window.title("Explore Duniya")
    admin_login_window.geometry("400x300")
    admin_login_window.config(bg="#fffde7")

    tk.Label(admin_login_window, text="Admin Login", font=("Algerian", 24), bg="#fffde7").pack(pady=20, anchor="w", padx=20)
    tk.Label(admin_login_window, text="Username:", font=("Times New Roman", 12), bg="#fffde7").pack(anchor="w", padx=20)
    admin_user_entry = tk.Entry(admin_login_window, font=("Times New Roman", 12))
    admin_user_entry.pack(padx=20, pady=5, anchor="w")

    tk.Label(admin_login_window, text="Password:", font=("Times New Roman", 12), bg="#fffde7").pack(anchor="w", padx=20)
    admin_pass_entry = tk.Entry(admin_login_window, show="*", font=("Times New Roman", 12))
    admin_pass_entry.pack(padx=20, pady=5, anchor="w")

    tk.Button(admin_login_window, text="Login", font=("Times New Roman", 12, "bold"), bg="#f57c00", fg="white",
              command=authenticate_admin).pack(pady=20, anchor="w", padx=20)


def admin_panel():
    def show_add_package_window():
        admin_panel_window.destroy()  # Close the selection window
        add_package()

    def show_remove_package_window():
        admin_panel_window.destroy()  # Close the selection window
        remove_package()

    # Main Admin Panel Window
    admin_panel_window = tk.Tk()
    admin_panel_window.title("Explore Duniya")
    admin_panel_window.geometry("400x400")
    admin_panel_window.config(bg="#f0f8ff")

    # Header Section
    header_frame = tk.Frame(admin_panel_window, bg="#0288d1", pady=20)
    header_frame.pack(fill="x")
    tk.Label(header_frame, text="Admin Panel", font=("Times New Roman", 20, "bold"), fg="white", bg="#0288d1").pack()

    # Selection Section
    selection_frame = tk.Frame(admin_panel_window, bg="#ffffff", pady=40)
    selection_frame.pack(fill="both", expand=True)

    tk.Label(selection_frame, text="What would you like to do?", font=("Times New Roman", 16), bg="#ffffff").pack(pady=10)

    tk.Button(selection_frame, text="Add Package", font=("Times New Roman", 14, "bold"), bg="#4caf50", fg="white", 
              command=show_add_package_window, width=15).pack(pady=10)

    tk.Button(selection_frame, text="Remove Package", font=("Times New Roman", 14, "bold"), bg="#f44336", fg="white", 
              command=show_remove_package_window, width=15).pack(pady=10)

    # Footer Section
    footer_frame = tk.Frame(admin_panel_window, bg="#f0f8ff", pady=10)
    footer_frame.pack(fill="x")
    tk.Label(footer_frame, text="Powered by Explore Duniya", font=("Times New Roman", 10), bg="#f0f8ff", fg="#0288d1").pack()

    admin_panel_window.mainloop()


def add_package():
    def save_package():
        name = name_entry.get()
        price = price_entry.get()
        description = description_entry.get()

        if not name or not price or not description:
            messagebox.showerror("Error", "All fields are required!")
            return
        
        try:
            cursor.execute("INSERT INTO packages (package_name, price_per_person,description) VALUES (%s, %s, %s)", 
                           (name, price, description))
            db.commit()
            messagebox.showinfo("Success", "Package added successfully!")
            add_package_window.destroy()
            admin_panel()  # Go back to admin panel
        except Exception as e:
            messagebox.showerror("Error", f"Error adding package: {e}")

    # Add Package Window
    add_package_window = tk.Tk()
    add_package_window.title("Explore Duniya")
    add_package_window.geometry("400x400")
    add_package_window.config(bg="#f0f8ff")

    tk.Label(add_package_window, text="Add Package", font=("Times New Roman", 20, "bold"), bg="#0288d1", fg="white").pack(fill="x", pady=10)

    frame = tk.Frame(add_package_window, bg="#ffffff", padx=20, pady=20)
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Package Name:", font=("Times New Roman", 14), bg="#ffffff").pack(anchor="w")
    name_entry = tk.Entry(frame, font=("Times New Roman", 14))
    name_entry.pack(fill="x", pady=5)

    tk.Label(frame, text="Package Price:", font=("Times New Roman", 14), bg="#ffffff").pack(anchor="w")
    price_entry = tk.Entry(frame, font=("Times New Roman", 14))
    price_entry.pack(fill="x", pady=5)

    tk.Label(frame, text="Package Description:", font=("Times New Roman", 14), bg="#ffffff").pack(anchor="w")
    description_entry = tk.Entry(frame, font=("Times New Roman", 14))
    description_entry.pack(fill="x", pady=5)

    tk.Button(frame, text="Save Package", font=("Times New Roman", 14, "bold"), bg="#4caf50", fg="white", command=save_package).pack(pady=20)

    add_package_window.mainloop()


def remove_package():
    def delete_package():
        selected_package = package_dropdown.get()
        if not selected_package:
            messagebox.showerror("Error", "Please select a package to delete!")
            return
        
        try:
            cursor.execute("DELETE FROM packages WHERE package_name = %s", (selected_package,))
            db.commit()
            messagebox.showinfo("Success", f"Package '{selected_package}' has been removed!")
            remove_package_window.destroy()
            admin_panel()  # Go back to admin panel
        except Exception as e:
            messagebox.showerror("Error", f"Error removing package: {e}")

    # Remove Package Window
    remove_package_window = tk.Tk()
    remove_package_window.title("Explore Duniya")
    remove_package_window.geometry("400x300")
    remove_package_window.config(bg="#f0f8ff")

    tk.Label(remove_package_window, text="Remove Package", font=("Times New Roman", 20, "bold"), bg="#f44336", fg="white").pack(fill="x", pady=10)

    frame = tk.Frame(remove_package_window, bg="#ffffff", padx=20, pady=20)
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Select Package:", font=("Times New Roman", 14), bg="#ffffff").pack(anchor="w")

    # Fetching Package Names for Dropdown
    cursor.execute("SELECT package_name FROM packages")
    packages = [row[0] for row in cursor.fetchall()]
    package_dropdown = ttk.Combobox(frame, values=packages, state="readonly", font=("Times New Roman", 12), width=30)
    package_dropdown.pack(pady=10)

    tk.Button(frame, text="Delete Package", font=("Times New Roman", 14, "bold"), bg="#f44336", fg="white", command=delete_package).pack(pady=20)

    remove_package_window.mainloop()




canvas.create_window(120, 200, window=tk.Button(root, text="Sign Up", font=("Times New Roman", 12, "bold"), bg="#0288d1", fg="white", 
                                                command=signup))
canvas.create_window(120, 250, window=tk.Button(root, text="Login", font=("Times New Roman", 12, "bold"), bg="#388e3c", fg="white", 
                                                command=login))
canvas.create_window(120, 300, window=tk.Button(root, text="Admin Login", font=("Times New Roman", 12, "bold"), bg="#f57c00", fg="white", 
                                                command=admin_login))
root.mainloop()


