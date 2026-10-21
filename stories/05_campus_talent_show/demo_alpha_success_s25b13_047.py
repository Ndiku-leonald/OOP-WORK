"""Demonstrate a fair running order without changing the original story menu."""
from story import Comedy, Dance, Poetry, TalentShow


def print_check(label, expected, actual):
    print(f"{label}")
    print(f"  Expected: {expected}")
    print(f"  Actual:   {actual}")


def main():
    show = TalentShow("Alpha Success", 11)
    plan = show.book_running_order([
        ("PERF-A", Comedy("First comedy set")),
        ("PERF-A", Dance("Second dance crew", minutes=3)),
        ("PERF-B", Poetry("Guest poem")),
        ("PERF-C", Comedy("Final comedy set")),
    ])
    actual_order = [slot.performer_id for slot in plan.slots]
    print_check(
        "Normal case (alternate performer when an eligible one is waiting)",
        ["PERF-A", "PERF-B", "PERF-A", "PERF-C"],
        actual_order,
    )
    print_check("Remaining minutes", 0, show.clock.remaining)

    short_show = TalentShow("Alpha Success", 1)
    too_long = Dance("Six-minute crew")
    before = (short_show.clock.remaining, short_show.act_count)
    refused = short_show.book_running_order([("PERF-D", too_long)])
    after = (short_show.clock.remaining, short_show.act_count)
    actual_refusal = (
        [slot.performer_id for slot in refused.skipped],
        before == after,
        after,
    )
    print_check(
        "Refusal case (oversized act is skipped; show state stays unchanged)",
        (["PERF-D"], True, (1, 0)),
        actual_refusal,
    )


if __name__ == "__main__":
    main()
