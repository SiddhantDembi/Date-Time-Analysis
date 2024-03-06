import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import webbrowser
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection details
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DATABASE = os.getenv("DB_DATABASE")

# Function to connect to MySQL database and fetch data
def fetch_data(data_type):
    try:
        # Establish connection to MySQL database
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_DATABASE
        )
        cursor = conn.cursor()
        
        # Determine the table name based on the data type selected by the user
        table_name = "raw_data_id" if data_type == "Raw Data" else "data_id"
        
        # Construct the query to fetch data from the specified table
        query = f"SELECT * FROM {table_name}"
        
        # Execute the query
        cursor.execute(query)
        
        # Fetch all rows from the result
        rows = cursor.fetchall()
        
        if not rows:
            st.error("No data fetched from the MySQL database.")
            return None
        
        # Get column names from cursor description
        columns = [desc[0] for desc in cursor.description]
        
        # Create DataFrame from fetched rows and column names
        df = pd.DataFrame(rows, columns=columns)
        
        # Close cursor and connection
        cursor.close()
        conn.close()
        
        return df
    except mysql.connector.Error as e:
        st.error(f"MySQL Error: {e}")
        return None
    except Exception as e:
        st.error(f"Error fetching data from MySQL database: {e}")
        return None

def main():
    # Sidebar with overview
    st.sidebar.button("Data Cleaner App", on_click=lambda: webbrowser.open_new_tab("https://datacleaner.streamlit.app/"))
    st.sidebar.button("Timestamp App", on_click=lambda: webbrowser.open_new_tab("https://timestamp.streamlit.app/"))
    st.sidebar.title("Overview")
    st.sidebar.write("This application analyzes timestamp data fetched from a MySQL database. The data collected has been cleaned using Data Cleaner app mentioned at the top.")
    st.sidebar.write("The data collection process began on October 26, 2019, and is ongoing. This data records the number of times push-ups were done each day.")
    st.sidebar.write("The cleaned data does not include data from October 2019, August 2023, and September 2023 due to miscalculations during that period. Raw data contains all available data.")
    st.sidebar.write("Raw data and cleaned data are separated to ensure accuracy during analysis.")
    st.sidebar.write("The application provides insights such as monthly counts, average monthly counts, date with the highest count, frequency with user input, days with frequency, and hourly frequency.")
    

    
    st.title("Timestamp Analysis")
    
    # Radio buttons for selecting data type
    data_type = st.radio("Select data type:", ("Cleaned Data","Raw Data"))
    st.write("-" * 30)
    
    # Fetch data from MySQL database based on the selected data type
    df = fetch_data(data_type)
    
    if df is not None:
        st.write("### All the data in table:")
        st.write(df)
        total_rows(df)
        
        # Create a button to download the CSV file
        csv_file = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv_file,
            file_name='data.csv',
            mime='text/csv'
        )
    st.write("-" * 30)
    
    display_insights(df)

def total_rows(df):
    if df is not None:
        num_rows = len(df)
        st.write(f"Total number of entries: {num_rows}")

def display_insights(df):
    if df is not None:
        display_monthly_counts(df)
        display_avg_monthly_counts(df)
        display_date_with_highest_count(df)
        display_frequency_with_user_input(df)
        display_days_with_frequency(df)
        display_hourly_frequency(df)
    
def display_monthly_counts(df):
    if df is not None:
        # Extract Month_Year column
        df['Month_Year'] = pd.to_datetime(df['Date']).dt.to_period('M')
        
        # Count occurrences of each Month_Year
        monthly_counts = df['Month_Year'].value_counts().sort_index()
        
        # Print the total number of rows for each month and year
        st.write("Total number of entries for each month and year:")
        st.write(monthly_counts)
        
        # Plot monthly counts
        plt.figure(figsize=(10, 6))
        monthly_counts.plot(kind='bar')
        plt.title('Total Number of Entries for Each Month and Year')
        plt.xlabel('Month and Year')
        plt.ylabel('Number of Entries')
        st.pyplot(plt)
        st.write("-" * 30)
    
def display_avg_monthly_counts(df):
    if df is not None:
        # Extract Month_Year column
        df['Month_Year'] = pd.to_datetime(df['Date']).dt.to_period('M')
        
        # Group by month and count occurrences of each Month_Year
        monthly_counts = df['Month_Year'].value_counts().sort_index()
        
        # Calculate average count for each month
        monthly_avg = monthly_counts.groupby(monthly_counts.index.strftime('%B')).mean()
        
        # Define the order of months
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                       'July', 'August', 'September', 'October', 'November', 'December']
        
        # Convert index to CategoricalIndex with specified order
        monthly_avg.index = pd.CategoricalIndex(monthly_avg.index, categories=month_order, ordered=True)
        
        # Sort the index
        monthly_avg = monthly_avg.sort_index()
        
        # Create a DataFrame to store the average counts
        avg_monthly_df = pd.DataFrame({'Month': monthly_avg.index, 'Average Count': monthly_avg.values})
        
        # Display the average counts in a table without index
        st.write("Average count for each month:")
        st.table(avg_monthly_df)
        
        # Generate bar plot
        plt.figure(figsize=(10, 6))
        plt.bar(avg_monthly_df['Month'], avg_monthly_df['Average Count'])
        plt.title('Average Count for Each Month')
        plt.xlabel('Month')
        plt.ylabel('Average Count')
        plt.xticks(rotation=45, ha='right')
        st.pyplot(plt)
        
        # Display the highest frequency month at the bottom
        st.write(f"Highest frequency month: {monthly_avg.idxmax()} ({monthly_avg.max():.2f})")
        st.write("-" * 30)

def display_date_with_highest_count(df):
    if df is not None:
        # Convert 'Date' column to datetime format
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Group by date and count occurrences
        date_counts = df['Date'].value_counts()
        
        # Find the maximum count
        max_count = date_counts.max()
        
        # Filter dates with the maximum count
        dates_with_max_count = date_counts[date_counts == max_count]
        
        # Display the dates with the highest number of rows in a table
        st.write("Date(s) with the highest number of entries:")
        dates_with_max_count_df = pd.DataFrame({'Date': dates_with_max_count.index, 'Count': dates_with_max_count.values})
        dates_with_max_count_df['Date'] = dates_with_max_count_df['Date'].dt.strftime('%Y-%m-%d')
        st.table(dates_with_max_count_df)
        
        st.write("-" * 30)

def display_frequency_with_user_input(df):
    if df is not None:
        # Count the occurrences of each date
        date_counts = df['Date'].value_counts()

        # Get the unique frequencies of dates
        unique_counts = sorted(date_counts.unique())

        # Convert frequencies to strings
        unique_counts_str = [str(count) for count in unique_counts]

        # Print the possible frequencies of dates
        st.write("Possible frequencies are:")
        st.write(", ".join(unique_counts_str))

        # Set the default value for user input to the highest frequency
        default_value = max(unique_counts) if unique_counts else 1

        # Take user input for frequency to display
        user_input = st.number_input("Enter the frequency you want to see:", min_value=min(unique_counts), max_value=max(unique_counts), value=default_value)

        # Display dates with the entered frequency
        if user_input in unique_counts:
            dates_with_frequency = date_counts[date_counts == user_input]
            if not dates_with_frequency.empty:
                st.write(f"Dates with frequency {user_input}:")
                # Display total count of the selected frequency
                total_count = dates_with_frequency.sum()
                st.write("Total count: ", str(total_count/user_input))
                for date in dates_with_frequency.index:
                    st.write(date.strftime("%d %B %Y"))
            else:
                st.write(f"No dates found with frequency {user_input}")
        else:
            st.error("Frequency not found in the dataset. Please enter a valid frequency.")

        st.write("-" * 30)

def display_days_with_frequency(df):
    # Convert 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'])

    # Define the order of days of the week
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Count the occurrences of each day of the week
    day_of_week_counts = df['Date'].dt.day_name().value_counts().reindex(day_order)
    
    # Create a DataFrame with the 'day of the week' column name
    day_of_week_counts_df = pd.DataFrame({'Days': day_of_week_counts.index, 'Frequency': day_of_week_counts.values})
    
    # Print the days of the week and their frequencies
    st.write("Days of the week and their frequencies:")
    st.table(day_of_week_counts_df)
    
    # Plot days with frequency
    plt.figure(figsize=(10, 6))
    plt.bar(day_of_week_counts.index, day_of_week_counts.values)
    plt.title('Days of the Week and Their Frequencies')
    plt.xlabel('Day of the Week')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)
    st.pyplot(plt)
    
    # Find the most common and least common days
    most_common_day = day_of_week_counts.idxmax()
    least_common_day = day_of_week_counts.idxmin()
    
    st.write(f"Most common day in the week: {most_common_day}")
    st.write(f"Least common day in the week: {least_common_day}")
    
    # Calculate the chance of doing the task on the most common day
    total_frequency = sum(day_of_week_counts)
    most_common_day_frequency = day_of_week_counts[most_common_day]
    chance_most_common_day = most_common_day_frequency / total_frequency * 100
    st.write(f"Likelihood of doing the task on {most_common_day}: {chance_most_common_day:.2f}%")
    st.write("-" * 30)

def display_hourly_frequency(df):
    # Convert the 'Time' column to datetime format
    df['Time'] = pd.to_datetime(df['Time'], errors='coerce', format='%I:%M %p')

    # Drop rows with missing or invalid times
    df.dropna(subset=['Time'], inplace=True)

    # Initialize a dictionary to store the frequency of each hour section
    hourly_frequency = {}

    # Iterate over each hour from 0 to 23
    for hour in range(0, 24):
        # Define the start and end times for the current hour section
        start_time = pd.to_datetime(f"{hour:02d}:00:00").time()
        end_time = pd.to_datetime(f"{hour:02d}:59:59").time()

        # Filter the dataframe to include only times within the current hour section
        filtered_df = df[(df['Time'].dt.time >= start_time) & (df['Time'].dt.time <= end_time)]

        # Count the number of rows in the filtered dataframe
        frequency = filtered_df.shape[0]

        # Store the frequency of the current hour section
        hourly_frequency[f"{hour:02d}:00 to {hour+1:02d}:00"] = frequency

    # Create a DataFrame from the hourly frequency dictionary
    hourly_frequency_df = pd.DataFrame(hourly_frequency.items(), columns=['Hour Section', 'Frequency'])

    # Print the hourly frequency table
    st.write("Hourly frequency:")
    st.table(hourly_frequency_df)
    
    # Generate a bar plot for hourly frequency
    plt.figure(figsize=(10, 6))
    plt.bar(hourly_frequency.keys(), hourly_frequency.values())
    plt.title('Hourly Frequency')
    plt.xlabel('Hour Section')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(plt)

    # Find the maximum frequency
    max_frequency = max(hourly_frequency.values())

    # Initialize a list to store hour sections with the highest frequency
    highest_frequency_hours = []

    # Iterate through the hourly_frequency dictionary to find hour sections with the maximum frequency
    for hour, frequency in hourly_frequency.items():
        if frequency == max_frequency:
            highest_frequency_hours.append(hour)
    
    # Print the hour section(s) with the highest frequency
    st.write("Hour section(s) with the highest frequency:")
    for hour in highest_frequency_hours:
        st.write(f"{hour} : ({max_frequency})")
    
    # Calculate the chance of doing the task during the hour section with the highest frequency
    total_frequency = sum(hourly_frequency.values())
    chance = max_frequency / total_frequency * 100
    st.write(f"Chance of doing the task during {hour}: {chance:.2f}%")
    st.write("-" * 30)

if __name__ == "__main__":
    main()
