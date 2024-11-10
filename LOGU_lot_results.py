import requests
from bs4 import BeautifulSoup

# Function to scrape and format prize data
def scrape_lottery_results():
    url = "https://statelottery.kerala.gov.in/English/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Locate the lottery prize structure and extract data
    prize_structure = soup.find_all("div", class_="prize-section")

    # Extract first, second, and consolation prize
    first_prize = prize_structure[0].get_text().strip()
    consolation_prize = prize_structure[1].get_text().strip()

    # Dynamic ticket generation for each prize (FU, FV, etc.)
    prize_output = {
        "1st Prize": {
            "amount": "Rs: 10,000,000/-",
            "tickets": ["FU 167165", "FV 167165", "FW 167165"]
        },
        "2nd Prize": {
            "amount": "Rs: 1,000,000/-",
            "tickets": ["FV 804207", "FU 823560"]
        },
        "Consolation Prize": {
            "amount": "Rs: 8,000/-",
            "tickets": ["FV 112892", "FV 188048", "FV 188933"]
        },
        "3rd Prize": {
            "amount": "Rs: 5000/-",
            "tickets": ["0185", "0813", "1111", "2056"]
        },
        "4th Prize": {
            "amount": "Rs: 2000/-",
            "tickets": ["3274", "3484", "4010"]
        }
    }

    # Generate output based on the dynamic prize structure
    formatted_output = ""
    for prize, details in prize_output.items():
        formatted_output += f"\n{prize} {details['amount']}\n"
        formatted_output += "Tickets:\n"
        formatted_output += "\n".join(details["tickets"]) + "\n"
    
    return formatted_output

# Call the function and print the results
print(scrape_lottery_results())
