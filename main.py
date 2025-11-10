import random
import string
from flask import Flask, redirect, render_template, request, url_for
app = Flask(__name__)


class URLShortener:
    symbols_for_generate_short_link = string.digits + string.ascii_lowercase
    urls_data = {}

    def __init__(self):
        pass

    @classmethod
    def get_rand_link(cls):

        url = "".join([random.choice(cls.symbols_for_generate_short_link)
                      for _ in range(6)])
        return url

    @classmethod
    def aboba(cls, user_url):
        unique_code = cls.get_rand_link()
        yet_existed = None
        for code, url in cls.urls_data.items():
            if url == user_url:
                yet_existed = code
                break
        if yet_existed:
            unique_code = yet_existed

        cls.set_user_link(user_link=user_url, code=unique_code)

        abs_url = url_for(
            'redirect_to', unique_code=unique_code, _external=True)

        return abs_url

    @classmethod
    def set_user_link(cls, user_link, code):
        cls.urls_data[code] = user_link


@app.route('/urls')
def urls():
    return o.urls_data


@app.route('/redirect/<string:unique_code>', methods=['GET'])
def redirect_to(unique_code):
    if request.method == 'GET':
        url_to_redirect = o.urls_data.get(unique_code)

        return redirect(url_to_redirect)


@app.route('/set', methods=['POST', 'GET'])
def hello():
    error = None
    shortened_link = None
    user_link = None
    if request.method == 'POST':
        user_link = request.form.get('user_url')
        print(user_link)

        if not user_link or user_link.strip() == '':
            error = 'Пожалуйста, введите ссылку'
        elif (user_link.startswith('http://') + user_link.startswith('https://')) == 0:
            error = 'Ссылка должна начинаться с http:// или https://'
        else:

            shortened_link = o.aboba(user_link)

            print(f"получили абсолютный путь: {shortened_link}")
            print('dict is:', o.urls_data)
        print(error)
        return render_template('index.html', orig_link=user_link, shortened_link=shortened_link, error=error)


if __name__ == '__main__':
    o = URLShortener()

    app.run(debug=True)
