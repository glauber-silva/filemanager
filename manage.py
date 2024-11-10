from app import create_app

app = create_app()

@app.cli.command("about")
def about():
    return "Simple service to manage files"


if __name__ == "__main__":
    app.run()