"""
Test File Manager
"""
from spidey.tools.file_manager import FileManager
import os


def test_file_manager():
    print()
    print("=" * 55)
    print("   📂 FILE MANAGER TEST")
    print("=" * 55)
    print()

    fm = FileManager()

    # Test 1: Search files
    print("--- Test 1: Search Files ---")
    results = fm.search("readme", max_results=5)
    print(fm.format_results(results, "README files"))
    print("✅ Passed!\n")

    # Test 2: Search by extension
    print("--- Test 2: Python Files ---")
    results = fm.search_by_extension(".py", max_results=5)
    print(fm.format_results(results, "Python Files"))
    print("✅ Passed!\n")

    # Test 3: Recent files
    print("--- Test 3: Recent Files ---")
    results = fm.search_recent(hours=24, max_results=5)
    print(fm.format_results(results, "Recent (24h)"))
    print("✅ Passed!\n")

    # Test 4: Large files
    print("--- Test 4: Large Files ---")
    results = fm.search_large_files(min_size_mb=10, max_results=5)
    print(fm.format_results(results, "Large (>10MB)"))
    print("✅ Passed!\n")

    # Test 5: List folder
    print("--- Test 5: List Desktop ---")
    items = fm.list_folder(os.path.expanduser("~\\Desktop"))
    for item in items[:10]:
        print(f"   {item['icon']} {item['name']} ({item['size_str']})")
    print("✅ Passed!\n")

    # Test 6: Disk space
    print("--- Test 6: Disk Space ---")
    info = fm.get_disk_space("C:")
    if isinstance(info, dict):
        print(f"   C: — {info['free']} free / {info['total']} ({info['percent_used']}% used)")
    print("✅ Passed!\n")

    # Test 7: File info
    print("--- Test 7: File Info ---")
    test_file = os.path.expanduser("~\\Desktop")
    info = fm.get_file_info(test_file)
    if isinstance(info, dict):
        for k, v in info.items():
            print(f"   {k}: {v}")
    print("✅ Passed!\n")

    print("=" * 55)
    print("   🎉 FILE MANAGER TESTS COMPLETE!")
    print("=" * 55)
    print()


if __name__ == "__main__":
    test_file_manager()