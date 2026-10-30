# What the tests check

The button tests and the in-memory wait tests need no server. The GreenMail tests talk to a real IMAP server and skip when Docker is not running. `pytest` runs all of them.

## Reading a button

`tests/test_links.py` builds small messages.

- `test_part_of_a_label_is_not_the_button` — "Activate" does not match "Activate account". The error still names the full button.
- `test_button_label_ignores_case_and_odd_spaces` — "activate   account" matches a button whose HTML uses a non-breaking space.
- `test_words_split_across_tags_are_one_label` — "Accept" and "invitation" in nested tags are one label.
- `test_the_same_button_twice_is_one_link` — the same words and the same URL twice is one link.
- `test_two_urls_for_one_label_are_reported` — the same words and two URLs raises `AmbiguousLink` and lists both URLs.
- `test_a_missing_label_names_the_links_that_exist` — asking the activation sample for "Reset password" raises `LinkNotFound` and names the buttons that are there.
- `test_html_button_wins_when_the_plain_part_uses_different_words` — the HTML button "Accept invitation" is returned. The plain-text line "Accept the invitation" is not used while HTML is present.
- `test_plain_text_uses_the_words_on_the_same_line` — a message with no HTML takes the URL from the line that names the button.
- `test_a_copy_on_cc_counts_without_joining_the_to_line` — a Cc address matches. It does not appear on `to`.
- `test_a_bad_date_does_not_hide_the_button` — a Date header that is not a date leaves `date` empty and the button is still readable.
- `test_delivered_to_counts_when_the_visible_to_was_rewritten` — `To` still shows the visible address. `addressed_to` also matches `Delivered-To`, and a longer plus-tag does not match.



## The sample messages

`tests/test_fixtures.py` reads `tests/samples/activation.eml` and `tests/samples/site_invitation.eml`.

- `test_activation_button_is_the_account_link` — "Activate account" is the activation URL, including the code and `lang=en`. The footer links and the logo link stay separate.
- `test_activation_headers_are_decoded` — the subject decodes the trademark sign, the date is UTC, and the plus-tag matches only in full. `qa+5e0c7a3` and `qa+5e0c7a311` are different addresses.
- `test_invitation_button_is_the_accept_link` — "Accept invitation" is the accept URL. "Warehouse – North" is the site link. The logo is the home page.
- `test_invitation_headers_keep_the_display_name_off_the_address` — the subject keeps "José Müller". The recipient is `qa+9b24d6f0@example.com`, without the display name "Anna Schmidt".



## Waiting, without a server

`tests/test_inbox.py` uses an in-memory mailbox that speaks the same four operations as an IMAP session.

- `test_unique_address_is_a_fresh_plus_tag` — two calls return two `qa+<random>@example.com` addresses. An address that already has a plus-tag is replaced, not stacked.
- `test_mail_already_in_the_box_is_returned` — mail that arrived before `wait_for` is returned. The log names the address and leaves the URL out.
- `test_mail_that_arrives_during_the_wait_is_returned` — the first look is empty. The message appears on the second look and is returned.
- `test_a_broken_address_search_still_reads_recent_mail` — a server search that finds nothing does not hide a recent message. The library reads the message and checks the address itself.
- `test_two_recipients_do_not_see_each_others_mail` — two plus-addresses in one box each get their own button.
- `test_the_newest_matching_message_wins` — two messages to the same address: the later one is returned.
- `test_newer_than_ignores_mail_that_was_already_there` — `mark` is taken after the old reset mail. The wait returns the reset mail that arrived after the mark.
- `test_subject_filter_skips_other_mail_to_the_same_address` — a welcome message to the same address is skipped when the wait asks for a subject containing "reset".
- `test_timeout_names_the_messages_that_were_seen` — nothing matches. `EmailTimeout` names the address that was requested and a subject that was in the box.
- `test_a_dropped_greeting_is_a_connection_error` — the server accepts the socket and then drops the greeting. The wait sees a connection error and can look again.
- `test_a_rejected_login_is_a_mailbox_error` — a login the server refuses raises `MailboxError`, and the socket is closed.
- `test_a_login_error_is_not_retried` — a rejected login raises `MailboxError` at once. The wait does not keep asking.
- `test_a_rebuilt_mailbox_does_not_keep_the_old_bookmark` — after the server's mailbox generation changes, the old mark no longer hides the message that was already there.
- `test_a_refused_connection_is_tried_again` — the first connection fails. The next look succeeds and returns the message.
- `test_delivered_to_is_enough_when_the_visible_to_was_rewritten` — `To` is the shared account. `Delivered-To` carries the plus-address, and that is enough to match.



## Waiting, on GreenMail

`tests/test_greenmail.py` sends real messages over SMTP and reads them over IMAP. These repeat the waits that depend on a server: mail already there, mail that arrives during the wait, two waits at once, `newer_than`, a timeout, and reading without setting the seen flag.

- `test_mail_already_in_the_box_is_returned` — the message is delivered, then the wait finds the Activate account link.
- `test_mail_that_arrives_during_the_wait_is_returned` — the wait starts first. The message is sent half a second later.
- `test_parallel_waits_keep_their_own_mail` — two threads wait in the same account and each returns its own link.
- `test_newer_than_ignores_mail_that_was_already_there` — the old reset mail is in the box before `mark`. The new one is returned.
- `test_timeout_when_nothing_arrives` — a fresh address and a short timeout raise `EmailTimeout`.
- `test_reading_does_not_mark_the_message_seen` — after `wait_for`, the message flags do not include `\Seen`.

