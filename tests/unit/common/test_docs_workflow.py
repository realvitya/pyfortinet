"""Documentation publication must stay separate from PR builds and target gh-pages."""

from pathlib import Path

from ruamel.yaml import YAML

ROOT = Path(__file__).resolve().parents[3]


def test_docs_publication_targets_output_branch_without_direct_deployment() -> None:
    workflow = YAML(typ="safe").load(ROOT / ".github" / "workflows" / "deploy-docs.yml")
    assert workflow["permissions"] == {"contents": "read"}
    assert "gh-pages" not in workflow["on"]["push"]["branches"]
    steps = [step for job in workflow["jobs"].values() for step in job["steps"]]
    publications = [step for step in steps if step.get("uses", "").startswith("peaceiris/actions-gh-pages@")]
    assert len(publications) == 1
    publish = publications[0]
    assert publish["with"]["publish_branch"] == "gh-pages"
    assert publish["with"]["publish_dir"] == "./site"
    assert publish["with"]["force_orphan"] is False
    assert publish["with"]["deploy_key"] == "${{ secrets.DOCS_DEPLOY_KEY }}"
    assert not any(step.get("uses", "").startswith("actions/deploy-pages@") for step in steps)
    assert not any("environment" in job for job in workflow["jobs"].values())


def test_docs_credentials_are_used_only_on_trusted_source_branch() -> None:
    workflow = YAML(typ="safe").load(ROOT / ".github" / "workflows" / "deploy-docs.yml")
    sensitive_steps = [
        step for job in workflow["jobs"].values() for step in job["steps"] if "secrets.DOCS_DEPLOY_KEY" in str(step)
    ]
    assert sensitive_steps
    for step in sensitive_steps:
        assert "github.event_name != 'pull_request'" in step["if"]
        assert "github.ref == 'refs/heads/master'" in step["if"]
    assert workflow["concurrency"]["cancel-in-progress"] == "${{ github.event_name == 'pull_request' }}"
