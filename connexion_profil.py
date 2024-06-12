import mysql.connector
from flask  import Flask, redirect, abort, render_template, g, request, url_for, flash, session

username = "adele.gaut"
password = "p2BhHbpWHegH8bzP"

app = Flask(__name__)
app.secret_key = 'jules'

# Création connexion
def createConnexion():
    cnx = None
    try :
        cnx = mysql.connector.connect(host='benoit.darties.fr', user=username, passwd=password, db="aeroclub")
    except :
        print("Connexion impossible")
    return cnx

# Fermeture connexion
def fermerConnexion(cnx):
    cnx.close()

@ app.route("/connexion", methods=["GET","POST"])
def connexion():  
    if request.method == "POST":
        return verif_connexion()
    return render_template("connexion.html")

@ app.route("/verif_connexion", methods=["GET","POST"])
def verif_connexion(): 
    Id = request.form["identifiant"]
    Mdp = request.form["motDePasse"]
    cnx = createConnexion()
    cursor = cnx.cursor()
    cursor.execute("SELECT licence, password FROM adherent WHERE licence = %s AND password = %s", (Id, Mdp))
    result = cursor.fetchone()
    fermerConnexion(cnx) 
    if result is None: 
        return redirect(url_for('connexion'))
    else:
        session['user_id'] = Id
        return redirect(url_for('profil'))
    


@ app.route("/profil")
def profil():  
    user_id = session.get('user_id')
    print(user_id)
    if user_id:
        connection = createConnexion()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT nom, prenom, date_naissance, mail, num_tel, commune, licence FROM adherent WHERE licence=%s", (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        connection.close()
        return render_template('profil.html', user=user_data)
    else:
        return redirect(url_for('connexion'))
        
if __name__ == "__main__":
    app.run(debug=True)
