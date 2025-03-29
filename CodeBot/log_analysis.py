import re

def analyze_logs(log_file):
    with open(log_file, 'r') as file:
        logs = file.readlines()
    
    fitness_scores = []
    for line in logs:
        match = re.search(r"Evaluated fitness for .*: (\d+)", line)
        if match:
            fitness_scores.append(int(match.group(1)))
    
    if fitness_scores:
        best_fitness = min(fitness_scores)
        avg_fitness = sum(fitness_scores) / len(fitness_scores)
        print(f"Best Fitness: {best_fitness}")
        print(f"Average Fitness: {avg_fitness}")
    else:
        print("No fitness scores found in logs.")

# Example usage
if __name__ == "__main__":
    analyze_logs('c:\\dev\\logs\\codebot_genetic.log')