import nox

nox.options.sessions = ["lint"]


PYTHON_VERSIONS = ["3.9"]


@nox.session(python=PYTHON_VERSIONS)
def lint(session):
    session.install("ruff==0.6.3")
    session.run("ruff", "check")


@nox.session(python=PYTHON_VERSIONS)
def test(session):
    session.install(".[test]")
    session.run("pytest", "--cov=file_manager", "tests/")


@nox.session(python=PYTHON_VERSIONS)
def test_no_remote(session):
    session.install(".[test]")
    session.run("pytest", "--cov=file_manager", "tests/", "-m", "not remote")
