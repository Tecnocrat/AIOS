# filepath: c:\dev\CodeBot\self_improvement.py
import ast
import autopep8
import random
import shutil
import os
import requests
import hashlib

# Replace logging calls with requests to OS/main.py
def log_to_os(namespace, level, message):
    """
    Sends a log message to OS/main.py for centralized logging.
    """
    try:
        # Example: Replace with actual inter-process communication if needed
        requests.post(
            "http://localhost:5000/log",  # Assuming OS/main.py runs a logging server
            json={"namespace": namespace, "level": level, "message": message}
        )
    except Exception as e:
        print(f"Failed to send log to OS: {e}")

def analyze_code(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    tree = ast.parse(code)
    # Analyze the AST for improvements (e.g., unused imports, redundant code)
    # Add logic to identify areas for improvement
    return "Analysis complete. Suggestions: [...]"

def auto_format_code(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    formatted_code = autopep8.fix_code(code)
    with open(file_path, 'w') as file:
        file.write(formatted_code)
    return "Code formatted successfully."

# Fitness function to evaluate code quality
def fitness_function(file_path):
    try:
        with open(file_path, 'r') as file:
            code = file.read()
        ast.parse(code)  # Check if the code is syntactically valid
        fitness = len(code)  # Example: shorter code is better (adjust as needed)
        log_to_os("codebot", "info", f"Evaluated fitness for {file_path}: {fitness}")
        return fitness
    except Exception as e:
        log_to_os("codebot", "error", f"Error evaluating fitness for {file_path}: {e}")
        return float('inf')  # Invalid code gets the worst score

# Generate initial population (copies of the original code)
def generate_population(source_file, population_size, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    population = []
    for i in range(population_size):
        individual_path = os.path.join(output_dir, f"individual_{i}.py")
        shutil.copy(source_file, individual_path)
        population.append(individual_path)
    return population

def deduplicate_population(output_dir):
    """
    Removes duplicate files in the genetic population folder by comparing file hashes.
    """
    print("Deduplicating population...")
    file_hashes = {}
    for file_name in os.listdir(output_dir):
        file_path = os.path.join(output_dir, file_name)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                file_hash = hashlib.md5(file.read()).hexdigest()
            if file_hash in file_hashes:
                os.remove(file_path)  # Delete duplicate file
                print(f"Deleted duplicate: {file_name}")
            else:
                file_hashes[file_hash] = file_name

# Select parents based on fitness
def select_parents(population):
    population.sort(key=fitness_function)  # Sort by fitness (lower is better)
    return population[:2]  # Select top 2 individuals

# Crossover: Combine two parents to create a child
def crossover(parent1, parent2, output_file):
    with open(parent1, 'r') as file1, open(parent2, 'r') as file2:
        code1 = file1.readlines()
        code2 = file2.readlines()
    midpoint = len(code1) // 2
    child_code = code1[:midpoint] + code2[midpoint:]
    with open(output_file, 'w') as file:
        file.writelines(child_code)

# Mutate: Apply random changes to the code
def mutate(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    mutated_code = autopep8.fix_code(code)  # Example: auto-format as mutation
    with open(file_path, 'w') as file:
        file.write(mutated_code)

# Run the genetic algorithm
def run_genetic_algorithm(source_file, generations, initial_population_size, output_dir):
    """
    Runs the genetic algorithm with exponential growth and deduplication.
    """
    log_to_os("codebot", "info", "Starting genetic algorithm...")
    population_size = initial_population_size
    population = generate_population(source_file, population_size, output_dir)

    for generation in range(generations):
        log_to_os("codebot", "info", f"Generation {generation + 1} started.")
        parents = select_parents(population)
        new_population = []

        # Exponential growth: Each individual produces two children
        for i in range(len(population)):
            child_path = os.path.join(output_dir, f"child_{generation}_{i}.py")
            crossover(parents[0], parents[1], child_path)
            mutate(child_path)
            new_population.append(child_path)

        # Add new population to the existing one
        population.extend(new_population)

        # Deduplicate population
        deduplicate_population(output_dir)

        log_to_os("codebot", "info", f"Generation {generation + 1} completed.")
        population_size *= 2  # Double the population size for the next generation

    # Return the best individual
    best_individual = population[0]
    log_to_os("codebot", "info", f"Best individual: {best_individual} with fitness {fitness_function(best_individual)}")
    return best_individual

# Example usage
if __name__ == "__main__":
    source_file = 'c:\\dev\\CodeBot\\example.py'
    output_dir = 'c:\\dev\\CodeBot\\genetic_population'
    best_code = run_genetic_algorithm(source_file, generations=5, initial_population_size=5, output_dir=output_dir)
    print(f"Best code is located at: {best_code}")