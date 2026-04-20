from app.pii import scrub_text


def test_scrub_email() -> None:
    out = scrub_text("Email me at student@vinuni.edu.vn")
    assert "student@" not in out
    assert "REDACTED_EMAIL" in out


def test_scrub_cccd_without_partial_phone_match() -> None:
    out = scrub_text("CCCD 012345678901 must be hidden")
    assert "012345678901" not in out
    assert "REDACTED_CCCD" in out
