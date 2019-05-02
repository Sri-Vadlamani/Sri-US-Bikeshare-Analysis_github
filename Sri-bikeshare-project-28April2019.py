import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

CITIES = {'chicago', 'new york', 'washington'}

def get_user_input(message, list):
    """
    An utility function to obtain user specific input value

    Args:
        (str) message -  message for a particular request
        (str) list - list of data either months or day of week
    Returns:
        (str) user_data - requested data from user
    """

    while True:
        user_data = input(message).lower()
        if user_data in list:
            break
        elif user_data == 'all':
            break
        else:
            print("Invalid data:Please choose from the list")
    return user_data

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('.............Hello! Let\'s explore some US bikeshare data!.....................')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
       city = input('Which city do you want to explore Chicago, New York or Washington? \n> ').lower()
       if city not in CITIES:
           print("Invalid data:Please choose from the list")
       else:
           break


    # get user input for month (all, january, february, ... , june)
    month = get_user_input('Provide us a month name or "all" to apply no month filter. \n(e.g. all, january, february, march, april, may, june) \n> ',
                            ['january', 'february', 'march', 'april', 'may', 'june'])


    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_user_input('Provide the week day or "all"to apply no day filter. \n(e.g. all, monday - sunday) \n> ',
                        ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday' ])

    print('-'*80)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week and hour from Start Time to add new columns to dataframe
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month to create new dataframe
    if month != 'all':
        MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
        month =  MONTHS.index(month) + 1
        df = df[ df['month'] == month ]

    # filter by day of week to create new dataframe
    if day != 'all':
        df = df[ df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\n........................Calculating The Most Frequent Times of Travel.................\n')
    start_time = time.time()

    # display the most common month
    m = df.month.mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    most_common_month = months[m - 1].capitalize()
    print("The most common month is :", most_common_month)

    # display the most common day of week
    most_common_day_of_week = df['day_of_week'].value_counts().idxmax()
    print("The most common day of week is :", most_common_day_of_week)

    # display the most common hour of day
    most_common_start_hour = df.hour.mode()[0]
    print("The most common hour of day is :", most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\n........................Calculating The Most Popular Stations and Trip...............\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].value_counts().idxmax()
    print("The most commonly used start station :", most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].value_counts().idxmax()
    print("The most commonly used end station :", most_common_end_station)

    # display most frequent combination of start station and end station trip
    most_common_start_end_station = df[['Start Station', 'End Station']].groupby(['Start Station', 'End Station']).size().nlargest(1)
    print("The most frequent combination of ", most_common_start_end_station )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\n...........................Calculating Trip Duration........................\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print("Total travel time :", total_travel)

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print("Mean travel time :", mean_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\n.....................Calculating User Stats.......................\n')
    start_time = time.time()

    # Display counts of user types
    user_counts = df['User Type'].value_counts()
    print ("Counts of user types: \n", user_counts)

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print("\nCounts of gender: \n",gender_counts)
    else:
        print("\nCounts of gender: No data provided\n")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = df['Birth Year'].min()
        print("\nThe most earliest year of birth:", earliest_year)
        most_recent = df['Birth Year'].max()
        print("The most recent year of birth:", most_recent)
        most_common_year = df['Birth Year'].value_counts().idxmax()
        print("The most common year of birth:", most_common_year)
    else:
        print("\nDisplay earliest, most recent, and most common year of birth: No data provided\n")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)

def disp_raw_data(df):
    '''
    Displays the raw data used to compute the stats
    Input:
        the df with all the bikeshare data
    Returns:
       none
    '''
    print('\n.....................displaying raw data.......................\n')
    row_index = 0
    view_data = input("\nWould yoy like to see 5 lines of raw data? Please type 'yes' or 'no' \n").lower()
    while True:
        if view_data == 'no':
            break
        if view_data == 'yes':
            print(df[row_index: row_index + 5])
            row_index = row_index + 5
            continue
        view_data = input("\n Would you like to see five more rows of the data ? Please type 'yes' or 'no' \n").lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        disp_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
