import json
from pathlib import Path
import logging
import pandas as pd

from .models import Habit, HabitEntry, Streak, StreakEntry

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

# Habit csv export comes without headers, so we need to define them ourselves
HABITS_COLUMNS = [
    "id",
    "name",
    "2",  # unknown column
    "description",
    "color_id",
    "creation_date",
    "goal",
    "7",  # unknown column
    "8",  # unknown column
    "unit",
    "date_quantity",
    "11",  # unknown column
]


def parse_habits_from_csv(habits_csv_path: Path) -> list[Habit]:
    """Parse the habits csv export from the "Habitude" app.

    Args:
        habits_csv_path (Path): Path to the habits csv export file.

    Returns:
        list[Habit]: List of parsed Habit objects.
    """
    df = pd.read_csv(habits_csv_path, header=None, names=HABITS_COLUMNS)

    habits = []

    # One habit per row with entries as a dash-separated list of date:quantity pairs
    for _, row in df.iterrows():
        entries = []
        if pd.notna(row["date_quantity"]):
            for entry in row["date_quantity"].split("-"):
                date, quantity = entry.split(":")
                entries.append(HabitEntry(date=date, quantity=int(quantity)))

        habit = Habit(
            id=int(row["id"]),
            name=row["name"],
            description=row["description"],
            color_id=int(row["color_id"]),
            creation_date=row["creation_date"],
            goal=row["goal"],
            unit=row["unit"],
            entries=sorted(entries),
        )
        habits.append(habit)

    return habits


def remap_habits(
    habits: list[Habit],
    remap: dict = {},
    drop_missing: bool = False,
) -> list[Habit]:
    """Remap the names of a list of habits, optionally dropping those without a
    corresponding key in the remapping dictionary.

    Args:
        habits (list[Habits]): The list of habits
        remap (dict): A dictionary mapping old to new name.
        drop_missing (bool): Whether to drop habits whose names are not present in `remap`

    Returns:
        List[Habit]: The processed habits.
    """
    remapped_habits = []
    for habit in habits:
        if habit.name in remap:
            habit.name = remap[habit.name]
        elif drop_missing:
            continue
        remapped_habits.append(habit)

    return remapped_habits


def convert_habit_to_streak(
    habit: Habit,
    icon: str = "ic_pen_quill",
    note="",
) -> Streak:
    """Convert a Habit object to a Streak object.

    Args:
        habit (Habit): The Habit object to convert.

    Returns:
        Streak: The converted Streak object.
    """
    streak_entries = []
    for entry in habit.entries:
        entry_date = entry.date  # YYYYMMDD
        entry_timestamp = (
            f"{entry.date[:4]}-{entry.date[4:6]}-{entry.date[6:]}T12:00:00Z"
        )
        entry_timezone = "UTC"

        streak_entry = StreakEntry(
            entry_type="completed_manually",
            entry_date=entry_date,
            entry_timestamp=entry_timestamp,
            entry_timezone=entry_timezone,
            quantity=entry.quantity,
            notes=note,
        )
        streak_entries.append(streak_entry)

    streak = Streak(
        title=habit.name,
        icon=icon,
        entries=streak_entries,
    )

    return streak


def export_streaks_to_csv(streaks: list[Streak], output_csv_path: Path) -> None:
    """Export a list of Streak objects to a csv file.

    Args:
        streaks (list[Streak]): List of Streak objects to export.
        output_csv_path (Path): Path to the output csv file.
    """
    rows = []
    for streak in streaks:
        for entry in streak.entries:
            row = {
                "task_id": streak.task_id,
                "title": streak.title,
                "icon": streak.icon,
                "page": streak.page,
                "entry_type": entry.entry_type,
                "entry_date": entry.entry_date,
                "entry_timestamp": entry.entry_timestamp,
                "entry_timezone": entry.entry_timezone,
                "quantity": entry.quantity,
                "notes": entry.notes,
            }
            rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv(output_csv_path, index=False)


def convert_habits_file_to_streaks_file(
    habits_csv_path: Path,
    output_csv_path: Path,
    remap_json: Path = None,
    skip_missing_keys: bool = False,
    icon: str = "ic_pen_quill",
    note="",
) -> None:
    """Convert a habits csv export file to a streaks csv import file.

    Args:
        habits_csv_path (Path): Path to the habits csv export file.
        output_csv_path (Path): Path to the output streaks csv import file.
        remap_json (Path): Path to the JSON file remapping habit names.
        skip_missing_keys (bool): Whether to drop habits not defined in the remapping.
        icon (str): The icon name of the streak.
        note (str): The note for every entry.
    """

    try:
        habits = parse_habits_from_csv(habits_csv_path)
    except Exception as e:
        logger.error(f"Failed to parse habits from {habits_csv_path}: {e}")
        return

    if remap_json:
        with remap_json.open("r") as f:
            remap = json.load(f)
        habits = remap_habits(habits, remap, drop_missing=skip_missing_keys)

    streaks = [convert_habit_to_streak(habit, icon, note) for habit in habits]
    export_streaks_to_csv(streaks, output_csv_path)
    logger.info(f"Successfully converted {len(habits)} habits to streaks.")
