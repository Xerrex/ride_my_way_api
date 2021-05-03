import os

from app.core import create_app
from app.models import User, Ride, Interest
from app.extensions import db


app = create_app(os.environ.get("ENV_CONFIG"))

# TODO consider @app.shell_context_processor
@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "User":User,
        "Ride": Ride,
        "Interest": Interest
    }


# if __name__ == '__main__':
#     app.run()
