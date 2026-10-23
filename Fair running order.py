from dataclasses import dataclass


@dataclass(frozen=True)
class Performance:
    """A single act with a performer ID, title, and duration in minutes."""

    performer_id: str
    title: str
    duration: int

    def __post_init__(self):
        if not isinstance(self.performer_id, str) or not self.performer_id.strip():
            raise ValueError('Performer ID is required')
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError('Performance title is required')
        if type(self.duration) is not int or self.duration <= 0:
            raise ValueError('Duration must be a positive whole number')


class FairnessPolicy:
    """Keep the show fair by avoiding back-to-back repeats whenever another act fits."""

    @staticmethod
    def choose_next(remaining, time_left, last_performer_id):
        if not remaining:
            return None

        fitting = [act for act in remaining if act.duration <= time_left]
        if not fitting:
            return None

        alternatives = [
            act for act in fitting if act.performer_id != last_performer_id
        ]

        # Registration order decides ties. Repeat only if no different performer can fit.
        chosen = (alternatives or fitting)[0]
        return chosen


class TalentShow:
    """Collection of all performances waiting to be scheduled."""

    def __init__(self):
        self._performances = []

    def add_performance(self, performance):
        if not isinstance(performance, Performance):
            raise TypeError('Expected a Performance object')
        self._performances.append(performance)

    @property
    def performances(self):
        return tuple(self._performances)


class RunningOrderPlanner:
    """Build a fair running order that respects the time available."""

    def __init__(self, show):
        if not isinstance(show, TalentShow):
            raise TypeError('Expected a TalentShow object')
        self._show = show
        self._schedule = ()

    @property
    def schedule(self):
        return self._schedule

    def plan(self, available_minutes):
        """Return a tuple of performances in fair schedule order."""
        if type(available_minutes) is not int or available_minutes < 0:
            raise ValueError('Available time must be a non-negative whole number')

        remaining = list(self._show.performances)
        new_schedule = []
        time_left = available_minutes
        last_performer = None

        while True:
            chosen = FairnessPolicy.choose_next(remaining, time_left, last_performer)
            if chosen is None:
                break

            new_schedule.append(chosen)
            remaining.remove(chosen)
            time_left -= chosen.duration
            last_performer = chosen.performer_id

        self._schedule = tuple(new_schedule)
        return self._schedule


def _assert_basic_checks():
    """Small automated checks to demonstrate the expected behaviour."""
    show = TalentShow()
    for act in (
        Performance('P001', 'Singing', 5),
        Performance('P001', 'Poetry', 3),
        Performance('P002', 'Dancing', 4),
        Performance('P003', 'Comedy', 6),
        Performance('P002', 'Drama', 4),
    ):
        show.add_performance(act)

    order = RunningOrderPlanner(show).plan(20)
    assert [act.performer_id for act in order] == ['P001', 'P002', 'P001', 'P003']
    assert sum(act.duration for act in order) == 18


def demo():
    """Show the fair running order in a simple campus talent-show format."""
    show = TalentShow()
    for act in (
        Performance('P001', 'Singing', 5),
        Performance('P001', 'Poetry', 3),
        Performance('P002', 'Dancing', 4),
        Performance('P003', 'Comedy', 6),
        Performance('P002', 'Drama', 4),
    ):
        show.add_performance(act)

    planner = RunningOrderPlanner(show)
    print('CAMPUS TALENT SHOW - FAIR RUNNING ORDER')
    for slot, act in enumerate(planner.plan(20), 1):
        print(f'{slot}. {act.performer_id}: {act.title} ({act.duration} min)')
    print('Total:', sum(act.duration for act in planner.schedule), 'minutes')


if __name__ == '__main__':
    _assert_basic_checks()
    demo()
