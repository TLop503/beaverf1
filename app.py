import json
import feedparser
import requests

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

def load_blog_posts():
    with open('static/blog_posts.json', 'r') as f:
        return json.load(f)

# Define routes
@app.route('/')
def index():
    # You can pass data to your template here if needed
    return render_template('index.html')

@app.route('/score_blog')
def score_blog():
    # Your score blog page logic here
    blog_posts = load_blog_posts()
    blog_posts = reversed(blog_posts)
    return render_template('score_blog.html', blog_posts=blog_posts)

@app.route('/post/<int:post_id>')
def post_detail(post_id):
    # Fetch the post with the specified ID from the JSON data
    blog_posts = load_blog_posts()
    post = next((post for post in blog_posts if post['id'] == post_id), None)
    
    if post:
        return render_template('post_detail.html', post=post)
    else:
        return 'Post not found', 404

@app.route('/rules')
def rules():
    # Your rules page logic here
    return render_template('rules.html')

@app.route('/my_team')
def my_team():
    # Your rules page logic here
    return render_template('team.html')

@app.route('/export')
def export():
    return render_template('export_data.html')

@app.route('/rss_feed')
def rss_feed():
    # URL of the RSS feed you want to fetch
    rss_url = 'https://www.formula1.com/en/latest/all.xml'

    # Fetch and parse the RSS feed
    feed = feedparser.parse(rss_url)

    # Extract relevant information from the feed entries
    entries = []
    for entry in feed.entries:
        entry_data = {
            'title': entry.title,
            'link': entry.link,
            'description': entry.description,
            # Add more fields as needed
        }
        entries.append(entry_data)

    # Render a template with the RSS feed data
    return render_template('rss_feed.html', entries=entries)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('user')
        password = request.form.get('pass')
        
        # Validate form data
        if not user or not password:
            return jsonify({'Error': 'Please provide both username and password'}), 400
        
        # Make POST request to login endpoint
        response = requests.post('http://localhost:5002/login', json={'user': user, 'pass': password})
        if response.status_code == 200:
            return jsonify({'Message': 'Login successful'}), 200
        elif response.status_code == 404:
            return jsonify({'Error': 'User does not exist'}), 404
        elif response.status_code == 401:
            return jsonify({'Error': 'Incorrect password'}), 401
        else:
            return jsonify({'Error': 'Failed to login'}), 500
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form.get('user')
        password = request.form.get('pass')
        
        # Validate form data
        if not user or not password:
            return jsonify({'Error': 'Please provide both username and password'}), 400
        
        # Make POST request to login endpoint
        response = requests.post('http://localhost:5001/register', json={'user': user, 'pass': password})
        if response.status_code == 201:
            return jsonify({'Message': 'Registration successful'}), 200
        elif response.status_code == 409:
            return jsonify({'Error': 'User already exists'}), 404
        elif response.status_code == 400:
            return jsonify({'Error': 'Missing info'}), 400
        else:
            return jsonify({'Error': 'Failed to register with status code', 'code' : response.status_code}), 500
    
    return render_template('register.html')


# Run the application
if __name__ == '__main__':
    app.run(debug=True)
