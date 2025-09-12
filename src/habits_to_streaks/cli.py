from pathlib import Path
import typer

from . import converter

app = typer.Typer(
    name="habits-to-streaks",
    help="A CLI tool to convert habit tracking data into streaks.",
    no_args_is_help=True,
    add_completion=False,
)

@app.command(
    no_args_is_help=True,
)
def print(
    habits_csv_path: Path = typer.Argument(..., help="Path to the habits CSV export file."),
):
    """Parse and print the habits from a CSV export file."""
    habits = converter.parse_habits_from_csv(habits_csv_path)
    for habit in habits:
        typer.echo(habit)

@app.command(
    no_args_is_help=True,
)
def convert(
    habits_csv: Path = typer.Argument(..., help="Path to the habits CSV export file."),
    output_csv: Path = typer.Option("streaks.csv", help="Path to the output streaks CSV import file."),
    remap_json: Path = typer.Option(None, help="Path to a JSON file for remapping habit names to streak titles."),
    icon: str = typer.Option("ic_pen_quill", help="Icon to use for the streaks."),
    note: str = typer.Option("habits_to_streaks", help="Note to add to each streak entry."),
):
    """Convert a habits CSV export file to a streaks CSV import file."""
    converter.convert_habits_file_to_streaks_file(habits_csv, output_csv, remap_json, icon, note)
    typer.echo(f"Converted {habits_csv} to {output_csv}.")


if __name__ == "__main__":
    app()
