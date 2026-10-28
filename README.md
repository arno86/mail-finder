# mail-finder

Tests use this library to read the link on a button in an email, such as Activate account or Accept invitation.

## Tests

Python 3.12 or newer.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

These tests read the sample messages. No mail server is involved.

## Decisions

The button is found by the words a person sees. "Activate account" is that button, not the website link in the footer. The whole label has to match. Letter case and odd spaces are ignored, because mail HTML pads text with tags and non-breaking spaces.

When the message has HTML, the link comes from the HTML. The plain part is used only when there is no HTML. On the invitation sample, the plain text says "Accept the invitation" and the button says "Accept invitation."

The same button twice with the same URL is one link. The same words pointing at two different URLs is an error. Guessing would open the wrong page.

Python's email package decodes the quoted-printable and base64 wrappers, and the encoded subjects. BeautifulSoup then reads the HTML. The samples break lines in the middle of a URL and write `&` as `&amp;`.
