from core.self_improvement import run_genetic_algorithm

if __name__ == "__main__":
    source_file = "c:\\dev\\CodeBot\\example.py"
    output_dir = "genetic_population"
    best_code = run_genetic_algorithm(source_file, generations=5, initial_population_size=5, output_dir=output_dir)
    print(f"Best code is located at: {best_code}")