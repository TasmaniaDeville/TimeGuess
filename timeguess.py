# to do  = 1 minute stopper, readme file

import random
import numpy as np
import time
import logging


def get_random_time() -> int:
    """
    Generate a random time between 1 and 10 seconds.

    Returns:
        int: Random time in seconds.
    """
    return random.randint(1, 10)


# Function to load and process data from the file
def load_data(file_path):
    times = {i: [] for i in range(1, 11)}
    with open(file_path, "r") as file:
        for line in file:
            expected_time, actual_time = map(float, line.strip().split(','))
            times[int(expected_time)].append(actual_time)
    return times


# Function to calculate the average error for each expected time
def calculate_average_errors(times):
    average_errors = {key: (np.mean([abs(key - actual) for actual in value]) if value else 0)
                      for key, value in times.items()}
    print(average_errors)
    return average_errors


# Function to create a Matplotlib visualization of the average errors
def create_visualization(average_errors):
    times = list(average_errors.keys())
    errors = list(average_errors.values())


def record_time_to_file(expected_time: int, actual_time: float) -> None:
    """
    Record the expected and actual time to a file.

    Args:
        expected_time (int): The expected time in seconds.
        actual_time (float): The actual elapsed time in seconds.
    """
    try:
        with open("data.txt", "a") as file:
            file.write(f"{expected_time} {actual_time}\n")
    except IOError as e:
        logging.error(f"Failed to write to file: {e}")


if __name__ == '__main__':

    """
    Main function to run the time perception test.
    """
    logging.basicConfig(filename='timeguess.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
    logging.info("Starting the time perception test.")

    try:
        input("Press Enter to generate a random time...")

        random_time = get_random_time()
        print(f"Try to guess when {random_time} seconds have passed.")

        input("Press Enter to start...")

        start_time = time.time()

        input("Press Enter when you think the time has elapsed...")

        end_time = time.time()

        actual_time = end_time - start_time

        record_time_to_file(random_time, actual_time)

        print(f"Expected time: {random_time} seconds")
        print(f"Actual time: {actual_time:.2f} seconds")

        logging.info(f"Expected time: {random_time} seconds, Actual time: {actual_time:.2f} seconds")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
