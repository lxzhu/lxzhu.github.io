"""Build a static site from src into docs."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import logging
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined, TemplateNotFound


LOGGER = logging.getLogger("pysite")
FRONT_MATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.DOTALL)


@dataclass
class Document:
	"""Model for a source page/post document."""

	source_path: Path
	source_root: Path
	kind: str
	category: str | None
	front_matter: dict[str, Any]
	body: str
	output_path: Path
	url: str
	layout_hint: str | None = None
	rendered_content: str = ""
	rendered_html: str = ""
	meta: dict[str, Any] = field(default_factory=dict)

	@property
	def stem(self) -> str:
		return self.source_path.stem

	@property
	def relative_source(self) -> Path:
		return self.source_path.relative_to(self.source_root)


def parse_front_matter(raw_text: str) -> tuple[dict[str, Any], str]:
	"""Return (front_matter_dict, body_without_front_matter)."""
	match = FRONT_MATTER_PATTERN.match(raw_text)
	if not match:
		return {}, raw_text

	front_matter_raw = match.group(1)
	body = raw_text[match.end() :]
	front_matter = yaml.safe_load(front_matter_raw) or {}
	if not isinstance(front_matter, dict):
		raise ValueError("Front matter must be a YAML mapping.")
	return front_matter, body


def load_data_model(data_dir: Path) -> dict[str, Any]:
	"""Load yaml/json files from _data into a nested dictionary."""
	data_model: dict[str, Any] = {}
	if not data_dir.exists():
		return data_model

	supported_suffixes = {".yml", ".yaml", ".json"}
	for file_path in sorted(data_dir.rglob("*")):
		if not file_path.is_file() or file_path.suffix.lower() not in supported_suffixes:
			continue

		relative = file_path.relative_to(data_dir)
		keys = list(relative.with_suffix("").parts)
		value = _load_data_file(file_path)
		_set_nested_value(data_model, keys, value)

	return data_model


def _load_data_file(file_path: Path) -> Any:
	if file_path.suffix.lower() == ".json":
		return json.loads(file_path.read_text(encoding="utf-8"))
	return yaml.safe_load(file_path.read_text(encoding="utf-8"))


def _set_nested_value(target: dict[str, Any], keys: list[str], value: Any) -> None:
	cursor = target
	for key in keys[:-1]:
		next_value = cursor.get(key)
		if not isinstance(next_value, dict):
			next_value = {}
			cursor[key] = next_value
		cursor = next_value
	cursor[keys[-1]] = value


def collect_posts(posts_dir: Path, src_root: Path, docs_root: Path) -> list[Document]:
	"""Collect markdown files under _posts/<category>/<post>.md."""
	documents: list[Document] = []
	if not posts_dir.exists():
		return documents

	for file_path in sorted(posts_dir.glob("*/*.md")):
		category = file_path.parent.name
		front_matter, body = parse_front_matter(file_path.read_text(encoding="utf-8"))
		output_path = docs_root / category / f"{file_path.stem}.html"
		url = f"/{category}/{file_path.stem}.html"
		documents.append(
			Document(
				source_path=file_path,
				source_root=src_root,
				kind="post",
				category=category,
				front_matter=front_matter,
				body=body,
				output_path=output_path,
				url=url,
				layout_hint=(front_matter.get("layout") or "post"),
			)
		)

	return documents


def collect_pages(pages_dir: Path, src_root: Path, docs_root: Path) -> list[Document]:
	"""Collect html/markdown files under _pages."""
	documents: list[Document] = []
	if not pages_dir.exists():
		return documents

	for file_path in sorted(pages_dir.rglob("*")):
		if not file_path.is_file() or file_path.suffix.lower() not in {".html", ".md"}:
			continue

		front_matter, body = parse_front_matter(file_path.read_text(encoding="utf-8"))
		relative = file_path.relative_to(pages_dir)
		stem_relative = relative.with_suffix("")

		if stem_relative.as_posix() == "index":
			output_path = docs_root / "index.html"
			url = "/"
		else:
			output_path = docs_root / "pages" / stem_relative.parent / f"{stem_relative.name}.html"
			url = f"/pages/{stem_relative.as_posix()}.html"

		layout_hint = front_matter.get("layout")
		if not layout_hint:
			if file_path.suffix.lower() == ".html":
				layout_hint = file_path.stem
			else:
				layout_hint = "page"

		documents.append(
			Document(
				source_path=file_path,
				source_root=src_root,
				kind="page",
				category=None,
				front_matter=front_matter,
				body=body,
				output_path=output_path,
				url=url,
				layout_hint=layout_hint,
			)
		)

	return documents


def resolve_layout_name(env: Environment, preferred: str | None, fallback: str | None) -> str | None:
	"""Return an existing layout template name using extension fallback."""

	def _first_existing(name: str | None) -> str | None:
		if not name:
			return None
		candidates = [name]
		if not name.endswith(".html"):
			candidates.append(f"{name}.html")
		for candidate in candidates:
			try:
				env.get_template(candidate)
			except TemplateNotFound:
				continue
			return candidate
		return None

	return _first_existing(preferred) or _first_existing(fallback)


def document_index_entry(document: Document) -> dict[str, Any]:
	"""Small metadata object exposed to templates via site model."""
	entry = dict(document.front_matter)
	entry.update(
		{
			"title": document.front_matter.get("title", document.stem),
			"url": document.url,
			"source": document.relative_source.as_posix(),
			"category": document.category,
			"kind": document.kind,
		}
	)
	return entry


def render_documents(
	env: Environment,
	documents: list[Document],
	site_model: dict[str, Any],
) -> None:
	"""Render each page/post with optional layout wrapping."""
	md_engine = markdown.Markdown(extensions=["extra", "tables", "fenced_code"])

	for document in documents:
		page_meta = dict(document.front_matter)
		page_meta.setdefault("title", document.stem)
		page_meta.setdefault("url", document.url)
		page_meta.setdefault("category", document.category)

		context = {
			"site": site_model,
			"data": site_model.get("data", {}),
			"page": page_meta,
			"post": page_meta if document.kind == "post" else None,
		}

		body_template = env.from_string(document.body)
		rendered_body = body_template.render(**context)
		document.rendered_content = rendered_body

		if document.source_path.suffix.lower() == ".md":
			rendered_html = md_engine.reset().convert(rendered_body)
		else:
			rendered_html = rendered_body

		layout_name = None
		if document.kind == "post":
			layout_name = resolve_layout_name(env, document.layout_hint, "post")
		else:
			html_default_fallback = "page"
			layout_name = resolve_layout_name(env, document.layout_hint, html_default_fallback)

		context["content"] = rendered_html

		if layout_name:
			LOGGER.debug("Rendering %s with layout %s", document.source_path, layout_name)
			layout_template = env.get_template(layout_name)
			document.rendered_html = layout_template.render(**context)
		else:
			LOGGER.debug("Rendering %s without layout", document.source_path)
			document.rendered_html = rendered_html


def write_documents(documents: list[Document]) -> None:
	"""Write rendered pages to destination files."""
	for document in documents:
		document.output_path.parent.mkdir(parents=True, exist_ok=True)
		document.output_path.write_text(document.rendered_html, encoding="utf-8")


def copy_static_assets(src_root: Path, docs_root: Path) -> None:
	"""Copy files from src that are not special content folders."""
	special_dirs = {"_posts", "_pages", "_layouts", "_includes", "_data"}
	for child in src_root.iterdir() if src_root.exists() else []:
		if child.name in special_dirs:
			continue
		target = docs_root / child.name
		if child.is_dir():
			shutil.copytree(child, target, dirs_exist_ok=True)
		else:
			target.parent.mkdir(parents=True, exist_ok=True)
			shutil.copy2(child, target)


def build_site(src_root: Path, docs_root: Path, clean: bool = False) -> int:
	"""Compile site from src into docs."""
	posts_dir = src_root / "_posts"
	pages_dir = src_root / "_pages"
	layouts_dir = src_root / "_layouts"
	includes_dir = src_root / "_includes"
	data_dir = src_root / "_data"

	if not src_root.exists():
		LOGGER.error("Source directory does not exist: %s", src_root)
		return 2

	if clean and docs_root.exists():
		LOGGER.info("Cleaning output directory: %s", docs_root)
		shutil.rmtree(docs_root)
	docs_root.mkdir(parents=True, exist_ok=True)

	env = Environment(
		loader=FileSystemLoader([str(layouts_dir), str(includes_dir)]),
		autoescape=True,
		undefined=StrictUndefined,
		trim_blocks=True,
		lstrip_blocks=True,
	)

	data_model = load_data_model(data_dir)
	posts = collect_posts(posts_dir, src_root, docs_root)
	pages = collect_pages(pages_dir, src_root, docs_root)

	site_model = {
		"data": data_model,
		"posts": [document_index_entry(item) for item in posts],
		"pages": [document_index_entry(item) for item in pages],
	}

	render_documents(env, posts + pages, site_model)
	write_documents(posts + pages)
	copy_static_assets(src_root, docs_root)

	LOGGER.info("Build complete: %s posts, %s pages -> %s", len(posts), len(pages), docs_root)
	return 0


def clean_docs(docs_root: Path) -> int:
	"""Delete and recreate the docs folder."""
	if docs_root.exists():
		LOGGER.info("Cleaning output directory: %s", docs_root)
		shutil.rmtree(docs_root)
	docs_root.mkdir(parents=True, exist_ok=True)
	LOGGER.info("Docs directory is ready: %s", docs_root)
	return 0


def preview_site(docs_root: Path) -> int:
	"""Serve docs folder on localhost:8000 in foreground."""
	if not docs_root.exists():
		LOGGER.error("Docs directory does not exist. Run build first: %s", docs_root)
		return 2

	server_command = [
		sys.executable,
		"-m",
		"http.server",
		"8000",
		"--bind",
		"127.0.0.1",
		"--directory",
		str(docs_root),
	]
	LOGGER.info("Preview server running at http://127.0.0.1:8000 (Ctrl+C to stop)")
	try:
		subprocess.run(server_command, check=True)
	except KeyboardInterrupt:
		LOGGER.info("Preview server stopped.")
		return 0
	except subprocess.CalledProcessError as exc:
		LOGGER.error("Preview server failed with exit code %s", exc.returncode)
		return exc.returncode
	return 0


def _run_git(repo_root: Path, args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
	"""Run a git command at repository root."""
	command = ["git", *args]
	return subprocess.run(
		command,
		cwd=repo_root,
		check=check,
		text=True,
		capture_output=True,
	)


def pack_site(commit_message: str) -> tuple[int, bool]:
	"""Stage and commit all repository changes without pushing."""
	repo_root = Path(__file__).resolve().parent.parent
	if not (repo_root / ".git").exists():
		LOGGER.error("Cannot pack: .git not found in %s", repo_root)
		return 2, False

	try:
		_run_git(repo_root, ["add", "-A"], check=True)
		staged_diff = _run_git(repo_root, ["diff", "--cached", "--quiet"], check=False)

		if staged_diff.returncode == 0:
			LOGGER.info("Nothing to pack: no changes to commit.")
			return 0, False

		_run_git(repo_root, ["commit", "-m", commit_message], check=True)
		LOGGER.info("Pack complete: committed changes with message: %s", commit_message)
		return 0, True
	except subprocess.CalledProcessError as exc:
		stderr = (exc.stderr or "").strip()
		stdout = (exc.stdout or "").strip()
		if stderr:
			LOGGER.error("Git command failed: %s", stderr)
		elif stdout:
			LOGGER.error("Git command failed: %s", stdout)
		else:
			LOGGER.error("Git command failed with exit code %s", exc.returncode)
		return exc.returncode or 1, False


def publish_site(src_root: Path, docs_root: Path, commit_message: str, clean: bool = False) -> int:
	"""Build site, pack changes, and push to GitHub when there is something to publish."""
	build_exit = build_site(src_root=src_root, docs_root=docs_root, clean=clean)
	if build_exit != 0:
		return build_exit

	pack_exit, has_new_commit = pack_site(commit_message=commit_message)
	if pack_exit != 0:
		return pack_exit

	if not has_new_commit:
		LOGGER.info("Nothing to publish: no new commit created.")
		return 0

	repo_root = Path(__file__).resolve().parent.parent
	try:

		_run_git(repo_root, ["push"], check=True)
		LOGGER.info("Publish complete: pushed current branch to remote.")
		return 0
	except subprocess.CalledProcessError as exc:
		stderr = (exc.stderr or "").strip()
		stdout = (exc.stdout or "").strip()
		if stderr:
			LOGGER.error("Git command failed: %s", stderr)
		elif stdout:
			LOGGER.error("Git command failed: %s", stdout)
		else:
			LOGGER.error("Git command failed with exit code %s", exc.returncode)
		return exc.returncode or 1


def _add_logging_argument(parser: argparse.ArgumentParser) -> None:
	parser.add_argument(
		"--verbose",
		action="store_true",
		help="Enable debug logging.",
	)


def _add_src_docs_arguments(parser: argparse.ArgumentParser) -> None:
	parser.add_argument(
		"--src",
		type=Path,
		default=Path("src"),
		help="Source folder containing _posts, _pages, _layouts, _includes, and _data.",
	)
	parser.add_argument(
		"--docs",
		type=Path,
		default=Path("docs"),
		help="Output folder for generated site files.",
	)


def build_parser() -> argparse.ArgumentParser:
	"""Build CLI parser with subcommands."""
	parser = argparse.ArgumentParser(
		description="Static site utility: clean, build, preview, pack, and publish.",
	)
	subparsers = parser.add_subparsers(dest="command")

	clean_parser = subparsers.add_parser("clean", help="Delete all files under docs.")
	clean_parser.add_argument(
		"--docs",
		type=Path,
		default=Path("docs"),
		help="Output folder to clean.",
	)
	_add_logging_argument(clean_parser)

	build_parser_cmd = subparsers.add_parser("build", help="Generate static site files from src.")
	_add_src_docs_arguments(build_parser_cmd)
	build_parser_cmd.add_argument(
		"--clean",
		action="store_true",
		help="Delete docs before generating.",
	)
	_add_logging_argument(build_parser_cmd)

	preview_parser = subparsers.add_parser("preview", help="Build then preview docs at http://127.0.0.1:8000.")
	_add_src_docs_arguments(preview_parser)
	preview_parser.add_argument(
		"--clean",
		action="store_true",
		help="Delete docs before generating.",
	)
	_add_logging_argument(preview_parser)

	pack_parser = subparsers.add_parser(
		"pack",
		help="Build and commit all changes without pushing.",
	)
	_add_src_docs_arguments(pack_parser)
	pack_parser.add_argument(
		"--clean",
		action="store_true",
		help="Delete docs before generating.",
	)
	pack_parser.add_argument(
		"--message",
		default=f"chore: pack site {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
		help="Commit message used by pack command.",
	)
	_add_logging_argument(pack_parser)

	publish_parser = subparsers.add_parser(
		"publish",
		help="Build, pack changes, and push current branch.",
	)
	_add_src_docs_arguments(publish_parser)
	publish_parser.add_argument(
		"--clean",
		action="store_true",
		help="Delete docs before generating.",
	)
	publish_parser.add_argument(
		"--message",
		default=f"chore: publish site {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
		help="Commit message used by publish command.",
	)
	_add_logging_argument(publish_parser)

	# Backward-compatible alias for the typo requested earlier.
	subparsers.add_parser("prview", help="Alias of preview.")

	return parser


def main() -> int:
	"""CLI entrypoint."""
	parser = build_parser()
	args = parser.parse_args()
	selected_command = args.command or "build"
	if selected_command == "prview":
		selected_command = "preview"

	verbosity = getattr(args, "verbose", False)

	logging.basicConfig(
		level=logging.DEBUG if verbosity else logging.INFO,
		format="%(levelname)s: %(message)s",
	)

	if selected_command == "clean":
		return clean_docs(docs_root=args.docs)

	if selected_command == "build":
		src_root = getattr(args, "src", Path("src"))
		docs_root = getattr(args, "docs", Path("docs"))
		do_clean = getattr(args, "clean", False)
		return build_site(src_root=src_root, docs_root=docs_root, clean=do_clean)

	if selected_command == "preview":
		src_root = getattr(args, "src", Path("src"))
		docs_root = getattr(args, "docs", Path("docs"))
		do_clean = getattr(args, "clean", False)
		build_exit = build_site(src_root=src_root, docs_root=docs_root, clean=do_clean)
		if build_exit != 0:
			return build_exit
		return preview_site(docs_root=docs_root)

	if selected_command == "publish":
		return publish_site(
			src_root=args.src,
			docs_root=args.docs,
			commit_message=args.message,
			clean=args.clean,
		)

	if selected_command == "pack":
		build_exit = build_site(src_root=args.src, docs_root=args.docs, clean=args.clean)
		if build_exit != 0:
			return build_exit
		pack_exit, _ = pack_site(commit_message=args.message)
		return pack_exit

	parser.print_help()
	return 2


if __name__ == "__main__":
	raise SystemExit(main())