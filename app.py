from flask import *
from assets import Database

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/add_url', methods=['POST'])
def add_url():
    d = Database()
    url = request.json.get('url')  # Using JSON for AJAX compatibility
    if url:
        key = d.add_key(url)
        short_url = f"https://small.pythonanywhere.com/{key}"
        return jsonify({'success': True, 'short_url': short_url})
    return jsonify({'success': False, 'message': "No URL provided!"})


@app.route('/<key>')
def reroute(key: str):
    print(key)
    d = Database()
    url = d.get_url(key)
    if url:
        return redirect(url)
    else:
        abort(404)


if __name__ == '__main__':
    app.run()
