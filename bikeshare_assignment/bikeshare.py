"""
Program name: bikeshare.py
Author: Kam Ming TAM (kamming.b.tam@leidos.com)
Date: 13 April 2020

Program description
    This program computes a variety of descriptive statistics used for bike share in Chicago, New York City, 
    Washington, gost city (dummy non-existed data file)

Version
    v1 - Original submission
    v2 - Second submission, modify the program as below 
        1. Recieve answers from user, and convert them to lower case.
        2. Offer option for user to see 5 rows of raw data, once a time.
    v3 - Update a line for Github Project

Inputs
    User inputs - city name, month, day of week
    File inputs - chicago.csv, new_york_city.csv, washington.csv, no_such_file.csv(non-ecisted file)

Outputs
1 Popular times of travel 
    most common month
    most common day of week
    most common hour of day
2 Popular stations and trip
    most common start station
    most common end station
    most common trip from start to end 
3 Trip duration
    total travel time
    average travel time
4 User info
    counts of each user type
    counts of each gender (only available for NYC and Chicago)
    earliest, most recent, most common year of birth (only available for NYC and Chicago)

Existing bugs
    Not found

"""
import time
import pandas as pd
import numpy as np
import os as os

# The 'ghost city' does not exist in the directory, which is used to demonstrate missing file handling
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv',
              'ghost city': 'no_such_file.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('='*60)
    print('\nHello! Let\'s explore some US bikeshare data!\n')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Please specify the name of city [chicago] [new york city] [washington] [ghost city]: ")
    city = city.lower()
    while city not in ["chicago", "new york city", "washington", "ghost city"]:
        print("You have just entered \"{}\"".format(city))
        print("Please enter the name of city again [chicago] [new york city] [washington] [ghost city]: ")
        print("    or [exit] to terminate the program\n")
        city = input("    Name of city: ")
        city = city.lower()
        if city == "exit":
            print("Bye, have a nice day! ")
            quit()
    print("\n")

    # TO DO: get user input for month (all, january, february, ... , june)
    month = input("Please specify the month [all] [january] [february] [march] [april] [may] [june]: ")
    month = month.lower()
    while month not in ["all", "january", "february", "march", "april", "may", "june"]:
        print("You have just entered \"{}\"".format(month))
        print("Please enter the month again [january] [february] [march] [april] [may] [june]: ")
        print("    or [all] for all months from janurary to june")
        print("    or [exit] to terminate the program\n")
        month = input("Month: ")
        month = month.lower()
        if month == "exit":
            print("Bye, have a nice day! ")
            quit()
    print("\n")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Please specify the day of week [all] [monday] [tuesday] [wednesday] [thursday] [friday] [saturday] [sunday]: ")
    day = day.lower()
    while day not in ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
        print("You have just entered \"{}\"".format(day))
        print("Please enter the day of week again [monday] [tuesday] [wednesday] [thursday] [friday] [saturday] [sunday]: ")
        print("    or [all] for all days from monday to sunday")
        print("    or [exit] to terminate the program\n")
        day = input("Day of week: ")
        day = day.lower()
        if day == "exit":
            print("Bye, have a nice day! ")
            quit()
    print("\n")
    print('='*60)

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
    if os.path.isfile(CITY_DATA[city]):
        df = pd.read_csv(CITY_DATA[city])
    else:
        print('Sorry this data file is not found in the directory, try other city instead!')
        quit()

    # convert the Start Time column to datetime
    if "Start Time" in (df.columns):
        df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
        df['month'] = df['Start Time'].dt.month
        df['day_of_week'] = df['Start Time'].dt.weekday
        df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # use the index of the day of week list to get the corresponding int
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day) 

        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]
        
    return df

def display_sample_data(df):
    """Displays sample data if the user wants."""
    increment_row = 5
    start_row = 0
    end_row = increment_row
    while True:
        see_sample_data = input('\nWould you like to see 5 rows of sample data? Enter yes or no.\n')
        if see_sample_data.lower() == 'yes':
            print(df.iloc[start_row:end_row])
            start_row += increment_row
            end_row += increment_row
            continue
        elif see_sample_data.lower() == 'no':            
            break
        else:
            print('Sorry, I do not understand your answer.')
            continue
    
    print('-'*60)

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    if "month" in (df.columns):
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        most_common_month = df['month'].mode()
        print('The Most Common Month is         ---> ', months[most_common_month[0]- 1])

    # TO DO: display the most common day of week
    if "day_of_week" in (df.columns):
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'firday', 'saturday', 'sunday']
        most_common_day = df['day_of_week'].mode()
        print('The Most Common Day is           ---> ', days[most_common_day[0]])
 
    # TO DO: display the most common start hour
    if "hour" in (df.columns):
        most_common_start_hour = df['hour'].mode()
        print('The Most Common Start Hour is    ---> ', most_common_start_hour[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    if "Start Station" in (df.columns):
        most_common_start_station = df['Start Station'].mode()
        print('The Most Common Start Station is ---> ', most_common_start_station[0])

    # TO DO: display most commonly used end station
    if "End Station" in (df.columns):
        most_common_end_station = df['End Station'].mode()
        print('The Most Common End Station is   ---> ', most_common_end_station[0])

    # TO DO: display most frequent combination of start station and end station trip
    df['Start End Station'] = df['Start Station'] + ' ==> ' + df['End Station']
    start_end_station = df['Start End Station'].mode()
    print('Common Combination Stations are  ---> ', start_end_station[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    if "Trip Duration" in (df.columns):
        total_travel_time = df['Trip Duration'].sum()
        travel_day = total_travel_time // (24 * 60 * 60)
        mod_travel_day = total_travel_time % (24 * 60 * 60)
        travel_hour = mod_travel_day // (60 * 60)
        mod_travel_hour = mod_travel_day % (60 * 60)
        travel_min = mod_travel_hour // 60
        travel_sec = mod_travel_hour % 60
        print('The Total Travel Time is         --->  {} day, {} hour, {} min, {} sec'.format(int(travel_day), int(travel_hour), int(travel_min), int(travel_sec)))

    # TO DO: display mean travel time
        mean_travel_time = df['Trip Duration'].mean()
        mean_min = mean_travel_time // 60 
        mean_sec = mean_travel_time % 60 
        print('The Mean Travel Time is          --->  {} min, {} sec'.format(int(mean_min), int(mean_sec)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
       
    # TO DO: Display counts of user types
    if "User Type" in (df.columns):
        print('Display counts of user types     --->')
        print(df.groupby(['User Type'])['User Type'].count())

    # TO DO: Display counts of gender
    if "Gender" in (df.columns):
        print('\nDisplay counts of gender         --->')
        print(df.groupby(['Gender'])['Gender'].count())
    
    # TO DO: Display earliest, most recent, and most common year of birth
    if "Birth Year" in (df.columns):
        print('\nThe earliest year of birth       --->', int(df['Birth Year'].min()))
        print('The most recent year of birth    --->', int(df['Birth Year'].max()))
        print('The most common year of birth    --->', int(df['Birth Year'].mode()))
 
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('='*60)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_sample_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

    print('\nThank you for using the bikeshare.py program, Bye!')

if __name__ == "__main__":
    main()
