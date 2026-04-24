import sortByType
import sortByDate
import duplicate_finder

def run_all(path):
    print("📂 Sorting by file type...")
    sortByType.sortByType(path)

    print("📅 Sorting by date...")
    sortByDate.sortByDate(path)

    print("🔁 Finding duplicates...")
    duplicate_finder.find_duplicates(path)

    print("✅ All tasks completed!")

if __name__ == "__main__":
    folder = input("Enter folder path to organize: ")
    run_all(folder)