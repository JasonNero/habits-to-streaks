import json
from pathlib import Path

import typer
from rich.console import Console

from . import converter

console = Console()

app = typer.Typer(
    name="habits-to-streaks",
    help="A CLI tool to convert habit tracking data into streaks.",
    no_args_is_help=True,
    add_completion=False,
)


@app.command(
    no_args_is_help=True,
)
def show(
    habits_csv_path: Path = typer.Argument(
        ...,
        help="Path to the habits CSV export file.",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    remap_json: Path = typer.Option(
        None,
        "--remap",
        "-r",
        help="Path to a JSON file for remapping habit names.",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    drop_missing_keys: bool = typer.Option(
        False,
        "--drop-missing",
        "-d",
        help="Drop habits that do not have a remapping key in the JSON file.",
    ),
):
    """Parse and show the habits from a CSV export file."""
    console.print(f"Reading habits from: {habits_csv_path}", style="blue")
    try:
        habits = converter.parse_habits_from_csv(habits_csv_path)
    except Exception as e:
        console.print(f"Error reading habits file: {e}", style="red")
        typer.Exit(1)

    if not habits:
        console.print("No habits found in the file.", style="yellow")
        return

    if remap_json:
        with remap_json.open("r") as f:
            remap = json.load(f)
        habits = converter.remap_habits(habits, remap, drop_missing=drop_missing_keys)

    console.print(f"Showing {len(habits)} habits:", style="green")
    for habit in habits:
        console.print(habit.__str__())


@app.command(
    no_args_is_help=True,
)
def convert(
    habits_csv: Path = typer.Argument(
        ...,
        help="Path to the habits CSV export file.",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    output_csv: Path = typer.Option(
        "streaks.csv",
        "--output",
        "-o",
        help="Path to the output streaks CSV import file.",
        exists=False,
    ),
    remap_json: Path = typer.Option(
        None,
        "--remap",
        "-r",
        help="Path to a JSON file for remapping habit names.",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    drop_missing_keys: bool = typer.Option(
        False,
        "--drop-missing",
        "-d",
        help="Drop habits that do not have a remapping key in the JSON file.",
    ),
    icon: str = typer.Option("ic_pen_quill", help="Icon to use for the streaks."),
    note: str = typer.Option(
        "habits_to_streaks", help="Note to add to each streak entry."
    ),
):
    """Convert a habits CSV export file to a streaks CSV import file."""
    if output_csv.exists():
        typer.confirm(
            f"Output file {output_csv} already exists. Overwrite?", abort=True
        )

    try:
        converter.convert_habits_file_to_streaks_file(
            habits_csv,
            output_csv,
            remap_json,
            drop_missing_keys,
            icon,
            note,
        )
    except Exception as e:
        console.print(f"Error converting file: {e}", style="red")
        typer.Exit(1)

    console.print(
        f"Successfully converted {habits_csv} to {output_csv}",
        style="green",
    )


if __name__ == "__main__":
    app()
