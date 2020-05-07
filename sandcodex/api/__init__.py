import connexion
from jsonschema import ValidationError

connexion_app = connexion.FlaskApp(__name__)
connexion_app.app.config.from_object('sandcodex.api.config')
connexion_app.add_api('openapi.yml')
app = connexion_app.app
