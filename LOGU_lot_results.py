import streamlit as st
import secrets
import hashlib
import json
from datetime import datetime, timedelta
import os
import schedule
import time
import numpy as np
import matplotlib.pyplot as plt

def generate_ticket_number():
    return f"{secrets.randbelow(10000):04d}"

def hash_ticket_number(ticket_number, salt=None):
    salt = salt or datetime.now().strftime('%Y%m%d%H%M')
    hashed = hashlib.sha256((ticket_number + salt).encode()).hexdigest().upper()[:6]
    return hashed


def generate_prize_list(count):
    """Generates and sorts a list of unique four-digit ticket numbers for a prize tier."""
    prize_list = set()
    while len(prize_list) < count:
        ticket_number = generate_ticket_number()
        prize_list.add(ticket_number)
    return sorted(prize_list)

def save_results_to_file(results, date):
    """Save generated lottery results to a JSON file with date as the key."""
    if os.path.exists("lottery_results.json"):
        with open("lottery_results.json", "r") as file:
            all_results = json.load(file)
    else:
        all_results = {}

    all_results[date] = results
    with open("lottery_results.json", "w") as file:
        json.dump(all_results, file)

def load_results_from_file(date=None):
    """Load lottery results from a JSON file. If date is provided, returns specific results."""
    if not os.path.exists("lottery_results.json"):
        return {}

    with open("lottery_results.json", "r") as file:
        all_results = json.load(file)
    return all_results if date is None else all_results.get(date, {})

def plot_prize_distribution(results):
    prize_names = list(results.keys())
    prize_counts = [len(prizes) if isinstance(prizes, list) else 1 for prizes in results.values()]

    fig, ax = plt.subplots()
    ax.bar(prize_names, prize_counts, color='skyblue')
    ax.set_xlabel('Prize Tiers')
    ax.set_ylabel('Number of Prizes')
    ax.set_title('Prize Distribution in the Latest Draw')
    st.pyplot(fig)




def display_kerala_lottery(results):
    """Displays the Kerala Fifty-Fifty Lottery Result in a specified format with spaced tables."""
    st.markdown("**KERALA STATE LOTTERIES - RESULT**")
    st.markdown(f"**FIFTY-FIFTY LOTTERY NO.FF-116th DRAW held on:** {datetime.now().strftime('%d/%m/%Y, %I:%M %p')}")
    st.markdown("""
    **AT GORKY BHAVAN, NEAR BAKERY JUNCTION, THIRUVANANTHAPURAM**

    **Phone**: 0471-2305230 | **Director**: 0471-2305193 | **Office**: 0471-2301740 | **Email**: cru.dir.lotteries@kerala.gov.in
    """)

    st.markdown("---")

    # Display Results
    for prize, numbers in results.items():
        if isinstance(numbers, list):
            st.markdown(f"**{prize}**")
            st.markdown(" ".join(numbers))
        else:
            st.markdown(f"**{prize}**: {numbers}")
        st.markdown("---")


def generate_and_save_latest_results():
    """Generates a new batch of lottery results and saves them to the file."""
    results = {}

    # First Prize
    results["1st Prize: ₹1,00,00,000"] = hash_ticket_number(generate_ticket_number())

    # Consolation Prizes
    results["Consolation Prizes: ₹8,000 each"] = [hash_ticket_number(generate_ticket_number()) for _ in range(10)]

    # Lower Prizes with four-digit format
    prize_structure = {
        "2nd Prize: ₹1,00,000 each": 12,
        "3rd Prize: ₹5000 each": 25,
        "4th Prize: ₹2000 each": 18,
        "5th Prize: ₹1000 each": 25,
        "6th Prize: ₹500 each": 30,
        "7th Prize: ₹100 each": 100
    }

    for prize_name, count in prize_structure.items():
        results[prize_name] = generate_prize_list(count)

    # Save the current results with the current date and time
    current_date = datetime.now().strftime('%d-%m-%Y %H:%M')
    save_results_to_file(results, current_date)

    return results
