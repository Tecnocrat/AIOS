import os
from core.self_improvement import generate_population

def test_generate_population():
    source_file = "c:\\dev\\CodeBot\\example.py"
    output_dir = "genetic_population"
    population = generate_population(source_file, 5, output_dir)
    assert len(population) == 5
    for individual in population:
        assert os.path.exists(individual)