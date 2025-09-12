from dataclasses import dataclass, field
from uuid import uuid4


@dataclass(order=True)
class HabitEntry:
    """A single entry of a habit from the "Habitude" app"""

    date: str  # ISO 8601 date string
    quantity: int


@dataclass
class Habit:
    """Known habit fields from the "Habitude" app csv export."""

    id: int
    name: str
    description: str
    color_id: int
    creation_date: str  # ISO 8601 date string
    goal: str  # Can be 1 for daily or "2:4" for 4 times a week
    unit: str

    entries: list[HabitEntry] = field(default_factory=list)

    def __str__(self) -> str:
        return f"Habit(id={self.id}, name='{self.name}', entries={len(self.entries)})"


@dataclass
class StreakEntry:
    """Fields representing a streak from the "Streaks" app csv export."""

    entry_type: str  # e.g. "completed_manually" or "missed_auto"
    entry_date: str  # YYYYMMDD date of checking off the habit
    entry_timestamp: str  # YYYY-MM-DDTHH:MM:SSZ timestamp of checking off the habit
    entry_timezone: str  # e.g. "Europe/Berlin" or "UTC"
    quantity: int  # quantity done on that day
    notes: str = ""  # any notes, empty string if none


@dataclass
class Streak:
    """Streak/Habit definition"""

    task_id: str = field(default_factory=lambda: str(uuid4()).upper())
    title: str = ""
    icon: str = "ic_pen_quill"
    # which page the habit is displayed on, automatically overflows on import
    page: int = 0

    entries: list[StreakEntry] = field(default_factory=list)

    def __str__(self) -> str:
        return f"Streak(title='{self.title}', entries={len(self.entries)})"
