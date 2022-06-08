from branchdiff import BranchDiff
import git

repo = git.Repo(".")
df = BranchDiff(repo, "master", "develop")
df.get_html_diff("README.rst", "html_diff.html")
