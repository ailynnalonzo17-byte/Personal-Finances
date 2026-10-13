# Pre-work step 5 — "Let Vera line it up" prompt (Phase P)

This is the text behind the "Copy the line-up prompt for Vera" button on the Week 4 pre-work page.
The student pastes it into a NEW Vera chat in Claude Code on their own computer, with Cloudflare and
GitHub signed in, after finishing steps 1 to 4. Vera runs Phase P of this skill.

**Keep this file byte-identical to `COMMAND_CENTER_LINEUP_PROMPT` in the Lovable project's
`src/components/lean-landlord/command-center-prep.tsx`.** They are the same prompt in two places, and
a drift between them is a student following one set of words while Vera follows another.

---

Hey Vera. I have finished steps 1 to 4 of the Week 4 pre-work. Load the command-center-builder skill and run its pre-work line-up, the part it calls Phase P.

In plain words: check my steps, put the holding page into my memory vault, connect Cloudflare to my vault and deploy it, put my read-only Airtable token where it goes, turn on the login gate for the page, run the refresh once, and give me my address.

Deploy it as a Worker, never with Cloudflare's older Pages option. My address must end in workers.dev. If it ends in pages.dev, fix that before we go on.

Do not build my Command Center yet. That is for the session.

Stop for two things only, and tell me exactly what to click each time: the GitHub window where I authorize Cloudflare, and my Airtable token. For the token, either bring the box up on screen and let me paste it in myself, or ask me for it in the chat and put it in for me. Tell me which one you want.

Everything else, do yourself and tell me in one line as you go.

When you are done, give me the address, tell me how to log in, and tell me plainly whether everything is ready for the session or exactly what is still missing. Do not tell me how to build the real thing or what to do next toward it. That is what the session is for, so just tell me I am ready for it.

I am on my own computer and signed into Cloudflare and GitHub in Chrome. If you are not in a session that can open my browser, say so first and stop.
