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

# 1. **Calculate Probability Function**
def calculate_probability(ticket_number: int, total_tickets: int, prize_category: str) -> float:
    """
    Calculate the probability of winning a specific prize category.
    :param ticket_number: The ticket number for which we want to calculate the probability
    :param total_tickets: The total number of tickets sold
    :param prize_category: The prize category (e.g., '1st', '2nd', '3rd', etc.)
    :return: The probability of winning the specified prize
    """
    prize_distribution = {
        '1st': 1,
        '2nd': 1,
        '3rd': 24840,
        '4th': 12360,
        '5th': 25920,
        '6th': 103680,
        '7th': 136080,
        'consolation': 88
    }

    if prize_category not in prize_distribution:
        raise ValueError(f"Invalid prize category: {prize_category}")
    
    prizes = prize_distribution[prize_category]
    probability = prizes / total_tickets
    return probability

# 2. **Calculate Crack Time Function**
def calculate_crack_time(total_tickets: int, winning_tickets_per_draw: int, draws_per_week: int = 1) -> float:
    """
    Estimate how long it would take to win based on draw frequency.
    :param total_tickets: Total number of tickets in the lottery
    :param winning_tickets_per_draw: Number of winning tickets per draw
    :param draws_per_week: Number of draws per week
    :return: The estimated crack time in weeks
    """
    tickets_per_week = winning_tickets_per_draw * draws_per_week
    crack_time_weeks = total_tickets / tickets_per_week
    return crack_time_weeks

# 3. **Display Complexity Analysis**
def display_complexity_analysis(total_tickets: int, prize_category: str):
    """
    Display a complexity analysis based on the prize category.
    :param total_tickets: The total number of tickets sold
    :param prize_category: The prize category (e.g., '1st', '2nd', etc.)
    """
    # Define valid prize categories
    valid_prize_categories = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', 'consolation']
    
    if prize_category not in valid_prize_categories:
        raise ValueError(f"Invalid prize category: {prize_category}")

    probability = calculate_probability(0, total_tickets, prize_category)  # ticket_number is not needed for probability
    print(f"Complexity Analysis for {prize_category} Prize:")
    print(f"Probability of winning: {probability * 100:.6f}%")
    crack_time_weeks = calculate_crack_time(total_tickets, prize_category)
    print(f"Estimated Crack Time: {crack_time_weeks:.2f} weeks")

# 4. **Process Past and Current Results for Ticket Comparison and Hash Variance**
def calculate_hash_variance(current_draw: list, past_draw: list) -> float:
    """
    Calculate the variance of hashes for the current and past draws.
    :param current_draw: The current ticket draw (list of winning numbers)
    :param past_draw: The past ticket draw (list of winning numbers)
    :return: Variance in hash values
    """
    # Create simple hash values for comparison, in this case using sums of ticket numbers.
    current_hash = sum(current_draw) % 1000  # Arbitrary modulus for simplicity
    past_hash = sum(past_draw) % 1000  # Same modulus
    
    variance = np.abs(current_hash - past_hash)
    return variance

def plot_variance_comparison(current_variance: float, past_variance: float):
    """
    Plot a comparison of the current and past variance in hashes.
    :param current_variance: Variance of the current ticket draw
    :param past_variance: Variance of the past ticket draw
    """
    categories = ['Current Draw', 'Past Draw']
    variances = [current_variance, past_variance]
    
    plt.bar(categories, variances, color=['blue', 'orange'])
    plt.title("Variance Comparison of Current and Past Draws")
    plt.ylabel("Variance Value")
    plt.show()


# Schedule weekly result generation every Wednesday at 3:00 pm
def scheduled_task():
    generate_and_save_latest_results()

schedule.every().wednesday.at("15:00").do(scheduled_task)

st.title("Kerala Fifty-Fifty Lottery Result Generator")

st.sidebar.write("### Options")
if st.sidebar.button("Refresh Results"):
    latest_results = generate_and_save_latest_results()
else:
    all_results = load_results_from_file()
    latest_results = all_results[max(all_results.keys())] if all_results else generate_and_save_latest_results()

st.write("### Latest Result")
display_kerala_lottery(latest_results)

available_dates = list(load_results_from_file().keys())
selected_date_from_menu = st.sidebar.selectbox("Select date to view past results", [""] + available_dates)
selected_date_input = st.sidebar.text_input("Or enter the date (dd-mm-yyyy HH:MM):")

past_results = load_results_from_file(selected_date_input or selected_date_from_menu) if selected_date_input or selected_date_from_menu else None
if past_results:
    st.write(f"### Results for {selected_date_input or selected_date_from_menu}")
    display_kerala_lottery(past_results)

display_complexity_analysis(latest_results, past_results)

while True:
    schedule.run_pending()
    time.sleep(1)
