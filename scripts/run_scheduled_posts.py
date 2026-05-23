#!/usr/bin/env python3
"""Publish any LinkedIn posts in the queue whose scheduled time has arrived.

Reads `posts/scheduled/queue.json`. For each entry where
`status == "pending"` and `scheduled_at <= now`, shells out to
`scripts/linkedin_post.py` with the right flags, captures the HTTP
result, and updates the queue entry to `published` (with post_id and
published_at) or `failed` (with error).

Designed to be invoked by:
  - a cron job:   `* * * * * cd /path/to/repo && python3 scripts/run_scheduled_posts.py`
  - a GitHub Actions cron workflow (runs every N minutes)
  - manually:     `python3 scripts/run_scheduled_posts.py`
  - foreground:   `python3 scripts/run_scheduled_posts.py --watch --interval 60`

Requires `LINKEDIN_ACCESS_TOKEN` and `LINKEDIN_AUTHOR_URN` to be set
in the environment.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
QUEUE_PATH = REPO_ROOT / "posts" / "scheduled" / "queue.json"
PUBLISH_SCRIPT = REPO_ROOT / "scripts" / "linkedin_post.py"


def load_queue() -> dict:
    if not QUEUE_PATH.exists():
        return {"version": 1, "entries": []}
    raw = QUEUE_PATH.read_text() or "{}"
    data = json.loads(raw) if raw.strip() else {}
    data.setdefault("version", 1)
    data.setdefault("entries", [])
    return data


def save_queue(data: dict) -> None:
    QUEUE_PATH.parent.mkdir(parents=True, exist_ok=True)
    QUEUE_PATH.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n")


def due_entries(queue: dict, now: datetime) -> list[dict]:
    due = []
    for e in queue["entries"]:
        if e.get("status") != "pending":
            continue
        when = datetime.fromisoformat(e["scheduled_at"])
        if when.tzinfo is None:
            when = when.replace(tzinfo=timezone.utc)
        if when <= now:
            due.append(e)
    return due


def publish_entry(entry: dict) -> tuple[bool, str, str | None]:
    """Return (success, raw_output, post_id_or_None)."""
    draft_path = entry["draft_path"]
    if not Path(draft_path).is_absolute():
        draft_path = str(REPO_ROOT / draft_path)

    cmd = ["python3", str(PUBLISH_SCRIPT), draft_path, "--slug", entry["slug"]]
    if entry.get("image"):
        image = entry["image"]
        if not Path(image).is_absolute():
            image = str(REPO_ROOT / image)
        cmd.extend(["--image", image])
    elif entry.get("carousel_dir"):
        carousel = entry["carousel_dir"]
        if not Path(carousel).is_absolute():
            carousel = str(REPO_ROOT / carousel)
        cmd.extend(["--carousel-dir", carousel])
    if entry.get("image_alt"):
        cmd.extend(["--image-alt", entry["image_alt"]])

    result = subprocess.run(cmd, capture_output=True, text=True)
    output = (result.stdout or "") + (result.stderr or "")
    if result.returncode != 0:
        return False, output, None

    # linkedin_post.py prints "HTTP <code>" then the response body.
    http_match = re.search(r"HTTP (\d+)", output)
    code = int(http_match.group(1)) if http_match else 0
    if not (200 <= code < 300):
        return False, output, None

    post_id = None
    id_match = re.search(r'"id"\s*:\s*"([^"]+)"', output)
    if id_match:
        post_id = id_match.group(1)
    return True, output, post_id


def run_once(dry_run: bool = False, verbose: bool = True) -> int:
    queue = load_queue()
    now = datetime.now(timezone.utc)
    due = due_entries(queue, now)
    if not due:
        if verbose:
            print(f"[{now.isoformat()}] no entries due.")
        return 0

    if dry_run:
        for e in due:
            print(f"[dry-run] would publish {e['id']} (scheduled {e['scheduled_at']})")
        return 0

    token = os.environ.get("LINKEDIN_ACCESS_TOKEN")
    author = os.environ.get("LINKEDIN_AUTHOR_URN")
    if not token or not author:
        print(
            "ERROR: LINKEDIN_ACCESS_TOKEN and LINKEDIN_AUTHOR_URN must be set; "
            "leaving due entries pending.",
            file=sys.stderr,
        )
        return 2

    failures = 0
    for entry in due:
        if verbose:
            print(f"[{now.isoformat()}] publishing {entry['id']} …")
        ok, output, post_id = publish_entry(entry)
        ts = datetime.now(timezone.utc).isoformat()
        if ok:
            entry["status"] = "published"
            entry["published_at"] = ts
            entry["post_id"] = post_id
            entry["error"] = None
            if verbose:
                print(f"  -> published (post_id={post_id})")
        else:
            entry["status"] = "failed"
            entry["error"] = output.strip()[-500:]
            failures += 1
            if verbose:
                print(f"  -> FAILED:\n{output}")
        save_queue(queue)

    return 1 if failures else 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dry-run", action="store_true", help="List due entries; do not publish.")
    p.add_argument(
        "--watch",
        action="store_true",
        help="Loop forever, sleeping --interval seconds between checks.",
    )
    p.add_argument("--interval", type=int, default=60, help="Seconds between checks in --watch mode.")
    p.add_argument("--quiet", action="store_true", help="Suppress 'no entries due' chatter.")
    args = p.parse_args()

    if args.watch:
        while True:
            run_once(dry_run=args.dry_run, verbose=not args.quiet)
            time.sleep(max(5, args.interval))
    return run_once(dry_run=args.dry_run, verbose=not args.quiet)


if __name__ == "__main__":
    sys.exit(main())
