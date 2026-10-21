# A5: Innovation — A fair running order

## User need

The MC needs a running order that gives the audience variety without running
past the show’s available time.

## Inputs, rules, and outcomes

- Each proposed slot has a fictional performer ID, such as `PERF-A`, and a
  performance object. Its duration comes from the object's `duration()` method.
- The planner repeatedly chooses the earliest proposed act that fits in the
  remaining time and whose performer differs from the preceding slot, whenever
  such an act is available.
- If every fitting waiting act belongs to the preceding performer, that
  performer may take the next slot; the fairness rule must not deadlock.
- Ties are resolved by original proposal order, making the result predictable.
- An act longer than the remaining time is skipped, and later shorter acts are
  still considered. Skipped acts do not consume time or change the show lineup.
- The plan reports booked slots, skipped slots, and unused minutes. The
  `TalentShow` books fitting slots against its existing clock and lineup, so
  normal cancellation still works.

For example, with eight minutes available, `PERF-A`'s six-minute dance is
followed by `PERF-B`'s four-minute poem (which cannot fit) and `PERF-C`'s
one-minute audience wave. The order is `PERF-A`, then `PERF-C`; the poem is
reported as skipped, and one minute remains. If equally eligible acts are
waiting, the earliest one in the proposed list wins.

## Why this is useful and how OOP helps

The MC can vary performers without manually calculating the remaining time.
`RunningOrderPlanner` owns the scheduling policy, while each performance
provides its own duration through the existing polymorphic interface (including
the duck-typed audience wave). `TalentShow` remains responsible for booking
the plan into its composed `ShowClock` and lineup.

## Automated checks

Run `python -m unittest discover -s stories\\05_campus_talent_show -v` to check
performer alternation, time limits, unchanged state when an act cannot fit,
skipping an oversized act in favor of a later fit, and compatibility with
direct booking and cancellation. Run the original story and separate extension
demo from the repository root:

```powershell
py -3 stories/05_campus_talent_show/story.py
py -3 stories/05_campus_talent_show/demo_alpha_success_s25b13_047.py
```

## Contribution links

| Pull request | Commit | Review |
|---|---|---|
| Pending PR creation | Pending commit | Pending review |
