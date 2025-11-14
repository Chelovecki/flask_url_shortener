import datetime
import random
import string
import uuid


class URLShortener:
    """
    Class-helper, wich helps provide all main methods for generate, save, update links

    1. Generate unique code for short link
    2. Generate short link for user link
    3. Save it link in way: short_code: user_link
    4. If need - get user_link by short_code
    """

    def __init__(self):
        self.symbols_for_short_link = string.digits + string.ascii_lowercase
        self.code_url = {}
        self.urls_code = {}

    def _generate_short_code(self, user_url) -> str:
        # for optimization we can send user_url for getting by key
        while True:
            code = str(uuid.uuid4())[:5]

            if self.urls_code.get(user_url) is None:
                return code

    def get_code_by_url(self, user_url: str) -> str:
        """
        Get existing short code for user_url or generate new one if not exists.

        Checks if the user_url already has a short code in storage.
        If found, returns the existing code. Otherwise generates a new code.

        Args:
            user_url (str): link wich user input on web

        Returns:
            str: short code for short link
        """
        value = self.urls_code.get(user_url)
        return value if value else self._generate_short_code(user_url)

    def get_link_by_code(self, short_code):
        return self.code_url.get(short_code)

    def set_user_link(self, user_link, code):
        self.code_url[code] = user_link
        self.urls_code[user_link] = code


def get_date_expire(year: int, month: int, day: int):

    now_data = datetime.datetime.now()

    date_future = datetime.timedelta(days=day + month*30 + year*365)
    link_expires_at = now_data + date_future
    day_expire = link_expires_at.day
    month_expire = link_expires_at.month
    year_expire = link_expires_at.year
    
    return year_expire, month_expire, day_expire
