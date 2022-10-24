#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import time

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='Air Ticket Reservation System', #airport_test/Air Ticket Reservation System
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define a route to hello function
@app.route('/')
def hello():
    cursor = conn.cursor()
    query = 'SELECT * FROM flight ORDER BY departure_time DESC'
    cursor.execute(query)
    data1 = cursor.fetchall() 
    for each in data1:
        print(each['airline_name'])
    cursor.close()
    return render_template('index.html', flight = data1)

@app.route('/customer')
def customer():
	return render_template('customer.html')

@app.route('/agent')
def agent():
	return render_template('agent.html')

@app.route('/staff')
def staff():
	return render_template('staff.html')

#Define route for login
@app.route('/login_customer')
def login_customer():
	return render_template('login_customer.html')

@app.route('/login_agent')
def login_agent():
	return render_template('login_agent.html')

@app.route('/login_staff')
def login_staff():
	return render_template('login_staff.html')

#Define route for register
@app.route('/register_customer')
def register_customer():
	return render_template('register_customer.html')

@app.route('/register_agent')
def register_agent():
	return render_template('register_agent.html')

@app.route('/register_staff')
def register_staff():
	return render_template('register_staff.html')

@app.route('/upcoming_flights')
def upcoming_flights():
	return render_template('upcoming_flights.html')

@app.route('/flight_status')
def flight_status():
	return render_template('flight_status.html')

@app.route('/homeCustomer')
def homeCustomer():  
    email = session['username']
    cursor = conn.cursor();
    query = 'SELECT * FROM flight NATURAL JOIN ticket NATURAL JOIN purchases \
            WHERE `status` = \'Upcoming\' \
                AND customer_email = %s \
            ORDER BY departure_time'
    cursor.execute(query, (email))
    data1 = cursor.fetchall() 
    for each in data1:
        print(each['flight_num'])
    cursor.close()
    
    cursor = conn.cursor();
    query = 'SELECT DISTINCT * FROM ticket_request NATURAL JOIN ticket \
            WHERE customer_email = %s'
    cursor.execute(query, (email))
    data2 = cursor.fetchall() 
    cursor.close()
    
    return render_template('home_customer.html', posts=data1, request=data2)

@app.route('/bookCustomer')
def bookCustomer():
    cursor = conn.cursor();
    query = 'SELECT * FROM flight NATURAL JOIN ticket \
            WHERE status = \'Upcoming\' \
            AND ticket_id NOT IN (SELECT ticket_id FROM purchases) \
            ORDER BY departure_time'
    cursor.execute(query)
    data1 = cursor.fetchall() 
    for each in data1:
        print(each['flight_num'])
    cursor.close()
    
    return render_template('book_customer.html', posts=data1)

@app.route('/filterbyCityCustomer', methods=['GET', 'POST'])
def filterbyCityCustomer():
    departure_city = request.form['departure_city']
    arrival_city = request.form['arrival_city']
    cursor = conn.cursor();
    if departure_city and arrival_city:  
        query = 'SELECT * FROM flight NATURAL JOIN ticket \
                WHERE status = \'Upcoming\' \
                AND ticket_id NOT IN (SELECT ticket_id FROM purchases) \
                AND departure_airport IN (SELECT airport_name FROM airport WHERE airport_city = %s) \
                AND arrival_airport IN (SELECT airport_name FROM airport WHERE airport_city = %s) \
                ORDER BY departure_time'
        cursor.execute(query, (departure_city, arrival_city))
        
    elif departure_city:
        query = 'SELECT * FROM flight NATURAL JOIN ticket \
                WHERE status = \'Upcoming\' \
                AND ticket_id NOT IN (SELECT ticket_id FROM purchases) \
                AND departure_airport IN (SELECT airport_name FROM airport WHERE airport_city = %s) \
                ORDER BY departure_time'
        cursor.execute(query, (departure_city))
        
    elif arrival_city:
        query = 'SELECT * FROM flight NATURAL JOIN ticket \
                WHERE status = \'Upcoming\' \
                AND ticket_id NOT IN (SELECT ticket_id FROM purchases) \
                AND arrival_airport IN (SELECT airport_name FROM airport WHERE airport_city = %s) \
                ORDER BY departure_time'
        cursor.execute(query, (arrival_city))
    else:
        query = 'SELECT * FROM flight NATURAL JOIN ticket \
                WHERE status = \'Upcoming\' \
                AND ticket_id NOT IN (SELECT ticket_id FROM purchases) \
                ORDER BY departure_time'
        cursor.execute(query)
    data1 = cursor.fetchall() 
    cursor.close()

    return render_template('book_customer.html', posts=data1)

@app.route('/filterbyAirportCustomer', methods=['GET', 'POST'])
def filterbyAirportCustomer():
    departure_airport = request.form['departure_airport']
    arrival_airport = request.form['arrival_airport']
    cursor = conn.cursor();
    if departure_airport and arrival_airport:  
        query = 'SELECT * FROM flight NATURAL JOIN ticket \
                WHERE status = \'Upcoming\' \
                AND ticket_id NOT IN (SELECT ticket_id FROM purchases) \
                AND departure_airport = %s \
                AND arrival_airport = %s \
                ORDER BY departure_time'
        cursor.execute(query, (departure_airport, arrival_airport))
        
    elif departure_airport:
        query = 'SELECT * FROM flight NATURAL JOIN ticket \
                WHERE status = \'Upcoming\' \
                AND ticket_id NOT IN (SELECT ticket_id FROM purchases) \
                AND departure_airport = %s \
                ORDER BY departure_time'
        cursor.execute(query, (departure_airport))
        
    elif arrival_airport:
        query = 'SELECT * FROM flight NATURAL JOIN ticket \
                WHERE status = \'Upcoming\' \
                AND ticket_id NOT IN (SELECT ticket_id FROM purchases) \
                AND arrival_airport = %s \
                ORDER BY departure_time'
        cursor.execute(query, (arrival_airport))
    else:
        query = 'SELECT * FROM flight NATURAL JOIN ticket \
                WHERE status = \'Upcoming\' \
                AND ticket_id NOT IN (SELECT ticket_id FROM purchases) \
                ORDER BY departure_time'
        cursor.execute(query)
    data1 = cursor.fetchall() 
    cursor.close()

    return render_template('book_customer.html', posts=data1)
        

@app.route('/filterbyTimeCustomer', methods=['GET', 'POST'])
def filterbyTimeCustomer():
    try:
        departure_time = time.strptime(str(request.form['departure_time']),"%Y-%m-%dT%H:%M")
        arrival_time = time.strptime(str(request.form['arrival_time']),"%Y-%m-%dT%H:%M")
    except:
        error = 'Invalid time filter!'
        return render_template('book_customer.html', error=error)
    
    cursor = conn.cursor();
    query = 'SELECT * FROM flight NATURAL JOIN ticket \
            WHERE status = \'Upcoming\' \
            AND ticket_id NOT IN (SELECT ticket_id FROM purchases) \
            AND departure_time < %s \
            AND arrival_time < %s \
            ORDER BY departure_time'
    cursor.execute(query, (departure_time, arrival_time))
    data1 = cursor.fetchall() 
    cursor.close()
    return render_template('book_customer.html', posts=data1)

@app.route('/buyCustomer', methods=['GET', 'POST'])
def buyCustomer():
    email = session['username']
    cursor = conn.cursor(); 
    ticket_id = request.form['ticket_id']
    query = 'INSERT INTO purchases(ticket_id, customer_email, booking_agent_id, purchase_date) \
            VALUES(%s, %s, NULL, CURRENT_DATE)'

    cursor.execute(query, (ticket_id, email))
    conn.commit()
    cursor.close()
    
    cursor = conn.cursor(); 
    ticket_id = request.form['ticket_id']
    query = 'DELETE FROM ticket_request \
            WHERE (ticket_id = %s AND customer_email = %s) '

    cursor.execute(query, (ticket_id, email))
    conn.commit()
    cursor.close()
    
    return redirect(url_for('homeCustomer'))

#newlt implemented request function
@app.route('/requestCustomer', methods=['GET', 'POST'])
def requestCustomer():
    email = session['username']
    cursor = conn.cursor(); 
    ticket_id = request.form['ticket_id']
    query = 'INSERT INTO ticket_request(ticket_id, customer_email, request_status) \
            VALUES(%s, %s, \'pending\')'

    cursor.execute(query, (ticket_id, email))
    conn.commit()
    cursor.close()
    
    return redirect(url_for('homeCustomer'))

@app.route('/spendingCustomer', methods=['GET', 'POST'])
def spendingCustomer():
    email = session['username']
    
    #total_spent
    cursor = conn.cursor();
    query = 'SELECT SUM(price) spending \
                FROM ticket NATURAL JOIN purchases NATURAL JOIN flight \
                WHERE customer_email = %s \
                AND purchase_date \
                    BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 1 YEAR) \
                        AND CURRENT_DATE'
    cursor.execute(query, (email))
    data1 = cursor.fetchall() 
    data1 = data1[0]['spending']
    cursor.close()
    
    #last 6 month
    cursor = conn.cursor();
    query = 'SELECT MONTH(purchase_date) `month`, SUM(price) spending \
                FROM ticket NATURAL JOIN purchases NATURAL JOIN flight \
                WHERE customer_email = %s \
                AND purchase_date \
                    BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 6 MONTH) \
                        AND CURRENT_DATE \
                GROUP BY MONTH(purchase_date) \
                ORDER BY MONTH(purchase_date)'
    cursor.execute(query, (email))
    data = cursor.fetchall() 
    data2 = dict()
    month = ['January', 'February', 'March', 'April', \
             'May', 'June', 'July', 'August', 'September', \
                 'October', 'November', 'December']
    data2['month'] = []
    data2['spending'] = []
    data2['color'] = []
    for each in data:
        data2['month'].append(month[each['month']-1])
        data2['spending'].append(float(each['spending'])) 
        data2['color'].append('orange')
    cursor.close()
    #data = {'month':['3','4','5'],'spending':[2000, 2321, 1423], 'color':['red','blue','orange']}
    
    return render_template('spending_customer.html', data1=data1, data2=data2)

@app.route('/filterbySpendTimeCustomer', methods=['GET', 'POST'])	
def filterbySpendTimeCustomer():
    email = session['username']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    if start_date and end_date:
        #total_spent
        cursor = conn.cursor();
        query = 'SELECT SUM(price) spending \
                    FROM ticket NATURAL JOIN purchases NATURAL JOIN flight \
                    WHERE customer_email = %s \
                    AND purchase_date \
                        BETWEEN %s AND %s'
        cursor.execute(query, (email, start_date, end_date))
        data3 = cursor.fetchall() 
        data3 = data3[0]['spending']
        cursor.close()
        
        cursor = conn.cursor();
        query = 'SELECT MONTH(purchase_date) `month`, SUM(price) spending \
                    FROM ticket NATURAL JOIN purchases NATURAL JOIN flight \
                    WHERE customer_email = %s \
                    AND purchase_date \
                        BETWEEN %s AND %s \
                    GROUP BY MONTH(purchase_date) \
                    ORDER BY MONTH(purchase_date)'
        cursor.execute(query, (email, start_date, end_date))
        data = cursor.fetchall() 
        data4 = dict()
        month = ['January', 'February', 'March', 'April', \
                 'May', 'June', 'July', 'August', 'September', \
                     'October', 'November', 'December']
        data4['month'] = []
        data4['spending'] = []
        data4['color'] = []
        for each in data:
            data4['month'].append(month[each['month']-1])
            data4['spending'].append(float(each['spending'])) 
            data4['color'].append('orange')
        cursor.close()
        
        return render_template('spending_filter_customer.html', data3=data3, data4=data4)
    else:
        error = 'Invalid time filter!'
        return render_template('spending_filter_customer.html', error=error)

#Ginette: codes for agent page
@app.route('/homeAgent')
def homeAgent():   
    email = session['username']
    cursor = conn.cursor();
    query = 'SELECT * FROM flight NATURAL JOIN ticket NATURAL JOIN purchases NATURAL JOIN booking_agent \
            WHERE status = \'Upcoming\' \
                AND email = %s \
            ORDER BY departure_time'
    cursor.execute(query, (email))
    data1 = cursor.fetchall() 
    cursor.close()
    
    return render_template('home_agent.html', posts=data1)

@app.route('/bookAgent')
def bookAgent():
    email = session['username']
    cursor = conn.cursor();
    query = 'SELECT * FROM flight NATURAL JOIN ticket \
            WHERE status = \'Upcoming\' \
            AND airline_name IN \
                (SELECT airline_name FROM booking_agent_work_for WHERE email = %s) \
            AND ticket_id NOT IN (SELECT ticket_id FROM purchases) \
            ORDER BY departure_time'
    cursor.execute(query, (email))
    data1 = cursor.fetchall() 
    cursor.close()
    
    cursor = conn.cursor();
    query = 'SELECT DISTINCT * FROM ticket_request NATURAL JOIN ticket \
            WHERE airline_name IN \
                (SELECT airline_name FROM booking_agent_work_for WHERE email = %s) \
            AND request_status = \'pending\''
    cursor.execute(query, (email))
    data2 = cursor.fetchall() 
    cursor.close()
    return render_template('book_agent.html', email=email, flight_ticket=data1, request=data2)

        
@app.route('/filterbyCityAgent', methods=['GET', 'POST'])
def filterbyCityAgent():
    email = session['username']
    departure_city = request.form['departure_city']
    arrival_city = request.form['arrival_city']
    cursor = conn.cursor();
    if departure_city and arrival_city:  
        query = 'SELECT * FROM flight NATURAL JOIN ticket \
                WHERE status = \'Upcoming\' \
                AND airline_name IN \
                    (SELECT airline_name FROM booking_agent_work_for WHERE email = %s) \
                AND ticket_id NOT IN (SELECT ticket_id FROM purchases) \
                AND departure_airport IN (SELECT airport_name FROM airport WHERE airport_city = %s) \
                AND arrival_airport IN (SELECT airport_name FROM airport WHERE airport_city = %s) \
                ORDER BY departure_time'
        cursor.execute(query, (email, departure_city, arrival_city))
        
    elif departure_city:
        query = 'SELECT * FROM flight NATURAL JOIN ticket \
                WHERE status = \'Upcoming\' \
                AND airline_name IN \
                    (SELECT airline_name FROM booking_agent_work_for WHERE email = %s) \
                AND ticket_id NOT IN (SELECT ticket_id FROM purchases) \
                AND departure_airport IN (SELECT airport_name FROM airport WHERE airport_city = %s) \
                ORDER BY departure_time'
        cursor.execute(query, (email, departure_city))
        
    elif arrival_city:
        query = 'SELECT * FROM flight NATURAL JOIN ticket \
                WHERE status = \'Upcoming\' \
                AND airline_name IN \
                    (SELECT airline_name FROM booking_agent_work_for WHERE email = %s) \
                AND ticket_id NOT IN (SELECT ticket_id FROM purchases) \
                AND arrival_airport IN (SELECT airport_name FROM airport WHERE airport_city = %s) \
                ORDER BY departure_time'
        cursor.execute(query, (email, arrival_city))
    else:
        query = 'SELECT * FROM flight NATURAL JOIN ticket \
                WHERE status = \'Upcoming\' \
                AND airline_name IN \
                    (SELECT airline_name FROM booking_agent_work_for WHERE email = %s) \
                AND ticket_id NOT IN (SELECT ticket_id FROM purchases) \
                ORDER BY departure_time'
        cursor.execute(query, (email))
    data1 = cursor.fetchall() 
    cursor.close()
    
    cursor = conn.cursor();
    query = 'SELECT DISTINCT * FROM ticket_request NATURAL JOIN ticket \
            WHERE airline_name IN \
                (SELECT airline_name FROM booking_agent_work_for WHERE email = %s) \
            AND ticket_id NOT IN (SELECT ticket_id FROM purchases)'
    cursor.execute(query, (email))
    data2 = cursor.fetchall() 
    cursor.close()

    return render_template('book_agent.html', flight_ticket=data1, request=data2)
        


@app.route('/filterbyAirportAgent', methods=['GET', 'POST'])
def filterbyAirportAgent():
    email = session['username']
    departure_airport = request.form['departure_airport']
    arrival_airport = request.form['arrival_airport']
    cursor = conn.cursor();
    if departure_airport and arrival_airport:  
        query = 'SELECT * FROM flight NATURAL JOIN ticket \
                WHERE status = \'Upcoming\' \
                AND airline_name IN \
                    (SELECT airline_name FROM booking_agent_work_for WHERE email = %s) \
                AND ticket_id NOT IN (SELECT ticket_id FROM purchases) \
                AND departure_airport = %s \
                AND arrival_airport = %s \
                ORDER BY departure_time'
        cursor.execute(query, (email, departure_airport, arrival_airport))
        
    elif departure_airport:
        query = 'SELECT * FROM flight NATURAL JOIN ticket \
                WHERE status = \'Upcoming\' \
                AND airline_name IN \
                    (SELECT airline_name FROM booking_agent_work_for WHERE email = %s) \
                AND ticket_id NOT IN (SELECT ticket_id FROM purchases) \
                AND departure_airport = %s \
                ORDER BY departure_time'
        cursor.execute(query, (email, departure_airport))
        
    elif arrival_airport:
        query = 'SELECT * FROM flight NATURAL JOIN ticket \
                WHERE status = \'Upcoming\' \
                AND airline_name IN \
                    (SELECT airline_name FROM booking_agent_work_for WHERE email = %s) \
                AND ticket_id NOT IN (SELECT ticket_id FROM purchases) \
                AND arrival_airport = %s \
                ORDER BY departure_time'
        cursor.execute(query, (email, arrival_airport))
    else:
        query = 'SELECT * FROM flight NATURAL JOIN ticket \
                WHERE status = \'Upcoming\' \
                AND airline_name IN \
                    (SELECT airline_name FROM booking_agent_work_for WHERE email = %s) \
                AND ticket_id NOT IN (SELECT ticket_id FROM purchases) \
                ORDER BY departure_time'
        cursor.execute(query, (email))
                
    data1 = cursor.fetchall() 
    cursor.close()
    
    cursor = conn.cursor();
    query = 'SELECT DISTINCT * FROM ticket_request NATURAL JOIN ticket \
            WHERE airline_name IN \
                (SELECT airline_name FROM booking_agent_work_for WHERE email = %s) \
            AND request_status = \'pending\''
    cursor.execute(query, (email))
    data2 = cursor.fetchall() 
    cursor.close()
    
    return render_template('book_agent.html', email=email, flight_ticket=data1, request=data2)


@app.route('/filterbyTimeAgent', methods=['GET', 'POST'])
def filterbyTimeAgent():
    email = session['username']
    try:
        departure_time = time.strptime(str(request.form['departure_time']),"%Y-%m-%dT%H:%M")
        arrival_time = time.strptime(str(request.form['arrival_time']),"%Y-%m-%dT%H:%M")
    except:
        error = 'Invalid time filter!'
        return render_template('book_customer.html', error=error)
    cursor = conn.cursor();
    query = 'SELECT * FROM flight NATURAL JOIN ticket \
            WHERE status = \'Upcoming\' \
            AND airline_name IN \
                (SELECT airline_name FROM booking_agent_work_for WHERE email = %s) \
            AND ticket_id NOT IN (SELECT ticket_id FROM purchases) \
            AND departure_time < %s \
            AND arrival_time < %s \
            ORDER BY departure_time'
    cursor.execute(query, (email, departure_time, arrival_time))
    data1 = cursor.fetchall() 
    cursor.close()
    
    cursor = conn.cursor();
    query = 'SELECT DISTINCT * FROM ticket_request NATURAL JOIN ticket \
            WHERE airline_name IN \
                (SELECT airline_name FROM booking_agent_work_for WHERE email = %s) \
            AND ticket_id NOT IN (SELECT ticket_id FROM purchases) \
            AND request_status = \'pending\' '
    cursor.execute(query, (email))
    data2 = cursor.fetchall() 
    cursor.close()
    
    return render_template('book_agent.html', email=email, flight_ticket=data1, request=data2)

@app.route('/buyAgent', methods=['GET', 'POST'])
def buyAgent():
    booking_agent_email = session['username']
    cursor = conn.cursor(); 
    ticket_id = request.form['ticket_id']
    customer_email = request.form['customer_email']
    
    query1 = "SELECT * FROM booking_agent NATURAL JOIN booking_agent_work_for \
            WHERE email = %s \
            AND airline_name = (SELECT airline_name FROM ticket \
                                WHERE ticket_id = %s)"
    cursor.execute(query1, (booking_agent_email, ticket_id))
    data1 = cursor.fetchall()
    cursor.close()
    error = None
    if (data1):  
        cursor = conn.cursor(); 
        query = 'INSERT INTO purchases(ticket_id, customer_email, booking_agent_id, purchase_date) \
                VALUES(%s, %s, \
                          (SELECT booking_agent_id FROM booking_agent WHERE email = %s), \
                           CURRENT_DATE)'
        cursor.execute(query, (ticket_id, customer_email, booking_agent_email))
        conn.commit()
        cursor.close()
               
        cursor = conn.cursor(); 
        ticket_id = request.form['ticket_id']
        customer_email = request.form['customer_email']
        query = 'UPDATE ticket_request SET request_status = \'success\' \
                    WHERE (ticket_id = %s AND customer_email = %s)'
        cursor.execute(query, (ticket_id, customer_email))
        conn.commit()
        cursor.close()
        
        cursor = conn.cursor(); 
        query = 'UPDATE ticket_request SET request_status = \'failed\' \
                    WHERE (ticket_id = %s AND customer_email <> %s)'
        cursor.execute(query, (ticket_id, customer_email))
        conn.commit()
        cursor.close()
        
        return redirect(url_for('homeAgent'))
    else:
        error = 'You may only purchase tickets from airlines you work for'
        
        cursor = conn.cursor();
        query = 'SELECT * FROM flight NATURAL JOIN ticket \
                WHERE status = \'Upcoming\' \
                AND airline_name IN \
                    (SELECT airline_name FROM booking_agent_work_for WHERE email = %s) \
                AND ticket_id NOT IN (SELECT ticket_id FROM purchases) \
                ORDER BY departure_time'
        cursor.execute(query, (booking_agent_email))
        data1 = cursor.fetchall() 
        cursor.close()
        
        cursor = conn.cursor();
        query = 'SELECT DISTINCT * FROM ticket_request NATURAL JOIN ticket \
                WHERE airline_name IN \
                    (SELECT airline_name FROM booking_agent_work_for WHERE email = %s) \
                AND ticket_id NOT IN (SELECT ticket_id FROM purchases)'
        cursor.execute(query, (booking_agent_email))
        data2 = cursor.fetchall() 
        cursor.close()
        return render_template('book_agent.html', flight_ticket=data1, request=data2, error2=error)

@app.route('/commissionAgent', methods=['GET', 'POST'])
def commissionAgent():
    booking_agent_email = session['username']
    
    #view my commission
    cursor = conn.cursor();
    query = 'SELECT SUM(price) total_com, AVG(price) avg_com, COUNT(*) number_tick \
                FROM ticket NATURAL JOIN purchases NATURAL JOIN flight NATURAL JOIN booking_agent\
                WHERE email = %s \
                AND purchase_date \
                    BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 30 DAY) \
                        AND CURRENT_DATE'
    cursor.execute(query, (booking_agent_email))
    data1 = cursor.fetchall() 
    data1[0]['total_com'] = 0.1*float("{:.2f}".format(data1[0]['total_com']))
    data1[0]['avg_com'] = 0.1*float("{:.2f}".format(data1[0]['avg_com']))
    data1 = data1[0]
    cursor.close()
    
    return render_template('commission_agent.html', data1=data1)

@app.route('/filterbyBookTimeAgent', methods=['GET', 'POST'])	
def filterbyBookTimeAgent():
    booking_agent_id = session['booking_agent_id']
    
    #view my commission
    cursor = conn.cursor();
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    if start_date and end_date:
        query = 'SELECT COALESCE(SUM(price),0) AS total_com, COALESCE(AVG(price),0) AS avg_com, COUNT(*) number_tick \
                    FROM ticket NATURAL JOIN purchases NATURAL JOIN flight \
                    WHERE booking_agent_id = %s \
                    AND purchase_date \
                        BETWEEN %s AND %s'
        cursor.execute(query, (booking_agent_id, start_date, end_date))
        data2 = cursor.fetchall() 
        data2[0]['total_com'] = 0.1*float(data2[0]['total_com'])
        data2[0]['avg_com'] = 0.1*float(data2[0]['avg_com'])
        data2 = data2[0]
        cursor.close()
        
        return render_template('commission_filter_agent.html', data2=data2)
    else:
        error = 'Invalid time filter!'
        return render_template('commission_filter_agent.html', error=error)

@app.route('/viewAgent', methods=['GET', 'POST'])
def viewAgent():
    booking_agent_email = session['username']
    
    #view top 5 customers based on number of tickets bought from the booking agent in the past 6 months
    cursor = conn.cursor();
    query = 'SELECT customer_email, COUNT(*) num_of_tick \
                FROM ticket NATURAL JOIN purchases NATURAL JOIN flight NATURAL JOIN booking_agent\
                WHERE email = %s \
                AND purchase_date \
                    BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 6 MONTH) \
                        AND CURRENT_DATE \
                GROUP BY customer_email \
                ORDER BY num_of_tick DESC \
                LIMIT 5'
    cursor.execute(query, (booking_agent_email))
    data = cursor.fetchall() 
    data1 = dict()
    data1['customer_email'] = []
    data1['num_of_tick'] = []
    data1['color'] = []
    for each in data:
        data1['customer_email'].append(each['customer_email'])
        data1['num_of_tick'].append(int(each['num_of_tick'])) 
        data1['color'].append('orange')
    cursor.close()
    
    #view top 5 customers based on amount of commission received in the last year
    cursor = conn.cursor();
    query = 'SELECT customer_email, SUM(price) total_com \
                FROM ticket NATURAL JOIN purchases NATURAL JOIN flight NATURAL JOIN booking_agent\
                WHERE email = %s \
                AND purchase_date \
                    BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 1 YEAR) \
                        AND CURRENT_DATE \
                GROUP BY customer_email \
                ORDER BY total_com DESC \
                LIMIT 5'
    cursor.execute(query, (booking_agent_email))
    data = cursor.fetchall() 
    data2 = dict()
    data2['customer_email'] = []
    data2['total_com'] = []
    data2['color'] = []
    for each in data:
        data2['customer_email'].append(each['customer_email'])
        data2['total_com'].append(float(each['total_com'])) 
        data2['color'].append('orange')
    cursor.close()
    
    return render_template('view_agent.html', data1=data1, data2=data2)

@app.route('/home_staff')
def home_staff():
	return render_template('home_staff.html')

@app.route('/view_flights')
def view_flights():
    username = session['username']
    cursor = conn.cursor();
    query = 'SELECT A.airline_name, flight_num, departure_airport, departure_time, \
        arrival_airport, arrival_time, price, status, airplane_id \
            FROM flight AS A JOIN airline_staff AS B \
                WHERE A.airline_name = B.airline_name AND B.username = %s \
                    AND CURRENT_DATE <= departure_time \
                        AND departure_time <= DATE_ADD(CURRENT_DATE(),INTERVAL 30 DAY)'
    cursor.execute(query, (username))
    data = cursor.fetchall() 
    cursor.close()
    error = None
    if(data):
        return render_template('view_flights.html', username=username, data=data)
    else:
        error = 'No result'
        return render_template('view_flights.html', username=username, error=error)
    
@app.route('/view_flights_result')
def view_flights_result():
	return render_template('view_flights_result.html')

@app.route('/view_flights_customer')
def view_flights_customer():
	return render_template('view_flights_customer.html')

@app.route('/create_flight')
def create_flight():
    username = session['username']
    cursor = conn.cursor();
    query = 'SELECT A.airline_name, flight_num, departure_airport, departure_time, \
        arrival_airport, arrival_time, price, status, airplane_id \
            FROM flight AS A JOIN airline_staff AS B \
                WHERE A.airline_name = B.airline_name AND B.username = %s \
                    AND CURRENT_DATE <= departure_time \
                        AND departure_time <= DATE_ADD(CURRENT_DATE(),INTERVAL 30 DAY)'
    cursor.execute(query, (username))
    data = cursor.fetchall() 
    cursor.close()
    error = None
    if(data):
        return render_template('create_flight.html', username=username, data=data)
    else:
        error = 'No result'
        return render_template('create_flight.html', username=username, error=error)
    
@app.route('/change_status')
def change_status():
	return render_template('change_status.html')

@app.route('/add_airplane')
def add_airplane():
    username = session['username']
    cursor = conn.cursor();
    query = 'SELECT airplane_id, seats FROM airline_staff AS A JOIN airplane AS B \
        WHERE A.airline_name = B.airline_name AND A.username = %s'
    cursor.execute(query, (username))
    data = cursor.fetchall() 
    cursor.close()
    error = None
    if(data):
        return render_template('add_airplane.html', username=username, data=data)
    else:
        error = 'No result'
        return render_template('add_airplane.html', username=username, error=error)
    
@app.route('/add_airport')
def add_airport():
	return render_template('add_airport.html')

@app.route('/view_agents')
def view_agents():
    cursor = conn.cursor()
    query1 = "SELECT email, COUNT(ticket_id) FROM agent_month GROUP BY email \
        ORDER BY COUNT(ticket_id) DESC LIMIT 5"
    cursor.execute(query1)
    data1 = cursor.fetchall()
    cursor.close()
    
    cursor = conn.cursor()
    query2 = "SELECT email, COUNT(ticket_id) FROM agent_year GROUP BY email \
        ORDER BY COUNT(ticket_id) DESC LIMIT 5"
    cursor.execute(query2)
    data2 = cursor.fetchall()
    cursor.close()
    
    cursor = conn.cursor()
    query3 = "SELECT email, SUM(commission) FROM agent_year_total GROUP BY email \
        ORDER BY COUNT(ticket_id) DESC LIMIT 5"
    cursor.execute(query3)
    data3 = cursor.fetchall()
    cursor.close()
    return render_template('view_agents.html', data1=data1, data2=data2, data3=data3)

@app.route('/view_customers')
def view_customers():
    cursor = conn.cursor()
    query = "SELECT customer_email, name, COUNT(ticket_id) FROM customer_year \
        GROUP BY customer_email ORDER BY COUNT(ticket_id) DESC LIMIT 1"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return render_template('view_customers.html', data=data)

@app.route('/customer_take_flights')
def customer_take_flights():
	return render_template('customer_take_flights.html')

@app.route('/view_destinations')
def view_destinations():
    cursor = conn.cursor()
    query1 = "SELECT airport_city, COUNT(ticket_id) FROM destination_3month \
        GROUP BY airport_city ORDER BY COUNT(ticket_id) DESC LIMIT 3"
    cursor.execute(query1)
    data1 = cursor.fetchall()
    cursor.close()
    
    cursor = conn.cursor()
    query2 = "SELECT airport_city, COUNT(ticket_id) FROM destination_year \
        GROUP BY airport_city ORDER BY COUNT(ticket_id) DESC LIMIT 3"
    cursor.execute(query2)
    data2 = cursor.fetchall()
    cursor.close()
    return render_template('view_destinations.html', data1=data1, data2=data2)

@app.route('/grant_permissions')
def grant_permissions():
	return render_template('grant_permissions.html')

@app.route('/add_agents')
def add_agents():
	return render_template('add_agents.html')

@app.route('/view_reports')
def view_reports():
	return render_template('view_reports.html')

#Authenticates the login
@app.route('/loginAuth_customer', methods=['GET', 'POST'])
def loginAuth_customer():
	#grabs information from the forms
    username = request.form['username']
    password = request.form['password']

	#cursor used to send queries
    cursor = conn.cursor()
	#executes query
    query = 'SELECT * FROM customer WHERE email = %s and password = md5(%s)'
    cursor.execute(query, (username, password))
	#stores the results in a variable
    data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data):
		#creates a session for the the user
		#session is a built in
        session['username'] = username
        #switch it to home_customer
        return redirect(url_for('homeCustomer'))
    else:
		#returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('login_customer.html', error=error)
    
@app.route('/loginAuth_agent', methods=['GET', 'POST'])
def loginAuth_agent():
	#grabs information from the forms
    username = request.form['username']
    password = request.form['password']

	#cursor used to send queries
    cursor = conn.cursor()
	#executes query
    query = 'SELECT * FROM booking_agent WHERE email = %s and password = md5(%s)'
    cursor.execute(query, (username, password))
	#stores the results in a variable
    data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data):
		#creates a session for the the user
		#session is a built in
        session['username'] = username
        #switch it to home_agent
        return redirect(url_for('homeAgent'))
    else:
		#returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('login_agent.html', error=error)

@app.route('/loginAuth_staff', methods=['GET', 'POST'])
def loginAuth_staff():
	#grabs information from the forms
    username = request.form['username']
    password = request.form['password']   

	#cursor used to send queries
    cursor = conn.cursor()
	#executes query
    query = 'SELECT * FROM airline_staff WHERE username = %s and password = md5(%s)'
    cursor.execute(query, (username, password))
	#stores the results in a variable
    data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data):
		#creates a session for the the user
		#session is a built in
        session['username'] = username
        return redirect(url_for('home_staff'))
    else:
		#returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('login_staff.html', error=error)

#Authenticates the register
@app.route('/registerAuth_customer', methods=['POST'])
def registerAuth_customer():
	#grabs information from the forms
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    building_number = request.form.get('building_number')
    street = request.form.get('street')
    city = request.form.get('city')
    state = request.form.get('state')
    phone_number = request.form.get('phone_number')
    passport_number = request.form.get('passport_number')
    passport_expiration = request.form.get('passport_expiration')
    passport_country = request.form.get('passport_country')
    date_of_birth = request.form.get('date_of_birth')

	#cursor used to send queries
    cursor = conn.cursor()
	#executes query
    query = 'SELECT * FROM customer WHERE email = %s'
    cursor.execute(query, (email))
	#stores the results in a variable
    data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
		#If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('register_customer.html', error = error)
    else:
        try:
            ins = 'INSERT INTO customer VALUES(%s, %s, md5(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(ins, (email, name, password, building_number, street, city, state, phone_number, passport_number, passport_expiration, passport_country, date_of_birth))
            conn.commit()
            cursor.close()
            return render_template('customer.html')
        except:
            error = "Invalid input. Please try again."
            return render_template('register_customer.html', error = error)
        
@app.route('/registerAuth_agent', methods=['POST'])
def registerAuth_agent():
	#grabs information from the forms
    username = request.form.get('username')
    password = request.form.get('password')
    booking_agent_id = request.form.get('booking_agent_id')

	#cursor used to send queries
    cursor = conn.cursor()
	#executes query
    query = 'SELECT * FROM booking_agent WHERE email = %s'
    cursor.execute(query, (username))
	#stores the results in a variable
    data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
		#If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('register_agent.html', error = error)
    else:
        try:
            ins = 'INSERT INTO booking_agent VALUES(%s, md5(%s), %s)'
            cursor.execute(ins, (username, password, booking_agent_id))
            conn.commit()
            cursor.close()
            return render_template('agent.html')
        except:
            error = "Invalid input. Please try again."
            return render_template('register_agent.html', error = error)

@app.route('/registerAuth_staff', methods=['POST'])
def registerAuth_staff():
	#grabs information from the forms
    username = request.form.get('username')
    password = request.form.get('password')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    date_of_birth = request.form.get('date_of_birth')
    airline_name = request.form.get('airline_name')

	#cursor used to send queries
    cursor = conn.cursor()
	#executes query
    query = 'SELECT * FROM airline_staff WHERE username = %s'
    cursor.execute(query, (username))
	#stores the results in a variable
    data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
		#If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('staff.html', error = error)
    else:
        try:
            ins = 'INSERT INTO airline_staff VALUES(%s, md5(%s), %s, %s, %s, %s)'
            cursor.execute(ins, (username, password, first_name, last_name, date_of_birth, airline_name))
            conn.commit()
            cursor.close()
            return render_template('staff.html')
        except:
            error = "Invalid input. Please try again."
            return render_template('staff.html', error = error)
        
@app.route('/search_upcoming_flights', methods=['GET', 'POST'])
def search_upcoming_flights():
    #grabs information from the forms
    source_city = request.form['source_city']
    departure_airport = request.form['departure_airport']
    destination_city = request.form['destination_city']
    arrival_airport = request.form['arrival_airport']
    departure_time = request.form['departure_time'] 

    if source_city == '':
        input1 = "LIKE \'%\'"
    else:
        input1 = "= " + "\'" + source_city + "\'"
    
    if departure_airport == '':
        input2 = "LIKE \'%\'"
    else:
        input2 = "= " + "\'" + departure_airport + "\'"
    
    if destination_city == '':
        input3 = "LIKE \'%\'"
    else:
        input3 = "= " + "\'" + destination_city + "\'"
    
    if arrival_airport == '':
        input4 = "LIKE \'%\'"
    else:
        input4 = "= " + "\'" + arrival_airport + "\'"
    
    if departure_time == '':
        input5 = "LIKE \'%\'"
    else:
        input5 = "= " + "\'" + departure_time + "\'"
                
   	#cursor used to send queries
    cursor = conn.cursor()
   	#executes query
    query = "SELECT airline_name, flight_num, departure_airport, departure_time, \
        arrival_airport, arrival_time, price, status, airplane_id FROM flight JOIN airport AS A JOIN airport AS B \
            WHERE departure_airport = A.airport_name AND arrival_airport = B.airport_name \
                AND status = 'Upcoming' AND A.airport_city %s AND departure_airport %s \
                    AND B.airport_city %s AND arrival_airport %s AND departure_time %s" \
                        % (input1, input2, input3, input4, input5)
    cursor.execute(query)
   	#stores the results in a variable
    data = cursor.fetchall()
   	#use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data):	
        return render_template('upcoming_flights.html', data=data)
    else:
		#returns an error message to the html page
        error = 'No result'
        return render_template('upcoming_flights.html', error=error)
    
@app.route('/search_flight_status', methods=['GET', 'POST'])
def search_flight_status():
    #grabs information from the forms
    flight_number = request.form['flight_number']
    arrival_date = request.form['arrival_date']
    departure_date = request.form['departure_date']

    if flight_number == '':
        input1 = "LIKE \'%\'"
    else:
        input1 = "= " + flight_number
    
    if departure_date == '':
        input2 = "LIKE \'%\'"
    else:
        input2 = "LIKE" + "\'" + departure_date + "%\'"
    
    if arrival_date == '':
        input3 = "LIKE \'%\'"
    else:
        input3 = "LIKE " + "\'" + arrival_date + "%\'"
                
   	#cursor used to send queries
    cursor = conn.cursor()
   	#executes query
    query = "SELECT airline_name, flight_num, departure_time, arrival_time, status \
        FROM flight WHERE flight_num %s AND departure_time %s AND arrival_time %s" \
            % (input1, input2, input3)
    cursor.execute(query)
   	#stores the results in a variable
    data = cursor.fetchall()
   	#use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data):	
        return render_template('flight_status.html', data=data)
    else:
		#returns an error message to the html page
        error = 'No result'
        return render_template('flight_status.html', error=error)

@app.route('/search_flights', methods=['GET', 'POST'])
def search_flights():
    #grabs information from the forms
    source_city = request.form['source_city']
    departure_airport = request.form['departure_airport']
    destination_city = request.form['destination_city']
    arrival_airport = request.form['arrival_airport']
    start_date = request.form['start_date']
    end_date = request.form['end_date']

    if source_city == '':
        input1 = "LIKE \'%\'"
    else:
        input1 = "= " + "\'" + source_city + "\'"
    
    if departure_airport == '':
        input2 = "LIKE \'%\'"
    else:
        input2 = "= " + "\'" + departure_airport + "\'"
    
    if destination_city == '':
        input3 = "LIKE \'%\'"
    else:
        input3 = "= " + "\'" + destination_city + "\'"
    
    if arrival_airport == '':
        input4 = "LIKE \'%\'"
    else:
        input4 = "= " + "\'" + arrival_airport + "\'"
    
    if start_date == '':
        input5 = "LIKE \'%\'"
    else:
        input5 = ">= " + "\'" + start_date + "\'"
        
    if end_date == '':
        input6 = "LIKE \'%\'"
    else:
        input6 = "<= " + "\'" + end_date + "\'"
                
   	#cursor used to send queries
    username = session['username']
    input0 = "\'" + username + "\'"
    cursor = conn.cursor()
   	#executes query
    query = "SELECT F.airline_name, flight_num, departure_airport, departure_time, \
        arrival_airport, arrival_time, price, status, airplane_id FROM flight AS F JOIN airport AS A JOIN airport AS B JOIN airline_staff AS S \
            WHERE departure_airport = A.airport_name AND arrival_airport = B.airport_name AND F.airline_name = S.airline_name \
                AND S.username = %s AND A.airport_city %s AND departure_airport %s \
                    AND B.airport_city %s AND arrival_airport %s AND departure_time %s AND departure_time %s" \
                        % (input0, input1, input2, input3, input4, input5, input6)
    cursor.execute(query)
   	#stores the results in a variable
    data1 = cursor.fetchall()
   	#use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data1):	
        return render_template('view_flights_result.html', data1=data1)
    else:
		#returns an error message to the html page
        error = 'No result'
        return render_template('view_flights_result.html', error=error)
    
@app.route('/customer_of_flight', methods=['GET', 'POST'])
def customer_of_flight():
	#grabs information from the forms
    airline_name = request.form['airline_name']
    flight_number = request.form['flight_number']
    
   	#cursor used to send queries
    username = session['username']
    cursor = conn.cursor()
	#executes query
    query = 'SELECT C.name FROM ticket AS T JOIN purchases AS P JOIN customer AS C JOIN airline_staff AS S\
        WHERE T.ticket_id = P.ticket_id AND P.customer_email = C.email AND T.airline_name = S.airline_name \
            AND username = %s AND T.airline_name = %s AND T.flight_num = %s'
    cursor.execute(query, (username, airline_name, flight_number))
	#stores the results in a variable
    data = cursor.fetchall()
	#use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data):
		#creates a session for the the user
		#session is a built in
        return render_template('view_flights_customer.html', data=data)
    else:
		#returns an error message to the html page
        error = 'No result'
        return render_template('view_flights_customer.html', error=error)
    
@app.route('/add_flight', methods=['POST'])
def add_flight():
	#grabs information from the forms
    airline_name = request.form.get('airline_name')
    flight_num = request.form.get('flight_num')
    departure_airport = request.form.get('departure_airport')
    departure_time = request.form.get('departure_time')
    arrival_airport = request.form.get('arrival_airport')
    arrival_time = request.form.get('arrival_time')
    price = request.form.get('price')
    status = request.form.get('status')
    airplane_id = request.form.get('airplane_id')
    
    username = session['username']
    cursor = conn.cursor()
    query1 = "SELECT * FROM permission WHERE username = %s AND permission_type = \'Admin\'"
    cursor.execute(query1, (username))
    data1 = cursor.fetchall()
    cursor.close()
    error = None
    if (data1):
        pass
    else:
        error = 'No Admin permission'
        return render_template('create_flight.html', error = error)

	#cursor used to send queries
    cursor = conn.cursor()
	#executes query
    query = 'SELECT * FROM flight WHERE airline_name = %s AND flight_num = %s'
    cursor.execute(query, (airline_name, flight_num))
	#stores the results in a variable
    data = cursor.fetchall()
	#use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
		#If the previous query returns data, then user exists
        error = "This flight already exists"
        return render_template('create_flight.html', error = error)
    else:
        ins = 'INSERT INTO flight VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
        try:
            cursor.execute(ins, (airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id))
            conn.commit()
            get_seat = 'SELECT seats FROM airplane WHERE airline_name = %s AND airplane_id = %s'
            cursor.execute(get_seat, (airline_name, airplane_id))
            seat = cursor.fetchall()
            seat_num = int(seat[0]['seats'])
            
            get_id = 'SELECT COUNT(*) AS total FROM ticket'
            cursor.execute(get_id)
            total = cursor.fetchall()
            cur_id = int(total[0]['total']) + 1
            for i in range(seat_num):
                plus_ticket = 'INSERT INTO ticket VALUES(%s, %s, %s)'
                cursor.execute(plus_ticket, (cur_id, airline_name, flight_num))
                conn.commit()
                cur_id += 1                    

            cursor.close()
            return render_template('create_flight.html')
        except:
            error = "Invalid data. Please try again."
            return render_template('create_flight.html', error = error)

@app.route('/change_flight_status', methods=['GET', 'POST'])
def change_flight_status():
	#grabs information from the forms
    airline_name = request.form['airline_name']
    flight_num = request.form['flight_num']
    status = request.form['updated_status']
    
    username = session['username']
    cursor = conn.cursor()
    query1 = "SELECT * FROM permission WHERE username = %s AND permission_type = \'Operator\'"
    cursor.execute(query1, (username))
    data1 = cursor.fetchall()
    cursor.close()
    error = None
    if (data1):
        pass
    else:
        error = 'No Operator permission'
        return render_template('change_status.html', error = error)
    
    cursor = conn.cursor()
    query = "UPDATE flight SET status = %s WHERE airline_name = %s AND flight_num = %s"
    try:
        cursor.execute(query, (status, airline_name, flight_num))
        conn.commit()
        cursor.close()
        return render_template('change_status.html')
    except:
        error = 'Invalid input'
        return render_template('change_status.html', error = error)
    
@app.route('/add_new_airplane', methods=['POST'])
def add_new_airplane():
	#grabs information from the forms
    airline_name = request.form.get('airline_name')
    airplane_id = request.form.get('airplane_id')
    seats = request.form.get('seats')
    
    username = session['username']
    cursor = conn.cursor()
    query1 = "SELECT * FROM permission WHERE username = %s AND permission_type = \'Admin\'"
    cursor.execute(query1, (username))
    data1 = cursor.fetchall()
    cursor.close()
    error = None
    if (data1):
        pass
    else:
        error = 'No Admin permission'
        return render_template('add_airplane.html', error = error)
    
    cursor = conn.cursor()
    query2 = "SELECT * FROM airline_staff WHERE username = %s AND airline_name = %s"
    cursor.execute(query2, (username, airline_name))
    data2 = cursor.fetchall()
    if (data2):
        pass
    else:
        error = 'Invalid airline_name input'
        return render_template('add_airplane.html', error = error)
    
	#cursor used to send queries
    cursor = conn.cursor()
	#executes query
    query = 'SELECT * FROM airplane WHERE airline_name = %s AND airplane_id = %s AND seats = %s'
    cursor.execute(query, (airline_name, airplane_id, seats))
	#stores the results in a variable
    data = cursor.fetchall()
	#use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
		#If the previous query returns data, then user exists
        error = "This airplane already exists"
        return render_template('add_airplane.html', error = error)
    else:
        ins = 'INSERT INTO airplane VALUES(%s, %s, %s)'
        try:
            cursor.execute(ins, (airline_name, airplane_id, seats))
            conn.commit()
            cursor.close()
            return render_template('add_airplane.html')
        except:
            error = "Invalid data. Please try again."
            return render_template('add_airplane.html', error = error)

@app.route('/add_new_airport', methods=['POST'])
def add_new_airport():
	#grabs information from the forms
    airport_name = request.form.get('airport_name')
    airport_city = request.form.get('airport_city')
    
    username = session['username']
    cursor = conn.cursor()
    query1 = "SELECT * FROM permission WHERE username = %s AND permission_type = \'Admin\'"
    cursor.execute(query1, (username))
    data1 = cursor.fetchall()
    cursor.close()
    error = None
    if (data1):
        pass
    else:
        error = 'No Admin permission'
        return render_template('add_airplane.html', error = error)

	#cursor used to send queries
    cursor = conn.cursor()
	#executes query
    query = 'SELECT * FROM airport WHERE airport_name = %s AND airport_city = %s'
    cursor.execute(query, (airport_name, airport_city))
	#stores the results in a variable
    data = cursor.fetchall()
	#use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
		#If the previous query returns data, then user exists
        error = "This airport already exists"
        return render_template('add_airport.html', error = error)
    else:
        ins = 'INSERT INTO airport VALUES(%s, %s)'
        try:
            cursor.execute(ins, (airport_name, airport_city))
            conn.commit()
            cursor.close()
            return render_template('add_airport.html')
        except:
            error = "Invalid data. Please try again."
            return render_template('add_airport.html', error = error)

@app.route('/flight_list', methods=['GET', 'POST'])
def flight_list():
	#grabs information from the forms
    customer_email = request.form['customer_email']
    
   	#cursor used to send queries
    username = session['username']
    cursor = conn.cursor()
	#executes query
    query = 'SELECT F.airline_name, F.flight_num, departure_airport, departure_time, \
        arrival_airport, arrival_time, price, status, airplane_id \
            FROM purchases as P, ticket AS T, flight AS F, airline_staff AS S \
                WHERE P.ticket_id = T.ticket_id AND T.airline_name = F.airline_name AND T.flight_num = F.flight_num \
                    AND F.airline_name = S.airline_name AND customer_email = %s AND S.username = %s'
    cursor.execute(query, (customer_email, username))
	#stores the results in a variable
    data = cursor.fetchall()
	#use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data):
		#creates a session for the the user
		#session is a built in
        return render_template('customer_take_flights.html', data=data)
    else:
		#returns an error message to the html page
        error = 'No result'
        return render_template('customer_take_flights.html', error=error)
    
@app.route('/permit', methods=['POST'])
def permit():
	#grabs information from the forms
    staff_username = request.form.get('username')
    permission_type = request.form.get('permission_type')
    
    username = session['username']
    cursor = conn.cursor()
    query1 = "SELECT * FROM permission WHERE username = %s AND permission_type = \'Admin\'"
    cursor.execute(query1, (username))
    data1 = cursor.fetchall()
    cursor.close()
    error = None
    if (data1):
        pass
    else:
        error = 'No Admin permission'
        return render_template('grant_permissions.html', error = error)
    
    cursor = conn.cursor()
    query2 = "SELECT airline_name FROM airline_staff WHERE username = %s"
    cursor.execute(query2, (username))
    data2 = cursor.fetchall()
    query3 = "SELECT airline_name FROM airline_staff WHERE username = %s"
    cursor.execute(query3, (staff_username))
    data3 = cursor.fetchall()
    cursor.close()
    error = None
    if (data2==data3):
        pass
    else:
        error = 'You can only grant permission to the staff in your airline'
        return render_template('grant_permissions.html', error = error)

	#cursor used to send queries
    cursor = conn.cursor()
	#executes query
    query = 'SELECT * FROM permission WHERE username = %s AND permission_type = %s'
    cursor.execute(query, (staff_username, permission_type))
	#stores the results in a variable
    data = cursor.fetchall()
	#use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
		#If the previous query returns data, then user exists
        error = "This user already had the permission"
        return render_template('grant_permissions.html', error = error)
    else:
        ins = 'INSERT INTO permission VALUES(%s, %s)'
        try:
            cursor.execute(ins, (staff_username, permission_type))
            conn.commit()
            cursor.close()
            return render_template('grant_permissions.html')
        except:
            error = "Invalid data. Please try again."
            return render_template('grant_permissions.html', error = error)
        
@app.route('/agent_airline', methods=['POST'])
def agent_airline():
	#grabs information from the forms
    agent_email = request.form.get('agent_email')
    airline_name = request.form.get('airline_name')
    
    username = session['username']
    cursor = conn.cursor()
    query1 = "SELECT * FROM permission WHERE username = %s AND permission_type = \'Admin\'"
    cursor.execute(query1, (username))
    data1 = cursor.fetchall()
    cursor.close()
    error = None
    if (data1):
        pass
    else:
        error = 'No Admin permission'
        return render_template('add_agents.html', error = error)
    
    cursor = conn.cursor()
    query2 = "SELECT * FROM airline_staff WHERE username = %s AND airline_name = %s"
    cursor.execute(query2, (username, airline_name))
    data2 = cursor.fetchall()
    cursor.close()
    error = None
    if (data2):
        pass
    else:
        error = 'You can only grant agents the permission to your airline'
        return render_template('add_agents.html', error = error)

	#cursor used to send queries
    cursor = conn.cursor()
	#executes query
    query = 'SELECT * FROM booking_agent_work_for WHERE email = %s AND airline_name = %s'
    cursor.execute(query, (agent_email, airline_name))
	#stores the results in a variable
    data = cursor.fetchall()
	#use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
		#If the previous query returns data, then user exists
        error = "This agent is already in the airline"
        return render_template('add_agents.html', error = error)
    else:
        ins = 'INSERT INTO booking_agent_work_for VALUES(%s, %s)'
        try:
            cursor.execute(ins, (agent_email, airline_name))
            conn.commit()
            cursor.close()
            return render_template('add_agents.html')
        except:
            error = "Invalid data. Please try again."
            return render_template('add_agents.html', error = error)
        
@app.route('/show_reports', methods=['GET', 'POST'])
def show_reports():
	#grabs information from the forms
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    
   	#cursor used to send queries
    cursor = conn.cursor()
    query = "SELECT COUNT(ticket_id) FROM purchases \
        WHERE purchase_date BETWEEN %s AND %s"
    cursor.execute(query, (start_date, end_date))
    data = cursor.fetchall()
    # if(data):
    #     return render_template('view_reports.html', data=data)
    # else:
    #     error = "No result"
    #     return render_template('view_reports.html', error=error)

    cursor = conn.cursor();
    query = 'SELECT MONTH(purchase_date) `month`, COUNT(ticket_id) `times` \
                FROM purchases WHERE purchase_date BETWEEN %s AND %s \
                GROUP BY MONTH(purchase_date) \
                ORDER BY MONTH(purchase_date)'
    cursor.execute(query, (start_date, end_date))
    data1 = cursor.fetchall()
    data2 = dict()
    month = ['January', 'February', 'March', 'April', \
             'May', 'June', 'July', 'August', 'September', \
                 'October', 'November', 'December']
    data2['month'] = []
    data2['times'] = []
    data2['color'] = []
    for each in data1:
        data2['month'].append(month[each['month']-1])
        data2['times'].append(int(each['times'])) 
        data2['color'].append('lightblue')
    cursor.close()
    #data = {'month':['3','4','5'],'spending':[2000, 2321, 1423], 'color':['red','blue','orange']}
    
    return render_template('view_reports.html', data=data, data2=data2)

@app.route('/compare_revenue1')
def compare_revenue1():
    cursor = conn.cursor()
    query1 = "SELECT SUM(price) AS MD FROM revenue_month_direct"
    cursor.execute(query1)
    data1 = cursor.fetchall()
    
    cursor = conn.cursor()
    query2 = "SELECT SUM(price) AS MI FROM revenue_month_indirect"
    cursor.execute(query2)
    data2 = cursor.fetchall()
    
    return render_template('compare_revenue1.html', data1=data1, data2=data2)

@app.route('/compare_revenue2')
def compare_revenue2():    
    cursor = conn.cursor()
    query3 = "SELECT SUM(price) AS YD FROM revenue_year_direct"
    cursor.execute(query3)
    data3 = cursor.fetchall()
    
    cursor = conn.cursor()
    query4 = "SELECT SUM(price) AS YI FROM revenue_year_indirect"
    cursor.execute(query4)
    data4 = cursor.fetchall()
    
    return render_template('compare_revenue2.html', data3=data3, data4=data4)


@app.route('/home')
def home():
    
    username = session['username']
    cursor = conn.cursor();
    query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
    cursor.execute(query, (username))
    data1 = cursor.fetchall() 
    for each in data1:
        print(each['blog_post'])
    cursor.close()
    return render_template('home.html', username=username, posts=data1)

		
@app.route('/post', methods=['GET', 'POST'])
def post():
	username = session['username']
	cursor = conn.cursor();
	blog = request.form['blog']
	query = 'INSERT INTO blog (blog_post, username) VALUES(%s, %s)'
	cursor.execute(query, (blog, username))
	conn.commit()
	cursor.close()
	return redirect(url_for('home'))

@app.route('/logout')
def logout():
	session.pop('username')
	return redirect('/')
		
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
