import os
import re
import xxhash
from multiprocessing import Pool
from functools import partial


dot_file = re.compile(r'^\.')
CORES = 8
BLOCKSIZE = 1048576


# Function returns name and date of file last modified
def last_modified_file(root_folder):
    last_modified_time = 0
    last_modified_file = None

    for root, dirs, files in os.walk(root_folder):
        for file in files:
            file_path = os.path.join(root, file)
            modification_time = os.path.getmtime(file_path)

            if modification_time > last_modified_time:
                last_modified_time = modification_time
                last_modified_file = file

    return [last_modified_time, last_modified_file]


def hash_file(filepath):
    """Generate xxHash64 of a file."""
    hasher = xxhash.xxh64()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(BLOCKSIZE), b""):
            hasher.update(byte_block)
    return hasher.hexdigest()


def hash_folder(folder_path):
    """Generate hashes for all files in a folder."""
    hashes = {}
    for root, _, files in os.walk(folder_path):
        for file in files:
            if not dot_file.match(file):
                filepath = os.path.join(root, file)
                relpath = os.path.relpath(filepath, folder_path)
                file_hash = hash_file(filepath)
                hashes[file_hash] = relpath
    return hashes


def hash_folder_mp(folder_path):
    """Generate hashes for all files in a folder."""
    hashes = {}
    with Pool(CORES) as pool:
        for root, _, files in os.walk(folder_path):
            results = pool.map(partial(process_file, root, folder_path), files)
            for result in results:
                if result:
                    file_hash, relpath = result
                    hashes[file_hash] = relpath
    return hashes


def process_file(root, folder_path, file):
    """Process a single file for hashing."""
    if not dot_file.match(file):
        filepath = os.path.join(root, file)
        relpath = os.path.relpath(filepath, folder_path)
        file_hash = hash_file(filepath)
        return file_hash, relpath
    return None
