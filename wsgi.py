import argparse

import api

app = api.create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        "db": api.db,
        "sa": api.models.sa,
        "api": api,
    }


if __name__ == "__main__":
    app.run()
