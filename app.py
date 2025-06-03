import streamlit as st
import pandas as pd
import requests

# Function to fetch stats and calculate hit chance
def fetch_player_data():
    # Example player data (in practice, you'd fetch this from an API)
    players = [
        {"name": "Player 1", "avg": 0.300, "obp": 0.375, "exit_velocity": 90, "woba": 0.400, "babip": 0.320},
        {"name": "Player 2", "avg": 0.250, "obp": 0.300, "exit_velocity": 85, "woba": 0.320, "babip": 0.290}
    ]
    return players

def calculate_hit_chance(player_data):
    # Simple hit chance model (example)
    return (player_data["avg"] + player_data["obp"] + player_data["woba"] + player_data["babip"]) / 4

# Streamlit setup
st.set_page_config(page_title="MLB Beat the Streak", page_icon="⚾", layout="wide")
st.title("MLB Beat the Streak - Player Hit Chance")

# Fetch player data
players = fetch_player_data()

# Calculate hit chances
for player in players:
    player["hit_chance"] = calculate_hit_chance(player)

# Create a dataframe to display
df = pd.DataFrame(players)

# Display dataframe in the app
st.dataframe(df)
