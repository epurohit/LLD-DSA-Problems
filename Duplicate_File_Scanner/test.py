from main import FileMock, find_duplicate_files

files = [
    FileMock("/a.txt", 100, "Hello World! This is a test file for the system."),
    FileMock("/b.txt", 100, "Hello World! This is a test file for the system."), # Duplicate of A
    FileMock("/c.txt", 50,  "Short file."), # Different size
    FileMock("/d.txt", 100, "Hello World! But the ending is totally different."), # Same size, diff content
    FileMock("/e.txt", 100, "Hello World! But the ending is totally different.")  # Duplicate of D
]

print(find_duplicate_files(files))

# Expected Output: 
# [
#   ["/a.txt", "/b.txt"],
#   ["/d.txt", "/e.txt"]
# ]