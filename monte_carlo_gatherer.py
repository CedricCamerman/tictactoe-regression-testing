import matplotlib.pyplot as plt
import numpy as np
# from tictactoe_montecarlo import MonteCarloTester
# from tictactoe_gravity_montecarlo import MonteCarloTester
# from tictactoe_3p_montecarlo import test_suite
# from tictactoe_ultimate_montecarlo import test_suite

def run_simulations(N):
    # Dummy function to simulate running simulations and returning prediction reliability scores
    # Replace this with the actual function that runs the simulations and returns the scores
    tester = MonteCarloTester(N)
    
    return tester.test_suite()

# Function to plot segmented trend lines
def plot_segmented_trend_line(x, y, color, label, segments=4):
    segment_length = len(x) // segments
    for i in range(segments):
        start_index = i * segment_length
        if i == segments - 1:  # Ensure the last segment includes the end of the data
            end_index = len(x)
        else:
            end_index = (i + 1) * segment_length + 1
        x_segment = x[start_index:end_index]
        y_segment = y[start_index:end_index]
        if len(x_segment) > 1:
            z = np.polyfit(x_segment, y_segment, 1)
            p = np.poly1d(z)
            plt.plot(x_segment, p(x_segment), linestyle='--', color=color, alpha=0.5, linewidth=2)

# requires uncommenting
def plot_reliability_scores():
    # Set M (the maximum number of simulations)
    M = 2500
    step = M//60

    # Initialize lists to store data
    simulations = []
    total_reliabilities = []
    user_reliabilities = []
    cpu_reliabilities = []
    tie_reliabilities = []

    # Run simulations from 1 to M in steps and store the average of each result
    for N in range(1, M + 1, step):
        total_reliabilities_sum = 0
        user_reliabilities_sum = 0
        cpu_reliabilities_sum = 0
        tie_reliabilities_sum = 0
    
        # Run each simulation 5 times
        for _ in range(5):
            reliabilities = run_simulations(N)
            total_reliabilities_sum += reliabilities[0]
            user_reliabilities_sum += reliabilities[3]
            cpu_reliabilities_sum += reliabilities[2]
            tie_reliabilities_sum += reliabilities[1]

        # Calculate the averages
        avg_total_reliabilities = total_reliabilities_sum / 5
        avg_user_reliabilities = user_reliabilities_sum / 5
        avg_cpu_reliabilities = cpu_reliabilities_sum / 5
        avg_tie_reliabilities = tie_reliabilities_sum / 5

        # Store the averages
        simulations.append(N)
        total_reliabilities.append(avg_total_reliabilities)
        user_reliabilities.append(avg_user_reliabilities)
        cpu_reliabilities.append(avg_cpu_reliabilities)
        tie_reliabilities.append(avg_tie_reliabilities)

    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.plot(simulations, total_reliabilities, label='Total Reliability', color='black')
    plot_segmented_trend_line(simulations, total_reliabilities, 'black', 'Total Reliability')
    plt.plot(simulations, user_reliabilities, label='User win Reliability', color='green')
    plot_segmented_trend_line(simulations, user_reliabilities, 'green', 'User win Reliability')
    plt.plot(simulations, cpu_reliabilities, label='CPU win Reliability', color='red')
    plot_segmented_trend_line(simulations, cpu_reliabilities, 'red', 'CPU win Reliability')
    plt.plot(simulations, tie_reliabilities, label='Tie Reliability', color='yellow')
    plot_segmented_trend_line(simulations, tie_reliabilities, 'yellow', 'Tie Reliability')

    plt.xlabel('Number of Simulations')
    plt.ylabel('Prediction Reliability (%)')
    plt.title('tictactoe_gravity.py Prediction Reliability Scores avg. over 5 runs')
    plt.legend()
    plt.grid(True)
    plt.show()

# requires uncommenting
def stability_scores():
    total_stability_sum = 0
    user_stability_sum = 0
    cpu_stability_sum = 0
    tie_stability_sum = 0
    for _ in range (5):
        stability_scores = run_simulations(3000)
        total_stability_sum += stability_scores[0]
        user_stability_sum += stability_scores[3]
        cpu_stability_sum += stability_scores[2]
        tie_stability_sum += stability_scores[1]

    avg_total_stability = total_stability_sum / 5
    avg_user_stability = user_stability_sum / 5
    avg_cpu_stability = cpu_stability_sum / 5
    avg_tie_stability = tie_stability_sum / 5

    print(f'Average Total Stability: {avg_total_stability:.2f}%')
    print(f'Average User Win Stability: {avg_user_stability:.2f}%')
    print(f'Average CPU Win Stability: {avg_cpu_stability:.2f}%')
    print(f'Average Tie Stability: {avg_tie_stability:.2f}%')

    

def piechart():
    # simulate 5 times for 10000 runs, take the average of those 5
    user_win_percentage = 0.4
    cpu1_win_percentage = 0.25
    cpu2_win_percentage = 0.21
    tie_percentage = 0.14

    # Data to plot
    labels = ['User Win', 'CPU1 Win', 'CPU2 Win', 'Tie']
    sizes = [user_win_percentage, cpu1_win_percentage, cpu2_win_percentage, tie_percentage]
    colors = ['#66b3ff', '#ff9999', '#ffcc66', '#99ff99']
    explode = (0.1, 0, 0, 0)  # explode 1st slice (User Win)

    # Plotting the pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=140)
    plt.title('Simulation Results tictactoe_3p.py')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Save the figure for thesis
    plt.savefig('simulation_results_pie_chart.png', dpi=300, bbox_inches='tight')

    # Display the pie chart
    plt.show()

piechart()
