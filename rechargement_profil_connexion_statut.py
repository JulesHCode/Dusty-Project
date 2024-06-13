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
    if user_id:
        cnx = createConnexion()
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("SELECT nom, prenom, date_naissance, mail, num_tel, commune, licence,solde FROM adherent WHERE licence=%s", (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        cnx.close()
        return render_template('profil.html', user=user_data)
    else:
        return redirect(url_for('connexion'))

  
@app.route("/rechargement", methods=["GET","POST"] )
def rechargement():
    if request.method == "POST":
        solde=request.form["solde"]
        user_id = session.get('user_id')
        if user_id:
            cnx = createConnexion()
            cursor = cnx.cursor()
            cursor.execute("UPDATE adherent SET solde = solde + %s WHERE licence = %s", (solde, user_id))
            cnx.commit()
            cursor.close()
            cnx.close()
            return redirect(url_for('profil'))
    return render_template('rechargement.html')

@app.route("/statut")
def statut():
    immats = ["F-CHUP", "F-DUST", "F-ISHA", "F-RISP", "F-ROCH", "F-SKIP"]
    dispos=[]
    cnx = createConnexion()
    cursor = cnx.cursor(dictionary=True)
    for immat in immats:
        cursor.execute("SELECT disponibilite FROM avion WHERE immat=%s", (immat,))
        dispo = cursor.fetchone()
        s=list(dispo.values())
        dispos.append(s)
    cursor.close()
    cnx.close()
    print(dispos)
    return render_template('statut.html', plane=dispos)

        
if __name__ == "__main__":
    app.run(debug=True)
