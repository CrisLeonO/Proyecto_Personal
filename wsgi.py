from app import app as application

from app.controllers import users
from app.controllers import pokes


if __name__ == "__main__":
    application.run()
