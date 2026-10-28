"""Errors a test can catch when a button is missing."""


class MailfinderError(Exception):
    """Base class for every error this library raises on purpose.

    A test can catch this one type when it does not care which failure it
    was: a missing button, or a label that points at two different URLs.
    """


class LinkNotFound(MailfinderError):
    """The message was read, and it has no button with the requested label.

    ``label`` is the text the test asked for. ``available`` is the button
    text that really was on the message, in the order the links appear, so
    a failure can show what the mail contained.
    """

    def __init__(self, label: str, available: tuple[str, ...]):
        """Store the missing label and the labels that were present."""

        self.label = label
        self.available = available
        if available:
            found = ", ".join(repr(item) for item in available)
            detail = f"Links present: {found}."
        else:
            detail = "The message has no links."
        super().__init__(f"No link with label {label!r}. {detail}")


class AmbiguousLink(MailfinderError):
    """The same label is attached to two different URLs.

    The library refuses to pick one, because the test would open the wrong
    page. The same button repeated with the same URL is a single link and
    does not raise. ``urls`` lists the different targets, in document order.
    """

    def __init__(self, label: str, urls: tuple[str, ...]):
        """Store the shared label and the URLs it points at."""

        self.label = label
        self.urls = urls
        choices = ", ".join(urls)
        super().__init__(f"Label {label!r} points at more than one URL: {choices}.")
