# Timestamp Analysis Application

## Overview
The Timestamp Analysis Application is a Streamlit-based web application designed to analyze timestamp data fetched from a MySQL database. This data records the number of times push-ups were done each day. The application provides insights such as monthly counts, average monthly counts, dates with the highest count, frequency with user input, days with frequency, and hourly frequency.

## Setup
1. **Clone the Repository**: 
    ```
    git clone <repository_url>
    ```
2. **Install Dependencies**: Install the required Python packages using pip.
    ```
    pip install -r requirements.txt
    ```
3. **Database Configuration**:
    - Ensure you have a MySQL database set up.
    - Create a `.env` file in the root directory of the project and provide the necessary environment variables:
        ```
        DB_HOST=your_database_host
        DB_USER=your_database_user
        DB_PASSWORD=your_database_password
        DB_DATABASE=your_database_name
        ```

## Features
- **Data Visualization**: The application provides visualizations such as bar plots to represent monthly counts, average monthly counts, hourly frequency, and days of the week with frequency.
- **Downloadable CSV**: Users can download the fetched data in CSV format for further analysis.
- **Insights**:
    - **Monthly Counts**: Displays the total number of entries for each month and year.
    - **Average Monthly Counts**: Shows the average count for each month along with the highest frequency month.
    - **Date with Highest Count**: Identifies the date(s) with the highest number of entries.
    - **Frequency with User Input**: Allows users to input a frequency and displays dates with that frequency.
    - **Days with Frequency**: Presents a table and bar plot depicting the frequency of each day of the week.
    - **Hourly Frequency**: Analyzes the frequency of activities performed during each hour section of the day, along with the hour section(s) with the highest frequency.
- **Sidebar Overview**: Provides a sidebar with an overview of the application and relevant links to other related apps.

## Run
Run the application using the following command:
```bash
streamlit run app.py
```
or
```bash
python -m streamlit run app.py
```


