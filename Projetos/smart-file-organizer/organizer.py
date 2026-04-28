import sortByType
import sortByDate
import duplicate_finder

def run_all(path, logger=print, progress_callback=None, selected_tasks=None):
    TASK_MAP = {
        "type": (sortByType.sortByType, "Sort by Type"),
        "date": (sortByDate.sortByDate, "Sort by Date"),
        "duplicates": (duplicate_finder.find_duplicates, "Find Duplicates")
    }

    if selected_tasks is None:
        selected_tasks = ["type", "date", "duplicates"]

    for task_name in selected_tasks:
        if task_name not in TASK_MAP:
            continue

        func, label = TASK_MAP[task_name]
        logger(f"▶ {label}...")

        func(path, logger=logger, progress_callback=progress_callback)

    logger("✅ All tasks completed!")

if __name__ == "__main__":
    folder = input("Enter folder path to organize: ")
    run_all(folder)