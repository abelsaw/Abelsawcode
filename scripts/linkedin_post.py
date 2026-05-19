#!/usr/bin/env python3
"""Publish a draft post to LinkedIn via the v2 UGC Posts API.

Reads a draft markdown file produced by the hr-post-writer agent. The
publishable text is everything between `---POST---` and `---END---` markers.
If a --slug is provided, the script finds the matching `## Post N — <slug>`
section and extracts that post; otherwise the first ---POST--- block is used.

Env vars required:
  LINKEDIN_ACCESS_TOKEN  OAuth token with `w_member_social` scope
  LINKEDIN_AUTHOR_URN    `urn:li:person:<member_id>`
"""
import argparse
import json
import mimetypes
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

LINKEDIN_UGC_URL = "https://api.linkedin.com/v2/ugcPosts"
LINKEDIN_REGISTER_URL = "https://api.linkedin.com/v2/assets?action=registerUpload"
MAX_CHARS = 3000


def extract_post(raw: str, slug: str | None) -> tuple[str, str | None]:
    """Return (post_text, section_header) for the requested draft."""
    if slug:
        section_pattern = re.compile(
            rf"(##\s+(?:Post|Option)\s+\d+\s+[-–—]\s+{re.escape(slug)}\b.*?)(?=^##\s|\Z)",
            re.DOTALL | re.MULTILINE,
        )
        match = section_pattern.search(raw)
        if not match:
            sys.exit(f"ERROR: no draft section found for slug '{slug}'.")
        section = match.group(1)
        header = section.splitlines()[0].strip()
    else:
        section = raw
        header = None

    body_match = re.search(r"---POST---\s*(.*?)\s*---END---", section, re.DOTALL)
    if not body_match:
        sys.exit("ERROR: no '---POST--- ... ---END---' block found in draft.")
    return body_match.group(1).strip(), header


def register_image_upload(token: str, author_urn: str) -> tuple[str, str]:
    """Register an image upload; return (upload_url, asset_urn)."""
    body = {
        "registerUploadRequest": {
            "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
            "owner": author_urn,
            "serviceRelationships": [
                {
                    "relationshipType": "OWNER",
                    "identifier": "urn:li:userGeneratedContent",
                }
            ],
        }
    }
    req = urllib.request.Request(
        LINKEDIN_REGISTER_URL,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        },
        method="POST",
    )
    with urllib.request.urlopen(req) as r:
        payload = json.loads(r.read().decode("utf-8"))
    value = payload["value"]
    upload_url = value["uploadMechanism"][
        "com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"
    ]["uploadUrl"]
    return upload_url, value["asset"]


def upload_image_binary(upload_url: str, token: str, image_path: Path) -> None:
    content_type = mimetypes.guess_type(str(image_path))[0] or "image/png"
    data = image_path.read_bytes()
    req = urllib.request.Request(
        upload_url,
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": content_type,
        },
        method="PUT",
    )
    with urllib.request.urlopen(req) as r:
        if not (200 <= r.status < 300):
            raise RuntimeError(f"image upload failed: HTTP {r.status}")


def post_to_linkedin(
    text: str,
    token: str,
    author_urn: str,
    image_path: Path | None = None,
    image_alt: str = "",
) -> tuple[int, str]:
    share_content: dict = {
        "shareCommentary": {"text": text},
        "shareMediaCategory": "NONE",
    }

    if image_path is not None:
        upload_url, asset_urn = register_image_upload(token, author_urn)
        upload_image_binary(upload_url, token, image_path)
        share_content["shareMediaCategory"] = "IMAGE"
        share_content["media"] = [
            {
                "status": "READY",
                "description": {"text": image_alt or text[:200]},
                "media": asset_urn,
                "title": {"text": image_alt[:100] if image_alt else "Post image"},
            }
        ]

    body = {
        "author": author_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {"com.linkedin.ugc.ShareContent": share_content},
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }
    req = urllib.request.Request(
        LINKEDIN_UGC_URL,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, r.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="replace")
    except urllib.error.URLError as e:
        return 0, f"Network error: {e.reason}"


def mark_published(draft_path: Path, section_header: str | None, post_id: str) -> None:
    raw = draft_path.read_text()
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    note = f"- **Status:** published\n- **LinkedIn post ID:** {post_id}\n- **Published at:** {timestamp}\n"

    if section_header:
        def replace(match: re.Match[str]) -> str:
            section = match.group(0)
            section = re.sub(
                r"-\s+\*\*Status:\*\*\s+draft",
                "- **Status:** published",
                section,
                count=1,
            )
            if "**LinkedIn post ID:**" not in section:
                section = section.rstrip() + f"\n- **LinkedIn post ID:** {post_id}\n- **Published at:** {timestamp}\n"
            return section

        new_raw = re.sub(
            rf"({re.escape(section_header)}\n.*?)(?=^##\s|\Z)",
            replace,
            raw,
            count=1,
            flags=re.DOTALL | re.MULTILINE,
        )
    else:
        new_raw = raw.rstrip() + f"\n\n{note}"

    draft_path.write_text(new_raw)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("draft_path", help="Path to a draft markdown file.")
    p.add_argument("--slug", help="Post slug from the section header. If omitted, the first ---POST--- block is used.")
    p.add_argument("--image", help="Optional path to a PNG/JPG image to attach.")
    p.add_argument("--image-alt", default="", help="Alt text for the attached image (accessibility).")
    p.add_argument("--dry-run", action="store_true", help="Print what would be posted; do not call the API.")
    args = p.parse_args()

    draft_path = Path(args.draft_path)
    if not draft_path.is_file():
        sys.exit(f"ERROR: draft file not found: {draft_path}")

    text, section_header = extract_post(draft_path.read_text(), args.slug)

    if not text:
        sys.exit("ERROR: extracted post body is empty.")
    if len(text) > MAX_CHARS:
        sys.exit(f"ERROR: post is {len(text)} chars; LinkedIn limit is {MAX_CHARS}.")

    image_path = None
    if args.image:
        image_path = Path(args.image)
        if not image_path.is_file():
            sys.exit(f"ERROR: image file not found: {image_path}")

    if args.dry_run:
        print("=== DRY RUN ===")
        if section_header:
            print(f"Section: {section_header}")
        print(f"Length: {len(text)} chars")
        word_count = len(text.split())
        print(f"Words: {word_count}")
        if image_path:
            print(f"Image: {image_path} ({image_path.stat().st_size} bytes)")
            if args.image_alt:
                print(f"Alt: {args.image_alt}")
        print("---")
        print(text)
        print("---")
        print("No API call made.")
        return 0

    token = os.environ.get("LINKEDIN_ACCESS_TOKEN")
    author = os.environ.get("LINKEDIN_AUTHOR_URN")
    if not token or not author:
        sys.exit(
            "ERROR: LINKEDIN_ACCESS_TOKEN and LINKEDIN_AUTHOR_URN must be set. "
            "See .env.example or invoke the linkedin-publisher agent for setup steps."
        )
    if not author.startswith("urn:li:person:"):
        sys.exit(f"ERROR: LINKEDIN_AUTHOR_URN must look like 'urn:li:person:<id>', got: {author}")

    status, response = post_to_linkedin(text, token, author, image_path, args.image_alt)
    print(f"HTTP {status}")
    print(response)

    if 200 <= status < 300:
        try:
            body = json.loads(response)
            post_id = body.get("id", "unknown")
        except json.JSONDecodeError:
            post_id = "unknown"
        mark_published(draft_path, section_header, post_id)
        print(f"Marked draft as published in {draft_path}.")
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
