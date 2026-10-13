# Troubleshooting

**Version: 1.3 - 2026-09-07**

Things that go wrong, in the words you would use to describe them. Find the one that sounds like your
problem and work down from there.

**This page will not fix anything for you, and that is deliberate.** The assistant on your own machine
is the only one who can see what is actually happening on it. This page tells you what is usually
behind a symptom and what to ask her, so you end up able to solve the next one without a page.

---

## First: ask your own Claude

**In a session running on your own computer, she can see your machine and nobody else can.** Not the
person who wrote this page, not the group channel, not anyone looking at a screenshot. When something
breaks she is the fastest and best informed help you have, and she is already open.

**In a cloud session she cannot see your computer at all.** No files, nothing you installed, nothing
on your screen. So anything about a missing program, a folder or a file has to be asked from a session
running on your own computer. If you are not sure which you are in, look at the chips along the bottom
of the message box.

Most people ask her badly. A good diagnostic ask has four parts:

1. **What you did.** "I clicked Cloud and picked my Memory Vault"
2. **What you saw**, in the exact words on the screen. Copy them, don't summarise them
3. **What you expected instead**
4. **Ask her to find the cause and tell you what she finds**, rather than quietly fixing it

Then the line that changes the answer more than anything else:

> "Read it from the actual system, don't tell me from memory"

Without it you get a confident, plausible answer built from how things usually work. With it she goes
and looks. Use it on anything to do with GitHub, your hub, your files, or whether something saved.

**When she offers a fix, ask her what was wrong before she applies it.** You are trying to end up
understanding your own system, not being carried by it.

---

## Still setting up?

Anything from your first connection lives in the **setup guide**, not here:
[`download/vera-setup.md`](../download/vera-setup.md), under "If something does not work". It holds
the click paths and it covers the ones that catch nearly everyone:

- You cannot find the GitHub connector at all
- You saw **"You don't have access to organization settings"** (your connection actually worked)
- The **Configure** button gave you a 404
- Your folder list came back empty with no error anywhere (two GitHub accounts)
- Installing git, on Windows and on Mac
- Vera cannot find a document that is open on your screen
- Vera can only see one of your Airtable bases

**This page does not repeat any of that**, on purpose. Two copies of the same instructions disagree
with each other within a week. Come back here once you are set up and something starts misbehaving.

---

## Nothing is saving

### Vera cannot find git, or git is not recognized

**Usually:** the piece that does the saving isn't installed. Claude runs perfectly well without it and
saving just quietly does nothing, which is why this one catches people twice.

**Try:** the install is different on Windows and on Mac, and the setup guide has both, including the
Mac popup that people cancel by mistake. Do it there, then fully quit Claude and open it again. Not a
new chat, quit the app.

**Ask your Claude, if it is installed and still not found:** *"git --version says not recognized after
I installed git. Find where git actually is on this machine and tell me what's missing from my PATH"*

**#tech-help if:** it installs cleanly and still isn't found after a proper restart. Say which
operating system you're on.

### Every git command gets blocked and nothing goes through

**Usually:** not a saving problem at all. She offered one long joined-up command, and joined commands
are what the permission system refuses. Your work is sitting safely on your machine the whole time.

**Try:** ask for the steps separately, and click Allow (or Always allow) on the prompts.

**Ask your Claude:** *"Don't use the combined command. Run the git steps one at a time as separate
commands: add only the files you changed, commit, pull, push, then confirm from GitHub that main has
the changes. I'll click Allow when asked"*

**Worth keeping:** any time she offers one big chained command, ask for it a step at a time. That one
habit prevents this happening again.

**#tech-help if:** the separate steps are still refused, or one returns a real error rather than a
prompt.

### I don't know which folder Claude is working in

**Usually:** nothing is wrong, you just can't see it. In a session on your own computer the folder is
shown as a chip at the bottom of the message box.

**Ask your Claude:** *"What folder are we working in? Give me the full path and open it in File
Explorer"* (or Finder on a Mac)

**#tech-help if:** the path isn't a folder you recognise, or it isn't the one holding your Memory
Vault.

### There is no Code tab, and nothing will connect

**Usually:** you're on the wrong side of Claude. Home is the chat side, and it has no working
folder on your computer and no saving loop, so no token and no sequence of steps will get your
work saved from there.

**Try:** top left of Claude there are two options, Home and Code. Home is the chat icon, Code is the
`<>` icon. Click Code. Everything in this program happens in Code.

**#tech-help if:** you're in Code and it still won't connect, and the setup guide's list hasn't got
you there.

---

## Working in the cloud

### I asked for a routine and ended up on a Cloud screen, or it says there are no connectors

**Usually:** you were working on claude.ai in a browser, or on your phone, rather than in the Claude
app on your computer. Ask for a routine there and Cloud is the only kind on offer, because that is the
only kind that place can make.

**What Cloud genuinely cannot do:** open a file on your own computer, or use a website you are signed
in to in your own browser. Every run starts from a fresh copy of a code repository and nothing of
yours is on that machine.

**What Cloud CAN do, and this catches people out in the other direction:** use the connections you
linked on claude.ai, like Google Drive, Gmail and Calendar. Those live on your account, not on your
computer, so a Cloud routine can reach them. What it cannot see is a connection you added on your own
machine rather than on claude.ai. If a session tells you connectors could not be loaded at all, that
is about that session, not about your account.

**So the question that decides it:**

- Does it need a file on your computer, or a site you are signed in to? **Local.**
- Does it only need your claude.ai connections and your repository? Cloud can do it in principle,
  though **we would still say Local**, because nobody has yet proven those connections behave the same
  way on an unattended scheduled Cloud run, and Local is known to work.

**The fix is the same either way: open the Claude app on your computer and ask her again there.**

**If she still offers you Cloud:** *"make this a local scheduled task on this machine, not a cloud
routine"*

### My Memory Vault doesn't appear when I choose Cloud

**Usually one of two things.** Either it was never granted to Claude on the GitHub side, or it belongs
to a different GitHub account from the one Claude is connected to. Two accounts, one personal and one
for work, is behind most of these and it produces an empty list with no error anywhere.

**Ask your Claude first, it's quicker than clicking:** *"Which GitHub account is Claude connected to
right now, and which account owns my Memory Vault? Read it from GitHub, don't tell me from memory"*

**Then:** the setup guide has the click path for granting it, and for what to do when the Configure
button gives you a 404. Afterwards, quit Claude fully and open it again.

**#tech-help if:** the accounts match, you've granted it, you've restarted, and it's still not listed.

### The Cloud menu is empty, my vault isn't in it

**Usually:** you're reading the wrong menu, and this is worth knowing because it looks exactly like a
fault. The Local / Cloud menu lists cloud **environments**, usually just "Default". It never lists
your vault.

**Try:** look at the chips along the bottom of the message box instead. If your vault's name and
`main` are sitting there, you're already connected. Click Cloud, choose Default, and type what you
want done.

**Don't:** click "Add cloud environment". That opens a dialog asking for a name, environment variables
and a setup script. It's developer tooling and nothing in this program needs it. Cancel it.

**#tech-help if:** the chips at the bottom are genuinely empty or show something you don't recognise.

### My work went to a claude/ branch, or Vera asks me about a pull request

**Usually the same thing both times.** A session did the work and hasn't filed it into the live copy
of your Memory Vault yet. So it either sits on a side branch, or she asks permission to move it.

**Nothing is lost.** A side branch is saved work that hasn't been filed. The live copy is what she
reads from, so work sitting on a branch doesn't shape her answers until it's merged.

**Try:** say yes when she asks, then stop being asked by telling her to finish the job herself. A
cloud session can do this on its own, whatever anyone tells you.

**Ask your Claude:** *"Merge everything to main now, then confirm from GitHub that main has today's
changes and that no claude/ branches are still ahead. From now on do that at every close-out"*

**Say no to this one:** if she suggests branch protection or adding a review step, decline. You're the
only person working in there, and a review with no reviewer just recreates the do-I-approve-this
question you're trying to get rid of.

**#tech-help if:** you said yes and it still hasn't landed on the live copy, or the merge reports
a conflict she can't resolve.

### I worked in two places at once, did I lose anything

**What it looks like:** the session on your computer says there's unsaved work, while a session on
your phone or in the browser already saved what looks like the same thing.

**Almost always: nothing is lost.** They're two real copies of the same vault and both have your work.

**Ask your Claude:** *"I've edited this from two sessions. Commit what's here, pull the other changes
on top, push, then show me from GitHub that both sets of changes are on main"*

**#tech-help if:** she reports a conflict, or the check at the end shows something missing. Say what
you changed in each place.

---

## The morning routine

### There is no way to set up my morning routine on the routines page

**Usually:** two completely different things share the name "routine", and the page you found only
makes the wrong one.

The **routines page on the website** makes routines that run on Anthropic's computers, not yours.
They start from a fresh copy of a code repository, they cannot see your machine, your files, or
anything you are signed into, and a connection you added on your own computer rather than on
claude.ai is not there either. That is a good fit for work that lives entirely inside a repository. It
is the wrong engine for your morning, because everything your morning touches, your vault, your
files, your signed-in browser, is on your computer.

**The one you want runs on your computer, and it is made somewhere else.** In the Claude app on your
machine: the **Code** tab, **Routines** in the sidebar, **New routine**, then choose **Local** rather
than Cloud. It asks you for a folder and asks you to trust that folder before it will save, and the
schedule is whichever preset it offers you.

**Easier, and what we would do:** do not build it by hand at all. Ask her, in a session on your own
computer.

**Ask your Claude:** *"Set up a scheduled task on this computer, every weekday at 9am my time, whose
whole prompt is 'Good morning, Vera' and nothing else. Make it a local task on my machine, not a
cloud routine. Then tell me where it lives so I can find it again"*

**If you already made one on the website:** delete it there and make the local one instead. It was
never going to reach your machine, so nothing is lost by removing it.

**#tech-help if:** the app on your computer has no Routines option anywhere. That usually means the
app is too old, so update it first and say which version you are on.

### My morning did not run

**Usually:** the computer was asleep, switched off, or the app was closed at that hour. A task on
your machine only fires while the machine is awake and Claude is open, and a run that lands on a
sleeping computer is skipped rather than queued up.

**You do get one catch-up, not a backlog.** When you next open the app or wake the machine, it starts
a single run for the most recently missed time and discards the older ones, and only from the last
seven days. A week away gives you one morning, not seven.

**Try:** if you want it to survive an idle machine, turn on **Keep computer awake** in Settings under
Desktop app, General. Closing the lid still puts it to sleep, so a laptop that gets shut needs the app
opened rather than a setting changed.

**Worth knowing:** because a 9am run can arrive at 11pm, tell her in the prompt what to do about that,
for example *"if it is already the afternoon, tell me what was missed instead of working the morning
list"*.

**#tech-help if:** the machine was awake, the app was open, and it still did not fire.

### It started and then just sat there doing nothing

**Usually:** it is waiting for you, not broken. The run asked to use something it had no standing
permission for and stopped at the prompt. Nothing errors and nothing tells you, so it reads as a
morning that quietly did not happen.

**Try:** open it under **Scheduled** in the sidebar. The prompt is sitting there. Answer it, and
choose **Always allow** rather than Allow, so the same thing does not stop you again tomorrow.

**Do this once, when you first create it:** click **Run now**, sit with it, and always-allow
everything it asks for. That one supervised run is what stops every future morning stalling, and it is
the step people skip.

**Ask your Claude:** *"My morning task stalled on a permission prompt. Show me everything it is
already allowed to do, and tell me what else it is likely to need, so I can approve those now instead
of one morning at a time"*

**#tech-help if:** you chose Always allow and it asks for the same thing again the next morning.

---

## Vera can't see or reach something

### Vera says a skill from the course doesn't exist

**Usually:** the skill is in the library and she simply never pulled it down. Your copies live in your
own vault and they only arrive when she fetches them.

**Ask your Claude:** *"Which skills have you actually pulled down into my vault? Then check the VA
Optional starter library for the one I asked about, and bring it in if it's missing"*

**#tech-help if:** she lists what she has, checks the library, and the skill genuinely isn't there.
That one is ours to fix, not yours. Say which skill you were looking for.

### Vera can't connect to my email

**Usually:** the direct connection to that provider doesn't work, which is not the same as there being
no way in. There is often another route through a connector you already have.

**Try:** push back rather than accepting the first answer. This is the general move and it works on
far more than email.

**Ask your Claude:** *"That won't work for me. Look at every connector I already have and find another
route to my mail. I don't want to do anything by hand"*

**#tech-help if:** she's genuinely out of routes. Say which email provider you use and which
connectors you already have switched on.

### Can Vera work with the tool I use

**Ask her, she'll go and check.** Name the tool and she'll tell you whether it has a proper
connection, a ready-made connector, or nothing, and what that means for you.

**Ask your Claude:** *"Can you connect to [tool name]? Check whether it has an API or a connector, and
tell me the best way for us to work with it"*

**The rule worth knowing up front:** she can drive a website in your browser, and she can never touch
a program installed on your computer. So the online version of a tool is usually workable and the
desktop version usually isn't. If yours is desktop only, the way through is exporting your data rather
than trying to make her click inside it.

**#tech-help if:** she says there's no route and that tool is central to how you work.

### Vera won't send my emails, she only writes drafts

**Not a fault, and not a setting to find.** Two things are going on and both are meant to be there.
The mail connection itself only ever creates drafts. And your assistant holds things for a human
anyway: nothing goes to a tenant, applicant, contractor or agency without you reading it first, and
that holds even when a routine runs while you're asleep.

**What to do:** read the draft and click send. That's the design.

**Later:** routine mail that isn't going to one of those people, the notifications you send yourself,
can be automated once you reach the automation module. **What never changes is the part above.** If
someone tells you there's a switch that makes your assistant send to a tenant unread, there isn't one.

---

## Something changed that I didn't expect

### Vera wiped the formatting on my Google Sheet

**Usually:** a hard limit rather than something you did wrong. The Drive connection can rename and
move a file, but it cannot edit inside a document that already exists. So every "update" is really
read the old one, build a new one, delete the old one, and your formatting, views and filters go with
it.

**Ask your Claude, so you can see the shape of it yourself:** *"Explain exactly what you do to my
spreadsheet each time you update it, and why the formatting doesn't survive. Then tell me whether this
data would be better in my hub, and what it would take to move it"*

**Usually the answer is to move it.** In your hub an update is a real edit, so formatting, views and
filters survive. If it has to stay a spreadsheet, batch your changes into one pass rather than asking
for an update after every finding.

**#tech-help if:** the data itself comes back wrong after a rebuild, not just the look of it. That's a
different problem and worth flagging.

### There are scheduled tasks I never set up

**Usually:** something got created as a schedule when it should have been a row in your routines
table. You should only ever have one scheduled task, the morning one. Everything else she does each
day lives as a row she reads.

**Try:** find out where they came from before deleting anything. A schedule you don't recognise is
usually a job you do want, in the wrong place.

**Ask your Claude:** *"Where did each of these scheduled tasks come from, and what does each one do?
Then move anything that should be a routine into my routines table and remove the extra schedules"*

**Worth doing:** ask her to walk you through what each one was for. It's the cheapest way to learn how
your own system is put together.

**#tech-help if:** you delete one and it comes back.

---

## It doesn't fit how I work

### The questions are all about rentals and that isn't my business

**Not a problem, and you don't have to work around it.** The material is written in landlord language
because that's where it started. The system underneath doesn't care, and it has been run against
brokerages, finance and professional services.

**Try:** tell her about your business, plainly. What you do, who's in it, what you're trying to get
off your plate. She adapts to that rather than to the example.

**Ask your Claude:** *"My business isn't rentals, it's [what you do]. Before we go further, ask me
what you need to know about it, then adjust how you work with me to match"*

**#tech-help if:** something in the course material only makes sense for rentals and you can't see the
equivalent for your business. Worth asking, others will have the same gap.

### I want projects and folders like ChatGPT has

**Use your vault instead, it does the job better.** Mirror whatever folder structure you already have
in your head as folders in your Memory Vault, tell her once, and she files things there as you go.

Then any chat, including a brand new one you open next month, can ask for what's in a folder and get
it. Chats are throwaway. The vault is the part that remembers.

**Ask your Claude:** *"Set up these folders in my Memory Vault: [your structure]. From now on file
everything we produce into the right one and tell me where it went"*

### Can I use Safari

**Chrome, or any browser built on it.** Edge and Brave both work with the same extension. Safari and
Firefox don't.

**And it's rarely urgent.** The extension only matters when she has to click around a site that has no
connection of its own. Everything else works from whatever browser you like.

---

## Chats and usage

### Should I start a new chat or keep going in this one

**Start a new one, once you've closed out.** Say "that's all" or "close session", let her wrap up and
save, then open a fresh chat for the next thing.

One long chat carrying everything you did all week gets slower, more expensive and easier to confuse.
Closing out is what moves what matters into your vault, so nothing is lost by starting again.

### Which model should I be using

**The strongest one you have, for everything, unless you're watching your usage.** The smarter the
model, the more of your allowance each message costs. On a smaller plan, keep the strong one for real
work and let a lighter one do simple reading jobs.

**Don't agonise over it.** Which model you pick is a much smaller lever than closing out and starting
fresh, which is the next entry.

### I keep running out of usage

**Usually:** long chats more than anything else. A chat that's been open all day re-reads everything in
it every single time you send a message, so the cost of each message keeps climbing.

**Try:** close out and start fresh more often. Then look at the model, per the entry above.

**#tech-help if:** you're running out fast on what feels like a normal day's work. Say roughly what
you were doing.

---

## When to bring it to #tech-help

Post in `#tech-help`, your cohort's group channel, rather than sending a direct message. The answer
then reaches everyone hitting the same thing. Private matters are the exception, those go in a DM.

**Bring it when:** you've asked your own Claude, done what she suggested, and it either didn't work or
she couldn't find the cause. That's genuinely the bar, and nobody expects you to solve everything
alone.

**Bring it straight away, without diagnosing anything**, for anything to do with your course access,
your sign-in link or your login. That isn't yours to fix.

**Include these four things**, because without them the first reply is always someone asking for them:

1. What you were trying to do
2. The exact words on your screen, copied or screenshotted
3. What you already tried, including what your Claude said
4. Whether you're working on your own computer or in the cloud, and Windows or Mac

**A short screen recording helps a lot** when something looks wrong and you can't put it into words.
Send it as well as the four things above, not instead of them.

**Nobody who answers you can see your machine.** Every reply in the channel is someone reasoning from
what you described, which is why the description is the whole game.
