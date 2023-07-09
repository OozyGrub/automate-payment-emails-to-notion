import re

pattern_uid = re.compile(r"\bUID (?P<uid>\d+)\b")

class ParseUtil:
    def parse_uid(data: any) -> str:
        match = re.search(pattern_uid, str(data))
        if match == False:
            raise Exception("Unable to parse uid")
        uid = match.group('uid')
        return uid
