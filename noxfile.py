import nox


@nox.session(venv_backend="none")
def build(session: nox.Session) -> None:
    session.run("npm", "run", "build")
    session.run(
        "uv",
        "pip",
        "compile",
        "--no-annotate",
        "pyproject.toml",
        "--output-file",
        "requirements.txt",
    )
