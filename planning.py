from flask import Flask, render_template
import mysql.connector
from datetime import timedelta

app = Flask(__name__)

# Database configuration
db_config = {
    'user': 'jules.humblet',
    'password': 'ybMe4jiduGVjQ0Xx',
    'host': 'enac.darties.fr',
    'database': 'aeroclub'
}

def get_reservations():
    try:
        print("Connecting to database...")
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM reservation")
        reservations = cursor.fetchall()
        cursor.close()
        conn.close()

        # Print the fetched reservations to debug
        print(f"Fetched Reservations: {reservations}")

        # Convert time columns to integers representing hours
        for res in reservations:
            if isinstance(res['heure_debut'], timedelta):
                res['heure_debut'] = res['heure_debut'].seconds // 3600
            if isinstance(res['heure_fin'], timedelta):
                res['heure_fin'] = res['heure_fin'].seconds // 3600
            print(f"Reservation for {res['immat']}: Start: {res['heure_debut']}, End: {res['heure_fin']}")

        return reservations
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return []
    except Exception as e:
        print(f"Other Error: {e}")
        return []

@app.route('/')
def planning():
    reservations = get_reservations()
    print(f"Reservations: {reservations}")
    return render_template('planning.html', reservations=reservations)

if __name__ == '__main__':
    app.run(debug=True)
    
