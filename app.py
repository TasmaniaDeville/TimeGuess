import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, send_file, render_template_string
import os
import logging
from typing import Dict, List

app = Flask(__name__)

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


def load_data(file_path: str) -> Dict[int, List[float]]:
    """
    Load the data from a file and process it.

    Args:
        file_path (str): Path to the data file.

    Returns:
        Dict[int, List[float]]: A dictionary where the keys are the expected times
        (in seconds) and the values are lists of actual times recorded.
    """
    logging.info("Loading data from file: %s", file_path)
    times = {i: [] for i in range(1, 11)}
    try:
        with open(file_path, "r") as file:
            for line in file:
                expected_time, actual_time = map(float, line.strip().split())
                times[int(expected_time)].append(actual_time)
    except FileNotFoundError:
        logging.error("File not found: %s", file_path)
        print(f"{file_path} not found. Please ensure the file exists and contains the required data.")
    return times


def calculate_average_errors(times: Dict[int, List[float]]) -> Dict[int, float]:
    """
    Calculate the average error for each expected time.

    Args:
        times (Dict[int, List[float]]): A dictionary of expected times and lists of actual times.

    Returns:
        Dict[int, float]: A dictionary where the keys are the expected times (in seconds)
        and the values are the average errors (in seconds).
    """
    logging.info("Calculating average errors.")
    average_errors = {key: (np.mean([abs(key - actual) for actual in value]) if value else 0)
                      for key, value in times.items()}
    return average_errors


def create_visualization(average_errors: Dict[int, float], output_path: str = 'static/error.png') -> None:
    """
    Create a Matplotlib visualization of the average errors.

    Args:
        average_errors (Dict[int, float]): A dictionary of average errors for each expected time.
    """
    logging.info("Creating visualization.")
    times = list(average_errors.keys())
    errors = list(average_errors.values())
    plt.figure(figsize=(10, 6))
    plt.bar(times, errors, color='mediumseagreen')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Average Error (seconds)')
    plt.title('Average Error of Human Time Perception')
    plt.xticks(times)
    plt.savefig('static/error.png')
    plt.close()
    logging.info("Visualization saved to %s", output_path)


@app.route('/')
def show_error_plot():
    """
    Flask route to display the error plot.

    Returns:
        str: Rendered HTML page containing the error plot.
    """
    logging.info("Serving the main page with error plot.")
    times = load_data('data.txt')
    average_errors = calculate_average_errors(times)
    create_visualization(average_errors)

    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Time Perception Error</title>
    </head>
    <body>
        <h1>Average Error of Human Time Perception</h1>
        <p>This shows the average error in seconds for each target time (1 to 10 seconds).</p>
        <img src="/static/error.png" alt="Error Visualization">
    </body>
    </html>
    '''
    return render_template_string(html)


@app.route('/static/error.png')
def serve_error_plot():
    """
    Flask route to serve the error plot image.

    Returns:
        send_file: Sends the error plot image as a response.
    """
    logging.info("Serving the error plot image.")
    return send_file('static/error.png', mimetype='image/png')


if __name__ == '__main__':
    if not os.path.exists('static'):
        os.makedirs('static')
    logging.info("Starting Flask app.")
    app.run(debug=True)
