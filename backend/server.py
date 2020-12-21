from flask_cors import CORS
from app.init import create_app

flask_app = create_app()
CORS(flask_app)

if __name__ == "__main__":
    flask_app.run(debug=True)
