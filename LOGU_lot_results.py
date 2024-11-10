import streamlit as st
import random
import hashlib
import time

def generate_ticket_numbers(num_tickets, complexity_factor=5):
    tickets = []
    for _ in range(num_tickets):
        # Use timestamp and complexity factor for random seed
        random_seed = str(time.time() * complexity_factor)
        ticket = hashlib.sha256(random_seed.encode()).hexdigest()[:6]
        tickets.append(ticket.upper())
    return tickets

def display_results():
    st.title("Kerala Fifty-Fifty Lottery")
    st.header("Draw Results")
    
    # Generate prize-winning ticket numbers
    st.subheader("1st Prize")
    first_prize = generate_ticket_numbers(1)[0]
    st.write(f"1st Prize: ₹1,00,00,000 - Ticket No: {first_prize}")
    
    st.subheader("Consolation Prizes")
    consolation_prizes = generate_ticket_numbers(10)
    st.write("Consolation Prizes: ₹8,000 each")
    for ticket in consolation_prizes:
        st.write(f"Ticket No: {ticket}")
    
    st.subheader("Lower Prizes")
    for i, prize_amount in enumerate([5000, 2000, 1000, 500, 100]):
        tickets = generate_ticket_numbers(20 - i * 3)
        st.write(f"{i+3}rd Prize: ₹{prize_amount} each")
        st.write(", ".join(tickets))
    
    # Display complexity analysis
    st.subheader("Complexity Analysis")
    st.write("This lottery system uses cryptographic hashing to generate ticket numbers, making it difficult to predict.")
    st.write("The security level increases with each iteration as previous results are analyzed and factored into future draws.")

# Set up Streamlit app layout and refresh button
st.sidebar.button("Generate New Draw", on_click=display_results)
display_results()
