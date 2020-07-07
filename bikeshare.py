import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
week_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('\n\t\tHello! Let\'s explore some US bikeshare files!\n'.center(60))

    info()
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = get_city(CITY_DATA)

    # get user input for month (all, january, february, ... , june)
    month = get_month(months)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_day(week_days)

    print('=' * 60)
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
    start_time = time.time()

    # load data file into a data frame
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'], errors='coerce')

    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month  # range (1-12)
    df['day_of_week'] = df['Start Time'].dt.dayofweek  # range (0-6)
    df['hour'] = df['Start Time'].dt.hour  # range (0-23)

    total_rides = len(df)

    # filter by month
    if month != 'all':
        month_index = months.index(month) + 1
        # filter by month to create the new data frame
        df = df[df.month == month_index]
        month = month.title()

    # filter by day of week
    if day != 'all':
        day_index = week_days.index(day)

        # filter by day of week to create the new data frame
        df = df[df.day_of_week == day_index]
        day = day.title()

    print(f"\n[This took {round((time.time() - start_time), 3)} seconds.]".rjust(50))

    infos(city.title(), month, day, total_rides, df)

    return df


def time_stats(df):
    """ Displays statistics on the most frequent times of travel. """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month = months[df['month'].mode()[0] - 1].title()
    print(f"\tThe most common month: {month}".ljust(80))

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    common_day = week_days[common_day].title()
    print(f"\tThe most common day of the week: {common_day}")

    # display the most common start hour
    hour = hour_12_format(df['hour'].mode()[0])
    print(f"\tThe most common start hour: {hour}")

    print(f"[\nThis took {round((time.time() - start_time), 3)} seconds.]".rjust(30))
    print('=' * 60)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]

    print(f"\tThe most commonly used start station: {start_station}".ljust(80))

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]

    print(f"The most commonly used end station: {end_station}".ljust(80))

    # display most frequent combination of start station and end station trip
    start_end_combination = df.groupby(['Start Station', 'End Station'])
    most_freq_trip_count = start_end_combination['Trip Duration'].count().max()
    most_freq_trip = start_end_combination['Trip Duration'].count().idxmax()

    print(f"The most frequent street combination: {most_freq_trip[0]}, {most_freq_trip[1]}".ljust(80))
    print(f"We have a total of : {most_freq_trip_count} trips".ljust(80))

    print(f"\n[This took {round((time.time() - start_time), 3)} seconds.]".rjust(50))
    print('=' * 60)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = int(df['Trip Duration'].sum())
    print(f"\tTotal travel time: {total_travel_time} seconds")
    print(f"\tTotal travel time in HMS: {seconds_to_HMS_str(total_travel_time)}")

    # display mean travel time
    mean_travel_time = int(df['Trip Duration'].mean())
    print(f"The Mean travel time: {mean_travel_time} seconds")
    print(f"The mean travel time in to HMS: {seconds_to_HMS_str(mean_travel_time)}")

    print(f"\n[This took {round((time.time() - start_time), 3)} seconds.]".rjust(50))
    print('=' * 60)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    for index in range(len(user_types)):
        value = user_types[index]
        user_type = user_types.index[index]
        print(f"\t{user_type + ':'} {value}".ljust(80))

    # Display counts of gender
    if 'Gender' in df.columns:
        genders = df['Gender'].value_counts()
        for index in range(len(genders)):
            value = genders[index]
            gender = genders.index[index]
            print(f"\t{gender + ':'} {value}".ljust(80))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print(f"Earliest Year of Birth: {int(df['Birth Year'].min())}".ljust(80))
        print(f"Most recent Year of Birth: {int(df['Birth Year'].max())}".ljust(80))
        print(f"Most common Year of Birth: {int(df['Birth Year'].mode())}".ljust(80))

    print(f"\n[This took {round((time.time() - start_time), 3)} seconds.]".rjust(50))
    print('=' * 60)


def trip_data(df):
    """
    Asks if the user would like to see some lines of data from the filtered dataset.
    Displays 5 (show_rows) lines, then asks if they would like to see 5 more.
    Continues asking until they say stop.
    """

    start_time = time.time()
    rows = 5
    start = 0
    end = rows - 1

    print('\n\tWould you like to see some data from the current dataset?'.ljust(80))
    while True:
        response = input("Enter y or n: ")
        if response.lower() == 'y':
            print(f"\n\tDisplaying rows {start + 1} to {end + 1}".ljust(80))
            print('\n', df.iloc[start:end + 1])
            start += rows
            end += rows
            print('=' * 60)
            print(f"\t\n Would you like to see the next {rows} rows")
            continue
        else:
            break

    print(f"\n[This took {round((time.time() - start_time), 3)} seconds.]".rjust(50))
    print('=' * 60)


def get_city(city_data):
    """ This function returns the name of the city to be analysed, chose by the user."""
    list_of_cities = []
    num = 0
    for city in city_data:
        list_of_cities.append(city)
    # Request the user to choose a city to be analysed by entering the corresponding number in the menu above.
    while True:
        city_name = input("\n Enter the name of the city: ").lower()

        if city_name in list_of_cities:
            break

    chosen_city = city_name
    return chosen_city


def get_month(mon):
    """ This function returns the month chosen by the user for analysis """
    month = ''
    while True:
        month_name = input(" Enter the name of the month or enter all:  ").lower()
        if month_name in mon:
            break
    
    month = month_name

    return month


def get_day(days_of_week):
    """ This function returns the day chosen by the user for analysis """
    day = None
    while True:
        day_name = input(" Enter the name of the day or or enter all:  ").lower()
        day = ''
        if day_name == 'all':
            day = day_name
            break
        elif day_name in days_of_week:
            day = day_name
            break
        else:
            continue

    return day


def infos(city, month, day, total_rides, df):
    """ This functions displays some basic information about the dataset of the chosen city. """
    start_time = time.time()

    total_rides = len(df)
    number_of_start_stations = len(df['Start Station'].unique())
    number_of_end_stations = len(df['End Station'].unique())

    print(f"\tStatistics for {city} dataset".ljust(80))
    print(f"\tFiltering the {city} for {month}, {day}".ljust(80))
    print(f"\tTotal number of rides in {city} dataset: {total_rides} rides".ljust(80))
    print(f"\tThe number of starting stations: {number_of_start_stations}".ljust(80))
    print(f"\tThe number of end stations: {number_of_end_stations}".ljust(80))

    print(f"[\nThis took {round((time.time() - start_time), 3)} seconds.]".rjust(30))
    print('=' * 60)


def hour_12_format(hour):
    """ Converts  24 hour time format to hour format with PM or AM. """

    if hour == 0:
        hour_string = '12 AM'
    elif hour == 12:
        hour_string = '12 PM'
    else:
        hour_string = f'{hour} AM' if hour < 12 else f'{hour - 12} PM'

    return hour_string


def seconds_to_HMS_str(total_seconds):
    """
    Converts number of seconds to human readable string format.

    Args:
        (int) total_seconds - number of seconds to convert
    Returns:
        (str) day_hour_str - number of weeks, days, hours, minutes, and seconds
    """

    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)

    day_hour_string = ''
    if weeks > 0:
        day_hour_string += f'{weeks} weeks, '
    if days > 0:
        day_hour_string += f'{days} days, '
    if hours > 0:
        day_hour_string += f'{hours} hours, '
    if minutes > 0:
        day_hour_string += f'{minutes} minutes, '
    if total_seconds > 59:
        day_hour_string += f'{seconds} seconds'

    return day_hour_string



def info():
    """This function displays the information about the cities to be analysed"""
    print('CITIES'.ljust(30), 'MONTHS'.ljust(30), 'DAYS OF THE WEEK'.ljust(30))
    print('1. Chicago'.ljust(30), '1. January'.ljust(30), '1. Monday'.ljust(30))
    print('2. New york city'.ljust(30), '2. February'.ljust(30), '2. Tuesday'.ljust(30))
    print('3. Washington'.ljust(30), '3. March'.ljust(30), '3. Wednesday'.ljust(30))
    print(' '.ljust(30), '4. April'.ljust(30), '4. Thursday'.ljust(30))
    print(' '.ljust(30), '5. May'.ljust(30), '5. Friday'.ljust(30))
    print(' '.ljust(30), '6. June'.ljust(30), '6. Saturday'.ljust(30))
    print(' '.ljust(30), 'a. all'.ljust(30), '7. Sunday'.ljust(30))
    print(' '.ljust(30), ' '.ljust(30), 'a. all'.ljust(30))


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        trip_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
