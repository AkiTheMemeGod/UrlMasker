from flask import *
from assets import Database
app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/add_url', methods=['POST'])
def add_url():
    d = Database()
    url = request.json.get('url')
    if url:
        key, qr = d.add_key(url)
        #short_url = f"http://127.0.0.1:5000/{key}"

        short_url = f"https://maskurl.pythonanywhere.com/{key}"
        return jsonify({'success': True, 'short_url': short_url, 'qr_code': qr})
    return jsonify({'success': False, 'message': "No URL provided!"})


@app.route('/<key>')
def reroute(key: str):
    print(key)
    d = Database()
    url = d.get_url(key)
    if url:
        if "https://" not in url:
            return redirect("https://"+url)
        else:
            return redirect(url)
    else:
        return render_template("404.html")


if __name__ == '__main__':
    app.run()
