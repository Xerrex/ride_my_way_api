import os

from app.core import create_app

# TODO consider @app.shell_context_processor

app = create_app(os.environ.get("ENV_CONFIG"))

if __name__ == '__main__':
    app.run()
