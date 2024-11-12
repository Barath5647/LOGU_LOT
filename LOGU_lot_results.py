import streamlit as st
import secrets
import hashlib
import json
from datetime import datetime
import os
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

def calculate_crack_time(attempts_per_sec, prize_counts, total_ticket_possibilities):
    total_attempts_needed = total_ticket_possibilities / prize_counts
    time_to_crack = total_attempts_needed / attempts_per_sec
    return round(time_to_crack, 2) if time_to_crack >= 1 else "Less than 1 second"

def calculate_probability(prize_counts, total_ticket_possibilities):
    total_prizes = sum(prize_counts.values())
    return (total_prizes / total_ticket_possibilities) * 100

def display_complexity_analysis(current_results, past_results=None):
    total_ticket_possibilities = 10000
    prize_counts = sum(len(v) if isinstance(v, list) else 1 for v in current_results.values())
    probability_to_win = round((prize_counts / total_ticket_possibilities) * 100, 2)
    
    st.markdown("### Probability Analysis")
    st.markdown(f"**Probability of winning any prize in this draw:** {probability_to_win}%")
    st.markdown("**Difficulty Level:** Hard")

    human_attempts_per_second = 1
    amateur_attempts_per_second = 1000
    expert_attempts_per_second = 100000
    supercomputer_attempts_per_second = 1e9

    st.markdown("**Estimated Time to Crack Each Prize Tier by Different Attackers:**")
    st.write(f"- **Human Alone**: {calculate_crack_time(human_attempts_per_second, prize_counts, total_ticket_possibilities)} seconds")
    st.write(f"- **Amateur with Basic Resources**: {calculate_crack_time(amateur_attempts_per_second, prize_counts, total_ticket_possibilities)} seconds")
    st.write(f"- **Expert with High-End Resources**: {calculate_crack_time(expert_attempts_per_second, prize_counts, total_ticket_possibilities)} seconds")
    st.write(f"- **Supercomputer**: {calculate_crack_time(supercomputer_attempts_per_second, prize_counts, total_ticket_possibilities)} seconds")

    # Plot prize distribution
    plot_prize_distribution(current_results)

    if past_results:
        st.markdown("### Comparative Analysis with Past Results")
        current_prizes_flat = [num for prize, nums in current_results.items() for num in (nums if isinstance(nums, list) else [nums])]
        past_prizes_flat = [num for prize, nums in past_results.items() for num in (nums if isinstance(nums, list) else [nums])]
        
        common_tickets = set(current_prizes_flat).intersection(set(past_prizes_flat))
        unique_current_tickets = len(current_prizes_flat) - len(common_tickets)
        
        st.write(f"**Unique ticket distribution in this draw:** {unique_current_tickets}")
        st.write(f"**Common tickets with past draw:** {len(common_tickets)}")
        
        # Calculate hash variance for current and past results
        current_hash_variance = np.var([int(hashlib.sha256(num.encode()).hexdigest(), 16) for num in current_prizes_flat])
        past_hash_variance = np.var([int(hashlib.sha256(num.encode()).hexdigest(), 16) for num in past_prizes_flat])
        variance_diff = round(abs(current_hash_variance - past_hash_variance), 2)
        
        st.write(f"**Hash variance difference from past results:** {variance_diff}")

        # Plot variance comparison
        fig, ax = plt.subplots()
        ax.bar(["Current Draw", "Past Draw"], [current_hash_variance, past_hash_variance], color=['blue', 'orange'])
        ax.set_ylabel("Hash Variance")
        ax.set_title("Variance Comparison of Current and Past Lottery Results")
        st.pyplot(fig)

def generate_and_save_latest_results():
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

    # Save results with the current date and time
    current_date = datetime.now().strftime('%d-%m-%Y %H:%M')
    save_results_to_file(results, current_date)

    return results

st.title("Kerala Fifty-Fifty Lottery Result Generator")
st.sidebar.write("### Options")

if st.sidebar.button("Refresh Results"):
    latest_results = generate_and_save_latest_results()
else:
    all_results = load_results_from_file()
    latest_results = all_results[max(all_results.keys())] if all_results else generate_and_save_latest_results()

st.write("### Latest Result")
display_complexity_analysis(latest_results, load_results_from_file(max(all_results.keys()) if len(all_results) > 1 else None))
