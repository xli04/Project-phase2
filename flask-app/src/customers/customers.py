########################################################
# Sample customers blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################
from flask import Blueprint, request, jsonify, make_response
import json
from src import db


customers = Blueprint('customers', __name__)

#Get all customers for the DB
@customers.route('/customers', methods=['GET'])
def get_customers():
    cursor = db.get_db().cursor()
    cursor.execute('select CustomerID, UserName, PassWord,\
        Email, Address from Customers')
    print("Statement executed")
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

#Route to add new customers
@customers.route('/customers',methods=['POST'])
def add_customer():
    cust_info = request.json #Obtain requested customer information
    # current_app.logger.infor(cust_info)
    
    cust_id = cust_info['CustomerID']
    username = cust_info['UserName']
    password = cust_info['PassWord']
    email = cust_info['Email']
    address = cust_info['Address']
    
    #Insert Customers into the DB
    query = '''
    INSERT INTO Customers 
    VALUES (%s,%s,%s,%s)
    '''
    #Tuple for SQL query 
    data = (username, password,email,address)
    cursor = db.get_db().cursor()
    cursor.execute(query,data)
    db.get_db().commit()
    return 'customer aaddddeeed!'

@customers.route('/customers/allProducts', methods=['GET'])
def get_all_products():
    cursor = db.get_db().cursor() #Cursor object to interact with database
    cursor.execute('select * from Products') #Fetch all Products
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall() #Fetch all rows from query
    for row in theData:
        json_data.append(dict(zip(row_headers, row))) #Result into list of Dictionaries
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200 
    the_response.mimetype = 'application/json'
    return the_response

@customers.route('/customers_put',methods=['PUT'])
def update_customer():
    cust_info = request.json
    # current_app.logger.infor(cust_info) 
    #Extract Individual Fields in customer info 
    id = cust_info['CustomerID'] 
    username = cust_info['UserName']
    password = cust_info['PassWord']
    email = cust_info['Email']
    address = cust_info['Address']
    #Update query for customers DB
    query = '''    
    UPDATE Customers 
    SET UserName = %s, PassWord = %s, Email = %s, Address = %s 
    WHERE CustomerID = %s
    '''
    data = (username, password,email,address,id)
    #Get DB cursor and update
    cursor = db.get_db().cursor()
    r = cursor.execute(query,data)
    db.get_db().commit()
    return 'customer updated!'

@customers.route('/customers/<userID>', methods=['GET'])
def get_customer(userID):
    cursor = db.get_db().cursor()
    #SQL query to fetch the customer with the given UserID
    cursor.execute('select * from Customers where CustomerID = {0}'.format(userID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    #Get all the rows from the query result
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row))) #Convert Result into list of dictionaries
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@customers.route('/customers/<userID>', methods=['DELETE'])
def delete_customer(userID):
    cursor = db.get_db().cursor() #Cursor Object to interacte with DB
    cursor.execute('''
                   DELETE FROM Customers where CustomerID = {0}
                   '''.format(userID)) #Delete Query for Customer
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    db.get_db().commit() #Commit all changes
    return the_response

# Get customer detail for customer with particular userID
@customers.route('/customers/cart/<id>', methods=['GET'])
def get_customer_cart(id):
    cursor = db.get_db().cursor()
    # Execute SQL query to fetch customer cart details
    cursor.execute('''
                   SELECT Products.*, Product_In_Cart.*
                   FROM Cart NATURAL JOIN Product_In_Cart NATURAL JOIN Products
                   WHERE Cart.CustomerID = {0}
                   '''.format(id)) 
    row_headers = [x[0] for x in cursor.description]
    json_data = [] 
    
    # Fetch all rows from the executed query
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@customers.route('/customers/cart', methods=['POST'])
def post_customer_cart():
    cursor = db.get_db().cursor()
    cart_info = request.json
        # current_app.logger.infor(cust_info)
    pro_id = cart_info['ProductID']
    cus_id = cart_info['CustomerID']
    quantity = cart_info['Quantity']
    cursor.execute('''
                    INSERT INTO commerce.Product_In_Cart (CustomerID, ProductID, Quantity)
                    VALUE (%s, %s, %s)
                    ''',(cus_id, pro_id, quantity))
    db.get_db().commit()
    return 'added'

@customers.route('/customers/cart', methods=['DELETE'])
def delete_customer_cart():
    cursor = db.get_db().cursor()
    cart_info = request.json
        # current_app.logger.infor(cust_info)
    cus_id = cart_info['CustomerID']
    product_id = cart_info['ProductID']
    
    # card_number = cart_info['CardNumber']
    # exp_date = cart_info['ExpirationDate']
    # billing_address = cart_info['BillingAddress']
    # delete product from customer's cart
    cursor.execute('''
                    DELETE FROM Product_In_Cart where CustomerID = %s and ProductID = %s
                    ''',(cus_id,product_id))
    db.get_db().commit()
    return 'delete'

# Get card detail for customer with particular userID
@customers.route('/customers/card/<id>', methods=['GET'])
def get_customer_card(id):
    cursor = db.get_db().cursor()
    cursor.execute('''
                SELECT * 
                FROM Customers NATURAL JOIN Card
                WHERE Customers.CustomerID = {0}
                '''.format(id))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    

    return the_response

@customers.route('/customers/card', methods=['POST'])
def add_customer_card():
    cursor = db.get_db().cursor()
    card_info = request.json
        # current_app.logger.infor(cust_info)
    card_number = card_info['CardNumber']
    cus_id = card_info['CustomerID']
    exp_date = card_info['ExpirationDate']
    billing_address = card_info['BillingAddress']
    cursor.execute('''
                    INSERT INTO Card (CardNumber, CustomerID, ExpirationDate, BillingAddress)
                    VALUE (%s, %s, %s, %s)
                    ''',(card_number,cus_id,exp_date,billing_address))
    db.get_db().commit()

    # return success statement
    return 'added'

@customers.route('/customers/cards/<customer_id>/<card_number>', methods=['PUT'])
def put_customer_card(customer_id, card_number):
    cursor = db.get_db().cursor()
    
    # Update the card details for the given card number
    card_info = request.json
    exp_date = card_info['ExpirationDate']
    billing_address = card_info['BillingAddress']
    # execute query to update customer card
    cursor.execute('''
        UPDATE Card
        SET ExpirationDate = %s, BillingAddress = %s
        WHERE CardNumber = %s AND CustomerID = %s
        ''', (exp_date, billing_address, card_number, customer_id))
        
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    db.get_db().commit()
    return the_response

@customers.route('/customers/cards/<customer_id>/<card_number>', methods=['DELETE'])
def delete_customer_card(customer_id, card_number):
    cursor = db.get_db().cursor()

    print('???')
    # Delete the card with the specified number
    cursor.execute('''
        DELETE FROM Card
        WHERE CardNumber = %s AND CustomerID = %s
        ''', (card_number, customer_id))
        
   
    db.get_db().commit()
    return "success"

# Get shipping details for customers using a specific userID
@customers.route('/customers/all_shipping/<id>', methods=['GET'])
def get_customer_shipments(id):
    cursor = db.get_db().cursor()
    cursor.execute('''
                   SELECT Destination, Estimated_Shipping_Time, Actual_Shipping_Time, PackageSize
                   FROM Customers NATURAL JOIN Shipping_Detail
                   WHERE Customers.CustomerID = {0}
                   '''.format(id))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get shipping of order details for customers using a specific userID
@customers.route('/customers/shipping_of_order/<order_id>', methods=['GET'])
def get_one_shipment(id):
    cursor = db.get_db().cursor()
    cursor.execute('''
                   SELECT Destination, Estimated_Shipping_Time, Actual_Shipping_Time, PackageSize
                   FROM Orders NATURAL JOIN Shipping_Detail
                   WHERE ShippingDetail.OrderID = {0}
                   '''.format(id))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get Orders detail for customers using a specific userID
@customers.route('/customers/orders_detail/<id>', methods=['GET'])
def get_customer_orders_detail(id):
    cursor = db.get_db().cursor()
    # execute query to obtain order details
    cursor.execute('''
                SELECT p.* 
                FROM Products p join OrderDetails o on p.ProductID = o.ProductID
                WHERE o.OrderID =  {0}
                '''.format(id))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# obtain orders for a customer with a certain customerID
@customers.route('/customers/orders/<id>', methods=['GET'])
def get_customer_orders(id):
    cursor = db.get_db().cursor()
    # execute SQL query to obtain the customer's orders
    cursor.execute('''
                SELECT *
                From Orders
                WHERE Orders.CustomerID = {0}
                '''.format(id))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@customers.route('/customers/order', methods=['POST'])
# add a customer's order
def add_customer_order():
    cursor = db.get_db().cursor()
    order_info = request.json
        # current_app.logger.infor(cust_info)
    PlacedTime = order_info['PlacedTime']
    cus_id = order_info['CustomerID']
    # execute a SQL query to add the customer's order 
    cursor.execute('''
                    INSERT INTO commerce.Orders (Cost, PlacedTime, Status, CustomerID)
                    VALUE (%s, %s, %s, %s)
                    ''',(0,PlacedTime,1,cus_id))
    db.get_db().commit()
    return 'added'

@customers.route('/customers/order_detail', methods=['POST'])
# add the details of a customer's order
def add_customer_order_detail():
    cursor = db.get_db().cursor()
    order_info = request.json
        # current_app.logger.infor(cust_info)
    ProductID = order_info['ProductID']
    OrderID = order_info['OrderID']
    Quantity = order_info['Quantity']
    # execute a SQL query to add the customer's order details
    cursor.execute('''
                    INSERT INTO commerce.OrderDetails (ProductID, OrderID, Quantity)
                    VALUE (%s, %s, %s)
                    ''',(ProductID, OrderID, Quantity))
    db.get_db().commit()
    return 'added'

# # Get orders detail for customer with particular userID
# @customers.route('/customers/orders/<id>', methods=['POST'])
# def add_customer_orders(id):
#     cursor = db.get_db().cursor()
    

#     the_data = request.json

#     #extracting the variable
#     orderId = the_data['OrderID']
#     cost = the_data['Cost']
#     placedTime = the_data['PlacedTime']
#     status = the_data['Status']
#     address = the_data['ShippingAddress']

#     # Constructing the query
#     query = 'insert into Orders (CompanyName, Rating, CompanyAddress) values ("'
#     query += orderId + '", "'
#     query += cost + '", '
#     query += placedTime + '", '
#     query += status + '", '
#     query += address + ')'
    
#     cursor.execute(query)
#     db.get_db().commit()
        
#     row_headers = [x[0] for x in cursor.description]
#     json_data = []
#     theData = cursor.fetchall()
#     for row in theData:
#         json_data.append(dict(zip(row_headers, row)))
#     the_response = make_response(jsonify(json_data))
#     the_response.status_code = 200
#     the_response.mimetype = 'application/json'
#     return the_response