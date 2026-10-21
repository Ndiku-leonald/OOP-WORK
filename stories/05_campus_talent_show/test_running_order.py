import unittest

from story import Comedy, Dance, Poetry, TalentShow


class RunningOrderTests(unittest.TestCase):
    def test_uses_earliest_different_fitting_performer(self):
        show = TalentShow("Joel", 11)
        first = Comedy("First act")
        same_performer = Dance("Second act crew", minutes=3)
        guest = Poetry("Guest poem")
        final_guest = Comedy("Final guest")

        plan = show.book_running_order([
            ("PERF-A", first),
            ("PERF-A", same_performer),
            ("PERF-B", guest),
            ("PERF-C", final_guest),
        ])

        self.assertEqual(
            [slot.performer_id for slot in plan.slots],
            ["PERF-A", "PERF-B", "PERF-A", "PERF-C"],
        )
        self.assertEqual(plan.remaining_minutes, 0)

    def test_skips_act_that_does_not_fit_without_changing_show_state(self):
        show = TalentShow("Joel", 1)
        performance = Dance("Six-minute crew")
        before = (show.clock.remaining, show.act_count)

        plan = show.book_running_order([("PERF-A", performance)])

        self.assertEqual(plan.slots, ())
        self.assertEqual([slot.performer_id for slot in plan.skipped], ["PERF-A"])
        self.assertEqual((show.clock.remaining, show.act_count), before)

    def test_considers_shorter_later_act_and_respects_budget(self):
        show = TalentShow("Joel", 2)
        too_long = Dance("Long crew")
        fits = Comedy("Short comedy")

        plan = show.book_running_order([
            ("PERF-A", too_long),
            ("PERF-B", fits),
        ])

        self.assertEqual([slot.performance for slot in plan.slots], [fits])
        self.assertEqual([slot.performance for slot in plan.skipped], [too_long])
        self.assertEqual(show.clock.remaining, 0)

    def test_respects_previously_booked_performer(self):
        show = TalentShow("Joel", 6)
        show.book(Comedy("Already booked"), "PERF-A")
        same_performer = Comedy("Same performer")
        guest = Comedy("Other performer")

        plan = show.book_running_order([
            ("PERF-A", same_performer),
            ("PERF-B", guest),
        ])

        self.assertEqual(
            [slot.performer_id for slot in plan.slots],
            ["PERF-B", "PERF-A"],
        )
        self.assertEqual(show.act_count, 3)

    def test_direct_booking_and_cancellation_still_work(self):
        show = TalentShow("Joel", 5)
        performance = Comedy("Booked comedy")

        self.assertIn("books", show.book(performance))
        self.assertEqual(show.act_count, 1)
        self.assertIn("cancels", show.cancel(performance))
        self.assertEqual(show.act_count, 0)
        self.assertEqual(show.clock.remaining, 5)


if __name__ == "__main__":
    unittest.main()
