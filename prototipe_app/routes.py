
from flask import (
    Blueprint,
    jsonify, 
    request
)

from .db import get_db

main = Blueprint("main", __name__)

@main.get("/")
def index():
    return "<h1>Esta es la pagina principal de la API de yeltic para el protipo de Sedena</h1>"
