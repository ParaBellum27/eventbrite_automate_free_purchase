# Eventbrite Auto-Register

Automates Eventbrite registration for time-sensitive free events.

## Setup

### Prerequisites
- Python 3.7+
- Google Chrome browser
- ChromeDriver

### Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/eventbrite-auto-register.git
cd eventbrite-auto-register
```

2. Install dependencies:
```bash
pip3 install -r requirements.txt
```

3. Install ChromeDriver:
```bash
# macOS
brew install chromedriver

```

## Usage

1. **Log into Eventbrite** in your browser with your account

2. **Navigate to the event page** and proceed to checkout:
   - Click "Get tickets"
   - Select quantity (1 ticket)
   - Click "Check out"
   - **STOP** when you see the form (First Name, Last Name, Email)

3. **Run the script**:
```bash
python3 eventbrite_auto.py
```

4. **Press ENTER** when prompted (after you're on the checkout page)

5. Script will automatically:
   - Fill in First Name: Grace
   - Fill in Last Name: Hoverman
   - Fill in Email: pg2576@stern.nyu.edu
   - Click "Place Order"

## Configuration

To change the registration details, edit these lines in `eventbrite_auto.py`:
```python
first_name.send_keys("First")          # Change first name
last_name.send_keys("Last")        # Change last name
email.send_keys("pg2576@stern.nyu.edu") # Change email
```

## Troubleshooting

### "chromedriver not found"
Install ChromeDriver using the instructions above.

### "Element not found"
The Eventbrite page structure may have changed. Update the element selectors in the script.

### Script runs but doesn't fill fields
Make sure you're on the **checkout page** (not the ticket selection page) before pressing ENTER.

## Legal

This script is for personal use only. Ensure you comply with Eventbrite's Terms of Service.