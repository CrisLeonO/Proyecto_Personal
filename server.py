from app import app
from app.controllers import users
from app.controllers import movies


if __name__ == "__main__":
    app.run(debug=True)
