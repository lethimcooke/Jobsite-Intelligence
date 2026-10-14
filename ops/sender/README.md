# ASI Sender: reference copy

`Code.gs` here is a read-only copy of `ops/sender/Code.gs` in the Austin-Signage repo, which owns it.
The live script runs in the user's Gmail (operations@asterfieldgroup.com) and serves both businesses.
Don't edit this copy; if the sender needs a change, tell the user, who brings it to the ASI session.

What it does for Jobsite: reads our manifest draft ("ASI-MANIFEST v1 <date> <sha256>", business
"Jobsite Intelligence"), re-checks every listed draft (exact recipient, subject and text; sites@ with
"Houston Jobsite Intelligence" in the signature and as a verified Send-mail-as alias; do-not-contact;
no reply or bounce; thread unchanged; first emails only to companies with no email history), and sends
it from sites@. Caps: 60 a day for the mailbox, 15 of them ours, first emails first. Modes: DRY_RUN,
TEST, LIVE, PAUSED (script property MODE, set by the user).
