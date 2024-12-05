from collections import defaultdict

from common.input import get_data_file

EXAMPLE_1 = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""


def sum_middles(data: str, correct_order: bool = True) -> int:
    priority, updates = get_input(data)
    priorities = defaultdict(set)
    for key, value in priority:
        priorities[key].add(value)

    correct, incorrect = [], []
    for update in updates:
        (correct if is_order_correct(update, priorities) else incorrect).append(update)

    if correct_order:
        return sum(update[len(update) // 2] for update in correct)
    return sum(re_sort(update, priorities)[len(update) // 2] for update in incorrect)


def re_sort(update: list[int], priority: dict[int, set]) -> list[int]:
    pages = set(update)
    ordered = []
    while pages:
        for page in list(pages):
            if not priority.get(page, set()).intersection(pages):
                ordered.append(page)
                pages.remove(page)
                break
        else:
            raise ValueError("Circular dependency detected")
    return ordered


def is_order_correct(update: list[int], priority: dict[int, set]) -> bool:
    done = set()
    for i in update:
        if priority.get(i, set()).intersection(done):
            return False
        done.add(i)
    return True


def get_input(data: str) -> (list[(int, int)], list[list[int]]):
    priority = []
    updates = []
    lines = data.strip().split("\n")
    for line in lines:
        if "|" in line:
            priority.append(tuple(map(int, line.split("|"))))
        elif "," in line:
            updates.append(list(map(int, line.split(","))))
    return priority, updates


def main() -> None:
    example_a = EXAMPLE_1
    print(f"Day 5 Part A Example = {sum_middles(example_a)}")
    part_a = get_data_file("day_5.txt")
    print(f"Day 5 Part A = {sum_middles(part_a)}")

    example_b = EXAMPLE_1
    print(f"Day 5 Part B Example = {sum_middles(example_b, False)}")
    part_b = get_data_file("day_5.txt")
    print(f"Day 5 Part B = {sum_middles(part_b, False)}")