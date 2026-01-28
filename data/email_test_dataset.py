# data/email_test_dataset.py

TEST_EMAILS = [

    # -------- IGNORE --------
    {
        "subject": "Big Sale on Electronics!",
        "body": "Limited time sale. Unsubscribe anytime.",
        "expected_category": "ignore"
    },
    {
        "subject": "Newsletter – October Edition",
        "body": "This is our monthly newsletter.",
        "expected_category": "ignore"
    },
    {
        "subject": "Exclusive Promotion for You",
        "body": "Special discounts available now.",
        "expected_category": "ignore"
    },
    {
        "subject": "Unsubscribe Confirmation",
        "body": "You have been unsubscribed successfully.",
        "expected_category": "ignore"
    },
    {
        "subject": "Flash Sale Alert",
        "body": "Huge offers on selected products.",
        "expected_category": "ignore"
    },
    {
        "subject": "Marketing Campaign Update",
        "body": "Latest trends in digital marketing.",
        "expected_category": "ignore"
    },
    {
        "subject": "Weekly Deals Newsletter",
        "body": "Top deals of the week.",
        "expected_category": "ignore"
    },
    {
        "subject": "Promotion: Buy One Get One",
        "body": "Limited period offer.",
        "expected_category": "ignore"
    },

    # -------- NOTIFY HUMAN --------
    {
        "subject": "Invoice for April",
        "body": "Please review the attached invoice.",
        "expected_category": "notify_human"
    },
    {
        "subject": "Payment Due Reminder",
        "body": "Your payment is due tomorrow.",
        "expected_category": "notify_human"
    },
    {
        "subject": "Account Alert",
        "body": "Suspicious login detected.",
        "expected_category": "notify_human"
    },
    {
        "subject": "System Warning",
        "body": "Your password will expire soon.",
        "expected_category": "notify_human"
    },
    {
        "subject": "Billing Notification",
        "body": "Your bill is now available.",
        "expected_category": "notify_human"
    },
    {
        "subject": "Security Alert",
        "body": "New device logged into your account.",
        "expected_category": "notify_human"
    },
    {
        "subject": "Payment Confirmation",
        "body": "Your transaction was successful.",
        "expected_category": "notify_human"
    },
    {
        "subject": "Service Interruption Notice",
        "body": "Scheduled maintenance tonight.",
        "expected_category": "notify_human"
    },

    # -------- RESPOND --------
    {
        "subject": "Urgent Meeting Request",
        "body": "Can we schedule a meeting today?",
        "expected_category": "respond"
    },
    {
        "subject": "Please Respond ASAP",
        "body": "Waiting for your response.",
        "expected_category": "respond"
    },
    {
        "subject": "Interview Schedule",
        "body": "Let us know your availability.",
        "expected_category": "respond"
    },
    {
        "subject": "Project Update Required",
        "body": "Please send the latest project update.",
        "expected_category": "respond"
    },
    {
        "subject": "Client Meeting",
        "body": "Can we reschedule our meeting?",
        "expected_category": "respond"
    },
    {
        "subject": "Follow-up Required",
        "body": "Please reply with your feedback.",
        "expected_category": "respond"
    },
    {
        "subject": "Urgent: Approval Needed",
        "body": "Please approve the document.",
        "expected_category": "respond"
    },
    {
        "subject": "Schedule Discussion",
        "body": "Let’s discuss the timeline.",
        "expected_category": "respond"
    }
]
