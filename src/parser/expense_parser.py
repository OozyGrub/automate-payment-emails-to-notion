from email.message import Message
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
from type.transaction import Transaction

class ExpenseParser:
    def parse(self, msg: Message) -> None:
        raise NotImplementedError("Not implemented")

    def validate(self, msg: Message) -> None:
        if msg['subject'] != self.expected_email_subject:
            raise Exception(f"Unexpected email subject: {msg['subject']}")
        if not msg.is_multipart():
            raise Exception(f"Unable to read non-multipart")

    def get_name(self) -> str:
        return self.name
    
    def get_prefix(self) -> str:
        return self.prefix

class SCBExpenseParser(ExpenseParser):
    name = "SCBExpenseParser"
    prefix = "SCB"
    expected_email_subject = "Alert from SCB Easy App : Automatic notice of transaction"

    def parse(self, msg: Message) -> Transaction:
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type != 'multipart/related':
                    continue
                related_parts = part.get_payload()
                for related_part in related_parts:
                    related_content_type = related_part.get_content_type()
                    if related_content_type != "text/html":
                        continue
                    email_body = related_part.get_payload(decode=True).decode('utf-8')
                    amount = self.extract_amount(email_body)
                    created_at = self.extract_datetime(email_body)
                    return Transaction(f"{self.get_prefix()} {created_at.strftime('%Y-%m-%dT%H:%M')}", created_at, amount)
        raise Exception("Unable to parse message")

    @staticmethod 
    def extract_amount(email_body: str) -> float:
        soup = BeautifulSoup(email_body, "html.parser")
        table = soup.find_all('table')
        df = pd.read_html(str(table))[0]
        baht_text = df[2][3]
        expense = float(baht_text.split(" ")[0])
        return expense

    @staticmethod 
    def extract_datetime(email_body: str) -> datetime:
        soup = BeautifulSoup(email_body, "html.parser")
        table = soup.find_all('table')
        df = pd.read_html(str(table))[0]
        date_string = df[1][4]
        return datetime.strptime(date_string, "%d %b %Y at %H:%M:%S")


class UOBCreditExpenseParser(ExpenseParser):
    name = "UOBCreditExpenseParser"

    def parse(self, msg):
        pass

class KBankCreditExpenseParser(ExpenseParser):
    name = "KBankCreditExpenseParser"

    def parse(self, msg):
        # TODO
        pass