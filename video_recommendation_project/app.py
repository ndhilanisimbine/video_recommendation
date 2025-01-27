from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS
from ml_model import recommend_videos

app = Flask(__name__)
CORS(app)

# Initialize the database
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            likes INTEGER DEFAULT 0,
            views INTEGER DEFAULT 0
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interactions (
            user_id TEXT,
            video_id INTEGER,
            action TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/upload', methods=['POST'])
def upload_video():
    title = request.form['title']
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO videos (title, likes, views) VALUES (?, 0, 0)", (title,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Video uploaded successfully!"})

@app.route('/feed', methods=['GET'])
def get_feed():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM videos")
    videos = cursor.fetchall()
    conn.close()
    return jsonify(videos)

@app.route('/like/<int:video_id>', methods=['POST'])
def like_video(video_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE videos SET likes = likes + 1 WHERE id = ?", (video_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Video liked!"})

@app.route('/recommend/<user_id>', methods=['GET'])
def recommend(user_id):
    recommendations = recommend_videos(user_id)
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)
