from app import create_app, db

app = create_app()

if __name__ == '__main__':
    import os
    from threading import Timer
    import webbrowser

    def open_browser():
        webbrowser.open_new("http://127.0.0.1:5000/login")

    # Bu koşul, sadece ana process için True olur, reload edileni engeller
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        Timer(1, open_browser).start()

    app.run(debug=True)
