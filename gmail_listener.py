from gmail_auth import get_gmail_service


# Store last processed historyId (memory-based)
LAST_HISTORY_ID = 0


def fetch_new_message_ids(history_id):
    """
    Fetch new Gmail message IDs using History API
    """

    global LAST_HISTORY_ID

    service = get_gmail_service()

    # Use previous history checkpoint
    start_id = LAST_HISTORY_ID if LAST_HISTORY_ID > 0 else history_id

    response = service.users().history().list(
    userId='me',
    startHistoryId=start_id,
    historyTypes=['messageAdded'],
    maxResults=50
    ).execute()


    message_ids = []

    if 'history' in response:
        for record in response['history']:
            if 'messagesAdded' in record:
                for msg in record['messagesAdded']:
                    message_ids.append(msg['message']['id'])

    # Update checkpoint
    LAST_HISTORY_ID = history_id

    return message_ids
   
