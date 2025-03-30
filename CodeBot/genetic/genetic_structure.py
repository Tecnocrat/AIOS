import sys
import os
sys.path.append(os.path.abspath("C:\\dev\\CodeBot\\modules"))
import shutil
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def flatten_directory(base_dir, target_dir):
    """
    Moves all files from nested directories into a single target directory.
    """
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            src_path = os.path.join(root, file)
            dest_path = os.path.join(target_dir, file)
            if not os.path.exists(dest_path):
                shutil.move(src_path, dest_path)
            else:
                print(f"Duplicate file skipped: {dest_path}")

def run_genetic_algorithm(source_file, generations, initial_population_size, output_dir):
    logging.info("Starting genetic algorithm...")
    population = generate_population(source_file, initial_population_size, output_dir)
    for generation in range(generations):
        logging.info(f"Generation {generation + 1}: Population size = {len(population)}")
        # Existing logic...
    logging.info("Genetic algorithm completed.")

if __name__ == "__main__":
    base_dir = "c:\\dev\\CodeBot\\adn_trash_code\\replicated_CodeBot"
    target_dir = "c:\\dev\\CodeBot\\optimized_code"
    flatten_directory(base_dir, target_dir)
    print(f"Files moved to {target_dir}")