import random
import hashlib
import pandas as pd
import streamlit as st

# Prize structure, defined with prize amount, number of prizes, and agent commission rates
prize_structure = {
    "First Prize": {"amount": 10000000, "num_prizes": 1, "agent_commission": 0.1},
    "Second Prize": {"amount": 1000000, "num_prizes": 1, "agent_commission": 0.1},
    "Third Prize": {"amount": 5000, "num_prizes": 24840, "agent_commission": 0.1},
    "Fourth Prize": {"amount": 2000, "num_prizes": 12960, "agent_commission": 0.1},
    "Fifth Prize": {"amount": 1000, "num_prizes": 25920, "agent_commission": 0.1},
    "Sixth Prize": {"amount": 500, "num_prizes": 103680, "agent_commission": 0.1},
    "Seventh Prize": {"amount": 100, "num_prizes": 136080, "agent_commission": 0.1},
    "Consolation Prize": {"amount": 8000, "num_prizes": 11, "agent_commission": 0.1}
}

# Total ticket pool
total_tickets = 1080000

# Function to generate secure hash for ticket numbers (for tamper-proofing)
def generate_ticket_hash(ticket_number):
    return hashlib.sha256(str(ticket_number).encode()).hexdigest()

# Function to draw unique winning numbers securely for each prize category
def draw_winning_numbers(num_draws, ticket_range):
    winning_numbers = set()
    while len(winning_numbers) < num_draws:
        winning_number = random.randint(1, ticket_range)
        hashed_number = generate_ticket_hash(winning_number)
        winning_numbers.add(hashed_number)
    return list(winning_numbers)

# Function to generate the prize distribution and calculate agent commissions
def generate_prize_distribution():
    prize_results = []
    for prize, details in prize_structure.items():
        prize_amount = details['amount']
        num_prizes = details['num_prizes']
        agent_commission = prize_amount * details['agent_commission']
        
        # Draw winning ticket numbers for each prize tier
        winning_numbers = draw_winning_numbers(num_prizes, total_tickets)
        
        # Append prize details for each winning ticket
        for ticket_hash in winning_numbers:
            prize_results.append({
                "Prize Category": prize,
                "Prize Amount": prize_amount,
                "Ticket Hash": ticket_hash,
                "Agent Commission": agent_commission
            })
    return pd.DataFrame(prize_results)

# Generate the prize distribution DataFrame
prize_distribution = generate_prize_distribution()

# Display the lottery results and statistics using Streamlit
st.title("Kerala Fifty-Fifty Weekly Lottery Results")
st.markdown("**Prize Structure and Results**")
st.write(prize_distribution)

# Calculate total prize amount and agent commission
total_prize_amount = prize_distribution["Prize Amount"].sum()
total_agent_commission = prize_distribution["Agent Commission"].sum()
st.markdown(f"**Total Prize Amount:** Rs. {total_prize_amount:,}")
st.markdown(f"**Total Agent Commission:** Rs. {total_agent_commission:,}")

# Provide a secure ticket hash validation tool for users to check if their ticket won
st.markdown("**Secure Ticket Hash Validation**")
ticket_input = st.text_input("Enter Ticket Number to Verify", "")
if ticket_input:
    ticket_hash = generate_ticket_hash(ticket_input)
    if ticket_hash in prize_distribution['Ticket Hash'].values:
        st.success("Congratulations! This ticket is a winner.")
    else:
        st.error("Sorry, this ticket did not win.")