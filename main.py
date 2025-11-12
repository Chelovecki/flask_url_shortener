import random
import string
from typing import Dict
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)


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
        self.urls_data = {}

    def _generate_short_code(self) -> str:
        """
        Generate unique short code with 6 symbols

        Returns:
            str: code for short link
        """
        while True:
            code = "".join([random.choice(self.symbols_for_short_link)
                            for _ in range(6)])
            if code not in self.urls_data.keys():
                return code

    def _get_code_of_user_url(self, user_url: str) -> str:
        """
        Get existing short code for user_url or generate new one if not exists.

        Checks if the user_url already has a short code in storage.
        If found, returns the existing code. Otherwise generates a new code.

        Args:
            user_url (str): link wich user input on web

        Returns:
            str: short code for short link
        """
        for existing_code, existing_url in self.urls_data.items():
            if existing_url == user_url:
                return existing_code

        return self._generate_short_code()

    def get_short_link(self, user_url):
        """
        Generate or retrieve short link for the given user URL.

        Args:
            user_url (_type_): _description_

        Returns:
            _type_: _description_
        """
        code = self._get_code_of_user_url(user_url)

        self.set_user_link(user_link=user_url, code=code)

        abs_url_with_short_link = url_for(
            'redirect_to', code=code, _external=True)

        return abs_url_with_short_link

    def get_user_link(self, short_code):
        return self.urls_data.get(short_code)

    def set_user_link(self, user_link, code):
        self.urls_data[code] = user_link


@app.route('/urls')
def urls() -> dict[str: str]:
    """
    Show all handled and saved user link

    Returns:
        dict[str: str]: code for short link: user orig link
    """

    return handler.urls_data


@app.route('/redirect/<string:code>', methods=['GET'])
def redirect_to(code: str) -> redirect:
    """
    Find user link by this `code` and redirect from this page to saved user link


    Args:
        code (str): mean code, wich reference to some user link

    Returns:
        redirect: link to user site
    """

    if request.method == 'GET':
        url_to_redirect = handler.urls_data.get(code)

        return redirect(url_to_redirect)


@app.route('/set', methods=['POST', 'GET'])
def main() -> render_template:
    """
    Main function, defines the conduction of creating short links
    1. Get user link from form
    2. Validate this input data
    3. If ok - create short link for this link, save it to dict
    4. Return page with rendered data (short link + original link)

    Returns:
        render_template: template with new info or empty form
    """
    error = None
    shortened_link = None
    user_link = None

    if request.method == 'POST':
        user_link = request.form.get('user_url')

        # пустая ссылка
        if not user_link or user_link.strip() == '':
            error = 'Пожалуйста, введите ссылку'

        # начинается не с http - не ссылка
        elif not user_link.startswith('http://') and not user_link.startswith('https://'):
            error = 'Ссылка должна начинаться с http:// или https://'

        # все хорошо, обрабатываем полученную ссылку
        else:
            shortened_link = handler.get_short_link(user_link)
    print(error)
    return render_template('index.html', orig_link=user_link, shortened_link=shortened_link, error=error)


if __name__ == '__main__':
    handler = URLShortener()
    app.run(debug=True)
