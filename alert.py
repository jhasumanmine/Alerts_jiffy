from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# MySQL connection details
db_config = {
    'host': 'localhost',
    'user': 'root',  # Your MySQL username
    'password': '',  # Your MySQL password
    'database': 'income_panel'  # Your database name
}

# Create a function to get the MySQL connection
def get_db_connection():
    connection = mysql.connector.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
    )
    return connection

# Get all alerts with optional filters
@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    category = request.args.get('category')
    priority = request.args.get('priority')
    status = request.args.get('status')
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')

    query = "SELECT * FROM alerts WHERE 1=1"
    filters = []
    
    if category:
        query += " AND category = %s"
        filters.append(category)
    if priority:
        query += " AND priority = %s"
        filters.append(priority)
    if status:
        query += " AND status = %s"
        filters.append(status)
    if from_date:
        query += " AND created_at >= %s"
        filters.append(from_date)
    if to_date:
        query += " AND created_at <= %s"
        filters.append(to_date)
    
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, tuple(filters))
    alerts = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return jsonify(alerts)

# Get a single alert by ID
@app.route('/api/alerts/<int:alert_id>', methods=['GET'])
def get_alert(alert_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM alerts WHERE alert_id = %s", (alert_id,))
    alert = cursor.fetchone()
    cursor.close()
    connection.close()
    
    if alert:
        return jsonify(alert)
    else:
        return jsonify({'message': 'Alert not found'}), 404

# Mark an alert as read
@app.route('/api/alerts/<int:alert_id>/mark-as-read', methods=['POST'])
def mark_alert_as_read(alert_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE alerts SET status = 'Read' WHERE alert_id = %s", (alert_id,))
    connection.commit()
    cursor.close()
    connection.close()
    
    return jsonify({'message': 'Alert marked as read'})

# Mark an alert as unread
@app.route('/api/alerts/<int:alert_id>/mark-as-unread', methods=['POST'])
def mark_alert_as_unread(alert_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE alerts SET status = 'Unread' WHERE alert_id = %s", (alert_id,))
    connection.commit()
    cursor.close()
    connection.close()
    
    return jsonify({'message': 'Alert marked as unread'})

# Send a payment reminder (example action)
@app.route('/api/alerts/<int:alert_id>/send-reminder', methods=['POST'])
def send_payment_reminder(alert_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM alerts WHERE alert_id = %s", (alert_id,))
    alert = cursor.fetchone()
    
    if alert:
        # Here you would integrate logic for sending a reminder (e.g., email or notification)
        # Placeholder logic for sending reminder
        message = f"Reminder: {alert['title']} is overdue. Please take action."
        print(message)  # Placeholder action
        
        return jsonify({'message': f"Reminder sent for {alert['title']}"})
    else:
        cursor.close()
        connection.close()
        return jsonify({'message': 'Alert not found'}), 404





if __name__ == '__main__':
    app.run(debug=True)
