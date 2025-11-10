import random
import string
from flask import Flask, redirect, render_template, request, url_for
app = Flask(__name__)


class URLShortener:
    def __init__(self):
        self.symbols_for_short_link = string.digits + string.ascii_lowercase
        self.urls_data = {}

    def _generate_short_code(self):
        url = "".join([random.choice(self.symbols_for_short_link)
                      for _ in range(6)])
        return url

    def _get_unique_code(self, user_url):
        unique_code = self._generate_short_code()

        yet_existed = None
        for code, url in self.urls_data.items():
            if url == user_url:
                yet_existed = code
                break

        if not yet_existed:
            yet_existed = unique_code

        return yet_existed

    def get_short_link(self, user_url):
        unique_code = self._get_unique_code(user_url)

        self.set_user_link(user_link=user_url, code=unique_code)

        abs_url_with_short_link = url_for(
            'redirect_to', unique_code=unique_code, _external=True)

        return abs_url_with_short_link

    def get_user_link(self, short_code):
        return self.urls_data.get(short_code)

    def set_user_link(self, user_link, code):
        self.urls_data[code] = user_link


@app.route('/urls')
def urls():
    return handler.urls_data


@app.route('/redirect/<string:unique_code>', methods=['GET'])
def redirect_to(unique_code):
    if request.method == 'GET':
        url_to_redirect = handler.urls_data.get(unique_code)

        return redirect(url_to_redirect)


@app.route('/set', methods=['POST', 'GET'])
def main():
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
