import os
from langsmith import Client
from dotenv import load_dotenv

load_dotenv()
client = Client()

dataset_name = "Email_Assistant_Triage_Golden_Set"

# FULL 101 EMAIL DATASET
emails = [
    # --- RESPOND (34 Examples) ---
    {"input": "Can we meet at 2pm tomorrow?", "output": "respond"},
    {"input": "What is the status of the project report?", "output": "respond"},
    {"input": "I need the budget files by Friday.", "output": "respond"},
    {"input": "Are you available for a quick sync today?", "output": "respond"},
    {"input": "Please send the updated slides.", "output": "respond"},
    {"input": "When is the deadline for milestone 2?", "output": "respond"},
    {"input": "Can you review my code by EOD?", "output": "respond"},
    {"input": "Do you have the link for the Zoom call?", "output": "respond"},
    {"input": "Can we reschedule our 1-on-1?", "output": "respond"},
    {"input": "I have a question about the AI architecture.", "output": "respond"},
    {"input": "Are we still on for lunch at 12?", "output": "respond"},
    {"input": "Can you provide feedback on the proposal?", "output": "respond"},
    {"input": "What time is the team stand-up?", "output": "respond"},
    {"input": "I missed the notes from today's meeting.", "output": "respond"},
    {"input": "Can you share the document link again?", "output": "respond"},
    {"input": "Are you coming to the office today?", "output": "respond"},
    {"input": "I need help with the LangSmith setup.", "output": "respond"},
    {"input": "Could you sign this document by tonight?", "output": "respond"},
    {"input": "What is the Wi-Fi password for the guest network?", "output": "respond"},
    {"input": "Can we move the meeting to 3 PM?", "output": "respond"},
    {"input": "Do you have a template for the report?", "output": "respond"},
    {"input": "Who is the lead for the UI task?", "output": "respond"},
    {"input": "Can you check if the server is up?", "output": "respond"},
    {"input": "Where is the project documentation stored?", "output": "respond"},
    {"input": "Did you receive my last email?", "output": "respond"},
    {"input": "Can you invite Intern-1 to the meeting?", "output": "respond"},
    {"input": "What is the budget for the AI API?", "output": "respond"},
    {"input": "Can you approve my leave request?", "output": "respond"},
    {"input": "Do we have a meeting with the mentor today?", "output": "respond"},
    {"input": "Can you send the invoice to the client?", "output": "respond"},
    {"input": "What is the target date for deployment?", "output": "respond"},
    {"input": "Can you fix the bug in the triage logic?", "output": "respond"},
    {"input": "Do you have the contact for the vendor?", "output": "respond"},
    {"input": "Can you update the Jira ticket?", "output": "respond"},

    # --- IGNORE (34 Examples) ---
    {"input": "Buy bitcoin now and get 500% returns!", "output": "ignore"},
    {"input": "Your daily newsletter is here.", "output": "ignore"},
    {"input": "Limited time offer: 50% off all shoes.", "output": "ignore"},
    {"input": "Congratulations! You won a gift card.", "output": "ignore"},
    {"input": "Claim your inheritance now.", "output": "ignore"},
    {"input": "Work from home and earn $5000.", "output": "ignore"},
    {"input": "Verify your account immediately.", "output": "ignore"},
    {"input": "Increase your followers today!", "output": "ignore"},
    {"input": "Weekly digest: Top stories.", "output": "ignore"},
    {"input": "Cheap pharmacy deals inside!", "output": "ignore"},
    {"input": "You have 1 new connection request on a site you don't use.", "output": "ignore"},
    {"input": "Your package is waiting at the post office (Fake link).", "output": "ignore"},
    {"input": "Don't miss our summer sale!", "output": "ignore"},
    {"input": "Invest in gold today!", "output": "ignore"},
    {"input": "Unsubscribe from this mailing list.", "output": "ignore"},
    {"input": "Your subscription will renew soon.", "output": "ignore"},
    {"input": "Check out these new restaurant openings.", "output": "ignore"},
    {"input": "Free webinar on how to get rich.", "output": "ignore"},
    {"input": "Low-interest credit card offers.", "output": "ignore"},
    {"input": "Special discount for loyal customers.", "output": "ignore"},
    {"input": "Your bill is ready to view (Spam).", "output": "ignore"},
    {"input": "Join our survey and win a prize.", "output": "ignore"},
    {"input": "Meet singles in your area.", "output": "ignore"},
    {"input": "New job alerts for you (Generic).", "output": "ignore"},
    {"input": "Weight loss secrets revealed!", "output": "ignore"},
    {"input": "Best deals on car insurance.", "output": "ignore"},
    {"input": "Update your profile settings.", "output": "ignore"},
    {"input": "A new device logged into your Facebook (Spam).", "output": "ignore"},
    {"input": "Your storage is 90% full. Buy more.", "output": "ignore"},
    {"input": "Reminder: Your appointment is in 2 months.", "output": "ignore"},
    {"input": "Check out this cool video!", "output": "ignore"},
    {"input": "You have a message from a stranger.", "output": "ignore"},
    {"input": "Final warning: Your account will be closed.", "output": "ignore"},
    {"input": "Holiday greetings from the marketing team.", "output": "ignore"},

    # --- NOTIFY_HUMAN (33 Examples) ---
    {"input": "URGENT: The production server is down!", "output": "notify_human"},
    {"input": "Hi, this is your CEO. Please call me ASAP.", "output": "notify_human"},
    {"input": "Mom: We are at the hospital.", "output": "notify_human"},
    {"input": "Security breach detected in your account.", "output": "notify_human"},
    {"input": "Legal Notice: Contract action required.", "output": "notify_human"},
    {"input": "Client is extremely unhappy with the delivery.", "output": "notify_human"},
    {"input": "I am resigning immediately.", "output": "notify_human"},
    {"input": "Emergency: House alarm triggered.", "output": "notify_human"},
    {"input": "Can you pick up the kids? Emergency.", "output": "notify_human"},
    {"input": "PRIVATE AND CONFIDENTIAL - CEO ONLY.", "output": "notify_human"},
    {"input": "The office is on fire! (Literal emergency)", "output": "notify_human"},
    {"input": "Lawsuit threat from a competitor.", "output": "notify_human"},
    {"input": "Your bank account has been frozen.", "output": "notify_human"},
    {"input": "Critical error in the payment gateway.", "output": "notify_human"},
    {"input": "The main database has been deleted.", "output": "notify_human"},
    {"input": "Your visa application has been rejected.", "output": "notify_human"},
    {"input": "Urgent: Someone is trying to change your password.", "output": "notify_human"},
    {"input": "A family member is trying to reach you urgently.", "output": "notify_human"},
    {"input": "The investor wants to pull out of the deal.", "output": "notify_human"},
    {"input": "The landlord is evicting us.", "output": "notify_human"},
    {"input": "Police are asking for you.", "output": "notify_human"},
    {"input": "The CFO needs to talk to you about the audit.", "output": "notify_human"},
    {"input": "Your car has been towed.", "output": "notify_human"},
    {"input": "A major bug was found in the live system.", "output": "notify_human"},
    {"input": "Someone is using your identity.", "output": "notify_human"},
    {"input": "The data center has lost power.", "output": "notify_human"},
    {"input": "Your flight has been cancelled, no rebooking.", "output": "notify_human"},
    {"input": "A critical vulnerability was found in your code.", "output": "notify_human"},
    {"input": "The board of directors needs an immediate answer.", "output": "notify_human"},
    {"input": "Your health insurance has been cancelled.", "output": "notify_human"},
    {"input": "Urgent: Please verify this $10,000 transaction.", "output": "notify_human"},
    {"input": "The API keys have been leaked on GitHub.", "output": "notify_human"},
    {"input": "Your home's water pipe has burst.", "output": "notify_human"}
]

# Create dataset and upload loop
if not client.has_dataset(dataset_name=dataset_name):
    client.create_dataset(dataset_name)

for email in emails:
    client.create_example(
        inputs={"email_body": email["input"]},
        outputs={"triage": email["output"]},
        dataset_name=dataset_name
    )

print(f"Uploaded {len(emails)} more emails! Total count will be much higher now.")