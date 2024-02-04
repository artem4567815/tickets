import time
from test import app, sendedToUsers, db, Users
from main import GetUsers, getDataFromForms, generationQr
from changerQrs import filingTemplate
import os
import schedule as sch

def fillingTableByUsers():
    users = GetUsers()
    for user in users:
        exists = db.session.query(db.session.query(Users).filter_by(name=user["name"]).exists()).scalar()
        if not exists:
            userdb = Users(name=user['name'], clas=user["class"], corpus=user['corpus'], state=user['state'])
            try:
                db.session.add(userdb)
                db.session.commit()
            except:
                print("Error!!!")

def QRForUsers():
    users = GetUsers()
    for user in range(len(users)):
        if users[user]["name"] not in sendedToUsers:
            generationQr(f"http://127.0.0.1:5000/user/{user}/edit", user)
            filingTemplate(f"qrs/{user}.png", user, users[user]["name"], users[user]["corpus"])
            #SendMail(f"qrs/{user}.png", users[user]["email"])
            os.remove(f"qrs/{user}.png")
            sendedToUsers.append(users[user]["name"])

with app.app_context():
    print("start")
    getDataFromForms()
    sch.every(1).seconds.do(getDataFromForms)
    sch.every(1).seconds.do(fillingTableByUsers)
    sch.every(1).seconds.do(QRForUsers)

    while True:
        sch.run_pending()
        time.sleep(1)

