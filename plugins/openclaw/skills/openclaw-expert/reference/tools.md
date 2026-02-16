# OpenClaw Tools Reference

All built-in tools, browser, skills, plugins, slash commands, sub-agents.


---
## Tools > Agent Send

[Source: https://docs.openclaw.ai/tools/agent-send]

Agent Send - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Agent coordination
Agent Send
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
openclaw agent (direct agent runs)
Behavior
Examples
Flags
Agent coordination
Agent Send
openclaw agent
(direct agent runs)
openclaw agent
runs a single agent turn without needing an inbound chat message.
By default it goes
through the Gateway
; add
--local
to force the embedded
runtime on the current machine.
Behavior
Required:
--message &lt;text&gt;
Session selection:
--to &lt;dest&gt;
derives the session key (group/channel targets preserve isolation; direct chats collapse to
main
--session-id &lt;id&gt;
reuses an existing session by id,
--agent &lt;id&gt;
targets a configured agent directly (uses that agent’s
main
session key)
Runs the same embedded agent runtime as normal inbound replies.
Thinking/verbose flags persist into the session store.
Output:
default: prints reply text (plus
MEDIA:&lt;url&gt;
lines)
--json
: prints structured payload + metadata
Optional delivery back to a channel with
--deliver
--channel
(target formats match
openclaw message --target
Use
--reply-channel
--reply-to
--reply-account
to override delivery without changing the session.
If the Gateway is unreachable, the CLI
falls back
to the embedded local run.
Examples
Copy
openclaw
agent
--to
+15555550123
--message
&quot;status update&quot;
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
--to
+15555550123
--message
&quot;Trace logs&quot;
--verbose
--json
openclaw
agent
--to
+15555550123
--message
&quot;Summon reply&quot;
--deliver
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
Flags
--local
: run locally (requires model provider API keys in your shell)
--deliver
: send the reply to the chosen channel
--channel
: delivery channel (
whatsapp|telegram|discord|googlechat|slack|signal|imessage
, default:
whatsapp
--reply-to
: delivery target override
--reply-channel
: delivery channel override
--reply-account
: delivery account id override
--thinking &lt;off|minimal|low|medium|high|xhigh&gt;
: persist thinking level (GPT-5.2 + Codex models only)
--verbose &lt;on|full|off&gt;
: persist verbose level
--timeout &lt;seconds&gt;
: override agent timeout
--json
: output structured JSON
Browser Troubleshooting
Sub-Agents

---
## Tools > Apply Patch

[Source: https://docs.openclaw.ai/tools/apply-patch]

apply_patch Tool - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Built-in tools
apply_patch Tool
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
apply_patch tool
Parameters
Notes
Example
Built-in tools
apply_patch Tool
apply_patch tool
Apply file changes using a structured patch format. This is ideal for multi-file
or multi-hunk edits where a single
edit
call would be brittle.
The tool accepts a single
input
string that wraps one or more file operations:
Copy
*** Begin Patch
*** Add File: path/to/file.txt
+line 1
+line 2
*** Update File: src/app.ts
-old line
+new line
*** Delete File: obsolete.txt
*** End Patch
Parameters
input
(required): Full patch contents including
*** Begin Patch
and
*** End Patch
Notes
Patch paths support relative paths (from the workspace directory) and absolute paths.
tools.exec.applyPatch.workspaceOnly
defaults to
true
(workspace-contained). Set it to
false
only if you intentionally want
apply_patch
to write/delete outside the workspace directory.
Use
*** Move to:
within an
*** Update File:
hunk to rename files.
*** End of File
marks an EOF-only insert when needed.
Experimental and disabled by default. Enable with
tools.exec.applyPatch.enabled
OpenAI-only (including OpenAI Codex). Optionally gate by model via
tools.exec.applyPatch.allowModels
Config is only under
tools.exec
Example
Copy
&quot;tool&quot;
&quot;apply_patch&quot;
&quot;input&quot;
&quot;*** Begin Patch\n*** Update File: src/index.ts\n@@\n-const foo = 1\n+const foo = 2\n*** End Patch&quot;
Web Tools
Elevated Mode

---
## Tools > Browser Linux Troubleshooting

[Source: https://docs.openclaw.ai/tools/browser-linux-troubleshooting]

Browser Troubleshooting - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Browser
Browser Troubleshooting
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
Browser Troubleshooting (Linux)
Problem: “Failed to start Chrome CDP on port 18800”
Root Cause
Solution 1: Install Google Chrome (Recommended)
Solution 2: Use Snap Chromium with Attach-Only Mode
Verifying the Browser Works
Config Reference
Problem: “Chrome extension relay is running, but no tab is connected”
Browser
Browser Troubleshooting
Browser Troubleshooting (Linux)
Problem: “Failed to start Chrome CDP on port 18800”
OpenClaw’s browser control server fails to launch Chrome/Brave/Edge/Chromium with the error:
Copy
{&quot;error&quot;:&quot;Error: Failed to start Chrome CDP on port 18800 for profile \&quot;openclaw\&quot;.&quot;}
Root Cause
On Ubuntu (and many Linux distros), the default Chromium installation is a
snap package
. Snap’s AppArmor confinement interferes with how OpenClaw spawns and monitors the browser process.
The
apt install chromium
command installs a stub package that redirects to snap:
Copy
Note, selecting &#x27;chromium-browser&#x27; instead of &#x27;chromium&#x27;
chromium-browser is already the newest version (2:1snap1-0ubuntu2).
This is NOT a real browser — it’s just a wrapper.
Solution 1: Install Google Chrome (Recommended)
Install the official Google Chrome
.deb
package, which is not sandboxed by snap:
Copy
wget
https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo
dpkg
google-chrome-stable_current_amd64.deb
sudo
apt
--fix-broken
install
# if there are dependency errors
Then update your OpenClaw config (
~/.openclaw/openclaw.json
Copy
&quot;browser&quot;
&quot;enabled&quot;
true
&quot;executablePath&quot;
&quot;/usr/bin/google-chrome-stable&quot;
&quot;headless&quot;
true
&quot;noSandbox&quot;
true
Solution 2: Use Snap Chromium with Attach-Only Mode
If you must use snap Chromium, configure OpenClaw to attach to a manually-started browser:
Update config:
Copy
&quot;browser&quot;
&quot;enabled&quot;
true
&quot;attachOnly&quot;
true
&quot;headless&quot;
true
&quot;noSandbox&quot;
true
Start Chromium manually:
Copy
chromium-browser
--headless
--no-sandbox
--disable-gpu
--remote-debugging-port=18800
--user-data-dir=$HOME/.openclaw/browser/openclaw/user-data
about:blank
&amp;
Optionally create a systemd user service to auto-start Chrome:
Copy
# ~/.config/systemd/user/openclaw-browser.service
[Unit]
Description=
OpenClaw Browser (Chrome CDP)
After=
network.target
[Service]
ExecStart=
/snap/bin/chromium --headless --no-sandbox --disable-gpu --
remote-debugging-port=
18800 --
user-data-dir=
%h/.openclaw/browser/openclaw/user-data about:blank
Restart=
on-failure
RestartSec=
[Install]
WantedBy=
default.target
Enable with:
systemctl --user enable --now openclaw-browser.service
Verifying the Browser Works
Check status:
Copy
curl
http://127.0.0.1:18791/
&#x27;{running, pid, chosenBrowser}&#x27;
Test browsing:
Copy
curl
POST
http://127.0.0.1:18791/start
curl
http://127.0.0.1:18791/tabs
Config Reference
Option
Description
Default
browser.enabled
Enable browser control
true
browser.executablePath
Path to a Chromium-based browser binary (Chrome/Brave/Edge/Chromium)
auto-detected (prefers default browser when Chromium-based)
browser.headless
Run without GUI
false
browser.noSandbox
Add
--no-sandbox
flag (needed for some Linux setups)
false
browser.attachOnly
Don’t launch browser, only attach to existing
false
browser.cdpPort
Chrome DevTools Protocol port
18800
Problem: “Chrome extension relay is running, but no tab is connected”
You’re using the
chrome
profile (extension relay). It expects the OpenClaw
browser extension to be attached to a live tab.
Fix options:
Use the managed browser:
openclaw browser start --browser-profile openclaw
(or set
browser.defaultProfile: &quot;openclaw&quot;
Use the extension relay:
install the extension, open a tab, and click the
OpenClaw extension icon to attach it.
Notes:
The
chrome
profile uses your
system default Chromium browser
when possible.
Local
openclaw
profiles auto-assign
cdpPort
cdpUrl
; only set those for remote CDP.
Chrome Extension
Agent Send

---
## Tools > Browser Login

[Source: https://docs.openclaw.ai/tools/browser-login]

Browser Login - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Browser
Browser Login
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
Browser login + X/Twitter posting
Manual login (recommended)
Which Chrome profile is used?
X/Twitter: recommended flow
Sandboxing + host browser access
Browser
Browser Login
Browser login + X/Twitter posting
Manual login (recommended)
When a site requires login,
sign in manually
in the
host
browser profile (the openclaw browser).
not
give the model your credentials. Automated logins often trigger anti‑bot defenses and can lock the account.
Back to the main browser docs:
Browser
Which Chrome profile is used?
OpenClaw controls a
dedicated Chrome profile
(named
openclaw
, orange‑tinted UI). This is separate from your daily browser profile.
Two easy ways to access it:
Ask the agent to open the browser
and then log in yourself.
Open it via CLI
Copy
openclaw
browser
start
openclaw
browser
open
https://x.com
If you have multiple profiles, pass
--browser-profile &lt;name&gt;
(the default is
openclaw
X/Twitter: recommended flow
Read/search/threads:
use the
host
browser (manual login).
Post updates:
use the
host
browser (manual login).
Sandboxing + host browser access
Sandboxed browser sessions are
more likely
to trigger bot detection. For X/Twitter (and other strict sites), prefer the
host
browser.
If the agent is sandboxed, the browser tool defaults to the sandbox. To allow host control:
Copy
agents
defaults
sandbox
mode
&quot;non-main&quot;
browser
allowHostControl
true
Then target the host browser:
Copy
openclaw
browser
open
https://x.com
--browser-profile
openclaw
--target
host
Or disable sandboxing for the agent that posts updates.
Browser (OpenClaw-managed)
Chrome Extension

---
## Tools > Browser

[Source: https://docs.openclaw.ai/tools/browser]

Browser (OpenClaw-managed) - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Browser
Browser (OpenClaw-managed)
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
Browser (openclaw-managed)
What you get
Quick start
Profiles: openclaw vs chrome
Configuration
Use Brave (or another Chromium-based browser)
Local vs remote control
Node browser proxy (zero-config default)
Browserless (hosted remote CDP)
Security
Profiles (multi-browser)
Chrome extension relay (use your existing Chrome)
Sandboxed sessions
Setup
Isolation guarantees
Browser selection
Control API (optional)
Playwright requirement
Docker Playwright install
How it works (internal)
CLI quick reference
Snapshots and refs
Wait power-ups
Debug workflows
JSON output
State and environment knobs
Security &amp; privacy
Troubleshooting
Agent tools + how control works
Browser
Browser (OpenClaw-managed)
Browser (openclaw-managed)
OpenClaw can run a
dedicated Chrome/Brave/Edge/Chromium profile
that the agent controls.
It is isolated from your personal browser and is managed through a small local
control service inside the Gateway (loopback only).
Beginner view:
Think of it as a
separate, agent-only browser
The
openclaw
profile does
not
touch your personal browser profile.
The agent can
open tabs, read pages, click, and type
in a safe lane.
The default
chrome
profile uses the
system default Chromium browser
via the
extension relay; switch to
openclaw
for the isolated managed browser.
What you get
A separate browser profile named
openclaw
(orange accent by default).
Deterministic tab control (list/open/focus/close).
Agent actions (click/type/drag/select), snapshots, screenshots, PDFs.
Optional multi-profile support (
openclaw
work
remote
, …).
This browser is
not
your daily driver. It is a safe, isolated surface for
agent automation and verification.
Quick start
Copy
openclaw
browser
--browser-profile
openclaw
status
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
If you get “Browser disabled”, enable it in config (see below) and restart the
Gateway.
Profiles:
openclaw
chrome
openclaw
: managed, isolated browser (no extension required).
chrome
: extension relay to your
system browser
(requires the OpenClaw
extension to be attached to a tab).
Set
browser.defaultProfile: &quot;openclaw&quot;
if you want managed mode by default.
Configuration
Browser settings live in
~/.openclaw/openclaw.json
Copy
browser
enabled
true
// default: true
// cdpUrl: &quot;http://127.0.0.1:18792&quot;,
// legacy single-profile override
remoteCdpTimeoutMs
1500
// remote CDP HTTP timeout (ms)
remoteCdpHandshakeTimeoutMs
3000
// remote CDP WebSocket handshake timeout (ms)
defaultProfile
&quot;chrome&quot;
color
&quot;#FF4500&quot;
headless
false
noSandbox
false
attachOnly
false
executablePath
&quot;/Applications/Brave Browser.app/Contents/MacOS/Brave Browser&quot;
profiles
openclaw
cdpPort
18800
color
&quot;#FF4500&quot;
work
cdpPort
18801
color
&quot;#0066CC&quot;
remote
cdpUrl
&quot;http://10.0.0.42:9222&quot;
color
&quot;#00AA00&quot;
Notes:
The browser control service binds to loopback on a port derived from
gateway.port
(default:
18791
, which is gateway + 2). The relay uses the next port (
18792
If you override the Gateway port (
gateway.port
OPENCLAW_GATEWAY_PORT
the derived browser ports shift to stay in the same “family”.
cdpUrl
defaults to the relay port when unset.
remoteCdpTimeoutMs
applies to remote (non-loopback) CDP reachability checks.
remoteCdpHandshakeTimeoutMs
applies to remote CDP WebSocket reachability checks.
attachOnly: true
means “never launch a local browser; only attach if it is already running.”
color
+ per-profile
color
tint the browser UI so you can see which profile is active.
Default profile is
chrome
(extension relay). Use
defaultProfile: &quot;openclaw&quot;
for the managed browser.
Auto-detect order: system default browser if Chromium-based; otherwise Chrome → Brave → Edge → Chromium → Chrome Canary.
Local
openclaw
profiles auto-assign
cdpPort
cdpUrl
— set those only for remote CDP.
Use Brave (or another Chromium-based browser)
If your
system default
browser is Chromium-based (Chrome/Brave/Edge/etc),
OpenClaw uses it automatically. Set
browser.executablePath
to override
auto-detection:
CLI example:
Copy
openclaw
config
set
browser.executablePath
&quot;/usr/bin/google-chrome&quot;
Copy
// macOS
browser
executablePath
&quot;/Applications/Brave Browser.app/Contents/MacOS/Brave Browser&quot;
// Windows
browser
executablePath
&quot;C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe&quot;
// Linux
browser
executablePath
&quot;/usr/bin/brave-browser&quot;
Local vs remote control
Local control (default):
the Gateway starts the loopback control service and can launch a local browser.
Remote control (node host):
run a node host on the machine that has the browser; the Gateway proxies browser actions to it.
Remote CDP:
set
browser.profiles.&lt;name&gt;.cdpUrl
(or
browser.cdpUrl
) to
attach to a remote Chromium-based browser. In this case, OpenClaw will not launch a local browser.
Remote CDP URLs can include auth:
Query tokens (e.g.,
https://provider.example?token=&lt;token&gt;
HTTP Basic auth (e.g.,
https://user:
[email&#160;protected]
OpenClaw preserves the auth when calling
/json/*
endpoints and when connecting
to the CDP WebSocket. Prefer environment variables or secrets managers for
tokens instead of committing them to config files.
Node browser proxy (zero-config default)
If you run a
node host
on the machine that has your browser, OpenClaw can
auto-route browser tool calls to that node without any extra browser config.
This is the default path for remote gateways.
Notes:
The node host exposes its local browser control server via a
proxy command
Profiles come from the node’s own
browser.profiles
config (same as local).
Disable if you don’t want it:
On the node:
nodeHost.browserProxy.enabled=false
On the gateway:
gateway.nodes.browser.mode=&quot;off&quot;
Browserless (hosted remote CDP)
Browserless
is a hosted Chromium service that exposes
CDP endpoints over HTTPS. You can point a OpenClaw browser profile at a
Browserless region endpoint and authenticate with your API key.
Example:
Copy
browser
enabled
true
defaultProfile
&quot;browserless&quot;
remoteCdpTimeoutMs
2000
remoteCdpHandshakeTimeoutMs
4000
profiles
browserless
cdpUrl
&quot;https://production-sfo.browserless.io?token=&lt;BROWSERLESS_API_KEY&gt;&quot;
color
&quot;#00AA00&quot;
Notes:
Replace
&lt;BROWSERLESS_API_KEY&gt;
with your real Browserless token.
Choose the region endpoint that matches your Browserless account (see their docs).
Security
Key ideas:
Browser control is loopback-only; access flows through the Gateway’s auth or node pairing.
If browser control is enabled and no auth is configured, OpenClaw auto-generates
gateway.auth.token
on startup and persists it to config.
Keep the Gateway and any node hosts on a private network (Tailscale); avoid public exposure.
Treat remote CDP URLs/tokens as secrets; prefer env vars or a secrets manager.
Remote CDP tips:
Prefer HTTPS endpoints and short-lived tokens where possible.
Avoid embedding long-lived tokens directly in config files.
Profiles (multi-browser)
OpenClaw supports multiple named profiles (routing configs). Profiles can be:
openclaw-managed
: a dedicated Chromium-based browser instance with its own user data directory + CDP port
remote
: an explicit CDP URL (Chromium-based browser running elsewhere)
extension relay
: your existing Chrome tab(s) via the local relay + Chrome extension
Defaults:
The
openclaw
profile is auto-created if missing.
The
chrome
profile is built-in for the Chrome extension relay (points at
http://127.0.0.1:18792
by default).
Local CDP ports allocate from
18800–18899
by default.
Deleting a profile moves its local data directory to Trash.
All control endpoints accept
?profile=&lt;name&gt;
; the CLI uses
--browser-profile
Chrome extension relay (use your existing Chrome)
OpenClaw can also drive
your existing Chrome tabs
(no separate “openclaw” Chrome instance) via a local CDP relay + a Chrome extension.
Full guide:
Chrome extension
Flow:
The Gateway runs locally (same machine) or a node host runs on the browser machine.
A local
relay server
listens at a loopback
cdpUrl
(default:
http://127.0.0.1:18792
You click the
OpenClaw Browser Relay
extension icon on a tab to attach (it does not auto-attach).
The agent controls that tab via the normal
browser
tool, by selecting the right profile.
If the Gateway runs elsewhere, run a node host on the browser machine so the Gateway can proxy browser actions.
Sandboxed sessions
If the agent session is sandboxed, the
browser
tool may default to
target=&quot;sandbox&quot;
(sandbox browser).
Chrome extension relay takeover requires host browser control, so either:
run the session unsandboxed, or
set
agents.defaults.sandbox.browser.allowHostControl: true
and use
target=&quot;host&quot;
when calling the tool.
Setup
Load the extension (dev/unpacked):
Copy
openclaw
browser
extension
install
Chrome →
chrome://extensions
→ enable “Developer mode”
“Load unpacked” → select the directory printed by
openclaw browser extension path
Pin the extension, then click it on the tab you want to control (badge shows
Use it:
CLI:
openclaw browser --browser-profile chrome tabs
Agent tool:
browser
with
profile=&quot;chrome&quot;
Optional: if you want a different name or relay port, create your own profile:
Copy
openclaw
browser
create-profile
--name
my-chrome
--driver
extension
--cdp-url
http://127.0.0.1:18792
--color
&quot;#00AA00&quot;
Notes:
This mode relies on Playwright-on-CDP for most operations (screenshots/snapshots/actions).
Detach by clicking the extension icon again.
Isolation guarantees
Dedicated user data dir
: never touches your personal browser profile.
Dedicated ports
: avoids
9222
to prevent collisions with dev workflows.
Deterministic tab control
: target tabs by
targetId
, not “last tab”.
Browser selection
When launching locally, OpenClaw picks the first available:
Chrome
Brave
Edge
Chromium
Chrome Canary
You can override with
browser.executablePath
Platforms:
macOS: checks
/Applications
and
~/Applications
Linux: looks for
google-chrome
brave
microsoft-edge
chromium
, etc.
Windows: checks common install locations.
Control API (optional)
For local integrations only, the Gateway exposes a small loopback HTTP API:
Status/start/stop:
GET /
POST /start
POST /stop
Tabs:
GET /tabs
POST /tabs/open
POST /tabs/focus
DELETE /tabs/:targetId
Snapshot/screenshot:
GET /snapshot
POST /screenshot
Actions:
POST /navigate
POST /act
Hooks:
POST /hooks/file-chooser
POST /hooks/dialog
Downloads:
POST /download
POST /wait/download
Debugging:
GET /console
POST /pdf
Debugging:
GET /errors
GET /requests
POST /trace/start
POST /trace/stop
POST /highlight
Network:
POST /response/body
State:
GET /cookies
POST /cookies/set
POST /cookies/clear
State:
GET /storage/:kind
POST /storage/:kind/set
POST /storage/:kind/clear
Settings:
POST /set/offline
POST /set/headers
POST /set/credentials
POST /set/geolocation
POST /set/media
POST /set/timezone
POST /set/locale
POST /set/device
All endpoints accept
?profile=&lt;name&gt;
If gateway auth is configured, browser HTTP routes require auth too:
Authorization: Bearer &lt;gateway token&gt;
x-openclaw-password: &lt;gateway password&gt;
or HTTP Basic auth with that password
Playwright requirement
Some features (navigate/act/AI snapshot/role snapshot, element screenshots, PDF) require
Playwright. If Playwright isn’t installed, those endpoints return a clear 501
error. ARIA snapshots and basic screenshots still work for openclaw-managed Chrome.
For the Chrome extension relay driver, ARIA snapshots and screenshots require Playwright.
If you see
Playwright is not available in this gateway build
, install the full
Playwright package (not
playwright-core
) and restart the gateway, or reinstall
OpenClaw with browser support.
Docker Playwright install
If your Gateway runs in Docker, avoid
npx playwright
(npm override conflicts).
Use the bundled CLI instead:
Copy
docker
compose
run
--rm
openclaw-cli
node
/app/node_modules/playwright-core/cli.js
install
chromium
To persist browser downloads, set
PLAYWRIGHT_BROWSERS_PATH
(for example,
/home/node/.cache/ms-playwright
) and make sure
/home/node
is persisted via
OPENCLAW_HOME_VOLUME
or a bind mount. See
Docker
How it works (internal)
High-level flow:
A small
control server
accepts HTTP requests.
It connects to Chromium-based browsers (Chrome/Brave/Edge/Chromium) via
CDP
For advanced actions (click/type/snapshot/PDF), it uses
Playwright
on top
of CDP.
When Playwright is missing, only non-Playwright operations are available.
This design keeps the agent on a stable, deterministic interface while letting
you swap local/remote browsers and profiles.
CLI quick reference
All commands accept
--browser-profile &lt;name&gt;
to target a specific profile.
All commands also accept
--json
for machine-readable output (stable payloads).
Basics:
openclaw browser status
openclaw browser start
openclaw browser stop
openclaw browser tabs
openclaw browser tab
openclaw browser tab new
openclaw browser tab select 2
openclaw browser tab close 2
openclaw browser open https://example.com
openclaw browser focus abcd1234
openclaw browser close abcd1234
Inspection:
openclaw browser screenshot
openclaw browser screenshot --full-page
openclaw browser screenshot --ref 12
openclaw browser screenshot --ref e12
openclaw browser snapshot
openclaw browser snapshot --format aria --limit 200
openclaw browser snapshot --interactive --compact --depth 6
openclaw browser snapshot --efficient
openclaw browser snapshot --labels
openclaw browser snapshot --selector &quot;#main&quot; --interactive
openclaw browser snapshot --frame &quot;iframe#main&quot; --interactive
openclaw browser console --level error
openclaw browser errors --clear
openclaw browser requests --filter api --clear
openclaw browser pdf
openclaw browser responsebody &quot;**/api&quot; --max-chars 5000
Actions:
openclaw browser navigate https://example.com
openclaw browser resize 1280 720
openclaw browser click 12 --double
openclaw browser click e12 --double
openclaw browser type 23 &quot;hello&quot; --submit
openclaw browser press Enter
openclaw browser hover 44
openclaw browser scrollintoview e12
openclaw browser drag 10 11
openclaw browser select 9 OptionA OptionB
openclaw browser download e12 report.pdf
openclaw browser waitfordownload report.pdf
openclaw browser upload /tmp/openclaw/uploads/file.pdf
openclaw browser fill --fields &#x27;[{&quot;ref&quot;:&quot;1&quot;,&quot;type&quot;:&quot;text&quot;,&quot;value&quot;:&quot;Ada&quot;}]&#x27;
openclaw browser dialog --accept
openclaw browser wait --text &quot;Done&quot;
openclaw browser wait &quot;#main&quot; --url &quot;**/dash&quot; --load networkidle --fn &quot;window.ready===true&quot;
openclaw browser evaluate --fn &#x27;(el) =&gt; el.textContent&#x27; --ref 7
openclaw browser highlight e12
openclaw browser trace start
openclaw browser trace stop
State:
openclaw browser cookies
openclaw browser cookies set session abc123 --url &quot;https://example.com&quot;
openclaw browser cookies clear
openclaw browser storage local get
openclaw browser storage local set theme dark
openclaw browser storage session clear
openclaw browser set offline on
openclaw browser set headers --json &#x27;{&quot;X-Debug&quot;:&quot;1&quot;}&#x27;
openclaw browser set credentials user pass
openclaw browser set credentials --clear
openclaw browser set geo 37.7749 -122.4194 --origin &quot;https://example.com&quot;
openclaw browser set geo --clear
openclaw browser set media dark
openclaw browser set timezone America/New_York
openclaw browser set locale en-US
openclaw browser set device &quot;iPhone 14&quot;
Notes:
upload
and
dialog
are
arming
calls; run them before the click/press
that triggers the chooser/dialog.
Download and trace output paths are constrained to OpenClaw temp roots:
traces:
/tmp/openclaw
(fallback:
${os.tmpdir()}/openclaw
downloads:
/tmp/openclaw/downloads
(fallback:
${os.tmpdir()}/openclaw/downloads
Upload paths are constrained to an OpenClaw temp uploads root:
uploads:
/tmp/openclaw/uploads
(fallback:
${os.tmpdir()}/openclaw/uploads
upload
can also set file inputs directly via
--input-ref
--element
snapshot
--format ai
(default when Playwright is installed): returns an AI snapshot with numeric refs (
aria-ref=&quot;&lt;n&gt;&quot;
--format aria
: returns the accessibility tree (no refs; inspection only).
--efficient
(or
--mode efficient
): compact role snapshot preset (interactive + compact + depth + lower maxChars).
Config default (tool/CLI only): set
browser.snapshotDefaults.mode: &quot;efficient&quot;
to use efficient snapshots when the caller does not pass a mode (see
Gateway configuration
Role snapshot options (
--interactive
--compact
--depth
--selector
) force a role-based snapshot with refs like
ref=e12
--frame &quot;&lt;iframe selector&gt;&quot;
scopes role snapshots to an iframe (pairs with role refs like
e12
--interactive
outputs a flat, easy-to-pick list of interactive elements (best for driving actions).
--labels
adds a viewport-only screenshot with overlayed ref labels (prints
MEDIA:&lt;path&gt;
click
type
/etc require a
ref
from
snapshot
(either numeric
or role ref
e12
CSS selectors are intentionally not supported for actions.
Snapshots and refs
OpenClaw supports two “snapshot” styles:
AI snapshot (numeric refs)
openclaw browser snapshot
(default;
--format ai
Output: a text snapshot that includes numeric refs.
Actions:
openclaw browser click 12
openclaw browser type 23 &quot;hello&quot;
Internally, the ref is resolved via Playwright’s
aria-ref
Role snapshot (role refs like
e12
openclaw browser snapshot --interactive
(or
--compact
--depth
--selector
--frame
Output: a role-based list/tree with
[ref=e12]
(and optional
[nth=1]
Actions:
openclaw browser click e12
openclaw browser highlight e12
Internally, the ref is resolved via
getByRole(...)
(plus
nth()
for duplicates).
Add
--labels
to include a viewport screenshot with overlayed
e12
labels.
Ref behavior:
Refs are
not stable across navigations
; if something fails, re-run
snapshot
and use a fresh ref.
If the role snapshot was taken with
--frame
, role refs are scoped to that iframe until the next role snapshot.
Wait power-ups
You can wait on more than just time/text:
Wait for URL (globs supported by Playwright):
openclaw browser wait --url &quot;**/dash&quot;
Wait for load state:
openclaw browser wait --load networkidle
Wait for a JS predicate:
openclaw browser wait --fn &quot;window.ready===true&quot;
Wait for a selector to become visible:
openclaw browser wait &quot;#main&quot;
These can be combined:
Copy
openclaw
browser
wait
&quot;#main&quot;
--url
&quot;**/dash&quot;
--load
networkidle
--fn
&quot;window.ready===true&quot;
--timeout-ms
15000
Debug workflows
When an action fails (e.g. “not visible”, “strict mode violation”, “covered”):
openclaw browser snapshot --interactive
Use
click &lt;ref&gt;
type &lt;ref&gt;
(prefer role refs in interactive mode)
If it still fails:
openclaw browser highlight &lt;ref&gt;
to see what Playwright is targeting
If the page behaves oddly:
openclaw browser errors --clear
openclaw browser requests --filter api --clear
For deep debugging: record a trace:
openclaw browser trace start
reproduce the issue
openclaw browser trace stop
(prints
TRACE:&lt;path&gt;
JSON output
--json
is for scripting and structured tooling.
Examples:
Copy
openclaw
browser
status
--json
openclaw
browser
snapshot
--interactive
--json
openclaw
browser
requests
--filter
api
--json
openclaw
browser
cookies
--json
Role snapshots in JSON include
refs
plus a small
stats
block (lines/chars/refs/interactive) so tools can reason about payload size and density.
State and environment knobs
These are useful for “make the site behave like X” workflows:
Cookies:
cookies
cookies set
cookies clear
Storage:
storage local|session get|set|clear
Offline:
set offline on|off
Headers:
set headers --json &#x27;{&quot;X-Debug&quot;:&quot;1&quot;}&#x27;
(or
--clear
HTTP basic auth:
set credentials user pass
(or
--clear
Geolocation:
set geo &lt;lat&gt; &lt;lon&gt; --origin &quot;https://example.com&quot;
(or
--clear
Media:
set media dark|light|no-preference|none
Timezone / locale:
set timezone ...
set locale ...
Device / viewport:
set device &quot;iPhone 14&quot;
(Playwright device presets)
set viewport 1280 720
Security &amp; privacy
The openclaw browser profile may contain logged-in sessions; treat it as sensitive.
browser act kind=evaluate
openclaw browser evaluate
and
wait --fn
execute arbitrary JavaScript in the page context. Prompt injection can steer
this. Disable it with
browser.evaluateEnabled=false
if you do not need it.
For logins and anti-bot notes (X/Twitter, etc.), see
Browser login + X/Twitter posting
Keep the Gateway/node host private (loopback or tailnet-only).
Remote CDP endpoints are powerful; tunnel and protect them.
Troubleshooting
For Linux-specific issues (especially snap Chromium), see
Browser troubleshooting
Agent tools + how control works
The agent gets
one tool
for browser automation:
browser
— status/start/stop/tabs/open/focus/close/snapshot/screenshot/navigate/act
How it maps:
browser snapshot
returns a stable UI tree (AI or ARIA).
browser act
uses the snapshot
ref
IDs to click/type/drag/select.
browser screenshot
captures pixels (full page or element).
browser
accepts:
profile
to choose a named browser profile (openclaw, chrome, or remote CDP).
target
sandbox
host
node
) to select where the browser lives.
In sandboxed sessions,
target: &quot;host&quot;
requires
agents.defaults.sandbox.browser.allowHostControl=true
target
is omitted: sandboxed sessions default to
sandbox
, non-sandbox sessions default to
host
If a browser-capable node is connected, the tool may auto-route to it unless you pin
target=&quot;host&quot;
target=&quot;node&quot;
This keeps the agent deterministic and avoids brittle selectors.
Reactions
Browser Login

---
## Tools > Chrome Extension

[Source: https://docs.openclaw.ai/tools/chrome-extension]

Chrome Extension - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Browser
Chrome Extension
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
Chrome extension (browser relay)
What it is (concept)
Install / load (unpacked)
Updates (no build step)
Use it (no extra config)
Attach / detach (toolbar button)
Which tab does it control?
Badge + common errors
Remote Gateway (use a node host)
Local Gateway (same machine as Chrome) — usually no extra steps
Remote Gateway (Gateway runs elsewhere) — run a node host
Sandboxing (tool containers)
Remote access tips
How “extension path” works
Security implications (read this)
Browser
Chrome Extension
Chrome extension (browser relay)
The OpenClaw Chrome extension lets the agent control your
existing Chrome tabs
(your normal Chrome window) instead of launching a separate openclaw-managed Chrome profile.
Attach/detach happens via a
single Chrome toolbar button
What it is (concept)
There are three parts:
Browser control service
(Gateway or node): the API the agent/tool calls (via the Gateway)
Local relay server
(loopback CDP): bridges between the control server and the extension (
http://127.0.0.1:18792
by default)
Chrome MV3 extension
: attaches to the active tab using
chrome.debugger
and pipes CDP messages to the relay
OpenClaw then controls the attached tab through the normal
browser
tool surface (selecting the right profile).
Install / load (unpacked)
Install the extension to a stable local path:
Copy
openclaw
browser
extension
install
Print the installed extension directory path:
Copy
openclaw
browser
extension
path
Chrome →
chrome://extensions
Enable “Developer mode”
“Load unpacked” → select the directory printed above
Pin the extension.
Updates (no build step)
The extension ships inside the OpenClaw release (npm package) as static files. There is no separate “build” step.
After upgrading OpenClaw:
Re-run
openclaw browser extension install
to refresh the installed files under your OpenClaw state directory.
Chrome →
chrome://extensions
→ click “Reload” on the extension.
Use it (no extra config)
OpenClaw ships with a built-in browser profile named
chrome
that targets the extension relay on the default port.
Use it:
CLI:
openclaw browser --browser-profile chrome tabs
Agent tool:
browser
with
profile=&quot;chrome&quot;
If you want a different name or a different relay port, create your own profile:
Copy
openclaw
browser
create-profile
--name
my-chrome
--driver
extension
--cdp-url
http://127.0.0.1:18792
--color
&quot;#00AA00&quot;
Attach / detach (toolbar button)
Open the tab you want OpenClaw to control.
Click the extension icon.
Badge shows
when attached.
Click again to detach.
Which tab does it control?
It does
not
automatically control “whatever tab you’re looking at”.
It controls
only the tab(s) you explicitly attached
by clicking the toolbar button.
To switch: open the other tab and click the extension icon there.
Badge + common errors
: attached; OpenClaw can drive that tab.
: connecting to the local relay.
: relay not reachable (most common: browser relay server isn’t running on this machine).
If you see
Make sure the Gateway is running locally (default setup), or run a node host on this machine if the Gateway runs elsewhere.
Open the extension Options page; it shows whether the relay is reachable.
Remote Gateway (use a node host)
Local Gateway (same machine as Chrome) — usually
no extra steps
If the Gateway runs on the same machine as Chrome, it starts the browser control service on loopback
and auto-starts the relay server. The extension talks to the local relay; the CLI/tool calls go to the Gateway.
Remote Gateway (Gateway runs elsewhere) —
run a node host
If your Gateway runs on another machine, start a node host on the machine that runs Chrome.
The Gateway will proxy browser actions to that node; the extension + relay stay local to the browser machine.
If multiple nodes are connected, pin one with
gateway.nodes.browser.node
or set
gateway.nodes.browser.mode
Sandboxing (tool containers)
If your agent session is sandboxed (
agents.defaults.sandbox.mode != &quot;off&quot;
), the
browser
tool can be restricted:
By default, sandboxed sessions often target the
sandbox browser
target=&quot;sandbox&quot;
), not your host Chrome.
Chrome extension relay takeover requires controlling the
host
browser control server.
Options:
Easiest: use the extension from a
non-sandboxed
session/agent.
Or allow host browser control for sandboxed sessions:
Copy
agents
defaults
sandbox
browser
allowHostControl
true
Then ensure the tool isn’t denied by tool policy, and (if needed) call
browser
with
target=&quot;host&quot;
Debugging:
openclaw sandbox explain
Remote access tips
Keep the Gateway and node host on the same tailnet; avoid exposing relay ports to LAN or public Internet.
Pair nodes intentionally; disable browser proxy routing if you don’t want remote control (
gateway.nodes.browser.mode=&quot;off&quot;
How “extension path” works
openclaw browser extension path
prints the
installed
on-disk directory containing the extension files.
The CLI intentionally does
not
print a
node_modules
path. Always run
openclaw browser extension install
first to copy the extension to a stable location under your OpenClaw state directory.
If you move or delete that install directory, Chrome will mark the extension as broken until you reload it from a valid path.
Security implications (read this)
This is powerful and risky. Treat it like giving the model “hands on your browser”.
The extension uses Chrome’s debugger API (
chrome.debugger
). When attached, the model can:
click/type/navigate in that tab
read page content
access whatever the tab’s logged-in session can access
This is not isolated
like the dedicated openclaw-managed profile.
If you attach to your daily-driver profile/tab, you’re granting access to that account state.
Recommendations:
Prefer a dedicated Chrome profile (separate from your personal browsing) for extension relay usage.
Keep the Gateway and any node hosts tailnet-only; rely on Gateway auth + node pairing.
Avoid exposing relay ports over LAN (
0.0.0.0
) and avoid Funnel (public).
The relay blocks non-extension origins and requires an internal auth token for CDP clients.
Related:
Browser tool overview:
Browser
Security audit:
Security
Tailscale setup:
Tailscale
Browser Login
Browser Troubleshooting

---
## Tools > Clawhub

[Source: https://docs.openclaw.ai/tools/clawhub]

ClawHub - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Skills
ClawHub
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
ClawHub
What ClawHub is
How it works
What you can do
Who this is for (beginner-friendly)
Quick start (non-technical)
Install the CLI
How it fits into OpenClaw
Skill system overview
What the service provides (features)
Security and moderation
CLI commands and parameters
Common workflows for agents
Search for skills
Download new skills
Update installed skills
Back up your skills (publish or sync)
Advanced details (technical)
Versioning and tags
Local changes vs registry versions
Sync scanning and fallback roots
Storage and lockfile
Telemetry (install counts)
Environment variables
Skills
ClawHub
ClawHub
ClawHub is the
public skill registry for OpenClaw
. It is a free service: all skills are public, open, and visible to everyone for sharing and reuse. A skill is just a folder with a
SKILL.md
file (plus supporting text files). You can browse skills in the web app or use the CLI to search, install, update, and publish skills.
Site:
clawhub.ai
What ClawHub is
A public registry for OpenClaw skills.
A versioned store of skill bundles and metadata.
A discovery surface for search, tags, and usage signals.
How it works
A user publishes a skill bundle (files + metadata).
ClawHub stores the bundle, parses metadata, and assigns a version.
The registry indexes the skill for search and discovery.
Users browse, download, and install skills in OpenClaw.
What you can do
Publish new skills and new versions of existing skills.
Discover skills by name, tags, or search.
Download skill bundles and inspect their files.
Report skills that are abusive or unsafe.
If you are a moderator, hide, unhide, delete, or ban.
Who this is for (beginner-friendly)
If you want to add new capabilities to your OpenClaw agent, ClawHub is the easiest way to find and install skills. You do not need to know how the backend works. You can:
Search for skills by plain language.
Install a skill into your workspace.
Update skills later with one command.
Back up your own skills by publishing them.
Quick start (non-technical)
Install the CLI (see next section).
Search for something you need:
clawhub search &quot;calendar&quot;
Install a skill:
clawhub install &lt;skill-slug&gt;
Start a new OpenClaw session so it picks up the new skill.
Install the CLI
Pick one:
Copy
npm
clawhub
Copy
pnpm
add
clawhub
How it fits into OpenClaw
By default, the CLI installs skills into
./skills
under your current working directory. If a OpenClaw workspace is configured,
clawhub
falls back to that workspace unless you override
--workdir
(or
CLAWHUB_WORKDIR
). OpenClaw loads workspace skills from
&lt;workspace&gt;/skills
and will pick them up in the
next
session. If you already use
~/.openclaw/skills
or bundled skills, workspace skills take precedence.
For more detail on how skills are loaded, shared, and gated, see
Skills
Skill system overview
A skill is a versioned bundle of files that teaches OpenClaw how to perform a
specific task. Each publish creates a new version, and the registry keeps a
history of versions so users can audit changes.
A typical skill includes:
SKILL.md
file with the primary description and usage.
Optional configs, scripts, or supporting files used by the skill.
Metadata such as tags, summary, and install requirements.
ClawHub uses metadata to power discovery and safely expose skill capabilities.
The registry also tracks usage signals (such as stars and downloads) to improve
ranking and visibility.
What the service provides (features)
Public browsing
of skills and their
SKILL.md
content.
Search
powered by embeddings (vector search), not just keywords.
Versioning
with semver, changelogs, and tags (including
latest
Downloads
as a zip per version.
Stars and comments
for community feedback.
Moderation
hooks for approvals and audits.
CLI-friendly API
for automation and scripting.
Security and moderation
ClawHub is open by default. Anyone can upload skills, but a GitHub account must
be at least one week old to publish. This helps slow down abuse without blocking
legitimate contributors.
Reporting and moderation:
Any signed in user can report a skill.
Report reasons are required and recorded.
Each user can have up to 20 active reports at a time.
Skills with more than 3 unique reports are auto hidden by default.
Moderators can view hidden skills, unhide them, delete them, or ban users.
Abusing the report feature can result in account bans.
Interested in becoming a moderator? Ask in the OpenClaw Discord and contact a
moderator or maintainer.
CLI commands and parameters
Global options (apply to all commands):
--workdir &lt;dir&gt;
: Working directory (default: current dir; falls back to OpenClaw workspace).
--dir &lt;dir&gt;
: Skills directory, relative to workdir (default:
skills
--site &lt;url&gt;
: Site base URL (browser login).
--registry &lt;url&gt;
: Registry API base URL.
--no-input
: Disable prompts (non-interactive).
-V, --cli-version
: Print CLI version.
Auth:
clawhub login
(browser flow) or
clawhub login --token &lt;token&gt;
clawhub logout
clawhub whoami
Options:
--token &lt;token&gt;
: Paste an API token.
--label &lt;label&gt;
: Label stored for browser login tokens (default:
CLI token
--no-browser
: Do not open a browser (requires
--token
Search:
clawhub search &quot;query&quot;
--limit &lt;n&gt;
: Max results.
Install:
clawhub install &lt;slug&gt;
--version &lt;version&gt;
: Install a specific version.
--force
: Overwrite if the folder already exists.
Update:
clawhub update &lt;slug&gt;
clawhub update --all
--version &lt;version&gt;
: Update to a specific version (single slug only).
--force
: Overwrite when local files do not match any published version.
List:
clawhub list
(reads
.clawhub/lock.json
Publish:
clawhub publish &lt;path&gt;
--slug &lt;slug&gt;
: Skill slug.
--name &lt;name&gt;
: Display name.
--version &lt;version&gt;
: Semver version.
--changelog &lt;text&gt;
: Changelog text (can be empty).
--tags &lt;tags&gt;
: Comma-separated tags (default:
latest
Delete/undelete (owner/admin only):
clawhub delete &lt;slug&gt; --yes
clawhub undelete &lt;slug&gt; --yes
Sync (scan local skills + publish new/updated):
clawhub sync
--root &lt;dir...&gt;
: Extra scan roots.
--all
: Upload everything without prompts.
--dry-run
: Show what would be uploaded.
--bump &lt;type&gt;
patch|minor|major
for updates (default:
patch
--changelog &lt;text&gt;
: Changelog for non-interactive updates.
--tags &lt;tags&gt;
: Comma-separated tags (default:
latest
--concurrency &lt;n&gt;
: Registry checks (default: 4).
Common workflows for agents
Search for skills
Copy
clawhub
search
&quot;postgres backups&quot;
Download new skills
Copy
clawhub
install
my-skill-pack
Update installed skills
Copy
clawhub
update
--all
Back up your skills (publish or sync)
For a single skill folder:
Copy
clawhub
publish
./my-skill
--slug
my-skill
--name
&quot;My Skill&quot;
--version
1.0.0
--tags
latest
To scan and back up many skills at once:
Copy
clawhub
sync
--all
Advanced details (technical)
Versioning and tags
Each publish creates a new
semver
SkillVersion
Tags (like
latest
) point to a version; moving tags lets you roll back.
Changelogs are attached per version and can be empty when syncing or publishing updates.
Local changes vs registry versions
Updates compare the local skill contents to registry versions using a content hash. If local files do not match any published version, the CLI asks before overwriting (or requires
--force
in non-interactive runs).
Sync scanning and fallback roots
clawhub sync
scans your current workdir first. If no skills are found, it falls back to known legacy locations (for example
~/openclaw/skills
and
~/.openclaw/skills
). This is designed to find older skill installs without extra flags.
Storage and lockfile
Installed skills are recorded in
.clawhub/lock.json
under your workdir.
Auth tokens are stored in the ClawHub CLI config file (override via
CLAWHUB_CONFIG_PATH
Telemetry (install counts)
When you run
clawhub sync
while logged in, the CLI sends a minimal snapshot to compute install counts. You can disable this entirely:
Copy
export
CLAWHUB_DISABLE_TELEMETRY
Environment variables
CLAWHUB_SITE
: Override the site URL.
CLAWHUB_REGISTRY
: Override the registry API URL.
CLAWHUB_CONFIG_PATH
: Override where the CLI stores the token/config.
CLAWHUB_WORKDIR
: Override the default workdir.
CLAWHUB_DISABLE_TELEMETRY=1
: Disable telemetry on
sync
Skills Config
Plugins

---
## Tools > Elevated

[Source: https://docs.openclaw.ai/tools/elevated]

Elevated Mode - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Built-in tools
Elevated Mode
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
Elevated Mode (/elevated directives)
What it does
What it controls (and what it doesn’t)
Resolution order
Setting a session default
Availability + allowlists
Logging + status
Built-in tools
Elevated Mode
Elevated Mode (/elevated directives)
What it does
/elevated on
runs on the gateway host and keeps exec approvals (same as
/elevated ask
/elevated full
runs on the gateway host
and
auto-approves exec (skips exec approvals).
/elevated ask
runs on the gateway host but keeps exec approvals (same as
/elevated on
ask
not
force
exec.security=full
; configured security/ask policy still applies.
Only changes behavior when the agent is
sandboxed
(otherwise exec already runs on the host).
Directive forms:
/elevated on|off|ask|full
/elev on|off|ask|full
Only
on|off|ask|full
are accepted; anything else returns a hint and does not change state.
What it controls (and what it doesn’t)
Availability gates
tools.elevated
is the global baseline.
agents.list[].tools.elevated
can further restrict elevated per agent (both must allow).
Per-session state
/elevated on|off|ask|full
sets the elevated level for the current session key.
Inline directive
/elevated on|ask|full
inside a message applies to that message only.
Groups
: In group chats, elevated directives are only honored when the agent is mentioned. Command-only messages that bypass mention requirements are treated as mentioned.
Host execution
: elevated forces
exec
onto the gateway host;
full
also sets
security=full
Approvals
full
skips exec approvals;
ask
honor them when allowlist/ask rules require.
Unsandboxed agents
: no-op for location; only affects gating, logging, and status.
Tool policy still applies
: if
exec
is denied by tool policy, elevated cannot be used.
Separate from
/exec
/exec
adjusts per-session defaults for authorized senders and does not require elevated.
Resolution order
Inline directive on the message (applies only to that message).
Session override (set by sending a directive-only message).
Global default (
agents.defaults.elevatedDefault
in config).
Setting a session default
Send a message that is
only
the directive (whitespace allowed), e.g.
/elevated full
Confirmation reply is sent (
Elevated mode set to full...
Elevated mode disabled.
If elevated access is disabled or the sender is not on the approved allowlist, the directive replies with an actionable error and does not change session state.
Send
/elevated
(or
/elevated:
) with no argument to see the current elevated level.
Availability + allowlists
Feature gate:
tools.elevated.enabled
(default can be off via config even if the code supports it).
Sender allowlist:
tools.elevated.allowFrom
with per-provider allowlists (e.g.
discord
whatsapp
Per-agent gate:
agents.list[].tools.elevated.enabled
(optional; can only further restrict).
Per-agent allowlist:
agents.list[].tools.elevated.allowFrom
(optional; when set, the sender must match
both
global + per-agent allowlists).
Discord fallback: if
tools.elevated.allowFrom.discord
is omitted, the
channels.discord.allowFrom
list is used as a fallback (legacy:
channels.discord.dm.allowFrom
). Set
tools.elevated.allowFrom.discord
(even
) to override. Per-agent allowlists do
not
use the fallback.
All gates must pass; otherwise elevated is treated as unavailable.
Logging + status
Elevated exec calls are logged at info level.
Session status includes elevated mode (e.g.
elevated=ask
elevated=full
apply_patch Tool
Thinking Levels

---
## Tools > Exec

[Source: https://docs.openclaw.ai/tools/exec]

Exec Tool - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Built-in tools
Exec Tool
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
Exec tool
Parameters
Config
PATH handling
Session overrides (/exec)
Authorization model
Exec approvals (companion app / node host)
Allowlist + safe bins
Examples
apply_patch (experimental)
Built-in tools
Exec Tool
Exec tool
Run shell commands in the workspace. Supports foreground + background execution via
process
process
is disallowed,
exec
runs synchronously and ignores
yieldMs
background
Background sessions are scoped per agent;
process
only sees sessions from the same agent.
Parameters
command
(required)
workdir
(defaults to cwd)
env
(key/value overrides)
yieldMs
(default 10000): auto-background after delay
background
(bool): background immediately
timeout
(seconds, default 1800): kill on expiry
pty
(bool): run in a pseudo-terminal when available (TTY-only CLIs, coding agents, terminal UIs)
host
sandbox | gateway | node
): where to execute
security
deny | allowlist | full
): enforcement mode for
gateway
node
ask
off | on-miss | always
): approval prompts for
gateway
node
node
(string): node id/name for
host=node
elevated
(bool): request elevated mode (gateway host);
security=full
is only forced when elevated resolves to
full
Notes:
host
defaults to
sandbox
elevated
is ignored when sandboxing is off (exec already runs on the host).
gateway
node
approvals are controlled by
~/.openclaw/exec-approvals.json
node
requires a paired node (companion app or headless node host).
If multiple nodes are available, set
exec.node
tools.exec.node
to select one.
On non-Windows hosts, exec uses
SHELL
when set; if
SHELL
fish
, it prefers
bash
(or
from
PATH
to avoid fish-incompatible scripts, then falls back to
SHELL
if neither exists.
Host execution (
gateway
node
) rejects
env.PATH
and loader overrides (
LD_*
DYLD_*
) to
prevent binary hijacking or injected code.
Important: sandboxing is
off by default
. If sandboxing is off,
host=sandbox
runs directly on
the gateway host (no container) and
does not require approvals
. To require approvals, run with
host=gateway
and configure exec approvals (or enable sandboxing).
Config
tools.exec.notifyOnExit
(default: true): when true, backgrounded exec sessions enqueue a system event and request a heartbeat on exit.
tools.exec.approvalRunningNoticeMs
(default: 10000): emit a single “running” notice when an approval-gated exec runs longer than this (0 disables).
tools.exec.host
(default:
sandbox
tools.exec.security
(default:
deny
for sandbox,
allowlist
for gateway + node when unset)
tools.exec.ask
(default:
on-miss
tools.exec.node
(default: unset)
tools.exec.pathPrepend
: list of directories to prepend to
PATH
for exec runs (gateway + sandbox only).
tools.exec.safeBins
: stdin-only safe binaries that can run without explicit allowlist entries.
Example:
Copy
tools
exec
pathPrepend
&quot;~/bin&quot;
&quot;/opt/oss/bin&quot;
PATH handling
host=gateway
: merges your login-shell
PATH
into the exec environment.
env.PATH
overrides are
rejected for host execution. The daemon itself still runs with a minimal
PATH
macOS:
/opt/homebrew/bin
/usr/local/bin
/usr/bin
/bin
Linux:
/usr/local/bin
/usr/bin
/bin
host=sandbox
: runs
sh -lc
(login shell) inside the container, so
/etc/profile
may reset
PATH
OpenClaw prepends
env.PATH
after profile sourcing via an internal env var (no shell interpolation);
tools.exec.pathPrepend
applies here too.
host=node
: only non-blocked env overrides you pass are sent to the node.
env.PATH
overrides are
rejected for host execution and ignored by node hosts. If you need additional PATH entries on a node,
configure the node host service environment (systemd/launchd) or install tools in standard locations.
Per-agent node binding (use the agent list index in config):
Copy
openclaw
config
get
agents.list
openclaw
config
set
agents.list[0].tools.exec.node
&quot;node-id-or-name&quot;
Control UI: the Nodes tab includes a small “Exec node binding” panel for the same settings.
Session overrides (
/exec
Use
/exec
to set
per-session
defaults for
host
security
ask
, and
node
Send
/exec
with no arguments to show the current values.
Example:
Copy
/exec host=gateway security=allowlist ask=on-miss node=mac-1
Authorization model
/exec
is only honored for
authorized senders
(channel allowlists/pairing plus
commands.useAccessGroups
It updates
session state only
and does not write config. To hard-disable exec, deny it via tool
policy (
tools.deny: [&quot;exec&quot;]
or per-agent). Host approvals still apply unless you explicitly set
security=full
and
ask=off
Exec approvals (companion app / node host)
Sandboxed agents can require per-request approval before
exec
runs on the gateway or node host.
See
Exec approvals
for the policy, allowlist, and UI flow.
When approvals are required, the exec tool returns immediately with
status: &quot;approval-pending&quot;
and an approval id. Once approved (or denied / timed out),
the Gateway emits system events (
Exec finished
Exec denied
). If the command is still
running after
tools.exec.approvalRunningNoticeMs
, a single
Exec running
notice is emitted.
Allowlist + safe bins
Allowlist enforcement matches
resolved binary paths only
(no basename matches). When
security=allowlist
, shell commands are auto-allowed only if every pipeline segment is
allowlisted or a safe bin. Chaining (
&amp;&amp;
) and redirections are rejected in
allowlist mode unless every top-level segment satisfies the allowlist (including safe bins).
Redirections remain unsupported.
Examples
Foreground:
Copy
&quot;tool&quot;
&quot;exec&quot;
&quot;command&quot;
&quot;ls -la&quot;
Background + poll:
Copy
&quot;tool&quot;
&quot;exec&quot;
&quot;command&quot;
&quot;npm run build&quot;
&quot;yieldMs&quot;
1000
&quot;tool&quot;
&quot;process&quot;
&quot;action&quot;
&quot;poll&quot;
&quot;sessionId&quot;
&quot;&lt;id&gt;&quot;
Send keys (tmux-style):
Copy
&quot;tool&quot;
&quot;process&quot;
&quot;action&quot;
&quot;send-keys&quot;
&quot;sessionId&quot;
&quot;&lt;id&gt;&quot;
&quot;keys&quot;
&quot;Enter&quot;
&quot;tool&quot;
&quot;process&quot;
&quot;action&quot;
&quot;send-keys&quot;
&quot;sessionId&quot;
&quot;&lt;id&gt;&quot;
&quot;keys&quot;
&quot;C-c&quot;
&quot;tool&quot;
&quot;process&quot;
&quot;action&quot;
&quot;send-keys&quot;
&quot;sessionId&quot;
&quot;&lt;id&gt;&quot;
&quot;keys&quot;
&quot;Up&quot;
&quot;Up&quot;
&quot;Enter&quot;
Submit (send CR only):
Copy
&quot;tool&quot;
&quot;process&quot;
&quot;action&quot;
&quot;submit&quot;
&quot;sessionId&quot;
&quot;&lt;id&gt;&quot;
Paste (bracketed by default):
Copy
&quot;tool&quot;
&quot;process&quot;
&quot;action&quot;
&quot;paste&quot;
&quot;sessionId&quot;
&quot;&lt;id&gt;&quot;
&quot;text&quot;
&quot;line1\nline2\n&quot;
apply_patch (experimental)
apply_patch
is a subtool of
exec
for structured multi-file edits.
Enable it explicitly:
Copy
tools
exec
applyPatch
enabled
true
workspaceOnly
true
allowModels
&quot;gpt-5.2&quot;
] }
Notes:
Only available for OpenAI/OpenAI Codex models.
Tool policy still applies;
allow: [&quot;exec&quot;]
implicitly allows
apply_patch
Config lives under
tools.exec.applyPatch
tools.exec.applyPatch.workspaceOnly
defaults to
true
(workspace-contained). Set it to
false
only if you intentionally want
apply_patch
to write/delete outside the workspace directory.
LLM Task
Web Tools

---
## Tools > Llm Task

[Source: https://docs.openclaw.ai/tools/llm-task]

LLM Task - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Built-in tools
LLM Task
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
LLM Task
Enable the plugin
Config (optional)
Tool parameters
Output
Example: Lobster workflow step
Safety notes
Built-in tools
LLM Task
LLM Task
llm-task
is an
optional plugin tool
that runs a JSON-only LLM task and
returns structured output (optionally validated against JSON Schema).
This is ideal for workflow engines like Lobster: you can add a single LLM step
without writing custom OpenClaw code for each workflow.
Enable the plugin
Enable the plugin:
Copy
&quot;plugins&quot;
&quot;entries&quot;
&quot;llm-task&quot;
&quot;enabled&quot;
true
Allowlist the tool (it is registered with
optional: true
Copy
&quot;agents&quot;
&quot;list&quot;
&quot;id&quot;
&quot;main&quot;
&quot;tools&quot;
&quot;allow&quot;
&quot;llm-task&quot;
] }
Config (optional)
Copy
&quot;plugins&quot;
&quot;entries&quot;
&quot;llm-task&quot;
&quot;enabled&quot;
true
&quot;config&quot;
&quot;defaultProvider&quot;
&quot;openai-codex&quot;
&quot;defaultModel&quot;
&quot;gpt-5.2&quot;
&quot;defaultAuthProfileId&quot;
&quot;main&quot;
&quot;allowedModels&quot;
&quot;openai-codex/gpt-5.3-codex&quot;
&quot;maxTokens&quot;
800
&quot;timeoutMs&quot;
30000
allowedModels
is an allowlist of
provider/model
strings. If set, any request
outside the list is rejected.
Tool parameters
prompt
(string, required)
input
(any, optional)
schema
(object, optional JSON Schema)
provider
(string, optional)
model
(string, optional)
authProfileId
(string, optional)
temperature
(number, optional)
maxTokens
(number, optional)
timeoutMs
(number, optional)
Output
Returns
details.json
containing the parsed JSON (and validates against
schema
when provided).
Example: Lobster workflow step
Copy
openclaw.invoke --tool llm-task --action json --args-json &#x27;{
&quot;prompt&quot;: &quot;Given the input email, return intent and draft.&quot;,
&quot;input&quot;: {
&quot;subject&quot;: &quot;Hello&quot;,
&quot;body&quot;: &quot;Can you help?&quot;
&quot;schema&quot;: {
&quot;type&quot;: &quot;object&quot;,
&quot;properties&quot;: {
&quot;intent&quot;: { &quot;type&quot;: &quot;string&quot; },
&quot;draft&quot;: { &quot;type&quot;: &quot;string&quot; }
&quot;required&quot;: [&quot;intent&quot;, &quot;draft&quot;],
&quot;additionalProperties&quot;: false
}&#x27;
Safety notes
The tool is
JSON-only
and instructs the model to output only JSON (no
code fences, no commentary).
No tools are exposed to the model for this run.
Treat output as untrusted unless you validate with
schema
Put approvals before any side-effecting step (send, post, exec).
Lobster
Exec Tool

---
## Tools > Lobster

[Source: https://docs.openclaw.ai/tools/lobster]

Lobster - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Built-in tools
Lobster
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
Lobster
Hook
Why
Why a DSL instead of plain programs?
How it works
Pattern: small CLI + JSON pipes + approvals
JSON-only LLM steps (llm-task)
Workflow files (.lobster)
Install Lobster
Enable the tool
Example: Email triage
Tool parameters
run
resume
Optional inputs
Output envelope
Approvals
OpenProse
Safety
Troubleshooting
Learn more
Case study: community workflows
Built-in tools
Lobster
Typed workflow runtime for OpenClaw — composable pipelines with approval gates.
Lobster
Lobster is a workflow shell that lets OpenClaw run multi-step tool sequences as a single, deterministic operation with explicit approval checkpoints.
Hook
Your assistant can build the tools that manage itself. Ask for a workflow, and 30 minutes later you have a CLI plus pipelines that run as one call. Lobster is the missing piece: deterministic pipelines, explicit approvals, and resumable state.
Why
Today, complex workflows require many back-and-forth tool calls. Each call costs tokens, and the LLM has to orchestrate every step. Lobster moves that orchestration into a typed runtime:
One call instead of many
: OpenClaw runs one Lobster tool call and gets a structured result.
Approvals built in
: Side effects (send email, post comment) halt the workflow until explicitly approved.
Resumable
: Halted workflows return a token; approve and resume without re-running everything.
Why a DSL instead of plain programs?
Lobster is intentionally small. The goal is not “a new language,” it’s a predictable, AI-friendly pipeline spec with first-class approvals and resume tokens.
Approve/resume is built in
: A normal program can prompt a human, but it can’t
pause and resume
with a durable token without you inventing that runtime yourself.
Determinism + auditability
: Pipelines are data, so they’re easy to log, diff, replay, and review.
Constrained surface for AI
: A tiny grammar + JSON piping reduces “creative” code paths and makes validation realistic.
Safety policy baked in
: Timeouts, output caps, sandbox checks, and allowlists are enforced by the runtime, not each script.
Still programmable
: Each step can call any CLI or script. If you want JS/TS, generate
.lobster
files from code.
How it works
OpenClaw launches the local
lobster
CLI in
tool mode
and parses a JSON envelope from stdout.
If the pipeline pauses for approval, the tool returns a
resumeToken
so you can continue later.
Pattern: small CLI + JSON pipes + approvals
Build tiny commands that speak JSON, then chain them into a single Lobster call. (Example command names below — swap in your own.)
Copy
inbox
list
--json
inbox
categorize
--json
inbox
apply
--json
Copy
&quot;action&quot;
&quot;run&quot;
&quot;pipeline&quot;
&quot;exec --json --shell &#x27;inbox list --json&#x27; | exec --stdin json --shell &#x27;inbox categorize --json&#x27; | exec --stdin json --shell &#x27;inbox apply --json&#x27; | approve --preview-from-stdin --limit 5 --prompt &#x27;Apply changes?&#x27;&quot;
&quot;timeoutMs&quot;
30000
If the pipeline requests approval, resume with the token:
Copy
&quot;action&quot;
&quot;resume&quot;
&quot;token&quot;
&quot;&lt;resumeToken&gt;&quot;
&quot;approve&quot;
true
AI triggers the workflow; Lobster executes the steps. Approval gates keep side effects explicit and auditable.
Example: map input items into tool calls:
Copy
gog.gmail.search
--query
&#x27;newer_than:1d&#x27;
openclaw.invoke
--tool
message
--action
send
--each
--item-key
message
--args-json
&#x27;{&quot;provider&quot;:&quot;telegram&quot;,&quot;to&quot;:&quot;...&quot;}&#x27;
JSON-only LLM steps (llm-task)
For workflows that need a
structured LLM step
, enable the optional
llm-task
plugin tool and call it from Lobster. This keeps the workflow
deterministic while still letting you classify/summarize/draft with a model.
Enable the tool:
Copy
&quot;plugins&quot;
&quot;entries&quot;
&quot;llm-task&quot;
&quot;enabled&quot;
true
&quot;agents&quot;
&quot;list&quot;
&quot;id&quot;
&quot;main&quot;
&quot;tools&quot;
&quot;allow&quot;
&quot;llm-task&quot;
] }
Use it in a pipeline:
Copy
openclaw.invoke --tool llm-task --action json --args-json &#x27;{
&quot;prompt&quot;: &quot;Given the input email, return intent and draft.&quot;,
&quot;input&quot;: { &quot;subject&quot;: &quot;Hello&quot;, &quot;body&quot;: &quot;Can you help?&quot; },
&quot;schema&quot;: {
&quot;type&quot;: &quot;object&quot;,
&quot;properties&quot;: {
&quot;intent&quot;: { &quot;type&quot;: &quot;string&quot; },
&quot;draft&quot;: { &quot;type&quot;: &quot;string&quot; }
&quot;required&quot;: [&quot;intent&quot;, &quot;draft&quot;],
&quot;additionalProperties&quot;: false
}&#x27;
See
LLM Task
for details and configuration options.
Workflow files (.lobster)
Lobster can run YAML/JSON workflow files with
name
args
steps
env
condition
, and
approval
fields. In OpenClaw tool calls, set
pipeline
to the file path.
Copy
name
inbox-triage
args
tag
default
&quot;family&quot;
steps
collect
command
inbox list --json
categorize
command
inbox categorize --json
stdin
$collect.stdout
approve
command
inbox apply --approve
stdin
$categorize.stdout
approval
required
execute
command
inbox apply --execute
stdin
$categorize.stdout
condition
$approve.approved
Notes:
stdin: $step.stdout
and
stdin: $step.json
pass a prior step’s output.
condition
(or
when
) can gate steps on
$step.approved
Install Lobster
Install the Lobster CLI on the
same host
that runs the OpenClaw Gateway (see the
Lobster repo
), and ensure
lobster
is on
PATH
If you want to use a custom binary location, pass an
absolute
lobsterPath
in the tool call.
Enable the tool
Lobster is an
optional
plugin tool (not enabled by default).
Recommended (additive, safe):
Copy
&quot;tools&quot;
&quot;alsoAllow&quot;
&quot;lobster&quot;
Or per-agent:
Copy
&quot;agents&quot;
&quot;list&quot;
&quot;id&quot;
&quot;main&quot;
&quot;tools&quot;
&quot;alsoAllow&quot;
&quot;lobster&quot;
Avoid using
tools.allow: [&quot;lobster&quot;]
unless you intend to run in restrictive allowlist mode.
Note: allowlists are opt-in for optional plugins. If your allowlist only names
plugin tools (like
lobster
), OpenClaw keeps core tools enabled. To restrict core
tools, include the core tools or groups you want in the allowlist too.
Example: Email triage
Without Lobster:
Copy
User: &quot;Check my email and draft replies&quot;
→ openclaw calls gmail.list
→ LLM summarizes
→ User: &quot;draft replies to #2 and #5&quot;
→ LLM drafts
→ User: &quot;send #2&quot;
→ openclaw calls gmail.send
(repeat daily, no memory of what was triaged)
With Lobster:
Copy
&quot;action&quot;
&quot;run&quot;
&quot;pipeline&quot;
&quot;email.triage --limit 20&quot;
&quot;timeoutMs&quot;
30000
Returns a JSON envelope (truncated):
Copy
&quot;ok&quot;
true
&quot;status&quot;
&quot;needs_approval&quot;
&quot;output&quot;
&quot;summary&quot;
&quot;5 need replies, 2 need action&quot;
&quot;requiresApproval&quot;
&quot;type&quot;
&quot;approval_request&quot;
&quot;prompt&quot;
&quot;Send 2 draft replies?&quot;
&quot;items&quot;
&quot;resumeToken&quot;
&quot;...&quot;
User approves → resume:
Copy
&quot;action&quot;
&quot;resume&quot;
&quot;token&quot;
&quot;&lt;resumeToken&gt;&quot;
&quot;approve&quot;
true
One workflow. Deterministic. Safe.
Tool parameters
run
Run a pipeline in tool mode.
Copy
&quot;action&quot;
&quot;run&quot;
&quot;pipeline&quot;
&quot;gog.gmail.search --query &#x27;newer_than:1d&#x27; | email.triage&quot;
&quot;cwd&quot;
&quot;/path/to/workspace&quot;
&quot;timeoutMs&quot;
30000
&quot;maxStdoutBytes&quot;
512000
Run a workflow file with args:
Copy
&quot;action&quot;
&quot;run&quot;
&quot;pipeline&quot;
&quot;/path/to/inbox-triage.lobster&quot;
&quot;argsJson&quot;
&quot;{\&quot;tag\&quot;:\&quot;family\&quot;}&quot;
resume
Continue a halted workflow after approval.
Copy
&quot;action&quot;
&quot;resume&quot;
&quot;token&quot;
&quot;&lt;resumeToken&gt;&quot;
&quot;approve&quot;
true
Optional inputs
lobsterPath
: Absolute path to the Lobster binary (omit to use
PATH
cwd
: Working directory for the pipeline (defaults to the current process working directory).
timeoutMs
: Kill the subprocess if it exceeds this duration (default: 20000).
maxStdoutBytes
: Kill the subprocess if stdout exceeds this size (default: 512000).
argsJson
: JSON string passed to
lobster run --args-json
(workflow files only).
Output envelope
Lobster returns a JSON envelope with one of three statuses:
→ finished successfully
needs_approval
→ paused;
requiresApproval.resumeToken
is required to resume
cancelled
→ explicitly denied or cancelled
The tool surfaces the envelope in both
content
(pretty JSON) and
details
(raw object).
Approvals
requiresApproval
is present, inspect the prompt and decide:
approve: true
→ resume and continue side effects
approve: false
→ cancel and finalize the workflow
Use
approve --preview-from-stdin --limit N
to attach a JSON preview to approval requests without custom jq/heredoc glue. Resume tokens are now compact: Lobster stores workflow resume state under its state dir and hands back a small token key.
OpenProse
OpenProse pairs well with Lobster: use
/prose
to orchestrate multi-agent prep, then run a Lobster pipeline for deterministic approvals. If a Prose program needs Lobster, allow the
lobster
tool for sub-agents via
tools.subagents.tools
. See
OpenProse
Safety
Local subprocess only
— no network calls from the plugin itself.
No secrets
— Lobster doesn’t manage OAuth; it calls OpenClaw tools that do.
Sandbox-aware
— disabled when the tool context is sandboxed.
Hardened
lobsterPath
must be absolute if specified; timeouts and output caps enforced.
Troubleshooting
lobster subprocess timed out
→ increase
timeoutMs
, or split a long pipeline.
lobster output exceeded maxStdoutBytes
→ raise
maxStdoutBytes
or reduce output size.
lobster returned invalid JSON
→ ensure the pipeline runs in tool mode and prints only JSON.
lobster failed (code …)
→ run the same pipeline in a terminal to inspect stderr.
Learn more
Plugins
Plugin tool authoring
Case study: community workflows
One public example: a “second brain” CLI + Lobster pipelines that manage three Markdown vaults (personal, partner, shared). The CLI emits JSON for stats, inbox listings, and stale scans; Lobster chains those commands into workflows like
weekly-review
inbox-triage
memory-consolidation
, and
shared-task-sync
, each with approval gates. AI handles judgment (categorization) when available and falls back to deterministic rules when not.
Thread:
https://x.com/plattenschieber/status/2014508656335770033
Repo:
https://github.com/bloomedai/brain-cli
Tools
LLM Task

---
## Tools > Multi Agent Sandbox Tools

[Source: https://docs.openclaw.ai/tools/multi-agent-sandbox-tools]

Multi-Agent Sandbox &amp; Tools - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Agent coordination
Multi-Agent Sandbox &amp; Tools
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
Multi-Agent Sandbox &amp; Tools Configuration
Overview
Configuration Examples
Example 1: Personal + Restricted Family Agent
Example 2: Work Agent with Shared Sandbox
Example 2b: Global coding profile + messaging-only agent
Example 3: Different Sandbox Modes per Agent
Configuration Precedence
Sandbox Config
Tool Restrictions
Tool groups (shorthands)
Elevated Mode
Migration from Single Agent
Tool Restriction Examples
Read-only Agent
Safe Execution Agent (no file modifications)
Communication-only Agent
Common Pitfall: “non-main”
Testing
Troubleshooting
Agent not sandboxed despite mode: &quot;all&quot;
Tools still available despite deny list
Container not isolated per agent
See Also
Agent coordination
Multi-Agent Sandbox &amp; Tools
Multi-Agent Sandbox &amp; Tools Configuration
Overview
Each agent in a multi-agent setup can now have its own:
Sandbox configuration
agents.list[].sandbox
overrides
agents.defaults.sandbox
Tool restrictions
tools.allow
tools.deny
, plus
agents.list[].tools
This allows you to run multiple agents with different security profiles:
Personal assistant with full access
Family/work agents with restricted tools
Public-facing agents in sandboxes
setupCommand
belongs under
sandbox.docker
(global or per-agent) and runs once
when the container is created.
Auth is per-agent: each agent reads from its own
agentDir
auth store at:
Copy
~/.openclaw/agents/&lt;agentId&gt;/agent/auth-profiles.json
Credentials are
not
shared between agents. Never reuse
agentDir
across agents.
If you want to share creds, copy
auth-profiles.json
into the other agent’s
agentDir
For how sandboxing behaves at runtime, see
Sandboxing
For debugging “why is this blocked?”, see
Sandbox vs Tool Policy vs Elevated
and
openclaw sandbox explain
Configuration Examples
Example 1: Personal + Restricted Family Agent
Copy
&quot;agents&quot;
&quot;list&quot;
&quot;id&quot;
&quot;main&quot;
&quot;default&quot;
true
&quot;name&quot;
&quot;Personal Assistant&quot;
&quot;workspace&quot;
&quot;~/.openclaw/workspace&quot;
&quot;sandbox&quot;
&quot;mode&quot;
&quot;off&quot;
&quot;id&quot;
&quot;family&quot;
&quot;name&quot;
&quot;Family Bot&quot;
&quot;workspace&quot;
&quot;~/.openclaw/workspace-family&quot;
&quot;sandbox&quot;
&quot;mode&quot;
&quot;all&quot;
&quot;scope&quot;
&quot;agent&quot;
&quot;tools&quot;
&quot;allow&quot;
&quot;read&quot;
&quot;deny&quot;
&quot;exec&quot;
&quot;write&quot;
&quot;edit&quot;
&quot;apply_patch&quot;
&quot;process&quot;
&quot;browser&quot;
&quot;bindings&quot;
&quot;agentId&quot;
&quot;family&quot;
&quot;match&quot;
&quot;provider&quot;
&quot;whatsapp&quot;
&quot;accountId&quot;
&quot;*&quot;
&quot;peer&quot;
&quot;kind&quot;
&quot;group&quot;
&quot;id&quot;
&quot;
[email&#160;protected]
&quot;
Result:
main
agent: Runs on host, full tool access
family
agent: Runs in Docker (one container per agent), only
read
tool
Example 2: Work Agent with Shared Sandbox
Copy
&quot;agents&quot;
&quot;list&quot;
&quot;id&quot;
&quot;personal&quot;
&quot;workspace&quot;
&quot;~/.openclaw/workspace-personal&quot;
&quot;sandbox&quot;
&quot;mode&quot;
&quot;off&quot;
&quot;id&quot;
&quot;work&quot;
&quot;workspace&quot;
&quot;~/.openclaw/workspace-work&quot;
&quot;sandbox&quot;
&quot;mode&quot;
&quot;all&quot;
&quot;scope&quot;
&quot;shared&quot;
&quot;workspaceRoot&quot;
&quot;/tmp/work-sandboxes&quot;
&quot;tools&quot;
&quot;allow&quot;
&quot;read&quot;
&quot;write&quot;
&quot;apply_patch&quot;
&quot;exec&quot;
&quot;deny&quot;
&quot;browser&quot;
&quot;gateway&quot;
&quot;discord&quot;
Example 2b: Global coding profile + messaging-only agent
Copy
&quot;tools&quot;
&quot;profile&quot;
&quot;coding&quot;
&quot;agents&quot;
&quot;list&quot;
&quot;id&quot;
&quot;support&quot;
&quot;tools&quot;
&quot;profile&quot;
&quot;messaging&quot;
&quot;allow&quot;
&quot;slack&quot;
] }
Result:
default agents get coding tools
support
agent is messaging-only (+ Slack tool)
Example 3: Different Sandbox Modes per Agent
Copy
&quot;agents&quot;
&quot;defaults&quot;
&quot;sandbox&quot;
&quot;mode&quot;
&quot;non-main&quot;
// Global default
&quot;scope&quot;
&quot;session&quot;
&quot;list&quot;
&quot;id&quot;
&quot;main&quot;
&quot;workspace&quot;
&quot;~/.openclaw/workspace&quot;
&quot;sandbox&quot;
&quot;mode&quot;
&quot;off&quot;
// Override: main never sandboxed
&quot;id&quot;
&quot;public&quot;
&quot;workspace&quot;
&quot;~/.openclaw/workspace-public&quot;
&quot;sandbox&quot;
&quot;mode&quot;
&quot;all&quot;
// Override: public always sandboxed
&quot;scope&quot;
&quot;agent&quot;
&quot;tools&quot;
&quot;allow&quot;
&quot;read&quot;
&quot;deny&quot;
&quot;exec&quot;
&quot;write&quot;
&quot;edit&quot;
&quot;apply_patch&quot;
Configuration Precedence
When both global (
agents.defaults.*
) and agent-specific (
agents.list[].*
) configs exist:
Sandbox Config
Agent-specific settings override global:
Copy
agents.list[].sandbox.mode &gt; agents.defaults.sandbox.mode
agents.list[].sandbox.scope &gt; agents.defaults.sandbox.scope
agents.list[].sandbox.workspaceRoot &gt; agents.defaults.sandbox.workspaceRoot
agents.list[].sandbox.workspaceAccess &gt; agents.defaults.sandbox.workspaceAccess
agents.list[].sandbox.docker.* &gt; agents.defaults.sandbox.docker.*
agents.list[].sandbox.browser.* &gt; agents.defaults.sandbox.browser.*
agents.list[].sandbox.prune.* &gt; agents.defaults.sandbox.prune.*
Notes:
agents.list[].sandbox.{docker,browser,prune}.*
overrides
agents.defaults.sandbox.{docker,browser,prune}.*
for that agent (ignored when sandbox scope resolves to
&quot;shared&quot;
Tool Restrictions
The filtering order is:
Tool profile
tools.profile
agents.list[].tools.profile
Provider tool profile
tools.byProvider[provider].profile
agents.list[].tools.byProvider[provider].profile
Global tool policy
tools.allow
tools.deny
Provider tool policy
tools.byProvider[provider].allow/deny
Agent-specific tool policy
agents.list[].tools.allow/deny
Agent provider policy
agents.list[].tools.byProvider[provider].allow/deny
Sandbox tool policy
tools.sandbox.tools
agents.list[].tools.sandbox.tools
Subagent tool policy
tools.subagents.tools
, if applicable)
Each level can further restrict tools, but cannot grant back denied tools from earlier levels.
agents.list[].tools.sandbox.tools
is set, it replaces
tools.sandbox.tools
for that agent.
agents.list[].tools.profile
is set, it overrides
tools.profile
for that agent.
Provider tool keys accept either
provider
(e.g.
google-antigravity
) or
provider/model
(e.g.
openai/gpt-5.2
Tool groups (shorthands)
Tool policies (global, agent, sandbox) support
group:*
entries that expand to multiple concrete tools:
group:runtime
exec
bash
process
group:fs
read
write
edit
apply_patch
group:sessions
sessions_list
sessions_history
sessions_send
sessions_spawn
session_status
group:memory
memory_search
memory_get
group:ui
browser
canvas
group:automation
cron
gateway
group:messaging
message
group:nodes
nodes
group:openclaw
: all built-in OpenClaw tools (excludes provider plugins)
Elevated Mode
tools.elevated
is the global baseline (sender-based allowlist).
agents.list[].tools.elevated
can further restrict elevated for specific agents (both must allow).
Mitigation patterns:
Deny
exec
for untrusted agents (
agents.list[].tools.deny: [&quot;exec&quot;]
Avoid allowlisting senders that route to restricted agents
Disable elevated globally (
tools.elevated.enabled: false
) if you only want sandboxed execution
Disable elevated per agent (
agents.list[].tools.elevated.enabled: false
) for sensitive profiles
Migration from Single Agent
Before (single agent):
Copy
&quot;agents&quot;
&quot;defaults&quot;
&quot;workspace&quot;
&quot;~/.openclaw/workspace&quot;
&quot;sandbox&quot;
&quot;mode&quot;
&quot;non-main&quot;
&quot;tools&quot;
&quot;sandbox&quot;
&quot;tools&quot;
&quot;allow&quot;
&quot;read&quot;
&quot;write&quot;
&quot;apply_patch&quot;
&quot;exec&quot;
&quot;deny&quot;
After (multi-agent with different profiles):
Copy
&quot;agents&quot;
&quot;list&quot;
&quot;id&quot;
&quot;main&quot;
&quot;default&quot;
true
&quot;workspace&quot;
&quot;~/.openclaw/workspace&quot;
&quot;sandbox&quot;
&quot;mode&quot;
&quot;off&quot;
Legacy
agent.*
configs are migrated by
openclaw doctor
; prefer
agents.defaults
agents.list
going forward.
Tool Restriction Examples
Read-only Agent
Copy
&quot;tools&quot;
&quot;allow&quot;
&quot;read&quot;
&quot;deny&quot;
&quot;exec&quot;
&quot;write&quot;
&quot;edit&quot;
&quot;apply_patch&quot;
&quot;process&quot;
Safe Execution Agent (no file modifications)
Copy
&quot;tools&quot;
&quot;allow&quot;
&quot;read&quot;
&quot;exec&quot;
&quot;process&quot;
&quot;deny&quot;
&quot;write&quot;
&quot;edit&quot;
&quot;apply_patch&quot;
&quot;browser&quot;
&quot;gateway&quot;
Communication-only Agent
Copy
&quot;tools&quot;
&quot;sessions&quot;
&quot;visibility&quot;
&quot;tree&quot;
&quot;allow&quot;
&quot;sessions_list&quot;
&quot;sessions_send&quot;
&quot;sessions_history&quot;
&quot;session_status&quot;
&quot;deny&quot;
&quot;exec&quot;
&quot;write&quot;
&quot;edit&quot;
&quot;apply_patch&quot;
&quot;read&quot;
&quot;browser&quot;
Common Pitfall: “non-main”
agents.defaults.sandbox.mode: &quot;non-main&quot;
is based on
session.mainKey
(default
&quot;main&quot;
not the agent id. Group/channel sessions always get their own keys, so they
are treated as non-main and will be sandboxed. If you want an agent to never
sandbox, set
agents.list[].sandbox.mode: &quot;off&quot;
Testing
After configuring multi-agent sandbox and tools:
Check agent resolution:
Copy
openclaw agents list --bindings
Verify sandbox containers:
Copy
docker ps --filter &quot;name=openclaw-sbx-&quot;
Test tool restrictions:
Send a message requiring restricted tools
Verify the agent cannot use denied tools
Monitor logs:
Copy
tail -f &quot;${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/logs/gateway.log&quot; | grep -E &quot;routing|sandbox|tools&quot;
Troubleshooting
Agent not sandboxed despite
mode: &quot;all&quot;
Check if there’s a global
agents.defaults.sandbox.mode
that overrides it
Agent-specific config takes precedence, so set
agents.list[].sandbox.mode: &quot;all&quot;
Tools still available despite deny list
Check tool filtering order: global → agent → sandbox → subagent
Each level can only further restrict, not grant back
Verify with logs:
[tools] filtering tools for agent:${agentId}
Container not isolated per agent
Set
scope: &quot;agent&quot;
in agent-specific sandbox config
Default is
&quot;session&quot;
which creates one container per session
See Also
Multi-Agent Routing
Sandbox Configuration
Session Management
Sub-Agents
Slash Commands

---
## Tools > Plugin

[Source: https://docs.openclaw.ai/tools/plugin]

Plugins - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Skills
Plugins
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
Plugins (Extensions)
Quick start (new to plugins?)
Available plugins (official)
Runtime helpers
Discovery &amp; precedence
Package packs
Channel catalog metadata
Plugin IDs
Config
Plugin slots (exclusive categories)
Control UI (schema + labels)
CLI
Plugin API (overview)
Plugin hooks
Example
Provider plugins (model auth)
Register a messaging channel
Write a new messaging channel (step‑by‑step)
Agent tools
Register a gateway RPC method
Register CLI commands
Register auto-reply commands
Register background services
Naming conventions
Skills
Distribution (npm)
Example plugin: Voice Call
Safety notes
Testing plugins
Skills
Plugins
Plugins (Extensions)
Quick start (new to plugins?)
A plugin is just a
small code module
that extends OpenClaw with extra
features (commands, tools, and Gateway RPC).
Most of the time, you’ll use plugins when you want a feature that’s not built
into core OpenClaw yet (or you want to keep optional features out of your main
install).
Fast path:
See what’s already loaded:
Copy
openclaw
plugins
list
Install an official plugin (example: Voice Call):
Copy
openclaw
plugins
install
@openclaw/voice-call
Npm specs are
registry-only
(package name + optional version/tag). Git/URL/file
specs are rejected.
Restart the Gateway, then configure under
plugins.entries.&lt;id&gt;.config
See
Voice Call
for a concrete example plugin.
Available plugins (official)
Microsoft Teams is plugin-only as of 2026.1.15; install
@openclaw/msteams
if you use Teams.
Memory (Core) — bundled memory search plugin (enabled by default via
plugins.slots.memory
Memory (LanceDB) — bundled long-term memory plugin (auto-recall/capture; set
plugins.slots.memory = &quot;memory-lancedb&quot;
Voice Call
@openclaw/voice-call
Zalo Personal
@openclaw/zalouser
Matrix
@openclaw/matrix
Nostr
@openclaw/nostr
Zalo
@openclaw/zalo
Microsoft Teams
@openclaw/msteams
Google Antigravity OAuth (provider auth) — bundled as
google-antigravity-auth
(disabled by default)
Gemini CLI OAuth (provider auth) — bundled as
google-gemini-cli-auth
(disabled by default)
Qwen OAuth (provider auth) — bundled as
qwen-portal-auth
(disabled by default)
Copilot Proxy (provider auth) — local VS Code Copilot Proxy bridge; distinct from built-in
github-copilot
device login (bundled, disabled by default)
OpenClaw plugins are
TypeScript modules
loaded at runtime via jiti.
Config
validation does not execute plugin code
; it uses the plugin manifest and JSON
Schema instead. See
Plugin manifest
Plugins can register:
Gateway RPC methods
Gateway HTTP handlers
Agent tools
CLI commands
Background services
Optional config validation
Skills
(by listing
skills
directories in the plugin manifest)
Auto-reply commands
(execute without invoking the AI agent)
Plugins run
in‑process
with the Gateway, so treat them as trusted code.
Tool authoring guide:
Plugin agent tools
Runtime helpers
Plugins can access selected core helpers via
api.runtime
. For telephony TTS:
Copy
const
result
await
api
runtime
tts
.textToSpeechTelephony
text
&quot;Hello from OpenClaw&quot;
cfg
api
.config
});
Notes:
Uses core
messages.tts
configuration (OpenAI or ElevenLabs).
Returns PCM audio buffer + sample rate. Plugins must resample/encode for providers.
Edge TTS is not supported for telephony.
Discovery &amp; precedence
OpenClaw scans, in order:
Config paths
plugins.load.paths
(file or directory)
Workspace extensions
&lt;workspace&gt;/.openclaw/extensions/*.ts
&lt;workspace&gt;/.openclaw/extensions/*/index.ts
Global extensions
~/.openclaw/extensions/*.ts
~/.openclaw/extensions/*/index.ts
Bundled extensions (shipped with OpenClaw,
disabled by default
&lt;openclaw&gt;/extensions/*
Bundled plugins must be enabled explicitly via
plugins.entries.&lt;id&gt;.enabled
openclaw plugins enable &lt;id&gt;
. Installed plugins are enabled by default,
but can be disabled the same way.
Each plugin must include a
openclaw.plugin.json
file in its root. If a path
points at a file, the plugin root is the file’s directory and must contain the
manifest.
If multiple plugins resolve to the same id, the first match in the order above
wins and lower-precedence copies are ignored.
Package packs
A plugin directory may include a
package.json
with
openclaw.extensions
Copy
&quot;name&quot;
&quot;my-pack&quot;
&quot;openclaw&quot;
&quot;extensions&quot;
&quot;./src/safety.ts&quot;
&quot;./src/tools.ts&quot;
Each entry becomes a plugin. If the pack lists multiple extensions, the plugin id
becomes
name/&lt;fileBase&gt;
If your plugin imports npm deps, install them in that directory so
node_modules
is available (
npm install
pnpm install
Security note:
openclaw plugins install
installs plugin dependencies with
npm install --ignore-scripts
(no lifecycle scripts). Keep plugin dependency
trees “pure JS/TS” and avoid packages that require
postinstall
builds.
Channel catalog metadata
Channel plugins can advertise onboarding metadata via
openclaw.channel
and
install hints via
openclaw.install
. This keeps the core catalog data-free.
Example:
Copy
&quot;name&quot;
&quot;@openclaw/nextcloud-talk&quot;
&quot;openclaw&quot;
&quot;extensions&quot;
&quot;./index.ts&quot;
&quot;channel&quot;
&quot;id&quot;
&quot;nextcloud-talk&quot;
&quot;label&quot;
&quot;Nextcloud Talk&quot;
&quot;selectionLabel&quot;
&quot;Nextcloud Talk (self-hosted)&quot;
&quot;docsPath&quot;
&quot;/channels/nextcloud-talk&quot;
&quot;docsLabel&quot;
&quot;nextcloud-talk&quot;
&quot;blurb&quot;
&quot;Self-hosted chat via Nextcloud Talk webhook bots.&quot;
&quot;order&quot;
&quot;aliases&quot;
&quot;nc-talk&quot;
&quot;nc&quot;
&quot;install&quot;
&quot;npmSpec&quot;
&quot;@openclaw/nextcloud-talk&quot;
&quot;localPath&quot;
&quot;extensions/nextcloud-talk&quot;
&quot;defaultChoice&quot;
&quot;npm&quot;
OpenClaw can also merge
external channel catalogs
(for example, an MPM
registry export). Drop a JSON file at one of:
~/.openclaw/mpm/plugins.json
~/.openclaw/mpm/catalog.json
~/.openclaw/plugins/catalog.json
Or point
OPENCLAW_PLUGIN_CATALOG_PATHS
(or
OPENCLAW_MPM_CATALOG_PATHS
) at
one or more JSON files (comma/semicolon/
PATH
-delimited). Each file should
contain
{ &quot;entries&quot;: [ { &quot;name&quot;: &quot;@scope/pkg&quot;, &quot;openclaw&quot;: { &quot;channel&quot;: {...}, &quot;install&quot;: {...} } } ] }
Plugin IDs
Default plugin ids:
Package packs:
package.json
name
Standalone file: file base name (
~/.../voice-call.ts
voice-call
If a plugin exports
, OpenClaw uses it but warns when it doesn’t match the
configured id.
Config
Copy
plugins
enabled
true
allow
&quot;voice-call&quot;
deny
&quot;untrusted-plugin&quot;
load
paths
&quot;~/Projects/oss/voice-call-extension&quot;
] }
entries
&quot;voice-call&quot;
enabled
true
config
provider
&quot;twilio&quot;
} }
Fields:
enabled
: master toggle (default: true)
allow
: allowlist (optional)
deny
: denylist (optional; deny wins)
load.paths
: extra plugin files/dirs
entries.&lt;id&gt;
: per‑plugin toggles + config
Config changes
require a gateway restart
Validation rules (strict):
Unknown plugin ids in
entries
allow
deny
, or
slots
are
errors
Unknown
channels.&lt;id&gt;
keys are
errors
unless a plugin manifest declares
the channel id.
Plugin config is validated using the JSON Schema embedded in
openclaw.plugin.json
configSchema
If a plugin is disabled, its config is preserved and a
warning
is emitted.
Plugin slots (exclusive categories)
Some plugin categories are
exclusive
(only one active at a time). Use
plugins.slots
to select which plugin owns the slot:
Copy
plugins
slots
memory
&quot;memory-core&quot;
// or &quot;none&quot; to disable memory plugins
If multiple plugins declare
kind: &quot;memory&quot;
, only the selected one loads. Others
are disabled with diagnostics.
Control UI (schema + labels)
The Control UI uses
config.schema
(JSON Schema +
uiHints
) to render better forms.
OpenClaw augments
uiHints
at runtime based on discovered plugins:
Adds per-plugin labels for
plugins.entries.&lt;id&gt;
.enabled
.config
Merges optional plugin-provided config field hints under:
plugins.entries.&lt;id&gt;.config.&lt;field&gt;
If you want your plugin config fields to show good labels/placeholders (and mark secrets as sensitive),
provide
uiHints
alongside your JSON Schema in the plugin manifest.
Example:
Copy
&quot;id&quot;
&quot;my-plugin&quot;
&quot;configSchema&quot;
&quot;type&quot;
&quot;object&quot;
&quot;additionalProperties&quot;
false
&quot;properties&quot;
&quot;apiKey&quot;
&quot;type&quot;
&quot;string&quot;
&quot;region&quot;
&quot;type&quot;
&quot;string&quot;
&quot;uiHints&quot;
&quot;apiKey&quot;
&quot;label&quot;
&quot;API Key&quot;
&quot;sensitive&quot;
true
&quot;region&quot;
&quot;label&quot;
&quot;Region&quot;
&quot;placeholder&quot;
&quot;us-east-1&quot;
CLI
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
install
&lt;
pat
&gt;
# copy a local file/dir into ~/.openclaw/extensions/&lt;id&gt;
openclaw
plugins
install
./extensions/voice-call
# relative path ok
openclaw
plugins
install
./plugin.tgz
# install from a local tarball
openclaw
plugins
install
./plugin.zip
# install from a local zip
openclaw
plugins
install
./extensions/voice-call
# link (no copy) for dev
openclaw
plugins
install
@openclaw/voice-call
# install from npm
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
doctor
plugins update
only works for npm installs tracked under
plugins.installs
Plugins may also register their own top‑level commands (example:
openclaw voicecall
Plugin API (overview)
Plugins export either:
A function:
(api) =&gt; { ... }
An object:
{ id, name, configSchema, register(api) { ... } }
Plugin hooks
Plugins can ship hooks and register them at runtime. This lets a plugin bundle
event-driven automation without a separate hook pack install.
Example
Copy
import { registerPluginHooksFromDir } from &quot;openclaw/plugin-sdk&quot;;
export default function register(api) {
registerPluginHooksFromDir(api, &quot;./hooks&quot;);
Notes:
Hook directories follow the normal hook structure (
HOOK.md
handler.ts
Hook eligibility rules still apply (OS/bins/env/config requirements).
Plugin-managed hooks show up in
openclaw hooks list
with
plugin:&lt;id&gt;
You cannot enable/disable plugin-managed hooks via
openclaw hooks
; enable/disable the plugin instead.
Provider plugins (model auth)
Plugins can register
model provider auth
flows so users can run OAuth or
API-key setup inside OpenClaw (no external scripts needed).
Register a provider via
api.registerProvider(...)
. Each provider exposes one
or more auth methods (OAuth, API key, device code, etc.). These methods power:
openclaw models auth login --provider &lt;id&gt; [--method &lt;id&gt;]
Example:
Copy
api
.registerProvider
&quot;acme&quot;
label
&quot;AcmeAI&quot;
auth
&quot;oauth&quot;
label
&quot;OAuth&quot;
kind
&quot;oauth&quot;
run
async
(ctx)
=&gt;
// Run OAuth flow and return auth profiles.
return
profiles
profileId
&quot;acme:default&quot;
credential
type
&quot;oauth&quot;
provider
&quot;acme&quot;
access
&quot;...&quot;
refresh
&quot;...&quot;
expires
Date
.now
3600
1000
defaultModel
&quot;acme/opus-1&quot;
});
Notes:
run
receives a
ProviderAuthContext
with
prompter
runtime
openUrl
, and
oauth.createVpsAwareHandlers
helpers.
Return
configPatch
when you need to add default models or provider config.
Return
defaultModel
--set-default
can update agent defaults.
Register a messaging channel
Plugins can register
channel plugins
that behave like built‑in channels
(WhatsApp, Telegram, etc.). Channel config lives under
channels.&lt;id&gt;
and is
validated by your channel plugin code.
Copy
const
myChannel
&quot;acmechat&quot;
meta
&quot;acmechat&quot;
label
&quot;AcmeChat&quot;
selectionLabel
&quot;AcmeChat (API)&quot;
docsPath
&quot;/channels/acmechat&quot;
blurb
&quot;demo channel plugin.&quot;
aliases
&quot;acme&quot;
capabilities
{ chatTypes
&quot;direct&quot;
] }
config
listAccountIds
(cfg)
=&gt;
Object
.keys
cfg
channels
acmechat
?.accounts
{})
resolveAccount
(cfg
accountId)
=&gt;
cfg
channels
acmechat
?.accounts?.[accountId
&quot;default&quot;
accountId
outbound
deliveryMode
&quot;direct&quot;
sendText
async
=&gt;
({ ok
true
export
default
function
(api) {
api
.registerChannel
({ plugin
myChannel });
Notes:
Put config under
channels.&lt;id&gt;
(not
plugins.entries
meta.label
is used for labels in CLI/UI lists.
meta.aliases
adds alternate ids for normalization and CLI inputs.
meta.preferOver
lists channel ids to skip auto-enable when both are configured.
meta.detailLabel
and
meta.systemImage
let UIs show richer channel labels/icons.
Write a new messaging channel (step‑by‑step)
Use this when you want a
new chat surface
(a “messaging channel”), not a model provider.
Model provider docs live under
/providers/*
Pick an id + config shape
All channel config lives under
channels.&lt;id&gt;
Prefer
channels.&lt;id&gt;.accounts.&lt;accountId&gt;
for multi‑account setups.
Define the channel metadata
meta.label
meta.selectionLabel
meta.docsPath
meta.blurb
control CLI/UI lists.
meta.docsPath
should point at a docs page like
/channels/&lt;id&gt;
meta.preferOver
lets a plugin replace another channel (auto-enable prefers it).
meta.detailLabel
and
meta.systemImage
are used by UIs for detail text/icons.
Implement the required adapters
config.listAccountIds
config.resolveAccount
capabilities
(chat types, media, threads, etc.)
outbound.deliveryMode
outbound.sendText
(for basic send)
Add optional adapters as needed
setup
(wizard),
security
(DM policy),
status
(health/diagnostics)
gateway
(start/stop/login),
mentions
threading
streaming
actions
(message actions),
commands
(native command behavior)
Register the channel in your plugin
api.registerChannel({ plugin })
Minimal config example:
Copy
channels
acmechat
accounts
default
token
&quot;ACME_TOKEN&quot;
enabled
true
Minimal channel plugin (outbound‑only):
Copy
const
plugin
&quot;acmechat&quot;
meta
&quot;acmechat&quot;
label
&quot;AcmeChat&quot;
selectionLabel
&quot;AcmeChat (API)&quot;
docsPath
&quot;/channels/acmechat&quot;
blurb
&quot;AcmeChat messaging channel.&quot;
aliases
&quot;acme&quot;
capabilities
{ chatTypes
&quot;direct&quot;
] }
config
listAccountIds
(cfg)
=&gt;
Object
.keys
cfg
channels
acmechat
?.accounts
{})
resolveAccount
(cfg
accountId)
=&gt;
cfg
channels
acmechat
?.accounts?.[accountId
&quot;default&quot;
accountId
outbound
deliveryMode
&quot;direct&quot;
sendText
async
({ text })
=&gt;
// deliver `text` to your channel here
return
{ ok
true
export
default
function
(api) {
api
.registerChannel
({ plugin });
Load the plugin (extensions dir or
plugins.load.paths
), restart the gateway,
then configure
channels.&lt;id&gt;
in your config.
Agent tools
See the dedicated guide:
Plugin agent tools
Register a gateway RPC method
Copy
export
default
function
(api) {
api
.registerGatewayMethod
&quot;myplugin.status&quot;
({ respond })
=&gt;
respond
true
{ ok
true
});
});
Register CLI commands
Copy
export
default
function
(api) {
api
.registerCli
({ program })
=&gt;
program
.command
&quot;mycmd&quot;
.action
(()
=&gt;
console
.log
&quot;Hello&quot;
});
{ commands
&quot;mycmd&quot;
] }
Register auto-reply commands
Plugins can register custom slash commands that execute
without invoking the
AI agent
. This is useful for toggle commands, status checks, or quick actions
that don’t need LLM processing.
Copy
export
default
function
(api) {
api
.registerCommand
name
&quot;mystatus&quot;
description
&quot;Show plugin status&quot;
handler
(ctx)
=&gt;
text
`Plugin is running! Channel:
ctx
.channel
});
Command handler context:
senderId
: The sender’s ID (if available)
channel
: The channel where the command was sent
isAuthorizedSender
: Whether the sender is an authorized user
args
: Arguments passed after the command (if
acceptsArgs: true
commandBody
: The full command text
config
: The current OpenClaw config
Command options:
name
: Command name (without the leading
description
: Help text shown in command lists
acceptsArgs
: Whether the command accepts arguments (default: false). If false and arguments are provided, the command won’t match and the message falls through to other handlers
requireAuth
: Whether to require authorized sender (default: true)
handler
: Function that returns
{ text: string }
(can be async)
Example with authorization and arguments:
Copy
api
.registerCommand
name
&quot;setmode&quot;
description
&quot;Set plugin mode&quot;
acceptsArgs
true
requireAuth
true
handler
async
(ctx)
=&gt;
const
mode
ctx
args
?.trim
&quot;default&quot;
await
saveMode
(mode);
return
{ text
`Mode set to:
mode
});
Notes:
Plugin commands are processed
before
built-in commands and the AI agent
Commands are registered globally and work across all channels
Command names are case-insensitive (
/MyStatus
matches
/mystatus
Command names must start with a letter and contain only letters, numbers, hyphens, and underscores
Reserved command names (like
help
status
reset
, etc.) cannot be overridden by plugins
Duplicate command registration across plugins will fail with a diagnostic error
Register background services
Copy
export
default
function
(api) {
api
.registerService
&quot;my-service&quot;
start
=&gt;
api
logger
.info
&quot;ready&quot;
stop
=&gt;
api
logger
.info
&quot;bye&quot;
});
Naming conventions
Gateway methods:
pluginId.action
(example:
voicecall.status
Tools:
snake_case
(example:
voice_call
CLI commands: kebab or camel, but avoid clashing with core commands
Skills
Plugins can ship a skill in the repo (
skills/&lt;name&gt;/SKILL.md
Enable it with
plugins.entries.&lt;id&gt;.enabled
(or other config gates) and ensure
it’s present in your workspace/managed skills locations.
Distribution (npm)
Recommended packaging:
Main package:
openclaw
(this repo)
Plugins: separate npm packages under
@openclaw/*
(example:
@openclaw/voice-call
Publishing contract:
Plugin
package.json
must include
openclaw.extensions
with one or more entry files.
Entry files can be
.js
.ts
(jiti loads TS at runtime).
openclaw plugins install &lt;npm-spec&gt;
uses
npm pack
, extracts into
~/.openclaw/extensions/&lt;id&gt;/
, and enables it in config.
Config key stability: scoped packages are normalized to the
unscoped
id for
plugins.entries.*
Example plugin: Voice Call
This repo includes a voice‑call plugin (Twilio or log fallback):
Source:
extensions/voice-call
Skill:
skills/voice-call
CLI:
openclaw voicecall start|status
Tool:
voice_call
RPC:
voicecall.start
voicecall.status
Config (twilio):
provider: &quot;twilio&quot;
twilio.accountSid/authToken/from
(optional
statusCallbackUrl
twimlUrl
Config (dev):
provider: &quot;log&quot;
(no network)
See
Voice Call
and
extensions/voice-call/README.md
for setup and usage.
Safety notes
Plugins run in-process with the Gateway. Treat them as trusted code:
Only install plugins you trust.
Prefer
plugins.allow
allowlists.
Restart the Gateway after changes.
Testing plugins
Plugins can (and should) ship tests:
In-repo plugins can keep Vitest tests under
src/**
(example:
src/plugins/voice-call.plugin.test.ts
Separately published plugins should run their own CI (lint/build/test) and validate
openclaw.extensions
points at the built entrypoint (
dist/index.js
ClawHub
Voice Call Plugin

---
## Tools > Reactions

[Source: https://docs.openclaw.ai/tools/reactions]

Reactions - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Built-in tools
Reactions
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
Reaction tooling
Built-in tools
Reactions
Reaction tooling
Shared reaction semantics across channels:
emoji
is required when adding a reaction.
emoji=&quot;&quot;
removes the bot’s reaction(s) when supported.
remove: true
removes the specified emoji when supported (requires
emoji
Channel notes:
Discord/Slack
: empty
emoji
removes all of the bot’s reactions on the message;
remove: true
removes just that emoji.
Google Chat
: empty
emoji
removes the app’s reactions on the message;
remove: true
removes just that emoji.
Telegram
: empty
emoji
removes the bot’s reactions;
remove: true
also removes reactions but still requires a non-empty
emoji
for tool validation.
WhatsApp
: empty
emoji
removes the bot reaction;
remove: true
maps to empty emoji (still requires
emoji
Signal
: inbound reaction notifications emit system events when
channels.signal.reactionNotifications
is enabled.
Thinking Levels
Browser (OpenClaw-managed)

---
## Tools > Skills Config

[Source: https://docs.openclaw.ai/tools/skills-config]

Skills Config - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Skills
Skills Config
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
Skills Config
Fields
Notes
Sandboxed skills + env vars
Skills
Skills Config
Skills Config
All skills-related configuration lives under
skills
~/.openclaw/openclaw.json
Copy
skills
allowBundled
&quot;gemini&quot;
&quot;peekaboo&quot;
load
extraDirs
&quot;~/Projects/agent-scripts/skills&quot;
&quot;~/Projects/oss/some-skill-pack/skills&quot;
watch
true
watchDebounceMs
250
install
preferBrew
true
nodeManager
&quot;npm&quot;
// npm | pnpm | yarn | bun (Gateway runtime still Node; bun not recommended)
entries
&quot;nano-banana-pro&quot;
enabled
true
apiKey
&quot;GEMINI_KEY_HERE&quot;
env
GEMINI_API_KEY
&quot;GEMINI_KEY_HERE&quot;
peekaboo
enabled
true
sag
enabled
false
Fields
allowBundled
: optional allowlist for
bundled
skills only. When set, only
bundled skills in the list are eligible (managed/workspace skills unaffected).
load.extraDirs
: additional skill directories to scan (lowest precedence).
load.watch
: watch skill folders and refresh the skills snapshot (default: true).
load.watchDebounceMs
: debounce for skill watcher events in milliseconds (default: 250).
install.preferBrew
: prefer brew installers when available (default: true).
install.nodeManager
: node installer preference (
npm
pnpm
yarn
bun
, default: npm).
This only affects
skill installs
; the Gateway runtime should still be Node
(Bun not recommended for WhatsApp/Telegram).
entries.&lt;skillKey&gt;
: per-skill overrides.
Per-skill fields:
enabled
: set
false
to disable a skill even if it’s bundled/installed.
env
: environment variables injected for the agent run (only if not already set).
apiKey
: optional convenience for skills that declare a primary env var.
Notes
Keys under
entries
map to the skill name by default. If a skill defines
metadata.openclaw.skillKey
, use that key instead.
Changes to skills are picked up on the next agent turn when the watcher is enabled.
Sandboxed skills + env vars
When a session is
sandboxed
, skill processes run inside Docker. The sandbox
does
not
inherit the host
process.env
Use one of:
agents.defaults.sandbox.docker.env
(or per-agent
agents.list[].sandbox.docker.env
bake the env into your custom sandbox image
Global
env
and
skills.entries.&lt;skill&gt;.env/apiKey
apply to
host
runs only.
Skills
ClawHub

---
## Tools > Skills

[Source: https://docs.openclaw.ai/tools/skills]

Skills - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Skills
Skills
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
Skills (OpenClaw)
Locations and precedence
Per-agent vs shared skills
Plugins + skills
ClawHub (install + sync)
Security notes
Format (AgentSkills + Pi-compatible)
Gating (load-time filters)
Config overrides (~/.openclaw/openclaw.json)
Environment injection (per agent run)
Session snapshot (performance)
Remote macOS nodes (Linux gateway)
Skills watcher (auto-refresh)
Token impact (skills list)
Managed skills lifecycle
Config reference
Looking for more skills?
Skills
Skills
Skills (OpenClaw)
OpenClaw uses
AgentSkills
-compatible
skill folders to teach the agent how to use tools. Each skill is a directory containing a
SKILL.md
with YAML frontmatter and instructions. OpenClaw loads
bundled skills
plus optional local overrides, and filters them at load time based on environment, config, and binary presence.
Locations and precedence
Skills are loaded from
three
places:
Bundled skills
: shipped with the install (npm package or OpenClaw.app)
Managed/local skills
~/.openclaw/skills
Workspace skills
&lt;workspace&gt;/skills
If a skill name conflicts, precedence is:
&lt;workspace&gt;/skills
(highest) →
~/.openclaw/skills
→ bundled skills (lowest)
Additionally, you can configure extra skill folders (lowest precedence) via
skills.load.extraDirs
~/.openclaw/openclaw.json
Per-agent vs shared skills
multi-agent
setups, each agent has its own workspace. That means:
Per-agent skills
live in
&lt;workspace&gt;/skills
for that agent only.
Shared skills
live in
~/.openclaw/skills
(managed/local) and are visible
all agents
on the same machine.
Shared folders
can also be added via
skills.load.extraDirs
(lowest
precedence) if you want a common skills pack used by multiple agents.
If the same skill name exists in more than one place, the usual precedence
applies: workspace wins, then managed/local, then bundled.
Plugins + skills
Plugins can ship their own skills by listing
skills
directories in
openclaw.plugin.json
(paths relative to the plugin root). Plugin skills load
when the plugin is enabled and participate in the normal skill precedence rules.
You can gate them via
metadata.openclaw.requires.config
on the plugin’s config
entry. See
Plugins
for discovery/config and
Tools
for the
tool surface those skills teach.
ClawHub (install + sync)
ClawHub is the public skills registry for OpenClaw. Browse at
https://clawhub.com
. Use it to discover, install, update, and back up skills.
Full guide:
ClawHub
Common flows:
Install a skill into your workspace:
clawhub install &lt;skill-slug&gt;
Update all installed skills:
clawhub update --all
Sync (scan + publish updates):
clawhub sync --all
By default,
clawhub
installs into
./skills
under your current working
directory (or falls back to the configured OpenClaw workspace). OpenClaw picks
that up as
&lt;workspace&gt;/skills
on the next session.
Security notes
Treat third-party skills as
untrusted code
. Read them before enabling.
Prefer sandboxed runs for untrusted inputs and risky tools. See
Sandboxing
skills.entries.*.env
and
skills.entries.*.apiKey
inject secrets into the
host
process
for that agent turn (not the sandbox). Keep secrets out of prompts and logs.
For a broader threat model and checklists, see
Security
Format (AgentSkills + Pi-compatible)
SKILL.md
must include at least:
Copy
---
name
nano-banana-pro
description
Generate or edit images via Gemini 3 Pro Image
---
Notes:
We follow the AgentSkills spec for layout/intent.
The parser used by the embedded agent supports
single-line
frontmatter keys only.
metadata
should be a
single-line JSON object
Use
{baseDir}
in instructions to reference the skill folder path.
Optional frontmatter keys:
homepage
— URL surfaced as “Website” in the macOS Skills UI (also supported via
metadata.openclaw.homepage
user-invocable
true|false
(default:
true
). When
true
, the skill is exposed as a user slash command.
disable-model-invocation
true|false
(default:
false
). When
true
, the skill is excluded from the model prompt (still available via user invocation).
command-dispatch
tool
(optional). When set to
tool
, the slash command bypasses the model and dispatches directly to a tool.
command-tool
— tool name to invoke when
command-dispatch: tool
is set.
command-arg-mode
raw
(default). For tool dispatch, forwards the raw args string to the tool (no core parsing).
The tool is invoked with params:
{ command: &quot;&lt;raw args&gt;&quot;, commandName: &quot;&lt;slash command&gt;&quot;, skillName: &quot;&lt;skill name&gt;&quot; }
Gating (load-time filters)
OpenClaw
filters skills at load time
using
metadata
(single-line JSON):
Copy
---
name
nano-banana-pro
description
Generate or edit images via Gemini 3 Pro Image
metadata
&quot;openclaw&quot;
&quot;requires&quot;
&quot;bins&quot;
&quot;uv&quot;
&quot;env&quot;
&quot;GEMINI_API_KEY&quot;
&quot;config&quot;
&quot;browser.enabled&quot;
] }
&quot;primaryEnv&quot;
&quot;GEMINI_API_KEY&quot;
---
Fields under
metadata.openclaw
always: true
— always include the skill (skip other gates).
emoji
— optional emoji used by the macOS Skills UI.
homepage
— optional URL shown as “Website” in the macOS Skills UI.
— optional list of platforms (
darwin
linux
win32
). If set, the skill is only eligible on those OSes.
requires.bins
— list; each must exist on
PATH
requires.anyBins
— list; at least one must exist on
PATH
requires.env
— list; env var must exist
be provided in config.
requires.config
— list of
openclaw.json
paths that must be truthy.
primaryEnv
— env var name associated with
skills.entries.&lt;name&gt;.apiKey
install
— optional array of installer specs used by the macOS Skills UI (brew/node/go/uv/download).
Note on sandboxing:
requires.bins
is checked on the
host
at skill load time.
If an agent is sandboxed, the binary must also exist
inside the container
Install it via
agents.defaults.sandbox.docker.setupCommand
(or a custom image).
setupCommand
runs once after the container is created.
Package installs also require network egress, a writable root FS, and a root user in the sandbox.
Example: the
summarize
skill (
skills/summarize/SKILL.md
) needs the
summarize
CLI
in the sandbox container to run there.
Installer example:
Copy
---
name
gemini
description
Use Gemini CLI for coding assistance and Google search lookups.
metadata
&quot;openclaw&quot;
&quot;emoji&quot;
&quot;♊️&quot;
&quot;requires&quot;
&quot;bins&quot;
&quot;gemini&quot;
] }
&quot;install&quot;
&quot;id&quot;
&quot;brew&quot;
&quot;kind&quot;
&quot;brew&quot;
&quot;formula&quot;
&quot;gemini-cli&quot;
&quot;bins&quot;
&quot;gemini&quot;
&quot;label&quot;
&quot;Install Gemini CLI (brew)&quot;
---
Notes:
If multiple installers are listed, the gateway picks a
single
preferred option (brew when available, otherwise node).
If all installers are
download
, OpenClaw lists each entry so you can see the available artifacts.
Installer specs can include
os: [&quot;darwin&quot;|&quot;linux&quot;|&quot;win32&quot;]
to filter options by platform.
Node installs honor
skills.install.nodeManager
openclaw.json
(default: npm; options: npm/pnpm/yarn/bun).
This only affects
skill installs
; the Gateway runtime should still be Node
(Bun is not recommended for WhatsApp/Telegram).
Go installs: if
is missing and
brew
is available, the gateway installs Go via Homebrew first and sets
GOBIN
to Homebrew’s
bin
when possible.
Download installs:
url
(required),
archive
tar.gz
tar.bz2
zip
extract
(default: auto when archive detected),
stripComponents
targetDir
(default:
~/.openclaw/tools/&lt;skillKey&gt;
If no
metadata.openclaw
is present, the skill is always eligible (unless
disabled in config or blocked by
skills.allowBundled
for bundled skills).
Config overrides (
~/.openclaw/openclaw.json
Bundled/managed skills can be toggled and supplied with env values:
Copy
skills
entries
&quot;nano-banana-pro&quot;
enabled
true
apiKey
&quot;GEMINI_KEY_HERE&quot;
env
GEMINI_API_KEY
&quot;GEMINI_KEY_HERE&quot;
config
endpoint
&quot;https://example.invalid&quot;
model
&quot;nano-pro&quot;
peekaboo
enabled
true
sag
enabled
false
Note: if the skill name contains hyphens, quote the key (JSON5 allows quoted keys).
Config keys match the
skill name
by default. If a skill defines
metadata.openclaw.skillKey
, use that key under
skills.entries
Rules:
enabled: false
disables the skill even if it’s bundled/installed.
env
: injected
only if
the variable isn’t already set in the process.
apiKey
: convenience for skills that declare
metadata.openclaw.primaryEnv
config
: optional bag for custom per-skill fields; custom keys must live here.
allowBundled
: optional allowlist for
bundled
skills only. If set, only
bundled skills in the list are eligible (managed/workspace skills unaffected).
Environment injection (per agent run)
When an agent run starts, OpenClaw:
Reads skill metadata.
Applies any
skills.entries.&lt;key&gt;.env
skills.entries.&lt;key&gt;.apiKey
process.env
Builds the system prompt with
eligible
skills.
Restores the original environment after the run ends.
This is
scoped to the agent run
, not a global shell environment.
Session snapshot (performance)
OpenClaw snapshots the eligible skills
when a session starts
and reuses that list for subsequent turns in the same session. Changes to skills or config take effect on the next new session.
Skills can also refresh mid-session when the skills watcher is enabled or when a new eligible remote node appears (see below). Think of this as a
hot reload
: the refreshed list is picked up on the next agent turn.
Remote macOS nodes (Linux gateway)
If the Gateway is running on Linux but a
macOS node
is connected
with
system.run
allowed
(Exec approvals security not set to
deny
), OpenClaw can treat macOS-only skills as eligible when the required binaries are present on that node. The agent should execute those skills via the
nodes
tool (typically
nodes.run
This relies on the node reporting its command support and on a bin probe via
system.run
. If the macOS node goes offline later, the skills remain visible; invocations may fail until the node reconnects.
Skills watcher (auto-refresh)
By default, OpenClaw watches skill folders and bumps the skills snapshot when
SKILL.md
files change. Configure this under
skills.load
Copy
skills
load
watch
true
watchDebounceMs
250
Token impact (skills list)
When skills are eligible, OpenClaw injects a compact XML list of available skills into the system prompt (via
formatSkillsForPrompt
pi-coding-agent
). The cost is deterministic:
Base overhead (only when ≥1 skill):
195 characters.
Per skill:
97 characters + the length of the XML-escaped
&lt;name&gt;
&lt;description&gt;
, and
&lt;location&gt;
values.
Formula (characters):
Copy
total = 195 + Σ (97 + len(name_escaped) + len(description_escaped) + len(location_escaped))
Notes:
XML escaping expands
&amp; &lt; &gt; &quot; &#x27;
into entities (
&amp;amp;
&amp;lt;
, etc.), increasing length.
Token counts vary by model tokenizer. A rough OpenAI-style estimate is ~4 chars/token, so
97 chars ≈ 24 tokens
per skill plus your actual field lengths.
Managed skills lifecycle
OpenClaw ships a baseline set of skills as
bundled skills
as part of the
install (npm package or OpenClaw.app).
~/.openclaw/skills
exists for local
overrides (for example, pinning/patching a skill without changing the bundled
copy). Workspace skills are user-owned and override both on name conflicts.
Config reference
See
Skills config
for the full configuration schema.
Looking for more skills?
Browse
https://clawhub.com
Slash Commands
Skills Config

---
## Tools > Slash Commands

[Source: https://docs.openclaw.ai/tools/slash-commands]

Slash Commands - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Skills
Slash Commands
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
Slash commands
Config
Command list
Usage surfaces (what shows where)
Model selection (/model)
Debug overrides
Config updates
Surface notes
Skills
Slash Commands
Slash commands
Commands are handled by the Gateway. Most commands must be sent as a
standalone
message that starts with
The host-only bash chat command uses
! &lt;cmd&gt;
(with
/bash &lt;cmd&gt;
as an alias).
There are two related systems:
Commands
: standalone
/...
messages.
Directives
/think
/verbose
/reasoning
/elevated
/exec
/model
/queue
Directives are stripped from the message before the model sees it.
In normal chat messages (not directive-only), they are treated as “inline hints” and do
not
persist session settings.
In directive-only messages (the message contains only directives), they persist to the session and reply with an acknowledgement.
Directives are only applied for
authorized senders
. If
commands.allowFrom
is set, it is the only
allowlist used; otherwise authorization comes from channel allowlists/pairing plus
commands.useAccessGroups
Unauthorized senders see directives treated as plain text.
There are also a few
inline shortcuts
(allowlisted/authorized senders only):
/help
/commands
/status
/whoami
/id
They run immediately, are stripped before the model sees the message, and the remaining text continues through the normal flow.
Config
Copy
commands
native
&quot;auto&quot;
nativeSkills
&quot;auto&quot;
text
true
bash
false
bashForegroundMs
2000
config
false
debug
false
restart
false
allowFrom
&quot;*&quot;
&quot;user1&quot;
discord
&quot;user:123&quot;
useAccessGroups
true
commands.text
(default
true
) enables parsing
/...
in chat messages.
On surfaces without native commands (WhatsApp/WebChat/Signal/iMessage/Google Chat/MS Teams), text commands still work even if you set this to
false
commands.native
(default
&quot;auto&quot;
) registers native commands.
Auto: on for Discord/Telegram; off for Slack (until you add slash commands); ignored for providers without native support.
Set
channels.discord.commands.native
channels.telegram.commands.native
, or
channels.slack.commands.native
to override per provider (bool or
&quot;auto&quot;
false
clears previously registered commands on Discord/Telegram at startup. Slack commands are managed in the Slack app and are not removed automatically.
commands.nativeSkills
(default
&quot;auto&quot;
) registers
skill
commands natively when supported.
Auto: on for Discord/Telegram; off for Slack (Slack requires creating a slash command per skill).
Set
channels.discord.commands.nativeSkills
channels.telegram.commands.nativeSkills
, or
channels.slack.commands.nativeSkills
to override per provider (bool or
&quot;auto&quot;
commands.bash
(default
false
) enables
! &lt;cmd&gt;
to run host shell commands (
/bash &lt;cmd&gt;
is an alias; requires
tools.elevated
allowlists).
commands.bashForegroundMs
(default
2000
) controls how long bash waits before switching to background mode (
backgrounds immediately).
commands.config
(default
false
) enables
/config
(reads/writes
openclaw.json
commands.debug
(default
false
) enables
/debug
(runtime-only overrides).
commands.allowFrom
(optional) sets a per-provider allowlist for command authorization. When configured, it is the
only authorization source for commands and directives (channel allowlists/pairing and
commands.useAccessGroups
are ignored). Use
&quot;*&quot;
for a global default; provider-specific keys override it.
commands.useAccessGroups
(default
true
) enforces allowlists/policies for commands when
commands.allowFrom
is not set.
Command list
Text + native (when enabled):
/help
/commands
/skill &lt;name&gt; [input]
(run a skill by name)
/status
(show current status; includes provider usage/quota for the current model provider when available)
/allowlist
(list/add/remove allowlist entries)
/approve &lt;id&gt; allow-once|allow-always|deny
(resolve exec approval prompts)
/context [list|detail|json]
(explain “context”;
detail
shows per-file + per-tool + per-skill + system prompt size)
/whoami
(show your sender id; alias:
/id
/subagents list|kill|log|info|send|steer
(inspect, kill, log, or steer sub-agent runs for the current session)
/kill &lt;id|#|all&gt;
(immediately abort one or all running sub-agents for this session; no confirmation message)
/steer &lt;id|#&gt; &lt;message&gt;
(steer a running sub-agent immediately: in-run when possible, otherwise abort current work and restart on the steer message)
/tell &lt;id|#&gt; &lt;message&gt;
(alias for
/steer
/config show|get|set|unset
(persist config to disk, owner-only; requires
commands.config: true
/debug show|set|unset|reset
(runtime overrides, owner-only; requires
commands.debug: true
/usage off|tokens|full|cost
(per-response usage footer or local cost summary)
/tts off|always|inbound|tagged|status|provider|limit|summary|audio
(control TTS; see
/tts
Discord: native command is
/voice
(Discord reserves
/tts
); text
/tts
still works.
/stop
/restart
/dock-telegram
(alias:
/dock_telegram
) (switch replies to Telegram)
/dock-discord
(alias:
/dock_discord
) (switch replies to Discord)
/dock-slack
(alias:
/dock_slack
) (switch replies to Slack)
/activation mention|always
(groups only)
/send on|off|inherit
(owner-only)
/reset
/new [model]
(optional model hint; remainder is passed through)
/think &lt;off|minimal|low|medium|high|xhigh&gt;
(dynamic choices by model/provider; aliases:
/thinking
/verbose on|full|off
(alias:
/reasoning on|off|stream
(alias:
/reason
; when on, sends a separate message prefixed
Reasoning:
stream
= Telegram draft only)
/elevated on|off|ask|full
(alias:
/elev
full
skips exec approvals)
/exec host=&lt;sandbox|gateway|node&gt; security=&lt;deny|allowlist|full&gt; ask=&lt;off|on-miss|always&gt; node=&lt;id&gt;
(send
/exec
to show current)
/model &lt;name&gt;
(alias:
/models
; or
/&lt;alias&gt;
from
agents.defaults.models.*.alias
/queue &lt;mode&gt;
(plus options like
debounce:2s cap:25 drop:summarize
; send
/queue
to see current settings)
/bash &lt;command&gt;
(host-only; alias for
! &lt;command&gt;
; requires
commands.bash: true
tools.elevated
allowlists)
Text-only:
/compact [instructions]
(see
/concepts/compaction
! &lt;command&gt;
(host-only; one at a time; use
!poll
!stop
for long-running jobs)
!poll
(check output / status; accepts optional
sessionId
/bash poll
also works)
!stop
(stop the running bash job; accepts optional
sessionId
/bash stop
also works)
Notes:
Commands accept an optional
between the command and args (e.g.
/think: high
/send: on
/help:
/new &lt;model&gt;
accepts a model alias,
provider/model
, or a provider name (fuzzy match); if no match, the text is treated as the message body.
For full provider usage breakdown, use
openclaw status --usage
/allowlist add|remove
requires
commands.config=true
and honors channel
configWrites
/usage
controls the per-response usage footer;
/usage cost
prints a local cost summary from OpenClaw session logs.
/restart
is disabled by default; set
commands.restart: true
to enable it.
/verbose
is meant for debugging and extra visibility; keep it
off
in normal use.
/reasoning
(and
/verbose
) are risky in group settings: they may reveal internal reasoning or tool output you did not intend to expose. Prefer leaving them off, especially in group chats.
Fast path:
command-only messages from allowlisted senders are handled immediately (bypass queue + model).
Group mention gating:
command-only messages from allowlisted senders bypass mention requirements.
Inline shortcuts (allowlisted senders only):
certain commands also work when embedded in a normal message and are stripped before the model sees the remaining text.
Example:
hey /status
triggers a status reply, and the remaining text continues through the normal flow.
Currently:
/help
/commands
/status
/whoami
/id
Unauthorized command-only messages are silently ignored, and inline
/...
tokens are treated as plain text.
Skill commands:
user-invocable
skills are exposed as slash commands. Names are sanitized to
a-z0-9_
(max 32 chars); collisions get numeric suffixes (e.g.
/skill &lt;name&gt; [input]
runs a skill by name (useful when native command limits prevent per-skill commands).
By default, skill commands are forwarded to the model as a normal request.
Skills may optionally declare
command-dispatch: tool
to route the command directly to a tool (deterministic, no model).
Example:
/prose
(OpenProse plugin) — see
OpenProse
Native command arguments:
Discord uses autocomplete for dynamic options (and button menus when you omit required args). Telegram and Slack show a button menu when a command supports choices and you omit the arg.
Usage surfaces (what shows where)
Provider usage/quota
(example: “Claude 80% left”) shows up in
/status
for the current model provider when usage tracking is enabled.
Per-response tokens/cost
is controlled by
/usage off|tokens|full
(appended to normal replies).
/model status
is about
models/auth/endpoints
, not usage.
Model selection (
/model
/model
is implemented as a directive.
Examples:
Copy
/model
/model list
/model 3
/model openai/gpt-5.2
/model opus@anthropic:default
/model status
Notes:
/model
and
/model list
show a compact, numbered picker (model family + available providers).
/model &lt;#&gt;
selects from that picker (and prefers the current provider when possible).
/model status
shows the detailed view, including configured provider endpoint (
baseUrl
) and API mode (
api
) when available.
Debug overrides
/debug
lets you set
runtime-only
config overrides (memory, not disk). Owner-only. Disabled by default; enable with
commands.debug: true
Examples:
Copy
/debug show
/debug set messages.responsePrefix=&quot;[openclaw]&quot;
/debug set channels.whatsapp.allowFrom=[&quot;+1555&quot;,&quot;+4477&quot;]
/debug unset messages.responsePrefix
/debug reset
Notes:
Overrides apply immediately to new config reads, but do
not
write to
openclaw.json
Use
/debug reset
to clear all overrides and return to the on-disk config.
Config updates
/config
writes to your on-disk config (
openclaw.json
). Owner-only. Disabled by default; enable with
commands.config: true
Examples:
Copy
/config show
/config show messages.responsePrefix
/config get messages.responsePrefix
/config set messages.responsePrefix=&quot;[openclaw]&quot;
/config unset messages.responsePrefix
Notes:
Config is validated before write; invalid changes are rejected.
/config
updates persist across restarts.
Surface notes
Text commands
run in the normal chat session (DMs share
main
, groups have their own session).
Native commands
use isolated sessions:
Discord:
agent:&lt;agentId&gt;:discord:slash:&lt;userId&gt;
Slack:
agent:&lt;agentId&gt;:slack:slash:&lt;userId&gt;
(prefix configurable via
channels.slack.slashCommand.sessionPrefix
Telegram:
telegram:slash:&lt;userId&gt;
(targets the chat session via
CommandTargetSessionKey
/stop
targets the active chat session so it can abort the current run.
Slack:
channels.slack.slashCommand
is still supported for a single
/openclaw
-style command. If you enable
commands.native
, you must create one Slack slash command per built-in command (same names as
/help
). Command argument menus for Slack are delivered as ephemeral Block Kit buttons.
Multi-Agent Sandbox &amp; Tools
Skills

---
## Tools > Subagents

[Source: https://docs.openclaw.ai/tools/subagents]

Sub-Agents - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Agent coordination
Sub-Agents
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
Sub-agents
Slash command
Tool
Nested Sub-Agents
How to enable
Depth levels
Announce chain
Tool policy by depth
Per-agent spawn limit
Cascade stop
Authentication
Announce
Tool Policy (sub-agent tools)
Concurrency
Stopping
Limitations
Agent coordination
Sub-Agents
Sub-agents
Sub-agents are background agent runs spawned from an existing agent run. They run in their own session (
agent:&lt;agentId&gt;:subagent:&lt;uuid&gt;
) and, when finished,
announce
their result back to the requester chat channel.
Slash command
Use
/subagents
to inspect or control sub-agent runs for the
current session
/subagents list
/subagents kill &lt;id|#|all&gt;
/subagents log &lt;id|#&gt; [limit] [tools]
/subagents info &lt;id|#&gt;
/subagents send &lt;id|#&gt; &lt;message&gt;
/subagents info
shows run metadata (status, timestamps, session id, transcript path, cleanup).
Primary goals:
Parallelize “research / long task / slow tool” work without blocking the main run.
Keep sub-agents isolated by default (session separation + optional sandboxing).
Keep the tool surface hard to misuse: sub-agents do
not
get session tools by default.
Support configurable nesting depth for orchestrator patterns.
Cost note: each sub-agent has its
own
context and token usage. For heavy or repetitive
tasks, set a cheaper model for sub-agents and keep your main agent on a higher-quality model.
You can configure this via
agents.defaults.subagents.model
or per-agent overrides.
Tool
Use
sessions_spawn
Starts a sub-agent run (
deliver: false
, global lane:
subagent
Then runs an announce step and posts the announce reply to the requester chat channel
Default model: inherits the caller unless you set
agents.defaults.subagents.model
(or per-agent
agents.list[].subagents.model
); an explicit
sessions_spawn.model
still wins.
Default thinking: inherits the caller unless you set
agents.defaults.subagents.thinking
(or per-agent
agents.list[].subagents.thinking
); an explicit
sessions_spawn.thinking
still wins.
Tool params:
task
(required)
label?
(optional)
agentId?
(optional; spawn under another agent id if allowed)
model?
(optional; overrides the sub-agent model; invalid values are skipped and the sub-agent runs on the default model with a warning in the tool result)
thinking?
(optional; overrides thinking level for the sub-agent run)
runTimeoutSeconds?
(default
; when set, the sub-agent run is aborted after N seconds)
cleanup?
delete|keep
, default
keep
Allowlist:
agents.list[].subagents.allowAgents
: list of agent ids that can be targeted via
agentId
[&quot;*&quot;]
to allow any). Default: only the requester agent.
Discovery:
Use
agents_list
to see which agent ids are currently allowed for
sessions_spawn
Auto-archive:
Sub-agent sessions are automatically archived after
agents.defaults.subagents.archiveAfterMinutes
(default: 60).
Archive uses
sessions.delete
and renames the transcript to
*.deleted.&lt;timestamp&gt;
(same folder).
cleanup: &quot;delete&quot;
archives immediately after announce (still keeps the transcript via rename).
Auto-archive is best-effort; pending timers are lost if the gateway restarts.
runTimeoutSeconds
does
not
auto-archive; it only stops the run. The session remains until auto-archive.
Auto-archive applies equally to depth-1 and depth-2 sessions.
Nested Sub-Agents
By default, sub-agents cannot spawn their own sub-agents (
maxSpawnDepth: 1
). You can enable one level of nesting by setting
maxSpawnDepth: 2
, which allows the
orchestrator pattern
: main → orchestrator sub-agent → worker sub-sub-agents.
How to enable
Copy
agents
defaults
subagents
maxSpawnDepth
// allow sub-agents to spawn children (default: 1)
maxChildrenPerAgent
// max active children per agent session (default: 5)
maxConcurrent
// global concurrency lane cap (default: 8)
Depth levels
Depth
Session key shape
Role
Can spawn?
agent:&lt;id&gt;:main
Main agent
Always
agent:&lt;id&gt;:subagent:&lt;uuid&gt;
Sub-agent (orchestrator when depth 2 allowed)
Only if
maxSpawnDepth &gt;= 2
agent:&lt;id&gt;:subagent:&lt;uuid&gt;:subagent:&lt;uuid&gt;
Sub-sub-agent (leaf worker)
Never
Announce chain
Results flow back up the chain:
Depth-2 worker finishes → announces to its parent (depth-1 orchestrator)
Depth-1 orchestrator receives the announce, synthesizes results, finishes → announces to main
Main agent receives the announce and delivers to the user
Each level only sees announces from its direct children.
Tool policy by depth
Depth 1 (orchestrator, when
maxSpawnDepth &gt;= 2
: Gets
sessions_spawn
subagents
sessions_list
sessions_history
so it can manage its children. Other session/system tools remain denied.
Depth 1 (leaf, when
maxSpawnDepth == 1
: No session tools (current default behavior).
Depth 2 (leaf worker)
: No session tools —
sessions_spawn
is always denied at depth 2. Cannot spawn further children.
Per-agent spawn limit
Each agent session (at any depth) can have at most
maxChildrenPerAgent
(default: 5) active children at a time. This prevents runaway fan-out from a single orchestrator.
Cascade stop
Stopping a depth-1 orchestrator automatically stops all its depth-2 children:
/stop
in the main chat stops all depth-1 agents and cascades to their depth-2 children.
/subagents kill &lt;id&gt;
stops a specific sub-agent and cascades to its children.
/subagents kill all
stops all sub-agents for the requester and cascades.
Authentication
Sub-agent auth is resolved by
agent id
, not by session type:
The sub-agent session key is
agent:&lt;agentId&gt;:subagent:&lt;uuid&gt;
The auth store is loaded from that agent’s
agentDir
The main agent’s auth profiles are merged in as a
fallback
; agent profiles override main profiles on conflicts.
Note: the merge is additive, so main profiles are always available as fallbacks. Fully isolated auth per agent is not supported yet.
Announce
Sub-agents report back via an announce step:
The announce step runs inside the sub-agent session (not the requester session).
If the sub-agent replies exactly
ANNOUNCE_SKIP
, nothing is posted.
Otherwise the announce reply is posted to the requester chat channel via a follow-up
agent
call (
deliver=true
Announce replies preserve thread/topic routing when available (Slack threads, Telegram topics, Matrix threads).
Announce messages are normalized to a stable template:
Status:
derived from the run outcome (
success
error
timeout
, or
unknown
Result:
the summary content from the announce step (or
(not available)
if missing).
Notes:
error details and other useful context.
Status
is not inferred from model output; it comes from runtime outcome signals.
Announce payloads include a stats line at the end (even when wrapped):
Runtime (e.g.,
runtime 5m12s
Token usage (input/output/total)
Estimated cost when model pricing is configured (
models.providers.*.models[].cost
sessionKey
sessionId
, and transcript path (so the main agent can fetch history via
sessions_history
or inspect the file on disk)
Tool Policy (sub-agent tools)
By default, sub-agents get
all tools except session tools
and system tools:
sessions_list
sessions_history
sessions_send
sessions_spawn
When
maxSpawnDepth &gt;= 2
, depth-1 orchestrator sub-agents additionally receive
sessions_spawn
subagents
sessions_list
, and
sessions_history
so they can manage their children.
Override via config:
Copy
agents
defaults
subagents
maxConcurrent
tools
subagents
tools
// deny wins
deny
&quot;gateway&quot;
&quot;cron&quot;
// if allow is set, it becomes allow-only (deny still wins)
// allow: [&quot;read&quot;, &quot;exec&quot;, &quot;process&quot;]
Concurrency
Sub-agents use a dedicated in-process queue lane:
Lane name:
subagent
Concurrency:
agents.defaults.subagents.maxConcurrent
(default
Stopping
Sending
/stop
in the requester chat aborts the requester session and stops any active sub-agent runs spawned from it, cascading to nested children.
/subagents kill &lt;id&gt;
stops a specific sub-agent and cascades to its children.
Limitations
Sub-agent announce is
best-effort
. If the gateway restarts, pending “announce back” work is lost.
Sub-agents still share the same gateway process resources; treat
maxConcurrent
as a safety valve.
sessions_spawn
is always non-blocking: it returns
{ status: &quot;accepted&quot;, runId, childSessionKey }
immediately.
Sub-agent context only injects
AGENTS.md
TOOLS.md
(no
SOUL.md
IDENTITY.md
USER.md
HEARTBEAT.md
, or
BOOTSTRAP.md
Maximum nesting depth is 5 (
maxSpawnDepth
range: 1–5). Depth 2 is recommended for most use cases.
maxChildrenPerAgent
caps active children per session (default: 5, range: 1–20).
Agent Send
Multi-Agent Sandbox &amp; Tools

---
## Tools > Thinking

[Source: https://docs.openclaw.ai/tools/thinking]

Thinking Levels - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Built-in tools
Thinking Levels
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
Thinking Levels (/think directives)
What it does
Resolution order
Setting a session default
Application by agent
Verbose directives (/verbose or /v)
Reasoning visibility (/reasoning)
Related
Heartbeats
Web chat UI
Built-in tools
Thinking Levels
Thinking Levels (/think directives)
What it does
Inline directive in any inbound body:
/t &lt;level&gt;
/think:&lt;level&gt;
, or
/thinking &lt;level&gt;
Levels (aliases):
off | minimal | low | medium | high | xhigh
(GPT-5.2 + Codex models only)
minimal → “think”
low → “think hard”
medium → “think harder”
high → “ultrathink” (max budget)
xhigh → “ultrathink+” (GPT-5.2 + Codex models only)
x-high
x_high
extra-high
extra high
, and
extra_high
map to
xhigh
highest
max
map to
high
Provider notes:
Z.AI (
zai/*
) only supports binary thinking (
off
). Any non-
off
level is treated as
(mapped to
low
Resolution order
Inline directive on the message (applies only to that message).
Session override (set by sending a directive-only message).
Global default (
agents.defaults.thinkingDefault
in config).
Fallback: low for reasoning-capable models; off otherwise.
Setting a session default
Send a message that is
only
the directive (whitespace allowed), e.g.
/think:medium
/t high
That sticks for the current session (per-sender by default); cleared by
/think:off
or session idle reset.
Confirmation reply is sent (
Thinking level set to high.
Thinking disabled.
). If the level is invalid (e.g.
/thinking big
), the command is rejected with a hint and the session state is left unchanged.
Send
/think
(or
/think:
) with no argument to see the current thinking level.
Application by agent
Embedded Pi
: the resolved level is passed to the in-process Pi agent runtime.
Verbose directives (/verbose or /v)
Levels:
(minimal) |
full
off
(default).
Directive-only message toggles session verbose and replies
Verbose logging enabled.
Verbose logging disabled.
; invalid levels return a hint without changing state.
/verbose off
stores an explicit session override; clear it via the Sessions UI by choosing
inherit
Inline directive affects only that message; session/global defaults apply otherwise.
Send
/verbose
(or
/verbose:
) with no argument to see the current verbose level.
When verbose is on, agents that emit structured tool results (Pi, other JSON agents) send each tool call back as its own metadata-only message, prefixed with
&lt;emoji&gt; &lt;tool-name&gt;: &lt;arg&gt;
when available (path/command). These tool summaries are sent as soon as each tool starts (separate bubbles), not as streaming deltas.
When verbose is
full
, tool outputs are also forwarded after completion (separate bubble, truncated to a safe length). If you toggle
/verbose on|full|off
while a run is in-flight, subsequent tool bubbles honor the new setting.
Reasoning visibility (/reasoning)
Levels:
on|off|stream
Directive-only message toggles whether thinking blocks are shown in replies.
When enabled, reasoning is sent as a
separate message
prefixed with
Reasoning:
stream
(Telegram only): streams reasoning into the Telegram draft bubble while the reply is generating, then sends the final answer without reasoning.
Alias:
/reason
Send
/reasoning
(or
/reasoning:
) with no argument to see the current reasoning level.
Related
Elevated mode docs live in
Elevated mode
Heartbeats
Heartbeat probe body is the configured heartbeat prompt (default:
Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK.
). Inline directives in a heartbeat message apply as usual (but avoid changing session defaults from heartbeats).
Heartbeat delivery defaults to the final payload only. To also send the separate
Reasoning:
message (when available), set
agents.defaults.heartbeat.includeReasoning: true
or per-agent
agents.list[].heartbeat.includeReasoning: true
Web chat UI
The web chat thinking selector mirrors the session’s stored level from the inbound session store/config when the page loads.
Picking another level applies only to the next message (
thinkingOnce
); after sending, the selector snaps back to the stored session level.
To change the session default, send a
/think:&lt;level&gt;
directive (as before); the selector will reflect it after the next reload.
Elevated Mode
Reactions

---
## Tools > Web

[Source: https://docs.openclaw.ai/tools/web]

Web Tools - OpenClaw
OpenClaw
home page
English
GitHub
Releases
Built-in tools
Web Tools
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
Web tools
How it works
Choosing a search provider
Getting a Brave API key
Where to set the key (recommended)
Using Perplexity (direct or via OpenRouter)
Getting an OpenRouter API key
Setting up Perplexity search
Available Perplexity models
web_search
Requirements
Config
Tool parameters
web_fetch
web_fetch requirements
web_fetch config
web_fetch tool parameters
Built-in tools
Web Tools
Web tools
OpenClaw ships two lightweight web tools:
web_search
— Search the web via Brave Search API (default) or Perplexity Sonar (direct or via OpenRouter).
web_fetch
— HTTP fetch + readable extraction (HTML → markdown/text).
These are
not
browser automation. For JS-heavy sites or logins, use the
Browser tool
How it works
web_search
calls your configured provider and returns results.
Brave
(default): returns structured results (title, URL, snippet).
Perplexity
: returns AI-synthesized answers with citations from real-time web search.
Results are cached by query for 15 minutes (configurable).
web_fetch
does a plain HTTP GET and extracts readable content
(HTML → markdown/text). It does
not
execute JavaScript.
web_fetch
is enabled by default (unless explicitly disabled).
Choosing a search provider
Provider
Pros
Cons
API Key
Brave
(default)
Fast, structured results, free tier
Traditional search results
BRAVE_API_KEY
Perplexity
AI-synthesized answers, citations, real-time
Requires Perplexity or OpenRouter access
OPENROUTER_API_KEY
PERPLEXITY_API_KEY
See
Brave Search setup
and
Perplexity Sonar
for provider-specific details.
Set the provider in config:
Copy
tools
web
search
provider
&quot;brave&quot;
// or &quot;perplexity&quot;
Example: switch to Perplexity Sonar (direct API):
Copy
tools
web
search
provider
&quot;perplexity&quot;
perplexity
apiKey
&quot;pplx-...&quot;
baseUrl
&quot;https://api.perplexity.ai&quot;
model
&quot;perplexity/sonar-pro&quot;
Getting a Brave API key
Create a Brave Search API account at
https://brave.com/search/api/
In the dashboard, choose the
Data for Search
plan (not “Data for AI”) and generate an API key.
Run
openclaw configure --section web
to store the key in config (recommended), or set
BRAVE_API_KEY
in your environment.
Brave provides a free tier plus paid plans; check the Brave API portal for the
current limits and pricing.
Where to set the key (recommended)
Recommended:
run
openclaw configure --section web
. It stores the key in
~/.openclaw/openclaw.json
under
tools.web.search.apiKey
Environment alternative:
set
BRAVE_API_KEY
in the Gateway process
environment. For a gateway install, put it in
~/.openclaw/.env
(or your
service environment). See
Env vars
Using Perplexity (direct or via OpenRouter)
Perplexity Sonar models have built-in web search capabilities and return AI-synthesized
answers with citations. You can use them via OpenRouter (no credit card required - supports
crypto/prepaid).
Getting an OpenRouter API key
Create an account at
https://openrouter.ai/
Add credits (supports crypto, prepaid, or credit card)
Generate an API key in your account settings
Setting up Perplexity search
Copy
tools
web
search
enabled
true
provider
&quot;perplexity&quot;
perplexity
// API key (optional if OPENROUTER_API_KEY or PERPLEXITY_API_KEY is set)
apiKey
&quot;sk-or-v1-...&quot;
// Base URL (key-aware default if omitted)
baseUrl
&quot;https://openrouter.ai/api/v1&quot;
// Model (defaults to perplexity/sonar-pro)
model
&quot;perplexity/sonar-pro&quot;
Environment alternative:
set
OPENROUTER_API_KEY
PERPLEXITY_API_KEY
in the Gateway
environment. For a gateway install, put it in
~/.openclaw/.env
If no base URL is set, OpenClaw chooses a default based on the API key source:
PERPLEXITY_API_KEY
pplx-...
https://api.perplexity.ai
OPENROUTER_API_KEY
sk-or-...
https://openrouter.ai/api/v1
Unknown key formats → OpenRouter (safe fallback)
Available Perplexity models
Model
Description
Best for
perplexity/sonar
Fast Q&amp;A with web search
Quick lookups
perplexity/sonar-pro
(default)
Multi-step reasoning with web search
Complex questions
perplexity/sonar-reasoning-pro
Chain-of-thought analysis
Deep research
web_search
Search the web using your configured provider.
Requirements
tools.web.search.enabled
must not be
false
(default: enabled)
API key for your chosen provider:
Brave
BRAVE_API_KEY
tools.web.search.apiKey
Perplexity
OPENROUTER_API_KEY
PERPLEXITY_API_KEY
, or
tools.web.search.perplexity.apiKey
Config
Copy
tools
web
search
enabled
true
apiKey
&quot;BRAVE_API_KEY_HERE&quot;
// optional if BRAVE_API_KEY is set
maxResults
timeoutSeconds
cacheTtlMinutes
Tool parameters
query
(required)
count
(1–10; default from config)
country
(optional): 2-letter country code for region-specific results (e.g., “DE”, “US”, “ALL”). If omitted, Brave chooses its default region.
search_lang
(optional): ISO language code for search results (e.g., “de”, “en”, “fr”)
ui_lang
(optional): ISO language code for UI elements
freshness
(optional): filter by discovery time
Brave:
, or
YYYY-MM-DDtoYYYY-MM-DD
Perplexity:
Examples:
Copy
// German-specific search
await
web_search
query
&quot;TV online schauen&quot;
count
country
&quot;DE&quot;
search_lang
&quot;de&quot;
});
// French search with French UI
await
web_search
query
&quot;actualités&quot;
country
&quot;FR&quot;
search_lang
&quot;fr&quot;
ui_lang
&quot;fr&quot;
});
// Recent results (past week)
await
web_search
query
&quot;TMBG interview&quot;
freshness
&quot;pw&quot;
});
web_fetch
Fetch a URL and extract readable content.
web_fetch requirements
tools.web.fetch.enabled
must not be
false
(default: enabled)
Optional Firecrawl fallback: set
tools.web.fetch.firecrawl.apiKey
FIRECRAWL_API_KEY
web_fetch config
Copy
tools
web
fetch
enabled
true
maxChars
50000
maxCharsCap
50000
maxResponseBytes
2000000
timeoutSeconds
cacheTtlMinutes
maxRedirects
userAgent
&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36&quot;
readability
true
firecrawl
enabled
true
apiKey
&quot;FIRECRAWL_API_KEY_HERE&quot;
// optional if FIRECRAWL_API_KEY is set
baseUrl
&quot;https://api.firecrawl.dev&quot;
onlyMainContent
true
maxAgeMs
86400000
// ms (1 day)
timeoutSeconds
web_fetch tool parameters
url
(required, http/https only)
extractMode
markdown
text
maxChars
(truncate long pages)
Notes:
web_fetch
uses Readability (main-content extraction) first, then Firecrawl (if configured). If both fail, the tool returns an error.
Firecrawl requests use bot-circumvention mode and cache results by default.
web_fetch
sends a Chrome-like User-Agent and
Accept-Language
by default; override
userAgent
if needed.
web_fetch
blocks private/internal hostnames and re-checks redirects (limit with
maxRedirects
maxChars
is clamped to
tools.web.fetch.maxCharsCap
web_fetch
caps the downloaded response body size to
tools.web.fetch.maxResponseBytes
before parsing; oversized responses are truncated and include a warning.
web_fetch
is best-effort extraction; some sites will need the browser tool.
See
Firecrawl
for key setup and service details.
Responses are cached (default 15 minutes) to reduce repeated fetches.
If you use tool profiles/allowlists, add
web_search
web_fetch
group:web
If the Brave key is missing,
web_search
returns a short setup hint with a docs link.
Exec Tool
apply_patch Tool