# import streamlit as st
# import random
# import hashlib
# import json
# from datetime import datetime, timedelta
# import os
# import schedule
# import time

# def generate_ticket_number():
#     """Generates a unique, randomized, four-digit ticket number."""
#     number = random.randint(0, 9999)
#     return f"{number:04d}"

# def hash_ticket_number(ticket_number):
#     """Hashes ticket number for cryptographic unpredictability."""
#     hashed = hashlib.sha256(ticket_number.encode()).hexdigest().upper()[:6]
#     return hashed

# def generate_prize_list(count):
#     """Generates and sorts a list of unique four-digit ticket numbers for a prize tier."""
#     prize_list = set()
#     while len(prize_list) < count:
#         ticket_number = generate_ticket_number()
#         prize_list.add(ticket_number)
#     return sorted(prize_list)

# def save_results_to_file(results, date):
#     """Save generated lottery results to a JSON file with date as the key."""
#     if os.path.exists("lottery_results.json"):
#         with open("lottery_results.json", "r") as file:
#             all_results = json.load(file)
#     else:
#         all_results = {}

#     all_results[date] = results
#     with open("lottery_results.json", "w") as file:
#         json.dump(all_results, file)

# def load_results_from_file(date=None):
#     """Load lottery results from a JSON file. If date is provided, returns specific results."""
#     if not os.path.exists("lottery_results.json"):
#         return {}

#     with open("lottery_results.json", "r") as file:
#         all_results = json.load(file)
#     return all_results if date is None else all_results.get(date, {})

# def display_kerala_lottery(results):
#     """Displays the Kerala Fifty-Fifty Lottery Result in a specified format with spaced tables."""

#     # Header Information
#     st.markdown("**KERALA STATE LOTTERIES - RESULT**")
#     st.markdown(f"**FIFTY-FIFTY LOTTERY NO.FF-116th DRAW held on:** {datetime.now().strftime('%d/%m/%Y, %I:%M %p')}")
#     st.markdown("""
#     **AT GORKY BHAVAN, NEAR BAKERY JUNCTION, THIRUVANANTHAPURAM**

#     **Phone**: 0471-2305230 | **Director**: 0471-2305193 | **Office**: 0471-2301740 | **Email**: cru.dir.lotteries@kerala.gov.in
#     """)

#     st.markdown("---")

#     # Display Results
#     for prize, numbers in results.items():
#         if isinstance(numbers, list):
#             st.markdown(f"**{prize}**")
#             st.markdown(" ".join(numbers))
#         else:
#             st.markdown(f"**{prize}**: {numbers}")
#         st.markdown("---")

# def generate_and_save_latest_results():
#     """Generates a new batch of lottery results and saves them to the file."""
#     results = {}

#     # First Prize
#     results["1st Prize: ₹1,00,00,000"] = hash_ticket_number(generate_ticket_number())

#     # Consolation Prizes
#     results["Consolation Prizes: ₹8,000 each"] = [hash_ticket_number(generate_ticket_number()) for _ in range(10)]

#     # Lower Prizes with four-digit format
#     prize_structure = {
#         "2nd Prize: ₹1,00,000 each": 12,
#         "3rd Prize: ₹5000 each": 25,
#         "4th Prize: ₹2000 each": 18,
#         "5th Prize: ₹1000 each": 25,
#         "6th Prize: ₹500 each": 30,
#         "7th Prize: ₹100 each": 100
#     }

#     for prize_name, count in prize_structure.items():
#         results[prize_name] = generate_prize_list(count)

#     # Save the current results with the current date and time
#     current_date = datetime.now().strftime('%d-%m-%Y %H:%M')
#     save_results_to_file(results, current_date)

#     return results

# # Complexity and Probability Analysis
# def display_complexity_analysis():
#     """Displays the complexity and cracking difficulty analysis at the end of the result."""
#     st.markdown("### Probability Analysis")
#     st.markdown("**Probability of winning any prize:** 0.98%")
#     st.markdown("**Difficulty Level:** Hard")

#     st.markdown("### Complexity Analysis")
#     st.markdown("This system uses cryptographic hashing with SHA-256 to generate ticket numbers, introducing high unpredictability.")
#     st.markdown("**How Hard to Crack:** Approximately 99.999% resilience against pattern recognition attempts.")
#     st.markdown("**Time for Human to Crack:** With manual methods, it would take centuries.")
#     st.markdown("**Time with Resources (e.g., supercomputers):** Decades due to adaptive complexity with historical draw integration.")

# # Schedule weekly result generation every Wednesday at 3:00 pm
# def scheduled_task():
#     generate_and_save_latest_results()

# schedule.every().wednesday.at("15:00").do(scheduled_task)

# # Streamlit app execution with sidebar options
# st.title("Kerala Fifty-Fifty Lottery Result Generator")

# # Sidebar options for refreshing and viewing past results
# st.sidebar.write("### Options")
# if st.sidebar.button("Refresh Results"):
#     latest_results = generate_and_save_latest_results()
# else:
#     # Load the latest available results if not refreshed
#     all_results = load_results_from_file()
#     latest_results = all_results[max(all_results.keys())] if all_results else generate_and_save_latest_results()

# # Display the latest results by default
# st.write("### Latest Result")
# display_kerala_lottery(latest_results)
# display_complexity_analysis()

# # Past results search option
# st.sidebar.write("### View Past Results")
# selected_date = st.sidebar.text_input("Enter the date (dd-mm-yyyy HH:MM) to view past results:")

# if selected_date:
#     past_results = load_results_from_file(selected_date)
#     if past_results:
#         st.write(f"### Results for {selected_date}")
#         display_kerala_lottery(past_results)
#     else:
#         st.write("No results found for the specified date.")

# # Running scheduled tasks continuously in the background
# while True:
#     schedule.run_pending()
#     time.sleep(1)



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

    # In the display function:
    plot_prize_distribution(current_results)

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

# def display_complexity_analysis(current_results, past_results=None):
#     """Real-time complexity analysis for the current lottery results."""
    
#     total_ticket_possibilities = 10000  # Four-digit numbers (0000 to 9999)
#     prize_counts = sum(len(v) if isinstance(v, list) else 1 for v in current_results.values())
#     probability_to_win = round((prize_counts / total_ticket_possibilities) * 100, 2)
    
#     st.markdown("### Probability Analysis")
#     st.markdown(f"**Probability of winning any prize in this draw:** {probability_to_win}%")
#     st.markdown("**Difficulty Level:** Hard")

#     st.markdown("### Complexity Analysis")
#     st.markdown("This system uses cryptographic SHA-256 hashing to enhance unpredictability of each prize-winning ticket.")
    
#     human_attempts_per_second = 1  # Manual
#     amateur_attempts_per_second = 1000
#     expert_attempts_per_second = 100000
#     supercomputer_attempts_per_second = 1e9

#     def calculate_crack_time(attempts_per_sec):
#         total_attempts_needed = total_ticket_possibilities / prize_counts
#         return round(total_attempts_needed / attempts_per_sec, 2)

#     st.markdown("**Estimated Time to Crack Each Prize Tier by Different Attackers:**")
#     st.write(f"- **Human Alone**: {calculate_crack_time(human_attempts_per_second)} seconds")
#     st.write(f"- **Amateur with Basic Resources**: {calculate_crack_time(amateur_attempts_per_second)} seconds")
#     st.write(f"- **Expert with High-End Resources**: {calculate_crack_time(expert_attempts_per_second)} seconds")
#     st.write(f"- **Supercomputer**: {calculate_crack_time(supercomputer_attempts_per_second)} seconds")

def calculate_crack_time(attempts_per_sec, prize_counts, total_ticket_possibilities):
    total_attempts_needed = total_ticket_possibilities / prize_counts
    return round(total_attempts_needed / attempts_per_sec, 2)

def display_complexity_analysis(current_results, past_results=None):
    total_ticket_possibilities = 10000  # Four-digit numbers (0000 to 9999)
    prize_counts = sum(len(v) if isinstance(v, list) else 1 for v in current_results.values())
    probability_to_win = round((prize_counts / total_ticket_possibilities) * 100, 2)
    
    st.markdown("### Probability Analysis")
    st.markdown(f"**Probability of winning any prize in this draw:** {probability_to_win}%")
    st.markdown("**Difficulty Level:** Hard")

    human_attempts_per_second = 1  # Manual
    amateur_attempts_per_second = 1000
    expert_attempts_per_second = 100000
    supercomputer_attempts_per_second = 1e9

    st.markdown("**Estimated Time to Crack Each Prize Tier by Different Attackers:**")
    st.write(f"- **Human Alone**: {calculate_crack_time(human_attempts_per_second, prize_counts, total_ticket_possibilities)} seconds")
    st.write(f"- **Amateur with Basic Resources**: {calculate_crack_time(amateur_attempts_per_second, prize_counts, total_ticket_possibilities)} seconds")
    st.write(f"- **Expert with High-End Resources**: {calculate_crack_time(expert_attempts_per_second, prize_counts, total_ticket_possibilities)} seconds")
    st.write(f"- **Supercomputer**: {calculate_crack_time(supercomputer_attempts_per_second, prize_counts, total_ticket_possibilities)} seconds")

    if past_results:
        st.markdown("### Comparative Analysis with Past Results")
        current_prizes_flat = [num for prize, nums in current_results.items() for num in (nums if isinstance(nums, list) else [nums])]
        past_prizes_flat = [num for prize, nums in past_results.items() for num in (nums if isinstance(nums, list) else [nums])]
        
        common_tickets = set(current_prizes_flat).intersection(set(past_prizes_flat))
        unique_current_tickets = len(current_prizes_flat) - len(common_tickets)
        
        st.write(f"**Unique ticket distribution in this draw:** {unique_current_tickets}")
        st.write(f"**Common tickets with past draw:** {len(common_tickets)}")
        
        current_hash_variance = np.var([int(hashlib.sha256(num.encode()).hexdigest(), 16) for num in current_prizes_flat])
        past_hash_variance = np.var([int(hashlib.sha256(num.encode()).hexdigest(), 16) for num in past_prizes_flat])
        variance_diff = round(abs(current_hash_variance - past_hash_variance), 2)
        
        st.write(f"**Hash variance difference from past results:** {variance_diff}")

        fig, ax = plt.subplots()
        ax.bar(["Current Draw", "Past Draw"], [current_hash_variance, past_hash_variance], color=['blue', 'orange'])
        ax.set_ylabel("Hash Variance")
        ax.set_title("Variance Comparison of Current and Past Lottery Results")
        st.pyplot(fig)

        st.markdown("### Conclusion")
        st.markdown("This analysis indicates that the SHA-256 hashing used for each prize level significantly reduces pattern predictability, with minimal overlap between current and previous results.")

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
