import requests
from typing import Dict, Tuple

endpoint = "https://api.devrev.ai/internal/"
token = ""
stageDiagram = {
    "name": "zendesk_uniphore_tickets.null",
    "stages": [ 

        {
            "name": "New",
            "is_start": True,
            "transitions": [
                "queued",
                "On-hold",
                "awaiting_delivery",
                "awaiting_sales",
                "awaiting_product_assist",
                "awaiting_vulnerabilities",
                "Work In Progress",
                "in_development",
                "awaiting_development",
                "awaiting_customer_response",
                "Resolved",
                "Closed",
               
            ],
        },
        {
            "name": "queued",
            "transitions": [
                "New",
                "In Progress",
                "On-hold",
                "awaiting_delivery",
                "awaiting_sales",
                "awaiting_product_assist",
                "awaiting_vulnerabilities",
                "Work In Progress",
                "in_development",
                "awaiting_development",
                "awaiting_customer_response",
                "Resolved",
                "Closed",    
            ],
        },
        {
            "name": "On-hold",
            "transitions": [
                "New",
                "queued",
                "awaiting_delivery",
                "awaiting_sales",
                "awaiting_product_assist",
                "awaiting_vulnerabilities",
                "Work In Progress",
                "in_development",
                "awaiting_development",
                "awaiting_customer_response",
                "Resolved",
                "Closed",       
            ],
        },
        {
            "name": "awaiting_delivery",
            "transitions": [
                "New",
                "queued",
                "On-hold",
                "awaiting_sales",
                "awaiting_product_assist",
                "awaiting_vulnerabilities",
                "Work In Progress",
                "in_development",
                "awaiting_development",
                "awaiting_customer_response",
                "Resolved",
                "Closed",
            ],
        },
        {
            "name": "awaiting_sales",
            "transitions": [
                "New",
                "queued",
                "On-hold",
                "awaiting_delivery",
                "awaiting_product_assist",
                "awaiting_vulnerabilities",
                "Work In Progress",
                "in_development",
                "awaiting_development",
                "awaiting_customer_response",
                "Resolved",
                "Closed",
            ],
        },
        {
            "name": "awaiting_product_assist",
            "transitions": [
                "New",
                "queued",
                "On-hold",
                "awaiting_delivery",
                "awaiting_sales",
                "awaiting_vulnerabilities",
                "Work In Progress",
                "in_development",
                "awaiting_development",
                "awaiting_customer_response",
                "Resolved",
                "Closed",
            ],
        },
        {
            "name": "awaiting_vulnerabilities",
            "transitions": [
                "New",
                "queued",
                "On-hold",
                "awaiting_delivery",
                "awaiting_sales",
                "awaiting_product_assist",
                "Work In Progress",
                "in_development",
                "awaiting_development",
                "awaiting_customer_response",
                "Resolved",
                "Closed",
            ],
        },

        {
            "name": "Work In Progress",
            "transitions": [
                "New",
                "queued",
                "On-hold",
                "awaiting_delivery",
                "awaiting_sales",
                "awaiting_product_assist",
                "awaiting_vulnerabilities",
                "in_development",
                "awaiting_development",
                "awaiting_customer_response",
                "Resolved",
                "Closed",
            ],
        },
        {
            "name": "in_development",
            "transitions": [
                "New",
                "queued",
                "On-hold",
                "awaiting_delivery",
                "awaiting_sales",
                "awaiting_product_assist",
                "awaiting_vulnerabilities",
                "Work In Progress",
                "awaiting_development",
                "awaiting_customer_response",
                "Resolved",
                "Closed",
            ],
        },
        {
            "name": "awaiting_development",
            "transitions": [
                "New",
                "queued",
                "On-hold",
                "awaiting_delivery",
                "awaiting_sales",
                "awaiting_product_assist",
                "awaiting_vulnerabilities",
                "Work In Progress",
                "in_development",
                "awaiting_customer_response",
                "Resolved",
                "Closed",
            ],
        },
        {
            "name": "awaiting_customer_response",
            "transitions": [
                "New",
                "queued",
                "In Progress",
                "On-hold",
                "awaiting_delivery",
                "awaiting_sales",
                "awaiting_product_assist",
                "awaiting_vulnerabilities",
                "Work In Progress",
                "in_development",
                "awaiting_development",
                "Resolved",
                "Closed",
            ],
        },
        {
            "name": "Resolved",
            "transitions": [
                "New",
                "queued",
                "On-hold",
                "awaiting_delivery",
                "awaiting_sales",
                "awaiting_product_assist",
                "awaiting_vulnerabilities",
                "Work In Progress",
                "in_development",
                "awaiting_development",
                "awaiting_customer_response",
                "Closed",
                
            ],
        },
        {
            "name": "Closed",
            "transitions": [
                "New",
                "queued",
                "On-hold",
                "awaiting_delivery",
                "awaiting_sales",
                "awaiting_product_assist",
                "awaiting_vulnerabilities",
                "Work In Progress",
                "in_development",
                "awaiting_development",
                "awaiting_customer_response",
                "Resolved",
            ],
        },
        


        # ZD stages which needs to be deprecated
        {
            "name": "pending",
            "is_deprecated": True,
            "transitions": [
                "New",
                
            ],
        },
        {
            "name": "Jira Closed",
            "is_deprecated": True,
            "transitions": [
                "New",
            ],
        },
        {
            "name": "Support Work In Progress",
            "is_deprecated": True,
            "transitions": [
                "New",
            ],
        },
        
        {
            "name": "Jira Pending",
            "is_deprecated": True,
            "transitions": [
                "New",
            ],
        },
        {
            "name": "Solved",
            "is_deprecated": True,
            "transitions": [
                "New",
            ],
        },


    ],
}



stagesListUrl = endpoint + "stages.custom.list"
stageDiagramsUpdateUrl = endpoint + "stage-diagrams.update"



def makeStageInfo() -> (
    Dict[str, Dict[str, any]]
):  # name: {ordinal: int, stage_id: str, state_id: str}
    resp = requests.get(
        stagesListUrl,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": token,
        },
    )
    if resp.status_code != 200:
        print(f"Failed to fetch stages")
    jsonResp = resp.json()
    stageInfo = {}
    for stage in jsonResp["result"]:
        stageInfo[stage["name"]] = {
            "ordinal": stage["ordinal"],
            "stage_id": stage["id"],
            "state_id": stage["state"]["id"],
        }

    return stageInfo



def updateStageDiagram(id: str):
    stageNodes = []
    stageInfo = makeStageInfo()
    for stage in stageDiagram["stages"]:
        transitions = []
        for targetStageName in stage["transitions"]:
            transitions.append(
                {"target_stage_id": stageInfo[targetStageName]["stage_id"]}
            )
        stageNodes.append(
            {
                "is_start": stage.get("is_start", False),
                "is_deprecated": stage.get("is_deprecated", False),
                "stage_id": stageInfo[stage["name"]]["stage_id"],
                "transitions": transitions,
            }
        )

    data = {
        "id": id,
        "name": stageDiagram["name"],
        "stages": stageNodes,
    }
    resp = requests.post(
        stageDiagramsUpdateUrl,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": token,
        },
        json=data,
    )
    if resp.status_code == 200 or resp.status_code == 201:
        print(f"Stage diagram updated")
        print(resp.json())

    if resp.status_code != 200 and resp.status_code != 201:
        print(f"Stage diagram update failed")
        print(resp.json())




if __name__ == "__main__":

    #Stage diagrams to be updated
    #don:core:dvrv-us-1:devo/NJ5yrCDA:stage_diagram/39    name: zendesk_uniphore_tickets.null 
    #don:core:dvrv-us-1:devo/NJ5yrCDA:stage_diagram/38    name:zendesk_uniphore_tickets.question  
    #don:core:dvrv-us-1:devo/NJ5yrCDA:stage_diagram/37    name:zendesk_uniphore_tickets.problem   
    #don:core:dvrv-us-1:devo/NJ5yrCDA:stage_diagram/36    name:zendesk_uniphore_tickets.incident


    stageDiagramId = ""
    
    updateStageDiagram(stageDiagramId)
   
