from flask import Flask, request, render_template, redirect, url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash

username = "adele.gaut"
password = "p2BhHbpWHegH8bzP"

app = Flask(__name__)
app.secret_key = 'jules'

# Création connexion
def createConnexion():
    cnx = None
    try:
        cnx = mysql.connector.connect(
            host='benoit.darties.fr', 
            user=username, 
            passwd=password, 
            db="aeroclub"
        )
        print("Connexion à la base de données réussie.")
    except Exception as e:
        print(f"Connexion impossible: {e}")
    return cnx

# Fermeture connexion
def fermerConnexion(cnx):
    if cnx:
        cnx.close()

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        try:
            nom = request.form['nom']
            prenom = request.form['prenom']
            date_naissance = request.form['dateNaissance']
            mail = request.form['email']
            licence = request.form['licence']
            num_tel = request.form['telephone']
            password_hashed = generate_password_hash(request.form['password'])
            commune = request.form['commune']
            solde = 0  # Default value for solde
        except KeyError as e:
            print(f"Champ manquant dans le formulaire: {e}")
            return "Champ manquant dans le formulaire", 400

        # Connexion à la base de données et insertion des données
        try:
            conn = createConnexion()
            if conn:
                cursor = conn.cursor()
                insert_query = '''
                    INSERT INTO adherent (licence, nom, prenom, date_naissance, mail, password, num_tel, commune, solde)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                '''
                cursor.execute(insert_query, (licence, nom, prenom, date_naissance, mail, password_hashed, num_tel, commune, solde))
                conn.commit()
                print("Données insérées avec succès.")
                cursor.close()
                fermerConnexion(conn)
                return redirect(url_for('inscription'))
            else:
                return "Erreur lors de la connexion à la base de données", 500
        except mysql.connector.Error as err:
            print(f"Erreur lors de l'insertion dans la base de données : {err}")
            return "Erreur lors de l'inscription", 500

    return render_template('inscription.html')

if __name__ == '__main__':
    app.run(debug=True)
