import time
import pandas as pd
import numpy as np
from datetime import timedelta

#added comment for git project section 3B - second submission


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
    city = ''
    month = 'all'
    day = 'all'
    months_d = {'january': 1, 'february': 2, 'march': 3, 'april': 4,'may': 5, 'june': 6}

    days_d = { 'monday':0, 'tuesday':1,'wednesday':2,'thursday':3,'friday':4,'saturday':5,'sunday':6}

    print('Hello! Let\'s explore some US bikeshare data!')
    # made input variables more user friendly
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while city.lower() not in ['chicago','new_york_city','washington']:
        user_input = input('Please choose a city to analyze. Would you like to explore Chicago (chi), New York (nyc), or Washington DC (wdc)?\n')
        if (user_input.lower() in ['chicago','chi']):
            city = 'chicago'
        elif (user_input.lower() in ['new york','nyc','new york city']):
            city = 'new_york_city'
        elif (user_input.lower() in ['washington','wdc','washington dc']):
            city = 'washington'
        else:
            print('Something went wrong. City not found, please try again\n')

    user_input_time_window,user_input_month,user_input_day= '','',''

    # get user input for month (all, january, february, ... , june)

    while user_input_time_window.lower() not in ['month', 'day', 'none']:

        user_input_time_window= input('\nWould you like to filter the data by month, day,'
                            ' or not at all? Type "none" for no time filter.\n')
        if user_input_time_window.lower() not in ['month', 'day', 'none']:
            print('Something went wrong. Choice invalid, please try again\n')

    if user_input_time_window.lower() == 'none':
        month = 'all'
        day = 'all'

    elif user_input_time_window  == 'month':
        while user_input_month.lower() not in months_d.keys():
            user_input_month = input('\nPlease enter the month you wist to examine..January, February, March, April, May, or June?\n')
            if user_input_month.lower() not in months_d.keys():
                print('Something went wrong. Choice invalid, please try again\n')
            else:
                month = months_d[user_input_month.lower()]



    # get user input for day of week (all, monday, tuesday, ... sunday)
    else:
        while user_input_day.lower() not in days_d.keys():
            user_input_day = input('\nPlease enter a day of the week (Sunday, Monday, ...)\n')
            if user_input_day.lower() not in days_d.keys():
                print('Something went wrong. Choice invalid, please try again\n')
            else: day = days_d[user_input_day.lower()]

    print('-'*40)

    return city +'.csv', month, day



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
    errors = 0
    # make sure input file loads
    try:
        df = pd.read_csv(city)
    except:
        print('Please check the {} file for errors. An error occurred'. format(city))
        errors += 1

    if errors == False:

        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['day_of_week'] = pd.to_datetime(df['Start Time']).dt.dayofweek
        df['month'] = pd.to_datetime(df['Start Time']).dt.month
        if day != 'all':
             df = df[df['day_of_week'] == day]
        if month != 'all':
            df = df[df['month'] == month]


    else:
        df = 'error'
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""


    print('\nCalculating The Most Frequent Times of Travel...\n')

    start_time = time.time()

    df['hour'] = df['Start Time'].dt.hour
    df['day_of_week'] = pd.to_datetime(df['Start Time']).dt.dayofweek
    df['dayname']= pd.to_datetime(df['Start Time']).dt.weekday_name
    df['month'] = pd.to_datetime(df['Start Time']).dt.month
    df['monthname'] = pd.to_datetime(df['Start Time']).dt.month_name()

    # display the most common month
    print('Most common month: ', df['monthname'].mode()[0])

    # display the most common day of week
    print('Most common day of week: ', df['dayname'].mode()[0])

    # display the most common start hour
    print('Most common start hour: ', df['hour'].mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    df['src_dest'] = df['Start Station'] + ' to ' + df['End Station']
    # display most commonly used start station
    print('Most common start station: ', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('Most common end station: ', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    print('Most common trip: ', df['src_dest'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print ('Total travel time: ', str(timedelta(seconds = int(df['Trip Duration'].sum()))))


    # display mean travel time
    print ('Mean travel time: ', str(timedelta(seconds = int(df['Trip Duration'].mean()))))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User breakdown:\n')
    usertype = df.groupby('User Type',as_index=False).count()
    for x in range(len(usertype)):
        print('{}: {}'.format(usertype['User Type'][x], usertype['Start Time'][x]))
    # not all CSV have Gender or Birthyear
    # Display counts of gender
    if 'Gender' in df:
        print('\nGender breakdown:\n')
        gendertype = df.groupby('Gender',as_index=False).count()
        for x in range(len(gendertype)):
            print('{}: {}'.format(gendertype['Gender'][x], gendertype['Start Time'][x]))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print('\nUser birth year stats:\n')
        print('Earliest year of birth: {}'.format(int(df['Birth Year'].min())))
        print('Most recent year of birth: {}'.format(int(df['Birth Year'].max())))
        print('Most common year of birth: {}'.format(int(df['Birth Year'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def raw_dump(df):
    choice = ''
    more =''
    start = 0
    end = 5
    non_raw = ['day_of_week','month','hour','dayname','monthname','src_dest']
    #drop added columns from raw data
    for name in non_raw:
        df.drop(name,axis=1,inplace=True)

    # reset index in case df was filtered

    df = df.reset_index(drop=True)

    while choice.lower() not in ['yes','no','y','n']:
        choice = input('Would you like to view raw data from this set? (yes, no)\n')
        if (choice.lower() in ['yes','y']):
            print(df.iloc[start:end])

            while more not in ['yes','y']:
                more = input('Would you like to view more records? (yes, no)\n')
                if (more in ['yes','y']):
                    start += 5
                    end += 5
                    print(df.iloc[start:end])
                    more = ''

                elif (more.lower() in ['no','n']):
                    print('Thanks for analyzing bike share data')
                    break
                else:
                    print('Option not recognized, please try again\n')
        elif (choice.lower() in ['no','n']):
            print('Thanks for analyzing bike share data')
            break
        else:
            print('Option not recognized, please try again\n')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_dump(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() not in ['yes','y']:
            break


if __name__ == "__main__":
	main()
