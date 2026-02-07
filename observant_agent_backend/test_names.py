#!/usr/bin/python

"""Unit tests for names.py to detect duplicates and naming conflicts."""

from .names import monsterNames, reservedNames


def test_no_duplicates_in_monster_names():
    """Check that monsterNames has no duplicate entries."""
    duplicates = [name for name in set(monsterNames) if monsterNames.count(name) > 1]
    assert not duplicates, f"Duplicate names found in monsterNames: {duplicates}"


def test_no_duplicates_in_reserved_names():
    """Check that reservedNames has no duplicate entries."""
    duplicates = [name for name in set(reservedNames) if reservedNames.count(name) > 1]
    assert not duplicates, f"Duplicate names found in reservedNames: {duplicates}"


def test_no_overlap_between_lists():
    """Check that monsterNames and reservedNames have no overlap."""
    overlap = set(monsterNames) & set(reservedNames)
    assert not overlap, f"Names appear in both lists: {overlap}"


def test_no_substring_conflicts():
    """Check that no name is a substring of another (potential for matching issues)."""
    all_names = monsterNames + reservedNames
    conflicts = []
    for i, name1 in enumerate(all_names):
        for j, name2 in enumerate(all_names):
            if i != j and name1 in name2 and name1 != name2:
                conflicts.append((name1, name2))
    
    if conflicts:
        msg = "Substring conflicts found (name1 is substring of name2):\n"
        for name1, name2 in conflicts:
            msg += f"  '{name1}' is in '{name2}'\n"
        assert False, msg


# if __name__ == "__main__":
#     try:
#         test_no_duplicates_in_monster_names()
#         print("✓ No duplicates in monsterNames")
#     except AssertionError as e:
#         print(f"✗ {e}")

#     try:
#         test_no_duplicates_in_reserved_names()
#         print("✓ No duplicates in reservedNames")
#     except AssertionError as e:
#         print(f"✗ {e}")

#     try:
#         test_no_overlap_between_lists()
#         print("✓ No overlap between monsterNames and reservedNames")
#     except AssertionError as e:
#         print(f"✗ {e}")

#     try:
#         test_no_substring_conflicts()
#         print("✓ No substring conflicts")
#     except AssertionError as e:
#         print(f"✗ {e}")

#     print("\nAll tests passed!")
