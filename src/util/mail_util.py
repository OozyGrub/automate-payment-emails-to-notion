import imaplib
from typing import List, Tuple 
from email.message import Message
from util.parse_util import ParseUtil
import email
from config import SMTP_SERVER, FROM_EMAIL, FROM_PWD

class MailUtil:
    def connect() -> imaplib.IMAP4_SSL:
        print("FROM_EMAIL: " + FROM_EMAIL)
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL, FROM_PWD) 
        return mail

    def get_email_uid(mail: str, email_id: str) -> str:
        _, data = mail.fetch(email_id, "(UID)")
        msg_uid = ParseUtil.parse_uid(data[0])
        return msg_uid

    def move_email(mail: str, uid: str, source_folder: str, destination_folder: str) -> None:
        result, data = mail.uid('COPY', uid, destination_folder)
        if result != 'OK':
            raise Exception("Unable to move email")
        # Mark the email as deleted in the source folder
        mail.uid('STORE', uid, '+FLAGS', '(\Deleted)')
        mail.expunge()

    def list_messages(mail: str, source_folder: str) -> List[Tuple[str, Message]]:
        mail.select(source_folder)
        data = mail.search(None, 'ALL')
        mail_ids = data[1]
        id_list = mail_ids[0].split()
        if (len(id_list) == 0):
            return []
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])
        results = []
        for i in range(latest_email_id, first_email_id - 1, -1):
            email_id = str(i)
            email_uid = MailUtil.get_email_uid(mail, email_id)
            data = mail.fetch(email_id, '(RFC822)' )
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    msg = email.message_from_string(str(arr[1], 'utf-8'))
                    results.append((email_uid, msg))
        return results
