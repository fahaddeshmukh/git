"""Module providing Functionality  for data manipulation and analysis."""
import pandas as pd

def load_dataframe(file_path, delimiter=','):
    """
    Load a DataFrame from a CSV file.

    Args:
        file_path (str): The path to the CSV file.
        delimiter (str, optional): The delimiter used in the CSV file. Defaults to ','.

    Returns:
        pandas.DataFrame: The loaded DataFrame.
    """
    data_frame = pd.read_csv(file_path, delimiter=delimiter)
    return data_frame


def clean_dataframe(data_frame):
    """
    Clean the DataFrame by removing unwanted columns and converting column types.

    Args:
        df (pandas.DataFrame): The DataFrame to be cleaned.

    Returns:
        pandas.DataFrame: The cleaned DataFrame.
    """
    # Removing unwanted columns
    data_frame = data_frame.iloc[:, :5]
    # Removing the total row that appears after every year
    data_frame = data_frame[data_frame['Cause of Death'] != 'Total']

    # Replacing missing values represented as '-' with 0
    data_frame.replace('-', 0, inplace=True)

    # Converting column types
    data_frame['Male'] = data_frame['Male'].astype(int)
    data_frame['Female'] = data_frame['Female'].astype(int)
    data_frame['Total'] = data_frame['Total'].astype(int)

    return data_frame
