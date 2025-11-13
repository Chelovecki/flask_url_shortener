from helpers import URLShortener
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)


@app.route('/urls')
def urls() -> dict[str: str]:
    """
    Show all handled and saved user link

    Returns:
        dict[str: str]: code for short link: user orig link
    """

    return handler.code_url


@app.route('/redirect/<string:code>', methods=['GET'])
def redirect_to(code: str) -> redirect:
    """
    Find user link by this `code` and redirect from this page to saved user link


    Args:
        code (str): mean code, wich reference to some user link

    Returns:
        redirect: link to user site
    """

    url_to_redirect = handler.code_url.get(code)

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
            shortened_link = get_short_link(user_link)
    print(error)
    return render_template('index.html', orig_link=user_link, shortened_link=shortened_link, error=error)


def get_short_link(user_url):
    code = handler.get_code_by_url(user_url)

    handler.set_user_link(user_link=user_url, code=code)

    abs_url_with_short_link = url_for('redirect_to', code=code, _external=True)

    return abs_url_with_short_link


handler = URLShortener()

if __name__ == '__main__':
    app.run(debug=True)
