import streamlit as st
import random

def generate_numbers(count, digits=4):
    """Generate a list of unique random lottery numbers with a specified digit length."""
    numbers = set()
    while len(numbers) < count:
        number = str(random.randint(10**(digits-1), 10**digits - 1)).zfill(digits)
        numbers.add(number)
    return sorted(numbers)

# Streamlit app layout
st.title("LOGU_LOT - RESULT")
st.subheader("www.examplelottery.com  |  PHONE: 1234-567890  |  EMAIL: info@examplelottery.com")
st.text("DRAW held on: 10/11/2024, 3:00 PM\nAT MAIN OFFICE, CITY CENTER, THIRUVANANTHAPURAM")

# Displaying 1st Prize
st.header("1st Prize Rs: 10,000,000/-")
st.write(f"1) {generate_numbers(1)[0]} (THIRUVANANTHAPURAM)")

# Consolation Prize
st.header("Consolation Prize Rs: 8,000/-")
consolation_numbers = generate_numbers(10)
st.write(" ".join(consolation_numbers))

# Displaying 2nd Prize
st.header("2nd Prize Rs: 1,000,000/-")
st.write(f"1) {generate_numbers(1)[0]} (KOCHI)")

# Displaying multiple prizes with 100 numbers each
for prize, amount in zip(["3rd", "4th", "5th", "6th", "7th"], ["5000", "2000", "1000", "500", "100"]):
    st.header(f"{prize} Prize Rs: {amount}/-")
    prize_numbers = generate_numbers(100)
    for i in range(0, len(prize_numbers), 10):
        st.write(" ".join(prize_numbers[i:i+10]))

# Footer with instructions
st.text("""
The prize winners are advised to verify the winning numbers with the results published in the official government Gazette 
and surrender the winning tickets within 30 days. 

Next LOGU_LOT Draw will be held on 17/11/2024 at MAIN OFFICE, CITY CENTER, THIRUVANANTHAPURAM
This is a digitally signed document. Authenticity may be verified through https://examplelottery.com
""")
