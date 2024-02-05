from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
import qrcode
from PIL import Image
from config import form_id
from test import fillingTableByUsers, app, Users, db
import time
from changerQrs import filingTemplate
import os
from sendEmails import SendMail

SCOPES = "https://www.googleapis.com/auth/forms.responses.readonly"
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

store = file.Storage("token.json")
creds = None
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets("client_secrets.json", SCOPES)
    creds = tools.run_flow(flow, store)
service = discovery.build(
    "forms",
    "v1",
    http=creds.authorize(Http()),
    discoveryServiceUrl=DISCOVERY_DOC,
    static_discovery=False,
)

def generationQr(url='/', name='default'):
    qr = qrcode.make(url)
    qr.save(f'qrs/{name}.png')
    img = Image.open(f'qrs/{name}.png').resize((250, 250))
    img.save(f'qrs/{name}.png')
    img.close()
    return "qr code was created!"


sendedToUsers = []
def QRForUsers(users):
    for user in range(len(users)):
        if users[user]["name"] not in sendedToUsers:
            generationQr(f"http://127.0.0.1:5000/user/{user}/edit", user)
            filingTemplate(f"qrs/{user}.png", user, users[user]["name"], users[user]["corpus"])
            try:
                SendMail(f"qrs/{user}.png", users[user]["email"])
            except:
                print("INcorrectEmail")
            os.remove(f"qrs/{user}.png")
            sendedToUsers.append(users[user]["name"])
def getDataFromForms():
    users = []
    result = service.forms().responses().list(formId=form_id).execute()

    if result:
        for i in range(len(result["responses"])):
            users.append({"name": result["responses"][i]["answers"]["57cb5553"]['textAnswers']['answers'][0]['value'],
                         "class": result["responses"][i]["answers"]["3fc8dd3e"]['textAnswers']['answers'][0]['value'],
                         "corpus": result["responses"][i]["answers"]["755f7eb5"]['textAnswers']['answers'][0]['value'],
                         "state": "Не пришел",
                         "email": result["responses"][i]["answers"]["27260596"]['textAnswers']['answers'][0]['value']})

    return users

    # class: 3fc8dd3e  name: 57cb5553 Contacts: 27260596  corpus: 755f7eb5


with app.app_context():
    print("start")
    res = db.session.query(Users).all()
    for user in res:
        sendedToUsers.append(user.name)
        print("succses")
    while True:
        users = getDataFromForms()
        fillingTableByUsers(users)
        QRForUsers(users)
        time.sleep(60)
