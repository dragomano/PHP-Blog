"""Show the last modification date of blog posts.

The date is taken from an explicit `update` (or `updated`) metadata key, if
present. Otherwise, the date of the last Git commit that touched the post is
used. Nothing is rendered when the post has never been modified after it was
published.
"""

import subprocess

from datetime import date, datetime, time, timezone
from typing import Optional

from mkdocs.plugins import event_priority


# Date of the last commit that modified the given file
def _git_date(path: str) -> Optional[datetime]:
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", path],
            capture_output=True,
            check=True,
            text=True
        )
    except (OSError, subprocess.SubprocessError):
        return None

    value = result.stdout.strip()
    if not value:
        return None

    try:
        return datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


# Normalize a metadata value to a timezone-aware datetime
def _to_datetime(value) -> Optional[datetime]:
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)

    if isinstance(value, date):
        return datetime.combine(value, time()).replace(tzinfo=timezone.utc)

    if isinstance(value, str):
        try:
            parsed = datetime.fromisoformat(value)
        except ValueError:
            return None

        return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)

    return None


@event_priority(-100)
def on_files(files, config):
    plugin = config.plugins.get("material/blog") or config.plugins.get("blog")
    if not plugin or not getattr(plugin, "blog", None):
        return files

    for post in plugin.blog.posts:
        dates = post.config.date
        if "updated" in dates:
            continue

        updated = _to_datetime(
            post.meta.get("update") or post.meta.get("updated")
        )
        if updated is None:
            updated = _git_date(post.file.abs_src_path)
        if updated is None or updated <= dates.created:
            continue

        dates["updated"] = updated

    return files
