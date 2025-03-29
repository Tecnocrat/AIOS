import os
from utils.pipeline import save_structure_to_json, flatten_directory, genetic_algorithm

def test_pipeline():
    base_dir = "c:\\dev\\CodeBot\\adn_trash_code\\replicated_CodeBot"
    output_file = "c:\\dev\\CodeBot\\folder_structure.json"
    optimized_dir = "c:\\dev\\CodeBot\\optimized_code"

    # Step 1: Analyze folder structure
    save_structure_to_json(base_dir, output_file)
    assert os.path.exists(output_file)

    # Step 2: Flatten directory
    flatten_directory(base_dir, optimized_dir)
    assert os.path.exists(optimized_dir)

    # Step 3: Run genetic algorithm
    best_file = genetic_algorithm(optimized_dir)
    assert os.path.exists(best_file)