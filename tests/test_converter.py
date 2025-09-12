from habits_to_streaks.converter import convert_habit_to_streak, remap_habits
from habits_to_streaks.models import Habit, HabitEntry, Streak, StreakEntry


def test_convert_habit_to_streak():
    habit = Habit(
        id=1,
        name="Test Habit",
        description="Did you apply TDD today?",
        color_id=5,
        creation_date="2023-01-01",
        goal="2:1",
        unit="happy checks",
        entries=[
            HabitEntry(date="20231001", quantity=1),
            HabitEntry(date="20231002", quantity=2),
        ],
    )

    streak = convert_habit_to_streak(habit, icon="ic_test_icon", note="Test note")

    assert isinstance(streak, Streak)
    assert streak.title == "Test Habit"
    assert streak.icon == "ic_test_icon"
    assert len(streak.entries) == 2

    for i, entry in enumerate(streak.entries):
        assert isinstance(entry, StreakEntry)
        assert entry.entry_type == "completed_manually"
        assert entry.entry_date == habit.entries[i].date
        assert (
            entry.entry_timestamp
            == f"{habit.entries[i].date[:4]}-{habit.entries[i].date[4:6]}-{habit.entries[i].date[6:]}T12:00:00Z"
        )
        assert entry.entry_timezone == "UTC"
        assert entry.quantity == habit.entries[i].quantity
        assert entry.notes == "Test note"


def test_remap_habits():
    habits = [
        Habit(
            id=1,
            name="Exercise",
            description="",
            color_id=1,
            creation_date="2025-01-01",
            goal="1",
            unit="times",
            entries=[],
        ),
        Habit(
            id=3,
            name="Read",
            description="",
            color_id=2,
            creation_date="2025-01-01",
            goal="2:4",
            unit="",
            entries=[],
        ),
        Habit(
            id=7,
            name="Meditate",
            description="",
            color_id=3,
            creation_date="2025-01-01",
            goal="2:3",
            unit="minutes",
            entries=[],
        ),
    ]

    remap = {
        "Exercise": "Workout",
        "Read": "Reading",
    }

    remapped_habits = remap_habits(habits, remap, drop_missing=True)
    assert len(remapped_habits) == 2
    assert remapped_habits[0].name == "Workout"
    assert remapped_habits[1].name == "Reading"

    remapped_habits = remap_habits(habits, remap, drop_missing=False)
    assert len(remapped_habits) == 3
    assert remapped_habits[0].name == "Workout"
    assert remapped_habits[1].name == "Reading"
    assert remapped_habits[2].name == "Meditate"
