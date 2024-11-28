from flask import Flask

app = Flask(__name__)
app.config.from_object('trarecoapp.config')
app.secret_key = 'session_key'

import trarecoapp.views