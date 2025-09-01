import typer

app = typer.Typer()


@app.command()
def run(conduit_path: str | None = None):
    conduit_path = "conduit" if conduit_path is None else conduit_path
    print(f"Runs both sources and targets. Active path: {conduit_path}")


if __name__ == "__main__":
    app()
