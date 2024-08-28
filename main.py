import pandas as pd
from datetime import datetime,time

# Load the data from the "Match Dump Sheet" sheet
file_path = "Excel File Path"
match_data = pd.read_excel(file_path, sheet_name='Match Dump Sheet')


def calculate_trp_priority(row):
    # Assign weights based on provided priority parameters
    
    # 1. Series Type
    if row['Series Type'] == 'World Cup':
        series_type_weight = 1
    else:
        series_type_weight = 2

    # 2. Rivalry
    if row['Rivalry'] == 'India vs Pakistan':
        rivalry_weight = 1
    elif row['Rivalry'] == 'Ashes - England vs Australia':
        rivalry_weight = 2
    else:
        rivalry_weight = 3

    # 3. Status (Assuming Match Type: Live, Upcoming, Completed etc.)
    league_event = row['League/Event']
    if isinstance(league_event, str) and 'Live' in league_event:
        status_weight = 1
    elif isinstance(league_event, str) and 'Upcoming' in league_event:
        status_weight = 2
    elif isinstance(league_event, str) and 'Completed' in league_event:
        status_weight = 3
    else:
        status_weight = 4  # Assuming default for other statuses


    # 4. Teams (considering both Team A and Team B)
    team_weights = {'India': 1, 'England': 2, 'Australia': 3, 'South Africa': 4,
                    'Pakistan': 5, 'New Zealand': 6, 'Sri Lanka': 7, 'West Indies': 8,
                    'Afghanistan': 9, 'Others': 10}
    
    team_a_weight = team_weights.get(row['Team A'], 10)
    team_b_weight = team_weights.get(row['Team B'], 10)
    team_weight = min(team_a_weight, team_b_weight)  # Consider the higher priority team

    # 5. Time (IST) - Start Time
    time_ranges = {'1700-2030': 1, '1200-1700': 2, '2030-2300': 3,
                   '0900-1200': 4, '2300-0100': 5, '0100-0600': 6, '0600-0900': 7}
    
    # Convert time to string for matching
    if pd.notna(row['Time (IST)']) and isinstance(row['Time (IST)'], pd.Timestamp):
        start_time = row['Time (IST)'].strftime('%H:%M')
        time_weight = 7  # Default weight
        for time_range, weight in time_ranges.items():
            start_hour, end_hour = time_range.split('-')
            if start_hour <= start_time <= end_hour:
                time_weight = weight
                break
    else:
        time_weight = 7  # Default weight if time is not valid

    # 6. Match Category
    match_category_weight = 1 if row['Match Category'] == 'International' else 2

    # 7. Format
    format_weights = {'T20I': 1, 'ODI': 2, 'Test': 3}
    format_weight = format_weights.get(row['Match Type'], 3)

    # 8. Is League (Yes=1, No=2)
    league_weight = 1 if isinstance(league_event, str) and 'League' in league_event else 2
    # 9. Number of Teams in Series
    teams_weight = row['No. of Teams'] if not pd.isna(row['No. of Teams']) else 1

    # 10. Gender
    gender_weight = 1 if row['Gender'] == 'Men' else 2

    # Calculate the total TRP priority
    total_trp = (series_type_weight + rivalry_weight + status_weight + team_weight +
                 time_weight + match_category_weight + format_weight +
                 league_weight + teams_weight + gender_weight)

    return total_trp

# Apply the TRP calculation function to each row
match_data['TRP Priority'] = match_data.apply(calculate_trp_priority, axis=1)

# Display the updated dataframe with TRP Priority
print(match_data[['Match No.', 'Team A', 'Team B', 'TRP Priority']].head())
