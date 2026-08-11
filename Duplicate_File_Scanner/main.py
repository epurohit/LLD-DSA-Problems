import hashlib

from collections import defaultdict

class FileMock:
    def __init__(self, path: str, size: int, content: str):
        self.path = path
        self.size = size
        self.small_hash = ""
        self._content = content # Private: Do not access directly!

    def read_chunk(self, start: int, length: int) -> str:
        """Simulates an I/O operation reading a specific chunk of the file."""
        return self._content[start : start + length]

def find_duplicate_files(files: list[FileMock]) -> list[list[str]]:
    file_sizes = defaultdict(list)
    for mockfile in files:
        file_sizes[mockfile.size].append(mockfile)

    ans = []
    
    # Process sequentially within isolated size buckets to prevent cross-contamination
    for size, size_group in file_sizes.items():
        if len(size_group) == 1:
            continue

        file_hash_small = defaultdict(list)
        for mockfile in size_group:
            chunk = mockfile.read_chunk(0, 100)
            file_chunk_hash = hashlib.sha256(chunk.encode("utf-8")).hexdigest()
            file_hash_small[file_chunk_hash].append(mockfile)

        for small_hash, chunk_group in file_hash_small.items():
            if len(chunk_group) == 1:
                continue

            file_hash_large = defaultdict(list)
            for mockfile in chunk_group:
                # Read via the public API instead of accessing the private _content variable
                full_content = mockfile.read_chunk(0, mockfile.size)
                file_hash = hashlib.sha256(full_content.encode("utf-8")).hexdigest()
                file_hash_large[file_hash].append(mockfile.path)

            for large_hash, paths in file_hash_large.items():
                if len(paths) > 1:
                    ans.append(paths)

    return ans