import nox


@nox.session(venv_backend="none")
def build(session: nox.Session) -> None:
    session.run(
        "npx",
        "tailwindcss",
        "-i",
        "./assets/css/input.css",
        "-o",
        "./static/main.min.css",
        "--minify",
    )
    session.run(
        "npx",
        "webpack",
        "--config",
        "webpack.config.js",
        "--mode",
        "production",
    )
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
    session.run("rm", ".coverage", "-f")
    session.run("rm", "-rf", "__pycache__", "-f")
    session.run("rm", "-rf", ".pytest_cache", "-f")
