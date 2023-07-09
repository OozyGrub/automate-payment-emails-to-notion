from type.transaction import Transaction
import requests
from config import NOTION_KEY

class NotionClient():
    headers = {
        'Authorization': 'Bearer '+ NOTION_KEY,
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28'
    }
    
    # TODO: refactor payload
    def create_page(self, parent_id: str, txn: Transaction) -> None:
        url = 'https://api.notion.com/v1/pages'
        start = txn.created_at.isoformat() + "Z"
        data = {
            "parent": { "database_id": parent_id },
            "properties": {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": txn.title,
                            }
                        }
                    ]
                },
                "Date": {
                    "date": {
                        "start": start,
                        "time_zone": "Asia/Bangkok"
                    }
                },
                "Price": {
                    "number": txn.amount
                }
            }
        }
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code != 200:
            raise Exception(f"Notion API Error with status: {response.status_code}")
        print("Request successful!")
        return