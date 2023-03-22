# Importando dados do banco de dados Firestore
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
import pandas as pd

json = "asteroides-firebase-adminsdk-1qzrt-db5ace13de.json"

def InsertData(nick, lifes, points):
    cred = credentials.Certificate(json)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    data = {'nickname' : nick, 'points':points, 'lifes':lifes}
    db.collection("Pontuacao_Geral").document(nick).set(data) # Adicionando pontuacao com ID personalizavel (nick)
    print(f"inserido com sucesso (Nick:{nick} points:{points} lifes:{lifes})")

def FindData(nick):
    cred = credentials.Certificate(json)
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    '''result = db.collection("Pontuacao_Geral").document(nick).get()
    if result.exists:
        print(result.to_dict())'''
    
    document = db.collection("Pontuacao_Geral").where("nickname", "==", nick).get()
    for doc in document:
        print(doc.to_dict())

def UpdateData(nick, points, life):
    cred = credentials.Certificate(json)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    db.collection("Pontuacao_Geral").document(nick).update({'points':points, 'lifes':life})


print("1")
cred = credentials.Certificate(json)
print("cred")
firebase_admin.initialize_app(credential= cred)
print("initi")
db = firestore.client()
print("db")

data={"name":"deu boa"}
print("data")
db.collection('persona').add(data)



# scoreArc = pd.read_csv("points\points.csv")

# for i in range(len(scoreArc)):
#     nick = scoreArc["Nickname"][i]
#     point = scoreArc["Score"][i]
#     print(f" {nick} {int(point)}")
#     InsertData(nick, 1,int(point))


# UpdateData('josue',1000)
# FindData('optmus')
# InsertData('josue',3,250)
