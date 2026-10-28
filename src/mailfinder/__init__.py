"""Find a test email and read the link on its button."""

from mailfinder.errors import AmbiguousLink, LinkNotFound, MailfinderError
from mailfinder.links import Link
from mailfinder.message import Message, parse

__all__ = [
    "AmbiguousLink",
    "Link",
    "LinkNotFound",
    "MailfinderError",
    "Message",
    "parse",
]
