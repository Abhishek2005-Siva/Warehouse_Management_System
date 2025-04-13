from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.mail import send_mail
import mysql.connector
from datetime import date, timedelta
import random

def verify_otp(request):
    if request.method == 'POST':
        input_otp = request.POST.get('otp')
        data = request.session.get('signup_data')

        if data and input_otp == data['otp']:
            # Insert into DB
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Letmein2272",
                database="InventoryDB"
            )
            cursor = conn.cursor()

            sql = "INSERT INTO customer (CustomerName, CustomerEmail, CustomerPassword) VALUES (%s, %s, %s)"
            values = (data['name'], data['email'], data['password'])

            cursor.execute(sql, values)
            conn.commit()
            cursor.close()
            conn.close()

            del request.session['signup_data']

            return render(request, 'customer_entry.html')  # Or redirect to dashboard

        return render(request, 'verify_otp.html', {'error': 'Invalid OTP'})

    return redirect('customer_signup')


def add_provider(request):
    if request.method == 'POST':
        provider_id = request.POST['provider_id']
        provider_name = request.POST['provider_name']
        provider_address = request.POST['provider_address']

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Letmein2272",
            database="InventoryDB"
        )
        cursor = conn.cursor()

        sql = "INSERT INTO Provider (ProviderID, ProviderName, ProviderAddress) VALUES (%s, %s, %s)"
        values = (provider_id, provider_name, provider_address)

        cursor.execute(sql, values)
        conn.commit()

        cursor.close()
        conn.close()

        return render(request, 'success.html')

    return render(request, 'add_provider.html')
def customer_signup(request):
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email')
        customer_password = request.POST.get('customer_password')

        if not all([customer_name, customer_email, customer_password]):
            return render(request, 'customer_signup.html', {'error': 'Please fill all fields.'})
        
        conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Letmein2272",
                database="InventoryDB"
            )
        cursor = conn.cursor()
        cursor.execute("Select * from customer where customeremail=%s",(customer_email,))
        answer=cursor.fetchone()
        if answer is not None:
            return render(request, 'customer_signup.html', {'error': 'Email is already used by another Account. Use another email!'})


        cursor.execute("Select * from customer where customername=%s",(customer_name,))
        answer=cursor.fetchone()
        if answer is not None:
            return render(request, 'customer_signup.html', {'error': 'Name already exists. Use another Name!'})
        
        otp = str(random.randint(100000, 999999))

        # Save all data including OTP to session
        request.session['signup_data'] = {
            'name': customer_name,
            'email': customer_email,
            'password': customer_password,
            'otp': otp
        }

        # Send OTP email
        send_mail(
            subject='Your OTP for Registration',
            message=f'Your OTP is: {otp}',
            from_email='your_email@gmail.com',
            recipient_list=[customer_email],
            fail_silently=False,
        )

        return render(request, 'verify_otp.html')

    return render(request, 'customer_signup.html')


def admin_signup(request):
    if request.method == 'POST':
        admin_id = request.POST['admin_id']
        admin_name = request.POST['admin_name']
        admin_email = request.POST['admin_email']
        admin_password = request.POST['admin_password']

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Letmein2272",
            database="InventoryDB"
        )
        cursor = conn.cursor()

        sql = "INSERT INTO Admin (AdminID, AdminName, AdminEmail, AdminPassword) VALUES (%s, %s, %s, %s)"
        values = (admin_id, admin_name, admin_email, admin_password)

        cursor.execute(sql, values)
        conn.commit()

        cursor.close()
        conn.close()

        return render(request, 'success.html')

    return render(request, 'admin_login.html')

def admin_dashboard(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Letmein2272",
        database="InventoryDB"
    )

    cursor = connection.cursor()

    tables = [
        "Admin", "Customer", "Provider", "Product",
        "`Order`", "OrderDetail", "Delivery", "DeliveryDetail",
        "Inventory", "Location", "Transfer", "Warehouse","request"
    ]

    data = {}

    for table in tables:
        try:
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            data[table] = {
                "columns": columns,
                "rows": rows
            }
        except Exception as e:
            data[table] = {
                "columns": ["Error"],
                "rows": [[str(e)]]
            }

    cursor.close()
    connection.close()

    return render(request, 'admin_dashboard.html', {'data': data})
def mainpage(request):
    return render(request, 'mainpage.html')

def admin_login(request):
    if request.method == "POST":
        name = request.POST['name']
        password = request.POST['password']

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Letmein2272",
            database="InventoryDB"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Admin WHERE AdminName=%s AND AdminPassword=%s", (name, password))
        admin = cursor.fetchone()
        conn.close()

        if admin:
            request.session['admin_logged_in'] = True
            return redirect('admin_dashboard')
        else:
            return render(request, 'admin_login.html', {'error': 'Wrong credentials!'})

    return render(request, 'admin_login.html')

def update_cell(request):
    if request.method == 'POST':
        import mysql.connector
        from django.shortcuts import redirect, render

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Letmein2272",
            database="InventoryDB"
        )
        cursor = conn.cursor()

        for key, value in request.POST.items():
            if key.startswith("cell_"):
                # Expected format: cell_tablename_columnname_primarykeyname_primarykeyvalue
                parts = key.split("_")
                if len(parts) < 5:
                    continue  # skip invalid entries

                table_name = parts[1]
                column_name = parts[2]
                primary_key_name = parts[3]
                primary_key_value = parts[4]

                # Prepare the SQL query dynamically
                query = f"UPDATE `{table_name}` SET `{column_name}` = %s WHERE `{primary_key_name}` = %s"
                cursor.execute(query, (value, primary_key_value))

        conn.commit()

        # ---------------------------------------------
        # Fetch data again like your admin_dashboard view
        data = {}
        cursor.execute("SHOW TABLES")
        tables = [t[0] for t in cursor.fetchall()]

        for table_name in tables:
            cursor.execute(f"SELECT * FROM `{table_name}`")
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            data[table_name] = {'columns': columns, 'rows': rows}
        # ---------------------------------------------

        cursor.close()
        conn.close()

        return render(request, 'admin_dashboard.html', {'data': data, 'saved': 'Saved all changes!'})



def customer_login(request):
    if request.method == "POST":
        name = request.POST['name']
        password=request.POST['password']
        

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Letmein2272",
            database="InventoryDB"
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Customer WHERE CustomerName=%s", (name,))
        customer = cursor.fetchone()
        conn.close()
        

        if customer and (customer['CustomerPassword']==password):
            request.session['customer_logged_in'] = True
            request.session['customer_name'] = name
            request.session['customer_id'] = customer['CustomerID']
            return redirect('customer_dashboard')
        else:
            return render(request, 'customer_login.html', {'error': 'Wrong Password'})

    return render(request, 'customer_login.html')


def logout_view(request):
    request.session.flush()  # Clear all session data
    return redirect('mainpage')

def customer_dashboard(request):
    customer_name = request.session.get('customer_name', 'Customer')

    # Connect to MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Letmein2272",
        database="InventoryDB"
    )
    cursor = conn.cursor(dictionary=True)

    # Get filter values
    search_query = request.GET.get('search', '')
    selected_provider = request.GET.get('provider', '')
    selected_type = request.GET.get('type', '')

    # Updated query with actual provider name
    query = """
        SELECT 
            p.ProductID AS product_id,
            p.ProductName AS product_name,
            p.ProductCategory AS type,
            p.ReorderQuantity AS price,
            i.QuantityAvailable AS quantity,
            pr.ProviderName AS provider_name,
            pr.ProviderID AS provider_id
        FROM product p
        JOIN inventory i ON p.ProductID = i.ProductID
        JOIN provider pr ON p.ProviderID = pr.ProviderID
        WHERE 1
    """
    params = []

    if search_query:
        query += " AND p.ProductName LIKE %s"
        params.append(f"%{search_query}%")
    
    if selected_provider:
        query += " AND pr.ProviderName = %s"
        params.append(selected_provider)

    if selected_type:
        query += " AND p.ProductCategory = %s"
        params.append(selected_type)

    cursor.execute(query, params)
    products = cursor.fetchall()

    # Get distinct providers and types
    cursor.execute("SELECT DISTINCT ProviderName FROM provider")
    provider_names = [row['ProviderName'] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT ProductCategory FROM product")
    types = [row['ProductCategory'] for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    return render(request, 'customer_dashboard.html', {
        'products': products,
        'search_query': search_query,
        'selected_provider': selected_provider,
        'selected_type': selected_type,
        'providers': provider_names,
        'types': types,
        'customer_name': customer_name,
    })

def request_product(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        customer_id = request.session.get('customer_id')  # store this during login
        quantity = request.POST.get('quantity')

        return redirect('customer_dashboard')
def customer_entry(request):
    return render(request, 'customer_entry.html')

def provider_login(request):
    if request.method == "POST":
        provider_name = request.POST['provider_name']
        provider_password = request.POST['provider_password']

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Letmein2272",
            database="InventoryDB"
        )
        cursor = conn.cursor()
        cursor.execute(
            "SELECT ProviderID FROM Provider WHERE ProviderName = %s AND ProviderPassword = %s",
            (provider_name, provider_password)
        )
        provider = cursor.fetchone()
        conn.close()

        if provider:
            request.session['provider_logged_in'] = True
            request.session['provider_id'] = provider[0]
            request.session['provider_name'] = provider_name
            return redirect('provider_dashboard')
        else:
            return HttpResponse("Invalid provider name or password.")

    return render(request, 'provider_login.html')


def provider_dashboard(request):
    if not request.session.get('provider_logged_in'):
        return redirect('provider_login')

    provider_id = request.session.get('provider_id')

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Letmein2272",
        database="InventoryDB"
    )
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        cursor.execute("""
            SELECT CustomerID, ProductID, QuantityRequested 
            FROM request 
            WHERE RequestID = %s
        """, (request_id,))
        result = cursor.fetchone()

        if result:
            customer_id = result['CustomerID']
            product_id = result['ProductID']
            quantity = result['QuantityRequested']

            # Check inventory
            cursor.execute("SELECT QuantityAvailable FROM inventory WHERE ProductID = %s", (product_id,))
            inventory = cursor.fetchone()

            if inventory and inventory['QuantityAvailable'] >= quantity:
                # Check if existing order already exists
                cursor.execute("""
                    SELECT od.OrderID FROM orderdetail od
                    JOIN `order` o ON od.OrderID = o.OrderID
                    WHERE o.CustomerID = %s AND od.ProductID = %s
                """, (customer_id, product_id))
                existing = cursor.fetchone()

                expected_date = date.today() + timedelta(days=5)

                
                # Reduce inventory
                cursor.execute("""
                    UPDATE inventory
                    SET QuantityAvailable = QuantityAvailable - %s
                    WHERE ProductID = %s
                """, (quantity, product_id))

                # Delete request
                cursor.execute("DELETE FROM request WHERE RequestID = %s", (request_id,))
                conn.commit()
            else:
                print("Not enough inventory")

    # Fetch dashboard data (e.g., requests for this provider)
    cursor.execute("""
        SELECT r.RequestID, r.CustomerID, c.CustomerName, p.ProductName, r.QuantityRequested
        FROM request r
        JOIN product p ON r.ProductID = p.ProductID
        JOIN customer c ON r.CustomerID = c.CustomerID
        WHERE p.ProviderID = %s
    """, (provider_id,))
    requests = cursor.fetchall()

    cursor.close()
    conn.close()

    return render(request, 'provider_dashboard.html', {'requests': requests})

def provider_logout(request):
    request.session.flush()
    return redirect('provider_login')

def request_product(request):
    if request.method == "POST":
        customer_id = request.session.get('customer_id')
        product_id = int(request.POST['product_id'])
        quantity = int(request.POST['quantity'])

        if not customer_id:
            return HttpResponse("You must be logged in to request a product.", status=403)

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Letmein2272",
            database="InventoryDB"
        )
        cursor = conn.cursor()

        # Insert into request table
        cursor.execute("""
            INSERT INTO request (CustomerID, ProductID, QuantityRequested)
            VALUES (%s, %s, %s)
        """, (customer_id, product_id, quantity))

        # Insert into order table
        cursor.execute("""
            INSERT INTO `order` (OrderDate, CustomerID)
            VALUES (%s, %s)
        """, (date.today(), customer_id))

        order_id = cursor.lastrowid  # Get the ID of the inserted order

        # Insert into orderdetail
        cursor.execute("""
            INSERT INTO orderdetail (OrderID, ProductID, OrderQuantity, ExpectedDate,status)
            VALUES (%s, %s, %s, %s,"Request Pending")
        """, (order_id, product_id, quantity, date.today() + timedelta(days=5)))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect('customer_dashboard')

    else:
        return HttpResponse("Invalid Request Method", status=405)
    
def customer_orders(request):
    customer_id = request.session.get('customer_id')

    if not customer_id:
        return redirect('customer_login')

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Letmein2272",
        database="InventoryDB"
    )
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT 
            o.OrderID,
            o.OrderDate,
            od.ProductID,
            p.ProductName,
            od.OrderQuantity,
            od.ExpectedDate,
            od.status
        FROM `order` o
        JOIN orderdetail od ON o.OrderID = od.OrderID
        JOIN product p ON od.ProductID = p.ProductID
        WHERE o.CustomerID = %s
        ORDER BY o.OrderDate DESC
    """

    cursor.execute(query, (customer_id,))
    orders = cursor.fetchall()

    cursor.close()
    conn.close()

    return render(request, 'customer_orders.html', {'orders': orders})


def mark_delivered(request):
    if request.method == 'POST':
        request_id = request.POST.get('request_id')

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Letmein2272",
            database="InventoryDB"
        )
        cursor = conn.cursor(dictionary=True, buffered=True)  # <-- FIXED: buffered=True

        # Fetch request info
        cursor.execute("""
            SELECT r.CustomerID, r.ProductID, r.QuantityRequested, p.ProviderID
            FROM request r
            JOIN product p ON r.ProductID = p.ProductID
            WHERE r.RequestID = %s
        """, (request_id,))
        req = cursor.fetchone()

        if req:
            customer_id = req['CustomerID']
            product_id = req['ProductID']
            quantity = req['QuantityRequested']

            # Check inventory
            cursor.execute("SELECT QuantityAvailable FROM inventory WHERE ProductID = %s", (product_id,))
            inventory = cursor.fetchone()

            if inventory and inventory['QuantityAvailable'] >= quantity:
                # Check if an order already exists for this customer and product
                cursor.execute("""
                    SELECT od.OrderID FROM orderdetail od
                    JOIN `order` o ON od.OrderID = o.OrderID
                    WHERE o.CustomerID = %s AND od.ProductID = %s
                """, (customer_id, product_id))
                existing = cursor.fetchone()

                if not existing:
                    # Create order and order detail
                    cursor.execute("INSERT INTO `order` (OrderDate, CustomerID) VALUES (%s, %s)", 
                                   (date.today(), customer_id))
                    order_id = cursor.lastrowid

                    expected_date = date.today() + timedelta(days=5)
                    cursor.execute("""
                        INSERT INTO orderdetail (OrderID, ProductID, OrderQuantity, ExpectedDate, status)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (order_id, product_id, quantity, expected_date, "Request Accepted"))
                else:
                    order_id = existing['OrderID']
                    expected_date = date.today() + timedelta(days=5)
                    cursor.execute("""
                        UPDATE orderdetail
                        SET OrderQuantity = OrderQuantity + %s,
                            ExpectedDate = %s,
                            status = %s
                        WHERE OrderID = %s AND ProductID = %s
                    """, (quantity, expected_date, "Request Accepted", order_id, product_id))

                # Update inventory
                cursor.execute("""
                    UPDATE inventory
                    SET QuantityAvailable = QuantityAvailable - %s
                    WHERE ProductID = %s
                """, (quantity, product_id))

                # Create delivery
                cursor.execute("""
                    INSERT INTO Delivery (CustomerID, SalesDate)
                    VALUES (%s, %s)
                """, (customer_id, date.today()))
                delivery_id = cursor.lastrowid

                # Create delivery detail
                cursor.execute("""
                    INSERT INTO DeliveryDetail (DeliveryID, ProductID, DeliveryQuantity, ExpectedDate, ActualDate)
                    VALUES (%s, %s, %s, %s, %s)
                """, (delivery_id, product_id, quantity, expected_date, date.today()))

                # Remove request
                cursor.execute("DELETE FROM request WHERE RequestID = %s", (request_id,))
                conn.commit()

        cursor.close()
        conn.close()

        return redirect('provider_dashboard')


def view_deliveries(request):
    if not request.session.get('provider_logged_in'):
        return redirect('provider_login')

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Letmein2272",
        database="InventoryDB"
    )
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            d.DeliveryID, d.SalesDate, d.CustomerID, 
            dd.ProductID, dd.DeliveryQuantity, dd.ExpectedDate, dd.ActualDate,
            c.CustomerName, p.ProductName
        FROM Delivery d
        JOIN DeliveryDetail dd ON d.DeliveryID = dd.DeliveryID
        JOIN Customer c ON d.CustomerID = c.CustomerID
        JOIN Product p ON dd.ProductID = p.ProductID
        WHERE p.ProviderID = %s
    """, (request.session.get('provider_id'),))
    
    deliveries = cursor.fetchall()

    cursor.close()
    conn.close()

    return render(request, 'provider_delivery_info.html', {
        'deliveries': deliveries
    })
def decline_request(request):
    if request.method == 'POST':
        request_id = request.POST.get('request_id')

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Letmein2272",
            database="InventoryDB"
        )
        cursor = conn.cursor(dictionary=True, buffered=True)

        # Fetch request info
        cursor.execute("""
            SELECT r.CustomerID, r.ProductID, r.QuantityRequested, p.ProviderID
            FROM request r
            JOIN product p ON r.ProductID = p.ProductID
            WHERE r.RequestID = %s
        """, (request_id,))
        req = cursor.fetchone()

        if req:
            customer_id = req['CustomerID']
            product_id = req['ProductID']
            quantity = req['QuantityRequested']

            # Check if an order exists
            cursor.execute("""
                SELECT od.OrderID FROM orderdetail od
                JOIN `order` o ON od.OrderID = o.OrderID
                WHERE o.CustomerID = %s AND od.ProductID = %s
            """, (customer_id, product_id))
            existing = cursor.fetchone()

            if existing:
                cursor.execute("""
                    UPDATE orderdetail od
                    JOIN `order` o ON od.OrderID = o.OrderID
                    SET od.status = 'Request Declined'
                    WHERE od.ProductID = %s AND o.CustomerID = %s
                """, (product_id, customer_id))

            # Remove request
            cursor.execute("DELETE FROM request WHERE RequestID = %s", (request_id,))
            conn.commit()

        cursor.close()
        conn.close()

        return redirect('provider_dashboard')

    return HttpResponse("Invalid request method", status=400)
