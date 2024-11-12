import streamlit as st
import secrets
import hashlib
import json
from datetime import datetime, timedelta
import os
import schedule
import time
import threading
import numpy as np
import matplotlib.pyplot as plt

def generate_ticket_number():
    return f"{secrets.randbelow(10000):04d}"

def hash_ticket_number(ticket_number, salt=None):
    salt = salt or datetime.now().strftime('%Y%m%d%H%M')
    hashed = hashlib.sha256((ticket_number + salt).encode()).hexdigest().upper()[:6]
    return hashed

def generate_prize_list(count):
    prize_list = set()
    while len(prize_list) < count:
        ticket_number = generate_ticket_number()
        prize_list.add(ticket_number)
    return sorted(prize_list)

def save_results_to_file(results, date):
    if os.path.exists("lottery_results.json"):
        with open("lottery_results.json", "r") as file:
            all_results = json.load(file)
    else:
        all_results = {}

    all_results[date] = results
    with open("lottery_results.json", "w") as file:
        json.dump(all_results, file)

def load_results_from_file(date=None):
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
    st.markdown("**KERALA STATE LOTTERIES - RESULT**")
    st.markdown(f"**FIFTY-FIFTY LOTTERY NO.FF-116th DRAW held on:** {datetime.now().strftime('%d/%m/%Y, %I:%M %p')}")
    st.markdown("---")
    for prize, numbers in results.items():
        if isinstance(numbers, list):
            st.markdown(f"**{prize}**")
            st.markdown(" ".join(numbers))
        else:
            st.markdown(f"**{prize}**: {numbers}")
        st.markdown("---")

def generate_and_save_latest_results():
    results = {}
    results["1st Prize: ₹1,00,00,000"] = hash_ticket_number(generate_ticket_number())
    results["Consolation Prizes: ₹8,000 each"] = [hash_ticket_number(generate_ticket_number()) for _ in range(10)]

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

    current_date = datetime.now().strftime('%d-%m-%Y %H:%M')
    save_results_to_file(results, current_date)

    return results

def calculate_probability(ticket_number: int, total_tickets: int, prize_category: str) -> float:
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

def display_complexity_analysis(total_tickets: int, prize_category: str):
    """
    Display a complexity analysis based on the prize category.
    :param total_tickets: The total number of tickets sold
    :param prize_category: The prize category (e.g., '1st', '2nd', etc.)
    """
    # Define valid prize categories and their winning ticket counts
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

    # Get the number of winning tickets for the selected prize category
    winning_tickets_per_draw = prize_distribution[prize_category]

    # Calculate probability
    probability = calculate_probability(0, total_tickets, prize_category)  # ticket_number is not needed for probability
    st.write(f"**Complexity Analysis for {prize_category} Prize:**")
    st.write(f"Probability of winning: {probability * 100:.6f}%")

    # Calculate crack time using the number of winning tickets for that prize category
    crack_time_weeks = calculate_crack_time(total_tickets, winning_tickets_per_draw)
    st.write(f"Estimated Crack Time: {crack_time_weeks:.2f} weeks")

def scheduled_task():
    generate_and_save_latest_results()

schedule.every().wednesday.at("15:00").do(scheduled_task)

def run_scheduled_tasks():
    while True:
        schedule.run_pending()
        time.sleep(1)

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

display_complexity_analysis(1000000, '1st')  # Example of passing correct parameters to the analysis

# Run the scheduled task in a separate thread to avoid blocking Streamlit app
task_thread = threading.Thread(target=run_scheduled_tasks, daemon=True)
task_thread.start()
