# mail-finder

Tests use this library to pick one email out of a shared mailbox and read the link on a button, such as Activate account or Accept invitation.

## Usage

```python
import os
from mailfinder import Inbox

inbox = Inbox(
    host="imap.gmail.com",
    username=os.environ["MAIL_USERNAME"],
    password=os.environ["MAIL_PASSWORD"],
)

recipient = inbox.unique_address()

# Trigger your application's signup using this address.
app.sign_up(email=recipient)

message = inbox.wait_for(
    recipient,
    timeout=30,
    subject_contains="Activate",
)
activation_url = message.link("Activate account")
```

app.sign_up() is a placeholder for the application under test. Replace it with your own API call or UI action that triggers a signup email to recipient.

### Reusing an address

```python
bookmark = inbox.mark()  # Take this before triggering the email.

app.request_password_reset(email=recipient)

message = inbox.wait_for(
    recipient,
    timeout=30,
    subject_contains="Reset",
    newer_than=bookmark,
)
reset_url = message.link("Reset password")
```



## Tests

Python 3.12 or newer.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

While the tests run, pytest prints a log of each wait: the address, the bookmark, and the subject of the message it kept. The body stays out of the log, because that is where the link is. A failed test still includes that log.

[TESTS.md](TESTS.md) says what each test checks.

The button tests and the waiting tests that use an in-memory mailbox need no server:

```bash
pytest -m "not integration"
```

The tests that talk to a real IMAP server use GreenMail. Docker is only for that. The library itself is given a host, a port, and a login, and speaks ordinary IMAP.

```bash
docker compose up -d
pytest -m integration
```

GreenMail here has logins turned off, which is a convenience of that test server. Gmail is TLS on port 993 (`ssl=True`). Many company servers start plain and upgrade (`starttls=True`, port 143). GreenMail in this file is plain IMAP on port 3143 (`ssl=False`).

## Decisions

Assumptions made:

1. Every test signs up with a plus address and all messages land ti the same address.
2. Old emails stay and no email is deleted
3. The message may already be delivered before test starts waiting.
4. when the message has HTML the person sees HTML, the plain text is a fallback.
5. The words on the button are the full labels not a part of it.
6. A server may rewrite the visible "To" line, so the original address can also be on "CC" or on a delivery header.

Decisions made:

1. Each run gets its own plus-address. Otherwise two machines running the same test can pick up the same old message.
2. The wait looks in the mailbox first. The app may have sent the mail before the test started waiting.
3. If an address is used again, like a password reset, it takes a bookmark before the send. The bookmark is the server's next message number. It does not compare clocks, because the test machine and the mail server may not agree on the time. IMAP's date search is only good to the day.
4. The server's address search as a hint. Servers handle plus-addresses differently, and a message that just arrived is sometimes missing from search. It reads the message and check the address. It also reads the newest messages, so a slow search cannot hide the mail from this run.
5. If the connection drops, It tries again until the timeout. If the server rejects the login, It stops. Trying again will not fix a wrong password.
6. It writes the logs under the name `mailfinder`. It does not write a log file. The project that runs the tests already decides where logs go, and these lines go there. It does not log the message body, because that is where the link is.

What is left out:

1. The library does not ask the server to push new mail. It looks again until the timeout.
2. It does not delete mail, move it, or mark it as seen.
3. It does not sign in with OAuth. Gmail uses a normal login, so an app password.
4. It does not guess the main button from colors or CSS.
5. It does not follow redirects. The link in the message is the link the test gets.
6. There is no separate piece for a header, a footer, or one button. The test looks at the whole message, so I did not build nested components. I would do that if the HTML were more complex and a test had to look inside one part of the message.



## Tools

Cursor with Grok 4.7 model.