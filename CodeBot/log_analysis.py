import re
import logging

# Configure logging
logger = logging.getLogger(__name__)

def analyze_logs(log_file):
    logger.info(f"Analyzing logs: {log_file}")
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
        logger.info(f"Best Fitness: {best_fitness}, Average Fitness: {avg_fitness}")
        print(f"Best Fitness: {best_fitness}")
        print(f"Average Fitness: {avg_fitness}")
    else:
        logger.warning("No fitness scores found in logs.")
        print("No fitness scores found in logs.")

# Example usage
if __name__ == "__main__":
    logger.info("Log Analysis started.")
    analyze_logs('c:\\dev\\CodeBot\\logs\\codebot_genetic.log')