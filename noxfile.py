import nox

nox.options.sessions = ["format", "test"]
nox.options.default_venv_backend = "venv"
nox.options.error_on_missing_interpreters = True
nox.options.error_on_external_run = True


@nox.session
def format(session):
    """Format source code."""
    session.install("isort", "black")
    session.run("isort", ".")
    session.run("black", ".")


@nox.session
def test(session):
    """Run tests."""
    session.install("pytest")
    session.run("pytest")


@nox.session
def lock(session):
    """Update lockfiles."""
    session.install("conda-lock")
    session.run("conda-lock", "--strip-auth")
