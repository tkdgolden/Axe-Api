from flask import Flask
from db import *


app = Flask(__name__)


db_connect()

