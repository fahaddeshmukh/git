"""Modules providing Functionality  for data manipulation, analysis,
support for CLI, plotting and data pre-processing."""
import argparse
import pandas as pd
import matplotlib.pyplot as plt
from data_processing import load_dataframe, clean_dataframe


FILE_PATH = 'D:/RSE1/data/Death_DE.csv'

#Basic descreptive statistics

def calculate_death_statistics(yearly_deaths: pd.DataFrame, grouped_causes: pd.DataFrame) -> None:
    """
    Calculate and print death statistics based on the yearly_deaths and grouped_causes DataFrames.

    Args:
        yearly_deaths (pd.DataFrame): DataFrame containing yearly deaths data.
        grouped_causes (pd.DataFrame): DataFrame containing grouped causes data.
    """
    total_deaths = yearly_deaths['Total'].sum()
    total_deaths_male = yearly_deaths['Male'].sum()
    total_deaths_female = yearly_deaths['Female'].sum()
    disease_count = grouped_causes['Cause of Death'].nunique()

    print(f"The total number of unique causes of death in the past decade is: {disease_count}")
    print(f"The total number of people who died in the past decade is: {total_deaths}")
    print(f"The total number of men who died in the past decade is: {total_deaths_male}")
    print(f"The total number of women who died in the past decade is: {total_deaths_female}")


def plot_death_charts(yearly_deaths):
    """
    Plot line and pie charts to visualize death statistics.

    Args:
        yearly_deaths (pandas.DataFrame): DataFrame containing yearly deaths data.
    """
    # Getting total male and female deaths
    total_deaths_male = yearly_deaths['Male'].sum()
    total_deaths_female = yearly_deaths['Female'].sum()

    # Create a list of labels for the pie chart
    labels = ['Male', 'Female']

    # Create a list of values for the pie chart
    values = [total_deaths_male, total_deaths_female]

    # Create a list of colors for the pie chart
    colors = ['blue', 'pink']

    # Create the line chart
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))  # Adjust figsize as needed

    ax1.plot(yearly_deaths['Year'], yearly_deaths['Male'], color='blue', linestyle='-', marker='o', label='Male')
    ax1.plot(yearly_deaths['Year'], yearly_deaths['Female'], color='pink', linestyle='--', marker='s', label='Female')
    ax1.plot(yearly_deaths['Year'], yearly_deaths['Total'], color='black', linestyle='-', marker='^', label='Total')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Number of Deaths')
    ax1.set_title('Annual Number of Deaths')
    ax1.legend()

    # Create the pie chart
    ax2.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax2.set_title('Male vs Female Deaths')

    # Adjust spacing between subplots
    plt.subplots_adjust(wspace=0.4)

    # Display the subplots
    plt.show()

def plot_causes(grouped_causes, plot_type='top', num_causes=10):
    """
    Plot bar charts for the top or lowest causes of death.

    Args:
        grouped_causes (pandas.DataFrame): DataFrame containing grouped causes of death.
        plot_type (str, optional): Type of plot to create, 'top' (default) or 'lowest'.
        num_causes (int, optional): Number of causes to include in the plot. Defaults to 10.

    Returns:
        None
    """
    if plot_type == 'top':
        top_causes = grouped_causes.nlargest(num_causes, 'Total')
        title_prefix = 'Top'
        colors = ['black', 'blue', 'pink']
    elif plot_type == 'lowest':
        top_causes = grouped_causes.nsmallest(num_causes, 'Total')
        title_prefix = 'Lowest'
        colors = ['black', 'blue', 'pink']
    else:
        raise ValueError("Invalid plot type. Supported values are 'top' or 'lowest'.")

    # Create the subplots
    fig, axes = plt.subplots(1, 3, figsize=(24, 8))

    for i, (ax, column, color) in enumerate(zip(axes, ['Total', 'Male', 'Female'], colors)):
        ax.bar(top_causes['Cause of Death'], top_causes[column], color=color)
        ax.set_xlabel('Cause of Death')
        ax.set_ylabel(f'{column} Deaths')
        ax.set_title(f'{num_causes} {title_prefix} Causes of Death ({column})')
        ax.set_xticks(range(num_causes))
        ax.set_xticklabels(top_causes['Cause of Death'], rotation='vertical')

    # Adjust spacing between subplots
    plt.subplots_adjust(wspace=0.4)

    # Display the subplots
    plt.show()

def plot_male_female_deaths_proportion(df):
    """
    Plots pie charts to,
    visualize the proportion of male and female deaths for 2011 & 2020.

    Args:
        df (DataFrame): DataFrame containing the data.

    """
    # Step 1: Filter the data for the years 2011 and 2020
    filtered_data = df[df['Year'].isin([2011, 2020])]

    # Step 2: Calculate the total number of male and female deaths for each year
    grouped_data = filtered_data.groupby('Year')[['Male', 'Female']].sum().reset_index()

    # Create the subplots
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    # Pie chart for male and female deaths in 2011
    axs[0].pie(grouped_data[grouped_data['Year'] == 2011][['Male', 'Female']].values.flatten(), labels=['Male', 'Female'], autopct='%1.1f%%', colors=['lightblue', 'pink'])
    axs[0].set_title('Proportion of Male and Female Deaths in 2011')

    # Pie chart for male and female deaths in 2020
    axs[1].pie(grouped_data[grouped_data['Year'] == 2020][['Male', 'Female']].values.flatten(), labels=['Male', 'Female'], autopct='%1.1f%%', colors=['lightblue', 'pink'])
    axs[1].set_title('Proportion of Male and Female Deaths in 2020')

    # Adjust spacing between subplots
    plt.tight_layout()

    # Display the charts
    plt.show()

def plot_top_causes_years(df, year1, year2, gender='Male', num_causes=20):
    """
    Plot line charts to,
    visualize and compare the top causes of death for a specific gender in two different years.

    Args:
        df (pandas.DataFrame): DataFrame containing death data.
        year1 (int): First year for analysis.
        year2 (int): Second year for analysis.
        gender (str, optional): Gender for analysis. Defaults to 'Male'.
        num_causes (int, optional): Number of top causes to include in the plot. Defaults to 20.

    Returns:
        None
    """
    #Filtering the data for the specified years and gender
    filtered_data = df[(df['Year'].isin([year1, year2])) & (df[gender] > 0)]

    #Grouping the data by the cause of death and calculate the total number of deaths for each cause
    grouped_data = filtered_data.groupby(['Year', 'Cause of Death'])[[gender]].sum().reset_index()

    #Sorting the causes of death based on the total number of deaths in descending order
    sorted_data_1 = grouped_data[grouped_data['Year'] == year1].sort_values(by=gender, ascending=False)
    sorted_data_2 = grouped_data[grouped_data['Year'] == year2].sort_values(by=gender, ascending=False)

    #Selecting the top causes of death for each year
    top_causes_1 = sorted_data_1.head(num_causes)
    top_causes_2 = sorted_data_2.head(num_causes)

    # Creating two line charts side by side to visualize the data
    fig, axs = plt.subplots(1, 2, figsize=(20, 11))

    # Plot for year1
    axs[0].plot(range(len(top_causes_1)), top_causes_1[gender], marker='o')
    axs[0].set_xticks(range(len(top_causes_1)))
    axs[0].set_xticklabels(top_causes_1['Cause of Death'], rotation=90)
    axs[0].set_title(f'Top {num_causes} Causes of Death for {gender} in {year1}')
    axs[0].set_xlabel('Cause of Death')
    axs[0].set_ylabel('Number of Deaths')

    # Plot for year2
    axs[1].plot(range(len(top_causes_2)), top_causes_2[gender], marker='o')
    axs[1].set_xticks(range(len(top_causes_2)))
    axs[1].set_xticklabels(top_causes_2['Cause of Death'], rotation=90)
    axs[1].set_title(f'Top {num_causes} Causes of Death for {gender} in {year2}')
    axs[1].set_xlabel('Cause of Death')
    axs[1].set_ylabel('Number of Deaths')

    # Adjust spacing between subplots
    plt.tight_layout()

    # Display the charts
    plt.show()


def plot_population_vs_deaths(df, population_2011, deaths_2011, population_2020, deaths_2020):
    """
    Plots pie charts to,
    visualize the proportion of population and deaths for 2011 and 2020.

    Args:
        df (DataFrame): DataFrame containing the data.
        population_2011 (int): Population count for the year 2011.
        deaths_2011 (int): Number of deaths for the year 2011.
        population_2020 (int): Population count for the year 2020.
        deaths_2020 (int): Number of deaths for the year 2020.

    """
    #Calculating the proportion of population and deaths for each year
    population_proportion_2011 = [population_2011 - deaths_2011, deaths_2011]
    population_proportion_2020 = [population_2020 - deaths_2020, deaths_2020]

    #Creating two pie charts side by side to visualize the proportion of population and deaths
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    # Pie chart for population and deaths in 2011
    axs[0].pie(population_proportion_2011, labels=['Alive', 'Deaths'], autopct='%1.1f%%', colors=['lightgreen', 'red'])
    axs[0].set_title('Proportion of Population and Deaths in 2011')

    # Pie chart for population and deaths in 2020
    axs[1].pie(population_proportion_2020, labels=['Alive', 'Deaths'], autopct='%1.1f%%', colors=['lightgreen', 'red'])
    axs[1].set_title('Proportion of Population and Deaths in 2020')

    # Adjust spacing between subplots
    plt.tight_layout()

    # Display the charts
    plt.show()



def main():
    """Main function, providing functionality for executing other functions."""
    parser = argparse.ArgumentParser(description='Foreign Population Analysis')
    parser.add_argument('FILE_PATH', type=str, help='Path to the dataset file')
    args = parser.parse_args()

    population_2011 = 80327900
    population_2020 = 83155031
    deaths_2011 = 944675
    deaths_2020 = 1068660
    file_path = args.FILE_PATH

    # Load and clean dataframe
    data_frame = load_dataframe(file_path, delimiter=';')
    data_frame = clean_dataframe(data_frame)

    # Grouping the causes of death for the last decade
    df_causes = data_frame.drop(data_frame.columns[0], axis=1)
    grouped_causes = df_causes.groupby('Cause of Death').sum().reset_index()

    # Getting annual yearly death counts
    df_years = data_frame.drop(data_frame.columns[1], axis=1)
    yearly_deaths = df_years.groupby('Year').sum().reset_index()

    # Calling functions
    calculate_death_statistics(yearly_deaths, grouped_causes)
    plot_death_charts(yearly_deaths)
    plot_causes(grouped_causes, plot_type='top', num_causes=10)
    plot_causes(grouped_causes, plot_type='lowest', num_causes=10)
    plot_top_causes_years(data_frame, 2011, 2020, gender='Male', num_causes=10)
    plot_top_causes_years(data_frame, 2011, 2020, gender='Female', num_causes=10)
    plot_male_female_deaths_proportion(data_frame)
    plot_population_vs_deaths(data_frame, population_2011, deaths_2011, population_2020, deaths_2020)

if __name__ == '__main__':
    main()
