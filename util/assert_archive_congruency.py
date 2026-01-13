## Simple Script to Assert Archive Congruency

# Dependency Imports
import os
from tqdm import tqdm

def assert_archive_congruency(archive_path_1, archive_path_2):
    """
    Asserts that two archive directories have congruent file structures and contents.
    
    Parameters:
    - archive_path_1: Path to the first archive directory.
    - archive_path_2: Path to the second archive directory.
    
    Raises:
    - AssertionError: If the archives are not congruent.
    """
    
    def get_file_structure(archive_path):
        file_structure = {}
        for root, _, files in tqdm(os.walk(archive_path), desc=f"Scanning {archive_path}"):
            for file in files:
                relative_path = os.path.relpath(os.path.join(root, file), archive_path)
                file_structure[relative_path] = sum([stat for stat in os.stat(os.path.join(root, file))])
        return file_structure
    
    structure_1 = get_file_structure(archive_path_1)
    structure_2 = get_file_structure(archive_path_2)
    
    # mismatch catchers
    structure_mismatches = []
    file_mismatches = []
    
    for key in tqdm(structure_1.keys(), desc="Comparing structures"):
        if key not in structure_2:
            structure_mismatches.append(key)
        elif structure_1[key] != structure_2[key]:
            file_mismatches.append(key)
    for key in tqdm(structure_2.keys(), desc="Comparing structures"):
        if key not in structure_1:
            structure_mismatches.append(key)
        elif structure_2[key] != structure_1[key]:
            file_mismatches.append(key)

    assert not structure_mismatches, f"Structure mismatches found: {structure_mismatches}"
    assert structure_1.keys() == structure_2.keys(), "File structures do not match."
    assert not file_mismatches, f"File content mismatches found: {file_mismatches}"
            
    print("Archives are congruent.")
    
# CLI Usage Example
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python assert_archive_congruency.py <archive_path_1> <archive_path_2>")
        sys.exit(1)
    
    archive_1 = sys.argv[1]
    archive_2 = sys.argv[2]
    
    assert_archive_congruency(archive_1, archive_2)
    
# how to use:
# python util/assert_archive_congruency.py path/to/archive1 path/to/archive2