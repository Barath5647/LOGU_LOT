import streamlit as st
import random
import hashlib
import json
from datetime import datetime, timedelta
import os
import schedule
import time

def generate_ticket_number():
    """Generates a unique, randomized, four-digit ticket number."""
    number = random.randint(0, 9999)
    return f"{number:04d}"

def hash_ticket_number(ticket_number):
    """Hashes ticket number for cryptographic unpredictability."""
    hashed = hashlib.sha256(ticket_number.encode()).hexdigest().upper()[:6]
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

def display_kerala_lottery():
    """Displays the Kerala Fifty-Fifty Lottery Result in a specified format with spaced tables."""

    # Header Information
    st.markdown("**KERALA STATE LOTTERIES - RESULT**")
    st.markdown(f"**FIFTY-FIFTY LOTTERY NO.FF-116th DRAW held on:** {datetime.now().strftime('%d/%m/%Y, %I:%M %p')}")
    st.markdown("""
    **AT GORKY BHAVAN, NEAR BAKERY JUNCTION, THIRUVANANTHAPURAM**

    **Phone**: 0471-2305230 | **Director**: 0471-2305193 | **Office**: 0471-2301740 | **Email**: cru.dir.lotteries@kerala.gov.in
    """)

    st.markdown("---")

    # Generate Results
    results = {}

    # First Prize
    st.markdown("**1st Prize: ₹1,00,00,000**")
    first_prize = hash_ticket_number(generate_ticket_number())
    st.markdown(f"Ticket No: {first_prize}")
    results["1st Prize"] = first_prize

    st.markdown("---")

    # Consolation Prizes
    st.markdown("**Consolation Prizes: ₹8,000 each**")
    consolation_prizes = [hash_ticket_number(generate_ticket_number()) for _ in range(10)]
    st.markdown(" | ".join(consolation_prizes))
    results["Consolation Prizes"] = consolation_prizes

    st.markdown("---")

    # Lower Prizes with four-digit format
    prize_structure = {
        "2nd Prize: ₹1,00,000 each": 12,
        "3rd Prize: ₹5000 each": 20,
        "4th Prize: ₹2000 each": 18,
        "5th Prize: ₹1000 each": 15,
        "6th Prize: ₹500 each": 12,
        "7th Prize: ₹100 each": 10
    }

    for prize_name, count in prize_structure.items():
        st.markdown(f"**{prize_name}**")
        prize_numbers = generate_prize_list(count)
        st.markdown(" | ".join(prize_numbers))
        results[prize_name] = prize_numbers
        st.markdown("---")

    # Save the current results with the current date and time
    save_results_to_file(results, datetime.now().strftime('%d-%m-%Y %H:%M'))

# Schedule weekly result generation every Wednesday at 3:00 pm
def scheduled_task():
    display_kerala_lottery()

schedule.every().wednesday.at("15:00").do(scheduled_task)

# Streamlit app execution with buttons
st.title("Kerala Fifty-Fifty Lottery Result Generator")

if st.button("Refresh Results"):
    display_kerala_lottery()

st.write("### View Past Results")
selected_date = st.text_input("Enter the date (dd-mm-yyyy HH:MM) to view past results:")

if selected_date:
    past_results = load_results_from_file(selected_date)
    if past_results:
        st.write(f"### Results for {selected_date}")
        for prize, numbers in past_results.items():
            if isinstance(numbers, list):
                st.markdown(f"**{prize}**")
                st.markdown(" | ".join(numbers))
            else:
                st.markdown(f"**{prize}**: {numbers}")
    else:
        st.write("No results found for the specified date.")

# Running scheduled tasks continuously in the background
while True:
    schedule.run_pending()
    time.sleep(1)
