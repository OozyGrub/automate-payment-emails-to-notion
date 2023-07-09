from util.mail_util import MailUtil
from parser.expense_parser import ExpenseParser, SCBExpenseParser
from api.notion_client import NotionClient
from typing import Tuple
from config import DATABASE_ID, FOLDER_PENDING, FOLDER_DONE

def read_expense(mail: str, source: str, dest: str, parser: ExpenseParser) -> Tuple[int, int]:
    print(parser().get_name())
    success = 0
    fail = 0
    for [uid, msg] in MailUtil.list_messages(mail, source):
        try:
            parser().validate(msg)
            transaction = parser().parse(msg)
            NotionClient().create_page(DATABASE_ID, transaction)
            MailUtil.move_email(mail, uid, source, dest)
            success += 1
        except Exception as e:
            print(e)
            fail += 1
    return (success, fail)
                
    
def execute():
    mail = MailUtil.connect()
    try:
        (success, fail) = read_expense(mail, FOLDER_PENDING, FOLDER_DONE, SCBExpenseParser)
        print(f"Total successful transaction(s): {success}")
        print(f"Total failed transaction(s): {fail}")
    finally:
        mail.logout()

if __name__ == "__main__":
    print("DATABASE_ID: " + DATABASE_ID)
    execute()