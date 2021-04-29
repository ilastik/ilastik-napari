from invoke import task


@task
def fmt(c):
    """Auto-format Python source files."""
    c.run("isort .")
    c.run("black .")


@task()
def test(c):
    """Run tests."""
    c.run("pytest", pty=True)
