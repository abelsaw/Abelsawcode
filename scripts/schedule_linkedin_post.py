#!/usr/bin/env python3
"""Manage the LinkedIn scheduled-post queue.

Entries live in `posts/scheduled/queue.json`. Each entry pairs a draft +
slug with an optional image (or carousel directory) and a scheduled UTC
timestamp. A separate script — `scripts/run_scheduled_posts.py` — reads
the queue and actually calls the LinkedIn API when entries come due.

Usage:
  schedule_linkedin_post.py add DRAFT_PATH --slug SLUG --when WHEN \
      [--image PATH | --carousel-dir DIR] [--image-alt TEXT] [--note TEXT]
  schedule_linkedin_post.py list [--pending|--all|--published|--failed]
  schedule_linkedin_post.py cancel ENTRY_ID
  schedule_linkedin_post.py show ENTRY_ID

WHEN accepts ISO 8601 with an explicit offset (e.g. `2026-05-24T09:00:00+02:00`
or `2026-05-24T07:00:00Z`). A naive `YYYY-MM-DDTHH:MM` is interpreted as UTC.
"""
import argparse
import json
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
QUEUE_PATH = REPO_ROOT / "posts" / "scheduled" / "queue.json"
QUEUE_VERSION = 1


def load_queue() -> dict:
    if not QUEUE_PATH.exists():
        return {"version": QUEUE_VERSION, "entries": []}
    raw = QUEUE_PATH.read_text() or "{}"
    data = json.loads(raw) if raw.strip() else {}
    data.setdefault("version", QUEUE_VERSION)
    data.setdefault("entries", [])
    return data


def save_queue(data: dict) -> None:
    QUEUE_PATH.parent.mkdir(parents=True, exist_ok=True)
    QUEUE_PATH.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n")


def parse_when(value: str) -> datetime:
    s = value.strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(s)
    except ValueError as e:
        sys.exit(f"ERROR: cannot parse --when '{value}': {e}")
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def validate_draft(draft_path: Path, slug: str) -> None:
    if not draft_path.is_file():
        sys.exit(f"ERROR: draft file not found: {draft_path}")
    raw = draft_path.read_text()
    section_pattern = re.compile(
        rf"##\s+(?:Post|Option)\s+\d+\s+[-–—]\s+{re.escape(slug)}\b",
        re.MULTILINE,
    )
    if not section_pattern.search(raw):
        sys.exit(
            f"ERROR: no draft section found for slug '{slug}' in {draft_path}."
        )
    section_match = re.search(
        rf"(##\s+(?:Post|Option)\s+\d+\s+[-–—]\s+{re.escape(slug)}\b.*?)(?=^##\s|\Z)",
        raw,
        re.DOTALL | re.MULTILINE,
    )
    body = section_match.group(1) if section_match else raw
    if "---POST---" not in body or "---END---" not in body:
        sys.exit(
            f"ERROR: slug '{slug}' has no '---POST--- … ---END---' block."
        )
    if re.search(r"-\s+\*\*Status:\*\*\s+(published|do-not-publish)", body):
        sys.exit(
            f"ERROR: slug '{slug}' is marked published or do-not-publish."
        )


def resolve_relative(path_value: str | None) -> Path | None:
    if not path_value:
        return None
    p = Path(path_value)
    if not p.is_absolute():
        p = (REPO_ROOT / p).resolve()
    return p


def relative_to_repo(p: Path) -> str:
    try:
        return str(p.relative_to(REPO_ROOT))
    except ValueError:
        return str(p)


def cmd_add(args: argparse.Namespace) -> int:
    draft_abs = resolve_relative(args.draft_path)
    if draft_abs is None:
        sys.exit("ERROR: DRAFT_PATH is required.")
    validate_draft(draft_abs, args.slug)

    if args.image and args.carousel_dir:
        sys.exit("ERROR: pass either --image or --carousel-dir, not both.")

    image_abs = resolve_relative(args.image)
    carousel_abs = resolve_relative(args.carousel_dir)
    if image_abs and not image_abs.is_file():
        sys.exit(f"ERROR: image file not found: {image_abs}")
    if carousel_abs:
        if not carousel_abs.is_dir():
            sys.exit(f"ERROR: carousel directory not found: {carousel_abs}")
        slides = sorted(carousel_abs.glob("slide-*.png"))
        if not slides:
            sys.exit(f"ERROR: no slide-*.png files in {carousel_abs}")
        if len(slides) > 9:
            sys.exit(
                f"ERROR: LinkedIn allows up to 9 images per post; found {len(slides)}."
            )

    when_utc = parse_when(args.when)
    now = datetime.now(timezone.utc)
    if when_utc <= now:
        sys.exit(
            f"ERROR: --when is in the past ({when_utc.isoformat()}). "
            f"Now is {now.isoformat()}."
        )

    queue = load_queue()
    for entry in queue["entries"]:
        if (
            entry.get("status") == "pending"
            and entry.get("draft_path") == relative_to_repo(draft_abs)
            and entry.get("slug") == args.slug
        ):
            sys.exit(
                f"ERROR: a pending entry already exists for this draft+slug "
                f"(id {entry['id']}, scheduled {entry['scheduled_at']}). "
                "Cancel it first if you want to reschedule."
            )

    entry_id = (
        when_utc.strftime("%Y%m%dT%H%M%SZ")
        + "-"
        + args.slug
        + "-"
        + uuid.uuid4().hex[:6]
    )
    entry = {
        "id": entry_id,
        "draft_path": relative_to_repo(draft_abs),
        "slug": args.slug,
        "image": relative_to_repo(image_abs) if image_abs else None,
        "carousel_dir": relative_to_repo(carousel_abs) if carousel_abs else None,
        "image_alt": args.image_alt or "",
        "scheduled_at": when_utc.isoformat(),
        "status": "pending",
        "created_at": now.isoformat(),
        "published_at": None,
        "post_id": None,
        "error": None,
        "note": args.note or "",
    }
    queue["entries"].append(entry)
    queue["entries"].sort(key=lambda e: e.get("scheduled_at") or "")
    save_queue(queue)

    print(f"Queued {entry_id}")
    print(f"  draft     : {entry['draft_path']}")
    print(f"  slug      : {entry['slug']}")
    if entry["image"]:
        print(f"  image     : {entry['image']}")
    if entry["carousel_dir"]:
        print(f"  carousel  : {entry['carousel_dir']}")
    print(f"  scheduled : {entry['scheduled_at']}  (UTC)")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    queue = load_queue()
    entries = queue["entries"]
    if args.pending:
        entries = [e for e in entries if e["status"] == "pending"]
    elif args.published:
        entries = [e for e in entries if e["status"] == "published"]
    elif args.failed:
        entries = [e for e in entries if e["status"] == "failed"]
    if not entries:
        print("(queue is empty)")
        return 0
    for e in entries:
        media = e["image"] or e["carousel_dir"] or "—"
        print(
            f"{e['status']:9s}  {e['scheduled_at']}  {e['id']}\n"
            f"           draft={e['draft_path']} slug={e['slug']}\n"
            f"           media={media}"
        )
        if e.get("error"):
            print(f"           error={e['error']}")
        if e.get("post_id"):
            print(f"           post_id={e['post_id']}")
    return 0


def cmd_cancel(args: argparse.Namespace) -> int:
    queue = load_queue()
    for e in queue["entries"]:
        if e["id"] == args.entry_id:
            if e["status"] != "pending":
                sys.exit(
                    f"ERROR: entry {args.entry_id} is {e['status']}, not pending."
                )
            e["status"] = "cancelled"
            e["error"] = "cancelled by user"
            save_queue(queue)
            print(f"Cancelled {args.entry_id}")
            return 0
    sys.exit(f"ERROR: entry not found: {args.entry_id}")


def cmd_show(args: argparse.Namespace) -> int:
    queue = load_queue()
    for e in queue["entries"]:
        if e["id"] == args.entry_id:
            print(json.dumps(e, indent=2))
            return 0
    sys.exit(f"ERROR: entry not found: {args.entry_id}")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    add = sub.add_parser("add", help="Queue a draft+slug for future posting.")
    add.add_argument("draft_path")
    add.add_argument("--slug", required=True)
    add.add_argument(
        "--when",
        required=True,
        help="ISO 8601 datetime (with offset or Z). Naive values are treated as UTC.",
    )
    add.add_argument("--image")
    add.add_argument("--carousel-dir")
    add.add_argument("--image-alt", default="")
    add.add_argument("--note", default="")
    add.set_defaults(func=cmd_add)

    lst = sub.add_parser("list", help="List queue entries.")
    g = lst.add_mutually_exclusive_group()
    g.add_argument("--pending", action="store_true")
    g.add_argument("--all", action="store_true")
    g.add_argument("--published", action="store_true")
    g.add_argument("--failed", action="store_true")
    lst.set_defaults(func=cmd_list)

    can = sub.add_parser("cancel", help="Cancel a pending entry by id.")
    can.add_argument("entry_id")
    can.set_defaults(func=cmd_cancel)

    sho = sub.add_parser("show", help="Print the full JSON for an entry.")
    sho.add_argument("entry_id")
    sho.set_defaults(func=cmd_show)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
