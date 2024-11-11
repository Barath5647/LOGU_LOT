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

def display_kerala_lottery(results):
    """Displays the Kerala Fifty-Fifty Lottery Result in a specified format with spaced tables."""

    # Header Information
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
            st.markdown(" | ".join(numbers))
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
        "3rd Prize: ₹5000 each": 20,
        "4th Prize: ₹2000 each": 18,
        "5th Prize: ₹1000 each": 15,
        "6th Prize: ₹500 each": 12,
        "7th Prize: ₹100 each": 10
    }

    for prize_name, count in prize_structure.items():
        results[prize_name] = generate_prize_list(count)

    # Save the current results with the current date and time
    current_date = datetime.now().strftime('%d-%m-%Y %H:%M')
    save_results_to_file(results, current_date)

    return results

# Schedule weekly result generation every Wednesday at 3:00 pm
def scheduled_task():
    generate_and_save_latest_results()

schedule.every().wednesday.at("15:00").do(scheduled_task)

# Streamlit app execution with sidebar options
st.title("Kerala Fifty-Fifty Lottery Result Generator")

# Sidebar options for refreshing and viewing past results
st.sidebar.write("### Options")
if st.sidebar.button("Refresh Results"):
    latest_results = generate_and_save_latest_results()
else:
    # Load the latest available results if not refreshed
    all_results = load_results_from_file()
    latest_results = all_results[max(all_results.keys())] if all_results else generate_and_save_latest_results()

# Display the latest results by default
st.write("### Latest Result")
display_kerala_lottery(latest_results)

# Past results search option
st.sidebar.write("### View Past Results")
selected_date = st.sidebar.text_input("Enter the date (dd-mm-yyyy HH:MM) to view past results:")

# Dropdown menu for past results selection
all_results = load_results_from_file()
if all_results:
    date_options = sorted(all_results.keys(), reverse=True)
    selected_date_dropdown = st.sidebar.selectbox("Or select from available dates:", date_options)

    # If user selects a date from the dropdown or enters a date manually
    if selected_date or selected_date_dropdown:
        date_to_show = selected_date if selected_date else selected_date_dropdown
        past_results = load_results_from_file(date_to_show)
        if past_results:
            st.write(f"### Results for {date_to_show}")
            display_kerala_lottery(past_results)
        else:
            st.write("No results found for the specified date.")
else:
    st.sidebar.write("No past results available.")

# Running scheduled tasks continuously in the background
while True:
    schedule.run_pending()
    time.sleep(1)
