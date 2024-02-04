from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
import json
import qrcode
from PIL import Image
from config import form_id, you
from test import fillingTableByUsers, app
import time
from changerQrs import filingTemplate
import os

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
            #SendMail(f"qrs/{user}.png", users[user]["email"])
            os.remove(f"qrs/{user}.png")
            sendedToUsers.append(users[user]["name"])
def getDataFromForms():
    users = []
    result = service.forms().responses().list(formId=form_id).execute()
    with open("test.txt", 'w') as file2:
        json.dump(result, file2, indent=1)


    for i in range(len(result["responses"])):
        users.append({"name": result["responses"][i]["answers"]["455f7693"]['textAnswers']['answers'][0]['value'],
                     "class": result["responses"][i]["answers"]["6399f9cd"]['textAnswers']['answers'][0]['value'],
                     "contact": result["responses"][i]["answers"]["5d2bcef3"]['textAnswers']['answers'][0]['value'],
                     "corpus": result["responses"][i]["answers"]["3e7403f8"]['textAnswers']['answers'][0]['value'],
                     "state": "Не пришел",
                     "email": f"{you}"})

    return users

    # class: 6399f9cd  name: 455f7693 Contacts: 5d2bcef3  corpus: 3e7403f8

with app.app_context():
    while True:
        users = getDataFromForms()
        fillingTableByUsers(users)
        QRForUsers(users)
        time.sleep(60)