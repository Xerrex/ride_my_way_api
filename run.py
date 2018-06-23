import os

from app import create_app

env_config = os.environ.get('FLASK_CONFIG')

app = create_app()

if __name__ == '__main__':
    app.run()
