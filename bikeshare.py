import time
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = str(input('\nWould you like to see data for:\nChicago\nNew York City\nWashington\n')).strip().lower()
        if city.replace(" ", "_") not in ('new_york_city', 'chicago', 'washington'):
            print ('\nThat is not a valid answer')
        else:
            break
    # get user input for month (all, january, february, ... , june)

    while True:
        month = str(input('\nWould you like to filter your results based on a month?\nYou can select between:\nJanuary\nFebruary\nMarch\nApril\nMay\nJune\nIf no filtering is desired enter "all"\n')).strip().lower()
        if month not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
            print ('\nThat is not a valid month')
        else:
            break


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = str(input('\nWould you like to filter your results based on a day?\nIf no filtering is desired enter "all"\n')).strip().lower()
        if day not in ('all','monday','tuesday','wednesday','thursday','friday','saturday','sunday'):
            print('\nThat is not a valid day')
        else:
            break

    print('-'*40)
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

    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    index = int(df['Start Time'].dt.month.mode())
    popular_month = months[index - 1]
    print('The most popular month is {}'.format(popular_month))

    # display the most common day of week
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                    'Saturday', 'Sunday']
    index = int(df['Start Time'].dt.dayofweek.mode())
    popular_day = days[index]
    print('The most popular day is {}'.format(popular_day))

    # display the most common start hour
    popular_hour = int(df['Start Time'].dt.hour.mode())
    popular_hour_24 = str(popular_hour) + ':' + '00'
    time_readable = time.strptime(popular_hour_24,"%H:%M")
    popular_hour = time.strftime("%I:%M %p",time_readable)

    print('The most popular hour is {}'.format(popular_hour))

    print('\nThis took %s seconds' % round((time.time() - start_time),2))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode().describe()["top"]

    # display most commonly used end station
    end_station = df['End Station'].mode().describe()["top"]

    # display most frequent combination of start station and end station trip
    combination_station = df['Start Station'].astype(str) + " to " + df['End Station'].astype(str)
    most_frequent = combination_station.describe()["top"]
    most_frequent_count = combination_station.describe()["freq"]
    print ('The most commonly used start station is "{}"\nThe most commonly used end station is "{}"\nThe most frequent trip is "{}" with {} counts'.format(start_station,end_station,most_frequent,most_frequent_count))

    print("\nThis took %s seconds." % round((time.time() - start_time),2))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = int(df['Trip Duration'].sum())

    # display mean travel time
    mean_travel = int(df['Trip Duration'].mean())

    print('The total traveled time is {}\nThe average travel time is {}'.format(display_time(total_travel),display_time(mean_travel)))

    print("\nThis took %s seconds" % round((time.time() - start_time),2))
    print('-'*40)

def display_time(seconds):
    """Helper method to turn seconds into redable time.
       Args:
            (int) seconds
        Returns:
            (list) redable time
    """
    #set time parameters according to their respective seconds
    parameters = (
    ('year(s)', 29030400),
    ('month(s)',2419200),
    ('week(s)', 604800),
    ('day(s)', 86400),
    ('hour(s)', 3600),
    ('minute(s)', 60),
    ('second(s)', 1)
    )

    result = []
    # calculate and merge timeframe
    for name, count in parameters:
        value = seconds // count
        if value:
            seconds -= value * count
            result.append("{} {}".format(value, name))
    return( ', '.join(result))

def user_stats(df):

    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()

    # Display counts of gender

    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
    else:
        gender_counts = 'No Gender statistics for this city.'


    # Display earliest, most recent, and most common year of birth

    if 'Birth Year' in df.columns:
        min_year = int(df['Birth Year'].min())
        max_year = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode())
    else:
        min_year = 'No Birth Year statistics for this city.'
        max_year = 'No Birth Year statistics for this city.'
        common_year = 'No Birth Year statistics for this city.'

    print('User Types:\n{}\n\nGender Counts:\n{}\n\nEarliest Birth Year: {}\nMost recet Birth Year: {}\nMost common Birth Year: {}\n'.format(user_types,gender_counts,min_year,max_year,common_year))

    print("\nThis took %s seconds." % round((time.time() - start_time),2))
    print('-'*40)

def  additional_stats(df):
    """Depending on the user's raw input, we will display 5 additional lines from the dataframe
       Then, we will prompt the user to decide if they want to continue seeing additiona data
    """
    #helper method to validate if user wants to view more data or not
    def available(valid):
        if valid.strip().lower() in ('yes','no'):
            return True
        else:
            return False
    #set counter for rows
    first = 0
    last = 5
    answer = False
    #check user's response
    while answer == False:
        valid = input('Display additional data?\nPlease enter "yes" or "no"\n')
        answer = available(valid)
        if answer == True:
            break
        else:
            print('That is not a valid answer.\nPlease enter "yes" or "no"\n')
    #print 5 rows of data
    if valid.strip().lower() == 'yes':
        print(df[df.columns].iloc[first:last])
        #check if user wants to see additional data
        valid_2 = ''
        while valid_2.strip().lower() != 'no':
                 answer_2 = False
                 while answer_2 == False:
                    valid_2 = input('Display additional data?\nPlease enter "yes" or "no"\n')
                    answer_2 = available(valid_2)
                    if answer_2 == True:
                        break
                    else:
                        print('That is not a valid answer.\nPlease enter "yes" or "no"\n')
                 #print 5 more rows
                 if valid_2.strip().lower() == 'yes':
                    first += 5
                    last += 5
                    print(df[df.columns].iloc[first:last])
                 elif valid_2.strip().lower() == 'no':
                    break


def restart():
    '''Helper method to validate if the program should
        continue or break

        Returns:
            False if answer is no, re-runs program if answer is yes, otherwise prompts the user to re-input answer
    '''
    user_input = str(input('\nWould you like to restart? Please enter "yes" or "no"\n'))
    if user_input.strip().lower() not in ('yes','no') :
            print('That is not a valid answer')
            restart()
    elif user_input.strip().lower() == 'yes':
        main()
    elif user_input.strip().lower() == 'no':
        return False


def main():
    '''Calculates and prints out the  statistics about a city
       and time argument input by the user
    '''
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        additional_stats(df)

        if not restart():
            break


if __name__ == "__main__":
	main()
