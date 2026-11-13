"""The independent reference generator preserves URLs and cleans only its own output."""

import runpy
from pathlib import Path

import pytest

GENERATOR = runpy.run_path(str(Path(__file__).resolve().parents[3] / "docs" / "gen_ref_pages.py"))
generate_reference = GENERATOR["generate_reference"]
GENERATED = GENERATOR["GENERATED"]


def write_source(root: Path, relative: str) -> Path:
    path = root / "pyfortinet" / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('"""Example source."""\n', encoding="utf-8")
    return path


def test_preserve_reference_urls_and_identifiers(tmp_path: Path) -> None:
    for name in ["__init__.py", "__main__.py", "settings.py", "fmg_api/__init__.py", "fmg_api/fmg.py"]:
        write_source(tmp_path, name)
    generate_reference(tmp_path)
    reference = tmp_path / "docs" / "reference"
    pages = {path.relative_to(reference).as_posix() for path in reference.rglob("*.md")}
    assert pages == {"SUMMARY.md", "settings.md", "fmg_api/__init__.md", "fmg_api/fmg.md"}
    assert (reference / "fmg_api" / "__init__.md").read_text(encoding="utf-8") == GENERATED + "::: fmg_api\n"
    assert (reference / "fmg_api" / "fmg.md").read_text(encoding="utf-8") == GENERATED + "::: fmg_api.fmg\n"
    assert (reference / "SUMMARY.md").read_text(encoding="utf-8") == (
        GENERATED + "- [fmg_api](fmg_api/__init__.md)\n    - [fmg](fmg_api/fmg.md)\n- [settings](settings.md)\n"
    )


def test_remove_stale_pages_and_keep_unrelated_files(tmp_path: Path) -> None:
    source = write_source(tmp_path, "old.py")
    generate_reference(tmp_path)
    reference = tmp_path / "docs" / "reference"
    unrelated = reference / "notes.txt"
    unrelated.write_text("Keep this file", encoding="utf-8")
    source.rename(source.with_name("new.py"))
    generate_reference(tmp_path)
    assert not (reference / "old.md").exists()
    assert (reference / "new.md").exists()
    assert unrelated.read_text(encoding="utf-8") == "Keep this file"


def test_refuse_unowned_markdown_before_writing(tmp_path: Path) -> None:
    write_source(tmp_path, "settings.py")
    reference = tmp_path / "docs" / "reference"
    reference.mkdir(parents=True)
    manual = reference / "settings.md"
    manual.write_text("Manually maintained", encoding="utf-8")
    with pytest.raises(ValueError, match="non-generated"):
        generate_reference(tmp_path)
    assert manual.read_text(encoding="utf-8") == "Manually maintained"
    assert not (reference / "SUMMARY.md").exists()


def test_require_source_before_touching_output(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="Missing Python source"):
        generate_reference(tmp_path)
    assert not (tmp_path / "docs").exists()
