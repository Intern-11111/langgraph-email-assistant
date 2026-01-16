def mock_send_email(data):
    print("\n------ INCOMING EMAIL HANDLER EXECUTED ------")
    # For received email, we process subject/body; 'to' may represent routing target
    if "to" in data:
        print("ROUTE TO:", data["to"]) 
    print("SUBJECT:", data.get("subject")) 
    print("BODY:", data.get("body")) 
    print("ACTION: Auto-Processed")
    print("---------------------------------\n")

    return {"status": "Email Processed"}
