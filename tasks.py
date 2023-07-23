from invoke import task


@task
def update_requirements(ctx):
    ctx.run("pip install -r requirements.txt --upgrade")


@task
def update_dev_requirements(ctx):
    ctx.run("pip install -r requirements-dev.txt --upgrade")


@task
def lint(ctx):
    ctx.run("flake8 --extend-ignore=E203,W503 --max-line-length=120 .")


@task
def lint_auto(ctx):
    ctx.run("autopep8 --in-place --aggressive --recursive --exclude venv .")


@task
def test(ctx):
    ctx.run("pytest")
