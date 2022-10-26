"""
Requirements.txt
    pygithub==1.56
    secretbox==2.7.0

.env contents:
    GITHUB_TOKEN = [some token with unknown requirements, smile.]
    BASE_URL = [GitHub api base url]
    SEARCH_FOR = [name of branch to find, case insensitive]
    LOGGING_LEVEL = [level, default INFO]

"""
from __future__ import annotations

import csv
import logging
import time
from io import StringIO
from typing import Sequence

from github import Github
from secretbox import SecretBox

FILENAME = "find-branch-report"
logger = logging.getLogger()


def search_all_orgs(client: Github, search_for: str) -> list[dict[str, str]]:
    """Search all orgs and repos within for branch matching `search_for`."""
    good, is_default, is_exists, archived, total_org, total_repo = 0, 0, 0, 0, 0, 0
    reports: list[dict[str, str]] = []

    # Off to the races! 三三ᕕ( ᐛ )ᕗ

    for org in client.get_organizations():
        logger.info("Organization start: %s", org.login)
        pause_for_ratelimit(client)
        total_org += 1
        report = {"org": org.login, "org_html_url": org.html_url, "actions": "none"}

        for repo in org.get_repos("all"):
            report["repo"] = repo.name
            report["repo_html_url"] = repo.html_url
            pause_for_ratelimit(client)
            total_repo += 1

            if repo.archived:
                archived += 1
                logger.info("REPO: %s - Archived", repo.name)

            elif repo.default_branch.lower() == search_for:
                is_default += 1
                report["actions"] = "Change default branch"
                reports.append(report)
                logger.info("REPO: %s - Default needs to change", repo.name)

            elif [br for br in repo.get_branches() if br.name.lower() == search_for]:
                is_exists += 1
                report["actions"] = "Remove old branch"
                reports.append(report)
                logger.info("REPO: %s - Exists but not default", repo.name)

            else:
                good += 1
                logger.info("REPO: %s - No action needed", repo.name)

    logger.info("Discovered %s orgs", total_org)
    logger.info("Discovered %s repos", total_repo)
    logger.info("No actions: %s", good)
    logger.info("Repo was Archived: %s", archived)
    logger.info("'%s' branch is default: %s", search_for, is_default)
    logger.info("'%s' branch was found: %s", search_for, is_exists)

    return reports


def pause_for_ratelimit(client: Github) -> None:
    """Sleeps if ratelimit is reached."""
    remaining, total = client.rate_limiting
    reset = client.rate_limiting_resettime
    # Give ourselves some padding as branches could blindly use some.
    if remaining <= 20:
        logger.warning(
            "Ratelimit reached. %d remaining of %d, sleeping until %d",
            remaining,
            total,
            reset,
        )
        while int(time.time()) < reset:
            logger.info("Sleeping until %d (now: %d)", reset, time.time())
            time.sleep(60)
    else:
        logger.info("%s of %s requested used", remaining, total)


def to_csv_string(
    objs: Sequence[dict[str, str]],
    fieldnames: list[str] | None = None,
) -> str:
    """
    Convert an object to a CSV. All attributes are included by default
    Args:
        objs: Sequence of Base objects to convert
        fieldsnames: Optionally define which keys are used, extra will be ignored
    """
    if not objs:
        return ""

    csv_file = StringIO()
    if not fieldnames:
        fieldnames = list(objs[0].keys())
    dict_writer = csv.DictWriter(
        csv_file,
        fieldnames=fieldnames,
        extrasaction="ignore",
    )
    dict_writer.writeheader()
    dict_writer.writerows([row for row in objs])

    return csv_file.getvalue()


def write_to_file(filepath: str, content: str) -> None:
    """Write string to filename/path. Empty strings are ignored."""
    if not content:
        return
    with open(filepath, "w", encoding="utf-8") as outfile:
        outfile.write(content)


def set_logging(level: str) -> None:
    """Define a file and console log handler."""
    filehandler = logging.FileHandler(filename=f"{FILENAME}.log", mode="w")
    filehandler.setLevel(level)
    stderrhandler = logging.StreamHandler()
    stderrhandler.setLevel(level)
    logging.getLogger().setLevel(level)
    logging.getLogger().addHandler(filehandler)
    logging.getLogger().addHandler(stderrhandler)


def main() -> int:
    sb = SecretBox(auto_load=True)
    git_token = sb.get("GITHUB_TOKEN")
    base_url = sb.get("BASE_URL")
    search_for = sb.get("SEARCH_FOR").lower()
    logging_level = sb.get("LOGGING_LEVEL", "INFO")

    set_logging(logging_level)

    client = Github(base_url=base_url, login_or_token=git_token, per_page=100, retry=5)

    reports = search_all_orgs(client, search_for)

    output_string = to_csv_string(reports)
    write_to_file(f"{FILENAME}.csv", output_string)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
