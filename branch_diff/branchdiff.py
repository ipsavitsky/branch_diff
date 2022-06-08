import difflib
import git
import logging


class BranchDiff:
    def __init__(self, repo: git.Repo, first_branch: str, second_branch: str):
        self.repo = repo
        self.first_branch = first_branch
        self.second_branch = second_branch

    def get_html_diff(self, filename: str, htmldifffilename: str):
        logging.debug("get_diff(%s)", filename)
        logging.debug("first_branch: %s", self.first_branch)
        initial_branch = self.repo.active_branch.name

        try:
            if self.first_branch != self.repo.active_branch.name:
                self.repo.heads[self.first_branch].checkout()
        except git.GitCommandError as e:
            logging.error("%s", e)
            return

        try:
            with open(filename, "r") as first_file:
                first_file_contains = first_file.read()
        except FileNotFoundError as e:
            logging.error("%s", e)
            self.repo.heads[initial_branch].checkout()
            return

        try:
            if self.second_branch != self.repo.active_branch.name:
                self.repo.heads[self.second_branch].checkout()
        except git.GitCommandError as e:
            logging.error("%s", e)
            self.repo.heads[initial_branch].checkout()
            return

        try:
            with open(filename, "r") as second_file:
                second_file_contains = second_file.read()
        except FileNotFoundError as e:
            logging.error("%s", e)
            self.repo.heads[initial_branch].checkout()
            return

        self.repo.heads[initial_branch].checkout()

        diff = difflib.HtmlDiff().make_file(
            first_file_contains.split("\n"),
            second_file_contains.split("\n"),
            self.first_branch + ":" + filename,
            self.second_branch + ":" + filename,
        )

        with open(htmldifffilename, "w") as diff_file:
            diff_file.write(diff)
