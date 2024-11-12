import random
import hashlib
import streamlit as st
from datetime import datetime

def generate_lottery_results(seed_phrase, date_str):
    """
    Generate Kerala-style lottery results with a cryptographic seed for randomness.

    Parameters:
    - seed_phrase (str): A unique phrase for seeding randomness.
    - date_str (str): The current date to ensure unique results per day.

    Returns:
    - dict: A dictionary containing lists of numbers for each prize tier.
    """
    # Define prize structure and limits
    results = {
        "1st Prize": [], 
        "Consolation Prize": [], 
        "2nd Prize": [], 
        "3rd Prize": []
    }
    prize_limits = {
        "1st Prize": 1, 
        "Consolation Prize": 5, 
        "2nd Prize": 10, 
        "3rd Prize": 20
    }

    # Seed the random generator for consistent, cryptographic randomness
    hash_seed = hashlib.sha256(f"{seed_phrase}{date_str}".encode()).hexdigest()
    random.seed(int(hash_seed, 16))

    # Generate unique numbers for each prize tier
    results["1st Prize"] = [f"{random.randint(100000, 999999)}"]
    results["Consolation Prize"] = sorted([
        f"{random.randint(100000, 999999)}" 
        for _ in range(prize_limits["Consolation Prize"])
    ])
    results["2nd Prize"] = sorted([
        f"{random.randint(1000, 9999)}" 
        for _ in range(prize_limits["2nd Prize"])
    ])
    results["3rd Prize"] = sorted([
        f"{random.randint(1000, 9999)}" 
        for _ in range(prize_limits["3rd Prize"])
    ])
    
    return results

def display_lottery_results(results, date_str):
    """
    Display Kerala-style lottery results in Streamlit format.

    Parameters:
    - results (dict): The generated lottery numbers for each prize tier.
    - date_str (str): Date of the result to display in the header.
    """
    st.title("Kerala State Lotteries - Result")
    st.write(f"Date: {date_str}")
    st.header("Results")
    for prize, numbers in results.items():
        st.subheader(f"{prize}:")
        for num in numbers:
            st.write(num)
        st.write("\n")

# Main execution
if __name__ == "__main__":
    # Set today's date as the lottery date
    date_str = datetime.today().strftime('%Y-%m-%d')
    seed_phrase = "Kerala Fifty-Fifty Lottery"
    
    # Generate and display results
    results = generate_lottery_results(seed_phrase, date_str)
    display_lottery_results(results, date_str)