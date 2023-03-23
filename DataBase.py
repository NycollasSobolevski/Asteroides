# Codigo para inserir os dados do CSV no firebase 
# Importando dados do banco de dados Firestore
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
import pandas as pd

json = "asteroides-firebase-adminsdk-1qzrt-94bdd72726.json"
cred = credentials.Certificate(json)
firebase_admin.initialize_app(cred)
db = firestore.client()

def InsertData(nick, lifes, points):
    data = {'nickname' : nick, 'points':points, 'lifes':lifes}
    db.collection("Pontuacao_Geral").document(nick).set(data) # Adicionando pontuacao com ID personalizavel (nick)
    print(f"inserido com sucesso (Nick:{nick} points:{points} lifes:{lifes})")

def FindData(nick):
    '''result = db.collection("Pontuacao_Geral").document(nick).get()
    if result.exists:
        print(result.to_dict())'''
    
    document = db.collection("Pontuacao_Geral").where("nickname", "==", nick).get()
    for doc in document:
        print(doc.to_dict())
    return True if len(document) > 0 else False

def UpdateData(nick, points, life):
    db.collection("Pontuacao_Geral").document(nick).update({'points':points, 'lifes':life})
    print("-----Data Updated-----")

print(FindData("Optmus"))
# UpdateData("Optmus",100,2)

# scoreArc = pd.read_csv("points\points.csv")
# # InsertData(scoreArc["Nickname"][0],1,int(scoreArc["Score"][0]))



# for i in range(len(scoreArc)):
#     nick = scoreArc["Nickname"][i]
#     point = scoreArc["Score"][i]
#     print(f" {nick} {int(point)}")
#     InsertData(scoreArc["Nickname"][i], 1,int(scoreArc["Score"][i]))


# UpdateData('josue',1000)
# FindData('optmus')
# InsertData('josue',3,250)
