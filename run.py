"""Start the web app with `python run.py`, or `python run.py --prod` for a production server."""
import os
import sys

from wsgi import app

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    if "--prod" in sys.argv:
        from waitress import serve

        print(f"Serving on http://localhost:{port}")
        serve(app, host="0.0.0.0", port=port)
    else:
        app.run(host="127.0.0.1", port=port, debug=True)
