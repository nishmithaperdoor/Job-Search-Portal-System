import requests
import json

endpoint = "https://api.devrev.ai/internal/"
token = ""  # Fill in
works_list_url = endpoint + "works.list"
works_update_url = endpoint + "works.update"

# Change the mapping as needed
stages_mapping = {
    "don:core:dvrv-us-1:devo/NJ5yrCDA:custom_stage/41": "", # Pending to 
    "don:core:dvrv-us-1:devo/NJ5yrCDA:custom_stage/70": "", # Jira Closed to
    "don:core:dvrv-us-1:devo/NJ5yrCDA:custom_stage/71": "", # Support Work In Progress to
    "don:core:dvrv-us-1:devo/NJ5yrCDA:custom_stage/72": "", # Work In Progress to 
    "don:core:dvrv-us-1:devo/NJ5yrCDA:custom_stage/73": "", # Jira Pending to
    "don:core:dvrv-us-1:devo/NJ5yrCDA:custom_stage/74": "", # New to 
    "don:core:dvrv-us-1:devo/NJ5yrCDA:custom_stage/75": "", # On hold to 
    "don:core:dvrv-us-1:devo/NJ5yrCDA:custom_stage/76": "", # Open to
    "don:core:dvrv-us-1:devo/NJ5yrCDA:custom_stage/77": ""  # Solved to
}

def get_tickets(cursor):
    url = works_list_url

    # Change the subtypes names as needed (if we only want to fetch of a specific subtype, like Zendesk only)
    payload = '{"stage":{"name":["Pending","Jira Closed","Support Work In Progress","Work In Progress","Jira Pending","New","On-hold","Open","Solved"]},"type":["ticket"],"ticket":{"subtype":["zendesk_uniphore_tickets.incident","zendesk_uniphore-q_tickets.incident","zendesk_uniphore_tickets.null","zendesk_uniphore-q_tickets.null","zendesk_uniphore_tickets.problem","zendesk_uniphore-q_tickets.problem","zendesk_uniphore-q_tickets.task","zendesk_uniphore_tickets.question"]},"exclude_child_items":true}'
    if cursor:
        payload = f'{{"cursor":"{cursor}", "stage":{{"name":["Pending","Jira Closed","Support Work In Progress","Work In Progress","Jira Pending","New","On-hold","Open","Solved"]}},"type":["ticket"],"ticket":{{"subtype":["zendesk_uniphore_tickets.incident","zendesk_uniphore-q_tickets.incident","zendesk_uniphore_tickets.null","zendesk_uniphore-q_tickets.null","zendesk_uniphore_tickets.problem","zendesk_uniphore-q_tickets.problem","zendesk_uniphore-q_tickets.task","zendesk_uniphore_tickets.question"]}},"exclude_child_items":true}}'

    resp = requests.post(
        url,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": token,
        },
        data=payload
    )
    jsonResp = resp.json()
    if resp.status_code != 200:
        print(f"Failed to fetch tickets")
        print(jsonResp)
        return [], None
    
    data = jsonResp["works"]

    next_cursor = None
    if "next_cursor" in jsonResp:
        next_cursor = jsonResp["next_cursor"]

    return data, next_cursor

def update_ticket(ticket_id: str, target_stage: str):
    resp = requests.post(
        works_update_url,
        headers={
            "Content-Type": "application/json",
            "Authorization": token,
        },
        data=f'{{"id": "{ticket_id}", "stage": {{"stage": "{target_stage}"}}}}'
    )
    if resp.status_code != 200:
        print(f"Failed to update ticket")
        print(resp.json())

def main():
    cursor = None
    # Starting cursor for starting where left off (in case we stopped the script for some reason)
    #cursor = "cldH6Ew"
    array = []
    while True:
        print("Cursor", cursor)
        tickets, cursor = get_tickets(cursor)
        print("Received", len(tickets), "tickets")
        for ticket in tickets:
            array.append(ticket)
            # Get stage
            stage = None
            if "stage" in ticket:
                stage = ticket["stage"]
            if stage is None:
                continue
            # Get target stage
            target_stage = None
            if stage["stage"]["id"] in stages_mapping:
                target_stage = stages_mapping[stage["stage"]["id"]]
            if target_stage is None:
                print(f"No mapping for stage {stage["name"]}")
                continue
            print(f"Updating ticket {ticket["id"]} from {stage["name"]} to {target_stage}")
            
            update_ticket(ticket["id"], target_stage)
        if not cursor:
            break
    # Saving to a file just to check tickets parsed
    with open("listed_tickets.json", "w") as f:
        json.dump(array, f)

if __name__ == "__main__":
    main()
