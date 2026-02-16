# OpenClaw Automation Reference

Cron jobs, hooks, webhooks, Gmail PubSub, polls, auth monitoring.


---
## Automation > Auth Monitoring

[Source: https://docs.openclaw.ai/automation/auth-monitoring]

Auth Monitoring - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Automation
Auth Monitoring
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
Overview
Tools
Built-in tools
Lobster
LLM Task
Exec Tool
Web Tools
apply_patch Tool
Elevated Mode
Thinking Levels
Reactions
Browser
Browser (OpenClaw-managed)
Browser Login
Chrome Extension
Browser Troubleshooting
Agent coordination
Agent Send
Sub-Agents
Multi-Agent Sandbox &amp; Tools
Skills
Slash Commands
Skills
Skills Config
ClawHub
Plugins
Extensions
Voice Call Plugin
Zalo Personal Plugin
Automation
Hooks
Cron Jobs
Cron vs Heartbeat
Automation Troubleshooting
Webhooks
Gmail PubSub
Polls
Auth Monitoring
Media and devices
Nodes
Node Troubleshooting
Image and Media Support
Audio and Voice Notes
Camera Capture
Talk Mode
Voice Wake
Location Command
Auth monitoring
Preferred: CLI check (portable)
Optional scripts (ops / phone workflows)
Automation
Auth Monitoring
Auth monitoring
OpenClaw exposes OAuth expiry health via
openclaw models status
. Use that for
automation and alerting; scripts are optional extras for phone workflows.
Preferred: CLI check (portable)
Copy
openclaw
models
status
--check
Exit codes:
: OK
: expired or missing credentials
: expiring soon (within 24h)
This works in cron/systemd and requires no extra scripts.
Optional scripts (ops / phone workflows)
These live under
scripts/
and are
optional
. They assume SSH access to the
gateway host and are tuned for systemd + Termux.
scripts/claude-auth-status.sh
now uses
openclaw models status --json
as the
source of truth (falling back to direct file reads if the CLI is unavailable),
so keep
openclaw
PATH
for timers.
scripts/auth-monitor.sh
: cron/systemd timer target; sends alerts (ntfy or phone).
scripts/systemd/openclaw-auth-monitor.{service,timer}
: systemd user timer.
scripts/claude-auth-status.sh
: Claude Code + OpenClaw auth checker (full/json/simple).
scripts/mobile-reauth.sh
: guided re‑auth flow over SSH.
scripts/termux-quick-auth.sh
: one‑tap widget status + open auth URL.
scripts/termux-auth-widget.sh
: full guided widget flow.
scripts/termux-sync-widget.sh
: sync Claude Code creds → OpenClaw.
If you don’t need phone automation or systemd timers, skip these scripts.
Polls
Nodes

---
## Automation > Cron Jobs

[Source: https://docs.openclaw.ai/automation/cron-jobs]

Cron Jobs - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Automation
Cron Jobs
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
Overview
Tools
Built-in tools
Lobster
LLM Task
Exec Tool
Web Tools
apply_patch Tool
Elevated Mode
Thinking Levels
Reactions
Browser
Browser (OpenClaw-managed)
Browser Login
Chrome Extension
Browser Troubleshooting
Agent coordination
Agent Send
Sub-Agents
Multi-Agent Sandbox &amp; Tools
Skills
Slash Commands
Skills
Skills Config
ClawHub
Plugins
Extensions
Voice Call Plugin
Zalo Personal Plugin
Automation
Hooks
Cron Jobs
Cron vs Heartbeat
Automation Troubleshooting
Webhooks
Gmail PubSub
Polls
Auth Monitoring
Media and devices
Nodes
Node Troubleshooting
Image and Media Support
Audio and Voice Notes
Camera Capture
Talk Mode
Voice Wake
Location Command
Cron jobs (Gateway scheduler)
TL;DR
Quick start (actionable)
Tool-call equivalents (Gateway cron tool)
Where cron jobs are stored
Beginner-friendly overview
Concepts
Jobs
Schedules
Main vs isolated execution
Main session jobs (system events)
Isolated jobs (dedicated cron sessions)
Payload shapes (what runs)
Announce delivery flow
Model and thinking overrides
Delivery (channel + target)
Telegram delivery targets (topics / forum threads)
JSON schema for tool calls
cron.add params
cron.update params
cron.run and cron.remove params
Storage &amp; history
Configuration
CLI quickstart
Gateway API surface
Troubleshooting
“Nothing runs”
A recurring job keeps delaying after failures
Telegram delivers to the wrong place
Automation
Cron Jobs
Cron jobs (Gateway scheduler)
Cron vs Heartbeat?
See
Cron vs Heartbeat
for guidance on when to use each.
Cron is the Gateway’s built-in scheduler. It persists jobs, wakes the agent at
the right time, and can optionally deliver output back to a chat.
If you want
“run this every morning”
“poke the agent in 20 minutes”
cron is the mechanism.
Troubleshooting:
/automation/troubleshooting
TL;DR
Cron runs
inside the Gateway
(not inside the model).
Jobs persist under
~/.openclaw/cron/
so restarts don’t lose schedules.
Two execution styles:
Main session
: enqueue a system event, then run on the next heartbeat.
Isolated
: run a dedicated agent turn in
cron:&lt;jobId&gt;
, with delivery (announce by default or none).
Wakeups are first-class: a job can request “wake now” vs “next heartbeat”.
Webhook posting is opt-in per job: set
notify: true
and configure
cron.webhook
Quick start (actionable)
Create a one-shot reminder, verify it exists, and run it immediately:
Copy
openclaw
cron
add
--name
&quot;Reminder&quot;
--at
&quot;2026-02-01T16:00:00Z&quot;
--session
main
--system-event
&quot;Reminder: check the cron docs draft&quot;
--wake
now
--delete-after-run
openclaw
cron
list
openclaw
cron
run
&lt;
job-i
&gt;
openclaw
cron
runs
--id
&lt;
job-i
&gt;
Schedule a recurring isolated job with delivery:
Copy
openclaw
cron
add
--name
&quot;Morning brief&quot;
--cron
&quot;0 7 * * *&quot;
--tz
&quot;America/Los_Angeles&quot;
--session
isolated
--message
&quot;Summarize overnight updates.&quot;
--announce
--channel
slack
--to
&quot;channel:C1234567890&quot;
Tool-call equivalents (Gateway cron tool)
For the canonical JSON shapes and examples, see
JSON schema for tool calls
Where cron jobs are stored
Cron jobs are persisted on the Gateway host at
~/.openclaw/cron/jobs.json
by default.
The Gateway loads the file into memory and writes it back on changes, so manual edits
are only safe when the Gateway is stopped. Prefer
openclaw cron add/edit
or the cron
tool call API for changes.
Beginner-friendly overview
Think of a cron job as:
when
to run +
what
to do.
Choose a schedule
One-shot reminder →
schedule.kind = &quot;at&quot;
(CLI:
--at
Repeating job →
schedule.kind = &quot;every&quot;
schedule.kind = &quot;cron&quot;
If your ISO timestamp omits a timezone, it is treated as
UTC
Choose where it runs
sessionTarget: &quot;main&quot;
→ run during the next heartbeat with main context.
sessionTarget: &quot;isolated&quot;
→ run a dedicated agent turn in
cron:&lt;jobId&gt;
Choose the payload
Main session →
payload.kind = &quot;systemEvent&quot;
Isolated session →
payload.kind = &quot;agentTurn&quot;
Optional: one-shot jobs (
schedule.kind = &quot;at&quot;
) delete after success by default. Set
deleteAfterRun: false
to keep them (they will disable after success).
Concepts
Jobs
A cron job is a stored record with:
schedule
(when it should run),
payload
(what it should do),
optional
delivery mode
(announce or none).
optional
agent binding
agentId
): run the job under a specific agent; if
missing or unknown, the gateway falls back to the default agent.
Jobs are identified by a stable
jobId
(used by CLI/Gateway APIs).
In agent tool calls,
jobId
is canonical; legacy
is accepted for compatibility.
One-shot jobs auto-delete after success by default; set
deleteAfterRun: false
to keep them.
Schedules
Cron supports three schedule kinds:
: one-shot timestamp via
schedule.at
(ISO 8601).
every
: fixed interval (ms).
cron
: 5-field cron expression with optional IANA timezone.
Cron expressions use
croner
. If a timezone is omitted, the Gateway host’s
local timezone is used.
Main vs isolated execution
Main session jobs (system events)
Main jobs enqueue a system event and optionally wake the heartbeat runner.
They must use
payload.kind = &quot;systemEvent&quot;
wakeMode: &quot;now&quot;
(default): event triggers an immediate heartbeat run.
wakeMode: &quot;next-heartbeat&quot;
: event waits for the next scheduled heartbeat.
This is the best fit when you want the normal heartbeat prompt + main-session context.
See
Heartbeat
Isolated jobs (dedicated cron sessions)
Isolated jobs run a dedicated agent turn in session
cron:&lt;jobId&gt;
Key behaviors:
Prompt is prefixed with
[cron:&lt;jobId&gt; &lt;job name&gt;]
for traceability.
Each run starts a
fresh session id
(no prior conversation carry-over).
Default behavior: if
delivery
is omitted, isolated jobs announce a summary (
delivery.mode = &quot;announce&quot;
delivery.mode
(isolated-only) chooses what happens:
announce
: deliver a summary to the target channel and post a brief summary to the main session.
none
: internal only (no delivery, no main-session summary).
wakeMode
controls when the main-session summary posts:
now
: immediate heartbeat.
next-heartbeat
: waits for the next scheduled heartbeat.
Use isolated jobs for noisy, frequent, or “background chores” that shouldn’t spam
your main chat history.
Payload shapes (what runs)
Two payload kinds are supported:
systemEvent
: main-session only, routed through the heartbeat prompt.
agentTurn
: isolated-session only, runs a dedicated agent turn.
Common
agentTurn
fields:
message
: required text prompt.
model
thinking
: optional overrides (see below).
timeoutSeconds
: optional timeout override.
Delivery config (isolated jobs only):
delivery.mode
none
announce
delivery.channel
last
or a specific channel.
delivery.to
: channel-specific target (phone/chat/channel id).
delivery.bestEffort
: avoid failing the job if announce delivery fails.
Announce delivery suppresses messaging tool sends for the run; use
delivery.channel
delivery.to
to target the chat instead. When
delivery.mode = &quot;none&quot;
, no summary is posted to the main session.
delivery
is omitted for isolated jobs, OpenClaw defaults to
announce
Announce delivery flow
When
delivery.mode = &quot;announce&quot;
, cron delivers directly via the outbound channel adapters.
The main agent is not spun up to craft or forward the message.
Behavior details:
Content: delivery uses the isolated run’s outbound payloads (text/media) with normal chunking and
channel formatting.
Heartbeat-only responses (
HEARTBEAT_OK
with no real content) are not delivered.
If the isolated run already sent a message to the same target via the message tool, delivery is
skipped to avoid duplicates.
Missing or invalid delivery targets fail the job unless
delivery.bestEffort = true
A short summary is posted to the main session only when
delivery.mode = &quot;announce&quot;
The main-session summary respects
wakeMode
now
triggers an immediate heartbeat and
next-heartbeat
waits for the next scheduled heartbeat.
Model and thinking overrides
Isolated jobs (
agentTurn
) can override the model and thinking level:
model
: Provider/model string (e.g.,
anthropic/claude-sonnet-4-20250514
) or alias (e.g.,
opus
thinking
: Thinking level (
off
minimal
low
medium
high
xhigh
; GPT-5.2 + Codex models only)
Note: You can set
model
on main-session jobs too, but it changes the shared main
session model. We recommend model overrides only for isolated jobs to avoid
unexpected context shifts.
Resolution priority:
Job payload override (highest)
Hook-specific defaults (e.g.,
hooks.gmail.model
Agent config default
Delivery (channel + target)
Isolated jobs can deliver output to a channel via the top-level
delivery
config:
delivery.mode
announce
(deliver a summary) or
none
delivery.channel
whatsapp
telegram
discord
slack
mattermost
(plugin) /
signal
imessage
last
delivery.to
: channel-specific recipient target.
Delivery config is only valid for isolated jobs (
sessionTarget: &quot;isolated&quot;
delivery.channel
delivery.to
is omitted, cron can fall back to the main session’s
“last route” (the last place the agent replied).
Target format reminders:
Slack/Discord/Mattermost (plugin) targets should use explicit prefixes (e.g.
channel:&lt;id&gt;
user:&lt;id&gt;
) to avoid ambiguity.
Telegram topics should use the
:topic:
form (see below).
Telegram delivery targets (topics / forum threads)
Telegram supports forum topics via
message_thread_id
. For cron delivery, you can encode
the topic/thread into the
field:
-1001234567890
(chat id only)
-1001234567890:topic:123
(preferred: explicit topic marker)
-1001234567890:123
(shorthand: numeric suffix)
Prefixed targets like
telegram:...
telegram:group:...
are also accepted:
telegram:group:-1001234567890:topic:123
JSON schema for tool calls
Use these shapes when calling Gateway
cron.*
tools directly (agent tool calls or RPC).
CLI flags accept human durations like
20m
, but tool calls should use an ISO 8601 string
for
schedule.at
and milliseconds for
schedule.everyMs
cron.add params
One-shot, main session job (system event):
Copy
&quot;name&quot;
&quot;Reminder&quot;
&quot;schedule&quot;
&quot;kind&quot;
&quot;at&quot;
&quot;at&quot;
&quot;2026-02-01T16:00:00Z&quot;
&quot;sessionTarget&quot;
&quot;main&quot;
&quot;wakeMode&quot;
&quot;now&quot;
&quot;payload&quot;
&quot;kind&quot;
&quot;systemEvent&quot;
&quot;text&quot;
&quot;Reminder text&quot;
&quot;deleteAfterRun&quot;
true
Recurring, isolated job with delivery:
Copy
&quot;name&quot;
&quot;Morning brief&quot;
&quot;schedule&quot;
&quot;kind&quot;
&quot;cron&quot;
&quot;expr&quot;
&quot;0 7 * * *&quot;
&quot;tz&quot;
&quot;America/Los_Angeles&quot;
&quot;sessionTarget&quot;
&quot;isolated&quot;
&quot;wakeMode&quot;
&quot;next-heartbeat&quot;
&quot;payload&quot;
&quot;kind&quot;
&quot;agentTurn&quot;
&quot;message&quot;
&quot;Summarize overnight updates.&quot;
&quot;delivery&quot;
&quot;mode&quot;
&quot;announce&quot;
&quot;channel&quot;
&quot;slack&quot;
&quot;to&quot;
&quot;channel:C1234567890&quot;
&quot;bestEffort&quot;
true
Notes:
schedule.kind
every
everyMs
), or
cron
expr
, optional
schedule.at
accepts ISO 8601 (timezone optional; treated as UTC when omitted).
everyMs
is milliseconds.
sessionTarget
must be
&quot;main&quot;
&quot;isolated&quot;
and must match
payload.kind
Optional fields:
agentId
description
enabled
notify
deleteAfterRun
(defaults to true for
delivery
wakeMode
defaults to
&quot;now&quot;
when omitted.
cron.update params
Copy
&quot;jobId&quot;
&quot;job-123&quot;
&quot;patch&quot;
&quot;enabled&quot;
false
&quot;schedule&quot;
&quot;kind&quot;
&quot;every&quot;
&quot;everyMs&quot;
3600000
Notes:
jobId
is canonical;
is accepted for compatibility.
Use
agentId: null
in the patch to clear an agent binding.
cron.run and cron.remove params
Copy
&quot;jobId&quot;
&quot;job-123&quot;
&quot;mode&quot;
&quot;force&quot;
Copy
&quot;jobId&quot;
&quot;job-123&quot;
Storage &amp; history
Job store:
~/.openclaw/cron/jobs.json
(Gateway-managed JSON).
Run history:
~/.openclaw/cron/runs/&lt;jobId&gt;.jsonl
(JSONL, auto-pruned).
Override store path:
cron.store
in config.
Configuration
Copy
cron
enabled
true
// default true
store
&quot;~/.openclaw/cron/jobs.json&quot;
maxConcurrentRuns
// default 1
webhook
&quot;https://example.invalid/cron-finished&quot;
// optional finished-run webhook endpoint
webhookToken
&quot;replace-with-dedicated-webhook-token&quot;
// optional, do not reuse gateway auth token
Webhook behavior:
The Gateway posts finished run events to
cron.webhook
only when the job has
notify: true
Payload is the cron finished event JSON.
cron.webhookToken
is set, auth header is
Authorization: Bearer &lt;cron.webhookToken&gt;
cron.webhookToken
is not set, no
Authorization
header is sent.
Disable cron entirely:
cron.enabled: false
(config)
OPENCLAW_SKIP_CRON=1
(env)
CLI quickstart
One-shot reminder (UTC ISO, auto-delete after success):
Copy
openclaw
cron
add
--name
&quot;Send reminder&quot;
--at
&quot;2026-01-12T18:00:00Z&quot;
--session
main
--system-event
&quot;Reminder: submit expense report.&quot;
--wake
now
--delete-after-run
One-shot reminder (main session, wake immediately):
Copy
openclaw
cron
add
--name
&quot;Calendar check&quot;
--at
&quot;20m&quot;
--session
main
--system-event
&quot;Next heartbeat: check calendar.&quot;
--wake
now
Recurring isolated job (announce to WhatsApp):
Copy
openclaw
cron
add
--name
&quot;Morning status&quot;
--cron
&quot;0 7 * * *&quot;
--tz
&quot;America/Los_Angeles&quot;
--session
isolated
--message
&quot;Summarize inbox + calendar for today.&quot;
--announce
--channel
whatsapp
--to
&quot;+15551234567&quot;
Recurring isolated job (deliver to a Telegram topic):
Copy
openclaw
cron
add
--name
&quot;Nightly summary (topic)&quot;
--cron
&quot;0 22 * * *&quot;
--tz
&quot;America/Los_Angeles&quot;
--session
isolated
--message
&quot;Summarize today; send to the nightly topic.&quot;
--announce
--channel
telegram
--to
&quot;-1001234567890:topic:123&quot;
Isolated job with model and thinking override:
Copy
openclaw
cron
add
--name
&quot;Deep analysis&quot;
--cron
&quot;0 6 * * 1&quot;
--tz
&quot;America/Los_Angeles&quot;
--session
isolated
--message
&quot;Weekly deep analysis of project progress.&quot;
--model
&quot;opus&quot;
--thinking
high
--announce
--channel
whatsapp
--to
&quot;+15551234567&quot;
Agent selection (multi-agent setups):
Copy
# Pin a job to agent &quot;ops&quot; (falls back to default if that agent is missing)
openclaw
cron
add
--name
&quot;Ops sweep&quot;
--cron
&quot;0 6 * * *&quot;
--session
isolated
--message
&quot;Check ops queue&quot;
--agent
ops
# Switch or clear the agent on an existing job
openclaw
cron
edit
&lt;
jobI
&gt;
--agent
ops
openclaw
cron
edit
&lt;
jobI
&gt;
--clear-agent
Manual run (force is the default, use
--due
to only run when due):
Copy
openclaw
cron
run
&lt;
jobI
&gt;
openclaw
cron
run
&lt;
jobI
&gt;
--due
Edit an existing job (patch fields):
Copy
openclaw
cron
edit
&lt;
jobI
&gt;
--message
&quot;Updated prompt&quot;
--model
&quot;opus&quot;
--thinking
low
Run history:
Copy
openclaw
cron
runs
--id
&lt;
jobI
&gt;
--limit
Immediate system event without creating a job:
Copy
openclaw
system
event
--mode
now
--text
&quot;Next heartbeat: check battery.&quot;
Gateway API surface
cron.list
cron.status
cron.add
cron.update
cron.remove
cron.run
(force or due),
cron.runs
For immediate system events without a job, use
openclaw system event
Troubleshooting
“Nothing runs”
Check cron is enabled:
cron.enabled
and
OPENCLAW_SKIP_CRON
Check the Gateway is running continuously (cron runs inside the Gateway process).
For
cron
schedules: confirm timezone (
--tz
) vs the host timezone.
A recurring job keeps delaying after failures
OpenClaw applies exponential retry backoff for recurring jobs after consecutive errors:
30s, 1m, 5m, 15m, then 60m between retries.
Backoff resets automatically after the next successful run.
One-shot (
) jobs disable after a terminal run (
error
, or
skipped
) and do not retry.
Telegram delivers to the wrong place
For forum topics, use
-100…:topic:&lt;id&gt;
so it’s explicit and unambiguous.
If you see
telegram:...
prefixes in logs or stored “last route” targets, that’s normal;
cron delivery accepts them and still parses topic IDs correctly.
Hooks
Cron vs Heartbeat

---
## Automation > Cron Vs Heartbeat

[Source: https://docs.openclaw.ai/automation/cron-vs-heartbeat]

Cron vs Heartbeat - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Automation
Cron vs Heartbeat
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
Overview
Tools
Built-in tools
Lobster
LLM Task
Exec Tool
Web Tools
apply_patch Tool
Elevated Mode
Thinking Levels
Reactions
Browser
Browser (OpenClaw-managed)
Browser Login
Chrome Extension
Browser Troubleshooting
Agent coordination
Agent Send
Sub-Agents
Multi-Agent Sandbox &amp; Tools
Skills
Slash Commands
Skills
Skills Config
ClawHub
Plugins
Extensions
Voice Call Plugin
Zalo Personal Plugin
Automation
Hooks
Cron Jobs
Cron vs Heartbeat
Automation Troubleshooting
Webhooks
Gmail PubSub
Polls
Auth Monitoring
Media and devices
Nodes
Node Troubleshooting
Image and Media Support
Audio and Voice Notes
Camera Capture
Talk Mode
Voice Wake
Location Command
Cron vs Heartbeat: When to Use Each
Quick Decision Guide
Heartbeat: Periodic Awareness
When to use heartbeat
Heartbeat advantages
Heartbeat example: HEARTBEAT.md checklist
Configuring heartbeat
Cron: Precise Scheduling
When to use cron
Cron advantages
Cron example: Daily morning briefing
Cron example: One-shot reminder
Decision Flowchart
Combining Both
Example: Efficient automation setup
Lobster: Deterministic workflows with approvals
When Lobster fits
How it pairs with heartbeat and cron
Operational notes (from the code)
Main Session vs Isolated Session
When to use main session cron
When to use isolated cron
Cost Considerations
Related
Automation
Cron vs Heartbeat
Cron vs Heartbeat: When to Use Each
Both heartbeats and cron jobs let you run tasks on a schedule. This guide helps you choose the right mechanism for your use case.
Quick Decision Guide
Use Case
Recommended
Why
Check inbox every 30 min
Heartbeat
Batches with other checks, context-aware
Send daily report at 9am sharp
Cron (isolated)
Exact timing needed
Monitor calendar for upcoming events
Heartbeat
Natural fit for periodic awareness
Run weekly deep analysis
Cron (isolated)
Standalone task, can use different model
Remind me in 20 minutes
Cron (main,
--at
One-shot with precise timing
Background project health check
Heartbeat
Piggybacks on existing cycle
Heartbeat: Periodic Awareness
Heartbeats run in the
main session
at a regular interval (default: 30 min). They’re designed for the agent to check on things and surface anything important.
When to use heartbeat
Multiple periodic checks
: Instead of 5 separate cron jobs checking inbox, calendar, weather, notifications, and project status, a single heartbeat can batch all of these.
Context-aware decisions
: The agent has full main-session context, so it can make smart decisions about what’s urgent vs. what can wait.
Conversational continuity
: Heartbeat runs share the same session, so the agent remembers recent conversations and can follow up naturally.
Low-overhead monitoring
: One heartbeat replaces many small polling tasks.
Heartbeat advantages
Batches multiple checks
: One agent turn can review inbox, calendar, and notifications together.
Reduces API calls
: A single heartbeat is cheaper than 5 isolated cron jobs.
Context-aware
: The agent knows what you’ve been working on and can prioritize accordingly.
Smart suppression
: If nothing needs attention, the agent replies
HEARTBEAT_OK
and no message is delivered.
Natural timing
: Drifts slightly based on queue load, which is fine for most monitoring.
Heartbeat example: HEARTBEAT.md checklist
Copy
# Heartbeat checklist
- Check email for urgent messages
- Review calendar for events in next 2 hours
- If a background task finished, summarize results
- If idle for 8+ hours, send a brief check-in
The agent reads this on each heartbeat and handles all items in one turn.
Configuring heartbeat
Copy
agents
defaults
heartbeat
every
&quot;30m&quot;
// interval
target
&quot;last&quot;
// where to deliver alerts
activeHours
start
&quot;08:00&quot;
end
&quot;22:00&quot;
// optional
See
Heartbeat
for full configuration.
Cron: Precise Scheduling
Cron jobs run at
exact times
and can run in isolated sessions without affecting main context.
When to use cron
Exact timing required
: “Send this at 9:00 AM every Monday” (not “sometime around 9”).
Standalone tasks
: Tasks that don’t need conversational context.
Different model/thinking
: Heavy analysis that warrants a more powerful model.
One-shot reminders
: “Remind me in 20 minutes” with
--at
Noisy/frequent tasks
: Tasks that would clutter main session history.
External triggers
: Tasks that should run independently of whether the agent is otherwise active.
Cron advantages
Exact timing
: 5-field cron expressions with timezone support.
Session isolation
: Runs in
cron:&lt;jobId&gt;
without polluting main history.
Model overrides
: Use a cheaper or more powerful model per job.
Delivery control
: Isolated jobs default to
announce
(summary); choose
none
as needed.
Immediate delivery
: Announce mode posts directly without waiting for heartbeat.
No agent context needed
: Runs even if main session is idle or compacted.
One-shot support
--at
for precise future timestamps.
Cron example: Daily morning briefing
Copy
openclaw
cron
add
--name
&quot;Morning briefing&quot;
--cron
&quot;0 7 * * *&quot;
--tz
&quot;America/New_York&quot;
--session
isolated
--message
&quot;Generate today&#x27;s briefing: weather, calendar, top emails, news summary.&quot;
--model
opus
--announce
--channel
whatsapp
--to
&quot;+15551234567&quot;
This runs at exactly 7:00 AM New York time, uses Opus for quality, and announces a summary directly to WhatsApp.
Cron example: One-shot reminder
Copy
openclaw
cron
add
--name
&quot;Meeting reminder&quot;
--at
&quot;20m&quot;
--session
main
--system-event
&quot;Reminder: standup meeting starts in 10 minutes.&quot;
--wake
now
--delete-after-run
See
Cron jobs
for full CLI reference.
Decision Flowchart
Copy
Does the task need to run at an EXACT time?
YES -&gt; Use cron
NO -&gt; Continue...
Does the task need isolation from main session?
YES -&gt; Use cron (isolated)
NO -&gt; Continue...
Can this task be batched with other periodic checks?
YES -&gt; Use heartbeat (add to HEARTBEAT.md)
NO -&gt; Use cron
Is this a one-shot reminder?
YES -&gt; Use cron with --at
NO -&gt; Continue...
Does it need a different model or thinking level?
YES -&gt; Use cron (isolated) with --model/--thinking
NO -&gt; Use heartbeat
Combining Both
The most efficient setup uses
both
Heartbeat
handles routine monitoring (inbox, calendar, notifications) in one batched turn every 30 minutes.
Cron
handles precise schedules (daily reports, weekly reviews) and one-shot reminders.
Example: Efficient automation setup
HEARTBEAT.md
(checked every 30 min):
Copy
# Heartbeat checklist
- Scan inbox for urgent emails
- Check calendar for events in next 2h
- Review any pending tasks
- Light check-in if quiet for 8+ hours
Cron jobs
(precise timing):
Copy
# Daily morning briefing at 7am
openclaw
cron
add
--name
&quot;Morning brief&quot;
--cron
&quot;0 7 * * *&quot;
--session
isolated
--message
&quot;...&quot;
--announce
# Weekly project review on Mondays at 9am
openclaw
cron
add
--name
&quot;Weekly review&quot;
--cron
&quot;0 9 * * 1&quot;
--session
isolated
--message
&quot;...&quot;
--model
opus
# One-shot reminder
openclaw
cron
add
--name
&quot;Call back&quot;
--at
&quot;2h&quot;
--session
main
--system-event
&quot;Call back the client&quot;
--wake
now
Lobster: Deterministic workflows with approvals
Lobster is the workflow runtime for
multi-step tool pipelines
that need deterministic execution and explicit approvals.
Use it when the task is more than a single agent turn, and you want a resumable workflow with human checkpoints.
When Lobster fits
Multi-step automation
: You need a fixed pipeline of tool calls, not a one-off prompt.
Approval gates
: Side effects should pause until you approve, then resume.
Resumable runs
: Continue a paused workflow without re-running earlier steps.
How it pairs with heartbeat and cron
Heartbeat/cron
decide
when
a run happens.
Lobster
defines
what steps
happen once the run starts.
For scheduled workflows, use cron or heartbeat to trigger an agent turn that calls Lobster.
For ad-hoc workflows, call Lobster directly.
Operational notes (from the code)
Lobster runs as a
local subprocess
lobster
CLI) in tool mode and returns a
JSON envelope
If the tool returns
needs_approval
, you resume with a
resumeToken
and
approve
flag.
The tool is an
optional plugin
; enable it additively via
tools.alsoAllow: [&quot;lobster&quot;]
(recommended).
If you pass
lobsterPath
, it must be an
absolute path
See
Lobster
for full usage and examples.
Main Session vs Isolated Session
Both heartbeat and cron can interact with the main session, but differently:
Heartbeat
Cron (main)
Cron (isolated)
Session
Main
Main (via system event)
cron:&lt;jobId&gt;
History
Shared
Shared
Fresh each run
Context
Full
Full
None (starts clean)
Model
Main session model
Main session model
Can override
Output
Delivered if not
HEARTBEAT_OK
Heartbeat prompt + event
Announce summary (default)
When to use main session cron
Use
--session main
with
--system-event
when you want:
The reminder/event to appear in main session context
The agent to handle it during the next heartbeat with full context
No separate isolated run
Copy
openclaw
cron
add
--name
&quot;Check project&quot;
--every
&quot;4h&quot;
--session
main
--system-event
&quot;Time for a project health check&quot;
--wake
now
When to use isolated cron
Use
--session isolated
when you want:
A clean slate without prior context
Different model or thinking settings
Announce summaries directly to a channel
History that doesn’t clutter main session
Copy
openclaw
cron
add
--name
&quot;Deep analysis&quot;
--cron
&quot;0 6 * * 0&quot;
--session
isolated
--message
&quot;Weekly codebase analysis...&quot;
--model
opus
--thinking
high
--announce
Cost Considerations
Mechanism
Cost Profile
Heartbeat
One turn every N minutes; scales with HEARTBEAT.md size
Cron (main)
Adds event to next heartbeat (no isolated turn)
Cron (isolated)
Full agent turn per job; can use cheaper model
Tips
Keep
HEARTBEAT.md
small to minimize token overhead.
Batch similar checks into heartbeat instead of multiple cron jobs.
Use
target: &quot;none&quot;
on heartbeat if you only want internal processing.
Use isolated cron with a cheaper model for routine tasks.
Related
Heartbeat
- full heartbeat configuration
Cron jobs
- full cron CLI and API reference
System
- system events + heartbeat controls
Cron Jobs
Automation Troubleshooting

---
## Automation > Gmail Pubsub

[Source: https://docs.openclaw.ai/automation/gmail-pubsub]

Gmail PubSub - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Automation
Gmail PubSub
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
Overview
Tools
Built-in tools
Lobster
LLM Task
Exec Tool
Web Tools
apply_patch Tool
Elevated Mode
Thinking Levels
Reactions
Browser
Browser (OpenClaw-managed)
Browser Login
Chrome Extension
Browser Troubleshooting
Agent coordination
Agent Send
Sub-Agents
Multi-Agent Sandbox &amp; Tools
Skills
Slash Commands
Skills
Skills Config
ClawHub
Plugins
Extensions
Voice Call Plugin
Zalo Personal Plugin
Automation
Hooks
Cron Jobs
Cron vs Heartbeat
Automation Troubleshooting
Webhooks
Gmail PubSub
Polls
Auth Monitoring
Media and devices
Nodes
Node Troubleshooting
Image and Media Support
Audio and Voice Notes
Camera Capture
Talk Mode
Voice Wake
Location Command
Gmail Pub/Sub -&gt; OpenClaw
Prereqs
Wizard (recommended)
One-time setup
Start the watch
Run the push handler
Expose the handler (advanced, unsupported)
Test
Troubleshooting
Cleanup
Automation
Gmail PubSub
Gmail Pub/Sub -&gt; OpenClaw
Goal: Gmail watch -&gt; Pub/Sub push -&gt;
gog gmail watch serve
-&gt; OpenClaw webhook.
Prereqs
gcloud
installed and logged in (
install guide
gog
(gogcli) installed and authorized for the Gmail account (
gogcli.sh
OpenClaw hooks enabled (see
Webhooks
tailscale
logged in (
tailscale.com
). Supported setup uses Tailscale Funnel for the public HTTPS endpoint.
Other tunnel services can work, but are DIY/unsupported and require manual wiring.
Right now, Tailscale is what we support.
Example hook config (enable Gmail preset mapping):
Copy
hooks
enabled
true
token
&quot;OPENCLAW_HOOK_TOKEN&quot;
path
&quot;/hooks&quot;
presets
&quot;gmail&quot;
To deliver the Gmail summary to a chat surface, override the preset with a mapping
that sets
deliver
+ optional
channel
Copy
hooks
enabled
true
token
&quot;OPENCLAW_HOOK_TOKEN&quot;
presets
&quot;gmail&quot;
mappings
match
path
&quot;gmail&quot;
action
&quot;agent&quot;
wakeMode
&quot;now&quot;
name
&quot;Gmail&quot;
sessionKey
&quot;hook:gmail:{{messages[0].id}}&quot;
messageTemplate
&quot;New email from {{messages[0].from}}\nSubject: {{messages[0].subject}}\n{{messages[0].snippet}}\n{{messages[0].body}}&quot;
model
&quot;openai/gpt-5.2-mini&quot;
deliver
true
channel
&quot;last&quot;
// to: &quot;+15551234567&quot;
If you want a fixed channel, set
channel
. Otherwise
channel: &quot;last&quot;
uses the last delivery route (falls back to WhatsApp).
To force a cheaper model for Gmail runs, set
model
in the mapping
provider/model
or alias). If you enforce
agents.defaults.models
, include it there.
To set a default model and thinking level specifically for Gmail hooks, add
hooks.gmail.model
hooks.gmail.thinking
in your config:
Copy
hooks
gmail
model
&quot;openrouter/meta-llama/llama-3.3-70b-instruct:free&quot;
thinking
&quot;off&quot;
Notes:
Per-hook
model
thinking
in the mapping still overrides these defaults.
Fallback order:
hooks.gmail.model
agents.defaults.model.fallbacks
→ primary (auth/rate-limit/timeouts).
agents.defaults.models
is set, the Gmail model must be in the allowlist.
Gmail hook content is wrapped with external-content safety boundaries by default.
To disable (dangerous), set
hooks.gmail.allowUnsafeExternalContent: true
To customize payload handling further, add
hooks.mappings
or a JS/TS transform module
under
~/.openclaw/hooks/transforms
(see
Webhooks
Wizard (recommended)
Use the OpenClaw helper to wire everything together (installs deps on macOS via brew):
Copy
openclaw
webhooks
gmail
setup
--account
[email&#160;protected]
Defaults:
Uses Tailscale Funnel for the public push endpoint.
Writes
hooks.gmail
config for
openclaw webhooks gmail run
Enables the Gmail hook preset (
hooks.presets: [&quot;gmail&quot;]
Path note: when
tailscale.mode
is enabled, OpenClaw automatically sets
hooks.gmail.serve.path
and keeps the public path at
hooks.gmail.tailscale.path
(default
/gmail-pubsub
) because Tailscale
strips the set-path prefix before proxying.
If you need the backend to receive the prefixed path, set
hooks.gmail.tailscale.target
(or
--tailscale-target
) to a full URL like
http://127.0.0.1:8788/gmail-pubsub
and match
hooks.gmail.serve.path
Want a custom endpoint? Use
--push-endpoint &lt;url&gt;
--tailscale off
Platform note: on macOS the wizard installs
gcloud
gogcli
, and
tailscale
via Homebrew; on Linux install them manually first.
Gateway auto-start (recommended):
When
hooks.enabled=true
and
hooks.gmail.account
is set, the Gateway starts
gog gmail watch serve
on boot and auto-renews the watch.
Set
OPENCLAW_SKIP_GMAIL_WATCHER=1
to opt out (useful if you run the daemon yourself).
Do not run the manual daemon at the same time, or you will hit
listen tcp 127.0.0.1:8788: bind: address already in use
Manual daemon (starts
gog gmail watch serve
+ auto-renew):
Copy
openclaw
webhooks
gmail
run
One-time setup
Select the GCP project
that owns the OAuth client
used by
gog
Copy
gcloud
auth
login
gcloud
config
set
project
&lt;
project-i
&gt;
Note: Gmail watch requires the Pub/Sub topic to live in the same project as the OAuth client.
Enable APIs:
Copy
gcloud
services
enable
gmail.googleapis.com
pubsub.googleapis.com
Create a topic:
Copy
gcloud
pubsub
topics
create
gog-gmail-watch
Allow Gmail push to publish:
Copy
gcloud
pubsub
topics
add-iam-policy-binding
gog-gmail-watch
--member=serviceAccount:
[email&#160;protected]
--role=roles/pubsub.publisher
Start the watch
Copy
gog
gmail
watch
start
--account
[email&#160;protected]
--label
INBOX
--topic
projects/
&lt;
project-i
&gt;
/topics/gog-gmail-watch
Save the
history_id
from the output (for debugging).
Run the push handler
Local example (shared token auth):
Copy
gog
gmail
watch
serve
--account
[email&#160;protected]
--bind
127.0.0.1
--port
8788
--path
/gmail-pubsub
--token
&lt;
share
&gt;
--hook-url
http://127.0.0.1:18789/hooks/gmail
--hook-token
OPENCLAW_HOOK_TOKEN
--include-body
--max-bytes
20000
Notes:
--token
protects the push endpoint (
x-gog-token
?token=
--hook-url
points to OpenClaw
/hooks/gmail
(mapped; isolated run + summary to main).
--include-body
and
--max-bytes
control the body snippet sent to OpenClaw.
Recommended:
openclaw webhooks gmail run
wraps the same flow and auto-renews the watch.
Expose the handler (advanced, unsupported)
If you need a non-Tailscale tunnel, wire it manually and use the public URL in the push
subscription (unsupported, no guardrails):
Copy
cloudflared
tunnel
--url
http://127.0.0.1:8788
--no-autoupdate
Use the generated URL as the push endpoint:
Copy
gcloud
pubsub
subscriptions
create
gog-gmail-watch-push
--topic
gog-gmail-watch
--push-endpoint
&quot;https://&lt;public-url&gt;/gmail-pubsub?token=&lt;shared&gt;&quot;
Production: use a stable HTTPS endpoint and configure Pub/Sub OIDC JWT, then run:
Copy
gog
gmail
watch
serve
--verify-oidc
--oidc-email
&lt;
svc@..
&gt;
Test
Send a message to the watched inbox:
Copy
gog
gmail
send
--account
[email&#160;protected]
--to
[email&#160;protected]
--subject
&quot;watch test&quot;
--body
&quot;ping&quot;
Check watch state and history:
Copy
gog
gmail
watch
status
--account
[email&#160;protected]
gog
gmail
history
--account
[email&#160;protected]
--since
&lt;
historyI
&gt;
Troubleshooting
Invalid topicName
: project mismatch (topic not in the OAuth client project).
User not authorized
: missing
roles/pubsub.publisher
on the topic.
Empty messages: Gmail push only provides
historyId
; fetch via
gog gmail history
Cleanup
Copy
gog
gmail
watch
stop
--account
[email&#160;protected]
gcloud
pubsub
subscriptions
delete
gog-gmail-watch-push
gcloud
pubsub
topics
delete
gog-gmail-watch
Webhooks
Polls

---
## Automation > Hooks

[Source: https://docs.openclaw.ai/automation/hooks]

Hooks - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Automation
Hooks
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
Overview
Tools
Built-in tools
Lobster
LLM Task
Exec Tool
Web Tools
apply_patch Tool
Elevated Mode
Thinking Levels
Reactions
Browser
Browser (OpenClaw-managed)
Browser Login
Chrome Extension
Browser Troubleshooting
Agent coordination
Agent Send
Sub-Agents
Multi-Agent Sandbox &amp; Tools
Skills
Slash Commands
Skills
Skills Config
ClawHub
Plugins
Extensions
Voice Call Plugin
Zalo Personal Plugin
Automation
Hooks
Cron Jobs
Cron vs Heartbeat
Automation Troubleshooting
Webhooks
Gmail PubSub
Polls
Auth Monitoring
Media and devices
Nodes
Node Troubleshooting
Image and Media Support
Audio and Voice Notes
Camera Capture
Talk Mode
Voice Wake
Location Command
Hooks
Getting Oriented
Overview
Getting Started
Bundled Hooks
Onboarding
Hook Discovery
Hook Packs (npm/archives)
Hook Structure
HOOK.md Format
Metadata Fields
Handler Implementation
Event Context
Event Types
Command Events
Agent Events
Gateway Events
Tool Result Hooks (Plugin API)
Future Events
Creating Custom Hooks
1. Choose Location
2. Create Directory Structure
3. Create HOOK.md
4. Create handler.ts
5. Enable and Test
Configuration
New Config Format (Recommended)
Per-Hook Configuration
Extra Directories
Legacy Config Format (Still Supported)
CLI Commands
List Hooks
Hook Information
Check Eligibility
Enable/Disable
Bundled hook reference
session-memory
bootstrap-extra-files
command-logger
boot-md
Best Practices
Keep Handlers Fast
Handle Errors Gracefully
Filter Events Early
Use Specific Event Keys
Debugging
Enable Hook Logging
Check Discovery
Check Registration
Verify Eligibility
Testing
Gateway Logs
Test Hooks Directly
Architecture
Core Components
Discovery Flow
Event Flow
Troubleshooting
Hook Not Discovered
Hook Not Eligible
Hook Not Executing
Handler Errors
Migration Guide
From Legacy Config to Discovery
See Also
Automation
Hooks
Hooks
Hooks provide an extensible event-driven system for automating actions in response to agent commands and events. Hooks are automatically discovered from directories and can be managed via CLI commands, similar to how skills work in OpenClaw.
Getting Oriented
Hooks are small scripts that run when something happens. There are two kinds:
Hooks
(this page): run inside the Gateway when agent events fire, like
/new
/reset
/stop
, or lifecycle events.
Webhooks
: external HTTP webhooks that let other systems trigger work in OpenClaw. See
Webhook Hooks
or use
openclaw webhooks
for Gmail helper commands.
Hooks can also be bundled inside plugins; see
Plugins
Common uses:
Save a memory snapshot when you reset a session
Keep an audit trail of commands for troubleshooting or compliance
Trigger follow-up automation when a session starts or ends
Write files into the agent workspace or call external APIs when events fire
If you can write a small TypeScript function, you can write a hook. Hooks are discovered automatically, and you enable or disable them via the CLI.
Overview
The hooks system allows you to:
Save session context to memory when
/new
is issued
Log all commands for auditing
Trigger custom automations on agent lifecycle events
Extend OpenClaw’s behavior without modifying core code
Getting Started
Bundled Hooks
OpenClaw ships with four bundled hooks that are automatically discovered:
💾 session-memory
: Saves session context to your agent workspace (default
~/.openclaw/workspace/memory/
) when you issue
/new
📎 bootstrap-extra-files
: Injects additional workspace bootstrap files from configured glob/path patterns during
agent:bootstrap
📝 command-logger
: Logs all command events to
~/.openclaw/logs/commands.log
🚀 boot-md
: Runs
BOOT.md
when the gateway starts (requires internal hooks enabled)
List available hooks:
Copy
openclaw
hooks
list
Enable a hook:
Copy
openclaw
hooks
enable
session-memory
Check hook status:
Copy
openclaw
hooks
check
Get detailed information:
Copy
openclaw
hooks
info
session-memory
Onboarding
During onboarding (
openclaw onboard
), you’ll be prompted to enable recommended hooks. The wizard automatically discovers eligible hooks and presents them for selection.
Hook Discovery
Hooks are automatically discovered from three directories (in order of precedence):
Workspace hooks
&lt;workspace&gt;/hooks/
(per-agent, highest precedence)
Managed hooks
~/.openclaw/hooks/
(user-installed, shared across workspaces)
Bundled hooks
&lt;openclaw&gt;/dist/hooks/bundled/
(shipped with OpenClaw)
Managed hook directories can be either a
single hook
or a
hook pack
(package directory).
Each hook is a directory containing:
Copy
my-hook/
├── HOOK.md # Metadata + documentation
└── handler.ts # Handler implementation
Hook Packs (npm/archives)
Hook packs are standard npm packages that export one or more hooks via
openclaw.hooks
package.json
. Install them with:
Copy
openclaw
hooks
install
&lt;
path-or-spe
&gt;
Npm specs are registry-only (package name + optional version/tag). Git/URL/file specs are rejected.
Example
package.json
Copy
&quot;name&quot;
&quot;@acme/my-hooks&quot;
&quot;version&quot;
&quot;0.1.0&quot;
&quot;openclaw&quot;
&quot;hooks&quot;
&quot;./hooks/my-hook&quot;
&quot;./hooks/other-hook&quot;
Each entry points to a hook directory containing
HOOK.md
and
handler.ts
(or
index.ts
Hook packs can ship dependencies; they will be installed under
~/.openclaw/hooks/&lt;id&gt;
Security note:
openclaw hooks install
installs dependencies with
npm install --ignore-scripts
(no lifecycle scripts). Keep hook pack dependency trees “pure JS/TS” and avoid packages that rely
postinstall
builds.
Hook Structure
HOOK.md Format
The
HOOK.md
file contains metadata in YAML frontmatter plus Markdown documentation:
Copy
---
name
my-hook
description
&quot;Short description of what this hook does&quot;
homepage
https://docs.openclaw.ai/automation/hooks#my-hook
metadata
&quot;openclaw&quot;
&quot;emoji&quot;
&quot;🔗&quot;
&quot;events&quot;
&quot;command:new&quot;
&quot;requires&quot;
&quot;bins&quot;
&quot;node&quot;
] } } }
---
# My Hook
Detailed documentation goes here...
## What It Does
- Listens for
`/new`
commands
- Performs some action
- Logs the result
## Requirements
- Node.js must be installed
## Configuration
No configuration needed.
Metadata Fields
The
metadata.openclaw
object supports:
emoji
: Display emoji for CLI (e.g.,
&quot;💾&quot;
events
: Array of events to listen for (e.g.,
[&quot;command:new&quot;, &quot;command:reset&quot;]
export
: Named export to use (defaults to
&quot;default&quot;
homepage
: Documentation URL
requires
: Optional requirements
bins
: Required binaries on PATH (e.g.,
[&quot;git&quot;, &quot;node&quot;]
anyBins
: At least one of these binaries must be present
env
: Required environment variables
config
: Required config paths (e.g.,
[&quot;workspace.dir&quot;]
: Required platforms (e.g.,
[&quot;darwin&quot;, &quot;linux&quot;]
always
: Bypass eligibility checks (boolean)
install
: Installation methods (for bundled hooks:
[{&quot;id&quot;:&quot;bundled&quot;,&quot;kind&quot;:&quot;bundled&quot;}]
Handler Implementation
The
handler.ts
file exports a
HookHandler
function:
Copy
import
type
{ HookHandler }
from
&quot;../../src/hooks/hooks.js&quot;
const
myHandler
HookHandler
async
(event)
=&gt;
// Only trigger on &#x27;new&#x27; command
event
.type
!==
&quot;command&quot;
event
.action
!==
&quot;new&quot;
) {
return
console
.log
`[my-hook] New command triggered`
console
.log
` Session:
event
.sessionKey
console
.log
` Timestamp:
event
timestamp
.toISOString
// Your custom logic here
// Optionally send message to user
event
messages
.push
&quot;✨ My hook executed!&quot;
export
default
myHandler;
Event Context
Each event includes:
Copy
type
&#x27;command&#x27;
&#x27;session&#x27;
&#x27;agent&#x27;
&#x27;gateway&#x27;
action
string
// e.g., &#x27;new&#x27;, &#x27;reset&#x27;, &#x27;stop&#x27;
sessionKey
string
// Session identifier
timestamp
Date
// When the event occurred
messages
string[]
// Push messages here to send to user
context
sessionEntry
SessionEntry
sessionId
string
sessionFile
string
commandSource
string
// e.g., &#x27;whatsapp&#x27;, &#x27;telegram&#x27;
senderId
string
workspaceDir
string
bootstrapFiles
WorkspaceBootstrapFile[]
cfg
OpenClawConfig
Event Types
Command Events
Triggered when agent commands are issued:
command
: All command events (general listener)
command:new
: When
/new
command is issued
command:reset
: When
/reset
command is issued
command:stop
: When
/stop
command is issued
Agent Events
agent:bootstrap
: Before workspace bootstrap files are injected (hooks may mutate
context.bootstrapFiles
Gateway Events
Triggered when the gateway starts:
gateway:startup
: After channels start and hooks are loaded
Tool Result Hooks (Plugin API)
These hooks are not event-stream listeners; they let plugins synchronously adjust tool results before OpenClaw persists them.
tool_result_persist
: transform tool results before they are written to the session transcript. Must be synchronous; return the updated tool result payload or
undefined
to keep it as-is. See
Agent Loop
Future Events
Planned event types:
session:start
: When a new session begins
session:end
: When a session ends
agent:error
: When an agent encounters an error
message:sent
: When a message is sent
message:received
: When a message is received
Creating Custom Hooks
1. Choose Location
Workspace hooks
&lt;workspace&gt;/hooks/
): Per-agent, highest precedence
Managed hooks
~/.openclaw/hooks/
): Shared across workspaces
2. Create Directory Structure
Copy
mkdir
~/.openclaw/hooks/my-hook
~/.openclaw/hooks/my-hook
3. Create HOOK.md
Copy
---
name
my-hook
description
&quot;Does something useful&quot;
metadata
&quot;openclaw&quot;
&quot;emoji&quot;
&quot;🎯&quot;
&quot;events&quot;
&quot;command:new&quot;
] } }
---
# My Custom Hook
This hook does something useful when you issue
`/new`
4. Create handler.ts
Copy
import
type
{ HookHandler }
from
&quot;../../src/hooks/hooks.js&quot;
const
handler
HookHandler
async
(event)
=&gt;
event
.type
!==
&quot;command&quot;
event
.action
!==
&quot;new&quot;
) {
return
console
.log
&quot;[my-hook] Running!&quot;
// Your logic here
export
default
handler;
5. Enable and Test
Copy
# Verify hook is discovered
openclaw
hooks
list
# Enable it
openclaw
hooks
enable
my-hook
# Restart your gateway process (menu bar app restart on macOS, or restart your dev process)
# Trigger the event
# Send /new via your messaging channel
Configuration
New Config Format (Recommended)
Copy
&quot;hooks&quot;
&quot;internal&quot;
&quot;enabled&quot;
true
&quot;entries&quot;
&quot;session-memory&quot;
&quot;enabled&quot;
true
&quot;command-logger&quot;
&quot;enabled&quot;
false
Per-Hook Configuration
Hooks can have custom configuration:
Copy
&quot;hooks&quot;
&quot;internal&quot;
&quot;enabled&quot;
true
&quot;entries&quot;
&quot;my-hook&quot;
&quot;enabled&quot;
true
&quot;env&quot;
&quot;MY_CUSTOM_VAR&quot;
&quot;value&quot;
Extra Directories
Load hooks from additional directories:
Copy
&quot;hooks&quot;
&quot;internal&quot;
&quot;enabled&quot;
true
&quot;load&quot;
&quot;extraDirs&quot;
&quot;/path/to/more/hooks&quot;
Legacy Config Format (Still Supported)
The old config format still works for backwards compatibility:
Copy
&quot;hooks&quot;
&quot;internal&quot;
&quot;enabled&quot;
true
&quot;handlers&quot;
&quot;event&quot;
&quot;command:new&quot;
&quot;module&quot;
&quot;./hooks/handlers/my-handler.ts&quot;
&quot;export&quot;
&quot;default&quot;
Note:
module
must be a workspace-relative path. Absolute paths and traversal outside the workspace are rejected.
Migration
: Use the new discovery-based system for new hooks. Legacy handlers are loaded after directory-based hooks.
CLI Commands
List Hooks
Copy
# List all hooks
openclaw
hooks
list
# Show only eligible hooks
openclaw
hooks
list
--eligible
# Verbose output (show missing requirements)
openclaw
hooks
list
--verbose
# JSON output
openclaw
hooks
list
--json
Hook Information
Copy
# Show detailed info about a hook
openclaw
hooks
info
session-memory
# JSON output
openclaw
hooks
info
session-memory
--json
Check Eligibility
Copy
# Show eligibility summary
openclaw
hooks
check
# JSON output
openclaw
hooks
check
--json
Enable/Disable
Copy
# Enable a hook
openclaw
hooks
enable
session-memory
# Disable a hook
openclaw
hooks
disable
command-logger
Bundled hook reference
session-memory
Saves session context to memory when you issue
/new
Events
command:new
Requirements
workspace.dir
must be configured
Output
&lt;workspace&gt;/memory/YYYY-MM-DD-slug.md
(defaults to
~/.openclaw/workspace
What it does
Uses the pre-reset session entry to locate the correct transcript
Extracts the last 15 lines of conversation
Uses LLM to generate a descriptive filename slug
Saves session metadata to a dated memory file
Example output
Copy
# Session: 2026-01-16 14:30:00 UTC
**Session Key**
: agent:main:main
**Session ID**
: abc123def456
**Source**
: telegram
Filename examples
2026-01-16-vendor-pitch.md
2026-01-16-api-design.md
2026-01-16-1430.md
(fallback timestamp if slug generation fails)
Enable
Copy
openclaw
hooks
enable
session-memory
bootstrap-extra-files
Injects additional bootstrap files (for example monorepo-local
AGENTS.md
TOOLS.md
) during
agent:bootstrap
Events
agent:bootstrap
Requirements
workspace.dir
must be configured
Output
: No files written; bootstrap context is modified in-memory only.
Config
Copy
&quot;hooks&quot;
&quot;internal&quot;
&quot;enabled&quot;
true
&quot;entries&quot;
&quot;bootstrap-extra-files&quot;
&quot;enabled&quot;
true
&quot;paths&quot;
&quot;packages/*/AGENTS.md&quot;
&quot;packages/*/TOOLS.md&quot;
Notes
Paths are resolved relative to workspace.
Files must stay inside workspace (realpath-checked).
Only recognized bootstrap basenames are loaded.
Subagent allowlist is preserved (
AGENTS.md
and
TOOLS.md
only).
Enable
Copy
openclaw
hooks
enable
bootstrap-extra-files
command-logger
Logs all command events to a centralized audit file.
Events
command
Requirements
: None
Output
~/.openclaw/logs/commands.log
What it does
Captures event details (command action, timestamp, session key, sender ID, source)
Appends to log file in JSONL format
Runs silently in the background
Example log entries
Copy
&quot;timestamp&quot;
&quot;2026-01-16T14:30:00.000Z&quot;
&quot;action&quot;
&quot;new&quot;
&quot;sessionKey&quot;
&quot;agent:main:main&quot;
&quot;senderId&quot;
&quot;+1234567890&quot;
&quot;source&quot;
&quot;telegram&quot;
&quot;timestamp&quot;
&quot;2026-01-16T15:45:22.000Z&quot;
&quot;action&quot;
&quot;stop&quot;
&quot;sessionKey&quot;
&quot;agent:main:main&quot;
&quot;senderId&quot;
&quot;
[email&#160;protected]
&quot;
&quot;source&quot;
&quot;whatsapp&quot;
View logs
Copy
# View recent commands
tail
~/.openclaw/logs/commands.log
# Pretty-print with jq
cat
~/.openclaw/logs/commands.log
# Filter by action
grep
&#x27;&quot;action&quot;:&quot;new&quot;&#x27;
~/.openclaw/logs/commands.log
Enable
Copy
openclaw
hooks
enable
command-logger
boot-md
Runs
BOOT.md
when the gateway starts (after channels start).
Internal hooks must be enabled for this to run.
Events
gateway:startup
Requirements
workspace.dir
must be configured
What it does
Reads
BOOT.md
from your workspace
Runs the instructions via the agent runner
Sends any requested outbound messages via the message tool
Enable
Copy
openclaw
hooks
enable
boot-md
Best Practices
Keep Handlers Fast
Hooks run during command processing. Keep them lightweight:
Copy
// ✓ Good - async work, returns immediately
const
handler
HookHandler
async
(event)
=&gt;
void
processInBackground
(event);
// Fire and forget
// ✗ Bad - blocks command processing
const
handler
HookHandler
async
(event)
=&gt;
await
slowDatabaseQuery
(event);
await
evenSlowerAPICall
(event);
Handle Errors Gracefully
Always wrap risky operations:
Copy
const
handler
HookHandler
async
(event)
=&gt;
try
await
riskyOperation
(event);
catch
(err) {
console
.error
&quot;[my-handler] Failed:&quot;
err
instanceof
Error
err
.message
String
(err));
// Don&#x27;t throw - let other handlers run
Filter Events Early
Return early if the event isn’t relevant:
Copy
const
handler
HookHandler
async
(event)
=&gt;
// Only handle &#x27;new&#x27; commands
event
.type
!==
&quot;command&quot;
event
.action
!==
&quot;new&quot;
) {
return
// Your logic here
Use Specific Event Keys
Specify exact events in metadata when possible:
Copy
metadata
&quot;openclaw&quot;
&quot;events&quot;
&quot;command:new&quot;
] } }
# Specific
Rather than:
Copy
metadata
&quot;openclaw&quot;
&quot;events&quot;
&quot;command&quot;
] } }
# General - more overhead
Debugging
Enable Hook Logging
The gateway logs hook loading at startup:
Copy
Registered hook: session-memory -&gt; command:new
Registered hook: bootstrap-extra-files -&gt; agent:bootstrap
Registered hook: command-logger -&gt; command
Registered hook: boot-md -&gt; gateway:startup
Check Discovery
List all discovered hooks:
Copy
openclaw
hooks
list
--verbose
Check Registration
In your handler, log when it’s called:
Copy
const
handler
HookHandler
async
(event)
=&gt;
console
.log
&quot;[my-handler] Triggered:&quot;
event
.type
event
.action);
// Your logic
Verify Eligibility
Check why a hook isn’t eligible:
Copy
openclaw
hooks
info
my-hook
Look for missing requirements in the output.
Testing
Gateway Logs
Monitor gateway logs to see hook execution:
Copy
# macOS
./scripts/clawlog.sh
# Other platforms
tail
~/.openclaw/gateway.log
Test Hooks Directly
Test your handlers in isolation:
Copy
import
{ test }
from
&quot;vitest&quot;
import
{ createHookEvent }
from
&quot;./src/hooks/hooks.js&quot;
import
myHandler
from
&quot;./hooks/my-hook/handler.js&quot;
test
&quot;my handler works&quot;
async
=&gt;
const
event
createHookEvent
&quot;command&quot;
&quot;new&quot;
&quot;test-session&quot;
foo
&quot;bar&quot;
});
await
myHandler
(event);
// Assert side effects
});
Architecture
Core Components
src/hooks/types.ts
: Type definitions
src/hooks/workspace.ts
: Directory scanning and loading
src/hooks/frontmatter.ts
: HOOK.md metadata parsing
src/hooks/config.ts
: Eligibility checking
src/hooks/hooks-status.ts
: Status reporting
src/hooks/loader.ts
: Dynamic module loader
src/cli/hooks-cli.ts
: CLI commands
src/gateway/server-startup.ts
: Loads hooks at gateway start
src/auto-reply/reply/commands-core.ts
: Triggers command events
Discovery Flow
Copy
Gateway startup
Scan directories (workspace → managed → bundled)
Parse HOOK.md files
Check eligibility (bins, env, config, os)
Load handlers from eligible hooks
Register handlers for events
Event Flow
Copy
User sends /new
Command validation
Create hook event
Trigger hook (all registered handlers)
Command processing continues
Session reset
Troubleshooting
Hook Not Discovered
Check directory structure:
Copy
-la
~/.openclaw/hooks/my-hook/
# Should show: HOOK.md, handler.ts
Verify HOOK.md format:
Copy
cat
~/.openclaw/hooks/my-hook/HOOK.md
# Should have YAML frontmatter with name and metadata
List all discovered hooks:
Copy
openclaw
hooks
list
Hook Not Eligible
Check requirements:
Copy
openclaw
hooks
info
my-hook
Look for missing:
Binaries (check PATH)
Environment variables
Config values
OS compatibility
Hook Not Executing
Verify hook is enabled:
Copy
openclaw
hooks
list
# Should show ✓ next to enabled hooks
Restart your gateway process so hooks reload.
Check gateway logs for errors:
Copy
./scripts/clawlog.sh
grep
hook
Handler Errors
Check for TypeScript/import errors:
Copy
# Test import directly
node
&quot;import(&#x27;./path/to/handler.ts&#x27;).then(console.log)&quot;
Migration Guide
From Legacy Config to Discovery
Before
Copy
&quot;hooks&quot;
&quot;internal&quot;
&quot;enabled&quot;
true
&quot;handlers&quot;
&quot;event&quot;
&quot;command:new&quot;
&quot;module&quot;
&quot;./hooks/handlers/my-handler.ts&quot;
After
Create hook directory:
Copy
mkdir
~/.openclaw/hooks/my-hook
./hooks/handlers/my-handler.ts
~/.openclaw/hooks/my-hook/handler.ts
Create HOOK.md:
Copy
---
name
my-hook
description
&quot;My custom hook&quot;
metadata
&quot;openclaw&quot;
&quot;emoji&quot;
&quot;🎯&quot;
&quot;events&quot;
&quot;command:new&quot;
] } }
---
# My Hook
Does something useful.
Update config:
Copy
&quot;hooks&quot;
&quot;internal&quot;
&quot;enabled&quot;
true
&quot;entries&quot;
&quot;my-hook&quot;
&quot;enabled&quot;
true
Verify and restart your gateway process:
Copy
openclaw
hooks
list
# Should show: 🎯 my-hook ✓
Benefits of migration
Automatic discovery
CLI management
Eligibility checking
Better documentation
Consistent structure
See Also
CLI Reference: hooks
Bundled Hooks README
Webhook Hooks
Configuration
Zalo Personal Plugin
Cron Jobs

---
## Automation > Poll

[Source: https://docs.openclaw.ai/automation/poll]

Polls - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Automation
Polls
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
Overview
Tools
Built-in tools
Lobster
LLM Task
Exec Tool
Web Tools
apply_patch Tool
Elevated Mode
Thinking Levels
Reactions
Browser
Browser (OpenClaw-managed)
Browser Login
Chrome Extension
Browser Troubleshooting
Agent coordination
Agent Send
Sub-Agents
Multi-Agent Sandbox &amp; Tools
Skills
Slash Commands
Skills
Skills Config
ClawHub
Plugins
Extensions
Voice Call Plugin
Zalo Personal Plugin
Automation
Hooks
Cron Jobs
Cron vs Heartbeat
Automation Troubleshooting
Webhooks
Gmail PubSub
Polls
Auth Monitoring
Media and devices
Nodes
Node Troubleshooting
Image and Media Support
Audio and Voice Notes
Camera Capture
Talk Mode
Voice Wake
Location Command
Polls
Supported channels
CLI
Gateway RPC
Channel differences
Agent tool (Message)
Automation
Polls
Polls
Supported channels
WhatsApp (web channel)
Discord
MS Teams (Adaptive Cards)
CLI
Copy
# WhatsApp
openclaw
message
poll
--target
+15555550123
--poll-question
&quot;Lunch today?&quot;
--poll-option
&quot;Yes&quot;
--poll-option
&quot;No&quot;
--poll-option
&quot;Maybe&quot;
openclaw
message
poll
--target
[email&#160;protected]
--poll-question
&quot;Meeting time?&quot;
--poll-option
&quot;10am&quot;
--poll-option
&quot;2pm&quot;
--poll-option
&quot;4pm&quot;
--poll-multi
# Discord
openclaw
message
poll
--channel
discord
--target
channel:123456789
--poll-question
&quot;Snack?&quot;
--poll-option
&quot;Pizza&quot;
--poll-option
&quot;Sushi&quot;
openclaw
message
poll
--channel
discord
--target
channel:123456789
--poll-question
&quot;Plan?&quot;
--poll-option
&quot;A&quot;
--poll-option
&quot;B&quot;
--poll-duration-hours
# MS Teams
openclaw
message
poll
--channel
msteams
--target
conversation:19:
[email&#160;protected]
--poll-question
&quot;Lunch?&quot;
--poll-option
&quot;Pizza&quot;
--poll-option
&quot;Sushi&quot;
Options:
--channel
whatsapp
(default),
discord
, or
msteams
--poll-multi
: allow selecting multiple options
--poll-duration-hours
: Discord-only (defaults to 24 when omitted)
Gateway RPC
Method:
poll
Params:
(string, required)
question
(string, required)
options
(string[], required)
maxSelections
(number, optional)
durationHours
(number, optional)
channel
(string, optional, default:
whatsapp
idempotencyKey
(string, required)
Channel differences
WhatsApp: 2-12 options,
maxSelections
must be within option count, ignores
durationHours
Discord: 2-10 options,
durationHours
clamped to 1-768 hours (default 24).
maxSelections &gt; 1
enables multi-select; Discord does not support a strict selection count.
MS Teams: Adaptive Card polls (OpenClaw-managed). No native poll API;
durationHours
is ignored.
Agent tool (Message)
Use the
message
tool with
poll
action (
pollQuestion
pollOption
, optional
pollMulti
pollDurationHours
channel
Note: Discord has no “pick exactly N” mode;
pollMulti
maps to multi-select.
Teams polls are rendered as Adaptive Cards and require the gateway to stay online
to record votes in
~/.openclaw/msteams-polls.json
Gmail PubSub
Auth Monitoring

---
## Automation > Troubleshooting

[Source: https://docs.openclaw.ai/automation/troubleshooting]

Automation Troubleshooting - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Automation
Automation Troubleshooting
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
Overview
Tools
Built-in tools
Lobster
LLM Task
Exec Tool
Web Tools
apply_patch Tool
Elevated Mode
Thinking Levels
Reactions
Browser
Browser (OpenClaw-managed)
Browser Login
Chrome Extension
Browser Troubleshooting
Agent coordination
Agent Send
Sub-Agents
Multi-Agent Sandbox &amp; Tools
Skills
Slash Commands
Skills
Skills Config
ClawHub
Plugins
Extensions
Voice Call Plugin
Zalo Personal Plugin
Automation
Hooks
Cron Jobs
Cron vs Heartbeat
Automation Troubleshooting
Webhooks
Gmail PubSub
Polls
Auth Monitoring
Media and devices
Nodes
Node Troubleshooting
Image and Media Support
Audio and Voice Notes
Camera Capture
Talk Mode
Voice Wake
Location Command
Automation troubleshooting
Command ladder
Cron not firing
Cron fired but no delivery
Heartbeat suppressed or skipped
Timezone and activeHours gotchas
Automation
Automation Troubleshooting
Automation troubleshooting
Use this page for scheduler and delivery issues (
cron
heartbeat
Command ladder
Copy
openclaw
status
openclaw
gateway
status
openclaw
logs
--follow
openclaw
doctor
openclaw
channels
status
--probe
Then run automation checks:
Copy
openclaw
cron
status
openclaw
cron
list
openclaw
system
heartbeat
last
Cron not firing
Copy
openclaw
cron
status
openclaw
cron
list
openclaw
cron
runs
--id
&lt;
jobI
&gt;
--limit
openclaw
logs
--follow
Good output looks like:
cron status
reports enabled and a future
nextWakeAtMs
Job is enabled and has a valid schedule/timezone.
cron runs
shows
or explicit skip reason.
Common signatures:
cron: scheduler disabled; jobs will not run automatically
→ cron disabled in config/env.
cron: timer tick failed
→ scheduler tick crashed; inspect surrounding stack/log context.
reason: not-due
in run output → manual run called without
--force
and job not due yet.
Cron fired but no delivery
Copy
openclaw
cron
runs
--id
&lt;
jobI
&gt;
--limit
openclaw
cron
list
openclaw
channels
status
--probe
openclaw
logs
--follow
Good output looks like:
Run status is
Delivery mode/target are set for isolated jobs.
Channel probe reports target channel connected.
Common signatures:
Run succeeded but delivery mode is
none
→ no external message is expected.
Delivery target missing/invalid (
channel
) → run may succeed internally but skip outbound.
Channel auth errors (
unauthorized
missing_scope
Forbidden
) → delivery blocked by channel credentials/permissions.
Heartbeat suppressed or skipped
Copy
openclaw
system
heartbeat
last
openclaw
logs
--follow
openclaw
config
get
agents.defaults.heartbeat
openclaw
channels
status
--probe
Good output looks like:
Heartbeat enabled with non-zero interval.
Last heartbeat result is
ran
(or skip reason is understood).
Common signatures:
heartbeat skipped
with
reason=quiet-hours
→ outside
activeHours
requests-in-flight
→ main lane busy; heartbeat deferred.
empty-heartbeat-file
HEARTBEAT.md
exists but has no actionable content.
alerts-disabled
→ visibility settings suppress outbound heartbeat messages.
Timezone and activeHours gotchas
Copy
openclaw
config
get
agents.defaults.heartbeat.activeHours
openclaw
config
get
agents.defaults.heartbeat.activeHours.timezone
openclaw
config
get
agents.defaults.userTimezone
echo
&quot;agents.defaults.userTimezone not set&quot;
openclaw
cron
list
openclaw
logs
--follow
Quick rules:
Config path not found: agents.defaults.userTimezone
means the key is unset; heartbeat falls back to host timezone (or
activeHours.timezone
if set).
Cron without
--tz
uses gateway host timezone.
Heartbeat
activeHours
uses configured timezone resolution (
user
local
, or explicit IANA tz).
ISO timestamps without timezone are treated as UTC for cron
schedules.
Common signatures:
Jobs run at the wrong wall-clock time after host timezone changes.
Heartbeat always skipped during your daytime because
activeHours.timezone
is wrong.
Related:
/automation/cron-jobs
/gateway/heartbeat
/automation/cron-vs-heartbeat
/concepts/timezone
Cron vs Heartbeat
Webhooks

---
## Automation > Webhook

[Source: https://docs.openclaw.ai/automation/webhook]

Webhooks - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Automation
Webhooks
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
Overview
Tools
Built-in tools
Lobster
LLM Task
Exec Tool
Web Tools
apply_patch Tool
Elevated Mode
Thinking Levels
Reactions
Browser
Browser (OpenClaw-managed)
Browser Login
Chrome Extension
Browser Troubleshooting
Agent coordination
Agent Send
Sub-Agents
Multi-Agent Sandbox &amp; Tools
Skills
Slash Commands
Skills
Skills Config
ClawHub
Plugins
Extensions
Voice Call Plugin
Zalo Personal Plugin
Automation
Hooks
Cron Jobs
Cron vs Heartbeat
Automation Troubleshooting
Webhooks
Gmail PubSub
Polls
Auth Monitoring
Media and devices
Nodes
Node Troubleshooting
Image and Media Support
Audio and Voice Notes
Camera Capture
Talk Mode
Voice Wake
Location Command
Webhooks
Enable
Auth
Endpoints
POST /hooks/wake
POST /hooks/agent
Session key policy (breaking change)
POST /hooks/&lt;name&gt; (mapped)
Responses
Examples
Use a different model
Security
Automation
Webhooks
Webhooks
Gateway can expose a small HTTP webhook endpoint for external triggers.
Enable
Copy
hooks
enabled
true
token
&quot;shared-secret&quot;
path
&quot;/hooks&quot;
// Optional: restrict explicit `agentId` routing to this allowlist.
// Omit or include &quot;*&quot; to allow any agent.
// Set [] to deny all explicit `agentId` routing.
allowedAgentIds
&quot;hooks&quot;
&quot;main&quot;
Notes:
hooks.token
is required when
hooks.enabled=true
hooks.path
defaults to
/hooks
Auth
Every request must include the hook token. Prefer headers:
Authorization: Bearer &lt;token&gt;
(recommended)
x-openclaw-token: &lt;token&gt;
Query-string tokens are rejected (
?token=...
returns
400
Endpoints
POST /hooks/wake
Payload:
Copy
&quot;text&quot;
&quot;System line&quot;
&quot;mode&quot;
&quot;now&quot;
text
required
(string): The description of the event (e.g., “New email received”).
mode
optional (
now
next-heartbeat
): Whether to trigger an immediate heartbeat (default
now
) or wait for the next periodic check.
Effect:
Enqueues a system event for the
main
session
mode=now
, triggers an immediate heartbeat
POST /hooks/agent
Payload:
Copy
&quot;message&quot;
&quot;Run this&quot;
&quot;name&quot;
&quot;Email&quot;
&quot;agentId&quot;
&quot;hooks&quot;
&quot;sessionKey&quot;
&quot;hook:email:msg-123&quot;
&quot;wakeMode&quot;
&quot;now&quot;
&quot;deliver&quot;
true
&quot;channel&quot;
&quot;last&quot;
&quot;to&quot;
&quot;+15551234567&quot;
&quot;model&quot;
&quot;openai/gpt-5.2-mini&quot;
&quot;thinking&quot;
&quot;low&quot;
&quot;timeoutSeconds&quot;
120
message
required
(string): The prompt or message for the agent to process.
name
optional (string): Human-readable name for the hook (e.g., “GitHub”), used as a prefix in session summaries.
agentId
optional (string): Route this hook to a specific agent. Unknown IDs fall back to the default agent. When set, the hook runs using the resolved agent’s workspace and configuration.
sessionKey
optional (string): The key used to identify the agent’s session. By default this field is rejected unless
hooks.allowRequestSessionKey=true
wakeMode
optional (
now
next-heartbeat
): Whether to trigger an immediate heartbeat (default
now
) or wait for the next periodic check.
deliver
optional (boolean): If
true
, the agent’s response will be sent to the messaging channel. Defaults to
true
. Responses that are only heartbeat acknowledgments are automatically skipped.
channel
optional (string): The messaging channel for delivery. One of:
last
whatsapp
telegram
discord
slack
mattermost
(plugin),
signal
imessage
msteams
. Defaults to
last
optional (string): The recipient identifier for the channel (e.g., phone number for WhatsApp/Signal, chat ID for Telegram, channel ID for Discord/Slack/Mattermost (plugin), conversation ID for MS Teams). Defaults to the last recipient in the main session.
model
optional (string): Model override (e.g.,
anthropic/claude-3-5-sonnet
or an alias). Must be in the allowed model list if restricted.
thinking
optional (string): Thinking level override (e.g.,
low
medium
high
timeoutSeconds
optional (number): Maximum duration for the agent run in seconds.
Effect:
Runs an
isolated
agent turn (own session key)
Always posts a summary into the
main
session
wakeMode=now
, triggers an immediate heartbeat
Session key policy (breaking change)
/hooks/agent
payload
sessionKey
overrides are disabled by default.
Recommended: set a fixed
hooks.defaultSessionKey
and keep request overrides off.
Optional: allow request overrides only when needed, and restrict prefixes.
Recommended config:
Copy
hooks
enabled
true
token
&quot;${OPENCLAW_HOOKS_TOKEN}&quot;
defaultSessionKey
&quot;hook:ingress&quot;
allowRequestSessionKey
false
allowedSessionKeyPrefixes
&quot;hook:&quot;
Compatibility config (legacy behavior):
Copy
hooks
enabled
true
token
&quot;${OPENCLAW_HOOKS_TOKEN}&quot;
allowRequestSessionKey
true
allowedSessionKeyPrefixes
&quot;hook:&quot;
// strongly recommended
POST /hooks/&lt;name&gt;
(mapped)
Custom hook names are resolved via
hooks.mappings
(see configuration). A mapping can
turn arbitrary payloads into
wake
agent
actions, with optional templates or
code transforms.
Mapping options (summary):
hooks.presets: [&quot;gmail&quot;]
enables the built-in Gmail mapping.
hooks.mappings
lets you define
match
action
, and templates in config.
hooks.transformsDir
transform.module
loads a JS/TS module for custom logic.
hooks.transformsDir
(if set) must stay within the transforms root under your OpenClaw config directory (typically
~/.openclaw/hooks/transforms
transform.module
must resolve within the effective transforms directory (traversal/escape paths are rejected).
Use
match.source
to keep a generic ingest endpoint (payload-driven routing).
TS transforms require a TS loader (e.g.
bun
tsx
) or precompiled
.js
at runtime.
Set
deliver: true
channel
on mappings to route replies to a chat surface
channel
defaults to
last
and falls back to WhatsApp).
agentId
routes the hook to a specific agent; unknown IDs fall back to the default agent.
hooks.allowedAgentIds
restricts explicit
agentId
routing. Omit it (or include
) to allow any agent. Set
to deny explicit
agentId
routing.
hooks.defaultSessionKey
sets the default session for hook agent runs when no explicit key is provided.
hooks.allowRequestSessionKey
controls whether
/hooks/agent
payloads may set
sessionKey
(default:
false
hooks.allowedSessionKeyPrefixes
optionally restricts explicit
sessionKey
values from request payloads and mappings.
allowUnsafeExternalContent: true
disables the external content safety wrapper for that hook
(dangerous; only for trusted internal sources).
openclaw webhooks gmail setup
writes
hooks.gmail
config for
openclaw webhooks gmail run
See
Gmail Pub/Sub
for the full Gmail watch flow.
Responses
200
for
/hooks/wake
202
for
/hooks/agent
(async run started)
401
on auth failure
429
after repeated auth failures from the same client (check
Retry-After
400
on invalid payload
413
on oversized payloads
Examples
Copy
curl
POST
http://127.0.0.1:18789/hooks/wake
&#x27;Authorization: Bearer SECRET&#x27;
&#x27;Content-Type: application/json&#x27;
&#x27;{&quot;text&quot;:&quot;New email received&quot;,&quot;mode&quot;:&quot;now&quot;}&#x27;
Copy
curl
POST
http://127.0.0.1:18789/hooks/agent
&#x27;x-openclaw-token: SECRET&#x27;
&#x27;Content-Type: application/json&#x27;
&#x27;{&quot;message&quot;:&quot;Summarize inbox&quot;,&quot;name&quot;:&quot;Email&quot;,&quot;wakeMode&quot;:&quot;next-heartbeat&quot;}&#x27;
Use a different model
Add
model
to the agent payload (or mapping) to override the model for that run:
Copy
curl
POST
http://127.0.0.1:18789/hooks/agent
&#x27;x-openclaw-token: SECRET&#x27;
&#x27;Content-Type: application/json&#x27;
&#x27;{&quot;message&quot;:&quot;Summarize inbox&quot;,&quot;name&quot;:&quot;Email&quot;,&quot;model&quot;:&quot;openai/gpt-5.2-mini&quot;}&#x27;
If you enforce
agents.defaults.models
, make sure the override model is included there.
Copy
curl
POST
http://127.0.0.1:18789/hooks/gmail
&#x27;Authorization: Bearer SECRET&#x27;
&#x27;Content-Type: application/json&#x27;
&#x27;{&quot;source&quot;:&quot;gmail&quot;,&quot;messages&quot;:[{&quot;from&quot;:&quot;Ada&quot;,&quot;subject&quot;:&quot;Hello&quot;,&quot;snippet&quot;:&quot;Hi&quot;}]}&#x27;
Security
Keep hook endpoints behind loopback, tailnet, or trusted reverse proxy.
Use a dedicated hook token; do not reuse gateway auth tokens.
Repeated auth failures are rate-limited per client address to slow brute-force attempts.
If you use multi-agent routing, set
hooks.allowedAgentIds
to limit explicit
agentId
selection.
Keep
hooks.allowRequestSessionKey=false
unless you require caller-selected sessions.
If you enable request
sessionKey
, restrict
hooks.allowedSessionKeyPrefixes
(for example,
[&quot;hook:&quot;]
Avoid including sensitive raw payloads in webhook logs.
Hook payloads are treated as untrusted and wrapped with safety boundaries by default.
If you must disable this for a specific hook, set
allowUnsafeExternalContent: true
in that hook’s mapping (dangerous).
Automation Troubleshooting
Gmail PubSub