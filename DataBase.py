# Importando dados do banco de dados Firestore
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
import pandas as pd


def InsertData(nick, lifes, points):
    cred = credentials.Certificate("asteroides-firebase-adminsdk.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    data = {'nickname' : nick, 'points':points, 'lifes':lifes}
    db.collection("Pontuacao_Geral").document(nick).set(data) # Adicionando pontuacao com ID personalizavel (nick)
    print(f"inserido com sucesso (Nick:{nick} points:{points} lifes:{lifes})")
def FindData(nick):
    cred = credentials.Certificate("asteroides-firebase-adminsdk.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    '''result = db.collection("Pontuacao_Geral").document(nick).get()
    if result.exists:
        print(result.to_dict())'''
    
    document = db.collection("Pontuacao_Geral").where("nickname", "==", "josue").get()
    for doc in document:
        print(doc.to_dict())
def UpdateData(nick, points, life):
    cred = credentials.Certificate("asteroides-firebase-adminsdk.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    db.collection("Pontuacao_Geral").document(nick).update({'points':points, 'lifes':life})

scoreArc = pd.read_csv("points.csv")
for i in range(len(scoreArc)):
    nick = scoreArc["Nickname"][i]
    point = scoreArc["Score"][i]
    # print(f" {type(nick)} {type(point)}")
    InsertData(nick, 1,int(point))


# UpdateData('josue',1000)
# FindData('optmus')
InsertData('josue',3,250)
