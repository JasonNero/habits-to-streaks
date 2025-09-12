
from habits_to_streaks.converter import convert_habit_to_streak
from habits_to_streaks.models import Habit, HabitEntry, Streak, StreakEntry


def test_convert_habit_to_streak():
    habit = Habit(
        id=1,
        name="Test Habit",
        description="A habit for testing",
        color_id=5,
        creation_date="2023-01-01",
        goal="2:1",
        unit="times",
        entries=[
            HabitEntry(date="2023-10-01", quantity=1),
            HabitEntry(date="2023-10-02", quantity=2),
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
        assert entry.entry_timestamp == f"{habit.entries[i].date}T12:00:00+00:00"
        assert entry.entry_timezone == "UTC"
        assert entry.quantity == habit.entries[i].quantity
        assert entry.notes == "Test note"
