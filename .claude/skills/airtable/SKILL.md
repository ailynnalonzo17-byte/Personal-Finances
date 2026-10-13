---
name: airtable
description: "Load before ANY work that reads from or writes to the hub: looking something up, adding or changing a record, adding a field or a table, building a view, or setting up an automation inside the base. Covers connecting it, why you read the owner's own schema instead of assuming one, the difference between a field you can write and a field you cannot, linked records, the dropdown trap that silently invents junk options, deleting things safely, and when a job belongs to an automation inside Airtable rather than to you. Trigger on 'Airtable', 'the base', 'the hub', 'a table', 'a field', 'a record', 'a view', 'add a column', 'link these', 'automation', or any request to look up, change or organise the owner's own business data."
---

# Airtable

**Version: 1.6 - 2026-09-21** (adds: building an automation FOR someone when the API refuses the one
step that does the work. Airtable will not create a "Run a script" action through the API, and that
refusal was being read as "the automation cannot be built". It can: build the shell over the API and
finish it in the browser, or walk the owner through the clicks, and never fall back on a schedule.)

Earlier: 1.5 and 1.4 read what an existing automation WRITES before adding one beside it; adding to
a multi-value field without wiping it; why a value that can arrive two ways needs two automations;
the four tests a copy-a-value automation should pass; and reading a field off a found record one
level at a time. 1.3 fill the unit as well as the property, using the owner's own building-wide unit; exclude
archived records before calling anything a gap; check what downstream reads a field you have started
filling; and keep a job's contract total separate from the payment a document is about.

Airtable is the hub. It holds the properties, the units, the leases, the tenants, the tasks and the
routines. Almost everything else in this system either reads from it or writes to it, so a mistake
here does not stay here.

**This skill is about handling the hub safely. What is actually IN the owner's hub lives in their own
base file, which you read at the start of a session. Never assume a table or a field exists because
another owner has it.**

## Connecting it

Airtable has an official connector. The owner turns it on in their connector settings and signs in to
Airtable to authorise it. It works from the desktop app, the web and Claude Code, and it is the right
way in. Do not reach for anything else first.

**Access is per base, not per account.** The connector can only see bases the owner's Airtable login
can see, and if they were given access to just one screen rather than the whole base, some things
will refuse. If a read fails with a permission message rather than a not-found message, that is
usually what happened.

## Read the schema, never guess it

**The most common failure by far is writing to a field that does not exist, or that exists under a
slightly different name.** Every owner renames things. Every owner adds their own columns. Anything
that assumes a fixed name breaks the first time somebody tidies up.

- **Before your first write in a session, read the table's real fields.** Not the owner's description
  of them. The real ones.
- **Refer to things by ROLE, not by name.** "The table that holds leases" is stable. A specific name
  is not.
- **If you cannot find the field the job needs, say so and stop.** Do not pick the nearest-looking
  one. A rent figure written into the wrong column is invisible until it reaches an invoice.

**Never rename a table or a field just because a tidier name occurs to you.** Other things point at
it: views, automations, and anything connected from outside. Suggest it, let the owner decide, and if
they do rename something, that is the moment to re-read the schema.

## Fields you can write and fields you cannot

Some columns are answers the base works out for itself: a formula, a rollup, a lookup, a count, a
created time. **These cannot be written to, and trying gives a confusing error rather than a clear
one.** If a value looks wrong in one of them, the cause is upstream, in the fields it reads.

The useful consequence: **when a computed number is wrong, do not chase the number. Go and look at
what feeds it.** Usually something it depends on is empty, or linked to the wrong record.

## Linked records, and the mistake everyone makes

A link between two tables is not text. **It points at one specific record, and it has to be written as
that record's identity, not as its name.** Writing a name into a link field either fails or, on some
paths, quietly creates a brand new empty record carrying that name. The owner then has two of
something and one of them is hollow.

**So: find the record you mean first, then link to the thing you found.** If the search returns more
than one match, stop and ask which. Guessing between two tenants with the same surname is exactly the
kind of error nobody catches for a month.

**Two tables can be joined in more than one way at the same time**, and that is a real design rather
than a mistake: for example a current relationship and a full history. When you write a link, know
which of the two you are writing. Putting a finished thing into the current relationship is what
makes live reports quietly wrong.

## The dropdown trap that invents junk

A single-select or multi-select field has a fixed list of choices. **Writing a value that is not on
the list normally fails, which is good, because it tells you the list has changed. But there is a
setting that instead makes the write succeed by silently ADDING your value as a new choice.**

That is how a base ends up with "Complete", "complete" and "Completed" as three separate statuses,
each holding some of the records, with every view and automation seeing only part of the picture.

- **Re-read the choices before writing to a dropdown.** Owners rename and reorder options without
  telling anyone.
- **Use the automatic-conversion setting only when creating an option is genuinely what you intend**,
  and say so when you do.
- **A write rejected because the value is not a valid choice is information, not an obstacle.** The
  list changed. Go and look at it.

## Adding to the base

You can add fields and tables, and sometimes that is the right answer. Two rules keep it safe:

- **Changing the shape of the data is the most expensive kind of change**, because everything built on
  top of it has to be revisited. Do it early and deliberately, or not at all.
- **A new field with no description is a mystery in three weeks.** Write what it is for, in the
  field's own description, in the same breath as creating it.

**Deleting is different.** A table or a field can be deleted, and it takes everything in it with it.
Before deleting anything, find out what points at it: views, automations, links from other tables, and
anything connected from outside the base. **Deleting a field cannot be done through the connector at
all, only by hand, which is a useful accident, because it forces a pause.**

## When the job belongs to an automation, not to you

Airtable can run its own automations inside the base: when a record changes, do something. **That is
the right home for anything that must happen every time, immediately, with nobody present.** Setting a
default on a new record. Keeping two fields in step. Reacting the second a box is ticked.

**You are the wrong tool for that**, because you only run when someone is talking to you.

The reverse is also true: **anything needing judgement, or reading an email, or looking at a document,
is yours and does not belong in a base automation.**

A useful third case: **a default value on a field.** If the answer is always the same for a new
record, that is not an automation at all, it is a default, and it is the cheapest of the three.

**Automations inside a base are invisible unless you go looking.** When something changes by itself
and nobody knows why, check them before assuming a bug.

### Read what an existing automation WRITES before you add one beside it

**A base collects automations over years, and a name is not a description.** Before you build
something that touches a field, list the base's automations and open any that already write to that
same field. Read the action itself, not the title.

This is not a tidiness rule. An automation named as though it keeps two fields in step may in fact be
overwriting one with the other, and nobody will have noticed, because the damage only shows on
records where the two were ever different. If every record so far happened to hold a single value,
a clobbering automation and a correct one look identical from the grid. **The owner asks you to add
the missing half; the real work is often that the existing half has been destroying data quietly.**
Say so plainly when you find it, and fix it in the same pass.

### Adding a value to a multi-value field without wiping what is there

**An automation that writes a field REPLACES it.** There is no "add to" write. So copying one field
into a multi-value field (a multi-select, or a link field holding several records) destroys anything
already selected there, unless you deliberately write the old values back alongside the new one.

To add rather than replace, the write has to be *existing values, then the new value*, joined into a
single value list. Three things make that fiddly, and all three are worth knowing before you start:

- **There is no merge or combine function.** You join the two sides into one comma separated list of
  record identifiers.
- **So it takes two branches, not one.** If either side is empty, a comma join leaves a stray empty
  half in the middle of the value. Split it: one branch for "both sides have something", which joins
  them, and one for "the field is empty", which writes the new value on its own.
- **An empty source should fall through both branches and write nothing.** Then clearing the source
  field never touches the destination, which is almost always what the owner wants.

Re-adding a value that is already in the list is safe: the field de-duplicates, so nothing doubles up.

**Say out loud that it adds but never removes.** Change the source from A to B and the destination
ends up holding both. That is usually right, but it means a genuine mistake has to be taken out by
hand, and the owner should hear that from you rather than discover it.

### A value can arrive two ways, so it usually takes two automations

**"When a record is created" does not fire on later edits, and "when a record is updated" does not
fire on creation.** If the field you are reacting to can be filled in either at creation or
afterwards, one automation covers only half the cases.

There is a wrinkle worth warning the owner about. **A row typed straight into the grid is created
empty**, so at the instant the create-time automation looks, the field is still blank and nothing
happens. It fills a second later, and the update-time one catches it. The create-time half earns its
place on records that arrive complete: a form submission, an import, anything another system writes.

### Test it with a throwaway record, and test the awkward cases

Name a scratch record so it is obviously disposable, run it through every path, then delete it. For a
copy-a-value automation that is four tests, and the last two are the ones people skip:

1. The value arrives on a record where the destination is empty.
2. The value changes on a record where the destination already has other values. **Those other values
   must survive.**
3. The value is set to something already in the destination. Nothing should double up.
4. The source is cleared. The destination should not be touched.

**Give it a moment before reading the result.** These run a second or two behind the change, and a
read taken immediately shows the old value and looks like a failure. If it still looks wrong, check
the automation's own run history before changing anything: it records whether it ran at all, and
whether the run failed or simply did nothing.

### Building one FOR someone, and the one step the API refuses

You can create most of an automation through the API: the name, the trigger, which fields it watches,
and the ordinary actions like create a record or send an email. **You cannot create the "Run a
script" action.** Airtable rejects it outright, every time, even with an empty script. The same
refusal blocks editing any automation that already contains one, so once a script exists, every
change to that automation is a browser job.

**That refusal is not a dead end, and it must never be reported as one.** The script step is usually
the only part that does real work, so "the API won't make it" reads like "it can't be built". It can.
Take these in order.

**1. Build the shell over the API, then finish it in the browser yourself.** Create the automation
with the real trigger and the real watched fields, plus a harmless "Find records" placeholder as its
action. Then in the browser: open the action, change its type to Run script, add the input variable
the script needs, set the script, and switch the automation on.

- **The placeholder needs a real filter or a named view. "All records" is rejected**, so point it at
  a condition that never matches and it will sit there doing nothing until you replace it.
- **Set the script in one go rather than typing it.** Typing a long script into the editor is slow and
  the editor's own autocomplete can corrupt it while you work. Putting the whole text in at once
  avoids both. Then prove it: read the script back and compare it to what you meant to send, or press
  Airtable's own Test button and check the result. **Do not verify a script by looking at it**, a long
  line runs off the edge of the screen and you cannot see the end of it.
- **Everything is created switched OFF.** Turning it on is a click, and until someone makes it the
  automation does nothing at all.
- **Editing one that is already on shows "unpublished changes".** Until someone clicks Update, the old
  version is still the one running.

**2. If you cannot drive the browser, walk the owner through the same clicks.** That is still you
building it, one step removed. **Write the finishing steps and the exact script into the automation's
own description** so whoever clicks has everything in front of them and does not need the
conversation you had.

**⛔ What NOT to fall back on: a schedule.** It is tempting to give up on the change-triggered
automation and run something every few minutes instead. **Do not.** A five minute schedule is
thousands of runs a day, almost all of them finding nothing, and it will exhaust whatever plan it
runs on. A schedule is a once-a-day safety net behind a real trigger, never the main path. If the
trigger genuinely cannot be built, say so plainly and let the owner decide.

**⚠️ And do not trust the automation API's own instructions document on this.** It does not list the
script action among the things it cannot create, and it points at a section that is not in the
document. The server's refusal is the only reliable answer, so read what comes back rather than what
the catalog promised.

## Working with a lot of records at once

- **Writes go in batches, and there is a limit per batch.** A long job is several batches, not one.
- **Filter and sort on the Airtable side rather than pulling everything and sifting.** Pulling a whole
  large table wastes the session and usually still comes back cut off.
- **Ask for only the fields you need.** Almost every "the result was too big" problem is really "I
  asked for every column".
- **Before a bulk change, say what you are about to change and how many records it will touch, and
  check that number is what you expected.** A filter that is slightly wrong does not fail. It just
  updates the wrong two hundred rows.

## Getting a base someone shared, and giving one away

This comes up twice: when the owner receives a starter base from somebody else, and when they hand a
base to a partner, an assistant or a client of their own.

**The thing everyone gets wrong: automations do not travel through a share link.** Clicking **Copy
base** on a public share link copies the tables, the views and the interfaces, and leaves every
automation behind. The shared page has no Automations tab on it at all. Airtable does that on purpose,
because an automation can hold a webhook address or an email address belonging to whoever shared the
base. So a base that arrives with no automations is not broken and nothing was forgotten. It came the
wrong way.

### Receiving a base properly

1. The owner needs an Airtable account and **a workspace of their own already created**. Airtable will
   tell them if they have none. A blank one is fine and it does not need a name.
2. They open the invitation email and then the shared base.
3. **In the shared base they click Duplicate, and choose THEIR OWN workspace as the destination.**
4. **Working inside the shared base instead is a real mistake, not a shortcut.** Whoever shared it can
   see everything put into it, and a hub like this ends up holding the whole business.
5. **The automations arrive switched OFF.** Open the **Automations** tab and turn on the ones they
   want. That is normal Airtable behaviour, not a fault in the base. Say this out loud to the owner,
   because nobody thinks to look.
6. Anything using a connected account, such as Gmail, Slack or a calendar, has to be reconnected under
   their own login.

### Giving a base to someone else

1. **Duplicate the base first, name the copy after that one recipient, and share the duplicate. Never
   share the master.** A Creator on the master can change it, and everyone invited afterwards inherits
   the change. One copy per recipient also means recipients never see each other.
2. Open that duplicate and click **Share** at the **top right of the base**.
3. Type the recipient's email address.
4. **Grant them Creator permission.** This is the level that carries the ability to duplicate a base.
   Grant anything lower and they have no way to take their own copy, and the whole thing stalls there.
5. Delete the intermediate copy once they have theirs.

### Audit a base before handing it to anyone

Whatever sits in it ships to the recipient, switched off but one click away from running. Go through
the **Automations** tab and look for anything that points at the SENDER'S systems rather than the
recipient's: webhooks, scripts, connected accounts, and anything whose name is really an internal
note. An automation the recipient innocently switches on can start sending their own records somewhere
they never chose.

## Fill the unit as well as the property

A record that points at a property but leaves the unit blank looks finished and is not. **When a
table offers both a property link and a unit link, fill both.**

The objection people reach for is "this job is not about any one unit, it is the whole building" -
a roof, the siding, the driveway, the foundation, a fire-code citation on the building. That is
real, and it is not a reason to leave the unit empty. **Most owners keep one unit per property that
stands for the building itself**, named something like "Property Level", for exactly this case. Ask
the owner what theirs is called once, write it down in their own base file, and use it from then on.

**Why it matters, and it is not neatness.** The unit link is what the base counts, groups and
reports by. A row with no unit drops out of every view and rollup built on units, so the job
disappears from the very screens meant to surface it. A unit that looks slightly wrong is visible
and gets corrected. A blank one is invisible.

**Find it with one read** rather than a lookup per property: filter the units table on the unit-name
field containing the building-wide name, pull the property link, and match. That hands you every
property's row in a single call.

**If an ACTIVE property has not got one, say so, do not improvise.** Leaving the unit blank hides
the job, and inventing a differently-worded unit ("Whole Building", "Common Area") quietly creates a
second convention that nothing filters on. Adding the row is an ordinary record write, but the NAME
has to match what the owner already uses, so confirm the spelling with them.

**⚠ Exclude archived properties BEFORE you call anything a gap.** Most owners keep sold or
no-longer-managed properties in the table behind an archive flag rather than deleting them. On the
portfolio this rule came from, the first pass counted every property row, found seven with no
building-wide unit, and reported a seven-property gap to the owner. All seven were archived. There
was no gap, and the owner had to say so. **Filter the archive flag out first, on any count, any
audit, and any "this record is missing" claim.**

### Check what reads a field before you start filling it

Filling this field correctly is the right thing to do, and it can still change what something else
prints. On the portfolio this rule came from, an e-signature automation built its job-location line
by joining street address, unit, town and state. The moment property-wide jobs carried a unit, that
line began reading "12 Example St., Property Level, Sometown, ST" on a legal release. The data was
right and the sentence was wrong.

**A rule that starts populating a field that used to be blank reaches every automation that reads
that field.** So when you begin filling one, go and look at what consumes it and check what it now
produces. This is the same habit as reading an automation's own filter before citing it as a
precedent: the change usually travels further than the reason for it.

## A job's total cost and the payment a document is about are two different numbers

When a job is paid in stages, a deposit then a balance, there are two figures and they are not
interchangeable:

- **what the job cost in total**, and
- **the amount of the specific payment the document in front of you concerns.**

**Give them separate fields.** One field cannot carry both jobs, and the moment it tries, whichever
meaning the reader assumes is the one that ends up on paper.

This is not bookkeeping fussiness. A conditional lien release on final payment releases the
contractor's claim in exchange for that check, so the amount printed on it has to BE that check. Put
the contract total on it instead and the release says the owner paid more on that payment than they
did. The automation reads whichever field it was pointed at and will not notice.

**So before writing any money value, say which field you are writing and why.** And when a document
needs an amount, ask which of the two it wants rather than reaching for the bigger number because it
is the one that was mentioned first.

## Diagnosis

| What you see | What it usually is | What to do |
|---|---|---|
| Field not found | The owner renamed it, or it never existed in this base | Re-read the schema. Never substitute a similar-looking field |
| Permission error on a base that clearly exists | The owner has screen-only access, not full base access | Read through the screens they were given instead |
| A write to a dropdown fails | The option list changed | Re-read the choices. Do not force it through |
| A duplicate empty record appeared | Something wrote a name into a link field | Delete the hollow record, then link properly |
| A computed column is wrong | Something it depends on is blank or linked wrongly | Fix the source. The computed column cannot be written |
| A value looks right in the grid but arrives as gibberish elsewhere | It is a lookup showing a friendly label while passing along an identity | Add a lookup of the value you actually want |
| Records changed and nobody did it | An automation inside the base | List the base's automations before assuming a bug |
| The result came back cut off | Too many rows, or too many columns asked for | Filter on the Airtable side and name the fields you need |
| A field you expected to gain a value instead lost its other values | An automation is writing that field, and a write replaces | Read that automation's action. Rebuild it as existing values plus the new one |
| An automation works when you edit a record but never on new ones | Record-updated triggers do not fire on creation | Add the create-time half as a second automation |
| The record looks unchanged straight after you changed it | The automation runs a second or two behind | Read it again, then check the run history before assuming it broke |
| Creating an automation fails the moment it includes a script step | The API never creates a "Run a script" action, nor edits an automation holding one | Build the shell with a placeholder action over the API, then finish the script step in the browser, or walk the owner through it |
| A base someone shared has no automations in it | It was taken through a share link, which never carries them | Ask them to invite you to a duplicate by email with Creator permission, then duplicate that into your own workspace |

## Reading a field off a found record: one property at a time

When an automation searches for a record and then uses a value from it, the natural shape is to ask
for the whole path at once. That is rejected, with an error about a function parameter mismatch that
does not mention paths at all.

**Step down one level at a time instead**, mapping once per level: first to the record's values,
then to the single field you want. The result is always an array even when you asked for one record,
so it goes through a map rather than an index; **numeric indexes into a result are rejected too.**

Two things that make this cheap rather than annoying:

- **A rejected automation saves nothing.** The previous configuration is untouched, so a failed
  attempt costs one call. Read the error and retry; do not rebuild from scratch.
- **Match the record you are looking for on something STABLE**, an id or a code, never its name.
  Names get tidied, and a lookup matched on a name breaks silently the first time someone renames
  the thing.

