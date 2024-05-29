import mutpy
import numpy as np

# Configuration for mutpy with selected mutation operators
config = mutpy.config.Configuration(
    target='tictactoe',  # Your Tic-Tac-Toe implementation module
    test='tictactoe_unittests',  # Your test module
    operators=['AOR', 'COR', 'LOR'],  # Add more operators if needed
    timeout=5,
)

runner = mutpy.MutationRunner(config)
results = runner.run()

# Analyze results
killed_mutants = sum(1 for mutant in results if mutant.is_killed())
total_mutants = len(results)
mutation_score = killed_mutants / total_mutants if total_mutants else 0

print(f"Mutation Score: {mutation_score:.2%}")

# Calculate standard deviation
mutation_scores = [result.score for result in results]
std_deviation = np.std(mutation_scores)

print(f"Standard Deviation of Mutation Scores: {std_deviation:.2f}")
