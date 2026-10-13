# Before-the-session "stuck" prompt — what a student pastes into Vera

This is the text behind the "Copy the stuck prompt for Vera" button on the Week 4 page. It is NOT a
follow-along script: steps 1 to 4 are the student's to do from the page (each step has a Loom
video). The prompt is for when a screen does not match. The student pastes it into a NEW Vera chat,
fills in the step number, and attaches a screenshot.

**Keep this file byte-identical to `COMMAND_CENTER_PREP_PROMPT` in the Lovable project's
`src/components/lean-landlord/command-center-prep.tsx`.**

---

Hey Vera. I am doing the before-the-session setup for my Command Center on my own, following the steps on the Week 4 page, and I am stuck on step [NUMBER]: [what I was trying to do]. Here is a screenshot of what I see: [attach screenshot]

Load the command-center-builder skill and open its Cloudflare reference, the section called "Before the session." Look at my screenshot, tell me exactly what to click next in plain words, one step at a time, and wait for me to say "done" before the next one. Assume I do not know what Cloudflare, a token, or Zero Trust is.

Rules: the ONE thing you may ask me to paste into this chat is my read-only Airtable token (it starts with pat). Never ask me to paste a password, a credit card number, or the Cloudflare token; for those, tell me where to paste them myself. Do not take screenshots while a secret is on my screen. If I get a 404 on the GitHub secrets page, tell me it means I am not signed into GitHub in that browser.

When I say I have finished steps 1 to 4, run the ready check with me: can I sign into Cloudflare, does Zero Trust open to its own dashboard, do both secrets appear in my memory vault on GitHub. Then tell me plainly whether I am ready for step 5, where you line it up, or exactly what is still missing.
