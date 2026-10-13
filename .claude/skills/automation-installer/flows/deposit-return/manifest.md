---
flow_id: deposit-return
name: Security Deposit Disposition
summary: >
  When a lease's deposit is ready to settle, this prepares the security-deposit
  return: it reads the numbers from your base, works out the interest owed,
  builds the disposition statement as a PDF, posts it to Slack for a one-click
  approve, then emails the tenant the statement and opens a return task.
trigger: Set the lease's "Security Deposit Disposition" field to "Prepare".
imports:
  # Import the child FIRST, then the parent (the parent must point at your child).
  - file: child.template.json
    order: 1
    note: The 42-step engine. Import first, then activate.
  - file: parent.template.json
    order: 2
    note: The dispatcher. After importing, open its "Process One Lease" node and
      pick YOUR imported child workflow (or the installer fills CHILD_WORKFLOW_ID).
connections:
  - service: Airtable
    credential_type: airtableTokenApi
    guide: airtable          # your base + a personal access token
  - service: Slack
    credential_type: slackApi
    guide: slack             # the bot that posts + waits for approval
  - service: Google Drive
    credential_type: googleDriveOAuth2Api
    guide: google-drive      # copies the Doc template, stores the PDF
  - service: Gmail / email
    credential_type: gmailOAuth2
    guide: gmail             # sends the statement to the tenant
variables:
  - key: SLACK_CHANNEL
    prompt: The Slack channel the approval posts to.
    how: The installer CREATES this channel for you (#finance) and fills its id.
    type: channel
  - key: AGENT_EMAIL
    prompt: The email address the tenant statement is sent FROM.
    example: you@yourcompany.com
    type: email
  - key: OWNER_EMAIL
    prompt: Your own email, for internal notices.
    example: you@gmail.com
    type: email
  - key: BUSINESS_NAME
    prompt: Your business name, used in the fallback email signature.
    example: Bright Key Rentals
    type: text
  - key: AGENT_NAME
    prompt: The name the tenant email is signed with.
    example: Jordan
    type: text
  - key: OWNER_WEBSITE_URL
    prompt: Your website, full URL, for the email link.
    example: https://www.yourcompany.com/
    type: text
  - key: OWNER_WEBSITE
    prompt: Your website shown as plain text in the email.
    example: yourcompany.com
    type: text
  - key: CHILD_WORKFLOW_ID
    prompt: The n8n id of your imported child workflow.
    how: Derived at install time, after you import the child. You do not type this.
    type: text
# The Airtable tables + fields this flow reads or writes. The installer checks
# your base has every one of these (by NAME) before it runs. Missing/renamed -> it stops.
airtable_structure:
  - table: Leases
    fields: ["Security Deposit Disposition", "Deposit Legal Deadline", "Notes",
      "Disposition Document URL", "Interest on Deposit", "Disposition Document Drive ID",
      "Disposition Email Sent"]
  - table: Tasks
    fields: ["Related Lease", "Assigned Employee", "Deadline", "Amount Owed",
      "Immediate Need?", "Title", "Priority Level", "Status", "Due Date", "Task Description"]
  - table: Units
    fields: []
  - table: Properties
    fields: []
  - table: Applicant Groups
    fields: []
  - table: Deposit Interest Rates
    fields: []
  - table: Policy Settings - States
    fields: []
  - table: Automation Settings
    fields: []
  - table: Automations
    fields: []
  - table: Daily Summary
    fields: []
# Things the flow reads from your base that YOU must fill in once (not in the JSON):
base_setup:
  - The Google Doc template id and the Drive folder id live in your base (the flow
    reads them, they are not in the workflow). Save the deposit-statement Doc
    template (shipped with this card) to your Drive, then put its id + your output
    folder id where your base expects them.
  - The tenant email subject + body come from your Automations table. Fill your own,
    or the flow falls back to a plain built-in email signed with the values above.
  - Deposit interest rates per state live in the Deposit Interest Rates table.
---

# Security Deposit Disposition — how it works

**What it is.** A two-workflow automation that prepares a tenant's security-deposit
return from start to finish: the maths, the statement PDF, the approval, the email,
and the follow-up task — with a human approving the dollar figure before anything
is sent.

**What sets it off.** You open the lease in your base, fill in any deductions, and
set the **Security Deposit Disposition** field to **"Prepare"**. That's the whole
trigger. Everything after is automatic up to the approval.

**What happens next.**
1. It reads the lease, unit, property, your state's deposit rules, and the interest
   rate, and works out interest owed and the amount to return.
2. It copies your deposit-statement Google Doc template, fills in the numbers, and
   exports a PDF to your Drive.
3. It posts the proposed statement to your **#finance** Slack channel and waits.
4. **You click approve** (or ask for changes — it parks the lease and tells you
   what it's waiting on).
5. On approve, it emails the tenant the statement PDF, opens a **return task** with
   the deadline and amount, and marks the lease **Statement Sent**.

**What you do day to day.** Fill deductions, set the field to "Prepare", glance at
Slack, click approve. That's it.

**One-time setup (the installer walks you through it).** Connect Airtable, Slack,
Google Drive and email; save the Doc template to your Drive and note its id; let the
installer create your #finance channel; import the child workflow, then the parent,
and bind the parent to your child.

**Want it changed?** Ask your own Vera to edit the workflow — this installer sets it
up but doesn't modify flows.
