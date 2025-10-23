# få sqlite3 fra biblioteket
import sqlite3
# få flask fra venv biblioteket
from flask import Flask, render_template, abort, request

app = Flask(__name__)
# database navn
DB_PATH = "blog.db"

# funksjon for å håndtere 0 posts
def create_db():
    with sqlite3.connect(DB_PATH) as con:
        con.execute(
            "CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, content TEXT NOT NULL)"
        )
        con.commit()

# funksjon for å få alle posts
def fetch_all_posts():
    # koble til databasen
    with sqlite3.connect(DB_PATH) as con:
        con.row_factory = sqlite3.Row
        rows = con.execute(
            "SELECT id, title, content FROM posts ORDER BY id DESC;"
        ).fetchall()
        # få alle posts
        return [[r["id"], r["title"], r["content"]] for r in rows]

# funksjon for å få posten
def fetch_post_by_id(post_id: int):
    # koble til databasen
    with sqlite3.connect(DB_PATH) as con:
        con.row_factory = sqlite3.Row
        row = con.execute(
            "SELECT id, title, content FROM posts WHERE id = ?",
            (post_id,)
        ).fetchone()
        if row is None:
            return None
        # få posten
        return [row["id"], row["title"], row["content"]]

# håndtere hjem siden
@app.get("/")
def index():
    posts = fetch_all_posts()
    return render_template("index.html", posts=posts)

# funksjon for å håndtere fjerning av post id
def delete_post_by_id(post_id: int):
    # koble til databasen
    with sqlite3.connect(DB_PATH) as con:
        con.row_factory = sqlite3.Row
        con.execute(
            "DELETE FROM posts WHERE id = ?",
            (post_id,)
        )
        con.commit()
        return True

# funksjon for å håndtere laging av post id
def add_post(title: str, content: str):
    # koble til databasen
    with sqlite3.connect(DB_PATH) as con:
        con.row_factory = sqlite3.Row
        # lag posten
        con.execute(
            "INSERT INTO posts (title, content) VALUES (?, ?)",
            (title, content)
        )
        con.commit()
        
        last_id = con.execute("SELECT last_insert_rowid()").fetchone()
        return fetch_post_by_id(last_id[0])

# håndtere post siden
@app.route("/post/<int:post_id>")
def post_detail(post_id: int) -> str:
    # få post
    post = fetch_post_by_id(post_id)

    # håndtere ugyldig post id
    if not post:
        abort(404)

    return render_template("post.html", post=post)

# håndtere delete post siden
@app.delete("/del/post/<int:post_id>")
def del_post_detail(post_id: int) -> str:
    # slett post
    del_post = delete_post_by_id(post_id)

    return render_template("del_post.html", del_post=del_post)

# håndtere add post siden
@app.post("/add/post")
def add_post_detail():
    title = request.form.get("Title", "Ny post")
    content = request.form.get("Content", "<p>Ny</p>")

    add_post_result = add_post(title, content)

    return render_template("add_post.html", add_post=add_post_result)

# håndtere 404 siden
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# håndtere 502 siden
@app.errorhandler(502)
def bad_gateway(e):
    return render_template("502.html"), 502

# kjør appen i debug mode
if __name__ == "__main__":
    create_db()
    app.run(debug=True)