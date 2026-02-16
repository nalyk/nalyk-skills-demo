# OpenClaw CLI Complete Reference

Every CLI command and subcommand with flags, examples, and usage.


---
## Cli > Agent

[Source: https://docs.openclaw.ai/cli/agent]

agent - OpenClaw
OpenClaw
home page
English
GitHub
Releases
CLI commands
agent
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
CLI commands
CLI Reference
agent
agents
approvals
browser
channels
configure
cron
dashboard
directory
dns
docs
doctor
gateway
health
hooks
logs
memory
message
models
nodes
onboard
pairing
plugins
reset
Sandbox CLI
security
sessions
setup
skills
status
system
tui
uninstall
update
voicecall
RPC and API
RPC Adapters
Device Model Database
Templates
Default AGENTS.md
AGENTS.md Template
BOOT.md Template
BOOTSTRAP.md Template
HEARTBEAT.md Template
IDENTITY
SOUL.md Template
TOOLS.md Template
USER
Technical reference
Wizard Reference
Token Use and Costs
grammY
Concept internals
TypeBox
Markdown Formatting
Typing Indicators
Usage Tracking
Timezones
Project
Credits
Release notes
Release Checklist
Tests
Experiments
Onboarding and Config Protocol
Cron Add Hardening
Telegram Allowlist Hardening
Workspace Memory Research
Model Config Exploration
openclaw agent
Examples
CLI commands
agent
openclaw agent
Run an agent turn via the Gateway (use
--local
for embedded).
Use
--agent &lt;id&gt;
to target a configured agent directly.
Related:
Agent send tool:
Agent send
Examples
Copy
openclaw
agent
--to
+15555550123
--message
&quot;status update&quot;
--deliver
openclaw
agent
--agent
ops
--message
&quot;Summarize logs&quot;
openclaw
agent
--session-id
1234
--message
&quot;Summarize inbox&quot;
--thinking
medium
openclaw
agent
--agent
ops
--message
&quot;Generate report&quot;
--deliver
--reply-channel
slack
--reply-to
&quot;#reports&quot;
CLI Reference
agents

---
## Cli > Agents

[Source: https://docs.openclaw.ai/cli/agents]

agents - OpenClaw
OpenClaw
home page
English
GitHub
Releases
CLI commands
agents
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
CLI commands
CLI Reference
agent
agents
approvals
browser
channels
configure
cron
dashboard
directory
dns
docs
doctor
gateway
health
hooks
logs
memory
message
models
nodes
onboard
pairing
plugins
reset
Sandbox CLI
security
sessions
setup
skills
status
system
tui
uninstall
update
voicecall
RPC and API
RPC Adapters
Device Model Database
Templates
Default AGENTS.md
AGENTS.md Template
BOOT.md Template
BOOTSTRAP.md Template
HEARTBEAT.md Template
IDENTITY
SOUL.md Template
TOOLS.md Template
USER
Technical reference
Wizard Reference
Token Use and Costs
grammY
Concept internals
TypeBox
Markdown Formatting
Typing Indicators
Usage Tracking
Timezones
Project
Credits
Release notes
Release Checklist
Tests
Experiments
Onboarding and Config Protocol
Cron Add Hardening
Telegram Allowlist Hardening
Workspace Memory Research
Model Config Exploration
openclaw agents
Examples
Identity files
Set identity
CLI commands
agents
openclaw agents
Manage isolated agents (workspaces + auth + routing).
Related:
Multi-agent routing:
Multi-Agent Routing
Agent workspace:
Agent workspace
Examples
Copy
openclaw
agents
list
openclaw
agents
add
work
--workspace
~/.openclaw/workspace-work
openclaw
agents
set-identity
--workspace
~/.openclaw/workspace
--from-identity
openclaw
agents
set-identity
--agent
main
--avatar
avatars/openclaw.png
openclaw
agents
delete
work
Identity files
Each agent workspace can include an
IDENTITY.md
at the workspace root:
Example path:
~/.openclaw/workspace/IDENTITY.md
set-identity --from-identity
reads from the workspace root (or an explicit
--identity-file
Avatar paths resolve relative to the workspace root.
Set identity
set-identity
writes fields into
agents.list[].identity
name
theme
emoji
avatar
(workspace-relative path, http(s) URL, or data URI)
Load from
IDENTITY.md
Copy
openclaw
agents
set-identity
--workspace
~/.openclaw/workspace
--from-identity
Override fields explicitly:
Copy
openclaw
agents
set-identity
--agent
main
--name
&quot;OpenClaw&quot;
--emoji
&quot;🦞&quot;
--avatar
avatars/openclaw.png
Config sample:
Copy
agents
list
&quot;main&quot;
identity
name
&quot;OpenClaw&quot;
theme
&quot;space lobster&quot;
emoji
&quot;🦞&quot;
avatar
&quot;avatars/openclaw.png&quot;
agent
approvals

---
## Cli > Approvals

[Source: https://docs.openclaw.ai/cli/approvals]

approvals - OpenClaw
OpenClaw
home page
English
GitHub
Releases
CLI commands
approvals
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
CLI commands
CLI Reference
agent
agents
approvals
browser
channels
configure
cron
dashboard
directory
dns
docs
doctor
gateway
health
hooks
logs
memory
message
models
nodes
onboard
pairing
plugins
reset
Sandbox CLI
security
sessions
setup
skills
status
system
tui
uninstall
update
voicecall
RPC and API
RPC Adapters
Device Model Database
Templates
Default AGENTS.md
AGENTS.md Template
BOOT.md Template
BOOTSTRAP.md Template
HEARTBEAT.md Template
IDENTITY
SOUL.md Template
TOOLS.md Template
USER
Technical reference
Wizard Reference
Token Use and Costs
grammY
Concept internals
TypeBox
Markdown Formatting
Typing Indicators
Usage Tracking
Timezones
Project
Credits
Release notes
Release Checklist
Tests
Experiments
Onboarding and Config Protocol
Cron Add Hardening
Telegram Allowlist Hardening
Workspace Memory Research
Model Config Exploration
openclaw approvals
Common commands
Replace approvals from a file
Allowlist helpers
Notes
CLI commands
approvals
openclaw approvals
Manage exec approvals for the
local host
gateway host
, or a
node host
By default, commands target the local approvals file on disk. Use
--gateway
to target the gateway, or
--node
to target a specific node.
Related:
Exec approvals:
Exec approvals
Nodes:
Nodes
Common commands
Copy
openclaw
approvals
get
openclaw
approvals
get
--node
&lt;
name
&gt;
openclaw
approvals
get
--gateway
Replace approvals from a file
Copy
openclaw
approvals
set
--file
./exec-approvals.json
openclaw
approvals
set
--node
&lt;
name
&gt;
--file
./exec-approvals.json
openclaw
approvals
set
--gateway
--file
./exec-approvals.json
Allowlist helpers
Copy
openclaw
approvals
allowlist
add
&quot;~/Projects/**/bin/rg&quot;
openclaw
approvals
allowlist
add
--agent
main
--node
&lt;
name
&gt;
&quot;/usr/bin/uptime&quot;
openclaw
approvals
allowlist
add
--agent
&quot;*&quot;
&quot;/usr/bin/uname&quot;
openclaw
approvals
allowlist
remove
&quot;~/Projects/**/bin/rg&quot;
Notes
--node
uses the same resolver as
openclaw nodes
(id, name, ip, or id prefix).
--agent
defaults to
&quot;*&quot;
, which applies to all agents.
The node host must advertise
system.execApprovals.get/set
(macOS app or headless node host).
Approvals files are stored per host at
~/.openclaw/exec-approvals.json
agents
browser

---
## Cli > Browser

[Source: https://docs.openclaw.ai/cli/browser]

browser - OpenClaw
OpenClaw
home page
English
GitHub
Releases
CLI commands
browser
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
CLI commands
CLI Reference
agent
agents
approvals
browser
channels
configure
cron
dashboard
directory
dns
docs
doctor
gateway
health
hooks
logs
memory
message
models
nodes
onboard
pairing
plugins
reset
Sandbox CLI
security
sessions
setup
skills
status
system
tui
uninstall
update
voicecall
RPC and API
RPC Adapters
Device Model Database
Templates
Default AGENTS.md
AGENTS.md Template
BOOT.md Template
BOOTSTRAP.md Template
HEARTBEAT.md Template
IDENTITY
SOUL.md Template
TOOLS.md Template
USER
Technical reference
Wizard Reference
Token Use and Costs
grammY
Concept internals
TypeBox
Markdown Formatting
Typing Indicators
Usage Tracking
Timezones
Project
Credits
Release notes
Release Checklist
Tests
Experiments
Onboarding and Config Protocol
Cron Add Hardening
Telegram Allowlist Hardening
Workspace Memory Research
Model Config Exploration
openclaw browser
Common flags
Quick start (local)
Profiles
Tabs
Snapshot / screenshot / actions
Chrome extension relay (attach via toolbar button)
Remote browser control (node host proxy)
CLI commands
browser
openclaw browser
Manage OpenClaw’s browser control server and run browser actions (tabs, snapshots, screenshots, navigation, clicks, typing).
Related:
Browser tool + API:
Browser tool
Chrome extension relay:
Chrome extension
Common flags
--url &lt;gatewayWsUrl&gt;
: Gateway WebSocket URL (defaults to config).
--token &lt;token&gt;
: Gateway token (if required).
--timeout &lt;ms&gt;
: request timeout (ms).
--browser-profile &lt;name&gt;
: choose a browser profile (default from config).
--json
: machine-readable output (where supported).
Quick start (local)
Copy
openclaw
browser
--browser-profile
chrome
tabs
openclaw
browser
--browser-profile
openclaw
start
openclaw
browser
--browser-profile
openclaw
open
https://example.com
openclaw
browser
--browser-profile
openclaw
snapshot
Profiles
Profiles are named browser routing configs. In practice:
openclaw
: launches/attaches to a dedicated OpenClaw-managed Chrome instance (isolated user data dir).
chrome
: controls your existing Chrome tab(s) via the Chrome extension relay.
Copy
openclaw
browser
profiles
openclaw
browser
create-profile
--name
work
--color
&quot;#FF5A36&quot;
openclaw
browser
delete-profile
--name
work
Use a specific profile:
Copy
openclaw
browser
--browser-profile
work
tabs
Tabs
Copy
openclaw
browser
tabs
openclaw
browser
open
https://docs.openclaw.ai
openclaw
browser
focus
&lt;
targetI
&gt;
openclaw
browser
close
&lt;
targetI
&gt;
Snapshot / screenshot / actions
Snapshot:
Copy
openclaw
browser
snapshot
Screenshot:
Copy
openclaw
browser
screenshot
Navigate/click/type (ref-based UI automation):
Copy
openclaw
browser
navigate
https://example.com
openclaw
browser
click
&lt;
&gt;
openclaw
browser
type
&lt;
&gt;
&quot;hello&quot;
Chrome extension relay (attach via toolbar button)
This mode lets the agent control an existing Chrome tab that you attach manually (it does not auto-attach).
Install the unpacked extension to a stable path:
Copy
openclaw
browser
extension
install
openclaw
browser
extension
path
Then Chrome →
chrome://extensions
→ enable “Developer mode” → “Load unpacked” → select the printed folder.
Full guide:
Chrome extension
Remote browser control (node host proxy)
If the Gateway runs on a different machine than the browser, run a
node host
on the machine that has Chrome/Brave/Edge/Chromium. The Gateway will proxy browser actions to that node (no separate browser control server required).
Use
gateway.nodes.browser.mode
to control auto-routing and
gateway.nodes.browser.node
to pin a specific node if multiple are connected.
Security + remote setup:
Browser tool
Remote access
Tailscale
Security
approvals
channels

---
## Cli > Channels

[Source: https://docs.openclaw.ai/cli/channels]

channels - OpenClaw
OpenClaw
home page
English
GitHub
Releases
CLI commands
channels
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
CLI commands
CLI Reference
agent
agents
approvals
browser
channels
configure
cron
dashboard
directory
dns
docs
doctor
gateway
health
hooks
logs
memory
message
models
nodes
onboard
pairing
plugins
reset
Sandbox CLI
security
sessions
setup
skills
status
system
tui
uninstall
update
voicecall
RPC and API
RPC Adapters
Device Model Database
Templates
Default AGENTS.md
AGENTS.md Template
BOOT.md Template
BOOTSTRAP.md Template
HEARTBEAT.md Template
IDENTITY
SOUL.md Template
TOOLS.md Template
USER
Technical reference
Wizard Reference
Token Use and Costs
grammY
Concept internals
TypeBox
Markdown Formatting
Typing Indicators
Usage Tracking
Timezones
Project
Credits
Release notes
Release Checklist
Tests
Experiments
Onboarding and Config Protocol
Cron Add Hardening
Telegram Allowlist Hardening
Workspace Memory Research
Model Config Exploration
openclaw channels
Common commands
Add / remove accounts
Login / logout (interactive)
Troubleshooting
Capabilities probe
Resolve names to IDs
CLI commands
channels
openclaw channels
Manage chat channel accounts and their runtime status on the Gateway.
Related docs:
Channel guides:
Channels
Gateway configuration:
Configuration
Common commands
Copy
openclaw
channels
list
openclaw
channels
status
openclaw
channels
capabilities
openclaw
channels
capabilities
--channel
discord
--target
channel:123
openclaw
channels
resolve
--channel
slack
&quot;#general&quot;
&quot;@jane&quot;
openclaw
channels
logs
--channel
all
Add / remove accounts
Copy
openclaw
channels
add
--channel
telegram
--token
&lt;
bot-toke
&gt;
openclaw
channels
remove
--channel
telegram
--delete
Tip:
openclaw channels add --help
shows per-channel flags (token, app token, signal-cli paths, etc).
Login / logout (interactive)
Copy
openclaw
channels
login
--channel
whatsapp
openclaw
channels
logout
--channel
whatsapp
Troubleshooting
Run
openclaw status --deep
for a broad probe.
Use
openclaw doctor
for guided fixes.
openclaw channels list
prints
Claude: HTTP 403 ... user:profile
→ usage snapshot needs the
user:profile
scope. Use
--no-usage
, or provide a claude.ai session key (
CLAUDE_WEB_SESSION_KEY
CLAUDE_WEB_COOKIE
), or re-auth via Claude Code CLI.
Capabilities probe
Fetch provider capability hints (intents/scopes where available) plus static feature support:
Copy
openclaw
channels
capabilities
openclaw
channels
capabilities
--channel
discord
--target
channel:123
Notes:
--channel
is optional; omit it to list every channel (including extensions).
--target
accepts
channel:&lt;id&gt;
or a raw numeric channel id and only applies to Discord.
Probes are provider-specific: Discord intents + optional channel permissions; Slack bot + user scopes; Telegram bot flags + webhook; Signal daemon version; MS Teams app token + Graph roles/scopes (annotated where known). Channels without probes report
Probe: unavailable
Resolve names to IDs
Resolve channel/user names to IDs using the provider directory:
Copy
openclaw
channels
resolve
--channel
slack
&quot;#general&quot;
&quot;@jane&quot;
openclaw
channels
resolve
--channel
discord
&quot;My Server/#support&quot;
&quot;@someone&quot;
openclaw
channels
resolve
--channel
matrix
&quot;Project Room&quot;
Notes:
Use
--kind user|group|auto
to force the target type.
Resolution prefers active matches when multiple entries share the same name.
browser
configure

---
## Cli > Configure

[Source: https://docs.openclaw.ai/cli/configure]

configure - OpenClaw
OpenClaw
home page
English
GitHub
Releases
CLI commands
configure
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
CLI commands
CLI Reference
agent
agents
approvals
browser
channels
configure
cron
dashboard
directory
dns
docs
doctor
gateway
health
hooks
logs
memory
message
models
nodes
onboard
pairing
plugins
reset
Sandbox CLI
security
sessions
setup
skills
status
system
tui
uninstall
update
voicecall
RPC and API
RPC Adapters
Device Model Database
Templates
Default AGENTS.md
AGENTS.md Template
BOOT.md Template
BOOTSTRAP.md Template
HEARTBEAT.md Template
IDENTITY
SOUL.md Template
TOOLS.md Template
USER
Technical reference
Wizard Reference
Token Use and Costs
grammY
Concept internals
TypeBox
Markdown Formatting
Typing Indicators
Usage Tracking
Timezones
Project
Credits
Release notes
Release Checklist
Tests
Experiments
Onboarding and Config Protocol
Cron Add Hardening
Telegram Allowlist Hardening
Workspace Memory Research
Model Config Exploration
openclaw configure
Examples
CLI commands
configure
openclaw configure
Interactive prompt to set up credentials, devices, and agent defaults.
Note: The
Model
section now includes a multi-select for the
agents.defaults.models
allowlist (what shows up in
/model
and the model picker).
Tip:
openclaw config
without a subcommand opens the same wizard. Use
openclaw config get|set|unset
for non-interactive edits.
Related:
Gateway configuration reference:
Configuration
Config CLI:
Config
Notes:
Choosing where the Gateway runs always updates
gateway.mode
. You can select “Continue” without other sections if that is all you need.
Channel-oriented services (Slack/Discord/Matrix/Microsoft Teams) prompt for channel/room allowlists during setup. You can enter names or IDs; the wizard resolves names to IDs when possible.
Examples
Copy
openclaw
configure
openclaw
configure
--section
models
--section
channels
channels
cron

---
## Cli > Cron

[Source: https://docs.openclaw.ai/cli/cron]

cron - OpenClaw
OpenClaw
home page
English
GitHub
Releases
CLI commands
cron
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
CLI commands
CLI Reference
agent
agents
approvals
browser
channels
configure
cron
dashboard
directory
dns
docs
doctor
gateway
health
hooks
logs
memory
message
models
nodes
onboard
pairing
plugins
reset
Sandbox CLI
security
sessions
setup
skills
status
system
tui
uninstall
update
voicecall
RPC and API
RPC Adapters
Device Model Database
Templates
Default AGENTS.md
AGENTS.md Template
BOOT.md Template
BOOTSTRAP.md Template
HEARTBEAT.md Template
IDENTITY
SOUL.md Template
TOOLS.md Template
USER
Technical reference
Wizard Reference
Token Use and Costs
grammY
Concept internals
TypeBox
Markdown Formatting
Typing Indicators
Usage Tracking
Timezones
Project
Credits
Release notes
Release Checklist
Tests
Experiments
Onboarding and Config Protocol
Cron Add Hardening
Telegram Allowlist Hardening
Workspace Memory Research
Model Config Exploration
openclaw cron
Common edits
CLI commands
cron
openclaw cron
Manage cron jobs for the Gateway scheduler.
Related:
Cron jobs:
Cron jobs
Tip: run
openclaw cron --help
for the full command surface.
Note: isolated
cron add
jobs default to
--announce
delivery. Use
--no-deliver
to keep
output internal.
--deliver
remains as a deprecated alias for
--announce
Note: one-shot (
--at
) jobs delete after success by default. Use
--keep-after-run
to keep them.
Note: recurring jobs now use exponential retry backoff after consecutive errors (30s → 1m → 5m → 15m → 60m), then return to normal schedule after the next successful run.
Common edits
Update delivery settings without changing the message:
Copy
openclaw
cron
edit
&lt;
job-i
&gt;
--announce
--channel
telegram
--to
&quot;123456789&quot;
Disable delivery for an isolated job:
Copy
openclaw
cron
edit
&lt;
job-i
&gt;
--no-deliver
Announce to a specific channel:
Copy
openclaw
cron
edit
&lt;
job-i
&gt;
--announce
--channel
slack
--to
&quot;channel:C1234567890&quot;
configure
dashboard

---
## Cli > Dashboard

[Source: https://docs.openclaw.ai/cli/dashboard]

dashboard - OpenClaw
OpenClaw
home page
English
GitHub
Releases
CLI commands
dashboard
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
CLI commands
CLI Reference
agent
agents
approvals
browser
channels
configure
cron
dashboard
directory
dns
docs
doctor
gateway
health
hooks
logs
memory
message
models
nodes
onboard
pairing
plugins
reset
Sandbox CLI
security
sessions
setup
skills
status
system
tui
uninstall
update
voicecall
RPC and API
RPC Adapters
Device Model Database
Templates
Default AGENTS.md
AGENTS.md Template
BOOT.md Template
BOOTSTRAP.md Template
HEARTBEAT.md Template
IDENTITY
SOUL.md Template
TOOLS.md Template
USER
Technical reference
Wizard Reference
Token Use and Costs
grammY
Concept internals
TypeBox
Markdown Formatting
Typing Indicators
Usage Tracking
Timezones
Project
Credits
Release notes
Release Checklist
Tests
Experiments
Onboarding and Config Protocol
Cron Add Hardening
Telegram Allowlist Hardening
Workspace Memory Research
Model Config Exploration
openclaw dashboard
CLI commands
dashboard
openclaw dashboard
Open the Control UI using your current auth.
Copy
openclaw
dashboard
openclaw
dashboard
--no-open
cron
directory

---
## Cli > Directory

[Source: https://docs.openclaw.ai/cli/directory]

directory - OpenClaw
OpenClaw
home page
English
GitHub
Releases
CLI commands
directory
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
CLI commands
CLI Reference
agent
agents
approvals
browser
channels
configure
cron
dashboard
directory
dns
docs
doctor
gateway
health
hooks
logs
memory
message
models
nodes
onboard
pairing
plugins
reset
Sandbox CLI
security
sessions
setup
skills
status
system
tui
uninstall
update
voicecall
RPC and API
RPC Adapters
Device Model Database
Templates
Default AGENTS.md
AGENTS.md Template
BOOT.md Template
BOOTSTRAP.md Template
HEARTBEAT.md Template
IDENTITY
SOUL.md Template
TOOLS.md Template
USER
Technical reference
Wizard Reference
Token Use and Costs
grammY
Concept internals
TypeBox
Markdown Formatting
Typing Indicators
Usage Tracking
Timezones
Project
Credits
Release notes
Release Checklist
Tests
Experiments
Onboarding and Config Protocol
Cron Add Hardening
Telegram Allowlist Hardening
Workspace Memory Research
Model Config Exploration
openclaw directory
Common flags
Notes
Using results with message send
ID formats (by channel)
Self (“me”)
Peers (contacts/users)
Groups
CLI commands
directory
openclaw directory
Directory lookups for channels that support it (contacts/peers, groups, and “me”).
Common flags
--channel &lt;name&gt;
: channel id/alias (required when multiple channels are configured; auto when only one is configured)
--account &lt;id&gt;
: account id (default: channel default)
--json
: output JSON
Notes
directory
is meant to help you find IDs you can paste into other commands (especially
openclaw message send --target ...
For many channels, results are config-backed (allowlists / configured groups) rather than a live provider directory.
Default output is
(and sometimes
name
) separated by a tab; use
--json
for scripting.
Using results with
message send
Copy
openclaw
directory
peers
list
--channel
slack
--query
&quot;U0&quot;
openclaw
message
send
--channel
slack
--target
user:U012ABCDEF
--message
&quot;hello&quot;
ID formats (by channel)
WhatsApp:
+15551234567
(DM),
[email&#160;protected]
(group)
Telegram:
@username
or numeric chat id; groups are numeric ids
Slack:
user:U…
and
channel:C…
Discord:
user:&lt;id&gt;
and
channel:&lt;id&gt;
Matrix (plugin):
user:@user:server
room:!roomId:server
, or
#alias:server
Microsoft Teams (plugin):
user:&lt;id&gt;
and
conversation:&lt;id&gt;
Zalo (plugin): user id (Bot API)
Zalo Personal /
zalouser
(plugin): thread id (DM/group) from
zca
friend list
group list
Self (“me”)
Copy
openclaw
directory
self
--channel
zalouser
Peers (contacts/users)
Copy
openclaw
directory
peers
list
--channel
zalouser
openclaw
directory
peers
list
--channel
zalouser
--query
&quot;name&quot;
openclaw
directory
peers
list
--channel
zalouser
--limit
Groups
Copy
openclaw
directory
groups
list
--channel
zalouser
openclaw
directory
groups
list
--channel
zalouser
--query
&quot;work&quot;
openclaw
directory
groups
members
--channel
zalouser
--group-id
&lt;
&gt;
dashboard
dns

---
## Cli > Dns

[Source: https://docs.openclaw.ai/cli/dns]

dns - OpenClaw
OpenClaw
home page
English
GitHub
Releases
CLI commands
dns
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
CLI commands
CLI Reference
agent
agents
approvals
browser
channels
configure
cron
dashboard
directory
dns
docs
doctor
gateway
health
hooks
logs
memory
message
models
nodes
onboard
pairing
plugins
reset
Sandbox CLI
security
sessions
setup
skills
status
system
tui
uninstall
update
voicecall
RPC and API
RPC Adapters
Device Model Database
Templates
Default AGENTS.md
AGENTS.md Template
BOOT.md Template
BOOTSTRAP.md Template
HEARTBEAT.md Template
IDENTITY
SOUL.md Template
TOOLS.md Template
USER
Technical reference
Wizard Reference
Token Use and Costs
grammY
Concept internals
TypeBox
Markdown Formatting
Typing Indicators
Usage Tracking
Timezones
Project
Credits
Release notes
Release Checklist
Tests
Experiments
Onboarding and Config Protocol
Cron Add Hardening
Telegram Allowlist Hardening
Workspace Memory Research
Model Config Exploration
openclaw dns
Setup
CLI commands
dns
openclaw dns
DNS helpers for wide-area discovery (Tailscale + CoreDNS). Currently focused on macOS + Homebrew CoreDNS.
Related:
Gateway discovery:
Discovery
Wide-area discovery config:
Configuration
Setup
Copy
openclaw
dns
setup
openclaw
dns
setup
--apply
directory
docs

---
## Cli > Docs

[Source: https://docs.openclaw.ai/cli/docs]

docs - OpenClaw
OpenClaw
home page
English
GitHub
Releases
CLI commands
docs
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
CLI commands
CLI Reference
agent
agents
approvals
browser
channels
configure
cron
dashboard
directory
dns
docs
doctor
gateway
health
hooks
logs
memory
message
models
nodes
onboard
pairing
plugins
reset
Sandbox CLI
security
sessions
setup
skills
status
system
tui
uninstall
update
voicecall
RPC and API
RPC Adapters
Device Model Database
Templates
Default AGENTS.md
AGENTS.md Template
BOOT.md Template
BOOTSTRAP.md Template
HEARTBEAT.md Template
IDENTITY
SOUL.md Template
TOOLS.md Template
USER
Technical reference
Wizard Reference
Token Use and Costs
grammY
Concept internals
TypeBox
Markdown Formatting
Typing Indicators
Usage Tracking
Timezones
Project
Credits
Release notes
Release Checklist
Tests
Experiments
Onboarding and Config Protocol
Cron Add Hardening
Telegram Allowlist Hardening
Workspace Memory Research
Model Config Exploration
openclaw docs
CLI commands
docs
openclaw docs
Search the live docs index.
Copy
openclaw
docs
browser
extension
openclaw
docs
sandbox
allowHostControl
dns
doctor

---
## Cli > Doctor

[Source: https://docs.openclaw.ai/cli/doctor]

doctor - OpenClaw
OpenClaw
home page
English
GitHub
Releases
CLI commands
doctor
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
CLI commands
CLI Reference
agent
agents
approvals
browser
channels
configure
cron
dashboard
directory
dns
docs
doctor
gateway
health
hooks
logs
memory
message
models
nodes
onboard
pairing
plugins
reset
Sandbox CLI
security
sessions
setup
skills
status
system
tui
uninstall
update
voicecall
RPC and API
RPC Adapters
Device Model Database
Templates
Default AGENTS.md
AGENTS.md Template
BOOT.md Template
BOOTSTRAP.md Template
HEARTBEAT.md Template
IDENTITY
SOUL.md Template
TOOLS.md Template
USER
Technical reference
Wizard Reference
Token Use and Costs
grammY
Concept internals
TypeBox
Markdown Formatting
Typing Indicators
Usage Tracking
Timezones
Project
Credits
Release notes
Release Checklist
Tests
Experiments
Onboarding and Config Protocol
Cron Add Hardening
Telegram Allowlist Hardening
Workspace Memory Research
Model Config Exploration
openclaw doctor
Examples
macOS: launchctl env overrides
CLI commands
doctor
openclaw doctor
Health checks + quick fixes for the gateway and channels.
Related:
Troubleshooting:
Troubleshooting
Security audit:
Security
Examples
Copy
openclaw
doctor
openclaw
doctor
--repair
openclaw
doctor
--deep
Notes:
Interactive prompts (like keychain/OAuth fixes) only run when stdin is a TTY and
--non-interactive
not
set. Headless runs (cron, Telegram, no terminal) will skip prompts.
--fix
(alias for
--repair
) writes a backup to
~/.openclaw/openclaw.json.bak
and drops unknown config keys, listing each removal.
macOS:
launchctl
env overrides
If you previously ran
launchctl setenv OPENCLAW_GATEWAY_TOKEN ...
(or
...PASSWORD
), that value overrides your config file and can cause persistent “unauthorized” errors.
Copy
launchctl
getenv
OPENCLAW_GATEWAY_TOKEN
launchctl
getenv
OPENCLAW_GATEWAY_PASSWORD
launchctl
unsetenv
OPENCLAW_GATEWAY_TOKEN
launchctl
unsetenv
OPENCLAW_GATEWAY_PASSWORD
docs
gateway

---
## Cli > Gateway

[Source: https://docs.openclaw.ai/cli/gateway]

gateway - OpenClaw
OpenClaw
home page
English
GitHub
Releases
CLI commands
gateway
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
CLI commands
CLI Reference
agent
agents
approvals
browser
channels
configure
cron
dashboard
directory
dns
docs
doctor
gateway
health
hooks
logs
memory
message
models
nodes
onboard
pairing
plugins
reset
Sandbox CLI
security
sessions
setup
skills
status
system
tui
uninstall
update
voicecall
RPC and API
RPC Adapters
Device Model Database
Templates
Default AGENTS.md
AGENTS.md Template
BOOT.md Template
BOOTSTRAP.md Template
HEARTBEAT.md Template
IDENTITY
SOUL.md Template
TOOLS.md Template
USER
Technical reference
Wizard Reference
Token Use and Costs
grammY
Concept internals
TypeBox
Markdown Formatting
Typing Indicators
Usage Tracking
Timezones
Project
Credits
Release notes
Release Checklist
Tests
Experiments
Onboarding and Config Protocol
Cron Add Hardening
Telegram Allowlist Hardening
Workspace Memory Research
Model Config Exploration
Gateway CLI
Run the Gateway
Options
Query a running Gateway
gateway health
gateway status
gateway probe
Remote over SSH (Mac app parity)
gateway call &lt;method&gt;
Manage the Gateway service
Discover gateways (Bonjour)
gateway discover
CLI commands
gateway
Gateway CLI
The Gateway is OpenClaw’s WebSocket server (channels, nodes, sessions, hooks).
Subcommands in this page live under
openclaw gateway …
Related docs:
/gateway/bonjour
/gateway/discovery
/gateway/configuration
Run the Gateway
Run a local Gateway process:
Copy
openclaw
gateway
Foreground alias:
Copy
openclaw
gateway
run
Notes:
By default, the Gateway refuses to start unless
gateway.mode=local
is set in
~/.openclaw/openclaw.json
. Use
--allow-unconfigured
for ad-hoc/dev runs.
Binding beyond loopback without auth is blocked (safety guardrail).
SIGUSR1
triggers an in-process restart when authorized (enable
commands.restart
or use the gateway tool/config apply/update).
SIGINT
SIGTERM
handlers stop the gateway process, but they don’t restore any custom terminal state. If you wrap the CLI with a TUI or raw-mode input, restore the terminal before exit.
Options
--port &lt;port&gt;
: WebSocket port (default comes from config/env; usually
18789
--bind &lt;loopback|lan|tailnet|auto|custom&gt;
: listener bind mode.
--auth &lt;token|password&gt;
: auth mode override.
--token &lt;token&gt;
: token override (also sets
OPENCLAW_GATEWAY_TOKEN
for the process).
--password &lt;password&gt;
: password override (also sets
OPENCLAW_GATEWAY_PASSWORD
for the process).
--tailscale &lt;off|serve|funnel&gt;
: expose the Gateway via Tailscale.
--tailscale-reset-on-exit
: reset Tailscale serve/funnel config on shutdown.
--allow-unconfigured
: allow gateway start without
gateway.mode=local
in config.
--dev
: create a dev config + workspace if missing (skips BOOTSTRAP.md).
--reset
: reset dev config + credentials + sessions + workspace (requires
--dev
--force
: kill any existing listener on the selected port before starting.
--verbose
: verbose logs.
--claude-cli-logs
: only show claude-cli logs in the console (and enable its stdout/stderr).
--ws-log &lt;auto|full|compact&gt;
: websocket log style (default
auto
--compact
: alias for
--ws-log compact
--raw-stream
: log raw model stream events to jsonl.
--raw-stream-path &lt;path&gt;
: raw stream jsonl path.
Query a running Gateway
All query commands use WebSocket RPC.
Output modes:
Default: human-readable (colored in TTY).
--json
: machine-readable JSON (no styling/spinner).
--no-color
(or
NO_COLOR=1
): disable ANSI while keeping human layout.
Shared options (where supported):
--url &lt;url&gt;
: Gateway WebSocket URL.
--token &lt;token&gt;
: Gateway token.
--password &lt;password&gt;
: Gateway password.
--timeout &lt;ms&gt;
: timeout/budget (varies per command).
--expect-final
: wait for a “final” response (agent calls).
Note: when you set
--url
, the CLI does not fall back to config or environment credentials.
Pass
--token
--password
explicitly. Missing explicit credentials is an error.
gateway health
Copy
openclaw
gateway
health
--url
ws://127.0.0.1:18789
gateway status
gateway status
shows the Gateway service (launchd/systemd/schtasks) plus an optional RPC probe.
Copy
openclaw
gateway
status
openclaw
gateway
status
--json
Options:
--url &lt;url&gt;
: override the probe URL.
--token &lt;token&gt;
: token auth for the probe.
--password &lt;password&gt;
: password auth for the probe.
--timeout &lt;ms&gt;
: probe timeout (default
10000
--no-probe
: skip the RPC probe (service-only view).
--deep
: scan system-level services too.
gateway probe
gateway probe
is the “debug everything” command. It always probes:
your configured remote gateway (if set), and
localhost (loopback)
even if remote is configured
If multiple gateways are reachable, it prints all of them. Multiple gateways are supported when you use isolated profiles/ports (e.g., a rescue bot), but most installs still run a single gateway.
Copy
openclaw
gateway
probe
openclaw
gateway
probe
--json
Remote over SSH (Mac app parity)
The macOS app “Remote over SSH” mode uses a local port-forward so the remote gateway (which may be bound to loopback only) becomes reachable at
ws://127.0.0.1:&lt;port&gt;
CLI equivalent:
Copy
openclaw
gateway
probe
--ssh
user@gateway-host
Options:
--ssh &lt;target&gt;
user@host
user@host:port
(port defaults to
--ssh-identity &lt;path&gt;
: identity file.
--ssh-auto
: pick the first discovered gateway host as SSH target (LAN/WAB only).
Config (optional, used as defaults):
gateway.remote.sshTarget
gateway.remote.sshIdentity
gateway call &lt;method&gt;
Low-level RPC helper.
Copy
openclaw
gateway
call
status
openclaw
gateway
call
logs.tail
--params
&#x27;{&quot;sinceMs&quot;: 60000}&#x27;
Manage the Gateway service
Copy
openclaw
gateway
install
openclaw
gateway
start
openclaw
gateway
stop
openclaw
gateway
restart
openclaw
gateway
uninstall
Notes:
gateway install
supports
--port
--runtime
--token
--force
--json
Lifecycle commands accept
--json
for scripting.
Discover gateways (Bonjour)
gateway discover
scans for Gateway beacons (
_openclaw-gw._tcp
Multicast DNS-SD:
local.
Unicast DNS-SD (Wide-Area Bonjour): choose a domain (example:
openclaw.internal.
) and set up split DNS + a DNS server; see
/gateway/bonjour
Only gateways with Bonjour discovery enabled (default) advertise the beacon.
Wide-Area discovery records include (TXT):
role
(gateway role hint)
transport
(transport hint, e.g.
gateway
gatewayPort
(WebSocket port, usually
18789
sshPort
(SSH port; defaults to
if not present)
tailnetDns
(MagicDNS hostname, when available)
gatewayTls
gatewayTlsSha256
(TLS enabled + cert fingerprint)
cliPath
(optional hint for remote installs)
gateway discover
Copy
openclaw
gateway
discover
Options:
--timeout &lt;ms&gt;
: per-command timeout (browse/resolve); default
2000
--json
: machine-readable output (also disables styling/spinner).
Examples:
Copy
openclaw
gateway
discover
--timeout
4000
openclaw
gateway
discover
--json
&#x27;.beacons[].wsUrl&#x27;
doctor
health

---
## Cli > Health

[Source: https://docs.openclaw.ai/cli/health]

health - OpenClaw
OpenClaw
home page
English
GitHub
Releases
CLI commands
health
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
CLI commands
CLI Reference
agent
agents
approvals
browser
channels
configure
cron
dashboard
directory
dns
docs
doctor
gateway
health
hooks
logs
memory
message
models
nodes
onboard
pairing
plugins
reset
Sandbox CLI
security
sessions
setup
skills
status
system
tui
uninstall
update
voicecall
RPC and API
RPC Adapters
Device Model Database
Templates
Default AGENTS.md
AGENTS.md Template
BOOT.md Template
BOOTSTRAP.md Template
HEARTBEAT.md Template
IDENTITY
SOUL.md Template
TOOLS.md Template
USER
Technical reference
Wizard Reference
Token Use and Costs
grammY
Concept internals
TypeBox
Markdown Formatting
Typing Indicators
Usage Tracking
Timezones
Project
Credits
Release notes
Release Checklist
Tests
Experiments
Onboarding and Config Protocol
Cron Add Hardening
Telegram Allowlist Hardening
Workspace Memory Research
Model Config Exploration
openclaw health
CLI commands
health
openclaw health
Fetch health from the running Gateway.
Copy
openclaw
health
openclaw
health
--json
openclaw
health
--verbose
Notes:
--verbose
runs live probes and prints per-account timings when multiple accounts are configured.
Output includes per-agent session stores when multiple agents are configured.
gateway
hooks

---
## Cli > Hooks

[Source: https://docs.openclaw.ai/cli/hooks]

hooks - OpenClaw
OpenClaw
home page
English
GitHub
Releases
CLI commands
hooks
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
CLI commands
CLI Reference
agent
agents
approvals
browser
channels
configure
cron
dashboard
directory
dns
docs
doctor
gateway
health
hooks
logs
memory
message
models
nodes
onboard
pairing
plugins
reset
Sandbox CLI
security
sessions
setup
skills
status
system
tui
uninstall
update
voicecall
RPC and API
RPC Adapters
Device Model Database
Templates
Default AGENTS.md
AGENTS.md Template
BOOT.md Template
BOOTSTRAP.md Template
HEARTBEAT.md Template
IDENTITY
SOUL.md Template
TOOLS.md Template
USER
Technical reference
Wizard Reference
Token Use and Costs
grammY
Concept internals
TypeBox
Markdown Formatting
Typing Indicators
Usage Tracking
Timezones
Project
Credits
Release notes
Release Checklist
Tests
Experiments
Onboarding and Config Protocol
Cron Add Hardening
Telegram Allowlist Hardening
Workspace Memory Research
Model Config Exploration
openclaw hooks
List All Hooks
Get Hook Information
Check Hooks Eligibility
Enable a Hook
Disable a Hook
Install Hooks
Update Hooks
Bundled Hooks
session-memory
bootstrap-extra-files
command-logger
boot-md
CLI commands
hooks
openclaw hooks
Manage agent hooks (event-driven automations for commands like
/new
/reset
, and gateway startup).
Related:
Hooks:
Hooks
Plugin hooks:
Plugins
List All Hooks
Copy
openclaw
hooks
list
List all discovered hooks from workspace, managed, and bundled directories.
Options:
--eligible
: Show only eligible hooks (requirements met)
--json
: Output as JSON
-v, --verbose
: Show detailed information including missing requirements
Example output:
Copy
Hooks (4/4 ready)
Ready:
🚀 boot-md ✓ - Run BOOT.md on gateway startup
📎 bootstrap-extra-files ✓ - Inject extra workspace bootstrap files during agent bootstrap
📝 command-logger ✓ - Log all command events to a centralized audit file
💾 session-memory ✓ - Save session context to memory when /new command is issued
Example (verbose):
Copy
openclaw
hooks
list
--verbose
Shows missing requirements for ineligible hooks.
Example (JSON):
Copy
openclaw
hooks
list
--json
Returns structured JSON for programmatic use.
Get Hook Information
Copy
openclaw
hooks
info
&lt;
nam
&gt;
Show detailed information about a specific hook.
Arguments:
&lt;name&gt;
: Hook name (e.g.,
session-memory
Options:
--json
: Output as JSON
Example:
Copy
openclaw
hooks
info
session-memory
Output:
Copy
💾 session-memory ✓ Ready
Save session context to memory when /new command is issued
Details:
Source: openclaw-bundled
Path: /path/to/openclaw/hooks/bundled/session-memory/HOOK.md
Handler: /path/to/openclaw/hooks/bundled/session-memory/handler.ts
Homepage: https://docs.openclaw.ai/automation/hooks#session-memory
Events: command:new
Requirements:
Config: ✓ workspace.dir
Check Hooks Eligibility
Copy
openclaw
hooks
check
Show summary of hook eligibility status (how many are ready vs. not ready).
Options:
--json
: Output as JSON
Example output:
Copy
Hooks Status
Total hooks: 4
Ready: 4
Not ready: 0
Enable a Hook
Copy
openclaw
hooks
enable
&lt;
nam
&gt;
Enable a specific hook by adding it to your config (
~/.openclaw/config.json
Note:
Hooks managed by plugins show
plugin:&lt;id&gt;
openclaw hooks list
and
can’t be enabled/disabled here. Enable/disable the plugin instead.
Arguments:
&lt;name&gt;
: Hook name (e.g.,
session-memory
Example:
Copy
openclaw
hooks
enable
session-memory
Output:
Copy
✓ Enabled hook: 💾 session-memory
What it does:
Checks if hook exists and is eligible
Updates
hooks.internal.entries.&lt;name&gt;.enabled = true
in your config
Saves config to disk
After enabling:
Restart the gateway so hooks reload (menu bar app restart on macOS, or restart your gateway process in dev).
Disable a Hook
Copy
openclaw
hooks
disable
&lt;
nam
&gt;
Disable a specific hook by updating your config.
Arguments:
&lt;name&gt;
: Hook name (e.g.,
command-logger
Example:
Copy
openclaw
hooks
disable
command-logger
Output:
Copy
⏸ Disabled hook: 📝 command-logger
After disabling:
Restart the gateway so hooks reload
Install Hooks
Copy
openclaw
hooks
install
&lt;
path-or-spe
&gt;
Install a hook pack from a local folder/archive or npm.
Npm specs are
registry-only
(package name + optional version/tag). Git/URL/file
specs are rejected. Dependency installs run with
--ignore-scripts
for safety.
What it does:
Copies the hook pack into
~/.openclaw/hooks/&lt;id&gt;
Enables the installed hooks in
hooks.internal.entries.*
Records the install under
hooks.internal.installs
Options:
-l, --link
: Link a local directory instead of copying (adds it to
hooks.internal.load.extraDirs
Supported archives:
.zip
.tgz
.tar.gz
.tar
Examples:
Copy
# Local directory
openclaw
hooks
install
./my-hook-pack
# Local archive
openclaw
hooks
install
./my-hook-pack.zip
# NPM package
openclaw
hooks
install
@openclaw/my-hook-pack
# Link a local directory without copying
openclaw
hooks
install
./my-hook-pack
Update Hooks
Copy
openclaw
hooks
update
&lt;
&gt;
openclaw
hooks
update
--all
Update installed hook packs (npm installs only).
Options:
--all
: Update all tracked hook packs
--dry-run
: Show what would change without writing
Bundled Hooks
session-memory
Saves session context to memory when you issue
/new
Enable:
Copy
openclaw
hooks
enable
session-memory
Output:
~/.openclaw/workspace/memory/YYYY-MM-DD-slug.md
See:
session-memory documentation
bootstrap-extra-files
Injects additional bootstrap files (for example monorepo-local
AGENTS.md
TOOLS.md
) during
agent:bootstrap
Enable:
Copy
openclaw
hooks
enable
bootstrap-extra-files
See:
bootstrap-extra-files documentation
command-logger
Logs all command events to a centralized audit file.
Enable:
Copy
openclaw
hooks
enable
command-logger
Output:
~/.openclaw/logs/commands.log
View logs:
Copy
# Recent commands
tail
~/.openclaw/logs/commands.log
# Pretty-print
cat
~/.openclaw/logs/commands.log
# Filter by action
grep
&#x27;&quot;action&quot;:&quot;new&quot;&#x27;
~/.openclaw/logs/commands.log
See:
command-logger documentation
boot-md
Runs
BOOT.md
when the gateway starts (after channels start).
Events
gateway:startup
Enable
Copy
openclaw
hooks
enable
boot-md
See:
boot-md documentation
health
logs

---
## Cli > Logs

[Source: https://docs.openclaw.ai/cli/logs]

logs - OpenClaw
OpenClaw
home page
English
GitHub
Releases
CLI commands
logs
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
CLI commands
CLI Reference
agent
agents
approvals
browser
channels
configure
cron
dashboard
directory
dns
docs
doctor
gateway
health
hooks
logs
memory
message
models
nodes
onboard
pairing
plugins
reset
Sandbox CLI
security
sessions
setup
skills
status
system
tui
uninstall
update
voicecall
RPC and API
RPC Adapters
Device Model Database
Templates
Default AGENTS.md
AGENTS.md Template
BOOT.md Template
BOOTSTRAP.md Template
HEARTBEAT.md Template
IDENTITY
SOUL.md Template
TOOLS.md Template
USER
Technical reference
Wizard Reference
Token Use and Costs
grammY
Concept internals
TypeBox
Markdown Formatting
Typing Indicators
Usage Tracking
Timezones
Project
Credits
Release notes
Release Checklist
Tests
Experiments
Onboarding and Config Protocol
Cron Add Hardening
Telegram Allowlist Hardening
Workspace Memory Research
Model Config Exploration
openclaw logs
Examples
CLI commands
logs
openclaw logs
Tail Gateway file logs over RPC (works in remote mode).
Related:
Logging overview:
Logging
Examples
Copy
openclaw
logs
openclaw
logs
--follow
openclaw
logs
--json
openclaw
logs
--limit
500
openclaw
logs
--local-time
openclaw
logs
--follow
--local-time
Use
--local-time
to render timestamps in your local timezone.
hooks
memory

---
## Cli > Memory

[Source: https://docs.openclaw.ai/cli/memory]

memory - OpenClaw
OpenClaw
home page
English
GitHub
Releases
CLI commands
memory
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
CLI commands
CLI Reference
agent
agents
approvals
browser
channels
configure
cron
dashboard
directory
dns
docs
doctor
gateway
health
hooks
logs
memory
message
models
nodes
onboard
pairing
plugins
reset
Sandbox CLI
security
sessions
setup
skills
status
system
tui
uninstall
update
voicecall
RPC and API
RPC Adapters
Device Model Database
Templates
Default AGENTS.md
AGENTS.md Template
BOOT.md Template
BOOTSTRAP.md Template
HEARTBEAT.md Template
IDENTITY
SOUL.md Template
TOOLS.md Template
USER
Technical reference
Wizard Reference
Token Use and Costs
grammY
Concept internals
TypeBox
Markdown Formatting
Typing Indicators
Usage Tracking
Timezones
Project
Credits
Release notes
Release Checklist
Tests
Experiments
Onboarding and Config Protocol
Cron Add Hardening
Telegram Allowlist Hardening
Workspace Memory Research
Model Config Exploration
openclaw memory
Examples
Options
CLI commands
memory
openclaw memory
Manage semantic memory indexing and search.
Provided by the active memory plugin (default:
memory-core
; set
plugins.slots.memory = &quot;none&quot;
to disable).
Related:
Memory concept:
Memory
Plugins:
Plugins
Examples
Copy
openclaw
memory
status
openclaw
memory
status
--deep
openclaw
memory
status
--deep
--index
openclaw
memory
status
--deep
--index
--verbose
openclaw
memory
index
openclaw
memory
index
--verbose
openclaw
memory
search
&quot;release checklist&quot;
openclaw
memory
status
--agent
main
openclaw
memory
index
--agent
main
--verbose
Options
Common:
--agent &lt;id&gt;
: scope to a single agent (default: all configured agents).
--verbose
: emit detailed logs during probes and indexing.
Notes:
memory status --deep
probes vector + embedding availability.
memory status --deep --index
runs a reindex if the store is dirty.
memory index --verbose
prints per-phase details (provider, model, sources, batch activity).
memory status
includes any extra paths configured via
memorySearch.extraPaths
logs
message

---
## Cli > Message

[Source: https://docs.openclaw.ai/cli/message]

message - OpenClaw
OpenClaw
home page
English
GitHub
Releases
CLI commands
message
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
CLI commands
CLI Reference
agent
agents
approvals
browser
channels
configure
cron
dashboard
directory
dns
docs
doctor
gateway
health
hooks
logs
memory
message
models
nodes
onboard
pairing
plugins
reset
Sandbox CLI
security
sessions
setup
skills
status
system
tui
uninstall
update
voicecall
RPC and API
RPC Adapters
Device Model Database
Templates
Default AGENTS.md
AGENTS.md Template
BOOT.md Template
BOOTSTRAP.md Template
HEARTBEAT.md Template
IDENTITY
SOUL.md Template
TOOLS.md Template
USER
Technical reference
Wizard Reference
Token Use and Costs
grammY
Concept internals
TypeBox
Markdown Formatting
Typing Indicators
Usage Tracking
Timezones
Project
Credits
Release notes
Release Checklist
Tests
Experiments
Onboarding and Config Protocol
Cron Add Hardening
Telegram Allowlist Hardening
Workspace Memory Research
Model Config Exploration
openclaw message
Usage
Common flags
Actions
Core
Threads
Emojis
Stickers
Roles / Channels / Members / Voice
Events
Moderation (Discord)
Broadcast
Examples
CLI commands
message
openclaw message
Single outbound command for sending messages and channel actions
(Discord/Google Chat/Slack/Mattermost (plugin)/Telegram/WhatsApp/Signal/iMessage/MS Teams).
Usage
Copy
openclaw message &lt;subcommand&gt; [flags]
Channel selection:
--channel
required if more than one channel is configured.
If exactly one channel is configured, it becomes the default.
Values:
whatsapp|telegram|discord|googlechat|slack|mattermost|signal|imessage|msteams
(Mattermost requires plugin)
Target formats (
--target
WhatsApp: E.164 or group JID
Telegram: chat id or
@username
Discord:
channel:&lt;id&gt;
user:&lt;id&gt;
(or
&lt;@id&gt;
mention; raw numeric ids are treated as channels)
Google Chat:
spaces/&lt;spaceId&gt;
users/&lt;userId&gt;
Slack:
channel:&lt;id&gt;
user:&lt;id&gt;
(raw channel id is accepted)
Mattermost (plugin):
channel:&lt;id&gt;
user:&lt;id&gt;
, or
@username
(bare ids are treated as channels)
Signal:
+E.164
group:&lt;id&gt;
signal:+E.164
signal:group:&lt;id&gt;
, or
username:&lt;name&gt;
u:&lt;name&gt;
iMessage: handle,
chat_id:&lt;id&gt;
chat_guid:&lt;guid&gt;
, or
chat_identifier:&lt;id&gt;
MS Teams: conversation id (
19:
[email&#160;protected]
) or
conversation:&lt;id&gt;
user:&lt;aad-object-id&gt;
Name lookup:
For supported providers (Discord/Slack/etc), channel names like
Help
#help
are resolved via the directory cache.
On cache miss, OpenClaw will attempt a live directory lookup when the provider supports it.
Common flags
--channel &lt;name&gt;
--account &lt;id&gt;
--target &lt;dest&gt;
(target channel or user for send/poll/read/etc)
--targets &lt;name&gt;
(repeat; broadcast only)
--json
--dry-run
--verbose
Actions
Core
send
Channels: WhatsApp/Telegram/Discord/Google Chat/Slack/Mattermost (plugin)/Signal/iMessage/MS Teams
Required:
--target
, plus
--message
--media
Optional:
--media
--reply-to
--thread-id
--gif-playback
Telegram only:
--buttons
(requires
channels.telegram.capabilities.inlineButtons
to allow it)
Telegram only:
--thread-id
(forum topic id)
Slack only:
--thread-id
(thread timestamp;
--reply-to
uses the same field)
WhatsApp only:
--gif-playback
poll
Channels: WhatsApp/Telegram/Discord/Matrix/MS Teams
Required:
--target
--poll-question
--poll-option
(repeat)
Optional:
--poll-multi
Discord only:
--poll-duration-hours
--silent
--message
Telegram only:
--poll-duration-seconds
(5-600),
--silent
--poll-anonymous
--poll-public
--thread-id
react
Channels: Discord/Google Chat/Slack/Telegram/WhatsApp/Signal
Required:
--message-id
--target
Optional:
--emoji
--remove
--participant
--from-me
--target-author
--target-author-uuid
Note:
--remove
requires
--emoji
(omit
--emoji
to clear own reactions where supported; see /tools/reactions)
WhatsApp only:
--participant
--from-me
Signal group reactions:
--target-author
--target-author-uuid
required
reactions
Channels: Discord/Google Chat/Slack
Required:
--message-id
--target
Optional:
--limit
read
Channels: Discord/Slack
Required:
--target
Optional:
--limit
--before
--after
Discord only:
--around
edit
Channels: Discord/Slack
Required:
--message-id
--message
--target
delete
Channels: Discord/Slack/Telegram
Required:
--message-id
--target
pin
unpin
Channels: Discord/Slack
Required:
--message-id
--target
pins
(list)
Channels: Discord/Slack
Required:
--target
permissions
Channels: Discord
Required:
--target
search
Channels: Discord
Required:
--guild-id
--query
Optional:
--channel-id
--channel-ids
(repeat),
--author-id
--author-ids
(repeat),
--limit
Threads
thread create
Channels: Discord
Required:
--thread-name
--target
(channel id)
Optional:
--message-id
--message
--auto-archive-min
thread list
Channels: Discord
Required:
--guild-id
Optional:
--channel-id
--include-archived
--before
--limit
thread reply
Channels: Discord
Required:
--target
(thread id),
--message
Optional:
--media
--reply-to
Emojis
emoji list
Discord:
--guild-id
Slack: no extra flags
emoji upload
Channels: Discord
Required:
--guild-id
--emoji-name
--media
Optional:
--role-ids
(repeat)
Stickers
sticker send
Channels: Discord
Required:
--target
--sticker-id
(repeat)
Optional:
--message
sticker upload
Channels: Discord
Required:
--guild-id
--sticker-name
--sticker-desc
--sticker-tags
--media
Roles / Channels / Members / Voice
role info
(Discord):
--guild-id
role add
role remove
(Discord):
--guild-id
--user-id
--role-id
channel info
(Discord):
--target
channel list
(Discord):
--guild-id
member info
(Discord/Slack):
--user-id
--guild-id
for Discord)
voice status
(Discord):
--guild-id
--user-id
Events
event list
(Discord):
--guild-id
event create
(Discord):
--guild-id
--event-name
--start-time
Optional:
--end-time
--desc
--channel-id
--location
--event-type
Moderation (Discord)
timeout
--guild-id
--user-id
(optional
--duration-min
--until
; omit both to clear timeout)
kick
--guild-id
--user-id
--reason
ban
--guild-id
--user-id
--delete-days
--reason
timeout
also supports
--reason
Broadcast
broadcast
Channels: any configured channel; use
--channel all
to target all providers
Required:
--targets
(repeat)
Optional:
--message
--media
--dry-run
Examples
Send a Discord reply:
Copy
openclaw message send --channel discord \
--target channel:123 --message &quot;hi&quot; --reply-to 456
Create a Discord poll:
Copy
openclaw message poll --channel discord \
--target channel:123 \
--poll-question &quot;Snack?&quot; \
--poll-option Pizza --poll-option Sushi \
--poll-multi --poll-duration-hours 48
Create a Telegram poll (auto-close in 2 minutes):
Copy
openclaw message poll --channel telegram \
--target @mychat \
--poll-question &quot;Lunch?&quot; \
--poll-option Pizza --poll-option Sushi \
--poll-duration-seconds 120 --silent
Send a Teams proactive message:
Copy
openclaw message send --channel msteams \
--target conversation:19:
[email&#160;protected]
--message &quot;hi&quot;
Create a Teams poll:
Copy
openclaw message poll --channel msteams \
--target conversation:19:
[email&#160;protected]
--poll-question &quot;Lunch?&quot; \
--poll-option Pizza --poll-option Sushi
React in Slack:
Copy
openclaw message react --channel slack \
--target C123 --message-id 456 --emoji &quot;✅&quot;
React in a Signal group:
Copy
openclaw message react --channel signal \
--target signal:group:abc123 --message-id 1737630212345 \
--emoji &quot;✅&quot; --target-author-uuid 123e4567-e89b-12d3-a456-426614174000
Send Telegram inline buttons:
Copy
openclaw message send --channel telegram --target @mychat --message &quot;Choose:&quot; \
--buttons &#x27;[ [{&quot;text&quot;:&quot;Yes&quot;,&quot;callback_data&quot;:&quot;cmd:yes&quot;}], [{&quot;text&quot;:&quot;No&quot;,&quot;callback_data&quot;:&quot;cmd:no&quot;}] ]&#x27;
memory
models

---
## Cli > Models

[Source: https://docs.openclaw.ai/cli/models]

models - OpenClaw
OpenClaw
home page
English
GitHub
Releases
CLI commands
models
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
CLI commands
CLI Reference
agent
agents
approvals
browser
channels
configure
cron
dashboard
directory
dns
docs
doctor
gateway
health
hooks
logs
memory
message
models
nodes
onboard
pairing
plugins
reset
Sandbox CLI
security
sessions
setup
skills
status
system
tui
uninstall
update
voicecall
RPC and API
RPC Adapters
Device Model Database
Templates
Default AGENTS.md
AGENTS.md Template
BOOT.md Template
BOOTSTRAP.md Template
HEARTBEAT.md Template
IDENTITY
SOUL.md Template
TOOLS.md Template
USER
Technical reference
Wizard Reference
Token Use and Costs
grammY
Concept internals
TypeBox
Markdown Formatting
Typing Indicators
Usage Tracking
Timezones
Project
Credits
Release notes
Release Checklist
Tests
Experiments
Onboarding and Config Protocol
Cron Add Hardening
Telegram Allowlist Hardening
Workspace Memory Research
Model Config Exploration
openclaw models
Common commands
models status
Aliases + fallbacks
Auth profiles
CLI commands
models
openclaw models
Model discovery, scanning, and configuration (default model, fallbacks, auth profiles).
Related:
Providers + models:
Models
Provider auth setup:
Getting started
Common commands
Copy
openclaw
models
status
openclaw
models
list
openclaw
models
set
&lt;
model-or-alia
&gt;
openclaw
models
scan
openclaw models status
shows the resolved default/fallbacks plus an auth overview.
When provider usage snapshots are available, the OAuth/token status section includes
provider usage headers.
Add
--probe
to run live auth probes against each configured provider profile.
Probes are real requests (may consume tokens and trigger rate limits).
Use
--agent &lt;id&gt;
to inspect a configured agent’s model/auth state. When omitted,
the command uses
OPENCLAW_AGENT_DIR
PI_CODING_AGENT_DIR
if set, otherwise the
configured default agent.
Notes:
models set &lt;model-or-alias&gt;
accepts
provider/model
or an alias.
Model refs are parsed by splitting on the
first
. If the model ID includes
(OpenRouter-style), include the provider prefix (example:
openrouter/moonshotai/kimi-k2
If you omit the provider, OpenClaw treats the input as an alias or a model for the
default provider
(only works when there is no
in the model ID).
models status
Options:
--json
--plain
--check
(exit 1=expired/missing, 2=expiring)
--probe
(live probe of configured auth profiles)
--probe-provider &lt;name&gt;
(probe one provider)
--probe-profile &lt;id&gt;
(repeat or comma-separated profile ids)
--probe-timeout &lt;ms&gt;
--probe-concurrency &lt;n&gt;
--probe-max-tokens &lt;n&gt;
--agent &lt;id&gt;
(configured agent id; overrides
OPENCLAW_AGENT_DIR
PI_CODING_AGENT_DIR
Aliases + fallbacks
Copy
openclaw
models
aliases
list
openclaw
models
fallbacks
list
Auth profiles
Copy
openclaw
models
auth
add
openclaw
models
auth
login
--provider
&lt;
&gt;
openclaw
models
auth
setup-token
openclaw
models
auth
paste-token
models auth login
runs a provider plugin’s auth flow (OAuth/API key). Use
openclaw plugins list
to see which providers are installed.
Notes:
setup-token
prompts for a setup-token value (generate it with
claude setup-token
on any machine).
paste-token
accepts a token string generated elsewhere or from automation.
message
nodes

---
## Cli > Nodes

[Source: https://docs.openclaw.ai/cli/nodes]

nodes - OpenClaw
OpenClaw
home page
English
GitHub
Releases
CLI commands
nodes
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
CLI commands
CLI Reference
agent
agents
approvals
browser
channels
configure
cron
dashboard
directory
dns
docs
doctor
gateway
health
hooks
logs
memory
message
models
nodes
onboard
pairing
plugins
reset
Sandbox CLI
security
sessions
setup
skills
status
system
tui
uninstall
update
voicecall
RPC and API
RPC Adapters
Device Model Database
Templates
Default AGENTS.md
AGENTS.md Template
BOOT.md Template
BOOTSTRAP.md Template
HEARTBEAT.md Template
IDENTITY
SOUL.md Template
TOOLS.md Template
USER
Technical reference
Wizard Reference
Token Use and Costs
grammY
Concept internals
TypeBox
Markdown Formatting
Typing Indicators
Usage Tracking
Timezones
Project
Credits
Release notes
Release Checklist
Tests
Experiments
Onboarding and Config Protocol
Cron Add Hardening
Telegram Allowlist Hardening
Workspace Memory Research
Model Config Exploration
openclaw nodes
Common commands
Invoke / run
Exec-style defaults
CLI commands
nodes
openclaw nodes
Manage paired nodes (devices) and invoke node capabilities.
Related:
Nodes overview:
Nodes
Camera:
Camera nodes
Images:
Image nodes
Common options:
--url
--token
--timeout
--json
Common commands
Copy
openclaw
nodes
list
openclaw
nodes
list
--connected
openclaw
nodes
list
--last-connected
24h
openclaw
nodes
pending
openclaw
nodes
approve
&lt;
requestI
&gt;
openclaw
nodes
status
openclaw
nodes
status
--connected
openclaw
nodes
status
--last-connected
24h
nodes list
prints pending/paired tables. Paired rows include the most recent connect age (Last Connect).
Use
--connected
to only show currently-connected nodes. Use
--last-connected &lt;duration&gt;
filter to nodes that connected within a duration (e.g.
24h
Invoke / run
Copy
openclaw
nodes
invoke
--node
&lt;
name
&gt;
--command
&lt;
comman
&gt;
--params
&lt;
jso
&gt;
openclaw
nodes
run
--node
&lt;
name
&gt;
&lt;
command..
&gt;
openclaw
nodes
run
--raw
&quot;git status&quot;
openclaw
nodes
run
--agent
main
--node
&lt;
name
&gt;
--raw
&quot;git status&quot;
Invoke flags:
--params &lt;json&gt;
: JSON object string (default
--invoke-timeout &lt;ms&gt;
: node invoke timeout (default
15000
--idempotency-key &lt;key&gt;
: optional idempotency key.
Exec-style defaults
nodes run
mirrors the model’s exec behavior (defaults + approvals):
Reads
tools.exec.*
(plus
agents.list[].tools.exec.*
overrides).
Uses exec approvals (
exec.approval.request
) before invoking
system.run
--node
can be omitted when
tools.exec.node
is set.
Requires a node that advertises
system.run
(macOS companion app or headless node host).
Flags:
--cwd &lt;path&gt;
: working directory.
--env &lt;key=val&gt;
: env override (repeatable). Note: node hosts ignore
PATH
overrides (and
tools.exec.pathPrepend
is not applied to node hosts).
--command-timeout &lt;ms&gt;
: command timeout.
--invoke-timeout &lt;ms&gt;
: node invoke timeout (default
30000
--needs-screen-recording
: require screen recording permission.
--raw &lt;command&gt;
: run a shell string (
/bin/sh -lc
cmd.exe /c
--agent &lt;id&gt;
: agent-scoped approvals/allowlists (defaults to configured agent).
--ask &lt;off|on-miss|always&gt;
--security &lt;deny|allowlist|full&gt;
: overrides.
models
onboard

---
## Cli > Onboard

[Source: https://docs.openclaw.ai/cli/onboard]

onboard - OpenClaw
OpenClaw
home page
English
GitHub
Releases
CLI commands
onboard
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
CLI commands
CLI Reference
agent
agents
approvals
browser
channels
configure
cron
dashboard
directory
dns
docs
doctor
gateway
health
hooks
logs
memory
message
models
nodes
onboard
pairing
plugins
reset
Sandbox CLI
security
sessions
setup
skills
status
system
tui
uninstall
update
voicecall
RPC and API
RPC Adapters
Device Model Database
Templates
Default AGENTS.md
AGENTS.md Template
BOOT.md Template
BOOTSTRAP.md Template
HEARTBEAT.md Template
IDENTITY
SOUL.md Template
TOOLS.md Template
USER
Technical reference
Wizard Reference
Token Use and Costs
grammY
Concept internals
TypeBox
Markdown Formatting
Typing Indicators
Usage Tracking
Timezones
Project
Credits
Release notes
Release Checklist
Tests
Experiments
Onboarding and Config Protocol
Cron Add Hardening
Telegram Allowlist Hardening
Workspace Memory Research
Model Config Exploration
openclaw onboard
Related guides
Examples
Common follow-up commands
CLI commands
onboard
openclaw onboard
Interactive onboarding wizard (local or remote Gateway setup).
Related guides
CLI onboarding hub:
Onboarding Wizard (CLI)
Onboarding overview:
Onboarding Overview
CLI onboarding reference:
CLI Onboarding Reference
CLI automation:
CLI Automation
macOS onboarding:
Onboarding (macOS App)
Examples
Copy
openclaw
onboard
openclaw
onboard
--flow
quickstart
openclaw
onboard
--flow
manual
openclaw
onboard
--mode
remote
--remote-url
ws://gateway-host:18789
Non-interactive custom provider:
Copy
openclaw
onboard
--non-interactive
--auth-choice
custom-api-key
--custom-base-url
&quot;https://llm.example.com/v1&quot;
--custom-model-id
&quot;foo-large&quot;
--custom-api-key
&quot;$CUSTOM_API_KEY&quot;
--custom-compatibility
openai
--custom-api-key
is optional in non-interactive mode. If omitted, onboarding checks
CUSTOM_API_KEY
Non-interactive Z.AI endpoint choices:
Note:
--auth-choice zai-api-key
now auto-detects the best Z.AI endpoint for your key (prefers the general API with
zai/glm-5
If you specifically want the GLM Coding Plan endpoints, pick
zai-coding-global
zai-coding-cn
Copy
# Promptless endpoint selection
openclaw
onboard
--non-interactive
--auth-choice
zai-coding-global
--zai-api-key
&quot;$ZAI_API_KEY&quot;
# Other Z.AI endpoint choices:
# --auth-choice zai-coding-cn
# --auth-choice zai-global
# --auth-choice zai-cn
Flow notes:
quickstart
: minimal prompts, auto-generates a gateway token.
manual
: full prompts for port/bind/auth (alias of
advanced
Fastest first chat:
openclaw dashboard
(Control UI, no channel setup).
Custom Provider: connect any OpenAI or Anthropic compatible endpoint,
including hosted providers not listed. Use Unknown to auto-detect.
Common follow-up commands
Copy
openclaw
configure
openclaw
agents
add
&lt;
nam
&gt;
--json
does not imply non-interactive mode. Use
--non-interactive
for scripts.
nodes
pairing

---
## Cli > Pairing

[Source: https://docs.openclaw.ai/cli/pairing]

pairing - OpenClaw
OpenClaw
home page
English
GitHub
Releases
CLI commands
pairing
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
CLI commands
CLI Reference
agent
agents
approvals
browser
channels
configure
cron
dashboard
directory
dns
docs
doctor
gateway
health
hooks
logs
memory
message
models
nodes
onboard
pairing
plugins
reset
Sandbox CLI
security
sessions
setup
skills
status
system
tui
uninstall
update
voicecall
RPC and API
RPC Adapters
Device Model Database
Templates
Default AGENTS.md
AGENTS.md Template
BOOT.md Template
BOOTSTRAP.md Template
HEARTBEAT.md Template
IDENTITY
SOUL.md Template
TOOLS.md Template
USER
Technical reference
Wizard Reference
Token Use and Costs
grammY
Concept internals
TypeBox
Markdown Formatting
Typing Indicators
Usage Tracking
Timezones
Project
Credits
Release notes
Release Checklist
Tests
Experiments
Onboarding and Config Protocol
Cron Add Hardening
Telegram Allowlist Hardening
Workspace Memory Research
Model Config Exploration
openclaw pairing
Commands
CLI commands
pairing
openclaw pairing
Approve or inspect DM pairing requests (for channels that support pairing).
Related:
Pairing flow:
Pairing
Commands
Copy
openclaw
pairing
list
whatsapp
openclaw
pairing
approve
whatsapp
&lt;
cod
&gt;
--notify
onboard
plugins

---
## Cli > Plugins

[Source: https://docs.openclaw.ai/cli/plugins]

plugins - OpenClaw
OpenClaw
home page
English
GitHub
Releases
CLI commands
plugins
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
CLI commands
CLI Reference
agent
agents
approvals
browser
channels
configure
cron
dashboard
directory
dns
docs
doctor
gateway
health
hooks
logs
memory
message
models
nodes
onboard
pairing
plugins
reset
Sandbox CLI
security
sessions
setup
skills
status
system
tui
uninstall
update
voicecall
RPC and API
RPC Adapters
Device Model Database
Templates
Default AGENTS.md
AGENTS.md Template
BOOT.md Template
BOOTSTRAP.md Template
HEARTBEAT.md Template
IDENTITY
SOUL.md Template
TOOLS.md Template
USER
Technical reference
Wizard Reference
Token Use and Costs
grammY
Concept internals
TypeBox
Markdown Formatting
Typing Indicators
Usage Tracking
Timezones
Project
Credits
Release notes
Release Checklist
Tests
Experiments
Onboarding and Config Protocol
Cron Add Hardening
Telegram Allowlist Hardening
Workspace Memory Research
Model Config Exploration
openclaw plugins
Commands
Install
Uninstall
Update
CLI commands
plugins
openclaw plugins
Manage Gateway plugins/extensions (loaded in-process).
Related:
Plugin system:
Plugins
Plugin manifest + schema:
Plugin manifest
Security hardening:
Security
Commands
Copy
openclaw
plugins
list
openclaw
plugins
info
&lt;
&gt;
openclaw
plugins
enable
&lt;
&gt;
openclaw
plugins
disable
&lt;
&gt;
openclaw
plugins
uninstall
&lt;
&gt;
openclaw
plugins
doctor
openclaw
plugins
update
&lt;
&gt;
openclaw
plugins
update
--all
Bundled plugins ship with OpenClaw but start disabled. Use
plugins enable
activate them.
All plugins must ship a
openclaw.plugin.json
file with an inline JSON Schema
configSchema
, even if empty). Missing/invalid manifests or schemas prevent
the plugin from loading and fail config validation.
Install
Copy
openclaw
plugins
install
&lt;
path-or-spe
&gt;
Security note: treat plugin installs like running code. Prefer pinned versions.
Npm specs are
registry-only
(package name + optional version/tag). Git/URL/file
specs are rejected. Dependency installs run with
--ignore-scripts
for safety.
Supported archives:
.zip
.tgz
.tar.gz
.tar
Use
--link
to avoid copying a local directory (adds to
plugins.load.paths
Copy
openclaw
plugins
install
./my-plugin
Uninstall
Copy
openclaw
plugins
uninstall
&lt;
&gt;
openclaw
plugins
uninstall
&lt;
&gt;
--dry-run
openclaw
plugins
uninstall
&lt;
&gt;
--keep-files
uninstall
removes plugin records from
plugins.entries
plugins.installs
the plugin allowlist, and linked
plugins.load.paths
entries when applicable.
For active memory plugins, the memory slot resets to
memory-core
By default, uninstall also removes the plugin install directory under the active
state dir extensions root (
$OPENCLAW_STATE_DIR/extensions/&lt;id&gt;
). Use
--keep-files
to keep files on disk.
--keep-config
is supported as a deprecated alias for
--keep-files
Update
Copy
openclaw
plugins
update
&lt;
&gt;
openclaw
plugins
update
--all
openclaw
plugins
update
&lt;
&gt;
--dry-run
Updates only apply to plugins installed from npm (tracked in
plugins.installs
pairing
reset

---
## Cli > Reset

[Source: https://docs.openclaw.ai/cli/reset]

reset - OpenClaw
OpenClaw
home page
English
GitHub
Releases
CLI commands
reset
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
CLI commands
CLI Reference
agent
agents
approvals
browser
channels
configure
cron
dashboard
directory
dns
docs
doctor
gateway
health
hooks
logs
memory
message
models
nodes
onboard
pairing
plugins
reset
Sandbox CLI
security
sessions
setup
skills
status
system
tui
uninstall
update
voicecall
RPC and API
RPC Adapters
Device Model Database
Templates
Default AGENTS.md
AGENTS.md Template
BOOT.md Template
BOOTSTRAP.md Template
HEARTBEAT.md Template
IDENTITY
SOUL.md Template
TOOLS.md Template
USER
Technical reference
Wizard Reference
Token Use and Costs
grammY
Concept internals
TypeBox
Markdown Formatting
Typing Indicators
Usage Tracking
Timezones
Project
Credits
Release notes
Release Checklist
Tests
Experiments
Onboarding and Config Protocol
Cron Add Hardening
Telegram Allowlist Hardening
Workspace Memory Research
Model Config Exploration
openclaw reset
CLI commands
reset
openclaw reset
Reset local config/state (keeps the CLI installed).
Copy
openclaw
reset
openclaw
reset
--dry-run
openclaw
reset
--scope
config+creds+sessions
--yes
--non-interactive
plugins
Sandbox CLI

---
## Cli > Sandbox

[Source: https://docs.openclaw.ai/cli/sandbox]

Sandbox CLI - OpenClaw
OpenClaw
home page
English
GitHub
Releases
CLI commands
Sandbox CLI
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
CLI commands
CLI Reference
agent
agents
approvals
browser
channels
configure
cron
dashboard
directory
dns
docs
doctor
gateway
health
hooks
logs
memory
message
models
nodes
onboard
pairing
plugins
reset
Sandbox CLI
security
sessions
setup
skills
status
system
tui
uninstall
update
voicecall
RPC and API
RPC Adapters
Device Model Database
Templates
Default AGENTS.md
AGENTS.md Template
BOOT.md Template
BOOTSTRAP.md Template
HEARTBEAT.md Template
IDENTITY
SOUL.md Template
TOOLS.md Template
USER
Technical reference
Wizard Reference
Token Use and Costs
grammY
Concept internals
TypeBox
Markdown Formatting
Typing Indicators
Usage Tracking
Timezones
Project
Credits
Release notes
Release Checklist
Tests
Experiments
Onboarding and Config Protocol
Cron Add Hardening
Telegram Allowlist Hardening
Workspace Memory Research
Model Config Exploration
Sandbox CLI
Overview
Commands
openclaw sandbox explain
openclaw sandbox list
openclaw sandbox recreate
Use Cases
After updating Docker images
After changing sandbox configuration
After changing setupCommand
For a specific agent only
Why is this needed?
Configuration
See Also
CLI commands
Sandbox CLI
Sandbox CLI
Manage Docker-based sandbox containers for isolated agent execution.
Overview
OpenClaw can run agents in isolated Docker containers for security. The
sandbox
commands help you manage these containers, especially after updates or configuration changes.
Commands
openclaw sandbox explain
Inspect the
effective
sandbox mode/scope/workspace access, sandbox tool policy, and elevated gates (with fix-it config key paths).
Copy
openclaw
sandbox
explain
openclaw
sandbox
explain
--session
agent:main:main
openclaw
sandbox
explain
--agent
work
openclaw
sandbox
explain
--json
openclaw sandbox list
List all sandbox containers with their status and configuration.
Copy
openclaw
sandbox
list
openclaw
sandbox
list
--browser
# List only browser containers
openclaw
sandbox
list
--json
# JSON output
Output includes:
Container name and status (running/stopped)
Docker image and whether it matches config
Age (time since creation)
Idle time (time since last use)
Associated session/agent
openclaw sandbox recreate
Remove sandbox containers to force recreation with updated images/config.
Copy
openclaw
sandbox
recreate
--all
# Recreate all containers
openclaw
sandbox
recreate
--session
main
# Specific session
openclaw
sandbox
recreate
--agent
mybot
# Specific agent
openclaw
sandbox
recreate
--browser
# Only browser containers
openclaw
sandbox
recreate
--all
--force
# Skip confirmation
Options:
--all
: Recreate all sandbox containers
--session &lt;key&gt;
: Recreate container for specific session
--agent &lt;id&gt;
: Recreate containers for specific agent
--browser
: Only recreate browser containers
--force
: Skip confirmation prompt
Important:
Containers are automatically recreated when the agent is next used.
Use Cases
After updating Docker images
Copy
# Pull new image
docker
pull
openclaw-sandbox:latest
docker
tag
openclaw-sandbox:latest
openclaw-sandbox:bookworm-slim
# Update config to use new image
# Edit config: agents.defaults.sandbox.docker.image (or agents.list[].sandbox.docker.image)
# Recreate containers
openclaw
sandbox
recreate
--all
After changing sandbox configuration
Copy
# Edit config: agents.defaults.sandbox.* (or agents.list[].sandbox.*)
# Recreate to apply new config
openclaw
sandbox
recreate
--all
After changing setupCommand
Copy
openclaw
sandbox
recreate
--all
# or just one agent:
openclaw
sandbox
recreate
--agent
family
For a specific agent only
Copy
# Update only one agent&#x27;s containers
openclaw
sandbox
recreate
--agent
alfred
Why is this needed?
Problem:
When you update sandbox Docker images or configuration:
Existing containers continue running with old settings
Containers are only pruned after 24h of inactivity
Regularly-used agents keep old containers running indefinitely
Solution:
Use
openclaw sandbox recreate
to force removal of old containers. They’ll be recreated automatically with current settings when next needed.
Tip: prefer
openclaw sandbox recreate
over manual
docker rm
. It uses the
Gateway’s container naming and avoids mismatches when scope/session keys change.
Configuration
Sandbox settings live in
~/.openclaw/openclaw.json
under
agents.defaults.sandbox
(per-agent overrides go in
agents.list[].sandbox
Copy
&quot;agents&quot;
&quot;defaults&quot;
&quot;sandbox&quot;
&quot;mode&quot;
&quot;all&quot;
// off, non-main, all
&quot;scope&quot;
&quot;agent&quot;
// session, agent, shared
&quot;docker&quot;
&quot;image&quot;
&quot;openclaw-sandbox:bookworm-slim&quot;
&quot;containerPrefix&quot;
&quot;openclaw-sbx-&quot;
// ... more Docker options
&quot;prune&quot;
&quot;idleHours&quot;
// Auto-prune after 24h idle
&quot;maxAgeDays&quot;
// Auto-prune after 7 days
See Also
Sandbox Documentation
Agent Configuration
Doctor Command
- Check sandbox setup
reset
security

---
## Cli > Security

[Source: https://docs.openclaw.ai/cli/security]

security - OpenClaw
OpenClaw
home page
English
GitHub
Releases
CLI commands
security
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
CLI commands
CLI Reference
agent
agents
approvals
browser
channels
configure
cron
dashboard
directory
dns
docs
doctor
gateway
health
hooks
logs
memory
message
models
nodes
onboard
pairing
plugins
reset
Sandbox CLI
security
sessions
setup
skills
status
system
tui
uninstall
update
voicecall
RPC and API
RPC Adapters
Device Model Database
Templates
Default AGENTS.md
AGENTS.md Template
BOOT.md Template
BOOTSTRAP.md Template
HEARTBEAT.md Template
IDENTITY
SOUL.md Template
TOOLS.md Template
USER
Technical reference
Wizard Reference
Token Use and Costs
grammY
Concept internals
TypeBox
Markdown Formatting
Typing Indicators
Usage Tracking
Timezones
Project
Credits
Release notes
Release Checklist
Tests
Experiments
Onboarding and Config Protocol
Cron Add Hardening
Telegram Allowlist Hardening
Workspace Memory Research
Model Config Exploration
openclaw security
Audit
CLI commands
security
openclaw security
Security tools (audit + optional fixes).
Related:
Security guide:
Security
Audit
Copy
openclaw
security
audit
openclaw
security
audit
--deep
openclaw
security
audit
--fix
The audit warns when multiple DM senders share the main session and recommends
secure DM mode
session.dmScope=&quot;per-channel-peer&quot;
(or
per-account-channel-peer
for multi-account channels) for shared inboxes.
It also warns when small models (
&lt;=300B
) are used without sandboxing and with web/browser tools enabled.
For webhook ingress, it warns when
hooks.defaultSessionKey
is unset, when request
sessionKey
overrides are enabled, and when overrides are enabled without
hooks.allowedSessionKeyPrefixes
It also warns when sandbox Docker settings are configured while sandbox mode is off, when
gateway.nodes.denyCommands
uses ineffective pattern-like/unknown entries, when global
tools.profile=&quot;minimal&quot;
is overridden by agent tool profiles, and when installed extension plugin tools may be reachable under permissive tool policy.
Sandbox CLI
sessions

---
## Cli > Sessions

[Source: https://docs.openclaw.ai/cli/sessions]

sessions - OpenClaw
OpenClaw
home page
English
GitHub
Releases
CLI commands
sessions
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
CLI commands
CLI Reference
agent
agents
approvals
browser
channels
configure
cron
dashboard
directory
dns
docs
doctor
gateway
health
hooks
logs
memory
message
models
nodes
onboard
pairing
plugins
reset
Sandbox CLI
security
sessions
setup
skills
status
system
tui
uninstall
update
voicecall
RPC and API
RPC Adapters
Device Model Database
Templates
Default AGENTS.md
AGENTS.md Template
BOOT.md Template
BOOTSTRAP.md Template
HEARTBEAT.md Template
IDENTITY
SOUL.md Template
TOOLS.md Template
USER
Technical reference
Wizard Reference
Token Use and Costs
grammY
Concept internals
TypeBox
Markdown Formatting
Typing Indicators
Usage Tracking
Timezones
Project
Credits
Release notes
Release Checklist
Tests
Experiments
Onboarding and Config Protocol
Cron Add Hardening
Telegram Allowlist Hardening
Workspace Memory Research
Model Config Exploration
openclaw sessions
CLI commands
sessions
openclaw sessions
List stored conversation sessions.
Copy
openclaw
sessions
openclaw
sessions
--active
120
openclaw
sessions
--json
security
setup

---
## Cli > Setup

[Source: https://docs.openclaw.ai/cli/setup]

setup - OpenClaw
OpenClaw
home page
English
GitHub
Releases
CLI commands
setup
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
CLI commands
CLI Reference
agent
agents
approvals
browser
channels
configure
cron
dashboard
directory
dns
docs
doctor
gateway
health
hooks
logs
memory
message
models
nodes
onboard
pairing
plugins
reset
Sandbox CLI
security
sessions
setup
skills
status
system
tui
uninstall
update
voicecall
RPC and API
RPC Adapters
Device Model Database
Templates
Default AGENTS.md
AGENTS.md Template
BOOT.md Template
BOOTSTRAP.md Template
HEARTBEAT.md Template
IDENTITY
SOUL.md Template
TOOLS.md Template
USER
Technical reference
Wizard Reference
Token Use and Costs
grammY
Concept internals
TypeBox
Markdown Formatting
Typing Indicators
Usage Tracking
Timezones
Project
Credits
Release notes
Release Checklist
Tests
Experiments
Onboarding and Config Protocol
Cron Add Hardening
Telegram Allowlist Hardening
Workspace Memory Research
Model Config Exploration
openclaw setup
Examples
CLI commands
setup
openclaw setup
Initialize
~/.openclaw/openclaw.json
and the agent workspace.
Related:
Getting started:
Getting started
Wizard:
Onboarding
Examples
Copy
openclaw
setup
openclaw
setup
--workspace
~/.openclaw/workspace
To run the wizard via setup:
Copy
openclaw
setup
--wizard
sessions
skills

---
## Cli > Skills

[Source: https://docs.openclaw.ai/cli/skills]

skills - OpenClaw
OpenClaw
home page
English
GitHub
Releases
CLI commands
skills
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
CLI commands
CLI Reference
agent
agents
approvals
browser
channels
configure
cron
dashboard
directory
dns
docs
doctor
gateway
health
hooks
logs
memory
message
models
nodes
onboard
pairing
plugins
reset
Sandbox CLI
security
sessions
setup
skills
status
system
tui
uninstall
update
voicecall
RPC and API
RPC Adapters
Device Model Database
Templates
Default AGENTS.md
AGENTS.md Template
BOOT.md Template
BOOTSTRAP.md Template
HEARTBEAT.md Template
IDENTITY
SOUL.md Template
TOOLS.md Template
USER
Technical reference
Wizard Reference
Token Use and Costs
grammY
Concept internals
TypeBox
Markdown Formatting
Typing Indicators
Usage Tracking
Timezones
Project
Credits
Release notes
Release Checklist
Tests
Experiments
Onboarding and Config Protocol
Cron Add Hardening
Telegram Allowlist Hardening
Workspace Memory Research
Model Config Exploration
openclaw skills
Commands
CLI commands
skills
openclaw skills
Inspect skills (bundled + workspace + managed overrides) and see what’s eligible vs missing requirements.
Related:
Skills system:
Skills
Skills config:
Skills config
ClawHub installs:
ClawHub
Commands
Copy
openclaw
skills
list
openclaw
skills
list
--eligible
openclaw
skills
info
&lt;
nam
&gt;
openclaw
skills
check
setup
status

---
## Cli > Status

[Source: https://docs.openclaw.ai/cli/status]

status - OpenClaw
OpenClaw
home page
English
GitHub
Releases
CLI commands
status
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
CLI commands
CLI Reference
agent
agents
approvals
browser
channels
configure
cron
dashboard
directory
dns
docs
doctor
gateway
health
hooks
logs
memory
message
models
nodes
onboard
pairing
plugins
reset
Sandbox CLI
security
sessions
setup
skills
status
system
tui
uninstall
update
voicecall
RPC and API
RPC Adapters
Device Model Database
Templates
Default AGENTS.md
AGENTS.md Template
BOOT.md Template
BOOTSTRAP.md Template
HEARTBEAT.md Template
IDENTITY
SOUL.md Template
TOOLS.md Template
USER
Technical reference
Wizard Reference
Token Use and Costs
grammY
Concept internals
TypeBox
Markdown Formatting
Typing Indicators
Usage Tracking
Timezones
Project
Credits
Release notes
Release Checklist
Tests
Experiments
Onboarding and Config Protocol
Cron Add Hardening
Telegram Allowlist Hardening
Workspace Memory Research
Model Config Exploration
openclaw status
CLI commands
status
openclaw status
Diagnostics for channels + sessions.
Copy
openclaw
status
openclaw
status
--all
openclaw
status
--deep
openclaw
status
--usage
Notes:
--deep
runs live probes (WhatsApp Web + Telegram + Discord + Google Chat + Slack + Signal).
Output includes per-agent session stores when multiple agents are configured.
Overview includes Gateway + node host service install/runtime status when available.
Overview includes update channel + git SHA (for source checkouts).
Update info surfaces in the Overview; if an update is available, status prints a hint to run
openclaw update
(see
Updating
skills
system

---
## Cli > System

[Source: https://docs.openclaw.ai/cli/system]

system - OpenClaw
OpenClaw
home page
English
GitHub
Releases
CLI commands
system
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
CLI commands
CLI Reference
agent
agents
approvals
browser
channels
configure
cron
dashboard
directory
dns
docs
doctor
gateway
health
hooks
logs
memory
message
models
nodes
onboard
pairing
plugins
reset
Sandbox CLI
security
sessions
setup
skills
status
system
tui
uninstall
update
voicecall
RPC and API
RPC Adapters
Device Model Database
Templates
Default AGENTS.md
AGENTS.md Template
BOOT.md Template
BOOTSTRAP.md Template
HEARTBEAT.md Template
IDENTITY
SOUL.md Template
TOOLS.md Template
USER
Technical reference
Wizard Reference
Token Use and Costs
grammY
Concept internals
TypeBox
Markdown Formatting
Typing Indicators
Usage Tracking
Timezones
Project
Credits
Release notes
Release Checklist
Tests
Experiments
Onboarding and Config Protocol
Cron Add Hardening
Telegram Allowlist Hardening
Workspace Memory Research
Model Config Exploration
openclaw system
Common commands
system event
system heartbeat last|enable|disable
system presence
Notes
CLI commands
system
openclaw system
System-level helpers for the Gateway: enqueue system events, control heartbeats,
and view presence.
Common commands
Copy
openclaw
system
event
--text
&quot;Check for urgent follow-ups&quot;
--mode
now
openclaw
system
heartbeat
enable
openclaw
system
heartbeat
last
openclaw
system
presence
system event
Enqueue a system event on the
main
session. The next heartbeat will inject
it as a
System:
line in the prompt. Use
--mode now
to trigger the heartbeat
immediately;
next-heartbeat
waits for the next scheduled tick.
Flags:
--text &lt;text&gt;
: required system event text.
--mode &lt;mode&gt;
now
next-heartbeat
(default).
--json
: machine-readable output.
system heartbeat last|enable|disable
Heartbeat controls:
last
: show the last heartbeat event.
enable
: turn heartbeats back on (use this if they were disabled).
disable
: pause heartbeats.
Flags:
--json
: machine-readable output.
system presence
List the current system presence entries the Gateway knows about (nodes,
instances, and similar status lines).
Flags:
--json
: machine-readable output.
Notes
Requires a running Gateway reachable by your current config (local or remote).
System events are ephemeral and not persisted across restarts.
status
tui

---
## Cli > Tui

[Source: https://docs.openclaw.ai/cli/tui]

tui - OpenClaw
OpenClaw
home page
English
GitHub
Releases
CLI commands
tui
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
CLI commands
CLI Reference
agent
agents
approvals
browser
channels
configure
cron
dashboard
directory
dns
docs
doctor
gateway
health
hooks
logs
memory
message
models
nodes
onboard
pairing
plugins
reset
Sandbox CLI
security
sessions
setup
skills
status
system
tui
uninstall
update
voicecall
RPC and API
RPC Adapters
Device Model Database
Templates
Default AGENTS.md
AGENTS.md Template
BOOT.md Template
BOOTSTRAP.md Template
HEARTBEAT.md Template
IDENTITY
SOUL.md Template
TOOLS.md Template
USER
Technical reference
Wizard Reference
Token Use and Costs
grammY
Concept internals
TypeBox
Markdown Formatting
Typing Indicators
Usage Tracking
Timezones
Project
Credits
Release notes
Release Checklist
Tests
Experiments
Onboarding and Config Protocol
Cron Add Hardening
Telegram Allowlist Hardening
Workspace Memory Research
Model Config Exploration
openclaw tui
Examples
CLI commands
tui
openclaw tui
Open the terminal UI connected to the Gateway.
Related:
TUI guide:
TUI
Examples
Copy
openclaw
tui
openclaw
tui
--url
ws://127.0.0.1:18789
--token
&lt;
toke
&gt;
openclaw
tui
--session
main
--deliver
system
uninstall

---
## Cli > Uninstall

[Source: https://docs.openclaw.ai/cli/uninstall]

uninstall - OpenClaw
OpenClaw
home page
English
GitHub
Releases
CLI commands
uninstall
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
CLI commands
CLI Reference
agent
agents
approvals
browser
channels
configure
cron
dashboard
directory
dns
docs
doctor
gateway
health
hooks
logs
memory
message
models
nodes
onboard
pairing
plugins
reset
Sandbox CLI
security
sessions
setup
skills
status
system
tui
uninstall
update
voicecall
RPC and API
RPC Adapters
Device Model Database
Templates
Default AGENTS.md
AGENTS.md Template
BOOT.md Template
BOOTSTRAP.md Template
HEARTBEAT.md Template
IDENTITY
SOUL.md Template
TOOLS.md Template
USER
Technical reference
Wizard Reference
Token Use and Costs
grammY
Concept internals
TypeBox
Markdown Formatting
Typing Indicators
Usage Tracking
Timezones
Project
Credits
Release notes
Release Checklist
Tests
Experiments
Onboarding and Config Protocol
Cron Add Hardening
Telegram Allowlist Hardening
Workspace Memory Research
Model Config Exploration
openclaw uninstall
CLI commands
uninstall
openclaw uninstall
Uninstall the gateway service + local data (CLI remains).
Copy
openclaw
uninstall
openclaw
uninstall
--all
--yes
openclaw
uninstall
--dry-run
tui
update

---
## Cli > Update

[Source: https://docs.openclaw.ai/cli/update]

update - OpenClaw
OpenClaw
home page
English
GitHub
Releases
CLI commands
update
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
CLI commands
CLI Reference
agent
agents
approvals
browser
channels
configure
cron
dashboard
directory
dns
docs
doctor
gateway
health
hooks
logs
memory
message
models
nodes
onboard
pairing
plugins
reset
Sandbox CLI
security
sessions
setup
skills
status
system
tui
uninstall
update
voicecall
RPC and API
RPC Adapters
Device Model Database
Templates
Default AGENTS.md
AGENTS.md Template
BOOT.md Template
BOOTSTRAP.md Template
HEARTBEAT.md Template
IDENTITY
SOUL.md Template
TOOLS.md Template
USER
Technical reference
Wizard Reference
Token Use and Costs
grammY
Concept internals
TypeBox
Markdown Formatting
Typing Indicators
Usage Tracking
Timezones
Project
Credits
Release notes
Release Checklist
Tests
Experiments
Onboarding and Config Protocol
Cron Add Hardening
Telegram Allowlist Hardening
Workspace Memory Research
Model Config Exploration
openclaw update
Usage
Options
update status
update wizard
What it does
Git checkout flow
--update shorthand
See also
CLI commands
update
openclaw update
Safely update OpenClaw and switch between stable/beta/dev channels.
If you installed via
npm/pnpm
(global install, no git metadata), updates happen via the package manager flow in
Updating
Usage
Copy
openclaw
update
openclaw
update
status
openclaw
update
wizard
openclaw
update
--channel
beta
openclaw
update
--channel
dev
openclaw
update
--tag
beta
openclaw
update
--no-restart
openclaw
update
--json
openclaw
--update
Options
--no-restart
: skip restarting the Gateway service after a successful update.
--channel &lt;stable|beta|dev&gt;
: set the update channel (git + npm; persisted in config).
--tag &lt;dist-tag|version&gt;
: override the npm dist-tag or version for this update only.
--json
: print machine-readable
UpdateRunResult
JSON.
--timeout &lt;seconds&gt;
: per-step timeout (default is 1200s).
Note: downgrades require confirmation because older versions can break configuration.
update status
Show the active update channel + git tag/branch/SHA (for source checkouts), plus update availability.
Copy
openclaw
update
status
openclaw
update
status
--json
openclaw
update
status
--timeout
Options:
--json
: print machine-readable status JSON.
--timeout &lt;seconds&gt;
: timeout for checks (default is 3s).
update wizard
Interactive flow to pick an update channel and confirm whether to restart the Gateway
after updating (default is to restart). If you select
dev
without a git checkout, it
offers to create one.
What it does
When you switch channels explicitly (
--channel ...
), OpenClaw also keeps the
install method aligned:
dev
→ ensures a git checkout (default:
~/openclaw
, override with
OPENCLAW_GIT_DIR
updates it, and installs the global CLI from that checkout.
stable
beta
→ installs from npm using the matching dist-tag.
Git checkout flow
Channels:
stable
: checkout the latest non-beta tag, then build + doctor.
beta
: checkout the latest
-beta
tag, then build + doctor.
dev
: checkout
main
, then fetch + rebase.
High-level:
Requires a clean worktree (no uncommitted changes).
Switches to the selected channel (tag or branch).
Fetches upstream (dev only).
Dev only: preflight lint + TypeScript build in a temp worktree; if the tip fails, walks back up to 10 commits to find the newest clean build.
Rebases onto the selected commit (dev only).
Installs deps (pnpm preferred; npm fallback).
Builds + builds the Control UI.
Runs
openclaw doctor
as the final “safe update” check.
Syncs plugins to the active channel (dev uses bundled extensions; stable/beta uses npm) and updates npm-installed plugins.
--update
shorthand
openclaw --update
rewrites to
openclaw update
(useful for shells and launcher scripts).
See also
openclaw doctor
(offers to run update first on git checkouts)
Development channels
Updating
CLI reference
uninstall
voicecall

---
## Cli > Voicecall

[Source: https://docs.openclaw.ai/cli/voicecall]

voicecall - OpenClaw
OpenClaw
home page
English
GitHub
Releases
CLI commands
voicecall
Install
Channels
Agents
Tools
Models
Platforms
Gateway &amp; Ops
Reference
Help
CLI commands
CLI Reference
agent
agents
approvals
browser
channels
configure
cron
dashboard
directory
dns
docs
doctor
gateway
health
hooks
logs
memory
message
models
nodes
onboard
pairing
plugins
reset
Sandbox CLI
security
sessions
setup
skills
status
system
tui
uninstall
update
voicecall
RPC and API
RPC Adapters
Device Model Database
Templates
Default AGENTS.md
AGENTS.md Template
BOOT.md Template
BOOTSTRAP.md Template
HEARTBEAT.md Template
IDENTITY
SOUL.md Template
TOOLS.md Template
USER
Technical reference
Wizard Reference
Token Use and Costs
grammY
Concept internals
TypeBox
Markdown Formatting
Typing Indicators
Usage Tracking
Timezones
Project
Credits
Release notes
Release Checklist
Tests
Experiments
Onboarding and Config Protocol
Cron Add Hardening
Telegram Allowlist Hardening
Workspace Memory Research
Model Config Exploration
openclaw voicecall
Common commands
Exposing webhooks (Tailscale)
CLI commands
voicecall
openclaw voicecall
voicecall
is a plugin-provided command. It only appears if the voice-call plugin is installed and enabled.
Primary doc:
Voice-call plugin:
Voice Call
Common commands
Copy
openclaw
voicecall
status
--call-id
&lt;
&gt;
openclaw
voicecall
call
--to
&quot;+15555550123&quot;
--message
&quot;Hello&quot;
--mode
notify
openclaw
voicecall
continue
--call-id
&lt;
&gt;
--message
&quot;Any questions?&quot;
openclaw
voicecall
end
--call-id
&lt;
&gt;
Exposing webhooks (Tailscale)
Copy
openclaw
voicecall
expose
--mode
serve
openclaw
voicecall
expose
--mode
funnel
openclaw
voicecall
unexpose
Security note: only expose the webhook endpoint to networks you trust. Prefer Tailscale Serve over Funnel when possible.
update
RPC Adapters