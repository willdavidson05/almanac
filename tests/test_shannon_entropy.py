import pathlib
from almanack.code_tracker import calculate_loc_changes
from almanack.shannon_entropy import calculate_shannon_entropy

def test_shannon_entropy(repository_paths: dict[str, pathlib.Path]):
    for _, repo_path in repository_paths.items():
        loc_changes = calculate_loc_changes(repo_path)
        entropy = calculate_shannon_entropy(loc_changes)
        
        assert isinstance(entropy, float)
        assert entropy >= 0
        print(f'Shannon entropy for {repo_path}: {entropy}')
