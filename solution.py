import time
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
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Which city would you like to see data from?\n").lower()
    check = ['chicago','new york city','washington']
    while(city not in check):
        print("You can choose either Chicago, New york city, or Washington ")
        city = input("Enter either Chicago, New York City or Washington\n").lower()
        break
    apply_filter = input('Would you like to filter data by Month, Day, Both, or not at all? Type "all" to apply no filter\n').lower()
    # get user input for month (all, january, february, ... , june)
    if (apply_filter == 'month'):
        month = input("Which Month?. Choose from January, February, March, April, May, June\n").lower()
        day = 'all'
    elif (apply_filter == 'day'):
        day = input("Which Day? Choose from Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday\n").lower()
        month = 'all'
    elif (apply_filter == 'both'):
        month = input("Which Month?. Choose from January, February, March, April, May, June\n").lower()
        day = input("Which Day? Choose from Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday\n").lower()
    else:
        month = 'all'
        day = 'all'

    print('-'*40)
    return city, month, day, apply_filter


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

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['start'] = df['Start Time'].dt.weekday_name

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

def time_stats(df, filter):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['start_hour'] = df['Start Time'].dt.hour

    # display the most common month
    month_key = df['month'].value_counts().keys().tolist()
    month_value = df['month'].value_counts().tolist()
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print("The most common month is:", months[month_key[0] - 1], ",Count:", month_value[0], ",Filter:", filter)

    # display the most common day of week
    day_key = df['day_of_week'].value_counts().keys().tolist()
    day_value = df['day_of_week'].value_counts().tolist()
    print("The most common day of the week is:", day_key[0], ",Count: ", day_value[0], ",Filter:", filter)

    # display the most common start hour
    hour_key = df['start_hour'].value_counts().keys().tolist()
    hour_value = df['start_hour'].value_counts().tolist()
    print("The most common start hour is:", hour_key[0], ",Count:", hour_value[0], ",Filter:", filter)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df, filter):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    df['popular_route'] = df['Start Station'] + " - " + df['End Station']

    # display most commonly used start station
    start_stn_key = df['Start Station'].value_counts().keys().tolist()
    start_stn_value = df['Start Station'].value_counts().tolist()
    print("The most commonly used start station is:",start_stn_key[0], "Count:", start_stn_value[0], ",Filter:", filter)
    # display most commonly used end station
    end_stn_key = df['End Station'].value_counts().keys().tolist()
    end_stn_value = df['End Station'].value_counts().tolist()
    print("The most commonly used end station is:",end_stn_key[0], "Count:", end_stn_value[0], ",Filter:", filter)

    # display most frequent combination of start station and end station trip
    pop_rte_key = df['popular_route'].value_counts().keys().tolist()
    pop_rte_value = df['popular_route'].value_counts().tolist()
    print("The most popular train route is:",pop_rte_key[0], "Count:", pop_rte_value[0], ",Filter:", filter)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, filter):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total = df['Trip Duration'].sum()
    print("Total trip duration is {} seconds".format(float(total)))

    # display mean travel time
    mean = df['Trip Duration'].mean()
    print("Mean travel duration is {} seconds".format(float(mean)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, filter):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print(user_type, filter)

    # Display counts of gender
    try:
        gender_count=df['User Type'].value_counts()
        print("Here are the counts of gender: {}".format(gender_count))
    except Execption as e:
        print('Can not calculate the amount and gender of users, as an Error occurred: {}'.format(e))

    # Display earliest, most recent, and most common year of birth
    #earliest year of birth
    try:
        min_year=int(df['Birth Year'].min())
        print("Earliest birth year is: {}".format(str(min_year)))

    #recent year of birth
        max_year=int(df['Birth Year'].max())
        print("Recent birth year is: {}".format(str(max_year)))

    # common birth year
        common_year=int(df['Birth Year'].mode().values[0])
        print("Common birth year is: {}".format(str(common_year)))
    except Exception as e:
        print('Couldn\'t calculate the age structure of our customers, as an Error occurred: {}'.format(e)) 

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day, filter = get_filters()
        df = load_data(city, month, day)
        time_stats(df, filter)
        station_stats(df, filter)
        trip_duration_stats(df, filter)
        user_stats(df, filter)
        raw_data = input('\n Would you like to see the raw data? Enter yes or no.\n')
        if raw_data.lower() == 'yes':
            while True:
                print(df.head(5))
                further = input('\n Would you like to see more rows of the dataser? Enter yes or no.\n')
                if further.lower() != 'yes':
                    break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
