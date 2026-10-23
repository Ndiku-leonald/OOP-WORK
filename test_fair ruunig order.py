import unittest

from VICTORS import Dance, PerformerAct, Poetry, RunningOrderPlanner, TalentShow


class RunningOrderPlannerTests(unittest.TestCase):
    def setUp(self):
        self.planner = RunningOrderPlanner()

    def test_alternates_performers_when_another_act_is_waiting(self):
        acts = [
            PerformerAct("P-101", Dance("River Dancers", 2)),
            PerformerAct("P-101", Poetry("River poem")),
            PerformerAct("P-202", Dance("Skyline Crew", 2)),
        ]

        plan = self.planner.plan(acts, 8)

        self.assertEqual(
            [act.performer_id for act in plan.scheduled],
            ["P-101", "P-202", "P-101"],
        )

    def test_ties_keep_the_submitted_order(self):
        acts = [
            PerformerAct("P-203", Dance("Hilltop Crew", 2)),
            PerformerAct("P-101", Dance("River Dancers", 2)),
            PerformerAct("P-202", Dance("Skyline Crew", 2)),
        ]

        plan = self.planner.plan(acts, 6)

        self.assertEqual(
            [act.performer_id for act in plan.scheduled],
            ["P-203", "P-101", "P-202"],
        )

    def test_skips_an_act_that_does_not_fit_and_keeps_planning(self):
        acts = [
            PerformerAct("P-101", Dance("River Dancers", 6)),
            PerformerAct("P-202", Dance("Skyline Crew", 3)),
            PerformerAct("P-303", Dance("Hilltop Crew", 2)),
        ]

        plan = self.planner.plan(acts, 5)

        self.assertEqual(
            [act.performer_id for act in plan.scheduled], ["P-202", "P-303"]
        )
        self.assertEqual(
            [act.performer_id for act in plan.not_scheduled], ["P-101"]
        )
        self.assertEqual(plan.remaining_minutes, 0)

    def test_no_fitting_act_leaves_show_state_unchanged(self):
        show = TalentShow("Joel", 2)
        show.book(Dance("Opening act", 1), "P-001")
        original_entries = show.running_order.entries
        original_minutes = show.clock.remaining
        acts = [
            PerformerAct("P-101", Dance("River Dancers", 3)),
            PerformerAct("P-202", Dance("Skyline Crew", 4)),
        ]

        plan = show.plan_and_book(acts)

        self.assertEqual(plan.scheduled, ())
        self.assertEqual(len(plan.not_scheduled), 2)
        self.assertEqual(show.running_order.entries, original_entries)
        self.assertEqual(show.clock.remaining, original_minutes)
        self.assertEqual(show.act_count, 1)

    def test_planning_respects_existing_lineup_and_updates_show(self):
        show = TalentShow("Faith", 8)
        show.book(Dance("Opening act", 1), "P-101")
        acts = [
            PerformerAct("P-101", Dance("River Dancers", 2)),
            PerformerAct("P-202", Poetry("Skyline poem")),
            PerformerAct("P-303", Dance("Hilltop Crew", 1)),
        ]

        plan = show.plan_and_book(acts)

        ids = [act.performer_id for act in show.running_order.entries]
        self.assertEqual(ids, ["P-101", "P-202", "P-101", "P-303"])
        self.assertEqual(show.clock.remaining, 0)
        self.assertEqual(show.act_count, 4)
        self.assertEqual(plan.remaining_minutes, 0)

    def test_rejects_negative_available_time(self):
        with self.assertRaises(ValueError):
            self.planner.plan([], -1)


if __name__ == "__main__":
    unittest.main()
