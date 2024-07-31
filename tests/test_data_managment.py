from almanack. data_management import save_entropy_to_json
import tempfile 
import json
def test_save_entropy_to_json():
    # Define test inputs
    repo_path = "test_repo_path"
    normalized_total_entropy = 0.4567

    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file_path = temp_file.name

    # Call the function with the temporary file path
    save_entropy_to_json(repo_path, normalized_total_entropy, temp_file_path)
    
    # Read the file to check if it has content
    with open(temp_file_path, 'r') as file:
        content = json.load(file)

    # Check if json file is non-emtpy
    assert content