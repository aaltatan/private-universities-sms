import nox


@nox.session(venv_backend="none")
def build(session: nox.Session) -> None:
    session.run(
        "npx",
        "tailwindcss",
        "-i",
        "./static/css/src/input.css",
        "-o",
        "./static/css/dist/styles.css",
        "--minify",
    )
    session.run("npx", "webpack", "--config", "webpack.config.js")
    session.run(
        "uv",
        "pip",
        "compile",
        "--no-annotate",
        "pyproject.toml",
        "--output-file",
        "requirements.txt",
    )
    session.run("rm", "htmlcov", "-rf")
    session.run("rm", ".coverage")
    session.run("rm", "-rf", "__pycache__")
    session.run("rm", "-rf", ".pytest_cache")
