"""Campus Talent Show: a cheerful MC must keep the show on time.
Run: python3 story.py. All acts and timings are fictional classroom examples.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Protocol, Sequence, Tuple


class SchedulablePerformance(Protocol):
    name: str

    def duration(self) -> int:
        ...


# ACT 1: Time is a resource with a rule: don't schedule negative minutes.
class ShowClock:
    def __init__(self, minutes):
        self.remaining = minutes  # Initialisation goes through the setter.
        self.capacity = minutes

    @property
    def remaining(self):
        return self.__remaining  # Name mangling; not an access-control system.

    @remaining.setter
    def remaining(self, amount):
        if amount < 0:
            raise ValueError("Show minutes cannot be negative.")
        self.__remaining = amount

    def reserve(self, minutes):
        if minutes <= 0 or minutes > self.remaining:
            return False
        self.remaining = self.remaining - minutes
        return True

    def release(self, minutes):
        if minutes <= 0 or minutes > self.capacity - self.remaining:
            return False
        self.remaining = self.remaining + minutes
        return True


# ACT 2: Every performance must tell the MC its duration.
class Performance(ABC):
    venue = "UCU student talent afternoon"  # Class attribute: shared fact.

    def __init__(self, name):
        self.name = name  # Instance attribute: this specific act's name.

    def describe(self):
        return f"{self.name}: {self.duration()} minutes at {self.venue}."

    @abstractmethod
    def duration(self):
        pass  # A bare Performance object is incomplete.


class Dance(Performance):  # IS-A Performance: single inheritance.
    def __init__(self, crew, minutes=6):
        super().__init__(f"{crew} dance")
        self.minutes = minutes

    def duration(self):
        return self.minutes  # Override the abstract method.


class Poetry(Performance):  # Shared parent: hierarchical inheritance.
    def duration(self):
        return 4


class Comedy(Performance):
    def duration(self):
        return 2


class ShortDance(Dance):  # Performance -> Dance -> ShortDance: multilevel.
    def duration(self):
        return super().duration() // 2  # Extend a parent's implementation.


# ACT 3: One extra capability joins the existing dance family.
class ApplauseMixin:
    def describe(self):
        return f"Mukono, make some noise! {super().describe()}"


class HeadlineDance(ApplauseMixin, ShortDance):
    pass  # Multiple parents and several levels: a hybrid hierarchy.


class AudienceWave:  # No Performance inheritance: the shared behaviour is enough.
    name = "Audience wave"

    def duration(self):
        return 1

    def describe(self):
        return "Audience wave: one minute, everybody gets to be famous."


@dataclass(frozen=True)
class RunningOrderSlot:
    performer_id: str
    performance: SchedulablePerformance
    duration: int


@dataclass(frozen=True)
class RunningOrderPlan:
    slots: Tuple[RunningOrderSlot, ...]
    skipped: Tuple[RunningOrderSlot, ...]
    remaining_minutes: int


# This planner owns the fair-turn rule and keeps each proposed slot's identity.
class RunningOrderPlanner:
    def plan(
        self,
        entries: Sequence[Tuple[str, SchedulablePerformance]],
        available_minutes: int,
        previous_performer_id: Optional[str] = None,
    ) -> RunningOrderPlan:
        if not isinstance(available_minutes, int) or isinstance(available_minutes, bool):
            raise ValueError("Available show minutes must be an integer.")
        if available_minutes < 0:
            raise ValueError("Available show minutes cannot be negative.")
        if previous_performer_id is not None and (
            not isinstance(previous_performer_id, str)
            or not previous_performer_id.strip()
        ):
            raise ValueError("A previous performer ID cannot be blank.")

        pending: List[RunningOrderSlot] = []
        for performer_id, performance in entries:
            if not isinstance(performer_id, str) or not performer_id.strip():
                raise ValueError("Every running-order entry needs a performer ID.")
            duration = performance.duration()
            if not isinstance(duration, int) or isinstance(duration, bool) or duration <= 0:
                raise ValueError("Every performance must have a positive whole-minute duration.")
            pending.append(RunningOrderSlot(performer_id, performance, duration))

        remaining = available_minutes
        previous = previous_performer_id
        slots: List[RunningOrderSlot] = []
        skipped: List[RunningOrderSlot] = []
        while pending:
            fitting = [
                (position, slot)
                for position, slot in enumerate(pending)
                if slot.duration <= remaining
            ]
            if not fitting:
                skipped.extend(pending)
                break

            different_performer = [
                item for item in fitting if item[1].performer_id != previous
            ]
            position, slot = different_performer[0] if different_performer else fitting[0]
            pending.pop(position)
            slots.append(slot)
            remaining -= slot.duration
            previous = slot.performer_id

        return RunningOrderPlan(tuple(slots), tuple(skipped), remaining)


# ACT 4: The show HAS-A clock; it borrows and swaps performance objects.
class TalentShow:
    def __init__(self, mc, minutes):
        self.mc = mc
        self.clock = ShowClock(minutes)  # Owned part: composition.
        self._lineup = []  # _ marks intended internal use, by convention.
        self.performance = None

    @property
    def act_count(self):  # Read-only: reflects the actual booked lineup.
        return len(self._lineup)

    def book(self, performance, performer_id=None):
        if performer_id is None:
            performer_id = performance.name
        elif not isinstance(performer_id, str) or not performer_id.strip():
            raise ValueError("A performer ID cannot be blank.")
        self.performance = performance  # Borrowed part: aggregation.
        minutes = performance.duration()  # Abstraction: MC doesn't count dance steps.
        if self.clock.reserve(minutes):
            self._lineup.append((performance, minutes, performer_id))
            return f"MC {self.mc} books {performance.name}."
        return f"No slot for {performance.name}. The timetable has entered the chat."

    def book_running_order(self, entries):
        previous_performer_id = self._lineup[-1][2] if self._lineup else None
        plan = RunningOrderPlanner().plan(
            entries, self.clock.remaining, previous_performer_id
        )
        booked_minutes = sum(slot.duration for slot in plan.slots)
        if booked_minutes and not self.clock.reserve(booked_minutes):
            raise RuntimeError("The planned running order no longer fits the show clock.")
        for slot in plan.slots:
            self.performance = slot.performance
            self._lineup.append((slot.performance, slot.duration, slot.performer_id))
        return plan

    def cancel(self, performance):
        for index, (booked_performance, minutes, _) in enumerate(self._lineup):
            if booked_performance is performance:
                self.clock.release(minutes)
                self._lineup.pop(index)
                return f"MC {self.mc} cancels {performance.name}."
        return f"No booking found for {performance.name}."


def audition(performances):  # Week 1's function, parameters, list, and loop.
    for performance in performances:
        print(performance.describe())  # One call, many versions: polymorphism.


def main():
    print("=== CAMPUS TALENT SHOW ===")
    print("MC Joel promised to finish on time. The dancers brought an encore.")
    acts = [Dance("Mukono Movers"), Poetry("Achen's spoken word"),
            HeadlineDance("Mukono Movers: short set"), AudienceWave(),
            Comedy("Campus comedy")]
    audition(acts)  # AudienceWave works by duck typing, with no common parent.
    joel = TalentShow("Joel", 8)
    faith = TalentShow("Faith", 8)  # Another show owns a different clock and list.
    print(joel.book(acts[2]))  # 3 minutes.
    print(joel.book(acts[0]))  # 6 won't fit in 5: refuse without changing state.
    print(joel.book(acts[1]))  # 4 minutes.
    print(joel.book(acts[3]))  # 1 minute: the whole audience finishes the show.
    print(faith.book(acts[0]))
    print(faith.book(acts[4]))
    print(faith.cancel(acts[4]))
    print(f"Joel: {joel.clock.remaining} minutes left; acts: {joel.act_count}")
    print(f"Faith: {faith.clock.remaining} minutes left; acts: {faith.act_count}")
    print("MRO (look left to right):")
    for parent in HeadlineDance.__mro__:
        print(parent.__name__)
    print("Ending: everyone gets a turn, and Joel's timetable survives.")


if __name__ == "__main__":
    main()
