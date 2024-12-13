import mysql.connector
from mysql.connector import Error

# Establish MySQL connection
def get_connection(database_name="erms"):  # Default database
    try:
        connection = mysql.connector.connect(
            host='localhost',  # XAMPP default
            user='root',
            password='',
            database=database_name
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None



# Insert a new user
def insert_user(username, password, role):
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                (username, password, role),
            )
            connection.commit()
        finally:
            connection.close()


# Validate login
def validate_login(username, password, role):
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username=%s AND password=%s AND role=%s",
                (username, password, role),
            )
            return cursor.fetchone()
        finally:
            connection.close()


# Get materials uploaded by a specific uploader
def get_materials_by_uploader(uploader_id):
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id, material_name, file_path, status, uploader_id FROM materials WHERE uploader_id=%s",
                (uploader_id,),
            )
            return cursor.fetchall()
        finally:
            connection.close()


# Add a new material (with file path)
def insert_uploaded_material(uploader_id, material_name, file_path):
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO materials (uploader_id, material_name, file_path, status) VALUES (%s, %s, %s, %s)",
                (uploader_id, material_name, file_path, "Pending"),
            )
            connection.commit()
        finally:
            connection.close()


# Get all uploaded materials
def get_uploaded_materials():
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT id, material_name, file_path, uploader_id, status FROM materials")
            return cursor.fetchall()
        finally:
            connection.close()

def get_material_requests():
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            # Ensure you're selecting a status-related column here, e.g., 'status'
            query = "SELECT id, request_description, status, requester_id FROM material_requests"
            cursor.execute(query)
            requests = cursor.fetchall()
            return requests
        finally:
            connection.close()

def approve_material(material_id): 
    connection = get_connection() 
    if connection: 
        try: 
            cursor = connection.cursor() 
            cursor.execute( "UPDATE materials SET status=%s WHERE id=%s", 
            ('approved', material_id), ) 
            connection.commit() 
        finally: 
            connection.close()

# Reject a material 
def reject_material(material_id): 
    connection = get_connection() 
    if connection: 
        try: 
            cursor = connection.cursor() 
            cursor.execute( "UPDATE materials SET status=%s WHERE id=%s", 
            ('rejected', material_id), ) 
            connection.commit() 
        finally: 
            connection.close() 

# Delete a material 
def delete_material(material_id): 
    connection = get_connection() 
    if connection: 
        try: 
            cursor = connection.cursor() 
            cursor.execute("DELETE FROM materials WHERE id=%s", 
            (material_id,)) 
            connection.commit() 
        finally: 
            connection.close()

# Approve or Reject a Material Request 
def approve_or_reject_request(request_id, status):
    connection = get_connection() 
    if connection: 
        try: 
            cursor = connection.cursor() 
            cursor.execute( "UPDATE material_requests SET status=%s WHERE id=%s", 
            (status, request_id), ) 
            connection.commit() 
        finally: 
            connection.close() 
# Approve a material request 
def approve_request(request_id): 
    return approve_or_reject_request(request_id, 'approved') 
# Reject a material request 
def reject_request(request_id):
    return approve_or_reject_request(request_id, 'rejected') 
# Delete a material request 
def delete_material_request(request_id):
    connection = get_connection()
    if connection:
        try: 
            cursor = connection.cursor() 
            cursor.execute("DELETE FROM material_requests WHERE id=%s", (request_id,)) 
            connection.commit() 
        finally: 
            connection.close()

# Update material details (material name or file path)
def update_uploaded_material(material_id, new_material_name, new_file_path):
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE materials SET material_name=%s, file_path=%s WHERE id=%s",
                (new_material_name, new_file_path, material_id),
            )
            connection.commit()
        finally:
            connection.close()

# Delete a material (Admin only)
def delete_uploaded_material(material_id):
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM materials WHERE id=%s", (material_id,))
            connection.commit()
        finally:
            connection.close()


# Insert a material request from a viewer
def insert_material_request(viewer_id, request_description, ):
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO material_requests (request_description, requester_id, status) VALUES (%s, %s, %s)",
                (request_description, viewer_id, 'pending'),
            )
            connection.commit()
        finally:
            connection.close()

# Fetch all users
def get_all_users():
    connection = get_connection()
    cursor = connection.cursor()
    query = "SELECT id, username, role, password FROM users"
    cursor.execute(query)
    users = cursor.fetchall()
    connection.close()
    return users

# Delete a material request
def delete_request(request_id):
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM material_requests WHERE id=%s", (request_id,))
            connection.commit()
        finally:
            connection.close()

# Delete a User
def delete_user(user_id):
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
            connection.commit()
        finally:
            connection.close()

def get_all_requests(viewer_id):
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "SELECT id, request_description, status FROM material_requests WHERE requester_id=%s"
            cursor.execute(query, (viewer_id,))
            requests = cursor.fetchall()  # Fetch all requests for the specific viewer
            return requests
        except Exception as e:
            print(f"Error fetching requests: {e}")
            return []
        finally:
            connection.close()  # Always close the connection
    else:
        print("Failed to establish a database connection.")
        return []
