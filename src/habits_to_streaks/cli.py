import typer

app = typer.Typer(
    name="habits-to-streaks",
    help="A CLI tool to convert habit tracking data into streaks.",
    no_args_is_help=True,
    add_completion=False,
)

@app.command()
def hello(name: str):
    print(f"Hello {name}")


@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")\


if __name__ == "__main__":
    app()
