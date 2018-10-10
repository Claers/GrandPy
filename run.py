from grandpy import app
import sys
import json
import os

# Launch the flask app in debug mode
if __name__ == "__main__":
    app.debug = True
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
