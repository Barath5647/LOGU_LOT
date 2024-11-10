import streamlit as st
import random

def generate_numbers(count, digits=6):
    """Generate a list of unique random lottery numbers with a specified digit length."""
    numbers = set()
    while len(numbers) < count:
        number = str(random.randint(100000, 999999))  # Ensures numbers are 6 digits
        numbers.add(number)
    return sorted(numbers)

# Streamlit app layout
st.title("KERALA STATE LOTTERIES - RESULT")
st.subheader("www.statelottery.kerala.gov.in | PHONE: 0471-2305230 | EMAIL: cru.dir.lotteries@kerala.gov.in")
st.text("FIFTY-FIFTY LOTTERY NO.FF-116th DRAW held on: 06/11/2024, 3:00 PM\nAT GORKY BHAVAN, NEAR BAKERY JUNCTION, THIRUVANANTHAPURAM")

# Displaying 1st Prize
st.header("1st Prize Rs: 10,000,000/-")
st.write(f"1) FU {generate_numbers(1)[0]} (ERNAKULAM)")

# Consolation Prize
st.header("Consolation Prize Rs: 8,000/-")
consolation_numbers = generate_numbers(10)
st.write(" ".join([f"FV {num}" for num in consolation_numbers]))

# Displaying 2nd Prize
st.header("2nd Prize Rs: 1,000,000/-")
st.write(f"1) FN {generate_numbers(1)[0]} (KOCHI)")

# Displaying multiple prizes with 100 numbers each
prizes = [("3rd", "5000"), ("4th", "2000"), ("5th", "1000"), ("6th", "500"), ("7th", "100")]
for prize, amount in prizes:
    st.header(f"{prize} Prize Rs: {amount}/-")
    prize_numbers = generate_numbers(100)
    for i in range(0, len(prize_numbers), 10):
        st.write(" ".join([f"FN {num}" for num in prize_numbers[i:i+10]]))

# Footer with instructions
st.text("""
The prize winners are advised to verify the winning numbers with the results published in the Kerala Government Gazette and surrender the winning tickets within 30 days.

Next FIFTY-FIFTY Draw will be held on 13/11/2024 at GORKY BHAVAN, NEAR BAKERY JUNCTION, THIRUVANANTHAPURAM.
This is a digitally signed document. Authenticity may be verified through https://statelottery.kerala.gov.in/
""")
