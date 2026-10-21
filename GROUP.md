# Group submission

- Group number / catch-up label:
- Story: Campus Talent Show
- Group fork URL: https://github.com/Ndiku-leonald/OOP-WORK
- Final branch: `main`

## Members and foundation work

| Full name | Access number | Registration number | GitHub username | Foundation task | Personal branch | Commit link(s) | Merged foundation PR |
|---|---|---|---|---|---|---|---|
| Ndiku Leonald | B35011 | S25B13/086 | Ndiku-leonald | Extension 6: Lightning dance | leo_branch | [71fa20d](https://github.com/Ndiku-leonald/OOP-WORK/commit/71fa20d), [9248ebd](https://github.com/Ndiku-leonald/OOP-WORK/commit/9248ebd) | |
|  | | | | | | | |
|  | | | | | | | |
|  | | | | | | | |
|  | | | | | | | |

## Three later-topic choices

Choose exactly three different IDs from A1-A5 and record each member's coding or testing responsibility.

| Selected option | Members and specific responsibilities | Merged later-topic PRs | Demo command | Automated-check command |
|---|---|---|---|---|
| A4 | Ndiku Leonald: factory implementation and meaningful automated tests | | `py -3 stories/05_campus_talent_show/demo_leonald_b35011_a4.py` | `py -3 -m unittest discover -s stories/05_campus_talent_show -p "test_*.py"` |
|  | | | | |
|  | | | | |

## Individual later-topic contributions and reviews

| Member | Later-topic responsibility | Personal branch | Commit link(s) | Merged later-topic PR(s) | Review/comment links on teammates' PRs |
|---|---|---|---|---|---|
| Ndiku Leonald | A4: factory, Single Responsibility improvement and automated tests | leo-advanced | [a20abc2](https://github.com/Ndiku-leonald/OOP-WORK/commit/a20abc2) | | |
|  | | | | | |
|  | | | | | |
|  | | | | | |
|  | | | | | |

## Explain the work

### A4: Choice factory, Single Responsibility, and automated tests

The factory creates `Dance`, `Poetry`, and `AudienceWave` objects from clear keys. This keeps object creation in `factory.py`, while `TalentShow` handles booking and `ShowClock` handles resource rules. The automated checks cover normal creation, use through `TalentShow`, refused booking without state changes, unknown keys, and independent show state. The test suite ran seven tests successfully, and the A4 demo completed successfully.

## Run the final project

Original story:

```powershell
py -3 stories/05_campus_talent_show/story.py
```

Foundation demo:

```powershell
py -3 stories/05_campus_talent_show/demo_leonard_b35011.py
```

## Group evaluation - maximum 250 words

Word count:

## Final check

- [ ] All required foundation tasks work on `main`.
- [ ] Exactly three later-topic choices are nominated and work together.
- [ ] Every member has merged foundation and later-topic PR evidence.
- [ ] Each PR has useful comments from all its author's teammates before merge.
- [ ] The original story still runs and matches the original expected output.
- [ ] All demos and automated checks run from final `main`.
- [ ] All members are listed with full names, access numbers, registration numbers and GitHub usernames.
- [ ] The story title, individual commits, PRs and review links are complete.
- [ ] The group evaluation is no more than 250 words.
- [ ] Every member can explain their own work.