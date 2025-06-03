import streamlit as st
import pandas as pd
import requests

# Define a function to fetch real-time player data from the API (mocked for now)
def fetch_player_data():
    # API URL for MLB (replace with real API URL or service)
    api_url = "https://mockapi.com/players"

    # Make a request to fetch data
    response = requests.get(api_url)

    # For the purposes of this example, we will mock the response data
    if response.status_code == 200:
        player_data = response.json()
        players = []
        for player in player_data['players']:
            players.append({
                "name": player['name'],
                "avg": player['avg'],  # Batting average
                "obp": player['obp'],  # On-base percentage
                "exit_velocity": player['exit_velocity'],  # Exit velocity (hard hit data)
                "woba": player['woba'],  # Weighted On-Base Average
                "babip": player['babip'],  # Batting Average on Balls In Play
                "barrel_percentage": player['barrel_percentage'],  # Barrel % for hard hit balls
                "era": player['era'],  # ERA of the pitcher for matchups
                "whip": player['whip'],  # Walks + Hits per Inning Pitched for the pitcher
                "pitcher_matchup": player['pitcher_matchup']  # Matchup against specific pitcher
            })
        return players
    else:
        # Return some mock data in case the API call fails
        return [{"name": "Error", "avg": 0.0, "obp": 0.0, "exit_velocity": 0, "woba": 0.0, "babip": 0.0, "barrel_percentage": 0.0, "era": 0.0, "whip": 0.0, "pitcher_matchup": "None"}]

# Function to calculate hit chance based on player stats
def calculate_hit_chance(player_data):
    # Example formula for calculating hit chance based on advanced stats
    hit_chance = (player_data["avg"] + player_data["obp"] + player_data["woba"] + player_data["babip"]) / 4
    
    # Add Exit Velocity and Barrel Percentage into the calculation (weight it slightly higher)
    hit_chance += (player_data["exit_velocity"] * 0.1) + (player_data["barrel_percentage"] * 0.2)

    # Subtract a bit if the pitcher matchup is bad (whip and era can factor into this)
    if player_data["whip"] > 1.5 or player_data["era"] > 4.50:
        hit_chance -= 0.05  # Reduce hit chance for tough pitchers

    # Return the final hit chance between 0 and 1 (scale it if needed)
    return min(max(hit_chance, 0), 1)

# Streamlit setup
st.set_page_config(page_title="MLB Beat the Streak", page_icon="⚾", layout="wide")
st.title("MLB Beat the Streak - Player Hit Chance")

# Fetch real-time player data
players = fetch_player_data()

# If the data was successfully fetched, calculate hit chances
for player in players:
    player["hit_chance"] = calculate_hit_chance(player)

# Create a dataframe to display the player data
df = pd.DataFrame(players)

# Display the dataframe
st.dataframe(df)

# Optional: You can display individual player data if needed
st.subheader("Player Hit Chances")
for player in players:
    st.write(f"**{player['name']}** - Hit Chance: {player['hit_chance'] * 100:.2f}%")
