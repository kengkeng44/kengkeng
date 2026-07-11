from generator.frontmatter import parse_frontmatter


def test_parses_meta_and_body():
    text = (
        "---\n"
        "name: sample-rule\n"
        "description: one line\n"
        "metadata:\n"
        "  type: feedback\n"
        "---\n"
        "\nbody text here\n"
    )
    meta, body = parse_frontmatter(text)
    assert meta["name"] == "sample-rule"
    assert meta["description"] == "one line"
    assert meta["metadata"]["type"] == "feedback"
    assert body.strip() == "body text here"


def test_no_frontmatter_returns_empty_meta():
    meta, body = parse_frontmatter("just text\n")
    assert meta == {}
    assert body.strip() == "just text"
