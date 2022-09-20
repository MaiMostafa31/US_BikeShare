import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }
def validate_day(day):
    """
    validates if day entered is a valid week day
    """

    days =  ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    if day in days:
        return True
    else:
        return False

def validate_month(month):
    """
    validates if month entered is a valid month in the dataset
    """
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    if month in months:
        return True
    else:
        return False


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (str) filter - type of filter to apply
    """

    # print hello message for the user
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while(True):
        city = input("Please choose a city (Chicago, New York, Washington): ")
        city = city.lower()
        if city in CITY_DATA.keys():
            break
        else:
            print("That was an in correct city. please choose again.")

    # getting the user to choose what filters to apply
    while(True):
        choice = input("would you like to filter data by month, day, both or none? ")
        choice = choice.lower()
        if choice == "month" or choice == "day" or choice == "both" or choice == "none":
            filter = choice
            break
        else:
            print("That was an in correct choice. please choose again.")

    # get user input for month (all, january, february, ... , june)
    if choice == "month":
        while(True):
            month = input("Please choose a month: January, February, March, April, May, June: ")
            month = month.lower()
            if validate_month(month):
                day = 'all'
                break
            else:
                print("That was an in correct month. please choose again.")
            

    # get user input for day of week
    if choice == "day":
        while(True):
            day = input("Please choose a day: Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday: ")
            day = day.title()
            if validate_day(day):
                month = 'all'
                break
            else:
                print("That was an in correct day. please choose again.")
    # get user input for both month and day
    if choice == 'both':
        while(True):
            month = input("Please choose a month: January, February, March, April, May, June: ")
            month = month.lower()
            day = input("Please choose a day: Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday: ")
            day = day.title()
            if validate_month(month) and validate_day(day):
                filter = "both month and day "
                break
            else:
                print("This was an incorrect input.")

    if choice == "none":
        month = "all"
        day = "all"


    print('-'*100)
    return city, month, day,filter


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
    df = pd.read_csv(CITY_DATA[city],index_col= [0])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    date =  df['Start Time'].dt
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] =date.strftime('%A')

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df,filter):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...filtering by {}\n'.format(filter))
    start_time = time.time()

    # display the most common month
    if filter == "day" or filter == "none":
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        common_month = months[df['month'].mode()[0]-1].title()
        print('The most common month:',common_month)

    # display the most common day of week
    if filter == "month" or filter == "none":
        common_day = df['day_of_week'].mode()[0]
        print('The most common day:',common_day)

    # display the most common start hour
    common_hour = df['Start Time'].dt.hour.mode()[0]
    print('The most common start hour:',common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)


def station_stats(df,filter):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...filtering by {}\n'.format(filter))
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print("The most commonly used start station:",common_start)

    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print("The most commonly used end station:",common_end)

    # display most frequent combination of start station and end station trip
    common_combination = (df['Start Station'] +" to "+ df['End Station']).mode()[0]
    print("The most frequent combination of start station and end station trip:",common_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)


def trip_duration_stats(df,filter):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...filtering by {}\n'.format(filter))
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print("The total travel time:",total_travel)


    # display mean travel time
    avg_travel = df['Trip Duration'].mean()
    print("The average travel time:",avg_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)


def user_stats(df,filter):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...filtering by {}\n'.format(filter))
    start_time = time.time()

    # Display counts of user types
    print("User Types:")
    user_types = dict(df['User Type'].value_counts())
    for type,count in user_types.items():
        print(type,': ',count)

    # Display counts of gender
    print("\ncounts of gender:")
    try:
        gender_count = dict(df['Gender'].value_counts())
        for gender,count in gender_count.items():
            print(gender,': ',count)
    except:
        print("No Gender info!")

    # Display earliest, most recent, and most common year of birth
    print("\nOldest, youngest and most popular year of birth:")
    try:
        print("Earliest year of birth:",int(df['Birth Year'].min()))
        print("Most recent year of birth:",int(df['Birth Year'].max()))
        print("Most popular year of birth:",int(df['Birth Year'].mode()[0]))

    except:
        print("No Birth Year Data to show!")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)

def display_data(df):
    """Displays raw data upon request by the user in an interactive manner in batches of 5 rows."""
    while True:
        choice = input("Do you want to display individual trip data? Enter yes or no: ").lower()
        if choice == 'yes' or choice == 'no':
            break
        else:
            print("Invalid input. Please type yes or no.")
    if choice == 'yes':
        start = 0
        end = start + 5
        while len(df.index) >= end and choice == 'yes':
            print(df.iloc[start:end])
            start += 5
            end = start+5
            while True:
                choice  = input("Do you want to display more individual trip data? Enter yes or no: ").lower()
                if choice == 'yes' or choice == 'no':
                    break
                else:
                    print("Invalid input. Please type yes or no.")
        if start <len(df.index)> end and choice == 'yes':
            print(df.iloc[start:])
            print("You reached rnd of data. No more data to show.")




def main():
    while True:
        city, month, day, filter = get_filters()
        df = load_data(city, month, day)

        time_stats(df,filter)
        station_stats(df,filter)
        trip_duration_stats(df,filter)
        user_stats(df,filter)
        display_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
