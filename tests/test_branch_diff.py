from branch_diff import __version__
from branch_diff import BranchDiff
import git


def test_version():
    assert __version__ == "0.1.0"


def test_branch_diff():
    repo = git.Repo(".")
    df = BranchDiff(repo, "master", "develop")
    print(df.first_branch, df.second_branch)


def test_get_diff():
    repo = git.Repo(".")
    df = BranchDiff(repo, "master", "develop")
    print(df.get_html_diff("README.rst", "html_diff.html"))
