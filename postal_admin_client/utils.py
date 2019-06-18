import re
from typing import List


def find_all_urls(content: str) -> List[str]:
    """
    Finds and returns all urls in a string
    """
    return re.findall(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
        content,
    ) 
