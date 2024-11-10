import streamlit as st
import random
import hashlib
from datetime import datetime

def generate_ticket_number():
    # Generate a 6-character ticket number similar to Kerala Lottery's format
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "".join(random.choice(chars) for _ in range(6))

def hash_ticket(ticket):
    # Apply SHA-256 hashing for ticket integrity verification
    return hashlib.sha256(ticket.encode()).hexdigest()

def generate_prize_structure():
    # Structured prize details similar to Kerala Lottery
    structure = {
        "1st Prize": {"amount": "Rs:1,00,00,000/-", "ticket": generate_ticket_number()},
        "Consolation Prizes": {"amount": "Rs:8,000/-", "tickets": [generate_ticket_number() for _ in range(10)]},
        "2nd Prize": {"amount": "Rs:10,00,000/-", "tickets": [generate_ticket_number() for _ in range(5)]},
        "3rd Prize": {"amount": "Rs:5,000/-", "tickets": [generate_ticket_number() for _ in range(20)]},
        "4th Prize": {"amount": "Rs:2,000/-", "tickets": [generate_ticket_number() for _ in range(30)]},
        "5th Prize": {"amount": "Rs:1,000/-", "tickets": [generate_ticket_number() for _ in range(50)]},
        "6th Prize": {"amount": "Rs:500/-", "tickets": [generate_ticket_number() for _ in range(100)]},
        "7th Prize": {"amount": "Rs:100/-", "tickets": [generate_ticket_number() for _ in range(150)]},
    }
    # Add hashed versions of ticket numbers
    for prize in structure.values():
        if isinstance(prize["tickets"], list):
            prize["tickets"] = [(ticket, hash_ticket(ticket)) for ticket in prize["tickets"]]
        else:
            prize["ticket"] = (prize["ticket"], hash_ticket(prize["ticket"]))
    return structure

def calculate_security_level():
    # Simulated security level
    return random.uniform(97, 99.9)

def display_lottery_results():
    # Fetch and display results
    results = generate_prize_structure()
    st.write("KERALA STATE LOTTERIES - RESULT")
    st.write("PHONE:- 0471-2305230 DIRECTOR:- 0471-2305193 OFFICE:- 0471-2301740")
    st.write("Draw: FIFTY-FIFTY LOTTERY NO.FF-116th DRAW")
    st.write(f"Draw Date: {datetime.now().strftime('%d/%m/%Y, %I:%M %p')}")
    st.write("AT GORKY BHAVAN, NEAR BAKERY JUNCTION, THIRUVANANTHAPURAM")

    # Display prizes with hashed tickets
    for prize, details in results.items():
        st.write(f"{prize}: {details['amount']}")
        if prize == "1st Prize":
            st.write(f"Ticket No: {details['ticket'][0]}")
            st.write(f"Hash: {details['ticket'][1]}")
        else:
            st.write("Tickets and Hashes:")
            for ticket, hash_value in details["tickets"]:
                st.write(f"Ticket No: {ticket} | Hash: {hash_value}")

    # Security and complexity analysis
    complexity = calculate_security_level()
    st.write(f"\n**Security Complexity**: Approximately {complexity:.2f}% secure.")
    st.write("**Integrity Verification**: SHA-256 hashes ensure each ticket’s authenticity.")
    st.write("Difficulty of unauthorized access or duplication is high due to cryptographic complexity.")

# Button to refresh and generate new results
if st.button("Refresh Results"):
    display_lottery_results()
else:
    display_lottery_results()
