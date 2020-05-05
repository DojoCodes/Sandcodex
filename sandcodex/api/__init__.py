import connexion
from jsonschema import ValidationError

connexion_app = connexion.FlaskApp(__name__)
connexion_app.add_api('openapi.yml', validate_responses=True)
app = connexion_app.app
