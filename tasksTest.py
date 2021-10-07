from tasks import TaskTracker
import os

def main():
    tracker = TaskTracker(db=":memory:")  # No changes to db occur
    assert tracker.tasks == []

    # Testing inserts
    tracker.add(["task1", "task2"])
    assert tracker.tasks == ["task1", "task2"]

    tracker.add(["task3"])
    assert tracker.tasks == ["task1", "task2", "task3"]
    tracker.add(["task4", "task5", "task6"])
    assert tracker.tasks == ["task1", "task2", "task3","task4", "task5", "task6"]

    # Testing deletions
    tracker.delete(["6"])
    assert tracker.tasks == ["task1", "task2", "task3","task4", "task5"]

    tracker.delete(["1"])
    assert tracker.tasks == ["task2", "task3","task4", "task5"]

    tracker.delete(["3", "1"])
    assert tracker.tasks == ["task3", "task5"]

    # Testing clears
    tracker.clear()
    assert tracker.tasks == []

    # Testing shifts
    tracker.add(["task1", "task2", "task3", "task4", "task5"])
    tracker.shift()
    assert tracker.tasks == ["task2", "task3", "task4", "task5", "task1"]

    tracker.clear()
    tracker.shift()
    assert tracker.tasks == []

    tracker.add(["task1"])
    tracker.shift()
    assert tracker.tasks == ["task1"]

    # Testing moves
    tracker.clear()
    tracker.add(["task1", "task2", "task3", "task4", "task5"])
    tracker.move(["1", "2"])
    assert tracker.tasks == ["task2", "task1", "task3", "task4", "task5"]

    tracker.move(["3", "1"])
    assert tracker.tasks == ["task3", "task2", "task1", "task4", "task5"]

    tracker.move(["5", "5"])
    assert tracker.tasks == ["task3", "task2", "task1", "task4", "task5"]

    print("All tests passed")

if __name__ == "__main__":
    main()
