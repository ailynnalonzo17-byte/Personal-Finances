---
flow_id: lien-waiver
name: Conditional Lien Waiver
summary: >
  When a contractor's job is done and you know what you paid them, this fills your
  lien waiver, creates it in DocuSign as a draft, and posts every filled-in value to
  Slack with an approve button. Approve and it sends. Decline and the draft is voided.
  You never open DocuSign to check it.
trigger: Set the maintenance job's "Lien Waiver Status" field to "Prepare".
imports:
  # Import the child FIRST, then the parent (the parent must point at your child).
  - file: child.template.json
    order: 1
    note: The engine — one execution per job. Import first, then activate.
  - file: parent.template.json
    order: 2
    note: The dispatcher. After importing, open its "Process One Job" node and pick
      YOUR imported child workflow (or the installer fills CHILD_WORKFLOW_ID).
connections:
  - service: Airtable
    credential_type: airtableTokenApi
    guide: airtable          # your base + a personal access token
  - service: Slack
    credential_type: slackApi
    guide: slack             # the bot that posts the values and waits for approve
  - service: DocuSign
    credential_type: none    # NOT an n8n credential — see docusign_setup below
    guide: docusign
variables:
  - key: SLACK_CHANNEL
    prompt: The Slack channel the approval posts to.
    how: The installer creates this channel for you and fills its id.
    type: channel
  - key: CHILD_WORKFLOW_ID
    prompt: The n8n id of your imported child workflow.
    how: Derived at install time, after you import the child. You do not type this.
    type: text
  - key: DOCUSIGN_TEMPLATE_NAME
    prompt: The exact name of your lien waiver template in DocuSign.
    example: Lien Waiver - Final Conditional
    how: The flow looks the template up BY NAME every run, so rebuilding your
      template never breaks it. Rename the template and you must change this.
    type: text
  - key: DOCUSIGN_ROLE_NAME
    prompt: The signer role on that template.
    example: Contractor
    how: Must match the role name on the template exactly, character for character.
    type: text
  - key: DOCUSIGN_INTEGRATION_KEY
    prompt: Your DocuSign app's Integration Key (a GUID).
    how: From your own DocuSign app. See docusign_setup.
    type: secret
  - key: DOCUSIGN_USER_ID
    prompt: Your DocuSign API Username / User ID (a GUID).
    how: DocuSign > Settings > Users > your user > API Username. See docusign_setup.
    type: secret
  - key: DOCUSIGN_PRIVATE_KEY
    prompt: The RSA private key you generated for that DocuSign app.
    how: The whole PEM block, BEGIN and END lines included. See docusign_setup.
    type: secret
# The Airtable tables + fields this flow reads or writes. The installer checks your
# base has every one of these BY NAME before it runs. Missing or renamed -> it stops.
airtable_structure:
  - table: Maintenance
    fields: ["Issue", "Property", "Unit", "Vendor", "Invoice Amount", "Invoice Number",
      "Completed Date", "Lien Waiver Status", "Lien Waiver Exceptions",
      "Lien Waiver Envelope ID"]
  - table: Properties
    fields: ["Street Address", "Town", "State (Select)", "Owner Entity", "Property Manager"]
  - table: Units
    fields: ["Unit"]
  - table: Vendors
    fields: ["Vendor Name", "Email"]
# Fields you create once, before installing. The installer can make these for you.
base_setup:
  - table: Maintenance
    create:
      - name: Lien Waiver Status
        type: singleSelect
        options: ["Prepare", "Draft ready", "Sent", "Signed", "Voided",
          "Blocked - missing data"]
        note: The value Prepare is the trigger. The flow writes the others.
      - name: Lien Waiver Exceptions
        type: multilineText
        note: Anything this waiver does NOT release. Blank prints "None".
      - name: Lien Waiver Envelope ID
        type: singleLineText
        note: Written by the flow. Its presence is what stops a second waiver being
          built for the same job. Clear it only to deliberately rebuild.
  - view:
      table: Maintenance
      name: Lien Waivers
      filter: Status is Completed
      group_by: Lien Waiver Status
      sort: Completed Date, newest first
      note: Do NOT filter on "Invoice Amount is not empty" — you often set the waiver
        up at the moment the invoice lands, and the row has to be visible to type it in.
# The one part that is genuinely yours to do, and it is not five minutes.
docusign_setup:
  - Your DocuSign plan must include API access. Check before you start; the entry
    tier does not have it.
  - Create an app in DocuSign (Settings > Apps and Keys > Add App and Integration Key).
    Note the Integration Key.
  - Generate an RSA keypair on that app and save the PRIVATE key. DocuSign shows it once.
  - Grant consent once, for the "signature impersonation" scope, as yourself.
  - Copy your API Username (User ID) from Settings > Users.
  - Build your lien waiver as a DocuSign template with ONE signer role, and put the
    eight tooltips below on the eight fields. See "Your template" in the body.
---

# Conditional Lien Waiver — how it works

**What it is.** A two-workflow automation that turns "the contractor finished and I
paid them" into a signed lien waiver, with you approving the numbers in Slack and
never opening DocuSign to check them.

**What sets it off.** You open the maintenance job in your base, make sure the vendor,
the invoice amount and the completed date are filled in, and set **Lien Waiver Status**
to **"Prepare"**. That's the whole trigger.

**What happens next.**
1. It reads the job, its property, its unit and its vendor, and builds the eight values
   the waiver needs.
2. If anything is missing it stops, sets the job to **Blocked - missing data**, and
   tells you in Slack exactly which fields are empty. Nothing is created in DocuSign.
3. Otherwise it fills your DocuSign template and creates the envelope as a **draft**.
   No file is uploaded — only the values travel, and DocuSign assembles the document
   from the template it already holds.
4. It posts every value to Slack, laid out as it will print: claimant, customer, owner,
   job location, maker of check, amount, through date, exceptions.
5. **You click Approve & send** and it sends, marks the job **Sent**, and confirms in
   the thread. **Decline** voids the draft in DocuSign and drops the job back to blocked.

**What you do day to day.** Fill the invoice amount, set the field to "Prepare", glance
at Slack, click approve.

## Your template, and the sample that comes with it

**A sample form ships with this card: `lien-waiver-sample.pdf`.** It is an original,
plainly drafted conditional waiver on final payment with all eight blanks laid out and
labeled, ready to upload to DocuSign and tag. `lien-waiver-sample.source.py` regenerates
it if you want to change the wording.

**Treat it as a starting point, not as the finished article.** Lien waiver requirements
are set by state — some states prescribe exact wording, and a form written for one state
can be worthless in another. Have your attorney confirm the right form for the state your
property is in, then build your DocuSign template from that. This is not legal advice.

**What makes it work with this automation is the tooltips, not the form.** Put a
DocuSign field on each blank, assign it to your signer role, and set its **Tooltip** to
exactly one of these:

| Tooltip | What it prints |
|---|---|
| `Name of Customer` | whoever hired the contractor — your management company, else the owner |
| `Owner` | the entity that owns the property |
| `Job Location` | street, unit, town, state — built for you |
| `Check Payable To` | the vendor's name |
| `Maker of Check` | who writes the check — your management company, else the owner |
| `Amount of Check` | the invoice amount |
| `Through Date` | the job's completed date |
| `Exceptions` | anything the waiver does not release; blank prints "None" |

The flow reads your template's tooltips **on every run** and works out which field is
which by itself. That means you can move fields around, or rebuild the template from
scratch, and nothing breaks. Two rules: every tooltip must be **unique**, and it must
match the spelling above exactly. A tooltip it cannot find stops the run and names it.

Three traps worth avoiding when you build the template:

- **Make every field a Text field, including the money one.** A DocuSign *Number*
  field cannot be filled through the API at all.
- **Do not tick Required on the fields you are prefilling.** They are also read-only,
  so required + read-only + a value that failed to arrive is a box your contractor can
  neither fill nor skip.
- **Leave the signature, printed name and date-signed fields alone.** They are the
  contractor's, and Date Signed fills itself.

**Want it changed?** Ask your own Vera to edit the workflow — this installer sets it up
but doesn't modify flows.
