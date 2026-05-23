#!/usr/bin/env python3
"""Bundle the 30 posts + carousels into per-set folders.

Reads POSTS from scripts/build_30_posts.py and produces:

  posts/sets/2026-05-22/
    INDEX.md
    option-01-{slug}/
      post.md           — post body + metadata + slide table
      slide-1.png … slide-5.png — carousel (1080×1080)
      cover.png         — single-image version (no slide indicator)
    option-02-{slug}/
      …

Each option folder is fully self-contained — open it, read post.md,
upload the slides, publish.
"""
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build_30_posts import POSTS, DATE, REPO


def main() -> int:
    out_root = REPO / "posts" / "sets" / DATE
    out_root.mkdir(parents=True, exist_ok=True)

    index_lines = [
        f"# {DATE} — 30-post batch",
        "",
        "30 LinkedIn posts with 5-slide bold-editorial carousels. Each option is",
        "in its own folder, ready to publish independently — open `post.md`,",
        "copy the body, upload `slide-1.png` through `slide-5.png` (or `cover.png`",
        "for a single-image post).",
        "",
        "Total: 30 posts, 150 carousel slides, 30 cover images.",
        "",
        "| # | Folder | Theme | Accent | Words |",
        "|---|---|---|---|---|",
    ]

    for i, (slug, theme, accent, sources, slides, body) in enumerate(POSTS, 1):
        folder_name = f"option-{i:02d}-{slug}"
        folder = out_root / folder_name
        folder.mkdir(parents=True, exist_ok=True)

        src_carousel = REPO / "posts" / "drafts" / "carousels" / f"{DATE}-option-{i}"
        for slide in sorted(src_carousel.glob("slide-*.png")):
            shutil.copy(slide, folder / slide.name)

        src_cover = REPO / "posts" / "drafts" / "images" / f"{DATE}-option-{i}.png"
        shutil.copy(src_cover, folder / "cover.png")

        wc = len(body.split())
        post_md = [
            f"# Option {i} — {slug}",
            "",
            f"- **Theme:** {theme}",
            f"- **Accent:** {accent}",
            f"- **Sources:** {sources}",
            f"- **Word count:** {wc}",
            "",
            "## Post body (≤50 words — copy into LinkedIn as-is)",
            "",
            "```",
            body,
            "```",
            "",
            "## Carousel slides (upload in this order)",
            "",
            "| # | Tag | Headline |",
            "|---|---|---|",
        ]
        for j, (tag, headline) in enumerate(slides, 1):
            post_md.append(f"| {j} | {tag} | {headline} |")
        post_md.extend([
            "",
            "## Files in this folder",
            "",
            "- `post.md` — this file",
            "- `slide-1.png` … `slide-5.png` — 5-slide carousel (1080×1080)",
            "- `cover.png` — single-image version (no slide indicator)",
        ])
        (folder / "post.md").write_text("\n".join(post_md) + "\n")

        index_lines.append(
            f"| {i:02d} | [{folder_name}/]({folder_name}/) | {theme} | {accent} | {wc} |"
        )

    index_lines.extend([
        "",
        "## How to publish a single post",
        "",
        "1. Open any `option-NN-{slug}/` folder.",
        "2. Open `post.md`. Copy the body inside the triple-backtick block.",
        "3. In LinkedIn, paste the body as your post text.",
        "4. Attach `slide-1.png` through `slide-5.png` as a multi-image post (or attach `cover.png` alone for a single image).",
        "5. Publish.",
        "",
        "## Reproducibility",
        "",
        "All 30 sets were generated from `scripts/build_30_posts.py` and bundled by",
        "`scripts/bundle_30_posts.py`. To regenerate, run both scripts in order.",
    ])
    (out_root / "INDEX.md").write_text("\n".join(index_lines) + "\n")

    file_count = sum(1 for _ in out_root.rglob("*") if _.is_file())
    print(f"Bundled {len(POSTS)} sets into {out_root}")
    print(f"Total files written: {file_count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
