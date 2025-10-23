import sqlite3
with sqlite3.connect("blog.db") as con:
    con.executescript("""
    CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL
    );
    
    INSERT INTO posts (title, content) VALUES
    ('Første innlegg', '<p>Hei og velkommen til mini-bloggen!</p>'),
    ('Flask-tips', '<ul><li>Bruk <code>url for</code></li><li>Arv fra 
    base.html</li></ul>'),
    ('Dagens sitat', '<blockquote>«Code is like humor. When you have to explain it, 
    it’s bad.»</blockquote>');
    """)