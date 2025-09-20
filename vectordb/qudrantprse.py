import requests
import json

BASE_URL = "http://localhost:6333"
COLLECTION = "split_hierarchical"

def fetch_all_node_contents(limit=100):
    url = f"{BASE_URL}/collections/{COLLECTION}/points/scroll"
    headers = {"Content-Type": "application/json"}
    payload = {"limit": limit, "with_payload": True, "with_vector": False}

    all_nodes = []
    offset = None

    while True:
        if offset:
            payload["offset"] = offset
        else:
            payload["offset"] = None

        resp = requests.post(url, headers=headers, data=json.dumps(payload))
        resp.raise_for_status()
        data = resp.json()

        points = data.get("result", {}).get("points", [])
        for p in points:
            node_content_str = p.get("payload", {}).get("_node_content")
            if node_content_str:
                try:
                    node_content_obj = json.loads(node_content_str)
                    all_nodes.append(node_content_obj)
                except json.JSONDecodeError:
                    # If it's not valid JSON, just keep it as string
                    all_nodes.append(node_content_str)

        # check if more pages
        offset = data.get("result", {}).get("next_page_offset")
        if not offset:
            break

    return all_nodes


node_contents = fetch_all_node_contents(limit=50)
open("node_contents.json", "w").write(json.dumps(node_contents, indent=2))
# print(json.dumps(node_contents, indent=2))
